#!/usr/bin/env python3
"""
Four-view comparison to separate where the post-layout deltas come from:

  sch  : schematic netlist (pre-layout)
  lay  : extracted layout, devices only (magic `ext2spice lvs`: real per-finger AD/AS/PD/PS,
         no wiring R or C)                                   -> device-geometry effect
  pexc : extracted layout + parasitic capacitance only (standard magic C + coupling extraction)
  pexr0: full-RC netlist with all wiring R shorted (keeps extresist's capacitance)
  pex  : extracted layout + full RC (magic extresist)

sch and pex results come from run_sims.py (results.json). This script simulates lay and
pexc with the same decks and writes sim/results_views.json with all four views.
"""
import os
import json
import concurrent.futures as cf
import run_sims as R

CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
R.DUT["lay"] = (os.path.join(R.ROOT, "mag", f"{CELL}.lvs.spice"), CELL)
R.DUT["pexc"] = (os.path.join(R.ROOT, "pex", f"{CELL}_cx.spice"), CELL)
# full-RC netlist with every wiring resistor shorted (1 mOhm): same capacitance as the RC
# netlist, no R  -> separates the effect of R from the extra substrate C that extresist adds
_src = os.path.join(R.ROOT, "pex", f"{CELL}_rcx.spice")
_dst = os.path.join(R.ROOT, "pex", f"{CELL}_rcx_R0.spice")
with open(_dst, "w") as fo:
    for l in open(_src):
        if l.startswith("R"):
            p = l.split()
            if p[1].split(".")[0] == p[2].split(".")[0]:
                p[3] = "1m"
                l = " ".join(p) + "\n"
        fo.write(l)
R.DUT["pexr0"] = (_dst, CELL)
TBS = ("stb", "dc", "psrr", "tran", "op")
VIEWS = ("lay", "pexc", "pexr0")


def main():
    with cf.ThreadPoolExecutor(max_workers=14) as ex:
        jobs = {(v, c, tb): ex.submit(R.write_and_run, v, tb, c)
                for v in VIEWS for c in R.CORNERS for tb in TBS}
        files = {k: f.result() for k, f in jobs.items()}
    base = json.load(open(os.path.join(R.SIM, "results.json")))
    out = {"sch": {c: base["sch"][c] for c in R.CORNERS}, "pex": {c: base["pex"][c] for c in R.CORNERS}}
    for v in VIEWS:
        out[v] = {c: R.analyse(v, c, {tb: files[(v, c, tb)] for tb in TBS}) for c in R.CORNERS}
    json.dump(out, open(os.path.join(R.SIM, "results_views.json"), "w"))
    keys = ["A0_dB", "UGF_MHz", "PM_deg", "off_0p9_mV", "PSRR_10Hz_dB", "PSRR_1MHz_dB",
            "tran_offpk_mV", "IDD_uA"]
    for k in keys:
        print(f"{k:14s} " + "  ".join(f"{v}:{out[v]['tt'][k]:8.3f}" for v in ("sch", "lay", "pexc", "pexr0", "pex")))


if __name__ == "__main__":
    main()
