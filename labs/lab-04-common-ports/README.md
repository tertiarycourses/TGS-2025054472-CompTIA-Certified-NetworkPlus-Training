# Lab 4 — Common Ports and Protocols

Network+ candidates must memorise the well-known ports. In this lab you will scan a live target and inspect the listening ports on your own machine to connect protocol names (SSH, HTTP, DNS…) to numbers (22, 80, 53…).

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Files in this lab folder**

| File | Use |
|---|---|
| `data/well-known-ports.csv` | the full N10-009 port list — service, port, transport, purpose |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

---

## Step 1 — Install nmap and net-tools

```bash
apt update && apt install -y nmap net-tools
```

`nmap` is the industry-standard port scanner. `net-tools` provides legacy commands like `netstat`.

---

## Step 2 — List ports listening on your own host

```bash
ss -tulnp
```

Flag breakdown:
- `-t` TCP
- `-u` UDP
- `-l` listening only
- `-n` numeric ports (no name resolution)
- `-p` show the owning process

Note any familiar ports (22 = SSH, 53 = DNS, 80 = HTTP, 443 = HTTPS).

---

## Step 3 — Scan a public test target

The Nmap project hosts `scanme.nmap.org` specifically for learning.

```bash
nmap -sT -p 1-1024 scanme.nmap.org
```

`-sT` is a TCP connect scan; `-p 1-1024` limits to the well-known port range.

---

## Step 4 — Map the results to the exam list

| Port | Protocol | Layer 4 |
|------|----------|---------|
| 20/21 | FTP | TCP |
| 22 | SSH / SFTP | TCP |
| 23 | Telnet | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | UDP/TCP |
| 67/68 | DHCP | UDP |
| 69 | TFTP | UDP |
| 80 | HTTP | TCP |
| 110 | POP3 | TCP |
| 123 | NTP | UDP |
| 143 | IMAP | TCP |
| 161/162 | SNMP | UDP |
| 389 | LDAP | TCP |
| 443 | HTTPS | TCP |
| 445 | SMB | TCP |
| 514 | Syslog | UDP |
| 636 | LDAPS | TCP |
| 993 | IMAPS | TCP |
| 995 | POP3S | TCP |
| 3306 | MySQL | TCP |
| 3389 | RDP | TCP |

The same list, extended with a one-line purpose for each service and a few extras
(587, 1433, 1521, 5060/5061), ships as `data/well-known-ports.csv`. Keep it as your
revision artifact — it greps well:

```bash
grep -i ldap data/well-known-ports.csv
grep ',UDP,' data/well-known-ports.csv
```

To drill yourself, hide the port column and recall each number from the service name:

```bash
cut -d, -f1,3 data/well-known-ports.csv
```

---

## Step 5 — Resolve a service name to a port

```bash
getent services https
getent services ssh
```

The numbers `getent` returns come from `/etc/services` and should match the CSV exactly.

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- How to enumerate listening services with `ss`.
- How to scan a remote host with `nmap`.
- The mapping from common protocol names to the well-known ports tested on N10-009.
- Which services are UDP-only, and how each cleartext protocol pairs with its TLS twin.
