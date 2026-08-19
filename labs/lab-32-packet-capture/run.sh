#!/usr/bin/env bash
# Lab 32 — Packet Capture and Filtering with tcpdump and the TIS PCAP Analyzer
# Runs the capture + filter sequence from README steps 1-6, ending with the
# base64 export you paste into your laptop for the TIS PCAP Analyzer.
# Every command below is exactly what the README shows.
set -euo pipefail

echo "== Step 1 — Install both tools =="
export DEBIAN_FRONTEND=noninteractive
apt update && apt install -y tcpdump tshark

echo
echo "== Step 2 — Capture 10 DNS packets from this host =="
tcpdump -i eth0 -nn -w /tmp/dns.pcap 'udp port 53 and src host 127.0.0.1' -c 10 &
sleep 1
for d in example.com cloudflare.com github.com; do dig +short @1.1.1.1 "$d"; done
wait

echo
echo "== Step 3 — Read the file with tshark =="
tshark -r /tmp/dns.pcap -Y "dns" -T fields \
  -e frame.time_relative -e dns.qry.name -e dns.qry.type

echo
echo "== Step 4 — Filter only response packets =="
tshark -r /tmp/dns.pcap -Y "dns.flags.response==1"

echo
echo "== Step 5 — Generate a friendly summary =="
tcpdump -nn -r /tmp/dns.pcap | head

echo
echo "== Step 6 — Export the .pcap for download =="
ls -lh /tmp/dns.pcap
base64 /tmp/dns.pcap > /tmp/dns.pcap.b64
echo "Base64 written to /tmp/dns.pcap.b64 ($(wc -c < /tmp/dns.pcap.b64) bytes)."
echo "Print it with:  cat /tmp/dns.pcap.b64"
echo "Then decode on your laptop:  base64 -d dns.pcap.b64 > dns.pcap"

echo
echo "== Step 7 — Analyse in the TIS PCAP Analyzer =="
echo "  https://alfredang.github.io/pcapanalyzer/   (upload dns.pcap)"
echo
echo "Now run ./verify.sh"
