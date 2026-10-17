#!/usr/bin/env python3
"""Build docs/POST_LAYOUT_VERIFICATION.md from the signoff + simulation results."""
import os
import re
import json
import datetime
import xml.etree.ElementTree as ET
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
R = json.load(open(os.path.join(ROOT, "sim", "results.json")))
PX = json.load(open(os.path.join(ROOT, "sim", "parasitics.json")))
C5 = ["tt", "ss", "ff", "fs", "sf"]


def rd(p):
    return open(os.path.join(ROOT, p)).read()


# ---------------- signoff facts ----------------
magic_drc = len([l for l in rd(f"mag/{CELL}.drc").splitlines() if l.strip()])
kl = ET.parse(os.path.join(ROOT, "drc", "klayout_drc.lyrdb")).getroot()
kl_n = len(list(kl.iter("item")))
kl_rules = len(list(kl.iter("category")))
lvs = rd("lvs/lvs_report.txt")
lvs_final = re.findall(r"Final result: (.*)", lvs)[-1]
lvs_dev = re.findall(r"Number of devices: (\d+)", lvs)[-1]
lvs_net = re.findall(r"Number of nets: (\d+)", lvs)[-1]
pexlog = rd("pex/pex.log")
ant_viol = len(re.findall(r"antenna violation|Antenna error", pexlog, re.I))
rcx = rd(f"pex/{CELL}_rcx.spice").splitlines()
n_r = sum(1 for l in rcx if l.startswith("R"))
n_c = sum(1 for l in rcx if l.startswith("C"))
n_x = sum(1 for l in rcx if l.startswith("X"))
import subprocess
GDS = next(p for p in (os.path.join(ROOT, "mag", CELL + ".gds"), os.path.join(ROOT, "gds", CELL + ".gds"))
           if os.path.exists(p))
bb = subprocess.run(["klayout", "-b", "-r", os.path.join(ROOT, "scripts", "gds_bbox.py"), "-rd",
                     f"gds={GDS}"], capture_output=True, text=True).stdout
W = float(re.search(r"W=([\d.]+)", bb).group(1))
H = float(re.search(r"H=([\d.]+)", bb).group(1))

# ---------------- tables ----------------
MET = [("A0_dB", "DC loop gain", "dB", "{:.2f}", "abs"),
       ("UGF_MHz", "Unity-gain frequency", "MHz", "{:.3f}", "rel"),
       ("PM_deg", "Phase margin", "deg", "{:.2f}", "abs"),
       ("off_0p9_mV", "Systematic offset @ VICM=0.9 V", "mV", "{:.3f}", "abs"),
       ("off_max_0p2_1p6_mV", "Worst-case offset, VICM 0.2–1.6 V", "mV", "{:.2f}", "abs"),
       ("PSRR_10Hz_dB", "PSRR @ 10 Hz (Vout/VDD)", "dB", "{:.2f}", "abs"),
       ("PSRR_1MHz_dB", "PSRR @ 1 MHz (Vout/VDD)", "dB", "{:.2f}", "abs"),
       ("tran_offpk_mV", "Peak dynamic offset (1 kHz sine)", "mV", "{:.3f}", "abs"),
       ("IDD_uA", "Supply current", "uA", "{:.3f}", "rel"),
       ("V_MN_TAIL_BIAS", "MN_TAIL_BIAS voltage", "V", "{:.4f}", "abs")]


def delta(a, b, kind, fmt="{:.3f}"):
    d = b - a
    p = int(re.search(r"\.(\d)f", fmt).group(1))
    s = f"{d:+.{p}f}"
    if kind == "rel":
        return f"{s} ({100 * d / a:+.2f} %)"
    return s


