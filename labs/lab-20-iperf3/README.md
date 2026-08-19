# Lab 20 — Performance Baseline with iperf3

`iperf3` is the standard tool for measuring throughput, jitter, and packet loss between two endpoints. Always baseline a network when it is healthy so you know what “normal” looks like.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `iperf3`

---

## Step 1 — Install iperf3

```bash
apt update && apt install -y iperf3
```

---

## Step 2 — Run a server in the background

```bash
iperf3 -s -D
```

`-s` server mode, `-D` daemonise.

---

## Step 3 — TCP throughput test (10 seconds)

```bash
iperf3 -c 127.0.0.1 -t 10
```

Read the **Bitrate** column. On loopback you will see multi-Gbps; on a real link it should approach line rate (e.g. ~940 Mbps on a 1 Gbps link).

---

## Step 4 — Parallel streams (saturate WAN circuits)

```bash
iperf3 -c 127.0.0.1 -P 4 -t 10
```

`-P 4` opens four parallel streams. Useful when single-stream TCP cannot fill a high-latency link.

---

## Step 5 — UDP test (jitter + loss)

```bash
iperf3 -c 127.0.0.1 -u -b 100M -t 10
```

`-u` UDP, `-b 100M` send at 100 Mbps. The result shows **Jitter** (ms) and **Lost/Total Datagrams**.

---

## Step 6 — Reverse mode (server sends to client)

```bash
iperf3 -c 127.0.0.1 -R -t 10
```

Useful when asymmetric throughput is suspected (e.g. cable modem upstream vs downstream).

---

## Step 7 — Stop the server

```bash
pkill iperf3
```

---

## What you learned
- iperf3 measures TCP and UDP separately.
- Parallel streams (`-P`) can reveal whether a slow result is bandwidth- or window-limited.
- Reverse mode (`-R`) is essential for diagnosing asymmetric problems.
