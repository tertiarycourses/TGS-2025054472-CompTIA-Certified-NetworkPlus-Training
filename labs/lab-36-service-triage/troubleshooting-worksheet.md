# Lab 36 — Troubleshooting Worksheet (CompTIA 7-Step Methodology)

**Learner name:** ______________________  **Date:** ____________

**The ticket:** *"https://example.com is down — nobody in the office can reach it."*

Work the seven steps **in order**. Do not skip to step 5. Fill in every box —
the discipline of writing the theory down *before* you test it is the whole
point of the methodology, and it is what the exam asks you to reproduce.

Commands available to you: `nc`, `openssl s_client`, `curl` (this lab), plus
`ping`, `traceroute`, `mtr` (Lab 29), `dig` (Lab 30), `ip route` (Lab 34).

---

## Step 1 — Identify the problem

*Gather information, question users, identify symptoms, determine if anything
has recently changed, and duplicate the problem if possible. Approach multiple
problems individually.*

**1a. What exactly is the reported symptom, in the user's own words?**

> _______________________________________________________________

**1b. What questions would you ask the user? (list at least three)**

| # | Question | Why it narrows the problem |
|---|----------|----------------------------|
| 1 |          |                            |
| 2 |          |                            |
| 3 |          |                            |

**1c. Scope — who and what is affected?**

- [ ] One user only
- [ ] All users on one subnet / VLAN
- [ ] Everyone
- [ ] One destination only, or all destinations?

> Evidence for your answer: ______________________________________

**1d. What changed recently?** (config change, patch, new firewall rule, cert renewal)

> _______________________________________________________________

**1e. Can you duplicate the problem?** Run the Step 2 command and paste the result.

```
$ nc -zv example.com 443

```

**1f. Is this one problem or several?** If several, list them and treat each separately.

> _______________________________________________________________

---

## Step 2 — Establish a theory of probable cause

*Question the obvious. Consider multiple approaches — top-to-bottom / bottom-to-top
of the OSI model, and divide-and-conquer.*

**2a. Which OSI layers are still known-good?** Tick what you have already proven.

| Layer | Test | Result | Verdict |
|-------|------|--------|---------|
| L3 — reachability | `ping -c2 example.com` | | works / fails |
| L3/L7 — name resolution | `dig example.com +short` | | works / fails |
| L4 — TCP handshake | `nc -zv example.com 443` | | works / fails |
| L6 — TLS | `echo \| openssl s_client -connect example.com:443 -servername example.com` | | works / fails |
| L7 — HTTP | `curl -v https://example.com` | | works / fails |

**2b. Which approach are you using?**

- [ ] Bottom-to-top (start at L1, work up)
- [ ] Top-to-bottom (start at L7, work down)
- [ ] Divide and conquer (start in the middle — L4)

> Why that one: _________________________________________________

**2c. State your theory in ONE sentence.** ("I believe the cause is …")

> _______________________________________________________________

**2d. What is the *obvious* explanation you should question before accepting it?**

> _______________________________________________________________

**2e. List one alternative theory you will fall back to if 2c is disproven.**

> _______________________________________________________________

---

## Step 3 — Test the theory to determine the cause

*If the theory is confirmed, determine the next steps. If it is NOT confirmed,
establish a new theory or escalate.*

**3a. What single test will confirm or disprove the theory in 2c?**

> Command: ______________________________________________________

**3b. What result would CONFIRM it?**

> _______________________________________________________________

**3c. What result would DISPROVE it?**

> _______________________________________________________________

**3d. Run it. Paste the actual output.**

```

```

**3e. Outcome:**

- [ ] Theory **confirmed** — continue to Step 4
- [ ] Theory **disproven** — return to Step 2 with theory 2e, and record the new theory here:

> New theory: ___________________________________________________

- [ ] Beyond my scope — **escalate**. To whom, and what information do you hand over?

> _______________________________________________________________

**3f. Root cause, stated precisely (what, where, since when):**

> _______________________________________________________________

---

## Step 4 — Establish a plan of action and identify potential effects

*Resolve the problem and identify potential effects of the fix.*

**4a. The fix, as an exact command or change:**

> _______________________________________________________________

**4b. What else could this change affect?** (other users, other services, security posture)

> _______________________________________________________________

**4c. Rollback plan — how do you undo it if it makes things worse?**

> _______________________________________________________________

**4d. Does this need a change window or approval?**

- [ ] No — low risk, apply now
- [ ] Yes — because: ____________________________________________

---

## Step 5 — Implement the solution or escalate

**5a. Command(s) actually run, with timestamps:**

```

```

**5b. Did implementation go as planned?**

- [ ] Yes
- [ ] No — what deviated: _______________________________________

**5c. If escalated instead, to which team and with what evidence attached?**

> _______________________________________________________________

---

## Step 6 — Verify full system functionality and implement preventive measures

**6a. Re-run the failing test. Paste the output.**

```
$ nc -zv example.com 443

```

**6b. Re-run the FULL triage to prove nothing else broke.**

| Test | Expected | Actual | Pass? |
|------|----------|--------|-------|
| `nc -zv example.com 443` | succeeded | | |
| `openssl s_client` verify code | `0 (ok)` | | |
| `curl -v https://example.com` | HTTP 200 | | |
| `curl -w` timing | all phases sub-second | | |

**6c. Did the user confirm the service is working for them?**

- [ ] Yes  - [ ] Not yet contacted

**6d. Preventive measure — what stops this recurring?**

> _______________________________________________________________

**6e. What monitoring or alert would have caught this before the user called?**

> _______________________________________________________________

---

## Step 7 — Document findings, actions and outcomes

*This is the step most often skipped and most often needed six months later.*

| Field | Entry |
|-------|-------|
| Ticket reference | |
| Date / time reported | |
| Date / time resolved | |
| Reported symptom | |
| Scope / users affected | |
| Root cause | |
| OSI layer of the fault | |
| Diagnostic commands that proved it | |
| Fix applied | |
| Rollback available? | |
| Verification evidence | |
| Preventive action raised | |
| Follow-up owner | |

**7a. Write the closing note the user will read (two sentences, no jargon):**

> _______________________________________________________________
>
> _______________________________________________________________

**7b. Write the knowledge-base entry the next engineer will read (technical):**

> _______________________________________________________________
>
> _______________________________________________________________

---

## Trainer sign-off

- [ ] All seven steps completed in order
- [ ] Theory was written down **before** it was tested (Step 2 before Step 3)
- [ ] Root cause identified correctly and matched to an OSI layer
- [ ] Rollback plan stated before the fix was applied
- [ ] Full-system verification done, not just the single failing test
- [ ] Documentation complete enough for another engineer to act on

**Trainer:** ______________________  **Signature:** ______________________
