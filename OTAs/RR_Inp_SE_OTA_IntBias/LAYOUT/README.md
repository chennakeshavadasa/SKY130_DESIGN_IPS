# Layout: Rail-to-Rail Input SE OTA with Internal Bias (SKY130A)

Full custom layout, physical verification and post-layout verification of this IP
(`OTAs/RR_Inp_SE_OTA_IntBias`).

**The schematic was not modified.** LVS runs against the xschem netlist of
[`../SCH/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sch`](../SCH/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sch),
and the pre-layout simulations use that same schematic.

**Jump to:** [schematic vs layout comparison](#verification--schematic-vs-layout-comparison-auto-generated) ·
[standalone report](docs/POST_LAYOUT_VERIFICATION.md) · [GDS](gds/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.gds) ·
[RC netlist](pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice)

| | |
|---|---|
| Top cell | `Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias` (same name as the schematic subcircuit) |
| Size | **87.07 µm × 47.20 µm = 4109 µm²** |
| Devices | 80 schematic instances (64 after netgen parallel merging), drawn as 225 fingers/segments |
| Active area | 1563 µm² gate + 171 µm² resistor body (≈ 42 % of the cell box) |
| Layers used | diff/tap, poly, li1, met1 (device straps, rails), met2 (horizontal tracks), met3 (vertical buses). **met4/met5 free** |
| Pins | VDD, EN, VINN, VOUT, VINP, MN_TAIL_BIAS, GNDA (same order as the symbol) |
| Signoff | magic DRC 0 · KLayout sky130 DRC 0 · antenna clean · LVS *Circuits match uniquely* |
| Power-down current | 16.6 pA (tt, 27 °C, PEX); 10–30 pA all corners; 2.4 nA at 125 °C |

---

## 1. Circuit recap

A folded-cascode OTA with **complementary input pairs** for rail-to-rail common-mode range,
plus an on-chip bias generator:

* **Input stage:** PMOS pair MP_A1/MP_A2 (pfet_01v8_lvt, 28 × W4/L2 each) with tail MP_PDIFF_BIAS,
  and NMOS pair MN_A1/MN_A2 (nfet_01v8_lvt, 8 × W2.5/L2 each) with tail MN_NDIFF_BIAS.
* **Folded cascode output:** PMOS loads MP_TOP_L1/L2 → PMOS cascodes MP_CASC_L1/L2 → VOUT ←
  NMOS cascodes MN_CASC_L1/L2 ← NMOS loads MN_BOT_L1/L2. net5 (the L1 cascode output) drives
  the MP_TOP gates (self-biased load).
* **Cascode bias:** VBP_CASC from a 3-high PMOS diode stack, VBN_CASC from an 8-high NMOS diode
  stack, both fed from the net8/net9 mirrors.
* **Internal reference:** beta multiplier XM1 (16 × W10/L4) / XM10 (4 × W10/L4) with the
  R14–R22 xhigh-po resistor chain, PMOS mirror M3/M4 (VBP_TOP), and copies M9 (→ net8) and M2.
* **Start-up and enable:** M2 + a 10 × L10 µm NMOS stack sense the bias (VSTRP_IP). An inverter
  and a ratioed NAND (VSTRP_OUT) drive injector M12, fed from VDD through R24–R34. EN/EN_B gate
  power-down switches MP_SW1–3, MN_SW1/2, M15, M16.

## 2. Floorplan

![annotated floorplan](docs/layout_annotated.png)

_Annotated floorplan (`scripts/annotate_layout.py`): each block of the final GDS outlined and
numbered, with the pins marked. The plain render is below._

![layout](docs/layout_full.png)

```
 x: 0.4 .......................... 41.6 | 41.6 .......................................... 87.5
 ┌────────────── nwell A (VDD ntap rail on top) ─────────────────────────────────────────────┐
 │ T1  MP_TOP_L1/L2  ABBA×3 (CC)           │ T1  net9 mirror [P4][D C][P4] + MP_SW1           │
 │ T2  MP_CASC_L1/L2 [A4][B4][B4][A4]      │ T2  MP_SW3, M9, M15, [M3 M4], M2×7, M12, logic P   │
 │     + VBP_CASC stack, MP_SW2            │                                                  │
 ├─────────────────────────────────────────┤  logic N, MN_SW1/MN_SW2, XM16  (GNDA ptap rail)  │
 │ NMOS pair MN_A1/A2 2×8, 2-D CC, p-ring  │  18 × xhigh_po_1p41 (R14–22, R24–34) + L=10 stack │
 ├─────────────────────────────────────────┤──────────────────────────────────────────────────┤
 │ PMOS pair MP_A1/A2 4×14, 2-D CC, n-ring │  XM1 / XM10 (W10 L4) 2 rows                       │
 │ MN_CASC_L1/L2 + VBN_CASC stack          │  [M1×4][M10×2][M1×4]  2-D CC, p-ring              │
 │ NMOS mirror rows (net8) 2-D CC          │                                                  │
 └──────────────────────── GNDA ptap rail ───────────────────────────────────────────────────┘
```

Why it is arranged this way:

* **Two columns.** The OTA core is on the left, built around one vertical symmetry axis
  (x = 20 µm). The bias generator is on the right. XM1/XM10 alone hold 800 µm² of gate, so the
  bias column is sized by that block, and the core column is stacked to the same height.
* **Signal flow follows the fold.** The NMOS input pair sits directly below the PMOS loads and
  cascodes it folds into (net3/net4). The PMOS input pair sits directly above the NMOS cascodes
  and mirror it folds into (net1/net2). Both fold paths are therefore short, and both input pairs
  are adjacent, so VINP/VINN routing is short and symmetric.
* **Wells.** nwell A (top, both columns) holds all PMOS except the input pair. The PMOS pair has
  its own nwell (body = VDD, as in the schematic) inside an n-tap guard ring. The top and bottom strips of both input-pair guard rings are li-only taps (no DC current), which frees met1 for the outer gate-strap shunts. The NMOS pair has a
  p-tap guard ring. Every NMOS row has a p-tap rail; the PMOS rows have n-tap rails top and bottom.
* **Long-L devices drawn vertically.** The 10 × W0.5/L10 start-up stack uses one shared poly
  sheet (gate = VDD) with 10 vertical diffusion strips, chained in a serpentine on li. That gives
  8.5 × 11 µm instead of a 100 µm-long row.
* **Resistors.** All 18 xhigh_po_1p41 are in one row at 1.89 µm pitch, serpentine-connected on
  met1. Body length is drawn so that magic extracts L = 6.4 µm / 7.05 µm exactly.

## 3. Matching

![input pairs](docs/layout_inputpairs.png)

| Group | Arrangement | Why |
|---|---|---|
| **MP_A1 / MP_A2** (pfet_lvt 28+28 × W4/L2) | 4 rows × 14 fingers; rows **X, X̄, X̄, X** with X = `ABBAABBAABBAAB`; gate straps shunted with met1 | Finger-level interdigitation. X/X̄ pairing gives a common centroid in x, and the X X̄ X̄ X stacking gives a common centroid in y and also cancels the xy-gradient term. Rows 1/4 end in A and rows 2/3 end in B, so both devices get the same number of edge fingers. A↔B share the source (net7) and A↔A / B↔B share drains, so the diffusion is continuous. |
| **MN_A1 / MN_A2** (nfet_lvt 8+8 × W2.5/L2) | 2 rows `ABBAABBA` / `BAABBAAB` | 2-D common centroid, shared tail (net6), p-tap guard ring |
| **MP_TOP_L1 / L2** (6+6 × W2/L2) | `ABBA ABBA ABBA` in one row | Exact 1-D common centroid with continuous diffusion (shared VDD sources) |
| **MN_BOT_L1 / L2** (6+6 × W0.5/L2) + **MN_NDIFF_BIAS** (8) | 2 rows `ABBAAB` / `BAABBA`, NDIFF_BIAS split 2+2 on both ends of each row | 2-D common centroid for the load pair. The tail-current copy is symmetric around it. All 23 fingers share one net8 gate strap with the diode MN_BIAS_EXT |
| **MP_CASC_L1 / L2** (8+8) | `[A4][B4][B4][A4]` | Common centroid at segment level |
| **MN_CASC_L1 / L2** (3+3) | `[A1][B2][A2][B1]` | The closest 1-D arrangement possible for 3+3 (residual 0.33 finger pitch). Cascode mismatch is second-order |
| **net9 mirror** (MP_PDIFF_BIAS 8, MP_PDIFF_BIAS_B 1, MP_CASC_B_SOURCE 1) | `[P4][D C][P4]` | Diode reference in the centre, output fingers symmetric around it |
| **VBP_TOP mirror** (M3 diode, M4, M9, M2) | M3/M4 adjacent with shared source, same row and orientation as M9/M2 | Beta-multiplier PMOS mirror (M3:M4 = 1:1) is tightly matched |
| **XM1 / XM10** (16+4 × W10/L4) | 2 identical rows `[M1×4][M10×2][M1×4]`, one merged gate strap | 2-D common centroid for the 4:1 ratio that sets the bias current |

General rules applied:

* Every finger keeps the schematic W and L. Netgen merges parallel fingers (W adds, L must
  match), so the merged devices are exactly the schematic sizes.
* All gate connections use li straps outside the active area. S/D use met1 stripes over the
  contacts. Matched devices get identical strap and stripe topology.
* **Dummies.** Dummy transistors cannot be used without editing the schematic: netgen counts them
  as extra devices, which I checked. Edge effects are instead balanced by the patterns above,
  and all matched devices sit inside guard rings away from well edges.

## 4. Routing and power strategy

* **li1:** gate straps and short local jumpers only (no DC current). The input-pair gate straps and the VINP/VINN bars are **shunted with met1**, with an mcon at every gate (see the before/after comparison in §5.1 of the results). That cut the mean pin-to-gate resistance from ≈ 1.1–1.4 kΩ to the values reported there.
* **met1:** S/D stripes over contacts, VDD/GNDA tap rails, start-up/logic verticals.
* **met2:** horizontal "tracks". Every row has one track per S/D net, via1 to the stripes of that
  net. Track pitch is 0.6 µm, because magic treats long met1/met2 as "wide" metal needing 0.28 µm
  spacing.
* **met3:** vertical inter-row buses (0.4 µm, 0.8 µm pitch). Left margin: VINP, net5, net1,
  net3. Right margin: VINN, net2, VOUT, net7. Over the core: net4, VBN_CASC, net9, VBP_CASC,
  net8, net6. Bias column: net12, VBP_TOP, MN_TAIL_BIAS, VDD (R24), net15, VSTRP_IP.
* **Power:** VDD n-tap rails at the top and bottom of nwell A, plus the PMOS-pair n-ring, tied by
  met1 straps on both sides. GNDA p-tap rails at the bottom and between the mirror rows, the
  XM1 ring, the logic/switch rail and the NMOS-pair ring are all tied by met1.
* **Labels:** internal nets carry the schematic names (net1…net15, VBP_CASC, VBN_CASC, VBP_TOP,
  VSTRP_IP, VSTRP_OUT, EN_B), so the extracted netlists are directly readable.

## 5. Pins

| Pin | Layer | Location |
|---|---|---|
| VDD | met1 | top ntap rail (full width) |
| GNDA | met1 | bottom ptap rail (full width) |
| VINP | met3 | left edge bus (x = 0.6 µm) |
| VINN | met3 | bus at x = 38.3 µm, brought to the top edge |
| VOUT | met3 | bus at x = 39.9 µm, brought to the bottom edge |
| MN_TAIL_BIAS | met3 | bus at x = 58.0 µm, brought to the bottom edge |
| EN | met2 | right edge, y = 43.7 µm |

## 6. How verification was done

| Step | Tool | Setup |
|---|---|---|
| DRC | magic 8.3 | `drc(full)` style of the sky130A tech file |
| DRC (independent) | KLayout 0.30 | official `sky130A_mr.drc`, FEOL + BEOL + off-grid |
| Antenna | magic | `extract do antenna; antennacheck` |
| LVS | netgen 1.5 | `sky130A_setup.tcl`; layout = magic `ext2spice lvs`; reference = xschem netlist of the original schematic |
| PEX | magic | full RC: `extract do resistance`, coupling caps, `extresist all`, `cthresh 0`, `rthresh 0` |
| Simulation | ngspice 46 | identical decks for schematic and extracted layout (§ below) |

**LVS reference note:** the schematic connects NMOS bodies to the global `GND` node. In silicon
the p-substrate is the `GNDA` net (every p-tap goes to GNDA), so `lvs/run_lvs.sh` maps body
`GND` → `GNDA` in the reference copy. The schematic file itself is untouched.

**Pre- vs post-layout DUTs**

* *Schematic:* `sim/dut_sch.spice`, the xschem simulation netlist of the untouched `.sch`. Device
  lines are identical to the repo's `different_spice/…spice`, including `mult=` (needed by the
  sky130 mismatch model) and xschem's AD/AS.
