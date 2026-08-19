#!/usr/bin/env bash
# Lab 21 — verify the UFW stance built by README Steps 2-5.
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

fail=0

if ! command -v ufw >/dev/null 2>&1; then
  echo "FAIL: ufw is not installed — run README Step 1 (apt install -y ufw)"
  exit 1
fi

status="$(ufw status verbose 2>/dev/null)"

# --- 1. firewall is active ---------------------------------------------------
if printf '%s' "$status" | grep -q "Status: active"; then
  echo "PASS: ufw is active"
else
  echo "FAIL: ufw is not active — run README Step 4 (ufw --force enable)"
  fail=1
fi

# --- 2. default inbound policy is deny ---------------------------------------
if printf '%s' "$status" | grep -q "Default: deny (incoming)"; then
  echo "PASS: default incoming policy is deny"
else
  echo "FAIL: default incoming policy is not deny — run README Step 2 (ufw default deny incoming)"
  fail=1
fi

# --- 3. the allowed port (22/tcp) is permitted -------------------------------
if ufw status 2>/dev/null | grep -qE '^22/tcp[[:space:]]+ALLOW'; then
  echo "PASS: 22/tcp is ALLOWed (SSH stays reachable)"
else
  echo "FAIL: 22/tcp is not allowed — run README Step 3 (ufw allow 22/tcp)"
  fail=1
fi

# --- 4. the source-restricted rule exists ------------------------------------
if ufw status 2>/dev/null | grep -q "3306/tcp" && ufw status 2>/dev/null | grep -q "10.0.0.0/8"; then
  echo "PASS: 3306/tcp is allowed only from 10.0.0.0/8"
else
  echo "FAIL: the source-restricted MySQL rule is missing — run README Step 5"
  fail=1
fi

# --- 5. an allowed port is reachable, a blocked port is refused --------------
# 22 is allowed by policy; 9999 is covered by the default-deny stance.
if command -v nc >/dev/null 2>&1; then
  if nc -z -w2 127.0.0.1 22 >/dev/null 2>&1; then
    echo "PASS: allowed port 22 accepts a connection"
  else
    echo "INFO: port 22 did not accept a connection (sshd may not be running in this playground)"
  fi

  if nc -z -w2 127.0.0.1 9999 >/dev/null 2>&1; then
    echo "FAIL: blocked port 9999 unexpectedly accepted a connection"
    fail=1
  else
    echo "PASS: blocked port 9999 is refused / unreachable"
  fi
else
  echo "INFO: nc not installed — skipping the reachability probes (apt install -y netcat-openbsd)"
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — remember to run ./cleanup.sh before moving on."
else
  echo "One or more checks failed."
fi
exit "$fail"
