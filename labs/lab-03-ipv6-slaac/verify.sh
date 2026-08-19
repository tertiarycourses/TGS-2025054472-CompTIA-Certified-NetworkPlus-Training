#!/usr/bin/env bash
# Lab 3 — verify the global IPv6 address from README Step 3 is present on eth0.
# Run this AFTER Step 4 and BEFORE the Step 7 cleanup.
set -uo pipefail

fail=0

if ip -6 addr show eth0 | grep -q 'inet6 fe80:'; then
  echo "PASS: eth0 has a link-local address (fe80::/10)"
  echo "      $(ip -6 addr show eth0 | grep 'inet6 fe80:' | head -1 | sed 's/^ *//')"
else
  echo "FAIL: no fe80:: link-local address on eth0"
  fail=1
fi

if ip -6 addr show eth0 | grep -q 'inet6 2001:db8::10/64'; then
  echo "PASS: global address 2001:db8::10/64 is configured on eth0"
else
  echo "FAIL: 2001:db8::10/64 not found — run: ip -6 addr add 2001:db8::10/64 dev eth0"
  fail=1
fi

if ping6 -c2 2001:db8::10 >/dev/null 2>&1; then
  echo "PASS: ping6 to 2001:db8::10 succeeded"
else
  echo "FAIL: ping6 to 2001:db8::10 failed"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — now run README Step 7 to clean up"
else
  echo "One or more checks failed."
fi
exit "$fail"
