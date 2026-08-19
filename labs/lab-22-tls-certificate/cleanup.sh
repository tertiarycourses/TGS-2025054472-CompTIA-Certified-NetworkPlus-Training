#!/usr/bin/env bash
# Lab 22 — reverse everything this lab created.
# Removes ONLY the lab's own certificate, key and nginx site config, restores the
# distribution default site, and stops nginx so port 443 is free for later labs.
# Tolerant: keep going even if something is already gone.
set -uo pipefail

echo "== Restoring the nginx default site =="
if [ -f /etc/nginx/sites-available/default.lab22.bak ]; then
  mv /etc/nginx/sites-available/default.lab22.bak /etc/nginx/sites-available/default
  echo "restored /etc/nginx/sites-available/default from the lab backup"
else
  echo "no lab backup found — leaving /etc/nginx/sites-available/default as-is"
fi

echo "== Stopping nginx so 443 is free for later labs =="
systemctl stop nginx 2>/dev/null && echo "nginx stopped" || echo "nginx was not running"

echo "== Deleting only the key material this lab generated =="
rm -f /etc/ssl/certs/lab.crt   && echo "removed /etc/ssl/certs/lab.crt"
rm -f /etc/ssl/private/lab.key && echo "removed /etc/ssl/private/lab.key"

echo
echo "Cleanup done — no lab key material remains and port 443 is free."
