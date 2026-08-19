# Lab 20 checklist — Performance Baseline with iperf3

Tick each item as you complete it.

- [ ] Installed iperf3 with `apt update && apt install -y iperf3`
- [ ] Started the server in the background with `iperf3 -s -D`
- [ ] Ran the 10-second TCP test with `iperf3 -c 127.0.0.1 -t 10` and read the **Bitrate** column
- [ ] Ran four parallel streams with `iperf3 -c 127.0.0.1 -P 4 -t 10` and compared the total to the single-stream result
- [ ] Ran the UDP test with `iperf3 -c 127.0.0.1 -u -b 100M -t 10` and read **Jitter** and **Lost/Total Datagrams**
- [ ] Ran reverse mode with `iperf3 -c 127.0.0.1 -R -t 10` and explained when it is needed
- [ ] Explained why parallel streams reveal a window-limited link rather than a bandwidth-limited one
- [ ] Opened `data/baseline-metrics.csv` and read the filled reference rows
- [ ] Entered your own Step 3–6 figures into the four blank `lab-vm loopback` rows
- [ ] Identified which segment in the baseline sheet would fail a voice-quality target (jitter and loss)
- [ ] Stopped the server with `pkill iperf3` (or `./cleanup.sh`) and confirmed TCP/5201 is free
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — the server listens on TCP/5201, a short TCP run returns a receiver bitrate, and a short UDP run returns a jitter/loss summary
