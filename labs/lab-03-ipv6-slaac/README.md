# Lab 3 — IPv6 Addressing and Link-Local

IPv6 is on the N10-009 exam blueprint. In this lab you will use the **TIS IP Calculator** to break down an IPv6 prefix, then add a global IPv6 address to your interface, observe the auto-generated link-local address, and ping across both. Every IPv6-capable interface gets a link-local address (`fe80::/10`) automatically — you do not configure it manually.

**Subnet calculator (open in a browser tab):**
👉 https://alfredang.github.io/ipcalculator/

Run the Linux commands on https://killercoda.com/playgrounds/scenario/ubuntu

**Files in this lab folder**

| File | Use |
|---|---|
| `answers.md` | worked address-shortening examples and the full EUI-64 derivation |
| `verify.sh` | checks the link-local and global addresses are present and pingable |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

Shorten the addresses by hand before opening `answers.md`.

---

## Step 1 — Plan the IPv6 prefix in the calculator

Open https://alfredang.github.io/ipcalculator/ in a browser tab and switch to the **IPv6** mode.

Enter:

```
IPv6 / Prefix:  2001:db8::/64
```

Read off:
- **Network (prefix)** — `2001:db8::/64`
- **First host** — `2001:db8::1`
- **Last host** — `2001:db8::ffff:ffff:ffff:ffff`
- **Total addresses** — 2⁶⁴ ≈ 1.8 × 10¹⁹

The `2001:db8::/32` range is reserved for documentation and examples so it is always safe to use in labs.

Now try splitting `2001:db8::/48` into `/64` subnets — the calculator shows that you get 2¹⁶ = **65 536** /64 subnets. That is the standard "site allocation" pattern for IPv6.

---

## Step 2 — Inspect the existing IPv6 configuration

In the Killercoda terminal:

```bash
ip -6 addr show eth0
```

You will see at least one address that begins with `fe80::`. That is the **link-local** address. It is valid only on the local link and is generated from the interface MAC (modified EUI-64) or a random token.

Notice the address is written in shortened form. Part A and B of `answers.md` work
through the two shortening rules on six examples — including the trap where `::` cannot
be used because there are two separate runs of zeros.

Part D of `answers.md` walks the modified EUI-64 derivation end to end: split the MAC,
insert `ff:fe`, flip the Universal/Local bit, prepend `fe80::`. Try it on the MAC from
`ip link show eth0` before reading the answer.

> If your `fe80::` address has no `ff:fe` in the middle, the kernel generated a
> stable-privacy identifier (RFC 7217) instead of an EUI-64 one. That is normal on
> modern Linux and not a fault.

---

## Step 3 — Add a documentation-range global address

```bash
ip -6 addr add 2001:db8::10/64 dev eth0
```

`/64` is the standard IPv6 subnet size — every LAN should be a /64 so that SLAAC can work.

---

## Step 4 — Verify the new address

```bash
ip -6 addr show eth0
```

You should now see two entries: the original `fe80::...` and the new `2001:db8::10/64`.

Confirm with the IP Calculator that `2001:db8::10` is inside the `2001:db8::/64` host range you computed in Step 1.

---

## Step 5 — Ping the link-local address

Link-local pings need a zone identifier so the kernel knows which interface to send out of.

```bash
ping6 -c2 ff02::1%eth0
```

`ff02::1` is the **all-nodes multicast** address — every IPv6 host on the link will reply.

---

## Step 6 — Ping the global address from itself

```bash
ping6 -c2 2001:db8::10
```

This should succeed because the address is now bound to your interface.

Confirm everything at once — **run this before the Step 7 cleanup**:

```bash
./verify.sh
```

It prints a `PASS:`/`FAIL:` line for the link-local address, the global address, and the
ping, and exits non-zero if any check fails.

---

## Step 7 — Clean up

```bash
ip -6 addr del 2001:db8::10/64 dev eth0
```

Finally, work through `checklist.md` and tick off each outcome.

---

## What you learned
- How to plan IPv6 prefixes with the **TIS IP Calculator** at https://alfredang.github.io/ipcalculator/
- The difference between link-local (`fe80::/10`) and global IPv6 addresses.
- Why every IPv6 LAN uses a /64.
- How to use the `%eth0` zone suffix when pinging link-local addresses.
