# Lab 7 — Simulating a Cloud VPC with Network Namespaces

Cloud providers like AWS build virtual networks called **VPCs** out of subnets, route tables, and gateways. Linux network namespaces let you simulate the same thing on one machine. In this lab you will build a VPC with two subnets and a bridge.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed on Ubuntu):**
- `iproute2` (provides `ip` command)

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

---

## Step 6 — Clean up

```bash
ip netns del web
ip netns del db
ip link del br0
```

---

## What you learned
- A network namespace behaves like an isolated VM for networking.
- A bridge is the Linux equivalent of a virtual switch.
- Two hosts on the same subnet can talk through a bridge with no router.
