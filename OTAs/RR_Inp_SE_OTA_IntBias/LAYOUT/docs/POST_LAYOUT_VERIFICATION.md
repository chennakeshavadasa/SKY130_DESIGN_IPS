# Post-Layout Verification: `Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias` (SKY130A)

_Generated 2026-10-17 by `sim/make_report.py` from the signoff and simulation results in this directory. Every number below comes from those files._

Layout of the rail-to-rail-input folded-cascode OTA with internal beta-multiplier bias from `OTAs/RR_Inp_SE_OTA_IntBias`. **The schematic was not modified.**

## 1. Signoff summary

| Check | Tool / setup | Result |
|---|---|---|
| DRC | magic 8.3, `drc(full)`, sky130A tech | **0 errors** |
| DRC (2nd opinion) | KLayout `sky130A_mr.drc`, FEOL+BEOL+off-grid (256 rule categories) | **0 violations** |
| Antenna | magic `antennacheck` | **0 violations** |
| LVS | netgen 1.5 + `sky130A_setup.tcl`, layout vs xschem netlist of the untouched schematic | **Circuits match uniquely.** (64 merged devices, 44 nets, no property errors) |
| PEX | magic full RC (`extresist`, coupling C, cthresh=0, rthresh=0) | 225 device fingers, 1450 C, 1464 R |
| Post-layout simulation | ngspice, 5 corners + 200-run mismatch MC + start-up + power-down/enable | all specs preserved, see §4 |

**Cell size:** 87.07 µm × 47.02 µm = 4094 µm².

![layout](layout_full.png)

_Full layout (KLayout render of the final GDS). Left: OTA core around a vertical symmetry axis. Right: internal bias (beta-multiplier XM1/XM10, xhigh-po resistors, start-up stack, enable logic)._

![input pairs](layout_inputpairs.png)

_Input pairs. Top: NMOS pair 2×8 (ABBAABBA / BAABBAAB) in a p-tap guard ring. Bottom: PMOS pair 4×14 (rows X, X̄, X̄, X with X = ABBAABBAABBAAB) in an n-tap guard ring. Gate contacts of MP_A1/MN_A1 (VINP) and MP_A2/MN_A2 (VINN) alternate sides and share li straps between rows._

## 2. What was compared

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

## 3. Headline comparison (tt, 27 °C)

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
| Power-down current (EN = 0) | pA | 15.8 | 16.6 | +0.9 |
| Wake-up time (EN↑ → Vout within 1 mV) | µs | 3.33 | 4.18 | +0.85 |
| MC offset σ (N=200/200) | mV | 1.625 | 1.562 | -0.063 |
| MC offset mean | mV | -0.253 | -0.018 | +0.235 |

_MC mean standard error ≈ 0.11 mV (σ/√N), so the two means agree to within about 2 standard errors; the systematic offset from the deterministic DC run is identical (−0.075 mV)._

## 4. Results across corners

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

### 4.1 Loop gain / stability

![stb](../sim/plots/sch_vs_pex_stb.png)

### 4.2 DC transfer: offset vs input common mode

![dc](../sim/plots/sch_vs_pex_dc.png)

### 4.3 PSRR

![psrr](../sim/plots/sch_vs_pex_psrr.png)

### 4.4 Transient tracking (dynamic offset)

![tran](../sim/plots/sch_vs_pex_tran.png)

### 4.5 Monte Carlo offset (mismatch, tt_mm)

| | N | mean (mV) | σ (mV) | ±3σ (mV) | min (mV) | max (mV) |
|---|---|---|---|---|---|---|
| schematic | 200 | -0.253 | 1.625 | ±4.88 | -4.41 | 5.47 |
| layout | 200 | -0.018 | 1.562 | ±4.69 | -4.06 | 4.30 |

With N = 200 the 95 % confidence interval on σ is about ±10 %, so the two σ values are statistically the same. The IP README reports σ = 1.59 mV (N = 1000), which agrees.

![mc](../sim/plots/sch_vs_pex_mc.png)

### 4.6 Start-up

