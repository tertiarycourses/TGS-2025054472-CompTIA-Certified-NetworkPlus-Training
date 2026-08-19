# Lab 1 — OSI Model Packet Inspection

In this lab you will capture real network traffic and map each protocol header to a layer of the OSI model. You will use `tcpdump`, the most common command-line packet sniffer on Linux, together with `curl` to generate HTTP traffic. By the end you will be able to point at a captured packet and say which header belongs to Layer 2, Layer 3, Layer 4, and Layer 7.

Run all commands on the Killercoda Ubuntu Playground:
https://killercoda.com/playgrounds/scenario/ubuntu

**Files in this lab folder**

| File | Use |
|---|---|
| `run.sh` | runs the whole capture + traffic sequence (Steps 1–7) in one go |
| `verify.sh` | checks the saved `osi-lab.pcap` exists, is non-empty and decodes |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

Work through the steps by hand first — the point of the lab is reading the packets.
Use `./run.sh` if you fall behind or want to regenerate a capture quickly.

---

## Step 1 — Install the capture tools

`tcpdump` is not always pre-installed. The `apt` package manager will fetch it from the Ubuntu repositories. We also install `curl` to generate predictable test traffic.

```bash
apt update && apt install -y tcpdump curl
```

`apt update` refreshes the local package index so `apt install` can find the latest version. The `-y` flag automatically answers “yes” to the install prompt.

---

## Step 2 — Identify the active interface

Before capturing, you need to know which Network Interface Card (NIC) is connected to the internet. On Killercoda this is usually `eth0`.

```bash
ip -brief addr
```

You should see output similar to:

```
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             10.244.0.5/24 ...
```

The interface marked `UP` with a routable IP is the one to capture on.

---

## Step 3 — Start a capture in the background

We will tell `tcpdump` to capture five packets on TCP port 80 (HTTP). The `&` symbol sends the command to the background so you can run another command in the same terminal.

```bash
tcpdump -i eth0 -nn -v -c 5 'tcp port 80' &
```

Flag breakdown:
- `-i eth0` — listen on the eth0 interface
- `-nn` — do not resolve hostnames or port names (faster, clearer)
- `-v` — verbose output, shows IP TTL and TCP flags
- `-c 5` — stop after 5 packets
- `'tcp port 80'` — Berkeley Packet Filter expression

---

## Step 4 — Generate HTTP traffic

In the same terminal, request a small web page. This will fill the capture buffer with real packets.

```bash
curl -s http://example.com > /dev/null
```

`-s` makes curl silent, and `> /dev/null` discards the HTML so you only see tcpdump output.

---

## Step 5 — Read the captured packet and map it to the OSI model

You will see something like:

```
IP 10.244.0.5.55512 > 93.184.216.34.80: Flags [S], seq 123, win 64240 ...
```

Match each piece to a layer:

| OSI Layer | Header you see | Example value |
|-----------|---------------|---------------|
| Layer 2 — Data Link | `link/ether` MAC addresses (visible with `-e`) | `00:16:3e:...` |
| Layer 3 — Network | `IP` source/destination | `10.244.0.5 > 93.184.216.34` |
| Layer 4 — Transport | `TCP` ports + `Flags` | `55512 > 80 [S]` |
| Layer 7 — Application | The HTTP request body | `GET / HTTP/1.1` |

Re-run with `-e -A` to also see Layer 2 MACs and the Layer 7 ASCII payload:

```bash
tcpdump -i eth0 -nn -e -A -c 10 'tcp port 80' &
curl -s http://example.com > /dev/null
```

---

## Step 6 — Stop background captures

```bash
kill %1 2>/dev/null
```

`%1` refers to the first background job in this shell.

---

## Step 7 — Inspect the capture in the TIS PCAP Analyzer

Save a fresh capture to a file, then analyze it visually in the free **TIS PCAP Analyzer**:

```bash
tcpdump -i eth0 -nn -w osi-lab.pcap -c 20 'tcp port 80' &
curl -s http://example.com > /dev/null
```

Download `osi-lab.pcap` from the Killercoda editor, then open the analyzer in a browser tab:

👉 https://alfredang.github.io/pcapanalyzer/

Load the file and step through each packet layer-by-layer — the analyzer decodes the Layer 2 Ethernet header, the Layer 3 IP header, the Layer 4 TCP header, and the Layer 7 HTTP payload, matching the mapping table from Step 5.

Before you download it, confirm the capture actually holds packets:

```bash
./verify.sh
```

It prints a `PASS:`/`FAIL:` line for each check and exits non-zero if the `.pcap` is
missing or empty — the usual cause being that no traffic was generated while `tcpdump`
was running.

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- How to install and run `tcpdump` on Ubuntu.
- How to filter captures with a BPF expression.
- How to identify which OSI layer each header in a packet belongs to.
- How to inspect a saved `.pcap` layer-by-layer in the **TIS PCAP Analyzer** at https://alfredang.github.io/pcapanalyzer/
