#!/usr/bin/env bash
# Lab 21 — reverse everything this lab created (README Steps 6-7).
# CRITICAL: a lab that leaves a default-deny firewall active breaks every later
# lab, so this script removes only the two rules the lab added and then disables
# ufw so the box is back to its open, pre-lab state.
# Tolerant: keep going even if a rule is already gone.
set -uo pipefail

if ! command -v ufw >/dev/null 2>&1; then
  echo "ufw is not installed — nothing to clean up."
  exit 0
fi

echo "== Deleting only the rules this lab added =="
ufw delete allow from 10.0.0.0/8 to any port 3306 proto tcp 2>/dev/null \
  && echo "deleted: 3306/tcp from 10.0.0.0/8" || echo "rule 3306/tcp from 10.0.0.0/8 already gone"
ufw delete allow 22/tcp 2>/dev/null \
  && echo "deleted: 22/tcp allow" || echo "rule 22/tcp already gone"

echo "== Restoring the permissive default so later labs are not blocked =="
ufw default allow incoming
ufw default allow outgoing

echo "== Disabling the firewall (README Step 7) =="
ufw disable

echo
echo "Remaining ufw state:"
ufw status verbose 2>/dev/null || true
echo "Cleanup done — inbound traffic is unfiltered again and the box is ready for Lab 22."
