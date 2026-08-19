# Lab 34 checklist — Diagnosing Routing Problems

Tick each item as you complete it.

- [ ] Ran `ip route` and identified the `default via X.X.X.X` gateway of last resort
- [ ] Ran `ip route get 8.8.8.8` and read the chosen interface, source IP and next-hop
- [ ] Ran `ip route get 10.99.0.5` and compared which route the kernel picked
- [ ] Added a static route with `ip route add 10.99.0.0/24 via $(ip route | awk '/default/ {print $3}') metric 100`
- [ ] Confirmed it with `ip route show 10.99.0.0/24` and read the metric
- [ ] Can explain what `metric` does when two routes compete (lower wins)
- [ ] Can explain longest-prefix match: `10.99.0.0/24` beats `10.0.0.0/8` regardless of metric
- [ ] Removed the test route with `ip route del 10.99.0.0/24`
- [ ] Can describe asymmetric routing and why it breaks stateful firewalls
- [ ] Ran `./break.sh` and reproduced the failure (`ping -c2 8.8.8.8` → Network is unreachable)
- [ ] Diagnosed the fault: `ip route` has no `default` line and `ip route get 8.8.8.8` returns "Network is unreachable"
- [ ] Ran `./cleanup.sh` and confirmed the ORIGINAL default route was restored from `/tmp/default-route.bak`
- [ ] **Test it:** `./verify.sh` reports `ALL CHECKS PASSED` — the default route is back, the 10.99.0.0/24 test route is gone, and `8.8.8.8` is reachable
