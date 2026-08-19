#!/usr/bin/env bash
# Lab 21 — Host Firewall with UFW
# Builds the firewall stance of README Steps 1-5.
# Idempotent: safe to re-run (ufw rules are not duplicated by ufw itself).
set -euo pipefail

echo "== Step 1: install ufw =="
apt update && apt install -y ufw

echo "== Step 2: set sane defaults (deny in / allow out) =="
ufw default deny incoming
ufw default allow outgoing

echo "== Step 3: allow SSH (port 22) BEFORE enabling =="
ufw allow 22/tcp

echo "== Step 4: enable the firewall =="
ufw --force enable
ufw status verbose

echo "== Step 5: add the source-restricted MySQL rule =="
ufw allow from 10.0.0.0/8 to any port 3306 proto tcp
ufw status numbered

echo
echo "Firewall active. Now run ./verify.sh — and ALWAYS run ./cleanup.sh before the next lab."