| corner | view | Vout final (V) | MN_TAIL_BIAS final (V) | IDD final, 1.8–2 ms avg (µA) | Vout within 1 mV after (µs) |
|---|---|---|---|---|---|
| tt | schematic | 0.8999 | 0.4800 | 26.01 | 11.7 |
| tt | layout | 0.8999 | 0.4800 | 25.97 | 12.2 |
| ss | schematic | 0.8999 | 0.4951 | 25.53 | 11.8 |
| ss | layout | 0.8999 | 0.4951 | 25.48 | 12.3 |
| ff | schematic | 0.8999 | 0.4649 | 26.49 | 11.4 |
| ff | layout | 0.8999 | 0.4650 | 26.45 | 11.8 |

The supply ramps for 10 µs. In every corner the internal bias starts, Vout settles to within 1 mV about 2 µs after the ramp ends, and the final supply current equals the DC operating point.

![startup](../sim/plots/sch_vs_pex_startup.png)

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

### 4.7 Post-layout (PEX, full RC) results by themselves

Post-layout netlist only, all five corners. These are the post-layout equivalents of the IP's original `IEEE_plots` (files in `sim/plots/pex/`).

**Loop gain and phase (A0, UGF, PM per corner in the legend)**

![Loop gain and phase (A0, UGF, PM per corner in the legend)](../sim/plots/pex/pex_stb.png)

**DC transfer: Vout vs VICM and offset (grey = 0.2–1.6 V window)**

![DC transfer: Vout vs VICM and offset (grey = 0.2–1.6 V window)](../sim/plots/pex/pex_dc.png)

**PSRR**

![PSRR](../sim/plots/pex/pex_psrr.png)

**Unity-gain tracking of a 1 kHz 0.25–1.55 V sine and the dynamic offset**

![Unity-gain tracking of a 1 kHz 0.25–1.55 V sine and the dynamic offset](../sim/plots/pex/pex_tran.png)

**Mismatch Monte Carlo with Gaussian fit and ±3σ**

![Mismatch Monte Carlo with Gaussian fit and ±3σ](../sim/plots/pex/pex_mc.png)

**Start-up**

![Start-up](../sim/plots/pex/pex_startup.png)

### 4.8 Power-down (EN = 0) and enable / disable timing

**Method.** The OTA starts enabled (VDD = 1.8 V, VICM = 0.9 V, unity gain, 10 pF). EN is pulled low at 5 µs and the circuit is simulated for 2 ms of power-down (Gear integration). The power-down current is the average supply current over 1.9–2.0 ms, and node states are taken at 2 ms. This mirrors what silicon sees. A plain DC operating point with EN = 0 is ill-conditioned: VOUT and several cascode/start-up nodes float, and in 3 of 16 cases the solver failed to converge and returned non-physical currents, so it is not used.

**Power-down supply current**

| Condition | Schematic (pA) | PEX full RC (pA) |
|---|---|---|
| tt, 27 °C | 15.8 | 16.6 |
| ss, 27 °C | 12.3 | 13.5 |
| ff, 27 °C | 25.3 | 25.8 |
| fs, 27 °C | 10.4 | 11.4 |
| sf, 27 °C | 29.1 | 28.9 |
| tt, −40 °C | 6.2 | 7.4 |
| tt, 85 °C | 369.3 | 292.3 |
| tt, 125 °C | 4430.0 | 2376.5 |

Power-down current is **10–30 pA at 27 °C in every corner**, 0.3–0.4 nA at 85 °C and 2.4–4.4 nA at 125 °C (junction leakage). At 125 °C the layout leaks less than the schematic because the drawn fingers share source/drain diffusions, giving less junction area than the schematic's per-finger AD/AS estimate.

![power-down current](../sim/plots/powerdown/pd_current.png)

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

VSTRP_OUT is not actively driven in power-down (M13, M14 and M39 are off). It settles at 1.66 V in sf and 1.70 V at −40 °C (PEX), which keeps M12 off in every simulated case; the power-down current confirms no leakage through the resistor chain.

**Enable / disable timing** (EN 0→1 at 20 µs, 1→0 at 120 µs)

