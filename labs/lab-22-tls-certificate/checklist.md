# Lab 22 checklist — TLS Certificate with OpenSSL and Nginx

Tick each item as you complete it.

- [ ] Installed the packages with `apt update && apt install -y openssl nginx curl`
- [ ] Generated the self-signed cert to `/etc/ssl/certs/lab.crt` and key to `/etc/ssl/private/lab.key`
- [ ] Can explain `-x509`, `-newkey rsa:2048` and `-nodes` in your own words
- [ ] Read `lab-openssl.cnf` and understand why a Subject Alternative Name is needed as well as `CN=lab.local`
- [ ] Installed `nginx-tls.conf` to `/etc/nginx/sites-available/default` and restarted nginx
- [ ] Ran `curl -kv https://localhost` and identified the TLS version and cipher suite in the output
- [ ] Explained why `-k` is required here and what would happen in production without it
- [ ] Inspected the cert with `openssl x509 -in /etc/ssl/certs/lab.crt -noout -text` and found Issuer, Subject and validity dates
- [ ] Saw Issuer == Subject and can say why that means "self-signed"
- [ ] Ran the live handshake with `openssl s_client -connect localhost:443 -servername lab.local`
- [ ] Ran `./cleanup.sh` — nginx stopped, `lab.crt` and `lab.key` deleted, default site restored
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — the cert exists with `CN=lab.local`, the key matches it, `curl -k https://localhost` completes the TLS handshake, and the served chain validates against `lab.crt` (`Verify return code: 0 (ok)`)
