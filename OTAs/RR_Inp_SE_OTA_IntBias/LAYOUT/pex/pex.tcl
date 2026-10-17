set cell Rail_to_Rail_IP_OP_OTA_with_Intrenal_Bias
load $cell
select top cell
# ---- C-only (coupling caps) ----
extract do capacitance
extract do coupling
extract all
ext2spice lvs
ext2spice format ngspice
ext2spice cthresh 0
ext2spice -o ${cell}_cx.spice
# ---- full RC (extresist) ----
extract do resistance
extract all
ext2sim labels on
ext2sim
extresist tolerance 10
extresist all
ext2spice lvs
ext2spice cthresh 0
ext2spice rthresh 0
ext2spice extresist on
ext2spice -o ${cell}_rcx.spice
# ---- antenna ----
extract do antenna
extract all
antennacheck
quit -noprompt
