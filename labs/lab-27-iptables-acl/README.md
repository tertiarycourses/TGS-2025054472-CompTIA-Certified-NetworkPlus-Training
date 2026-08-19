# Lab 27 — Building an ACL with iptables

Access Control Lists allow or deny traffic based on source/destination/port. In this lab you will permit MySQL traffic from one subnet and deny it from everywhere else.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iptables`

**Files in this lab folder:**

| File | Use |
|---|---|
| `setup.sh` | Applies Steps 1–5 in one go (idempotent — never duplicates a rule) |
| `verify.sh` | Pass/fail check — permitted traffic passes, denied traffic is blocked |
| `cleanup.sh` | **Run before Lab 28** — deletes only the rules this lab added |
| `data/acl-plan.csv` | The ACL design worksheet you fill in before Step 2 |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

---

## Step 1 — Inspect current rules

```bash
iptables -L INPUT -n -v --line-numbers
```

The default Ubuntu policy is `ACCEPT` everywhere — we will tighten that for one port.

> **Shortcut:** `./setup.sh` applies Steps 1–5 exactly as written below, and is
> idempotent so it never leaves duplicate rules in the chain. Read the steps
> first.

### Plan the ACL before you type it

An ACL is designed on paper and then transcribed — never invented at the
prompt, because a mis-ordered rule locks people out. Open `data/acl-plan.csv`:

```
sequence,action,protocol,source,destination,port,purpose
10,ACCEPT,tcp,10.0.0.0/24,any,3306,Application subnet is the only network allowed to reach MySQL
20,DROP,tcp,any,any,3306,Catch-all deny for MySQL - must be evaluated AFTER sequence 10
...
160,DROP,any,any,any,any,Implicit deny-all - the last line of every ACL
```

The `sequence` column is the whole point: rows are evaluated in ascending order
and the **first match wins**. Sequence 10 must come before sequence 20, or the
permit is never reached. Steps 2 and 3 below implement exactly those first two
rows.

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

Check it objectively:

```bash
./verify.sh
```

It confirms both rules exist, that the ACCEPT is at a **lower line number** than
the DROP, that `10.0.0.5/24` is on `lo`, that the denied source gets no response,
and that the permitted source is not filtered. It also reports the ACCEPT rule's
packet counter — proof the rule is actually matching traffic.

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

Or run the script, which does the same by exact match and also re-saves
`/etc/iptables/rules.v4` so the DROP rule you persisted in Step 6 does not come
back on the next boot:

```bash
./cleanup.sh
```

**This is the most important cleanup in Domain 4.** A `DROP` rule left in the
`INPUT` chain silently blackholes traffic in every later lab, and the symptom
(a timeout with no error) is exactly the kind of fault the Domain 5
troubleshooting labs are trying to teach you to *find*. Note what `cleanup.sh`
does **not** do: it never runs `iptables -F`, because a blanket flush would also
wipe rules that Docker, ufw or the playground itself installed.

Confirm you are clean before starting Lab 28:

```bash
iptables -L INPUT -n --line-numbers | grep 3306   # should print nothing
```

Finish by ticking off `checklist.md`.

---

## What you learned
- ACLs are evaluated top-to-bottom; the first match wins.
- The `-I` (insert) vs `-A` (append) flags control where a rule lands.
- Without `iptables-persistent`, rules disappear on reboot.
