# Lab 6 — DHCP Lease Capture (DORA)

DHCP automatically assigns IP addresses using a four-step exchange known as **DORA**: Discover → Offer → Request → Acknowledge. In this lab you will release your existing lease and capture all four messages live.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `isc-dhcp-client`
- `tcpdump`

**Files in this lab folder**

| File | Use |
|---|---|
| `run.sh` | runs the capture + release + renew sequence (Steps 1–5) in one go |
| `cleanup.sh` | stops any leftover `tcpdump` and renews the lease so the next lab starts clean |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

The timing matters in this lab — the capture must already be running before you release
the lease. Follow Steps 1–5 by hand, or run `./run.sh` which sequences them for you.

> This lab briefly drops your IP address. If the terminal stops responding after
> Step 3, the renew in Step 4 will restore it; `./cleanup.sh` also forces a renew.

---

## Step 1 — Install the tools

```bash
apt update && apt install -y isc-dhcp-client tcpdump
```

---

## Step 2 — Start a capture for DHCP ports

DHCP uses UDP/67 (server) and UDP/68 (client). Run tcpdump in the background.

```bash
tcpdump -i eth0 -nn -v 'port 67 or port 68' &
```

---

## Step 3 — Release the current lease

```bash
dhclient -v -r eth0
```

`-r` releases the lease and sends a DHCPRELEASE.

---

## Step 4 — Request a new lease

```bash
dhclient -v eth0
```

Watch the tcpdump output — you should see:
1. **DHCPDISCOVER** (broadcast from 0.0.0.0 → 255.255.255.255)
2. **DHCPOFFER** (from server, includes proposed IP)
3. **DHCPREQUEST** (client confirms which offer)
4. **DHCPACK** (server confirms lease)

---

## Step 5 — Stop the capture

```bash
kill %1 2>/dev/null
```

---

## Step 6 — Clean up

This lab changes your interface's address state, so restore it before moving on:

```bash
./cleanup.sh
```

It stops any `tcpdump` this lab started and renews the DHCP lease on `eth0`, then prints
the resulting address. Confirm you have a routable IPv4 address again:

```bash
ip -4 addr show eth0
```

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- The four DHCP messages and the DORA mnemonic.
- The UDP ports DHCP uses (67/68).
- How to release and renew a lease on Linux.
