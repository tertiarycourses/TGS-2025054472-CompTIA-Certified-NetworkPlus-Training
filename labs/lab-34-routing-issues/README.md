# Lab 34 — Diagnosing Routing Problems

Misconfigured routes show up as “I can ping this but not that”. In this lab you will inspect the routing table, query which route a destination would use, and add/remove a static route.

Run on https://killercoda.com/playgrounds/scenario/ubuntu

**Required software (free, pre-installed):**
- `iproute2`

**Files in this lab folder:**

| File | Use |
|------|-----|
| `break.sh` | deletes the default route so you can diagnose a real fault (Step 8) — backs it up first |
| `cleanup.sh` | restores the **original** default route from `/tmp/default-route.bak` and removes the test route |
| `verify.sh` | objective pass/fail check that routing and connectivity are restored |
| `checklist.md` | tick-box list of everything you should be able to do by the end |

> **This lab changes routing state.** Always finish with Step 6 and `./cleanup.sh`
> so the next lab starts clean.

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

## Step 8 — Diagnose an injected fault

Now work a fault you did not create.

```bash
./break.sh
```

`break.sh` writes your current default route to `/tmp/default-route.bak`
**before** it deletes anything, then removes the gateway of last resort.

Reproduce the symptom — note that it is *selective*, the classic
"I can ping this but not that":

```bash
ping -c2 $(cat /tmp/default-route.bak | awk '{print $3}')   # local gateway still answers
ping -c2 8.8.8.8                                            # Network is unreachable
```

Now diagnose it with the Step 1 and Step 2 commands:

```bash
ip route
ip route get 8.8.8.8
ip route get 10.99.0.5
```

`ip route` has no `default via …` line, and `ip route get` answers
`Network is unreachable` — the kernel is telling you directly that no route
matches. The gateway itself is still reachable because it sits on a connected
subnet, which is exactly why the symptom looks partial rather than total.

Then restore and confirm:

```bash
./cleanup.sh
./verify.sh
```

`cleanup.sh` re-adds the saved default route and clears the `10.99.0.0/24` test
route from Step 3. `verify.sh` prints `PASS:` / `FAIL:` lines and exits non-zero
if anything is still wrong.

---

## What you learned
- Use `ip route get` to ask the kernel “which route applies to this IP?”.
- The longest-prefix-match rule.
- How to add and remove a static route, and why metric matters.
- Why a missing default route produces a *partial* outage, not a total one.

---

## Before you leave

Run `./cleanup.sh` if you have not already, then work through `checklist.md` and tick every line.
