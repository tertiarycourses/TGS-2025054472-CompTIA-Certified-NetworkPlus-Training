#!/usr/bin/env bash
# Lab 30 — restore the ORIGINAL /etc/resolv.conf saved by break.sh.
# Tolerant: keep going even if one step has already been undone.
set -uo pipefail

BAK=/tmp/resolv.conf.bak
SYMLINK_NOTE=/tmp/resolv.conf.symlink

if [ -f "$SYMLINK_NOTE" ]; then
  TARGET=$(cat "$SYMLINK_NOTE")
  rm -f /etc/resolv.conf
  ln -s "$TARGET" /etc/resolv.conf && echo "Restored /etc/resolv.conf symlink -> $TARGET"
  rm -f "$SYMLINK_NOTE"
elif [ -f "$BAK" ]; then
  cp "$BAK" /etc/resolv.conf && echo "Restored /etc/resolv.conf from $BAK"
else
  echo "No backup found at $BAK — writing a known-good public resolver instead."
  printf 'nameserver 1.1.1.1\nnameserver 8.8.8.8\n' > /etc/resolv.conf
fi

echo "== Flushing the systemd-resolved cache (README Step 6) =="
resolvectl flush-caches 2>/dev/null && echo "caches flushed" || echo "resolvectl not available — skipped"

echo
echo "Current resolver configuration:"
cat /etc/resolv.conf

echo
echo "Cleanup done — run ./verify.sh to confirm resolution is working again."
