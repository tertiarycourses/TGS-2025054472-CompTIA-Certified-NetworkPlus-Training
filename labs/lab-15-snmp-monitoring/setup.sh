#!/usr/bin/env bash
# Lab 15 — SNMP Monitoring
# Runs README steps 1-2: install the agent + client, configure a read-only
# community string, restart snmpd. Idempotent — safe to re-run.
set -euo pipefail

echo "== Step 1 — Install agent and client =="
apt update && apt install -y snmpd snmp snmp-mibs-downloader

echo
echo "== Step 2 — Configure a read-only community =="
sed -i 's/^agentaddress.*/agentaddress udp:127.0.0.1:161/' /etc/snmp/snmpd.conf
if grep -q '^rocommunity public 127.0.0.1' /etc/snmp/snmpd.conf; then
  echo "rocommunity already present — leaving /etc/snmp/snmpd.conf as is"
else
  echo 'rocommunity public 127.0.0.1' >> /etc/snmp/snmpd.conf
fi
systemctl restart snmpd

echo
echo "Agent listening. Continue with README Step 3, or run ./verify.sh"
