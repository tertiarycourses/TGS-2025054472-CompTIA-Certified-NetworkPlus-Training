# Lab 8 — Static Routing Between Two Subnets

Routers forward packets between subnets using a routing table. In this lab you will build a tiny three-node topology: subnet A ↔ Router ↔ subnet B, and add the static routes that make A and B talk.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2`
- Linux kernel `sysctl` (built in)

**Files shipped with this lab**

| File | Use |
|------|-----|
| `setup.sh` | Builds the whole topology (Steps 1–5) in one go |
| `verify.sh` | Objective `PASS`/`FAIL` check of Step 6 |
| `cleanup.sh` | Reverses Step 7 and sweeps leftover veth halves |
| `data/routing-table.csv` | Routing-table planning worksheet used in Step 6 |
| `checklist.md` | Tick-box list of everything you must be able to show |

Work through Steps 1–7 by hand the first time — that is where the learning is.
If you need to rebuild the topology quickly (e.g. after a playground reset), run
`./setup.sh`, which executes exactly the commands in Steps 1–5.

---

## Step 1 — Create three namespaces

```bash
ip netns add a
ip netns add r1
ip netns add b
```

`r1` will be our router.

---

## Step 2 — Wire A↔R1 and B↔R1 with veth pairs

```bash
ip link add a-r type veth peer name r-a
ip link add b-r type veth peer name r-b
ip link set a-r netns a
ip link set r-a netns r1
ip link set b-r netns b
ip link set r-b netns r1
```

---

## Step 3 — Assign IPs (two different subnets)

```bash
ip netns exec a  ip addr add 10.1.1.2/24 dev a-r
ip netns exec r1 ip addr add 10.1.1.1/24 dev r-a
ip netns exec r1 ip addr add 10.2.2.1/24 dev r-b
ip netns exec b  ip addr add 10.2.2.2/24 dev b-r
for n in a r1 b; do ip netns exec $n ip link set lo up; done
ip netns exec a  ip link set a-r up
ip netns exec r1 ip link set r-a up
ip netns exec r1 ip link set r-b up
ip netns exec b  ip link set b-r up
```

---

## Step 4 — Enable IP forwarding on the router

A router must explicitly forward packets between interfaces.

```bash
ip netns exec r1 sysctl -w net.ipv4.ip_forward=1
```

---

## Step 5 — Add static routes on the end hosts

Each host knows only its own subnet, so we tell it to send everything else through R1.

```bash
ip netns exec a ip route add 10.2.2.0/24 via 10.1.1.1
ip netns exec b ip route add 10.1.1.0/24 via 10.2.2.1
```

---

## Step 6 — Verify

```bash
ip netns exec a ping -c2 10.2.2.2
ip netns exec a ip route
```

Compare the output of `ip route` with the planning worksheet
`data/routing-table.csv`, which lists every destination, mask, gateway,
interface and metric in this topology plus a few extra subnets to plan for:

```bash
cat data/routing-table.csv
```

Then run the automated check, which asserts the addressing, `ip_forward`, both
static routes and the end-to-end ping:

```bash
./verify.sh
```

---

## Step 7 — Clean up

```bash
for n in a r1 b; do ip netns del $n; done
```

Or run the provided script, which does the same and also removes any veth half
left behind:

```bash
./cleanup.sh
```

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- Routing requires `net.ipv4.ip_forward=1` on the router.
- End hosts use static routes (or a default gateway) to reach networks beyond their LAN.
- The format `via <next-hop>` tells the kernel which neighbour to send packets to.
