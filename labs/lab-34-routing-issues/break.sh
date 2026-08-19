#!/usr/bin/env bash
# Lab 34 — fault injection: delete the default route.
#
# This SAVES the current default route to /tmp/default-route.bak FIRST, then
# deletes it. The box will still reach its own subnet but nothing beyond it —
# the classic "I can ping this but not that" ticket.
#
# ALWAYS recoverable:  ./cleanup.sh   (re-adds the saved default route)
set -euo pipefail

BAK=/tmp/default-route.bak

DEF=$(ip route show default | head -1)
if [ -z "$DEF" ]; then
  echo "No default route present — has break.sh already run? Try ./cleanup.sh"
  exit 1
fi

if [ -e "$BAK" ]; then
  echo "Backup $BAK already exists — leaving it untouched (it holds the ORIGINAL)."
else
  printf '%s\n' "$DEF" > "$BAK"
  echo "Saved original default route to $BAK:"
  echo "    $DEF"
fi

GW=$(printf '%s\n' "$DEF" | awk '{print $3}')

echo
echo "== Deleting the default route =="
ip route del default
ip route

echo
echo "FAULT INJECTED — there is no gateway of last resort."
echo
echo "Reproduce the symptom:"
echo "    ping -c2 $GW        # the local gateway still answers (same subnet)"
echo "    ping -c2 8.8.8.8    # Network is unreachable"
echo
echo "Now diagnose it using README Step 1 and Step 2:"
echo "    ip route                 # no 'default via ...' line"
echo "    ip route get 8.8.8.8     # RTNETLINK answers: Network is unreachable"
echo "    ip route get 10.99.0.5   # also unreachable - nothing matches"
echo
echo "When you have found it:  ./cleanup.sh   then  ./verify.sh"
