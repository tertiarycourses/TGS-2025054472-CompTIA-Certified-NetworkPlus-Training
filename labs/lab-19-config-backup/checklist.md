# Lab 19 checklist — Configuration Backup with Git

Tick each item as you complete it.

- [ ] Installed git with `apt update && apt install -y git`
- [ ] Initialised a repository in `/etc` with `git init`
- [ ] Set the commit identity with `git config user.email` and `git config user.name`
- [ ] Staged the network configs with `git add hosts hostname resolv.conf network/ bind/`
- [ ] Created the baseline commit `baseline: initial network configuration`
- [ ] Made a change by appending `127.0.1.2 lab-vm` to `/etc/hosts`
- [ ] Reviewed the change with `git -C /etc diff hosts` before committing it
- [ ] Committed the change as `add lab-vm hostname mapping`
- [ ] Inspected the audit trail with `git -C /etc log --oneline` and `git -C /etc show HEAD`
- [ ] Rolled the change back with `git -C /etc revert HEAD --no-edit` and confirmed with `cat /etc/hosts`
- [ ] Opened `data/change-log.csv` and matched its columns to the git history (who requested, who approved, how to roll back)
- [ ] Explained why a revert commit is safer than deleting history with `git reset --hard`
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `/etc` is a git repo, `git log` shows the baseline, change and revert commits, and `127.0.1.2 lab-vm` is gone from `/etc/hosts`
