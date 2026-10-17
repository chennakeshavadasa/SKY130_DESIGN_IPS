#!/usr/bin/env python3
"""Four-view comparison plots (schematic / layout devices-only / PEX C-only / PEX RC) -> sim/plots/views/."""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SIM, "results_views.json")))
OUT = os.path.join(SIM, "plots", "views")
os.makedirs(OUT, exist_ok=True)
C5 = ["tt", "ss", "ff", "fs", "sf"]
V = [("sch", "Schematic", "k", ":"), ("lay", "Layout, devices only", "#2a6fdb", "--"),
     ("pexc", "PEX, C only", "#edae49", "-."), ("pex", "PEX, full RC", "#d1495b", "-")]
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "font.family": "serif"})

# loop gain tt: full + zoom
fig, axs = plt.subplots(2, 2, figsize=(10, 6))
for v, lab, col, ls in V:
    f, m, p = R[v]["tt"]["stb_curve"]
    f = np.array(f)
    for j, (lo, hi) in enumerate(((1, 1e9), (5e5, 1e9))):
        k = (f >= lo) & (f <= hi)
        axs[0, j].semilogx(f[k], np.array(m)[k], ls, color=col, lw=1.3,
                           label=f"{lab}: UGF {R[v]['tt']['UGF_MHz']:.3f} MHz, PM {R[v]['tt']['PM_deg']:.2f}°")
        axs[1, j].semilogx(f[k], np.array(p)[k], ls, color=col, lw=1.3)
for j in range(2):
    axs[0, j].axhline(0, color="0.4", lw=0.6)
    axs[1, j].set_xlabel("frequency (Hz)")
axs[0, 0].set_ylabel("|T| (dB)")
axs[1, 0].set_ylabel("phase(T) rel. DC (deg)")
axs[0, 0].set_title("Loop gain, tt (full range)")
axs[0, 1].set_title("Zoom 0.5 MHz – 1 GHz (where parasitics act)")
axs[0, 0].legend(fontsize=7, loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "views_stb_tt.png"), dpi=160)
plt.close(fig)

# PSRR tt
fig, ax = plt.subplots(figsize=(6.6, 3.8))
for v, lab, col, ls in V:
    f, db = R[v]["tt"]["psrr_curve"]
    ax.semilogx(f, db, ls, color=col, lw=1.3,
                label=f"{lab}: {R[v]['tt']['PSRR_10Hz_dB']:.2f} dB @10 Hz, {R[v]['tt']['PSRR_1MHz_dB']:.2f} dB @1 MHz")
ax.axvline(1e6, color="0.4", ls="--", lw=0.7)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("Vout / VDD (dB)")
ax.set_title("PSRR, tt: schematic vs layout views")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "views_psrr_tt.png"), dpi=160)
plt.close(fig)

# DC offset tt + difference to schematic
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
vin0, off0 = map(np.array, R["sch"]["tt"]["dc_curve"])
for v, lab, col, ls in V:
    vin, off = map(np.array, R[v]["tt"]["dc_curve"])
    a1.plot(vin, off, ls, color=col, lw=1.3, label=lab)
    if v != "sch":
        a2.plot(vin, (np.interp(vin0, vin, off) - off0) * 1e3, ls, color=col, lw=1.3, label=lab)
a1.set_ylim(-60, 60)
a1.set_ylabel("Vout − VICM (mV)")
a2.set_ylabel("Δ vs schematic (µV)")
a2.set_xlabel("VICM (V)")
a1.set_title("Unity-gain DC offset, tt")
a1.legend(fontsize=7)
a2.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "views_dc_tt.png"), dpi=160)
plt.close(fig)

# TRAN dynamic offset tt + difference
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
t0, d0 = map(np.array, R["sch"]["tt"]["tran_curve"])
for v, lab, col, ls in V:
    t, d = map(np.array, R[v]["tt"]["tran_curve"])
    a1.plot(t * 1e3, d, ls, color=col, lw=1.2, label=f"{lab}: peak {R[v]['tt']['tran_offpk_mV']:.3f} mV")
    if v != "sch":
        a2.plot(t0 * 1e3, (np.interp(t0, t, d) - d0) * 1e3, ls, color=col, lw=1.2, label=lab)
a1.set_ylabel("Vout − VICM (mV)")
a2.set_ylabel("Δ vs schematic (µV)")
a2.set_xlabel("time (ms)")
a1.set_title("Dynamic offset, 1 kHz sine, tt")
a1.legend(fontsize=7, loc="lower left")
a2.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "views_tran_tt.png"), dpi=160)
plt.close(fig)

# metrics vs corner for all views
M = [("UGF_MHz", "UGF (MHz)"), ("PM_deg", "Phase margin (deg)"), ("A0_dB", "DC loop gain (dB)"),
     ("PSRR_1MHz_dB", "PSRR @1 MHz (dB)"), ("IDD_uA", "IDD (µA)"), ("tran_offpk_mV", "peak dyn. offset (mV)")]
fig, axs = plt.subplots(2, 3, figsize=(11, 5.6))
for ax, (k, lab) in zip(axs.flat, M):
    for v, vl, col, ls in V:
        ax.plot(C5, [R[v][c][k] for c in C5], ls, marker="o", ms=4, color=col, lw=1.2, label=vl)
    ax.set_title(lab, fontsize=9)
axs[0, 0].legend(fontsize=7)
fig.suptitle("Key metrics per corner: schematic → layout (devices) → PEX C → PEX RC")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "views_metrics_corners.png"), dpi=160)
plt.close(fig)
print("view plots ->", OUT, sorted(os.listdir(OUT)))
