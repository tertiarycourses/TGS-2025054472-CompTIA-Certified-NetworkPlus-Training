# Lab 13 — DHCP Server with isc-dhcp-server

In this lab you will configure the ISC DHCP server to hand out leases on a private subnet.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `isc-dhcp-server`

**Files shipped with this lab**

| File | Use |
|------|-----|
| `dhcpd.conf` | The real scope file — copied to `/etc/dhcp/dhcpd.conf` in Step 3 |
| `setup.sh` | Runs Steps 1–5 (install, dummy interface, config, listen interface, start) |
| `verify.sh` | Objective `PASS`/`FAIL` check, including `dhcpd -t` and the service state |
| `cleanup.sh` | Reverses Step 7 and restores the packaged `dhcpd.conf` |
| `checklist.md` | Tick-box list of everything you must be able to show |

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

The scope is shipped with this lab as `dhcpd.conf`. Read it first — every line
matters:

```
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
```

| Line | Meaning |
|------|---------|
| `default-lease-time 600` | A client that does not ask for a specific duration gets 600 s |
| `max-lease-time 7200` | The longest lease this server will ever grant |
| `authoritative` | This server is the official DHCP server here, so it may DHCPNAK bad requests |
| `range 10.50.0.100 10.50.0.150` | The 51 addresses in the dynamic pool |
| `option routers` | The default gateway pushed to clients |
| `option domain-name-servers` | The resolvers pushed to clients |
| `option broadcast-address` | The subnet's broadcast address |

Now copy the provided file into place instead of retyping it:

```bash
cp dhcpd.conf /etc/dhcp/dhcpd.conf
```

Check it parses before you start the daemon:

```bash
dhcpd -t -cf /etc/dhcp/dhcpd.conf
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

`verify.sh` checks the whole build — the dummy interface, every element of the
scope, that `dhcpd -t` parses the file, the `INTERFACESv4` binding, and that the
service is active with a lease database:

```bash
./verify.sh
```

---

## Step 7 — Clean up

```bash
systemctl stop isc-dhcp-server
ip link del dum0
```

Or run the provided script, which also restores the `dhcpd.conf` the package
originally shipped:

```bash
./cleanup.sh
```

Finally, work through `checklist.md` and tick off each outcome.

---

## Shortcut

If you need to rebuild after a playground reset, `./setup.sh` runs Steps 1–5
exactly as written above (it copies the same `dhcpd.conf`). Do the steps by
hand the first time — reading the scope file is the point of the lab.

---

## What you learned
- The structure of a DHCP scope: range, routers, DNS, lease times.
- How to restrict the DHCP daemon to a specific interface.
- Where Linux stores lease state (`/var/lib/dhcp/dhcpd.leases`).
