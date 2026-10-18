#!/usr/bin/env python3
"""Detect disulfide bonds from PDB file by SG-SG distance.

Usage:
    python detect_ssbond.py input.pdb           # inter-chain only (default)
    python detect_ssbond.py input.pdb --all     # include intra-chain bonds

Output: tab-separated list of paired CYS residues (chain resnum) to stdout.
"""
import math
import sys
from pathlib import Path

THRESHOLD = 2.5  # SG-SG distance threshold for disulfide bond (Angstrom)


def parse_cys_sg(pdb_path):
    """Extract (chain, resnum, x, y, z) for all CYS SG atoms."""
    atoms = []
    with open(pdb_path) as f:
        for line in f:
            if not line.startswith("ATOM") and not line.startswith("HETATM"):
                continue
            resname = line[17:20].strip()
            atname = line[12:16].strip()
            if resname != "CYS" or atname != "SG":
                continue
            chain = line[21:22].strip()
            resnum = line[22:26].strip()
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
            except ValueError:
                continue
            atoms.append((chain, resnum, x, y, z))
    return atoms


def find_disulfide(atoms, inter_chain_only=False):
    """Find cysteine pairs forming disulfide bonds.

    If inter_chain_only is True, only return bonds between different chains.
    """
    paired = set()
    bonds = []
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            c1, r1, x1, y1, z1 = atoms[i]
            c2, r2, x2, y2, z2 = atoms[j]
            if inter_chain_only and c1 == c2:
                continue
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
            if dist <= THRESHOLD:
                bonds.append((c1, r1, c2, r2, dist))
                paired.add((c1, r1))
                paired.add((c2, r2))
    return bonds, paired


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        sys.exit(f"Usage: {sys.argv[0]} input.pdb [--all]")

    pdb = Path(sys.argv[1])
    if not pdb.is_file():
        sys.exit(f"PDB not found: {pdb}")

    inter_chain_only = "--all" not in sys.argv

    atoms = parse_cys_sg(pdb)
    if not atoms:
        sys.exit("No CYS SG atoms found.")

    bonds, paired = find_disulfide(atoms, inter_chain_only=inter_chain_only)

    if not bonds:
        sys.exit(0)

    # Output paired CYS to stdout (one per line: chain resnum)
    for chain, resnum in sorted(set(paired)):
        print(f"{chain}\t{resnum}")


if __name__ == "__main__":
    main()
