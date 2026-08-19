# Lab 31 — ARP and the IPv6 Neighbour Table

ARP (IPv4) and Neighbour Discovery (IPv6) translate IP addresses to MAC addresses. Stale or poisoned entries are a frequent cause of connectivity problems.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `iputils-arping`
- `iproute2` (pre-installed)

---

## Step 1 — View the current neighbour table

```bash
ip neigh
```

Each line: `<IP> dev <iface> lladdr <MAC> STATE`. Common states:
- `REACHABLE` — recently confirmed.
- `STALE` — known but not recently confirmed.
- `FAILED` — no response.

---

## Step 2 — Probe a neighbour with arping

```bash
apt update && apt install -y iputils-arping
arping -I eth0 -c2 $(ip route | awk '/default/ {print $3}')
```

This sends ARP requests directly to the default gateway.

---

## Step 3 — Detect duplicate IP

```bash
arping -D -I eth0 -c2 $(ip -4 -o addr show eth0 | awk '{print $4}' | cut -d/ -f1)
```

`-D` enables duplicate address detection — if another host claims the same IP you will see “address already in use”.

---

## Step 4 — Add a static ARP entry

```bash
ip neigh add 10.0.0.99 lladdr de:ad:be:ef:00:01 dev eth0
ip neigh
```

Useful for pinning critical neighbours when ARP poisoning is a concern.

---

## Step 5 — Flush the table

```bash
ip neigh flush all
ip neigh
```

The table will repopulate as you generate traffic.

---

## Step 6 — IPv6 neighbour discovery

```bash
ip -6 neigh
ndisc6 ff02::1 eth0 2>/dev/null || apt install -y ndisc6
```

`ndisc6` sends ICMPv6 Neighbour Solicitation — the IPv6 equivalent of ARP.

---

## What you learned
- ARP is IPv4-only; IPv6 uses ICMPv6 Neighbour Discovery (NDP).
- `arping -D` detects duplicate IP allocations.
- Flushing the neighbour table is the IP-layer equivalent of bouncing the interface.
