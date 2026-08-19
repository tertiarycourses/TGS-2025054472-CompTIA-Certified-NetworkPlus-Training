# Lab 31 checklist — ARP and the IPv6 Neighbour Table

Tick each item as you complete it.

- [ ] Ran `ip neigh` and read the `<IP> dev <iface> lladdr <MAC> STATE` format
- [ ] Can explain `REACHABLE`, `STALE`, `INCOMPLETE` and `FAILED`
- [ ] Installed `iputils-arping` with `apt update && apt install -y iputils-arping`
- [ ] Probed the gateway with `arping -I eth0 -c2 $(ip route | awk '/default/ {print $3}')`
- [ ] Ran duplicate address detection with `arping -D -I eth0 -c2 <own IP>` and know what "address already in use" means
- [ ] Added a static entry with `ip neigh add 10.0.0.99 lladdr de:ad:be:ef:00:01 dev eth0` and saw it in `ip neigh`
- [ ] Flushed the table with `ip neigh flush all` and watched it repopulate after generating traffic
- [ ] Ran `ip -6 neigh` and compared the IPv6 neighbour cache with the IPv4 ARP table
- [ ] Sent an ICMPv6 Neighbour Solicitation with `ndisc6 ff02::1 eth0`
- [ ] Opened `data/arp-table.csv` and found the **duplicate MAC** and the two unresolved entries
- [ ] Can state why ARP does not exist in IPv6 and what replaces it (NDP / ICMPv6)
- [ ] **Test it:** after `ip neigh flush all` and a ping to the gateway, `ip neigh` shows the gateway back in `REACHABLE` (or `STALE`) state
