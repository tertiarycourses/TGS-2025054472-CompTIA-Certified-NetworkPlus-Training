# Lab 8 checklist — Static Routing Between Two Subnets

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Created the three namespaces `a`, `r1` and `b` (`ip netns list` shows all three)
- [ ] Wired both veth pairs and moved each end into the right namespace (`a-r`/`r-a`, `b-r`/`r-b`)
- [ ] Assigned 10.1.1.2/24 to `a-r` in namespace `a` and 10.2.2.2/24 to `b-r` in namespace `b`
- [ ] Assigned both router legs on `r1`: 10.1.1.1/24 on `r-a` and 10.2.2.1/24 on `r-b`
- [ ] Brought `lo` and every veth interface up in all three namespaces
- [ ] Enabled `net.ipv4.ip_forward=1` inside namespace `r1`
- [ ] Added the static route on `a`: `10.2.2.0/24 via 10.1.1.1`
- [ ] Added the static route on `b`: `10.1.1.0/24 via 10.2.2.1`
- [ ] Read `ip netns exec a ip route` and can explain each line against `data/routing-table.csv`
- [ ] Ran `./cleanup.sh` (or `for n in a r1 b; do ip netns del $n; done`) so the box is clean
- [ ] **Test it:** `ip netns exec a ping -c2 10.2.2.2` gets replies across the router (`./verify.sh` prints `PASS: Lab 8 complete`)
