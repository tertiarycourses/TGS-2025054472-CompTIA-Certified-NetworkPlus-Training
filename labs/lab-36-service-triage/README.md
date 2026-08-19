# Lab 36 — Service Reachability Triage (curl, nc, openssl)

When a user says “the website is down”, you must isolate which layer is failing: TCP reachability, TLS, HTTP, or the app itself. This lab walks through that triage with three tools.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `curl`
- `netcat-openbsd`
- `openssl`

**Files in this lab folder:**

| File | Use |
|------|-----|
| `run.sh` | runs the layered triage sequence (Steps 1–5) — or follow the steps by hand |
| `troubleshooting-worksheet.md` | **the main deliverable** — the CompTIA 7-step form you complete in Step 7 |
| `break.sh` | injects a fault so you meet the ticket cold — backs up the firewall rules first |
| `cleanup.sh` | restores the **original** iptables rules from `/tmp/lab36-iptables.bak` |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

This is the **capstone lab for Domain 5**. The commands are only half of it —
the assessed output is the completed `troubleshooting-worksheet.md`.

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

Steps 1–5 are scripted: run `./run.sh` to walk the whole triage in order.

---

## Step 7 — Capstone: work a real ticket with the CompTIA 7-step methodology

Everything above told you *which commands* to run. This step is about the
*discipline* of running them in the right order and writing down what you found —
the CompTIA Network+ troubleshooting methodology:

| # | Step |
|---|------|
| 1 | Identify the problem |
| 2 | Establish a theory of probable cause |
| 3 | Test the theory to determine the cause |
| 4 | Establish a plan of action and identify potential effects |
| 5 | Implement the solution or escalate |
| 6 | Verify full system functionality and implement preventive measures |
| 7 | Document findings, actions and outcomes |

**Inject the fault** — do not read `break.sh` first, meet the ticket cold:

```bash
./break.sh
```

`break.sh` saves the current firewall rules to `/tmp/lab36-iptables.bak`
**before** it changes anything, then adds a single rule. The ticket reads:

> *"https://example.com is down — nobody in the office can reach it."*

**Now open `troubleshooting-worksheet.md` and work all seven steps in order.**
Fill in every box. The rule that matters most: write your theory down in Step 2
*before* you test it in Step 3 — that is what separates methodical
troubleshooting from guessing, and it is what the exam asks you to reproduce.

Useful commands beyond this lab's three: `ping` and `mtr` (Lab 29), `dig`
(Lab 30), `ip route` (Lab 34), and:

```bash
iptables -L OUTPUT -n --line-numbers
```

**Restore the box** once you have documented your findings:

```bash
./cleanup.sh
```

`cleanup.sh` removes the injected rule, restores the original filter table from
the backup, and re-tests reachability so you can see the service come back.

---

## What you learned
- A layered triage approach to “site is down” reports.
- How to test each protocol layer in isolation with the right tool.
- How to break a single curl request into its timing phases.
- The CompTIA 7-step troubleshooting methodology, applied end to end to a live fault.
- Why documenting the outcome (Step 7) is the step most often skipped and most often needed later.

---

## Before you leave

Run `./cleanup.sh`, hand in your completed `troubleshooting-worksheet.md`, then
work through `checklist.md` and tick every line.
