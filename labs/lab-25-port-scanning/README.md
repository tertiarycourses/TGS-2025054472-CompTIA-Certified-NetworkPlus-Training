# Lab 25 — Port Scanning and Service Hardening

You will use `nmap` to enumerate exposed services on your own host, then disable the unnecessary ones — a basic attack-surface reduction exercise.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `nmap`

**Files in this lab folder:**

| File | Use |
|---|---|
| `run.sh` | Runs the whole scan sequence and saves it to `scan-results.txt` |
| `data/port-scan-findings.csv` | The finding register you complete at Step 5 |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

> **Scope:** scan only `127.0.0.1`, your own playground host. Scanning any
> address you do not own is an offence in Singapore under the Computer Misuse
> Act.

---

## Step 1 — Install nmap

```bash
apt update && apt install -y nmap
```

> **Shortcut:** `./run.sh` runs Steps 1–5 and 7 exactly as written below, echoing
> each phase and saving everything to `scan-results.txt` — useful because the
> full 65535-port scan in Step 2 takes several minutes. It does not replace the
> reading; every command is explained here.

---

## Step 2 — Scan all 65535 TCP ports on yourself

```bash
nmap -sS -p- 127.0.0.1
```

`-sS` is a SYN (half-open) scan; `-p-` covers every port.

---

## Step 3 — Enumerate service versions

```bash
nmap -sV -p 22,80,443 127.0.0.1
```

`-sV` probes each port and tries to identify the service banner and version.

---

## Step 4 — OS fingerprint (requires root)

```bash
nmap -O 127.0.0.1
```

---

## Step 5 — Cross-check with ss

```bash
ss -tulnp
```

For each open port, ask: *do I need this service running?*

Record the answer. A scan you do not write up is not an audit — open
`data/port-scan-findings.csv` and add one row per open port:

```
host,port,state,service,version,risk,action
127.0.0.1,22,open,ssh,OpenSSH 8.9p1 Ubuntu 3ubuntu0.6,Low,Keep - required for administration; harden per Lab 23
127.0.0.1,3306,open,mysql,MySQL 8.0.36-0ubuntu0.22.04.1,High,Restrict to 10.0.0.0/8 with the Lab 27 ACL
127.0.0.1,631,open,ipp,CUPS 2.4,Medium,Disable - a server does not need a print spooler
...
```

The sample rows show the shape of a real finding register. Replace them with
what *your* host actually reported, and make sure every `action` is something a
colleague could carry out.

---

## Step 6 — Disable an unneeded service (example)

```bash
systemctl status apache2 2>/dev/null && systemctl disable --now apache2
```

If a service is not present you have nothing to disable — that is the goal.

---

## Step 7 — Re-scan to confirm closure

```bash
nmap -sS -p 80 127.0.0.1
```

Compare this result with the Step 2 baseline in `scan-results.txt` — a hardening
change you cannot demonstrate before-and-after is a change nobody will trust.
Finish by ticking off `checklist.md`.

---

## What you learned
- The difference between `-sS`, `-sT`, `-sU`, and `-sV` scans.
- The “minimum services” principle: every open port is a potential entry point.
- Cross-checking nmap output with `ss` to identify the owning process.
