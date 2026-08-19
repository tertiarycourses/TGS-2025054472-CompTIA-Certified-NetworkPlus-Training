#!/usr/bin/env bash
# Lab 20 — Performance Baseline with iperf3
# Runs README steps 1-6: install, start the server, then the TCP, parallel,
# UDP and reverse tests.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install iperf3 =="
DEBIAN_FRONTEND=noninteractive apt update
DEBIAN_FRONTEND=noninteractive apt install -y iperf3

echo
echo "== Step 2 — Run a server in the background =="
if pgrep -x iperf3 >/dev/null 2>&1; then
  echo "iperf3 server already running — leaving it alone"
else
  iperf3 -s -D
  echo "iperf3 server daemonised on TCP/5201"
fi
sleep 2

echo
echo "== Step 3 — TCP throughput test (10 seconds) =="
iperf3 -c 127.0.0.1 -t 10

echo
echo "== Step 4 — Parallel streams (saturate WAN circuits) =="
iperf3 -c 127.0.0.1 -P 4 -t 10

echo
echo "== Step 5 — UDP test (jitter + loss) =="
iperf3 -c 127.0.0.1 -u -b 100M -t 10

echo
echo "== Step 6 — Reverse mode (server sends to client) =="
iperf3 -c 127.0.0.1 -R -t 10

echo
echo "Record your Bitrate, Jitter and Lost/Total figures in data/baseline-metrics.csv"
echo "Then run ./verify.sh, then ./cleanup.sh"
