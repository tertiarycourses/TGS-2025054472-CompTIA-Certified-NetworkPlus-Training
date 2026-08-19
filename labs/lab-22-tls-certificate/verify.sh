#!/usr/bin/env bash
# Lab 22 — verify the certificate and the live TLS handshake (README Steps 4-6).
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

CRT=/etc/ssl/certs/lab.crt
KEY=/etc/ssl/private/lab.key
fail=0

# --- 1. certificate and key exist -------------------------------------------
if [ -s "$CRT" ]; then
  echo "PASS: $CRT exists"
else
  echo "FAIL: $CRT missing — re-run README Step 2 (openssl req -x509 ...)"
  fail=1
fi

if [ -s "$KEY" ]; then
  echo "PASS: $KEY exists"
else
  echo "FAIL: $KEY missing — re-run README Step 2"
  fail=1
fi

# --- 2. the subject is CN=lab.local ------------------------------------------
if [ -s "$CRT" ]; then
  subj="$(openssl x509 -in "$CRT" -noout -subject 2>/dev/null)"
  if printf '%s' "$subj" | grep -q "CN *= *lab.local"; then
    echo "PASS: certificate subject is CN=lab.local  ($subj)"
  else
    echo "FAIL: unexpected subject — got: $subj"
    fail=1
  fi

  # --- 3. certificate is currently valid -------------------------------------
  if openssl x509 -in "$CRT" -noout -checkend 0 >/dev/null 2>&1; then
    echo "PASS: certificate is within its validity window ($(openssl x509 -in "$CRT" -noout -enddate))"
  else
    echo "FAIL: certificate has expired — regenerate it with -days 365"
    fail=1
  fi

  # --- 4. the key matches the certificate ------------------------------------
  if [ -s "$KEY" ]; then
    cmod="$(openssl x509 -in "$CRT" -noout -modulus 2>/dev/null | openssl md5)"
    kmod="$(openssl rsa  -in "$KEY" -noout -modulus 2>/dev/null | openssl md5)"
    if [ -n "$cmod" ] && [ "$cmod" = "$kmod" ]; then
      echo "PASS: private key matches the certificate"
    else
      echo "FAIL: key/certificate mismatch — nginx will refuse to start"
      fail=1
    fi
  fi
fi

# --- 5. nginx is serving TLS on 443 ------------------------------------------
if curl -ks --max-time 10 https://localhost -o /dev/null; then
  echo "PASS: curl completed a TLS handshake with https://localhost"
else
  echo "FAIL: https://localhost did not respond — check 'systemctl status nginx' and README Step 3"
  fail=1
fi

# --- 6. the served chain validates against our own certificate ---------------
if [ -s "$CRT" ]; then
  if echo | openssl s_client -connect localhost:443 -servername lab.local \
       -CAfile "$CRT" 2>/dev/null | grep -q "Verify return code: 0 (ok)"; then
    echo "PASS: served chain validates against $CRT (Verify return code: 0)"
  else
    echo "FAIL: the chain served on 443 does not validate against $CRT"
    fail=1
  fi
fi

# --- 7. a bare curl (no -k) must fail — that is the point of self-signed -----
if curl -s --max-time 10 https://localhost -o /dev/null 2>/dev/null; then
  echo "FAIL: curl without -k succeeded — the cert should NOT be trusted by default"
  fail=1
else
  echo "PASS: curl without -k is rejected (self-signed cert is untrusted, as expected)"
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — run ./cleanup.sh before moving on to Lab 23."
else
  echo "One or more checks failed."
fi
exit "$fail"
