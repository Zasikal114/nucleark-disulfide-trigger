#!/bin/bash
# Usage: bash afoldx.sh [--all]
#   --all  include intra-chain disulfide bonds (default: inter-chain only)

DETECT_ARGS=""
if [ "$1" = "--all" ]; then
    DETECT_ARGS="--all"
fi

lists=$(ls Input/)
rm -f ./results/*
echo -e "filename\tn.cys" > filelist.txt

DETECT_SCRIPT="../detect_ssbond.py"

for x in $lists;do
    pdb="Input/$x"

    # ── Step 1: Detect disulfide-bonded CYS ──
    > mutant_list.txt
    > individual_list.txt

    if [ -f "$DETECT_SCRIPT" ]; then
        python3 "$DETECT_SCRIPT" "$pdb" $DETECT_ARGS > mutant_list.txt
    fi

    # Skip if no disulfide bonds detected
    if [ ! -s mutant_list.txt ]; then
        echo "  -> No disulfide bond detected, skipping $x"
        continue
    fi

    nmut=$(wc -l < mutant_list.txt)

    if [ "$nmut" -eq 0 ]; then
        echo -e "$x\t0" >> filelist.txt
        continue
    fi

    (awk '{ printf "%sC%s%sS", sep, $1, $2; sep="," } END { print ";" }' mutant_list.txt) > individual_list.txt

    # ── Step 2: FoldX RepairPDB → BuildModel ──
    (cat "$pdb") > x.pdb
    ./foldx --command=RepairPDB --pdb=x.pdb
    ./foldx --command=BuildModel \
            --pdb=x_Repair.pdb \
          --mutant-file=individual_list.txt \
          --output-dir=./results
    echo -e "$x\t$nmut" >> filelist.txt
done

sed -i '1,8d' ./results/Average_x_Repair.fxout
(paste -d "\t" filelist.txt ./results/Average_x_Repair.fxout | awk -v OFS='\t' '
  $2+0==$2 {
    # E(V) = -ΔΔG / (23.06 * n_cys)
    dG  = $5          # total ΔΔG
    dSs = $22         # disulfide contribution to ΔΔG
    ncys = $2
    baseline = -0.220  # standard cysteine/cystine E° (V)
    e1 = -dG / 23.06 / ncys + baseline
    e2 = -dSs / 23.06 / ncys + baseline
    e3 = -(dG + dSs) / 23.06 / ncys + baseline
    print $0, e1, e2, e3
    next
  }
  { print $0, "E(V)", "E_disulfide(V)", "E_combined(V)" }
') > ./results/final_result.txt
