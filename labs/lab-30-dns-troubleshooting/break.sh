#!/usr/bin/env bash
# Lab 30 — fault injection: point the system at a dead resolver.
#
# This SAVES /etc/resolv.conf to /tmp/resolv.conf.bak FIRST, then replaces it
# with a nameserver on a black-holed RFC1918 address. Resolution will hang and
# then fail — your job is to diagnose it with the README Step 2/3 commands.
#
# ALWAYS recoverable:  ./cleanup.sh   (restores /tmp/resolv.conf.bak)
set -euo pipefail

BAK=/tmp/resolv.conf.bak

if [ -e "$BAK" ]; then
  echo "Backup $BAK already exists — leaving it untouched (it holds the ORIGINAL)."
else
  cp /etc/resolv.conf "$BAK"
  echo "Saved original /etc/resolv.conf to $BAK"
fi

# /etc/resolv.conf is often a symlink to a systemd-resolved stub. Replace the
# symlink with a real file so the broken nameserver actually takes effect.
if [ -L /etc/resolv.conf ]; then
  LINK_TARGET=$(readlink /etc/resolv.conf)
  echo "$LINK_TARGET" > /tmp/resolv.conf.symlink
  echo "Noted that /etc/resolv.conf was a symlink to $LINK_TARGET"
  rm -f /etc/resolv.conf
fi

cat > /etc/resolv.conf <<'EOF'
# Injected by Lab 30 break.sh — this resolver does not exist.
nameserver 10.99.0.53
options timeout:2 attempts:1
EOF

echo
echo "FAULT INJECTED — /etc/resolv.conf now points at 10.99.0.53 (black hole)."
echo
echo "Reproduce the symptom:"
echo "    dig example.com +short          # times out / no answer"
echo "    ping -c2 example.com            # Temporary failure in name resolution"
echo
echo "Now diagnose it using README Step 2 and Step 3:"
echo "    cat /etc/resolv.conf"
echo "    resolvectl status | head -20"
echo "    dig @1.1.1.1 example.com +short   # works -> the resolver is the fault, not the network"
echo "    dig @8.8.8.8 example.com +short"
echo
echo "When you have found it:  ./cleanup.sh   then  ./verify.sh"
