# Lab 12 checklist — NAT and PAT with iptables

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Created namespace `a` and the `a-h` / `h-a` veth pair
- [ ] Addressed the host side 10.1.1.1/24 and the namespace side 10.1.1.2/24
- [ ] Gave namespace `a` a default route via 10.1.1.1
- [ ] Enabled `net.ipv4.ip_forward=1` on the host
- [ ] Added the PAT rule `iptables -t nat -A POSTROUTING -s 10.1.1.0/24 -o eth0 -j MASQUERADE`
- [ ] Confirmed `ip netns exec a ping -c2 8.8.8.8` gets replies
- [ ] Ran `ip netns exec a curl -s ifconfig.me` and saw the host's public IP, not 10.1.1.2
- [ ] Can explain the difference between NAT (1-to-1) and PAT (many-to-1 via source ports)
- [ ] Can explain why `MASQUERADE` is used instead of `SNAT --to-source` on a dynamic-IP uplink
- [ ] Installed `conntrack` and read the live translation table
- [ ] Ran `./cleanup.sh` so **no NAT rule from this lab remains** (`iptables -t nat -L POSTROUTING -n` is clean)
- [ ] **Test it:** `conntrack -L` shows an entry with `src=10.1.1.2` translated to the host's address (`./verify.sh` prints `PASS: Lab 12 complete`)