| corner | view | IDD enabled (µA) | bias within 1 % (µs) | IDD within 2 % (µs) | Vout within 1 mV (µs) | IDD < 1 % after EN↓ (µs) | IDD 100 µs after EN↓ (nA) |
|---|---|---|---|---|---|---|---|
| tt | schematic | 26.01 | 2.45 | 3.28 | 3.33 | 0.38 | 0.023 |
| tt | PEX | 25.97 | 3.03 | 4.08 | 4.18 | 0.41 | 0.031 |
| ss | schematic | 25.53 | 2.61 | 3.42 | 3.47 | 0.37 | 0.020 |
| ss | PEX | 25.48 | 3.22 | 4.59 | 4.69 | 0.42 | 0.027 |
| ff | schematic | 26.49 | 2.44 | 3.13 | 3.03 | 0.36 | 0.032 |
| ff | PEX | 26.45 | 2.71 | 3.73 | 3.78 | 0.40 | 0.038 |

Wake-up to full accuracy takes 3.0–4.7 µs. The extracted layout is 0.6–1.2 µs slower than the schematic because of the extra parasitic capacitance on the bias rails. Shut-down drops the current below 1 % within 0.4 µs; the remaining tail settles to the pA leakage floor over ~100 µs.

![EN toggle](../sim/plots/powerdown/en_toggle.png)

![wake-up](../sim/plots/powerdown/wakeup_zoom.png)

## 5. Layout vs PEX: where the deltas come from

To separate the effect of the physical devices from the wiring parasitics, the same testbenches were also run on two intermediate views of the layout:

