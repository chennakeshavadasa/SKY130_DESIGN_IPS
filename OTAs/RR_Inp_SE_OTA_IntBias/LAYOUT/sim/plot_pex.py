#!/usr/bin/env python3
"""Post-layout (PEX, full RC) results on their own, all corners -> sim/plots/pex/."""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(SIM, "results.json")))["pex"]
OUT = os.path.join(SIM, "plots", "pex")
os.makedirs(OUT, exist_ok=True)
C5 = ["tt", "ss", "ff", "fs", "sf"]
COL = dict(tt="#2a6fdb", ss="#d1495b", ff="#2e933c", fs="#edae49", sf="#7b4fb3")
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "font.family": "serif"})
TAG = "Post-layout (PEX, full RC)"

# ---- loop gain ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
for c in C5:
    f, m, p = R[c]["stb_curve"]
    lab = f"{c}: A0={R[c]['A0_dB']:.1f} dB, UGF={R[c]['UGF_MHz']:.2f} MHz, PM={R[c]['PM_deg']:.1f}°"
    a1.semilogx(f, m, color=COL[c], lw=1.3, label=lab)
    a2.semilogx(f, p, color=COL[c], lw=1.3)
a1.axhline(0, color="k", lw=0.6)
a1.set_ylabel("|T| (dB)")
a2.set_ylabel("phase(T) rel. DC (deg)")
a2.set_xlabel("frequency (Hz)")
a1.set_title(f"{TAG}: loop gain, unity gain, CL = 10 pF")
a1.legend(fontsize=7, loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_stb.png"), dpi=160)
plt.close(fig)

# ---- DC transfer ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
for c in C5:
    vin, off = np.array(R[c]["dc_curve"][0]), np.array(R[c]["dc_curve"][1])
    a1.plot(vin, vin + off / 1e3, color=COL[c], lw=1.3, label=c)
    a2.plot(vin, off, color=COL[c], lw=1.3, label=f"{c}: {R[c]['off_0p9_mV']:+.3f} mV @0.9 V")
a1.plot([0, 1.8], [0, 1.8], "k:", lw=0.8, label="ideal")
a1.set_ylabel("Vout (V)")
a2.set_ylabel("Vout − VICM (mV)")
a2.set_xlabel("VICM (V)")
a2.set_ylim(-60, 60)
a2.axvspan(0.2, 1.6, color="0.9", zorder=0)
a1.set_title(f"{TAG}: unity-gain DC transfer (rail-to-rail input)")
a1.legend(fontsize=7, ncol=3)
a2.legend(fontsize=7, ncol=2, loc="lower left")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_dc.png"), dpi=160)
plt.close(fig)

# ---- PSRR ----
fig, ax = plt.subplots(figsize=(6.6, 3.6))
for c in C5:
    f, db = R[c]["psrr_curve"]
    ax.semilogx(f, db, color=COL[c], lw=1.3,
                label=f"{c}: {R[c]['PSRR_10Hz_dB']:.1f} dB @10 Hz, {R[c]['PSRR_1MHz_dB']:.1f} dB @1 MHz")
ax.axvline(1e6, color="k", ls="--", lw=0.7)
ax.set_xlabel("frequency (Hz)")
ax.set_ylabel("Vout / VDD (dB)")
ax.set_title(f"{TAG}: PSRR")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_psrr.png"), dpi=160)
plt.close(fig)

# ---- transient ----
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.6, 5.4), sharex=True)
for c in C5:
    p = os.path.join(SIM, "pex", "tran", f"tran_{c}.dat")
    if os.path.exists(p):
        a = np.loadtxt(p).reshape(-1, 3)
        t, vo, vi = a[:, 0] * 1e3, a[:, 1], a[:, 2]
        a1.plot(t, vo, color=COL[c], lw=1.1, label=f"Vout {c}")
        if c == "tt":
            a1.plot(t, vi, "k:", lw=1.0, label="VICM")
        a2.plot(t, (vo - vi) * 1e3, color=COL[c], lw=1.1,
                label=f"{c}: peak {R[c]['tran_offpk_mV']:.2f} mV")
a1.set_ylabel("V")
a2.set_ylabel("Vout − VICM (mV)")
a2.set_xlabel("time (ms)")
a1.set_title(f"{TAG}: unity-gain tracking, 1 kHz 0.25–1.55 V sine")
a1.legend(fontsize=7, ncol=3)
a2.set_ylim(-11, 7)
a2.legend(fontsize=6.5, ncol=5, loc="upper center")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_tran.png"), dpi=160)
plt.close(fig)

# ---- Monte Carlo ----
mc = np.array(json.load(open(os.path.join(SIM, "results.json")))["pex"]["mc"])
mu, sd = mc.mean(), mc.std(ddof=1)
fig, ax = plt.subplots(figsize=(6.6, 3.8))
ax.hist(mc, bins=30, color="#2a6fdb", alpha=0.75, edgecolor="white")
x = np.linspace(mu - 4 * sd, mu + 4 * sd, 300)
bw = (mc.max() - mc.min()) / 30
ax.plot(x, len(mc) * bw / (sd * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sd) ** 2), "k-", lw=1.2,
        label=f"Gaussian fit  μ = {mu:.3f} mV, σ = {sd:.3f} mV")
for k in (-3, 3):
    ax.axvline(mu + k * sd, color="#d1495b", ls="--", lw=0.9)
ax.set_xlabel("input-referred offset Vout − VICM (mV), VICM = 0.9 V")
ax.set_ylabel("count")
ax.set_title(f"{TAG}: mismatch Monte Carlo (tt_mm, N = {len(mc)}), ±3σ = ±{3 * sd:.2f} mV")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_mc.png"), dpi=160)
plt.close(fig)

# ---- start-up ----
fig, axs = plt.subplots(1, 3, figsize=(10, 3.2))
S = json.load(open(os.path.join(SIM, "results.json")))["pex"]["start"]
for c in ("tt", "ss", "ff"):
    s = S[c]
    t = np.array(s["t"]) * 1e6
    m = t <= 40
    axs[0].plot(t[m], np.array(s["vout"])[m], color=COL[c], label=c)
    axs[1].plot(t[m], np.array(s["mtb"])[m], color=COL[c])
    axs[2].plot(t[m], np.array(s["idd"])[m] * 1e6, color=COL[c])
for ax, yl in zip(axs, ("Vout (V)", "MN_TAIL_BIAS (V)", "IDD (µA)")):
    ax.set_xlabel("t (µs)")
    ax.set_ylabel(yl)
axs[0].legend(fontsize=7)
fig.suptitle(f"{TAG}: start-up, VDD/EN/VICM ramp 0 → final in 10 µs")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pex_startup.png"), dpi=160)
plt.close(fig)
print("PEX plots ->", OUT, sorted(os.listdir(OUT)))
