#!/usr/bin/env python3
"""
Pre- vs post-layout verification for Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.

DUT variants
  sch : xschem simulation netlist of the (untouched) schematic (sim/dut_sch.spice)
  pex : magic RC-extracted layout (pex/<cell>_rcx.spice)

Testbenches (same as the original IP testbenches, 10 pF load, VDD=1.8 V, 27 C)
  stb  : Middlebrook loop gain in unity-gain feedback  -> A0, UGF, PM
  dc   : unity-gain Vout-VICM vs VICM 0..1.8 V          -> offset
  psrr : Vout/VDD (ac) in unity gain                    -> PSRR @10 Hz, 1 MHz
  tran : 1 kHz 0.25..1.55 V sine in unity gain          -> dynamic offset
  op   : supply current, tail-bias node
  start: VDD/EN ramp 0->1.8 V in 10 us, 2 ms                    -> bias start-up check
  mc   : tt_mm mismatch Monte Carlo, one process per run -> offset sigma
"""
import os
import sys
import json
import subprocess
import concurrent.futures as cf
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM = os.path.join(ROOT, "sim")
LIB = os.path.join(os.environ.get("PDK_ROOT", os.path.expanduser("~/.ciel")), "sky130A/libs.tech/combined/sky130.lib.spice")
DUT = {
    "sch": (os.path.join(ROOT, "sim", "dut_sch.spice"), "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"),
    "pex": (os.path.join(ROOT, "pex", "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice"), "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"),
}
CORNERS = ["tt", "ss", "ff", "fs", "sf"]

COMMON = """\
.lib {lib} {corner}
.include {dut}
.temp 27
.option gmin=1e-18 reltol=1e-4
V3 GNDA 0 0
V5 EN GNDA 1.8
C1 Vout GNDA 10p
C2 mtb GNDA 1p
"""

TB = {}
TB["stb"] = """\
V4 VDD GNDA dc 1.8
V2 VICM GNDA dc 0.9
Vprobe1 probe Vout dc 0 ac 1
Vprobe2 probe vfb 0
Iprobe1 0 probe dc 0 ac 0
X1 VDD EN vfb Vout VICM mtb GNDA {sub}
.control
 save all
 alter @Vprobe1[acmag]=1
 alter @Iprobe1[acmag]=0
 ac dec 40 1 1e9
 alter @Vprobe1[acmag]=0
 alter @Iprobe1[acmag]=1
 ac dec 40 1 1e9
 let ip22 = ac2.i(Vprobe2)
 let vprb1 = ac1.probe
 let tl = 1/(vprb1+ip22)-1
 set wr_singlescale
 wrdata {out} real(tl) imag(tl)
.endc
.end
"""
TB["dc"] = """\
V4 VDD GNDA dc 1.8
V2 VICM GNDA dc 0.9
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 dc V2 0 1.8 5m
 set wr_singlescale
 wrdata {out} v(Vout)
.endc
.end
"""
TB["psrr"] = """\
V4 VDD GNDA dc 1.8 ac 1
V2 VICM GNDA dc 0.9
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 ac dec 20 1 1e9
 set wr_singlescale
 wrdata {out} vm(Vout)
.endc
.end
"""
TB["tran"] = """\
V4 VDD GNDA dc 1.8
V2 VICM GNDA dc 0.9 sin(0.9 0.65 1k)
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 tran 2u 4m 0 2u
 set wr_singlescale
 wrdata {out} v(Vout) v(VICM)
.endc
.end
"""
TB["op"] = """\
V4 VDD GNDA dc 1.8
V2 VICM GNDA dc 0.9
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 op
 echo "RESULT idd $&i(V4) vout $&v(Vout) mtb $&v(mtb)" > {out}
.endc
.end
"""
TB["start"] = """\
.option method=gear maxord=2
V4 VDD GNDA pwl(0 0 10u 1.8)
V2 VICM GNDA pwl(0 0 10u 0.9)
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 tran 50n 2m 0 1u
 set wr_singlescale
 wrdata {out} v(Vout) v(mtb) i(V4)
.endc
.end
"""
TB["mc"] = """\
.options seed={seed}
V4 VDD GNDA dc 1.8
V2 VICM GNDA dc 0.9
X1 VDD EN Vout Vout VICM mtb GNDA {sub}
.control
 save all
 op
 echo "RESULT $&v(Vout)" > {out}
.endc
.end
"""
# the original EN input of TB: V5 EN = 1.8 (enabled); start uses EN tied to the ramping VDD
START_EN = "V5 EN GNDA pwl(0 0 10u 1.8)\n"


def write_and_run(mode, tb, corner, seed=None):
    d = os.path.join(SIM, mode, tb)
    os.makedirs(d, exist_ok=True)
    tag = corner if seed is None else f"{corner}_{seed:04d}"
    sp = os.path.join(d, f"{tb}_{tag}.spice")
    out = os.path.join(d, f"{tb}_{tag}.dat")
    dut, sub = DUT[mode]
    txt = f"* {tb} {mode} {tag}\n" + COMMON.format(lib=LIB, corner=corner, dut=dut)
    if tb == "start":
        txt = txt.replace("V5 EN GNDA 1.8\n", START_EN)
    txt += TB[tb].format(sub=sub, out=out, seed=seed if seed is not None else 1)
    open(sp, "w").write(txt)
    if os.path.exists(out):
        os.remove(out)
    r = subprocess.run(["ngspice", "-b", sp], cwd=d, capture_output=True, text=True, timeout=1800)
    open(sp.replace(".spice", ".log"), "w").write(r.stdout + r.stderr)
    return out


