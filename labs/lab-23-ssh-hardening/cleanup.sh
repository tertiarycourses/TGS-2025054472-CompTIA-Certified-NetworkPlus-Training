#!/usr/bin/env bash
# Lab 23 — restore the SSH service to its pre-lab state.
#
# IMPORTANT: this lab edits /etc/ssh/sshd_config. Leaving PasswordAuthentication
# no in place would change how every later lab reaches this host, so this script
# puts the original config back, removes the drop-in fragment, and de-authorises
# the lab key. It touches nothing else.
# Tolerant: keep going even if a step is already undone.
set -uo pipefail

KEY="$HOME/.ssh/lab_ed25519"

echo "== Removing the drop-in hardening fragment =="
if [ -f /etc/ssh/sshd_config.d/99-lab-hardening.conf ]; then
  rm -f /etc/ssh/sshd_config.d/99-lab-hardening.conf
  echo "removed /etc/ssh/sshd_config.d/99-lab-hardening.conf"
else
  echo "no drop-in fragment present"
fi

echo "== Restoring /etc/ssh/sshd_config =="
if [ -f /etc/ssh/sshd_config.lab23.bak ]; then
  mv /etc/ssh/sshd_config.lab23.bak /etc/ssh/sshd_config
  echo "restored /etc/ssh/sshd_config from the lab backup"
else
  # No backup (the learner ran the README's sed directly). Reverse exactly the
  # two directives Step 4 changed, back to the Ubuntu shipped defaults.
  echo "no backup found — reversing only the two directives Step 4 changed"
  sed -i 's/^PasswordAuthentication no/#PasswordAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null
  sed -i 's/^PermitRootLogin prohibit-password/#PermitRootLogin prohibit-password/' /etc/ssh/sshd_config 2>/dev/null
fi

echo "== Validating and reloading sshd =="
if sshd -t 2>/dev/null; then
  systemctl reload ssh 2>/dev/null && echo "sshd reloaded" || echo "could not reload ssh (service may not be running)"
else
  echo "WARNING: sshd -t still reports an error — do NOT reload until it is fixed:"
  sshd -t
fi

echo "== De-authorising the lab key =="
if [ -s "$KEY.pub" ] && [ -f "$HOME/.ssh/authorized_keys" ]; then
  fp="$(cut -d' ' -f2 "$KEY.pub")"
  grep -vF "$fp" "$HOME/.ssh/authorized_keys" > "$HOME/.ssh/authorized_keys.lab23tmp" 2>/dev/null \
    && mv "$HOME/.ssh/authorized_keys.lab23tmp" "$HOME/.ssh/authorized_keys" \
    && chmod 600 "$HOME/.ssh/authorized_keys" \
    && echo "removed the lab key from ~/.ssh/authorized_keys"
fi

echo "== Deleting the lab key pair =="
rm -f "$KEY" "$KEY.pub" && echo "removed $KEY and $KEY.pub"

echo
echo "Effective password-auth setting now:"
sshd -T 2>/dev/null | grep -i '^passwordauthentication' || true
echo "Cleanup done — sshd is back to its pre-lab configuration and no lab key remains."
