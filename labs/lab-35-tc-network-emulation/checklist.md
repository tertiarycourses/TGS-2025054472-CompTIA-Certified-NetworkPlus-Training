# Lab 35 checklist — Simulating Slow / Lossy Links with tc

Tick each item as you complete it.

- [ ] Ran `./setup.sh` (or confirmed `tc`, `sch_netem` and `iperf3` by hand) before shaping anything
- [ ] Ran `ping -c5 8.8.8.8` and wrote down the **baseline** average RTT
- [ ] Added delay with `tc qdisc add dev eth0 root netem delay 200ms` and saw RTT jump by ~200 ms
- [ ] Added jitter with `tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal` and saw RTT vary ±50 ms
- [ ] Added loss with `tc qdisc change dev eth0 root netem delay 200ms loss 5%` and saw roughly 1 in 20 packets time out over `ping -c20`
- [ ] Swapped netem for a token bucket filter: `tc qdisc del dev eth0 root` then `tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms`
- [ ] Installed iperf3, started it with `iperf3 -s -D`, and measured with `iperf3 -c 127.0.0.1 -t 5`
- [ ] Confirmed throughput capped at ~1 Mbit/s
- [ ] Can explain the difference between `netem` (delay/jitter/loss) and `tbf` (bandwidth shaping)
- [ ] Removed all shaping with `tc qdisc del dev eth0 root`
- [ ] **Ran `./cleanup.sh`** — this is mandatory; a leftover qdisc degrades every later lab on this box
- [ ] **Test it:** after `./cleanup.sh`, `tc qdisc show dev eth0` shows no `netem` or `tbf` line and `ping -c3 8.8.8.8` returns to the Step 1 baseline RTT
