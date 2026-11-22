#!/usr/bin/env bash
# Create the project virtualenv with uv. Not run automatically.
#
#   scripts/setup_env.sh            base install (download, eval, report)
#   scripts/setup_env.sh full       + torch CUDA, transformers, bitsandbytes, pytest
set -euo pipefail
cd "$(dirname "$0")/.."

uv venv --python 3.12 .venv
if [ "${1:-}" = "full" ]; then
  # CUDA 12.x wheels for the RTX 3060; change the index for other setups.
  uv pip install --python .venv torch --index-url https://download.pytorch.org/whl/cu128
  uv pip install --python .venv -e ".[abliterate,dev]"
else
  uv pip install --python .venv -e ".[dev]"
fi
echo "Activate with: source .venv/Scripts/activate"
