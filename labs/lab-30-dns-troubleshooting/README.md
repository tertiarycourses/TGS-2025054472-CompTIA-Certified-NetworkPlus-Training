# Lab 30 — DNS Troubleshooting

When a user reports “the site is down”, DNS is one of the first things to verify. In this lab you will use `dig`, `+trace`, and `resolvectl` to isolate resolution problems.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `dnsutils`
- `systemd-resolved` (pre-installed)

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

## What you learned
- How to identify which resolver Linux is using.
- How `+trace` walks the DNS hierarchy from the root.
- The meaning of NXDOMAIN, SERVFAIL, and REFUSED.