* *Layout:* `pex/<cell>_rcx.spice`, the magic RC extraction of the final layout.

**Testbenches** (same as the IP's original ones: VDD = EN = 1.8 V, CL = 10 pF, 1 pF on
MN_TAIL_BIAS, 27 °C, corners tt/ss/ff/fs/sf):

| TB | What | Metrics |
|---|---|---|
| STB | unity-gain loop broken by a Middlebrook probe (V-probe and I-probe AC runs), VICM = 0.9 V | DC loop gain, UGF, phase margin |
| DC | unity gain, VICM 0 → 1.8 V | offset at 0.9 V, worst offset 0.2–1.6 V |
| PSRR | 1 V AC on VDD | Vout/VDD at 10 Hz and 1 MHz |
| TRAN | 1 kHz, 0.25–1.55 V sine, unity gain | peak dynamic offset |
| OP | VICM = 0.9 V | IDD, V(MN_TAIL_BIAS) |
| Start-up | VDD, EN, VICM ramp 0 → final in 10 µs, Gear integration | settling, final IDD and bias, internal start-up nodes |
| Power-down | enabled → EN low, 2 ms (Gear); 5 corners at 27 °C + tt at −40/85/125 °C; EN 0→1→0 transient | power-down IDD, disabled node states, wake-up and shut-down times |
| MC | `tt_mm` mismatch, 200 independent ngspice processes (seed 1…200), VICM = 0.9 V | offset mean and σ |

**Netlist views compared**

