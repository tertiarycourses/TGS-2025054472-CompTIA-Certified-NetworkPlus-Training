#!/usr/bin/env bash
# Lab 32 — verify the DNS capture from README Step 2 exists, is non-empty and
# holds decodable DNS packets ready for the TIS PCAP Analyzer.
set -uo pipefail

PCAP=/tmp/dns.pcap
B64=/tmp/dns.pcap.b64
fail=0

if [ -f "$PCAP" ]; then
  echo "PASS: $PCAP exists"
else
  echo "FAIL: $PCAP not found — re-run README Step 2 (tcpdump -w /tmp/dns.pcap ...)"
  fail=1
fi

if [ -s "$PCAP" ]; then
  echo "PASS: $PCAP is non-empty ($(wc -c < "$PCAP") bytes)"
else
  echo "FAIL: $PCAP is empty — no packets captured, make sure the dig loop runs while tcpdump is active"
  fail=1
fi

if command -v tcpdump >/dev/null 2>&1 && [ -s "$PCAP" ]; then
  count=$(tcpdump -nn -r "$PCAP" 2>/dev/null | wc -l | tr -d ' ')
  if [ "${count:-0}" -gt 0 ]; then
    echo "PASS: $PCAP decodes to $count packet(s)"
  else
    echo "FAIL: $PCAP contains no readable packets"
    fail=1
  fi
fi

if command -v tshark >/dev/null 2>&1 && [ -s "$PCAP" ]; then
  q=$(tshark -r "$PCAP" -Y "dns" -T fields -e dns.qry.name 2>/dev/null | sort -u | grep -c . )
  if [ "${q:-0}" -gt 0 ]; then
    echo "PASS: capture contains $q distinct DNS query name(s)"
  else
    echo "FAIL: no DNS queries found — check the BPF filter 'udp port 53 and src host 127.0.0.1'"
    fail=1
  fi
fi

if [ -s "$B64" ]; then
  echo "PASS: $B64 exists — paste it into your laptop and decode for the analyzer"
else
  echo "FAIL: $B64 not found — re-run README Step 6 (base64 /tmp/dns.pcap > /tmp/dns.pcap.b64)"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — upload dns.pcap to https://alfredang.github.io/pcapanalyzer/"
else
  echo "One or more checks failed."
fi
exit "$fail"
