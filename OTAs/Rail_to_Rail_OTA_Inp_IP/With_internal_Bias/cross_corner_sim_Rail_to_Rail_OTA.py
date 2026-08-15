#!/usr/bin/env python3
"""
Cross-Corner Simulation Automation Script
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Design  : Rail_to_Rail_IP_OP_OTA_with_Internal_Bias
PDK     : SKY130 (SkyWater 130nm)
Tool    : ngspice (batch mode)

Testbenches handled
  DC   ─ DC transfer curve  (VICM swept 0→1.8 V, unity-gain buffer)
  PSRR ─ Power-supply rejection (AC, 1 Hz → 1 THz, VDD ac=1)
  TRAN ─ Transient response (1 kHz sine on VICM, 10 ms window)
  STB  ─ Loop-gain / stability (Middlebrook double-injection)
  MC   ─ Offset voltage Monte Carlo (1000 runs, tt_mm corner)

Usage
  python3 cross_corner_sim_Rail_to_Rail_OTA.py                  # full flow
  python3 cross_corner_sim_Rail_to_Rail_OTA.py --generate-only  # netlists only
  python3 cross_corner_sim_Rail_to_Rail_OTA.py --plot-only       # parse+plot
  python3 cross_corner_sim_Rail_to_Rail_OTA.py --corners tt ss   # subset
  python3 cross_corner_sim_Rail_to_Rail_OTA.py --mc-runs 200     # fewer MC runs
"""

# ============================================================
# 1. IMPORTS + USER CONFIGURATION
# ============================================================
import argparse
import pathlib
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Source SPICE files (place next to this script, or update paths) ──────────
SRC_DC_TRAN_PSRR = pathlib.Path(
    "tb_Rail_to_Rail_IP_OP_OTA_int_bias_DC_TRAN_PSRR.spice"
)
SRC_STB = pathlib.Path(
    "tb_Rail_to_Rail_IP_OP_OTA_int_bias_STB.spice"
)
SRC_MC = pathlib.Path(
    "tb_Rail_to_Rail_IP_OP_OTA_int_bias_MC.spice"
)

# ── Output root ───────────────────────────────────────────────────────────────
DESIGN_NAME = "Rail_to_Rail_IP_OP_OTA_int_bias"
OUT_ROOT    = pathlib.Path(f"{DESIGN_NAME}_Sims")

# ── Simulation settings ───────────────────────────────────────────────────────
MC_RUNS     = 1000          # number of Monte Carlo runs
MC_PARALLEL = 8             # parallel ngspice workers for MC
SIM_TIMEOUT = 300           # seconds; increase for slow machines

# ── SKY130 corners (DO NOT add tt_mm here; it is MC-only) ────────────────────
ALL_CORNERS = ["tt", "ss", "ff", "fs", "sf"]
MC_CORNER   = "tt_mm"

# ============================================================
# 2. CORNER COLORS, DASH STYLES, TB EXTRACTION TABLE
# ============================================================
CORNER_COLOR = {
    "tt"   : "#0055FF",
    "ss"   : "#FF2200",
    "ff"   : "#00BB00",
    "fs"   : "#FF8800",
    "sf"   : "#CC00FF",
    "tt_mm": "#00AAAA",
}

CORNER_DASH = {
    "tt"   : "solid",
    "ss"   : "dot",
    "ff"   : "dash",
    "fs"   : "dashdot",
    "sf"   : "longdash",
    "tt_mm": "solid",
}

# ngspice wrdata raw-column extraction (0-indexed)
#   Real vector   → 2 raw cols  [scale, value]
#   Complex vector → 3 raw cols  [scale, real, imag]   (frequency in AC)
_TB_EXTRACT = {
    "dc"  : {"indices": [1, 3],    "names": ["input_v",   "output_v"]},
    "psrr": {"indices": [1, 4],    "names": ["frequency", "vdb_out"]},   # 5-col; 4-col fallback below
    "tran": {"indices": [1, 3, 5], "names": ["time",      "v_out", "v_in"]},
    "stb" : {"indices": [1, 4, 6], "names": ["frequency", "vdb_mb", "phase_mb"]},
    "mc"  : {"indices": [1],       "names": ["v_diff_mis"]},
}

# ============================================================
# 3. DIRECTORY STRUCTURE
# ============================================================
def make_dirs() -> dict:
    """Create the output directory tree and return a path registry."""
    dirs = {}
    for tb in ("DC", "PSRR", "TRAN", "STB", "MC"):
        sp = OUT_ROOT / tb / "spice"
        cv = OUT_ROOT / tb / "csv_results"
        sp.mkdir(parents=True, exist_ok=True)
        cv.mkdir(parents=True, exist_ok=True)
        dirs[tb.lower()] = {"spice": sp, "csv": cv}
    ieee = OUT_ROOT / "IEEE_plots"
    ieee.mkdir(parents=True, exist_ok=True)
    dirs["ieee"] = ieee
    return dirs

# ============================================================
# 4. NETLIST HELPERS
# ============================================================
def read_source(filepath: pathlib.Path) -> str:
    return filepath.read_text(errors="replace")


