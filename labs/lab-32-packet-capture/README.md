# Lab 32 — Packet Capture and Filtering with tcpdump and the TIS PCAP Analyzer

When ping and traceroute don't find the answer, packet capture does. In this lab you will capture only DNS queries from one host, save them to a `.pcap`, then analyse the file in two ways: with `tshark` on the command line, and graphically in your browser using the **TIS PCAP Analyzer**.

**PCAP analyser (open in a browser tab):**
👉 https://alfredang.github.io/pcapanalyzer/

Run the Linux commands on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `tcpdump`
- `tshark` (text Wireshark)

---

## Step 1 — Install both tools

```bash
apt update && apt install -y tcpdump tshark
```

When tshark asks whether non-root users may capture, answer **No** for the lab.

---

## Step 2 — Capture 10 DNS packets from this host

```bash
tcpdump -i eth0 -nn -w /tmp/dns.pcap 'udp port 53 and src host 127.0.0.1' -c 10 &
sleep 1
for d in example.com cloudflare.com github.com; do dig +short @1.1.1.1 $d; done
wait
```

`-w` writes binary pcap; the BPF filter limits it to UDP/53 from loopback.

---

## Step 3 — Read the file with tshark

```bash
tshark -r /tmp/dns.pcap -Y "dns" -T fields \
  -e frame.time_relative -e dns.qry.name -e dns.qry.type
```

This prints just the queried name and record type per row.

---

## Step 4 — Filter only response packets

```bash
tshark -r /tmp/dns.pcap -Y "dns.flags.response==1"
```

---

## Step 5 — Generate a friendly summary

```bash
tcpdump -nn -r /tmp/dns.pcap | head
```

---

## Step 6 — Download the .pcap to your laptop

In the Killercoda terminal, base64 the file so you can copy it through the browser:

```bash
ls -lh /tmp/dns.pcap
base64 /tmp/dns.pcap > /tmp/dns.pcap.b64
cat /tmp/dns.pcap.b64
```

Copy all the printed text into a file called `dns.pcap.b64` on your laptop, then decode it back:

- macOS / Linux:
  ```bash
  base64 -d dns.pcap.b64 > dns.pcap
  ```
- Windows PowerShell:
  ```powershell
  [IO.File]::WriteAllBytes("dns.pcap", [Convert]::FromBase64String((Get-Content dns.pcap.b64 -Raw)))
  ```

(Or use `scp` if you have SSH access to the Killercoda VM.)

---

## Step 7 — Analyse the capture in the TIS PCAP Analyzer

Open the analyser in a browser tab:

```
https://alfredang.github.io/pcapanalyzer/
```

Steps:

1. Click **Upload PCAP** (or drag-and-drop `dns.pcap` onto the page).
2. The tool will parse the file and show:
   - A packet list with timestamps, source/destination IP, protocol and length.
   - A protocol summary (e.g. DNS = 100%).
   - Per-packet details — expand each row to see the Ethernet, IP, UDP, and DNS layers.
3. Use the search/filter box to narrow down packets, e.g. `example.com` or `dns`.
4. Confirm you see your three queries (`example.com`, `cloudflare.com`, `github.com`) and their replies.

---

## Step 8 — Quick analysis questions

Using the analyser, answer:
1. How many packets are in the capture?
2. What is the **source port** of each DNS query? (Should be a high random ephemeral port.)
3. What is the **destination port** of each query? (53)
4. What **transaction ID** does each query share with its matching response?
5. What **record type** (A, AAAA…) was requested?

---

## What you learned
- The difference between a **capture filter** (BPF) and a **display filter** (`-Y` / web search box).
- How to capture once and analyse many times by writing to a `.pcap`.
- How to use the **TIS PCAP Analyzer** at https://alfredang.github.io/pcapanalyzer/ for in-browser, no-install graphical analysis.
