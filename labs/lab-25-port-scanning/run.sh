#!/usr/bin/env bash
# Lab 25 — Port Scanning and Service Hardening
# Runs the scan sequence of README Steps 1-5 and 7, echoing each phase.
# This does NOT replace the README — every command below is shown there with its
# explanation. The script exists so the full-port scan can run unattended.
#
# Scan ONLY 127.0.0.1 (your own playground host). Scanning any address you do not
# own is unlawful in Singapore under the Computer Misuse Act.
set -euo pipefail

TARGET=127.0.0.1
OUT=scan-results.txt

echo "== Step 1: install nmap =="
apt update && apt install -y nmap

: > "$OUT"

echo
echo "== Step 2: SYN scan of all 65535 TCP ports on $TARGET =="
echo "   (this is the slow one — several minutes is normal)"
{ echo "### Step 2 — nmap -sS -p- $TARGET"; nmap -sS -p- "$TARGET"; echo; } | tee -a "$OUT"

echo
echo "== Step 3: service/version enumeration on 22,80,443 =="
{ echo "### Step 3 — nmap -sV -p 22,80,443 $TARGET"; nmap -sV -p 22,80,443 "$TARGET"; echo; } | tee -a "$OUT"

echo
echo "== Step 4: OS fingerprint =="
{ echo "### Step 4 — nmap -O $TARGET"; nmap -O "$TARGET" || true; echo; } | tee -a "$OUT"

echo
echo "== Step 5: cross-check the listeners with ss =="
{ echo "### Step 5 — ss -tulnp"; ss -tulnp; echo; } | tee -a "$OUT"

echo
echo "== Step 7: re-scan port 80 to confirm closure =="
{ echo "### Step 7 — nmap -sS -p 80 $TARGET"; nmap -sS -p 80 "$TARGET"; echo; } | tee -a "$OUT"

echo
echo "Full output saved to $OUT."
echo "Now transcribe every open port into data/port-scan-findings.csv and decide,"
echo "for each one: do I need this service running?"
