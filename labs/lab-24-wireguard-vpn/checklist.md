# Lab 24 checklist — Site-to-Site VPN with WireGuard

Tick each item as you complete it.

- [ ] Installed WireGuard with `apt update && apt install -y wireguard wireguard-tools`
- [ ] Created the two site namespaces `site-a` and `site-b`
- [ ] Generated both key pairs with `wg genkey | tee a.key | wg pubkey > a.pub` (and the same for `b`)
- [ ] Can explain why the private key never leaves its own peer, and only the `.pub` is exchanged
- [ ] Created the `wg0` WireGuard interfaces in both namespaces
- [ ] Addressed them `10.99.0.1/24` on site-a and `10.99.0.2/24` on site-b
- [ ] Configured site-a with `listen-port 51820` and site-b's public key, `allowed-ips 10.99.0.2/32`
- [ ] Configured site-b with `listen-port 51821`, site-a's public key, `allowed-ips 10.99.0.1/32` and `endpoint 127.0.0.1:51820`
- [ ] Read `wg0-a.conf` and `wg0-b.conf` and can map every imperative `wg set` flag to its config-file directive
- [ ] Confirmed neither shipped config contains a real key — only `<PASTE_..._HERE>` placeholders
- [ ] Brought both interfaces up and pinged `10.99.0.1` from site-b successfully
- [ ] Ran `ip netns exec site-a wg show` and found the peer public key, a recent handshake and non-zero transfer counters
- [ ] Can explain why `allowed-ips` is both a routing rule and an inbound ACL
- [ ] Ran `./cleanup.sh` — both namespaces deleted and `/tmp/*.key` removed
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — both peers hold each other's public key, a handshake has completed, encrypted bytes have moved, and `ping -c2 10.99.0.1` succeeds across the tunnel
