#!/usr/bin/env bash
# Lab 17 — verify rsyslog listens on TCP/514, forwards, and that a freshly
# injected test event lands in the aggregated log.
set -uo pipefail

fail=0

if command -v logger >/dev/null 2>&1; then
  echo "PASS: logger is available"
else
  echo "FAIL: logger not found"
  exit 1
fi

if ss -tlnp 2>/dev/null | grep -q ':514'; then
  echo "PASS: rsyslog is listening on TCP/514"
else
  echo "FAIL: nothing listening on :514 — enable imtcp and restart rsyslog (README Steps 1 and 3)"
  fail=1
fi

if [ -f /etc/rsyslog.d/50-forward.conf ]; then
  echo "PASS: /etc/rsyslog.d/50-forward.conf exists"
  if grep -q '^\*\.\* @@127.0.0.1:514$' /etc/rsyslog.d/50-forward.conf; then
    echo "PASS: forwarding rule is *.* @@127.0.0.1:514 (TCP)"
  else
    echo "FAIL: forwarding rule is not '*.* @@127.0.0.1:514' (README Step 2)"
    fail=1
  fi
else
  echo "FAIL: /etc/rsyslog.d/50-forward.conf not found (README Step 2)"
  fail=1
fi

# Inject a fresh event and confirm it is aggregated into /var/log/syslog.
logger -p local0.info "Network+ Lab 17 test event"
sleep 2
if grep -q "Lab 17 test" /var/log/syslog 2>/dev/null; then
  echo "PASS: the 'Lab 17 test' event landed in /var/log/syslog"
else
  echo "FAIL: the test event is not in /var/log/syslog — check systemctl status rsyslog (README Steps 4-5)"
  fail=1
fi

# Confirm the extended regex from Step 7 matches the sample log.
if [ -f data/sample-syslog.log ]; then
  hits=$(grep -cE 'Lab 1[0-9] test' data/sample-syslog.log 2>/dev/null)
  echo "PASS: data/sample-syslog.log present ($hits line(s) match 'Lab 1[0-9] test')"
else
  echo "FAIL: data/sample-syslog.log not found (README Step 7)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — the forwarding pipeline works end to end"
else
  echo "One or more checks failed."
fi
exit "$fail"
