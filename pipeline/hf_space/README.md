---
title: FoldX-EV
emoji: 🧬
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# FoldX-EV: Disulfide Bond Redox Potential Calculator

Upload multiple **.cif** files of protein complexes to calculate the redox potential of disulfide bonds.

## How it works

1. **CIF → PDB** conversion via `pdb-tools`
2. **FoldX** `RepairPDB` → `BuildModel` (all CYS → ALA mutation)
3. Calculates **E(V) = −ΔΔG / (23.06 × n_cys)**

## Usage

1. Upload one or more `.cif` files
2. Click **Submit**
3. View the results table and download `final_result.txt`

## Input

- `.cif` files (AlphaFold / PDB format) containing protein complexes with disulfide bonds

## Output

| Column | Description |
|--------|-------------|
| `filename` | Input file name |
| `n.cys` | Number of cysteine residues |
| `total energy` | ΔΔG of CYS→ALA mutation (kcal/mol) |
| `E (V)` | Redox potential |

Larger |E(V)| indicates stronger disulfide bond contribution to stability.
