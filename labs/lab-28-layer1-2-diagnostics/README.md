# Lab 28 — Layer 1/2 Diagnostics with ip and ethtool

Most “the network is down” calls turn out to be a Layer 1 (cable) or Layer 2 (interface) problem. In this lab you will use `ip`, `ethtool`, and the kernel’s interface counters to diagnose.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `ethtool`
- `iproute2` (pre-installed)

---

## Step 1 — Install ethtool

```bash
apt update && apt install -y ethtool
```

---

## Step 2 — Check operational state

```bash
ip -brief link show
```

`UP` = admin up + carrier present. `LOWERLAYERDOWN` usually means cable unplugged.

---

## Step 3 — Inspect link parameters

```bash
ethtool eth0
```

Fields to read:
- **Speed / Duplex** — should match the switch port (mismatched duplex causes high error rates).
- **Auto-negotiation** — usually `on`.
- **Link detected** — `yes` means carrier sense is good.

---

## Step 4 — Check error counters

```bash
ip -s link show eth0
ethtool -S eth0 | grep -iE 'err|drop|crc|frame'
```

Non-zero `errors`, `dropped`, or `CRC` counters point at cable/optical/duplex issues.

---

## Step 5 — Bounce the interface

```bash
ip link set eth0 down
sleep 1
ip link set eth0 up
```

Wait a few seconds, re-check with `ip -brief link`.

---

## Step 6 — Force speed/duplex (rarely needed)

```bash
# Example only — do NOT run on Killercoda's primary NIC
# ethtool -s eth0 speed 1000 duplex full autoneg off
```

---

## What you learned
- The four states of a Linux NIC (DOWN / UP / NOCARRIER / LOWERLAYERDOWN).
- Where to read CRC and frame error counters.
- Why duplex mismatch shows as high error rates without a full link drop.
