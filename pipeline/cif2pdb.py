#!/usr/bin/env python3
"""Convert all .cif files under CIF/ to .pdb files under Input/ using pdb-tools."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent / "foldx"
CIF_DIR = BASE / "CIF"
INPUT_DIR = BASE / "Input"
CONDA_ENV = "pdb_tools"


def find_exe(name: str) -> str | None:
    """Find an executable in PATH or common conda locations."""
    # 1. direct PATH lookup
    found = shutil.which(name)
    if found:
        return found
    # 2. search conda envs (WSL and Windows)
    for root in [
        os.path.expanduser("~/miniconda3"),
        os.path.expanduser("~/anaconda3"),
        "/home/lenovo/miniconda3",
    ]:
        path = Path(root) / "envs" / CONDA_ENV / "bin" / name
        if path.is_file():
            return str(path)
    return None


def main():
    if not CIF_DIR.exists():
        sys.exit(f"CIF/ directory not found: {CIF_DIR}")

    cif_files = sorted(CIF_DIR.glob("*.cif"))
    if not cif_files:
        sys.exit(f"No .cif files found in {CIF_DIR}")

    exe = find_exe("pdb_fromcif")
    if not exe:
        sys.exit(
            f"pdb_fromcif not found. Install pdb-tools in conda env '{CONDA_ENV}':\n"
            f"  conda install -n {CONDA_ENV} -c conda-forge pdb-tools -y"
        )

    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    ok, fail = 0, 0
    for cif in cif_files:
        out = INPUT_DIR / f"{cif.stem}.pdb"
        print(f"{cif.name}  ->  {out.name}  ", end="", flush=True)
        result = subprocess.run(
            [exe, str(cif)],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            out.write_text(result.stdout)
            print("OK")
            ok += 1
        else:
            print("FAIL")
            if result.stderr.strip():
                print(f"  {result.stderr.strip()}", file=sys.stderr)
            fail += 1

    print(f"\nDone: {ok} converted, {fail} failed (total {len(cif_files)})")
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
