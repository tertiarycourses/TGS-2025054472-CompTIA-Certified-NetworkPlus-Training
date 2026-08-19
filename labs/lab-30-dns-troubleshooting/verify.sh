#!/usr/bin/env bash
# Lab 30 — verify DNS resolution is healthy again after break.sh + cleanup.sh.
set -uo pipefail

fail=0

if command -v dig >/dev/null 2>&1; then
  echo "PASS: dig is installed (dnsutils, README Step 1)"
else
  echo "FAIL: dig not found — run: apt update && apt install -y dnsutils"
  fail=1
fi

if grep -q '10\.99\.0\.53' /etc/resolv.conf 2>/dev/null; then
  echo "FAIL: /etc/resolv.conf still contains the injected black-hole resolver 10.99.0.53 — run ./cleanup.sh"
  fail=1
else
  echo "PASS: the injected resolver 10.99.0.53 is gone from /etc/resolv.conf"
fi

if [ "${fail}" -eq 0 ] && command -v dig >/dev/null 2>&1; then
  ans=$(dig example.com +short +time=3 +tries=1 2>/dev/null | head -1)
  if [ -n "$ans" ]; then
    echo "PASS: system resolver answers for example.com ($ans)"
  else
    echo "FAIL: system resolver returned no answer for example.com"
    fail=1
  fi

  up=$(dig @1.1.1.1 example.com +short +time=3 +tries=1 2>/dev/null | head -1)
  if [ -n "$up" ]; then
    echo "PASS: upstream 1.1.1.1 answers for example.com ($up)"
  else
    echo "FAIL: upstream 1.1.1.1 returned no answer — check outbound UDP/53"
    fail=1
  fi
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — DNS resolution is restored."
else
  echo "One or more checks failed."
fi
exit "$fail"