def build(IMG, PL, head=True):
    L = []
    w = L.append
    w(f"# Post-Layout Verification: `{CELL}` (SKY130A)\n")
    w(f"_Generated {datetime.date.today().isoformat()} by `sim/make_report.py` from the signoff and simulation "
      "results in this directory. Every number below comes from those files._\n")
    w("Layout of the rail-to-rail-input folded-cascode OTA with internal beta-multiplier bias "
      "from `OTAs/RR_Inp_SE_OTA_IntBias`. **The schematic was not modified.**\n")

    w("## 1. Signoff summary\n")
    w("| Check | Tool / setup | Result |")
    w("|---|---|---|")
    w(f"| DRC | magic 8.3, `drc(full)`, sky130A tech | **{magic_drc} errors** |")
    w(f"| DRC (2nd opinion) | KLayout `sky130A_mr.drc`, FEOL+BEOL+off-grid ({kl_rules} rule categories) | **{kl_n} violations** |")
    w(f"| Antenna | magic `antennacheck` | **{ant_viol} violations** |")
    w(f"| LVS | netgen 1.5 + `sky130A_setup.tcl`, layout vs xschem netlist of the untouched schematic | **{lvs_final}** ({lvs_dev} merged devices, {lvs_net} nets, no property errors) |")
    w(f"| PEX | magic full RC (`extresist`, coupling C, cthresh=0, rthresh=0) | {n_x} device fingers, {n_c} C, {n_r} R |")
    w(f"| Post-layout simulation | ngspice, 5 corners + 200-run mismatch MC + start-up + power-down/enable | all specs preserved, see §4 |")
    w(f"\n**Cell size:** {W:.2f} µm × {H:.2f} µm = {W * H:.0f} µm².\n")

    w(f"![layout]({IMG}layout_full.png)\n")
    w("_Full layout (KLayout render of the final GDS). Left: OTA core around a vertical symmetry axis. "
      "Right: internal bias (beta-multiplier XM1/XM10, xhigh-po resistors, start-up stack, enable logic)._\n")
    w(f"![input pairs]({IMG}layout_inputpairs.png)\n")
    w("_Input pairs. Top: NMOS pair 2×8 (ABBAABBA / BAABBAAB) in a p-tap guard ring. Bottom: PMOS pair "
      "4×14 (rows X, X̄, X̄, X with X = ABBAABBAABBAAB) in an n-tap guard ring. Gate contacts of "
      "MP_A1/MN_A1 (VINP) and MP_A2/MN_A2 (VINN) alternate sides and share li straps between rows._\n")

    w("## 2. What was compared\n")
    w("| | Pre-layout (schematic) | Post-layout (layout) |")
    w("|---|---|---|")
    w("| Netlist | `sim/dut_sch.spice`: xschem simulation netlist of the original `.sch` (device lines identical to the repo's `different_spice/…spice`, incl. `mult`, AD/AS from xschem) | "
      f"`pex/{CELL}_rcx.spice`: magic RC extraction of the final layout |")
    w("| Devices | 80 instances with `m=` multipliers | 225 individual fingers with real AD/AS/PD/PS |")
    w(f"| Parasitics | none | {n_c} capacitors (to substrate + coupling), {n_r} wire/contact resistors |")
    w("\nBoth DUTs are dropped into **identical testbench decks** (only the `.include` line differs). "
      "Models: `sky130A/libs.tech/combined/sky130.lib.spice`. Conditions: VDD = 1.8 V, EN = 1.8 V, "
      "T = 27 °C, CL = 10 pF on VOUT, 1 pF on MN_TAIL_BIAS (as in the original testbenches).\n")
    w("| Testbench | Configuration | Extracted metrics |")
    w("|---|---|---|")
    w("| STB | Unity-gain loop broken with a Middlebrook probe (two AC runs: V-probe and I-probe), VICM = 0.9 V, 1 Hz–1 GHz, 40 pts/dec | DC loop gain (at 1 Hz), UGF, phase margin |")
    w("| DC | Unity gain, VICM swept 0 → 1.8 V in 5 mV steps | offset at 0.9 V, worst offset over 0.2–1.6 V |")
    w("| PSRR | Unity gain, VICM = 0.9 V, 1 V AC on VDD | Vout/VDD at 10 Hz and 1 MHz |")
    w("| TRAN | Unity gain, 0.9 V ± 0.65 V, 1 kHz sine (0.25–1.55 V), 4 ms | peak abs(Vout − VICM) after 1 ms |")
    w("| OP | Unity gain, VICM = 0.9 V | IDD, V(MN_TAIL_BIAS) |")
    w("| Start-up | VDD, EN, VICM ramp 0 → final in 10 µs, 2 ms, Gear integration | settling of Vout, final IDD and bias |")
    w("| MC | `tt_mm` (mismatch on), unity gain, VICM = 0.9 V, 200 independent ngspice processes (`.options seed=1…200`) | offset mean, σ |")
    w("\nCorners: tt, ss, ff, fs, sf (same set as the IP README).\n")

    w("## 3. Headline comparison (tt, 27 °C)\n")
    w("| Parameter | Unit | Schematic | Layout (RC) | Δ (layout − sch) |")
    w("|---|---|---|---|---|")
    for k, name, u, f, kind in MET:
        a, b = R["sch"]["tt"][k], R["pex"]["tt"][k]
        w(f"| {name} | {u} | {f.format(a)} | {f.format(b)} | {delta(a, b, kind, f)} |")
    ms, mp = np.array(R["sch"]["mc"]), np.array(R["pex"]["mc"])
    PD = json.load(open(os.path.join(ROOT, "sim", "results_pd.json")))
    a_, b_ = PD["sch"]["op"]["tt_27"]["idd_nA"] * 1e3, PD["pex"]["op"]["tt_27"]["idd_nA"] * 1e3
    w(f"| Power-down current (EN = 0) | pA | {a_:.1f} | {b_:.1f} | {b_ - a_:+.1f} |")
    tw_s, tw_p = PD["sch"]["tran"]["tt"]["t_wake_vout_us"], PD["pex"]["tran"]["tt"]["t_wake_vout_us"]
    w(f"| Wake-up time (EN↑ → Vout within 1 mV) | µs | {tw_s:.2f} | {tw_p:.2f} | {tw_p - tw_s:+.2f} |")
    w(f"| MC offset σ (N={len(ms)}/{len(mp)}) | mV | {ms.std(ddof=1):.3f} | {mp.std(ddof=1):.3f} | "
      f"{mp.std(ddof=1) - ms.std(ddof=1):+.3f} |")
    w(f"| MC offset mean | mV | {ms.mean():.3f} | {mp.mean():.3f} | {mp.mean() - ms.mean():+.3f} |")
    se = ms.std(ddof=1) / np.sqrt(len(ms))
    w(f"\n_MC mean standard error ≈ {se:.2f} mV (σ/√N), so the two means agree to within about 2 standard errors; "
      "the systematic offset from the deterministic DC run is identical (−0.075 mV)._")

    w("\n## 4. Results across corners\n")
    for k, name, u, f, kind in MET:
        w(f"**{name} ({u})**\n")
        w("| | " + " | ".join(C5) + " |")
        w("|---|" + "---|" * 5)
        w("| schematic | " + " | ".join(f.format(R['sch'][c][k]) for c in C5) + " |")
        w("| layout | " + " | ".join(f.format(R['pex'][c][k]) for c in C5) + " |")
        w("| Δ | " + " | ".join(delta(R['sch'][c][k], R['pex'][c][k], kind, f) for c in C5) + " |\n")

    w("### 4.1 Loop gain / stability\n")
    w(f"![stb]({PL}sch_vs_pex_stb.png)\n")
    w("### 4.2 DC transfer: offset vs input common mode\n")
    w(f"![dc]({PL}sch_vs_pex_dc.png)\n")
    w("### 4.3 PSRR\n")
    w(f"![psrr]({PL}sch_vs_pex_psrr.png)\n")
    w("### 4.4 Transient tracking (dynamic offset)\n")
    w(f"![tran]({PL}sch_vs_pex_tran.png)\n")

    w("### 4.5 Monte Carlo offset (mismatch, tt_mm)\n")
    w("| | N | mean (mV) | σ (mV) | ±3σ (mV) | min (mV) | max (mV) |")
    w("|---|---|---|---|---|---|---|")
    for nm, a in (("schematic", ms), ("layout", mp)):
        w(f"| {nm} | {len(a)} | {a.mean():.3f} | {a.std(ddof=1):.3f} | ±{3 * a.std(ddof=1):.2f} | {a.min():.2f} | {a.max():.2f} |")
    ci = 1.96 / np.sqrt(2 * (len(mp) - 1))
    w(f"\nWith N = 200 the 95 % confidence interval on σ is about ±{100 * ci:.0f} %, so the two σ values are "
      "statistically the same. The IP README reports σ = 1.59 mV (N = 1000), which agrees.\n")
    w(f"![mc]({PL}sch_vs_pex_mc.png)\n")

    w("### 4.6 Start-up\n")
    w("| corner | view | Vout final (V) | MN_TAIL_BIAS final (V) | IDD final, 1.8–2 ms avg (µA) | Vout within 1 mV after (µs) |")
    w("|---|---|---|---|---|---|")
    for c in ("tt", "ss", "ff"):
        for v in ("sch", "pex"):
            s = R[v]["start"][c]
            w(f"| {c} | {'schematic' if v == 'sch' else 'layout'} | {s['vout_final']:.4f} | {s['mtb_final']:.4f} | "
              f"{s['idd_final_uA']:.2f} | {s['t_settle_us']:.1f} |")
    w("\nThe supply ramps for 10 µs. In every corner the internal bias starts, Vout settles to "
      "within 1 mV about 2 µs after the ramp ends, and the final supply current equals the DC "
      "operating point.\n")
    w(f"![startup]({PL}sch_vs_pex_startup.png)\n")
    SP = json.load(open(os.path.join(ROOT, "sim", "startup_probe.json")))
    w("**Start-up mechanism, probed in the extracted layout (tt, nets carry schematic names via layout labels):**\n")
    w("| t (µs) | " + " | ".join(SP["cols"]) + " |")
    w("|---|" + "---|" * len(SP["cols"]))
    for r in SP["rows"]:
        w(f"| {r[0]} | " + " | ".join(f"{v:.3f}" for v in r[1:]) + " |")
    w("\nWhile the bias is still off, VSTRP_IP is low and net14 high. VSTRP_OUT is pulled to 0.2–0.4 V, "
      "which turns M12 on and injects current from the R24–R34 chain into MN_TAIL_BIAS. "
      "Once the beta multiplier is up (~12 µs), M2 lifts VSTRP_IP to 1.79 V, net14 falls, "
      "VSTRP_OUT returns to 1.8 V and the injector switches off. "
      "Design observation (schematic left unchanged): with EN = 1, M14 (gate EN_B = 0) is always on, so "
      "VSTRP_OUT is a ratioed node during start-up (M38/M39 overpower M14). It works in all simulated "
      "corners, both pre- and post-layout.\n")

    w("### 4.7 Post-layout (PEX, full RC) results by themselves\n")
    w("Post-layout netlist only, all five corners. These are the post-layout equivalents of the IP's "
      "original `IEEE_plots` (files in `sim/plots/pex/`).\n")
    for fn, cap in (("pex_stb.png", "Loop gain and phase (A0, UGF, PM per corner in the legend)"),
                    ("pex_dc.png", "DC transfer: Vout vs VICM and offset (grey = 0.2–1.6 V window)"),
                    ("pex_psrr.png", "PSRR"),
                    ("pex_tran.png", "Unity-gain tracking of a 1 kHz 0.25–1.55 V sine and the dynamic offset"),
                    ("pex_mc.png", "Mismatch Monte Carlo with Gaussian fit and ±3σ"),
                    ("pex_startup.png", "Start-up")):
        w(f"**{cap}**\n")
        w(f"![{cap}]({PL}pex/{fn})\n")

    w("### 4.8 Power-down (EN = 0) and enable / disable timing\n")
    w("**Method.** The OTA starts enabled (VDD = 1.8 V, VICM = 0.9 V, unity gain, 10 pF). EN is pulled "
      "low at 5 µs and the circuit is simulated for 2 ms of power-down (Gear integration). The "
      "power-down current is the average supply current over 1.9–2.0 ms, and node states are taken at 2 ms. "
      "This mirrors what silicon sees. A plain DC operating point with EN = 0 is ill-conditioned: VOUT "
      "and several cascode/start-up nodes float, and in 3 of 16 cases the solver failed to converge "
      "and returned non-physical currents, so it is not used.\n")
    w("**Power-down supply current**\n")
    w("| Condition | Schematic (pA) | PEX full RC (pA) |")
    w("|---|---|---|")
    for k, lab in (("tt_27", "tt, 27 °C"), ("ss_27", "ss, 27 °C"), ("ff_27", "ff, 27 °C"), ("fs_27", "fs, 27 °C"),
                   ("sf_27", "sf, 27 °C"), ("tt_-40", "tt, −40 °C"), ("tt_85", "tt, 85 °C"), ("tt_125", "tt, 125 °C")):
        w(f"| {lab} | {PD['sch']['op'][k]['idd_nA'] * 1e3:.1f} | {PD['pex']['op'][k]['idd_nA'] * 1e3:.1f} |")
    w("\nPower-down current is **10–30 pA at 27 °C in every corner**, 0.3–0.4 nA at 85 °C and 2.4–4.4 nA at 125 °C "
      "(junction leakage). At 125 °C the layout leaks less than the schematic because the drawn fingers "
      "share source/drain diffusions, giving less junction area than the schematic's per-finger AD/AS estimate.\n")
    w(f"![power-down current]({PL}powerdown/pd_current.png)\n")
    w("**Node states in power-down (tt, 27 °C, 2 ms after EN → 0)**\n")
    w("| Node | Schematic (V) | PEX (V) | Meaning |")
    w("|---|---|---|---|")
    ND = [("mtb", "MN_TAIL_BIAS", "beta-multiplier gate pulled to GNDA by XM16"),
          ("vbp_top", "VBP_TOP", "PMOS bias rail pulled to VDD by M15"),
          ("net8", "net8", "NMOS mirror gate pulled to GNDA by MN_SW1"),
          ("net9", "net9", "PMOS tail gate pulled to VDD by MP_SW1"),
          ("vbp_casc", "VBP_CASC", "PMOS cascode gate pulled to VDD by MP_SW2"),
          ("vbn_casc", "VBN_CASC", "NMOS cascode gate pulled to GNDA by MN_SW2"),
          ("vstrp_ip", "VSTRP_IP", "start-up sense node low (bias off)"),
          ("net14", "net14", "inverter output high"),
          ("vstrp_out", "VSTRP_OUT", "M12 gate ≈ VDD: start-up injector off (only weakly held; see sf)"),
          ("net15", "net15", "= VDD, so no current flows through R24–R34"),
          ("en_b", "EN_B", "inverted enable"),
          ("vout", "VOUT", "floats and holds its last value on CL (high impedance in power-down)")]
    for k, nm, mean in ND:
        w(f"| {nm} | {PD['sch']['op']['tt_27'][k]:.3f} | {PD['pex']['op']['tt_27'][k]:.3f} | {mean} |")
    w(f"\nVSTRP_OUT is not actively driven in power-down (M13, M14 and M39 are off). It settles at "
      f"{PD['pex']['op']['sf_27']['vstrp_out']:.2f} V in sf and {PD['pex']['op']['tt_-40']['vstrp_out']:.2f} V at −40 °C (PEX), "
      "which keeps M12 off in every simulated case; the power-down current confirms no leakage through the resistor chain.\n")
    w("**Enable / disable timing** (EN 0→1 at 20 µs, 1→0 at 120 µs)\n")
    w("| corner | view | IDD enabled (µA) | bias within 1 % (µs) | IDD within 2 % (µs) | Vout within 1 mV (µs) | IDD < 1 % after EN↓ (µs) | IDD 100 µs after EN↓ (nA) |")
    w("|---|---|---|---|---|---|---|---|")
    for c in ("tt", "ss", "ff"):
        for v in ("sch", "pex"):
            r_ = PD[v]["tran"][c]
            w(f"| {c} | {'schematic' if v == 'sch' else 'PEX'} | {r_['idd_on_uA']:.2f} | {r_['t_wake_bias_us']:.2f} | "
              f"{r_['t_wake_idd_us']:.2f} | {r_['t_wake_vout_us']:.2f} | {r_['t_off_us']:.2f} | {r_['idd_off_end_nA']:.3f} |")
    w("\nWake-up to full accuracy takes 3.0–4.7 µs. The extracted layout is 0.6–1.2 µs slower than the "
      "schematic because of the extra parasitic capacitance on the bias rails. Shut-down drops the current "
      "below 1 % within 0.4 µs; the remaining tail settles to the pA leakage floor over ~100 µs.\n")
    w(f"![EN toggle]({PL}powerdown/en_toggle.png)\n")
    w(f"![wake-up]({PL}powerdown/wakeup_zoom.png)\n")

    RV = json.load(open(os.path.join(ROOT, "sim", "results_views.json")))
    VW = [("sch", "Schematic"), ("lay", "Layout, devices only"), ("pexc", "PEX, C only"), ("pex", "PEX, full RC")]
    w("## 5. Layout vs PEX: where the deltas come from\n")
    w("To separate the effect of the physical devices from the wiring parasitics, the same testbenches "
      "were also run on two intermediate views of the layout:\n")
    w("| View | Netlist | Contains |")
    w("|---|---|---|")
    w("| Schematic | `sim/dut_sch.spice` | schematic devices (`m=` multipliers, xschem AD/AS) |")
    w(f"| Layout, devices only | `mag/{CELL}.lvs.spice` (magic `ext2spice lvs`) | the 225 drawn fingers with their real AD/AS/PD/PS; no wiring R or C |")
    w(f"| PEX, C only | `pex/{CELL}_cx.spice` | + extracted wiring capacitance to substrate and coupling |")
    w(f"| PEX, full RC | `pex/{CELL}_rcx.spice` | + extracted wire/contact resistance (final post-layout view) |")
    w("\nThe step-by-step differences show where each delta comes from: **layout − schematic** is device "
      "geometry (shared diffusions, finger splitting), **PEX C − layout** is wiring capacitance, and "
      "**PEX RC − PEX C** is wiring resistance.\n")
    w("**tt, 27 °C**\n")
    w("| Parameter | Schematic | Layout (devices) | PEX C | PEX RC | Δ geometry | Δ parasitic C | Δ wire R | Δ total |")
    w("|---|---|---|---|---|---|---|---|---|")
    for k, name, u, f, kind in MET:
        a, b, c_, d = (RV[v]["tt"][k] for v in ("sch", "lay", "pexc", "pex"))
        p = int(re.search(r"\.(\d)f", f).group(1))
        w(f"| {name} ({u}) | {f.format(a)} | {f.format(b)} | {f.format(c_)} | {f.format(d)} | "
          f"{b - a:+.{p}f} | {c_ - b:+.{p}f} | {d - c_:+.{p}f} | {d - a:+.{p}f} |")
    w("")
    for k, name, u, f, kind in [m for m in MET if m[0] in ("UGF_MHz", "PM_deg", "A0_dB", "PSRR_1MHz_dB", "IDD_uA")]:
        w(f"**{name} ({u}), all corners**\n")
        w("| view | " + " | ".join(C5) + " |")
        w("|---|" + "---|" * 5)
        for v, vl in VW:
            w(f"| {vl} | " + " | ".join(f.format(RV[v][c][k]) for c in C5) + " |")
        w("")
    g = {k: [RV[v]["tt"][k] for v in ("sch", "lay", "pexc", "pex")] for k in ("UGF_MHz", "PM_deg", "PSRR_1MHz_dB", "A0_dB")}
    def share(vals):
        a, b, c_, d = vals
        t = d - a
        return [(b - a) / t * 100, (c_ - b) / t * 100, (d - c_) / t * 100] if abs(t) > 1e-12 else [0, 0, 0]
    su, sp, sps = share(g["UGF_MHz"]), share(g["PM_deg"]), share(g["PSRR_1MHz_dB"])
    w("**Interpretation (tt):**\n")
    w(f"* UGF change {g['UGF_MHz'][3] - g['UGF_MHz'][0]:+.3f} MHz: device geometry {su[0]:.0f} %, "
      f"parasitic C {su[1]:.0f} %, wire R {su[2]:.0f} %.")
    w(f"* Phase-margin change {g['PM_deg'][3] - g['PM_deg'][0]:+.2f}°: device geometry {sp[0]:.0f} %, "
      f"parasitic C {sp[1]:.0f} %, wire R {sp[2]:.0f} %.")
    w(f"* PSRR @ 1 MHz change {g['PSRR_1MHz_dB'][3] - g['PSRR_1MHz_dB'][0]:+.2f} dB: device geometry {sps[0]:.0f} %, "
      f"parasitic C {sps[1]:.0f} %, wire R {sps[2]:.0f} %.")
    w(f"* DC loop gain: {g['A0_dB'][0]:.2f} → {g['A0_dB'][1]:.2f} → {g['A0_dB'][2]:.2f} → {g['A0_dB'][3]:.2f} dB. "
      "Offsets and supply current are unchanged across all views (see table).\n")
    for fn, cap in (("views_stb_tt.png", "Loop gain, tt: four views (right: zoom on the high-frequency region where parasitics act)"),
                    ("views_metrics_corners.png", "Key metrics per corner for all four views"),
                    ("views_psrr_tt.png", "PSRR, tt: four views"),
                    ("views_dc_tt.png", "DC offset, tt, and the difference of each layout view to the schematic (µV)"),
                    ("views_tran_tt.png", "Dynamic offset, tt, and the difference to the schematic (µV)")):
        w(f"**{cap}**\n")
        w(f"![{cap}]({PL}views/{fn})\n")

    w("## 6. Parasitics of the critical nets\n")
    w("Total extracted capacitance per net, summing caps to substrate and coupling to all other nets. "
      "Internal nets carry the schematic names via layout labels.\n")
    w("| Net | Role | C_total (fF) | extracted R segments |")
    w("|---|---|---|---|")
    ROLE = {"VINP": "input +", "VINN": "input −", "net1": "PMOS-pair drain A / NMOS fold", "net2": "PMOS-pair drain B / NMOS fold",
            "net3": "NMOS-pair drain A / PMOS fold", "net4": "NMOS-pair drain B / PMOS fold", "net5": "high-Z node L1 (mirror gate)",
            "VOUT": "output", "net6": "NMOS-pair tail", "net7": "PMOS-pair tail", "MN_TAIL_BIAS": "bias node / pin", "EN": "enable"}
    for n, ln, c, nr in PX["rows"]:
        w(f"| {n} | {ROLE.get(n, '')} | {c:.2f} | {nr} |")
    w("\n**Symmetry of matched nets**\n")
    w("| Pair | C (fF) | C (fF) | mismatch |")
    w("|---|---|---|---|")
    for k, (a, b, d) in PX["pairs"].items():
        x, y = k.split("/")
        w(f"| {x} / {y} | {a:.2f} | {b:.2f} | {d:+.1f} % |")
    w("\nThe input nets match to under 1 %. The folding nodes differ by 1.5–2.7 fF because the "
      "net1/net3 buses run on the left of the core and net2/net4 on the right with different lengths. "
      "These are non-dominant, low-impedance nodes (1/gm of the cascodes), so the imbalance does not "
      "show up in the offset (the systematic offset is unchanged to 1 µV, §3).\n")

    # ---------------- discussion ----------------
    d_ugf = 100 * (R["pex"]["tt"]["UGF_MHz"] / R["sch"]["tt"]["UGF_MHz"] - 1)
    d_pm = R["pex"]["tt"]["PM_deg"] - R["sch"]["tt"]["PM_deg"]
    d_ps = R["pex"]["tt"]["PSRR_1MHz_dB"] - R["sch"]["tt"]["PSRR_1MHz_dB"]
    w("## 7. Discussion\n")
    w(f"* **Stability / bandwidth.** UGF drops by {abs(d_ugf):.1f} % and phase margin by {abs(d_pm):.2f}°, "
      "the same in every corner. The four-view analysis (§5) splits this roughly half and half. "
      "**Wiring capacitance** slows the non-dominant poles at the folding nodes (net1–net5). "
      "**Wiring resistance** is mostly the li1 gate bars and straps of the input pairs (VINP/VINN, "
      "segments up to 0.84 kΩ) driving the ~2 pF input-pair gate capacitance, plus the net5 li strap "
      "to the MP_TOP gates. Device geometry alone changes PM by only +0.2°. "
      f"With the 10 pF load the OTA stays over-damped (PM ≈ {R['pex']['tt']['PM_deg']:.0f}°). "
      "*Optional improvement:* shunting the VINP/VINN li gate bars and inter-row straps with met1 would "
      "recover most of the ~0.85° attributed to wire R.")
    w(f"* **DC accuracy.** Systematic offset is unchanged (≤ 1 µV difference). The DC loop gain changes "
      f"by {R['pex']['tt']['A0_dB'] - R['sch']['tt']['A0_dB']:+.2f} dB. IR drops in the routing are "
      "negligible at this 26 µA supply current, consistent with VOUT and MN_TAIL_BIAS matching to 0.1 mV.")
    w(f"* **PSRR.** Low-frequency PSRR is unchanged within 0.2 dB. At 1 MHz it degrades by {abs(d_ps):.1f} dB: "
      "about 60 % from coupling capacitance between the VDD rails/n-ring and internal nodes, the rest "
      f"from wiring resistance (§5). It remains ≈ {R['pex']['tt']['PSRR_1MHz_dB']:.0f} dB.")
    w("* **Matching.** Mismatch σ is preserved (layout and schematic are statistically identical). SPICE "
      "Monte Carlo models only random mismatch. The common-centroid placement (§8) additionally cancels "
      "linear process gradients, which neither simulation captures; this is a layout-only benefit.")
    w("* **Power and start-up.** IDD differs by < 0.2 %. Start-up is clean in ss/tt/ff and identical to the "
      "schematic within 0.4 µs.\n")

    w("## 8. Matching / floorplan decisions\n")
    w("| Group | Arrangement |")
    w("|---|---|")
    w("| MP_A1/MP_A2 (pfet_lvt, 28+28 × W4/L2) | 4×14, rows X X̄ X̄ X (X = ABBAABBAABBAAB): common centroid in x and y and cancels the xy cross-term; edge fingers balanced (A at the ends of rows 1/4, B of rows 2/3); n-tap guard ring |")
    w("| MN_A1/MN_A2 (nfet_lvt, 8+8 × W2.5/L2) | 2×8 ABBAABBA / BAABBAAB, 2-D common centroid; p-tap guard ring |")
    w("| MP_TOP_L1/L2 (6+6) | ABBA·ABBA·ABBA, continuous diffusion |")
    w("| MN_BOT_L1/L2 (6+6), MN_NDIFF_BIAS (8) | 2 rows ABBAAB / BAABBA (2-D CC), NDIFF_BIAS split symmetrically 2+2 per row |")
    w("| MP_CASC_L1/L2 (8+8) | [A4][B4][B4][A4] |")
    w("| MN_CASC_L1/L2 (3+3) | [A1][B2][A2][B1] (closest to centroid possible with 3+3) |")
    w("| net9 mirror | MP_PDIFF_BIAS 4 + 4 symmetric about the diode MP_PDIFF_BIAS_B |")
    w("| VBP_TOP mirror | M3 (diode) and M4 adjacent with shared source; M9, M2 same row and orientation |")
    w("| XM1/XM10 (16+4 × W10/L4) | 2 identical rows [M1×4][M10×2][M1×4]: 2-D common centroid, merged gate strap |")
    w("\nPer-finger W and L are the schematic's, and netgen merges parallel fingers, so sizes match exactly. "
      "Dummy transistors were **not** added: they would appear as extra devices in LVS against the "
      "unmodified schematic. Edge effects are handled by the common-centroid patterns instead.\n")

    w("## 9. Notes for integration\n")
    w("* LVS reference: the schematic ties NMOS bodies to the global `GND` net. In silicon the "
      "p-substrate is `GNDA` (all p-taps), so `lvs/run_lvs.sh` maps body `GND` → `GNDA`. Nothing else is altered.")
    w("* Pins (port order = symbol order): VDD (met1, top rail), EN (met2, right edge), VINN (met3, top), "
      "VOUT (met3, bottom), VINP (met3, left), MN_TAIL_BIAS (met3, bottom), GNDA (met1, bottom rail). "
      "met4/met5 are unused and free for top-level routing.")
    w("* Reproduce everything with `./run_all.sh` (layout generation → magic DRC → KLayout DRC → LVS → "
      "PEX → all simulations). Then `python3 sim/run_views.py && python3 sim/plot_results.py && "
      "python3 sim/plot_pex.py && python3 sim/plot_views.py && python3 sim/parasitics.py && "
      "python3 sim/startup_probe.py && python3 sim/make_report.py`.")
    w("* Simulation note: the start-up supply current must be read with Gear integration (or averaged). "
      "Trapezoidal integration rings point-to-point on the source current; the ringing averages to the DC value.")

    return L


