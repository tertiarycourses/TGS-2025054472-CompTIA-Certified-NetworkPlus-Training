# Lab 18 — Time Synchronisation with Chrony

Many security and logging features fail when clocks drift. NTP synchronises clocks across the network using stratum hierarchy. Modern Ubuntu uses `chrony` instead of the legacy `ntpd`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `chrony`

**Files in this lab folder:**

| File | What it is |
|---|---|
| `chrony.conf.lab` | the server line Step 4 appends to `/etc/chrony/chrony.conf` |
| `verify.sh` | objective pass/fail check — `chronyc sources` must show a synced source |
| `checklist.md` | tick-list of everything you should have done |

This lab changes no routing or interface state, so there is nothing to clean up.

---

## Step 1 — Install chrony

```bash
apt update && apt install -y chrony
systemctl enable --now chrony
```

---

## Step 2 — List your time sources

```bash
chronyc sources -v
```

Each line shows a server, its stratum, and offset from your clock. The `^*` symbol marks the currently selected source.

---

## Step 3 — Show synchronisation state

```bash
chronyc tracking
```

Key fields:
- **Stratum** — distance from a reference clock (Stratum 1 = GPS / atomic clock).
- **System time** — offset between your clock and NTP.
- **Last offset** / **RMS offset** — recent drift.

---

## Step 4 — Add an extra NTP server

```bash
echo "server time.cloudflare.com iburst" >> /etc/chrony/chrony.conf
systemctl restart chrony
chronyc sources -v
```

`iburst` sends a quick burst of packets at start so the source is selected faster.

The same line ships as `chrony.conf.lab` in this folder, with production notes in its comments:

```
server time.cloudflare.com iburst
```

so `cat chrony.conf.lab >> /etc/chrony/chrony.conf` is equivalent to the `echo` above.

---

## Step 5 — Force an immediate sync

```bash
chronyc -a makestep
```

---

## Test it

```bash
./verify.sh
```

Expect `ALL CHECKS PASSED` — `chronyd` is running, `chronyc sources -v` shows a `^*` selected source, `chronyc tracking` reports a usable stratum, and the Step 4 server line is present in `/etc/chrony/chrony.conf`. If the `^*` check fails, wait about a minute for chrony to settle and re-run. Work through `checklist.md` as you go.

---

## What you learned
- NTP uses UDP/123 and a stratum hierarchy.
- Chrony replaces `ntpd` on most modern Linux distributions.
- `chronyc tracking` is your one-stop diagnostic for clock drift.
