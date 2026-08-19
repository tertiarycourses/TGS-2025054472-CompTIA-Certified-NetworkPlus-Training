# Lab 36 — Service Reachability Triage (curl, nc, openssl)

When a user says “the website is down”, you must isolate which layer is failing: TCP reachability, TLS, HTTP, or the app itself. This lab walks through that triage with three tools.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `curl`
- `netcat-openbsd`
- `openssl`

---

## Step 1 — Install the tools

```bash
apt update && apt install -y curl netcat-openbsd openssl
```

---

## Step 2 — Layer 4 reachability (TCP handshake only)

```bash
nc -zv example.com 443
```

`-z` zero-I/O mode; `-v` verbose. A `succeeded` line proves a working TCP handshake all the way to the destination — i.e. routing, firewall, and listener are fine.

---

## Step 3 — Layer 6 TLS handshake

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | head -20
```

Look for:
- **subject=** — certificate is for the right domain.
- **issuer=** — trusted CA.
- **Verify return code: 0 (ok)** — chain validated.

A non-zero verify code points at an expired or untrusted certificate.

---

## Step 4 — Layer 7 HTTP

```bash
curl -v https://example.com 2>&1 | head -30
```

Read the response status:
| Code | Meaning |
|------|---------|
| 200 | OK |
| 301/302 | Redirect |
| 401 | Auth required |
| 403 | Forbidden |
| 404 | Not found |
| 500 | App error |
| 502/503/504 | Upstream / overload |

---

## Step 5 — Inspect timing breakdown

```bash
curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} TTFB:%{time_starttransfer} TOTAL:%{time_total}\n" \
     -o /dev/null -s https://example.com
```

This isolates which phase is slow.

---

## Step 6 — Decision tree

1. `nc -zv` fails → routing or firewall (use traceroute, mtr).
2. `nc` works but `openssl s_client` fails → TLS issue (cert/SNI/protocol).
3. TLS works but HTTP returns 5xx → application or upstream.
4. Slow `time_namelookup` → DNS issue (Lab 30).
5. Slow `time_starttransfer` → server-side processing.

---

## What you learned
- A layered triage approach to “site is down” reports.
- How to test each protocol layer in isolation with the right tool.
- How to break a single curl request into its timing phases.
