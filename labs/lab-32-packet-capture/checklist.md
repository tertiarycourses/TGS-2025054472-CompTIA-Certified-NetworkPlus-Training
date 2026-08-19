# Lab 32 checklist — Packet Capture with tcpdump and the TIS PCAP Analyzer

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y tcpdump tshark` (answered **No** to the non-root capture prompt)
- [ ] Captured 10 DNS packets to `/tmp/dns.pcap` with the BPF filter `'udp port 53 and src host 127.0.0.1'`
- [ ] Generated the traffic with the `dig +short @1.1.1.1` loop over `example.com`, `cloudflare.com`, `github.com`
- [ ] Read the file back with `tshark -r /tmp/dns.pcap -Y "dns" -T fields -e frame.time_relative -e dns.qry.name -e dns.qry.type`
- [ ] Filtered responses only with `tshark -r /tmp/dns.pcap -Y "dns.flags.response==1"`
- [ ] Printed the summary with `tcpdump -nn -r /tmp/dns.pcap | head`
- [ ] Exported the capture with `base64 /tmp/dns.pcap > /tmp/dns.pcap.b64` and decoded it on your laptop
- [ ] Opened https://alfredang.github.io/pcapanalyzer/ and uploaded `dns.pcap`
- [ ] Saw the packet list, the protocol summary, and expanded one packet's Ethernet / IP / UDP / DNS layers
- [ ] Answered all five Step 8 questions: packet count, ephemeral source port, destination port 53, matching transaction ID, record type
- [ ] Can explain the difference between a **capture filter** (BPF, before capture) and a **display filter** (`-Y` or the web search box, after capture)
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `/tmp/dns.pcap` exists, is non-empty, decodes to at least one packet, and contains DNS query names
