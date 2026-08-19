#!/usr/bin/env bash
# Lab 29 — ping, traceroute and mtr
# Runs the full path-analysis sequence from README steps 1-5.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install the tools =="
apt update && apt install -y traceroute mtr-tiny

echo
echo "== Step 2 — Baseline reachability with ping =="
ping -c5 8.8.8.8 || true

echo
echo "== Step 3 — Trace the hop-by-hop path =="
traceroute 8.8.8.8 || true

echo
echo "== Step 4 — Combined live view with mtr (report mode, 20 cycles) =="
mtr -rwc 20 8.8.8.8 || true

echo
echo "== Step 5 — TCP traceroute for paths that block ICMP =="
apt install -y traceroute
traceroute -T -p 443 example.com || true

echo
echo "Record your hop RTTs and loss percentages in data/latency-log.csv"
