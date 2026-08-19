# Lab 7 checklist — Simulating a Cloud VPC with Network Namespaces

Tick each item as you complete it.

- [ ] Created both namespaces with `ip netns add web` and `ip netns add db`
- [ ] Explained why a namespace has its own routing table, interfaces and firewall
- [ ] Created the bridge with `ip link add br0 type bridge` and brought it up
- [ ] Identified the bridge as the Linux equivalent of a virtual switch
- [ ] Created both veth pairs: `veth-web`/`br-web` and `veth-db`/`br-db`
- [ ] Enslaved `br-web` and `br-db` to `br0` with `ip link set ... master br0`
- [ ] Brought the bridge-side ends up
- [ ] Moved `veth-web` into the `web` namespace and `veth-db` into the `db` namespace
- [ ] Assigned `10.0.1.10/24` in `web` and `10.0.1.20/24` in `db`
- [ ] Brought up `veth-web`, `veth-db` and `lo` inside both namespaces
- [ ] Explained why the two hosts need no router to talk (same /24, one bridge)
- [ ] Mapped the topology to AWS terms: namespace = VM, bridge = VPC subnet switch
- [ ] Tore the topology down with `./cleanup.sh` (or `ip netns del web`, `ip netns del db`, `ip link del br0`)
- [ ] **Test it:** `ip netns exec web ping -c2 10.0.1.20` gets replies — or `./verify.sh` reports `ALL CHECKS PASSED`
