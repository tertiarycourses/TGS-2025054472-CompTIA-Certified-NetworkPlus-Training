# Lab 13 — DHCP Server with isc-dhcp-server

In this lab you will configure the ISC DHCP server to hand out leases on a private subnet.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `isc-dhcp-server`

---

## Step 1 — Install the server

```bash
apt update && apt install -y isc-dhcp-server
```

---

## Step 2 — Create a dummy interface for the lab

We do not want to disrupt eth0, so we create a dummy interface with our test subnet.

```bash
ip link add dum0 type dummy
ip addr add 10.50.0.1/24 dev dum0
ip link set dum0 up
```

---

## Step 3 — Configure the scope

```bash
cat >/etc/dhcp/dhcpd.conf <<EOF
default-lease-time 600;
max-lease-time 7200;
authoritative;

subnet 10.50.0.0 netmask 255.255.255.0 {
  range 10.50.0.100 10.50.0.150;
  option routers 10.50.0.1;
  option subnet-mask 255.255.255.0;
  option domain-name-servers 1.1.1.1, 8.8.8.8;
  option broadcast-address 10.50.0.255;
}
EOF
```

---

## Step 4 — Tell the server which interface to listen on

```bash
sed -i 's/^INTERFACESv4=.*/INTERFACESv4="dum0"/' /etc/default/isc-dhcp-server
```

---

## Step 5 — Start the service

```bash
systemctl restart isc-dhcp-server
systemctl status isc-dhcp-server --no-pager
```

---

## Step 6 — Inspect the leases file

```bash
cat /var/lib/dhcp/dhcpd.leases
```

When real clients connect, their leases will appear here.

---

## Step 7 — Clean up

```bash
systemctl stop isc-dhcp-server
ip link del dum0
```

---

## What you learned
- The structure of a DHCP scope: range, routers, DNS, lease times.
- How to restrict the DHCP daemon to a specific interface.
- Where Linux stores lease state (`/var/lib/dhcp/dhcpd.leases`).
