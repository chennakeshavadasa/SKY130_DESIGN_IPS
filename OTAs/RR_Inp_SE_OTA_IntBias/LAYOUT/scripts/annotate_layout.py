#!/usr/bin/env python3
"""Annotated floorplan: KLayout render of the final GDS with every functional block outlined
and labelled.  Block boxes are taken from the layout generator itself (exact geometry).
Output: docs/layout_annotated.png"""
import os
import sys
import subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import matplotlib.image as mpimg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gen_ota as g  # noqa: E402

for f in (g.build_core_bottom, g.build_mn_casc, g.build_pmos_pair, g.build_nmos_pair, g.build_xm1,
          g.build_resistors, g.build_top, g.build_logic):
    f()
um = 1e-3


def bb(segs, pad=250, extra=()):
    xs = [s.x1 for s in segs] + [s.x2 for s in segs] + [e[0] for e in extra] + [e[2] for e in extra]
    ys = [s.ybot - 500 for s in segs] + [s.ytop + 500 for s in segs] + [e[1] for e in extra] + [e[3] for e in extra]
    return (min(xs) - pad, min(ys), max(xs) + pad, max(ys))


R, Y = g.ROWS, g.Y
M = R["mirror"]["segs"]
C = R["mncasc"]
T = R["top"]
Lg = R["logic"]
res = R["res"]
stk = R["stack"]
heads = res["heads"]
rx = 1410 // 2
blocks = [
    ("1", "PMOS input pair MP_A1/MP_A2\n4×14 common centroid + n-ring", R["ppair"]["ring"], "#d62728"),
    ("2", "NMOS input pair MN_A1/MN_A2\n2×8 common centroid + p-ring", R["npair"]["ring"], "#1f77b4"),
    ("3", "NMOS cascodes MN_CASC_L1/L2\n+ VBN_CASC bias stack", bb(C["segs"] + [C["stack"]], extra=()), "#9467bd"),
    ("4", "NMOS current mirrors: load MN_BOT_L1/L2 (CC),\ntail MN_NDIFF_BIAS, diode MN_BIAS_EXT, MN_BIAS_SOURCE,\nMN_CASC_B_SOURCE (net8)",
     bb(M["a"] + M["b"]), "#2ca02c"),
    ("5", "PMOS load mirror MP_TOP_L1/L2 (ABBA CC)", bb([T["mptop"]]), "#ff7f0e"),
    ("6", "PMOS cascodes MP_CASC_L1/L2 + VBP_CASC stack\n+ MP_SW2", bb(T["cas"] + [T["stk"], T["sw2"]]), "#8c564b"),
    ("7", "PMOS tail mirror (net9): MP_PDIFF_BIAS, diode _B,\nMP_CASC_B_SOURCE + MP_SW1", bb([T["p4a"], T["dc"], T["p4b"], T["sw1"]]), "#e377c2"),
    ("8", "VBP_TOP mirror: M3 (diode) / M4 (beta-mult. PMOS),\nM9 (→net8), M2 (start-up sense), MP_SW3, M15",
     bb([T["sw3"], T["m9"], T["m15"], T["m34"], T["m2"]]), "#bcbd22"),
    ("9", "Beta-multiplier gm cell XM1 (16×) / XM10 (4×)\nW10/L4, 2-D common centroid + p-ring", R["xm1"]["ring"], "#17becf"),
    ("10", "R14–R22: beta-multiplier resistor\n(xhigh_po_1p41, 9 × L6.4)",
     (heads[0][0][0] - rx - 250, heads[0][0][1] - 1330, heads[8][1][0] + rx + 250, heads[8][1][1] + 1330), "#7f7f7f"),
    ("11", "R24–R34: start-up feed from VDD\n(xhigh_po_1p41, 9 × L7.05)",
     (heads[9][0][0] - rx - 250, heads[9][0][1] - 1330, heads[17][1][0] + rx + 250, heads[17][1][1] + 1330), "#aec7e8"),
    ("12", "Start-up sense load M19–M32\n10 × W0.5/L10 (shared VDD gate)",
     (stk["xs"] - 900, res["y0"] - 250, stk["x2"] + 250, res["y0"] + 10580 + 250), "#ff9896"),
    ("13", "Start-up injector M12 (pfet W0.5/L4, gate = VSTRP_OUT)", bb([T["m12"]]), "#c5b0d5"),
    ("14", "Enable / start-up logic: inverters M5/M6, M42/M43,\nNAND M13/M14/M38/M39",
     bb([Lg[f"P{k}"] for k in range(4)] + [Lg[f"N{k}"] for k in range(4)], pad=500), "#98df8a"),
    ("15", "EN_B power-down switches MN_SW1/MN_SW2, XM16", bb([Lg["sw"], Lg["m16"]], pad=200), "#ffbb78"),
]

