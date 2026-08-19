#!/usr/bin/env bash
# Lab 14 — reverse everything the lab created (README Step 6).
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Stopping BIND9 =="
systemctl stop bind9 2>/dev/null && echo "stopped bind9" || echo "bind9 was not running"

echo "== Restoring the packaged named.conf.local =="
if [ -f /etc/bind/named.conf.local.lab14.bak ]; then
  cp /etc/bind/named.conf.local.lab14.bak /etc/bind/named.conf.local
  echo "restored /etc/bind/named.conf.local from the pre-lab backup"
  echo "(the lab.local and reverse zone blocks are gone)"
else
  echo "no pre-lab backup found — /etc/bind/named.conf.local left as-is"
fi

echo "== Removing the zone files this lab installed =="
# Exactly the two files setup.sh copied in — nothing else under /etc/bind is
# touched, and no directory is ever removed.
for f in /etc/bind/db.lab.local /etc/bind/db.10.0.0; do
  rm -f "$f" 2>/dev/null && echo "removed $f" || true
done

echo "Cleanup done — no lab.local zone is served any more."
