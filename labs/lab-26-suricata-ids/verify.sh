#!/usr/bin/env bash
# Lab 26 — verify Suricata is running and an alert actually fires in eve.json
# (README Steps 3-5). This script triggers the Step 4 test itself, then reads
# the alert back out of the log.
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

EVE=/var/log/suricata/eve.json
FAST=/var/log/suricata/fast.log
fail=0

# --- 1. Suricata is running ---------------------------------------------------
if pgrep -x suricata >/dev/null 2>&1; then
  echo "PASS: suricata is running (pid $(pgrep -x suricata | head -1))"
else
  echo "FAIL: suricata is not running — re-run README Step 3 (suricata -i eth0 -D)"
  fail=1
fi

# --- 2. the lab's own rules are loaded ---------------------------------------
if [ -s /etc/suricata/rules/local.rules ]; then
  echo "PASS: /etc/suricata/rules/local.rules is installed"
else
  echo "FAIL: local.rules not installed — cp local.rules /etc/suricata/rules/"
  fail=1
fi
if grep -q "Loading rule file.*local.rules\|local.rules" /var/log/suricata/suricata.log 2>/dev/null; then
  echo "PASS: suricata.log shows local.rules was loaded"
else
  echo "FAIL: local.rules was not loaded — add it to rule-files: in /etc/suricata/suricata.yaml"
  fail=1
fi

# --- 3. the logs exist --------------------------------------------------------
for f in "$FAST" "$EVE"; do
  if [ -f "$f" ]; then
    echo "PASS: $f exists"
  else
    echo "FAIL: $f missing — Suricata has not written any events yet"
    fail=1
  fi
done

# --- 4. trigger the Step 4 signature and wait for the alert -------------------
before=0
[ -f "$EVE" ] && before=$(wc -l < "$EVE")

echo "INFO: triggering the test signature (README Step 4)..."
curl -s --max-time 20 http://testmynids.org/uid/index.html >/dev/null || \
  echo "INFO: could not reach testmynids.org — if this playground is offline the alert cannot fire"

# Suricata flushes asynchronously; give it up to 30s.
found=""
for _ in $(seq 1 30); do
  if [ -f "$EVE" ] && grep -q '"event_type":"alert"' "$EVE" 2>/dev/null; then
    found=yes
    break
  fi
  sleep 1
done

if [ -n "$found" ]; then
  echo "PASS: an alert event is present in $EVE"
  echo "----- most recent alert -----"
  if command -v jq >/dev/null 2>&1; then
    grep '"event_type":"alert"' "$EVE" | tail -1 | \
      jq -r '"\(.timestamp)  sid=\(.alert.signature_id)  \(.alert.signature)"' 2>/dev/null
  else
    grep '"event_type":"alert"' "$EVE" | tail -1
  fi
  echo "-----------------------------"
else
  after=0
  [ -f "$EVE" ] && after=$(wc -l < "$EVE")
  echo "FAIL: no alert event in $EVE (eve.json grew from $before to $after lines)"
  fail=1
fi

# --- 5. fast.log carries the same alert ---------------------------------------
if [ -s "$FAST" ]; then
  echo "PASS: $FAST is non-empty — last line:"
  tail -1 "$FAST"
else
  echo "FAIL: $FAST is empty — no alert reached the fast log"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — run ./cleanup.sh before moving on to Lab 27."
else
  echo "One or more checks failed."
fi
exit "$fail"
