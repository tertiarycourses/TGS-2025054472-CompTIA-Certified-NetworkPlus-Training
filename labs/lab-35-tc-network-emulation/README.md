# Lab 35 — Simulating Slow / Lossy Links with tc

`tc` (traffic control) lets you add delay, jitter, and loss to an interface — perfect for reproducing customer “the WAN is slow” complaints in a lab.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2` (`tc` lives here)
- Kernel module `sch_netem`

**Files in this lab folder:**

| File | Use |
|------|-----|
| `setup.sh` | checks `tc`, loads `sch_netem`, installs `iperf3`, clears any leftover qdisc |
| `run.sh` | runs the shaping sequence (Steps 1–6) — or follow the steps by hand |
| `cleanup.sh` | **mandatory** — deletes the `eth0` root qdisc and stops the iperf3 server |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

> ⚠️ **You MUST run `./cleanup.sh` before leaving this lab.** A qdisc left on
> `eth0` keeps the link delayed, lossy or rate-limited, and **every later lab on
> this box will look broken**. This is the single most important cleanup in the
> whole course.

Start by preparing the box:

```bash
./setup.sh
```

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

Steps 1–6 are scripted: `./run.sh` runs every shaping command above and removes
the qdisc on the way out.

Then, **always**, run the cleanup:

```bash
./cleanup.sh
```

It deletes any remaining `eth0` root qdisc, stops the backgrounded `iperf3 -s -D`
server from Step 5, and pings once more so you can confirm the RTT is back to
your Step 1 baseline. Check the qdisc yourself:

```bash
tc qdisc show dev eth0
```

A plain `pfifo_fast`, `fq_codel` or `noqueue` line means `eth0` is unshaped. If
you still see `netem` or `tbf`, the box is still degraded — run `./cleanup.sh`
again.

---

## What you learned
- `netem` (network emulator) injects delay, jitter, and loss.
- `tbf` (token bucket filter) shapes bandwidth.
- These tools let you reproduce WAN conditions on a single VM for application testing.
- Why emulation must always be torn down — a forgotten qdisc becomes someone else's mystery outage.

---

## Before you leave

Run `./cleanup.sh` and confirm `tc qdisc show dev eth0` shows no `netem` or `tbf`,
then work through `checklist.md` and tick every line.
