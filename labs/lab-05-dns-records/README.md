# Lab 5 — DNS Record Types

DNS resolves names into IPs and a lot more. In this lab you will use `dig` to query each of the record types listed in the N10-009 objectives: A, AAAA, MX, TXT, NS, CNAME, PTR, SOA, SRV.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

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

---

## What you learned
- How to query every record type required for N10-009.
- How CNAMEs differ from A records, and what a PTR record is used for.
- How `dig +short` gives you the bare answer suitable for scripts.
