#!/usr/bin/env bash
# Lab 24 — verify the tunnel of README Steps 4-6: handshake established and
# traffic crosses the tunnel.
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

fail=0

# --- 1. both namespaces exist -------------------------------------------------
for n in site-a site-b; do
  if ip netns list 2>/dev/null | grep -qw "$n"; then
    echo "PASS: namespace $n exists"
  else
    echo "FAIL: namespace $n missing — re-run README Step 2 (ip netns add $n)"
    fail=1
  fi
done

# --- 2. wg0 is up in both, with the right address -----------------------------
check_addr() {   # $1 = netns, $2 = expected address
  if ip -n "$1" addr show wg0 2>/dev/null | grep -q "inet $2/24"; then
    echo "PASS: $1 wg0 has $2/24"
  else
    echo "FAIL: $1 wg0 does not have $2/24 — re-run README Step 4"
    fail=1
  fi
  if ip -n "$1" link show wg0 2>/dev/null | grep -q "state UNKNOWN\|UP"; then
    echo "PASS: $1 wg0 is up"
  else
    echo "FAIL: $1 wg0 is not up — run 'ip -n $1 link set wg0 up' (README Step 5)"
    fail=1
  fi
}
check_addr site-a 10.99.0.1
check_addr site-b 10.99.0.2

# --- 3. each peer knows the other's public key --------------------------------
a_pub="$(ip netns exec site-a wg show wg0 public-key 2>/dev/null)"
b_pub="$(ip netns exec site-b wg show wg0 public-key 2>/dev/null)"
if [ -n "$a_pub" ] && ip netns exec site-b wg show wg0 peers 2>/dev/null | grep -qF "$a_pub"; then
  echo "PASS: site-b lists site-a's public key as a peer"
else
  echo "FAIL: site-b does not have site-a configured as a peer — re-run README Step 4"
  fail=1
fi
if [ -n "$b_pub" ] && ip netns exec site-a wg show wg0 peers 2>/dev/null | grep -qF "$b_pub"; then
  echo "PASS: site-a lists site-b's public key as a peer"
else
  echo "FAIL: site-a does not have site-b configured as a peer — re-run README Step 4"
  fail=1
fi

# --- 4. traffic crosses the tunnel (README Step 5) ----------------------------
if ip netns exec site-b ping -c2 -W3 10.99.0.1 >/dev/null 2>&1; then
  echo "PASS: site-b can ping 10.99.0.1 across the tunnel"
else
  echo "FAIL: ping across the tunnel failed — check the endpoint and allowed-ips"
  fail=1
fi

# --- 5. a handshake has actually completed (README Step 6) --------------------
# `wg show wg0 latest-handshakes` prints "<peer> <unix-timestamp>"; 0 means never.
hs="$(ip netns exec site-a wg show wg0 latest-handshakes 2>/dev/null | awk '{print $2}' | sort -rn | head -1)"
if [ "${hs:-0}" -gt 0 ] 2>/dev/null; then
  echo "PASS: handshake established on site-a (latest-handshake epoch $hs)"
else
  echo "FAIL: no handshake on site-a — the peers have not authenticated each other"
  fail=1
fi

# --- 6. encrypted bytes have moved --------------------------------------------
rx="$(ip netns exec site-a wg show wg0 transfer 2>/dev/null | awk '{print $2}' | head -1)"
if [ "${rx:-0}" -gt 0 ] 2>/dev/null; then
  echo "PASS: site-a has received $rx encrypted bytes from the peer"
else
  echo "FAIL: no encrypted bytes received on site-a"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — run ./cleanup.sh to tear the tunnel down."
else
  echo "One or more checks failed. 'ip netns exec site-a wg show' shows the full state."
fi
exit "$fail"
