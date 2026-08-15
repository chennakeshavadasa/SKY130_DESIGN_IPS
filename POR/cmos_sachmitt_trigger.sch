v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 0 -140 160 -140 {lab=#net1}
N 0 -140 -0 -100 {lab=#net1}
N -0 -180 -0 -140 {lab=#net1}
N 0 -40 -0 -0 {lab=0}
N 0 -410 160 -410 {lab=#net2}
N -0 -410 -0 -380 {lab=#net2}
N 0 -430 -0 -410 {lab=#net2}
N 0 -320 0 -240 {lab=VOUT}
N 190 -370 190 -180 {lab=VOUT}
N 0 -280 190 -280 {lab=VOUT}
N 190 -280 350 -280 {lab=VOUT}
N -90 -70 -40 -70 {lab=VIN}
N -90 -210 -90 -70 {lab=VIN}
N -90 -210 -40 -210 {lab=VIN}
N -90 -350 -90 -210 {lab=VIN}
N -90 -350 -40 -350 {lab=VIN}
N -90 -460 -90 -350 {lab=VIN}
N -90 -460 -40 -460 {lab=VIN}
N 0 -530 0 -490 {lab=VDD}
N -140 -280 -90 -280 {lab=VIN}
N 220 -410 290 -410 {lab=0}
N 220 -140 290 -140 {lab=VDD}
N -350 -120 -350 -90 {lab=0}
N -350 -210 -350 -180 {lab=VDD}
N -410 -120 -410 -90 {lab=0}
N -410 -210 -410 -180 {lab=VIN}
C {sky130_fd_pr/nfet3_01v8.sym} -20 -70 0 0 {name=M1
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
C {sky130_fd_pr/nfet3_01v8.sym} -20 -210 0 0 {name=M2
W=5
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
C {sky130_fd_pr/nfet3_01v8.sym} 190 -160 1 0 {name=M3
W=30
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
C {sky130_fd_pr/pfet3_01v8.sym} -20 -350 0 0 {name=M4
W=20
L=0.15
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
C {sky130_fd_pr/pfet3_01v8.sym} -20 -460 0 0 {name=M5
W=5
L=0.15
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
C {sky130_fd_pr/pfet3_01v8.sym} 190 -390 1 1 {name=M6
W=1
L=0.15
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
C {vdd.sym} 0 -530 0 0 {name=l1 lab=VDD}
C {gnd.sym} 0 0 0 0 {name=l2 lab=0}
C {lab_pin.sym} -140 -280 0 0 {name=p1 sig_type=std_logic lab=VIN}
C {lab_pin.sym} 350 -280 2 0 {name=p2 sig_type=std_logic lab=VOUT}
C {gnd.sym} 290 -410 0 0 {name=l3 lab=0}
C {vdd.sym} 290 -140 0 0 {name=l4 lab=VDD}
C {vsource.sym} -350 -150 0 0 {name=V2 value=1.8 savecurrent=false}
C {gnd.sym} -350 -90 0 0 {name=l5 lab=0}
C {vdd.sym} -350 -210 0 0 {name=l6 lab=VDD}
C {vsource.sym} -410 -150 0 0 {name=V1 value=0.9 savecurrent=false}
C {gnd.sym} -410 -90 0 0 {name=l7 lab=0}
C {lab_pin.sym} -410 -210 0 0 {name=p3 sig_type=std_logic lab=VIN}
C {devices/code_shown.sym} -740 -400 0 0 {name="DC_OP_SIMS" only_toplevel=true 
value="
.option wnflag=1
.option savecurrents
.temp 27
.control
save all
op
write cmos_schmitt_trigger.raw
set appendwrite 
dc V1 0 1.8 1m 
plot v(VOUT) vs v(VIN)
plot Idiff
write cmos_schmitt_trigger.raw
.endc
"
}
C {code.sym} -330 -420 0 0 {
name=TT_MODELS
only_toplevel=true
format="tcleval( @value )"
value="
** opencircuitdesign pdks install
.lib $::SKYWATER_MODELS/sky130.lib.spice tt
"
spice_ignore=false
      }
