# Lab 16 — NetFlow Analysis with nfdump

NetFlow records statistics about each conversation traversing a router (5-tuple, byte/packet counts). In this lab you will run a flow exporter (`fprobe`) and a collector (`nfcapd`) on the same VM, then analyse the flows with `nfdump`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `nfdump`
- `fprobe`

---

## Step 1 — Install the tools

```bash
apt update && apt install -y nfdump fprobe
```

When prompted by `fprobe`, accept the default collector address.

---

## Step 2 — Start the collector

```bash
mkdir -p /tmp/flows
nfcapd -p 9995 -l /tmp/flows -D
```

`-D` daemonises; `-p 9995` is the UDP port; `-l` is the output directory.

---

## Step 3 — Start the exporter

```bash
fprobe -i eth0 127.0.0.1:9995
```

`fprobe` reads packets from eth0 and emits NetFlow v5 records.

---

## Step 4 — Generate traffic

```bash
curl -s https://example.com > /dev/null
ping -c5 8.8.8.8
```

---

## Step 5 — Analyse the flows

```bash
sleep 60   # wait for the collector to roll a file
nfdump -R /tmp/flows -o long | head
nfdump -R /tmp/flows -s srcip
nfdump -R /tmp/flows -s dstport
```

`-s srcip` summarises top talker IPs; `-s dstport` shows the busiest destination ports.

---

## Step 6 — Clean up

```bash
pkill fprobe
pkill nfcapd
```

---

## What you learned
- NetFlow exports a 5-tuple summary, not packet contents.
- A typical deployment has many exporters and one central collector.
- `nfdump -s` builds top-N reports useful for capacity planning and incident response.
