# Lab 23 — SSH Hardening with Key Authentication

Password SSH is one of the most attacked services on the internet. In this lab you will create an Ed25519 key pair, install the public key, and disable password login.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `openssh-server`
- `openssh-client`

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

```bash
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sshd -t && systemctl reload ssh
```

`sshd -t` validates the configuration — never reload without testing.

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

---

## What you learned
- Public-key authentication eliminates passwords as an attack surface.
- Why Ed25519 is preferred over RSA-2048 today (faster, smaller, equally strong).
- The role of `sshd -t` in change management.
