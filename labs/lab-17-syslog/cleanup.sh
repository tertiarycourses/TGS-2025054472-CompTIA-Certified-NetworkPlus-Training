#!/usr/bin/env bash
# Lab 17 — remove the forwarding rule this lab installed and restart rsyslog
# so the next lab starts on a clean logging pipeline. Reverses Step 2 only;
# the imtcp module lines in /etc/rsyslog.conf are left commented back out.
set -uo pipefail

echo "== Removing the lab forwarding rule =="
rm -f /etc/rsyslog.d/50-forward.conf
echo "/etc/rsyslog.d/50-forward.conf removed"

echo "== Disabling the imtcp receiver =="
sed -i 's/^module(load="imtcp")/#module(load="imtcp")/' /etc/rsyslog.conf
sed -i 's/^input(type="imtcp" port="514")/#input(type="imtcp" port="514")/' /etc/rsyslog.conf

echo "== Restarting rsyslog =="
systemctl restart rsyslog 2>/dev/null || true

echo "Cleanup complete — rsyslog no longer listens on TCP/514."
