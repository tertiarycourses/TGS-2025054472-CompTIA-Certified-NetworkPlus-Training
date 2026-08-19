# Lab 4 — Common Ports and Protocols

Network+ candidates must memorise the well-known ports. In this lab you will scan a live target and inspect the listening ports on your own machine to connect protocol names (SSH, HTTP, DNS…) to numbers (22, 80, 53…).

Run on https://killercoda.com/playgrounds/scenario/ubuntu

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

---

## Step 5 — Resolve a service name to a port

```bash
getent services https
getent services ssh
```

---

## What you learned
- How to enumerate listening services with `ss`.
- How to scan a remote host with `nmap`.
- The mapping from common protocol names to the well-known ports tested on N10-009.
