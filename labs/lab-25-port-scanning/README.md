# Lab 25 — Port Scanning and Service Hardening

You will use `nmap` to enumerate exposed services on your own host, then disable the unnecessary ones — a basic attack-surface reduction exercise.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `nmap`

---

## Step 1 — Install nmap

```bash
apt update && apt install -y nmap
```

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

---

## What you learned
- The difference between `-sS`, `-sT`, `-sU`, and `-sV` scans.
- The “minimum services” principle: every open port is a potential entry point.
- Cross-checking nmap output with `ss` to identify the owning process.
