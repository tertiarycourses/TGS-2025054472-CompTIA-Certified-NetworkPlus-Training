#!/usr/bin/env bash
# Lab 18 — verify chrony is running, has sources, and has selected one.
set -uo pipefail

fail=0

if command -v chronyc >/dev/null 2>&1; then
  echo "PASS: chronyc is installed"
else
  echo "FAIL: chronyc not found — run apt install -y chrony (README Step 1)"
  exit 1
fi

if systemctl is-active --quiet chrony 2>/dev/null || pgrep -x chronyd >/dev/null 2>&1; then
  echo "PASS: chronyd is running"
else
  echo "FAIL: chronyd is not running — systemctl enable --now chrony (README Step 1)"
  fail=1
fi

sources=$(chronyc sources -v 2>/dev/null | grep -cE '^\^')
if [ "${sources:-0}" -gt 0 ]; then
  echo "PASS: chronyc sources lists $sources time source(s)"
else
  echo "FAIL: chronyc sources listed no servers (README Step 2)"
  fail=1
fi

if chronyc sources -v 2>/dev/null | grep -qE '^\^\*'; then
  selected=$(chronyc sources -v 2>/dev/null | grep -E '^\^\*' | awk '{print $2}')
  echo "PASS: a source is selected and synced -> ^* $selected"
else
  echo "FAIL: no '^*' selected source yet — wait ~60s for chrony to settle, then re-run (README Step 2)"
  fail=1
fi

stratum=$(chronyc tracking 2>/dev/null | awk -F': *' '/^Stratum/{print $2}')
if [ -n "${stratum:-}" ] && [ "$stratum" != "0" ]; then
  echo "PASS: chronyc tracking reports Stratum $stratum"
else
  echo "FAIL: chronyc tracking reports no usable stratum (README Step 3)"
  fail=1
fi

if grep -q '^server time.cloudflare.com iburst$' /etc/chrony/chrony.conf 2>/dev/null; then
  echo "PASS: the extra NTP server from Step 4 is in /etc/chrony/chrony.conf"
else
  echo "FAIL: 'server time.cloudflare.com iburst' not found in /etc/chrony/chrony.conf (README Step 4)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — the clock is synchronised to a selected NTP source"
else
  echo "One or more checks failed."
fi
exit "$fail"
