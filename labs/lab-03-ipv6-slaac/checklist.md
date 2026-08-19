# Lab 3 checklist — IPv6 Addressing and Link-Local

Tick each item as you complete it.

- [ ] Opened the TIS IP Calculator at https://alfredang.github.io/ipcalculator/ and switched to IPv6 mode
- [ ] Entered `2001:db8::/64` and read off the prefix, first host, last host and total addresses
- [ ] Split `2001:db8::/48` into `/64`s and confirmed the result is 65 536 subnets
- [ ] Shortened all six worked examples in `answers.md` by hand before checking them
- [ ] Explained why `::` may appear only once in an address (example 6)
- [ ] Ran `ip -6 addr show eth0` and found the automatic `fe80::` link-local address
- [ ] Derived a modified EUI-64 interface identifier from a MAC by hand (split, insert `ff:fe`, flip bit 7)
- [ ] Added the global address with `ip -6 addr add 2001:db8::10/64 dev eth0`
- [ ] Confirmed `2001:db8::10` falls inside the `2001:db8::/64` host range from Step 1
- [ ] Pinged all-nodes multicast with `ping6 -c2 ff02::1%eth0` and understood why `%eth0` is required
- [ ] Pinged the global address with `ping6 -c2 2001:db8::10`
- [ ] Removed the address with `ip -6 addr del 2001:db8::10/64 dev eth0`
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — `ip -6 addr show eth0` lists both the `fe80::` link-local and `2001:db8::10/64`, and the global address answers ping
