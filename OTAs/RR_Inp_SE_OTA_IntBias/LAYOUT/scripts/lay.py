"""
Minimal programmatic layout library for magic / sky130A.

All coordinates are integer nanometres on a 5 nm grid.  Shapes are collected per
magic layer and emitted as a Tcl script (box/paint) in a fixed layer order so that
magic's paint rules build devices (diff + poly -> mos) and stacked contacts.
"""
import collections

GRID = 5


def sn(v):
    """snap to 5 nm grid"""
    return int(round(v / GRID)) * GRID


# paint order: base layers first, device/contacts later, metals last
ORDER = [
    "nwell", "pwell",
    "ndiff", "pdiff", "nsubdiff", "psubdiff",
    "poly",
    "xpolyres", "xpolycontact",
    "nmos", "pmos", "nmoslvt", "pmoslvt",
    "ndiffc", "pdiffc", "nsubdiffcont", "psubdiffcont", "polycont",
    "locali", "viali",
    "metal1", "via1",
    "metal2", "via2",
    "metal3", "via3",
    "metal4",
]

# rule constants (nm)
CT = 170          # licon / mcon size
GC = 60           # gate to diff-contact spacing used by PDK generator
SD = GC + CT + GC  # 290: width of a contacted S/D strip between two gates
PC_GAP = 190      # diff edge -> poly contact edge
HEAD = PC_GAP + CT + 80   # 440: poly extension beyond diff for a contacted gate
ENDCAP = 130      # poly extension beyond diff (no contact)
LI_EXT = 80       # li overlap of contact (directional)
M1_W = 260        # S/D metal1 stripe width (fits via1)
V1 = 260          # drawn via1 (magic size incl. surround)
V2 = 280          # drawn via2
M2_W = 300        # metal2 track width
M3_W = 400        # metal3 bus width


