# klayout -zz -r render.py -rd gds=... -rd png=... [-rd box=x1,y1,x2,y2] [-rd hide=...]
import pya, os
lyp = os.path.join(os.environ.get("PDK_ROOT", os.path.expanduser("~/.ciel")), "sky130A/libs.tech/klayout/tech/sky130A.lyp")
lv = pya.LayoutView()
lv.load_layout(gds, 0)
lv.load_layer_props(lyp)
lv.max_hier()
w = int(globals().get("w", "2000")); h = int(globals().get("h", "1400"))
# hide noisy marker layers
hide = globals().get("hide", "")
if hide:
    hs = set(hide.split(","))
    it = lv.begin_layers()
    while not it.at_end():
        lp = it.current()
        if lp.source_layer >= 0 and f"{lp.source_layer}/{lp.source_datatype}" in hs:
            lp.visible = False
            lv.set_layer_properties(it, lp)
        it.next()
lv.set_config("background-color", "#ffffff")
lv.set_config("grid-visible", "false")
if globals().get("box"):
    x1, y1, x2, y2 = [float(v) for v in box.split(",")]
    lv.zoom_box(pya.DBox(x1, y1, x2, y2))
else:
    lv.zoom_fit()
lv.save_image(png, w, h)
