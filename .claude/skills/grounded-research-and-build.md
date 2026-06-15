---
name: grounded-research-and-build
description: Use when a question needs a deep, decision-grade answer that must be both verified AND proven on real data — "map this field/these options and tell me which we should adopt and why," "investigate X exhaustively," "actually run/clone each approach and bench it on our kind of data," "find the things they're talking about," "take the time you need / be comprehensive." Fires on prompts that grant latitude, demand first-principles + trade-offs, point you at the human's own context, and tell you to RUN it rather than just report. The execution counterpart to strategic-deliberation. Not for quick lookups, pure coding, or strategy with no empirical legwork.
---

# Grounded research and build

This skill is for the runs where the human hands you a real question with stakes and effectively says *go find out, and don't come back with a survey — come back with the answer, proven*. A field to map and a decision riding on it ("which family do we go under?"). A claim to settle ("is this approach actually better, on data like ours?"). The shape that works: ingest the human's *real* context before you research anything → say what you think the question actually is, and reframe it if their framing is off → fan out verified research in parallel → then **refuse to stop at what the literature says** and go ground it by actually running the thing on real data → synthesize into a decision tied to *their* first principles → stay honest about what you couldn't do → leave artifacts that outlive the run.

You are the research manager who also gets their hands dirty. Your job is to cover empirical ground fast, to trust nothing you haven't verified, and — the part that makes this skill different from a normal research flow — **to turn "the field believes X" into "X is true, here is the number, on data shaped like yours."** Most agent research stops at assertion. This loop's quality lives in the refusal to stop there.

## When to use

- "Map this field / these camps and tell me what we should do" — survey + decision
- "Investigate X exhaustively" where a recommendation, not a reading list, is the deliverable
- "Benchmark the options" / "actually try each approach and see which holds up"
- Overnight or high-effort runs where the human has given you latitude and gone quiet
- Anytime a load-bearing claim can be *checked by running something* — and therefore should be

## When not to use

- Quick fact lookups or single-file edits (just answer / just do it)
- Pure implementation with a known spec (use the normal coding/TDD flow)
- A go/no-go *deliberation* with no empirical legwork yet — that's `strategic-deliberation`; this skill is what you run *after* the decision is "go find out"
- When the human wants a fast take and explicitly doesn't want the heavy machinery

## The thing that makes this work

**Grounding is the whole game.** A literature scan that ends in "here's what each camp argues" is cheap and forgettable. The version that lands is the one where you *spent the horsepower to make the abstract concrete*: you installed the actual tools, found a dataset shaped like the human's real problem, ran one method from each camp, and produced a number that settles the argument ("the adult reference mislabels 81% of cells"). The literature told you where to look; the run told you what's true.

