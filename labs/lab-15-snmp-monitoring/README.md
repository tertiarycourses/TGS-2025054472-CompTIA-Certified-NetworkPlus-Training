# Lab 15 — SNMP Monitoring

SNMP (Simple Network Management Protocol) lets a manager poll devices for system metrics. In this lab you will install an SNMP agent, configure a community string, and walk the MIB.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `snmpd` (agent)
- `snmp` (client tools: `snmpwalk`, `snmpget`)
- `snmp-mibs-downloader` (optional, for friendly OID names)

**Files in this lab folder:**

| File | What it is |
|---|---|
| `snmpd.conf.lab` | the two agent directives Step 2 adds to `/etc/snmp/snmpd.conf` |
| `setup.sh` | runs Steps 1–2 for you (idempotent) |
| `verify.sh` | objective pass/fail check — `snmpget` must return a value |
| `cleanup.sh` | stops `snmpd` and removes the lab community string |
| `data/device-inventory.csv` | 20-device asset inventory used in Step 6 |
| `checklist.md` | tick-list of everything you should have done |

---

## Step 1 — Install agent and client

```bash
apt update && apt install -y snmpd snmp snmp-mibs-downloader
```

---

## Step 2 — Configure a read-only community

```bash
sed -i 's/^agentaddress.*/agentaddress udp:127.0.0.1:161/' /etc/snmp/snmpd.conf
echo 'rocommunity public 127.0.0.1' >> /etc/snmp/snmpd.conf
systemctl restart snmpd
```

`rocommunity public` allows read-only queries with the community string `public` (default and insecure — use SNMPv3 in production).

The same two directives are shipped as `snmpd.conf.lab` in this folder:

```
agentaddress udp:127.0.0.1:161
rocommunity public 127.0.0.1
```

Run `./setup.sh` to perform Steps 1–2 in one go, or type the commands above by hand — the script runs exactly them.

---

## Step 3 — Walk system info

```bash
snmpwalk -v2c -c public 127.0.0.1 system
```

You will see OIDs like `sysDescr`, `sysName`, `sysUpTime`.

---

## Step 4 — Get a single OID

```bash
snmpget -v2c -c public 127.0.0.1 sysUpTime.0
```

---

## Step 5 — Walk interface counters

```bash
snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifDescr
snmpwalk -v2c -c public 127.0.0.1 IF-MIB::ifInOctets
```

---

## Step 6 — Record what you poll: the device inventory

Monitoring is only as good as the inventory behind it. `data/device-inventory.csv` is a 20-device asset register for the fictitious `nettech.local` estate — hostname, management IP, device type, rack location, SNMP community, SNMP version and end-of-life date.

```bash
column -s, -t < data/device-inventory.csv | less -S

# Which devices are still on the insecure SNMP v1?
grep ',v1,' data/device-inventory.csv

# Which devices reach end of life in 2026?
grep ',2026-' data/device-inventory.csv
```

Both queries are real operations work: v1/v2c devices need an SNMPv3 migration plan, and EOL devices need a refresh budget.

---

## Step 7 — Clean up

```bash
./cleanup.sh
```

This stops `snmpd` and strips the `rocommunity public 127.0.0.1` line so the next lab starts on a clean box.

---

## Test it

```bash
./verify.sh
```

Expect `ALL CHECKS PASSED` — the agent listens on UDP/161, `snmpget` returns values for `sysDescr.0` and `sysUpTime.0`, and `IF-MIB::ifDescr` lists at least one interface. Work through `checklist.md` as you go.

---

## What you learned
- SNMP versions: v1/v2c (community strings) vs v3 (auth + encryption).
- How `snmpwalk` traverses an OID subtree and `snmpget` fetches a single OID.
- The IF-MIB exposes per-interface counters used by monitoring tools like LibreNMS or Zabbix.
