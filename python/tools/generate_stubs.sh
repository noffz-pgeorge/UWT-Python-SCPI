#!/usr/bin/env bash
# python/tools/generate_stubs.sh — regenerate the dut._generated gRPC stubs from proto/
# Run after changing the proto, or to match a different grpcio/protobuf install.
# Requires the dev extra: pip install -e "python/[demo,dev]"
set -euo pipefail

PY_ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # .../python  (this script lives in python/tools)
REPO_ROOT="$(cd "$PY_ROOT/.." && pwd)"        # repo root    (one level above python/)
OUT="$PY_ROOT/demos"                          # protoc writes <OUT>/<import prefix>/...

cd "$REPO_ROOT"
# -I<prefix>=proto: treat proto/ as if it lived at dut/_generated/. That makes protoc
#   (1) write the files to $OUT/dut/_generated/ and
#   (2) emit "from dut._generated import dut_control_pb2" inside the _grpc stub,
# which matches how demos import it (demos/ is on sys.path when a demo script runs).
python -m grpc_tools.protoc \
  -Idut/_generated=proto \
  --python_out="$OUT" --pyi_out="$OUT" --grpc_python_out="$OUT" \
  proto/dut_control.proto

echo "Generated stubs in python/demos/dut/_generated/"