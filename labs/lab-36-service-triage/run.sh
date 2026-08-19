#!/usr/bin/env bash
# Lab 36 — Service Reachability Triage (curl, nc, openssl)
# Runs the layered triage sequence from README steps 1-5.
# Every command below is exactly what the README shows.
# Record what each layer tells you in troubleshooting-worksheet.md.
set -euo pipefail

echo "== Step 1 — Install the tools =="
apt update && apt install -y curl netcat-openbsd openssl

echo
echo "== Step 2 — Layer 4 reachability (TCP handshake only) =="
nc -zv example.com 443 || echo "(nc failed -> routing or firewall: go to traceroute / mtr, Lab 29)"

echo
echo "== Step 3 — Layer 6 TLS handshake =="
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | head -20

echo
echo "== Step 4 — Layer 7 HTTP =="
curl -v https://example.com 2>&1 | head -30

echo
echo "== Step 5 — Timing breakdown (which phase is slow?) =="
curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} TTFB:%{time_starttransfer} TOTAL:%{time_total}\n" \
     -o /dev/null -s https://example.com

echo
echo "== Step 6 — Decision tree =="
echo "  1. nc -zv fails                  -> routing or firewall (traceroute, mtr)"
echo "  2. nc works, s_client fails      -> TLS issue (cert / SNI / protocol)"
echo "  3. TLS works, HTTP 5xx           -> application or upstream"
echo "  4. slow time_namelookup          -> DNS issue (Lab 30)"
echo "  5. slow time_starttransfer       -> server-side processing"

echo
echo "Now complete troubleshooting-worksheet.md using the CompTIA 7-step methodology."
