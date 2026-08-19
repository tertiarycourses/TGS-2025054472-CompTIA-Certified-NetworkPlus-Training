# Lab 27 checklist — Building an ACL with iptables

Tick each item as you complete it.

- [ ] Inspected the starting rules with `iptables -L INPUT -n -v --line-numbers`
- [ ] Noted that the default Ubuntu INPUT policy is `ACCEPT`
- [ ] Planned the ACL in `data/acl-plan.csv` before typing a single rule
- [ ] Inserted the permit with `iptables -I INPUT -p tcp --dport 3306 -s 10.0.0.0/24 -j ACCEPT`
- [ ] Appended the deny with `iptables -A INPUT -p tcp --dport 3306 -j DROP`
- [ ] Can explain the difference between `-I` (insert at top) and `-A` (append at bottom)
- [ ] Re-listed the chain and confirmed the ACCEPT sits **above** the DROP
- [ ] Can state why "first match wins" makes ordering the whole game
- [ ] Added the allowed test source with `ip addr add 10.0.0.5/24 dev lo`
- [ ] Compared `nc -zv 127.0.0.1 3306` (blocked — no response) with `nc -zv -s 10.0.0.5 127.0.0.1 3306` (permitted)
- [ ] Can explain why a `DROP` gives a timeout while a `REJECT` gives an immediate refusal
- [ ] Persisted the rules with `apt install -y iptables-persistent && netfilter-persistent save`
- [ ] Ran `./cleanup.sh` — both rules deleted, `10.0.0.5/24` removed from `lo`, and `rules.v4` re-saved
- [ ] Confirmed `iptables -L INPUT -n | grep 3306` returns nothing before starting Lab 28
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — both rules exist, the ACCEPT is ordered before the DROP, the denied source is blocked on 3306, and the permitted source `10.0.0.5` passes the filter
