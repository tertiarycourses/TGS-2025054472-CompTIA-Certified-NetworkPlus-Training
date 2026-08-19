# Lab 36 checklist — Service Reachability Triage (capstone)

Tick each item as you complete it.

- [ ] Installed the tools with `apt update && apt install -y curl netcat-openbsd openssl`
- [ ] Tested Layer 4 with `nc -zv example.com 443` and saw the `succeeded` line
- [ ] Explained what a successful TCP handshake already proves (routing, firewall and listener are fine)
- [ ] Tested Layer 6 with `echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | head -20`
- [ ] Read `subject=`, `issuer=` and `Verify return code: 0 (ok)` from the TLS output
- [ ] Tested Layer 7 with `curl -v https://example.com 2>&1 | head -30` and read the status code
- [ ] Can decode 200 / 301 / 401 / 403 / 404 / 500 / 502-503-504 from the Step 4 table
- [ ] Ran the timing breakdown with `curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} TTFB:%{time_starttransfer} TOTAL:%{time_total}\n" -o /dev/null -s https://example.com`
- [ ] Identified which phase (DNS / TCP / TLS / TTFB) dominates the total time
- [ ] Walked the Step 6 decision tree and can say which tool to reach for at each branch
- [ ] Ran `./break.sh` and met the fault cold, without being told what it was
- [ ] Completed **all seven steps** of `troubleshooting-worksheet.md`, writing the theory down in Step 2 *before* testing it in Step 3
- [ ] Identified the root cause and matched it to the correct OSI layer
- [ ] Ran `./cleanup.sh` and confirmed the ORIGINAL iptables rules were restored from `/tmp/lab36-iptables.bak`
- [ ] **Test it:** after `./cleanup.sh`, `nc -zv example.com 443` reports `succeeded` and `curl -o /dev/null -s -w "%{http_code}\n" https://example.com` returns `200`
