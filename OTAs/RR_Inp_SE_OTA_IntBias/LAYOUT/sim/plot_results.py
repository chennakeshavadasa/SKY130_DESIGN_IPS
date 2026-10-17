#!/usr/bin/env python3
"""Plots + markdown table: schematic (pre-layout) vs RC-extracted layout (post-layout)."""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SIM, "results.json")))
OUT = os.path.join(SIM, "plots")
os.makedirs(OUT, exist_ok=True)
CORNERS = ["tt", "ss", "ff", "fs", "sf"]
COL = dict(tt="#2a6fdb", ss="#d1495b", ff="#2e933c", fs="#edae49", sf="#7b4fb3")
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3})


def pair(fig_name, key, xlab, ylab, logx=False, title=""):
    fig, ax = plt.subplots(1, 1, figsize=(6.4, 3.8))
    for c in CORNERS:
        for mode, ls in (("sch", ":"), ("pex", "-")):
            x, y = R[mode][c][key][0], R[mode][c][key][1]
            ax.plot(x, y, ls, color=COL[c], lw=1.2, label=f"{c} {'SCH' if mode == 'sch' else 'PEX'}")
    if logx:
        ax.set_xscale("log")
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    ax.legend(ncol=5, fontsize=7, loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fig_name), dpi=150)
    plt.close(fig)


# loop gain + phase
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 5.2), sharex=True)
for c in CORNERS:
    for mode, ls in (("sch", ":"), ("pex", "-")):
        f, m, p = R[mode][c]["stb_curve"]
        a1.semilogx(f, m, ls, color=COL[c], lw=1.2, label=f"{c} {'SCH' if mode == 'sch' else 'PEX'}")
        a2.semilogx(f, p, ls, color=COL[c], lw=1.2)
a1.axhline(0, color="k", lw=0.6)
a1.set_ylabel("|T| (dB)")
a2.set_ylabel("phase(T) rel. DC (deg)")
a2.set_xlabel("frequency (Hz)")
a1.set_title("Loop gain T (Middlebrook), unity gain, CL=10 pF\ndotted: schematic (SCH), solid: extracted layout (PEX, full RC)", fontsize=9)
a1.legend(ncol=5, fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sch_vs_pex_stb.png"), dpi=150)
plt.close(fig)

pair("sch_vs_pex_dc.png", "dc_curve", "VICM (V)", "Vout - VICM (mV)",
     title="Unity-gain DC offset vs VICM (dotted: SCH, solid: PEX full RC)")
pair("sch_vs_pex_psrr.png", "psrr_curve", "frequency (Hz)", "Vout/VDD (dB)", logx=True,
     title="PSRR Vout/VDD (dotted: SCH, solid: PEX full RC)")
pair("sch_vs_pex_tran.png", "tran_curve", "time (s)", "Vout - VICM (mV)",
     title="Dynamic offset, 1 kHz 0.25..1.55 V sine (dotted: SCH, solid: PEX full RC)")

# start-up
fig, axs = plt.subplots(1, 3, figsize=(10, 3.2))
for c in ("tt", "ss", "ff"):
    for mode, ls in (("sch", ":"), ("pex", "-")):
        s = R[mode]["start"][c]
        t = np.array(s["t"]) * 1e6
        m = t <= 40
        axs[0].plot(t[m], np.array(s["vout"])[m], ls, color=COL[c], label=f"{c} {'SCH' if mode == 'sch' else 'PEX'}")
        axs[1].plot(t[m], np.array(s["mtb"])[m], ls, color=COL[c])
        axs[2].plot(t[m], np.array(s["idd"])[m] * 1e6, ls, color=COL[c])
for ax, yl in zip(axs, ("Vout (V)", "MN_TAIL_BIAS (V)", "IDD (uA)")):
    ax.set_xlabel("t (us)")
    ax.set_ylabel(yl)
axs[0].legend(fontsize=7)
fig.suptitle("Start-up: VDD, EN, VICM ramp 0 -> final in 10 us (dotted: SCH, solid: PEX full RC)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sch_vs_pex_startup.png"), dpi=150)
plt.close(fig)

# MC histogram
fig, ax = plt.subplots(figsize=(6.4, 3.6))
for mode, col in (("sch", "#999999"), ("pex", "#2a6fdb")):
    a = np.array(R[mode]["mc"])
    ax.hist(a, bins=30, alpha=0.6, color=col,
            label=f"{'SCH' if mode == 'sch' else 'PEX'}-layout  N={len(a)}  mu={a.mean():.2f} mV  sigma={a.std(ddof=1):.2f} mV")
ax.set_xlabel("input-referred offset Vout - VICM (mV), VICM = 0.9 V, tt_mm")
ax.set_ylabel("count")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "sch_vs_pex_mc.png"), dpi=150)
plt.close(fig)

# markdown table
keys = [("A0_dB", "DC loop gain (dB)", "{:.1f}"), ("UGF_MHz", "UGF (MHz)", "{:.3f}"),
        ("PM_deg", "Phase margin (deg)", "{:.1f}"), ("off_0p9_mV", "Offset @ VICM=0.9 V (mV)", "{:.3f}"),
        ("off_max_0p2_1p6_mV", "max |offset| 0.2-1.6 V (mV)", "{:.2f}"),
        ("PSRR_10Hz_dB", "PSRR @10 Hz (dB)", "{:.1f}"), ("PSRR_1MHz_dB", "PSRR @1 MHz (dB)", "{:.1f}"),
        ("tran_offpk_mV", "peak dyn. offset (mV)", "{:.2f}"), ("IDD_uA", "IDD (uA)", "{:.2f}")]
lines = ["| Parameter | " + " | ".join(f"{c} pre / post" for c in CORNERS) + " |",
         "|---|" + "---|" * len(CORNERS)]
for k, name, fmt in keys:
    cells = [f"{fmt.format(R['sch'][c][k])} / {fmt.format(R['pex'][c][k])}" for c in CORNERS]
    lines.append(f"| {name} | " + " | ".join(cells) + " |")
for mode in ("sch", "pex"):
    a = np.array(R[mode]["mc"])
    lines.append(f"\nMC ({'SCH' if mode == 'sch' else 'PEX'}-layout, tt_mm, N={len(a)}): "
                 f"mean {a.mean():.3f} mV, sigma {a.std(ddof=1):.3f} mV")
open(os.path.join(SIM, "summary_table.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
