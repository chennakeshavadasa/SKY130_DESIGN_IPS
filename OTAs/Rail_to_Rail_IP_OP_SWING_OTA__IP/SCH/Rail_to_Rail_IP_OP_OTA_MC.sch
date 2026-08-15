v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -460 -240 -460 -200 {lab=VICM}
N -460 -140 -460 -110 {lab=0}
N -250 -390 -250 -340 {lab=VDD}
N -640 -220 -640 -180 {lab=VDD}
N -640 -120 -640 -90 {lab=0}
N -870 -120 -870 -90 {lab=0}
N -870 -210 -870 -180 {lab=GNDA}
N -780 -120 -780 -90 {lab=0}
N -780 -210 -780 -180 {lab=EN}
N -460 -300 -380 -300 {lab=Vout}
N -460 -240 -380 -240 {lab=VICM}
N -230 -380 -230 -330 {lab=EN}
N -80 -270 10 -270 {lab=Vout}
N -240 -200 -240 -130 {lab=0}
N 10 -270 70 -270 {lab=Vout}
N 10 -160 10 -120 {lab=0}
N 10 -270 10 -220 {lab=Vout}
N -380 -300 -330 -300 {lab=Vout}
N -380 -240 -330 -240 {lab=VICM}
N -130 -270 -80 -270 {lab=Vout}
N -460 -440 10 -440 {lab=Vout
}
N 10 -440 10 -270 {lab=Vout}
N -460 -440 -460 -300 {lab=Vout}
C {gnd.sym} -240 -130 0 0 {name=l1 lab=0}
C {gnd.sym} -460 -110 0 0 {name=l2 lab=0}
C {vdd.sym} -250 -390 0 0 {name=l3 lab=VDD}
C {gnd.sym} -640 -90 0 0 {name=l4 lab=0}
C {vdd.sym} -640 -220 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 70 -270 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {vsource.sym} -870 -150 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} -870 -90 0 0 {name=l6 lab=0}
C {lab_pin.sym} -870 -210 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} -650 -400 0 0 {name=SAVE_COMM only_toplevel=false value="

.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_bot_l2.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_l2.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_bot_l1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_l1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_l2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_l1.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_top_l1.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.x1.xmn_a1.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[gm]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[gds]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[vth]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[vdsat]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[cgg]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[cgso]
.save @m.x1.xmn_a2.msky130_fd_pr__nfet_01v8_lvt[cgdo]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[gm]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[gds]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[vth]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[vdsat]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[cgg]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[cgso]
.save @m.x1.xmp_a1.msky130_fd_pr__pfet_01v8_lvt[cgdo]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[gm]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[gds]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[vth]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[vdsat]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[cgg]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[cgso]
.save @m.x1.xmp_a2.msky130_fd_pr__pfet_01v8_lvt[cgdo]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_pdiff_bias.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_ndiff_bias.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_pdiff_bias_b.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_top_l2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_bias_source.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_bias_ext.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_b_source.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias8.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_b_source.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_bias1.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias7.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias6.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_bias2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_casc_bias3.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias5.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias4.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias3.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_casc_bias2.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_sw1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_sw1.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_sw2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[gm]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[gds]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[vth]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[cgg]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[cgso]
.save @m.x1.xmn_sw2.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[gm]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[gds]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[vth]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[cgg]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[cgso]
.save @m.x1.xmp_sw3.msky130_fd_pr__pfet_01v8[cgdo]
"}
C {vsource.sym} -780 -150 0 0 {name=V5 value=1.8 savecurrent=false}
C {gnd.sym} -780 -90 0 0 {name=l8 lab=0}
C {lab_pin.sym} -780 -210 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code.sym} -780 -400 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
place=header}
C {devices/launcher.sym} -690 -480 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {capa.sym} 10 -190 0 0 {name=C1
m=1
value=10p
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 10 -120 0 0 {name=l10 lab=0}
C {title.sym} -900 -30 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} -920 -390 0 0 {name=MC_SIMS only_toplevel=true 
value="
.option gmin=1e-18
.options savecurrents
.save all
.temp=27
.control
 let runs=200
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
}
C {lab_pin.sym} -460 -240 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {devices/launcher.sym} -690 -520 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {lab_pin.sym} -230 -380 0 1 {name=p5 sig_type=std_logic lab=EN }
C {/home/nithin/eda/SKYWATER_DESIGN_IPS/OTAs/Rail_to_Rail_IP_OP_OTA.sym} -600 -270 0 0 {name=x1}
C {vsource.sym} -460 -170 0 0 {name=V2 value="dc 0.9 sin(0.9 0.65 1k)" savecurrent=false}
C {vsource.sym} -640 -150 0 0 {name=V4 value="dc 1.8 ac 1" savecurrent=false}
