# Lab 27 — Building an ACL with iptables

Access Control Lists allow or deny traffic based on source/destination/port. In this lab you will permit MySQL traffic from one subnet and deny it from everywhere else.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iptables`

---

## Step 1 — Inspect current rules

```bash
iptables -L INPUT -n -v --line-numbers
```

The default Ubuntu policy is `ACCEPT` everywhere — we will tighten that for one port.

---

## Step 2 — Allow MySQL from 10.0.0.0/24 only

```bash
iptables -I INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT
```

`-I INPUT` inserts at the top so the rule is matched before any later DROP.

---

## Step 3 — Drop MySQL from everywhere else

```bash
iptables -A INPUT -p tcp --dport 3306 -j DROP
```

`-A INPUT` appends to the bottom.

---

## Step 4 — Verify ordering

```bash
iptables -L INPUT -n -v --line-numbers
```

Order matters: the ACCEPT must come before the DROP.

---

## Step 5 — Test the ACL

```bash
nc -zv 127.0.0.1 3306        # blocked unless your IP is in 10.0.0.0/24
ip addr add 10.0.0.5/24 dev lo
nc -zv -s 10.0.0.5 127.0.0.1 3306   # connection attempt from allowed source
```

(Even with no MySQL listening you will see TCP RST vs no response — proving filtering works.)

---

## Step 6 — Persist the rules

```bash
apt install -y iptables-persistent
netfilter-persistent save
```

`netfilter-persistent` writes `/etc/iptables/rules.v4` so rules survive reboot.

---

## Step 7 — Clean up

```bash
iptables -D INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT
iptables -D INPUT -p tcp --dport 3306 -j DROP
ip addr del 10.0.0.5/24 dev lo
```

---

## What you learned
- ACLs are evaluated top-to-bottom; the first match wins.
- The `-I` (insert) vs `-A` (append) flags control where a rule lands.
- Without `iptables-persistent`, rules disappear on reboot.
