#!/usr/bin/env bash
# Lab 16 — NetFlow Analysis with nfdump
# Runs README steps 4-5: generate traffic, wait for the collector to roll a
# file, then produce the three nfdump reports.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 4 — Generate traffic =="
curl -s https://example.com > /dev/null
ping -c5 8.8.8.8

echo
echo "== Step 5 — Analyse the flows =="
echo "-- waiting 60s for nfcapd to roll a file --"
sleep 60

echo
echo "-- nfdump -R /tmp/flows -o long | head --"
nfdump -R /tmp/flows -o long | head

echo
echo "-- nfdump -R /tmp/flows -s srcip (top talkers) --"
nfdump -R /tmp/flows -s srcip

echo
echo "-- nfdump -R /tmp/flows -s dstport (busiest ports) --"
nfdump -R /tmp/flows -s dstport

echo
echo "Now run ./verify.sh, then ./cleanup.sh"
