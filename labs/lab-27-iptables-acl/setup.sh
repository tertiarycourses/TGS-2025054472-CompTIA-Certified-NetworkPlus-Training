#!/usr/bin/env bash
# Lab 27 — Building an ACL with iptables
# Applies the ACL of README Steps 1-3 and adds the test address from Step 5.
# Idempotent: any previous run of these exact rules is removed first, so the
# chain never accumulates duplicates.
set -euo pipefail

echo "== Step 0: remove any previous run of these exact rules =="
while iptables -C INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT 2>/dev/null; do
  iptables -D INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT
done
while iptables -C INPUT -p tcp --dport 3306 -j DROP 2>/dev/null; do
  iptables -D INPUT -p tcp --dport 3306 -j DROP
done
ip addr del 10.0.0.5/24 dev lo 2>/dev/null || true

echo "== Step 1: current INPUT rules =="
iptables -L INPUT -n -v --line-numbers

echo "== Step 2: allow MySQL from 10.0.0.0/24 only (insert at the top) =="
iptables -I INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT

echo "== Step 3: drop MySQL from everywhere else (append at the bottom) =="
iptables -A INPUT -p tcp --dport 3306 -j DROP

echo "== Step 4: verify ordering — ACCEPT must come before DROP =="
iptables -L INPUT -n -v --line-numbers

echo "== Step 5 prep: add the allowed test source address to lo =="
ip addr add 10.0.0.5/24 dev lo

echo
echo "ACL applied. Now run ./verify.sh — and ALWAYS run ./cleanup.sh before the next lab."
