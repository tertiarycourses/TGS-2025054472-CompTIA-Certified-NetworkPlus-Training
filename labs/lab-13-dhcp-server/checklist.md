# Lab 13 checklist — DHCP Server with isc-dhcp-server

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Installed `isc-dhcp-server` with apt
- [ ] Created the `dum0` dummy interface and gave it 10.50.0.1/24
- [ ] Can explain why the lab uses a dummy interface instead of `eth0`
- [ ] Copied the provided `dhcpd.conf` into `/etc/dhcp/dhcpd.conf`
- [ ] Read the file and can name every element of the scope: `range`, `option routers`, `option subnet-mask`, `option domain-name-servers`, `option broadcast-address`
- [ ] Can explain what `default-lease-time`, `max-lease-time` and `authoritative` do
- [ ] Set `INTERFACESv4="dum0"` in `/etc/default/isc-dhcp-server`
- [ ] Started the service and confirmed `systemctl status isc-dhcp-server` shows *active (running)*
- [ ] Inspected `/var/lib/dhcp/dhcpd.leases` and can say what appears there once a real client connects
- [ ] Ran `./cleanup.sh` (or `systemctl stop isc-dhcp-server; ip link del dum0`) so the box is clean
- [ ] **Test it:** `dhcpd -t -cf /etc/dhcp/dhcpd.conf` parses without error and the service is active with the 10.50.0.0/24 scope loaded (`./verify.sh` prints `PASS: Lab 13 complete`)
