"""
optimize_schmitt.py — v10  FINAL PUSH
======================================
Status from v9:
  Best single-param state: V_PH=1.7385  V_PL=1.3881  (M4=15, all levers max)
  Gap: V_PH needs -139mV, V_PL needs +12mV

  The only way to bring V_PH down is L4↑ or W4↓ — but both hurt V_PL.
  We need to find the [L4, M4] combination where:
    V_PH lands at 1.60V  AND  V_PL stays ≥ 1.385V

  Strategy: 2D grid search on [L4, M4], then bisect the winner.
  Starting point: all-levers-max state from v9.
"""

import subprocess, os
import numpy as np

LIB     = "/home/nithin/.ciel/sky130A/libs.tech/combined/sky130.lib.spice"
TMP     = "tmp_v10.spice"
VDD     = 1.8
TPH     = 1.60
TPL     = 1.40
TOL     = 0.015
TIMEOUT = 35
SIM_N   = 0

# Best state from v9 (all positive levers maxed)
BEST = dict(W1=0.42,  L1=8.0,   M1=1,
            W2=0.42,  L2=8.0,   M2=1,
            W3=6.5,   L3=0.15,  M3=10,
            W4=16.0,  L4=0.15,  M4=10,
            W6=1.0,   L6=10.0,  M6=1)


# ─────────────────────────────────────────────────────────────────────────────
# NETLIST / SIM (proven flat format)
# ─────────────────────────────────────────────────────────────────────────────

def write(p, vs, ve, raw):
    def n(nm,d,g,s,b,W,L,M):
        ad,pd=W*0.29,W*2+0.58; nrd=0.29/W
        return (f"{nm} {d} {g} {s} {b} sky130_fd_pr__nfet_01v8 "
                f"L={L:.4f} W={W:.4f} nf=1 ad={ad:.4f} as={ad:.4f} "
                f"pd={pd:.4f} ps={pd:.4f} nrd={nrd:.5f} nrs={nrd:.5f} "
                f"sa=0 sb=0 sd=0 mult={M} m={M}")
    def pf(nm,d,g,s,b,W,L,M):
        ad,pd=W*0.29,W*2+0.58; nrd=0.29/W
        return (f"{nm} {d} {g} {s} {b} sky130_fd_pr__pfet_01v8 "
                f"L={L:.4f} W={W:.4f} nf=1 ad={ad:.4f} as={ad:.4f} "
                f"pd={pd:.4f} ps={pd:.4f} nrd={nrd:.5f} nrs={nrd:.5f} "
                f"sa=0 sb=0 sd=0 mult={M} m={M}")
    step = 0.003 if ve>vs else -0.003
    txt = "\n".join([
        "** v10", f".lib {LIB} tt", ".option wnflag=1", ".temp 27",
        f"VVDD VDD 0 {VDD}", f"VIN VIN 0 DC {vs}", "",
        n( "XM1","net1","VIN", "0",   "GND",p['W1'],p['L1'],p['M1']),
        n( "XM2","VOUT","VIN", "net1","GND",p['W2'],p['L2'],p['M2']),
        n( "XM3","VDD", "VOUT","net1","GND",p['W3'],p['L3'],p['M3']),
        pf("XM4","VOUT","VIN", "net2","VDD",p['W4'],p['L4'],p['M4']),
        pf("XM5","net2","VIN", "VDD", "VDD",p['W4'],p['L4'],p['M4']),
        pf("XM6","net2","VOUT","0",   "VDD",p['W6'],p['L6'],p['M6']),
        "", f".dc VIN {vs} {ve} {step}",
        ".control", "set filetype=ascii", "run",
        f"write {raw} v(VIN) v(VOUT)", ".endc",
        ".GLOBAL VDD", ".end"])
    with open(TMP,'w') as f: f.write(txt)

