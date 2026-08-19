# Lab 33 — MTU and Path-MTU Discovery

The Maximum Transmission Unit is the largest single frame an interface will send. Mismatched MTUs across a path cause silent failures with anything larger than ~1400 bytes — classic “small pings work, downloads stall” symptom.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iputils-ping`

**Files in this lab folder:**

| File | Use |
|------|-----|
| `run.sh` | runs the DF-bit probe sequence (Steps 1–5) and restores the MTU at the end |
| `cleanup.sh` | puts `eth0`'s MTU back to 1500 if `run.sh` was interrupted mid-lab |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

> **This lab changes interface state.** Step 4 lowers `eth0`'s MTU to 1400.
> Always finish with Step 5 (or `./cleanup.sh`) so the next lab starts clean.

---

## Step 1 — See your interface MTU

```bash
ip -brief link show eth0
```

Standard Ethernet is `1500`. Tunnels (VPN, GRE) typically run lower.

---

## Step 2 — Send a packet at the largest size that fits

The IP header is 20 bytes, ICMP header 8 bytes — so the payload max is `1500 − 28 = 1472`.

```bash
ping -M do -s 1472 -c2 8.8.8.8
```

`-M do` sets the **Don’t Fragment** bit; `-s 1472` is the payload size.

---

## Step 3 — Force fragmentation needed

```bash
ping -M do -s 1500 -c2 8.8.8.8
```

Expected output:
```
ping: local error: message too long, mtu=1500
```

The kernel won’t even send it; on a real path you would get back ICMP type 3 code 4 (“Fragmentation Needed and DF set”).

---

## Step 4 — Lower the interface MTU and retest

```bash
ip link set eth0 mtu 1400
ping -M do -s 1400 -c2 8.8.8.8 || true
ping -M do -s 1372 -c2 8.8.8.8
```

Now the largest payload that fits is `1400 − 28 = 1372`.

---

## Step 5 — Restore the MTU

```bash
ip link set eth0 mtu 1500
```

Steps 1–5 are scripted end to end: `./run.sh` runs every probe above and restores
the MTU to 1500 on the way out. If you interrupted it (or ran the steps by hand
and stopped part way), run:

```bash
./cleanup.sh
```

That is the safety net — it puts `eth0` back to `mtu 1500` and confirms it.

---

## Step 6 — When MTU mismatch causes blackholes

ICMP-blocking firewalls strip the “Fragmentation Needed” message, so the sender never learns to drop down. Symptoms:
- Small pings and SSH login work.
- Web pages or file downloads hang at exactly the moment of the first big packet.
- Workaround: enable **TCP MSS clamping** on the router (`iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`).

---

## What you learned
- The maths: payload = MTU − 20 (IP) − 8 (ICMP/UDP) or − 20 (TCP).
- How `-M do` simulates Path MTU Discovery.
- Why ICMP filtering breaks PMTUD and how MSS clamping rescues TCP.

---

## Before you leave

Confirm `ip -brief link show eth0` reports `mtu 1500` (run `./cleanup.sh` if not),
then work through `checklist.md` and tick every line.
