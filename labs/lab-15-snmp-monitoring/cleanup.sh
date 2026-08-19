#!/usr/bin/env bash
# Lab 15 — stop the SNMP agent and remove the lab's community string so the
# next lab starts from a clean box. Reverses README Step 2 only.
set -uo pipefail

echo "== Stopping snmpd =="
systemctl stop snmpd 2>/dev/null || true

echo "== Removing the lab community string from /etc/snmp/snmpd.conf =="
if [ -f /etc/snmp/snmpd.conf ]; then
  sed -i '/^rocommunity public 127.0.0.1$/d' /etc/snmp/snmpd.conf
  echo "rocommunity line removed (if it was present)"
else
  echo "/etc/snmp/snmpd.conf not found — nothing to undo"
fi

echo "Cleanup complete."
