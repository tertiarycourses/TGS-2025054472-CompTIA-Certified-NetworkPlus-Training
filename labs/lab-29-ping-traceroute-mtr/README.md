# Lab 29 — ping, traceroute and mtr

These three tools answer the same question — “where is the slowness or loss?” — at different levels of detail.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `iputils-ping` (pre-installed)
- `traceroute`
- `mtr-tiny`

**Files in this lab folder:**

| File | Use |
|------|-----|
| `run.sh` | runs the whole path-analysis sequence (Steps 1–5) — or follow the steps by hand |
| `data/latency-log.csv` | worked example plus the format for recording your own results (Step 6) |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

---

## Step 1 — Install the tools

```bash
apt update && apt install -y traceroute mtr-tiny
```

---

## Step 2 — Baseline reachability with ping

```bash
ping -c5 8.8.8.8
```

Read **time=** for RTT and the loss summary at the end.

---

## Step 3 — Trace the hop-by-hop path

```bash
traceroute 8.8.8.8
```

Each line is one router on the way; columns are three RTT samples. `* * *` means the hop dropped ICMP — usually filtered, not actually broken.

---

## Step 4 — Combined live view with mtr

```bash
mtr -rwc 20 8.8.8.8
```

Flags:
- `-r` report mode (no curses).
- `-w` wide IP/host columns.
- `-c 20` 20 cycles.

The **Loss%** column tells you exactly where loss starts. Loss that **persists** all the way down indicates a real problem; loss only on one hop usually means that single router rate-limits ICMP.

---

## Step 5 — Use TCP traceroute when ICMP is blocked

```bash
apt install -y traceroute
traceroute -T -p 443 example.com
```

`-T` uses TCP SYN packets instead of UDP/ICMP, so they pass firewalls that block ping.

Run `./run.sh` to execute Steps 1–5 in one go.

---

## Step 6 — Record your results

`data/latency-log.csv` holds a worked example from a fictitious `nettech.local`
site. Read it first:

```bash
column -s, -t data/latency-log.csv | less -S
```

Note how hop 4 shows **100 % loss that does not persist** (an ICMP rate-limiting
router — ignore it), while the 4.5 % loss that starts at hop 7 **carries all the
way to the destination** — that is the real fault, and hop 7 is where it begins.

Now overwrite the rows with your own `mtr -rwc 20 8.8.8.8` output, one row per hop,
and answer:
1. At which hop does loss first appear in *your* trace?
2. Does it persist to the destination, or stop at that hop?
3. Where does the average RTT take its biggest single jump?

---

## What you learned
- ping measures end-to-end RTT and loss.
- traceroute reveals each L3 hop.
- mtr combines the two and updates continuously, making it the best first tool for path issues.
- TCP traceroute (`-T`) bypasses ICMP filters.

---

## Before you leave

Work through `checklist.md` and tick every line.
