# Lab 23 — SSH Hardening with Key Authentication

Password SSH is one of the most attacked services on the internet. In this lab you will create an Ed25519 key pair, install the public key, and disable password login.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `openssh-server`
- `openssh-client`

**Files in this lab folder:**

| File | Use |
|---|---|
| `sshd_hardening.conf` | The hardened directives as a real drop-in fragment |
| `verify.sh` | Pass/fail check — key auth works, password auth is refused |
| `cleanup.sh` | **Run before Lab 24** — restores the original `sshd_config` |
| `data/hardening-checklist.csv` | Control register you complete at Step 6 |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

> No key material ships with this lab. You generate your own Ed25519 pair in
> Step 1, and `cleanup.sh` deletes it again.

---

## Step 1 — Generate an Ed25519 key pair

```bash
ssh-keygen -t ed25519 -N '' -f ~/.ssh/lab_ed25519
```

Flags:
- `-t ed25519` — modern, fast elliptic-curve algorithm.
- `-N ''` — empty passphrase (for lab convenience only).
- `-f` — output filename.

---

## Step 2 — Install the public key as authorised

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
cat ~/.ssh/lab_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

---

## Step 3 — Test key login

```bash
ssh -i ~/.ssh/lab_ed25519 -o StrictHostKeyChecking=no root@localhost whoami
```

You should get `root` without being prompted for a password.

---

## Step 4 — Disable password authentication

**Back the config up first** — `cleanup.sh` restores from this file, and in the
real world you never edit `sshd_config` without a way back:

```bash
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.lab23.bak
```

```bash
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sshd -t && systemctl reload ssh
```

`sshd -t` validates the configuration — never reload without testing.

### The same hardening as a drop-in file

Editing a vendor config with `sed` is fine for a lab, but a real fleet drops a
file into `/etc/ssh/sshd_config.d/` instead. `sshd_hardening.conf` in this folder
is that file:

```conf
PasswordAuthentication no
PermitRootLogin prohibit-password
MaxAuthTries 3
PermitEmptyPasswords no
KbdInteractiveAuthentication no
AllowTcpForwarding no
X11Forwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
LoginGraceTime 30
#Port 2222
#AllowUsers admin
```

```bash
cp sshd_hardening.conf /etc/ssh/sshd_config.d/99-lab-hardening.conf
sshd -t && systemctl reload ssh
```

`Port` and `AllowUsers` are deliberately commented out — enabling either
mid-lab would drop your Killercoda session.

---

## Step 5 — Verify password login is blocked

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no root@localhost
```

You should see `Permission denied (publickey)`.

---

## Step 6 — Bonus hardening checklist

- Change default port (`Port 2222`) — security through obscurity, but reduces noise.
- Restrict by user (`AllowUsers admin`).
- Install `fail2ban` to ban brute-force IPs.
- Use `MaxAuthTries 3`.

Work through `data/hardening-checklist.csv` — one row per control, with the
shipped default, the hardened value and the reason:

```
control,setting,default_value,hardened_value,rationale
Authentication,PasswordAuthentication,yes,no,Removes password guessing ... entirely
Brute force,MaxAuthTries,6,3,Drops the connection after three failures ...
Key hygiene,authorized_keys permissions,644,600,sshd silently ignores ... world writable
```

Being able to defend the **rationale** column is what a device-hardening
standard is actually made of.

---

## Step 7 — Check your work

```bash
./verify.sh
```

It confirms the key pair and its permissions, that `sshd -t` passes, that the
effective config has `PasswordAuthentication no`, that key login returns `root`,
and that a forced password login is refused with `Permission denied`.

---

## Step 8 — Restore the box

```bash
./cleanup.sh
```

**Do not skip this.** Later labs connect to this host; leaving
`PasswordAuthentication no` and a stray authorised key behind changes their
starting conditions. The script restores `/etc/ssh/sshd_config` from the Step 4
backup (or reverses exactly the two directives if you did not take one), removes
the drop-in fragment, de-authorises the lab key and deletes the key pair — then
re-validates with `sshd -t` before reloading. Finish by ticking off
`checklist.md`.

---

## What you learned
- Public-key authentication eliminates passwords as an attack surface.
- Why Ed25519 is preferred over RSA-2048 today (faster, smaller, equally strong).
- The role of `sshd -t` in change management.
