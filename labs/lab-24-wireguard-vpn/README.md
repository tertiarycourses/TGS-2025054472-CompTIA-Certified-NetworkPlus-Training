# Lab 24 — Site-to-Site VPN with WireGuard

WireGuard is a modern, fast VPN protocol that uses Curve25519 for key exchange. In this lab you will build a tunnel between two Linux network namespaces playing the role of two VPN endpoints.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `wireguard`
- `wireguard-tools`

---

## Step 1 — Install WireGuard

```bash
apt update && apt install -y wireguard wireguard-tools
```

---

## Step 2 — Create two namespaces representing the two sites

```bash
ip netns add site-a
ip netns add site-b
```

---

## Step 3 — Generate key pairs for each peer

```bash
cd /tmp
wg genkey | tee a.key | wg pubkey > a.pub
wg genkey | tee b.key | wg pubkey > b.pub
```

---

## Step 4 — Configure the WireGuard interfaces

```bash
ip -n site-a link add wg0 type wireguard
ip -n site-b link add wg0 type wireguard

ip -n site-a addr add 10.99.0.1/24 dev wg0
ip -n site-b addr add 10.99.0.2/24 dev wg0

ip netns exec site-a wg set wg0 \
  private-key /tmp/a.key listen-port 51820 \
  peer "$(cat /tmp/b.pub)" allowed-ips 10.99.0.2/32

ip netns exec site-b wg set wg0 \
  private-key /tmp/b.key listen-port 51821 \
  peer "$(cat /tmp/a.pub)" allowed-ips 10.99.0.1/32 \
  endpoint 127.0.0.1:51820
```

---

## Step 5 — Bring tunnels up and test

```bash
ip -n site-a link set wg0 up
ip -n site-b link set wg0 up
ip netns exec site-b ping -c2 10.99.0.1
```

Note: namespaces share the host’s loopback, so the endpoint `127.0.0.1` works only because both peers are on the same kernel. In the real world you would specify the public IP of the remote site.

---

## Step 6 — Inspect the tunnel state

```bash
ip netns exec site-a wg show
```

You will see the peer’s public key, last handshake time, and bytes transferred.

---

## Step 7 — Clean up

```bash
ip netns del site-a
ip netns del site-b
rm /tmp/a.key /tmp/a.pub /tmp/b.key /tmp/b.pub
```

---

## What you learned
- WireGuard keys are tiny (32-byte) and require no PKI.
- `allowed-ips` doubles as a routing rule and an inbound ACL.
- Modern VPN deployments prefer WireGuard over IPsec for its simplicity and speed.
