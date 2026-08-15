#!/usr/bin/env python3
"""
Standalone MC histogram re-plot
Reads an existing mc_results.csv and overwrites only:
  <SIMS_ROOT>/MC/mc_plot.html
  <SIMS_ROOT>/IEEE_plots/mc_ieee.png
  <SIMS_ROOT>/IEEE_plots/mc_ieee.pdf

Run from your With_internal_Bias/ directory:
  python3 replot_mc_only.py
  python3 replot_mc_only.py --sims-dir path/to/Rail_to_Rail_IP_OP_OTA_int_bias_Sims
"""

import argparse, pathlib, sys
import numpy as np
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# ── USER CONFIG ──────────────────────────────────────────────────────────────
DESIGN_NAME = "Rail_to_Rail_IP_OP_OTA_int_bias"
MC_CORNER   = "tt_mm"
SIMS_ROOT   = pathlib.Path("Rail_to_Rail_IP_OP_OTA_int_bias_Sims")
MC_COLOR    = "#00AAAA"   # tt_mm teal
N_BINS      = 60

# Sigma line colors: 1σ green, 2σ orange, 3σ red
SIGMA_COLOR = {1: "#228B22", 2: "#FF8C00", 3: "#CC1100"}

IEEE_RC = {
    "font.family": "serif",
    "font.serif":  ["Liberation Serif", "DejaVu Serif", "Times New Roman"],
    "font.size": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5,
    "lines.linewidth": 1.2, "axes.linewidth": 0.7,
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": True,
    "axes.grid": True, "grid.linewidth": 0.35, "grid.alpha": 0.40,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
    "pdf.fonttype": 42, "ps.fonttype": 42,
}
COL1 = 3.5   # IEEE single-column [inches]


# ── HELPERS ──────────────────────────────────────────────────────────────────
def _gaussian(x, mu, sig):
    """Gaussian PDF — no scipy required."""
    return (1.0 / (sig * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sig) ** 2)


def load_mc_csv(csv_path: pathlib.Path) -> np.ndarray:
    """Parse bare-numeric ngspice wrdata CSV. Returns V_OS values in mV."""
    tokens, n_cols = [], None
    for ln in csv_path.read_text(errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        vals, ok = [], True
        for tok in ln.split():
            try:   vals.append(float(tok))
            except ValueError: ok = False; break
        if ok and vals:
            if n_cols is None: n_cols = len(vals)
            if len(vals) == n_cols: tokens.extend(vals)
    if not tokens or n_cols is None:
        sys.exit(f"[ERROR] Could not parse {csv_path}")
    trim = len(tokens) % n_cols
    if trim: tokens = tokens[:-trim]
    arr = np.array(tokens).reshape(-1, n_cols)
    # col index 1 = v(DIFF_MIS) in volts → convert to mV
    return arr[:, 1] * 1e3


# ── PLOTLY ───────────────────────────────────────────────────────────────────
def plot_mc_plotly(vos_mV: np.ndarray, out_html: pathlib.Path) -> None:
    mu, sig, n = float(np.mean(vos_mV)), float(np.std(vos_mV)), len(vos_mV)
    data_range = vos_mV.max() - vos_mV.min()
    bin_w      = data_range / N_BINS if data_range > 0 else sig * 0.2

    x_fine        = np.linspace(mu - 4.5*sig, mu + 4.5*sig, 600)
    gauss_counts  = _gaussian(x_fine, mu, sig) * n * bin_w

    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=vos_mV, nbinsx=N_BINS,
        marker_color=MC_COLOR, marker_line=dict(width=0.4, color="white"),
        name=f"Simulated V_OS  (n={n})", opacity=0.78,
    ))

    # Gaussian fit curve
    fig.add_trace(go.Scatter(
        x=x_fine, y=gauss_counts, mode="lines",
        name=f"Gaussian fit  μ={mu:.3f} mV, σ={sig:.3f} mV",
        line=dict(color="#EE2200", width=2.5),
    ))

    # Shaded σ bands (draw outermost first so inner bands overlay)
    for k, fill in [(3, "rgba(255,60,60,0.07)"),
                    (2, "rgba(255,165,0,0.10)"),
                    (1, "rgba(30,180,30,0.14)")]:
        fig.add_vrect(x0=mu - k*sig, x1=mu + k*sig,
                      fillcolor=fill, layer="below", line_width=0)

    # Mean line
    fig.add_vline(x=mu, line_color="#EE2200", line_width=2.0,
                  annotation_text=f"μ = {mu:.3f} mV",
                  annotation_position="top right",
                  annotation=dict(font=dict(size=13, color="#EE2200")))

    # Individually labelled ±1σ / ±2σ / ±3σ vertical lines
    for k in (1, 2, 3):
        col = SIGMA_COLOR[k]
        for sign in (-1, 1):
            label = f"{'+' if sign > 0 else '−'}{k}σ"
            pos   = "top right" if sign > 0 else "top left"
            fig.add_vline(x=mu + sign*k*sig,
                          line=dict(color=col, width=1.4, dash="dash"),
                          annotation_text=label, annotation_position=pos,
                          annotation=dict(font=dict(size=13, color=col),
                                          bgcolor="rgba(255,255,255,0.7)"))

    # Stats annotation box
    stats = (
        f"<b>Statistics</b><br>"
        f"n   = {n}<br>"
        f"μ   = {mu:.4f} mV<br>"
        f"σ   = {sig:.4f} mV<br>"
        f"σ²  = {sig**2*1e6:.4f} μV²<br>"
        f"±1σ = [{mu-sig:.3f}, {mu+sig:.3f}] mV<br>"
        f"±2σ = [{mu-2*sig:.3f}, {mu+2*sig:.3f}] mV<br>"
        f"±3σ = [{mu-3*sig:.3f}, {mu+3*sig:.3f}] mV"
    )
    fig.add_annotation(xref="paper", yref="paper", x=0.98, y=0.98,
                       text=stats, showarrow=False, align="left",
                       font=dict(size=14, family="Courier New"),
                       bgcolor="white", bordercolor="#888888", borderwidth=1)

    fig.update_layout(
        title=f"{DESIGN_NAME} — MC Offset Voltage  ({n} runs, corner: {MC_CORNER})",
        xaxis_title="V<sub>OS</sub>  [mV]",
        yaxis_title="Count",
        font=dict(size=13), template="plotly_white",
        hovermode="x unified", bargap=0.04,
        legend=dict(font=dict(size=12), x=0.02, y=0.97,
                    bgcolor="rgba(255,255,255,0.85)", borderwidth=1),
    )
    fig.write_html(str(out_html))
    print(f"  Saved → {out_html}")


