# Outreach Quality Check — Runnable Checklist

This skill is the gate. Before declaring any line, batch, folder, or iteration
"done," run every applicable item below. Return PASS / FAIL / UNSURE per item
with a one-sentence justification. If any FAIL, fix before proceeding.

This codifies bars from `taste.md` and `.claude/skills/outreach.md`. Pointers
follow each item; if an item feels unclear, read the cited section in full.

## Per line — runs on every personalization sentence

**Rationalization (must be explicit, even if internal):**
- [ ] Why does our project care about THIS person? (→ taste.md "Well-rationalized")
- [ ] What does THIS person uniquely know — beyond their role/title/institution? If unanswerable, line is role-matched: flag, do not force. (→ taste.md "Well-motivated conversation")
- [ ] Why this specific wording — what's it doing the default wouldn't? (→ taste.md "Per-piece rationalization")

**Motivation tests:**
- [ ] "Why are they emailing ME?" answerable in 3 seconds from the line alone. (→ taste.md "Well-motivated conversation")
- [ ] "What would we talk about?" answerable in 3 seconds from the line alone. (→ same)
- [ ] Swap test: replace this person with a different person in the same field — does the line still work? If yes, X isn't load-bearing → KILL. (→ outreach.md "Per-line rationalization")
- [ ] Causal path explicit: the sentence STATES the connection between X and Y, doesn't IMPLY it. (→ taste.md "The causal path must be explicit")
- [ ] Match the person's world: would THIS recipient want to talk about THIS topic? (→ taste.md "Match the person's world")

**Banned shapes:**
- [ ] No stawker opener — line does NOT start with "You [verb]ed" in any form: "You took", "You filed", "You wrote", "You led", "You were", "You've designed", "You sit inside", "You pioneered", "You own". (→ taste.md "Stawker openers" + Praneel framings)
- [ ] No role-framing: "Your directorship of X", "Your role as Y." The "of" after a possessive is almost always wrong. (→ taste.md "Role-framing")
- [ ] No credential-framing: "Your 30+ years", "Your 625+ publications", "Your DACVP boards." (→ taste.md "Credential-framing")
- [ ] No double emphasis: "first real", "one of the very few", "most important." (→ taste.md "Double emphasis")
- [ ] No sycophancy rhymes: "rare combination", "unique seat", "uniquely positioned", "one of the few", "puts you closer than almost anyone", "exactly what we need", "nobody has more experience." (→ taste.md "Sycophancy patterns")
- [ ] No institution names — except the person's own company (e.g., "Loyal" for Halioua is fine; "at ELIQUENT" for an employee is not). (→ taste.md V4 bans)
- [ ] No consultant verbs as load-bearing: "formalize", "accelerate", "leverage", "structure", "align", "convert their thesis." (→ taste.md "Consultant verbs")
- [ ] No banned AI tells: "defensible", "serious"/"take seriously", "credibly" (>10% of batch), "lands at", "changes the calculus", "fundable", "XCA-adjacent" / "[anything]-grade" / "[anything]-generated", "would have changed anything upstream", "ground truth", "meaningfully", "the kind of [noun]". (→ taste.md "Tells that signal AI-generated")
- [ ] No wordslop: any 3+ word noun phrase you can't explain in one concrete sentence ("genomic comparability thresholds", "translational signal optimization") → cut. (→ taste.md "Wordslop")
- [ ] Em-dash test: read the post-em-dash phrase alone. If it's "— especially Y" / "— particularly Z" (generic connector), banned. The thing after the dash must be a load-bearing specific claim. (→ taste.md "Em-dashes are load-bearing")
- [ ] Don't assume failure narratives for industry contacts. Reference a failed trial by name; don't claim to know why it failed. (→ taste.md "Don't assume failure narratives")
- [ ] Study names have context — "how you'd read SHIMMER" is wordslop unless you've said what SHIMMER is. (→ taste.md "Tells")

**Voice / texture:**
- [ ] Max ONE emphasis word per sentence: count "really" / "super" / "specially" / "very" / "actually". >1 = cut. Zero is fine. (→ taste.md "One deeply-human word", "One emphasis word per sentence, max")
- [ ] Concrete nouns over abstract — no load-bearing "framework", "ecosystem", "paradigm", "landscape." If you reach for an abstract noun, decompose it. (→ taste.md "Concrete nouns")
- [ ] Concrete-noun-load-bearing test: if line names a drug/trial/paper/program (HIMALAYA, LOY-002, Luxturna, EVERLAST, rabacfosadine), remove the noun. Does sentence still work? If yes → flexing, cut. If it collapses → the noun belongs. (→ outreach.md "Naming concrete things")
- [ ] Tag question if you want a reply: "Does that map onto what you've seen?" / "No chance it's perfect, right?" (→ taste.md "Tag questions invite replies")
- [ ] Don't fake confidence: honest "we don't yet know X" beats hedged bullshit. (→ taste.md "Don't fake confidence")
- [ ] Each idea is the natural consequence of the one before it. Re-read sentence; does it require a re-read to understand? If yes, the sentence failed. (→ taste.md "The core rule")

**Tier tag:**
- [ ] Line tagged AMAZING (creative, specific, quotable) or GOOD (simple, human, functional). 0% CONSULTANT. (→ taste.md "Communication hierarchy")
- [ ] Read-aloud test: could you say this out loud to the recipient without cringing? (→ same)
- [ ] Amazing > Human > Consultant ladder: ideal is creative, backup is one-deeply-human-thing, failure is consultant. (→ taste.md "Amazing > Human > Consultant")

## Per batch — runs every ~10-20 lines

