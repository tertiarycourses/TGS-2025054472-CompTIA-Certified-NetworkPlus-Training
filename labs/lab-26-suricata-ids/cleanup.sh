#!/usr/bin/env bash
# Lab 26 — reverse everything this lab created (README Step 6).
# Stops the Suricata daemon, removes the lab's own rule file and restores
# suricata.yaml. Suricata sniffs promiscuously and rewrites eve.json constantly,
# so leaving it running slows every later capture lab down.
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Stopping Suricata =="
if pgrep -x suricata >/dev/null 2>&1; then
  pkill suricata && echo "suricata stopped"
  sleep 2
  pgrep -x suricata >/dev/null 2>&1 && { pkill -9 suricata; echo "forced stop"; } || true
else
  echo "suricata was not running"
fi

echo "== Removing the lab's own rule file =="
if [ -f /etc/suricata/rules/local.rules ]; then
  rm -f /etc/suricata/rules/local.rules && echo "removed /etc/suricata/rules/local.rules"
else
  echo "no local.rules to remove"
fi

echo "== Restoring suricata.yaml =="
if [ -f /etc/suricata/suricata.yaml.lab26.bak ]; then
  mv /etc/suricata/suricata.yaml.lab26.bak /etc/suricata/suricata.yaml
  echo "restored /etc/suricata/suricata.yaml from the lab backup"
else
  echo "no lab backup — leaving /etc/suricata/suricata.yaml as-is"
fi

echo
echo "Logs under /var/log/suricata/ are left in place so you can still read your alerts."
echo "Cleanup done — nothing is sniffing the interface any more."
