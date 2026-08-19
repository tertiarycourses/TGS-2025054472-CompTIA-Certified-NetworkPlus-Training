#!/usr/bin/env bash
# Lab 16 — verify the collector captured flows and nfdump can report on them.
set -uo pipefail

FLOWDIR="/tmp/flows"
fail=0

if command -v nfdump >/dev/null 2>&1; then
  echo "PASS: nfdump is installed"
else
  echo "FAIL: nfdump not found — run apt install -y nfdump fprobe (README Step 1)"
  exit 1
fi

if [ -d "$FLOWDIR" ]; then
  echo "PASS: $FLOWDIR exists"
else
  echo "FAIL: $FLOWDIR not found — start the collector (README Step 2)"
  exit 1
fi

files=$(find "$FLOWDIR" -type f -name 'nfcapd.*' 2>/dev/null | wc -l | tr -d ' ')
if [ "${files:-0}" -gt 0 ]; then
  echo "PASS: $files nfcapd file(s) written to $FLOWDIR"
else
  echo "FAIL: no nfcapd.* files in $FLOWDIR — nfcapd rolls a file every 5 minutes, wait and retry (README Step 5)"
  fail=1
fi

flows=$(nfdump -R "$FLOWDIR" -o long 2>/dev/null | grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}')
if [ "${flows:-0}" -gt 0 ]; then
  echo "PASS: nfdump reports $flows flow record(s)"
else
  echo "FAIL: nfdump reported no flow records — generate traffic while fprobe runs (README Step 4)"
  fail=1
fi

if nfdump -R "$FLOWDIR" -s srcip 2>/dev/null | grep -q 'Top'; then
  echo "PASS: nfdump -s srcip produced a top-talker report"
else
  echo "FAIL: nfdump -s srcip produced no report (README Step 5)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — flows were exported, collected and reported on"
else
  echo "One or more checks failed."
fi
exit "$fail"
