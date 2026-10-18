import os
import shutil
import subprocess
from pathlib import Path

import gradio as gr
import pandas as pd

WORKDIR = Path("/app")
CIF_DIR = WORKDIR / "CIF"
INPUT_DIR = WORKDIR / "Input"
RESULTS_DIR = WORKDIR / "results"
PIPELINE = WORKDIR / "pipeline.sh"

TITLE = "FoldX-EV | Disulfide Bond Redox Potential"
DESCRIPTION = """
Upload **.cif files** of protein complexes → CYS→ALA mutation by FoldX → **redox potential E(V)**.

**E(V) = −ΔΔG / (23.06 × n_cys)**  ·  Larger |E(V)| = stronger disulfide bond.
"""


def check_foldx():
    fx = WORKDIR / "foldx"
    return str(fx) if fx.is_file() and os.access(fx, os.X_OK) else None


def clear_dirs():
    for d in [CIF_DIR, INPUT_DIR, RESULTS_DIR]:
        if d.exists():
            shutil.rmtree(d)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def count_steps(pdb_count):
    """Each file: RepairPDB + BuildModel + final = 2*pdb_count + 1"""
    return 2 * pdb_count + 1


def run_analysis(files, progress=gr.Progress()):
    fx = check_foldx()
    if not fx:
        yield pd.DataFrame({"Error": ["FoldX binary not found."]}), "FoldX binary missing."
        return

    if not files:
        yield pd.DataFrame({"Info": ["Please upload .cif files."]}), "Waiting for input..."
        return

    clear_dirs()
    CIF_DIR.mkdir(parents=True, exist_ok=True)

    for f in files:
        shutil.copy(f.name, CIF_DIR / Path(f.name).name)

    cif_files = sorted(CIF_DIR.glob("*.cif"))
    log = [f"Uploaded {len(cif_files)} file(s)"]

    progress(0, desc="Converting CIF → PDB...")
    yield pd.DataFrame({"Status": ["Converting..."]}), "\n".join(log)

    # ── Step 1: CIF → PDB ──
    converted = 0
    for cif in cif_files:
        out = INPUT_DIR / f"{cif.stem}.pdb"
        r = subprocess.run(["pdb_fromcif", str(cif)], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            out.write_text(r.stdout)
            converted += 1
            log.append(f"  {cif.name} → {out.name}")
        else:
            log.append(f"  {cif.name} FAILED")

    if converted == 0:
        yield pd.DataFrame({"Error": ["Conversion failed."]}), "\n".join(log)
        return

    log.append(f"Converted {converted}/{len(cif_files)} to PDB")
    progress(0.05, desc="Starting FoldX pipeline...")
    yield pd.DataFrame({"Status": ["Running FoldX..."]}), "\n".join(log)

    # ── Step 2: Run FoldX pipeline ──
    env = os.environ.copy()
    env["FOLDX_BIN"] = fx
    env["WORKDIR"] = str(WORKDIR)

    proc = subprocess.Popen(
        ["bash", str(PIPELINE)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, env=env, cwd=str(WORKDIR),
    )

    total_steps = count_steps(converted)
    step = 0
    done_files = 0

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue

        if line.startswith("[STEP]"):
            # Parse: [STEP] RepairPDB [1/3] name.pdb (6 Cys)
            step += 1
            progress(step / total_steps, desc=line[6:])
            log.append(line[6:])
            yield pd.DataFrame({"Running": [f"{step}/{total_steps} steps"]}), "\n".join(log)

        elif line.startswith("[OK]"):
            step += 1
            progress(step / total_steps, desc=line[4:])
            log.append("  " + line[4:])
            if "BuildModel" in line:
                done_files += 1
            yield pd.DataFrame({"Running": [f"{done_files}/{converted} files done"]}), "\n".join(log)

        elif "[DONE]" in line:
            log.append("Generating results...")

        elif "ERROR" in line:
            log.append(line)

    proc.wait()

    # ── Step 3: Read results ──
    final = RESULTS_DIR / "final_result.txt"
    if not final.exists():
        log.append(f"Pipeline failed (exit {proc.returncode})")
        yield pd.DataFrame({"Error": ["Pipeline failed."]}), "\n".join(log)
        return

    df = pd.read_csv(final, sep="\t")
    for c in ["total energy", "E (V)"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").round(6)

    progress(1.0, desc="Done!")
    log.append(f"Complete: {len(df)} result(s)")
    yield df, "\n".join(log)


if __name__ == "__main__":
    fx = check_foldx()
    print("FoldX ready" if fx else "FoldX not found!")

    demo = gr.Interface(
        fn=run_analysis,
        inputs=gr.File(
            file_count="multiple",
            file_types=[".cif"],
            label="Upload .cif files",
        ),
        outputs=[
            gr.Dataframe(label="Results", wrap=True),
            gr.Textbox(label="Progress", lines=18, max_lines=40),
        ],
        title=TITLE,
        description=DESCRIPTION,
        flagging_mode="never",
    )
    demo.queue(max_size=10).launch(server_name="0.0.0.0", server_port=7860, theme="soft")
