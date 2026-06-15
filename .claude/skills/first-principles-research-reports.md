 ---
name: first-principles-research-reports
description: >-
  Use when you have a group of experiments to write up and the deliverable is a
  report that answers a real question — a program write-up, a thread synthesis, a
  decision-grade findings doc. Teaches two things that are one thing: reasoning
  from first principles (decompose the problem to irreducible axes, reason UP to
  beliefs, generate a question-space, recurse) and the report structure that flows
  from it (question → first-principles spine → datasets → design+intuition →
  results+figure → post-hoc story grouping → extracted principles), plus the
  honesty ledger and the figure-as-argument discipline. Use strategic-deliberation
  instead when the deliverable is a kill/keep decision in conversation, not a
  written report over results that already exist.
---

# First-principles research reports

This skill is for the moment the experiments are done and you have to turn a pile of runs into a write-up that someone makes a decision on. The pile is not the report. The report is an argument: it states a question, decomposes that question to the axes that actually govern the answer, shows that each experiment was *forced* by the previous answer, and re-derives the finding as a consequence of the decomposition rather than as a thing you happened to observe. When it works, the reader never re-reads a sentence, because every step is the natural consequence of the one before it.

The reasoning and the structure are one thing: **first-principles reasoning** generates the questions and entails the experiments, and **the report structure** is the trace that reasoning leaves on the page. If the reasoning is real, the structure writes itself; reach for the structure without the reasoning and you get section headers with no argument. Build the reasoning first.

The voice of the report itself is governed by `taste.md` — read it before you write a word the human will read. This skill governs the *shape* and the *method*; taste governs the prose.

## When to use

