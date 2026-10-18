#!/usr/bin/env python3
"""Push the Space code files to Hugging Face Hub using huggingface_hub API."""
import os
from pathlib import Path
from huggingface_hub import HfApi, create_repo, CommitOperationAdd

SPACE_ID = "kalendar114/Foldx-EV"
TOKEN = os.environ["HF_TOKEN"]  # Hugging Face write token, supplied by the deployer
SPACE_DIR = Path(__file__).resolve().parent

EXCLUDE = {
    ".git", ".gitignore", "__pycache__",
    "CIF", "Input", "results",
    "foldx", "x.pdb", "x_Repair.pdb", "x_Repair.fxout",
    "upload_foldx.py", "push_to_hf.py",
}

api = HfApi()

# Ensure space exists
try:
    api.repo_info(repo_id=SPACE_ID, repo_type="space")
    print(f"Space {SPACE_ID} exists.")
except Exception:
    print(f"Creating space {SPACE_ID}...")
    create_repo(
        repo_id=SPACE_ID,
        repo_type="space",
        space_sdk="docker",
        private=False,
        token=TOKEN,
    )
    print("Space created.")

# Gather files
operations = []
for root, dirs, files in os.walk(SPACE_DIR):
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for f in files:
        if f in EXCLUDE:
            continue
        fp = Path(root) / f
        rel = fp.relative_to(SPACE_DIR)
        operations.append(
            CommitOperationAdd(path_in_repo=str(rel).replace("\\", "/"), path_or_fileobj=str(fp))
        )

print(f"Uploading {len(operations)} files...")
for op in operations:
    print(f"  {op.path_in_repo}")

api.create_commit(
    repo_id=SPACE_ID,
    repo_type="space",
    operations=operations,
    commit_message="Update Space files",
    token=TOKEN,
)
print("Done! https://huggingface.co/spaces/kalendar114/Foldx-EV")
