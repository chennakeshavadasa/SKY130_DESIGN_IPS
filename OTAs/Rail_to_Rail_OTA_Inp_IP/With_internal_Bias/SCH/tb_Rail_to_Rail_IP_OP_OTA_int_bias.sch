v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -820 -50 -820 -10 {lab=VICM}
N -820 50 -820 80 {lab=GNDA}
N -540 -200 -540 -150 {lab=VDD}
N -1000 -30 -1000 10 {lab=VDD}
N -1000 70 -1000 100 {lab=GNDA}
N -1230 70 -1230 100 {lab=0}
N -1230 -20 -1230 10 {lab=GNDA}
N -1140 70 -1140 100 {lab=GNDA}
N -1140 -20 -1140 10 {lab=EN}
N -560 -200 -560 -150 {lab=EN}
N -540 -10 -540 60 {lab=GNDA}
N -350 30 -350 70 {lab=GNDA}
N -350 -80 -350 -30 {lab=Vout}
N -480 -310 -350 -310 {lab=Vout
spice_ignore=true}
N -820 -310 -720 -310 {lab=#net1
spice_ignore=true}
N -660 -310 -540 -310 {lab=probe
spice_ignore=true}
N -590 -500 -590 -460 {lab=0
spice_ignore=true}
N -590 -400 -590 -310 {lab=probe
spice_ignore=true}
N -750 -100 -700 -100 {lab=Vout}
N -750 -60 -700 -60 {lab=VICM}
N -820 -250 -350 -250 {lab=Vout
}
N -350 -250 -350 -80 {lab=Vout}
N -820 -250 -820 -110 {lab=Vout}
N -820 -310 -820 -250 {lab=Vout
}
N -350 -310 -350 -250 {lab=Vout
spice_ignore=true}
N -820 -100 -750 -100 {lab=Vout}
N -820 -110 -820 -100 {lab=Vout}
N -820 -60 -820 -50 {lab=VICM}
N -820 -60 -750 -60 {lab=VICM}
N -560 -10 -560 0 {lab=#net1}
N -400 -80 -340 -80 {lab=Vout}
N -340 -80 -290 -80 {lab=Vout}
C {vdd.sym} -540 -200 0 0 {name=l3 lab=VDD}
C {vdd.sym} -1000 -30 0 0 {name=l5 lab=VDD}
C {lab_pin.sym} -290 -80 2 0 {name=p1 sig_type=std_logic lab=Vout}
C {vsource.sym} -1230 40 0 0 {name=V3 value=0 savecurrent=false}
C {gnd.sym} -1230 100 0 0 {name=l6 lab=0}
C {lab_pin.sym} -1230 -20 0 0 {name=p9 sig_type=std_logic lab=GNDA}
C {code.sym} -1010 -210 0 0 {name=SAVE_COMM only_toplevel=false value="

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
C {vsource.sym} -1140 40 0 0 {name=V5 value=1.8 savecurrent=false}
C {lab_pin.sym} -1140 -20 0 0 {name=p10 sig_type=std_logic lab=EN }
C {devices/code_shown.sym} -1590 -540 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.param A=10k Vos=0 VDD=1.8 VSS=0 
.option wnflag=1 gmin=1e-18
.option savecurrents
.temp 27
.control
save all
op
write tb_Rail_to_Rail_IP_OP_OTA_int_bias.raw
set appendwrite 
**Plotting How Vout follows VICM in DC
dc v2 0 1.8 10m
write tb_Rail_to_Rail_IP_OP_OTA_int_bias.raw
set appendwrite 
plot v(Vout) v(VICM)
plot v(Vout)-v(VICM)
**Plotting PSRR
ac dec 20 1 1e12 
write tb_Rail_to_Rail_IP_OP_OTA_int_bias.raw
plot vdb(Vout)
**Plotting Transient
tran 100u 10m 0.01m 
write tb_Rail_to_Rail_IP_OP_OTA_int_bias.raw
plot v(Vout) v(VICM) v(Vout)-v(VICM)
plot v(Vout)-v(VICM)
.endc
"
}
C {devices/code.sym} -1140 -210 0 0 {name=TT_MODELS
only_toplevel=true
format="tcleval(@value )"
value=".lib $::SKYWATER_MODELS/sky130.lib.spice tt
.include $::SKYWATER_STDCELLS/sky130_fd_sc_hd.spice
"
place=header}
C {devices/launcher.sym} -1050 -290 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {capa.sym} -350 0 0 0 {name=C1
m=1
value=10p
footprint=1206
device="ceramic capacitor"}
C {title.sym} -1260 160 0 0 {name=l11 author="Nithin Purushothama"}
C {devices/code.sym} -1100 -480 0 0 {name=MC_SIMS only_toplevel=true 
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
C {lab_pin.sym} -820 -60 0 0 {name=p3 sig_type=std_logic lab=VICM}
C {vsource.sym} -510 -310 3 0 {name=Vprobe1 value="dc 0 ac 1" savecurrent=false
spice_ignore=true}
C {vsource.sym} -690 -310 1 0 {name=Vprobe2 value=0 savecurrent=false
spice_ignore=true}
C {isource.sym} -590 -430 0 0 {name=Iprobe1 value="dc 0 ac 1"
spice_ignore=true}
C {gnd.sym} -590 -500 2 0 {name=l7 lab=0
spice_ignore=true}
C {devices/code.sym} -960 -480 0 0 {name=STB_SIMS only_toplevel=true 
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
C {lab_pin.sym} -590 -310 3 0 {name=p4 sig_type=std_logic lab=probe
spice_ignore=true}
C {devices/launcher.sym} -1050 -330 0 0 {name=h17 
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file tail [file rootname [xschem get current_name]]].raw tran
"
}
C {lab_pin.sym} -560 -200 0 0 {name=p5 sig_type=std_logic lab=EN }
C {vsource.sym} -820 20 0 0 {name=V2 value="dc 0.9 sin(0.9 0.65 1k)" savecurrent=false}
C {vsource.sym} -1000 40 0 0 {name=V4 value="dc 1.8 ac 1" savecurrent=false}
C {lab_pin.sym} -540 60 0 1 {name=p2 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -1140 100 0 0 {name=p6 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -1000 100 0 0 {name=p7 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -820 80 0 0 {name=p8 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} -350 70 0 0 {name=p11 sig_type=std_logic lab=GNDA}
C {capa.sym} -560 30 0 1 {name=C2
m=1
value=1p
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} -560 60 0 0 {name=p12 sig_type=std_logic lab=GNDA}
C {ngspice_probe.sym} -560 0 0 1 {name=r1}
C {/home/nithin/eda/SKY130_DESIGN_IPS/OTAs/Rail_to_Rail_OTA_Inp_IP/Single_ended/With_internal_Bias/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sym} -550 -80 0 0 {name=x2}
