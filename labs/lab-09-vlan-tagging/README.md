# Lab 9 — 802.1Q VLAN Tagging

VLANs separate broadcast domains on the same physical switch. The IEEE 802.1Q standard inserts a 4-byte tag with the VLAN ID into each Ethernet frame. In this lab you will create two VLAN sub-interfaces on Linux.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2`
- Kernel module `8021q`

---

## Step 1 — Load the 802.1Q kernel module

```bash
modprobe 8021q
lsmod | grep 8021q
```

If `lsmod` shows the module name, the kernel is ready to tag frames.

---

## Step 2 — Create two VLAN sub-interfaces on eth0

```bash
ip link add link eth0 name eth0.10 type vlan id 10
ip link add link eth0 name eth0.20 type vlan id 20
```

`eth0.10` will tag every outgoing frame with VLAN ID 10; `eth0.20` will use VLAN 20.

---

## Step 3 — Assign each VLAN its own subnet

```bash
ip addr add 192.168.10.1/24 dev eth0.10
ip addr add 192.168.20.1/24 dev eth0.20
ip link set eth0.10 up
ip link set eth0.20 up
```

---

## Step 4 — Verify

```bash
ip -d link show eth0.10
ip -d link show eth0.20
```

The `-d` flag shows the VLAN ID in the output.

---

## Step 5 — Capture a tagged frame

```bash
apt install -y tcpdump
tcpdump -i eth0 -nn -e vlan &
ping -c2 -I eth0.10 192.168.10.1
kill %1
```

The `-e` flag prints Ethernet headers including the VLAN tag.

---

## Step 6 — Clean up

```bash
ip link del eth0.10
ip link del eth0.20
```

---

## What you learned
- 802.1Q adds a 4-byte VLAN tag to Ethernet frames.
- A trunk port carries multiple VLANs; an access port carries one.
- Linux models trunk ports with sub-interfaces named `iface.<vlan-id>`.
