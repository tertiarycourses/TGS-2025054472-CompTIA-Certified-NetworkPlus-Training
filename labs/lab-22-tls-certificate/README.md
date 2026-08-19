# Lab 22 — TLS Certificate with OpenSSL and Nginx

You will generate a self-signed X.509 certificate and serve it from nginx, then confirm the TLS handshake from the client side.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `openssl`
- `nginx`
- `curl`

**Files in this lab folder:**

| File | Use |
|---|---|
| `lab-openssl.cnf` | The certificate expressed as a real OpenSSL config (adds the SAN) |
| `nginx-tls.conf` | The Step 3 server block as a real file — `cp` it into place |
| `setup.sh` | Runs Steps 1–3: install, generate the cert, configure nginx |
| `verify.sh` | Pass/fail check — TLS handshake succeeds and the chain validates |
| `cleanup.sh` | **Run before Lab 23** — stops nginx, deletes `lab.crt` / `lab.key` |
| `checklist.md` | Tick-list of everything you should be able to show the trainer |

> No private key is shipped with this lab. `/etc/ssl/private/lab.key` is generated
> on your own machine at Step 2 and deleted again by `cleanup.sh`.

---

## Step 1 — Install the packages

```bash
apt update && apt install -y openssl nginx curl
```

> **Shortcut:** `./setup.sh` performs Steps 1–3 exactly as written below. Read the
> steps first — the script saves typing, not understanding.

---

## Step 2 — Generate a self-signed cert

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout /etc/ssl/private/lab.key \
  -out    /etc/ssl/certs/lab.crt \
  -days 365 \
  -subj "/CN=lab.local"
```

Flag breakdown:
- `-x509` produce a self-signed cert (not a CSR).
- `-newkey rsa:2048` generate a fresh 2048-bit RSA key.
- `-nodes` no DES — do not encrypt the private key (no passphrase).

### The same certificate as a config file

Real PKI work is driven by an OpenSSL config, not a one-liner, because a modern
browser ignores `CN` entirely and matches the hostname against the **Subject
Alternative Name**. `lab-openssl.cnf` in this folder is that config:

```ini
[ req_distinguished_name ]
CN = lab.local
O  = Tertiary Infotech Academy

[ v3_req ]
basicConstraints       = CA:FALSE
keyUsage               = critical, digitalSignature, keyEncipherment
extendedKeyUsage       = serverAuth
subjectAltName         = @alt_names

[ alt_names ]
DNS.1 = lab.local
DNS.2 = localhost
IP.1  = 127.0.0.1
```

Generate the same cert from it with:

```bash
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout /etc/ssl/private/lab.key \
  -out    /etc/ssl/certs/lab.crt \
  -days 365 -config lab-openssl.cnf -extensions v3_req
```

---

## Step 3 — Configure nginx for HTTPS

```bash
cat >/etc/nginx/sites-available/default <<'EOF'
server {
    listen 443 ssl default_server;
    server_name _;
    ssl_certificate     /etc/ssl/certs/lab.crt;
    ssl_certificate_key /etc/ssl/private/lab.key;
    root /var/www/html;
    index index.html;
}
EOF
systemctl restart nginx
```

That server block also ships as `nginx-tls.conf`, so you can install it without
retyping the heredoc:

```bash
cp nginx-tls.conf /etc/nginx/sites-available/default
nginx -t && systemctl restart nginx
```

`nginx -t` validates the syntax before the restart — the nginx equivalent of
`sshd -t` in Lab 23.

---

## Step 4 — Test from the client side

```bash
curl -kv https://localhost 2>&1 | head -30
```

`-k` accepts the self-signed cert. `-v` prints the TLS handshake details: protocol (TLS 1.3), cipher suite, certificate subject.

---

## Step 5 — Inspect the certificate

```bash
openssl x509 -in /etc/ssl/certs/lab.crt -noout -text | head -20
```

You will see Issuer, Subject, validity dates, and the public key.

---

## Step 6 — Test the live handshake with s_client

```bash
echo | openssl s_client -connect localhost:443 -servername lab.local 2>/dev/null | head -20
```

---

## Step 7 — Check your work

```bash
./verify.sh
```

It confirms the cert and key exist, the subject really is `CN=lab.local`, the key
matches the certificate, `curl -k https://localhost` completes a TLS handshake,
and the chain served on 443 validates against `lab.crt` (`Verify return code: 0`).
It also checks that plain `curl` **without** `-k` is still rejected — a
self-signed cert must not be trusted by default.

---

## Step 8 — Clean up

```bash
./cleanup.sh
```

Stops nginx (freeing port 443 for later labs), restores the distribution's
default site, and deletes `/etc/ssl/certs/lab.crt` and `/etc/ssl/private/lab.key`
so no private key is left on the box. Finish by ticking off `checklist.md`.

---

## What you learned
- How to generate a self-signed certificate with `openssl req -x509`.
- How TLS 1.3 differs from TLS 1.2 (fewer round-trips).
- Why production uses a CA-signed cert (Let’s Encrypt, internal PKI) instead of self-signed.
