# Lab 5 — DNS Record Types

DNS resolves names into IPs and a lot more. In this lab you will use `dig` to query each of the record types listed in the N10-009 objectives: A, AAAA, MX, TXT, NS, CNAME, PTR, SOA, SRV.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Files in this lab folder**

| File | Use |
|---|---|
| `run.sh` | runs all ten `dig` queries (Steps 1–10) in sequence, labelled by record type |
| `data/dns-records.csv` | reference zone showing each record type, an example value and its purpose |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

Type the queries yourself the first time — reading the answers is the lab. Use
`./run.sh` afterwards to replay all ten at once and compare the output side by side.

---

## Step 1 — Install dnsutils

```bash
apt update && apt install -y dnsutils
```

This package provides `dig`, `nslookup`, and `host`.

---

## Step 2 — Query an A record (hostname → IPv4)

```bash
dig +short A google.com
```

`+short` removes the verbose header and only prints the answer.

---

## Step 3 — Query an AAAA record (hostname → IPv6)

```bash
dig +short AAAA google.com
```

---

## Step 4 — Query an MX record (mail exchanger)

```bash
dig +short MX google.com
```

The number in front (e.g. `10`) is the priority — lower is preferred.

---

## Step 5 — Query a TXT record (free-form text, used for SPF, DKIM, verification)

```bash
dig +short TXT google.com
```

---

## Step 6 — Query NS records (which servers are authoritative)

```bash
dig +short NS google.com
```

---

## Step 7 — Query a CNAME (canonical alias)

```bash
dig +short CNAME www.github.com
```

A CNAME points one name at another name (not at an IP).

---

## Step 8 — Reverse lookup (PTR record, IP → name)

```bash
dig +short -x 8.8.8.8
```

---

## Step 9 — Query the SOA (zone authority)

```bash
dig +short SOA google.com
```

The SOA record shows the primary nameserver, admin email, serial number, and refresh timers for the zone.

---

## Step 10 — Query an SRV record (service location)

```bash
dig +short SRV _xmpp-server._tcp.gmail.com
```

The four fields of an SRV answer are **priority, weight, port, target**.

---

## Step 11 — Replay everything and compare against the reference zone

Run all ten queries in one pass:

```bash
./run.sh
```

Then open `data/dns-records.csv`. It is a small fictitious `nettech.local` zone showing
each record type with an example value and what it is for — the same record types you
just queried live, but laid out as a zone administrator would plan them:

```bash
grep '^MX' data/dns-records.csv
cut -d, -f1,4 data/dns-records.csv
```

Match each live answer from Steps 2–10 to its row in the CSV.

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- How to query every record type required for N10-009.
- How CNAMEs differ from A records, and what a PTR record is used for.
- How `dig +short` gives you the bare answer suitable for scripts.
- How the record types fit together inside a single zone.