class Layout:
    def __init__(self, name):
        self.name = name
        self.shapes = collections.defaultdict(list)
        self.labels = []   # (net, layer, x1,y1,x2,y2, port_index or None)

    # ------------------------------------------------------------ basic
    def rect(self, layer, x1, y1, x2, y2):
        x1, x2 = sorted((sn(x1), sn(x2)))
        y1, y2 = sorted((sn(y1), sn(y2)))
        if x1 == x2 or y1 == y2:
            raise ValueError(f"zero-size {layer} {x1} {y1} {x2} {y2}")
        self.shapes[layer].append((x1, y1, x2, y2))
        return (x1, y1, x2, y2)

    def label(self, net, layer, x1, y1, x2, y2, port=None):
        self.labels.append((net, layer, sn(x1), sn(y1), sn(x2), sn(y2), port))

    # ------------------------------------------------------------ vias
    def mcon(self, cx, cy, m1_ext_x=60, m1_ext_y=60):
        """li -> m1 contact centred at (cx,cy); paints li pad, mcon, m1 pad"""
        h = CT // 2
        self.rect("locali", cx - h, cy - h - LI_EXT, cx + h, cy + h + LI_EXT)
        self.rect("viali", cx - h, cy - h, cx + h, cy + h)
        self.rect("metal1", cx - h - m1_ext_x, cy - h - m1_ext_y,
                  cx + h + m1_ext_x, cy + h + m1_ext_y)

    def via1(self, cx, cy, m1=True, m2=True, horiz=True):
        h = V1 // 2
        self.rect("via1", cx - h, cy - h, cx + h, cy + h)
        if m1:
            if horiz:
                self.rect("metal1", cx - h - 30, cy - h, cx + h + 30, cy + h)
            else:
                self.rect("metal1", cx - h, cy - h - 30, cx + h, cy + h + 30)
        if m2:
            if horiz:
                self.rect("metal2", cx - h - 30, cy - h - 20, cx + h + 30, cy + h + 20)
            else:
                self.rect("metal2", cx - h - 20, cy - h - 30, cx + h + 20, cy + h + 30)

    def via2(self, cx, cy, m2=True, m3=True):
        h = V2 // 2
        self.rect("via2", cx - h, cy - h, cx + h, cy + h)
        if m2:
            self.rect("metal2", cx - h - 45, cy - h - 10, cx + h + 45, cy + h + 10)
        if m3:
            self.rect("metal3", cx - 200, cy - 200, cx + 200, cy + 200)

    def via3(self, cx, cy):
        h = 160
        self.rect("via3", cx - h, cy - h, cx + h, cy + h)
        self.rect("metal3", cx - h - 30, cy - h - 30, cx + h + 30, cy + h + 30)
        self.rect("metal4", cx - h - 30, cy - h - 30, cx + h + 30, cy + h + 30)

    def li_m2(self, cx, cy):
        """li pad -> m1 -> m2 at one spot"""
        self.mcon(cx, cy, m1_ext_x=45, m1_ext_y=60)
        self.via1(cx, cy)

    def m1_m3(self, cx, cy):
        self.via1(cx, cy)
        self.via2(cx, cy)

    # ------------------------------------------------------------ wires
    def hwire(self, layer, x1, x2, y, w):
        return self.rect(layer, min(x1, x2) , y - w // 2, max(x1, x2), y + w // 2)

    def vwire(self, layer, x, y1, y2, w):
        return self.rect(layer, x - w // 2, min(y1, y2), x + w // 2, max(y1, y2))

    # ------------------------------------------------------------ output
    def tcl(self):
        out = []
        out.append(f"load {self.name} -force")
        out.append("snap internal")
        out.append("box 0 0 0 0")
        for layer in ORDER:
            for (x1, y1, x2, y2) in self.shapes.get(layer, []):
                out.append(f"box {x1/1000:.3f}um {y1/1000:.3f}um {x2/1000:.3f}um {y2/1000:.3f}um")
                out.append(f"paint {layer}")
        unknown = set(self.shapes) - set(ORDER)
        if unknown:
            raise ValueError(f"layers not in ORDER: {unknown}")
        for (net, layer, x1, y1, x2, y2, port) in self.labels:
            out.append(f"box {x1/1000:.3f}um {y1/1000:.3f}um {x2/1000:.3f}um {y2/1000:.3f}um")
            out.append(f"label {net} FreeSans 0.2 0 0 0 c {layer}")
            if port is not None:
                out.append(f"port make {port}")
                out.append("port use signal")
                out.append("port class inout")
        return "\n".join(out) + "\n"

    def bbox(self, layers=None):
        xs, ys = [], []
        for layer, rs in self.shapes.items():
            if layers and layer not in layers:
                continue
            for r in rs:
                xs += [r[0], r[2]]
                ys += [r[1], r[3]]
        return min(xs), min(ys), max(xs), max(ys)


# ====================================================================
#  MOS segment
# ====================================================================
class Seg:
    """Result of a MOS segment: strip centres, gate ranges, contact y-range"""
    pass


def mos_segment(lay, x0, y0, kind, W, L, gates, strips, gate_side,
                lvt=False, contact_strips=None, li_strap=True, strap_ext=(0, 0)):
    """
    Draw one continuous-diffusion MOS segment.

    x0,y0      : lower-left of diffusion
    kind       : 'n' or 'p'
    W, L       : finger width / length (nm)
    gates      : list of gate net names (len N); 'DUMMY' not allowed (no fake devices)
    strips     : list of S/D net names (len N+1); None => uncontacted (series stack)
    gate_side  : dict gate-net -> 'top' | 'bot' | 'none'
    returns Seg with .sx (strip centres), .gx (gate x1,x2), .x1 .x2, .ytop .ybot,
            .strap[(net,side)] = (x1,x2,yc) of li strap
    """
    n = len(gates)
    assert len(strips) == n + 1
    Ls = list(L) if isinstance(L, (list, tuple)) else [L] * n
    diff = "ndiff" if kind == "n" else "pdiff"
    dc = "ndiffc" if kind == "n" else "pdiffc"
    mos = ("nmoslvt" if lvt else "nmos") if kind == "n" else ("pmoslvt" if lvt else "pmos")
    s = Seg()
    pcg = PC_GAP if kind == "n" else 235
    head = pcg + CT + 80
    s.pcg, s.head = pcg, head
    s.sx, s.gx, s.strip_net = [], [], list(strips)
    s.gate_net = list(gates)
    x = x0
    # uncontacted inner strips only need poly spacing (210)
    widths = []
    for i, net in enumerate(strips):
        if net is None:
            assert 0 < i < n, "end strips must be contacted"
            widths.append(210)
        else:
            widths.append(SD)
    for i in range(n + 1):
        s.sx.append(x + widths[i] // 2)
        x += widths[i]
        if i < n:
            s.gx.append((x, x + Ls[i]))
            x += Ls[i]
    x1d, x2d = x0, x
    s.x1, s.x2 = x1d, x2d
    s.ybot, s.ytop = y0, y0 + W
    lay.rect(diff, x1d, y0, x2d, y0 + W)
    # gates
    for i, (gx1, gx2) in enumerate(s.gx):
        side = gate_side.get(gates[i], "top")
        top = y0 + W + (head if side == "top" else ENDCAP)
        bot = y0 - (head if side == "bot" else ENDCAP)
        if Ls[i] < 330 and side in ("top", "bot"):
            raise ValueError("short-L contacted gates need dogbone; not supported here")
        lay.rect("poly", gx1, bot, gx2, top)
        if lvt:
            lay.rect(mos, gx1, y0, gx2, y0 + W)
        if side in ("top", "bot"):
            if side == "top":
                cy1 = y0 + W + pcg
            else:
                cy1 = y0 - pcg - CT
            lay.rect("polycont", gx1 + 80, cy1, gx2 - 80, cy1 + CT)
            # li over poly contact (extends 80 in x via strap or pad)
            lay.rect("locali", gx1, cy1, gx2, cy1 + CT)
    # straps per (net, side): li bar across all gates of that net
    s.strap = {}
    groups = collections.defaultdict(list)
    for i, g in enumerate(gates):
        side = gate_side.get(g, "top")
        if side in ("top", "bot"):
            groups[(g, side)].append(s.gx[i])
    for (g, side), rngs in groups.items():
        xa = min(r[0] for r in rngs) - strap_ext[0]
        xb = max(r[1] for r in rngs) + strap_ext[1]
        cy1 = y0 + W + pcg if side == "top" else y0 - pcg - CT
        if li_strap:
            lay.rect("locali", xa, cy1, xb, cy1 + CT)
        s.strap[(g, side)] = (xa, xb, cy1 + CT // 2)
    # S/D contacts
    s.cy1, s.cy2 = y0 + 60, y0 + W - 60
    for i, net in enumerate(strips):
        if net is None:
            continue
        cx = s.sx[i]
        lay.rect("locali", cx - CT // 2, s.cy1 - LI_EXT, cx + CT // 2, s.cy2 + LI_EXT)
        lay.rect(dc, cx - CT // 2, s.cy1, cx + CT // 2, s.cy2)
        lay.rect("viali", cx - CT // 2, s.cy1, cx + CT // 2, s.cy2)
        lay.rect("metal1", cx - M1_W // 2, s.cy1 - 60, cx + M1_W // 2, s.cy2 + 60)
    return s


def tap_strip(lay, kind, x1, x2, yc, h=290, m1=True, cx1=None, cx2=None):
    """substrate/well tap strip (horizontal) centred at yc with li + mcon + m1 rail"""
    sub = "psubdiff" if kind == "p" else "nsubdiff"
    cont = "psubdiffcont" if kind == "p" else "nsubdiffcont"
    cx1 = x1 + 120 if cx1 is None else cx1
    cx2 = x2 - 120 if cx2 is None else cx2
    lay.rect(sub, x1, yc - h // 2, x2, yc + h // 2)
    lay.rect(cont, cx1, yc - CT // 2, cx2, yc + CT // 2)
    lay.rect("locali", min(x1, cx1 - LI_EXT), yc - CT // 2, max(x2, cx2 + LI_EXT), yc + CT // 2)
    if m1:
        lay.rect("viali", cx1, yc - CT // 2, cx2, yc + CT // 2)
        lay.rect("metal1", x1, yc - 145, x2, yc + 145)


def vtap_strip(lay, kind, xc, y1, y2, w=290, m1=True, cy1=None, cy2=None):
    sub = "psubdiff" if kind == "p" else "nsubdiff"
    cont = "psubdiffcont" if kind == "p" else "nsubdiffcont"
    cy1 = y1 + 120 if cy1 is None else cy1
    cy2 = y2 - 120 if cy2 is None else cy2
    lay.rect(sub, xc - w // 2, y1, xc + w // 2, y2)
    lay.rect(cont, xc - CT // 2, cy1, xc + CT // 2, cy2)
    lay.rect("locali", xc - CT // 2, min(y1, cy1 - LI_EXT), xc + CT // 2, max(y2, cy2 + LI_EXT))
    if m1:
        lay.rect("viali", xc - CT // 2, cy1, xc + CT // 2, cy2)
        lay.rect("metal1", xc - 145, y1, xc + 145, y2)


def tap_ring(lay, kind, x1, y1, x2, y2, w=290, m1=True):
    """closed guard ring of taps; (x1,y1,x2,y2) is the OUTER boundary"""
    tap_strip(lay, kind, x1, x2, y1 + w // 2, h=w, m1=m1, cx1=x1 + w + 150, cx2=x2 - w - 150)
    tap_strip(lay, kind, x1, x2, y2 - w // 2, h=w, m1=m1, cx1=x1 + w + 150, cx2=x2 - w - 150)
    vtap_strip(lay, kind, x1 + w // 2, y1, y2, w=w, m1=m1)
    vtap_strip(lay, kind, x2 - w // 2, y1, y2, w=w, m1=m1)


# ====================================================================
#  helpers for strip nets / tracks
# ====================================================================
def chain(fingers, first, term):
    """strip nets for a finger sequence. term[dev] = (a, b) S/D nets."""
    s = [first]
    for i, f in enumerate(fingers):
        a, b = term[f]
        cur = s[-1]
        assert cur in (a, b), (fingers, i, cur, term[f])
        s.append(b if cur == a else a)
    return s


def stripe_to(lay, seg, idx, y):
    """extend S/D metal1 stripe of strip idx vertically to y (inclusive of a via pad)"""
    cx = seg.sx[idx]
    ya = min(seg.cy1 - 60, y - 160)
    yb = max(seg.cy2 + 60, y + 160)
    lay.rect("metal1", cx - M1_W // 2, ya, cx + M1_W // 2, yb)


VIA_REG = {}   # y -> list of (x, net)


def strips_to_track(lay, seg, net, y, via=True):
    """connect every strip of `net` in seg to an m2 track at y; returns x list.
    Same-net vias closer than 600 nm are merged with an m1 bridge; a different-net
    via within 600 nm raises."""
    xs = []
    for i, n in enumerate(seg.strip_net):
        if n == net:
            cx = seg.sx[i]
            stripe_to(lay, seg, i, y)
            if via:
                near = [(vx, vn) for (vx, vn) in VIA_REG.get(y, []) if abs(vx - cx) < 600]
                bad = [v for v in near if v[1] != net]
                if bad:
                    raise ValueError(f"via clash {net}@({cx},{y}) vs {bad}")
                if near:
                    vx = near[0][0]
                    lay.rect("metal1", min(vx, cx) - 130, y - 160, max(vx, cx) + 130, y + 160)
                else:
                    lay.via1(cx, y, horiz=False)
                    VIA_REG.setdefault(y, []).append((cx, net))
            xs.append(cx)
    return xs


def strips_to_rail(lay, seg, net, y):
    """extend m1 stripes of `net` to a metal1 rail centred at y"""
    xs = []
    for i, n in enumerate(seg.strip_net):
        if n == net:
            cx = seg.sx[i]
            lay.rect("metal1", cx - M1_W // 2, min(seg.cy1 - 60, y), cx + M1_W // 2,
                     max(seg.cy2 + 60, y))
            xs.append(cx)
    return xs


def m2_track(lay, x1, x2, y, w=M2_W):
    lay.rect("metal2", min(x1, x2) - 160, y - w // 2, max(x1, x2) + 160, y + w // 2)


def mos_short(lay, x0, y0, kind, W, gnet, s_net, d_net, head="top", tail=300, s_w=SD):
    """single finger L=0.15 device with dogbone poly contact and an li tail.
    strips: s_net (left), d_net (right).  Returns Seg with .tail=(x,y) li end point."""
    L = 150
    diff = "ndiff" if kind == "n" else "pdiff"
    dc = "ndiffc" if kind == "n" else "pdiffc"
    pcg = PC_GAP if kind == "n" else 235
    s = Seg()
    s.sx = [x0 + s_w // 2, x0 + s_w + L + SD // 2]
    s.gx = [(x0 + s_w, x0 + s_w + L)]
    s.strip_net = [s_net, d_net]
    s.gate_net = [gnet]
    s.x1, s.x2 = x0, x0 + s_w + SD + L
    s.ybot, s.ytop = y0, y0 + W
    s.cy1, s.cy2 = y0 + 60, y0 + W - 60
    lay.rect(diff, s.x1, y0, s.x2, y0 + W)
    gc = x0 + s_w + L // 2
    if head == "top":
        pcy = y0 + W + pcg
        lay.rect("poly", gc - 75, y0 - ENDCAP, gc + 75, pcy)
    else:
        pcy = y0 - pcg - CT
        lay.rect("poly", gc - 75, pcy + CT, gc + 75, y0 + W + ENDCAP)
    lay.rect("poly", gc - 135, pcy - 80, gc + 135, pcy + CT + 80)
    lay.rect("polycont", gc - 85, pcy, gc + 85, pcy + CT)
    xt = s.x2 + tail
    lay.rect("locali", min(gc - 165, xt - 85), pcy, max(gc + 165, xt + 85), pcy + CT)
    s.tail = (xt, pcy + CT // 2)
    s.pcy = pcy + CT // 2
    for i, net in enumerate(s.strip_net):
        cx = s.sx[i]
        lay.rect("locali", cx - CT // 2, s.cy1 - LI_EXT, cx + CT // 2, s.cy2 + LI_EXT)
        lay.rect(dc, cx - CT // 2, s.cy1, cx + CT // 2, s.cy2)
        lay.rect("viali", cx - CT // 2, s.cy1, cx + CT // 2, s.cy2)
        lay.rect("metal1", cx - M1_W // 2, s.cy1 - 60, cx + M1_W // 2, s.cy2 + 60)
    return s


XRW = 1410     # xhigh_po_1p41 width
XHEAD = 2160   # xpolycontact length


def xres(lay, x, y, Lsch):
    """sky130_fd_pr__res_xhigh_po_1p41, vertical, lower-left (x,y).
    Body drawn Lsch-160 so that magic extracts l=Lsch.  Returns (bot_c, top_c) head centres."""
    Lb = Lsch - 160
    lay.rect("xpolycontact", x, y, x + XRW, y + XHEAD)
    lay.rect("xpolyres", x, y + XHEAD, x + XRW, y + XHEAD + Lb)
    yt = y + XHEAD + Lb
    lay.rect("xpolycontact", x, yt, x + XRW, yt + XHEAD)
    for yy in (y, yt):
        lay.rect("viali", x + 80, yy + 85, x + XRW - 80, yy + XHEAD - 90)
        lay.rect("metal1", x + 50, yy + 25, x + XRW - 50, yy + XHEAD - 30)
    return (x + XRW // 2, y + XHEAD // 2), (x + XRW // 2, yt + XHEAD // 2)
