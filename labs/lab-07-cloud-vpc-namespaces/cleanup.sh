#!/usr/bin/env bash
# Lab 7 — tear down the simulated VPC (README Step 6).
# Deleting a namespace also deletes the veth end inside it, and deleting one
# end of a veth pair removes the other, so br-web / br-db disappear with them.
set -uo pipefail

echo "== Step 6 — Clean up =="

for ns in web db; do
  if ip netns del "$ns" 2>/dev/null; then
    echo "  deleted namespace $ns"
  else
    echo "  namespace $ns already gone"
  fi
done

if ip link del br0 2>/dev/null; then
  echo "  deleted bridge br0"
else
  echo "  bridge br0 already gone"
fi

# Safety net: if setup aborted before moving the veths into the namespaces,
# the host-side ends may still exist. Remove only the interfaces this lab created.
for link in veth-web veth-db br-web br-db; do
  if ip link show "$link" >/dev/null 2>&1; then
    ip link del "$link" 2>/dev/null && echo "  deleted leftover interface $link"
  fi
done

echo
echo "Remaining namespaces:"
ip netns list || echo "  (none)"

echo
echo "Cleanup complete."
