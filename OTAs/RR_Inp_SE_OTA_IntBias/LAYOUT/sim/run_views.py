#!/usr/bin/env python3
"""
Four-view comparison to separate where the post-layout deltas come from:

  sch  : schematic netlist (pre-layout)
  lay  : extracted layout, devices only (magic `ext2spice lvs`: real per-finger AD/AS/PD/PS,
         no wiring R or C)                                   -> device-geometry effect
  pexc : extracted layout + parasitic capacitance only (magic C/coupling extraction)
  pex  : extracted layout + full RC (magic extresist)        -> final post-layout view

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
TBS = ("stb", "dc", "psrr", "tran", "op")
VIEWS = ("lay", "pexc")


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
        print(f"{k:14s} " + "  ".join(f"{v}:{out[v]['tt'][k]:8.3f}" for v in ("sch", "lay", "pexc", "pex")))


if __name__ == "__main__":
    main()
