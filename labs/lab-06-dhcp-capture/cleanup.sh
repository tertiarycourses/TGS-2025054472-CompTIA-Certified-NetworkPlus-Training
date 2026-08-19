#!/usr/bin/env bash
# Lab 6 — restore the box after the DHCP capture lab.
# Stops any tcpdump left running and makes sure eth0 holds a valid DHCP lease
# again, so the next lab starts on a working network.
set -uo pipefail

echo "== Stopping any tcpdump processes started by this lab =="
if pkill -f "tcpdump -i eth0" 2>/dev/null; then
  echo "  stopped tcpdump"
else
  echo "  no tcpdump running"
fi

echo
echo "== Renewing the DHCP lease on eth0 =="
dhclient -v eth0 || echo "  WARNING: dhclient did not complete — check connectivity"

echo
echo "== Current address on eth0 =="
ip -4 addr show eth0

echo
echo "Cleanup complete. eth0 should show a routable IPv4 address above."
