---
name: weakest-not-shortest
description: >-
  Bennett's Razor — the hypothesis that generalises is the weakest, not the shortest.
  Invoke when choosing between competing explanations for a bug or a result, when deciding
  how general a fix or an abstraction should be, when designing an experiment or eval so its
  conclusion will transfer, when deciding how strongly to state a research claim, or whenever
  an argument leans on simplicity, compression, minimum description length, Ockham's Razor or
  "elegance" as evidence that something will generalise. Paper: Michael Timothy Bennett,
  arXiv:2301.12987, in `context/`.
---

# The weakest hypothesis, not the shortest

## What it's about

The paper challenges the long-held assumption — Ockham's Razor, formalised as the Minimum
Description Length principle — that shorter and simpler hypotheses generalise better. That is
the "compression = intelligence" idea, and it is load-bearing: it underlies Solomonoff
induction, Kolmogorov complexity, Chaitin's framing of compression as a proxy for intelligence,
and Hutter's AIXI. Bennett's observation is that the assumption had gone essentially
unchallenged, and his result is that it is wrong — not approximately right, but *neither
necessary nor sufficient*.

## Key claims

- **Compression is neither necessary nor sufficient** to maximise the probability that a
  hypothesis generalises to unseen tasks.
- The alternative proxy is **weakness** — the cardinality of a hypothesis's *extension*, meaning
  the set of decisions it still permits. The weaker, i.e. the less committal, a *valid*
  hypothesis is, the more likely it is to generalise.
- If tasks are uniformly distributed, **weakness maximisation is necessary and sufficient** for
  optimal generalisation: there is no choice of proxy that performs at least as well as weakness
  across all child/parent task pairs while performing strictly better on even one.
- The math is built on a **formalism of enactive cognition**: the environment is modelled as sets
  of declarative programs related to one another so as to form a lattice, and induction is
  formalised as tasks defined by situations, decisions and models. The unusual representation
  isn't decoration — it is what makes both weakness and description length well-defined on the
  same object.

## Experiments

Maximum weakness versus minimum description length on binary arithmetic — 8-bit string
prediction over addition and multiplication, with propositional logic as the vocabulary. Each
trial generates a parent task from every 4-bit input, samples a child task from it, computes
both a weakest model and an MDL model from the child, then tests both against the parent.

- **Rate of generalisation** (exact recovery of the parent): weakness at **1.1×–5×** MDL.
- **Extent** (fraction recovered when recovery was partial): weakness at 1.03×–1.56× MDL.
- The gap **widens with more data** rather than washing out — at 14 examples on binary addition,
  68% of weak models generalised against 24% of MDL models.

Bennett argues the same mechanism explains why DeepMind's Apperception Engine generalises so
effectively: it forms hypotheses only from universally quantified logical formulae, and
universally quantified statements are weak. What looked like a mysteriously good inductive bias
was weakness maximisation in disguise.

> **Bennett's Razor: explanations should be no more specific than necessary.**

**In short:** it is a theoretical AGI paper arguing that when choosing between hypotheses that
fit your data, you should pick the weakest, most permissive one, not the shortest one.

## Weakness is not simplicity

They come apart in both directions, and conflating them is the main way to misapply this.

"All things are blue crabs" is about as short a statement as you can make, and it rules out
nearly everything — it is maximally *strong*. A long, elaborate, heavily qualified utterance can
assert almost nothing and be very weak. Weakness is a consequence of extension, not of form.

The operative rule: **terseness is not evidence of generality, and neither is elegance.** A
clever one-liner that hardcodes the shape of the input you happened to see is short and strong —
exactly the wrong object. The instinct that compressed things are general is the instinct this
paper refutes.

## The scientist's version

This is the part that pays rent day to day. The live question in an experiment is rarely "is my
hypothesis true" — it is **"will this generalise,"** and over-strong priors are what stop it.

Every commitment a hypothesis makes beyond what the data forces is one more condition you have
to control, one more joint where it can break, and one more reason the result won't transfer to
the next system. That is why strong priors are *harder to work with*, quite separately from
being less likely to be right. Weak hypotheses are cheap to hold, cheap to test, and they
survive contact with the next dataset.

- **Ask what your conclusion still permits.** A result that holds only under the exact conditions
  you ran is a strong hypothesis: it explains your run and generalises to nothing. A result
  stated so that it still permits many configurations is the one worth having.
- **Design so the weakest sufficient hypothesis is what survives.** Vary the things your
  hypothesis doesn't mention — seed, scale, batch, dataset, cell line, whatever the claim is
  silent about. Whatever holds across that variation is the claim you have actually earned, and
  it will be the weak one.
- **Prefer the explanation that also accounts for what you weren't chasing.** Of the causes
  consistent with *every* observation, take the least specific. If your candidate explains only
  the effect you went looking for and none of the surrounding oddities, it is too strong — it
  has been fitted to the effect.
- **A mechanism requiring a precise coincidence is a red flag.** "Only when the cache is cold and
  the retry lands in the same millisecond" explains this trace and predicts nothing.
- **Report at the weakest strength the evidence supports** — weakest, but still *sufficient*.
  Over-conditioning ("holds for this model at this seed on this dataset") is a strong claim that
  generalises to nothing, and is as much a failure as overclaiming. If the mechanism is general,
  say so and name the check that shows it.
