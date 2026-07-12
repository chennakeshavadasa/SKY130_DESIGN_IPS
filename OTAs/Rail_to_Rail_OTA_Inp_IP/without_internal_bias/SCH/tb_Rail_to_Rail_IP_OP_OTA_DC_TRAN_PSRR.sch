v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -460 -240 -460 -200 {lab=VICM}
N -460 -140 -460 -110 {lab=GNDA}
N -250 -390 -250 -340 {lab=VDD}
N -640 -220 -640 -180 {lab=VDD}
N -640 -120 -640 -90 {lab=GNDA}
N -870 -120 -870 -90 {lab=0}
N -870 -210 -870 -180 {lab=GNDA}
N -780 -120 -780 -90 {lab=GNDA}
N -780 -210 -780 -180 {lab=EN}
N -460 -300 -380 -300 {lab=Vout}
N -460 -240 -380 -240 {lab=VICM}
N -230 -380 -230 -330 {lab=EN}
N -80 -270 10 -270 {lab=Vout}
N -240 -200 -240 -130 {lab=GNDA}
N 10 -270 70 -270 {lab=Vout}
N 10 -160 10 -120 {lab=GNDA}
N 10 -270 10 -220 {lab=Vout}
N -120 -500 10 -500 {lab=Vout
spice_ignore=true}
N -460 -500 -360 -500 {lab=#net1
spice_ignore=true}
N -300 -500 -180 -500 {lab=probe
spice_ignore=true}
N -230 -690 -230 -650 {lab=0
spice_ignore=true}
N -230 -590 -230 -500 {lab=probe
spice_ignore=true}
N -380 -300 -330 -300 {lab=Vout}
N -380 -240 -330 -240 {lab=VICM}
N -130 -270 -80 -270 {lab=Vout}
N -460 -440 10 -440 {lab=Vout
}
N 10 -440 10 -270 {lab=Vout}
N -460 -440 -460 -300 {lab=Vout}
N -460 -500 -460 -440 {lab=Vout
}
N 10 -500 10 -440 {lab=Vout
spice_ignore=true}
C {vdd.sym} -250 -390 0 0 {name=l3 lab=VDD}
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
C {lab_pin.sym} -780 -210 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code_shown.sym} -1160 -700 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.param A=10k Vos=0 VDD=1.8 VSS=0 
.option wnflag=1 gmin=1e-18
.option savecurrents
.temp 27
.control
save all
op
write tb_Rail_to_Rail_IP_OP_OTA.raw
set appendwrite 
**Plotting How Vout follows VICM in DC
dc v2 0 1.8 10m
write tb_Rail_to_Rail_IP_OP_OTA.raw
set appendwrite 
plot v(Vout) v(VICM)
plot v(Vout)-v(VICM)
**Plotting PSRR
ac dec 20 1 1e12 
write tb_Rail_to_Rail_IP_OP_OTA.raw
plot vdb(Vout)
**Plotting Transient
tran 100u 10m 0.01m 
write tb_Rail_to_Rail_IP_OP_OTA.raw
plot v(Vout) v(VICM) v(Vout)-v(VICM)
plot v(Vout)-v(VICM)
.endc
"
}
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
C {title.sym} -900 -30 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} -740 -670 0 0 {name=MC_SIMS only_toplevel=true 
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
C {lab_pin.sym} -460 -240 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {vsource.sym} -150 -500 3 0 {name=Vprobe1 value="dc 0 ac 1" savecurrent=false
spice_ignore=true}
C {vsource.sym} -330 -500 1 0 {name=Vprobe2 value=0 savecurrent=false
spice_ignore=true}
C {isource.sym} -230 -620 0 0 {name=Iprobe1 value="dc 0 ac 1"
spice_ignore=true}
C {gnd.sym} -230 -690 2 0 {name=l7 lab=0
spice_ignore=true}
C {devices/code.sym} -600 -670 0 0 {name=STB_SIMS only_toplevel=true 
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
spice_ignore=true}
C {lab_pin.sym} -230 -500 3 0 {name=p4 sig_type=std_logic lab=probe
spice_ignore=true}
C {devices/launcher.sym} -690 -520 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {lab_pin.sym} -230 -380 0 1 {name=p5 sig_type=std_logic lab=EN }
C {vsource.sym} -460 -170 0 0 {name=V2 value="dc 0.9 sin(0.9 0.65 1k)" savecurrent=false}
C {vsource.sym} -640 -150 0 0 {name=V4 value="dc 1.8 ac 1" savecurrent=false}
C {/home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_OTA_IP/SCH/Rail_to_Rail_IP_OP_OTA.sym} -600 -270 0 0 {name=x2}
C {lab_pin.sym} -240 -130 0 0 {name=p2 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -780 -90 0 0 {name=p6 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -640 -90 0 0 {name=p7 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -460 -110 0 0 {name=p8 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 10 -120 0 0 {name=p11 sig_type=std_logic lab=GNDA}
