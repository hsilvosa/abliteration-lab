#!/usr/bin/env bash
# Convert an own abliterated checkpoint (safetensors) to GGUF and quantize it.
#
# Usage: scripts/convert_to_gguf.sh <output_name> [QUANT]
#   <output_name>  folder under $ABL_MODELS_DIR/own/ (default models dir: D:/models)
#   QUANT          llama.cpp quant type, default Q4_K_M
#
# Needs:
#   LLAMA_CPP_DIR  a llama.cpp source checkout (for convert_hf_to_gguf.py and its
#                  Python requirements); the winget build ships binaries only.
#   llama-quantize on PATH (included in the winget llama.cpp package).
set -euo pipefail

name="${1:?usage: convert_to_gguf.sh <output_name> [QUANT]}"
quant="${2:-Q4_K_M}"
models_dir="${ABL_MODELS_DIR:-D:/models}"
src="$models_dir/own/$name"
: "${LLAMA_CPP_DIR:?set LLAMA_CPP_DIR to a llama.cpp checkout}"

[ -f "$src/config.json" ] || { echo "missing $src/config.json" >&2; exit 1; }

f16="$src/$name-F16.gguf"
out="$src/$name-$quant.gguf"

python "$LLAMA_CPP_DIR/convert_hf_to_gguf.py" "$src" --outtype f16 --outfile "$f16"
llama-quantize "$f16" "$out" "$quant"
echo "Wrote $out"
echo "Evaluate with: abl eval --own $name --file $(basename "$out")"
