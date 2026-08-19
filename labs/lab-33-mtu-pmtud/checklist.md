# Lab 33 checklist — MTU and Path-MTU Discovery

Tick each item as you complete it.

- [ ] Ran `ip -brief link show eth0` and read the interface MTU (standard Ethernet = 1500)
- [ ] Can do the maths: payload = MTU − 20 (IP) − 8 (ICMP), so 1500 − 28 = **1472**
- [ ] Ran `ping -M do -s 1472 -c2 8.8.8.8` and got replies
- [ ] Ran `ping -M do -s 1500 -c2 8.8.8.8` and saw `ping: local error: message too long, mtu=1500`
- [ ] Explained what `-M do` does (sets the Don't Fragment bit)
- [ ] Lowered the MTU with `ip link set eth0 mtu 1400`
- [ ] Confirmed `ping -M do -s 1400` now fails and `ping -M do -s 1372` succeeds (1400 − 28 = 1372)
- [ ] Restored the MTU with `ip link set eth0 mtu 1500` (or `./cleanup.sh`)
- [ ] Can describe the PMTUD blackhole symptom: small pings and SSH work, downloads hang on the first big packet
- [ ] Can name the fix: TCP MSS clamping with `iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`
- [ ] **Test it:** after `./cleanup.sh`, `ip -brief link show eth0` shows `mtu 1500` and `ping -M do -s 1472 -c2 8.8.8.8` succeeds again
