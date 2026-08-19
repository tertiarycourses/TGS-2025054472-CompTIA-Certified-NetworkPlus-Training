# Lab 26 — Intrusion Detection with Suricata

Suricata is a free, open-source IDS/IPS. In this lab you will install it, update its rule set, generate a benign “attack” signature, and watch it light up in the alert log.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `suricata`
- `jq` (optional, for pretty-printing JSON alerts)

---

## Step 1 — Install Suricata

```bash
apt update && apt install -y suricata jq
```

---

## Step 2 — Update the Emerging Threats community ruleset

```bash
suricata-update
```

---

## Step 3 — Identify the active interface and start Suricata

```bash
suricata -i eth0 -D
sleep 5
tail /var/log/suricata/suricata.log
```

`-D` daemonises the process.

---

## Step 4 — Trigger a test signature

The NIDS test page generates traffic that matches a well-known ET rule.

```bash
curl -s http://testmynids.org/uid/index.html >/dev/null
```

---

## Step 5 — Inspect the alert log

```bash
tail /var/log/suricata/fast.log
cat /var/log/suricata/eve.json | jq 'select(.event_type=="alert")' | head -20
```

You should see an alert similar to `GPL ATTACK_RESPONSE id check returned root`.

---

## Step 6 — Stop Suricata

```bash
pkill suricata
```

---

## Step 7 — Explore attack patterns in the TIS Cybersecurity Simulator

Open the **TIS Cybersecurity Simulator** (https://alfredang.github.io/cybersecuritysimulator/) in your browser and run the network-attack scenarios — DoS, ARP poisoning, port scanning and more — to see the traffic patterns your IDS must recognise. Relate each simulated pattern back to the Suricata rule categories you saw firing in `fast.log` and `eve.json`.

---

## What you learned
- IDS (detect) vs IPS (detect + block).
- Where alert events live (`fast.log`, `eve.json`).
- Why community rule feeds (Emerging Threats, Snort VRT) are essential to keep coverage current.
- How simulated attack traffic (TIS Cybersecurity Simulator) maps to the signatures an IDS matches.