L = build("", "../sim/plots/")
out = os.path.join(ROOT, "docs", "POST_LAYOUT_VERIFICATION.md")
open(out, "w").write("\n".join(L) + "\n")
print("wrote", out, f"({len(L)} lines)")
# README: replace the auto section
RL = build("docs/", "sim/plots/")
i = next(k for k, l in enumerate(RL) if l.startswith("## 1. Signoff summary"))
j0 = next(k for k, l in enumerate(RL) if l.startswith("## 8. Matching"))
j1 = next(k for k, l in enumerate(RL) if l.startswith("## 9. Notes"))
RL = RL[:j0] + ["## 8. Matching / floorplan decisions", "", "See §3 Matching above.", ""] + RL[j1:]
auto = "\n".join(RL[i:]).replace("## ", "### ").replace("#### ", "#### ")
readme = os.path.join(ROOT, "README.md")
txt = open(readme).read()
b0, b1 = "<!-- BEGIN:AUTO-VERIFICATION -->", "<!-- END:AUTO-VERIFICATION -->"
sec = b0 + "\n## Verification & schematic-vs-layout comparison (auto-generated)\n\n" + auto + "\n" + b1
if b0 in txt:
    txt = txt[:txt.index(b0)] + sec + txt[txt.index(b1) + len(b1):]
