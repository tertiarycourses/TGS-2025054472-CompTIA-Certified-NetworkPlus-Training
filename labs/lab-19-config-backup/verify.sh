#!/usr/bin/env bash
# Lab 19 — verify /etc is under version control and holds the lab's commits.
set -uo pipefail

fail=0

if command -v git >/dev/null 2>&1; then
  echo "PASS: git is installed"
else
  echo "FAIL: git not found — run apt install -y git (README Step 1)"
  exit 1
fi

if [ -d /etc/.git ]; then
  echo "PASS: /etc is a git repository"
else
  echo "FAIL: /etc/.git not found — run git init in /etc (README Step 2)"
  exit 1
fi

commits=$(git -C /etc log --oneline 2>/dev/null | wc -l | tr -d ' ')
if [ "${commits:-0}" -ge 3 ]; then
  echo "PASS: git log shows $commits commits (baseline, change, revert)"
elif [ "${commits:-0}" -ge 1 ]; then
  echo "FAIL: git log shows only $commits commit(s) — expected 3 after Steps 3, 4 and 6"
  fail=1
else
  echo "FAIL: git log shows no commits (README Step 3)"
  fail=1
fi

if git -C /etc log --oneline 2>/dev/null | grep -q 'baseline: initial network configuration'; then
  echo "PASS: the baseline commit is in the history"
else
  echo "FAIL: no 'baseline: initial network configuration' commit (README Step 3)"
  fail=1
fi

if git -C /etc log --oneline 2>/dev/null | grep -q 'add lab-vm hostname mapping'; then
  echo "PASS: the 'add lab-vm hostname mapping' change commit is in the history"
else
  echo "FAIL: no 'add lab-vm hostname mapping' commit (README Step 4)"
  fail=1
fi

if git -C /etc log --oneline 2>/dev/null | grep -qi 'revert'; then
  echo "PASS: the rollback commit is in the history"
else
  echo "FAIL: no revert commit — run git -C /etc revert HEAD --no-edit (README Step 6)"
  fail=1
fi

if grep -q '127.0.1.2 lab-vm' /etc/hosts 2>/dev/null; then
  echo "FAIL: '127.0.1.2 lab-vm' is still in /etc/hosts — the revert did not take effect (README Step 6)"
  fail=1
else
  echo "PASS: the revert removed '127.0.1.2 lab-vm' from /etc/hosts"
fi

if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED — /etc has a full change history and a working rollback"
else
  echo "One or more checks failed."
fi
exit "$fail"
