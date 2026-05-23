v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 600 -230 600 -180 {lab=VICM}
N 600 -120 600 -90 {lab=0}
N 830 -130 830 -100 {lab=0}
N 420 -190 420 -150 {lab=VDD}
N 420 -90 420 -60 {lab=0}
N 190 -90 190 -60 {lab=0}
N 190 -180 190 -150 {lab=GNDA}
N 280 -90 280 -60 {lab=0}
N 280 -180 280 -150 {lab=EN}
N 600 -250 680 -250 {lab=VICM}
N 600 -230 680 -230 {lab=VICM}
N 830 -360 830 -310 {lab=VDD}
N 980 -240 1060 -240 {lab=Vout}
N 1060 -240 1070 -240 {lab=Vout}
N 830 -170 830 -130 {lab=0}
N 1070 -240 1130 -240 {lab=Vout}
N 1070 -130 1070 -90 {lab=0}
N 1070 -240 1070 -190 {lab=Vout}
N 600 -250 600 -230 {lab=VICM}
C {/home/nithin/eda/LPCAS_TTSKY26a/OTA_Gm_Cell_v3.sym} 830 -240 0 0 {name=x1}
C {gnd.sym} 830 -100 0 0 {name=l1 lab=0}
C {vsource.sym} 600 -150 0 0 {name=V1 value=0.9 savecurrent=false}
C {gnd.sym} 600 -90 0 0 {name=l2 lab=0}
C {vsource.sym} 420 -120 0 0 {name=V2 value=1.8 savecurrent=false}
C {gnd.sym} 420 -60 0 0 {name=l4 lab=0}
C {vdd.sym} 420 -190 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 1130 -240 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {vsource.sym} 190 -120 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} 190 -60 0 0 {name=l6 lab=0}
C {lab_pin.sym} 190 -180 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} 410 -370 0 0 {name=SAVE_COMM only_toplevel=false value="

.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm3.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm4.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm5.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm6.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm7.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm10.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm12.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm15.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm16.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm8.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm9.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm11.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm19.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm20.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm21.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm26.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm27.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm28.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm29.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm30.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm31.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm32.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.x1.xm33.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.x1.xm34.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm35.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm36.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm37.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm38.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm39.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm40.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm41.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm42.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm43.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm44.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xm45.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm46.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm47.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm48.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm49.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm50.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xm51.msky130_fd_pr__pfet_01v8[cgdo]
"}
C {vsource.sym} 280 -120 0 0 {name=V5 value=1.8 savecurrent=false}
C {gnd.sym} 280 -60 0 0 {name=l8 lab=0}
C {lab_pin.sym} 280 -180 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code_shown.sym} 0 -450 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.option wnflag=1 gmin=1e-18
.option savecurrents
.temp 27
.control
save all
op
write tb_Gm_Cell_v3.raw
set appendwrite 
**dc temp -40 140 10
**write OTA_Gm_Cell.raw
.endc
"}
C {devices/code.sym} 280 -370 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt_mm
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
spice_ignore=false
place=header}
C {devices/launcher.sym} 460 -450 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {vdd.sym} 830 -360 0 0 {name=l9 lab=VDD}
C {capa.sym} 1070 -160 0 0 {name=C1
m=1
value=50p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1070 -90 0 0 {name=l10 lab=0}
C {title.sym} 160 0 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} -140 -450 0 0 {name=MC_SIMS only_toplevel=true 
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
C {lab_pin.sym} 600 -230 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {devices/code.sym} -140 -310 0 0 {name=STB_SIMS only_toplevel=true 
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
 write OTA_STB_TB_v3_\{$run\}.raw
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
