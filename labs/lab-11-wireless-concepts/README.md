# Lab 11 — Wireless Concepts and Channel Survey

The Killercoda playground has no wireless radio, so this lab uses a mix of theory questions and a `iw` survey you can run on a real laptop. The N10-009 expects you to know 2.4 / 5 / 6 GHz behaviour, channels, and security modes.

**Required software (free):**
- On Linux laptop: `iw`, `wavemon` (`apt install iw wavemon`)
- On Windows laptop: **WiFi Analyzer** (free from Microsoft Store) or **Acrylic Wi-Fi Home** (free)
- On macOS: built-in **Wireless Diagnostics** (Option-click the Wi-Fi icon)

**Files shipped with this lab**

| File | Use |
|------|-----|
| `data/site-survey.csv` | Survey worksheet you fill in during Step 2 — example rows plus blank rows to extend |
| `checklist.md` | Tick-box list of everything you must be able to show |

This lab ships **no setup scripts**: it runs on your own laptop's wireless
adapter, not on the Linux playground.

---

## Step 1 — List supported PHYs (on a real wireless device)

```bash
iw list | less
```

Look for supported bands (2.4 / 5 / 6 GHz) and HT/VHT/HE capabilities.

---

## Step 2 — Scan nearby APs

```bash
iw dev wlan0 scan | grep -E "SSID|freq|signal|RSN|WPA"
```

For each AP record the SSID, channel, signal (dBm) and security (WPA2-PSK / WPA3-SAE).

Record them in the worksheet shipped with this lab — open
`data/site-survey.csv` in a spreadsheet or a text editor. It already contains
ten example rows showing the format; delete none of them, just add one row per
AP your own scan finds:

```
ssid,bssid,channel,band,rssi_dbm,security,notes
NETTECH-STAFF,02:1a:2b:00:10:01,1,2.4 GHz,-42,WPA3-SAE,...
```

Windows and macOS users: read the same columns off WiFi Analyzer / Wireless
Diagnostics and fill in the worksheet by hand.

---

## Step 3 — Map channels to bands

| Band | Non-overlapping channels | Notes |
|------|--------------------------|-------|
| 2.4 GHz | 1, 6, 11 | 20 MHz wide; congested |
| 5 GHz | 36–165 (DFS in middle) | 20/40/80/160 MHz |
| 6 GHz (Wi-Fi 6E) | 1–233 (PSC) | Requires WPA3 |

---

## Step 4 — Compare security modes

| Mode | Encryption | Key exchange | Notes |
|------|-----------|--------------|-------|
| WEP | RC4 | Static | Broken — never use |
| WPA2-PSK | AES-CCMP | 4-way handshake | Susceptible to PMKID attack |
| WPA2-Enterprise | AES-CCMP | 802.1X / RADIUS | Per-user creds |
| WPA3-SAE | AES-CCMP/GCMP | SAE (Dragonfly) | Forward secrecy |
| WPA3-Enterprise 192-bit | GCMP-256 | 802.1X | Government-grade |

---

## Step 5 — Quiz yourself
1. Why are 1/6/11 the only non-overlapping 2.4 GHz channels?
2. What does DFS stand for and why does it cause brief outages?
3. Why does Wi-Fi 6E require WPA3?

Use your completed `data/site-survey.csv` to answer a fourth question: which
two APs in your survey are on overlapping 2.4 GHz channels, and which AP is the
weakest-secured?

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- Channel layout for 2.4 / 5 / 6 GHz.
- The differences between WEP, WPA2, and WPA3.
- How to do a basic site survey using free tools.