def split_netlist(text: str):
    """
    Split a SPICE netlist into (preamble, control_lines, postamble).

    Returns
    -------
    preamble      : str   – everything before .control
    control_lines : list  – lines INSIDE .control / .endc (exclusive)
    postamble     : str   – everything after .endc
    """
    lines = text.splitlines(keepends=True)
    ctrl_start = ctrl_end = None
    for i, ln in enumerate(lines):
        s = ln.strip().lower()
        if s.startswith(".control") and ctrl_start is None:
            ctrl_start = i
        elif s.startswith(".endc") and ctrl_start is not None:
            ctrl_end = i
            break

    if ctrl_start is None or ctrl_end is None:
        raise ValueError("Could not locate .control / .endc block in netlist.")

    preamble      = "".join(lines[:ctrl_start])
    control_lines = lines[ctrl_start + 1 : ctrl_end]
    postamble     = "".join(lines[ctrl_end + 1 :])
    return preamble, control_lines, postamble


def set_corner(text: str, corner: str) -> str:
    """Replace the SKY130 lib corner string."""
    return re.sub(
        r'(\.lib\s+\S+sky130\.lib\.spice\s+)\S+',
        r'\g<1>' + corner,
        text,
        flags=re.IGNORECASE,
    )


def assemble(preamble: str, control_lines: list, postamble: str) -> str:
    """Re-assemble preamble + new control block + postamble."""
    ctrl_block = ".control\n" + "".join(control_lines) + ".endc\n"
    return preamble + ctrl_block + postamble

# ============================================================
# 5. CORNER NETLIST GENERATORS  (DC / PSRR / TRAN / STB)
# ============================================================

# ── DC ──────────────────────────────────────────────────────
def _gen_dc_control(csv_path: pathlib.Path) -> list:
    """DC transfer: sweep VICM (V2) 0→1.8 V."""
    csv_abs = str(csv_path.resolve())
    return [
        "save all\n",
        "op\n",
        "dc v2 0 1.8 10m\n",
        f"wrdata {csv_abs} v(VICM) v(Vout)\n",
    ]


def generate_dc_netlists(dirs: dict, corner_list: list, src_text: str) -> dict:
    paths = {}
    preamble, _, postamble = split_netlist(src_text)
    for corner in corner_list:
        csv_path = dirs["dc"]["csv"] / f"dc_{corner}.csv"
        ctrl     = _gen_dc_control(csv_path)
        netlist  = set_corner(assemble(preamble, ctrl, postamble), corner)
        sp_file  = dirs["dc"]["spice"] / f"dc_{corner}.spice"
        sp_file.write_text(netlist)
        paths[corner] = (sp_file, csv_path)
    return paths


# ── PSRR ────────────────────────────────────────────────────
def _gen_psrr_control(csv_path: pathlib.Path) -> list:
    """AC PSRR: VDD has ac=1, sweep 1 Hz → 1 THz."""
    csv_abs = str(csv_path.resolve())
    return [
        "save all\n",
        "op\n",
        "ac dec 20 1 1e12\n",
        f"wrdata {csv_abs} frequency vdb(Vout)\n",
    ]


def generate_psrr_netlists(dirs: dict, corner_list: list, src_text: str) -> dict:
    paths = {}
    preamble, _, postamble = split_netlist(src_text)
    for corner in corner_list:
        csv_path = dirs["psrr"]["csv"] / f"psrr_{corner}.csv"
        ctrl     = _gen_psrr_control(csv_path)
        netlist  = set_corner(assemble(preamble, ctrl, postamble), corner)
        sp_file  = dirs["psrr"]["spice"] / f"psrr_{corner}.spice"
        sp_file.write_text(netlist)
        paths[corner] = (sp_file, csv_path)
    return paths


# ── TRAN ────────────────────────────────────────────────────
def _gen_tran_control(csv_path: pathlib.Path) -> list:
    """Transient: 1 kHz sine on VICM, 10 ms window (no uic)."""
    csv_abs = str(csv_path.resolve())
    return [
        "save all\n",
        "op\n",
        "tran 100u 10m 0.01m\n",
        f"wrdata {csv_abs} time v(Vout) v(VICM)\n",
    ]


def generate_tran_netlists(dirs: dict, corner_list: list, src_text: str) -> dict:
    paths = {}
    preamble, _, postamble = split_netlist(src_text)
    for corner in corner_list:
        csv_path = dirs["tran"]["csv"] / f"tran_{corner}.csv"
        ctrl     = _gen_tran_control(csv_path)
        netlist  = set_corner(assemble(preamble, ctrl, postamble), corner)
        sp_file  = dirs["tran"]["spice"] / f"tran_{corner}.spice"
        sp_file.write_text(netlist)
        paths[corner] = (sp_file, csv_path)
    return paths


# ── STB ─────────────────────────────────────────────────────
def _modify_stb_control(
    control_lines: list,
    corner: str,
    csv_path: pathlib.Path,
) -> list:
    """
    Apply the three STB-specific modifications to the original control lines:
      1. Comment out all  plot ...  lines
      2. Redirect  write <file>.raw  to a corner-tagged filename (CWD-relative)
      3. Inject    wrdata <csv> frequency vdb(mb) phase_mb  after  let phase_mb = ...
    Everything else is preserved verbatim (dowhile, alter, meas, etc.).
    """
    new_lines   = []
    csv_abs     = str(csv_path.resolve())
    phase_done  = False

    for line in control_lines:
        stripped = line.strip()

        # 1) Comment out plot commands
        if re.match(r'plot\s+', stripped, re.IGNORECASE):
            new_lines.append("*" + line if not line.startswith("*") else line)
            continue

        # 2) Redirect write .raw lines (keep {$run} token intact)
        m = re.match(r'(\s*write\s+)(\S+)', line, re.IGNORECASE)
        if m:
            orig_fname = pathlib.Path(m.group(2)).name      # strip any existing dir
            base       = re.sub(r'\.raw$', '', orig_fname, flags=re.IGNORECASE)
            new_fname  = f"{base}_{corner}.raw"
            new_lines.append(f"{m.group(1)}{new_fname}\n")
            continue

        # 3) Inject wrdata after  let phase_mb = ...
        if (re.search(r'let\s+phase_mb\s*=', stripped, re.IGNORECASE)
                and not phase_done):
            new_lines.append(line)
            new_lines.append(
                f" wrdata {csv_abs} frequency vdb(mb) phase_mb\n"
            )
            phase_done = True
            continue

        new_lines.append(line)

    return new_lines


