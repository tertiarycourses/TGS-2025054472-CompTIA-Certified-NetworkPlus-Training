# Lab 28 checklist — Layer 1/2 Diagnostics with ip and ethtool

Tick each item as you complete it.

- [ ] Installed `ethtool` with `apt update && apt install -y ethtool`
- [ ] Ran `ip -brief link show` and identified the state of every interface
- [ ] Explained the difference between `DOWN`, `UP`, `NO-CARRIER` and `LOWERLAYERDOWN`
- [ ] Ran `ethtool eth0` and read Speed, Duplex, Auto-negotiation and Link detected
- [ ] Ran `ip -s link show eth0` and located the RX/TX `errors` and `dropped` counters
- [ ] Ran `ethtool -S eth0 | grep -iE 'err|drop|crc|frame'` for the driver-level counters
- [ ] Bounced the interface with `ip link set eth0 down` / `ip link set eth0 up` and confirmed it came back UP
- [ ] Read Step 6 and can explain why you would *not* hard-set speed/duplex on a live NIC
- [ ] Opened `data/interface-errors.csv` and matched each error pattern to its likely cause
- [ ] Can state why a duplex mismatch produces high error counters *without* dropping the link
- [ ] **Test it:** `./run.sh` completes and `ip -brief link show eth0` reports `UP` after the interface bounce
