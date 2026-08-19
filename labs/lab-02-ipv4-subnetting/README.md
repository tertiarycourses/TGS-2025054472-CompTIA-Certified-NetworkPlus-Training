# Lab 2 — IPv4 Subnetting and CIDR

In this lab you will take a single `/24` network and break it into four equal `/26` subnets. You will use the **TIS IP Calculator** web tool to verify the math, then assign one of the resulting addresses to a virtual interface on Linux. Subnetting is one of the highest-weighted Network+ skills because every router, firewall, and cloud VPC requires correct CIDR planning.

**Subnet calculator (open in a browser tab):**
👉 https://alfredang.github.io/ipcalculator/

Run the Linux commands on https://killercoda.com/playgrounds/scenario/ubuntu

---

## Step 1 — Open the IP Calculator

In a new browser tab, open:

```
https://alfredang.github.io/ipcalculator/
```

This is a free web-based subnet calculator — no install required. You will use it to confirm network/broadcast/host ranges for each CIDR in this lab.

---

## Step 2 — Understand the parent network

Start with `192.168.10.0/24`. The `/24` means the first 24 bits identify the network and the last 8 bits identify hosts, giving 256 addresses total (254 usable).

In the IP Calculator, enter:

```
IP / Prefix:  192.168.10.0/24
```

Then click **Calculate** and read off:
- **Network address**
- **Broadcast address**
- **Usable host range** (HostMin → HostMax)
- **Subnet mask** (255.255.255.0)
- **Total / Usable hosts** (256 / 254)

---

## Step 3 — Split into four /26 subnets

Adding two bits to the network portion (24 → 26) creates 4 subnets, each with 64 addresses (62 usable).

Use the calculator one at a time for each:

```
192.168.10.0/26
192.168.10.64/26
192.168.10.128/26
192.168.10.192/26
```

Fill in this table from the calculator output:

| Subnet | Network | First Host | Last Host | Broadcast |
|--------|---------|-----------|-----------|-----------|
| 1 | 192.168.10.0 | 192.168.10.1 | 192.168.10.62 | 192.168.10.63 |
| 2 | 192.168.10.64 | … | … | … |
| 3 | 192.168.10.128 | … | … | … |
| 4 | 192.168.10.192 | … | … | … |

Verify each subnet has:
- 64 total addresses
- A unique network and broadcast address
- 62 usable host addresses

---

## Step 4 — Assign an IP from subnet 2 to your interface

Switch to the Killercoda terminal. We will give your interface a secondary IP that sits inside `192.168.10.64/26`.

```bash
ip addr add 192.168.10.65/26 dev eth0 label eth0:1
```

The `label eth0:1` creates a virtual sub-interface so the new address does not replace the primary one.

---

## Step 5 — Verify

```bash
ip -4 addr show eth0
```

You should see `inet 192.168.10.65/26 ... eth0:1` in the output.

---

## Step 6 — Clean up

```bash
ip addr del 192.168.10.65/26 dev eth0
```

---

## What you learned
- How to verify subnet boundaries using the **TIS IP Calculator** at https://alfredang.github.io/ipcalculator/
- How a `/24` divides into four `/26` networks with 62 usable hosts each.
- How to assign and remove a CIDR-formatted IP on Linux.
