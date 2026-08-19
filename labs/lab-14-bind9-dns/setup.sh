#!/usr/bin/env bash
# Lab 14 — Authoritative DNS with BIND9
# Runs README Steps 1-4: install, install the zone file, register the zone,
# validate and reload.
#
#   ./setup.sh            core lab only (forward zone lab.local)
#   ./setup.sh --reverse  also install the optional reverse zone (Step 7 bonus)
#
# Idempotent: safe to re-run — it never appends the same zone block twice.
# Must be run from the lab folder so ./db.lab.local resolves.
set -euo pipefail

cd "$(dirname "$0")"
WANT_REVERSE=0
if [ "${1:-}" = "--reverse" ]; then WANT_REVERSE=1; fi

echo "== Step 1: install BIND9 =="
apt update && apt install -y bind9 dnsutils

echo "== Step 2: install the zone file =="
cp ./db.lab.local /etc/bind/db.lab.local
echo "installed /etc/bind/db.lab.local"

echo "== Step 3: register the zone =="
if [ -f /etc/bind/named.conf.local ] && [ ! -f /etc/bind/named.conf.local.lab14.bak ]; then
  cp /etc/bind/named.conf.local /etc/bind/named.conf.local.lab14.bak
fi
if grep -q 'zone "lab.local"' /etc/bind/named.conf.local 2>/dev/null; then
  echo "zone lab.local already registered — not appending again"
else
  cat ./named.conf.local >> /etc/bind/named.conf.local
  echo "appended the lab.local zone block to /etc/bind/named.conf.local"
fi

if [ "$WANT_REVERSE" -eq 1 ]; then
  echo "== Step 7 bonus: install and register the reverse zone =="
  cp ./db.10.0.0 /etc/bind/db.10.0.0
  if grep -q 'zone "0.0.10.in-addr.arpa"' /etc/bind/named.conf.local 2>/dev/null; then
    echo "reverse zone already registered — not appending again"
  else
    cat ./named.conf.local.reverse >> /etc/bind/named.conf.local
    echo "appended the reverse zone block"
  fi
fi

echo "== Step 4: validate and reload =="
named-checkconf
named-checkzone lab.local /etc/bind/db.lab.local
if [ "$WANT_REVERSE" -eq 1 ]; then
  named-checkzone 0.0.10.in-addr.arpa /etc/bind/db.10.0.0
fi
systemctl restart bind9

echo
echo "BIND9 is authoritative for lab.local. Now run ./verify.sh"
