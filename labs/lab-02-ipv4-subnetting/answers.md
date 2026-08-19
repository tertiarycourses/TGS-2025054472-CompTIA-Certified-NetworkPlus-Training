# Lab 2 — Answers

Self-check only. Work the subnets out yourself first, verify in the
**TIS IP Calculator** (https://alfredang.github.io/ipcalculator/), then compare here.

---

## Part A — The parent network `192.168.10.0/24` (README Step 2)

| Field | Value |
|---|---|
| Network address | 192.168.10.0 |
| Subnet mask | 255.255.255.0 |
| Broadcast address | 192.168.10.255 |
| Usable host range | 192.168.10.1 → 192.168.10.254 |
| Total addresses | 256 |
| Usable hosts | 254 |

---

## Part B — Splitting the /24 into four /26 subnets (README Step 3)

### The math

Going from `/24` to `/26` borrows **2 host bits** for the network portion:

- Number of subnets = 2^(bits borrowed) = 2² = **4**
- Addresses per subnet = 2^(32 − 26) = 2⁶ = **64**
- Usable hosts per subnet = 64 − 2 = **62** (one network address, one broadcast address)
- New mask = 255.255.255.**192** (the last octet: 128+64 = 192)
- **Block size = 64**, so the subnets step 0 → 64 → 128 → 192 in the fourth octet

### The completed Step 3 table

| Subnet | CIDR | Network | First Host | Last Host | Broadcast |
|---|---|---|---|---|---|
| 1 | 192.168.10.0/26 | 192.168.10.0 | 192.168.10.1 | 192.168.10.62 | 192.168.10.63 |
| 2 | 192.168.10.64/26 | 192.168.10.64 | 192.168.10.65 | 192.168.10.126 | 192.168.10.127 |
| 3 | 192.168.10.128/26 | 192.168.10.128 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 |
| 4 | 192.168.10.192/26 | 192.168.10.192 | 192.168.10.193 | 192.168.10.254 | 192.168.10.255 |

Each row checks out: 64 total addresses, unique network and broadcast, 62 usable hosts.

The address you assign in README Step 4 — `192.168.10.65/26` — is the **first usable
host of subnet 2**, which is why it does not collide with subnet 1.

---

## Part C — Completed `data/subnet-plan.csv`

The NetTech Solutions plan. Within each site, subnets are allocated **largest
requirement first** (VLSM) so no address space is wasted.

### Jurong HQ — parent 192.168.10.0/24

| Department | Hosts needed | CIDR | Network | First host | Last host | Broadcast |
|---|---|---|---|---|---|---|
| Guest Wi-Fi | 60 | 192.168.10.0/26 | 192.168.10.0 | 192.168.10.1 | 192.168.10.62 | 192.168.10.63 |
| Engineering | 50 | 192.168.10.64/26 | 192.168.10.64 | 192.168.10.65 | 192.168.10.126 | 192.168.10.127 |
| Sales | 40 | 192.168.10.128/26 | 192.168.10.128 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 |
| Finance | 25 | 192.168.10.192/26 | 192.168.10.192 | 192.168.10.193 | 192.168.10.254 | 192.168.10.255 |

All four fit exactly the four /26 blocks from Part B. Finance needs only 25 hosts, but a
/27 (30 usable) would still leave the last /26 block half-empty here, so the equal /26
split is the clean answer for this site.

### Tampines Branch — parent 192.168.20.0/24

| Department | Hosts needed | CIDR | Network | First host | Last host | Broadcast |
|---|---|---|---|---|---|---|
| Operations | 120 | 192.168.20.0/25 | 192.168.20.0 | 192.168.20.1 | 192.168.20.126 | 192.168.20.127 |
| Warehouse | 30 | 192.168.20.128/27 | 192.168.20.128 | 192.168.20.129 | 192.168.20.158 | 192.168.20.159 |
| Reception | 10 | 192.168.20.160/28 | 192.168.20.160 | 192.168.20.161 | 192.168.20.174 | 192.168.20.175 |

Operations needs 120, so a /26 (62 usable) is too small — step up to a /25 (126 usable).

### Woodlands DC — parent 192.168.30.0/24

| Department | Hosts needed | CIDR | Network | First host | Last host | Broadcast |
|---|---|---|---|---|---|---|
| Server Farm | 100 | 192.168.30.0/25 | 192.168.30.0 | 192.168.30.1 | 192.168.30.126 | 192.168.30.127 |
| Storage | 20 | 192.168.30.128/27 | 192.168.30.128 | 192.168.30.129 | 192.168.30.158 | 192.168.30.159 |
| Out-of-Band Mgmt | 12 | 192.168.30.160/28 | 192.168.30.160 | 192.168.30.161 | 192.168.30.174 | 192.168.30.175 |

### Changi Office — parent 192.168.40.0/24

| Department | Hosts needed | CIDR | Network | First host | Last host | Broadcast |
|---|---|---|---|---|---|---|
| Support Desk | 55 | 192.168.40.0/26 | 192.168.40.0 | 192.168.40.1 | 192.168.40.62 | 192.168.40.63 |
| Training Room | 28 | 192.168.40.64/27 | 192.168.40.64 | 192.168.40.65 | 192.168.40.94 | 192.168.40.95 |

---

## Prefix quick-reference

| Prefix | Mask | Addresses | Usable hosts | Block size (4th octet) |
|---|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 | 256 |
| /25 | 255.255.255.128 | 128 | 126 | 128 |
| /26 | 255.255.255.192 | 64 | 62 | 64 |
| /27 | 255.255.255.224 | 32 | 30 | 32 |
| /28 | 255.255.255.240 | 16 | 14 | 16 |
| /29 | 255.255.255.248 | 8 | 6 | 8 |
| /30 | 255.255.255.252 | 4 | 2 | 4 |

**Rule of thumb:** pick the smallest prefix whose *usable* host count is ≥ the requirement,
then the network address of the next subnet = previous network + block size.

---

## Step 5 expected output

After `ip addr add 192.168.10.65/26 dev eth0 label eth0:1`, the command
`ip -4 addr show eth0` prints a line containing:

```
inet 192.168.10.65/26 scope global eth0:1
```
