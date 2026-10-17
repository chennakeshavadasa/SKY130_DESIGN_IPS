#!/usr/bin/env python3
"""Probe the internal start-up nodes (post-layout, labelled nets) during the 10 us supply ramp."""
import os, json, subprocess, numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
LIB = os.path.join(os.environ.get("PDK_ROOT", os.path.expanduser("~/.ciel")), "sky130A/libs.tech/combined/sky130.lib.spice")
d = os.path.join(ROOT, "sim", "pex", "start_probe"); os.makedirs(d, exist_ok=True)
nodes = ["vstrp_ip", "net14", "vstrp_out", "en_b", "vbp_top"]
deck = f"""* start-up internals (post-layout, tt)
.lib {LIB} tt
.include {ROOT}/pex/{CELL}_rcx.spice
.option gmin=1e-18 reltol=1e-4 method=gear maxord=2
V3 GNDA 0 0
C1 Vout GNDA 10p
C2 mtb GNDA 1p
X1 VDD EN Vout Vout VICM mtb GNDA {CELL}
V4 VDD GNDA pwl(0 0 10u 1.8)
V5 EN GNDA pwl(0 0 10u 1.8)
V2 VICM GNDA pwl(0 0 10u 0.9)
.control
 save all
 tran 20n 40u 0 20n
 set wr_singlescale
 wrdata {d}/probe.dat v(VDD) {' '.join(f'v(x1.{n})' for n in nodes)} v(mtb) v(Vout)
.endc
.end
"""
open(f"{d}/probe.spice", "w").write(deck)
subprocess.run(["ngspice", "-b", "probe.spice"], cwd=d, capture_output=True)
a = np.loadtxt(f"{d}/probe.dat")
cols = ["VDD", "VSTRP_IP", "net14", "VSTRP_OUT", "EN_B", "VBP_TOP", "MN_TAIL_BIAS", "VOUT"]
rows = []
for tt in (2, 4, 6, 8, 10, 12, 15, 20, 40):
    k = min(np.searchsorted(a[:, 0], tt * 1e-6), len(a) - 1)
    rows.append([tt] + [float(x) for x in a[k, 1:]])
json.dump({"cols": cols, "rows": rows}, open(os.path.join(ROOT, "sim", "startup_probe.json"), "w"))
for r in rows: print(r[0], " ".join(f"{c}={v:.3f}" for c, v in zip(cols, r[1:])))
