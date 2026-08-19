# Lab 5 checklist — DNS Record Types

Tick each item as you complete it.

- [ ] Installed `dig` with `apt update && apt install -y dnsutils`
- [ ] Queried an A record: `dig +short A google.com`
- [ ] Queried an AAAA record: `dig +short AAAA google.com`
- [ ] Queried an MX record and identified the priority number: `dig +short MX google.com`
- [ ] Queried a TXT record and spotted the SPF string: `dig +short TXT google.com`
- [ ] Queried NS records: `dig +short NS google.com`
- [ ] Queried a CNAME: `dig +short CNAME www.github.com`
- [ ] Performed a reverse PTR lookup: `dig +short -x 8.8.8.8`
- [ ] Queried the SOA and read the serial number: `dig +short SOA google.com`
- [ ] Queried an SRV record: `dig +short SRV _xmpp-server._tcp.gmail.com`
- [ ] Explained why a CNAME points at a name while an A record points at an IP
- [ ] Compared each answer against the reference set in `data/dns-records.csv`
- [ ] **Test it:** all ten record types return an answer — `dig +short A google.com` prints at least one IPv4 address and `dig +short MX google.com` prints at least one priority + mail host pair