| View | Netlist | What it isolates |
|---|---|---|
| SCH (schematic) | `sim/dut_sch.spice` | the designer's schematic |
| Layout, devices only | `mag/<cell>.lvs.spice` | real finger geometry (AD/AS/PD/PS), no wiring parasitics |
| **PEX C-only** | `pex/<cell>_cx.spice` | + wiring capacitance (substrate + coupling): magic's standard extraction, the **best estimate** |
| PEX RC, R shorted | `pex/<cell>_rcx_R0.spice` | the extra substrate capacitance that `extresist` writes on the resistor sub-nodes |
| **PEX full RC** | `pex/<cell>_rcx.spice` | + wire/contact resistance: the **conservative** post-layout view, used for MC, start-up and power-down |

**Where the plots are**

| Plot set | Folder | Content |
|---|---|---|
| Schematic vs PEX | [`sim/plots/`](sim/plots/) `sch_vs_pex_*.png` | SCH (dotted) and PEX full RC (solid, conservative) overlaid, 5 corners: loop gain, DC offset, PSRR, TRAN, MC, start-up |
| PEX only | [`sim/plots/pex/`](sim/plots/pex/) `pex_*.png` | post-layout results alone, 5 corners, same set of analyses as the IP's `IEEE_plots` |
| Layout vs PEX (five views) | [`sim/plots/views/`](sim/plots/views/) `views_*.png` | schematic → layout devices → PEX C-only → PEX RC (R shorted) → PEX full RC, showing where each delta comes from |
| Power-down / enable | [`sim/plots/powerdown/`](sim/plots/powerdown/) | power-down current vs corner and temperature, EN on/off transient, wake-up zoom (SCH vs PEX) |

<!-- BEGIN:AUTO-VERIFICATION -->
## Verification & schematic-vs-layout comparison (auto-generated)

### 1. Signoff summary

| Check | Tool / setup | Result |
|---|---|---|
| DRC | magic 8.3, `drc(full)`, sky130A tech | **0 errors** |
| DRC (2nd opinion) | KLayout `sky130A_mr.drc`, FEOL+BEOL+off-grid (256 rule categories) | **0 violations** |
| Antenna | magic `antennacheck` | **0 violations** |
| LVS | netgen 1.5 + `sky130A_setup.tcl`, layout vs xschem netlist of the untouched schematic | **Circuits match uniquely.** (64 merged devices, 44 nets, no property errors) |
| PEX, C-only | magic standard extraction: substrate + coupling C (cthresh=0) | 424 C, total 0.68 pF: **best estimate** of wiring capacitance |
| PEX, full RC | magic `extresist` (wire R + C, rthresh=0) | 225 device fingers, 1505 C, 1562 R, total 1.43 pF: **conservative** (see §5) |
| Post-layout simulation | ngspice, 5 corners + 200-run mismatch MC + start-up + power-down/enable | all specs preserved, see §4 |

**Cell size:** 87.07 µm × 47.20 µm = 4109 µm².

![annotated floorplan](docs/layout_annotated.png)

_Annotated floorplan: every functional block of the final layout outlined and numbered (input pairs, cascodes, current mirrors, beta-multiplier gm bias cell, resistors, start-up, enable logic) with the pin locations. Boxes come from the layout generator's own geometry._

![layout](docs/layout_full.png)

_Full layout (KLayout render of the final GDS). Left: OTA core around a vertical symmetry axis. Right: internal bias (beta-multiplier XM1/XM10, xhigh-po resistors, start-up stack, enable logic)._

![input pairs](docs/layout_inputpairs.png)

_Input pairs. Top: NMOS pair 2×8 (ABBAABBA / BAABBAAB) in a p-tap guard ring. Bottom: PMOS pair 4×14 (rows X, X̄, X̄, X with X = ABBAABBAABBAAB) in an n-tap guard ring. Gate contacts of MP_A1/MN_A1 (VINP) and MP_A2/MN_A2 (VINN) alternate sides and share li straps between rows._

### 2. What was compared