def generate_stb_netlists(dirs: dict, corner_list: list, src_text: str) -> dict:
    paths = {}
    preamble, control_lines, postamble = split_netlist(src_text)
    for corner in corner_list:
        csv_path  = dirs["stb"]["csv"] / f"stb_{corner}.csv"
        ctrl      = _modify_stb_control(control_lines, corner, csv_path)
        netlist   = set_corner(assemble(preamble, ctrl, postamble), corner)
        sp_file   = dirs["stb"]["spice"] / f"stb_{corner}.spice"
        sp_file.write_text(netlist)
        paths[corner] = (sp_file, csv_path)
    return paths

# ============================================================
# 6. MC NETLIST GENERATOR  (single-run; MUST be defined before run_mc_simulations)
# ============================================================
def generate_mc_single_run(
    run_idx: int,
    dirs: dict,
    src_text: str,
) -> tuple:
    """
    Generate one MC netlist for a SINGLE op run using the tt_mm corner.

    SKY130 tt_mm corner: agauss() in the PDK is re-evaluated at parse time
    for each new ngspice process → each separate process gets a fresh random
    mismatch draw from the OS RNG seed.  No dowhile+reset needed.

    Returns (spice_path, csv_path).
    """
    csv_path = dirs["mc"]["csv"] / "mc_results.csv"
    csv_abs  = str(csv_path.resolve())

    preamble, _, postamble = split_netlist(src_text)

    ctrl_lines = [
        "save all\n",
        "op\n",
        "let DIFF_MIS = v(VICM) - v(Vout)\n",
        "set appendwrite\n",
        f"wrdata {csv_abs} v(DIFF_MIS)\n",
    ]

    netlist = set_corner(assemble(preamble, ctrl_lines, postamble), MC_CORNER)
    sp_file = dirs["mc"]["spice"] / f"mc_run_{run_idx:04d}.spice"
    sp_file.write_text(netlist)
    return sp_file, csv_path

# ============================================================
# 7. GENERATE ALL NETLISTS
# ============================================================
def generate_all_netlists(dirs: dict, corner_list: list) -> dict:
    """Read all source files and generate netlists for every TB and corner."""
    dc_tran_psrr_text = read_source(SRC_DC_TRAN_PSRR)
    stb_text          = read_source(SRC_STB)
    mc_text           = read_source(SRC_MC)

    netlist_paths = {}

    print("[GEN] Generating DC netlists ...")
    netlist_paths["dc"]   = generate_dc_netlists(dirs, corner_list, dc_tran_psrr_text)

    print("[GEN] Generating PSRR netlists ...")
    netlist_paths["psrr"] = generate_psrr_netlists(dirs, corner_list, dc_tran_psrr_text)

    print("[GEN] Generating TRAN netlists ...")
    netlist_paths["tran"] = generate_tran_netlists(dirs, corner_list, dc_tran_psrr_text)

    print("[GEN] Generating STB netlists ...")
    netlist_paths["stb"]  = generate_stb_netlists(dirs, corner_list, stb_text)

    # MC run-0 placeholder to register CSV path; all runs generated inside run_mc_simulations
    mc_sp, mc_csv = generate_mc_single_run(0, dirs, mc_text)
    netlist_paths["mc"] = {"csv": mc_csv}

    total = sum(len(v) for k, v in netlist_paths.items() if k != "mc")
    print(f"[GEN] Done — {total} deterministic netlists written to {OUT_ROOT.resolve()}")
    return netlist_paths

