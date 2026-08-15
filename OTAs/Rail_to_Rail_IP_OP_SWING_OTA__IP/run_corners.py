#!/usr/bin/env python3
"""
Rail_to_Rail_IP_OP_OTA  Cross-Corner + Monte Carlo Simulation Runner
=====================================================================
Usage:
  python3 run_corners.py                    # full flow
  python3 run_corners.py --generate-only    # netlists only
  python3 run_corners.py --plot-only        # replot existing CSVs
  python3 run_corners.py --corners tt ss    # subset of corners

How to open all plots after running:
  firefox Rail_to_Rail_OTA_Sims/DC/DC_cross_corner.html
  firefox Rail_to_Rail_OTA_Sims/PSRR/PSRR_cross_corner.html
  firefox Rail_to_Rail_OTA_Sims/TRAN/TRAN_cross_corner.html
  firefox Rail_to_Rail_OTA_Sims/STB/STB_cross_corner.html
  firefox Rail_to_Rail_OTA_Sims/MC/MC_offset_histogram.html

  IEEE figures (PNG + PDF) are in:
  Rail_to_Rail_OTA_Sims/IEEE_plots/
"""

import argparse, re, subprocess, sys, pathlib
import numpy  as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
#  USER CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
SRC_MC  = pathlib.Path("Rail_to_Rail_IP_OP_OTA_MC.spice")
SRC_STB = pathlib.Path("Rail_to_Rail_IP_OP_OTA_STB.spice")
SRC_DCT = pathlib.Path("tb_Rail_to_Rail_IP_OP_OTA_DC_TRAN_PSRR.spice")
OUTDIR    = pathlib.Path("Rail_to_Rail_OTA_Sims")
NGSPICE   = "ngspice"
CORNERS   = ["tt", "ss", "ff", "fs", "sf"]
MC_CORNER = "tt_mm"
# ─────────────────────────────────────────────────────────────────────────────

TB_NAMES = ["DC", "PSRR", "TRAN", "STB", "MC"]

CORNER_COLOR = {
    "tt":    "#0055FF",
    "ss":    "#FF2200",
    "ff":    "#00BB00",
    "fs":    "#FF8800",
    "sf":    "#CC00FF",
    "tt_mm": "#00AAAA",
}
CORNER_DASH = {
    "tt": "solid",
    "ss": "dot",
    "ff": "dash",
    "fs": "dashdot",
    "sf": "longdashdot",
}

# ngspice wrdata raw column indices (confirmed from CSV inspection)
# real vector    -> 2 raw cols: [scale, value]
# complex vector -> 3 raw cols: [scale, real, imag]   (frequency in AC is complex)
#   DC   wrdata v(VICM) v(Vout)         ->  4 raw cols  (2+2)
#   PSRR wrdata frequency vdb(Vout)     ->  5 raw cols  (3+2)
#   TRAN wrdata time v(Vout) v(VICM)    ->  6 raw cols  (2+2+2)
#   STB  wrdata frequency vdb(mb) phase ->  7 raw cols  (3+2+2)
#   MC   wrdata r v(DIFF_MIS)           ->  4 raw cols  (2+2)
_TB_EXTRACT = {
    "DC":   dict(indices=[1, 3],    names=["v(vicm)", "v(vout)"]),
    "PSRR": dict(indices=[1, 4],    names=["frequency", "vdb(vout)"], fallback=[1, 3]),
    "TRAN": dict(indices=[1, 3, 5], names=["time", "v(vout)", "v(vicm)"]),
    "STB":  dict(indices=[1, 4, 6], names=["frequency", "vdb(mb)", "phase_mb"]),
    "MC":   dict(indices=[1, 3],    names=["r", "v(diff_mis)"]),
}

# Shared Plotly layout defaults
_LAYOUT = dict(
    template="plotly_white",
    font=dict(family="Arial, sans-serif", size=13),
    title_font=dict(size=17, family="Arial, sans-serif"),
    hovermode="x unified",
    legend=dict(title_font_size=13, font_size=13,
                bordercolor="#CCCCCC", borderwidth=1),
    margin=dict(l=75, r=40, t=75, b=65),
)
_ANNOT_FONT = dict(size=13, family="Arial, sans-serif")
_ANNOT_BOX  = dict(bgcolor="white", bordercolor="#999999", borderwidth=1)


# =============================================================================
#  STEP 0 – Directories
# =============================================================================
def make_dirs():
    for tb in TB_NAMES:
        (OUTDIR / tb / "spice").mkdir(parents=True, exist_ok=True)
        (OUTDIR / tb / "csv_results").mkdir(parents=True, exist_ok=True)
    (OUTDIR / "IEEE_plots").mkdir(parents=True, exist_ok=True)
    print(f"[DIR] {OUTDIR.resolve()}\n")


# =============================================================================
#  STEP 1 – Netlist helpers
# =============================================================================
def read_source(p):
    if not p.exists(): sys.exit(f"[ERROR] Not found: {p.resolve()}")
    return p.read_text()