# ── IEEE MATPLOTLIB ──────────────────────────────────────────────────────────
def plot_mc_ieee(vos_mV: np.ndarray, out_dir: pathlib.Path) -> None:
    mu, sig, n = float(np.mean(vos_mV)), float(np.std(vos_mV)), len(vos_mV)

    with plt.rc_context(IEEE_RC):
        fig, ax = plt.subplots(figsize=(COL1, 3.2))

        # Histogram — get exact bin edges for scaling Gaussian
        counts, edges, _ = ax.hist(
            vos_mV, bins=N_BINS,
            color=MC_COLOR, alpha=0.72, edgecolor="none", label="Simulated",
        )
        bin_w = edges[1] - edges[0]

        # Gaussian PDF curve scaled to count units
        x_fine       = np.linspace(mu - 4.5*sig, mu + 4.5*sig, 600)
        gauss_counts = _gaussian(x_fine, mu, sig) * n * bin_w
        ax.plot(x_fine, gauss_counts, color="#CC1100", lw=1.2, label="Gaussian fit")

        # Shaded σ bands (outermost first)
        for k, col, alpha in [(3, "#FF3C3C", 0.07),
                               (2, "#FF8C00", 0.11),
                               (1, "#1AAA1A", 0.17)]:
            ax.axvspan(mu - k*sig, mu + k*sig, color=col, alpha=alpha, lw=0)

        # Individually labelled ±1σ / ±2σ / ±3σ vertical lines
        ax.set_xlim(mu - 4.2*sig, mu + 4.2*sig)
        y_top = ax.get_ylim()[1]
        for k in (1, 2, 3):
            col = SIGMA_COLOR[k]
            for sign in (-1, 1):
                x_val = mu + sign * k * sig
                ax.axvline(x_val, color=col, lw=0.7, ls="--")
                label = f"${'+' if sign > 0 else r'-'}{k}\\sigma$"
                ha = "left" if sign > 0 else "right"
                ax.text(x_val + sign*0.01*sig, y_top*0.97, label,
                        fontsize=5.5, color=col, ha=ha, va="top")

        # Mean line
        ax.axvline(mu, color="#CC1100", lw=0.9, ls="-")
        ax.text(mu, y_top*0.97, r"$\mu$",
                fontsize=5.5, color="#CC1100", ha="left", va="top")

        # Inset stats (lower-left)
        stats = (f"n = {n}\nμ = {mu:.3f} mV\nσ = {sig:.3f} mV\n"
                 f"±1σ: 68.3%\n±2σ: 95.4%\n±3σ: 99.7%\n"
                 f"±3σ = [{mu-3*sig:.3f}, {mu+3*sig:.3f}] mV")
        ax.text(0.02, 0.02, stats, transform=ax.transAxes,
                fontsize=5.5, va="bottom", ha="left", family="monospace",
                bbox=dict(boxstyle="square,pad=0.25", fc="white",
                          ec="#BBBBBB", lw=0.6))

        ax.set_xlabel(r"$V_{OS}$ [mV]")
        ax.set_ylabel("Count")
        ax.set_title(f"MC Offset Voltage  ({n} runs, {MC_CORNER})", pad=3)
        ax.legend(loc="upper right", fontsize=6)
        fig.tight_layout()

        for ext in ("png", "pdf"):
            dest = out_dir / f"mc_ieee.{ext}"
            fig.savefig(str(dest))
            print(f"  Saved → {dest}")
        plt.close(fig)


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Regenerate MC histogram plots from existing mc_results.csv"
    )
    parser.add_argument("--sims-dir", type=pathlib.Path, default=SIMS_ROOT,
                        help=f"Path to the Sims output directory (default: {SIMS_ROOT})")
    args = parser.parse_args()

    sims  = args.sims_dir
    csv   = sims / "MC" / "csv_results" / "mc_results.csv"
    html  = sims / "MC" / "mc_plot.html"
    ieee  = sims / "IEEE_plots"

    for p in (csv, ieee):
        if not p.exists():
            sys.exit(f"[ERROR] Path not found: {p}\n"
                     f"        Run from With_internal_Bias/ or pass --sims-dir.")

    print(f"[MC] Reading {csv}  ({csv.stat().st_size//1024} kB)")
    vos_mV = load_mc_csv(csv)
    print(f"[MC] {len(vos_mV)} samples loaded  "
          f"μ={np.mean(vos_mV):.3f} mV  σ={np.std(vos_mV):.3f} mV")

    print("[MC] Generating Plotly HTML ...")
    plot_mc_plotly(vos_mV, html)

    print("[MC] Generating IEEE PNG + PDF ...")
    plot_mc_ieee(vos_mV, ieee)

    print("[MC] Done.")


if __name__ == "__main__":
    main()
