# Lab 24 — Site-to-Site VPN with WireGuard

WireGuard is a modern, fast VPN protocol that uses Curve25519 for key exchange. In this lab you will build a tunnel between two Linux network namespaces playing the role of two VPN endpoints.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `wireguard`
- `wireguard-tools`

**Files in this lab folder:**

| File | Use |
|---|---|
| `wg0-a.conf` | site-a's tunnel as a real WireGuard config (placeholder keys) |
| `wg0-b.conf` | site-b's tunnel as a real WireGuard config (placeholder keys) |
| `setup.sh` | Runs Steps 1–5: namespaces, keys, interfaces, tunnel up |
| `verify.sh` | Pass/fail check — handshake established and ping crosses the tunnel |
| `cleanup.sh` | **Run before Lab 25** — tears the interfaces down, deletes the keys |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

> **No real keys ship with this lab.** `wg0-a.conf` and `wg0-b.conf` contain only
> `<PASTE_..._HERE>` placeholders. You generate the real keys yourself in Step 3;
> `setup.sh` substitutes them into working copies under `/tmp`, and `cleanup.sh`
> deletes them again.

---

## Step 1 — Install WireGuard

```bash
apt update && apt install -y wireguard wireguard-tools
```

> **Shortcut:** `./setup.sh` performs Steps 1–5 exactly as written below. Read the
> steps first — 24 commands is a lot to mistype, which is precisely why the
> script exists.

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

### The same tunnel as config files

Production WireGuard is declared in a file, not typed in as flags. `wg0-a.conf`
and `wg0-b.conf` in this folder are exactly the tunnel above, in that form:

**`wg0-a.conf`**
```ini
[Interface]
Address    = 10.99.0.1/24
ListenPort = 51820
PrivateKey = <PASTE_SITE_A_PRIVATE_KEY_HERE>

[Peer]
PublicKey  = <PASTE_SITE_B_PUBLIC_KEY_HERE>
AllowedIPs = 10.99.0.2/32
```

**`wg0-b.conf`**
```ini
[Interface]
Address    = 10.99.0.2/24
ListenPort = 51821
PrivateKey = <PASTE_SITE_B_PRIVATE_KEY_HERE>

[Peer]
PublicKey  = <PASTE_SITE_A_PUBLIC_KEY_HERE>
AllowedIPs = 10.99.0.1/32
Endpoint   = 127.0.0.1:51820
PersistentKeepalive = 25
```

Paste your own keys over the placeholders — `PrivateKey` from that peer's own
`.key` file, `PublicKey` from the *other* peer's `.pub` file — then apply them.
`wg setconf` does not understand the wg-quick-only `Address` line, so drop it and
keep using `ip addr add`:

```bash
sed '/^Address/d' wg0-a.conf > /tmp/wg0-a.conf   # after pasting your keys
ip netns exec site-a wg setconf wg0 /tmp/wg0-a.conf
```

A private key must never be committed to a repository, an image, or a ticket —
that single line is the entire security of the tunnel.

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

Check it objectively:

```bash
./verify.sh
```

It confirms both namespaces exist, `wg0` is up and addressed in each, each peer
holds the other's public key, a handshake has actually completed
(`latest-handshakes` is non-zero), encrypted bytes have moved, and the ping
crosses the tunnel.

---

## Step 7 — Clean up

```bash
ip netns del site-a
ip netns del site-b
rm /tmp/a.key /tmp/a.pub /tmp/b.key /tmp/b.pub
```

Or run the script, which also brings `wg0` down first and removes the working
configs under `/tmp`:

```bash
./cleanup.sh
```

Leaving `site-a` / `site-b` behind will confuse the namespace-based labs later in
the course, so do not skip it. Finish by ticking off `checklist.md`.

---

## What you learned
- WireGuard keys are tiny (32-byte) and require no PKI.
- `allowed-ips` doubles as a routing rule and an inbound ACL.
- Modern VPN deployments prefer WireGuard over IPsec for its simplicity and speed.