def split_netlist(c):
    mc = re.search(r'^\.control\s*$', c, re.MULTILINE | re.IGNORECASE)
    me = re.search(r'^\.endc\s*$',   c, re.MULTILINE | re.IGNORECASE)
    if not mc or not me: raise ValueError("No .control/.endc")
    return c[:mc.start()], c[mc.end():me.start()], c[me.end():]

def set_corner(c, corner):
    return re.sub(r'(\.lib\s+\S+sky130\.lib\.spice\s+)\S+',
                  r'\g<1>' + corner, c, flags=re.IGNORECASE)

def assemble(h, ctrl, f): return h + ".control\n" + ctrl + ".endc\n" + f


# =============================================================================
#  STEP 2 – Netlist generation
# =============================================================================
def _dc_ctrl(csv):
    return f"save all\nop\ndc v2 0 1.8 10m\nwrdata {csv} v(VICM) v(Vout)\n"

def _psrr_ctrl(csv):
    return f"save all\nop\nac dec 20 1 1e12\nwrdata {csv} frequency vdb(Vout)\n"

def _tran_ctrl(csv):
    return f"save all\nop\ntran 100u 10m 0.01m\nwrdata {csv} time v(Vout) v(VICM)\n"

def generate_dct_netlists(src, corner):
    h, _, f = split_netlist(src); h = set_corner(h, corner)
    out = {}
    for tb, fn in [("DC", _dc_ctrl), ("PSRR", _psrr_ctrl), ("TRAN", _tran_ctrl)]:
        csv = (OUTDIR / tb / "csv_results" /
               f"Rail_to_Rail_OTA_{corner}_{tb}.csv").resolve()
        out[tb] = assemble(h, fn(csv), f)
    return out

def generate_stb_netlist(src, corner):
    h, ctrl, f = split_netlist(src); h = set_corner(h, corner)
    csv  = (OUTDIR / "STB" / "csv_results" /
            f"Rail_to_Rail_OTA_{corner}_STB.csv").resolve()
    sdir = (OUTDIR / "STB" / "spice").resolve()
    lines, done = [], False
    for ln in ctrl.split('\n'):
        s = ln.strip()
        if re.match(r'write\s+OTA_STB_TB_\{', s, re.IGNORECASE):
            lines.append(f' write {sdir}/OTA_STB_TB_{corner}_{{$run}}.raw'); continue
        if re.match(r'\s*plot\s+', ln):
            lines.append(f'*{ln}'); continue
        lines.append(ln)
        if not done and re.search(r'let\s+phase_mb\s*=', s, re.IGNORECASE):
            lines.append(f' wrdata {csv} frequency vdb(mb) phase_mb'); done = True
    return assemble(h, '\n'.join(lines), f)

def generate_mc_netlist(src):
    h, ctrl, f = split_netlist(src); h = set_corner(h, MC_CORNER)
    csv = (OUTDIR / "MC" / "csv_results" /
           "Rail_to_Rail_OTA_tt_mm_MC.csv").resolve()
    raw = (OUTDIR / "MC" / "spice" /
           "Rail_to_Rail_OTA_tt_mm_MC.raw").resolve()
    ctrl = re.sub(r'/home/\S+?\.raw\b', str(raw),    ctrl)
    ctrl = re.sub(r'/home/\S+?\.txt\b', '/dev/null', ctrl)
    ctrl = re.sub(r'/home/\S+?\.csv\b', str(csv),    ctrl)
    ctrl = re.sub(r'^(\s*plot\s+)', r'*\1', ctrl, flags=re.MULTILINE)
    return assemble(h, ctrl, f)

def generate_all_netlists(corners=None):
    if corners is None: corners = CORNERS
    s_dct = read_source(SRC_DCT)
    s_stb = read_source(SRC_STB)
    s_mc  = read_source(SRC_MC)
    jobs = []
    for corner in corners:
        for tb, txt in generate_dct_netlists(s_dct, corner).items():
            fp = OUTDIR / tb / "spice" / f"Rail_to_Rail_OTA_{corner}_{tb}.spice"
            fp.write_text(txt); print(f"[GEN] {fp}"); jobs.append((fp, tb, corner))
        fp = OUTDIR / "STB" / "spice" / f"Rail_to_Rail_OTA_{corner}_STB.spice"
        fp.write_text(generate_stb_netlist(s_stb, corner))
        print(f"[GEN] {fp}"); jobs.append((fp, "STB", corner))
    fp = OUTDIR / "MC" / "spice" / "Rail_to_Rail_OTA_tt_mm_MC.spice"
    fp.write_text(generate_mc_netlist(s_mc))
    print(f"[GEN] {fp}"); jobs.append((fp, "MC", MC_CORNER))
    print(f"\n[GEN] {len(jobs)} netlists written.\n")
    return jobs


