#!/usr/bin/env python3
"""Parasitic summary of the extracted layout with layout nets mapped to schematic names.

Mapping is derived from device connectivity in the C-only extraction:
  PMOS pair (pfet_lvt): common source -> net7, VINP-side drain -> net1, VINN-side -> net2
  NMOS pair (nfet_lvt): common source -> net6, VINP-side drain -> net3, VINN-side -> net4
  MP_TOP (pfet W2/L2, S=VDD, D in {net3,net4}) gate -> net5
Total C = sum of all extracted capacitors touching the net (to substrate and coupling).
Wire R = series resistance between the two most distant terminals is not computed; instead
the summed extracted resistance per net from the RC netlist is reported as an upper bound.
"""
import os
import re
import json
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
CX = os.path.join(ROOT, "pex", f"{CELL}_cx.spice")
RCX = os.path.join(ROOT, "pex", f"{CELL}_rcx.spice")
UNIT = {"f": 1e-15, "p": 1e-12, "a": 1e-18, "n": 1e-9, "": 1.0}


def val(s):
    m = re.match(r"([-\d.eE+]+)([fpan]?)", s)
    return float(m.group(1)) * UNIT[m.group(2)]


devs, caps = [], []
for l in open(CX):
    p = l.split()
    if not p:
        continue
    if p[0].startswith("X"):
        model = [t for t in p if t.startswith("sky130_fd_pr")][0]
        i = p.index(model)
        prm = dict(t.split("=") for t in p[i + 1:] if "=" in t)
        if "fet" in model:
            devs.append((p[1:i], model, prm))
    elif p[0].startswith("C"):
        caps.append((p[1], p[2], val(p[3])))

name = {}
for model, gnd in (("sky130_fd_pr__pfet_01v8_lvt", ("net7", "net1", "net2")),
                   ("sky130_fd_pr__nfet_01v8_lvt", ("net6", "net3", "net4"))):
    sd = collections.defaultdict(set)
    for (d, g, s, b), m, _ in devs:
        if m == model:
            sd[g] |= {d, s}
    common = (sd["VINP"] & sd["VINN"]).pop()
    name[common] = gnd[0]
    name[(sd["VINP"] - {common}).pop()] = gnd[1]
    name[(sd["VINN"] - {common}).pop()] = gnd[2]
inv = {v: k for k, v in name.items()}
for (d, g, s, b), m, prm in devs:
    if m == "sky130_fd_pr__pfet_01v8" and prm.get("w") == "2" and prm.get("l") == "2":
        if {d, s} & {inv["net3"], inv["net4"]} and "VDD" in (d, s):
            name[g] = "net5"
for k in ("VOUT", "VINP", "VINN", "MN_TAIL_BIAS", "EN", "VDD", "GNDA"):
    name[k] = k
inv = {v: k for k, v in name.items()}

ctot = collections.Counter()
cgnd = collections.Counter()
for a, b, c in caps:
    for n in (a, b):
        ctot[n] += c
    if "GNDA" in (a, b) or "VSUBS" in (a, b):
        for n in (a, b):
            cgnd[n] += c
rsum = collections.Counter()
nres = collections.Counter()
for l in open(RCX):
    if l.startswith("R"):
        p = l.split()
        net = p[1].split(".")[0]
        net = net + "#" if net.startswith("a_") else net
        rsum[net] += float(p[3])
        nres[net] += 1

rows = []
for n in ("VINP", "VINN", "net1", "net2", "net3", "net4", "net5", "VOUT", "net6", "net7", "MN_TAIL_BIAS", "EN"):
    ln = inv.get(n, n)
    rows.append((n, ln, ctot[ln] * 1e15, nres[ln]))
out = {"rows": rows, "pairs": {}}
for a, b in (("VINP", "VINN"), ("net1", "net2"), ("net3", "net4")):
    ca = ctot[inv.get(a, a)]
    cb = ctot[inv.get(b, b)]
    out["pairs"][f"{a}/{b}"] = (ca * 1e15, cb * 1e15, 100 * (cb - ca) / ((ca + cb) / 2))
json.dump(out, open(os.path.join(ROOT, "sim", "parasitics.json"), "w"), indent=1)
print(f"{'net':14s} {'layout name':16s} {'C_total (fF)':>12s} {'#R segs':>8s}")
for r in rows:
    print(f"{r[0]:14s} {r[1]:16s} {r[2]:12.2f} {r[3]:8d}")
print("matched-net capacitance symmetry:")
for k, (a, b, d) in out["pairs"].items():
    print(f"  {k:10s} {a:7.2f} fF vs {b:7.2f} fF  (diff {d:+.1f} %)")
print("total extracted caps:", len(caps), " total C:", f"{sum(c for *_, c in caps) * 1e12:.3f} pF")
