#!/usr/bin/env bash
# Lab 15 — verify the SNMP agent answers a v2c poll with community "public".
set -uo pipefail

fail=0

if command -v snmpwalk >/dev/null 2>&1; then
  echo "PASS: snmpwalk is installed"
else
  echo "FAIL: snmpwalk not found — run apt install -y snmp (README Step 1)"
  exit 1
fi

if ss -ulnp 2>/dev/null | grep -q ':161'; then
  echo "PASS: an agent is listening on UDP/161"
else
  echo "FAIL: nothing listening on UDP/161 — check systemctl status snmpd (README Step 2)"
  fail=1
fi

sysdescr=$(snmpget -v2c -c public -Ovq 127.0.0.1 sysDescr.0 2>/dev/null)
if [ -n "$sysdescr" ]; then
  echo "PASS: sysDescr.0 returned a value -> $sysdescr"
else
  echo "FAIL: sysDescr.0 returned nothing — is rocommunity public 127.0.0.1 set? (README Step 2)"
  fail=1
fi

uptime_val=$(snmpget -v2c -c public -Ovq 127.0.0.1 sysUpTime.0 2>/dev/null)
if [ -n "$uptime_val" ]; then
  echo "PASS: sysUpTime.0 returned a value -> $uptime_val"
else
  echo "FAIL: sysUpTime.0 returned nothing (README Step 4)"
  fail=1
fi

ifcount=$(snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifDescr 2>/dev/null | wc -l | tr -d ' ')
if [ "${ifcount:-0}" -gt 0 ]; then
  echo "PASS: IF-MIB::ifDescr listed $ifcount interface(s)"
else
  echo "FAIL: IF-MIB::ifDescr returned no interfaces (README Step 5)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — the agent answers v2c polls on 127.0.0.1:161"
else
  echo "One or more checks failed."
fi
exit "$fail"