- [ ] Shape diversity, not word diversity. Different SENTENCE SHAPES across the batch — or same shape with different fillers? Same shape = converged. (→ outreach.md "Convergence is the #1 failure mode")
- [ ] No template repetition: no 3+ uses of any single phrasing — including once-praised ones that have gone stale ("Your X would help us understand whether Y", "One thing our analysis rests on", "is the core XCA bet", "is operating directly in that question"). (→ outreach.md "Convergence")
- [ ] Editorial QA by a SEPARATE subagent. The writer subagent CANNOT QA itself reliably; its self-audit will report clean while editorial read says bad. (→ outreach.md "QA subagent self-audits are unreliable")
- [ ] Re-read exemplars at this checkpoint. Every 5-10 contacts. (→ outreach.md "Exemplar-driven calibration")
- [ ] Read holistically, not via regex. Regex catches words; only editorial eyes catch shape. (→ outreach.md "How to fight convergence")

## Per folder — runs before launching a folder rewrite

- [ ] **Folder has its own exemplar** if it's under ~10 contacts and doesn't fit cleanly into a tier-default. Don't rewrite a small folder before the human writes its exemplar. (→ outreach.md "Small folders need their own exemplar")
- [ ] **Bad-email ≠ bad-contact.** A thin writeup is a rewrite signal, not a delete signal. Only delete contacts with no thesis connection at all. (→ taste.md "The 'bad email ≠ bad contact' rule", outreach.md)

## Per iteration round — runs before launching another rewrite pass

- [ ] **Iteration cap reached?** After 3-4 rounds, marginal quality gain < marginal convergence risk. Ship the imperfect 5-10% as a manual queue for the human; don't run another round. (→ taste.md "Iteration discipline", outreach.md)
- [ ] **Trust human's editorial read over your audit numbers.** When data says "clean" and human says "bad," the human is right. Always. (→ outreach.md "Trust the human's editorial read")
- [ ] **Surface-compliance check.** Did the rewrite swap a banned word for an allowed one and call it done? Or did it actually do editorial work — motivation, specificity, voice? Surface compliance is the most seductive trap. (→ outreach.md "Surface compliance is the most seductive trap")
- [ ] **AI-can't-write check.** Are there contacts where any line you write will be mediocre — senior FDA, very high-profile founder, someone whose context is deeply specialized? Flag for the human, don't ship to hit coverage. (→ outreach.md "Some contacts AI cannot write well")
- [ ] **Diversity-quota check.** Was the prompt told to "rotate openers, vary structure"? If yes → expect sycophancy ("rare combination", "uniquely positioned"). Forced diversity creates fake variety. Aim for the GOLD per contact instead. (→ outreach.md "How to fight convergence")

## Deliverable-level (one-pagers, memos, anything beyond a single email)

- [ ] **Delete-or-respond test.** Simulate the reader receiving this cold. Would they respond, or hit delete? (→ taste.md "Quality gates")
- [ ] **What-are-you-asking-me-to-do test.** Reader knows in one sentence what happens if they say yes. (→ same)
- [ ] **Who-wrote-this test.** Reader understands who you are without being told you're serious. The quality of the analysis IS the credibility. (→ same)
- [ ] **Lazard bar.** For visual argumentation, study the Lazard "Geopolitics of Biotech" report (URL in taste.md). Your content should hit that bar even if formatting happens later. (→ taste.md "Lazard bar")
- [ ] **Lead with risk-reduction, not opportunity.** "X could have predicted these failures" beats "X unlocks $YB." Negative framing earns attention; positive framing earns skepticism. (→ taste.md, outreach.md)
- [ ] **Evidence labels in working docs.** Every factual claim is [PRIMARY] / [VERIFIED] / [INFERENCE]. Final deliverable doesn't show labels; working doc does. (→ taste.md "Evidence labels")

## Exemplar handling — runs whenever exemplars are read or extracted

- [ ] Don't "improve" the human's exemplars. Typos, awkward phrasing, unfinished thoughts ARE signal. Cleaning them up destroys voice. (→ taste.md "The exemplar principle", outreach.md)
- [ ] Read the human's REASONING, not just the line. "I left [this nuance] there because there's probably a better way to say it" tells you the human knows the line is imperfect AND the direction it should improve. Both pieces matter. (→ outreach.md "How to get exemplars")
- [ ] Treat extracted rules as decaying signal. Rules from exemplars become templates over time; re-derive from new exemplars rather than stacking forever. (→ outreach.md, taste.md "Iteration discipline")
- [ ] When rules conflict with exemplars, exemplars win. (→ taste.md "The exemplar principle")

## Hard stops (any of these = halt and surface to the human)

- A subagent cannot answer "What does this person uniquely know?" for a contact.
- A batch shows the same sentence shape >40% of lines.
- The human's editorial read disagrees with audit numbers.
- A small folder (<10 contacts) is about to be rewritten without its own exemplar.
- A subagent is rewriting based on a Python regex scan of antipatterns.
- "Diversity rotation" is being instructed in the prompt.

If any hard stop fires: stop the pass, write what you found, ask the human.

## Pointers (full context lives here)

- `taste.md` (repo root) — communication hierarchy, V4 antipatterns, Praneel's framings, well-motivated conversation, quality gates (delete-or-respond, what-are-you-asking, who-wrote-this), Lazard bar, lead-with-risk-reduction, evidence labels, the exemplar principle, iteration discipline.
- `.claude/skills/outreach.md` — full pipeline (find → write → QA → fix → apply → human review → iterate → ship), tier treatment, exemplar collection process, what actually breaks at the edges, small-folder rule, trust-human-read.
- `context/exemplars.md` (per-project) — calibration truth. The human's own hand-written lines + reasoning. Never clean up.
