# Lab 21 — Host Firewall with UFW

UFW (Uncomplicated Firewall) is a friendly front-end for `iptables`. In this lab you will deny everything by default and only permit SSH.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `ufw`

**Files in this lab folder:**

| File | Use |
|---|---|
| `setup.sh` | Runs Steps 1–5 in one go (or follow them by hand) |
| `verify.sh` | Objective pass/fail check — allowed port reachable, blocked port refused |
| `cleanup.sh` | **Run this before Lab 22** — deletes the lab's rules and disables UFW |
| `data/firewall-rules.csv` | Rule-planning worksheet you fill in at Step 5 |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

---

## Step 1 — Install UFW

```bash
apt update && apt install -y ufw
```

> **Shortcut:** `./setup.sh` performs Steps 1–5 exactly as written below. Read the
> steps first — the script exists to save typing, not to replace the learning.

---

## Step 2 — Set sane defaults

```bash
ufw default deny incoming
ufw default allow outgoing
```

A deny-by-default inbound stance is the foundation of any host firewall.

---

## Step 3 — Allow SSH (port 22)

```bash
ufw allow 22/tcp
```

If you skip this in a real SSH session you will lock yourself out — UFW will warn you.

---

## Step 4 — Enable the firewall

```bash
ufw --force enable
ufw status verbose
```

`--force` skips the interactive “are you sure” prompt.

---

## Step 5 — Add a source-restricted rule

```bash
ufw allow from 10.0.0.0/8 to any port 3306 proto tcp
ufw status numbered
```

Only RFC 1918 hosts in `10.0.0.0/8` can reach MySQL.

A real firewall is planned on paper before it is typed. Open
`data/firewall-rules.csv` — it is the rule register for this host:

```
rule_no,action,direction,protocol,port,source,purpose
1,deny,incoming,any,any,any,Default-deny baseline - nothing enters unless a rule permits it
3,allow,incoming,tcp,22,any,Remote administration over SSH - added BEFORE enabling to avoid lockout
4,allow,incoming,tcp,3306,10.0.0.0/8,MySQL reachable only from the internal RFC 1918 estate
...
```

For every `allow` row ask: *which business service needs this, and can the source
be narrowed?* A rule you cannot justify in the `purpose` column should not exist.

---

## Step 6 — Delete a rule

```bash
ufw delete 1
```

Deletes rule number 1 from the numbered list.

---

## Step 7 — Check your work

```bash
./verify.sh
```

It confirms UFW is active, the default incoming policy is `deny`, `22/tcp` is
allowed, `3306/tcp` is restricted to `10.0.0.0/8`, and that a blocked port
(9999) is refused. It prints `PASS:` / `FAIL:` per check and exits non-zero on
failure.

---

## Step 8 — Disable when done

```bash
ufw disable
```

**This matters more than usual.** A default-deny firewall left running will break
every later lab in the course (DNS, SNMP, iperf3, WireGuard). Use the cleanup
script so the rules this lab added are removed as well as the firewall stopped:

```bash
./cleanup.sh
```

It deletes only the two rules the lab created, restores the permissive default,
and runs `ufw disable`. Finish by ticking off `checklist.md`.

---

## What you learned
- The principle of default-deny.
- How to allow a port globally vs from a specific source.
- How UFW maps to iptables behind the scenes (`iptables -L` will still show the rules).