# =============================================================================
#  STEP 3 – Run ngspice
# =============================================================================
def run_ngspice(sp, tb, corner):
    lp = sp.with_suffix(".log")
    print(f"[RUN] {tb:4s} {corner:5s}  ->  {sp.name}")
    with open(lp, "w") as lg:
        r = subprocess.run([NGSPICE, "-b", str(sp.name)],
                           cwd=str(sp.parent),
                           stdout=lg, stderr=subprocess.STDOUT)
    ok = r.returncode == 0
    print(f"       [{'OK ' if ok else 'ERR'}]  log -> {lp}")
    if not ok:
        for ln in lp.read_text().splitlines()[-15:]: print(f"        {ln}")
    return ok

def run_all_simulations(jobs):
    print("=" * 70 + "\n  SIMULATION PHASE\n" + "=" * 70)
    failed = [f"{tb}/{c}" for sp, tb, c in jobs if not run_ngspice(sp, tb, c)]
    print()
    if failed: print(f"[WARN] Failed: {', '.join(failed)}")
    else:      print(f"[OK]  All {len(jobs)} done.")
    print()


# =============================================================================
#  STEP 4 – CSV parsing
# =============================================================================
def parse_ngspice_csv(fp):
    fp = pathlib.Path(fp)
    if not fp.exists():       print(f"  [WARN] Missing: {fp}"); return None
    if fp.stat().st_size == 0: print(f"  [WARN] Empty: {fp}");  return None
    tokens, n_cols = [], None
    for ln in fp.read_text(errors="replace").splitlines():
        ln = ln.strip()
        if not ln: continue
        vals, ok = [], True
        for t in ln.split():
            try: vals.append(float(t))
            except ValueError: ok = False; break
        if ok:
            if n_cols is None: n_cols = len(vals)
            tokens.extend(vals)
    if not tokens: print(f"  [WARN] No data: {fp.name}"); return None
    nc = n_cols or 1; total = len(tokens); trim = total % nc
    if trim: tokens = tokens[:total - trim]
    arr = np.array(tokens).reshape(-1, nc)
    df  = pd.DataFrame(arr, columns=[f"col_{i}" for i in range(nc)])
    print(f"  [RAW] {fp.name}: {df.shape[0]} rows x {nc} raw cols")
    return df

def _apply_tb_extract(df, tb):
    if df is None: return None
    spec = _TB_EXTRACT[tb]; idx = spec["indices"]; names = spec["names"]
    if max(idx) >= len(df.columns) and "fallback" in spec:
        idx = spec["fallback"]; print(f"  [INFO] {tb}: using fallback {idx}")
    if max(idx) >= len(df.columns):
        print(f"  [WARN] {tb}: index OOB ({len(df.columns)} cols)"); return None
    out = df.iloc[:, idx].copy(); out.columns = names
    print(f"  [CSV] cols {idx} -> {names}")
    return out

def load_all_csvs(corners=None):
    if corners is None: corners = CORNERS
    print("=" * 70 + "\n  CSV PARSING PHASE\n" + "=" * 70)
    data = {}
    for tb in ["DC", "PSRR", "TRAN", "STB"]:
        data[tb] = {}
        for c in corners:
            fp = OUTDIR / tb / "csv_results" / f"Rail_to_Rail_OTA_{c}_{tb}.csv"
            data[tb][c] = _apply_tb_extract(parse_ngspice_csv(fp), tb)
    data["MC"] = {}
    fp = OUTDIR / "MC" / "csv_results" / "Rail_to_Rail_OTA_tt_mm_MC.csv"
    data["MC"][MC_CORNER] = _apply_tb_extract(parse_ngspice_csv(fp), "MC")
    print()
    return data


# =============================================================================
#  STEP 5 – Shared plot helpers
# =============================================================================
def _ls(corner, width=2.5):
    return dict(color=CORNER_COLOR.get(corner, "#333"),
                dash=CORNER_DASH.get(corner, "solid"), width=width)

def _log_interp(x_query, xdata, ydata):
    return float(np.interp(np.log10(x_query), np.log10(xdata), ydata))

def _stb_metrics(df):
    freq  = df["frequency"].values
    gain  = df["vdb(mb)"].values
    phase = df["phase_mb"].values
    dc_gain = gain[0]
    idx = np.where(np.diff(np.sign(gain)) < 0)[0]
    if len(idx):
        i = idx[0]; log_f = np.log10(freq)
        f_ugf = 10 ** (np.interp(0, [gain[i+1], gain[i]], [log_f[i+1], log_f[i]]))
        pm    = float(np.interp(np.log10(f_ugf), log_f, phase)) + 180
        return f_ugf, pm, dc_gain
    return None, None, dc_gain


# =============================================================================
#  STEP 6 – Plotly plots
# =============================================================================

