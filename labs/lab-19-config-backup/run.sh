#!/usr/bin/env bash
# Lab 19 — Configuration Backup with Git
# Runs README steps 1-6: install git, init the repo in /etc, baseline the
# network configs, make a change, commit it, inspect the audit trail, roll back.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install git =="
apt update && apt install -y git

echo
echo "== Step 2 — Initialise a repo in /etc =="
cd /etc
git init
git config user.email "netadmin@lab.local"
git config user.name  "Net Admin"

echo
echo "== Step 3 — Add critical network configs =="
git add hosts hostname resolv.conf network/ bind/ 2>/dev/null || true
git commit -m "baseline: initial network configuration"

echo
echo "== Step 4 — Make a change and commit it =="
echo "127.0.1.2 lab-vm" >> /etc/hosts
git -C /etc diff hosts
git -C /etc add hosts
git -C /etc commit -m "add lab-vm hostname mapping"

echo
echo "== Step 5 — Inspect the audit trail =="
git -C /etc log --oneline
git -C /etc show HEAD

echo
echo "== Step 6 — Roll back =="
git -C /etc revert HEAD --no-edit
cat /etc/hosts

echo
echo "Three commits should now exist. Run ./verify.sh"
