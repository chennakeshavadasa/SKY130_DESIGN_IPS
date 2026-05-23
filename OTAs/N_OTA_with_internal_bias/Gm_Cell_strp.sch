v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 160 -330 250 -330 {lab=VDD
}
N 290 -460 290 -440 {lab=VDD}
N 290 -380 290 -360 {lab=#net1}
N 250 -150 250 -90 {lab=VDD}
N 250 -210 250 -150 {lab=VDD}
N 250 -270 250 -210 {lab=VDD}
N 250 -330 250 -270 {lab=VDD}
N 250 -90 250 210 {lab=VDD}
C {sky130_fd_pr/nfet3_01v8.sym} 270 -330 0 0 {name=M12
W=0.5
L=10
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
C {vdd.sym} 290 -460 0 0 {name=l1 lab=VDD}
C {vsource.sym} 50 -110 0 0 {name=V1 value=1.8 savecurrent=false}
C {vdd.sym} 50 -140 0 0 {name=l2 lab=VDD}
C {gnd.sym} 50 -80 0 0 {name=l3 lab=0}
C {vdd.sym} 160 -330 0 0 {name=l4 lab=VDD}
C {devices/code_shown.sym} 770 -320 0 0 {name="NGSPICE" only_toplevel=true 
value="
.option wnflag=1
.option savecurrents
.temp 27
.control
save all
op
write Gm_Cell_strp.raw
set appendwrite 
**wrdata /foss/designs/SC_AMPs/Ideal_TB/SC-amp_try-2_OP_fft.txt mag(v(vout))
.endc
"}
C {title.sym} 160 340 0 0 {name=l6 author="Stefan Schippers"}
C {devices/code.sym} 1040 -310 0 0 {name=SAVE_COMM only_toplevel=true 
value="

.save @m.xm12.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm12.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm12.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm12.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm12.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm12.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm12.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm1.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm1.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm1.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm1.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm1.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm1.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm1.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm2.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm2.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm2.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm2.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm2.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm2.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm2.msky130_fd_pr__nfet_01v8[cgdo]
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
.save @m.xm5.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm5.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm5.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm5.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm5.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm5.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm5.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm6.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm6.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm6.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm6.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm6.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm6.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm6.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm7.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm7.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm7.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm7.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm7.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm7.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm7.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm8.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm8.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm8.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm8.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm8.msky130_fd_pr__nfet_01v8[cgdo]
.save @m.xm9.msky130_fd_pr__nfet_01v8[gm]
.save @m.xm9.msky130_fd_pr__nfet_01v8[gds]
.save @m.xm9.msky130_fd_pr__nfet_01v8[vth]
.save @m.xm9.msky130_fd_pr__nfet_01v8[vdsat]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgg]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgso]
.save @m.xm9.msky130_fd_pr__nfet_01v8[cgdo]
"}
C {sky130_fd_pr/corner.sym} 1190 -310 0 0 {name=CORNER only_toplevel=true corner=ff}
C {ammeter.sym} 290 -410 0 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {devices/launcher.sym} 1410 -290 0 0 {name=h15
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {sky130_fd_pr/nfet3_01v8.sym} 270 -270 0 0 {name=M1
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 -210 0 0 {name=M2
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 -150 0 0 {name=M3
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 -90 0 0 {name=M4
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 -30 0 0 {name=M5
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 30 0 0 {name=M6
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 90 0 0 {name=M7
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 150 0 0 {name=M8
W=0.5
L=10
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
C {sky130_fd_pr/nfet3_01v8.sym} 270 210 0 0 {name=M9
W=0.5
L=10
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
C {gnd.sym} 290 240 0 0 {name=l5 lab=0}
