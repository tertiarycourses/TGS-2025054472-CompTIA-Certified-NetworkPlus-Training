# Lab asset spec — what ships inside each `labs/lab-NN-slug/` folder

Every lab is a folder. `README.md` is the lab itself; the files below make it
runnable and checkable instead of something the learner retypes by hand.

**Golden rule: add a file only when it earns its place.** A 5-command lab needs
no script. Never add a file the README does not reference.

## File types

| File | When to add it | Notes |
|---|---|---|
| `setup.sh` | the lab needs >3 commands of environment prep (namespaces, dummy interfaces, package installs) | idempotent; safe to re-run |
| `run.sh` | the lab has a long or error-prone command sequence (>12 commands) | echoes each phase; does NOT hide the teaching — the README still shows every command |
| `verify.sh` | the lab has an objective pass/fail check | prints `PASS:` / `FAIL:` lines and exits non-zero on failure |
| `cleanup.sh` | the lab changes routing, firewall, DHCP or interface state | must restore the box so the next lab starts clean |
| `*.conf` / `*.zone` / `*.yaml` | the lab writes a real service config | the actual file, not a snippet — the README says `cp dhcpd.conf /etc/dhcp/` |
| `checklist.md` | every lab | short "did I do it" list the learner ticks; also the trainer's observation aid |
| `data/*.csv` | the lab benefits from realistic sample data (subnet plans, IPAM records, log samples, port inventories) | header row + realistic rows; referenced from a README step |
| `answers.md` | labs with a worked calculation (subnetting, VLSM) | expected values so the learner can self-check |

## Hard rules

1. **Every script starts with** `#!/usr/bin/env bash` and `set -euo pipefail`
   (except deliberately tolerant verify/cleanup scripts, which use `set -uo pipefail`
   so one failed check does not abort the rest).
2. **Every script is executable** (`chmod +x`).
3. **Commands must match the README exactly** — same flags, same addresses, same
   interface names. A script that drifts from the README is worse than no script.
4. **No `rm -rf` on anything outside the lab's own scratch dir.** Cleanup reverses
   what the lab created (ip link del, iptables -D, systemctl stop) — nothing else.
5. **Scripts are for the Killercoda Ubuntu playground** (root shell, apt available).
   Lab 11 (wireless) runs on the learner's own laptop — give it no Linux scripts.
6. **The README must reference every file it ships**, in the step where it is used,
   e.g. "Run `./setup.sh` (or follow steps 2–4 by hand)".
7. **No `.bat` files** — every lab runs on Linux. Windows learners use the browser
   playground, so a `.bat` would never execute.
8. `checklist.md` uses GitHub task-list syntax (`- [ ] …`) so it renders as tick
   boxes, one line per verifiable outcome, ending with the lab's Test-it check.

## CSV mock-data conventions

Realistic but obviously fictitious: RFC1918 addresses, `example.com` / `nettech.local`
domains, and no real hostnames, MACs or public IPs of real organisations. Give every
CSV a header row and 8–25 rows — enough to be useful in a calculation or a grep,
small enough to read on screen.
