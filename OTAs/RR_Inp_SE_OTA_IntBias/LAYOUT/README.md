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
| Size | **87.07 µm × 47.02 µm = 4094 µm²** |
| Devices | 80 schematic instances (64 after netgen parallel merging), drawn as 225 fingers/segments |
| Active area | 1563 µm² gate + 171 µm² resistor body (≈ 42 % of the cell box) |
| Layers used | diff/tap, poly, li1, met1 (device straps, rails), met2 (horizontal tracks), met3 (vertical buses). **met4/met5 free** |
| Pins | VDD, EN, VINN, VOUT, VINP, MN_TAIL_BIAS, GNDA (same order as the symbol) |
| Signoff | magic DRC 0 · KLayout sky130 DRC 0 · antenna clean · LVS *Circuits match uniquely* |

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
  its own nwell (body = VDD, as in the schematic) inside an n-tap guard ring. The NMOS pair has a
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
| **MP_A1 / MP_A2** (pfet_lvt 28+28 × W4/L2) | 4 rows × 14 fingers; rows **X, X̄, X̄, X** with X = `ABBAABBAABBAAB` | Finger-level interdigitation. X/X̄ pairing gives a common centroid in x, and the X X̄ X̄ X stacking gives a common centroid in y and also cancels the xy-gradient term. Rows 1/4 end in A and rows 2/3 end in B, so both devices get the same number of edge fingers. A↔B share the source (net7) and A↔A / B↔B share drains, so the diffusion is continuous. |
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

* **li1:** gate straps and short local jumpers only (no DC current).
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
| MC | `tt_mm` mismatch, 200 independent ngspice processes (seed 1…200), VICM = 0.9 V | offset mean and σ |

<!-- BEGIN:AUTO-VERIFICATION -->
## Verification & schematic-vs-layout comparison (auto-generated)

### 1. Signoff summary

| Check | Tool / setup | Result |
|---|---|---|
| DRC | magic 8.3, `drc(full)`, sky130A tech | **0 errors** |
| DRC (2nd opinion) | KLayout `sky130A_mr.drc`, FEOL+BEOL+off-grid (256 rule categories) | **0 violations** |
| Antenna | magic `antennacheck` | **0 violations** |
| LVS | netgen 1.5 + `sky130A_setup.tcl`, layout vs xschem netlist of the untouched schematic | **Circuits match uniquely.** (64 merged devices, 44 nets, no property errors) |
| PEX | magic full RC (`extresist`, coupling C, cthresh=0, rthresh=0) | 225 device fingers, 1450 C, 1464 R |
| Post-layout simulation | ngspice, 5 corners + 200-run mismatch MC + start-up | all specs preserved, see §4 |

**Cell size:** 87.07 µm × 47.02 µm = 4094 µm².

![layout](docs/layout_full.png)

_Full layout (KLayout render of the final GDS). Left: OTA core around a vertical symmetry axis. Right: internal bias (beta-multiplier XM1/XM10, xhigh-po resistors, start-up stack, enable logic)._

![input pairs](docs/layout_inputpairs.png)

_Input pairs. Top: NMOS pair 2×8 (ABBAABBA / BAABBAAB) in a p-tap guard ring. Bottom: PMOS pair 4×14 (rows X, X̄, X̄, X with X = ABBAABBAABBAAB) in an n-tap guard ring. Gate contacts of MP_A1/MN_A1 (VINP) and MP_A2/MN_A2 (VINN) alternate sides and share li straps between rows._

### 2. What was compared

