# Lab 30 — DNS Troubleshooting

When a user reports “the site is down”, DNS is one of the first things to verify. In this lab you will use `dig`, `+trace`, and `resolvectl` to isolate resolution problems.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `dnsutils`
- `systemd-resolved` (pre-installed)

**Files in this lab folder:**

| File | Use |
|------|-----|
| `break.sh` | injects a broken resolver so you can diagnose a real fault (Step 8) — backs up `/etc/resolv.conf` first |
| `cleanup.sh` | restores the **original** `/etc/resolv.conf` from `/tmp/resolv.conf.bak` |
| `verify.sh` | objective pass/fail check that resolution is working again |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

---

## Step 1 — Install dnsutils

```bash
apt update && apt install -y dnsutils
```

---

## Step 2 — Confirm which resolver the system is using

```bash
cat /etc/resolv.conf
resolvectl status | head -20
```

If `/etc/resolv.conf` points to `127.0.0.53` you are going through systemd-resolved.

---

## Step 3 — Compare two upstream resolvers

```bash
dig @1.1.1.1 example.com +short
dig @8.8.8.8 example.com +short
```

If one returns NXDOMAIN and the other an IP, the first resolver is the problem.

---

## Step 4 — Trace the recursive resolution chain

```bash
dig +trace example.com
```

You will see each delegation: root → `.com` TLD → authoritative for example.com.

---

## Step 5 — Check for slow upstream

```bash
time dig @1.1.1.1 example.com
```

A consistent multi-second response indicates an upstream issue, not a client one.

---

## Step 6 — Flush systemd-resolved cache

```bash
resolvectl flush-caches
resolvectl statistics
```

The statistics counter will reset.

---

## Step 7 — Common DNS error decode

| Status | Meaning |
|--------|---------|
| NOERROR | Successful response |
| NXDOMAIN | Name does not exist |
| SERVFAIL | Upstream failure (DNSSEC, broken zone) |
| REFUSED | Server refuses to answer (often ACL) |

---

## Step 8 — Diagnose an injected fault

Now put the theory to work on a fault you did not create.

```bash
./break.sh
```

`break.sh` copies your current `/etc/resolv.conf` to `/tmp/resolv.conf.bak`
**before** it changes anything, then repoints the system at `10.99.0.53` — an
address that goes nowhere.

Reproduce the symptom:

```bash
dig example.com +short
ping -c2 example.com
```

Now diagnose it with the Step 2 and Step 3 commands:

```bash
cat /etc/resolv.conf
resolvectl status | head -20
dig @1.1.1.1 example.com +short
dig @8.8.8.8 example.com +short
```

The key observation: querying `1.1.1.1` **directly** works, so the network path
and the upstream are both fine — the fault is the *configured resolver*, not
connectivity. That distinction is the whole point of Step 3 of this lab.

Then restore and confirm:

```bash
./cleanup.sh
./verify.sh
```

`cleanup.sh` puts the original `/etc/resolv.conf` back (symlink and all) and
flushes the cache. `verify.sh` prints `PASS:` / `FAIL:` lines and exits non-zero
if anything is still broken.

---

## What you learned
- How to identify which resolver Linux is using.
- How `+trace` walks the DNS hierarchy from the root.
- The meaning of NXDOMAIN, SERVFAIL, and REFUSED.
- How to tell a **resolver** fault from a **connectivity** fault by querying an upstream directly.

---

## Before you leave

Run `./cleanup.sh` if you have not already, then work through `checklist.md` and tick every line.