# ============================================================
# 8. NGSPICE EXECUTION
# ============================================================
def run_ngspice(spice_file: pathlib.Path, timeout: int = SIM_TIMEOUT) -> bool:
    """
    Run ngspice in batch mode (CWD = spice file's parent directory so that
    relative paths in the netlist resolve correctly).
    Returns True on success.
    """
    log_file = spice_file.with_suffix(".log")
    try:
        with open(log_file, "w") as log:
            result = subprocess.run(
                ["ngspice", "-b", spice_file.name],
                cwd=str(spice_file.parent),
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
        if result.returncode != 0:
            print(f"  [WARN] ngspice exited {result.returncode} for {spice_file.name}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Timeout ({timeout}s) — {spice_file.name}")
        return False
    except FileNotFoundError:
        print("[ERROR] ngspice not found. Install it and ensure it is on PATH.")
        sys.exit(1)


def run_all_simulations(dirs: dict, netlist_paths: dict, corner_list: list) -> None:
    """Run DC / PSRR / TRAN / STB simulations sequentially across all corners."""
    for tb in ("dc", "psrr", "tran", "stb"):
        print(f"\n[SIM] {tb.upper()} — running {len(corner_list)} corner(s) ...")
        for corner in corner_list:
            sp_file, _ = netlist_paths[tb][corner]
            print(f"  {tb.upper():4s} [{corner:6s}] ... ", end="", flush=True)
            t0 = time.time()
            ok = run_ngspice(sp_file)
            dt = time.time() - t0
            print(f"{'OK  ' if ok else 'FAIL'} ({dt:.1f}s)")

# ============================================================
# 9. MC SIMULATIONS  (N separate ngspice processes — NEVER dowhile+reset)
# ============================================================
def run_mc_simulations(dirs: dict, n_runs: int = MC_RUNS) -> pathlib.Path:
    """
    Generate N netlists and run them as separate ngspice processes.

    WHY separate processes:
      ngspice evaluates agauss() ONCE at parse time.  A dowhile+reset loop
      reuses the SAME random draw → σ = 0 (all runs identical).
      Each new process re-parses the netlist → fresh OS-seeded random draw.
    """
    mc_text  = read_source(SRC_MC)
    csv_path = dirs["mc"]["csv"] / "mc_results.csv"

    # Remove stale CSV so appendwrite starts fresh
    if csv_path.exists():
        csv_path.unlink()
        print("[MC] Removed stale mc_results.csv")

    print(f"[MC] Launching {n_runs} runs (corner: {MC_CORNER}, "
          f"parallelism: {MC_PARALLEL}) ...")

    def _run_one(run_idx: int):
        sp_file, _ = generate_mc_single_run(run_idx, dirs, mc_text)
        ok = run_ngspice(sp_file, timeout=60)
        return ok, run_idx

    done = failed = 0
    with ThreadPoolExecutor(max_workers=MC_PARALLEL) as pool:
        futures = {pool.submit(_run_one, i): i for i in range(n_runs)}
        for fut in as_completed(futures):
            ok, idx = fut.result()
            done += 1
            if not ok:
                failed += 1
            if done % 100 == 0 or done == n_runs:
                print(f"  MC progress: {done}/{n_runs}  (failed: {failed})")

    print(f"[MC] Complete — {done - failed}/{n_runs} runs succeeded.")
    return csv_path

# ============================================================
# 10. CSV PARSING
# ============================================================
def parse_ngspice_csv(fp) -> Optional[pd.DataFrame]:
    """
    Parse bare-numeric ngspice wrdata output (no header line).
    Handles blank lines, non-numeric tokens, and ragged row counts.
    Returns a DataFrame with columns col_0 … col_N or None on failure.
    """
    fp = pathlib.Path(fp)
    if not fp.exists():
        return None

    tokens: list = []
    n_cols: Optional[int] = None

    for ln in fp.read_text(errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        vals, ok = [], True
        for tok in ln.split():
            try:
                vals.append(float(tok))
            except ValueError:
                ok = False
                break
        if ok and vals:
            if n_cols is None:
                n_cols = len(vals)
            if len(vals) == n_cols:
                tokens.extend(vals)

    if not tokens or n_cols is None:
        return None

    trim = len(tokens) % n_cols
    if trim:
        tokens = tokens[:-trim]

    arr = np.array(tokens).reshape(-1, n_cols)
    return pd.DataFrame(arr, columns=[f"col_{i}" for i in range(n_cols)])


def _apply_tb_extract(df: Optional[pd.DataFrame], tb: str) -> Optional[pd.DataFrame]:
    """
    Extract named columns from raw ngspice CSV using _TB_EXTRACT.
    PSRR fallback: if only 4 raw cols (ngspice wrote frequency as real),
    fall back to indices [1, 3] instead of [1, 4].
    """
    if df is None:
        return None

    spec    = _TB_EXTRACT[tb]
    indices = list(spec["indices"])
    names   = list(spec["names"])

    if tb == "psrr" and len(df.columns) < 5:
        indices = [1, 3]    # frequency real → only 2 cols instead of 3

    result = {}
    for name, idx in zip(names, indices):
        if idx < len(df.columns):
            result[name] = df.iloc[:, idx].values.astype(float)
        else:
            print(f"  [WARN] Column index {idx} out of range for {tb.upper()} "
                  f"({len(df.columns)} raw cols) — filling with zeros.")
            result[name] = np.zeros(len(df))
    return pd.DataFrame(result)


def load_all_csvs(dirs: dict, netlist_paths: dict, corner_list: list) -> dict:
    """Load and parse all simulation CSV results. Returns a nested dict."""
    data = {tb: {} for tb in ("dc", "psrr", "tran", "stb")}

    for tb in ("dc", "psrr", "tran", "stb"):
        for corner in corner_list:
            _, csv_path = netlist_paths[tb][corner]
            raw = parse_ngspice_csv(csv_path)
            if raw is None:
                print(f"  [WARN] No data: {tb.upper()} [{corner}]  ({csv_path})")
                data[tb][corner] = None
            else:
                extracted = _apply_tb_extract(raw, tb)
                data[tb][corner] = extracted
                if extracted is not None:
                    print(f"  [OK]   {tb.upper()} [{corner}] — {len(extracted)} rows")

    # MC
    mc_csv = netlist_paths["mc"]["csv"]
    raw_mc = parse_ngspice_csv(mc_csv)
    if raw_mc is None:
        print("  [WARN] No MC data found.")
        data["mc"] = None
    else:
        data["mc"] = _apply_tb_extract(raw_mc, "mc")
        print(f"  [OK]   MC — {len(raw_mc)} samples parsed")

    return data

# ============================================================
# 11. PLOTLY INTERACTIVE PLOT FUNCTIONS
# ============================================================
_PLOTLY_STYLE = dict(
    line_width=2.5,
    font_size=13,
    template="plotly_white",
)


def _base_fig(title: str, xtitle: str, ytitle: str, log_x: bool = False):
    fig = go.Figure()
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title=xtitle,
        yaxis_title=ytitle,
        hovermode="x unified",
        legend=dict(font=dict(size=13)),
        font=dict(size=13),
        template="plotly_white",
    )
    if log_x:
        fig.update_xaxes(type="log")
    return fig


def _ann_box(fig, text: str, x: float = 0.98, y: float = 0.98):
    fig.add_annotation(
        xref="paper", yref="paper", x=x, y=y,
        text=text, showarrow=False, align="left",
        font=dict(size=14, family="Courier New"),
        bgcolor="white", bordercolor="#888888", borderwidth=1,
    )


# ── DC ──────────────────────────────────────────────────────
def plot_dc(data: dict, dirs: dict, corner_list: list):
    fig = _base_fig(
        f"{DESIGN_NAME} — DC Transfer (Unity-Gain Buffer)",
        "V<sub>ICM</sub>  [V]", "V<sub>OUT</sub>  [V]",
    )
    for corner in corner_list:
        df = data["dc"].get(corner)
        if df is None:
            continue
        fig.add_trace(go.Scatter(
            x=df["input_v"], y=df["output_v"],
            name=corner,
            line=dict(color=CORNER_COLOR.get(corner, "#888"),
                      width=2.5,
                      dash=CORNER_DASH.get(corner, "solid")),
        ))
    # Ideal 1:1 reference
    fig.add_trace(go.Scatter(
        x=[0, 1.8], y=[0, 1.8],
        name="Ideal",
        line=dict(color="black", width=1.2, dash="dot"),
    ))
    out_html = dirs["dc"]["csv"].parent / "dc_plot.html"
    fig.write_html(str(out_html))
    print(f"[PLOT] DC → {out_html}")
    return fig


# ── PSRR ────────────────────────────────────────────────────
def plot_psrr(data: dict, dirs: dict, corner_list: list):
    fig = _base_fig(
        f"{DESIGN_NAME} — PSRR",
        "Frequency [Hz]", "PSRR  [dB]",
        log_x=True,
    )
    fig.add_vline(
        x=1e6, line_dash="dash", line_color="gray", line_width=1.2,
        annotation_text="1 MHz", annotation_position="top right",
        annotation=dict(font=dict(size=12)),
    )

    ann = "<b>PSRR Summary</b><br>"
    for corner in corner_list:
        df = data["psrr"].get(corner)
        if df is None:
            continue
        freq = df["frequency"].values
        vdb  = df["vdb_out"].values
        dc_psrr   = vdb[0]
        idx_1mhz  = np.argmin(np.abs(freq - 1e6))
        psrr_1mhz = vdb[idx_1mhz]
        ann += (f"{corner}: DC = {dc_psrr:.1f} dB  |  "
                f"@1 MHz = {psrr_1mhz:.1f} dB<br>")
        fig.add_trace(go.Scatter(
            x=freq, y=vdb, name=corner,
            line=dict(color=CORNER_COLOR.get(corner, "#888"),
                      width=2.5,
                      dash=CORNER_DASH.get(corner, "solid")),
        ))

    _ann_box(fig, ann)
    out_html = dirs["psrr"]["csv"].parent / "psrr_plot.html"
    fig.write_html(str(out_html))
    print(f"[PLOT] PSRR → {out_html}")
    return fig


# ── TRAN ────────────────────────────────────────────────────
def plot_tran(data: dict, dirs: dict, corner_list: list):
    fig = _base_fig(
        f"{DESIGN_NAME} — Transient Response",
        "Time [s]", "Voltage [V]",
    )
    vicm_plotted = False
    for corner in corner_list:
        df = data["tran"].get(corner)
        if df is None:
            continue
        t = df["time"].values
        fig.add_trace(go.Scatter(
            x=t, y=df["v_out"].values,
            name=f"Vout [{corner}]",
            line=dict(color=CORNER_COLOR.get(corner, "#888"),
                      width=2.5,
                      dash=CORNER_DASH.get(corner, "solid")),
        ))
        if not vicm_plotted:
            fig.add_trace(go.Scatter(
                x=t, y=df["v_in"].values,
                name="VICM (input, all corners)",
                line=dict(color="#888888", width=1.5, dash="dot"),
            ))
            vicm_plotted = True

    out_html = dirs["tran"]["csv"].parent / "tran_plot.html"
    fig.write_html(str(out_html))
    print(f"[PLOT] TRAN → {out_html}")
    return fig


# ── STB helpers ──────────────────────────────────────────────
def stb_metrics(df: Optional[pd.DataFrame]):
    """
    Compute UGF [Hz], phase margin [deg], DC loop gain [dB] from STB data.
    PM = interpolated_phase_at_UGF + 180  (phase_mb is negative by convention).
    """
    if df is None:
        return None, None, None
    freq  = df["frequency"].values
    gain  = df["vdb_mb"].values
    phase = df["phase_mb"].values

    dc_gain = float(gain[0]) if len(gain) else None

    sign_changes = np.where(np.diff(np.sign(gain)) < 0)[0]
    if not len(sign_changes):
        return None, None, dc_gain

    i   = sign_changes[0]
    lf  = np.log10(np.maximum(freq, 1e-15))
    f_ugf = 10 ** float(
        np.interp(0.0, [gain[i + 1], gain[i]], [lf[i + 1], lf[i]])
    )
    pm = float(np.interp(np.log10(f_ugf), lf, phase)) + 180.0
    return f_ugf, pm, dc_gain


# ── STB ─────────────────────────────────────────────────────
def plot_stb(data: dict, dirs: dict, corner_list: list):
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("Loop Gain  [dB]", "Phase  [°]"),
        vertical_spacing=0.10,
    )
    # MUST apply log without row/col filter — shared_xaxes requires it globally
    fig.update_xaxes(type="log")

    ann = "<b>Stability Metrics</b><br>"
    for corner in corner_list:
        df  = data["stb"].get(corner)
        ugf, pm, a0 = stb_metrics(df)
        if df is None:
            continue
        color = CORNER_COLOR.get(corner, "#888")
        dash  = CORNER_DASH.get(corner, "solid")
        freq  = df["frequency"].values
        gain  = df["vdb_mb"].values
        phase = df["phase_mb"].values

        fig.add_trace(
            go.Scatter(x=freq, y=gain, name=corner, legendgroup=corner,
                       line=dict(color=color, width=2.5, dash=dash)),
            row=1, col=1,
        )
        fig.add_trace(
            go.Scatter(x=freq, y=phase, name=corner, legendgroup=corner,
                       showlegend=False,
                       line=dict(color=color, width=2.5, dash=dash)),
            row=2, col=1,
        )
        ugf_s = f"{ugf/1e6:.2f} MHz" if ugf  else "N/A"
        pm_s  = f"{pm:.1f}°"         if pm   else "N/A"
        a0_s  = f"{a0:.1f} dB"       if a0   else "N/A"
        ann += f"{corner}: UGF={ugf_s}  PM={pm_s}  A₀={a0_s}<br>"

    # Reference lines: 0 dB and −180°
    fig.add_hline(y=0,    line_dash="dot", line_color="black", line_width=1.0, row=1, col=1)
    fig.add_hline(y=-180, line_dash="dot", line_color="black", line_width=1.0, row=2, col=1)

    _ann_box(fig, ann)
    fig.update_layout(
        title=f"{DESIGN_NAME} — Stability / Loop Gain (Middlebrook)",
        hovermode="x unified",
        font=dict(size=13),
        template="plotly_white",
    )
    out_html = dirs["stb"]["csv"].parent / "stb_plot.html"
    fig.write_html(str(out_html))
    print(f"[PLOT] STB → {out_html}")
    return fig


