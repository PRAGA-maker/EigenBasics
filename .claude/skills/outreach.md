# Cold Outreach Pipeline — From Contact List to Sent Emails

This skill runs the full cycle: find people, write personalized emails, QA them,
and prepare for send. It was battle-tested across 419 contacts in the XCA Analysis
project and went through 5 iteration rounds before shipping. Everything below is
hard-won.

## Quality enforcement

**Before declaring any line, batch, folder, or iteration "done," run the
`outreach-quality-check` skill** (`.claude/skills/outreach-quality-check.md`).
It codifies every bar from this file plus `taste.md` into a runnable per-line /
per-batch / per-folder / per-iteration / deliverable / exemplar-handling check,
plus hard-stop conditions that halt the pass and surface to the human.

Subagents return PASS / FAIL / UNSURE + one-sentence justification per item.
Any FAIL = fix before proceeding. Any hard-stop fires = halt and ask.

Don't try to remember every rule from the prose below. The prose explains the
WHY; the checklist enforces the WHAT. Use both.

## When to use

When the human says: "find contacts", "write outreach", "cold email campaign",
"personalization pass", "email pipeline", or anything about mass-personalized outreach.

## The loop (this is the bread and butter)

```
1. FIND contacts (web search, conferences, papers, directories)
   └── Per contact: .md file with Name, Title, Org, Email, Why Contact,
       Personalization Hook, Draft Email
   └── Quality bar: "would this person's perspective be useful?" not
       "does their title match?"

2. WRITE personalization (per-contact, isolated context)
   └── Read taste.md for the rules
   └── Use 5 hand-written EXEMPLARS as few-shot calibration (human writes these)
   └── Each rewrite gets a rationalization: why this person, why this phrasing
   └── Output: staging JSON (NOT directly to .md files)

3. QA via editorial subagent (NOT mechanical .py)
   └── Subagent reads the batch holistically
   └── Flags: convergence patterns, consultant-speak, banned phrases, lines
       where Y doesn't motivate X
   └── Sample-based, not exhaustive (read all lines, deeply review 30-40)

4. FIX surgically (per-flagged-line, NOT batch rewrite)
   └── Fix ONLY what QA flagged
   └── Preserve the rest verbatim
   └── Don't "improve" clean lines

5. APPLY to .md files (non-destructive)
   └── Replace ONLY the personalization paragraph
   └── Preserve everything else (metadata, Calendly link, sign-off)
   └── Log what was applied and from which proposal file

6. HUMAN REVIEW on samples (not full review)
   └── Pull 20-25 diverse samples across tiers
   └── Human edits/comments → new exemplars + new banned patterns
   └── Iterate steps 2-5 with tightened rules

7. Repeat 2-6 until human says "ship"
```

## What actually breaks (read this carefully)

### Convergence is the #1 failure mode.

Every batch rewrite converges. It's not a bug — it's how language models work.
You write 50 lines, and by line 30 they all sound the same. The opener drifts to
one pattern. The ask-verb drifts to one phrase. Word counts cluster.

**How to fight it:**
- Isolated context per contact. Each rewrite sees ONLY: taste.md + exemplars +
  that one contact's .md file. NOT the previous 49 rewrites.
- **Aim for the GOLD per contact, not for variety quotas.** Diversity emerges
  from per-contact thought. Forced diversity creates sycophancy: instructing
  "rotate openers, vary structure" makes the model fill the variety quota with
  "rare combination," "unique seat," "puts you closer than almost anyone." This
  was the single biggest rig-systemic mistake in the prior 5-round XCA session.
