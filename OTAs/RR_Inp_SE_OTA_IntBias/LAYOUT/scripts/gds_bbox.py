import pya
ly = pya.Layout(); ly.read(gds)
top = ly.top_cell(); b = top.dbbox()
print(f"BBOX {b.left:.3f} {b.bottom:.3f} {b.right:.3f} {b.top:.3f} W={b.width():.3f} H={b.height():.3f} A={b.width()*b.height():.1f} top={top.name}")
