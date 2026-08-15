v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1620 -440 2110 -190 {flags=graph
y1=-0.11
y2=1.8
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=1.8
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vout
vicm
vout vicm -"
color="4 7 10"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/tb_Gm_Cell_v2.raw
sim_type=dc
autoload=1
hilight_wave=-1}
B 2 1620 -720 2110 -440 {flags=graph
y1=-0.013
y2=1.6
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=1.6e-05
x2=0.01
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="vout
vicm
vout vicm -"
color="4 7 10"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/tb_Gm_Cell_v2.raw
sim_type=tran
autoload=1
hilight_wave=-1}
B 2 1130 -700 1620 -450 {flags=graph
y1=-80
y2=-52
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=0
x2=12
divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0
node="vout log10() 20 *"
color=4
dataset=-1
unitx=1
logx=1
logy=0
rawfile=$netlist_dir/tb_Gm_Cell_v2.raw
sim_type=ac
autoload=1
hilight_wave=-1}
N 600 -220 600 -180 {lab=VICM}
N 600 -120 600 -90 {lab=0}
N 850 -370 850 -320 {lab=VDD}
N 810 -160 810 -110 {lab=MN_BIAS}
N 740 -110 810 -110 {lab=MN_BIAS}
N 420 -190 420 -150 {lab=VDD}
N 420 -90 420 -60 {lab=0}
N 190 -90 190 -60 {lab=0}
N 190 -180 190 -150 {lab=GNDA}
N 280 -90 280 -60 {lab=0}
N 280 -180 280 -150 {lab=EN}
N 600 -260 680 -260 {lab=Vout}
N 600 -220 680 -220 {lab=VICM}
N 810 -370 810 -320 {lab=EN}
N 980 -240 1070 -240 {lab=Vout}
N 850 -160 850 -90 {lab=0}
N 1070 -240 1130 -240 {lab=Vout}
N 1070 -130 1070 -90 {lab=0}
N 1070 -240 1070 -190 {lab=Vout}
N 940 -470 1070 -470 {lab=Vout
spice_ignore=true}
N 600 -470 700 -470 {lab=Vout
spice_ignore=true}
N 760 -470 880 -470 {lab=probe
spice_ignore=true}
N 830 -660 830 -620 {lab=0
spice_ignore=true}
N 830 -560 830 -470 {lab=probe
spice_ignore=true}
N 600 -700 600 -260 {lab=Vout}
N 600 -700 1070 -700 {lab=Vout}
N 1070 -700 1070 -240 {lab=Vout}
C {/home/nithin/eda/LPCAS_TTSKY26a/OTA_Gm_Cell_v2.sym} 830 -240 0 0 {name=DUT}
C {gnd.sym} 850 -90 0 0 {name=l1 lab=0}
C {vsource.sym} 600 -150 0 0 {name=V1 value="dc 0.9 sin(0.9 0.65 1k)" savecurrent=false}
C {gnd.sym} 600 -90 0 0 {name=l2 lab=0}
C {vdd.sym} 850 -370 0 0 {name=l3 lab=VDD}
C {vsource.sym} 420 -120 0 0 {name=V2 value="dc 1.8 ac 1" savecurrent=false}
C {gnd.sym} 420 -60 0 0 {name=l4 lab=0}
C {vdd.sym} 420 -190 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 1130 -240 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {lab_pin.sym} 740 -110 2 1 {name=p2 sig_type=std_logic lab=MN_BIAS}
C {vsource.sym} 190 -120 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} 190 -60 0 0 {name=l6 lab=0}
C {lab_pin.sym} 190 -180 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} 410 -370 0 0 {name=SAVE_COMM only_toplevel=false value="

.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm3.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm4.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm5.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm6.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm7.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm10.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm12.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm15.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm16.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm8.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm9.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm11.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm19.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm20.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm21.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm26.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm27.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm28.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm29.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm30.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm31.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm32.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.dut.xm33.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.dut.xm34.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm35.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm36.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm37.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm38.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm39.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm42.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm43.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm44.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[gm]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[gds]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[vth]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[cgg]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[cgso]
.save @m.dut.xm45.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm46.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm47.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm48.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm49.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm50.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm51.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm13.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[gm]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[gds]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[vth]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[cgg]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[cgso]
.save @m.dut.xm14.msky130_fd_pr__pfet_01v8[cgdo]
"}
C {vsource.sym} 280 -120 0 0 {name=V5 value=1.8 savecurrent=false}
C {gnd.sym} 280 -60 0 0 {name=l8 lab=0}
C {lab_pin.sym} 280 -180 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code_shown.sym} 0 -670 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.param A=10k Vos=0 VDD=1.8 VSS=0
.option wnflag=1 gmin=1e-18
.option savecurrents
.temp 27
.control
save all
op
write tb_Gm_Cell_v2.raw
set appendwrite 
dc v1 0 1.8 10m
write tb_Gm_Cell_v2.raw
set appendwrite 
plot v(Vout) v(VICM)
plot v(Vout)-v(VICM)
ac dec 20 1 1e12 
write tb_Gm_Cell_v2.raw
plot vdb(Vout)
tran 100u 10m 0.01m 
write tb_Gm_Cell_v2.raw
plot v(Vout) v(VICM) v(Vout)-v(VICM)
plot v(Vout)-v(VICM)
.endc
"
}
C {devices/code.sym} 280 -370 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
place=header}
C {devices/launcher.sym} 460 -450 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {capa.sym} 1070 -160 0 0 {name=C1
m=1
value=50p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1070 -90 0 0 {name=l10 lab=0}
C {title.sym} 160 0 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} 320 -640 0 0 {name=MC_SIMS only_toplevel=true 
value="
.option gmin=1e-18
.options savecurrents
.save all
.temp=27
.control
 let runs=1000
 let r=0
 dowhile r < runs
   reset
   let run=r
   op
   write /home/nithin/eda/LPCAS_TTSKY26a/tb_Gm_Cell_v2_MC_Sims_TB.raw
   set appendwrite
   let DIFF_MIS=v(VICM)-v(Vout) 
   print v(DIFF_MIS)
   wrdata /home/nithin/eda/LPCAS_TTSKY26a/tb_Gm_Cell_v2_MC_Sims_TB.txt r v(DIFF_MIS)
   wrdata /home/nithin/eda/LPCAS_TTSKY26a/tb_Gm_Cell_v2_MC_Sims_TB.csv r v(DIFF_MIS)

   let r = r + 1
 end
.endc"
spice_ignore=true}
C {lab_pin.sym} 600 -220 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {vsource.sym} 910 -470 3 0 {name=Vprobe1 value="dc 0 ac 1" savecurrent=false
spice_ignore=true}
C {vsource.sym} 730 -470 1 0 {name=Vprobe2 value=0 savecurrent=false
spice_ignore=true}
C {isource.sym} 830 -590 0 0 {name=Iprobe1 value="dc 0 ac 1"
spice_ignore=true}
C {gnd.sym} 830 -660 2 0 {name=l7 lab=0
spice_ignore=true}
C {devices/code.sym} 460 -640 0 0 {name=STB_SIMS only_toplevel=true 
value="
.options savecurrents
.control
 save all
 let runs=2
 let run=0

 alter @Vprobe1[acmag]=1
 alter @iprobe1[acmag]=0

 dowhile run < runs
 set run =”$&run”
 ac dec 20 1 10G
 write OTA_STB_TB_\{$run\}.raw
 all
 alter @Vprobe1[acmag]=0
 alter @iprobe1[acmag]=1
 let run = run + 1
 end

 let ip22 = ac2.i(Vprobe2)
 let vprb1 = ac1.probe
 let mb = 1/(vprb1+ip22)-1
 let phase_mb = 180/PI*vp(mb)
 plot vdb(mb)
 plot phase_mb
 plot vdb(mb) phase_mb
 echo "-------------------------------"
 echo "-------------------------------"
 meas ac peak MAX vmag(mb) FROM=2 TO=1.5GHZ
 let f3db = peak/sqrt(2)
 meas ac f1 WHEN vmag(mb)=f3db RISE=1
 meas ac BW WHEN vmag(mb)=f3db FALL=1
 let GBW = peak*BW
 meas ac pm_deg find phase_mb when vdb(mb)=0
 meas ac dominant_pole_f when vdb(mb)=0
 meas ac loop_gain find vdb(mb) at=0.01
 print GBW
 op
 show m : gm : gmbs : gds : vds : vdsat : vgs : vth : id
.endc"
spice_ignore=true}
C {lab_pin.sym} 830 -470 3 0 {name=p4 sig_type=std_logic lab=probe
spice_ignore=true}
C {devices/launcher.sym} 460 -490 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {sky130_fd_pr/corner.sym} 230 -520 0 0 {name=CORNER only_toplevel=true corner=tt
spice_ignore=true}
C {lab_pin.sym} 810 -370 0 0 {name=p5 sig_type=std_logic lab=EN }
