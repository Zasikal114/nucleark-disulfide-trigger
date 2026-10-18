#!/usr/bin/env python3
"""Convert AlphaFold ModelCIF (.cif) files in foldx/Input/ to PDB format, then delete the source .cif."""
import sys
from pathlib import Path


def parse_mmcif(cif_path):
    """Parse mmCIF atom_site records. Returns list of dicts."""
    atoms = []
    in_atom_site = False
    columns = []

    with open(cif_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("_atom_site."):
                columns.append(line.split(".")[1])
                in_atom_site = True
                continue
            if in_atom_site:
                if line.startswith("#") or line.startswith("_") or line.startswith("loop_") or not line:
                    if columns and (line.startswith("#") or line.startswith("_") or line.startswith("loop_")):
                        in_atom_site = False
                    continue
                # Data row: split on whitespace
                fields = line.split()
                if len(fields) == len(columns):
                    row = dict(zip(columns, fields))
                    if row.get("group_PDB") in ("ATOM", "HETATM"):
                        atoms.append(row)

    return atoms


def format_atom(row):
    """Format one atom as a PDB ATOM/HETATM record."""
    group = row["group_PDB"]  # ATOM or HETATM
    serial = int(row["id"])
    at_name = row["label_atom_id"]
    alt = row.get("label_alt_id", ".")
    if alt in (".", "?"):
        alt = " "
    res_name = row["label_comp_id"]
    chain = row.get("label_asym_id", "A")
    res_seq = int(row["label_seq_id"])
    ins_code = row.get("pdbx_PDB_ins_code", "?")
    if ins_code in (".", "?"):
        ins_code = " "
    x = float(row["Cartn_x"])
    y = float(row["Cartn_y"])
    z = float(row["Cartn_z"])
    occ = float(row["occupancy"])
    tf = float(row["B_iso_or_equiv"])
    elem = row.get("type_symbol", at_name[0])

    # PDB atom name formatting (col 13-16)
    if len(elem) == 2:
        name_fmt = f" {at_name:<3s}"[:4]  # left-justified, col 13 blank
    else:
        name_fmt = f" {at_name:<3s}"[:4]   # starts at col 14
        if len(at_name) == 4:
            name_fmt = at_name[:4]

    return (
        f"{group:<6s}"
        f"{serial:>5d} "
        f"{name_fmt:<4s}"
        f"{alt:1s}"
        f"{res_name:>3s} "
        f"{chain:1s}"
        f"{res_seq:>4d}"
        f"{ins_code:1s}   "
        f"{x:8.3f}"
        f"{y:8.3f}"
        f"{z:8.3f}"
        f"{occ:6.2f}"
        f"{tf:6.2f}          "
        f"{elem:>2s}"
        f"  \n"
    )


def convert(cif_path, pdb_path):
    atoms = parse_mmcif(cif_path)
    if not atoms:
        print(f"  WARNING: no ATOM records found in {cif_path.name}", file=sys.stderr)
        return False
    with open(pdb_path, "w") as f:
        for a in atoms:
            f.write(format_atom(a))
        f.write("END\n")
    return True


def main():
    base = Path(__file__).resolve().parent / "foldx"
    inp_dir = base / "Input"

    if not inp_dir.exists():
        sys.exit(f"Input/ directory not found: {inp_dir}")

    cif_files = sorted(inp_dir.glob("*.cif"))
    if not cif_files:
        print("No .cif files found in Input/")
        sys.exit(0)

    ok, fail = 0, 0
    for cif in cif_files:
        out = inp_dir / f"{cif.stem}.pdb"
        print(f"{cif.name}  ->  {out.name}  ", end="", flush=True)
        if convert(cif, out):
            cif.unlink()
            print("OK")
            ok += 1
        else:
            print("FAIL")
            fail += 1

    print(f"\nDone: {ok} converted, {fail} failed (total {len(cif_files)})")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
