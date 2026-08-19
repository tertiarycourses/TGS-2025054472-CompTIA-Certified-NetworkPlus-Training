# Lab 30 checklist — DNS Troubleshooting

Tick each item as you complete it.

- [ ] Installed `dnsutils` with `apt update && apt install -y dnsutils`
- [ ] Ran `cat /etc/resolv.conf` and `resolvectl status | head -20` and identified the active resolver
- [ ] Explained what `nameserver 127.0.0.53` means (going through systemd-resolved)
- [ ] Compared two upstreams with `dig @1.1.1.1 example.com +short` and `dig @8.8.8.8 example.com +short`
- [ ] Ran `dig +trace example.com` and named the three delegation levels (root → `.com` → authoritative)
- [ ] Timed a query with `time dig @1.1.1.1 example.com` and noted the response time
- [ ] Flushed the cache with `resolvectl flush-caches` and saw the counters reset in `resolvectl statistics`
- [ ] Can decode NOERROR, NXDOMAIN, SERVFAIL and REFUSED from the Step 7 table
- [ ] Ran `./break.sh` and reproduced the failure (`dig example.com +short` returns nothing)
- [ ] Diagnosed the fault: `cat /etc/resolv.conf` shows `10.99.0.53`, but `dig @1.1.1.1` still works — so the **resolver**, not the network, is broken
- [ ] Ran `./cleanup.sh` and confirmed the ORIGINAL `/etc/resolv.conf` was restored from `/tmp/resolv.conf.bak`
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — the black-hole resolver is gone and both the system resolver and `1.1.1.1` answer for `example.com`