def plot_dc(data, corners):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["V(out) vs V(ICM)  —  DC Transfer",
                        "Offset = V(out) - V(ICM)"],
        shared_xaxes=True, vertical_spacing=0.14,
    )
    fig.add_trace(go.Scatter(x=[0, 1.8], y=[0, 1.8], name="Ideal (y=x)",
        line=dict(color="#AAAAAA", dash="dash", width=1.5)), row=1, col=1)
    for corner in corners:
        df = data["DC"].get(corner)
        if df is None: continue
        x = df["v(vicm)"]; y = df["v(vout)"]
        fig.add_trace(go.Scatter(x=x, y=y, name=corner, legendgroup=corner,
            line=_ls(corner),
            hovertemplate=f"<b>{corner}</b><br>VICM=%{{x:.3f}} V<br>Vout=%{{y:.3f}} V<extra></extra>"),
            row=1, col=1)
        fig.add_trace(go.Scatter(x=x, y=(y - x) * 1e3, name=corner,
            legendgroup=corner, line=_ls(corner), showlegend=False,
            hovertemplate=f"<b>{corner}</b><br>VICM=%{{x:.3f}} V<br>Offset=%{{y:.2f}} mV<extra></extra>"),
            row=2, col=1)
    fig.update_xaxes(title_text="V(ICM)  [V]", tickfont_size=13, row=2, col=1)
    fig.update_yaxes(title_text="V(out)  [V]",  tickfont_size=13, row=1, col=1)
    fig.update_yaxes(title_text="Offset  [mV]", tickfont_size=13, row=2, col=1)
    fig.update_layout(title="Rail-to-Rail OTA  —  DC Transfer Characteristic",
                      **_LAYOUT)
    fig.write_html(str(OUTDIR / "DC" / "DC_cross_corner.html"))
    print(f"[PLOT] DC_cross_corner.html")


def plot_psrr(data, corners):
    fig = go.Figure()
    dc_lines  = ["<b>DC PSRR  (@ lowest freq)</b>"]
    mhz_lines = ["<b>PSRR  @ 1 MHz</b>"]

    for corner in corners:
        df = data["PSRR"].get(corner)
        if df is None: continue
        freq = df["frequency"].values; vdb = df["vdb(vout)"].values
        fig.add_trace(go.Scatter(x=freq, y=vdb, name=corner,
            line=_ls(corner), mode="lines",
            hovertemplate=f"<b>{corner}</b><br>f=%{{x:.2e}} Hz<br>PSRR=%{{y:.1f}} dB<extra></extra>"))
        dc_lines.append(f"  {corner}: {vdb[0]:.1f} dB")
        mhz_lines.append(f"  {corner}: {_log_interp(1e6, freq, vdb):.1f} dB")

    fig.add_vline(x=1e6, line_dash="dash", line_color="#555555", line_width=1.5,
                  annotation_text="1 MHz", annotation_font_size=14,
                  annotation_position="top right")

    combined = dc_lines + [""] + mhz_lines
    fig.add_annotation(x=0.02, y=0.04, xref="paper", yref="paper",
        xanchor="left", yanchor="bottom", showarrow=False, align="left",
        text="<br>".join(combined), font=dict(size=14, family="Arial, sans-serif"),
        **_ANNOT_BOX)

    fig.update_xaxes(title_text="Frequency  [Hz]", type="log",
                     tickfont_size=13, showgrid=True)
    fig.update_yaxes(title_text="V(out)/V(DD)  [dB]  (lower = better)",
                     tickfont_size=13, showgrid=True)
    fig.update_layout(title="Rail-to-Rail OTA  —  PSRR", **_LAYOUT)
    fig.write_html(str(OUTDIR / "PSRR" / "PSRR_cross_corner.html"))
    print(f"[PLOT] PSRR_cross_corner.html")


def plot_tran(data, corners):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["V(out) & V(ICM)  —  Transient",
                        "Offset = V(out) - V(ICM)"],
        shared_xaxes=True, vertical_spacing=0.14,
    )
    for corner in corners:
        df = data["TRAN"].get(corner)
        if df is None: continue
        t = df["time"] * 1e3
        vout = df["v(vout)"]; vicm = df["v(vicm)"]
        sty = _ls(corner)
        fig.add_trace(go.Scatter(x=t, y=vout, name=f"Vout ({corner})",
            legendgroup=corner, line=sty,
            hovertemplate=f"<b>Vout {corner}</b><br>t=%{{x:.3f}} ms<br>V=%{{y:.4f}} V<extra></extra>"),
            row=1, col=1)
        fig.add_trace(go.Scatter(x=t, y=vicm, name=f"VICM ({corner})",
            legendgroup=corner,
            line=dict(color=sty["color"], dash="dot", width=1.5),
            hovertemplate=f"<b>VICM {corner}</b><br>t=%{{x:.3f}} ms<br>V=%{{y:.4f}} V<extra></extra>"),
            row=1, col=1)
        fig.add_trace(go.Scatter(x=t, y=(vout - vicm) * 1e3, name=corner,
            legendgroup=corner, line=sty, showlegend=False,
            hovertemplate=f"<b>{corner}</b><br>t=%{{x:.3f}} ms<br>Offset=%{{y:.2f}} mV<extra></extra>"),
            row=2, col=1)
    fig.update_xaxes(title_text="Time  [ms]",    tickfont_size=13, row=2, col=1)
    fig.update_yaxes(title_text="Voltage  [V]",  tickfont_size=13, row=1, col=1)
    fig.update_yaxes(title_text="Offset  [mV]",  tickfont_size=13, row=2, col=1)
    fig.update_layout(title="Rail-to-Rail OTA  —  Transient Response", **_LAYOUT)
    fig.write_html(str(OUTDIR / "TRAN" / "TRAN_cross_corner.html"))
    print(f"[PLOT] TRAN_cross_corner.html")


