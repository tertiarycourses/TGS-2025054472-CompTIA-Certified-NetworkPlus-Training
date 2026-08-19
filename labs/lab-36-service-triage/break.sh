#!/usr/bin/env bash
# Lab 36 — fault injection for the capstone: black-hole outbound TCP/443 to
# example.com so the learner meets the ticket cold and works the 7 steps.
#
# This SAVES the current filter table to /tmp/lab36-iptables.bak FIRST, then
# adds ONE reject rule. Nothing else on the box is touched.
#
# ALWAYS recoverable:  ./cleanup.sh   (deletes the rule, restores the backup)
set -euo pipefail

BAK=/tmp/lab36-iptables.bak

if [ -e "$BAK" ]; then
  echo "Backup $BAK already exists — leaving it untouched (it holds the ORIGINAL)."
else
  iptables-save > "$BAK"
  echo "Saved original iptables rules to $BAK"
fi

echo
echo "== Injecting the fault: reject outbound TCP/443 to example.com =="
iptables -A OUTPUT -p tcp --dport 443 -d example.com -j REJECT --reject-with tcp-reset
iptables -L OUTPUT -n --line-numbers | tail -5

echo
echo "FAULT INJECTED — the ticket reads: \"https://example.com is down for everyone.\""
echo
echo "Work the CompTIA 7 steps in troubleshooting-worksheet.md. Start with:"
echo "    nc -zv example.com 443                     # Step 2 - Layer 4"
echo "    echo | openssl s_client -connect example.com:443 -servername example.com"
echo "    curl -v https://example.com"
echo "    ping -c2 example.com                       # ICMP still works - narrows it to TCP/443"
echo "    dig example.com +short                     # DNS still works - not Lab 30"
echo
echo "The Step 6 decision tree tells you which layer failed. Find the rule with:"
echo "    iptables -L OUTPUT -n --line-numbers"
echo
echo "When you have documented it:  ./cleanup.sh"
