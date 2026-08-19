#!/usr/bin/env bash
# Lab 23 — verify key auth works and password auth is refused (README Steps 3-5).
# Tolerant: one failed check must not abort the rest.
set -uo pipefail

KEY="$HOME/.ssh/lab_ed25519"
fail=0

# --- 1. the Ed25519 key pair exists ------------------------------------------
if [ -s "$KEY" ] && [ -s "$KEY.pub" ]; then
  echo "PASS: key pair $KEY / $KEY.pub exists"
else
  echo "FAIL: key pair missing — re-run README Step 1 (ssh-keygen -t ed25519 -N '' -f ~/.ssh/lab_ed25519)"
  fail=1
fi

# --- 2. the public key is authorised -----------------------------------------
if [ -s "$KEY.pub" ] && [ -f "$HOME/.ssh/authorized_keys" ] \
   && grep -qFf <(cut -d' ' -f2 "$KEY.pub") "$HOME/.ssh/authorized_keys" 2>/dev/null; then
  echo "PASS: the lab public key is present in ~/.ssh/authorized_keys"
else
  echo "FAIL: public key not authorised — re-run README Step 2"
  fail=1
fi

# --- 3. file permissions sshd will actually accept ---------------------------
if [ "$(stat -c %a "$HOME/.ssh" 2>/dev/null)" = "700" ]; then
  echo "PASS: ~/.ssh is mode 700"
else
  echo "FAIL: ~/.ssh must be mode 700 — sshd ignores a loose directory (chmod 700 ~/.ssh)"
  fail=1
fi
if [ "$(stat -c %a "$HOME/.ssh/authorized_keys" 2>/dev/null)" = "600" ]; then
  echo "PASS: ~/.ssh/authorized_keys is mode 600"
else
  echo "FAIL: ~/.ssh/authorized_keys must be mode 600 (chmod 600 ~/.ssh/authorized_keys)"
  fail=1
fi

# --- 4. the sshd configuration is syntactically valid ------------------------
if sshd -t 2>/dev/null; then
  echo "PASS: sshd -t reports a valid configuration"
else
  echo "FAIL: sshd -t rejects the configuration — fix it BEFORE reloading, or you lock yourself out"
  sshd -t
  fail=1
fi

# --- 5. the effective config disables password auth --------------------------
eff="$(sshd -T 2>/dev/null)"
if printf '%s' "$eff" | grep -qi '^passwordauthentication no'; then
  echo "PASS: effective config has PasswordAuthentication no"
else
  echo "FAIL: PasswordAuthentication is still enabled — re-run README Step 4"
  fail=1
fi
if printf '%s' "$eff" | grep -qi '^permitrootlogin prohibit-password'; then
  echo "PASS: effective config has PermitRootLogin prohibit-password"
else
  echo "FAIL: PermitRootLogin is not prohibit-password — re-run README Step 4"
  fail=1
fi

# --- 6. key login actually works (README Step 3) -----------------------------
if [ -s "$KEY" ]; then
  who="$(ssh -i "$KEY" -o StrictHostKeyChecking=no -o BatchMode=yes \
          -o ConnectTimeout=10 root@localhost whoami 2>/dev/null)"
  if [ "$who" = "root" ]; then
    echo "PASS: key authentication succeeds (ssh -i $KEY root@localhost whoami -> root)"
  else
    echo "FAIL: key login did not return 'root' — check sshd is running and Step 2 was done"
    fail=1
  fi
fi

# --- 7. password login is refused (README Step 5) ----------------------------
out="$(ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no \
        -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=10 \
        root@localhost whoami 2>&1)"
if printf '%s' "$out" | grep -q "Permission denied"; then
  echo "PASS: password authentication is refused (Permission denied (publickey))"
else
  echo "FAIL: password authentication was not refused — got: $out"
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — run ./cleanup.sh to restore the original sshd_config."
else
  echo "One or more checks failed."
fi
exit "$fail"