- **A patch keyed to the inputs that reproduced the bug** is the overfit wearing the clothes of a
  solution. Cheap test for the weakest sufficient fix: name an input you never observed that it
  still handles.
- **In eval and task design**, an item is itself a hypothesis about what it measures. An item
  admitting exactly one solution path is strong and measures the path; one admitting many is weak
  and measures the capability.

Three of this repo's standing rules are the same rule, and this is the proof under them:

- **Anti-overfit.** A tall tower on one borrowed analogy is the strongest, least likely
  hypothesis available. Breadth of cheap, independent, separately-falsifiable probes beats it for
  exactly the reason weak hypotheses beat short ones — each probe is silent about what the others
  test, so what survives all of them is weak.
- **"No is not no."** Killing a direction on one failed experiment is an over-specific inference
  from a single child task. The negative result licenses a much weaker conclusion than "this
  doesn't work," and the weaker one is usually the true one.
- **Frame first.** "Out of scope includes prescribing the answer before understanding the
  problem" is a weakness constraint: a frame that already names the answer has an extension of
  one.

Bennett's own reflexive note: he conjectures that language models fabricate and contradict
themselves *because* they are optimised only to minimise loss and never to maximise weakness,
and speculates that grokking might be inducible by optimising for weakness instead.

## The formalism, in one pass

Enough to reason with. Read the paper before leaning hard on it.

An **environment** is a set of states Φ, one of which is the present state. A **declarative
program** is a function `f: Φ → {true, false}`. A finite **vocabulary** `𝔳` of such programs
generates an **implementable language** `L_𝔳`, whose **statements** are the subsets of `𝔳` that
some state satisfies simultaneously.

The **extension** of a statement `a` is `Z_a = {b ∈ L_𝔳 : a ⊆ b}` — everything in the language
that contains it. This is the load-bearing definition, and it inverts the way length behaves:
assert more and fewer statements contain you, so your extension shrinks and you become
*stronger*; assert less and more of the language is consistent with you, so your extension grows
and you become *weaker*.

A **task** `α = ⟨S_α, D_α, M_α⟩` has situations `S_α`, correct decisions `D_α`, and models `M_α`
— the statements whose extension carves out exactly the correct decisions among the situations.
`α` is a **child** of `ω` when `S_α ⊆ S_ω` and `D_α ⊆ D_ω`. Generalisation is getting from child
to parent: you learn `h` from `α` and you want `h ∈ M_ω`.

Two proxies over models, both maps `L_𝔳 → ℕ` to be maximised: **weakness** `q(l) = |Z_l|`, and
**description length** `q(l) = 1/|l|`.

The three results:

- **Prop 1 (sufficiency).** For `h ∈ M_α` and `α ⊏ ω`, the probability that `h` also models `ω`
  is `2^{|Z̄_{S_α} ∩ Z_h|} / 2^{|Z̄_{S_α}|}`, maximised exactly when `|Z_h|` is maximised.
- **Prop 2 (necessity).** Generalisation is only possible when the extension is large enough to
  contain the parent's decisions, so you *must* use weakness or a function of it. Nothing else.
- **Prop 3.** Minimum description length is therefore neither necessary nor sufficient —
  delivered by explicit counterexample, not asymptotics, which is what makes it hard to wave
  away. A task is constructed whose models are `{z}` and `{j,k}`; description length picks `{z}`,
  weakness picks `{j,k}`. Minimising length did not maximise weakness, and vice versa.

One elegant sanity check in Remark 1: the same expression taken over the whole language rather
than a parent task is maximised at `h = ∅`. Given no information, the optimal hypothesis is to
assume nothing — you have no sequence to predict, so why make assertions the environment might
contradict?

## Where it does not apply

Say these out loud rather than using the razor as a general solvent.

- **The proof is conditional.** It assumes tasks are uniformly distributed and lives inside a
  specific formalism of enactive cognition over a *finite* vocabulary; Bennett flags both in
  footnotes. Another proxy can beat weakness on a cherry-picked child/parent pair. What is proved
  is that none beats it across the uniform distribution over all tasks.
- **Hypotheses, not every artifact.** Assertions, types, invariants, contracts and test oracles
  exist to *rule things out* and should be as strong as the truth allows. Weakening a test to
  make it pass is not this principle — it is the failure this principle is meant to catch, since
  what should be weak is the hypothesis under test, not the test.
- **Weak is not vague.** The razor selects the least specific hypothesis *that is still
  sufficient* — still a model of the task, still accounting for everything observed. Drop the
  sufficiency constraint and you get a hypothesis that permits everything and predicts nothing.

## The paper

`context/2301.12987_bennett_weakest-not-shortest.pdf` — Michael Timothy Bennett (ANU), *The
Optimal Choice of Hypothesis Is the Weakest, Not the Shortest*, arXiv:2301.12987v4, 11 April
2024. Ten pages,
one sitting: §2–4 formalism and the three proofs, §5 experiments, §6 the razor plus the remarks
on the Apperception Engine and neural networks. Appendices and experiment code are separate, at
`github.com/ViscousLemming/Technical-Appendices`.

Read the paper when a decision turns on it. This file is a summary, and summaries are the
over-specific artifact the paper is about.
