# Lab 4 checklist — Common Ports and Protocols

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y nmap net-tools`
- [ ] Listed local listening sockets with `ss -tulnp`
- [ ] Explained each `ss` flag: `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric, `-p` process
- [ ] Identified at least one familiar port in the `ss` output (22, 53, 80 or 443)
- [ ] Scanned the public test target with `nmap -sT -p 1-1024 scanme.nmap.org`
- [ ] Understood that `-sT` is a TCP connect scan and `-p 1-1024` is the well-known range
- [ ] Compared the open ports nmap reported against the Step 4 exam table
- [ ] Opened `data/well-known-ports.csv` and revised the full N10-009 port list
- [ ] Covered the port column and recalled each number from the service name alone
- [ ] Noted which services are UDP-only (DHCP, TFTP, NTP, SNMP, Syslog) and which run on both (DNS, SIP)
- [ ] Paired each cleartext protocol with its TLS equivalent (HTTP/HTTPS, LDAP/LDAPS, IMAP/IMAPS, POP3/POP3S)
- [ ] **Test it:** `getent services https` returns `https 443/tcp` and `getent services ssh` returns `ssh 22/tcp`, matching the CSV
