#!/usr/bin/env python3
"""
Layout generator: Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias (sky130A)

Floorplan (two columns, VDD on top, GNDA at the bottom)
  core column (x ~ 0..41 um)              bias column (x ~ 42..)
  -------------------------------------------------------------------
  T1: MP_TOP_L1/L2  ABBA x3 (CC)         T1: net9 mirror [P4][D C][P4] + EN switches
  T2: MP_CASC_L1/L2 [A4 B4 B4 A4] + bias T2: VBP_TOP mirror [M3 M4][M9][M2] + logic P
  NMOS pair MN_A1/2 2x8 2-D CC + ring    logic N + EN_B switches
  PMOS pair MP_A1/2 4x14 2-D CC + ring   xhigh_po resistors + L=10 stack
  MN_CASC_L1/L2 + VBN_CASC stack         XM1/XM10 beta-multiplier pair 2 rows CC
  NMOS mirror rows (net8) 2-D CC
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lay import *          # noqa
from runmagic import build  # noqa

um = 1000
CELL = "Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias"
lay = Layout(CELL)

# m3 bus registry for spacing checks: (net, x, y1, y2)
BUSES = []


def bus(net, x, y1, y2, w=M3_W):
    for (n, bx, a, b) in BUSES:
        if n != net and not (y2 < a - 300 or y1 > b + 300) and abs(bx - x) < w + 400:
            raise ValueError(f"m3 bus clash {net}@{x} vs {n}@{bx}")
    BUSES.append((net, x, min(y1, y2), max(y1, y2)))
    lay.vwire("metal3", x, y1 - 200, y2 + 200, w)


def tap2bus(net, x, y):
    """m2 track (already present at y) -> m3 bus at x"""
    lay.via2(x, y)


XCC = 20000          # core column symmetry axis
ROWS = {}            # name -> info dict


# ====================================================================
# 1. NMOS mirror rows (net8 gate), W=0.5 L=2   (core bottom)
# ====================================================================
def nmos_mirror(yb, ya):
    W, L = 500, 2000
    termN = {"N": ("GNDA", "n6"), "A": ("GNDA", "n1"), "B": ("GNDA", "n2"),
             "X": ("GNDA", "n8"), "S": ("GNDA", "n9"), "C": ("GNDA", "VBPC")}
    gs = {"net8": "top"}
    info = {}
    for row, y0, pat, side in (("b", yb, "BAABBA", "top"), ("a", ya, "ABBAAB", "bot")):
        gside = {"net8": side}
        x = XCC - 12155
        segs = []
        for fingers, first in (("NN", "n6"), (pat, "n1" if pat[0] == "A" else "n2"), ("NN", "n6")):
            strips = chain(list(fingers), first, termN)
            s = mos_segment(lay, x, y0, "n", W, L, ["net8"] * len(fingers), strips, gside)
            segs.append(s)
            x = s.x2 + 270
        x += 430
        if row == "a":
            strips = chain(["X", "S"], "n8", termN)
        else:
            strips = chain(["C"], "VBPC", termN)
        s = mos_segment(lay, x, y0, "n", W, L, ["net8"] * (len(strips) - 1), strips, gside)
        segs.append(s)
        info[row] = segs
    # GNDA rails (bottom rail spans full chip later) and shared mid rail
    return info


TP = 600      # m2 track pitch (0.3 wide, 0.3 space: magic treats long metal as wide)
RS = 300      # clearance via pad -> rail
RAIL_H = 290


def chan_below(d, k):
    """track ys for k tracks below a diffusion bottom edge d (nearest first)"""
    return [d - 250 - i * TP for i in range(k)]


def chan_above(d, k):
    return [d + 250 + i * TP for i in range(k)]


Y = {}   # named y coordinates


def build_core_bottom():
    W = 500
    Y["rail0"] = 350
    r0top = Y["rail0"] + RAIL_H // 2
    # row b : 3 tracks below
    Y["mb_d"] = r0top + RS + 160 + 2 * TP + 250
    tb_y = chan_below(Y["mb_d"], 3)
    # row a : strap below, sharing net8 with row b strap above
    Y["ma_d"] = Y["mb_d"] + W + 440 + 210 + 440
    ta_y = chan_above(Y["ma_d"] + W, 3)
    Y["rail1"] = ta_y[-1] + 160 + RS + RAIL_H // 2
    info = nmos_mirror(Y["mb_d"], Y["ma_d"])
    x1 = XCC - 17500
    x2 = XCC + 17900
    tap_strip(lay, "p", x1, XB0 + 300, Y["rail0"], cx2=XB0 - 150)   # bottom GNDA rail
    tap_strip(lay, "p", x1, x2, Y["rail1"])          # between mirror row a and MN_CASC
    tb = {"n6": tb_y[0], "n1": tb_y[1], "n2": tb_y[2], "VBPC": tb_y[1]}
    ta = {"n6": ta_y[0], "n1": ta_y[1], "n2": ta_y[2], "n8": ta_y[0], "n9": ta_y[1]}
    for row, tr, rail in (("b", tb, Y["rail0"]), ("a", ta, Y["rail1"])):
        for s in info[row]:
            strips_to_rail(lay, s, "GNDA", rail)
            for net, y in tr.items():
                strips_to_track(lay, s, net, y)
        segs = info[row]
        m2_track(lay, segs[0].sx[0], segs[2].sx[-1], tr["n6"])
        core = segs[1]
        m2_track(lay, core.sx[0], core.sx[-1], tr["n1"])
        m2_track(lay, core.sx[0], core.sx[-1], tr["n2"])
    # li fill joining the two facing net8 straps
    xs = min(s.x1 for s in info["a"] + info["b"]) + 290
    xe = max(s.x2 for s in info["b"]) - 290
    lay.rect("locali", xs, Y["mb_d"] + W + 190, xe, Y["ma_d"] - 190)
    # MN_BIAS_EXT diode: its n8 drain strip li down to the net8 strap (row a, bottom side)
    single = info["a"][3]
    cx = single.sx[0]
    lay.rect("locali", cx - 85, Y["ma_d"] - 360, cx + 85, single.cy1)
    lay.rect("locali", cx - 85, Y["ma_d"] - 360, single.gx[0][0] + 50, Y["ma_d"] - 190)
    ROWS["mirror"] = {"segs": info, "tb": tb, "ta": ta}
    return info


def build_mn_casc():
    """MN_CASC_L1 (A: n1->n5) / MN_CASC_L2 (B: n2->VOUT) W.5 L.5 and the
    8-high VBN_CASC diode stack; gate strap VBNC on top."""
    W, L = 500, 500
    r1top = Y["rail1"] + RAIL_H // 2
    y0 = r1top + RS + 160 + TP + 250
    Y["mc_d"] = y0
    below = chan_below(y0, 2)              # n2 (near), n1
    above = [y0 + W + 190 + 170 + 200 + 150, y0 + W + 190 + 170 + 200 + 150 + TP]
    Y["mc_top_track"] = above[-1]
    term = {"A": ("n1", "n5"), "B": ("n2", "VOUT")}
    gside = {"VBNC": "top"}
    segs = []
    order = [("A", 1, "n5"), ("B", 2, "VOUT"), ("A", 2, "n1"), ("B", 1, "n2")]
    widths = [(k + 1) * SD + k * L for (_, k, _) in order]
    tot = sum(widths) + 270 * (len(order) - 1)
    x = XCC - tot // 2
    for dev, k, first in order:
        strips = chain([dev] * k, first, term)
        s = mos_segment(lay, x, y0, "n", W, L, ["VBNC"] * k, strips, gside)
        segs.append(s)
        x = s.x2 + 270
    # VBN_CASC stack: GNDA |8| . |7| ... |1| VBNC  (uncontacted inner nodes)
    xs = segs[-1].x2 + 600
    strips = ["GNDA"] + [None] * 7 + ["VBNC"]
    st = mos_segment(lay, xs, y0, "n", W, L, ["VBNC"] * 8, strips, gside)
    cx = st.sx[-1]
    lay.rect("locali", cx - 85, st.cy2, cx + 85, y0 + W + 190 + 170)
    lay.rect("locali", st.gx[-1][1] - 10, y0 + W + 190, cx + 85, y0 + W + 190 + 170)
    strips_to_rail(lay, st, "GNDA", Y["rail1"])
    tr = {"n2": below[0], "n1": below[1], "n5": above[0], "VOUT": above[1]}
    for s in segs:
        for net, y in tr.items():
            strips_to_track(lay, s, net, y)
    xa, xb = segs[0].sx[0], segs[-1].sx[-1]
    for y in tr.values():
        m2_track(lay, xa, xb, y)
    lay.rect("locali", segs[0].gx[0][0], y0 + W + 190, st.gx[-1][1], y0 + W + 190 + 170)
    ROWS["mncasc"] = {"segs": segs, "stack": st, "tr": tr}


def build_pmos_pair():
    """MP_A1 (A, VINP, D=n1) / MP_A2 (B, VINN, D=n2), pfet_01v8_lvt W=4 L=2 x28 each.
    4 rows of 14 fingers, row patterns X, X', X', X  (2-D common centroid).
    Gate straps between rows are shared: S0=VINP, S1=VINN, S2=VINP, S3=VINN, S4=VINP."""
    W, L = 4000, 2000
    X = "ABBAABBAABBAAB"
    Xb = "BAABBAABBAABBA"
    term = {"A": ("n7", "n1"), "B": ("n7", "n2")}
    ring_y1 = Y["mc_top_track"] + 160 + RS
    r1 = ring_y1 + 290 + 200 + 485
    bots = [r1]
    for g in (825, 640, 825):
        bots.append(bots[-1] + W + g)
    pats = [X, Xb, Xb, X]
    sides = [{"VINP": "bot", "VINN": "top"}, {"VINN": "bot", "VINP": "top"},
             {"VINP": "bot", "VINN": "top"}, {"VINN": "bot", "VINP": "top"}]
    nW = 15 * SD + 14 * L
    x0 = XCC - nW // 2
    segs = []
    for k in range(4):
        pat = pats[k]
        strips = chain(list(pat), "n1" if pat[0] == "A" else "n2", term)
        gates = ["VINP" if c == "A" else "VINN" for c in pat]
        segs.append(mos_segment(lay, x0, bots[k], "p", W, L, gates, strips, sides[k], lvt=True))
    gx1, gx2 = x0 + SD, x0 + nW - SD
    # VINN li fill between R1/R2 and R3/R4 (facing straps)
    for a, b in ((0, 1), (2, 3)):
        lay.rect("locali", gx1, segs[a].ytop + 235, gx2, segs[b].ybot - 235)
    sy = {"S0": bots[0] - 320, "S1": (segs[0].ytop + segs[1].ybot) // 2,
          "S2": segs[1].ytop + 320, "S3": (segs[2].ytop + segs[3].ybot) // 2,
          "S4": segs[3].ytop + 320}
    xbl, xbr = x0 - 600, x0 + nW + 600
    def sxa(net, y):   # first / last gate x of the strap(s) of `net` at level y
        r = [v for s in segs for k, v in s.strap.items() if k[0] == net and abs(v[2] - y) < 400]
        return min(v[0] for v in r), max(v[1] for v in r)
    for k in ("S0", "S2", "S4"):
        lay.rect("locali", xbl - 85, sy[k] - 85, sxa("VINP", sy[k])[0] + 100, sy[k] + 85)
    for k in ("S1", "S3"):
        lay.rect("locali", sxa("VINN", sy[k])[1] - 100, sy[k] - 85, xbr + 85, sy[k] + 85)
    lay.rect("locali", xbl - 85, sy["S0"] - 85, xbl + 85, sy["S4"] + 85)
    lay.rect("locali", xbr - 85, sy["S1"] - 85, xbr + 85, sy["S3"] + 85)
    # gate exits to m2 (VINP left at S2 level, VINN right at S2 level)
    lay.li_m2(xbl, sy["S2"])
    lay.li_m2(xbr, sy["S2"])
    # tracks n1/n7/n2 over each row
    tr = []
    for s in segs:
        t = {"n1": s.ybot + 1000, "n7": s.ybot + 2000, "n2": s.ybot + 3000}
        for net, y in t.items():
            strips_to_track(lay, s, net, y)
        tr.append(t)
    # n-tap guard ring (VDD) + nwell
    rx1 = xbl - 160 - RS - 290
    rx2 = xbr + 160 + RS + 290
    ry2 = segs[3].ytop + 485 + 200 + 290
    tap_ring(lay, "n", rx1, ring_y1, rx2, ry2)
    lay.rect("nwell", rx1 - 180, ring_y1 - 180, rx2 + 180, ry2 + 180)
    ROWS["ppair"] = {"segs": segs, "tr": tr, "sy": sy, "xbl": xbl, "xbr": xbr,
                     "ring": (rx1, ring_y1, rx2, ry2)}
    Y["ppair_top"] = ry2 + 180


def build_nmos_pair():
    """MN_A1 (A, VINP, D=n3) / MN_A2 (B, VINN, D=n4) nfet_01v8_lvt W=2.5 L=2 x8 each.
    2 rows (ABBAABBA / BAABBAAB) 2-D common centroid, p-tap guard ring.
    Straps: S0=VINN (below R1), S1=VINP (shared), S2=VINN (above R2)."""
    W, L = 2500, 2000
    P1, P2 = "ABBAABBA", "BAABBAAB"
    term = {"A": ("n6", "n3"), "B": ("n6", "n4")}
    ring_y1 = Y["ppair_top"] + 130
    r1 = ring_y1 + 290 + 200 + 440
    bots = [r1, r1 + W + 780]
    sides = [{"VINN": "bot", "VINP": "top"}, {"VINP": "bot", "VINN": "top"}]
    nW = 9 * SD + 8 * L
    x0 = XCC - nW // 2
    segs = []
    for k, pat in enumerate((P1, P2)):
        strips = chain(list(pat), "n3" if pat[0] == "A" else "n4", term)
        gates = ["VINP" if c == "A" else "VINN" for c in pat]
        segs.append(mos_segment(lay, x0, bots[k], "n", W, L, gates, strips, sides[k], lvt=True))
    gx1, gx2 = x0 + SD, x0 + nW - SD
    lay.rect("locali", gx1, segs[0].ytop + 190, gx2, segs[1].ybot - 190)   # VINP fill
    sy = {"S0": bots[0] - 275, "S1": (segs[0].ytop + segs[1].ybot) // 2, "S2": segs[1].ytop + 275}
    xbl, xbr = x0 - 600, x0 + nW + 600
    def sxa(net, y):
        r = [v for s in segs for k, v in s.strap.items() if k[0] == net and abs(v[2] - y) < 400]
        return min(v[0] for v in r), max(v[1] for v in r)
    lay.rect("locali", xbl - 85, sy["S1"] - 85, sxa("VINP", sy["S1"])[0] + 100, sy["S1"] + 85)
    for k in ("S0", "S2"):
        lay.rect("locali", sxa("VINN", sy[k])[1] - 100, sy[k] - 85, xbr + 85, sy[k] + 85)
    lay.rect("locali", xbr - 85, sy["S0"] - 85, xbr + 85, sy["S2"] + 85)
    lay.li_m2(xbl, sy["S1"])
    lay.li_m2(xbr, sy["S1"])
    tr = []
    for s in segs:
        t = {"n3": s.ybot + 600, "n6": s.ybot + 1250, "n4": s.ybot + 1900}
        for net, y in t.items():
            strips_to_track(lay, s, net, y)
        tr.append(t)
    rx1 = xbl - 160 - RS - 290
    rx2 = xbr + 160 + RS + 290
    ry2 = segs[1].ytop + 440 + 200 + 290
    tap_ring(lay, "p", rx1, ring_y1, rx2, ry2)
    ROWS["npair"] = {"segs": segs, "tr": tr, "sy": sy, "xbl": xbl, "xbr": xbr,
                     "ring": (rx1, ring_y1, rx2, ry2)}
    Y["npair_top"] = ry2


XB0 = 41600          # bias column left edge


def build_xm1():
    """XM1 (W10 L4 x16, D=VBPT S=n12) / XM10 (W10 L4 x4 diode MTB, S=GNDA).
    2 identical rows [M1 x4][M10 x2][M1 x4] -> 2-D common centroid; gate MTB.
    Facing gate heads merged into one shared strap; p-tap ring = GNDA."""
    W, L = 10000, 4000
    term = {"M": ("n12", "VBPT"), "T": ("GNDA", "MTB")}
    ry1 = Y["rail0"] - 145
    r1 = ry1 + 290 + 200 + 130
    bots = [r1, r1 + W + 550]
    x0 = XB0 + 690
    rows = []
    for k, y0 in enumerate(bots):
        side = {"MTB": "top" if k == 0 else "bot"}
        x = x0
        segs = []
        for f, first in (("MMMM", "n12"), ("TT", "GNDA"), ("MMMM", "n12")):
            strips = chain(list(f), first, term)
            s = mos_segment(lay, x, y0, "n", W, L, ["MTB"] * len(f), strips, side)
            segs.append(s)
            x = s.x2 + 270
        rows.append(segs)
    # shared strap across the whole row width
    sy1 = bots[0] + W + 190
    lay.rect("locali", rows[0][0].gx[0][0], sy1, rows[0][2].gx[-1][1], sy1 + 170)
    # XM10 diode: MTB strips li to strap
    for k, segs in enumerate(rows):
        cx = segs[1].sx[1]
        if k == 0:
            lay.rect("locali", cx - 85, segs[1].cy2, cx + 85, sy1 + 10)
        else:
            lay.rect("locali", cx - 85, sy1 + 160, cx + 85, segs[1].cy1)
    tr = []
    for segs in rows:
        yb = segs[0].ybot
        t = {"GNDA": yb + 1500, "n12": yb + 3500, "VBPT": yb + 5500, "MTB": yb + 7500}
        for s in segs:
            for net, y in t.items():
                strips_to_track(lay, s, net, y)
        tr.append(t)
    rx2 = rows[0][2].x2 + 400 + 290
    ry2 = bots[1] + W + 130 + 200 + 290
    tap_ring(lay, "p", XB0, ry1, rx2, ry2)
    ROWS["xm1"] = {"rows": rows, "tr": tr, "ring": (XB0, ry1, rx2, ry2)}
    Y["xm1_top"] = ry2


def build_resistors():
    """R14..R22 (L=6.4, n12 -> GNDA) and R24..R34 (L=7.05, VDD -> net15)
    xhigh_po_1p41 in one serpentine row, pitch 1.89 um.  Plus the L=10 stack."""
    y0 = Y["xm1_top"] + 600
    x0 = XB0 + 690
    P = XRW + 480
    heads = []
    for i in range(18):
        Ls = 6400 if i < 9 else 7050
        heads.append(xres(lay, x0 + i * P, y0, Ls))
    # serpentine links: group A (0..8): R0.bot=n12, links top(0,1) bot(1,2)...; R8.top=GNDA
    def link(i, j, which):
        a = heads[i][which]
        b = heads[j][which]
        lay.rect("metal1", a[0], a[1] - 500, b[0], a[1] + 500)
    for i in range(8):
        link(i, i + 1, 1 if i % 2 == 0 else 0)
    # group B (9..17): R9.bot = VDD, links bot(9,10) top(10,11) ...; R17.top = net15
    for i in range(9, 17):
        link(i, i + 1, 1 if (i - 9) % 2 == 0 else 0)
    ROWS["res"] = {"heads": heads, "y0": y0}
    Y["res_top"] = heads[17][1][1] + XHEAD // 2
    # ---------------- M19..M32 : 10 x nfet W0.5 L10 in series, gate VDD -------------
    xs = x0 + 18 * P + 900
    ys = y0
    sw, pitch, Lg = 500, 770, 10000
    n = 10
    ytop = ys + 290 + Lg + 290
    for k in range(n):
        sx = xs + k * pitch
        lay.rect("ndiff", sx, ys, sx + sw, ytop)
    lay.rect("poly", xs - 130, ys + 290, xs + (n - 1) * pitch + sw + 130, ys + 290 + Lg)
    cys = {"b": (ys + 60, ys + 230), "t": (ytop - 230, ytop - 60)}
    for k in range(n):
        sx = xs + k * pitch
        for key, (c1, c2) in cys.items():
            lay.rect("locali", sx + 85, c1, sx + 415, c2)
            lay.rect("ndiffc", sx + 165, c1, sx + 335, c2)
    # serpentine: (0,1) bottom, (1,2) top, ...
    for k in range(n - 1):
        key = "b" if k % 2 == 0 else "t"
        c1, c2 = cys[key]
        lay.rect("locali", xs + k * pitch + 85, c1, xs + (k + 1) * pitch + 415, c2)
    # gate tab (VDD) on the left
    gy = ys + 290 + Lg // 2
    lay.rect("poly", xs - 760, gy - 250, xs - 130, gy + 250)
    lay.rect("polycont", xs - 600, gy - 85, xs - 430, gy + 85)
    lay.rect("locali", xs - 680, gy - 85, xs - 350, gy + 85)
    lay.mcon(xs - 515, gy)
    # VSI (strip 0 top) and GNDA (strip 9 top) contacts to m1
    tc = (cys["t"][0] + cys["t"][1]) // 2
    lay.mcon(xs + 250, tc)
    lay.mcon(xs + (n - 1) * pitch + 250, tc)
    ROWS["stack"] = {"xs": xs, "gate": (xs - 515, gy), "vsi": (xs + 250, tc),
                     "gnd": (xs + (n - 1) * pitch + 250, tc), "x2": xs + (n - 1) * pitch + sw + 130}


def build_top():
    """nwell A: T2 row (cascodes / VBP_TOP mirror / logic P) and T1 row
    (MP_TOP load / net9 mirror / switches).  Logic N + EN_B switches below the well."""
    yA0 = Y["npair_top"] + 300
    Y["A0"] = yA0
    yRb = yA0 + 180 + 145
    L0, L1, L2, L3 = yRb, yRb + 145 + RS + 160, yRb + 145 + RS + 160 + TP, yRb + 145 + RS + 160 + 2 * TP
    yT2 = L3 + 250
    yT1 = yT2 + 2000 + 485 + 210 + 485
    yEN = yT1 - 625
    tA, tB, tC = yT1 + 400, yT1 + 1000, yT1 + 1600
    yRt = yT1 + 2000 + RS + 145
    Y.update(dict(L0=L0, L1=L1, L2=L2, L3=L3, T2=yT2, T1=yT1, EN=yEN, tA=tA, tB=tB, tC=tC,
                  Rb=yRb, Rt=yRt))
    cn = {"n3": yT2 + 1355, "n4": yT2 + 1955}       # core T1/T2 channel tracks
    Y.update(cn3=cn["n3"], cn4=cn["n4"])
    W2, L2u = 2000, 2000
    pg = {}
    # ---------------- T1 core: MP_TOP_L1 (A,n3) / L2 (B,n4) ABBA x3, gate net5 bottom ----------
    pat = "ABBAABBAABBA"
    term = {"A": ("VDD", "n3"), "B": ("VDD", "n4")}
    nW = 13 * SD + 12 * L2u
    x0 = XCC - nW // 2
    st = chain(list(pat), "n3", term)
    mt = mos_segment(lay, x0, yT1, "p", W2, L2u, ["net5"] * 12, st, {"net5": "bot"})
    strips_to_rail(lay, mt, "VDD", yRt)
    strips_to_track(lay, mt, "n3", cn["n3"])
    strips_to_track(lay, mt, "n4", cn["n4"])
    pg["mptop"] = mt
    # ---------------- T2 core: MP_CASC [A4][B4][B4][A4] W.5 L.5 gate VBPC top ---------------
    term = {"A": ("n3", "n5"), "B": ("n4", "VOUT")}
    x = XCC - (4 * (5 * SD + 4 * 500) + 3 * 270) // 2
    cas = []
    for dev in "ABBA":
        stp = chain([dev] * 4, "n3" if dev == "A" else "n4", term)
        sg = mos_segment(lay, x, yT2, "p", 500, 500, ["VBPC"] * 4, stp, {"VBPC": "top"})
        cas.append(sg)
        x = sg.x2 + 270
    for sg in cas:
        strips_to_track(lay, sg, "n3", cn["n3"])
        strips_to_track(lay, sg, "n4", cn["n4"])
        strips_to_track(lay, sg, "n5", L1)
        strips_to_track(lay, sg, "VOUT", L2)
    # VBP_CASC diode stack: VDD |1| . |2| . |3| VBPC
    xs = cas[-1].x2 + 600
    stk = mos_segment(lay, xs, yT2, "p", 500, 500, ["VBPC"] * 3, ["VDD", None, None, "VBPC"],
                      {"VBPC": "top"})
    cx = stk.sx[-1]
    sy1 = yT2 + 500 + 235
    lay.rect("locali", cx - 85, stk.cy2, cx + 85, sy1 + 170)
    lay.rect("locali", cas[0].gx[0][0], sy1, cx + 85, sy1 + 170)      # join all VBPC straps
    strips_to_rail(lay, stk, "VDD", yRb)
    # MP_SW2 [VBPC SW2 VDD] W2 L2 gate EN (top)
    sw2 = mos_segment(lay, stk.x2 + 300, yT2, "p", W2, L2u, ["EN"], ["VBPC", "VDD"], {"EN": "top"})
    lay.rect("locali", cx, yT2 + 100, sw2.sx[0], yT2 + 400)          # VBPC jumper stack->SW2
    strips_to_rail(lay, sw2, "VDD", yRb)
    strips_to_track(lay, sw2, "VBPC", L3)
    pg.update(cas=cas, stk=stk, sw2=sw2)
    # core VDD m1 rail at the bottom of nwell A, li-only tap across the bias column
    xc1, xc2 = 2300, XB0 - 300
    tap_strip(lay, "n", xc1, xc2, yRb)
    tap_strip(lay, "n", xc2 + 300, XB0 + 45690, yRb, m1=False)
    # top VDD rail (full width)
    tap_strip(lay, "n", xc1, XB0 + 45690, yRt)
    lay.rect("nwell", xc1 - 180, yA0, XB0 + 45690 + 180, yRt + 145 + 180)
    Y["top"] = yRt + 145 + 180

    # ---------------- T2 bias ----------------------------------------------------------------
    x = XB0 + 300
    def seg(name, W, L, gates, strips, side, y=yT2):
        nonlocal x
        sg = mos_segment(lay, x, y, "p", W, L, gates, strips, side)
        pg[name] = sg
        x = sg.x2 + 300
        return sg
    seg("sw3", W2, L2u, ["EN"], ["n5", "VDD"], {"EN": "top"})
    seg("m9", W2, L2u, ["VBPT"] * 2, ["n8", "VDD", "n8"], {"VBPT": "top"})
    seg("m15", 500, 1000, ["EN"], ["VDD", "VBPT"], {"EN": "top"})
    seg("m34", W2, L2u, ["VBPT"] * 2, ["VBPT", "VDD", "MTB"], {"VBPT": "top"})
    seg("m2", W2, L2u, ["VBPT"] * 7, ["VSI", "VDD"] * 4, {"VBPT": "top"})
    seg("m12", 500, 4000, ["VSO"], ["net15", "MTB"], {"VSO": "top"})
    for nm in ("sw3", "m9", "m15", "m34", "m2", "m12"):
        strips_to_track(lay, pg[nm], "VDD", L0)
    strips_to_track(lay, pg["sw3"], "n5", L1)
    strips_to_track(lay, pg["m9"], "n8", L3)
    strips_to_track(lay, pg["m15"], "VBPT", L2)
    strips_to_track(lay, pg["m34"], "VBPT", L2)
    strips_to_track(lay, pg["m34"], "MTB", L3)
    strips_to_track(lay, pg["m2"], "VSI", L1)
    strips_to_track(lay, pg["m12"], "net15", L2)
    strips_to_track(lay, pg["m12"], "MTB", L3)
    # VBPT strap: join m9 / m34 / m2 straps, M3 diode
    sy = yT2 + W2 + 235
    lay.rect("locali", pg["m9"].gx[0][0], sy, pg["m2"].gx[-1][1], sy + 170)
    c = pg["m34"].sx[0]
    lay.rect("locali", c - 85, pg["m34"].cy2, c + 85, sy + 170)
    Y["logic_x0"] = x
    # ---------------- T1 bias: [P4][D C][P4][SW1], gate net9 (bottom) -------------------------
    x = XB0 + 300
    term = {"P": ("VDD", "n7")}
    seg("p4a", W2, L2u, ["net9"] * 4, chain(list("PPPP"), "n7", term), {"net9": "bot"}, y=yT1)
    seg("dc", W2, L2u, ["net9"] * 2, ["net9", "VDD", "VBNC"], {"net9": "bot"}, y=yT1)
    seg("p4b", W2, L2u, ["net9"] * 4, chain(list("PPPP"), "n7", term), {"net9": "bot"}, y=yT1)
    seg("sw1", W2, L2u, ["EN"], ["VDD", "net9"], {"EN": "bot"}, y=yT1)
    for nm in ("p4a", "dc", "p4b", "sw1"):
        strips_to_rail(lay, pg[nm], "VDD", yRt)
    for nm in ("p4a", "p4b"):
        strips_to_track(lay, pg[nm], "n7", tA)
    strips_to_track(lay, pg["dc"], "net9", tB)
    strips_to_track(lay, pg["sw1"], "net9", tB)
    strips_to_track(lay, pg["dc"], "VBNC", tC)
    sy = yT1 - 235 - 170
    lay.rect("locali", pg["p4a"].gx[0][0], sy, pg["p4b"].gx[-1][1], sy + 170)
    c = pg["dc"].sx[0]
    lay.rect("locali", c - 85, sy, c + 85, pg["dc"].cy1)          # MP_PDIFF_BIAS_B diode
    ROWS["top"] = pg


def build_logic():
    """EN inverter (M6/M5), VSTRP_IP inverter (M43/M42), start-up gate (M13,M14 / M38,M39),
    EN_B switches MN_SW1/MN_SW2 and XM16.  PMOS share the T2 row; NMOS sit under nwell A."""
    yT2 = Y["T2"]
    yNt = Y["A0"] - 400            # N-row diffusion top
    yNb = yNt - 1000
    yTr = yNb - 250                # VBNC / EN_B local track under the N row
    yG = yTr - 160 - RS - 145      # GNDA rail centre
    Y.update(Nt=yNt, Ntr=yTr, NG=yG)
    tap_strip(lay, "p", XB0 + 2900, XB0 + 45690, yG)
    lay.rect("metal1", 30365, yG - 145, XB0 + 2900, yG + 145)       # GNDA link to NMOS-pair ring
    lg = {}
    # --- MN_SW1 (L1) / MN_SW2 (L2) [n8 SW1 GNDA SW2 VBNC], gate EN_B on top ---
    sw = mos_segment(lay, 45000, yNb, "n", 1000, [1000, 2000], ["EN_B", "EN_B"],
                     ["n8", "GNDA", "VBNC"], {"EN_B": "top"})
    strips_to_track(lay, sw, "n8", Y["L3"])
    strips_to_track(lay, sw, "VBNC", yTr)
    strips_to_rail(lay, sw, "GNDA", yG)
    sy = yNt + 190
    lay.rect("locali", sw.gx[0][0], sy, 49685, sy + 170)
    lay.mcon(49600, sy + 85)
    lay.vwire("metal1", 49600, sy + 85, yTr, 260)
    lay.via1(49600, yTr, horiz=False)
    VIA_REG.setdefault(yTr, []).append((49600, "EN_B"))
    lg["sw"] = sw
    # --- XM16 [GNDA M16 MTB] W0.5 L6.4 gate EN_B top ---
    m16 = mos_segment(lay, 60615, yNt - 500, "n", 500, 6400, ["EN_B"], ["GNDA", "MTB"], {"EN_B": "top"})
    strips_to_rail(lay, m16, "GNDA", yG)
    strips_to_track(lay, m16, "MTB", Y["L3"])
    lay.rect("locali", m16.gx[0][1] - 10, sy, 68135, sy + 170)
    lay.mcon(68050, sy + 85)
    lay.vwire("metal1", 68050, sy + 85, yTr, 260)
    lay.via1(68050, yTr, horiz=False)
    VIA_REG.setdefault(yTr, []).append((68050, "EN_B"))
    lg["m16"] = m16
    # --- logic columns: P over N, single-finger L=0.15 devices with li tails ---
    cols = [("VSI", ("VDD", "n14"), ("GNDA", "n14"), "VSI"),     # M43 / M42
            ("EN", ("VDD", "EN_B"), ("GNDA", "EN_B"), "EN"),     # M6  / M5
            ("n14", ("VDD", "VSO"), ("net13", "VSO"), "n14"),    # M13 / M38
            ("EN_B", ("VDD", "VSO"), ("GNDA", "net13"), "EN")]   # M14 / M39
    X0 = 79200
    for k, (gp, (ps, pd), (ns, nd), gn) in enumerate(cols):
        x = X0 + k * 1700
        ntail = 400 if k < 3 else 1000
        P = mos_short(lay, x, yT2, "p", 1000, gp, ps, pd, head="top", tail=400, s_w=500)
        N = mos_short(lay, x, yNb, "n", 1000, gn, ns, nd, head="top", tail=ntail, s_w=500)
        lg[f"P{k}"], lg[f"N{k}"] = P, N
        # sources
        strips_to_track(lay, P, "VDD", Y["L0"])
        strips_to_rail(lay, N, "GNDA", yG)
        # tails -> m1 verticals
        for d in (P, N):
            lay.mcon(d.tail[0], d.tail[1], m1_ext_x=45, m1_ext_y=60)
        if k < 3:      # common gate: join P and N tails
            lay.vwire("metal1", P.tail[0], N.tail[1] - 145, P.tail[1] + 145, 260)
        # drains
        if pd == nd:
            cx = P.sx[1]
            lay.vwire("metal1", cx, N.cy1 - 60, P.cy2 + 60, M1_W)
    # gate / drain hookups to tracks
    L = lg
    def via_at(x, y, net):
        near = [v for v in VIA_REG.get(y, []) if abs(v[0] - x) < 600]
        if any(v[1] != net for v in near):
            raise ValueError(f"via clash {net} {x} {y} {near}")
        lay.via1(x, y, horiz=False)
        VIA_REG.setdefault(y, []).append((x, net))
    via_at(L["P0"].tail[0], Y["L1"], "VSI")
    via_at(L["P0"].sx[1], Y["L2"], "n14")
    lay.vwire("metal1", L["P1"].tail[0], L["P1"].tail[1], Y["EN"], 260)
    via_at(L["P1"].tail[0], Y["EN"], "EN")
    lay.vwire("metal1", L["N1"].sx[1], L["N1"].cy1, yTr, M1_W)
    via_at(L["N1"].sx[1], yTr, "EN_B")
    via_at(L["P2"].tail[0], Y["L2"], "n14")
    via_at(L["P2"].sx[1], Y["L3"], "VSO")
    # col 3: P gate EN_B down to yTr; N gate EN up to EN track; P drain VSO to L3
    lay.vwire("metal1", L["P3"].tail[0], L["P3"].tail[1], yTr, 260)
    via_at(L["P3"].tail[0], yTr, "EN_B")
    lay.vwire("metal1", L["N3"].tail[0], L["N3"].tail[1], Y["EN"], 260)
    via_at(L["N3"].tail[0], Y["EN"], "EN")
    strips_to_track(lay, L["P3"], "VSO", Y["L3"])
    # net13: li jumper under the N row from N3 drain (right) to N2 source (left)
    yj = yNb - 360
    a, b = L["N2"].sx[0], L["N3"].sx[1]
    lay.rect("locali", a - 85, yj, a + 85, L["N2"].cy1 - 80)
    lay.rect("locali", b - 85, yj, b + 85, L["N3"].cy1 - 80)
    lay.rect("locali", a - 85, yj, b + 85, yj + 170)
    ROWS["logic"] = lg


BUSX = dict(VINP=600, n5=1400, n1=2200, n3=5000, n6=20000, n4=32200, VBNC=33000, n9=33800,
            VBPC=34600, n8=35400, VINN=38300, n2=39100, VOUT=39900, n7=40700, n12=43000,
            VBPT=51000, MTB=58000, VDDR=60000, net15=75100, VSI=77460)


def sx_of(segs, net):
    return [s.sx[i] for s in segs for i, n in enumerate(s.strip_net) if n == net]


def route():
    pts = {k: [] for k in BUSX}

    def T(net, y, xs, bus_net=None):
        bn = bus_net or net
        bx = BUSX[bn]
        m2_track(lay, min(xs + [bx]), max(xs + [bx]), y)
        lay.via2(bx, y)
        pts[bn].append(y)

    def stack_at(net, x, y):
        """m1 pad already present at (x,y): drop via1+via2 to the bus at x"""
        lay.via1(x, y)
        lay.via2(x, y)
        pts[net].append(y)

    M = ROWS["mirror"]
    segs_b, segs_a = M["segs"]["b"], M["segs"]["a"]
    tb, ta = M["tb"], M["ta"]
    T("n1", tb["n1"], sx_of(segs_b, "n1"))
    T("n2", tb["n2"], sx_of(segs_b, "n2"))
    T("n6", tb["n6"], sx_of(segs_b, "n6"))
    T("VBPC", tb["VBPC"], sx_of(segs_b, "VBPC"))
    T("n1", ta["n1"], sx_of(segs_a, "n1"))
    T("n2", ta["n2"], sx_of(segs_a, "n2"))
    T("n6", ta["n6"], sx_of(segs_a, "n6"))
    T("n8", ta["n8"], sx_of(segs_a, "n8"))
    T("n9", ta["n9"], sx_of(segs_a, "n9"))
    C = ROWS["mncasc"]
    for net in ("n1", "n2", "n5", "VOUT"):
        T(net, C["tr"][net], sx_of(C["segs"], net))
    st = C["stack"]
    stripe_to(lay, st, len(st.strip_net) - 1, C["tr"]["n1"])
    lay.via1(st.sx[-1], C["tr"]["n1"], horiz=False)
    T("VBNC", C["tr"]["n1"], [st.sx[-1]])
    PP = ROWS["ppair"]
    for s, t in zip(PP["segs"], PP["tr"]):
        for net in ("n1", "n2", "n7"):
            T(net, t[net], sx_of([s], net))
    T("VINP", PP["sy"]["S2"], [PP["xbl"]])
    T("VINN", PP["sy"]["S2"], [PP["xbr"]])
    NP = ROWS["npair"]
    for s, t in zip(NP["segs"], NP["tr"]):
        for net in ("n3", "n4", "n6"):
            T(net, t[net], sx_of([s], net))
    T("VINP", NP["sy"]["S1"], [NP["xbl"]])
    T("VINN", NP["sy"]["S1"], [NP["xbr"]])
    # ---- top rows ----
    pg = ROWS["top"]
    T("n3", Y["cn3"], sx_of([pg["mptop"]] + pg["cas"], "n3"))
    T("n4", Y["cn4"], sx_of([pg["mptop"]] + pg["cas"], "n4"))
    T("n5", Y["L1"], sx_of(pg["cas"] + [pg["sw3"]], "n5"))
    T("VOUT", Y["L2"], sx_of(pg["cas"], "VOUT"))
    T("VBPC", Y["L3"], sx_of([pg["sw2"]], "VBPC"))
    T("n8", Y["L3"], sx_of([pg["m9"], ROWS["logic"]["sw"]], "n8"))
    T("VBPT", Y["L2"], sx_of([pg["m15"], pg["m34"]], "VBPT"))
    T("MTB", Y["L3"], sx_of([pg["m34"], pg["m12"], ROWS["logic"]["m16"]], "MTB"))
    T("VSI", Y["L1"], sx_of([pg["m2"]], "VSI") + [ROWS["logic"]["P0"].tail[0]])
    T("net15", Y["L2"], sx_of([pg["m12"]], "net15"))
    T("n7", Y["tA"], sx_of([pg["p4a"], pg["p4b"]], "n7"))
    T("n9", Y["tB"], sx_of([pg["dc"], pg["sw1"]], "net9"))
    T("VBNC", Y["tC"], sx_of([pg["dc"]], "VBNC"))
    T("VBNC", Y["Ntr"], sx_of([ROWS["logic"]["sw"]], "VBNC"))
    # net5 gate strap (MP_TOP, bottom) -> n5 bus via li extension
    sy = Y["T1"] - 235 - 85
    lay.rect("locali", BUSX["n5"] - 85, sy - 85, pg["mptop"].gx[0][0] + 100, sy + 85)
    lay.mcon(BUSX["n5"], sy)
    stack_at("n5", BUSX["n5"], sy)
    # ---- logic-local tracks ----
    lg = ROWS["logic"]
    m2_track(lay, lg["P0"].sx[1], lg["P2"].tail[0], Y["L2"])                  # n14
    m2_track(lay, 78750, lg["P3"].sx[1], Y["L3"])                             # VSO
    m2_track(lay, 49600, lg["P3"].tail[0], Y["Ntr"])                         # EN_B
    # M12 gate (VSO) exit
    m12 = pg["m12"]
    gy = Y["T2"] + 500 + 235 + 85
    lay.rect("locali", m12.gx[0][1] - 10, gy - 85, 78835, gy + 85)
    lay.mcon(78750, gy)
    lay.vwire("metal1", 78750, gy, Y["L3"], 260)
    lay.via1(78750, Y["L3"], horiz=False)
    # ---- EN track: SW2, SW3, M15 (T2 straps), SW1 (T1 strap), logic ----
    yEN = Y["EN"]
    en_x = []
    for nm, side in (("sw2", "top"), ("sw3", "top"), ("m15", "top"), ("sw1", "bot")):
        s = pg[nm]
        gx = (s.gx[0][0] + s.gx[0][1]) // 2
        sy = (s.ytop + 235 + 85) if side == "top" else (s.ybot - 235 - 85)
        lay.mcon(gx, sy)
        lay.vwire("metal1", gx, sy, yEN, 260)
        lay.via1(gx, yEN, horiz=False)
        en_x.append(gx)
    xr = XB0 + 45690
    m2_track(lay, min(en_x), xr - 160, yEN)
    # ---- bias column ----
    X = ROWS["xm1"]
    rows = X["rows"]
    for segs, t in zip(rows, X["tr"]):
        T("n12", t["n12"], sx_of(segs, "n12"))
        T("VBPT", t["VBPT"], sx_of(segs, "VBPT"))
        T("MTB", t["MTB"], sx_of(segs, "MTB"))
        rx1, _, rx2, _ = X["ring"]
        m2_track(lay, rx1 + 145, rx2 - 145, t["GNDA"])
        for xx in (rx1 + 145, rx2 - 145):
            lay.via1(xx, t["GNDA"], horiz=False)
    R = ROWS["res"]
    h = R["heads"]
    stack_at("n12", BUSX["n12"], h[0][0][1])            # R14 bottom head
    stack_at("VDDR", BUSX["VDDR"], h[9][0][1])          # R24 bottom head
    stack_at("net15", BUSX["net15"], h[17][1][1])       # R34 top head
    # R22 top head -> GNDA rail (m1)
    x22, y22 = h[8][1]
    lay.rect("metal1", x22 - 200, y22, x22 + 200, Y["NG"])
    S = ROWS["stack"]
    stack_at("VSI", S["vsi"][0], S["vsi"][1])
    lay.rect("metal1", S["gnd"][0] - 200, S["gnd"][1], S["gnd"][0] + 200, Y["NG"])
    gx, gy = S["gate"]
    lay.via1(gx, gy)
    m2_track(lay, BUSX["VDDR"], gx, gy)
    lay.via2(BUSX["VDDR"], gy)
    pts["VDDR"].append(gy)
    T("VDDR", Y["L0"], [], bus_net="VDDR")
    # ---- power ----
    # VDD m2 track L0 across the bias column (+ link to core m1 rail), taps tied with mcon
    m2_track(lay, 41155, lg["P3"].sx[0], Y["L0"])
    lay.via1(41155, Y["L0"], horiz=False)
    lay.rect("metal1", 2300, Y["Rb"] - 145, 41300, Y["Rb"] + 145)
    for (vx, vn) in VIA_REG.get(Y["L0"], []):
        if vn == "VDD" and vx > XB0:
            lay.rect("viali", vx - 85, Y["L0"] - 85, vx + 85, Y["L0"] + 85)
    lay.rect("metal1", 41010, Y["Rb"] - 145, 41300, Y["Rt"])                  # right VDD link
    ring = PP["ring"]
    lay.rect("metal1", ring[0], ring[3] - 290, ring[0] + 290, Y["Rt"])       # left VDD link
    lay.rect("metal1", 2500, Y["rail0"], 2790, Y["rail1"])                   # left GNDA link
    rx2 = X["ring"][2]
    lay.rect("metal1", rx2 - 290, X["ring"][3] - 290, rx2, Y["NG"])          # right GNDA link
    # ---- pins: extend buses ----
    pts["VINN"].append(Y["top"] - 200)
    pts["VOUT"].append(400)
    pts["MTB"].append(400)
    for net, ys in pts.items():
        if ys:
            bus(net, BUSX[net], min(ys), max(ys))
    # internal net labels (names as in the schematic netlist; not ports)
    NAMES = dict(n1="net1", n2="net2", n3="net3", n4="net4", n5="net5", n6="net6", n7="net7",
                 n8="net8", n9="net9", VBPC="VBP_CASC", VBNC="VBN_CASC", n12="net12",
                 VBPT="VBP_TOP", net15="net15", VSI="VSTRP_IP")
    for net, nm in NAMES.items():
        x, y = BUSX[net], pts[net][0]
        lay.label(nm, "metal3", x - 100, y - 100, x + 100, y + 100)
    lay.label("VSTRP_OUT", "metal2", 78750 - 100, Y["L3"] - 100, 78750 + 100, Y["L3"] + 100)
    x14 = lg["P0"].sx[1]
    lay.label("net14", "metal2", x14 - 100, Y["L2"] - 100, x14 + 100, Y["L2"] + 100)
    lay.label("EN_B", "metal2", 49600 - 100, Y["Ntr"] - 100, 49600 + 100, Y["Ntr"] + 100)
    # labels / ports  (order: VDD EN VINN VOUT VINP MN_TAIL_BIAS GNDA)
    lay.label("VDD", "metal1", 3000, Y["Rt"] - 100, 3200, Y["Rt"] + 100, 1)
    lay.label("EN", "metal2", xr - 400, yEN - 100, xr - 200, yEN + 100, 2)
    lay.label("VINN", "metal3", BUSX["VINN"] - 100, Y["top"] - 500, BUSX["VINN"] + 100, Y["top"] - 300, 3)
    lay.label("VOUT", "metal3", BUSX["VOUT"] - 100, 300, BUSX["VOUT"] + 100, 500, 4)
    lay.label("VINP", "metal3", BUSX["VINP"] - 100, PP["sy"]["S2"] + 400, BUSX["VINP"] + 100,
              PP["sy"]["S2"] + 600, 5)
    lay.label("MN_TAIL_BIAS", "metal3", BUSX["MTB"] - 100, 300, BUSX["MTB"] + 100, 500, 6)
    lay.label("GNDA", "metal1", 3000, Y["rail0"] - 100, 3200, Y["rail0"] + 100, 7)


PARTS = sys.argv[1:] or ["all"]

if __name__ == "__main__":
    build_core_bottom()
    build_mn_casc()
    build_pmos_pair()
    build_nmos_pair()
    build_xm1()
    build_resistors()
    build_top()
    build_logic()
    route()
    out = os.environ.get("OTA_OUT") or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mag")
    log = build(lay, out, extract=True)
    print([l for l in log.splitlines() if "DRC_TOTAL" in l])
