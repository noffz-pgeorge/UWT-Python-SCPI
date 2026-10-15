#!/usr/bin/env bash
# python/tools/generate_stubs.sh — regenerate rf_demo.dut._generated stubs from proto/
# Run after changing the proto, or to match a different grpcio/protobuf install.
# Requires the dev extra: pip install -e "python/[dev]"
set -euo pipefail

PY_ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # .../python
REPO_ROOT="$(cd "$PY_ROOT/.." && pwd)"
OUT="$PY_ROOT/src"

cd "$REPO_ROOT"
python -m grpc_tools.protoc \
  -Irf_demo/dut/_generated=proto \
  --python_out="$OUT" --pyi_out="$OUT" --grpc_python_out="$OUT" \
  proto/dut_control.proto

echo "Generated stubs in python/src/rf_demo/dut/_generated/"