#!/usr/bin/env bash
# Lab 13 — DHCP Server with isc-dhcp-server
# Runs README Steps 1-5: install, dummy interface, scope, listen interface, start.
# Idempotent: safe to re-run.
# Must be run from the lab folder so ./dhcpd.conf resolves.
set -euo pipefail

cd "$(dirname "$0")"

echo "== Step 1: install the server =="
apt update && apt install -y isc-dhcp-server

echo "== Step 2: create a dummy interface for the lab =="
if ip link show dum0 >/dev/null 2>&1; then
  echo "dum0 already exists — reusing it"
else
  ip link add dum0 type dummy
fi
ip addr replace 10.50.0.1/24 dev dum0
ip link set dum0 up

echo "== Step 3: configure the scope =="
# Back up whatever the package shipped, once.
if [ -f /etc/dhcp/dhcpd.conf ] && [ ! -f /etc/dhcp/dhcpd.conf.lab13.bak ]; then
  cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.lab13.bak
fi
cp ./dhcpd.conf /etc/dhcp/dhcpd.conf
echo "installed $(pwd)/dhcpd.conf -> /etc/dhcp/dhcpd.conf"

echo "== Step 4: tell the server which interface to listen on =="
sed -i 's/^INTERFACESv4=.*/INTERFACESv4="dum0"/' /etc/default/isc-dhcp-server

echo "== Step 5: start the service =="
systemctl restart isc-dhcp-server
systemctl status isc-dhcp-server --no-pager

echo
echo "DHCP server running on dum0. Now run ./verify.sh"
