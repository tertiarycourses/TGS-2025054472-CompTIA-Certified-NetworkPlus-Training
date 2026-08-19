#!/usr/bin/env bash
# Lab 20 — stop the backgrounded iperf3 server (README Step 8) so TCP/5201
# is free for the next lab.
set -uo pipefail

echo "== Step 8 — Stop the server =="
pkill iperf3 2>/dev/null || true
sleep 1

if ss -tlnp 2>/dev/null | grep -q ':5201'; then
  echo "WARNING: something is still listening on :5201"
else
  echo "TCP/5201 is free — iperf3 server stopped"
fi

echo "Cleanup complete."
