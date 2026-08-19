#!/usr/bin/env bash
# Lab 13 — objective pass/fail check.
# Tolerant on purpose: one failed check must not abort the remaining checks.
set -uo pipefail

fails=0
check() {  # check <description> <command...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    fails=$((fails + 1))
  fi
}

echo "== Lab 13 verification =="

check "isc-dhcp-server is installed" \
  bash -c "command -v dhcpd"
check "dum0 exists and carries 10.50.0.1/24" \
  bash -c "ip -4 addr show dev dum0 | grep -q '10.50.0.1/24'"
check "/etc/dhcp/dhcpd.conf declares subnet 10.50.0.0" \
  bash -c "grep -q 'subnet 10.50.0.0 netmask 255.255.255.0' /etc/dhcp/dhcpd.conf"
check "the scope hands out range 10.50.0.100 - 10.50.0.150" \
  bash -c "grep -q 'range 10.50.0.100 10.50.0.150' /etc/dhcp/dhcpd.conf"
check "the scope sets option routers 10.50.0.1" \
  bash -c "grep -q 'option routers 10.50.0.1' /etc/dhcp/dhcpd.conf"
check "dhcpd.conf parses cleanly (dhcpd -t)" \
  dhcpd -t -cf /etc/dhcp/dhcpd.conf
check "the daemon is bound to dum0 in /etc/default/isc-dhcp-server" \
  bash -c "grep -q '^INTERFACESv4=\"dum0\"' /etc/default/isc-dhcp-server"

# The Test-it check from the README: the service is running and the lease
# database exists.
check "isc-dhcp-server service is active" \
  systemctl is-active --quiet isc-dhcp-server
check "the lease database /var/lib/dhcp/dhcpd.leases exists" \
  test -f /var/lib/dhcp/dhcpd.leases

if systemctl is-active --quiet isc-dhcp-server; then
  echo "-- dhcpd is listening; recent journal lines --"
  journalctl -u isc-dhcp-server -n 5 --no-pager 2>/dev/null || true
fi

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 13 complete — dhcpd is running with the 10.50.0.0/24 scope on dum0."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
exit 1
