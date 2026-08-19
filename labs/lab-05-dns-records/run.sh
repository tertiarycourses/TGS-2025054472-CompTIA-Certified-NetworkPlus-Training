#!/usr/bin/env bash
# Lab 5 — DNS Record Types
# Runs every dig query from README steps 1-10 in sequence.
# Each command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install dnsutils =="
apt update && apt install -y dnsutils

echo
echo "== Step 2 — A record (hostname -> IPv4) =="
dig +short A google.com

echo
echo "== Step 3 — AAAA record (hostname -> IPv6) =="
dig +short AAAA google.com

echo
echo "== Step 4 — MX record (mail exchanger; lower number = preferred) =="
dig +short MX google.com

echo
echo "== Step 5 — TXT record (SPF, DKIM, domain verification) =="
dig +short TXT google.com

echo
echo "== Step 6 — NS records (authoritative nameservers) =="
dig +short NS google.com

echo
echo "== Step 7 — CNAME (canonical alias -> another name, not an IP) =="
dig +short CNAME www.github.com

echo
echo "== Step 8 — PTR via reverse lookup (IP -> name) =="
dig +short -x 8.8.8.8

echo
echo "== Step 9 — SOA (zone authority: primary NS, admin email, serial, timers) =="
dig +short SOA google.com

echo
echo "== Step 10 — SRV record (service location) =="
dig +short SRV _xmpp-server._tcp.gmail.com

echo
echo "All ten record types queried. Compare each answer against data/dns-records.csv."
