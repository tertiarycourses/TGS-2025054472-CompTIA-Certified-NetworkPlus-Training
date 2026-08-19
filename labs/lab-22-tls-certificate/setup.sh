#!/usr/bin/env bash
# Lab 22 — TLS Certificate with OpenSSL and Nginx
# Performs README Steps 1-3: install packages, generate the self-signed
# certificate for CN=lab.local, and serve it from nginx on 443.
# Idempotent: safe to re-run (the cert and site config are overwritten).
#
# NO key material ships with this lab. /etc/ssl/private/lab.key is generated
# here, at run time, and is deleted again by ./cleanup.sh.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "== Step 1: install openssl, nginx and curl =="
apt update && apt install -y openssl nginx curl

echo "== Step 3 prep: back up the existing nginx default site =="
if [ -f /etc/nginx/sites-available/default ] && [ ! -f /etc/nginx/sites-available/default.lab22.bak ]; then
  cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.lab22.bak
  echo "backed up to /etc/nginx/sites-available/default.lab22.bak"
fi

echo "== Step 2: generate the self-signed cert for CN=lab.local =="
mkdir -p /etc/ssl/private /etc/ssl/certs
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout /etc/ssl/private/lab.key \
  -out    /etc/ssl/certs/lab.crt \
  -days 365 \
  -config "$HERE/lab-openssl.cnf" -extensions v3_req
chmod 600 /etc/ssl/private/lab.key

echo "== Step 3: install the nginx TLS site config and restart =="
cp "$HERE/nginx-tls.conf" /etc/nginx/sites-available/default
nginx -t
systemctl restart nginx

echo
echo "Serving HTTPS on 443 with CN=lab.local. Now run ./verify.sh"