# ── MC Histogram ─────────────────────────────────────────────
def plot_mc(mc_df: Optional[pd.DataFrame], dirs: dict):
    if mc_df is None:
        print("[PLOT] MC — no data, skipping.")
        return None

    vos_mV = mc_df["v_diff_mis"].values * 1e3   # V → mV
    mu, sig = np.mean(vos_mV), np.std(vos_mV)
    n = len(vos_mV)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=vos_mV, nbinsx=60,
        marker_color=CORNER_COLOR["tt_mm"],
        name=f"V_OS ({n} runs)",
        opacity=0.80,
    ))

    # ±1σ / ±2σ / ±3σ bands + vertical markers
    for k, fill in [(3, "rgba(255,50,50,0.08)"),
                    (2, "rgba(255,165,0,0.10)"),
                    (1, "rgba(0,200,0,0.12)")]:
        fig.add_vrect(x0=mu - k*sig, x1=mu + k*sig,
                      fillcolor=fill, layer="below", line_width=0)
        for sign in (-1, 1):
            fig.add_vline(x=mu + sign*k*sig,
                          line_dash="dash", line_color="gray",
                          line_width=0.8,
                          annotation_text=f"±{k}σ",
                          annotation_position="top" if sign > 0 else "top")

    stats = (
        f"n  = {n}<br>"
        f"μ  = {mu:.4f} mV<br>"
        f"σ  = {sig:.4f} mV<br>"
        f"σ² = {sig**2 * 1e6:.4f} μV²<br>"
        f"±1σ = [{mu-sig:.3f}, {mu+sig:.3f}] mV<br>"
        f"±2σ = [{mu-2*sig:.3f}, {mu+2*sig:.3f}] mV<br>"
        f"±3σ = [{mu-3*sig:.3f}, {mu+3*sig:.3f}] mV"
    )
    _ann_box(fig, stats)

    fig.update_layout(
        title=(f"{DESIGN_NAME} — MC Offset Voltage "
               f"({n} runs, corner: {MC_CORNER})"),
        xaxis_title="V<sub>OS</sub>  [mV]",
        yaxis_title="Count",
        font=dict(size=13),
        template="plotly_white",
        hovermode="x unified",
    )
    out_html = dirs["mc"]["csv"].parent / "mc_plot.html"
    fig.write_html(str(out_html))
    print(f"[PLOT] MC → {out_html}")
    return fig

