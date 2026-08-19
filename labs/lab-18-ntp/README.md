# Lab 18 — Time Synchronisation with Chrony

Many security and logging features fail when clocks drift. NTP synchronises clocks across the network using stratum hierarchy. Modern Ubuntu uses `chrony` instead of the legacy `ntpd`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `chrony`

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

---

## Step 5 — Force an immediate sync

```bash
chronyc -a makestep
```

---

## What you learned
- NTP uses UDP/123 and a stratum hierarchy.
- Chrony replaces `ntpd` on most modern Linux distributions.
- `chronyc tracking` is your one-stop diagnostic for clock drift.
