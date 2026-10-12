#!/usr/bin/env bash
# scripts/generate_stubs.sh — regenerate src/dut_grpc stubs from proto/
# Run after changing the proto, or to match an older grpcio/protobuf install.
set -euo pipefail
cd "$(dirname "$0")/.."
python -m grpc_tools.protoc -Idut_grpc=proto \
  --python_out=src --pyi_out=src --grpc_python_out=src \
  proto/dut_control.proto
echo "Generated stubs in dut_grpc/"