| View | Netlist | Contains |
|---|---|---|
| Schematic | `sim/dut_sch.spice` | schematic devices (`m=` multipliers, xschem AD/AS) |
| Layout, devices only | `mag/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.lvs.spice` (magic `ext2spice lvs`) | the 225 drawn fingers with their real AD/AS/PD/PS; no wiring R or C |
| PEX, C only | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_cx.spice` | + extracted wiring capacitance to substrate and coupling |
| PEX, full RC | `pex/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias_rcx.spice` | + extracted wire/contact resistance (final post-layout view) |

The step-by-step differences show where each delta comes from: **layout − schematic** is device geometry (shared diffusions, finger splitting), **PEX C − layout** is wiring capacitance, and **PEX RC − PEX C** is wiring resistance.

**tt, 27 °C**

| Parameter | Schematic | Layout (devices) | PEX C | PEX RC | Δ geometry | Δ parasitic C | Δ wire R | Δ total |
|---|---|---|---|---|---|---|---|---|
| DC loop gain (dB) | 71.12 | 70.95 | 70.95 | 70.90 | -0.17 | -0.00 | -0.05 | -0.23 |
| Unity-gain frequency (MHz) | 2.147 | 2.144 | 2.124 | 2.104 | -0.003 | -0.020 | -0.020 | -0.043 |
| Phase margin (deg) | 86.64 | 86.83 | 85.83 | 84.98 | +0.19 | -1.00 | -0.85 | -1.66 |
| Systematic offset @ VICM=0.9 V (mV) | -0.075 | -0.076 | -0.076 | -0.075 | -0.001 | +0.000 | +0.001 | -0.000 |
| Worst-case offset, VICM 0.2–1.6 V (mV) | 15.64 | 15.39 | 15.39 | 15.80 | -0.25 | +0.00 | +0.41 | +0.16 |
| PSRR @ 10 Hz (Vout/VDD) (dB) | -68.45 | -68.29 | -68.29 | -68.25 | +0.16 | +0.00 | +0.04 | +0.20 |
| PSRR @ 1 MHz (Vout/VDD) (dB) | -37.36 | -37.31 | -36.45 | -35.90 | +0.06 | +0.85 | +0.55 | +1.46 |
| Peak dynamic offset (1 kHz sine) (mV) | 7.788 | 7.684 | 7.685 | 7.887 | -0.104 | +0.000 | +0.202 | +0.098 |
| Supply current (uA) | 26.013 | 26.002 | 26.002 | 25.970 | -0.011 | +0.000 | -0.032 | -0.043 |
| MN_TAIL_BIAS voltage (V) | 0.4800 | 0.4800 | 0.4800 | 0.4800 | -0.0000 | +0.0000 | +0.0001 | +0.0000 |

**DC loop gain (dB), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 71.12 | 71.31 | 70.68 | 71.37 | 70.76 |
| Layout, devices only | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX, C only | 70.95 | 71.16 | 70.49 | 71.21 | 70.58 |
| PEX, full RC | 70.90 | 71.10 | 70.43 | 71.15 | 70.53 |

**Unity-gain frequency (MHz), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 2.147 | 2.120 | 2.167 | 2.131 | 2.151 |
| Layout, devices only | 2.144 | 2.117 | 2.163 | 2.128 | 2.148 |
| PEX, C only | 2.124 | 2.098 | 2.143 | 2.108 | 2.128 |
| PEX, full RC | 2.104 | 2.078 | 2.123 | 2.089 | 2.108 |

**Phase margin (deg), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 86.64 | 86.62 | 86.67 | 86.63 | 86.66 |
| Layout, devices only | 86.83 | 86.83 | 86.84 | 86.82 | 86.85 |
| PEX, C only | 85.83 | 85.81 | 85.86 | 85.81 | 85.88 |
| PEX, full RC | 84.98 | 84.94 | 85.03 | 84.95 | 85.05 |

**PSRR @ 1 MHz (Vout/VDD) (dB), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | -37.36 | -37.08 | -37.60 | -37.66 | -36.95 |
| Layout, devices only | -37.31 | -37.01 | -37.56 | -37.59 | -36.91 |
| PEX, C only | -36.45 | -36.17 | -36.69 | -36.70 | -36.09 |
| PEX, full RC | -35.90 | -35.65 | -36.12 | -36.13 | -35.57 |

**Supply current (uA), all corners**

| view | tt | ss | ff | fs | sf |
|---|---|---|---|---|---|
| Schematic | 26.013 | 25.526 | 26.493 | 25.894 | 26.131 |
| Layout, devices only | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX, C only | 26.002 | 25.515 | 26.483 | 25.883 | 26.121 |
| PEX, full RC | 25.970 | 25.485 | 26.449 | 25.852 | 26.087 |

**Interpretation (tt):**

* UGF change -0.043 MHz: device geometry 7 %, parasitic C 46 %, wire R 46 %.
* Phase-margin change -1.66°: device geometry -12 %, parasitic C 60 %, wire R 51 %.
* PSRR @ 1 MHz change +1.46 dB: device geometry 4 %, parasitic C 59 %, wire R 38 %.
* DC loop gain: 71.12 → 70.95 → 70.95 → 70.90 dB. Offsets and supply current are unchanged across all views (see table).

**Loop gain, tt: four views (right: zoom on the high-frequency region where parasitics act)**

![Loop gain, tt: four views (right: zoom on the high-frequency region where parasitics act)](../sim/plots/views/views_stb_tt.png)

**Key metrics per corner for all four views**

![Key metrics per corner for all four views](../sim/plots/views/views_metrics_corners.png)

**PSRR, tt: four views**

![PSRR, tt: four views](../sim/plots/views/views_psrr_tt.png)

**DC offset, tt, and the difference of each layout view to the schematic (µV)**

![DC offset, tt, and the difference of each layout view to the schematic (µV)](../sim/plots/views/views_dc_tt.png)

**Dynamic offset, tt, and the difference to the schematic (µV)**

![Dynamic offset, tt, and the difference to the schematic (µV)](../sim/plots/views/views_tran_tt.png)

## 6. Parasitics of the critical nets

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

## 7. Discussion

* **Stability / bandwidth.** UGF drops by 2.0 % and phase margin by 1.66°, the same in every corner. The four-view analysis (§5) splits this roughly half and half. **Wiring capacitance** slows the non-dominant poles at the folding nodes (net1–net5). **Wiring resistance** is mostly the li1 gate bars and straps of the input pairs (VINP/VINN, segments up to 0.84 kΩ) driving the ~2 pF input-pair gate capacitance, plus the net5 li strap to the MP_TOP gates. Device geometry alone changes PM by only +0.2°. With the 10 pF load the OTA stays over-damped (PM ≈ 85°). *Optional improvement:* shunting the VINP/VINN li gate bars and inter-row straps with met1 would recover most of the ~0.85° attributed to wire R.
* **DC accuracy.** Systematic offset is unchanged (≤ 1 µV difference). The DC loop gain changes by -0.23 dB. IR drops in the routing are negligible at this 26 µA supply current, consistent with VOUT and MN_TAIL_BIAS matching to 0.1 mV.
* **PSRR.** Low-frequency PSRR is unchanged within 0.2 dB. At 1 MHz it degrades by 1.5 dB: about 60 % from coupling capacitance between the VDD rails/n-ring and internal nodes, the rest from wiring resistance (§5). It remains ≈ -36 dB.
* **Matching.** Mismatch σ is preserved (layout and schematic are statistically identical). SPICE Monte Carlo models only random mismatch. The common-centroid placement (§8) additionally cancels linear process gradients, which neither simulation captures; this is a layout-only benefit.
* **Power and start-up.** IDD differs by < 0.2 %. Start-up is clean in ss/tt/ff and identical to the schematic within 0.4 µs.

## 8. Matching / floorplan decisions

| Group | Arrangement |
|---|---|
| MP_A1/MP_A2 (pfet_lvt, 28+28 × W4/L2) | 4×14, rows X X̄ X̄ X (X = ABBAABBAABBAAB): common centroid in x and y and cancels the xy cross-term; edge fingers balanced (A at the ends of rows 1/4, B of rows 2/3); n-tap guard ring |
| MN_A1/MN_A2 (nfet_lvt, 8+8 × W2.5/L2) | 2×8 ABBAABBA / BAABBAAB, 2-D common centroid; p-tap guard ring |
| MP_TOP_L1/L2 (6+6) | ABBA·ABBA·ABBA, continuous diffusion |
| MN_BOT_L1/L2 (6+6), MN_NDIFF_BIAS (8) | 2 rows ABBAAB / BAABBA (2-D CC), NDIFF_BIAS split symmetrically 2+2 per row |
| MP_CASC_L1/L2 (8+8) | [A4][B4][B4][A4] |
| MN_CASC_L1/L2 (3+3) | [A1][B2][A2][B1] (closest to centroid possible with 3+3) |
| net9 mirror | MP_PDIFF_BIAS 4 + 4 symmetric about the diode MP_PDIFF_BIAS_B |
| VBP_TOP mirror | M3 (diode) and M4 adjacent with shared source; M9, M2 same row and orientation |
| XM1/XM10 (16+4 × W10/L4) | 2 identical rows [M1×4][M10×2][M1×4]: 2-D common centroid, merged gate strap |

Per-finger W and L are the schematic's, and netgen merges parallel fingers, so sizes match exactly. Dummy transistors were **not** added: they would appear as extra devices in LVS against the unmodified schematic. Edge effects are handled by the common-centroid patterns instead.

## 9. Notes for integration

* LVS reference: the schematic ties NMOS bodies to the global `GND` net. In silicon the p-substrate is `GNDA` (all p-taps), so `lvs/run_lvs.sh` maps body `GND` → `GNDA`. Nothing else is altered.
* Pins (port order = symbol order): VDD (met1, top rail), EN (met2, right edge), VINN (met3, top), VOUT (met3, bottom), VINP (met3, left), MN_TAIL_BIAS (met3, bottom), GNDA (met1, bottom rail). met4/met5 are unused and free for top-level routing.
* Reproduce everything with `./run_all.sh` (layout generation → magic DRC → KLayout DRC → LVS → PEX → all simulations). Then `python3 sim/run_views.py && python3 sim/plot_results.py && python3 sim/plot_pex.py && python3 sim/plot_views.py && python3 sim/parasitics.py && python3 sim/startup_probe.py && python3 sim/make_report.py`.
* Simulation note: the start-up supply current must be read with Gear integration (or averaged). Trapezoidal integration rings point-to-point on the source current; the ringing averages to the DC value.
