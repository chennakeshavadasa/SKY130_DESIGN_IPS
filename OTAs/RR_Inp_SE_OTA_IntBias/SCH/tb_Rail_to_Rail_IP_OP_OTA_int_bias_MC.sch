v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 400 260 400 300 {lab=VICM}
N 400 360 400 390 {lab=GNDA}
N 680 110 680 160 {lab=VDD}
N 220 280 220 320 {lab=VDD}
N 220 380 220 410 {lab=GNDA}
N -10 380 -10 410 {lab=0}
N -10 290 -10 320 {lab=GNDA}
N 80 380 80 410 {lab=GNDA}
N 80 290 80 320 {lab=EN}
N 660 110 660 160 {lab=EN}
N 680 300 680 370 {lab=GNDA}
N 870 340 870 380 {lab=GNDA}
N 870 230 870 280 {lab=Vout}
N 470 210 520 210 {lab=Vout}
N 470 250 520 250 {lab=VICM}
N 870 60 870 230 {lab=Vout}
N 400 60 400 200 {lab=Vout}
N 400 0 400 60 {lab=Vout
}
N 870 0 870 60 {lab=Vout
}
N 400 210 470 210 {lab=Vout}
N 400 200 400 210 {lab=Vout}
N 400 250 400 260 {lab=VICM}
N 400 250 470 250 {lab=VICM}
N 660 300 660 310 {lab=#net1}
N 820 230 880 230 {lab=Vout}
N 880 230 930 230 {lab=Vout}
N 400 0 870 0 {lab=Vout}
C {vdd.sym} 680 110 0 0 {name=l3 lab=VDD}
C {vdd.sym} 220 280 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 930 230 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {vsource.sym} -10 350 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} -10 410 0 0 {name=l6 lab=0}
C {lab_pin.sym} -10 290 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} 210 100 0 0 {name=SAVE_COMM only_toplevel=false value="

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
C {vsource.sym} 80 350 0 0 {name=V5 value=1.8 savecurrent=false}
C {lab_pin.sym} 80 290 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code.sym} 80 100 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
place=header}
C {devices/launcher.sym} 170 20 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {capa.sym} 870 310 0 0 {name=C1
m=1
value=10p
footprint=1206
device="ceramic capacitor"}
C {title.sym} -40 470 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} 120 -170 0 0 {name=MC_SIMS only_toplevel=true 
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
   wrdata /home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_Inp_IP/Single_ended/With_internal_Bias/tb_Rail_to_Rail_IP_OP_OTA_int_bias_MC.txt r v(DIFF_MIS)
   wrdata /home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_Inp_IP/Single_ended/With_internal_Bias/tb_Rail_to_Rail_IP_OP_OTA_int_bias_MC.txt r v(DIFF_MIS)

   let r = r + 1
 end
.endc"
}
C {lab_pin.sym} 400 250 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {devices/launcher.sym} 170 -20 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {lab_pin.sym} 660 110 0 0 {name=p5 sig_type=std_logic lab=EN }
C {vsource.sym} 400 330 0 0 {name=V2 value=0.9 savecurrent=false}
C {vsource.sym} 220 350 0 0 {name=V4 value="dc 1.8 ac 1" savecurrent=false}
C {lab_pin.sym} 680 370 0 1 {name=p2 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 80 410 0 0 {name=p6 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 220 410 0 0 {name=p7 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 400 390 0 0 {name=p8 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 870 380 0 0 {name=p11 sig_type=std_logic lab=GNDA}
C {capa.sym} 660 340 0 1 {name=C2
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 660 370 0 0 {name=p12 sig_type=std_logic lab=GNDA}
C {ngspice_probe.sym} 660 310 0 1 {name=r1}
C {/home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_OTA_Inp_IP/Single_ended/With_internal_Bias/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sym} 670 230 0 0 {name=x2}
