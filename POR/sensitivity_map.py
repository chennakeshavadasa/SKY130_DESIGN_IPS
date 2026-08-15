"""
sensitivity_map.py  v5
=======================
Back to mult=10 on XM3/XM4/XM5 (original netlist intent).
DC sweep with ASCII raw for threshold extraction.

From v4 sweep with mult=1 we learned:
  - V_PL barely moves with anything → circuit is fundamentally weak here
  - Need mult=10 to restore original operating point

This version:
  1. Sweeps key params with ORIGINAL mult values
  2. Finds what actually has leverage on V_PL at mult=10
  3. Uses 2D bisection (most robust) rather than Newton
"""

import subprocess, os, json
import numpy as np
from pathlib import Path

LIB       = "/home/nithin/.ciel/sky130A/libs.tech/combined/sky130.lib.spice"
TMP       = "tmp_sens.spice"
VDD       = 1.8
TARGET_PH = 1.60
TARGET_PL = 1.40
TOL       = 0.015
TIMEOUT   = 30

# Original netlist nominal (with original mults)
NOM = {
    'W1': 1.0,   'L1': 2.50,  'M1': 1,
    'W2': 5.0,   'L2': 2.50,  'M2': 1,
    'W3': 6.5,   'L3': 0.15,  'M3': 10,   # XM3 NMOS feedback
    'W4': 16.0,  'L4': 0.15,  'M4': 10,   # XM4=XM5 PMOS
    'W6': 1.0,   'L6': 0.15,  'M6': 1,
}

SIM_COUNT  = 0
FAIL_COUNT = 0


# ─────────────────────────────────────────────────────────────────────────────
# NETLIST WRITER  — respects individual mult per device
# ─────────────────────────────────────────────────────────────────────────────

def ap(w, m=1):
    return w*0.29*m, (w*2+0.58)*m

def write_netlist(p, vin_start, vin_stop, raw_path):
    def nmos(name, d, g, s, b, W, L, M):
        ad,pd = ap(W); nrd = 0.29/W
        return (f"{name} {d} {g} {s} {b} sky130_fd_pr__nfet_01v8 "
                f"L={L:.4f} W={W:.4f} nf=1 "
                f"ad={ad:.4f} as={ad:.4f} pd={pd:.4f} ps={pd:.4f} "
                f"nrd={nrd:.5f} nrs={nrd:.5f} sa=0 sb=0 sd=0 mult={M} m={M}")
    def pmos(name, d, g, s, b, W, L, M):
        ad,pd = ap(W); nrd = 0.29/W
        return (f"{name} {d} {g} {s} {b} sky130_fd_pr__pfet_01v8 "
                f"L={L:.4f} W={W:.4f} nf=1 "
                f"ad={ad:.4f} as={ad:.4f} pd={pd:.4f} ps={pd:.4f} "
                f"nrd={nrd:.5f} nrs={nrd:.5f} sa=0 sb=0 sd=0 mult={M} m={M}")

    step = 0.005 if vin_stop > vin_start else -0.005
    lines = [
        "** Schmitt DC sweep (with original mults)",
        f".lib {LIB} tt",
        ".option wnflag=1",
        ".temp 27",
        f"VVDD VDD 0 {VDD}",
        f"VIN  VIN 0 DC {vin_start}",
        "",
        nmos("XM1","net1","VIN", "0",   "GND", p['W1'],p['L1'],p['M1']),
        nmos("XM2","VOUT","VIN", "net1","GND", p['W2'],p['L2'],p['M2']),
        nmos("XM3","VDD", "VOUT","net1","GND", p['W3'],p['L3'],p['M3']),
        pmos("XM4","VOUT","VIN", "net2","VDD", p['W4'],p['L4'],p['M4']),
        pmos("XM5","net2","VIN", "VDD", "VDD", p['W4'],p['L4'],p['M4']),
        pmos("XM6","net2","VOUT","0",   "VDD", p['W6'],p['L6'],p['M6']),
        "",
        f".dc VIN {vin_start} {vin_stop} {step}",
        ".control",
        "set filetype=ascii",
        "run",
        f"write {raw_path} v(VIN) v(VOUT)",
        ".endc",
        ".GLOBAL VDD",
        ".end",
    ]
    with open(TMP,'w') as f:
        f.write('\n'.join(lines))


