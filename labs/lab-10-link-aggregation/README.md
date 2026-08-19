# Lab 10 — Link Aggregation (LACP Bond)

Link aggregation bundles multiple NICs into one logical interface for redundancy and increased bandwidth. The dynamic protocol is **LACP** (IEEE 802.3ad). On Linux this is implemented by the `bonding` driver.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `ifenslave`
- Kernel `bonding` module

---

## Step 1 — Install ifenslave and load the bonding driver

```bash
apt update && apt install -y ifenslave
modprobe bonding mode=802.3ad miimon=100
```

`mode=802.3ad` selects LACP. `miimon=100` polls link state every 100 ms.

---

## Step 2 — Create the bond interface

```bash
ip link add bond0 type bond mode 802.3ad
```

---

## Step 3 — Add slave interfaces

In Killercoda only `eth0` exists, so we will demonstrate the syntax with one slave. On real hardware you would add two NICs.

```bash
ip link set eth0 down
ip link set eth0 master bond0
ip link set eth0 up
ip link set bond0 up
```

Note: enslaving the only NIC will disconnect Killercoda. Run this on a multi-NIC VM or rebuild the playground after.

---

## Step 4 — Inspect the bond status

```bash
cat /proc/net/bonding/bond0
```

You will see the LACP partner MAC, the aggregator ID, and per-slave link state.

---

## Step 5 — Clean up

```bash
ip link set eth0 nomaster
ip link del bond0
```

---

## What you learned
- LACP (802.3ad) negotiates aggregation dynamically with the switch.
- Other modes include active-backup (no switch support needed) and balance-rr.
- `/proc/net/bonding/<bond>` shows LACP state and slave health.
