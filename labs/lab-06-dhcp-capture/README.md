# Lab 6 — DHCP Lease Capture (DORA)

DHCP automatically assigns IP addresses using a four-step exchange known as **DORA**: Discover → Offer → Request → Acknowledge. In this lab you will release your existing lease and capture all four messages live.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `isc-dhcp-client`
- `tcpdump`

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

## What you learned
- The four DHCP messages and the DORA mnemonic.
- The UDP ports DHCP uses (67/68).
- How to release and renew a lease on Linux.
