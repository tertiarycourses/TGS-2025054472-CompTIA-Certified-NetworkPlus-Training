#!/usr/bin/env bash
# Lab 24 — reverse everything this lab created (README Step 7).
# Tears the wg0 interfaces down, deletes the two namespaces, and shreds the
# generated key material from /tmp. Touches nothing else on the box.
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Bringing the wg0 interfaces down =="
for n in site-a site-b; do
  ip -n "$n" link set wg0 down 2>/dev/null && echo "$n wg0 down" || true
  ip -n "$n" link del wg0      2>/dev/null && echo "$n wg0 deleted" || true
done

echo "== Deleting the namespaces site-a and site-b =="
for n in site-a site-b; do
  ip netns del "$n" 2>/dev/null && echo "deleted netns $n" || echo "netns $n already gone"
done

echo "== Removing the generated key material and working configs =="
for f in /tmp/a.key /tmp/a.pub /tmp/b.key /tmp/b.pub /tmp/wg0-a.conf /tmp/wg0-b.conf; do
  [ -e "$f" ] && rm -f "$f" && echo "removed $f"
done

echo
echo "Remaining WireGuard interfaces on the host (should be none):"
wg show interfaces 2>/dev/null || echo "(wg reports no interfaces)"
echo "Cleanup done — no tunnel and no private keys remain."
