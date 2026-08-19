#!/usr/bin/env bash
# Lab 26 — Intrusion Detection with Suricata
# Performs README Steps 1-3: install, update the ET ruleset, install the custom
# local.rules, and start Suricata on the active interface.
# Idempotent: safe to re-run (any previous suricata is stopped first).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IFACE=eth0

echo "== Step 0: stop any Suricata left over from a previous run =="
pkill suricata 2>/dev/null || true
sleep 1

echo "== Step 1: install suricata and jq =="
apt update && apt install -y suricata jq

echo "== Step 2: update the Emerging Threats community ruleset =="
suricata-update || echo "WARNING: suricata-update failed (offline?) — the local rules below still work"

echo "== Step 2b: install the lab's own rules =="
mkdir -p /etc/suricata/rules
cp "$HERE/local.rules" /etc/suricata/rules/local.rules
echo "installed /etc/suricata/rules/local.rules"

# Make sure suricata.yaml actually loads local.rules.
if grep -q '^\s*-\s*local\.rules\s*$' /etc/suricata/suricata.yaml; then
  echo "suricata.yaml already lists local.rules"
else
  cp /etc/suricata/suricata.yaml /etc/suricata/suricata.yaml.lab26.bak
  # Append local.rules directly under the rule-files: list.
  sed -i '/^rule-files:/a\  - local.rules' /etc/suricata/suricata.yaml
  echo "added local.rules to rule-files: in suricata.yaml (backup at suricata.yaml.lab26.bak)"
fi

echo "== Validating the configuration and rules =="
suricata -T -c /etc/suricata/suricata.yaml -v

echo "== Step 3: start Suricata on $IFACE =="
if ! ip link show "$IFACE" >/dev/null 2>&1; then
  IFACE="$(ip -o -4 route show default | awk '{print $5}' | head -1)"
  echo "eth0 not present — using the default-route interface: $IFACE"
fi
suricata -i "$IFACE" -D
sleep 5
tail /var/log/suricata/suricata.log

echo
echo "Suricata is running on $IFACE. Now trigger a signature (README Step 4) and run ./verify.sh"