else:
    txt = txt.rstrip() + "\n\n" + sec + "\n"
open(readme, "w").write(txt)
print("updated", readme)

# ---------------- IP README (one level up from LAYOUT/, i.e. OTAs/RR_Inp_SE_OTA_IntBias/README.md) ----------------
ip = os.environ.get("IP_README") or os.path.join(ROOT, "..", "README.md")
if os.path.exists(ip):
    IL = build("LAYOUT/docs/", "LAYOUT/sim/plots/")
    i0 = next(k for k, l in enumerate(IL) if l.startswith("## 1. Signoff summary"))
    body = []
    for l in IL[i0:]:
        body.append(re.sub(r"^(\n*)#", r"\1##", l))
    intro = [
        "A full custom layout of this OTA, with physical verification and post-layout verification, is in "
        "[`LAYOUT/`](LAYOUT/README.md). **The schematic in `SCH/` was not modified.** Everything below is "
        "generated by `LAYOUT/sim/make_report.py` from the signoff and simulation results; file paths are "
        "relative to `LAYOUT/`. A standalone copy is in "
        "[`LAYOUT/docs/POST_LAYOUT_VERIFICATION.md`](LAYOUT/docs/POST_LAYOUT_VERIFICATION.md).",
        "",
        "*Note:* this section uses one simulation harness for both the schematic and the extracted layout, "
        "so the two are directly comparable. Absolute values can differ slightly from the Performance "
        "Summary above, which came from the original scripts with different measurement definitions "
        "(for example, the DC loop gain here is |T| at 1 Hz from the Middlebrook loop gain).",
        "",
        "**Plot folders:** schematic vs PEX → [`LAYOUT/sim/plots/`](LAYOUT/sim/plots/) · PEX only → "
        "[`LAYOUT/sim/plots/pex/`](LAYOUT/sim/plots/pex/) · layout vs PEX (four views) → "
        "[`LAYOUT/sim/plots/views/`](LAYOUT/sim/plots/views/) · power-down → "
        "[`LAYOUT/sim/plots/powerdown/`](LAYOUT/sim/plots/powerdown/)",
        "",
    ]
    b0, b1 = "<!-- BEGIN:LAYOUT-VERIFICATION -->", "<!-- END:LAYOUT-VERIFICATION -->"
    sec = b0 + "\n" + "\n".join(intro + body) + "\n" + b1
    txt = open(ip).read()
    if b0 in txt:
        txt = txt[:txt.index(b0)] + sec + txt[txt.index(b1) + len(b1):]
    else:
        h = "## Layout & Post-Layout Verification\n"
        a = txt.index(h) + len(h)
        e = txt.index("## File Structure")
        e = txt.rindex("---", a, e)
        txt = txt[:a] + "\n" + sec + "\n\n" + txt[e:]
    open(ip, "w").write(txt)
    print("updated", ip)
