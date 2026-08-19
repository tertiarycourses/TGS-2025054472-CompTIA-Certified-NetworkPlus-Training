# Lab 14 — Authoritative DNS with BIND9

You will run your own DNS server hosting the zone `lab.local` and query it with `dig`.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `bind9`
- `dnsutils` (for `dig`)

**Files shipped with this lab**

| File | Use |
|------|-----|
| `db.lab.local` | The real forward zone file — copied to `/etc/bind/` in Step 2 |
| `named.conf.local` | The zone registration block — appended in Step 3 |
| `db.10.0.0` | *Optional* reverse zone for 10.0.0.0/24 (Step 7 bonus) |
| `named.conf.local.reverse` | *Optional* reverse-zone registration block (Step 7 bonus) |
| `setup.sh` | Runs Steps 1–4; add `--reverse` to include the bonus zone |
| `verify.sh` | Objective `PASS`/`FAIL` check — digs every record against 127.0.0.1 |
| `cleanup.sh` | Reverses Step 6 and restores the packaged `named.conf.local` |
| `checklist.md` | Tick-box list of everything you must be able to show |

---

## Step 1 — Install BIND9

```bash
apt update && apt install -y bind9 dnsutils
```

---

## Step 2 — Create the zone file

The zone is shipped with this lab as `db.lab.local`. Read it before you install
it — every line is examinable:

```
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
```

| Line | Meaning |
|------|---------|
| `$TTL 86400` | Default time-to-live for records with no explicit TTL |
| `SOA` | Start of Authority — names the primary NS and the admin mailbox (`admin.lab.local.` = admin@lab.local) |
| `2026051001 ; serial` | Version number. **Bump it on every edit** or slaves never notice |
| `3600 / 1800 / 604800 / 86400` | refresh / retry / expire / negative-cache TTL, in seconds |
| `NS` | Delegates the zone to `ns.lab.local.` |
| `A` | Name → address (`www` → 10.0.0.10, `mail` → 10.0.0.20) |
| `MX 10` | Mail exchanger with preference 10 — lower preference wins |

The trailing dots matter: `mail.lab.local.` is absolute; `mail.lab.local`
without the dot would expand to `mail.lab.local.lab.local.`

Copy the provided file into place instead of retyping it:

```bash
cp db.lab.local /etc/bind/db.lab.local
```

---

## Step 3 — Register the zone

BIND only serves a zone it has been told about. The registration block ships as
`named.conf.local`:

```
zone "lab.local" {
    type master;
    file "/etc/bind/db.lab.local";
};
```

`type master` means this server holds the authoritative copy (BIND 9.16+ also
accepts the synonym `type primary`). Append the provided block:

```bash
cat named.conf.local >> /etc/bind/named.conf.local
```

---

## Step 4 — Validate and reload

```bash
named-checkconf
named-checkzone lab.local /etc/bind/db.lab.local
systemctl restart bind9
```

`named-checkconf` validates `named.conf*` — silence means success.
`named-checkzone` parses the zone file and confirms the syntax is valid; it
prints `OK` on the last line.

---

## Step 5 — Query your own server

```bash
dig @127.0.0.1 www.lab.local
dig @127.0.0.1 MX lab.local
```

The `@127.0.0.1` forces dig to use your local BIND instance. Look for the `aa`
flag in the header — that is what proves the answer is **authoritative** rather
than cached.

`verify.sh` runs all of these queries and asserts each answer:

```bash
./verify.sh
```

---

## Step 6 — Clean up

```bash
systemctl stop bind9
```

Or run the provided script, which also restores the `named.conf.local` the
package shipped and removes the zone files this lab installed:

```bash
./cleanup.sh
```

Finally, work through `checklist.md` and tick off each outcome.

---

## Step 7 (optional) — Add the reverse zone

Forward DNS maps a name to an address. **Reverse DNS** maps an address back to
a name using `PTR` records in the `in-addr.arpa` tree, with the octets
reversed. Since both A records in this zone live in 10.0.0.0/24, the matching
reverse zone is `0.0.10.in-addr.arpa`. Two extra files ship for this:

```
; db.10.0.0
10      IN  PTR   www.lab.local.
20      IN  PTR   mail.lab.local.
```

```
// named.conf.local.reverse
zone "0.0.10.in-addr.arpa" {
    type master;
    file "/etc/bind/db.10.0.0";
};
```

```bash
cp db.10.0.0 /etc/bind/db.10.0.0
cat named.conf.local.reverse >> /etc/bind/named.conf.local
named-checkzone 0.0.10.in-addr.arpa /etc/bind/db.10.0.0
systemctl restart bind9
dig @127.0.0.1 -x 10.0.0.10
```

The `-x` flag tells dig to do a reverse lookup — it should answer
`www.lab.local.`

---

## Shortcut

To rebuild quickly after a playground reset, `./setup.sh` runs Steps 1–4
exactly as written above; `./setup.sh --reverse` also installs the Step 7 zone.
Do the steps by hand the first time — reading the zone file is the point.

---

## What you learned
- The structure of a SOA record (serial, refresh, retry, expire, minimum TTL).
- How to register a zone with BIND9.
- How to validate zone syntax before reloading the daemon.
