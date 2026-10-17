#!/usr/bin/env python3
"""Power-down / enable plots (schematic vs PEX) -> sim/plots/powerdown/."""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIM = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(SIM, "results_pd.json")))
OUT = os.path.join(SIM, "plots", "powerdown")
os.makedirs(OUT, exist_ok=True)
COL = dict(tt="#2a6fdb", ss="#d1495b", ff="#2e933c")
plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.3, "font.family": "serif"})

# EN toggle transient
fig, axs = plt.subplots(4, 1, figsize=(7.2, 8.2), sharex=True)
for c in ("tt", "ss", "ff"):
    for v, ls in (("sch", ":"), ("pex", "-")):
        r = P[v]["tran"][c]
        t = np.array(r["t"]) * 1e6
        lab = f"{c} {'SCH' if v == 'sch' else 'PEX'}"
        if c == "tt" and v == "pex":
            axs[0].plot(t, r["en"], "k-", lw=1.1)
        axs[1].plot(t, r["vout"], ls, color=COL[c], lw=1.2, label=lab)
        axs[2].plot(t, r["mtb"], ls, color=COL[c], lw=1.2)
        axs[3].semilogy(t, np.clip(np.array(r["idd"]), 1e-12, None) * 1e6, ls, color=COL[c], lw=1.2)
axs[0].set_ylabel("EN (V)")
axs[1].set_ylabel("Vout (V)")
axs[2].set_ylabel("MN_TAIL_BIAS (V)")
axs[3].set_ylabel("IDD (µA, log)")
axs[3].set_xlabel("time (µs)")
axs[1].legend(fontsize=7, ncol=3)
axs[0].set_title("Enable / power-down: EN 0→1 at 20 µs, 1→0 at 120 µs\n(dotted: SCH, solid: PEX full RC)", fontsize=9)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "en_toggle.png"), dpi=160)
plt.close(fig)

# zoom on wake-up
fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
for c in ("tt", "ss", "ff"):
    for v, ls in (("sch", ":"), ("pex", "-")):
        r = P[v]["tran"][c]
        t = np.array(r["t"]) * 1e6
        m = (t > 19) & (t < 30)
        axs[0].plot(t[m] - 20, np.array(r["mtb"])[m], ls, color=COL[c], label=f"{c} {'SCH' if v == 'sch' else 'PEX'}")
        axs[1].plot(t[m] - 20, np.array(r["idd"])[m] * 1e6, ls, color=COL[c])
axs[0].set_ylabel("MN_TAIL_BIAS (V)")
axs[1].set_ylabel("IDD (µA)")
for a in axs:
    a.set_xlabel("time after EN rising edge (µs)")
axs[0].legend(fontsize=7)
fig.suptitle("Wake-up from power-down")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "wakeup_zoom.png"), dpi=160)
plt.close(fig)

# power-down current vs corner / temperature
keys = [("tt_27", "tt\n27°C"), ("ss_27", "ss\n27°C"), ("ff_27", "ff\n27°C"), ("fs_27", "fs\n27°C"),
        ("sf_27", "sf\n27°C"), ("tt_-40", "tt\n−40°C"), ("tt_85", "tt\n85°C"), ("tt_125", "tt\n125°C")]
x = np.arange(len(keys))
fig, ax = plt.subplots(figsize=(7.2, 3.6))
for i, (v, col, lab) in enumerate((("sch", "#999999", "SCH"), ("pex", "#2a6fdb", "PEX (full RC)"))):
    vals = [P[v]["op"][k]["idd_nA"] * 1e3 for k, _ in keys]
    ax.bar(x + (i - 0.5) * 0.38, vals, 0.38, color=col, label=lab)
ax.set_yscale("log")
ax.set_xticks(x, [l for _, l in keys])
ax.set_ylabel("power-down IDD (pA)")
ax.set_title("Power-down supply current, EN = 0 (2 ms after disable, VDD = 1.8 V)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "pd_current.png"), dpi=160)
plt.close(fig)
print("power-down plots ->", OUT, sorted(os.listdir(OUT)))
