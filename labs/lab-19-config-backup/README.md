# Lab 19 — Configuration Backup with Git

Network configuration drift is a leading cause of outages. Putting `/etc` (or a network device’s running-config) under version control gives you change history, blame, and rollback for free.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `git`

**Files in this lab folder:**

| File | What it is |
|---|---|
| `run.sh` | runs Steps 1–6 end to end (init, baseline, change, log, rollback) |
| `verify.sh` | objective pass/fail check — `git log` must show all three commits |
| `data/change-log.csv` | 16-row change register used in Step 7 |
| `checklist.md` | tick-list of everything you should have done |

Run `./run.sh` from this folder (it `cd`s to `/etc` itself), then come back here for `./verify.sh`.

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

The `lab-vm` line is gone, but nothing was erased — the revert is itself a fourth entry in the audit trail. That is why you revert rather than `git reset --hard`.

---

## Step 7 — Tie the commits to a change register

Git tells you *what* changed and *when*. Change management tells you *who asked*, *who approved*, and *how to back out*. `data/change-log.csv` is a 16-row register for the fictitious `nettech.local` estate with exactly those columns: `date,change_id,device,description,requester,approver,rollback_plan`.

```bash
column -s, -t < data/change-log.csv | less -S

# Every change to the perimeter firewall
grep 'fw-perim-01' data/change-log.csv

# How many changes each approver signed off
cut -d, -f6 data/change-log.csv | tail -n +2 | sort | uniq -c | sort -rn
```

In a mature shop the commit message carries the change ID, so `git log --oneline --grep=CHG-2026-0041` jumps straight from the register to the diff. Add the change ID to your Step 4 commit message and try it.

---

## Test it

```bash
./verify.sh
```

Expect `ALL CHECKS PASSED` — `/etc` is a git repository, `git log` contains the baseline commit, the `add lab-vm hostname mapping` commit and the revert commit, and `127.0.1.2 lab-vm` is no longer in `/etc/hosts`. Work through `checklist.md` as you go.

---

## What you learned
- Why every change to network config should be tracked.
- Basic git workflow: init → add → commit → log → revert.
- The same approach works for backing up router/switch configs (push them to git via a script).
