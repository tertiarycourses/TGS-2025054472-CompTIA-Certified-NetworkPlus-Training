# Lab 17 checklist — Centralised Logging with Rsyslog

Tick each item as you complete it.

- [ ] Uncommented `module(load="imtcp")` and `input(type="imtcp" port="514")` in `/etc/rsyslog.conf`
- [ ] Read `50-forward.conf` and understood why the selector is `*.*` and the target uses `@@`
- [ ] Created the forwarding rule `*.* @@127.0.0.1:514` in `/etc/rsyslog.d/50-forward.conf`
- [ ] Restarted rsyslog and confirmed with `ss -tlnp | grep 514` that it listens on `:514`
- [ ] Injected a test event with `logger -p local0.info "Network+ Lab 17 test event"`
- [ ] Found the event with `grep "Lab 17 test" /var/log/syslog`
- [ ] Explained the difference between a facility (`auth`, `mail`, `local0`) and a severity (`info`, `warning`, `emerg`)
- [ ] Built an extended regex in the TIS Regex Generator (https://alfredang.github.io/regexgenerator/)
- [ ] Matched both test events in one pass with `grep -E 'Lab 1[0-9] test' /var/log/syslog`
- [ ] Ran the regex against `data/sample-syslog.log` and counted the matching lines
- [ ] Filtered `data/sample-syslog.csv` for the `emergency`, `alert` and `critical` rows an on-call engineer would page on
- [ ] Ran `./cleanup.sh` to remove the forwarding rule and disable the TCP receiver
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — rsyslog listens on TCP/514, the forwarding rule is in place, and a freshly injected `Lab 17 test` event appears in `/var/log/syslog`
