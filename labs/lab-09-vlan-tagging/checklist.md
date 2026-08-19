# Lab 9 checklist — 802.1Q VLAN Tagging

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Loaded the `8021q` kernel module and confirmed it with `lsmod | grep 8021q`
- [ ] Created `eth0.10` as a VLAN sub-interface with `id 10`
- [ ] Created `eth0.20` as a VLAN sub-interface with `id 20`
- [ ] Assigned 192.168.10.1/24 to `eth0.10` and 192.168.20.1/24 to `eth0.20`
- [ ] Brought both sub-interfaces up
- [ ] Ran `ip -d link show eth0.10` and located the VLAN ID in the `-d` output
- [ ] Read `data/vlan-plan.csv` and can say which VLANs are tagged on a trunk and which are untagged access ports
- [ ] Installed `tcpdump` and captured traffic on `eth0` with `-e vlan`
- [ ] Can explain why the tag is 4 bytes and where it sits in the Ethernet header
- [ ] Ran `./cleanup.sh` (or `ip link del eth0.10; ip link del eth0.20`) so the box is clean
- [ ] **Test it:** `tcpdump -i eth0 -nn -e vlan` shows a frame tagged `vlan 10` while pinging out of `eth0.10` (`./verify.sh` prints `PASS: Lab 9 complete`)
