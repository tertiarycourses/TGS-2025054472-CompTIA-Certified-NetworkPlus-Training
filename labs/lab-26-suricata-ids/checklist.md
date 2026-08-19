# Lab 26 checklist — Intrusion Detection with Suricata

Tick each item as you complete it.

- [ ] Installed Suricata and jq with `apt update && apt install -y suricata jq`
- [ ] Ran `suricata-update` and saw the Emerging Threats ruleset download
- [ ] Installed `local.rules` to `/etc/suricata/rules/` and added it to `rule-files:` in `suricata.yaml`
- [ ] Read one signature in `local.rules` and identified the action, protocol, direction, `msg`, `sid` and `rev`
- [ ] Can explain why a local `sid` must be 1000000 or above
- [ ] Validated the config with `suricata -T -c /etc/suricata/suricata.yaml`
- [ ] Started Suricata with `suricata -i eth0 -D` and checked `/var/log/suricata/suricata.log`
- [ ] Triggered the test signature with `curl -s http://testmynids.org/uid/index.html`
- [ ] Found the alert in `/var/log/suricata/fast.log`
- [ ] Pretty-printed the same alert from `eve.json` with `jq 'select(.event_type=="alert")'`
- [ ] Can state the difference between IDS (detect) and IPS (detect + block)
- [ ] Ran the DoS, ARP-poisoning and port-scan scenarios in the TIS Cybersecurity Simulator (https://alfredang.github.io/cybersecuritysimulator/)
- [ ] Mapped each simulated attack pattern to a rule in `local.rules` (sid 1000004 scan, 1000005 flood, 1000006 policy)
- [ ] Stopped Suricata and ran `./cleanup.sh` — the daemon is stopped and `local.rules` removed
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — Suricata is running with `local.rules` loaded, and an `"event_type":"alert"` record appears in `/var/log/suricata/eve.json` after the test request
