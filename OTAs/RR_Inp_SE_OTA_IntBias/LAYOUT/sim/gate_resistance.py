#!/usr/bin/env python3
"""Effective resistance from an input pin to every input-pair gate in an RC-extracted netlist.

Builds the resistor network of the net (magic extresist sub-nodes NET.xxx), grounds the pin
node and solves the Laplacian for each gate terminal (unit current injection):
R_eff(gate) = potential at the gate node.  Usage: gate_resistance.py <rcx.spice> [json_out]
"""
import sys
import json
import collections
import numpy as np


def analyse(path, net):
    res = []
    gates = []
    for l in open(path):
        p = l.split()
        if not p:
            continue
        if p[0].startswith("R") and p[1].split(".")[0] == net and p[2].split(".")[0] == net:
            res.append((p[1], p[2], float(p[3])))
        elif p[0].startswith("X") and "_lvt" in l:
            g = p[2]
            if g.split(".")[0] == net:
                gates.append(g)
    nodes = sorted({a for a, b, r in res} | {b for a, b, r in res} | set(gates) | {net})
    idx = {n: i for i, n in enumerate(nodes)}
    G = np.zeros((len(nodes), len(nodes)))
    for a, b, r in res:
        i, j = idx[a], idx[b]
        g = 1.0 / max(r, 1e-6)
        G[i, i] += g
        G[j, j] += g
        G[i, j] -= g
        G[j, i] -= g
    keep = [i for n, i in idx.items() if n != net]          # pin node grounded
    Gr = G[np.ix_(keep, keep)] + np.eye(len(keep)) * 1e-12
    pos = {n: k for k, n in enumerate([nodes[i] for i in keep])}
    Rg = []
    for g in gates:
        if g == net:
            Rg.append(0.0)
            continue
        e = np.zeros(len(keep))
        e[pos[g]] = 1.0
        Rg.append(float(np.linalg.solve(Gr, e)[pos[g]]))
    Rg = np.array(Rg)
    return {"n_gates": len(gates), "n_res": len(res), "R_max": float(Rg.max()), "R_mean": float(Rg.mean()),
            "R_min": float(Rg.min())}


if __name__ == "__main__":
    out = {n: analyse(sys.argv[1], n) for n in ("VINP", "VINN")}
    for n, d in out.items():
        print(f"{n}: {d['n_gates']} lvt gate fingers, {d['n_res']} R; pin->gate R_eff "
              f"min {d['R_min']:.0f} / mean {d['R_mean']:.0f} / max {d['R_max']:.0f} ohm")
    if len(sys.argv) > 2:
        json.dump(out, open(sys.argv[2], "w"), indent=1)
