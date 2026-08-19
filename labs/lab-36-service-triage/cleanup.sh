#!/usr/bin/env bash
# Lab 36 — restore the ORIGINAL iptables rules saved by break.sh.
# Tolerant: keep going even if the rule has already been removed by hand.
set -uo pipefail

BAK=/tmp/lab36-iptables.bak

echo "== Removing the injected reject rule =="
iptables -D OUTPUT -p tcp --dport 443 -d example.com -j REJECT --reject-with tcp-reset 2>/dev/null \
  && echo "rule deleted" || echo "rule already gone (or you removed it during triage)"

if [ -f "$BAK" ]; then
  echo
  echo "== Restoring the full original filter table from $BAK =="
  iptables-restore < "$BAK" && echo "iptables restored" || echo "iptables-restore failed — check $BAK by hand"
else
  echo
  echo "No backup at $BAK — the single rule deletion above is the only change to undo."
fi

echo
echo "== Current OUTPUT chain =="
iptables -L OUTPUT -n --line-numbers

echo
echo "== Confirming the service is reachable again =="
nc -zv example.com 443 || echo "still blocked — check for other rules"

echo
echo "Cleanup done — the box is back to its pre-lab state."
