#!/bin/bash
# LVS: magic-extracted layout vs xschem netlist of the untouched schematic.
# The schematic ties NMOS bodies to the global GND; in silicon the p-substrate is
# the GNDA net (all p-taps), so the reference maps body GND -> GNDA.
cd "$(dirname "$0")"
CELL=Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias
sed -E 's/ GND (sky130_fd_pr__nfet)/ GNDA \1/' ../xschem/ota_lvs.spice | grep -v "^\.save" > ref.spice
cp ../mag/$CELL.lvs.spice layout.spice
netgen -batch lvs "layout.spice $CELL" "ref.spice $CELL" \
   ${PDK_ROOT:-$HOME/.ciel}/sky130A/libs.tech/netgen/sky130A_setup.tcl lvs_report.txt > netgen.log 2>&1
grep -E "Final result" lvs_report.txt | tail -1
