# Lab 34 — Diagnosing Routing Problems

Misconfigured routes show up as “I can ping this but not that”. In this lab you will inspect the routing table, query which route a destination would use, and add/remove a static route.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2`

---

## Step 1 — Print the full routing table

```bash
ip route
```

`default via X.X.X.X` is the gateway of last resort — used when nothing more specific matches.

---

## Step 2 — Ask the kernel which route a destination uses

```bash
ip route get 8.8.8.8
ip route get 10.99.0.5
```

The kernel returns the chosen interface, source IP, and next-hop. This is the fastest way to confirm a route is being applied.

---

## Step 3 — Add a static route

```bash
ip route add 10.99.0.0/24 via $(ip route | awk '/default/ {print $3}') metric 100
```

`metric` lets the kernel pick between competing routes — lower metric wins.

---

## Step 4 — Show route metrics

```bash
ip route show 10.99.0.0/24
```

---

## Step 5 — Detect asymmetric routing

Asymmetric routing = packet leaves through one path and returns by another. It often breaks stateful firewalls. Detect it by comparing:

```bash
traceroute 8.8.8.8     # outbound path
# from the other end, traceroute back to your IP
```

If the AS numbers (with `mtr -z`) are not symmetric, you have asymmetric routing.

---

## Step 6 — Remove the test route

```bash
ip route del 10.99.0.0/24
```

---

## Step 7 — Investigate route precedence

The longer the prefix, the more specific. `10.99.0.0/24` wins over `10.0.0.0/8` even if the latter has a lower metric.

---

## What you learned
- Use `ip route get` to ask the kernel “which route applies to this IP?”.
- The longest-prefix-match rule.
- How to add and remove a static route, and why metric matters.
