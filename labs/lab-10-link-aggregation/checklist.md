# Lab 10 checklist — Link Aggregation (LACP Bond)

Tick each box as you complete it. The trainer uses the same list to observe you.

- [ ] Installed `ifenslave` with `apt install -y ifenslave`
- [ ] Loaded the bonding driver with `modprobe bonding mode=802.3ad miimon=100`
- [ ] Can explain what `mode=802.3ad` and `miimon=100` each control
- [ ] Created the bond with `ip link add bond0 type bond mode 802.3ad`
- [ ] Read the Step 3 warning and understand why enslaving the only NIC disconnects Killercoda
- [ ] Enslaved at least one interface (`ip link set eth0 master bond0`) and brought `bond0` up
- [ ] Read `/proc/net/bonding/bond0` and located the aggregator ID, the LACP partner MAC and the per-slave link state
- [ ] Can name two other bonding modes (active-backup, balance-rr) and when each is used
- [ ] Ran `./cleanup.sh` (or `ip link set eth0 nomaster; ip link del bond0`) so the box is clean
- [ ] **Test it:** `cat /proc/net/bonding/bond0` lists every slave with `MII Status: up` (`./verify.sh` prints `PASS: Lab 10 complete`)
