#!/usr/bin/env bash
# Lab 1 — verify the saved capture from README Step 7 exists and holds packets.
set -uo pipefail

PCAP="osi-lab.pcap"
fail=0

if [ -f "$PCAP" ]; then
  echo "PASS: $PCAP exists"
else
  echo "FAIL: $PCAP not found — re-run README Step 7 (tcpdump -w osi-lab.pcap)"
  fail=1
fi

if [ -s "$PCAP" ]; then
  echo "PASS: $PCAP is non-empty ($(wc -c < "$PCAP") bytes)"
else
  echo "FAIL: $PCAP is empty — no packets were captured, generate traffic with curl while tcpdump runs"
  fail=1
fi

if command -v tcpdump >/dev/null 2>&1 && [ -s "$PCAP" ]; then
  count=$(tcpdump -nn -r "$PCAP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${count:-0}" -gt 0 ]; then
    echo "PASS: $PCAP decodes to $count packet(s)"
  else
    echo "FAIL: $PCAP contains no readable packets"
    fail=1
  fi
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — load $PCAP into https://alfredang.github.io/pcapanalyzer/"
else
  echo "One or more checks failed."
fi
exit "$fail"
