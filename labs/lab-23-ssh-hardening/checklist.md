# Lab 23 checklist — SSH Hardening with Key Authentication

Tick each item as you complete it.

- [ ] Generated the key pair with `ssh-keygen -t ed25519 -N '' -f ~/.ssh/lab_ed25519`
- [ ] Can explain why Ed25519 is preferred over RSA-2048 today
- [ ] Created `~/.ssh` with mode `700` and appended the public key to `~/.ssh/authorized_keys`
- [ ] Set `~/.ssh/authorized_keys` to mode `600` (sshd ignores a loose file)
- [ ] Logged in with `ssh -i ~/.ssh/lab_ed25519 root@localhost whoami` and got `root` with no password prompt
- [ ] Backed up the original config with `cp /etc/ssh/sshd_config /etc/ssh/sshd_config.lab23.bak`
- [ ] Set `PasswordAuthentication no` and `PermitRootLogin prohibit-password`
- [ ] Read `sshd_hardening.conf` and know what each directive in it does
- [ ] Validated with `sshd -t` **before** reloading, and can say why that order matters
- [ ] Reloaded with `systemctl reload ssh`
- [ ] Confirmed `Permission denied (publickey)` when forcing password authentication
- [ ] Completed `data/hardening-checklist.csv` — every control, its default and its hardened value
- [ ] Ran `./cleanup.sh` — original `sshd_config` restored, lab key removed and de-authorised
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — key login returns `root`, and a forced password login is refused with `Permission denied`
