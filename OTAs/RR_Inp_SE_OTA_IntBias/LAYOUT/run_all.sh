#!/bin/bash
# Full flow: generate layout -> magic DRC -> KLayout DRC -> LVS -> PEX -> pre/post-layout sims
set -e
cd "$(dirname "$0")"
export PDK_ROOT=${PDK_ROOT:-$HOME/.ciel} PDK=sky130A
CELL=Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias
echo "== generate + magic DRC + extract";  python3 scripts/gen_ota.py
echo "== KLayout sky130 DRC deck"
(cd drc && klayout -b -rd input=$PWD/../mag/$CELL.gds -rd top_cell=$CELL -rd report=$PWD/klayout_drc.lyrdb \
   -rd feol=true -rd beol=true -rd offgrid=true -r $PDK_ROOT/sky130A/libs.tech/klayout/drc/sky130A_mr.drc > klayout_drc.log 2>&1)
python3 -c "import xml.etree.ElementTree as E; r=E.parse('drc/klayout_drc.lyrdb').getroot(); print('KLayout DRC violations:', len(list(r.iter('item'))))"
echo "== LVS";  ./lvs/run_lvs.sh
echo "== PEX"
(cd pex && cp ../mag/$CELL.mag . && magic -dnull -noconsole -rcfile $PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc pex.tcl < /dev/null > pex.log 2>&1)
grep -i "antenna" pex/pex.log | tail -2
echo "== simulations"; (cd sim && python3 run_sims.py ${NMC:-200} | tee summary.txt)
