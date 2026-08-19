# Lab 22 — TLS Certificate with OpenSSL and Nginx

You will generate a self-signed X.509 certificate and serve it from nginx, then confirm the TLS handshake from the client side.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, installed via apt):**
- `openssl`
- `nginx`
- `curl`

---

## Step 1 — Install the packages

```bash
apt update && apt install -y openssl nginx curl
```

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

## What you learned
- How to generate a self-signed certificate with `openssl req -x509`.
- How TLS 1.3 differs from TLS 1.2 (fewer round-trips).
- Why production uses a CA-signed cert (Let’s Encrypt, internal PKI) instead of self-signed.
