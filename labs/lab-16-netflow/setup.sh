#!/usr/bin/env bash
# Lab 16 — NetFlow Analysis with nfdump
# Runs README steps 1-3: install nfdump + fprobe, start the collector on
# UDP/9995, start the exporter on eth0. Idempotent — safe to re-run.
set -euo pipefail

echo "== Step 1 — Install the tools =="
DEBIAN_FRONTEND=noninteractive apt update
DEBIAN_FRONTEND=noninteractive apt install -y nfdump fprobe

echo
echo "== Step 2 — Start the collector =="
mkdir -p /tmp/flows
if pgrep -x nfcapd >/dev/null 2>&1; then
  echo "nfcapd already running — leaving it alone"
else
  nfcapd -p 9995 -l /tmp/flows -D
  echo "nfcapd listening on UDP/9995, writing to /tmp/flows"
fi

echo
echo "== Step 3 — Start the exporter =="
if pgrep -x fprobe >/dev/null 2>&1; then
  echo "fprobe already running — leaving it alone"
else
  fprobe -i eth0 127.0.0.1:9995
  echo "fprobe reading eth0, exporting NetFlow v5 to 127.0.0.1:9995"
fi

echo
echo "Collector and exporter are up. Continue with README Step 4, or run ./run.sh"
