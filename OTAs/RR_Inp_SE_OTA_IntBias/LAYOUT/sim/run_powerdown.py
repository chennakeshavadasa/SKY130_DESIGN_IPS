#!/usr/bin/env python3
"""
Power-down (EN = 0) verification, schematic vs PEX (full RC).

  pd      : enabled -> EN pulled low at 5 us -> 2 ms of power-down (Gear); VDD = 1.8 V,
            VICM = 0.9 V, unity gain.  IDD = average over 1.9-2.0 ms, node states at 2 ms.
            5 corners at 27 C, and tt at -40 / 85 / 125 C (leakage).
            (A plain DC operating point with EN = 0 is ill-conditioned: VOUT and several
            cascode/start-up nodes float, and the solver can return non-physical solutions.)
  en_tran : VDD = 1.8 V, EN 0 -> 1 at 20 us (wake-up), 1 -> 0 at 120 us (shut-down)
            Gear integration; tt / ss / ff
Writes sim/results_pd.json.
"""
import os
import json
import subprocess
import concurrent.futures as cf
import numpy as np
import run_sims as R

NODES = ["vstrp_out", "vstrp_ip", "net14", "vbp_top", "net8", "net9", "vbp_casc", "vbn_casc", "net15", "en_b"]
HEAD = """* {name}
.lib {lib} {corner}
.include {dut}
.temp {temp}
.option gmin=1e-18 reltol=1e-4
V3 GNDA 0 0
C1 Vout GNDA 10p
C2 mtb GNDA 1p
V2 VICM GNDA dc 0.9
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
"""
PD_OP = """.option method=gear maxord=2
V4 VDD GNDA dc 1.8
V5 EN GNDA pwl(0 1.8 5u 1.8 5.01u 0)
.control
 save all
 tran 50n 2m 0 2u
 meas tran idd AVG i(V4) from=1.9m to=2m
 meas tran vout FIND v(Vout) AT=2m
 meas tran mtb FIND v(mtb) AT=2m
{meas}
 echo "RESULT idd $&idd vout $&vout mtb $&mtb {probes}" > {out}
.endc
.end
"""
EN_TRAN = """.option method=gear maxord=2
V4 VDD GNDA dc 1.8
V5 EN GNDA pwl(0 0 20u 0 20.01u 1.8 120u 1.8 120.01u 0)
.control
 save all
 tran 20n 220u 0 50n
 set wr_singlescale
 wrdata {out} v(Vout) v(mtb) i(V4) v(x1.vstrp_out) v(EN)
.endc
.end
"""


def run(view, kind, corner, temp=27):
    d = os.path.join(R.SIM, view, "pd")
    os.makedirs(d, exist_ok=True)
    tag = f"{kind}_{corner}_{temp}"
    sp, out = os.path.join(d, tag + ".spice"), os.path.join(d, tag + ".dat")
    dut, sub = R.DUT[view]
    txt = HEAD.format(name=tag, lib=R.LIB, corner=corner, dut=dut, temp=temp, sub=sub)
    if kind == "op":
        meas = "\n".join(f" meas tran {n} FIND v(x1.{n}) AT=2m" for n in NODES)
        probes = " ".join(f"{n} $&{n}" for n in NODES)
        txt += PD_OP.format(out=out, probes=probes, meas=meas)
    else:
        txt += EN_TRAN.format(out=out)
    open(sp, "w").write(txt)
    if os.path.exists(out):
        os.remove(out)
    r = subprocess.run(["ngspice", "-b", sp], cwd=d, capture_output=True, text=True, timeout=3600)
    open(sp.replace(".spice", ".log"), "w").write(r.stdout + r.stderr)
    return out