C_ = g.CELL
gds = next(p for p in (os.path.join(ROOT, "mag", C_ + ".gds"), os.path.join(ROOT, "gds", C_ + ".gds")) if os.path.exists(p))
X1, Y1, X2, Y2 = -1.0, -1.0, 89.0, 49.0           # view box (um), aspect 1.8
png = os.path.join(ROOT, "docs", "_render_annot.png")
subprocess.run(["klayout", "-zz", "-r", os.path.join(HERE, "render.py"), "-rd", f"gds={gds}", "-rd", f"png={png}",
                "-rd", f"box={X1},{Y1},{X2},{Y2}", "-rd", "w=3600", "-rd", "h=2000"], capture_output=True)
img = mpimg.imread(png)

fig = plt.figure(figsize=(18, 12.6))
ax = fig.add_axes([0.02, 0.30, 0.96, 0.68])
ax.imshow(img, extent=[X1, X2, Y1, Y2], alpha=0.55, interpolation="lanczos")
for num, txt, (x1, y1, x2, y2), col in blocks:
    ax.add_patch(mp.Rectangle((x1 * um, y1 * um), (x2 - x1) * um, (y2 - y1) * um, fill=True, facecolor=col,
                              alpha=0.12, edgecolor="none"))
    ax.add_patch(mp.Rectangle((x1 * um, y1 * um), (x2 - x1) * um, (y2 - y1) * um, fill=False, edgecolor=col, lw=2.4))
    ax.text(x1 * um + 0.35, y2 * um - 0.35, num, fontsize=15, fontweight="bold", va="top", ha="left", color="white",
            bbox=dict(boxstyle="circle,pad=0.25", fc=col, ec="black", lw=0.8))
# pins
P = R["ppair"]
pins = [("VINP", g.BUSX["VINP"] * um, (P["sy"]["S2"]) * um + 1.2), ("VINN", g.BUSX["VINN"] * um, Y["top"] * um - 0.6),
        ("VOUT", g.BUSX["VOUT"] * um, 0.4), ("MN_TAIL_BIAS", g.BUSX["MTB"] * um, 0.4),
        ("EN", (g.XB0 + 45690) * um - 0.5, Y["EN"] * um), ("VDD", 12.0, Y["Rt"] * um), ("GNDA", 12.0, Y["rail0"] * um)]
for name, x, y in pins:
    ax.plot([x], [y], marker="s", ms=9, mfc="yellow", mec="black")
    ax.annotate(name, (x, y), xytext=(6, 6), textcoords="offset points", fontsize=11, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="yellow", ec="black", lw=0.6))
ax.annotate("", xy=(20.0, 1.0), xytext=(20.0, 46.5), arrowprops=dict(arrowstyle="-", ls="--", color="k", lw=0.8))
ax.text(20.2, 46.6, "core symmetry axis", fontsize=9, style="italic")
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)
ax.set_xlabel("x (µm)")
ax.set_ylabel("y (µm)")
ax.set_title(f"{C_}: annotated floorplan (87 µm × 47 µm, sky130A)", fontsize=14)
# legend panel
lx = fig.add_axes([0.02, 0.0, 0.96, 0.27])
lx.axis("off")
cols = 3
for i, (num, txt, _, col) in enumerate(blocks):
    cx, cy = (i % cols) / cols, 1 - (i // cols) * 0.2
    lx.text(cx + 0.005, cy - 0.02, num, fontsize=13, fontweight="bold", color="white", va="top",
            bbox=dict(boxstyle="circle,pad=0.25", fc=col, ec="black", lw=0.8))
    lx.text(cx + 0.03, cy - 0.02, txt, fontsize=10.5, va="top")
out = os.path.join(ROOT, "docs", "layout_annotated.png")
fig.savefig(out, dpi=120)
try:   # palette-quantize to keep the README image small
    from PIL import Image
    Image.open(out).convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)
except Exception as e:  # noqa: BLE001
    print("quantize skipped:", e)
os.remove(png)
print("wrote", out)
