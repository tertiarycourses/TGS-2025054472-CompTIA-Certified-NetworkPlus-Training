# Lab 14 checklist — Authoritative DNS with BIND9

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Installed `bind9` and `dnsutils` with apt
- [ ] Copied the provided `db.lab.local` into `/etc/bind/`
- [ ] Read the zone file and can name all five SOA timers: serial, refresh, retry, expire, minimum
- [ ] Can explain why the serial must be bumped on every edit
- [ ] Can explain why `ns.lab.local.` and `mail.lab.local.` end in a trailing dot
- [ ] Identified each record type in the zone: `SOA`, `NS`, `A` (ns / www / mail), `MX 10`
- [ ] Appended the provided `named.conf.local` block so BIND is `type master` for `lab.local`
- [ ] Ran `named-checkconf` with no output (no output means no errors)
- [ ] Ran `named-checkzone lab.local /etc/bind/db.lab.local` and saw `OK`
- [ ] Restarted BIND9 and confirmed the service is running
- [ ] Queried `dig @127.0.0.1 www.lab.local` and found 10.0.0.10 in the ANSWER section
- [ ] Queried `dig @127.0.0.1 MX lab.local` and found `10 mail.lab.local.`
- [ ] Spotted the `aa` (authoritative answer) flag in the dig header
- [ ] *(Optional)* Installed the reverse zone and confirmed `dig -x 10.0.0.10` returns `www.lab.local.`
- [ ] Ran `./cleanup.sh` (or `systemctl stop bind9`) so the box is clean
- [ ] **Test it:** `dig @127.0.0.1 www.lab.local` returns 10.0.0.10 and `dig @127.0.0.1 MX lab.local` returns `10 mail.lab.local.` from your own server (`./verify.sh` prints `PASS: Lab 14 complete`)
