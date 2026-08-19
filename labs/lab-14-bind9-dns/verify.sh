#!/usr/bin/env bash
# Lab 14 — objective pass/fail check.
# Tolerant on purpose: one failed check must not abort the remaining checks.
set -uo pipefail

fails=0
check() {  # check <description> <command...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    fails=$((fails + 1))
  fi
}

echo "== Lab 14 verification =="

check "bind9 is installed" \
  bash -c "command -v named"
check "dig is installed (dnsutils)" \
  bash -c "command -v dig"
check "/etc/bind/db.lab.local exists" \
  test -f /etc/bind/db.lab.local
check "named.conf.local registers zone lab.local" \
  bash -c "grep -q 'zone \"lab.local\"' /etc/bind/named.conf.local"
check "named-checkconf accepts the configuration" \
  named-checkconf
check "named-checkzone accepts the lab.local zone" \
  named-checkzone lab.local /etc/bind/db.lab.local
check "bind9 service is active" \
  bash -c "systemctl is-active --quiet bind9 || systemctl is-active --quiet named"

# The Test-it check from the README: dig against the local server returns the
# records defined in the zone file.
echo "-- querying 127.0.0.1 --"

if dig +short @127.0.0.1 www.lab.local A 2>/dev/null | grep -q '^10\.0\.0\.10$'; then
  echo "PASS: www.lab.local resolves to 10.0.0.10"
else
  echo "FAIL: www.lab.local did not return 10.0.0.10"
  fails=$((fails + 1))
fi

if dig +short @127.0.0.1 mail.lab.local A 2>/dev/null | grep -q '^10\.0\.0\.20$'; then
  echo "PASS: mail.lab.local resolves to 10.0.0.20"
else
  echo "FAIL: mail.lab.local did not return 10.0.0.20"
  fails=$((fails + 1))
fi

if dig +short @127.0.0.1 lab.local MX 2>/dev/null | grep -q '10 mail.lab.local.'; then
  echo "PASS: lab.local MX returns '10 mail.lab.local.'"
else
  echo "FAIL: lab.local MX record not returned"
  fails=$((fails + 1))
fi

if dig @127.0.0.1 lab.local SOA 2>/dev/null | grep -q 'flags:.* aa'; then
  echo "PASS: the answer is authoritative (aa flag set)"
else
  echo "FAIL: no 'aa' flag — this server is not authoritative for lab.local"
  fails=$((fails + 1))
fi

# Optional Step 7 bonus: only checked if the reverse zone was installed.
if grep -q 'zone "0.0.10.in-addr.arpa"' /etc/bind/named.conf.local 2>/dev/null; then
  echo "-- optional reverse zone detected --"
  if dig +short @127.0.0.1 -x 10.0.0.10 2>/dev/null | grep -q 'www.lab.local.'; then
    echo "PASS: reverse lookup of 10.0.0.10 returns www.lab.local."
  else
    echo "FAIL: reverse lookup of 10.0.0.10 did not return www.lab.local."
    fails=$((fails + 1))
  fi
else
  echo "-- reverse zone not installed (optional Step 7 bonus) — skipped --"
fi

echo
if [ "$fails" -eq 0 ]; then
  echo "PASS: Lab 14 complete — BIND9 answers authoritatively for lab.local."
  exit 0
fi
echo "FAIL: $fails check(s) failed."
exit 1
