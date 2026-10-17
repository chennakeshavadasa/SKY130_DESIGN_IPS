#!/usr/bin/env python3
"""Which net's wiring resistance costs phase margin?
For every net with extracted resistance, short that net's resistors (1 mOhm) in the full-RC
netlist, rerun the tt loop-gain (STB) testbench, and compare UGF/PM with the unmodified RC
netlist and with all resistors shorted.  Writes sim/r_attribution.json."""
import os
import re
import json
import collections
import concurrent.futures as cf
import numpy as np
import run_sims as R

CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
SRC = os.path.join(R.ROOT, "pex", f"{CELL}_rcx.spice")
D = os.path.join(R.SIM, "rattr")
os.makedirs(D, exist_ok=True)
lines = open(SRC).read().splitlines()
sumr = collections.Counter()
for l in lines:
    if l.startswith("R"):
        p = l.split()
        if p[1].split(".")[0] == p[2].split(".")[0]:
            sumr[p[1].split(".")[0]] += float(p[3])
nets = [n for n, v in sumr.items() if v > 300]


def variant(tag, short):
    out = []
    for l in lines:
        if l.startswith("R"):
            p = l.split()
            n1, n2 = p[1].split(".")[0], p[2].split(".")[0]
            if n1 == n2 and (short == "ALL" or n1 in short):
                p[3] = "1m"
                l = " ".join(p)
        out.append(l)
    path = os.path.join(D, f"rcx_{tag}.spice")
    open(path, "w").write("\n".join(out) + "\n")
    R.DUT[f"r_{tag}"] = (path, CELL)
    return f"r_{tag}"


def stb(view):
    p = R.write_and_run(view, "stb", "tt")
    a = R.load(p, 3)
    f, t = a[:, 0], a[:, 1] + 1j * a[:, 2]
    m = 20 * np.log10(np.abs(t))
    ph = np.unwrap(np.angle(t)) * 180 / np.pi
    i = np.where((m[:-1] > 0) & (m[1:] <= 0))[0][0]
    fr = m[i] / (m[i] - m[i + 1])
    ugf = 10 ** (np.log10(f[i]) + fr * (np.log10(f[i + 1]) - np.log10(f[i])))
    return float(ugf / 1e6), float(180 + (ph[i] + fr * (ph[i + 1] - ph[i]) - ph[0]))


views = {"full_RC": variant("full", []), "all_R_shorted": variant("allshort", "ALL")}
for n in nets:
    views[n] = variant(re.sub(r"[^A-Za-z0-9_]", "_", n), [n])
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    res = dict(zip(views, ex.map(stb, views.values())))
base_u, base_p = res["full_RC"]
out = {"full_RC": res["full_RC"], "all_R_shorted": res["all_R_shorted"],
       "per_net": sorted(((n, sumr[n], res[n][0] - base_u, res[n][1] - base_p) for n in nets),
                         key=lambda r: -r[3])}
json.dump(out, open(os.path.join(R.SIM, "r_attribution.json"), "w"), indent=1)
print(f"full RC: UGF {base_u:.4f} MHz, PM {base_p:.3f} deg;  all R shorted: UGF {res['all_R_shorted'][0]:.4f}, "
      f"PM {res['all_R_shorted'][1]:.3f}")
print(f"{'net (R shorted)':16s} {'sum R (ohm)':>11s} {'dUGF (kHz)':>10s} {'dPM (deg)':>9s}")
for n, s, du, dp in out["per_net"]:
    print(f"{n:16s} {s:11.0f} {du * 1e3:10.2f} {dp:9.3f}")
