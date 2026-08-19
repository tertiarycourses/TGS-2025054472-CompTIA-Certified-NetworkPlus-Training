# Lab 21 — Host Firewall with UFW

UFW (Uncomplicated Firewall) is a friendly front-end for `iptables`. In this lab you will deny everything by default and only permit SSH.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `ufw`

---

## Step 1 — Install UFW

```bash
apt update && apt install -y ufw
```

---

## Step 2 — Set sane defaults

```bash
ufw default deny incoming
ufw default allow outgoing
```

A deny-by-default inbound stance is the foundation of any host firewall.

---

## Step 3 — Allow SSH (port 22)

```bash
ufw allow 22/tcp
```

If you skip this in a real SSH session you will lock yourself out — UFW will warn you.

---

## Step 4 — Enable the firewall

```bash
ufw --force enable
ufw status verbose
```

`--force` skips the interactive “are you sure” prompt.

---

## Step 5 — Add a source-restricted rule

```bash
ufw allow from 10.0.0.0/8 to any port 3306 proto tcp
ufw status numbered
```

Only RFC 1918 hosts in `10.0.0.0/8` can reach MySQL.

---

## Step 6 — Delete a rule

```bash
ufw delete 1
```

Deletes rule number 1 from the numbered list.

---

## Step 7 — Disable when done

```bash
ufw disable
```

---

## What you learned
- The principle of default-deny.
- How to allow a port globally vs from a specific source.
- How UFW maps to iptables behind the scenes (`iptables -L` will still show the rules).
