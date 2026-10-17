#!/bin/bash
# Netlist the (unmodified) schematic for LVS and for pre-layout simulation.
#   ota_lvs.spice : LVS-mode netlist (reference for lvs/run_lvs.sh)
#   ota_sim.spice : simulation netlist (keeps mult=, ad/as ...) -> sim/dut_sch.spice
# Usage: ./netlist.sh [path/to/SCH]   (default: ../../SCH, i.e. the IP's SCH folder in the repo)
cd "$(dirname "$0")"
export PDK_ROOT=${PDK_ROOT:-$HOME/.ciel} PDK=sky130A
SCH=${1:-../../SCH}/Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias.sch
cat > xschemrc <<RC
source \$env(PDK_ROOT)/\$env(PDK)/libs.tech/xschem/xschemrc
append XSCHEM_LIBRARY_PATH :[file dirname [file normalize $SCH]]
RC
timeout 120 xschem -n -s -q --no_x --rcfile xschemrc --tcl "set lvs_netlist 1; set top_subckt 1" -o "$PWD" -N ota_lvs.spice "$SCH" >/dev/null 2>&1
timeout 120 xschem -n -s -q --no_x --rcfile xschemrc --tcl "set top_subckt 1" -o "$PWD" -N ota_sim.spice "$SCH" >/dev/null 2>&1
grep -v "^\.end$" ota_sim.spice | sed 's/^\*\*\.subckt/.subckt/;s/^\*\*\.ends/.ends/' > ../sim/dut_sch.spice
echo "netlisted: $(grep -c '^X' ota_lvs.spice) devices (LVS), $(grep -c '^X' ../sim/dut_sch.spice) devices (sim)"
