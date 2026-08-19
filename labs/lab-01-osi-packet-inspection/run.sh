#!/usr/bin/env bash
# Lab 1 — OSI Model Packet Inspection
# Runs the capture + traffic sequence from README steps 1-7.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install the capture tools =="
apt update && apt install -y tcpdump curl

echo
echo "== Step 2 — Identify the active interface =="
ip -brief addr

echo
echo "== Step 3 — Start a capture in the background (5 packets, tcp port 80) =="
tcpdump -i eth0 -nn -v -c 5 'tcp port 80' &
sleep 2

echo
echo "== Step 4 — Generate HTTP traffic =="
curl -s http://example.com > /dev/null
wait %1 2>/dev/null || true

echo
echo "== Step 5 — Re-run with Layer 2 MACs (-e) and Layer 7 ASCII payload (-A) =="
tcpdump -i eth0 -nn -e -A -c 10 'tcp port 80' &
sleep 2
curl -s http://example.com > /dev/null
wait %1 2>/dev/null || true

echo
echo "== Step 6 — Stop background captures =="
kill %1 2>/dev/null || true

echo
echo "== Step 7 — Save a capture to osi-lab.pcap for the TIS PCAP Analyzer =="
tcpdump -i eth0 -nn -w osi-lab.pcap -c 20 'tcp port 80' &
sleep 2
curl -s http://example.com > /dev/null
curl -s http://example.com > /dev/null
wait %1 2>/dev/null || true

echo
echo "Capture written to $(pwd)/osi-lab.pcap"
echo "Download it from the Killercoda editor and open https://alfredang.github.io/pcapanalyzer/"
echo "Now run ./verify.sh"
