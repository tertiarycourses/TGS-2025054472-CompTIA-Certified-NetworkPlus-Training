# Lab 29 checklist — ping, traceroute and mtr

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y traceroute mtr-tiny`
- [ ] Ran `ping -c5 8.8.8.8` and read both the `time=` RTT values and the loss summary
- [ ] Ran `traceroute 8.8.8.8` and counted the number of L3 hops to the destination
- [ ] Explained what a `* * *` line means (hop filters ICMP — not necessarily broken)
- [ ] Ran `mtr -rwc 20 8.8.8.8` and can name what `-r`, `-w` and `-c 20` do
- [ ] Located the first hop in the `Loss%` column where loss appears
- [ ] Decided whether that loss **persists** to the destination (real fault) or stops (ICMP rate limiting)
- [ ] Ran `traceroute -T -p 443 example.com` and saw it get further than the UDP/ICMP trace
- [ ] Recorded your own hop, loss %, and min/avg/max values in `data/latency-log.csv`
- [ ] Can state which of the three tools you would reach for first on a "the WAN is slow" ticket
- [ ] **Test it:** `mtr -rwc 20 8.8.8.8` completes and the final row shows the destination `8.8.8.8` with its end-to-end `Loss%` and `Avg` RTT
