# Lab 26 — Intrusion Detection with Suricata

Suricata is a free, open-source IDS/IPS. In this lab you will install it, update its rule set, generate a benign “attack” signature, and watch it light up in the alert log.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `suricata`
- `jq` (optional, for pretty-printing JSON alerts)

**Files in this lab folder:**

| File | Use |
|---|---|
| `local.rules` | The lab's own Suricata signatures — copied into `/etc/suricata/rules/` |
| `setup.sh` | Runs Steps 1–3: install, `suricata-update`, install the rules, start |
| `verify.sh` | Pass/fail check — triggers the signature and reads the alert from `eve.json` |
| `cleanup.sh` | **Run before Lab 27** — stops Suricata and removes the lab's rules |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

---

## Step 1 — Install Suricata

```bash
apt update && apt install -y suricata jq
```

> **Shortcut:** `./setup.sh` performs Steps 1–3 exactly as written below, plus
> the `local.rules` install. Read the steps first.

---

## Step 2 — Update the Emerging Threats community ruleset

```bash
suricata-update
```

### Add the lab's own rules

The ET feed covers real threats, but you cannot read 40,000 signatures. This lab
ships `local.rules` — six short signatures you *can* read end to end, and which
tie the other Domain 4 labs together:

```
# alert  proto  src_ip src_port -> dst_ip dst_port  (options)

alert http any any -> any any (msg:"LOCAL NETPLUS id check returned root"; \
    flow:established,to_client; \
    content:"uid=0|28|root|29|"; \
    classtype:bad-unknown; sid:1000001; rev:1;)

alert tcp any any -> $HOME_NET any (msg:"LOCAL NETPLUS possible TCP SYN port scan"; \
    flags:S; \
    threshold:type both, track by_src, count 30, seconds 10; \
    classtype:attempted-recon; sid:1000004; rev:1;)

alert icmp any any -> $HOME_NET any (msg:"LOCAL NETPLUS ICMP flood (possible DoS)"; \
    itype:8; \
    threshold:type both, track by_src, count 100, seconds 5; \
    classtype:attempted-dos; sid:1000005; rev:1;)
```

Read the anatomy: **action** (`alert`), **protocol**, **source → destination**,
then the options — `msg` is what lands in `fast.log`, `content` is the byte
pattern matched, `threshold` turns a single packet into a rate-based detection,
and `sid` uniquely identifies the rule (local rules must use 1000000 or above).
`rev` increments every time you edit the rule.

Install them and tell Suricata to load them:

```bash
cp local.rules /etc/suricata/rules/local.rules
sed -i '/^rule-files:/a\  - local.rules' /etc/suricata/suricata.yaml
suricata -T -c /etc/suricata/suricata.yaml -v
```

`suricata -T` is the config test — the Suricata equivalent of `sshd -t` in
Lab 23. Never start an IDS on a config you have not validated.

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

You should see an alert similar to `GPL ATTACK_RESPONSE id check returned root`,
and — because you installed `local.rules` — your own
`LOCAL NETPLUS id check returned root` with `sid 1000001` alongside it.

Check it objectively:

```bash
./verify.sh
```

It confirms Suricata is running with `local.rules` loaded, triggers the Step 4
request itself, waits for the log to flush, and prints the alert it found in
`eve.json` (timestamp, sid, signature). It exits non-zero if no alert fires.

---

## Step 6 — Stop Suricata

```bash
pkill suricata
```

Or run the script, which also removes the lab's rule file and restores
`suricata.yaml`:

```bash
./cleanup.sh
```

Suricata sniffs the interface promiscuously and writes to `eve.json`
continuously — leaving it running slows down every later capture and
troubleshooting lab. Your logs under `/var/log/suricata/` are left in place so
you can keep reading the alerts.

---

## Step 7 — Explore attack patterns in the TIS Cybersecurity Simulator

Open the **TIS Cybersecurity Simulator** (https://alfredang.github.io/cybersecuritysimulator/) in your browser and run the network-attack scenarios — DoS, ARP poisoning, port scanning and more — to see the traffic patterns your IDS must recognise. Relate each simulated pattern back to the Suricata rule categories you saw firing in `fast.log` and `eve.json`.

Three of the signatures in `local.rules` were written for exactly this exercise —
match each simulator scenario to the rule that would catch it:

| Simulator scenario | Rule in `local.rules` | `classtype` |
|---|---|---|
| Port scanning | sid `1000004` — 30 SYNs from one source in 10s | `attempted-recon` |
| DoS / flood | sid `1000005` — 100 ICMP echo requests in 5s | `attempted-dos` |
| Unauthorised database access | sid `1000006` — MySQL from outside `10.0.0.0/24` | `policy-violation` |

Finish by ticking off `checklist.md`.

---

## What you learned
- IDS (detect) vs IPS (detect + block).
- Where alert events live (`fast.log`, `eve.json`).
- Why community rule feeds (Emerging Threats, Snort VRT) are essential to keep coverage current.
- How simulated attack traffic (TIS Cybersecurity Simulator) maps to the signatures an IDS matches.
