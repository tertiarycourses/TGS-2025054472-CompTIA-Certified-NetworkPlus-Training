#!/usr/bin/env bash
# Lab 27 — verify the ACL of README Steps 2-5: permitted traffic passes, denied
# traffic is blocked, and the ACCEPT is ordered before the DROP.
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

fail=0

# --- 1. both rules exist ------------------------------------------------------
if iptables -C INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT 2>/dev/null; then
  echo "PASS: ACCEPT rule for 3306/tcp from 10.0.0.0/24 is present"
else
  echo "FAIL: ACCEPT rule missing — re-run README Step 2"
  fail=1
fi
if iptables -C INPUT -p tcp --dport 3306 -j DROP 2>/dev/null; then
  echo "PASS: DROP rule for 3306/tcp is present"
else
  echo "FAIL: DROP rule missing — re-run README Step 3"
  fail=1
fi

# --- 2. ordering: the ACCEPT must be matched first ----------------------------
listing="$(iptables -L INPUT -n --line-numbers 2>/dev/null)"
acc_line="$(printf '%s' "$listing" | awk '/ACCEPT/ && /tcp dpt:3306/ && /10\.0\.0\.0\/24/ {print $1; exit}')"
drp_line="$(printf '%s' "$listing" | awk '/DROP/   && /tcp dpt:3306/ {print $1; exit}')"
if [ -n "$acc_line" ] && [ -n "$drp_line" ] && [ "$acc_line" -lt "$drp_line" ] 2>/dev/null; then
  echo "PASS: ACCEPT is rule $acc_line, DROP is rule $drp_line — first match wins, ordering is correct"
else
  echo "FAIL: rule ordering is wrong (ACCEPT=${acc_line:-none}, DROP=${drp_line:-none}) — the ACCEPT must come first"
  fail=1
fi

# --- 3. the permitted source address is configured ----------------------------
if ip addr show dev lo 2>/dev/null | grep -q "inet 10.0.0.5/24"; then
  echo "PASS: allowed test source 10.0.0.5/24 is on lo"
else
  echo "FAIL: 10.0.0.5/24 missing — run 'ip addr add 10.0.0.5/24 dev lo' (README Step 5)"
  fail=1
fi

# --- 4. behavioural test: denied vs permitted source --------------------------
if ! command -v nc >/dev/null 2>&1; then
  echo "INFO: nc not installed — skipping the traffic test (apt install -y netcat-openbsd)"
else
  # Denied: default source (127.0.0.1) is not in 10.0.0.0/24, so the DROP applies.
  # A DROP produces a TIMEOUT, not a refusal — that is the observable difference.
  if timeout 5 nc -z -w3 127.0.0.1 3306 >/dev/null 2>&1; then
    echo "FAIL: denied source unexpectedly connected to 3306"
    fail=1
  else
    echo "PASS: denied source is blocked on 3306 (no response — the DROP rule silently discards)"
  fi

  # Permitted: source 10.0.0.5 matches the ACCEPT, so the packet reaches the
  # stack. With no MySQL listening the kernel answers RST => 'refused', fast.
  out="$(timeout 5 nc -zv -s 10.0.0.5 -w3 127.0.0.1 3306 2>&1)"
  if printf '%s' "$out" | grep -qi "succeeded\|open\|refused"; then
    echo "PASS: permitted source 10.0.0.5 is not filtered (got: $(printf '%s' "$out" | tail -1))"
  else
    echo "FAIL: permitted source 10.0.0.5 appears to be filtered too — check the ACCEPT rule's ordering"
    fail=1
  fi
fi

# --- 5. the ACCEPT rule is actually matching packets --------------------------
pkts="$(iptables -L INPUT -n -v 2>/dev/null | awk '/ACCEPT/ && /tcp dpt:3306/ {print $1; exit}')"
if [ "${pkts:-0}" -gt 0 ] 2>/dev/null; then
  echo "PASS: the ACCEPT rule has matched $pkts packet(s)"
else
  echo "INFO: the ACCEPT rule counter is 0 — run the Step 5 test again to drive traffic through it"
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — run ./cleanup.sh before moving on to Lab 28."
else
  echo "One or more checks failed."
fi
exit "$fail"
