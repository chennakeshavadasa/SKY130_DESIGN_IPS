"""
debug_raw.py
Writes one netlist, runs ngspice, dumps the raw file header + first 20 lines
so we can fix the parser.
"""
import subprocess, os, textwrap

LIB = "/home/nithin/.ciel/sky130A/libs.tech/combined/sky130.lib.spice"
VDD = 1.8
TMP = "tmp_dbg.spice"
RAW = "tmp_dbg.raw"

netlist = textwrap.dedent(f"""\
    ** debug raw
    .lib {LIB} tt
    .option wnflag=1
    .temp 27
    VVDD VDD 0 {VDD}
    VIN  VIN 0 DC 0
    XM1 net1 VIN  0    GND  sky130_fd_pr__nfet_01v8 L=2.5  W=1.0  nf=1 ad=0.29  as=0.29  pd=2.58  ps=2.58  nrd=0.29   nrs=0.29   sa=0 sb=0 sd=0 mult=1
    XM2 VOUT VIN  net1 GND  sky130_fd_pr__nfet_01v8 L=2.5  W=5.0  nf=1 ad=1.45  as=1.45  pd=10.58 ps=10.58 nrd=0.058  nrs=0.058  sa=0 sb=0 sd=0 mult=1
    XM3 VDD  VOUT net1 GND  sky130_fd_pr__nfet_01v8 L=0.15 W=6.5  nf=1 ad=1.885 as=1.885 pd=13.58 ps=13.58 nrd=0.0446 nrs=0.0446 sa=0 sb=0 sd=0 mult=1
    XM4 VOUT VIN  net2 VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=16.0 nf=1 ad=4.64  as=4.64  pd=32.58 ps=32.58 nrd=0.0181 nrs=0.0181 sa=0 sb=0 sd=0 mult=1
    XM5 net2 VIN  VDD  VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=16.0 nf=1 ad=4.64  as=4.64  pd=32.58 ps=32.58 nrd=0.0181 nrs=0.0181 sa=0 sb=0 sd=0 mult=1
    XM6 net2 VOUT 0    VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=1.0  nf=1 ad=0.29  as=0.29  pd=2.58  ps=2.58  nrd=0.29   nrs=0.29   sa=0 sb=0 sd=0 mult=1
    .dc VIN 0 1.8 0.005
    .control
    run
    write {RAW} v(VIN) v(VOUT)
    .endc
    .GLOBAL VDD
    .end
""")

with open(TMP,'w') as f:
    f.write(netlist)

print("=== Running ngspice ===")
proc = subprocess.Popen(["ngspice","-b",TMP],
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
out,err = proc.communicate(timeout=60)
for f in [TMP]: 
    if os.path.exists(f): os.remove(f)

print("--- stdout ---")
print(out[:2000])
print("--- stderr (last 10 lines) ---")
for l in err.split('\n')[-10:]:
    if l.strip(): print(l)

print(f"\n=== RAW file exists: {os.path.exists(RAW)} ===")
if os.path.exists(RAW):
    with open(RAW,'r',errors='replace') as f:
        lines = f.readlines()
    print(f"Total lines: {len(lines)}")
    print("--- First 40 lines ---")
    for i,l in enumerate(lines[:40]):
        print(f"{i:3d}: {repr(l)}")
    print("--- Lines around 'Values:' ---")
    for i,l in enumerate(lines):
        if 'alues' in l or 'DATA' in l.upper():
            print(f"{i:3d}: {repr(l)}")
            for j in lines[i:i+8]:
                print(f"     {repr(j)}")
            break
    os.remove(RAW)
else:
    # Maybe ngspice wrote it elsewhere — check cwd
    import glob
    print("Raw files in cwd:", glob.glob("*.raw"))
