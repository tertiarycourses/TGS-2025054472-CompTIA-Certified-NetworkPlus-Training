# Lab 14 — Authoritative DNS with BIND9

You will run your own DNS server hosting the zone `lab.local` and query it with `dig`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `bind9`
- `dnsutils` (for `dig`)

---

## Step 1 — Install BIND9

```bash
apt update && apt install -y bind9 dnsutils
```

---

## Step 2 — Create the zone file

```bash
cat >/etc/bind/db.lab.local <<'EOF'
$TTL 86400
@   IN  SOA ns.lab.local. admin.lab.local. (
            2026051001 ; serial
            3600       ; refresh
            1800       ; retry
            604800     ; expire
            86400 )    ; minimum
@       IN  NS    ns.lab.local.
ns      IN  A     127.0.0.1
www     IN  A     10.0.0.10
mail    IN  A     10.0.0.20
@       IN  MX 10 mail.lab.local.
EOF
```

---

## Step 3 — Register the zone

```bash
cat >>/etc/bind/named.conf.local <<'EOF'
zone "lab.local" {
    type master;
    file "/etc/bind/db.lab.local";
};
EOF
```

---

## Step 4 — Validate and reload

```bash
named-checkzone lab.local /etc/bind/db.lab.local
systemctl restart bind9
```

`named-checkzone` parses the file and confirms the syntax is valid.

---

## Step 5 — Query your own server

```bash
dig @127.0.0.1 www.lab.local
dig @127.0.0.1 MX lab.local
```

The `@127.0.0.1` forces dig to use your local BIND instance.

---

## Step 6 — Clean up

```bash
systemctl stop bind9
```

---

## What you learned
- The structure of a SOA record (serial, refresh, retry, expire, minimum TTL).
- How to register a zone with BIND9.
- How to validate zone syntax before reloading the daemon.
