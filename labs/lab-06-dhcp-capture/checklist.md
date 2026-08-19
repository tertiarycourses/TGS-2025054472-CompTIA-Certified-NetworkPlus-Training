# Lab 6 checklist — DHCP Lease Capture (DORA)

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y isc-dhcp-client tcpdump`
- [ ] Started the background capture: `tcpdump -i eth0 -nn -v 'port 67 or port 68' &`
- [ ] Explained why the filter uses UDP 67 (server) and UDP 68 (client)
- [ ] Released the existing lease with `dhclient -v -r eth0`
- [ ] Requested a new lease with `dhclient -v eth0`
- [ ] Saw **DHCPDISCOVER** broadcast from `0.0.0.0` to `255.255.255.255`
- [ ] Saw **DHCPOFFER** from the server carrying a proposed IP address
- [ ] Saw **DHCPREQUEST** from the client confirming which offer it accepted
- [ ] Saw **DHCPACK** from the server confirming the lease
- [ ] Recited the DORA mnemonic: Discover → Offer → Request → Acknowledge
- [ ] Stopped the capture with `kill %1`
- [ ] Ran `./cleanup.sh` so eth0 holds a working lease for the next lab
- [ ] **Test it:** all four DORA messages appear in order in the tcpdump output, and `ip -4 addr show eth0` afterwards shows a valid IPv4 address
