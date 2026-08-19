# Lab 15 — SNMP Monitoring

SNMP (Simple Network Management Protocol) lets a manager poll devices for system metrics. In this lab you will install an SNMP agent, configure a community string, and walk the MIB.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `snmpd` (agent)
- `snmp` (client tools: `snmpwalk`, `snmpget`)
- `snmp-mibs-downloader` (optional, for friendly OID names)

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

## What you learned
- SNMP versions: v1/v2c (community strings) vs v3 (auth + encryption).
- How `snmpwalk` traverses an OID subtree and `snmpget` fetches a single OID.
- The IF-MIB exposes per-interface counters used by monitoring tools like LibreNMS or Zabbix.
