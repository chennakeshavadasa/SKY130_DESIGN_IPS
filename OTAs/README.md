# OTA IP Library — SKY130 (SkyWater 130 nm)

Collection of Operational Transconductance Amplifier (OTA) IP blocks designed and verified using open-source tools on the SkyWater 130 nm PDK.

---

## Naming Convention

```
<Input_Stage>_<Output_Stage>_OTA_<Bias>
```

| Token | Meaning |
|-------|---------|
| `NMOS_SrcDeg` | Single NMOS differential pair with source degeneration |
| `RR_Inp` | Complementary NMOS + PMOS input pair — rail-to-rail input |
| `SE` | Single-ended output |
| `IntBias` | Fully self-contained on-chip bias generation |
| `ExtBias` | External bias pins required |

---

## Available IPs

### 1. [`NMOS_FoldedCasc_SE_OTA_IntBias/`](NMOS_FoldedCasc_SE_OTA_IntBias/)

**NMOS Folded-Cascode OTA with Gm-Independent Bias (Internal)**

NMOS differential input pair driving a folded-cascode output stage. The bias network is embedded in the cascode load and keeps Gm independent of process and temperature — no external bias pins required.

| Property | Value |
|----------|-------|
| Input stage | Single NMOS differential pair |
| Bias technique | Gm-independent, embedded in cascode load |
| Output | Single-ended |
| Bias | Internal |
| Schematic tool | Xschem |
| Simulator | ngspice |
| Simulations done | DC, STB, Monte Carlo (V_OS) |

---

### 2. [`RR_Inp_SE_OTA_ExtBias/`](RR_Inp_SE_OTA_ExtBias/)

**Rail-to-Rail Input OTA with External Bias**

Complementary NMOS + PMOS input stage for full rail-to-rail common-mode input range. Single-ended output. Bias current is supplied externally via dedicated bias pins.

| Property | Value |
|----------|-------|
| Input stage | Complementary NMOS + PMOS (LVT) |
| Input CM range | Rail-to-rail (0 → VDD) |
| Output | Single-ended |
| Bias | External |
| VDD | 1.8 V |
| Schematic tool | Xschem |
| Simulator | ngspice |
| Automation | `run_corners.py` |
| Simulations done | DC, PSRR, TRAN, STB, Monte Carlo |

---

### 3. [`RR_Inp_SE_OTA_IntBias/`](RR_Inp_SE_OTA_IntBias/)

**Rail-to-Rail Input/Output OTA with Internal Bias** ← *most complete IP*

Complementary NMOS + PMOS input stage (both LVT) with regulated cascode output for rail-to-rail output swing. Fully integrated bias generation with active-high enable (`EN`) for power-down. No external bias pins required.

| Property | Value |
|----------|-------|
| Input stage | Complementary NMOS + PMOS (LVT) |
| Input CM range | Rail-to-rail (0 → VDD) |
| Output swing | Rail-to-rail |
| Bias | Internal (self-contained) |
| Enable | Active-high `EN` pin |
| VDD | 1.8 V |
| Load cap | 10 pF |
| Schematic tool | Xschem |
| Simulator | ngspice |
| Corners | tt / ss / ff / fs / sf + tt_mm (MC) |
| Automation | `cross_corner_sim_Rail_to_Rail_OTA.py` |
| MC re-plot | `replot_mc_only.py` |
| Simulations done | DC, PSRR, TRAN, STB, Monte Carlo (1000 runs) |
| Plots | Interactive Plotly HTML + IEEE-format PNG/PDF |

---

### 4. [`Rail_to_Rail_IP_OP_SWING_OTA__IP/`](Rail_to_Rail_IP_OP_SWING_OTA__IP/)

**Rail-to-Rail Swing OTA**

Rail-to-rail input OTA variant optimised for output swing. Simulation infrastructure uses an earlier-generation automation script.

| Property | Value |
|----------|-------|
| Input stage | Complementary NMOS + PMOS |
| Output | Single-ended |
| Schematic tool | Xschem |
| Simulator | ngspice |
| Simulations done | DC, PSRR, TRAN, STB, Monte Carlo |

---

### 5. [`Rail_to_Rail_OTA_Inp_IP/`](Rail_to_Rail_OTA_Inp_IP/)

**Rail-to-Rail Input OTA — Design Variants**

Parent folder for additional variants under active development.

```
Rail_to_Rail_OTA_Inp_IP/
├── Single_ended/
│   └── without_internal_bias/    ← SE output, external bias
└── fully_differential/           ← WIP: fully differential topology
```

---

## Tool Requirements

| Tool | Purpose |
|------|---------|
| [Xschem](https://xschem.sourceforge.io/) ≥ 3.4 | Schematic capture |
| [ngspice](https://ngspice.sourceforge.io/) ≥ 40 | SPICE simulation |
| [SKY130 PDK](https://github.com/google/skywater-pdk) via ciel | Device models |
| Python ≥ 3.10 + `plotly matplotlib numpy pandas` | Automation & plots |

---

## Quick Comparison

| IP | Input CM | Output Type | Output Swing | Bias | EN Pin | Automation |
|----|----------|------------|--------------|------|--------|------------|
| `NMOS_FoldedCasc_SE_OTA_IntBias` | Limited (NMOS only) | Single-ended | VDD−Vov to Vov | Internal | — | Manual |
| `RR_Inp_SE_OTA_ExtBias` | Rail-to-rail | Single-ended | VDD−Vov to Vov | External | — | `run_corners.py` |
| `RR_Inp_SE_OTA_IntBias` | Rail-to-rail | Single-ended | ~0 → ~VDD | Internal | ✓ | Full automation |
| `Rail_to_Rail_IP_OP_SWING_OTA__IP` | Rail-to-rail | Single-ended | ~0 → ~VDD | — | — | Partial |
| `Rail_to_Rail_OTA_Inp_IP/` | Rail-to-rail | SE / Diff (WIP) | VDD−Vov to Vov | External / WIP | — | `run_corners.py` |

---

*Maintained by [Nithin P (chennakeshavadasa)](https://github.com/chennakeshavadasa) · Last updated: **August 2026***
