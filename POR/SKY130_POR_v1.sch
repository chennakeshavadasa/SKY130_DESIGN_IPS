v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {~500nA} 720 -100 0 0 0.4 0.4 {}
T {~10u} 490 -100 0 0 0.4 0.4 {}
T {~500nA} 920 -100 0 0 0.4 0.4 {}
T {Vddmin=1.5
Vddnom=1.8} 560 -760 0 0 0.4 0.4 {}
T {gm/id=10
vov=0.157} 660 -980 0 0 0.2 0.2 {}
T {gm/id=10} 750 -780 0 0 0.2 0.2 {}
N 550 -1000 700 -1000 {lab=IBIAS_P}
N 510 -970 510 -840 {lab=IBIAS_P}
N 510 -930 580 -930 {lab=IBIAS_P}
N 580 -1000 580 -930 {lab=IBIAS_P}
N 510 -1100 510 -1030 {lab=VDDA}
N 510 -1100 740 -1100 {lab=VDDA}
N 740 -1100 740 -1030 {lab=VDDA}
N 740 -970 740 -840 {lab=IBIAS_N}
N 780 -810 900 -810 {lab=IBIAS_N}
N 820 -870 820 -810 {lab=IBIAS_N}
N 740 -870 820 -870 {lab=IBIAS_N}
N 940 -780 940 -740 {lab=#net1}
N 740 -780 740 -600 {lab=GNDA}
N 700 -1000 900 -1000 {lab=IBIAS_P}
N 940 -1100 940 -1030 {lab=VDDA}
N 740 -1100 940 -1100 {lab=VDDA}
N 1310 -1100 1310 -1030 {lab=VDDA}
N 950 -1100 1180 -1100 {lab=VDDA}
N 940 -1100 950 -1100 {lab=VDDA}
N 1310 -970 1310 -840 {lab=#net2}
N 1230 -1000 1270 -1000 {lab=V_DECISION}
N 1230 -1000 1230 -810 {lab=V_DECISION}
N 1230 -810 1270 -810 {lab=V_DECISION}
N 940 -910 1100 -910 {lab=V_DECISION}
N 1310 -780 1310 -610 {lab=GNDA}
N 1550 -1100 1550 -1030 {lab=VDDA}
N 1320 -1100 1550 -1100 {lab=VDDA}
N 1550 -970 1550 -840 {lab=V_POR}
N 1470 -1000 1510 -1000 {lab=#net2}
N 1470 -1000 1470 -810 {lab=#net2}
N 1470 -810 1510 -810 {lab=#net2}
N 1310 -910 1470 -910 {lab=#net2}
N 1550 -780 1550 -610 {lab=GNDA}
N 300 -150 300 -120 {lab=0}
N 50 -150 50 -120 {lab=0}
N 300 -240 300 -210 {lab=GNDA}
N 50 -240 50 -210 {lab=VDDA}
N 390 -980 390 -930 {lab=IBIAS_P}
N 390 -930 510 -930 {lab=IBIAS_P}
N 360 -1020 420 -1020 {lab=VDDA}
N 390 -1100 390 -1020 {lab=VDDA}
N 390 -1100 510 -1100 {lab=VDDA}
N 1070 -750 1130 -750 {lab=GNDA}
N 1100 -910 1100 -790 {lab=V_DECISION}
N 1100 -750 1100 -600 {lab=GNDA}
N 1100 -910 1230 -910 {lab=V_DECISION}
N 1180 -1100 1320 -1100 {lab=VDDA}
N 1550 -910 1610 -910 {lab=V_POR}
N 940 -850 940 -840 {lab=#net3}
N 960 -710 960 -650 {lab=GNDA}
N 960 -650 960 -590 {lab=GNDA}
N 960 -590 960 -530 {lab=GNDA}
N 960 -530 960 -470 {lab=GNDA}
N 960 -470 960 -410 {lab=GNDA}
N 960 -410 960 -350 {lab=GNDA}
N 960 -350 960 -290 {lab=GNDA}
N 960 -290 960 -230 {lab=GNDA}
N 960 -230 960 -170 {lab=GNDA}
N 960 -170 960 -110 {lab=GNDA}
N 940 -110 960 -110 {lab=GNDA}
N 940 -140 940 -110 {lab=GNDA}
N 530 -730 530 -670 {lab=GNDA}
N 530 -670 530 -610 {lab=GNDA}
N 530 -610 530 -550 {lab=GNDA}
N 530 -550 530 -490 {lab=GNDA}
N 530 -490 530 -430 {lab=GNDA}
N 520 -110 940 -110 {lab=GNDA}
N 510 -110 520 -110 {lab=GNDA}
N 510 -400 510 -110 {lab=GNDA}
N 530 -430 530 -110 {lab=GNDA}
N 530 -790 530 -730 {lab=GNDA}
N 740 -600 740 -110 {lab=GNDA}
N 1100 -600 1100 -120 {lab=GNDA}
N 1100 -120 1100 -110 {lab=GNDA}
N 960 -110 1100 -110 {lab=GNDA}
N 1310 -610 1310 -110 {lab=GNDA}
N 1100 -110 1310 -110 {lab=GNDA}
N 1550 -610 1550 -120 {lab=GNDA}
N 1550 -120 1550 -110 {lab=GNDA}
N 1310 -110 1550 -110 {lab=GNDA}
N 510 -840 510 -820 {lab=IBIAS_P}
N 450 -110 510 -110 {lab=GNDA}
C {sky130_fd_pr/pfet3_01v8.sym} 530 -1000 0 1 {name=M1
W=1.5
L=1
body=VDD
nf=1
mult=10
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet3_01v8.sym} 720 -1000 0 0 {name=M2
W=1.5
L=1
body=VDD
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8.sym} 760 -810 0 1 {name=M3
W=0.5
L=2
body=GND
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8.sym} 920 -810 0 0 {name=M4
W=0.5
L=2
body=GND
nf=1
mult=4
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet3_01v8.sym} 920 -1000 0 0 {name=M5
W=1.5
L=1
body=VDD
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet3_01v8.sym} 1290 -1000 0 0 {name=M6
W=1
L=0.15
body=VDD
nf=1
mult=3
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8.sym} 1290 -810 0 0 {name=M8
W=1
L=0.15
body=GND
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/pfet3_01v8.sym} 1530 -1000 0 0 {name=M7
W=1
L=0.15
body=VDD
nf=1
mult=3
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8.sym} 1530 -810 0 0 {name=M9
W=1
L=0.15
body=GND
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {vsource.sym} 50 -180 0 0 {name=V1 value="dc 1.5 PWL(0 0 10u 0v 100u 1.8 150u 1.8)" savecurrent=false}
C {vsource.sym} 300 -180 0 0 {name=V2 value=0 savecurrent=false}
C {gnd.sym} 300 -120 0 0 {name=l1 lab=0}
C {gnd.sym} 50 -120 0 0 {name=l2 lab=0}
C {lab_pin.sym} 50 -240 0 0 {name=p1 sig_type=std_logic lab=VDDA}
C {lab_pin.sym} 300 -240 2 0 {name=p2 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 450 -110 0 0 {name=p3 sig_type=std_logic lab=GNDA}
C {lab_pin.sym} 390 -1100 0 0 {name=p4 sig_type=std_logic lab=VDDA}
C {lab_pin.sym} 580 -930 2 0 {name=p5 sig_type=std_logic lab=IBIAS_P}
C {lab_pin.sym} 740 -880 0 0 {name=p6 sig_type=std_logic lab=IBIAS_N}
C {sky130_fd_pr/pfet3_01v8.sym} 390 -1000 3 0 {name=M10
W=1
L=1
body=VDD
nf=1
mult=10
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {sky130_fd_pr/nfet3_01v8.sym} 1100 -770 1 0 {name=M11
W=1
L=1
body=GND
nf=1
mult=10
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {lab_pin.sym} 1100 -910 1 0 {name=p7 sig_type=std_logic lab=V_DECISION}
C {lab_pin.sym} 1610 -910 2 0 {name=p8 sig_type=std_logic lab=V_POR}
C {devices/code.sym} 0 -660 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.option wnflag=1 gmin=1e-18
.option savecurrents
.temp 27
.control
save all
op
write SKY130_POR_v1.raw
set appendwrite 
tran 0.1u 150u uic
let Idiff= vmeas#branch-vmeas1#branch
plot v(V_POR) v(V_DECISION) v(VDDA)
plot v(V_POR) vs v(VDDA)
plot v(V_DECISION) vs v(VDDA)
plot vmeas#branch vmeas1#branch
plot Idiff
**wrdata /home/nithin/eda/SKY130_DEAIGN_IPS/POR/SKY130_POR_v1.txt v(V_POR) v(V_DECISION) v(VDDA) vmeas#branch vmeas1#branch 
write SKY130_POR_v1.raw
.endc
"
}
C {devices/code.sym} 10 -490 0 0 {name=SAVE_COMM only_toplevel=true 
value="

.save @m.xm1.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm1.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm1.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm1.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm1.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm1.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm1.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm2.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm2.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm2.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm2.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm2.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm2.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm2.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm3.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm3.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm3.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm3.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm3.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm3.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm3.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm4.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm4.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm4.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm4.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm4.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm4.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm4.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm5.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm5.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm5.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm5.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm5.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm5.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm5.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm6.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm6.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm6.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm6.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm6.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm6.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm6.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm8.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm8.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm8.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm8.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm7.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm7.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm7.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm7.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm7.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm7.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm7.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm9.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm9.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm9.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm9.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm10.msky130_fd_pr__pfet_01v8[gm]
.save @m.xm10.msky130_fd_pr__pfet_01v8[gds]
.save @m.xm10.msky130_fd_pr__pfet_01v8[vth]
.save @m.xm10.msky130_fd_pr__pfet_01v8[vdsat]
.save @m.xm10.msky130_fd_pr__pfet_01v8[cgg]
.save @m.xm10.msky130_fd_pr__pfet_01v8[cgso]
.save @m.xm10.msky130_fd_pr__pfet_01v8[cgdo]
.save @m.xm11.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm11.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm11.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm11.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm11.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm11.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm11.msky130_fd_pr__nfet_01v8[cgdo]
"
}
C {ammeter.sym} 940 -940 0 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {ammeter.sym} 940 -880 0 0 {name=Vmeas1 savecurrent=true spice_ignore=0}
C {code.sym} 140 -660 0 0 {
name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
** opencircuitdesign pdks install
.lib $::SKYWATER_MODELS/sky130.lib.spice fs
"
spice_ignore=false
      }
C {devices/launcher.sym} 120 -70 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {title.sym} 160 0 0 0 {name=l3 author="Nithin Purusthama"}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -710 0 1 {name=R3
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -650 0 1 {name=R2
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -590 0 1 {name=R4
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -530 0 1 {name=R5
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -470 0 1 {name=R6
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -410 0 1 {name=R7
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -350 0 1 {name=R8
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -290 0 1 {name=R9
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -230 0 1 {name=R10
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 940 -170 0 1 {name=R11
L=1.75
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -790 0 1 {name=R12
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -730 0 1 {name=R1
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -670 0 1 {name=R13
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -610 0 1 {name=R14
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -550 0 1 {name=R15
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -490 0 1 {name=R16
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
C {sky130_fd_pr/res_xhigh_po_0p35.sym} 510 -430 0 1 {name=R17
L=2
model=res_xhigh_po_0p35
spiceprefix=X
mult=1}