# ============================================================
# 12. IEEE MATPLOTLIB FIGURE GENERATOR  (MUST be before plot_all)
# ============================================================
IEEE_RC = {
    "font.family"     : "serif",
    "font.serif"      : ["Liberation Serif", "DejaVu Serif", "Times New Roman"],
    "font.size"       : 8,
    "axes.labelsize"  : 8,
    "xtick.labelsize" : 7,
    "ytick.labelsize" : 7,
    "legend.fontsize" : 6.5,
    "lines.linewidth" : 1.2,
    "axes.linewidth"  : 0.7,
    "xtick.direction" : "in",
    "ytick.direction" : "in",
    "xtick.top"       : True,
    "ytick.right"     : True,
    "axes.grid"       : True,
    "grid.linewidth"  : 0.35,
    "grid.alpha"      : 0.40,
    "savefig.dpi"     : 300,
    "savefig.bbox"    : "tight",
    "savefig.pad_inches": 0.03,
    "pdf.fonttype"    : 42,
    "ps.fonttype"     : 42,
}

COL1 = 3.5     # IEEE single-column width  [inches]
COL2 = 7.16    # IEEE double-column width  [inches]


def _inset(ax, text: str):
    """Small monospace annotation box inside plot area (lower-left)."""
    ax.text(
        0.02, 0.02, text, transform=ax.transAxes,
        fontsize=5.5, va="bottom", ha="left", family="monospace",
        bbox=dict(boxstyle="square,pad=0.25",
                  fc="white", ec="#BBBBBB", lw=0.6),
    )


