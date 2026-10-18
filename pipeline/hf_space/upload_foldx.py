#!/usr/bin/env python3
"""Upload the FoldX binary to the HF Space via huggingface_hub API."""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi

SPACE_ID = "kalendar114/Foldx-EV"
TOKEN = os.environ["HF_TOKEN"]  # Hugging Face write token, supplied by the deployer
FOLDX_PATH = Path(__file__).resolve().parent.parent / "foldx" / "foldx"

if not FOLDX_PATH.is_file():
    sys.exit(f"FoldX binary not found at {FOLDX_PATH}")

print(f"Uploading {FOLDX_PATH} ({FOLDX_PATH.stat().st_size / 1e6:.1f} MB) ...")
api = HfApi()
api.upload_file(
    path_or_fileobj=str(FOLDX_PATH),
    path_in_repo="foldx",
    repo_id=SPACE_ID,
    repo_type="space",
    token=TOKEN,
)
print("Done. Restart the Space at https://huggingface.co/spaces/kalendar114/Foldx-EV")
