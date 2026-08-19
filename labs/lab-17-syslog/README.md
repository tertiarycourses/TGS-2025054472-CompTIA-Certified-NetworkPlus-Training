# Lab 17 — Centralised Logging with Rsyslog

Most network gear can forward log events over UDP/514 (or TCP/514) to a central collector. In this lab you will configure rsyslog to both **send** and **receive** on the same VM (loopback), proving the forwarding pipeline.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `rsyslog`

**Files in this lab folder:**

| File | What it is |
|---|---|
| `50-forward.conf` | the real forwarding rule Step 2 installs into `/etc/rsyslog.d/` |
| `setup.sh` | runs Steps 1–3 for you (idempotent) |
| `verify.sh` | objective pass/fail check — a test message must land in the aggregated log |
| `cleanup.sh` | removes the forwarding rule and disables the TCP receiver |
| `data/sample-syslog.log` | 42 realistic raw syslog lines to practise your regex on |
| `data/sample-syslog.csv` | the same events parsed into fields (facility, severity, host, message) |
| `checklist.md` | tick-list of everything you should have done |

---

## Step 1 — Enable the TCP receiver

```bash
sed -i 's/#module(load="imtcp")/module(load="imtcp")/' /etc/rsyslog.conf
sed -i 's/#input(type="imtcp" port="514")/input(type="imtcp" port="514")/' /etc/rsyslog.conf
```

The `imtcp` input module makes rsyslog listen on TCP/514.

---

## Step 2 — Add a forwarding rule

```bash
echo '*.* @@127.0.0.1:514' > /etc/rsyslog.d/50-forward.conf
```

The double `@@` means TCP (a single `@` would mean UDP).

The same rule ships as `50-forward.conf` in this folder — the whole file is one selector line:

```
*.* @@127.0.0.1:514
```

so `cp 50-forward.conf /etc/rsyslog.d/50-forward.conf` is equivalent to the `echo` above.

---

## Step 3 — Restart rsyslog

```bash
systemctl restart rsyslog
ss -tlnp | grep 514
```

You should see rsyslog listening on `:514`.

Steps 1–3 are also in `./setup.sh`, which runs exactly these commands.

---

## Step 4 — Generate a test event

```bash
logger -p local0.info "Network+ Lab 17 test event"
```

---

## Step 5 — Verify the event landed

```bash
grep "Lab 17 test" /var/log/syslog
```

---

## Step 6 — Inspect severity and facility

Rsyslog uses `facility.severity` selectors. Examples:
- `auth.warning` — authentication warnings
- `*.emerg` — emergency-level messages from any facility
- `mail.*` — every mail-related message

---

## Step 7 — Filter the aggregated log with a regex

Real collectors aggregate thousands of events — plain `grep` for a fixed string quickly stops being enough. Build an extended regex in the **TIS Regex Generator** (https://alfredang.github.io/regexgenerator/): paste a sample log line, describe the pattern you want to match (e.g. "Lab" followed by a two-digit number), and copy the generated expression. Then use it with `grep -E`:

```bash
logger -p local0.info "Network+ Lab 18 test event"
grep -E 'Lab 1[0-9] test' /var/log/syslog
```

The character class `1[0-9]` matches both the Lab 17 and Lab 18 test events in one pass — one regex instead of one grep per string.

---

## Step 8 — Practise on a realistic aggregated log

Your VM's `/var/log/syslog` only holds its own events. `data/sample-syslog.log` is 42 lines of what a collector actually receives from switches, routers, firewalls, a DHCP server, a WLC and a UPS — an emergency through to informational.

```bash
# The same regex, against the sample collector log
grep -E 'Lab 1[0-9] test' data/sample-syslog.log

# Every interface that flapped
grep -E 'GigabitEthernet[0-9/]+, changed state to (up|down)' data/sample-syslog.log

# Failed SSH logins, whoever the user was
grep -E 'Failed password for (invalid user )?[a-z]+ from 10\.' data/sample-syslog.log
```

`data/sample-syslog.csv` is the same event stream already parsed into `timestamp,host,facility,severity,severity_num,process,message`, which is how a SIEM stores it. Filter it by severity the way an on-call rota would:

```bash
# Everything an on-call engineer should be paged on (severity 0-2)
awk -F, '$5 <= 2' data/sample-syslog.csv

# Count events per host
cut -d, -f2 data/sample-syslog.csv | tail -n +2 | sort | uniq -c | sort -rn
```

---

## Step 9 — Clean up

```bash
./cleanup.sh
```

Removes `/etc/rsyslog.d/50-forward.conf`, re-comments the `imtcp` lines and restarts rsyslog.

---

## Test it

```bash
./verify.sh
```

Expect `ALL CHECKS PASSED` — rsyslog listens on TCP/514, the `*.* @@127.0.0.1:514` rule is in place, and a freshly injected `Lab 17 test` event appears in `/var/log/syslog`. Run it **before** `./cleanup.sh`. Work through `checklist.md` as you go.

---

## What you learned
- Syslog forwarding uses UDP/514 by default, TCP/514 for reliability, TCP/6514 for TLS.
- `imtcp`/`imudp` are rsyslog input modules that open the listening socket.
- `logger` is the easiest way to inject test events.
- Extended regexes (built in the TIS Regex Generator, run with `grep -E`) filter classes of events from an aggregated log.