def plot_stb(data, corners):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=["Loop Gain  [dB]", "Phase  [deg]"],
        shared_xaxes=True, vertical_spacing=0.12,
    )
    metric_lines = ["<b>Corner &nbsp; UGF &nbsp;&nbsp;&nbsp; PM &nbsp;&nbsp; DC Gain</b>"]

    for corner in corners:
        df = data["STB"].get(corner)
        if df is None: continue
        sty  = _ls(corner)
        freq = df["frequency"]; gain = df["vdb(mb)"]; ph = df["phase_mb"]
        fig.add_trace(go.Scatter(x=freq, y=gain, name=corner, legendgroup=corner,
            line=sty,
            hovertemplate=f"<b>{corner}</b><br>f=%{{x:.2e}} Hz<br>Gain=%{{y:.2f}} dB<extra></extra>"),
            row=1, col=1)
        fig.add_trace(go.Scatter(x=freq, y=ph, name=corner, legendgroup=corner,
            line=sty, showlegend=False,
            hovertemplate=f"<b>{corner}</b><br>f=%{{x:.2e}} Hz<br>Phase=%{{y:.1f}} deg<extra></extra>"),
            row=2, col=1)
        ugf, pm, dc = _stb_metrics(df)
        if ugf:
            metric_lines.append(
                f"  {corner}: &nbsp; {ugf/1e6:.2f} MHz &nbsp; {pm:.1f}° &nbsp; {dc:.1f} dB")

    fig.add_hline(y=0,    line_dash="dash", line_color="#888888", line_width=1.2,
                  annotation_text="0 dB", annotation_font_size=14,
                  annotation_position="right", row=1, col=1)
    fig.add_hline(y=-180, line_dash="dash", line_color="#888888", line_width=1.2,
                  annotation_text="-180°", annotation_font_size=14,
                  annotation_position="right", row=2, col=1)

    fig.add_annotation(x=0.01, y=0.98, xref="paper", yref="paper",
        xanchor="left", yanchor="top", showarrow=False, align="left",
        text="<br>".join(metric_lines),
        font=dict(size=14, family="Arial, sans-serif"), **_ANNOT_BOX)

    # KEY: set log scale on ALL x-axes (shared_xaxes needs this globally)
    fig.update_xaxes(type="log", showgrid=True, tickfont_size=13,
                     tickformat=".0e")
    fig.update_xaxes(title_text="Frequency  [Hz]", row=2, col=1)
    fig.update_yaxes(title_text="Gain  [dB]",  showgrid=True,
                     tickfont_size=13, row=1, col=1)
    fig.update_yaxes(title_text="Phase  [deg]", showgrid=True,
                     tickfont_size=13, row=2, col=1)
    fig.update_layout(title="Rail-to-Rail OTA  —  Stability (Bode Plot)", **_LAYOUT)
    fig.write_html(str(OUTDIR / "STB" / "STB_cross_corner.html"))
    print(f"[PLOT] STB_cross_corner.html")


