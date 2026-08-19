# Lab 3 — Answers

Self-check only. Work each address out by hand first, confirm in the
**TIS IP Calculator** (https://alfredang.github.io/ipcalculator/), then compare here.

---

## Part A — The two shortening rules

1. **Drop leading zeros** in each 16-bit group: `0db8` → `db8`, `0000` → `0`.
2. **Replace one run of all-zero groups with `::`** — and only one, otherwise the
   address is ambiguous. When there are two equal-length runs, compress the **leftmost**.

---

## Part B — Worked shortening examples

| # | Full (expanded) form | Shortened form | What was applied |
|---|---|---|---|
| 1 | `2001:0db8:0000:0000:0000:0000:0000:0010` | `2001:db8::10` | leading zeros dropped, five zero groups → `::` |
| 2 | `fe80:0000:0000:0000:0216:3eff:fe4a:7b2c` | `fe80::216:3eff:fe4a:7b2c` | three zero groups → `::`, `0216` → `216` |
| 3 | `2001:0db8:85a3:0000:0000:8a2e:0370:7334` | `2001:db8:85a3::8a2e:370:7334` | middle run of two zero groups → `::` |
| 4 | `0000:0000:0000:0000:0000:0000:0000:0001` | `::1` | the loopback — every group but the last is zero |
| 5 | `ff02:0000:0000:0000:0000:0000:0000:0001` | `ff02::1` | the all-nodes multicast address from Step 5 |
| 6 | `2001:0db8:0000:0042:0000:8a2e:0370:7334` | `2001:db8:0:42:0:8a2e:370:7334` | **two separate** single-zero runs — `::` would be ambiguous, so neither is compressed |

Row 6 is the exam trap: `::` may appear **at most once**. Writing
`2001:db8::42:0:8a2e:370:7334` loses the information about how many groups were collapsed.

### Expanding back out

Going the other way, count the groups you can see and let `::` supply the rest:

`2001:db8::10` has 3 visible groups (`2001`, `db8`, `10`), so `::` stands for
8 − 3 = **5** zero groups → `2001:0db8:0000:0000:0000:0000:0000:0010`.

---

## Part C — The `2001:db8::/64` prefix (README Step 1)

| Field | Value |
|---|---|
| Network (prefix) | `2001:db8::/64` |
| First host | `2001:db8::1` |
| Last host | `2001:db8::ffff:ffff:ffff:ffff` |
| Total addresses | 2⁶⁴ = 18 446 744 073 709 551 616 (≈ 1.8 × 10¹⁹) |

Splitting `2001:db8::/48` into `/64`s borrows 64 − 48 = 16 bits, giving
2¹⁶ = **65 536** subnets — the standard IPv6 site allocation.

The Step 3 address `2001:db8::10/64` sits between the first and last host above,
so it is a valid host address inside this prefix.

---

## Part D — EUI-64 derivation (README Step 2)

A link-local address is `fe80::/10` plus a 64-bit **interface identifier**. When that
identifier is derived from the MAC (rather than randomised for privacy), the process is
modified EUI-64:

Starting MAC: `00:16:3e:4a:7b:2c`

**Step 1 — split the 48-bit MAC in half**

```
00:16:3e   |   4a:7b:2c
  OUI          device ID
```

**Step 2 — insert `ff:fe` between the halves** (48 bits → 64 bits)

```
00:16:3e:ff:fe:4a:7b:2c
```

**Step 3 — flip the 7th bit of the first byte** (the Universal/Local bit)

```
first byte 00 = 0000 0000
flip bit 7   → 0000 0010 = 02
```

So `00` becomes `02`:

```
02:16:3e:ff:fe:4a:7b:2c
```

**Step 4 — regroup into four 16-bit hextets and prepend the link-local prefix**

```
0216:3eff:fe4a:7b2c
fe80:0000:0000:0000:0216:3eff:fe4a:7b2c
```

**Step 5 — shorten**

```
fe80::216:3eff:fe4a:7b2c
```

### How to spot an EUI-64 address at a glance

Look for **`ff:fe` in the middle** of the interface identifier — `...3eff:fe4a...`.
That is the giveaway. Then flip bit 7 of the first byte back (`02` → `00`) and delete
the `fffe` to recover the original MAC.

### Two more to check yourself against

| MAC | Modified EUI-64 link-local |
|---|---|
| `00:16:3e:4a:7b:2c` | `fe80::216:3eff:fe4a:7b2c` |
| `52:54:00:12:34:56` | `fe80::5054:ff:fe12:3456` |
| `aa:bb:cc:dd:ee:ff` | `fe80::a8bb:ccff:fedd:eeff` |

Note the second row: `52` = `0101 0010`, bit 7 is already 1, so flipping it gives
`0101 0000` = `50`. The flip goes **both ways**.

Modern Linux often uses RFC 7217 stable-privacy addresses instead, so the `fe80::`
address you see in Step 2 may look random with no `ff:fe` — that is expected and not
a fault.

---

## Part E — Expected command output

**Step 4** — after `ip -6 addr add 2001:db8::10/64 dev eth0`, the command
`ip -6 addr show eth0` prints two `inet6` lines:

```
inet6 2001:db8::10/64 scope global
inet6 fe80::.../64 scope link
```

**Step 5** — `ping6 -c2 ff02::1%eth0` returns at least one reply from the host's own
link-local address (marked `DUP!` if several nodes answer).

**Step 6** — `ping6 -c2 2001:db8::10` reports `2 packets transmitted, 2 received, 0% packet loss`.

**Step 7** — after `ip -6 addr del 2001:db8::10/64 dev eth0`, only the `scope link`
`fe80::` line remains.
