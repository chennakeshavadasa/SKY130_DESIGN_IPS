#!/usr/bin/env bash
# ============================================================
# OTAs directory reorganisation
# Run from the SKY130_DESIGN_IPS repo root:
#   bash reorganise_otas.sh
# ============================================================
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
echo "Repo root: $(pwd)"

# ============================================================
# 1. NMOS_SrcDeg_SE_OTA_IntBias
#    was: OTAs/N_OTA_with_internal_bias  (flat dump — no sub-dirs)
# ============================================================
echo ""
echo "── Step 1: N_OTA → NMOS_SrcDeg_SE_OTA_IntBias ──────────────"

git mv "OTAs/N_OTA_with_internal_bias" \
       "OTAs/NMOS_SrcDeg_SE_OTA_IntBias"

mkdir -p "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/SCH"
mkdir -p "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/Sims"

# Move schematics + symbols + PDF into SCH/
for f in \
  "Gm_Cell_strp.sch" \
  "Gm_STRP_N_BOT.sch" "Gm_STRP_N_BOT.sym" \
  "OTA_Gm_Cell.sch" \
  "OTA_Gm_Cell_v2.sch" "OTA_Gm_Cell_v2.sym" "OTA_Gm_Cell_v2.pdf" \
  "OTA_Gm_Cell_v3.sch" "OTA_Gm_Cell_v3.sym" \
  "Res_70K.sch" "Res_70K.sym" \
  "tb_Gm_Cell_v2.sch" "tb_Gm_Cell_v2.png" \
  "tb_Gm_Cell_v3.sch"; do
  [[ -f "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/$f" ]] && \
    git mv "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/$f" \
           "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/SCH/$f"
done

# Move simulation raw data + result plots into Sims/
for f in \
  "tb_Gm_Cell_v2_MC_Sims_TB.raw" \
  "tb_Gm_Cell_v2_MC_Sims_TB.txt" \
  "tb_Gm_Cell_v2_STB_.raw" \
  "mc_hist_mismatch.png" \
  "mc_hist_vos.html" \
  "mc_hist_vos.png" \
  "mc_scatter_vos.png" \
  "newplot.png"; do
  [[ -f "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/$f" ]] && \
    git mv "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/$f" \
           "OTAs/NMOS_SrcDeg_SE_OTA_IntBias/Sims/$f"
done
# GM_CELL_OTA_MC_SIMS.ipynb stays at root (analysis notebook)

echo "  Done."

# ============================================================
# 2. RR_Inp_SE_OTA_ExtBias
#    was: OTAs/Rail_to_Rail_OTA_Inp_IP/without_internal_bias
#    (flatten one level up; clean up root-level loose files)
# ============================================================
echo ""
echo "── Step 2: without_internal_bias → RR_Inp_SE_OTA_ExtBias ───"

git mv "OTAs/Rail_to_Rail_OTA_Inp_IP/without_internal_bias" \
       "OTAs/RR_Inp_SE_OTA_ExtBias"

# Root-level SPICE files are duplicates of different_spice/ → delete
# Use -f because git mv already staged these files in the index
for f in \
  "Rail_to_Rail_IP_OP_OTA_MC.spice" \
  "Rail_to_Rail_IP_OP_OTA_STB.spice" \
  "tb_Rail_to_Rail_IP_OP_OTA_DC_TRAN_PSRR.spice"; do
  [[ -f "OTAs/RR_Inp_SE_OTA_ExtBias/$f" ]] && \
    git rm -f "OTAs/RR_Inp_SE_OTA_ExtBias/$f"
done

# This int_bias file is misplaced — belongs to RR_Inp_SE_OTA_IntBias (delete here)
[[ -f "OTAs/RR_Inp_SE_OTA_ExtBias/tb_Rail_to_Rail_IP_OP_OTA_DC_TRAN_PSRR_int_bias.spice" ]] && \
  git rm -f "OTAs/RR_Inp_SE_OTA_ExtBias/tb_Rail_to_Rail_IP_OP_OTA_DC_TRAN_PSRR_int_bias.spice"

echo "  Done."

# ============================================================
# 3. RR_Inp_SE_OTA_IntBias
#    was: OTAs/Rail_to_Rail_OTA_Inp_IP/With_internal_Bias
# ============================================================
echo ""
echo "── Step 3: With_internal_Bias → RR_Inp_SE_OTA_IntBias ──────"

git mv "OTAs/Rail_to_Rail_OTA_Inp_IP/With_internal_Bias" \
       "OTAs/RR_Inp_SE_OTA_IntBias"

echo "  Done."

# ============================================================
# 4. Remove now-empty Rail_to_Rail_OTA_Inp_IP parent
# ============================================================
echo ""
echo "── Step 4: Remove empty parent folder ───────────────────────"
[[ -f "OTAs/Rail_to_Rail_OTA_Inp_IP/README.md" ]] && \
  git rm "OTAs/Rail_to_Rail_OTA_Inp_IP/README.md"
echo "  Done."

# ============================================================
# 5. Delete Rail_to_Rail_OTA_IP (confirmed byte-for-byte
#    duplicate of what is now RR_Inp_SE_OTA_ExtBias)
# ============================================================
echo ""
echo "── Step 5: Delete duplicate Rail_to_Rail_OTA_IP ─────────────"
git rm -r "OTAs/Rail_to_Rail_OTA_IP"
echo "  Done."

# ============================================================
# 6. Commit
# ============================================================
echo ""
echo "── Step 6: Commit ───────────────────────────────────────────"
git add -A
git commit -m "refactor(OTAs): standardise nomenclature + clean structure

Rename and reorganise all OTA IP folders:

  N_OTA_with_internal_bias
    → NMOS_SrcDeg_SE_OTA_IntBias
    + create SCH/ (schematics) and Sims/ (raw data + plots)
    + organise previously flat root dump into sub-dirs

  Rail_to_Rail_OTA_Inp_IP/without_internal_bias
    → RR_Inp_SE_OTA_ExtBias  (flattened one level)
    + remove root-level SPICE duplicates (already in different_spice/)
    + remove misplaced tb_..._int_bias.spice

  Rail_to_Rail_OTA_Inp_IP/With_internal_Bias
    → RR_Inp_SE_OTA_IntBias  (flattened one level)

  Rail_to_Rail_OTA_IP
    DELETED — byte-for-byte duplicate of RR_Inp_SE_OTA_ExtBias

Naming convention: <Input_Stage>_<Output_Stage>_OTA_<Bias>
  NMOS_SrcDeg  = single NMOS pair, source-degenerated
  RR_Inp       = complementary NMOS+PMOS (rail-to-rail input)
  SE           = single-ended output
  IntBias      = self-contained bias  |  ExtBias = external pins"

echo ""
echo "All done. Final OTAs/ tree:"
find OTAs -type d | sort