def plot_mc(data):
    df = data["MC"].get(MC_CORNER)
    if df is None: print("[PLOT] MC: no data, skipping."); return

    vals  = df["v(diff_mis)"].values * 1e3
    mu    = float(vals.mean())
    sigma = float(vals.std())
    var   = float(vals.var())
    n     = len(vals)

    fig = go.Figure()

    for k, color, alpha in [(3, "#FF4444", 0.08), (2, "#FFAA00", 0.12), (1, "#22BB22", 0.18)]:
        fig.add_vrect(x0=mu - k*sigma, x1=mu + k*sigma,
                      fillcolor=color, opacity=alpha, line_width=0,
                      annotation_text=f"±{k}σ",
                      annotation_font_size=15,
                      annotation_position="top left")

    fig.add_trace(go.Histogram(x=vals, nbinsx=max(20, n // 8),
        marker=dict(color=CORNER_COLOR["tt_mm"],
                    line=dict(color="white", width=0.5)),
        opacity=0.88, name="Offset distribution",
        hovertemplate="Bin: %{x:.3f} mV<br>Count: %{y}<extra></extra>"))

    vline_specs = [
        (mu,          "solid",       "#000000", f"μ={mu:.3f} mV"),
        (mu + sigma,  "dot",         "#22BB22", f"+1σ"),
        (mu - sigma,  "dot",         "#22BB22", f"−1σ"),
        (mu + 2*sigma,"dash",        "#FF8800", f"+2σ"),
        (mu - 2*sigma,"dash",        "#FF8800", f"−2σ"),
        (mu + 3*sigma,"longdashdot", "#FF4444", f"+3σ"),
        (mu - 3*sigma,"longdashdot", "#FF4444", f"−3σ"),
    ]
    for xv, dash, col, label in vline_specs:
        fig.add_vline(x=xv, line_dash=dash, line_color=col, line_width=2.0,
                      annotation_text=label,
                      annotation_font_size=13,
                      annotation_font_color=col,
                      annotation_position="top")

    stats_text = (
        f"<b>Statistics  (N={n})</b><br>"
        f"Mean  μ  =  {mu:.3f} mV<br>"
        f"Std   σ  =  {sigma:.3f} mV<br>"
        f"Var   σ² =  {var*1e3:.3f} μV²<br>"
        f"<br>"
        f"±1σ:  [{mu-sigma:.3f},  {mu+sigma:.3f}] mV<br>"
        f"±2σ:  [{mu-2*sigma:.3f},  {mu+2*sigma:.3f}] mV<br>"
        f"±3σ:  [{mu-3*sigma:.3f},  {mu+3*sigma:.3f}] mV"
    )
    fig.add_annotation(x=0.98, y=0.98, xref="paper", yref="paper",
        xanchor="right", yanchor="top", showarrow=False, align="left",
        text=stats_text, font=dict(size=14, family="Arial, sans-serif"),
        **_ANNOT_BOX)

    fig.update_xaxes(title_text="Input-Referred Offset Voltage  [mV]",
                     tickfont_size=13, showgrid=True, zeroline=True)
    fig.update_yaxes(title_text="Count", tickfont_size=13, showgrid=True)
    fig.update_layout(
        title=(f"Rail-to-Rail OTA  —  Monte Carlo Offset  (tt_mm)  "
               f"N={n},  μ={mu:.3f} mV,  σ={sigma:.3f} mV"),
        **_LAYOUT, showlegend=False)
    fig.write_html(str(OUTDIR / "MC" / "MC_offset_histogram.html"))
    print(f"[PLOT] MC_offset_histogram.html")


# =============================================================================
#  STEP 7 – IEEE paper-style plots  (matplotlib, 300 DPI PNG + PDF)
# =============================================================================
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib.lines import Line2D
    _MPL_OK = True
except ImportError:
    _MPL_OK = False

_COL1 = 3.5   # IEEE single-column width (inches)

_IEEE_RC = {
    'font.family':        'serif',
    'font.serif':         ['Liberation Serif', 'DejaVu Serif', 'Times New Roman'],
    'font.size':          8,          # base body text
    'axes.labelsize':     8,          # x/y axis labels
    'axes.titlesize':     8,
    'xtick.labelsize':    7,          # tick numbers
    'ytick.labelsize':    7,
    'legend.fontsize':    6.5,        # legend text
    'legend.framealpha':  0.88,
    'legend.edgecolor':   '#BBBBBB',
    'legend.handlelength':1.6,
    'legend.handletextpad':0.4,
    'legend.columnspacing':0.8,
    'lines.linewidth':    1.2,
    'axes.linewidth':     0.7,
    'xtick.major.width':  0.7,
    'ytick.major.width':  0.7,
    'xtick.minor.width':  0.4,
    'ytick.minor.width':  0.4,
    'xtick.major.size':   3.5,
    'ytick.major.size':   3.5,
    'xtick.minor.size':   2.0,
    'ytick.minor.size':   2.0,
    'xtick.direction':    'in',
    'ytick.direction':    'in',
    'xtick.top':          True,
    'ytick.right':        True,
    'axes.grid':          True,
    'grid.linewidth':     0.35,
    'grid.alpha':         0.40,
    'grid.color':         '#AAAAAA',
    'figure.dpi':         150,
    'savefig.dpi':        300,
    'savefig.bbox':       'tight',
    'savefig.pad_inches': 0.03,
    'pdf.fonttype':       42,         # embed TrueType in PDF (needed for LaTeX)
    'ps.fonttype':        42,
}

_MPL_STYLE = {
    "tt": dict(color="#0055FF", ls="-",           lw=1.3, label="tt"),
    "ss": dict(color="#FF2200", ls=":",           lw=1.4, label="ss"),
    "ff": dict(color="#00BB00", ls="--",          lw=1.3, label="ff"),
    "fs": dict(color="#FF8800", ls="-.",          lw=1.3, label="fs"),
    "sf": dict(color="#CC00FF", ls=(0,(4,1,1,1)), lw=1.3, label="sf"),
}


def _ieee_save(fig, name, outdir):
    for ext in ("png", "pdf"):
        fig.savefig(str(outdir / f"{name}.{ext}"))
    plt.close(fig)
    print(f"  [IEEE] {name}.png / .pdf")


def generate_ieee_plots(data, corners):
    if not _MPL_OK:
        print("[SKIP] matplotlib unavailable – no IEEE plots."); return

    outdir = OUTDIR / "IEEE_plots"
    outdir.mkdir(parents=True, exist_ok=True)
    matplotlib.rcParams.update(_IEEE_RC)

    print("=" * 70 + "\n  IEEE PLOT GENERATION\n" + "=" * 70)

    # ── DC ───────────────────────────────────────────────────────────────────
    if any(data["DC"].get(c) is not None for c in corners):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(_COL1, 4.0),
                                        sharex=True,
                                        gridspec_kw=dict(hspace=0.08))
        ax1.plot([0, 1.8], [0, 1.8], color="#AAAAAA", ls="--", lw=0.9,
                 label="Ideal ($y=x$)", zorder=0)
        for c in corners:
            df = data["DC"].get(c)
            if df is None: continue
            x = df["v(vicm)"].values; y = df["v(vout)"].values
            ax1.plot(x, y, **_MPL_STYLE[c])
            ax2.plot(x, (y - x) * 1e3, **_MPL_STYLE[c])
        ax1.set_ylabel("$V_{out}$ [V]")
        ax1.legend(ncol=3, loc="upper left", handlelength=2.0)
        ax2.set_xlabel("$V_{ICM}$ [V]")
        ax2.set_ylabel("Offset [mV]")
        ax2.axhline(0, color="#AAAAAA", lw=0.7, ls="--")
        for ax in (ax1, ax2): ax.set_xlim(0, 1.8)
        _ieee_save(fig, "IEEE_DC", outdir)

    # ── PSRR ─────────────────────────────────────────────────────────────────
    if any(data["PSRR"].get(c) is not None for c in corners):
        fig, ax = plt.subplots(figsize=(_COL1, 2.8))
        for c in corners:
            df = data["PSRR"].get(c)
            if df is None: continue
            ax.semilogx(df["frequency"].values, df["vdb(vout)"].values,
                        **_MPL_STYLE[c])
        ax.axvline(1e6, color="#555555", ls="--", lw=0.9)
        ylims = ax.get_ylim()
        ax.text(1.15e6, ylims[0] + (ylims[1]-ylims[0])*0.04,
                "1 MHz", fontsize=6, color="#555555", va="bottom")
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("PSRR [$V_{out}/V_{DD}$] [dB]")
        ax.legend(ncol=5, loc="lower left", handlelength=1.8)
        ax.xaxis.set_major_formatter(ticker.LogFormatterSciNotation())
        _ieee_save(fig, "IEEE_PSRR", outdir)

    # ── TRAN ─────────────────────────────────────────────────────────────────
    if any(data["TRAN"].get(c) is not None for c in corners):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(_COL1, 4.0),
                                        sharex=True,
                                        gridspec_kw=dict(hspace=0.08))
        for c in corners:
            df = data["TRAN"].get(c)
            if df is None: continue
            t  = df["time"].values * 1e3
            vo = df["v(vout)"].values; vi = df["v(vicm)"].values
            sty = dict(_MPL_STYLE[c])
            ax1.plot(t, vo, **sty)
            sty2 = dict(sty); sty2["ls"] = ":"; sty2["lw"] = 0.9
            ax1.plot(t, vi, **sty2)
            ax2.plot(t, (vo - vi) * 1e3, **_MPL_STYLE[c])
        legend_elems = [
            Line2D([0],[0], color="#555", ls="-",  lw=1.0, label="$V_{out}$"),
            Line2D([0],[0], color="#555", ls=":",  lw=1.0, label="$V_{ICM}$"),
        ]
        corner_elems = [Line2D([0],[0], **dict(_MPL_STYLE[c]))
                        for c in corners if data["TRAN"].get(c) is not None]
        ax1.legend(handles=legend_elems + corner_elems, ncol=4,
                   loc="upper right", handlelength=1.8, fontsize=7)
        ax1.set_ylabel("Voltage [V]")
        ax2.set_xlabel("Time [ms]")
        ax2.set_ylabel("Offset [mV]")
        ax2.axhline(0, color="#AAAAAA", lw=0.7, ls="--")
        _ieee_save(fig, "IEEE_TRAN", outdir)

    # ── STB Bode ─────────────────────────────────────────────────────────────
    if any(data["STB"].get(c) is not None for c in corners):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(_COL1, 4.5),
                                        sharex=True,
                                        gridspec_kw=dict(hspace=0.08))
        for c in corners:
            df = data["STB"].get(c)
            if df is None: continue
            freq  = df["frequency"].values
            gain  = df["vdb(mb)"].values
            phase = df["phase_mb"].values
            ax1.semilogx(freq, gain,  **_MPL_STYLE[c])
            ax2.semilogx(freq, phase, **_MPL_STYLE[c])

        ax1.axhline(0,    color="#888", lw=0.8, ls="--")
        ax2.axhline(-180, color="#888", lw=0.8, ls="--")

        # Metrics table inset (compact, small font)
        rows = ["C   UGF      PM    A0"]
        for c in corners:
            df = data["STB"].get(c)
            if df is None: continue
            ugf, pm, dc = _stb_metrics(df)
            if ugf:
                rows.append(f"{c}  {ugf/1e6:.2f}M  {pm:.0f}  {dc:.0f}dB")
        ax1.text(0.02, 0.02, "\n".join(rows),
                 transform=ax1.transAxes, fontsize=5.5,
                 va="bottom", ha="left", family="monospace",
                 bbox=dict(boxstyle="square,pad=0.25", fc="white",
                           ec="#BBBBBB", lw=0.6))

        ax1.set_ylabel("Loop Gain [dB]")
        ax1.legend(ncol=5, loc="upper right", handlelength=1.8)
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Phase [°]")
        ax2.xaxis.set_major_formatter(ticker.LogFormatterSciNotation())
        for ax in (ax1, ax2):
            ax.set_xlim(1, 1e8)
            ax.xaxis.set_minor_locator(ticker.LogLocator(subs=range(2, 10)))
            ax.xaxis.set_minor_formatter(ticker.NullFormatter())
        _ieee_save(fig, "IEEE_STB", outdir)

    # ── MC Histogram ─────────────────────────────────────────────────────────
    df_mc = data["MC"].get(MC_CORNER)
    if df_mc is not None:
        vals  = df_mc["v(diff_mis)"].values * 1e3
        mu    = float(vals.mean())
        sigma = float(vals.std())
        n     = len(vals)

        fig, ax = plt.subplots(figsize=(_COL1, 2.8))
        for k, col, alp in [(3,"#FF4444",0.10),(2,"#FFAA00",0.14),(1,"#22BB22",0.20)]:
            ax.axvspan(mu - k*sigma, mu + k*sigma, color=col, alpha=alp, lw=0)

        ax.hist(vals, bins=max(20, n // 8), color=CORNER_COLOR["tt_mm"],
                edgecolor="white", linewidth=0.4, alpha=0.88)

        ax.axvline(mu,          color="black",  lw=1.1, ls="-",
                   label=f"$\\mu$={mu:.2f}")
        ax.axvline(mu + sigma,  color="#22BB22", lw=0.9, ls="--",
                   label=f"$\\pm\\sigma$={sigma:.2f}")
        ax.axvline(mu - sigma,  color="#22BB22", lw=0.9, ls="--")
        ax.axvline(mu + 2*sigma,color="#FF8800", lw=0.9, ls="-.",
                   label="$\\pm 2\\sigma$")
        ax.axvline(mu - 2*sigma,color="#FF8800", lw=0.9, ls="-.")
        ax.axvline(mu + 3*sigma,color="#FF4444", lw=0.9, ls=":",
                   label="$\\pm 3\\sigma$")
        ax.axvline(mu - 3*sigma,color="#FF4444", lw=0.9, ls=":")

        stats = (f"$N={n}$,  $\\mu={mu:.2f}$ mV\n"
                 f"$\\sigma={sigma:.3f}$ mV,  $\\sigma^2={sigma**2:.3f}$ mV$^2$")
        ax.text(0.97, 0.97, stats, transform=ax.transAxes,
                fontsize=6.0, va="top", ha="right",
                bbox=dict(boxstyle="square,pad=0.25", fc="white",
                          ec="#BBBBBB", lw=0.6))
        ax.legend(loc="upper left", ncol=2, handlelength=1.4,
                  fontsize=6.0, borderpad=0.4)
        ax.set_xlabel("Input-Referred Offset [mV]")
        ax.set_ylabel("Count")
        _ieee_save(fig, "IEEE_MC", outdir)

    print(f"  -> IEEE plots in: {outdir.resolve()}")


# =============================================================================
#  STEP 8 – Orchestration
# =============================================================================
def plot_all(data, corners):
    print("=" * 70 + "\n  PLOTTING PHASE\n" + "=" * 70)
    plot_dc(data, corners)
    plot_psrr(data, corners)
    plot_tran(data, corners)
    plot_stb(data, corners)
    plot_mc(data)
    generate_ieee_plots(data, corners)   # <-- defined above, no ordering issue
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--generate-only", action="store_true",
                   help="Write SPICE netlists only, do not simulate or plot.")
    p.add_argument("--plot-only",     action="store_true",
                   help="Replot from existing CSVs; skip generation and simulation.")
    p.add_argument("--corners", nargs="+", default=CORNERS, choices=CORNERS,
                   help=f"Corners to process. Default: all {CORNERS}")
    args = p.parse_args()
    if args.generate_only and args.plot_only:
        sys.exit("[ERROR] --generate-only and --plot-only are mutually exclusive.")

    corners = args.corners
    make_dirs()

    if not args.plot_only:
        print("=" * 70 + "\n  NETLIST GENERATION PHASE\n" + "=" * 70)
        jobs = generate_all_netlists(corners)
        if not args.generate_only:
            run_all_simulations(jobs)

    if not args.generate_only:
        data = load_all_csvs(corners)
        plot_all(data, corners)

        print("=" * 70)
        print("  HOW TO VIEW RESULTS")
        print("=" * 70)
        print()
        print("  Interactive Plotly plots (open in Firefox/Chrome):")
        for tb in TB_NAMES:
            for h in sorted((OUTDIR / tb).glob("*.html")):
                print(f"    firefox {h} &")
        print()
        print(f"  IEEE PNG/PDF figures:")
        ieee_dir = OUTDIR / "IEEE_plots"
        for img in sorted(ieee_dir.glob("*.png")):
            print(f"    {img}")
        print()


if __name__ == "__main__":
    main()
