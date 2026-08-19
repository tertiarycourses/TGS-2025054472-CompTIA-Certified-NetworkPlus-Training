# Lab 7 — Simulating a Cloud VPC with Network Namespaces

Cloud providers like AWS build virtual networks called **VPCs** out of subnets, route tables, and gateways. Linux network namespaces let you simulate the same thing on one machine. In this lab you will build a VPC with two subnets and a bridge.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed on Ubuntu):**
- `iproute2` (provides `ip` command)

**Files in this lab folder**

| File | Use |
|---|---|
| `setup.sh` | builds the whole topology — namespaces, bridge, veth pairs, addressing (Steps 1–4) |
| `verify.sh` | checks both namespaces, the bridge, both addresses and that the pings pass (Step 5) |
| `cleanup.sh` | deletes the namespaces and the bridge (Step 6) |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

This is the longest lab in Domain 1 — 22 commands. Build it by hand the first time so
you see what each command does, then use the scripts to rebuild it quickly:

```bash
./setup.sh    # Steps 1-4: build the topology
./verify.sh   # Step 5: prove web can reach db
./cleanup.sh  # Step 6: tear it all down
```

`setup.sh` is idempotent — it removes any leftovers from a previous run before building,
so it is safe to re-run if a step fails halfway.

The finished topology:

```
  namespace web                              namespace db
  10.0.1.10/24                               10.0.1.20/24
     veth-web                                   veth-db
        |                                          |
     br-web ------------[ br0 ]--------------- br-db
                      (the VPC switch)
```

---

## Step 1 — Create two namespaces (representing two VMs)

```bash
ip netns add web
ip netns add db
```

Each namespace has its own routing table, interfaces and firewall — like a virtual machine.

---

## Step 2 — Create a bridge (the VPC switch)

```bash
ip link add br0 type bridge
ip link set br0 up
```

---

## Step 3 — Connect each namespace to the bridge with a veth pair

```bash
ip link add veth-web type veth peer name br-web
ip link add veth-db  type veth peer name br-db

ip link set br-web master br0
ip link set br-db  master br0
ip link set br-web up
ip link set br-db  up

ip link set veth-web netns web
ip link set veth-db  netns db
```

A `veth` pair is a virtual cable with two ends.

---

## Step 4 — Assign IPs in the same /24 subnet

```bash
ip netns exec web ip addr add 10.0.1.10/24 dev veth-web
ip netns exec db  ip addr add 10.0.1.20/24 dev veth-db
ip netns exec web ip link set veth-web up
ip netns exec db  ip link set veth-db  up
ip netns exec web ip link set lo up
ip netns exec db  ip link set lo up
```

---

## Step 5 — Test connectivity between the two “VMs”

```bash
ip netns exec web ping -c2 10.0.1.20
```

If it replies, you have a working VPC subnet.

To check every part of the build at once — namespaces, bridge state, both addresses and
the ping in both directions:

```bash
./verify.sh
```

It prints a `PASS:`/`FAIL:` line per check and exits non-zero if anything is wrong. The
most common failure is a veth end that was never brought up, or one that was not
enslaved to `br0`.

---

## Step 6 — Clean up

```bash
ip netns del web
ip netns del db
ip link del br0
```

Or run the script, which does the same and reports what it removed:

```bash
./cleanup.sh
```

Deleting a namespace also deletes the veth end inside it, and removing one end of a veth
pair removes the other — so `br-web` and `br-db` disappear along with the namespaces.

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- A network namespace behaves like an isolated VM for networking.
- A bridge is the Linux equivalent of a virtual switch.
- Two hosts on the same subnet can talk through a bridge with no router.