The second half of the game is **trusting nothing you haven't verified — including yourself.** Fanned-out research hallucinates. Your own benchmark has confounds. The discipline is to verify claims adversarially (spawn skeptics whose job is to *refute*), to be your own harshest reviewer when a result looks too clean, and to interrogate a surprising finding instead of shipping it. When the human pokes at a result, the move is not to defend it — it's to go back to the data and find out whether it holds. (A "hippocampal" cluster that turns out to be ~99% one drug + one donor is not a finding; it's a confound, and saying so is worth more than the original claim.)

If you're not going to ground and verify — if you're going to relay sources and call it research — don't spin up the machinery. Just answer the question.

## What the prompt looks like when this fires (and how to induce it)

Half the quality is in how the human shows up — and the human can deliberately induce this loop by *writing* these levers into the prompt. When you see a prompt carrying most of them, this is the skill. The levers, with the verbatim shapes from the run this was distilled from:

- **Latitude + time** → license to spend the horsepower and not check in. *"Take as much time as you need." "I'll be back in ~6 hours, feel free."*
- **Exhaustiveness, not a summary** → fan out + verify. *"I need a super comprehensive understanding." "Extremely exhaustively."*
- **A real decision attached** → synthesize to a recommendation, not a survey. *"What family do we go under? What are the trade-offs? Why?" "We'll either train our own or use someone else's, then validate on our data."*
- **"Actually run it" — the load-bearing lever** → the grounding step. *"Actually bench it." "Run the approach from each branch you can clone." "See if you can find the things they're talking about."* This is the clause that flips the run from report to proof. **If it's missing, this skill degrades into a literature survey** — so when the human wants the grounded version, make sure this lever is present (or add it yourself and say you are).
- **First-principles framing** → the reframe + the synthesis. *"What is their first-principles thinking?" "Why is there a difference?" "What is *actually* different?"*
- **A pointer to their own context** → recon FIRST. *"Company context is under /downloads." "Look at my repo for the tooling."*
- **Concrete scope + an output location** → named entities/options to investigate; *"put the .mds under /downloads/annotation."*
- **Honesty about their own gaps** → licenses you to teach and to correct their framing. *"I'm the ML person; I don't know the science nuances; I don't really know what's going on."*

**Reusable prompt to induce this in a fresh Claude (paste and fill the brackets):**
> "Map [field / these options] and tell me which we should adopt and why — first principles, the real trade-offs, how the camps *actually* differ and how their views evolved. Be exhaustive; take the time you need, I'll check back later. Our context is in [path] — read it first. Then **actually run one approach per camp on a real dataset like ours, clone what you need, bench it, and see if you find what they claim**. Put findings as .mds in [path]. Be honest about what you couldn't run. I'm the [role]; assume I don't know the domain nuances, so reframe my framing if it's off."

## The loop (defaults, not a checklist)

The deliverable is a grounded decision. Loop-compliance is not the same thing. These are the phases this usually takes; decide which earn their weight for *this* question, then run those with full force.

0. **Recon the human's real context first.** Before you research the world, read *their* world — the repo, the docs, the prior decisions, the constraints, the tooling they already have. Tailor everything downstream to the decision they actually face, not a generic version of it. (Finding that they already cite atlas X, already have tool Y in their stack, already chose line Z changes the entire recommendation.)
1. **Say what the question is — and reframe if their framing is off.** Don't just execute the literal ask. If the real fault line is somewhere other than where they pointed, say so early, with evidence. The reframe is often the most valuable thing you produce.
2. **Fan out verified research, in parallel.** Spawn workflows, not loose agents (see the repo's orchestration posture). Force structured output. Run complementary angles — general web *and* domain-specific sources — so they cross-check. Then **adversarially verify the load-bearing claims** (majority-refute to kill). Keep the kills; they're signal.
3. **Ground it — actually run each branch.** This is the step normal research skips. Stand up the real tools, get a dataset that resembles the human's actual problem, and run one method per camp/option. Compute metrics that make the camps' disagreements *measurable*. Function-driven, not smoke: a passing happy path is not evidence — evidence is the real work done correctly across the real heterogeneity (the edge populations, the messy states, not just the clean case).
4. **Go incremental; fix at the root.** Get a guaranteed-correct core result first, then reach for the stretch. Diagnose bugs at the source and fix them; never paper over with a silent fallback. Each step verified before the next.
5. **Synthesize into a decision, tied to their first principles.** Don't dump agent output — write your own synthesis and route it back to *their* business logic (what they sell, what their bottleneck is, build-vs-buy, a validation plan, what they already have). The recommendation is the point.
6. **Persist artifacts; parallelize; never idle.** Run research, installs, and downloads in the background and do useful work while they run. Leave a status file the human can read cold, durable deliverables, provenance, and memory. The work should outlive the session.

## You are grounding, not reporting

There is a difference between running the loop and actually settling the question. The failure mode is execution theater: you fan out agents, collect their prose, assemble it into a handsome report, and never run the thing that would tell you whether any of it is true. It *looks* like deep research and has none of the load-bearing weight.

Watch for these signs you've slipped into reporting mode:
- Your "findings" are all restatements of sources — not one number you produced yourself
- You hit an install/data wall and quietly narrowed the benchmark instead of fixing it or naming the gap
- A result came out suspiciously clean and you shipped it without trying to break it
- You're relaying what each camp claims rather than testing whose claim survives on real data
- The human asked a sharp follow-up and you defended your result instead of re-opening the data
- You're waiting on a background job and doing nothing, instead of writing/preparing the next phase

## Honesty is an output, not a footnote

A logged problem is a TODO, not a resolution. If you couldn't run the full-fidelity version (too big a download, no GPU, a package that won't build), say exactly that, in a "what I could NOT do" section, and say what the production-grade version would be. A degradation you mention and move past is a silent fallback wearing a hi-vis vest. The human trusts the grounded claims *because* you were precise about the ungrounded ones.

## When the shape is right vs. the wrong shape

The loop earns its weight when: the question has a decision attached and real stakes; the human gave you latitude ("take your time," "be exhaustive," "actually bench it"); there are load-bearing claims that *can* be checked by running something; and there's enough of their real context to tailor the answer.

The loop is the wrong shape when: the answer is a lookup or a known-spec edit; nothing can be grounded by running it (then it's a `strategic-deliberation` or a plain synthesis); the human wants speed over rigor; or there's no decision riding on the outcome. Don't manufacture a benchmark to feed the loop when the question doesn't have an empirical core — that produces a skill-shaped artifact with no substance, which is the exact failure this skill exists to prevent.

## Worked example — the run this was distilled from

A one-line-per-phase trace of the session that produced this skill. The ask: *"map the field of organoid cell-type annotation into camps, profile the key researchers, then actually benchmark one method per camp on a real dataset and recommend which we adopt; company context is in `/downloads`."* Output lived in `Downloads/annotation/` as a numbered set of `.md`s plus a runnable `bench/`.

- **Phase 0 — recon.** Read the human's own docs *first*. Surfaced that they already cited the field's reference atlas, already had two of the candidate tools in their stack, had already chosen their cell line, and treated batch/donor confounding as their product-killer. → every recommendation downstream was tailored to that, not generic. *(Output: nothing yet — but it set the frame for everything.)*
- **Phase 1 — reframe.** They framed it as "reference-genome build A vs B." The real axis was the reference *atlas* and what counts as ground truth for a developmentally-young cell. Said so up front. *(Output: `01_field_and_three_families.md`, opening "reframing your mental model" section.)*
- **Phase 2 — fan out + verify.** Two background research workflows (a broad web pass and a primary-source pass over PubMed/bioRxiv), structured output, adversarial verification that *killed* several over-confident claims (which became explicit "honesty notes"). *(Output: `02_researcher_profiles.md` — per-person family / first-principles / reference-frame / method / immaturity-stance / evolution / key-papers; `03_tradeoffs_and_tools.md` — tools-per-camp tables + decision tree; raw verified material persisted under `_research/`.)*
- **Phase 3 — ground.** Built a venv, installed the *real* tools for each camp, downloaded a real dataset shaped like the human's product (it even used their own cell line), ran one method per camp, computed metrics that made the camps' disagreement measurable. The abstract debate became a number: the naive reference mislabeled ~80% of cells as types that cannot exist in the sample; the camp-appropriate methods got it right. *(Output: `04_benchmark_report.md` + `bench/` — `scripts/` 01→06, `results/summary.md`, CSVs, and the headline figure.)*
- **Phase 4 — incremental / root-cause.** Got a conclusive core result before the stretch methods. Fixed bugs at the source (a workflow await-precedence bug, an output-parsing mismatch, OS-path and won't-build-on-this-platform issues) and *named* every workaround instead of hiding it. *(Output: the "install gotchas" and "what I could NOT do" sections.)*
- **Phase 5 — synthesize to a decision.** *(Output: `05_engram_recommendation.md` — the call ("layered, not one camp"), five first-principles reasons routed to the human's actual business, a concrete pipeline that drops into their existing stack, build-vs-buy, a validation plan, and a one-paragraph version for their colleagues.)*
- **Phase 6 — persist / parallelize.** Wrote the status file *first* so the human could read progress cold; ran research/installs/downloads in the background while writing the synthesis; saved a durable project memory. *(Output: `00_STATUS.md`, the durable folder, a memory entry.)*
- **Later — adversarial scrutiny on demand.** A sharp follow-up ("what about hippocampal annotations?") got the data re-opened, not the result defended: the suspect cluster turned out to be ~99% one perturbation + one donor and driven by genes that perturbation itself moves, so it was written up as a confound, not a finding. *(Output: `06_hippocampal_case_study.md`.)*

The reusable shape, stripped of the domain: **recon their world → reframe → fan out + kill weak claims → run the real thing on real data → decide, tied to their first principles → persist → stay skeptical of your own results.**

### The output anatomy (and why each piece earns its place)

The output is half the quality, and it's the most portable half. The deliverable is not one file — it's a **navigable set**: decision-first, evidence-deep, honest about its own bounds, reproducible. The principle behind the shape: *a busy human should get the answer in one page, be able to drill into the evidence, see exactly what was run, and trust it because the gaps are named.* The literal tree from the run (generalize the filenames to your domain; the **why** column is the transferable part):

```
README.md                          → the set's front door
  ├ "Read in this order" (1..N)        why: a set needs a path through it
  └ Executive summary (ONE page)       why: THE ANSWER before the evidence — map + headline numbers + the recommendation + caveats
00_STATUS.md                       → the cold-read / honesty file
  ├ ✅ DONE + where to start            why: a human reading cold knows it's finished and where to go
  ├ "What you asked for"               why: restate the ask so scope is auditable
  ├ live log (timestamped)             why: progress trace mid-run; provenance
  └ "What I could NOT do" + reproduce  why: honesty + a path to re-run
01_field_and_three_families.md     → the MAP (concepts)
  ├ §0 reframing your mental model      why: fix the human's framing FIRST — usually the highest-value move
  ├ §1 the families (one-line table)    why: the scannable spine
  ├ §2 first-principles disagreement    why: the real intellectual content ("why they differ")
  ├ §3 why the camps exist (lineage)    why: makes them memorable + predicts their behavior
  ├ §4 how each handles [the hard cases] why: operationalize the abstraction onto the human's actual problems
  └ §5 punchline for a data company     why: route the map to the human's decision
02_researcher_profiles.md          → the EVIDENCE (who backs the map)
  ├ per-entity: principle/ref/method/evolution   why: granular backing for the map
  ├ a "for [the human/company]" line each        why: tie every fact to the decision, not trivia
  └ honesty notes (what verification killed)     why: trust — show the kills, not just the wins
03_tradeoffs_and_tools.md          → the HOW (concrete software)
  ├ tools-by-camp tables               why: turn camps into installable things
  ├ install gotchas (tested)           why: hard-won, proves it was actually run, saves the next person hours
  └ tradeoff table + decision tree     why: actionable selection logic
04_benchmark_report.md             → the GROUNDING (the proof)
  ├ bottom line + dataset + methods-run  why: result in a para; provenance; what actually executed
  ├ headline metric table               why: the killer number that settles the debate
  ├ mechanism tables (per-class)        why: show WHY it fails, not just that it fails
  └ per-camp verdict + limitations      why: tie results back to the camps; bound the claims
05_[company]_recommendation.md        → the DECISION
  ├ TL;DR answer                        why: the call, up front
  ├ why, from first principles (their business)  why: justify in the human's own terms
  ├ pipeline + build-vs-buy + validation plan    why: actionable, drops into their stack
  ├ risks / caveats                     why: honesty
  └ one-paragraph version for their colleagues   why: the human must SELL this internally — hand them the words
06_hippocampal_case_study.md       → SCRUTINY on demand
  └ evidence → confound → conclusion    why: re-open the data on a sharp follow-up; don't defend the result
bench/                             → REPRODUCIBILITY
  ├ BENCHMARK_DESIGN.md                 why: pre-registered design = principled, not post-hoc
  ├ scripts/ 01..06 + common.py         why: the runnable pipeline
  ├ data/DATASET.md                     why: dataset provenance + why this one
  └ results/ (summary.md, CSVs, figs)   why: machine- and human-readable evidence
_research/                         → PROVENANCE
  └ raw verified profiles/tools/sources why: the audit trail behind the synthesis
```

Port the section *types*, not the filenames: **an exec-summary/TL;DR up front** (decision before evidence), **a reframe** (fix the framing), **a scannable table map**, **a first-principles "why" section**, **a "for-the-human" tie-back on every unit**, **a named "what I could not do" section**, **a one-paragraph version the human can forward to colleagues**, and **provenance** (raw research, dataset, design) so every claim is auditable. Numbered files (`00_`, `01_`…) so the set has an obvious reading order.

## Pairs with

- **`strategic-deliberation`** — its sibling. That skill decides *whether / what* (the bear-and-bull, reframe-from-the-human conversation); this one *goes and proves it on real data*. A high-stakes question often runs deliberation first, then this.
- **The repo's `claude.md` orchestration posture** — fan out with workflows, adversarial-verify, loop-until-dry, no silent fallback, explore/exploit. This skill is the concrete execution loop those principles describe.
- **`using-kimi-for-research`** -- Great tool for heavy research, especially that which requires great bookeeeping and determistic exploration (eg. 400 datasources to canvas -- use Claude workflow or Kimi Agent Swarm)
