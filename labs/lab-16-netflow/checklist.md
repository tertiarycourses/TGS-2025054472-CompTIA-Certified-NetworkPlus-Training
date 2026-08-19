# Lab 16 checklist — NetFlow Analysis with nfdump

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y nfdump fprobe`
- [ ] Accepted the default collector address at the `fprobe` prompt
- [ ] Created `/tmp/flows` and started the collector with `nfcapd -p 9995 -l /tmp/flows -D`
- [ ] Started the exporter with `fprobe -i eth0 127.0.0.1:9995`
- [ ] Generated traffic with `curl -s https://example.com > /dev/null` and `ping -c5 8.8.8.8`
- [ ] Waited ~60s for the collector to roll a file before running `nfdump`
- [ ] Listed the flows with `nfdump -R /tmp/flows -o long | head`
- [ ] Identified the top talkers with `nfdump -R /tmp/flows -s srcip`
- [ ] Identified the busiest destination ports with `nfdump -R /tmp/flows -s dstport`
- [ ] Explained why NetFlow shows the 5-tuple but never the packet payload
- [ ] Stopped both processes with `pkill fprobe` and `pkill nfcapd` (or `./cleanup.sh`)
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `nfcapd.*` files exist in `/tmp/flows`, `nfdump` reports at least one flow record, and `nfdump -s srcip` produces a top-talker report