- Writing up a researchDetect program or thread once the experiments exist (`WRITEUP.md`, `FINDINGS.md`, a thread synthesis)
- A decision-grade report where someone will act on the verdict (invest in X / don't bootstrap Y / kill the direction)
- Any time you have ≥3 experiments that need to read as one story, not a chronological log
- When the framing prompt asks for "graphs that tell us whether this is possible" — the report exists to answer a specific quantitative question with a figure

## When not to use

- The decision is happening live in conversation and the experiments don't exist yet → `strategic-deliberation`
- A single experiment with a single number → just report it; the spine is overhead
- A literature scan with no experiments of your own → normal synthesis + `research-paper-pointers`
- An append-only `runlog.md` entry → that's a finding log, not a report; don't story-group it

## Do the experiments first, then write

The report is written on a *complete* result set, not alongside an open one. If two experiments are still running, finish them — run those as parallel workflows — and only then write. A write-up drafted over half-finished results bakes in a story the last experiment may refute, and you will have to tear it down. The recursion below tells you when you are actually done: you are done when the last answer leaves nothing open that the question demands.

---

## Part A — Reasoning from first principles

### What first principles is NOT

First principles is **not a list of beliefs.** A section that reads `Belief 0 / Q0 / Belief 1 / Q1` is the failure mode, just numbered. Listing things you believe — even true things, even numbered — is not reasoning; it's inventory. The tell: you could shuffle the bullets and lose nothing, because no bullet is *forced* by the one above it.

First principles is a generative procedure. You run it; you don't enumerate it.

### The procedure

1. **Name the axes that matter.** Take the problem space and ask: what are the irreducible dimensions along which the answer actually varies? Not the variables you happened to log — the ones the answer is a *function of*. For the virtual-cell write-up the axes were: (I) did you measure it vs. (II) do you generalize from a correlated prior; in-span vs. off-span signal; what is the response a learnable function of; and the scalar power-gates (data depth, context match). Each axis is a question the answer cannot dodge.

2. **Decompose each axis to something irreducible.** Push until you hit a quantity you can't usefully split further — and ideally one you can *plot*. "Does transfer degrade with biological difference" decomposes to "transfer as a function of neighbor radius (same gene → paralog family → pathway → disease module → random)." That's irreducible and it's an axis on a figure. If your decomposition bottoms out at something vague ("representation quality"), you haven't decomposed it yet.

3. **Reason UP to beliefs from the axes.** This is the inversion that matters. You don't start with a belief and look for support; you start with the axis + cited theory and *derive* what must be true. "Deep-linear theory says only off-span signal is unrecoverable by a linear baseline → therefore the shuffle gate is not hygiene, it is the *definition* of the quantity of interest." The belief is the output of the reasoning, not its premise. Every derived belief should make you able to say "this is forced *because*…".

4. **Generate a question/solution space.** The axes, reasoned over, spawn the questions worth asking and the candidate answers worth testing. The decomposition is a *generator*: it produces more questions than you'll run, and you pick the one whose answer most constrains the rest.

5. **Recurse.** Each answer closes one question and opens the next. Ask explicitly: *what did the last answer leave open?* That question is the next experiment — not a topic change, an entailment. Keep recursing until the question the report exists to answer is closed.

### The recursion is the backbone of the whole report

The chain of "answer → what it leaves open → next experiment" is not just how you plan the work; it is the spine the report is built on, told twice. Once as pure derivation (the first-principles spine, §A), once as instrumented experiments (the experiment chunks, §B). They must align — the same chain, the abstract version and the concrete version. That they align is itself a consistency check: if the derivation says experiment 4 was forced by experiment 3's answer, but in the chunks experiment 4 is sitting next to an unrelated run, one of the two is wrong.

The report closes the loop by **re-deriving the empirical finding from the first-principles spine at the end** — stating the law as clauses entailed by the axes ("what transfers: a tight protein complex, because it is one causal node; what does not: a disease module, because it is a phenotype label"), then "therefore the question resolves cleanly." The verdict is re-derived, not re-asserted.

### Worked instance of "reasoning up to a belief"

The strongest example from the source session, verbatim in spirit: instead of "I believe upstream signal generalizes better," the reasoning was — *our measurement is the transcriptome; in biology you'd model close to measurement (1–2 causal steps, low-D, linear) for cleanliness; but a foundation model has capacity, so the hypothesis is the opposite — model processes far upstream of the transcriptome, because they propagate across many causal paths in high-complexity ways there's more to learn from.* That is an axis (causal distance from measurement), reasoned over with theory (dimensionality, causal-path propagation), producing a testable belief, converted into an experiment that varies systems along the axis. Belief as *output*. (In that case the belief was refuted — near-readout tiers were richest — which is fine; the procedure is judged by whether the belief was *derived and tested*, not by whether it survived.)

---

## Part B — The report structure that flows from it

**Output contract.** Write the report to `<program>/WRITEUP.md` at the program root, with figures saved to `<program>/outputs/figures/` and referenced by that relative path so the embeds resolve from the repo. Maintain a companion `<program>/FINDINGS.md` as the honesty ledger — the same verdict in claim form, plus every superseded claim quoted verbatim under a banner (§D). The WRITEUP is the argument; FINDINGS is the durable claim-and-correction record.

The spine, in this exact order. This is the canonical ordering and it is not negotiable; what varies is depth per section, not sequence.

1. **The question.** The actual ask, stated sharp, usually quoting the README or the framing prompt. Not a topic — a question with a yes/no or a number attached.

2. **The first-principles spine.** The §A decomposition, written as a derivation: axes → reasoning → derived beliefs → the question-space → the recursion stated explicitly as "each question is forced by the previous answer's implication." This is the load-bearing section and the one most often faked. If it reads as a belief-list, it is wrong — rewrite it as one entailment chain.

3. **Datasets available (with provenance).** Not "which DB we used" — **why this DB over that named alternative**, what each source actually measured, and how well it matches the biological question. If you used dataset A, the reader will ask "why A over HNOCA?" — answer it in the text. When matched data runs thin, the move is to deep-research whether better-matched data exists (spawn a subagent), not to settle and stay quiet about it.

4. **Per experiment-chunk, loop this block:**
   - **Question** — the specific thing this experiment asks.
   - **First-principles** — why this is the right experiment, tied to the spine.
   - **Datasets** — what data, and the controls.
   - **Design** — including the leakage controls, the shuffle/null gate, and the reliability ceiling (e.g. Spearman-Brown half-sample). Every control must be derivable: you must be able to explain *why this is the right control* from first principles, or it isn't legitimate. (If asked "what is the shuffle and why do you do it," you should be able to derive it from the theory, not recite it.)
   - **What we wanted to show, intuitively** — the plain-language bet *before* the number.
   - **Results** — the number, CI-bounded, against the floor and the ceiling.
   - **Figure** — if one exists; introduced at the experiment that produced it.
   - **Analysis** — between chunks, what this chunk's result means and what it forces next.

5. **Post-hoc story grouping** (this is how the chunks are ordered — see below).

6. **Results and what they tell us** — the reconciled verdict, with full CI-bounded numbers.

7. **Extracted principles** — the domain-portable laws, each a short verdict earned by the body.

### Post-hoc story grouping

Experiments are presented **neither chronologically nor by infrastructure.** After the fact, regroup the runs into chunks where each chunk's result motivates the next: *"now that we know X, we want to know Y, so we did Z."* The grouping principle is *what-question-each-run-answered*, not what-dataset-it-used or when-it-ran — a single chunk can mix three datasets if they jointly answer one question.

Each chunk opens with a one-sentence causal transition that carries the prior result forward and motivates the move, and closes with a synthesis line that hands off to the next chunk ("this forces Q_n: …"). Done right, twelve runs over three weeks read as eight chunks of forced entailment, and the chronology is invisible. The opener is doing the work — if a chunk could open with "we also ran…", the grouping failed. (Note: the reference WRITEUP's own chunk labels are mis-numbered — the body text carries two "Chunk 7"s and the synthesis lines skip Q-numbers — so copy the *entailment ordering*, not the literal labels. The forced-entailment chain is what's exemplary; the numbering is a defect in the source.)

### The anchor experiment is trivial and clean

The first experiment is one trivial, super-clean design that answers the core question and proves the instrument before any null is trusted. Don't overcomplicate it. The extra axes — relatedness radius, region replication, causal distance — get added later, *as the story forces them*, never up front. Complexity earns its place by being entailed.

### Judge design against what the program is FOR

A technically-valid experiment that answers a mechanical proxy is bad design, full stop. "Does cheap linear work at all" is not the question if the bet is "can we calibrate a cheap head on a *frozen* foundation-model embedding using matched organoid data, vs. bootstrapping a bespoke FM." Code running is not the bar; answering the real bet is the bar. Before you write up an experiment, check it against the program's actual question — if it answers a proxy, it doesn't go in the story, or it goes in as a labeled detour.

---

## Part C — The figure is an argument

The best figure is the **minimal example that tells the story so obviously it is intuitive.** Finding it is worth deliberately spending real thinking budget on — think hard about the single figure that carries the whole claim, the way you'd think about a proof. The figure is the punchline made self-evident, not a data dump.

There is one **hero figure** the whole story converges on. It plots the entire claim's contrast on one axis — the positive lever *and* the negatives the report spends chunks refuting, all on the same plot against the same floor. The full-spectrum relatedness figure works because tight complexes sit high, family/pathway/disease modules sit on the random floor, and one glance carries "structural, not semantic." Embed it twice: once under the abstract as the thesis-in-one-image, once at the experiment that produced it.

Every other figure is subordinated to its claim and captioned with the *finding*, not the contents: "Causal-distance refuted: near-readout tiers are richest," not "Spearman by tier." A figure whose caption describes axes instead of stating a conclusion is decorative — cut it or recaption it. And a figure is allowed to admit its own limit in the caption ("n=2 regions is not a trend") — that's honesty, not weakness.

---

## Part D — The honesty ledger

Honesty discipline is non-negotiable and it cuts both ways.

- **Every headline number is CI-bounded and cross-checked against the on-disk source artifact.** If the artifact says +0.105 [+0.000, +0.210], the report does not say "~+0.25." Report the floor-relative, CI-bounded lift, not the shuffle-subtracted number that looks bigger. A number in the report that doesn't match the file it came from is a defect, not a rounding.
- **A suspiciously clean result is a flag, not a win.** If a result contradicts strong priors (embeddings should beat a tiny DB; a lift looks too good), re-run it cleanly — one workflow per config — *before* believing it. The reflex "this ought to be clean, so why isn't it / why is it too clean" is the reflex that catches the leak.
- **Frame effects by regime, not as universal wins.** When a lever holds only in deep/homogeneous data and collapses to null in power-limited data, say "power-gated and regime-conditional" and report the per-regime *pair*, not a single number. A headline that hides the regime it depends on is an overstatement.
- **Walk-backs stay in the record.** The report carries an explicit honesty ledger of corrections, each named and CI-bounded ("the asymmetric-gate fix," "the complex lever is power-gated"). The companion findings doc keeps the superseded claim quoted verbatim under a banner, so a reader sees the correction *and* what it corrected. You don't delete the wrong number; you demote it visibly.

**A logged degradation is a TODO, not a resolution.** "80% match rate," "N rows dropped," "fell back to the regex path" — writing it down is not handling it. If the report launders a degradation into "handled," that's a silent fallback in a hi-vis vest. Either fix it or state it as an open limitation with the number attached.

In working docs, label provenance: `[PRIMARY]` you read the source artifact, `[VERIFIED]` you cross-checked it, `[INFERENCE]` an explicitly-labeled deduction. These stay in the working notes, not the final deliverable — but they are the backbone of traceability, and they're how "principled inferences need to be made explicit" gets enforced.

### The verdict appears three times and they must agree

The verdict shows up in the **abstract** (asserted, with headline numbers), in the **spine** (derived from the axes — "therefore the question resolves cleanly"), and in the **closing** (reconciled, with full CIs). The abstract and the closing are deliberate mirrors — same bolded directives, the abstract with headline numbers, the closing with the full CI-bounded findings. All three must agree. If the derived verdict and the reconciled verdict disagree, you have a real inconsistency to resolve, not a wording choice. End the reconciliation pointing forward — name the single decisive open experiment — not just summarizing.

---

## The checklist

Run this before you call a report done. Any box you can't check is a symptom that the reasoning was faked somewhere upstream — stop and redo that section, don't paper over it.

- [ ] The question is stated sharp, with a yes/no or a number, quoting the framing prompt.
- [ ] The first-principles section is an entailment chain, not a belief-list. (Shuffle test: can you reorder the bullets without loss? If yes, it's inventory — rewrite.)
- [ ] Every derived belief can be stated as "forced *because*…".
- [ ] Dataset provenance answers "why this one over [named alternative]," not just "which one."
- [ ] The anchor experiment is trivial and clean and comes first.
- [ ] Each experiment is checked against the program's real question, not a mechanical proxy.
- [ ] Every control (shuffle/null, leakage, ceiling) is derivable from first principles.
- [ ] Chunks are grouped by question-answered and open with a causal "now that we know X…" transition.
- [ ] There is one hero figure; it shows the positive lever and the refuted negatives on one axis; captions state findings, not contents.
- [ ] Every headline number is CI-bounded and matches the on-disk artifact.
- [ ] Regime-conditional effects are reported as a per-regime pair, not a single number.
- [ ] The honesty ledger names every walk-back; superseded claims are demoted visibly, not deleted.
- [ ] The verdict in abstract, spine, and closing all agree.
- [ ] The closing re-derives the finding from the spine and names the next decisive experiment.

## Reach for this when

Someone hands you a directory of experiment outputs and says "write it up so we can decide." Read `taste.md`, finish any open experiments as parallel workflows first, build the first-principles spine before you touch the structure, then loop the per-chunk block and converge on the one hero figure that makes the whole story obvious.

## Composes with

- **`taste.md`** — read it before writing any prose a human will read; this skill is the shape, taste is the register.
- **`strategic-deliberation`** — the upstream sibling: it produces the kill/keep decision in conversation; this produces the written report once the experiments that decision spawned have run.
- **`research-paper-pointers`** — pull any theory paper the spine derives from (deep-linear, scaling-law) into `context/papers/` before you cite it in the first-principles section. Don't derive an axis from a summary.
- **The literature MCP sweep** (PubMed + bioRxiv + Consensus + WebSearch in parallel) — for the dataset-provenance section when you need to establish whether a better-matched DB exists.

## Worked example

The write-up this skill was extracted from — "Calibrate, Don't Bootstrap — A First-Principles Resolution of the Virtual-Cell Question" — is the reference artifact. Read it for the four macro-movements (Abstract → First-Principles Spine → The Experiments → Closing), the §4 recursion that runs the entailment chain as `→ result … Entailment → next experiment`, the eight post-hoc chunks each opened by an italic causal transition, the money figure embedded twice, and the closing honesty ledger that walks back the radius lift from "~+0.25" to "+0.105 [+0.000, +0.210]" with the lower bound touching zero. The companion `FINDINGS.md` shows the superseded-claim banner: the old overstated answer left quoted verbatim under the verdict that demoted it. That preserved walk-back — correction *and* what it corrected, both visible — is the move to copy. This may not exist on every machine -- company internal IP on company box. 
