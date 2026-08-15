v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 210 -70 210 -30 {lab=VICM}
N 210 30 210 60 {lab=GNDA}
N 490 -220 490 -170 {lab=VDD}
N 30 -50 30 -10 {lab=VDD}
N 30 50 30 80 {lab=GNDA}
N -200 50 -200 80 {lab=0}
N -200 -40 -200 -10 {lab=GNDA}
N -110 50 -110 80 {lab=GNDA}
N -110 -40 -110 -10 {lab=EN}
N 470 -220 470 -170 {lab=EN}
N 490 -30 490 40 {lab=GNDA}
N 680 10 680 50 {lab=GNDA}
N 680 -100 680 -50 {lab=Vout}
N 550 -330 680 -330 {lab=Vout
}
N 210 -330 310 -330 {lab=#net1
}
N 370 -330 490 -330 {lab=probe
}
N 440 -520 440 -480 {lab=0
}
N 440 -420 440 -330 {lab=probe
}
N 280 -120 330 -120 {lab=#net1}
N 280 -80 330 -80 {lab=VICM}
N 680 -270 680 -100 {lab=Vout}
N 210 -270 210 -130 {lab=#net1}
N 210 -330 210 -270 {lab=#net1
}
N 680 -330 680 -270 {lab=Vout
}
N 210 -120 280 -120 {lab=#net1}
N 210 -130 210 -120 {lab=#net1}
N 210 -80 210 -70 {lab=VICM}
N 210 -80 280 -80 {lab=VICM}
N 470 -30 470 -20 {lab=#net2}
N 630 -100 690 -100 {lab=Vout}
N 690 -100 740 -100 {lab=Vout}
C {vdd.sym} 490 -220 0 0 {name=l3 lab=VDD}
C {vdd.sym} 30 -50 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} 740 -100 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {vsource.sym} -200 20 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} -200 80 0 0 {name=l6 lab=0}
C {lab_pin.sym} -200 -40 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} 20 -230 0 0 {name=SAVE_COMM only_toplevel=false value="

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
C {vsource.sym} -110 20 0 0 {name=V5 value=1.8 savecurrent=false}
C {lab_pin.sym} -110 -40 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code.sym} -110 -230 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
place=header}
C {devices/launcher.sym} -20 -310 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {capa.sym} 680 -20 0 0 {name=C1
m=1
value=10p
footprint=1206
device="ceramic capacitor"}
C {title.sym} -230 140 0 0 {name=l11 author="Nithin Purushothama"}
C {lab_pin.sym} 210 -80 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {vsource.sym} 520 -330 3 0 {name=Vprobe1 value="dc 0 ac 1" savecurrent=false
}
C {vsource.sym} 340 -330 1 0 {name=Vprobe2 value=0 savecurrent=false
}
C {isource.sym} 440 -450 0 0 {name=Iprobe1 value="dc 0 ac 1"
}
C {gnd.sym} 440 -520 2 0 {name=l7 lab=0
}
C {devices/code.sym} 70 -500 0 0 {name=STB_SIMS only_toplevel=true 
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
 ac dec 20 1 1e8
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
 **show m : gm : gmbs : gds : vds : vdsat : vgs : vth : id
.endc"
}
C {lab_pin.sym} 440 -330 3 0 {name=p4 sig_type=std_logic lab=probe
}
C {devices/launcher.sym} -20 -350 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {lab_pin.sym} 470 -220 0 0 {name=p5 sig_type=std_logic lab=EN }
C {vsource.sym} 210 0 0 0 {name=V2 value="dc 0.9 sin(0.9 0.65 1k)" savecurrent=false}
C {vsource.sym} 30 20 0 0 {name=V4 value="dc 1.8 ac 1" savecurrent=false}
C {lab_pin.sym} 490 40 0 1 {name=p2 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -110 80 0 0 {name=p6 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 30 80 0 0 {name=p7 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 210 60 0 0 {name=p8 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 680 50 0 0 {name=p11 sig_type=std_logic lab=GNDA}
C {capa.sym} 470 10 0 1 {name=C2
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 470 40 0 0 {name=p12 sig_type=std_logic lab=GNDA}
C {ngspice_probe.sym} 470 -20 0 1 {name=r1}
C {/home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_OTA_Inp_IP/Single_ended/With_internal_Bias/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sym} 480 -100 0 0 {name=x2}
