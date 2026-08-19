# Lab 25 checklist — Port Scanning and Service Hardening

Tick each item as you complete it.

- [ ] Installed nmap with `apt update && apt install -y nmap`
- [ ] Confirmed you are scanning **only** `127.0.0.1`, a host you own
- [ ] Ran the full TCP sweep `nmap -sS -p- 127.0.0.1` and noted every open port
- [ ] Can explain what makes `-sS` a "half-open" scan and why it is quieter than `-sT`
- [ ] Ran `nmap -sV -p 22,80,443 127.0.0.1` and recorded the service banners and versions
- [ ] Ran the OS fingerprint `nmap -O 127.0.0.1` and can say why it needs root
- [ ] Cross-checked with `ss -tulnp` and matched each open port to its owning process
- [ ] Asked, for every open port, *do I need this service running?*
- [ ] Disabled an unneeded service with `systemctl disable --now apache2` (or confirmed none was present)
- [ ] Re-scanned with `nmap -sS -p 80 127.0.0.1` and saw the port change state
- [ ] Completed `data/port-scan-findings.csv` — host, port, state, service, version, risk and action for every finding
- [ ] Can state the difference between `-sS`, `-sT`, `-sU` and `-sV`
- [ ] **Test it:** `./run.sh` completes, `scan-results.txt` contains the Step 2 full-port scan and the Step 7 re-scan, and the port-80 re-scan shows the state you expect after Step 6
