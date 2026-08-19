#!/usr/bin/env bash
# Lab 20 — verify iperf3 is installed, the server is listening, and a short
# TCP and UDP run both return usable results.
set -uo pipefail

fail=0

if command -v iperf3 >/dev/null 2>&1; then
  echo "PASS: iperf3 is installed"
else
  echo "FAIL: iperf3 not found — run apt install -y iperf3 (README Step 1)"
  exit 1
fi

if ss -tlnp 2>/dev/null | grep -q ':5201'; then
  echo "PASS: an iperf3 server is listening on TCP/5201"
else
  echo "FAIL: nothing listening on :5201 — start the server with iperf3 -s -D (README Step 2)"
  exit 1
fi

tcp_out=$(iperf3 -c 127.0.0.1 -t 3 2>/dev/null)
if echo "$tcp_out" | grep -q 'receiver'; then
  rate=$(echo "$tcp_out" | awk '/receiver/{print $(NF-2), $(NF-1)}')
  echo "PASS: TCP test completed — receiver bitrate $rate"
else
  echo "FAIL: the TCP test produced no receiver summary (README Step 3)"
  fail=1
fi

udp_out=$(iperf3 -c 127.0.0.1 -u -b 10M -t 3 2>/dev/null)
if echo "$udp_out" | grep -q 'Jitter'; then
  echo "PASS: UDP test reported a Jitter / Lost-Datagrams summary"
else
  echo "FAIL: the UDP test produced no jitter summary (README Step 5)"
  fail=1
fi

if [ -f data/baseline-metrics.csv ]; then
  rows=$(($(wc -l < data/baseline-metrics.csv) - 1))
  echo "PASS: data/baseline-metrics.csv present ($rows data row(s))"
else
  echo "FAIL: data/baseline-metrics.csv not found (README Step 7)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — iperf3 measures TCP throughput and UDP jitter/loss"
else
  echo "One or more checks failed."
fi
exit "$fail"
