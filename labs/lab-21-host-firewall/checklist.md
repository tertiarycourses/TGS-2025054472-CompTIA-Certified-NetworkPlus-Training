# Lab 21 checklist — Host Firewall with UFW

Tick each item as you complete it.

- [ ] Installed UFW with `apt update && apt install -y ufw`
- [ ] Set the default-deny inbound stance with `ufw default deny incoming`
- [ ] Set `ufw default allow outgoing` so the host can still reach apt and DNS
- [ ] Allowed SSH **before** enabling with `ufw allow 22/tcp` (avoids lock-out)
- [ ] Enabled the firewall with `ufw --force enable` and read `ufw status verbose`
- [ ] Added the source-restricted rule `ufw allow from 10.0.0.0/8 to any port 3306 proto tcp`
- [ ] Listed the rules with `ufw status numbered` and explained why order/number matters
- [ ] Deleted a rule by number with `ufw delete 1`
- [ ] Filled in `data/firewall-rules.csv` and can justify every allow line
- [ ] Confirmed the rules also appear in `iptables -L` (UFW is an iptables front-end)
- [ ] Ran `./cleanup.sh` — UFW is **disabled** and inbound traffic is unfiltered again
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — ufw is active, default incoming is deny, 22/tcp is allowed, 3306/tcp is allowed only from `10.0.0.0/8`, and blocked port 9999 is refused