- Re-read exemplars every 5-10 contacts. This is a HARD RULE, not a suggestion.
- After each batch: read the lines holistically with editorial eyes. If the
  SHAPE feels uniform even when the words differ ("Your X would help us
  understand whether Y" repeated 22 times in a 50-line batch), you've converged.
  Regex won't catch shape. Only editorial reading will.

### Batch rewrites always introduce correlated errors.

A Python script that touches 400 files will introduce one uniform bug across all
400. "At Retired" as an org name. Removing a word that should've stayed. Adding
"actually" to every line. The fix is worse than the original.

**Rule: Python is for DETECTION (flagging antipatterns via regex). Subagents are
for REWRITING (editorial judgment per line). Never use .py to rewrite.**

### "Bad email" ≠ "bad contact."

The most valuable contacts often have the worst initial writeups. An FDA director
who built the pathway you're studying will have a boring-looking .md file because
their value isn't in a flashy research hook — it's in institutional knowledge.

**Rule: if someone has a thin hook but real value, REWRITE the email. Only DELETE
contacts that genuinely have no connection to the project's thesis.**

### QA subagent self-audits are unreliable.

A subagent that wrote 50 lines will report "0 antipatterns, 100% clean" because
it can't see its own convergence. A SEPARATE QA subagent catches what the writer
missed — every time.

**Rule: always QA with a different subagent than the one that wrote.**

### Each iteration bans the last iteration's tells, and the model invents new ones.

You ban "actually" → it starts using "genuinely." You ban "holds up" → it starts
using "carries weight." You ban "one of the few" → it starts using "a rare."
This is an arms race with diminishing returns.

**Rule: after 3-4 rounds, stop iterating on the batch and ship. The remaining
5-10% of imperfect lines are less costly than another round of convergence.**

### Trust the human's editorial read over your audit numbers.

Every iteration round in the prior XCA session, the agent's audit said "0
antipatterns, 100% clean" and the human's editorial read said "~50% bad." The
human was right every single time. Self-audit numbers measure surface
compliance with rules; they cannot measure whether a line feels written. When
the human says "this is bad" and your data says "this is fine," update toward
the human. Always.

### Surface compliance is the most seductive trap.

A subagent will add an emphasis word, swap a banned phrase, and report "I
applied taste.md!" — while the line is still hollow. It's optimizing for
surface compliance ("I rotated the opener!") instead of doing the editorial
work (does the Y motivate the X? would the recipient know what to talk
about?). Grade rewrites on rationalization quality, not surface compliance.

### Some contacts AI cannot write well.

Senior FDA officials, very high-profile founders, people whose context is
deeply specialized. The right answer is sometimes "flag this for the human to
write personally." Don't ship a mediocre line because you're trying to hit
100% coverage. Honest "I can't do this contact justice" beats fake confidence.

## Tier treatment (different contacts need different emails)

Don't use one template for all contacts. At minimum, separate:

- **Academic researchers** — one clean research hook, direct scientific question.
  Short (20-28 words). They read their own email.
- **Practitioners bridging roles** (former-FDA-now-consulting, etc.) — the
  combination of experiences IS the value. Name each side concretely.
- **Industry / pharma** — don't assume failure narratives. Lead with thesis,
  reference their work softly. Comparative questions ("XCA or organ-on-chip?")
  invite expert judgment.
- **VCs / investors** — use their own language. Invite skepticism. 0% expected
  response rate. Design for the signal, not the reply.
- **Executives / founders** — assume an EA reads first. Lead with thesis + why
  THIS person matters. Non-standard framings OK.

For VCs, execs, and senior industry: add a P.S. paragraph ("happy to speak with
someone on your team if better") — but as a SEPARATE paragraph, NOT bundled
into the personalization line. Inline forward-closes read as "shoved on."

### Small folders need their own exemplar

Any folder under ~10 contacts that doesn't fit cleanly into a tier exemplar
(e.g., niche sub-categories like xca-pioneers, reg-boutique-analysts,
cro-animal-trials) needs its own hand-written exemplar from the human BEFORE
any rewriting. Editorial calibration in the prior session found 4-of-4 KILL
lines in a 4-contact niche folder that had no exemplar — the model defaulted
to its average voice. **Don't rewrite a small folder before getting its
exemplar.** This is the highest-leverage rule that prior sessions missed.

## Exemplar-driven calibration

The single most important input to the pipeline is 5 hand-written exemplar
personalization lines from the human. These are the calibration truth — when
rules conflict with exemplars, exemplars win.

**How to get exemplars:**
1. Pick 5 contacts spanning different tiers (academic, practitioner, industry,
   VC, exec)
2. Show the human the current line + the contact's context (Why Contact, Hook)
3. Ask them to write their version, or react to yours
4. The human's version — including typos, awkward phrasing, unfinished thoughts —
   IS the exemplar. Don't clean it up. Their voice is the target.
5. **Read their REASONING, not just the line.** Humans often write reasoning
   that looks like "unfinished thoughts" but is actually them explaining their
   thought process — like a symbolic-logic puzzle where many useful inferences
   are embedded in the explanation. Example: "I left [this nuance] there because
   I think there's probably a better way to say it" is signal that the human
   knows the line is imperfect AND knows the direction it should improve in.
   Both pieces matter. Read the reasoning carefully.
6. Extract RULES from the exemplars (what patterns they used, what they avoided)
   and add those rules to taste.md — but be careful: rules that came from
   exemplars eventually become templates. Treat rules as signal that decays;
   re-derive them from new exemplars over time.

**Without exemplars, every batch will converge to generic "good cold email" voice
instead of the human's actual voice. This is the #1 reason prior attempts failed.**

## The email structure

```
Good morning,

[Boilerplate intro — who we are, what we're doing, 1-2 sentences]

[PERSONALIZATION LINE — THIS is what the pipeline writes. 20-40 words depending
on tier. The ONE sentence that tells the reader why WE are emailing THEM
specifically.]
[Standard closer — "Would love a 20-minute chat if you're open to it"]

[Calendly link + one-pager attachment mention]
[Thank you + warm sign-off]
[Name / Title / Org]

[P.S. — forward-to-team line, ONLY for senior contacts]
```

The pipeline touches ONLY the personalization line. Everything else is templated
and preserved.

## Per-line rationalization (prevents template-filling)

Before finalizing each line, the subagent must answer three questions:

1. **Connection to project:** why does our thesis care about this person's work?
2. **Connection to them:** what's THEIR unique perspective — not their role, not
   their title, but what they specifically KNOW?
3. **Phrasing rationale:** why THIS wording? What's it doing that the default
   wouldn't?

If the subagent can't answer #2, the contact is probably a role-match and should
be flagged for review, not forced into a template.

### Naming concrete things is the highest-leverage editorial move

Specific drug names, trial names, paper titles, company programs — these signal
"writer did the homework" instantly. "HIMALAYA," "LOY-002," "Luxturna,"
"rabacfosadine," "EVERLAST." But ONLY when load-bearing for the question. Test:
remove the proper noun. Does the question still work? If yes, you're flexing —
cut it. If the question collapses, the name belongs.

## Communication hierarchy

Every line should land in one of two tiers:

- **AMAZING** (~30%) — creative, specific, makes a smart reader stop and think.
  The kind of phrasing that makes someone want to reply.
- **GOOD** (~60%) — simple, human, functional. Says what's happening without
  jargon, without flourish. Clear enough to forward.
- **CONSULTANT** (0%) — generic, could appear in any strategy deck. "Align with
  regulatory shifts." "Fills disease model gaps." Flag and rewrite.

The bar: "Could I read this line out loud to the person without cringing?"

## Sending

Once the human approves the batch:
1. Regenerate `review.csv` to get the final contact list with emails
2. Attach the one-pager PDF
3. Use Gmail API / send_emails.py / or manual send depending on human preference
4. Log sent emails for follow-up tracking
