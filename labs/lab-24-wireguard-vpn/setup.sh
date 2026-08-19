#!/usr/bin/env bash
# Lab 24 — Site-to-Site VPN with WireGuard
# Builds the tunnel of README Steps 1-5: site-a (10.99.0.1) <-> site-b (10.99.0.2)
# Idempotent: safe to re-run (it deletes any previous run first).
#
# KEY MATERIAL IS GENERATED HERE, AT RUN TIME. The shipped wg0-a.conf / wg0-b.conf
# carry only <PASTE_..._HERE> placeholders; this script substitutes the freshly
# generated keys into working copies under /tmp. Nothing secret is committed.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== Step 0: remove any previous run =="
for n in site-a site-b; do
  ip netns del "$n" 2>/dev/null || true
done
rm -f /tmp/a.key /tmp/a.pub /tmp/b.key /tmp/b.pub /tmp/wg0-a.conf /tmp/wg0-b.conf

echo "== Step 1: install WireGuard =="
apt update && apt install -y wireguard wireguard-tools

echo "== Step 2: create the two site namespaces =="
ip netns add site-a
ip netns add site-b

echo "== Step 3: generate a key pair for each peer =="
cd /tmp
( umask 077; wg genkey | tee a.key | wg pubkey > a.pub )
( umask 077; wg genkey | tee b.key | wg pubkey > b.pub )
chmod 600 /tmp/a.key /tmp/b.key
echo "site-a public key: $(cat /tmp/a.pub)"
echo "site-b public key: $(cat /tmp/b.pub)"

echo "== Step 4a: create the wg0 interfaces and address them =="
ip -n site-a link add wg0 type wireguard
ip -n site-b link add wg0 type wireguard

ip -n site-a addr add 10.99.0.1/24 dev wg0
ip -n site-b addr add 10.99.0.2/24 dev wg0

echo "== Step 4b: materialise wg0-a.conf / wg0-b.conf with the generated keys =="
# `wg setconf` understands [Interface]/[Peer] but NOT the wg-quick-only Address
# line, so it is dropped from the working copies.
sed -e "s|<PASTE_SITE_A_PRIVATE_KEY_HERE>|$(cat /tmp/a.key)|" \
    -e "s|<PASTE_SITE_B_PUBLIC_KEY_HERE>|$(cat /tmp/b.pub)|" \
    -e '/^Address/d' \
    "$HERE/wg0-a.conf" > /tmp/wg0-a.conf
sed -e "s|<PASTE_SITE_B_PRIVATE_KEY_HERE>|$(cat /tmp/b.key)|" \
    -e "s|<PASTE_SITE_A_PUBLIC_KEY_HERE>|$(cat /tmp/a.pub)|" \
    -e '/^Address/d' \
    "$HERE/wg0-b.conf" > /tmp/wg0-b.conf
chmod 600 /tmp/wg0-a.conf /tmp/wg0-b.conf

echo "== Step 4c: apply the configs =="
ip netns exec site-a wg setconf wg0 /tmp/wg0-a.conf
ip netns exec site-b wg setconf wg0 /tmp/wg0-b.conf

echo "== Step 5: bring the tunnels up =="
ip -n site-a link set lo up
ip -n site-b link set lo up
ip -n site-a link set wg0 up
ip -n site-b link set wg0 up

echo "== Forcing the first handshake =="
ip netns exec site-b ping -c2 -W2 10.99.0.1 || true

echo
echo "Tunnel built. Now run ./verify.sh — and ./cleanup.sh before the next lab."