def load(path, ncol):
    a = np.loadtxt(path)
    return a.reshape(-1, ncol)


def analyse(mode, corner, files):
    res = {}
    # STB
    a = load(files["stb"], 3)
    f, t = a[:, 0], a[:, 1] + 1j * a[:, 2]
    mag = 20 * np.log10(np.abs(t))
    ph = np.unwrap(np.angle(t)) * 180 / np.pi
    res["A0_dB"] = float(mag[0])
    i = np.where((mag[:-1] > 0) & (mag[1:] <= 0))[0][0]
    fr = mag[i] / (mag[i] - mag[i + 1])
    ugf = 10 ** (np.log10(f[i]) + fr * (np.log10(f[i + 1]) - np.log10(f[i])))
    phu = ph[i] + fr * (ph[i + 1] - ph[i])
    res["UGF_MHz"] = float(ugf / 1e6)
    res["PM_deg"] = float(180 + (phu - ph[0]))      # phase lag relative to DC
    res["stb_curve"] = (f.tolist(), mag.tolist(), (ph - ph[0]).tolist())
    # DC
    a = load(files["dc"], 2)
    vin, vout = a[:, 0], a[:, 1]
    off = (vout - vin) * 1e3
    res["off_0p9_mV"] = float(np.interp(0.9, vin, off))
    m = (vin >= 0.2) & (vin <= 1.6)
    res["off_max_0p2_1p6_mV"] = float(np.max(np.abs(off[m])))
    res["dc_curve"] = (vin.tolist(), off.tolist())
    # PSRR
    a = load(files["psrr"], 2)
    fp, vm = a[:, 0], a[:, 1]
    db = 20 * np.log10(vm)
    res["PSRR_10Hz_dB"] = float(np.interp(1, np.log10(fp), db))
    res["PSRR_1MHz_dB"] = float(np.interp(6, np.log10(fp), db))
    res["psrr_curve"] = (fp.tolist(), db.tolist())
    # TRAN
    a = load(files["tran"], 3)
    tt, vo, vi = a[:, 0], a[:, 1], a[:, 2]
    m = tt > 1e-3
    doff = (vo - vi)[m] * 1e3
    res["tran_offpk_mV"] = float(np.max(np.abs(doff)))
    res["tran_curve"] = (tt[m].tolist(), doff.tolist())
    # OP
    s = open(files["op"]).read().split()
    res["IDD_uA"] = float(-float(s[s.index("idd") + 1]) * 1e6)
    res["V_MN_TAIL_BIAS"] = float(s[s.index("mtb") + 1])
    return res


def main():
    nmc = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    jobs = {}
    with cf.ThreadPoolExecutor(max_workers=14) as ex:
        for mode in DUT:
            for c in CORNERS:
                for tb in ("stb", "dc", "psrr", "tran", "op"):
                    jobs[(mode, c, tb)] = ex.submit(write_and_run, mode, tb, c)
            for c in ("tt", "ss", "ff"):
                jobs[(mode, c, "start")] = ex.submit(write_and_run, mode, "start", c)
            for k in range(nmc):
                jobs[(mode, "tt_mm", "mc", k)] = ex.submit(write_and_run, mode, "mc", "tt_mm", k + 1)
        files = {k: v.result() for k, v in jobs.items()}
    out = {}
    for mode in DUT:
        out[mode] = {}
        for c in CORNERS:
            fs = {tb: files[(mode, c, tb)] for tb in ("stb", "dc", "psrr", "tran", "op")}
            out[mode][c] = analyse(mode, c, fs)
        st = {}
        for c in ("tt", "ss", "ff"):
            a = load(files[(mode, c, "start")], 4)
            t, vo, mtb, idd = a[:, 0], a[:, 1], a[:, 2], -a[:, 3]
            m = t > 0.9 * t[-1]
            st[c] = {"t": t.tolist(), "vout": vo.tolist(), "mtb": mtb.tolist(), "idd": idd.tolist(),
                     "idd_final_uA": float(np.mean(idd[m]) * 1e6), "vout_final": float(vo[-1]),
                     "mtb_final": float(mtb[-1]),
                     "t_settle_us": float(t[np.where(np.abs(vo - vo[-1]) > 1e-3)[0][-1] + 1] * 1e6)}
        out[mode]["start"] = st
        mc = []
        for k in range(nmc):
            p = files[(mode, "tt_mm", "mc", k)]
            try:
                s = open(p).read().split()
                mc.append((float(s[1]) - 0.9) * 1e3)
            except Exception:
                pass
        out[mode]["mc"] = mc
    json.dump(out, open(os.path.join(SIM, "results.json"), "w"))
    # summary
    keys = ["A0_dB", "UGF_MHz", "PM_deg", "off_0p9_mV", "off_max_0p2_1p6_mV", "PSRR_10Hz_dB",
            "PSRR_1MHz_dB", "tran_offpk_mV", "IDD_uA", "V_MN_TAIL_BIAS"]
    for k in keys:
        row = "  ".join(f"{c}:{out['sch'][c][k]:8.3f}/{out['pex'][c][k]:8.3f}" for c in CORNERS)
        print(f"{k:20s} {row}")
    for mode in DUT:
        a = np.array(out[mode]["mc"])
        print(f"MC {mode}: N={len(a)} mean={a.mean():.3f} mV sigma={a.std(ddof=1):.3f} mV")
        for c in ("tt", "ss", "ff"):
            print(f"  start {c}: IDD={out[mode]['start'][c]['idd_final_uA']:.2f} uA "
                  f"Vout={out[mode]['start'][c]['vout_final']:.4f} V")


if __name__ == "__main__":
    main()
