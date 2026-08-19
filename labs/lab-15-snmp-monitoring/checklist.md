# Lab 15 checklist — SNMP Monitoring

Tick each item as you complete it.

- [ ] Installed the agent and client with `apt install -y snmpd snmp snmp-mibs-downloader`
- [ ] Read `snmpd.conf.lab` and understood both directives before applying them
- [ ] Set `agentaddress udp:127.0.0.1:161` in `/etc/snmp/snmpd.conf`
- [ ] Appended `rocommunity public 127.0.0.1` and restarted with `systemctl restart snmpd`
- [ ] Walked system info with `snmpwalk -v2c -c public 127.0.0.1 system` and found `sysDescr`, `sysName`, `sysUpTime`
- [ ] Fetched a single OID with `snmpget -v2c -c public 127.0.0.1 sysUpTime.0`
- [ ] Listed interfaces with `snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifDescr`
- [ ] Read the counters with `snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifInOctets`
- [ ] Opened `data/device-inventory.csv` and identified every device still polled with SNMP v1
- [ ] Listed the devices in the inventory whose `eol_date` falls inside the next 12 months
- [ ] Explained why `rocommunity public` is unsafe on a production network (v2c community strings are cleartext — use v3)
- [ ] Ran `./cleanup.sh` to stop `snmpd` and remove the lab community string
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `snmpget` returns a value for `sysDescr.0` and `sysUpTime.0`, and `IF-MIB::ifDescr` lists at least one interface
