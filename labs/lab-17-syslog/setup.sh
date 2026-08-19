#!/usr/bin/env bash
# Lab 17 — Centralised Logging with Rsyslog
# Runs README steps 1-3: enable the imtcp receiver, install the forwarding
# rule, restart rsyslog and show the listening socket. Idempotent.
set -euo pipefail

echo "== Step 1 — Enable the TCP receiver =="
sed -i 's/#module(load="imtcp")/module(load="imtcp")/' /etc/rsyslog.conf
sed -i 's/#input(type="imtcp" port="514")/input(type="imtcp" port="514")/' /etc/rsyslog.conf
grep -E 'imtcp' /etc/rsyslog.conf || true

echo
echo "== Step 2 — Add a forwarding rule =="
echo '*.* @@127.0.0.1:514' > /etc/rsyslog.d/50-forward.conf
cat /etc/rsyslog.d/50-forward.conf

echo
echo "== Step 3 — Restart rsyslog =="
systemctl restart rsyslog
sleep 2
ss -tlnp | grep 514 || echo "WARNING: nothing listening on :514 yet"

echo
echo "Receiver is up. Continue with README Step 4, or run ./verify.sh"
