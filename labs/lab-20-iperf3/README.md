# Lab 20 — Performance Baseline with iperf3

`iperf3` is the standard tool for measuring throughput, jitter, and packet loss between two endpoints. Always baseline a network when it is healthy so you know what “normal” looks like.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `iperf3`

**Files in this lab folder:**

| File | What it is |
|---|---|
| `run.sh` | runs Steps 1–6: install, start the server, then all four tests |
| `verify.sh` | objective pass/fail check — a TCP and a UDP run must return results |
| `cleanup.sh` | Step 7: stops the server and frees TCP/5201 |
| `data/baseline-metrics.csv` | baseline record with reference rows plus blanks for your results |
| `checklist.md` | tick-list of everything you should have done |

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

Steps 1–6 are also in `./run.sh`, which runs exactly these commands in order.

---

## Step 7 — Record the baseline

A measurement you do not write down is not a baseline. `data/baseline-metrics.csv` is a baseline record for the fictitious `nettech.local` estate — `link_segment,date,test_type,throughput_mbps,latency_ms,jitter_ms,loss_pct,notes` — with 13 reference rows already filled and four blank `lab-vm loopback` rows for your own results.

```bash
column -s, -t < data/baseline-metrics.csv | less -S
```

Fill the four blank rows with your Step 3–6 figures (TCP, TCP-P4, UDP, TCP-R), then read the filled rows as an operations engineer would:

```bash
# Every UDP result - the ones that carry jitter and loss
grep ',UDP,' data/baseline-metrics.csv

# The WAN circuits
grep 'WAN' data/baseline-metrics.csv
```

Note the `branch-rtr-jb` rows: single-stream TCP reached 94.2 Mbps but four parallel streams only reached 96.8 Mbps on the same 100 Mbps circuit. That circuit is bandwidth-limited, not window-limited — exactly the distinction `-P` exists to reveal.

---

## Step 8 — Stop the server

```bash
pkill iperf3
```

`./cleanup.sh` does this and confirms TCP/5201 is free for the next lab.

---

## Test it

```bash
./verify.sh
```

Expect `ALL CHECKS PASSED` — the server is listening on TCP/5201, a short TCP run returns a receiver bitrate, and a short UDP run returns a Jitter / Lost-Datagrams summary. Run it **before** `./cleanup.sh`. Work through `checklist.md` as you go.

---

## What you learned
- iperf3 measures TCP and UDP separately.
- Parallel streams (`-P`) can reveal whether a slow result is bandwidth- or window-limited.
- Reverse mode (`-R`) is essential for diagnosing asymmetric problems.
