"""Run magic in batch on a generated Layout: paint, save, DRC report, extract."""
import os
import subprocess

PDK_ROOT = os.environ.get("PDK_ROOT", os.path.expanduser("~/.ciel"))
RC = f"{PDK_ROOT}/sky130A/libs.tech/magic/sky130A.magicrc"


def run_tcl(script, cwd, log="magic.log", timeout=900):
    path = os.path.join(cwd, "_run.tcl")
    with open(path, "w") as f:
        f.write(script)
    env = dict(os.environ, PDK_ROOT=PDK_ROOT, PDK="sky130A")
    with open(os.path.join(cwd, log), "w") as lf:
        subprocess.run(["magic", "-dnull", "-noconsole", "-rcfile", RC, path],
                       cwd=cwd, stdout=lf, stderr=subprocess.STDOUT,
                       stdin=subprocess.DEVNULL, env=env, timeout=timeout)
    return open(os.path.join(cwd, log)).read()


DRC_DUMP = r"""
proc drc_dump {fname} {
    set fo [open $fname w]
    select top cell
    drc check
    drc catchup
    set tot 0
    foreach {why boxes} [drc listall why] {
        foreach b $boxes {
            set coords {}
            foreach c $b { lappend coords [expr {$c * 0.005}] }
            puts $fo "$why | $coords"
            incr tot
        }
    }
    close $fo
    puts "DRC_TOTAL $tot"
}
"""


def build(lay, cwd, extract=True, gds=True, drc=True, extra=""):
    os.makedirs(cwd, exist_ok=True)
    for ext in (".mag", ".ext", ".drc", ".gds", ".lvs.spice"):
        p = os.path.join(cwd, lay.name + ext)
        if os.path.exists(p):
            os.remove(p)
    s = DRC_DUMP + lay.tcl()
    s += f"save {lay.name}\n"
    if drc:
        s += f"drc euclidean on\ndrc style drc(full)\ndrc_dump {lay.name}.drc\n"
    if gds:
        s += f"gds write {lay.name}.gds\n"
    if extract:
        s += ("select top cell\nextract all\next2spice lvs\n"
              f"ext2spice -o {lay.name}.lvs.spice\n")
    s += extra
    s += "quit -noprompt\n"
    return run_tcl(s, cwd)
