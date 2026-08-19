#!/usr/bin/env bash
# Lab 27 — reverse everything this lab created (README Step 7).
#
# CRITICAL: this deletes ONLY the two rules the lab added, by exact match. It
# deliberately does NOT run `iptables -F` — a blanket flush would also destroy
# Docker's, ufw's or the playground's own rules and break the box for the next
# lab. Leaving the DROP rule in place would silently break Lab 28 onwards.
# Tolerant: keep going even if a rule is already gone.
set -uo pipefail

echo "== Deleting the ACCEPT rule (README Step 2), all copies =="
n=0
while iptables -C INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT 2>/dev/null; do
  iptables -D INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT && n=$((n+1))
done
echo "removed $n copy/copies of the ACCEPT rule"

echo "== Deleting the DROP rule (README Step 3), all copies =="
n=0
while iptables -C INPUT -p tcp --dport 3306 -j DROP 2>/dev/null; do
  iptables -D INPUT -p tcp --dport 3306 -j DROP && n=$((n+1))
done
echo "removed $n copy/copies of the DROP rule"

echo "== Removing the test address from lo (README Step 5) =="
ip addr del 10.0.0.5/24 dev lo 2>/dev/null && echo "removed 10.0.0.5/24 from lo" \
  || echo "10.0.0.5/24 was not on lo"

echo "== Re-saving the persisted rule set so the deletions survive a reboot =="
# Step 6 wrote /etc/iptables/rules.v4. If we do not re-save, the lab's DROP rule
# comes back on the next boot and silently breaks later labs.
if command -v netfilter-persistent >/dev/null 2>&1; then
  netfilter-persistent save && echo "re-saved /etc/iptables/rules.v4 without the lab rules"
else
  echo "netfilter-persistent not installed — nothing was persisted, nothing to re-save"
fi

echo
echo "Remaining INPUT rules mentioning 3306 (should be none):"
iptables -L INPUT -n --line-numbers 2>/dev/null | grep "3306" || echo "(none)"
echo "Cleanup done — the box is back to its pre-lab state."