def main():
    jobs = {}
    with cf.ThreadPoolExecutor(max_workers=14) as ex:
        for v in ("sch", "pex"):
            for c in R.CORNERS:
                jobs[(v, "op", c, 27)] = ex.submit(run, v, "op", c, 27)
            for t in (-40, 85, 125):
                jobs[(v, "op", "tt", t)] = ex.submit(run, v, "op", "tt", t)
            for c in ("tt", "ss", "ff"):
                jobs[(v, "tran", c, 27)] = ex.submit(run, v, "tran", c, 27)
        files = {k: f.result() for k, f in jobs.items()}
    res = {}
    for v in ("sch", "pex"):
        res[v] = {"op": {}, "tran": {}}
        for (vv, kind, c, t), p in files.items():
            if vv != v or kind != "op":
                continue
            s = open(p).read().split()
            d = {s[i]: float(s[i + 1]) for i in range(1, len(s) - 1, 2)}
            d["idd_nA"] = -d["idd"] * 1e9
            res[v]["op"][f"{c}_{t}"] = d
        for c in ("tt", "ss", "ff"):
            a = np.loadtxt(files[(v, "tran", c, 27)]).reshape(-1, 6)
            t, vo, mtb, idd, vso, en = a[:, 0], a[:, 1], a[:, 2], -a[:, 3], a[:, 4], a[:, 5]
            on = (t > 100e-6) & (t < 119e-6)
            mtb_on, idd_on = mtb[on].mean(), idd[on].mean()
            w = (t > 20e-6) & (t < 120e-6)
            tw, mw, iw, vw = t[w], mtb[w], idd[w], vo[w]
            def settle(x, tgt, tol):
                bad = np.where(np.abs(x - tgt) > tol)[0]
                return float(tw[bad[-1] + 1] - 20e-6) if len(bad) else 0.0
            off = t > 120e-6
            to, io = t[off], idd[off]
            below = np.where(io > 0.01 * idd_on)[0]
            res[v]["tran"][c] = {
                "t": t.tolist(), "vout": vo.tolist(), "mtb": mtb.tolist(), "idd": idd.tolist(),
                "vso": vso.tolist(), "en": en.tolist(),
                "idd_on_uA": float(idd_on * 1e6), "mtb_on": float(mtb_on),
                "t_wake_bias_us": settle(mw, mtb_on, 0.01 * mtb_on) * 1e6,
                "t_wake_idd_us": settle(iw, idd_on, 0.02 * idd_on) * 1e6,
                "t_wake_vout_us": settle(vw, vw[-1], 1e-3) * 1e6,
                "t_off_us": float((to[below[-1] + 1] if len(below) else to[0]) - 120e-6) * 1e6,
                "idd_off_end_nA": float(io[-200:].mean() * 1e9),
            }
    json.dump(res, open(os.path.join(R.SIM, "results_pd.json"), "w"))
    print("Power-down supply current (nA), 2 ms after EN -> 0:")
    for k in [f"{c}_27" for c in R.CORNERS] + ["tt_-40", "tt_85", "tt_125"]:
        print(f"  {k:8s} SCH {res['sch']['op'][k]['idd_nA']:9.4f}   PEX {res['pex']['op'][k]['idd_nA']:9.4f}"
              f"   VSTRP_OUT sch/pex {res['sch']['op'][k]['vstrp_out']:.3f}/{res['pex']['op'][k]['vstrp_out']:.3f}"
              f"   net15 {res['pex']['op'][k]['net15']:.3f}  MTB {res['pex']['op'][k]['mtb']:.4f}  Vout {res['pex']['op'][k]['vout']:.3f}")
    for c in ("tt", "ss", "ff"):
        for v in ("sch", "pex"):
            r = res[v]["tran"][c]
            print(f"  EN toggle {c} {v}: IDD on {r['idd_on_uA']:.2f} uA, bias wake {r['t_wake_bias_us']:.2f} us,"
                  f" IDD wake {r['t_wake_idd_us']:.2f} us, Vout settle {r['t_wake_vout_us']:.2f} us,"
                  f" off <1% in {r['t_off_us']:.2f} us, IDD end {r['idd_off_end_nA']:.2f} nA")


if __name__ == "__main__":
    main()