# ─────────────────────────────────────────────────────────────────────────────
# RAW PARSER + CROSSING FINDER
# ─────────────────────────────────────────────────────────────────────────────

def parse_raw(raw_path):
    try:
        with open(raw_path,'r',errors='replace') as f:
            content = f.read()
    except FileNotFoundError:
        return None, None
    lines = content.splitlines()
    n_vars,n_pts,var_names,data_start = 0,0,[],0
    i = 0
    while i < len(lines):
        l=lines[i].strip(); ll=l.lower()
        if   ll.startswith('no. variables:'): n_vars=int(l.split(':')[1])
        elif ll.startswith('no. points:'):    n_pts =int(l.split(':')[1])
        elif ll.startswith('variables:'):
            i+=1
            while i<len(lines) and lines[i].startswith('\t'):
                parts=lines[i].strip().split()
                if len(parts)>=2: var_names.append(parts[1].lower())
                i+=1
            continue
        elif ll.startswith('values:'):
            data_start=i+1; break
        i+=1
    if not var_names or n_pts==0 or data_start==0: return None,None
    numbers=[]
    for line in lines[data_start:]:
        for tok in line.split():
            try: numbers.append(float(tok))
            except ValueError: pass
    stride=n_vars+1
    if len(numbers)<stride: return None,None
    n_pts=min(n_pts,len(numbers)//stride)
    data=np.array(numbers[:stride*n_pts]).reshape(n_pts,stride)
    try:
        ci=var_names.index('v(vin)')+1
        co=var_names.index('v(vout)')+1
    except ValueError:
        ci,co=1,2
    return data[:,ci],data[:,co]

def find_crossing(vin,vout,level=0.9,edge='fall'):
    for i in range(len(vout)-1):
        v0,v1=vout[i],vout[i+1]
        if edge=='fall' and v0>=level>v1:
            frac=(level-v0)/(v1-v0+1e-15)
            return float(vin[i]+frac*(vin[i+1]-vin[i]))
        if edge=='rise' and v0<=level<v1:
            frac=(level-v0)/(v1-v0+1e-15)
            return float(vin[i]+frac*(vin[i+1]-vin[i]))
    return None


# ─────────────────────────────────────────────────────────────────────────────
# RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_one(p, vin_start, vin_stop, raw_suffix, label):
    global SIM_COUNT, FAIL_COUNT
    SIM_COUNT += 1
    raw = f"tmp_sens_{raw_suffix}.raw"
    write_netlist(p, vin_start, vin_stop, raw)
    print(f"  sim#{SIM_COUNT:03d}  {label:<32}", end='', flush=True)
    try:
        proc = subprocess.Popen(["ngspice","-b",TMP],
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                text=True)
        _,_ = proc.communicate(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill(); FAIL_COUNT+=1
        print("TIMEOUT"); return None,None
    except Exception as e:
        print(f"ERROR:{e}"); return None,None
    finally:
        if os.path.exists(TMP): os.remove(TMP)
    va,vo=parse_raw(raw)
    if os.path.exists(raw): os.remove(raw)
    return va,vo

def run_sim(p, tag=""):
    """Two DC sweeps → (V_PH, V_PL)."""
    vu,vou=run_one(p,0.0,VDD,"up",  f"{tag} ↑")
    if vu is None: print(); return None,None
    vph=find_crossing(vu,vou,0.9,'fall')

    vd,vod=run_one(p,VDD,0.0,"dn",  f"{tag} ↓")
    if vd is None: print(); return None,None
    vpl=find_crossing(vd,vod,0.9,'rise')

    if vph is None or vpl is None:
        print(f"  no crossing (vph={vph} vpl={vpl})")
        return None,None
    if not (0.05<vpl<vph<VDD-0.05):
        print(f"  unphysical vph={vph:.3f} vpl={vpl:.3f}")
        return None,None

    print(f"  V_PH={vph:.4f}  V_PL={vpl:.4f}  "
          f"(ePH={vph-TARGET_PH:+.4f} ePL={vpl-TARGET_PL:+.4f})")
    return vph,vpl

def converged(vph,vpl):
    return (vph and vpl and
            abs(vph-TARGET_PH)<=TOL and abs(vpl-TARGET_PL)<=TOL)


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1: SWEEP with original mults
# ─────────────────────────────────────────────────────────────────────────────

# What to sweep — only vary W and L, keep M fixed at original
SWEEP = {
    # param: (nom_key, mult_key, values_to_try)
    'W3': ('W3','M3', [0.42, 1.0, 2.0, 4.0, 6.5, 10.0]),
    'L3': ('L3','M3', [0.15, 0.5, 1.0, 2.0, 4.0]),
    'W4': ('W4','M4', [4.0, 8.0, 16.0, 24.0, 32.0, 40.0]),
    'L4': ('L4','M4', [0.15, 0.3, 0.5, 0.8, 1.2, 2.0]),
    'W6': ('W6','M6', [0.42, 1.0, 2.0, 4.0, 6.0]),
    'L6': ('L6','M6', [0.15, 0.3, 0.5, 1.0, 2.0]),
    'W2': ('W2','M2', [1.0, 2.5, 5.0, 8.0, 12.0]),
    'L2': ('L2','M2', [0.15, 0.5, 1.0, 2.5, 5.0]),
    'W1': ('W1','M1', [0.42, 1.0, 2.5, 5.0]),
    'L1': ('L1','M1', [0.15, 0.5, 1.5, 2.5, 5.0]),
}

def run_sweep():
    total = 1 + sum(
        sum(1 for v in vals if abs(v-NOM[wk])>1e-4)
        for wk,_,vals in SWEEP.values())
    print(f"\n  {total} sim-pairs  (~{total*8//60} min)")
    print(f"  mult: XM3=10  XM4=XM5=10  others=1  (original netlist values)\n")

    results = []
    vph0,vpl0 = run_sim(NOM, "nominal")
    if vph0 is None:
        raise RuntimeError("Nominal sim failed")
    print(f"\n  Baseline: V_PH={vph0:.4f}  V_PL={vpl0:.4f}")
    results.append({'params':dict(NOM),'vph':vph0,'vpl':vpl0})

    done = 1
    for param,(wk,_,vals) in SWEEP.items():
        print(f"\n  ── {param} (nom={NOM[wk]:.3f}, mult={NOM[wk[0]+'3'[-1] if param[1]=='3' else param[1:] ]}) ──")
        print(f"  {'Val':>7}  {'V_PH':>8}  {'V_PL':>8}  {'ΔV_PH':>8}  {'ΔV_PL':>8}")
        for val in vals:
            if abs(val-NOM[wk])<1e-4: continue
            done += 1
            p = dict(NOM); p[wk] = float(val)
            tag = f"{param}={val:.2f} [{done}/{total}]"
            vph,vpl = run_sim(p, tag)
            if vph is None: continue
            print(f"  {val:>7.3f}  {vph:>8.4f}  {vpl:>8.4f}  "
                  f"{vph-vph0:>+8.4f}  {vpl-vpl0:>+8.4f}")
            results.append({'params':p,'vph':vph,'vpl':vpl})

    with open("sensitivity_cache.json",'w') as f:
        json.dump(results,f,indent=2)
    print(f"\n  {len(results)} points → sensitivity_cache.json")
    return results, vph0, vpl0


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2: PRINT SENSITIVITY TABLE  (linear dV/dParam at nominal)
# ─────────────────────────────────────────────────────────────────────────────

def print_sensitivity_table(results, vph0, vpl0):
    print("\n" + "="*62)
    print("  SENSITIVITY TABLE  (ΔV per unit param change at nominal)")
    print("="*62)
    print(f"  {'Param':<8} {'nom':>6}  {'dVPH/dX':>10} {'dVPL/dX':>10}  "
          f"{'reach VPH?':>10} {'reach VPL?':>10}")
    print(f"  {'─'*72}")

    wk_map = {wk: (wk, vals) for wk,(_,__,vals) in SWEEP.items()}
    for param,(wk,_,vals) in SWEEP.items():
        pts = [(r['params'][wk], r['vph'], r['vpl'])
               for r in results
               if abs(r['params'][wk]-NOM[wk])>1e-4
               and all(abs(r['params'][k]-NOM[k])<1e-4
                       for k in NOM if k!=wk and k!='M'+wk[1])]
        if len(pts) < 2: continue

        # Finite difference at nominal using nearest points
        pts.sort(key=lambda x:x[0])
        xs  = np.array([p[0] for p in pts])
        yph = np.array([p[1] for p in pts])
        ypl = np.array([p[2] for p in pts])

        # Fit linear slope
        slope_ph = np.polyfit(xs,yph,1)[0]
        slope_pl = np.polyfit(xs,ypl,1)[0]

        # Can we reach target by varying only this param?
        vph_range = f"{min(yph):.3f}–{max(yph):.3f}"
        vpl_range = f"{min(ypl):.3f}–{max(ypl):.3f}"
        reach_ph  = "YES" if min(yph)<=TARGET_PH<=max(yph) else f"NO  [{vph_range}]"
        reach_pl  = "YES" if min(ypl)<=TARGET_PL<=max(ypl) else f"NO  [{vpl_range}]"

        print(f"  {param:<8} {NOM[wk]:>6.3f}  "
              f"{slope_ph:>+10.4f} {slope_pl:>+10.4f}  "
              f"{reach_ph:>10} {reach_pl:>10}")


# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3: 2D BISECTION — most robust, guaranteed convergence
# ─────────────────────────────────────────────────────────────────────────────
# Strategy based on sweep results:
#   Find which single param brackets V_PL (the hard one)
#   Bisect that param to hit V_PL
#   Then bisect a second param to hit V_PH (while keeping V_PL fixed)
#   Joint Newton for final fine-tune

def find_bracketing_param(results, vph0, vpl0, target):
    """Find which param has V_PL ranging across target."""
    print(f"\n  Finding param that brackets target={target:.3f}...")
    for param,(wk,_,vals) in SWEEP.items():
        pts = [(r['params'][wk], r['vpl'])
               for r in results
               if all(abs(r['params'][k]-NOM[k])<1e-4
                      for k in NOM if k!=wk)]
        if len(pts)<2: continue
        vpls = [p[1] for p in pts]
        if min(vpls)<=target<=max(vpls):
            print(f"  → {param} brackets V_PL: [{min(vpls):.4f}, {max(vpls):.4f}]")
            return param, wk
    print("  No single param brackets V_PL target!")
    return None, None

def bisect_1d(p_base, wk, lo, hi, target_fn, target_val, label, n_iter=12):
    """
    Bisect parameter p_base[wk] in [lo,hi] to hit target_fn(vph,vpl)=target_val.
    target_fn: lambda vph,vpl: value_to_compare  (e.g. lambda v,u: u for VPL)
    Returns (best_param_val, best_vph, best_vpl).
    """
    print(f"\n  Bisecting {wk} in [{lo:.3f},{hi:.3f}] for {label}={target_val:.3f}")

    # Check monotonicity
    p=dict(p_base); p[wk]=lo
    vph_lo,vpl_lo=run_sim(p,f"{wk}={lo:.3f}")
    p[wk]=hi
    vph_hi,vpl_hi=run_sim(p,f"{wk}={hi:.3f}")

    if vph_lo is None or vph_hi is None:
        print("  bracket sims failed"); return None,None,None

    val_lo=target_fn(vph_lo,vpl_lo)
    val_hi=target_fn(vph_hi,vpl_hi)
    print(f"  bracket: {label}({wk}={lo:.3f})={val_lo:.4f}  "
          f"{label}({wk}={hi:.3f})={val_hi:.4f}")

    if not (min(val_lo,val_hi)<=target_val<=max(val_lo,val_hi)):
        print(f"  target not bracketed — clamping to nearest")
        if abs(val_lo-target_val)<abs(val_hi-target_val):
            return lo,vph_lo,vpl_lo
        else:
            return hi,vph_hi,vpl_hi

    # Orient: lo=side with lower value
    if val_lo>val_hi:
        lo,hi=hi,lo
        val_lo,val_hi=val_hi,val_lo

    best_w,best_vph,best_vpl=lo,vph_lo,vpl_lo
    for i in range(n_iter):
        mid=(lo+hi)/2.0
        p=dict(p_base); p[wk]=mid
        vph,vpl=run_sim(p,f"bisect {wk}={mid:.4f}")
        if vph is None: break
        val_mid=target_fn(vph,vpl)
        best_w,best_vph,best_vpl=mid,vph,vpl
        if abs(val_mid-target_val)<=TOL:
            print(f"  ✓ bisect converged: {wk}={mid:.4f}  {label}={val_mid:.4f}")
            break
        if val_mid<target_val: lo=mid
        else:                   hi=mid

    return best_w, best_vph, best_vpl


def run_optimizer_2d(results, vph0, vpl0):
    print("\n" + "="*62)
    print("  PHASE 3: 2D Sequential Bisection")
    print("="*62)

    # Step 1: Find what moves V_PL to 1.4V
    # From sweep, look at which params have V_PL ranging across 1.4V
    print("\n  Step 1: Find V_PL lever")
    vpl_levers = []
    for param,(wk,_,vals) in SWEEP.items():
        pts = [(r['params'][wk], r['vph'], r['vpl'])
               for r in results
               if all(abs(r['params'][k]-NOM[k])<1e-4
                      for k in NOM if k!=wk)]
        if len(pts)<2: continue
        vpl_vals = [p[2] for p in pts]
        vph_vals = [p[1] for p in pts]
        vpl_min,vpl_max=min(vpl_vals),max(vpl_vals)
        vph_min,vph_max=min(vph_vals),max(vph_vals)
        brackets_vpl = vpl_min<=TARGET_PL<=vpl_max
        brackets_vph = vph_min<=TARGET_PH<=vph_max
        vpl_levers.append((param, wk, vpl_min, vpl_max,
                           vph_min, vph_max,
                           brackets_vpl, brackets_vph,
                           max(vpl_vals)-min(vpl_vals)))

    print(f"\n  {'Param':<6} {'VPL range':>16}  {'VPH range':>16}  "
          f"{'VPL bracket':>12} {'VPH bracket':>12}")
    print(f"  {'─'*68}")
    for param,wk,plmin,plmax,phmin,phmax,bpl,bph,rng in sorted(
            vpl_levers,key=lambda x:-x[8]):
        print(f"  {param:<6} [{plmin:.3f},{plmax:.3f}]  "
              f"[{phmin:.3f},{phmax:.3f}]  "
              f"{'✓ YES' if bpl else 'NO':>12}  "
              f"{'✓ YES' if bph else 'NO':>12}")

    # Pick best V_PL lever: most range, brackets target
    vpl_lever = next(((p,wk,mn,mx) for p,wk,mn,mx,*_ in
                      sorted(vpl_levers,key=lambda x:-x[8])
                      if x[6]),None) if False else None

    for p,wk,plmin,plmax,phmin,phmax,bpl,bph,rng in sorted(vpl_levers,key=lambda x:-x[8]):
        if bpl:
            vpl_lever=(p,wk,plmin,plmax)
            break

    if vpl_lever is None:
        print("\n  [!] No single param brackets V_PL=1.4V")
        print("      This means the circuit topology may need redesign")
        print("      Showing best-effort result from sweep:")
        best = max(results, key=lambda r: r['vpl'] if r['vpl'] else 0)
        print(f"      Best V_PL achieved: {best['vpl']:.4f}V with params:")
        diffs = {k:best['params'][k] for k in NOM
                 if abs(best['params'].get(k,NOM[k])-NOM[k])>0.01}
        for k,v in diffs.items():
            print(f"        {k}={v:.4f} (nom={NOM[k]:.4f})")
        return dict(NOM), best['vph'], best['vpl']

    param_pl, wk_pl, vpl_min, vpl_max = vpl_lever
    print(f"\n  V_PL lever: {param_pl}  range=[{vpl_min:.4f},{vpl_max:.4f}]")

    # Find bounds from sweep
    pts_sorted = sorted(
        [(r['params'][wk_pl],r['vph'],r['vpl']) for r in results
         if all(abs(r['params'][k]-NOM[k])<1e-4
                for k in NOM if k!=wk_pl)],
        key=lambda x:x[0])
    lo_bound = pts_sorted[0][0]
    hi_bound = pts_sorted[-1][0]

    # Step 2: Bisect V_PL lever
    p_work = dict(NOM)
    best_w, vph_a, vpl_a = bisect_1d(
        p_work, wk_pl, lo_bound, hi_bound,
        lambda ph,pl: pl, TARGET_PL, "V_PL")

    if best_w is None:
        return dict(NOM), vph0, vpl0
    p_work[wk_pl] = best_w

    print(f"\n  After V_PL bisection: V_PH={vph_a:.4f}  V_PL={vpl_a:.4f}")

    if converged(vph_a, vpl_a):
        return p_work, vph_a, vpl_a

    # Step 3: Find V_PH lever (must not disturb V_PL much)
    print(f"\n  Step 3: Find V_PH lever (that minimally affects V_PL)")
    # From levers, pick one that brackets V_PH and has small dVPL/dX
    vph_lever = None
    for par,wk,plmin,plmax,phmin,phmax,bpl,bph,rng in vpl_levers:
        if par==param_pl: continue
        if bph:
            vph_lever=(par,wk,phmin,phmax)
            break

    if vph_lever is None:
        # Use W4 as fallback — always has some V_PH range
        vph_lever=('W4','W4',None,None)
        print("  Using W4 as V_PH trim (fallback)")

    param_ph,wk_ph,_,_ = vph_lever
    pts_ph = sorted(
        [(r['params'][wk_ph],r['vph'],r['vpl']) for r in results
         if all(abs(r['params'][k]-NOM[k])<1e-4
                for k in NOM if k!=wk_ph)],
        key=lambda x:x[0])
    lo_ph = pts_ph[0][0] if pts_ph else 2.0
    hi_ph = pts_ph[-1][0] if pts_ph else 40.0

    best_ph, vph_b, vpl_b = bisect_1d(
        p_work, wk_ph, lo_ph, hi_ph,
        lambda ph,pl: ph, TARGET_PH, "V_PH")

    if best_ph is None:
        return p_work, vph_a, vpl_a
    p_work[wk_ph] = best_ph

    print(f"\n  After V_PH bisection: V_PH={vph_b:.4f}  V_PL={vpl_b:.4f}")
    return p_work, vph_b, vpl_b


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*62)
    print("  SKY130 Schmitt Trigger  v5  |  Original mults restored")
    print(f"  Target: V_PH={TARGET_PH:.3f}V  V_PL={TARGET_PL:.3f}V  ±{TOL*1e3:.0f}mV")
    print(f"  XM3 mult=10  XM4=XM5 mult=10  others mult=1")
    print("="*62)

    cache = Path("sensitivity_cache.json")
    if cache.exists():
        print(f"\n  Loading cache (delete to re-run sweep)...")
        with open(cache) as f: results=json.load(f)
        nom=next((r for r in results
                  if all(abs(r['params'].get(k,0)-NOM[k])<1e-4
                         for k in ['W3','L3','W4','L4'])),None)
        if nom and abs(nom['params'].get('M3',0)-10)<1:
            vph0,vpl0=nom['vph'],nom['vpl']
            print(f"  Nominal (mult=10): V_PH={vph0:.4f}  V_PL={vpl0:.4f}")
        else:
            print("  Cache from mult=1 run — re-sweeping with mult=10")
            cache.unlink()
            results,vph0,vpl0=run_sweep()
    else:
        print("\n" + "="*62)
        print("  PHASE 1: Sensitivity Sweep (mult=10 on XM3/XM4/XM5)")
        print("="*62)
        results,vph0,vpl0=run_sweep()

    print_sensitivity_table(results,vph0,vpl0)

    p_f,vph_f,vpl_f = run_optimizer_2d(results,vph0,vpl0)

    print("\n" + "="*62)
    ok=converged(vph_f,vpl_f)
    print(f"  {'✓ CONVERGED' if ok else '✗ Best effort'}  "
          f"({SIM_COUNT} ngspice calls  {FAIL_COUNT} failed)")
    if vph_f:
        print(f"  V_PH = {vph_f:.4f} V  (err {vph_f-TARGET_PH:+.4f} V)")
        print(f"  V_PL = {vpl_f:.4f} V  (err {vpl_f-TARGET_PL:+.4f} V)")
    print(f"\n  Final sizing:")
    for i in range(0,10,2):
        k='W1 L1 W2 L2 W3 L3 W4 L4 W6 L6'.split()[i:i+2]
        wk,lk=k[0],k[1]
        dev=wk[1]
        m=p_f.get('M'+dev, NOM.get('M'+dev,1))
        chg='*' if (abs(p_f.get(wk,NOM[wk])-NOM[wk])>0.01 or
                    abs(p_f.get(lk,NOM[lk])-NOM[lk])>0.01) else ' '
        print(f"  {chg} XM{dev}: W={p_f.get(wk,NOM[wk]):.4f}µm  "
              f"L={p_f.get(lk,NOM[lk]):.4f}µm  mult={m}")
    print(f"    XM5 = XM4")
    print("="*62+"\n")

if __name__ == "__main__":
    main()
