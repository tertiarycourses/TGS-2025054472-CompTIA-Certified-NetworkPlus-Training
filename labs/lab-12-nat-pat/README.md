# Lab 12 — NAT and PAT with iptables

NAT translates private IPs (RFC 1918) into a routable public IP. PAT (Port Address Translation, also called NAT overload) lets many private hosts share one public IP by tracking source ports. Linux implements both via `iptables` `MASQUERADE`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `iptables` (usually pre-installed)

---

## Step 1 — Re-create the namespace from Lab 7 (or 8)

```bash
ip netns add a
ip link add a-h type veth peer name h-a
ip link set a-h netns a
ip addr add 10.1.1.1/24 dev h-a
ip link set h-a up
ip netns exec a ip addr add 10.1.1.2/24 dev a-h
ip netns exec a ip link set a-h up
ip netns exec a ip link set lo up
ip netns exec a ip route add default via 10.1.1.1
```

---

## Step 2 — Enable forwarding on the host

```bash
sysctl -w net.ipv4.ip_forward=1
```

---

## Step 3 — Add the MASQUERADE rule (PAT)

```bash
iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE
```

This rewrites the source IP of any packet from `10.1.1.0/24` to the host’s eth0 IP and tracks the source port for return traffic.

---

## Step 4 — Test from inside the namespace

```bash
ip netns exec a ping -c2 8.8.8.8
ip netns exec a curl -s ifconfig.me
```

The IP printed by `ifconfig.me` will be the host’s public IP, not 10.1.1.2 — that proves the translation worked.

---

## Step 5 — Inspect the conntrack table

```bash
apt install -y conntrack
conntrack -L | head
```

You will see entries like `tcp ... src=10.1.1.2 ... [SRC=<public-ip>]` showing the translation.

---

## Step 6 — Clean up

```bash
iptables -t nat -F POSTROUTING
ip netns del a
ip link del h-a 2>/dev/null
```

---

## What you learned
- The difference between NAT (1-to-1) and PAT (many-to-1).
- `MASQUERADE` is dynamic SNAT that always uses the outgoing interface’s address.
- `conntrack -L` shows the live translation table.