def generate_ieee_plots(data: dict, dirs: dict, corner_list: list) -> None:
    ieee_dir = dirs["ieee"]

    with plt.rc_context(IEEE_RC):

        # ── DC ──────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(COL1, 2.8))
        for corner in corner_list:
            df = data["dc"].get(corner)
            if df is None:
                continue
            ax.plot(df["input_v"], df["output_v"],
                    color=CORNER_COLOR.get(corner, "#555"), label=corner)
        ax.plot([0, 1.8], [0, 1.8], "k--", lw=0.6, label="Ideal")
        ax.set_xlabel(r"$V_{ICM}$ [V]")
        ax.set_ylabel(r"$V_{OUT}$ [V]")
        ax.set_title("DC Transfer — Unity-Gain Buffer", pad=3)
        ax.legend(ncol=3, loc="upper left", fontsize=6)
        _inset(ax, f"SKY130 | corners: {', '.join(corner_list)}")
        fig.savefig(str(ieee_dir / "dc_ieee.png"))
        fig.savefig(str(ieee_dir / "dc_ieee.pdf"))
        plt.close(fig)

        # ── PSRR ────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(COL1, 2.8))
        ann_lines: list = []
        for corner in corner_list:
            df = data["psrr"].get(corner)
            if df is None:
                continue
            freq = df["frequency"].values
            vdb  = df["vdb_out"].values
            ax.semilogx(freq, vdb,
                        color=CORNER_COLOR.get(corner, "#555"), label=corner)
            dc_psrr  = vdb[0]
            psrr_1m  = float(vdb[np.argmin(np.abs(freq - 1e6))])
            ann_lines.append(f"{corner}: DC={dc_psrr:.0f}dB  @1M={psrr_1m:.0f}dB")
        ax.axvline(1e6, color="gray", lw=0.6, ls="--")
        ax.set_xlabel("Frequency [Hz]")
        ax.set_ylabel("PSRR [dB]")
        ax.set_title("Power-Supply Rejection Ratio", pad=3)
        ax.legend(ncol=2, loc="lower left", fontsize=6)
        _inset(ax, "\n".join(ann_lines))
        fig.savefig(str(ieee_dir / "psrr_ieee.png"))
        fig.savefig(str(ieee_dir / "psrr_ieee.pdf"))
        plt.close(fig)

        # ── TRAN ────────────────────────────────────────────
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(COL1, 4.5), sharex=True,
            gridspec_kw=dict(hspace=0.08),
        )
        vicm_plotted = False
        for corner in corner_list:
            df = data["tran"].get(corner)
            if df is None:
                continue
            t_ms = df["time"].values * 1e3
            ax1.plot(t_ms, df["v_out"].values,
                     color=CORNER_COLOR.get(corner, "#555"), label=corner)
            if not vicm_plotted:
                ax2.plot(t_ms, df["v_in"].values,
                         color="black", lw=0.8, label="VICM")
                vicm_plotted = True
        ax1.set_ylabel(r"$V_{OUT}$ [V]")
        ax1.set_title("Transient Response", pad=3)
        ax1.legend(ncol=3, loc="upper right", fontsize=6)
        ax2.set_xlabel("Time [ms]")
        ax2.set_ylabel(r"$V_{ICM}$ [V]")
        ax2.legend(loc="upper right", fontsize=6)
        fig.savefig(str(ieee_dir / "tran_ieee.png"))
        fig.savefig(str(ieee_dir / "tran_ieee.pdf"))
        plt.close(fig)

        # ── STB (Bode) ──────────────────────────────────────
        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(COL1, 4.5), sharex=True,
            gridspec_kw=dict(hspace=0.08),
        )
        stb_ann: list = []
        for corner in corner_list:
            df = data["stb"].get(corner)
            if df is None:
                continue
            ugf, pm, a0 = stb_metrics(df)
            freq  = df["frequency"].values
            gain  = df["vdb_mb"].values
            phase = df["phase_mb"].values
            c = CORNER_COLOR.get(corner, "#555")
            ax1.semilogx(freq, gain,  color=c, label=corner)
            ax2.semilogx(freq, phase, color=c, label=corner)
            ugf_s = f"{ugf/1e6:.2f}M" if ugf else "N/A"
            pm_s  = f"{pm:.0f}°"      if pm  else "N/A"
            a0_s  = f"{a0:.0f}dB"     if a0  else "N/A"
            stb_ann.append(f"{corner}:  fu={ugf_s}  PM={pm_s}  A0={a0_s}")
        ax1.axhline(0,    color="k", lw=0.6, ls="--")
        ax2.axhline(-180, color="k", lw=0.6, ls="--")
        ax1.set_ylabel("Loop Gain [dB]")
        ax1.set_title("Bode Plot — Loop Gain", pad=3)
        ax1.legend(ncol=2, loc="upper right", fontsize=6)
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Phase [°]")
        ax2.legend(ncol=2, loc="upper right", fontsize=6)
        _inset(ax1, "\n".join(stb_ann))
        fig.savefig(str(ieee_dir / "stb_ieee.png"))
        fig.savefig(str(ieee_dir / "stb_ieee.pdf"))
        plt.close(fig)

        # ── MC Histogram ────────────────────────────────────
        mc_df = data.get("mc")
        if mc_df is not None:
            vos_mV = mc_df["v_diff_mis"].values * 1e3
            mu, sig = np.mean(vos_mV), np.std(vos_mV)
            n = len(vos_mV)

            fig, ax = plt.subplots(figsize=(COL1, 2.8))
            n_bins = min(60, max(20, n // 20))
            ax.hist(vos_mV, bins=n_bins,
                    color=CORNER_COLOR["tt_mm"], alpha=0.75, edgecolor="none")

            for k, alpha in [(3, 0.08), (2, 0.12), (1, 0.18)]:
                ax.axvspan(mu - k*sig, mu + k*sig, color="red",
                           alpha=alpha, lw=0)
            for k in (1, 2, 3):
                for sign in (-1, 1):
                    ax.axvline(mu + sign*k*sig, color="gray",
                               lw=0.6, ls="--")

            stats = (f"n = {n}\nμ = {mu:.3f} mV\n"
                     f"σ = {sig:.3f} mV\n"
                     f"±3σ = [{mu-3*sig:.3f}, {mu+3*sig:.3f}] mV")
            _inset(ax, stats)
            ax.set_xlabel(r"$V_{OS}$ [mV]")
            ax.set_ylabel("Count")
            ax.set_title(f"MC Offset Voltage  ({n} runs, {MC_CORNER})", pad=3)
            fig.savefig(str(ieee_dir / "mc_ieee.png"))
            fig.savefig(str(ieee_dir / "mc_ieee.pdf"))
            plt.close(fig)

    print(f"[PLOT] IEEE figures → {ieee_dir}")

# ============================================================
# 13. PLOT ALL  (calls generate_ieee_plots → must be defined after it)
# ============================================================
def plot_all(data: dict, dirs: dict, corner_list: list) -> None:
    print("\n[PLOT] Generating Plotly interactive figures ...")
    plot_dc(data, dirs, corner_list)
    plot_psrr(data, dirs, corner_list)
    plot_tran(data, dirs, corner_list)
    plot_stb(data, dirs, corner_list)
    plot_mc(data.get("mc"), dirs)

    print("\n[PLOT] Generating IEEE matplotlib figures (300 DPI PNG + PDF) ...")
    generate_ieee_plots(data, dirs, corner_list)

# ============================================================
# HELPER  (path reconstruction for --plot-only; before main)
# ============================================================
def _reconstruct_paths(dirs: dict, corner_list: list) -> dict:
    """Rebuild netlist_paths from existing files — used by --plot-only."""
    paths = {tb: {} for tb in ("dc", "psrr", "tran", "stb")}
    for tb in ("dc", "psrr", "tran", "stb"):
        for corner in corner_list:
            paths[tb][corner] = (
                dirs[tb]["spice"] / f"{tb}_{corner}.spice",
                dirs[tb]["csv"]   / f"{tb}_{corner}.csv",
            )
    paths["mc"] = {"csv": dirs["mc"]["csv"] / "mc_results.csv"}
    return paths

# ============================================================
# 14. MAIN  (must be last function before if __name__)
# ============================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Cross-corner simulation automation — "
            "Rail-to-Rail IP/OP OTA with Internal Bias (SKY130 / ngspice)"
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--generate-only", action="store_true",
        help="Write netlists only; skip simulation and plotting.",
    )
    parser.add_argument(
        "--plot-only", action="store_true",
        help="Parse existing CSVs and plot; skip netlist generation and simulation.",
    )
    parser.add_argument(
        "--corners", nargs="+", default=None, metavar="CORNER",
        help=f"Subset of corners to run. Choices: {ALL_CORNERS}",
    )
    parser.add_argument(
        "--mc-runs", type=int, default=MC_RUNS,
        help="Number of MC runs.",
    )
    args = parser.parse_args()

    corner_list = args.corners if args.corners else ALL_CORNERS
    for c in corner_list:
        if c not in ALL_CORNERS:
            parser.error(f"Unknown corner '{c}'. Valid corners: {ALL_CORNERS}")

    print(f"\n{'═'*62}")
    print(f"  {DESIGN_NAME}")
    print(f"  PDK: SKY130  |  Corners: {corner_list}")
    print(f"  Output root : {OUT_ROOT.resolve()}")
    print(f"{'═'*62}\n")

    dirs = make_dirs()

    # ── Generate netlists ────────────────────────────────────
    if not args.plot_only:
        for src in (SRC_DC_TRAN_PSRR, SRC_STB, SRC_MC):
            if not src.exists():
                print(f"[ERROR] Source file not found: {src.resolve()}")
                print("        Place the source SPICE files next to this script,")
                print("        or edit SRC_* paths at the top of the script.")
                sys.exit(1)
        netlist_paths = generate_all_netlists(dirs, corner_list)
    else:
        netlist_paths = _reconstruct_paths(dirs, corner_list)

    if args.generate_only:
        print("\n[INFO] --generate-only: netlists written. Exiting.")
        return

    # ── Run simulations ──────────────────────────────────────
    if not args.plot_only:
        run_all_simulations(dirs, netlist_paths, corner_list)
        run_mc_simulations(dirs, n_runs=args.mc_runs)

    # ── Parse CSVs + generate all plots ─────────────────────
    print("\n[PARSE] Loading simulation results ...")
    data = load_all_csvs(dirs, netlist_paths, corner_list)
    plot_all(data, dirs, corner_list)

    print(f"\n{'═'*62}")
    print("  DONE.  All outputs in:")
    print(f"  {OUT_ROOT.resolve()}")
    print(f"{'═'*62}\n")

# ============================================================
# 15. ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
