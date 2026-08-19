# Lab 35 — Simulating Slow / Lossy Links with tc

`tc` (traffic control) lets you add delay, jitter, and loss to an interface — perfect for reproducing customer “the WAN is slow” complaints in a lab.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2` (`tc` lives here)
- Kernel module `sch_netem`

---

## Step 1 — Baseline ping

```bash
ping -c5 8.8.8.8
```

Note the average RTT.

---

## Step 2 — Add 200 ms of delay

```bash
tc qdisc add dev eth0 root netem delay 200ms
ping -c5 8.8.8.8
```

The RTT should jump by ~200 ms.

---

## Step 3 — Add jitter

```bash
tc qdisc change dev eth0 root netem delay 200ms 50ms distribution normal
ping -c10 8.8.8.8
```

Each RTT now varies ±50 ms around 200 ms.

---

## Step 4 — Add packet loss

```bash
tc qdisc change dev eth0 root netem delay 200ms loss 5%
ping -c20 8.8.8.8
```

You should see roughly 1 in 20 packets time out.

---

## Step 5 — Limit bandwidth (token bucket filter)

```bash
tc qdisc del dev eth0 root
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
apt install -y iperf3
iperf3 -s -D
iperf3 -c 127.0.0.1 -t 5
```

Throughput will cap at 1 Mbit/s.

---

## Step 6 — Remove all shaping

```bash
tc qdisc del dev eth0 root
ping -c3 8.8.8.8
```

---

## What you learned
- `netem` (network emulator) injects delay, jitter, and loss.
- `tbf` (token bucket filter) shapes bandwidth.
- These tools let you reproduce WAN conditions on a single VM for application testing.
