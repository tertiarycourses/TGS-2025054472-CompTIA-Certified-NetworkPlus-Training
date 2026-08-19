# Lab 28 — Layer 1/2 Diagnostics with ip and ethtool

Most “the network is down” calls turn out to be a Layer 1 (cable) or Layer 2 (interface) problem. In this lab you will use `ip`, `ethtool`, and the kernel’s interface counters to diagnose.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `ethtool`
- `iproute2` (pre-installed)

**Files in this lab folder:**

| File | Use |
|------|-----|
| `run.sh` | runs the whole diagnostic sequence (Steps 1–5) — or follow the steps by hand |
| `data/interface-errors.csv` | triage worksheet of sample interface counters, used in Step 7 |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

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

Run `./run.sh` to execute Steps 1–5 in one go (Step 6 is printed, never executed).

---

## Step 7 — Triage worksheet

Open `data/interface-errors.csv`. Each row is one interface from a fictitious
`nettech.local` site, with its link state, negotiated speed/duplex and error
counters. Work down the rows and, for each one, decide what the counters tell you
**before** you read the `likely_cause` column:

```bash
column -s, -t data/interface-errors.csv | less -S
```

Questions to answer from the data:
1. Which interface shows the classic **duplex mismatch** signature? (high CRC **and** collisions, `duplex=half`, `autoneg=off`)
2. Which interface has a **cabling** fault rather than a configuration fault? (CRC on receive only)
3. Which two rows are *not* Layer 1/2 faults at all, and why?
4. Which rows need no action?

---

## What you learned
- The four states of a Linux NIC (DOWN / UP / NOCARRIER / LOWERLAYERDOWN).
- Where to read CRC and frame error counters.
- Why duplex mismatch shows as high error rates without a full link drop.

---

## Before you leave

Work through `checklist.md` and tick every line.
