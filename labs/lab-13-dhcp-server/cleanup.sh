#!/usr/bin/env bash
# Lab 13 — reverse everything the lab created (README Step 7).
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Stopping the DHCP server =="
systemctl stop isc-dhcp-server 2>/dev/null && echo "stopped isc-dhcp-server" || echo "isc-dhcp-server was not running"

echo "== Deleting the dummy interface =="
ip link del dum0 2>/dev/null && echo "deleted dum0" || echo "dum0 already gone"

echo "== Restoring the packaged dhcpd.conf =="
if [ -f /etc/dhcp/dhcpd.conf.lab13.bak ]; then
  cp /etc/dhcp/dhcpd.conf.lab13.bak /etc/dhcp/dhcpd.conf
  echo "restored /etc/dhcp/dhcpd.conf from the pre-lab backup"
else
  echo "no pre-lab backup found — /etc/dhcp/dhcpd.conf left as-is"
fi

echo "Cleanup done — no DHCP server is serving the lab subnet."