| | Pre-layout (schematic) | Post-layout (extracted layout) |
|---|---|---|
| Netlist | `sim/dut_sch.spice`: xschem simulation netlist of the original `.sch` (device lines identical to the repo's `different_spice/…spice`, incl. `mult`, AD/AS from xschem) | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_cx.spice` (**PEX C-only**, best estimate) and `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice` (**PEX full RC**, conservative) |
| Devices | 80 instances with `m=` multipliers | 225 individual fingers with real AD/AS/PD/PS |
| Parasitics | none | C-only: 424 capacitors, 0.68 pF total. Full RC: 1505 capacitors (1.43 pF) + 1562 wire/contact resistors |

Both DUTs are dropped into **identical testbench decks** (only the `.include` line differs). Models: `sky130A/libs.tech/combined/sky130.lib.spice`. Conditions: VDD = 1.8 V, EN = 1.8 V, T = 27 °C, CL = 10 pF on VOUT, 1 pF on MN_TAIL_BIAS (as in the original testbenches).

| Testbench | Configuration | Extracted metrics |
|---|---|---|
| STB | Unity-gain loop broken with a Middlebrook probe (two AC runs: V-probe and I-probe), VICM = 0.9 V, 1 Hz–1 GHz, 40 pts/dec | DC loop gain (at 1 Hz), UGF, phase margin |
| DC | Unity gain, VICM swept 0 → 1.8 V in 5 mV steps | offset at 0.9 V, worst offset over 0.2–1.6 V |
| PSRR | Unity gain, VICM = 0.9 V, 1 V AC on VDD | Vout/VDD at 10 Hz and 1 MHz |
| TRAN | Unity gain, 0.9 V ± 0.65 V, 1 kHz sine (0.25–1.55 V), 4 ms | peak abs(Vout − VICM) after 1 ms |
| OP | Unity gain, VICM = 0.9 V | IDD, V(MN_TAIL_BIAS) |
| Start-up | VDD, EN, VICM ramp 0 → final in 10 µs, 2 ms, Gear integration | settling of Vout, final IDD and bias |
| MC | `tt_mm` (mismatch on), unity gain, VICM = 0.9 V, 200 independent ngspice processes (`.options seed=1…200`) | offset mean, σ |

Corners: tt, ss, ff, fs, sf (same set as the IP README).

### 3. Headline comparison (tt, 27 °C)

Two post-layout netlists are reported. **PEX C-only** is magic's standard parasitic extraction (substrate + coupling capacitance): the best estimate. **PEX full RC** is magic's `extresist` netlist. It adds wire resistance, but it also writes extra substrate capacitance on every resistor sub-node (1.43 pF total vs 0.68 pF), so it is a conservative bound. Wiring resistance itself is negligible (§5). Startup, power-down and MC were run on the conservative RC netlist.

| Parameter | Unit | Schematic | PEX C-only | PEX full RC | Δ C-only | Δ full RC |
|---|---|---|---|---|---|---|
| DC loop gain | dB | 71.12 | 70.95 | 70.90 | -0.17 | -0.23 |
| Unity-gain frequency | MHz | 2.147 | 2.121 | 2.099 | -0.026 (-1.20 %) | -0.048 (-2.22 %) |
| Phase margin | deg | 86.64 | 85.83 | 85.07 | -0.81 | -1.57 |
| Systematic offset @ VICM=0.9 V | mV | -0.075 | -0.076 | -0.075 | -0.001 | -0.000 |
| Worst-case offset, VICM 0.2–1.6 V | mV | 15.64 | 15.39 | 15.80 | -0.25 | +0.16 |
| PSRR @ 10 Hz (Vout/VDD) | dB | -68.45 | -68.29 | -68.25 | +0.16 | +0.20 |
| PSRR @ 1 MHz (Vout/VDD) | dB | -37.36 | -36.40 | -35.87 | +0.96 | +1.49 |
| Peak dynamic offset (1 kHz sine) | mV | 7.788 | 7.685 | 7.887 | -0.104 | +0.098 |
| Supply current | uA | 26.013 | 26.002 | 25.970 | -0.011 (-0.04 %) | -0.043 (-0.16 %) |
| MN_TAIL_BIAS voltage | V | 0.4800 | 0.4800 | 0.4800 | -0.0000 | +0.0000 |
| Power-down current (EN = 0) | pA | 15.8 | — | 16.6 | — | +0.9 |
| Wake-up time (EN↑ → Vout within 1 mV) | µs | 3.33 | — | 4.15 | — | +0.82 |
| MC offset σ (N=200/200) | mV | 1.625 | — | 1.712 | — | +0.087 |
| MC offset mean | mV | -0.253 | — | -0.062 | — | +0.190 |

_MC mean standard error ≈ 0.11 mV (σ/√N), so the two means agree to within about 2 standard errors; the systematic offset from the deterministic DC run is identical (−0.075 mV)._

### 4. Results across corners

**DC loop gain (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 71.12 | 71.31 | 70.68 | 71.37 | 70.76 |
| PEX C-only | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX full RC | 70.90 | 71.10 | 70.43 | 71.15 | 70.53 |
| Δ C-only | -0.17 | -0.15 | -0.20 | -0.17 | -0.18 |
| Δ full RC | -0.23 | -0.21 | -0.25 | -0.22 | -0.23 |

**Unity-gain frequency (MHz)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 2.147 | 2.120 | 2.167 | 2.131 | 2.151 |
| PEX C-only | 2.121 | 2.095 | 2.141 | 2.106 | 2.125 |
| PEX full RC | 2.099 | 2.073 | 2.118 | 2.084 | 2.103 |
| Δ C-only | -0.026 (-1.20 %) | -0.025 (-1.18 %) | -0.026 (-1.22 %) | -0.025 (-1.19 %) | -0.026 (-1.20 %) |
| Δ full RC | -0.048 (-2.22 %) | -0.047 (-2.20 %) | -0.049 (-2.25 %) | -0.047 (-2.21 %) | -0.048 (-2.23 %) |

**Phase margin (deg)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 86.64 | 86.62 | 86.67 | 86.63 | 86.66 |
| PEX C-only | 85.83 | 85.80 | 85.86 | 85.81 | 85.88 |
| PEX full RC | 85.07 | 85.03 | 85.13 | 85.04 | 85.14 |
| Δ C-only | -0.81 | -0.81 | -0.81 | -0.83 | -0.79 |
| Δ full RC | -1.57 | -1.59 | -1.54 | -1.59 | -1.53 |

**Systematic offset @ VICM=0.9 V (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -0.075 | -0.077 | -0.074 | -0.059 | -0.093 |
| PEX C-only | -0.076 | -0.079 | -0.075 | -0.060 | -0.095 |
| PEX full RC | -0.075 | -0.078 | -0.074 | -0.059 | -0.094 |
| Δ C-only | -0.001 | -0.001 | -0.002 | -0.001 | -0.002 |
| Δ full RC | -0.000 | -0.000 | -0.000 | +0.000 | -0.001 |

**Worst-case offset, VICM 0.2–1.6 V (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 15.64 | 16.85 | 13.51 | 11.65 | 16.18 |
| PEX C-only | 15.39 | 16.60 | 13.29 | 11.48 | 15.92 |
| PEX full RC | 15.80 | 17.03 | 13.65 | 11.78 | 16.34 |
| Δ C-only | -0.25 | -0.25 | -0.21 | -0.17 | -0.25 |
| Δ full RC | +0.16 | +0.18 | +0.14 | +0.13 | +0.17 |

**PSRR @ 10 Hz (Vout/VDD) (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -68.45 | -68.11 | -68.47 | -69.34 | -67.03 |
| PEX C-only | -68.29 | -67.96 | -68.29 | -69.18 | -66.87 |
| PEX full RC | -68.25 | -67.93 | -68.25 | -69.14 | -66.83 |
| Δ C-only | +0.16 | +0.15 | +0.18 | +0.16 | +0.17 |
| Δ full RC | +0.20 | +0.18 | +0.22 | +0.20 | +0.20 |

**PSRR @ 1 MHz (Vout/VDD) (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -37.36 | -37.08 | -37.60 | -37.66 | -36.95 |
| PEX C-only | -36.40 | -36.12 | -36.64 | -36.65 | -36.04 |
| PEX full RC | -35.87 | -35.61 | -36.08 | -36.09 | -35.54 |
| Δ C-only | +0.96 | +0.96 | +0.97 | +1.01 | +0.91 |
| Δ full RC | +1.49 | +1.47 | +1.52 | +1.57 | +1.42 |

**Peak dynamic offset (1 kHz sine) (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 7.788 | 8.805 | 5.944 | 4.383 | 8.554 |
| PEX C-only | 7.685 | 8.683 | 5.874 | 4.329 | 8.444 |
| PEX full RC | 7.887 | 8.917 | 6.023 | 4.446 | 8.662 |
| Δ C-only | -0.104 | -0.122 | -0.071 | -0.055 | -0.110 |
| Δ full RC | +0.098 | +0.112 | +0.079 | +0.063 | +0.107 |

**Supply current (uA)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 26.013 | 25.526 | 26.493 | 25.894 | 26.131 |
| PEX C-only | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX full RC | 25.970 | 25.484 | 26.449 | 25.852 | 26.087 |
| Δ C-only | -0.011 (-0.04 %) | -0.011 (-0.04 %) | -0.011 (-0.04 %) | -0.011 (-0.04 %) | -0.011 (-0.04 %) |
| Δ full RC | -0.043 (-0.16 %) | -0.041 (-0.16 %) | -0.044 (-0.17 %) | -0.042 (-0.16 %) | -0.044 (-0.17 %) |

**MN_TAIL_BIAS voltage (V)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 0.4800 | 0.4950 | 0.4649 | 0.5069 | 0.4531 |
| PEX C-only | 0.4800 | 0.4950 | 0.4649 | 0.5069 | 0.4531 |
| PEX full RC | 0.4800 | 0.4951 | 0.4650 | 0.5070 | 0.4531 |
| Δ C-only | -0.0000 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| Δ full RC | +0.0000 | +0.0000 | +0.0001 | +0.0000 | +0.0000 |

#### 4.1 Loop gain / stability

![stb](sim/plots/sch_vs_pex_stb.png)

#### 4.2 DC transfer: offset vs input common mode

![dc](sim/plots/sch_vs_pex_dc.png)

#### 4.3 PSRR

![psrr](sim/plots/sch_vs_pex_psrr.png)

#### 4.4 Transient tracking (dynamic offset)

![tran](sim/plots/sch_vs_pex_tran.png)

#### 4.5 Monte Carlo offset (mismatch, tt_mm)

| | N | mean (mV) | σ (mV) | ±3σ (mV) | min (mV) | max (mV) |
|---|---|---|---|---|---|---|
| schematic | 200 | -0.253 | 1.625 | ±4.88 | -4.41 | 5.47 |
| layout | 200 | -0.062 | 1.712 | ±5.14 | -5.39 | 4.41 |

With N = 200 the 95 % confidence interval on σ is about ±10 %, so the two σ values are statistically the same. The IP README reports σ = 1.59 mV (N = 1000), which agrees.

![mc](sim/plots/sch_vs_pex_mc.png)

#### 4.6 Start-up

| corner | view | Vout final (V) | MN_TAIL_BIAS final (V) | IDD final, 1.8–2 ms avg (µA) | Vout within 1 mV after (µs) |
|---|---|---|---|---|---|
| tt | schematic | 0.8999 | 0.4800 | 26.01 | 11.7 |
| tt | layout | 0.8999 | 0.4800 | 25.97 | 12.2 |
| ss | schematic | 0.8999 | 0.4951 | 25.53 | 11.8 |
| ss | layout | 0.8999 | 0.4951 | 25.48 | 12.3 |
| ff | schematic | 0.8999 | 0.4649 | 26.49 | 11.4 |
| ff | layout | 0.8999 | 0.4650 | 26.45 | 11.8 |

The supply ramps for 10 µs. In every corner the internal bias starts, Vout settles to within 1 mV about 2 µs after the ramp ends, and the final supply current equals the DC operating point.

![startup](sim/plots/sch_vs_pex_startup.png)

**Start-up mechanism, probed in the extracted layout (tt, nets carry schematic names via layout labels):**

| t (µs) | VDD | VSTRP_IP | net14 | VSTRP_OUT | EN_B | VBP_TOP | MN_TAIL_BIAS | VOUT |
|---|---|---|---|---|---|---|---|---|
| 2 | 0.360 | 0.175 | 0.162 | 0.251 | 0.069 | 0.135 | 0.005 | 0.017 |
| 4 | 0.720 | 0.360 | 0.600 | 0.694 | 0.000 | 0.271 | 0.008 | 0.031 |
| 6 | 1.080 | 0.128 | 1.079 | 0.181 | 0.001 | 0.403 | 0.013 | 0.045 |
| 8 | 1.440 | 0.099 | 1.438 | 0.291 | 0.003 | 0.600 | 0.082 | 0.058 |
| 10 | 1.800 | 0.058 | 1.795 | 0.421 | 0.005 | 1.013 | 0.361 | 0.069 |
| 12 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.705 | 0.476 | 0.894 |
| 15 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |
| 20 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |
| 40 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |

While the bias is still off, VSTRP_IP is low and net14 high. VSTRP_OUT is pulled to 0.2–0.4 V, which turns M12 on and injects current from the R24–R34 chain into MN_TAIL_BIAS. Once the beta multiplier is up (~12 µs), M2 lifts VSTRP_IP to 1.79 V, net14 falls, VSTRP_OUT returns to 1.8 V and the injector switches off. Design observation (schematic left unchanged): with EN = 1, M14 (gate EN_B = 0) is always on, so VSTRP_OUT is a ratioed node during start-up (M38/M39 overpower M14). It works in all simulated corners, both pre- and post-layout.

#### 4.7 Post-layout (PEX, full RC) results by themselves

Post-layout netlist only, all five corners. These are the post-layout equivalents of the IP's original `IEEE_plots` (files in `sim/plots/pex/`).

**Loop gain and phase (A0, UGF, PM per corner in the legend)**

![Loop gain and phase (A0, UGF, PM per corner in the legend)](sim/plots/pex/pex_stb.png)

**DC transfer: Vout vs VICM and offset (grey = 0.2–1.6 V window)**

![DC transfer: Vout vs VICM and offset (grey = 0.2–1.6 V window)](sim/plots/pex/pex_dc.png)

**PSRR**

![PSRR](sim/plots/pex/pex_psrr.png)

**Unity-gain tracking of a 1 kHz 0.25–1.55 V sine and the dynamic offset**

![Unity-gain tracking of a 1 kHz 0.25–1.55 V sine and the dynamic offset](sim/plots/pex/pex_tran.png)

**Mismatch Monte Carlo with Gaussian fit and ±3σ**

![Mismatch Monte Carlo with Gaussian fit and ±3σ](sim/plots/pex/pex_mc.png)

**Start-up**

![Start-up](sim/plots/pex/pex_startup.png)

#### 4.8 Power-down (EN = 0) and enable / disable timing

**Method.** The OTA starts enabled (VDD = 1.8 V, VICM = 0.9 V, unity gain, 10 pF). EN is pulled low at 5 µs and the circuit is simulated for 2 ms of power-down (Gear integration). The power-down current is the average supply current over 1.9–2.0 ms, and node states are taken at 2 ms. This mirrors what silicon sees. A plain DC operating point with EN = 0 is ill-conditioned: VOUT and several cascode/start-up nodes float, and in 3 of 16 cases the solver failed to converge and returned non-physical currents, so it is not used.

**Power-down supply current**

| Condition | Schematic (pA) | PEX full RC (pA) |
|---|---|---|
| tt, 27 °C | 15.8 | 16.6 |
| ss, 27 °C | 12.3 | 13.5 |
| ff, 27 °C | 25.3 | 25.7 |
| fs, 27 °C | 10.4 | 11.4 |
| sf, 27 °C | 29.1 | 28.9 |
| tt, −40 °C | 6.2 | 7.4 |
| tt, 85 °C | 369.3 | 292.2 |
| tt, 125 °C | 4430.0 | 2376.4 |

Power-down current is **10–30 pA at 27 °C in every corner**, 0.3–0.4 nA at 85 °C and 2.4–4.4 nA at 125 °C (junction leakage). At 125 °C the layout leaks less than the schematic because the drawn fingers share source/drain diffusions, giving less junction area than the schematic's per-finger AD/AS estimate.

![power-down current](sim/plots/powerdown/pd_current.png)

**Node states in power-down (tt, 27 °C, 2 ms after EN → 0)**

| Node | Schematic (V) | PEX (V) | Meaning |
|---|---|---|---|
| MN_TAIL_BIAS | 0.000 | 0.000 | beta-multiplier gate pulled to GNDA by XM16 |
| VBP_TOP | 1.800 | 1.800 | PMOS bias rail pulled to VDD by M15 |
| net8 | 0.000 | 0.000 | NMOS mirror gate pulled to GNDA by MN_SW1 |
| net9 | 1.800 | 1.800 | PMOS tail gate pulled to VDD by MP_SW1 |
| VBP_CASC | 1.800 | 1.800 | PMOS cascode gate pulled to VDD by MP_SW2 |
| VBN_CASC | 0.000 | 0.000 | NMOS cascode gate pulled to GNDA by MN_SW2 |
| VSTRP_IP | 0.000 | 0.000 | start-up sense node low (bias off) |
| net14 | 1.800 | 1.800 | inverter output high |
| VSTRP_OUT | 1.799 | 1.799 | M12 gate ≈ VDD: start-up injector off (only weakly held; see sf) |
| net15 | 1.800 | 1.800 | = VDD, so no current flows through R24–R34 |
| EN_B | 1.800 | 1.800 | inverted enable |
| VOUT | 0.902 | 0.902 | floats and holds its last value on CL (high impedance in power-down) |

VSTRP_OUT is not actively driven in power-down (M13, M14 and M39 are off). It settles at 1.66 V in sf and 1.71 V at −40 °C (PEX), which keeps M12 off in every simulated case; the power-down current confirms no leakage through the resistor chain.

**Enable / disable timing** (EN 0→1 at 20 µs, 1→0 at 120 µs)

| corner | view | IDD enabled (µA) | bias within 1 % (µs) | IDD within 2 % (µs) | Vout within 1 mV (µs) | IDD < 1 % after EN↓ (µs) | IDD 100 µs after EN↓ (nA) |
|---|---|---|---|---|---|---|---|
| tt | schematic | 26.01 | 2.45 | 3.28 | 3.33 | 0.38 | 0.023 |
| tt | PEX | 25.97 | 3.04 | 4.06 | 4.15 | 0.42 | 0.031 |
| ss | schematic | 25.53 | 2.61 | 3.42 | 3.47 | 0.37 | 0.020 |
| ss | PEX | 25.48 | 3.22 | 4.60 | 4.70 | 0.42 | 0.027 |
| ff | schematic | 26.49 | 2.44 | 3.13 | 3.03 | 0.36 | 0.032 |
| ff | PEX | 26.45 | 2.71 | 3.73 | 3.78 | 0.39 | 0.038 |

Wake-up to full accuracy takes 3.0–4.7 µs. The extracted layout is 0.6–1.2 µs slower than the schematic because of the extra parasitic capacitance on the bias rails. Shut-down drops the current below 1 % within 0.4 µs; the remaining tail settles to the pA leakage floor over ~100 µs.

![EN toggle](sim/plots/powerdown/en_toggle.png)

![wake-up](sim/plots/powerdown/wakeup_zoom.png)

### 5. Layout vs PEX: where the deltas come from

The same testbenches were run on five netlist views. Each step adds exactly one effect:

| View | Netlist | Adds |
|---|---|---|
| Schematic | `sim/dut_sch.spice` | — (schematic devices, `m=` multipliers, xschem AD/AS) |
| Layout, devices only | `mag/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.lvs.spice` (`ext2spice lvs`) | **device geometry**: the 225 drawn fingers with real AD/AS/PD/PS, no wiring |
| PEX C-only | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_cx.spice` | **wiring capacitance** (substrate + coupling), magic's standard extraction: best estimate |
| PEX RC, all R shorted | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx_R0.spice` | the **extra substrate capacitance** that magic's `extresist` writes on the resistor sub-nodes (no resistance) |
| PEX full RC | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice` | **wiring resistance** |

**Why two capacitance levels.** The coupling capacitors are identical in both extractions. `extresist`, however, writes additional substrate capacitance on every resistor sub-node, while the lumped node capacitance stays in the netlist. Total extracted capacitance rises from 0.68 pF (C-only) to 1.43 pF (RC), about 1.9–2× on every signal net. For VOUT, for example, the substrate capacitance goes from 1.5 fF to ≈ 9.7 fF, while a hand estimate of its ≈ 40 µm met3 bus and ≈ 50 µm of met2 tracks gives a few fF. The C-only value is therefore the best estimate, and the RC netlist is a conservative bound.

**tt, 27 °C, step by step**

| Parameter | Schematic | Layout (devices) | PEX C-only | PEX RC, R shorted | PEX full RC | Δ geometry | Δ wiring C | Δ extresist extra C | Δ wiring R |
|---|---|---|---|---|---|---|---|---|---|
| DC loop gain (dB) | 71.12 | 70.95 | 70.95 | 70.95 | 70.90 | -0.17 | -0.00 | +0.00 | -0.05 |
| Unity-gain frequency (MHz) | 2.147 | 2.144 | 2.121 | 2.103 | 2.099 | -0.003 | -0.022 | -0.018 | -0.004 |
| Phase margin (deg) | 86.64 | 86.83 | 85.83 | 85.07 | 85.07 | +0.19 | -1.00 | -0.75 | -0.00 |
| Systematic offset @ VICM=0.9 V (mV) | -0.075 | -0.076 | -0.076 | -0.076 | -0.075 | -0.001 | +0.000 | +0.000 | +0.001 |
| Worst-case offset, VICM 0.2–1.6 V (mV) | 15.64 | 15.39 | 15.39 | 15.39 | 15.80 | -0.25 | +0.00 | -0.00 | +0.41 |
| PSRR @ 10 Hz (Vout/VDD) (dB) | -68.45 | -68.29 | -68.29 | -68.29 | -68.25 | +0.16 | +0.00 | +0.00 | +0.04 |
| PSRR @ 1 MHz (Vout/VDD) (dB) | -37.36 | -37.31 | -36.40 | -35.88 | -35.87 | +0.06 | +0.91 | +0.52 | +0.01 |
| Peak dynamic offset (1 kHz sine) (mV) | 7.788 | 7.684 | 7.685 | 7.685 | 7.887 | -0.104 | +0.000 | +0.000 | +0.202 |
| Supply current (uA) | 26.013 | 26.002 | 26.002 | 26.002 | 25.970 | -0.011 | +0.000 | +0.000 | -0.032 |
| MN_TAIL_BIAS voltage (V) | 0.4800 | 0.4800 | 0.4800 | 0.4800 | 0.4800 | -0.0000 | +0.0000 | +0.0000 | +0.0001 |

**DC loop gain (dB), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 71.12 | 71.31 | 70.68 | 71.37 | 70.76 |
| Layout, devices only | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX C-only | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX RC, all R shorted | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX full RC | 70.90 | 71.10 | 70.43 | 71.15 | 70.53 |

**Unity-gain frequency (MHz), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 2.147 | 2.120 | 2.167 | 2.131 | 2.151 |
| Layout, devices only | 2.144 | 2.117 | 2.163 | 2.128 | 2.148 |
| PEX C-only | 2.121 | 2.095 | 2.141 | 2.106 | 2.125 |
| PEX RC, all R shorted | 2.103 | 2.077 | 2.122 | 2.087 | 2.107 |
| PEX full RC | 2.099 | 2.073 | 2.118 | 2.084 | 2.103 |

**Phase margin (deg), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 86.64 | 86.62 | 86.67 | 86.63 | 86.66 |
| Layout, devices only | 86.83 | 86.83 | 86.84 | 86.82 | 86.85 |
| PEX C-only | 85.83 | 85.80 | 85.86 | 85.81 | 85.88 |
| PEX RC, all R shorted | 85.07 | 85.03 | 85.13 | 85.04 | 85.14 |
| PEX full RC | 85.07 | 85.03 | 85.13 | 85.04 | 85.14 |

**PSRR @ 1 MHz (Vout/VDD) (dB), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | -37.36 | -37.08 | -37.60 | -37.66 | -36.95 |
| Layout, devices only | -37.31 | -37.01 | -37.56 | -37.59 | -36.91 |
| PEX C-only | -36.40 | -36.12 | -36.64 | -36.65 | -36.04 |
| PEX RC, all R shorted | -35.88 | -35.62 | -36.09 | -36.10 | -35.55 |
| PEX full RC | -35.87 | -35.61 | -36.08 | -36.09 | -35.54 |

**Supply current (uA), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 26.013 | 25.526 | 26.493 | 25.894 | 26.131 |
| Layout, devices only | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX C-only | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX RC, all R shorted | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX full RC | 25.970 | 25.484 | 26.449 | 25.852 | 26.087 |

**Interpretation (tt):**

* **Device geometry** (real fingers and shared diffusions) changes PM by +0.19°, UGF by -3.2 kHz and the DC loop gain by -0.17 dB.
* **Wiring capacitance** (best estimate) changes PM by -1.00°, UGF by -22.5 kHz and PSRR @ 1 MHz by +0.91 dB.
* The **extra substrate capacitance from `extresist`** adds -0.75° PM, -18.3 kHz UGF and +0.52 dB PSRR @ 1 MHz on top. This is the pessimism of the RC netlist.
* **Wiring resistance** is negligible: -0.005° PM and -3.7 kHz UGF.

**Per-net check of wiring resistance (tt):** each net's extracted resistors were shorted one at a time in the full-RC netlist and the loop gain re-simulated (`sim/r_attribution.py`). The largest single-net effects are:

| Net whose R is shorted | Σ R in net (Ω) | Δ UGF (kHz) | Δ PM (deg) |
|---|---|---|---|
| GNDA | 252315 | +0.33 | -0.0076 |
| VINN | 8002 | +0.00 | +0.0045 |
| net2 | 2764 | +0.68 | +0.0032 |
| net4 | 4701 | +1.19 | +0.0029 |
| net3 | 4811 | -0.45 | +0.0022 |
| VDD | 72233 | -0.56 | -0.0022 |
| net5 | 6626 | -0.04 | +0.0020 |
| VINP | 8948 | -0.00 | +0.0011 |

All nets shorted together: PM 85.072° vs 85.067° with resistance. No net's wiring resistance matters for stability in this layout.

**Loop gain, tt: all views (right: zoom on the high-frequency region where parasitics act)**

![Loop gain, tt: all views (right: zoom on the high-frequency region where parasitics act)](sim/plots/views/views_stb_tt.png)

**Key metrics per corner for all views**

![Key metrics per corner for all views](sim/plots/views/views_metrics_corners.png)

**PSRR, tt: all views**

![PSRR, tt: all views](sim/plots/views/views_psrr_tt.png)

**DC offset, tt, and the difference of each layout view to the schematic (µV)**

![DC offset, tt, and the difference of each layout view to the schematic (µV)](sim/plots/views/views_dc_tt.png)

**Dynamic offset, tt, and the difference to the schematic (µV)**

![Dynamic offset, tt, and the difference to the schematic (µV)](sim/plots/views/views_tran_tt.png)

#### 5.1 met1 shunt of the input gate straps: before → after

The first layout routed the input-pair gates on li1 only (≈ 12.8 Ω/sq): a strap along each row and a vertical li bar per input. That gave a mean pin-to-gate resistance of 1.1–1.4 kΩ (up to 3 kΩ), and VINP and VINN were noticeably asymmetric. The final layout shunts every input gate strap (PMOS pair S0–S4, NMOS pair S0–S2) and both vertical bars with met1, with an mcon at every gate. To keep magic's 0.28 µm spacing from the long S/D stripes, the merged PMOS strap gap grew from 0.64 to 0.80 µm and the NMOS one from 0.78 to 0.80 µm (+0.18 µm cell height). The top and bottom strips of the two input guard rings became li-only taps (no DC current; the vertical ring strips keep met1).

**Effective resistance from the input pin to the 36 input-pair gate fingers** (solved on the extracted RC network, `sim/gate_resistance.py`)

| Net | Before: mean / max (Ω) | After: mean / max (Ω) | Reduction of mean |
|---|---|---|---|
| VINP | 1435 / 3016 | 111 / 124 | 92 % |
| VINN | 1090 / 1670 | 111 / 123 | 90 % |

**Effect on stability.** Shorting all wiring resistance in the old RC netlist raised PM by only +0.104°. After the shunt the same test gives +0.005°. The shunt therefore removed essentially all of the (small) resistive effect, and PM improved by the expected ≈ 0.1°. Stability was never resistance-limited: VINP is driven from outside the feedback loop, and VINN's gate capacitance is largely bootstrapped by the pair's common source. The practical benefits of the shunt are **symmetric, low-resistance inputs** (≈ 110 Ω) and less gate-resistance thermal noise (√(4kTR): 4.9 → 1.4 nV/√Hz on VINP).

| Metric | Corner | Schematic | PEX RC before | PEX RC after | Change |
|---|---|---|---|---|---|
| UGF (MHz) | tt | 2.147 | 2.104 | 2.099 | -0.005 |
| UGF (MHz) | ss | 2.120 | 2.078 | 2.073 | -0.005 |
| UGF (MHz) | ff | 2.167 | 2.123 | 2.118 | -0.005 |
| UGF (MHz) | fs | 2.131 | 2.089 | 2.084 | -0.005 |
| UGF (MHz) | sf | 2.151 | 2.108 | 2.103 | -0.005 |
| Phase margin (deg) | tt | 86.64 | 84.98 | 85.07 | +0.090 |
| Phase margin (deg) | ss | 86.62 | 84.94 | 85.03 | +0.089 |
| Phase margin (deg) | ff | 86.67 | 85.03 | 85.13 | +0.092 |
| Phase margin (deg) | fs | 86.63 | 84.95 | 85.04 | +0.090 |
| Phase margin (deg) | sf | 86.66 | 85.05 | 85.14 | +0.090 |
| PSRR @ 1 MHz (dB) | tt | -37.36 | -35.90 | -35.87 | +0.035 |
| PSRR @ 1 MHz (dB) | ss | -37.08 | -35.65 | -35.61 | +0.035 |
| PSRR @ 1 MHz (dB) | ff | -37.60 | -36.12 | -36.08 | +0.036 |
| PSRR @ 1 MHz (dB) | fs | -37.66 | -36.13 | -36.09 | +0.037 |
| PSRR @ 1 MHz (dB) | sf | -36.95 | -35.57 | -35.54 | +0.034 |
| DC loop gain (dB) | tt | 71.12 | 70.90 | 70.90 | +0.000 |
| DC loop gain (dB) | ss | 71.31 | 71.10 | 71.10 | +0.000 |
| DC loop gain (dB) | ff | 70.68 | 70.43 | 70.43 | +0.000 |
| DC loop gain (dB) | fs | 71.37 | 71.15 | 71.15 | +0.000 |
| DC loop gain (dB) | sf | 70.76 | 70.53 | 70.53 | +0.000 |

MC offset σ (PEX): 1.562 mV before, 1.712 mV after. Offsets, supply current and start-up are unaffected by the change.

### 6. Parasitics of the critical nets

Total extracted capacitance per net from the **PEX C-only** (best-estimate) extraction, summing capacitance to substrate and coupling to all other nets. Internal nets carry the schematic names via layout labels. The R-segment count is from the full-RC extraction.

| Net | Role | C_total (fF) | extracted R segments |
|---|---|---|---|
| VINP | input + | 80.35 | 119 |
| VINN | input − | 79.52 | 137 |
| net1 | PMOS-pair drain A / NMOS fold | 52.32 | 73 |
| net2 | PMOS-pair drain B / NMOS fold | 54.81 | 73 |
| net3 | NMOS-pair drain A / PMOS fold | 19.56 | 43 |
| net4 | NMOS-pair drain B / PMOS fold | 18.15 | 42 |
| net5 | high-Z node L1 (mirror gate) | 30.39 | 47 |
| VOUT | output | 16.44 | 21 |
| net6 | NMOS-pair tail | 24.42 | 47 |
| net7 | PMOS-pair tail | 67.84 | 127 |
| MN_TAIL_BIAS | bias node / pin | 69.00 | 55 |
| EN | enable | 12.99 | 13 |

**Symmetry of matched nets**

| Pair | C (fF) | C (fF) | mismatch |
|---|---|---|---|
| VINP / VINN | 80.35 | 79.52 | -1.0 % |
| net1 / net2 | 52.32 | 54.81 | +4.6 % |
| net3 / net4 | 19.56 | 18.15 | -7.5 % |

The input nets match to under 1 %. The folding nodes differ by 1.5–2.7 fF because the net1/net3 buses run on the left of the core and net2/net4 on the right with different lengths. These are non-dominant, low-impedance nodes (1/gm of the cascodes), so the imbalance does not show up in the offset (the systematic offset is unchanged to 1 µV, §3).

### 7. Discussion

* **Stability / bandwidth.** Against the schematic, the best-estimate extraction (C-only) changes UGF by -1.2 % and PM by -0.81°. The conservative RC netlist changes them by -2.2 % and -1.57°, the same in every corner. Almost all of it is parasitic capacitance at the folding nodes (net1–net5) acting on the non-dominant poles. Wiring resistance contributes -0.005° (§5). With the 10 pF load the OTA stays over-damped (PM ≈ 85–86°).
* **DC accuracy.** Systematic offset is unchanged (≤ 1 µV difference). The DC loop gain changes by -0.23 dB. IR drops in the routing are negligible at this 26 µA supply current, consistent with VOUT and MN_TAIL_BIAS matching to 0.1 mV.
* **PSRR.** Low-frequency PSRR is unchanged within 0.2 dB. At 1 MHz it degrades by +0.96 dB (C-only) to +1.49 dB (RC), through coupling capacitance between the VDD rails/n-ring and internal nodes. It remains ≈ -36 dB.
* **Matching.** Mismatch σ is preserved (layout and schematic are statistically identical). SPICE Monte Carlo models only random mismatch. The common-centroid placement (§8) additionally cancels linear process gradients, which neither simulation captures; this is a layout-only benefit.
* **Power and start-up.** IDD differs by < 0.2 %. Start-up is clean in ss/tt/ff and identical to the schematic within 0.4 µs.

### 8. Matching / floorplan decisions

See §3 Matching above.

### 9. Notes for integration

* LVS reference: the schematic ties NMOS bodies to the global `GND` net. In silicon the p-substrate is `GNDA` (all p-taps), so `lvs/run_lvs.sh` maps body `GND` → `GNDA`. Nothing else is altered.
* Pins (port order = symbol order): VDD (met1, top rail), EN (met2, right edge), VINN (met3, top), VOUT (met3, bottom), VINP (met3, left), MN_TAIL_BIAS (met3, bottom), GNDA (met1, bottom rail). met4/met5 are unused and free for top-level routing.
* Reproduce everything with `./run_all.sh` (layout generation → magic DRC → KLayout DRC → LVS → PEX → all simulations). Then `python3 sim/run_views.py && python3 sim/plot_results.py && python3 sim/plot_pex.py && python3 sim/plot_views.py && python3 sim/parasitics.py && python3 sim/startup_probe.py && python3 sim/make_report.py`.
* Post-layout netlists for top-level simulation: `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_cx.spice` (C-only, best estimate) or `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice` (full RC, conservative, with extra substrate C from `extresist`). Both have the same port order as the symbol.
* Simulation note: the start-up supply current must be read with Gear integration (or averaged). Trapezoidal integration rings point-to-point on the source current; the ringing averages to the DC value.
<!-- END:AUTO-VERIFICATION -->

## Files

```
LAYOUT/
├── README.md                  this document (hand-written sections + auto-generated results)
├── run_all.sh                 full flow: generate → magic DRC → KLayout DRC → LVS → PEX → simulations
├── gds/                       final GDS  (top cell Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias)
├── mag/                       magic layout (.mag), magic DRC report (.drc, empty = clean), LVS extraction
├── drc/                       KLayout sky130A_mr.drc report (.lyrdb) + log
├── lvs/                       run_lvs.sh, reference netlist (ref.spice), netgen report (lvs_report.txt)
├── pex/                       *_rcx.spice (full RC), *_cx.spice (C only), pex.tcl, pex.log (antenna)
├── xschem/                    netlist.sh → ota_lvs.spice (LVS) and ota_sim.spice (simulation),
│                              both netlisted from ../SCH (schematic unchanged)
├── sim/                       run_sims.py (SCH + PEX testbenches), run_views.py (4 views),
│   │                          run_powerdown.py, dut_sch.spice, results*.json, summary.txt,
│   │                          parasitics.py/json, startup_probe.py/json, plot_*.py, make_report.py
│   └── plots/                 sch_vs_pex_*.png · pex/ (PEX only) · views/ (layout vs PEX) · powerdown/
├── docs/                      POST_LAYOUT_VERIFICATION.md (standalone report), layout renders
└── scripts/                   layout generator (gen_ota.py, lay.py), magic runner, KLayout renderer
```

## Reproducing

Tools used: magic 8.3.637, netgen 1.5.323, ngspice 46, KLayout 0.30.8, xschem 3.4.8,
sky130A from ciel (open_pdks `1689ac3f2dc763876eaf967227c7dfe831b031ae`), Python 3 with numpy and matplotlib.
Set `PDK_ROOT` to the directory that contains `sky130A` (default `~/.ciel`).

```bash
cd OTAs/RR_Inp_SE_OTA_IntBias/LAYOUT
./xschem/netlist.sh            # (re)netlist ../SCH for LVS and pre-layout simulation
NMC=200 ./run_all.sh           # layout + DRC + KLayout DRC + LVS + PEX + SCH/PEX simulations (~30 min)
cd sim
python3 run_views.py           # layout devices-only, PEX C-only and RC-with-R-shorted views (~15 min)
python3 r_attribution.py       # per-net wiring-resistance check (tt loop gain)
python3 gate_resistance.py ../pex/*_rcx.spice gate_resistance.json   # pin-to-gate R of the input pairs
python3 run_powerdown.py       # power-down current (corners, temperature) + EN on/off transient
python3 plot_results.py && python3 plot_pex.py && python3 plot_views.py && python3 plot_powerdown.py
python3 parasitics.py && python3 startup_probe.py
python3 make_report.py         # docs/POST_LAYOUT_VERIFICATION.md + this README + ../README.md sections
cd .. && python3 scripts/annotate_layout.py   # docs/layout_annotated.png
```

The raw per-run simulation decks and outputs (`sim/sch/`, `sim/pex/`) and magic intermediates are
regenerated by the flow and are not committed (see `.gitignore`).
