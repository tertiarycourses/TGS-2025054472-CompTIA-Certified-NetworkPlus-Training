#!/usr/bin/env bash
# Lab 35 — Simulating Slow / Lossy Links with tc
# Runs the shaping sequence from README steps 1-6.
# Every command below is exactly what the README shows.
#
# IMPORTANT: this script leaves eth0 UNSHAPED at the end (Step 6 deletes the
# qdisc). If it is interrupted part way, run ./cleanup.sh immediately —
# otherwise every later lab runs over a degraded link.
set -euo pipefail

echo "== Step 1 — Baseline ping =="
ping -c5 8.8.8.8 || true

echo
echo "== Step 2 — Add 200 ms of delay =="
tc qdisc add dev eth0 root netem delay 200ms
tc qdisc show dev eth0
ping -c5 8.8.8.8 || true

echo
echo "== Step 3 — Add jitter (200ms +/- 50ms, normal distribution) =="
tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal
ping -c10 8.8.8.8 || true

echo
echo "== Step 4 — Add 5% packet loss =="
tc qdisc change dev eth0 root netem delay 200ms loss 5%
ping -c20 8.8.8.8 || true

echo
echo "== Step 5 — Limit bandwidth with a token bucket filter (1 Mbit/s) =="
tc qdisc del dev eth0 root
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
apt install -y iperf3
iperf3 -s -D
sleep 1
iperf3 -c 127.0.0.1 -t 5 || true

echo
echo "== Step 6 — Remove all shaping =="
tc qdisc del dev eth0 root
tc qdisc show dev eth0
ping -c3 8.8.8.8 || true

echo
echo "Shaping removed. Run ./cleanup.sh to confirm eth0 is clean and stop iperf3."