| | Pre-layout (schematic) | Post-layout (layout) |
|---|---|---|
| Netlist | `sim/dut_sch.spice`: xschem simulation netlist of the original `.sch` (device lines identical to the repo's `different_spice/…spice`, incl. `mult`, AD/AS from xschem) | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice`: magic RC extraction of the final layout |
| Devices | 80 instances with `m=` multipliers | 225 individual fingers with real AD/AS/PD/PS |
| Parasitics | none | 1450 capacitors (to substrate + coupling), 1464 wire/contact resistors |

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

| Parameter | Unit | Schematic | Layout (RC) | Δ (layout − sch) |
|---|---|---|---|---|
| DC loop gain | dB | 71.12 | 70.90 | -0.23 |
| Unity-gain frequency | MHz | 2.147 | 2.104 | -0.043 (-2.00 %) |
| Phase margin | deg | 86.64 | 84.98 | -1.66 |
| Systematic offset @ VICM=0.9 V | mV | -0.075 | -0.075 | -0.000 |
| Worst-case offset, VICM 0.2–1.6 V | mV | 15.64 | 15.80 | +0.16 |
| PSRR @ 10 Hz (Vout/VDD) | dB | -68.45 | -68.25 | +0.20 |
| PSRR @ 1 MHz (Vout/VDD) | dB | -37.36 | -35.90 | +1.46 |
| Peak dynamic offset (1 kHz sine) | mV | 7.788 | 7.887 | +0.098 |
| Supply current | uA | 26.013 | 25.970 | -0.043 (-0.16 %) |
| MN_TAIL_BIAS voltage | V | 0.4800 | 0.4800 | +0.0000 |
| MC offset σ (N=200/200) | mV | 1.625 | 1.562 | -0.063 |
| MC offset mean | mV | -0.253 | -0.018 | +0.235 |

_MC mean standard error ≈ 0.11 mV (σ/√N), so the two means agree to within about 2 standard errors; the systematic offset from the deterministic DC run is identical (−0.075 mV)._

### 4. Results across corners

**DC loop gain (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 71.12 | 71.31 | 70.68 | 71.37 | 70.76 |
| layout | 70.90 | 71.10 | 70.43 | 71.15 | 70.53 |
| Δ | -0.23 | -0.21 | -0.25 | -0.22 | -0.23 |

**Unity-gain frequency (MHz)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 2.147 | 2.120 | 2.167 | 2.131 | 2.151 |
| layout | 2.104 | 2.078 | 2.123 | 2.089 | 2.108 |
| Δ | -0.043 (-2.00 %) | -0.042 (-1.98 %) | -0.044 (-2.03 %) | -0.042 (-1.99 %) | -0.043 (-2.01 %) |

**Phase margin (deg)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 86.64 | 86.62 | 86.67 | 86.63 | 86.66 |
| layout | 84.98 | 84.94 | 85.03 | 84.95 | 85.05 |
| Δ | -1.66 | -1.68 | -1.64 | -1.68 | -1.62 |

**Systematic offset @ VICM=0.9 V (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -0.075 | -0.077 | -0.074 | -0.059 | -0.093 |
| layout | -0.075 | -0.078 | -0.074 | -0.059 | -0.094 |
| Δ | -0.000 | -0.000 | -0.000 | +0.000 | -0.001 |

**Worst-case offset, VICM 0.2–1.6 V (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 15.64 | 16.85 | 13.51 | 11.65 | 16.18 |
| layout | 15.80 | 17.03 | 13.65 | 11.78 | 16.34 |
| Δ | +0.16 | +0.18 | +0.14 | +0.13 | +0.17 |

**PSRR @ 10 Hz (Vout/VDD) (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -68.45 | -68.11 | -68.47 | -69.34 | -67.03 |
| layout | -68.25 | -67.93 | -68.25 | -69.14 | -66.83 |
| Δ | +0.20 | +0.18 | +0.22 | +0.20 | +0.20 |

**PSRR @ 1 MHz (Vout/VDD) (dB)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | -37.36 | -37.08 | -37.60 | -37.66 | -36.95 |
| layout | -35.90 | -35.65 | -36.12 | -36.13 | -35.57 |
| Δ | +1.46 | +1.43 | +1.48 | +1.53 | +1.38 |

**Peak dynamic offset (1 kHz sine) (mV)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 7.788 | 8.805 | 5.944 | 4.383 | 8.554 |
| layout | 7.887 | 8.917 | 6.023 | 4.446 | 8.662 |
| Δ | +0.098 | +0.112 | +0.079 | +0.063 | +0.107 |

**Supply current (uA)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 26.013 | 25.526 | 26.493 | 25.894 | 26.131 |
| layout | 25.970 | 25.485 | 26.449 | 25.852 | 26.087 |
| Δ | -0.043 (-0.16 %) | -0.041 (-0.16 %) | -0.044 (-0.17 %) | -0.041 (-0.16 %) | -0.044 (-0.17 %) |

**MN_TAIL_BIAS voltage (V)**

| | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| schematic | 0.4800 | 0.4950 | 0.4649 | 0.5069 | 0.4531 |
| layout | 0.4800 | 0.4951 | 0.4650 | 0.5070 | 0.4531 |
| Δ | +0.0000 | +0.0000 | +0.0001 | +0.0000 | +0.0000 |

#### 4.1 Loop gain / stability

![stb](sim/plots/stb_pre_post.png)

#### 4.2 DC transfer: offset vs input common mode

![dc](sim/plots/dc_offset_pre_post.png)

#### 4.3 PSRR

![psrr](sim/plots/psrr_pre_post.png)

#### 4.4 Transient tracking (dynamic offset)

![tran](sim/plots/tran_offset_pre_post.png)

#### 4.5 Monte Carlo offset (mismatch, tt_mm)

| | N | mean (mV) | σ (mV) | ±3σ (mV) | min (mV) | max (mV) |
|---|---|---|---|---|---|---|
| schematic | 200 | -0.253 | 1.625 | ±4.88 | -4.41 | 5.47 |
| layout | 200 | -0.018 | 1.562 | ±4.69 | -4.06 | 4.30 |

With N = 200 the 95 % confidence interval on σ is about ±10 %, so the two σ values are statistically the same. The IP README reports σ = 1.59 mV (N = 1000), which agrees.

![mc](sim/plots/mc_offset_pre_post.png)

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

![startup](sim/plots/startup_pre_post.png)

**Start-up mechanism, probed in the extracted layout (tt, nets carry schematic names via layout labels):**

| t (µs) | VDD | VSTRP_IP | net14 | VSTRP_OUT | EN_B | VBP_TOP | MN_TAIL_BIAS | VOUT |
|---|---|---|---|---|---|---|---|---|
| 2 | 0.361 | 0.175 | 0.162 | 0.251 | 0.069 | 0.135 | 0.005 | 0.016 |
| 4 | 0.721 | 0.360 | 0.599 | 0.694 | 0.000 | 0.271 | 0.008 | 0.031 |
| 6 | 1.080 | 0.128 | 1.079 | 0.181 | 0.001 | 0.403 | 0.013 | 0.045 |
| 8 | 1.440 | 0.099 | 1.438 | 0.291 | 0.003 | 0.600 | 0.082 | 0.058 |
| 10 | 1.800 | 0.058 | 1.795 | 0.421 | 0.005 | 1.013 | 0.361 | 0.068 |
| 12 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.705 | 0.476 | 0.894 |
| 15 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |
| 20 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |
| 40 | 1.800 | 1.786 | 0.000 | 1.800 | 0.000 | 0.701 | 0.480 | 0.900 |

While the bias is still off, VSTRP_IP is low and net14 high. VSTRP_OUT is pulled to 0.2–0.4 V, which turns M12 on and injects current from the R24–R34 chain into MN_TAIL_BIAS. Once the beta multiplier is up (~12 µs), M2 lifts VSTRP_IP to 1.79 V, net14 falls, VSTRP_OUT returns to 1.8 V and the injector switches off. Design observation (schematic left unchanged): with EN = 1, M14 (gate EN_B = 0) is always on, so VSTRP_OUT is a ratioed node during start-up (M38/M39 overpower M14). It works in all simulated corners, both pre- and post-layout.

### 5. Parasitics of the critical nets

Total extracted capacitance per net, summing caps to substrate and coupling to all other nets. Internal nets carry the schematic names via layout labels.

| Net | Role | C_total (fF) | extracted R segments |
|---|---|---|---|
| VINP | input + | 66.67 | 69 |
| VINN | input − | 67.25 | 71 |
| net1 | PMOS-pair drain A / NMOS fold | 51.35 | 73 |
| net2 | PMOS-pair drain B / NMOS fold | 54.09 | 73 |
| net3 | NMOS-pair drain A / PMOS fold | 19.35 | 43 |
| net4 | NMOS-pair drain B / PMOS fold | 17.84 | 42 |
| net5 | high-Z node L1 (mirror gate) | 30.41 | 47 |
| VOUT | output | 16.74 | 21 |
| net6 | NMOS-pair tail | 24.13 | 47 |
| net7 | PMOS-pair tail | 66.81 | 127 |
| MN_TAIL_BIAS | bias node / pin | 68.98 | 55 |
| EN | enable | 12.99 | 13 |

**Symmetry of matched nets**

| Pair | C (fF) | C (fF) | mismatch |
|---|---|---|---|
| VINP / VINN | 66.67 | 67.25 | +0.9 % |
| net1 / net2 | 51.35 | 54.09 | +5.2 % |
| net3 / net4 | 19.35 | 17.84 | -8.1 % |

The input nets match to under 1 %. The folding nodes differ by 1.5–2.7 fF because the net1/net3 buses run on the left of the core and net2/net4 on the right with different lengths. These are non-dominant, low-impedance nodes (1/gm of the cascodes), so the imbalance does not show up in the offset (the systematic offset is unchanged to 1 µV, §3).

### 6. Discussion

* **Stability / bandwidth.** UGF drops by -2.0 % and phase margin by 1.66°, the same in every corner. This is the expected effect of the extracted wiring and junction capacitance at the folding nodes (net1–net5) on the non-dominant poles. With the 10 pF load the OTA stays over-damped (PM ≈ 85°).
* **DC accuracy.** Systematic offset is unchanged (≤ 1 µV difference). The DC loop gain changes by -0.23 dB. IR drops in the routing are negligible at this 26 µA supply current, consistent with VOUT and MN_TAIL_BIAS matching to 0.1 mV.
* **PSRR.** Low-frequency PSRR is unchanged within 0.2 dB. At 1 MHz it degrades by 1.5 dB through extracted coupling capacitance from the VDD rails/ring to internal nodes; it remains ≈ -36 dB.
* **Matching.** Mismatch σ is preserved (layout and schematic are statistically identical). SPICE Monte Carlo models only random mismatch. The common-centroid placement (§7) additionally cancels linear process gradients, which neither simulation captures; this is a layout-only benefit.
* **Power and start-up.** IDD differs by < 0.2 %. Start-up is clean in ss/tt/ff and identical to the schematic within 0.4 µs.

### 7. Matching / floorplan decisions

See §3 Matching above.

### 8. Notes for integration

* LVS reference: the schematic ties NMOS bodies to the global `GND` net. In silicon the p-substrate is `GNDA` (all p-taps), so `lvs/run_lvs.sh` maps body `GND` → `GNDA`. Nothing else is altered.
* Pins (port order = symbol order): VDD (met1, top rail), EN (met2, right edge), VINN (met3, top), VOUT (met3, bottom), VINP (met3, left), MN_TAIL_BIAS (met3, bottom), GNDA (met1, bottom rail). met4/met5 are unused and free for top-level routing.
* Reproduce everything with `./run_all.sh` (layout generation → magic DRC → KLayout DRC → LVS → PEX → all simulations). Then `python3 sim/plot_results.py && python3 sim/parasitics.py && python3 sim/make_report.py`.
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
├── sim/                       run_sims.py (all testbenches), dut_sch.spice, results.json,
│   │                          summary.txt, summary_table.md, parasitics.py/json,
│   │                          startup_probe.py/json, plot_results.py, make_report.py
│   └── plots/                 schematic-vs-layout plots (STB, DC, PSRR, TRAN, MC, start-up)
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
NMC=200 ./run_all.sh           # layout + DRC + KLayout DRC + LVS + PEX + all simulations (~30 min)
python3 sim/plot_results.py && python3 sim/parasitics.py && \
python3 sim/startup_probe.py && python3 sim/make_report.py   # plots + report + README results
```

The raw per-run simulation decks and outputs (`sim/sch/`, `sim/pex/`) and magic intermediates are
regenerated by the flow and are not committed (see `.gitignore`).
