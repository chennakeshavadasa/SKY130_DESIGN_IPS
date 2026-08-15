"""
plot_transfer.py
================
Runs both DC sweeps and prints the raw V(VOUT) vs V(VIN) table
so we can see exactly where crossings happen and whether
hysteresis exists at all in the current netlist.
"""
import subprocess, os, textwrap
import numpy as np

LIB     = "/home/nithin/.ciel/sky130A/libs.tech/combined/sky130.lib.spice"
TMP     = "tmp_plot.spice"
VDD     = 1.8
TIMEOUT = 40

def write(vs, ve, raw):
    step = 0.01 if ve>vs else -0.01
    txt = textwrap.dedent(f"""\
        ** Transfer curve
        .lib {LIB} tt
        .option wnflag=1
        .temp 27
        VVDD VDD 0 {VDD}
        VIN  VIN 0 DC {vs}
        XM1 net1 VIN  0    GND  sky130_fd_pr__nfet_01v8 L=2.5  W=1.0  nf=1 ad=0.29  as=0.29  pd=2.58  ps=2.58  nrd=0.29   nrs=0.29   sa=0 sb=0 sd=0 mult=1
        XM2 VOUT VIN  net1 GND  sky130_fd_pr__nfet_01v8 L=2.5  W=5.0  nf=1 ad=1.45  as=1.45  pd=10.58 ps=10.58 nrd=0.058  nrs=0.058  sa=0 sb=0 sd=0 mult=1
        XM3 VDD  VOUT net1 GND  sky130_fd_pr__nfet_01v8 L=0.15 W=6.5  nf=1 ad=1.885 as=1.885 pd=13.58 ps=13.58 nrd=0.0446 nrs=0.0446 sa=0 sb=0 sd=0 mult=10 m=10
        XM4 VOUT VIN  net2 VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=16.0 nf=1 ad=4.64  as=4.64  pd=32.58 ps=32.58 nrd=0.0181 nrs=0.0181 sa=0 sb=0 sd=0 mult=10 m=10
        XM5 net2 VIN  VDD  VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=16.0 nf=1 ad=4.64  as=4.64  pd=32.58 ps=32.58 nrd=0.0181 nrs=0.0181 sa=0 sb=0 sd=0 mult=10 m=10
        XM6 net2 VOUT 0    VDD  sky130_fd_pr__pfet_01v8 L=0.15 W=1.0  nf=1 ad=0.29  as=0.29  pd=2.58  ps=2.58  nrd=0.29   nrs=0.29   sa=0 sb=0 sd=0 mult=1
        .dc VIN {vs} {ve} {step}
        .control
        set filetype=ascii
        run
        write {raw} v(VIN) v(VOUT) v(net1) v(net2)
        .endc
        .GLOBAL VDD
        .end
    """)
    with open(TMP,'w') as f: f.write(txt)

def parse(raw):
    try: txt=open(raw,'r',errors='replace').read()
    except: return None
    lines=txt.splitlines(); vars_=[]; ds=0; nv=np_=0; i=0
    while i<len(lines):
        l=lines[i].strip(); ll=l.lower()
        if ll.startswith('no. variables:'): nv=int(l.split(':')[1])
        elif ll.startswith('no. points:'): np_=int(l.split(':')[1])
        elif ll.startswith('variables:'):
            i+=1
            while i<len(lines) and lines[i].startswith('\t'):
                p=lines[i].strip().split()
                if len(p)>=2: vars_.append(p[1].lower())
                i+=1
            continue
        elif ll.startswith('values:'): ds=i+1; break
        i+=1
    if not vars_ or np_==0 or ds==0: return None
    nums=[]
    for line in lines[ds:]:
        for t in line.split():
            try: nums.append(float(t))
            except: pass
    st=nv+1
    if len(nums)<st: return None
    np_=min(np_,len(nums)//st)
    D=np.array(nums[:st*np_]).reshape(np_,st)
    result={}
    for j,name in enumerate(vars_):
        result[name]=D[:,j+1]
    return result

def run_dc(vs, ve, label):
    raw=f"tmp_plot_{label}.raw"
    write(vs,ve,raw)
    print(f"  Running {label} sweep ({vs}V→{ve}V)...",flush=True)
    try:
        proc=subprocess.Popen(["ngspice","-b",TMP],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        proc.communicate(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill(); print("  TIMEOUT"); return None
    finally:
        if os.path.exists(TMP): os.remove(TMP)
    d=parse(raw)
    if os.path.exists(raw): os.remove(raw)
    return d

print("="*60)
print("  Schmitt Trigger Transfer Curve Analysis")
print("="*60)

# UP sweep
du = run_dc(0, VDD, "up")
# DOWN sweep  
dd = run_dc(VDD, 0, "down")

for label, d in [("UP (0→1.8V)", du), ("DOWN (1.8→0V)", dd)]:
    if d is None:
        print(f"\n{label}: FAILED"); continue
    vin  = d.get('v(vin)',  d.get('v(v-sweep)', None))
    vout = d.get('v(vout)', None)
    net1 = d.get('v(net1)', None)
    net2 = d.get('v(net2)', None)
    if vin is None or vout is None:
        print(f"\n{label}: parse failed, keys={list(d.keys())}"); continue

    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    print(f"  {'VIN':>7}  {'VOUT':>7}  {'net1':>7}  {'net2':>7}")
    print(f"  {'─'*35}")

    # Print every 5th point + points near transitions
    prev_vout = vout[0]
    for i in range(len(vin)):
        vi,vo = vin[i],vout[i]
        n1 = net1[i] if net1 is not None else 0
        n2 = net2[i] if net2 is not None else 0
        # print near transitions or every 10th point
        transition = abs(vo-prev_vout)>0.05
        sparse     = (i%5==0)
        if transition or sparse:
            marker = " ←" if transition else ""
            print(f"  {vi:>7.4f}  {vo:>7.4f}  {n1:>7.4f}  {n2:>7.4f}{marker}")
        prev_vout = vo

    # Find crossings
    for level in [0.9]:
        for edge,name in [('fall','V_PH'),('rise','V_PL')]:
            for i in range(len(vout)-1):
                v0,v1=vout[i],vout[i+1]
                if edge=='fall' and v0>=level>v1:
                    frac=(level-v0)/(v1-v0+1e-15)
                    val=vin[i]+frac*(vin[i+1]-vin[i])
                    print(f"\n  >>> {name} = {val:.4f} V  (VOUT crosses {level}V {edge})")
                    break
                if edge=='rise' and v0<=level<v1:
                    frac=(level-v0)/(v1-v0+1e-15)
                    val=vin[i]+frac*(vin[i+1]-vin[i])
                    print(f"\n  >>> {name} = {val:.4f} V  (VOUT crosses {level} V {edge})")
                    break

print("\n" + "="*60)
