# Lab 19 — Configuration Backup with Git

Network configuration drift is a leading cause of outages. Putting `/etc` (or a network device’s running-config) under version control gives you change history, blame, and rollback for free.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `git`

---

## Step 1 — Install git

```bash
apt update && apt install -y git
```

---

## Step 2 — Initialise a repo in /etc

```bash
cd /etc
git init
git config user.email "netadmin@lab.local"
git config user.name  "Net Admin"
```

---

## Step 3 — Add critical network configs

```bash
git add hosts hostname resolv.conf network/ bind/ 2>/dev/null
git commit -m "baseline: initial network configuration"
```

---

## Step 4 — Make a change and commit it

```bash
echo "127.0.1.2 lab-vm" >> /etc/hosts
git -C /etc diff hosts
git -C /etc add hosts
git -C /etc commit -m "add lab-vm hostname mapping"
```

---

## Step 5 — Inspect the audit trail

```bash
git -C /etc log --oneline
git -C /etc show HEAD
```

---

## Step 6 — Roll back

```bash
git -C /etc revert HEAD --no-edit
cat /etc/hosts
```

---

## What you learned
- Why every change to network config should be tracked.
- Basic git workflow: init → add → commit → log → revert.
- The same approach works for backing up router/switch configs (push them to git via a script).
