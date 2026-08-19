#!/usr/bin/env bash
# Lab 16 — stop the exporter and collector (README Step 6) and remove the
# lab's own scratch directory of captured flow files.
set -uo pipefail

echo "== Step 6 — Clean up =="
pkill fprobe 2>/dev/null || true
pkill nfcapd 2>/dev/null || true
echo "fprobe and nfcapd stopped"

echo "== Removing this lab's flow files =="
rm -rf /tmp/flows
echo "/tmp/flows removed"

echo "Cleanup complete."
