# Lab 1 checklist — OSI Model Packet Inspection

Tick each item as you complete it.

- [ ] Installed `tcpdump` and `curl` with `apt install -y tcpdump curl`
- [ ] Ran `ip -brief addr` and identified the UP interface (usually `eth0`)
- [ ] Started a background capture with `tcpdump -i eth0 -nn -v -c 5 'tcp port 80' &`
- [ ] Generated HTTP traffic with `curl -s http://example.com > /dev/null`
- [ ] Read a captured line and identified the Layer 3 source/destination IP
- [ ] Identified the Layer 4 TCP ports and the `Flags [S]` field
- [ ] Re-ran with `-e -A` and saw the Layer 2 MAC addresses
- [ ] Saw the Layer 7 `GET / HTTP/1.1` request text in the ASCII payload
- [ ] Stopped the background capture with `kill %1`
- [ ] Saved a capture to `osi-lab.pcap` with `tcpdump -i eth0 -nn -w osi-lab.pcap -c 20 'tcp port 80'`
- [ ] Opened the TIS PCAP Analyzer at https://alfredang.github.io/pcapanalyzer/ and loaded `osi-lab.pcap`
- [ ] Stepped through one packet in the analyzer and matched all four layers to the Step 5 table
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `osi-lab.pcap` exists, is non-empty, and decodes to at least one packet