def parse(raw):
    try: txt=open(raw,'r',errors='replace').read()
    except: return None,None
    lines=txt.splitlines(); vars_=[]; ds=nv=np_=0; i=0
    while i<len(lines):
        l=lines[i].strip(); ll=l.lower()
        if ll.startswith('no. variables:'): nv=int(l.split(':')[1])
        elif ll.startswith('no. points:'): np_=int(l.split(':')[1])
        elif ll.startswith('variables:'):
            i+=1
            while i<len(lines) and lines[i].startswith('\t'):
                pt=lines[i].strip().split()
                if len(pt)>=2: vars_.append(pt[1].lower())
                i+=1
            continue
        elif ll.startswith('values:'): ds=i+1; break
        i+=1
    if not vars_ or np_==0 or ds==0: return None,None
    nums=[]
    for line in lines[ds:]:
        for t in line.split():
            try: nums.append(float(t))
            except: pass
    st=nv+1
    if len(nums)<st: return None,None
    np_=min(np_,len(nums)//st)
    D=np.array(nums[:st*np_]).reshape(np_,st)
    try: ci=vars_.index('v(vin)')+1; co=vars_.index('v(vout)')+1
    except: ci,co=1,2
    return D[:,ci],D[:,co]

def xcross(vin,vout,lv=0.9,edge='fall'):
    for i in range(len(vout)-1):
        v0,v1=vout[i],vout[i+1]
        if edge=='fall' and v0>=lv>v1:
            return float(vin[i]+(lv-v0)/(v1-v0+1e-15)*(vin[i+1]-vin[i]))
        if edge=='rise' and v0<=lv<v1:
            return float(vin[i]+(lv-v0)/(v1-v0+1e-15)*(vin[i+1]-vin[i]))
    return None

def sim(p, tag=""):
    global SIM_N; vph=vpl=None
    for vs,ve,suf,ed in [(0,VDD,'u','fall'),(VDD,0,'d','rise')]:
        SIM_N+=1; raw=f"tmp_v10_{suf}.raw"
        write(p,vs,ve,raw)
        print(f"  #{SIM_N:03d} {tag:<34}{'↑' if suf=='u' else '↓'} ",
              end='',flush=True)
        try:
            proc=subprocess.Popen(["ngspice","-b",TMP],
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            proc.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill(); print("TIMEOUT")
            for f in [TMP,raw]:
                if os.path.exists(f): os.remove(f)
            return None,None
        finally:
            if os.path.exists(TMP): os.remove(TMP)
        va,vo=parse(raw)
        if os.path.exists(raw): os.remove(raw)
        if va is None: print("parse fail"); return None,None
        v=xcross(va,vo,0.9,ed)
        if ed=='fall': vph=v; print(f"V_PH={vph:.4f}" if vph else "NO_CROSS",end='   ')
        else:          vpl=v; print(f"V_PL={vpl:.4f}" if vpl else "NO_CROSS")
    if vph and vpl and 0.05<vpl<vph<VDD-0.05:
        print(f"       ePH={vph-TPH:+.4f}  ePL={vpl-TPL:+.4f}")
        return vph,vpl
    return None,None

def ok(vph,vpl):
    return vph and vpl and abs(vph-TPH)<=TOL and abs(vpl-TPL)<=TOL

def bisect(p_base, key, lo, hi, fn, target, label, n=14):
    print(f"\n  Bisect {key} [{lo:.4f}→{hi:.4f}] for {label}={target:.3f}")
    pb=dict(p_base); pb[key]=lo; r0=sim(pb,f"{key}={lo:.4f}")
    pb[key]=hi;              r1=sim(pb,f"{key}={hi:.4f}")
    if r0[0] is None or r1[0] is None:
        print("  bracket failed"); return None,None,None
    f0,f1=fn(*r0),fn(*r1)
    print(f"  [{label}={f0:.4f}@{lo:.4f}  {label}={f1:.4f}@{hi:.4f}]")
    if not (min(f0,f1)<=target<=max(f0,f1)):
        print(f"  not bracketed — best end")
        return (lo,*r0) if abs(f0-target)<abs(f1-target) else (hi,*r1)
    if f0>f1: lo,hi=hi,lo
    bw,br=lo,r0
    for _ in range(n):
        mid=(lo+hi)/2
        pb=dict(p_base); pb[key]=mid
        r=sim(pb,f"{key}={mid:.5f}")
        if r[0] is None: break
        fm=fn(*r); bw,br=mid,r
        if abs(fm-target)<=TOL:
            print(f"  ✓ {key}={mid:.5f}  {label}={fm:.4f}"); break
        if fm<target: lo=mid
        else:         hi=mid
    return bw,br[0],br[1]


# ─────────────────────────────────────────────────────────────────────────────
# 2D GRID SEARCH on [L4, M4]
# ─────────────────────────────────────────────────────────────────────────────

def grid_search_2d(p_base):
    """
    Search [L4 × M4] space.
    We want: V_PH ≈ 1.60  AND  V_PL ≥ 1.385
    L4 controls V_PH (L4↑ → V_PH↓, V_PL↓)
    M4 controls both (M4↑ → V_PH↑, V_PL↑)
    """
    print("\n" + "="*62)
    print("  2D GRID: L4 × M4  (find [V_PH≈1.60, V_PL≥1.385])")
    print("="*62)

    L4_vals = [0.15, 0.18, 0.21, 0.25, 0.30, 0.36, 0.42]
    M4_vals = [10,   12,   15,   18,   20,   25,   30  ]

    print(f"\n  {'L4':>6}  {'M4':>4}  {'V_PH':>8}  {'V_PL':>8}  "
          f"{'ePH':>8}  {'ePL':>8}  {'score':>8}")
    print(f"  {'─'*65}")

    best_score = 1e9
    best_p = None
    best_vph = best_vpl = None

    results = []
    for m4 in M4_vals:
        for l4 in L4_vals:
            pb = dict(p_base)
            pb['L4'] = l4
            pb['M4'] = m4
            vph,vpl = sim(pb, f"L4={l4:.3f} M4={m4}")
            if vph is None: continue

            eph = vph - TPH
            epl = vpl - TPL
            # Score: weighted sum of squared errors
            # Penalize V_PH error more if V_PL is close (we know V_PL is harder)
            score = eph**2 + 4*epl**2
            flag = " ← BEST" if score < best_score else ""

            print(f"  {l4:>6.3f}  {m4:>4d}  {vph:>8.4f}  {vpl:>8.4f}  "
                  f"{eph:>+8.4f}  {epl:>+8.4f}  {score:>8.5f}{flag}")

            results.append((l4,m4,vph,vpl,score))
            if score < best_score:
                best_score = score
                best_p = dict(pb)
                best_vph,best_vpl = vph,vpl

            # Early exit if converged
            if ok(vph,vpl):
                print(f"\n  ✓ CONVERGED during grid search!")
                return best_p, vph, vpl

    return best_p, best_vph, best_vpl


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*62)
    print("  SKY130 Schmitt Trigger  v10  |  2D [L4×M4] Grid + Bisect")
    print(f"  Target: V_PH={TPH}V  V_PL={TPL}V  ±{TOL*1e3:.0f}mV")
    print("="*62)
    print(f"""
  Starting from v9 best state (all positive levers maxed):
    W1=0.42µm L1=8.0µm  W2=0.42µm L2=8.0µm
    W4=16µm   L4=0.15µm M4=10     W6=1µm L6=10µm
    V_PH=1.72V  V_PL=1.36V

  Gap: V_PH needs -120mV, V_PL needs +40mV
  Only L4↑ can bring V_PH down, but it also reduces V_PL.
  M4↑ raises both. Need to find the [L4,M4] sweet spot.
  """)

    p = dict(BEST)

    # Step 1: 2D grid search on [L4, M4]
    best_p, vph_grid, vpl_grid = grid_search_2d(p)

    print(f"\n  Grid best: V_PH={vph_grid:.4f}  V_PL={vpl_grid:.4f}")
    print(f"  L4={best_p['L4']:.4f}  M4={best_p['M4']}")

    if ok(vph_grid, vpl_grid):
        print("  ✓ Already converged from grid!")
        p = best_p
        vph_f, vpl_f = vph_grid, vpl_grid
    else:
        p = best_p
        vph_f, vpl_f = vph_grid, vpl_grid

        # Step 2: Bisect L4 to nail V_PH exactly (M4 fixed at grid best)
        print(f"\n── Bisect L4 to hit V_PH=1.60 (M4={p['M4']} fixed) ─────────")
        # Find bracketing range around grid best L4
        l4_lo = max(0.15, p['L4'] - 0.15)
        l4_hi = min(1.0,  p['L4'] + 0.15)
        bw,vph_f,vpl_f = bisect(p,'L4', l4_lo, l4_hi,
                                 lambda ph,pl: ph, TPH, "V_PH")
        if bw:
            p['L4'] = bw
            print(f"\n  After L4 bisect: V_PH={vph_f:.4f}  V_PL={vpl_f:.4f}")

        # Step 3: If V_PL still short, try nudging M4 up one step
        if vpl_f and vpl_f < TPL - TOL:
            print(f"\n── Fine-tune: nudge M4 up if V_PL still short ───────────────")
            for m4_try in range(p['M4']+1, p['M4']+8):
                pb = dict(p); pb['M4'] = m4_try
                vph_t,vpl_t = sim(pb, f"M4={m4_try} check")
                if vph_t is None: continue
                print(f"  M4={m4_try}: V_PH={vph_t:.4f}  V_PL={vpl_t:.4f}  "
                      f"ePH={vph_t-TPH:+.4f}  ePL={vpl_t-TPL:+.4f}")
                if vpl_t >= TPL - TOL:
                    # Re-bisect L4 to fix V_PH
                    p['M4'] = m4_try
                    bw2,vph_f,vpl_f = bisect(p,'L4',
                                              max(0.15,p['L4']-0.1),
                                              min(1.0, p['L4']+0.1),
                                              lambda ph,pl:ph, TPH, "V_PH")
                    if bw2: p['L4']=bw2
                    break
                if ok(vph_t,vpl_t):
                    p['M4']=m4_try; vph_f,vpl_f=vph_t,vpl_t; break

    # Final
    print("\n" + "="*62)
    print(f"  {'✓ CONVERGED' if ok(vph_f,vpl_f) else '✗ Best effort'}  "
          f"({SIM_N} ngspice calls)")
    if vph_f:
        print(f"  V_PH = {vph_f:.4f} V  (err {vph_f-TPH:+.4f} V)")
        print(f"  V_PL = {vpl_f:.4f} V  (err {vpl_f-TPL:+.4f} V)")

    BASE = dict(W1=1.0,L1=2.5,M1=1,W2=5.0,L2=2.5,M2=1,
                W3=6.5,L3=0.15,M3=10,W4=16.,L4=0.15,M4=10,W6=1.0,L6=0.15,M6=1)
    print(f"\n  Optimized sizing (changes from original netlist marked *):")
    for dev,wk,lk,mk in [('1','W1','L1','M1'),('2','W2','L2','M2'),
                          ('3','W3','L3','M3'),('4','W4','L4','M4'),
                          ('6','W6','L6','M6')]:
        chg='*' if (abs(p.get(wk,BASE[wk])-BASE[wk])>0.01 or
                    abs(p.get(lk,BASE[lk])-BASE[lk])>0.01 or
                    p.get(mk,BASE[mk])!=BASE[mk]) else ' '
        print(f"  {chg} XM{dev}: W={p.get(wk,BASE[wk]):.4f}µm  "
              f"L={p.get(lk,BASE[lk]):.4f}µm  mult={p.get(mk,BASE[mk])}"
              f"  (was W={BASE[wk]} L={BASE[lk]} m={BASE[mk]})")
    print(f"    XM5 = XM4")
    print("="*62+"\n")

if __name__=="__main__":
    main()
