---
name: autometrics
description: >-
  Use when you need to turn a corpus of unstructured qualitative text (documents,
  transcripts, reviews, complaints, case files) into a small set of interpretable,
  quantitative, predictive features, and the document features that predict your
  outcome are unknown a priori — the "what characteristics predict outcome Y?"
  question, where you can't enumerate the columns because you don't yet know what
  to look for. Adapts AutoMetrics (Ryan et al. 2025, arXiv:2512.17267). Use
  extracting-from-media-corpus instead when the fields are already known.
---

# AutoMetrics — qualitative cause-finding, run as a Workflow

Induce **interpretable metrics that correlate with a sparse outcome signal, when you don't yet know which criteria matter.** The method paper built it to evaluate subjective AI-output quality from under 100 feedback points; the applied "Iterative Metric Induction" deck re-pointed it at a real prediction problem (what makes a regulatory comment get substantively engaged-with). Both shapes are the same as the general question this skill serves: *what characteristics of a document predict its outcome, when the predictive features aren't enumerable in advance?*

You are **not** evaluating an AI system. You re-use the engine for **qualitative cause-finding over a text corpus**: the dependent variable is a measurable outcome (a yes/no label, a score, a magnitude, a latency); the candidate "metrics" are *characteristics of the document* an LLM proposes and scores; the output is a short, ranked, human-readable list of operationalized features plus their measured association — i.e., candidate causes to then test rigorously with DiD / causal-forests.

## Two algorithms — know which one you're running

**(A) Paper version — PLS, one-shot (arXiv:2512.17267, §3):**
1. **Generate** candidate evaluators with an LLM (default ~10 single-criterion + ~5 rubric + 1 example-based + 1 prompt-optimized per run; each gets a "Metric Card").
2. **Retrieve** — augment with a bank of pre-built metrics, narrowed to top-k. *Usually vestigial for a fresh domain — see "What we keep / drop."*
3. **Regress** — z-score, fit **Partial Least Squares (PLS)** of the outcome on the metric matrix (PLS because high-p/low-n + collinear predictors break OLS), rank by first-component weight, keep top-n (n≈5), refit; drop wrong-sign generated metrics.
4. **Report** — surviving metrics, weights, correlations, cards.

**(B) Applied version — ElasticNet + residual loop ("Iterative Metric Induction," Algorithm 1). This is the variant to run by default.**
Inputs: dataset `D = {(x_i, y_i)}`, `y_i ∈ {0,1}` (or continuous); hyperparams `n` (examples per label fed back), `K_new` (max new metrics/iteration), `δ` (min meta-improvement). Loop:
- **Init (t=0):** split into `D_train` / `D_meta`. Prompt the LLM for `K0` initial metrics `M(0)`.
- **For t = 1,2,…:**
  1. **Fit + residuals:** score every metric on `D_train`; fit **ElasticNet** predicting `y`; compute residuals `r_i = y_i − f̂(x_i)`.
  2. **Mine high-residual examples:** for each label, take the top-`n` examples with the largest residual — the cases the current metrics get *most wrong*.
  3. **LLM proposes new metrics:** prompt the LLM with (i) the high-residual set and (ii) a summary of previously-proposed metrics; get `ΔM` new candidates.
  4. **Evaluate + sparsify:** refit ElasticNet on `M(t-1) ∪ ΔM`, allowing at most `K_new` nonzero coefficients among the new metrics; keep the nonzero ones → `M(t)`.
  5. **Meta-eval + stop:** compute meta-performance on `D_meta`. If it improved by `≥ δ`, reset the patience counter; else increment it. Stop on patience; return the metric set from the last improving iteration.

The residual loop is the upgrade: instead of one generation pass, it **targets the LLM's next proposals at exactly the cases the current feature set can't explain**, climbing toward the outcome's explainable ceiling. Use (B). Fall back to (A)'s PLS only if N is so small that ElasticNet won't stabilize and you need PLS's collinearity-robustness for a single pass.

## What the evidence actually supports (don't inherit the hype)

**Validity (paper §3.2, §4):** *criterion validity* = rank correlation (Kendall's τ) vs. a ground-truth rating; AutoMetrics beat LLM-judge / DnA-Eval / MetaMetrics / fine-tuned-BERT across all 5 reported tasks. *Construct validity* = **Sensitivity** (scores degraded outputs lower) and **Stability** (invariant to meaning-preserving edits). Roughly ~80 labels saturate; below that, variance dominates. On out-of-distribution low-resource tasks, "Generated-only" (skip the metric bank) can *beat* "Full" because pre-built metrics are noisy predictors that spuriously correlate.

**Applied-deck evidence (the realistic bar):** on real documents, iterative induction lifted Pearson r from ~0.13 to a **plateau around 0.33** over ~9 iterations. That is a *modest* correlation, and the deck is explicit that some of the signal is **inarticulable ("taste")** — the gap between the articulable metric set and a black-box model's correlation. Per-feature prompt length grew every iteration (metrics get more complex over time). Take the ceiling seriously: this method finds *candidate* drivers, not a high-R² predictor.

**Stated limitations (paper §6 + deck):**
- Metrics are **co-optimized with a particular LLM**; swapping the model at run time degrades them — reoptimize, don't swap.
- Generalizes only as far as the input data is representative.
- The **high-p / low-n spurious-correlation risk is real**; mitigated by sparsity + a significance warning, not eliminated.
- **Human oversight is essential** — experts must cull spuriously-correlated metrics the filter misses (the paper's headline practitioner lesson).
- The outcome label is **itself often noisy and confound-laden.** Define it carefully (see "Outcome definition is a first-class decision").

## When to use this (and when NOT to)

**Use it when:**
- The outcome is **measurable** (a yes/no flag, a score, a magnitude, a latency) **but the predictive document features are not enumerable a priori.** You can't write the columns because you don't yet know what to look for. This is the "unknown features" case.
- The evidence lives in **unstructured text** (documents, transcripts, reviews, complaints, comments, case files, support tickets).
- You want **interpretable candidate causes** to feed a real causal design.

**Do NOT use it when:**
- The fields are already known/enumerable → use **`extracting-from-media-corpus`** (consensus-ladder extraction of *specified* fields). AutoMetrics *discovers* the fields; that skill *measures known* fields at scale.
- You already have a clean causal hypothesis + design → go straight to DiD / causal-forests.
- N is tiny *and* the outcome is rare/lopsided (e.g. <~30 usable labeled docs with a near-degenerate outcome). The high-p/low-n warning bites hardest here; the regression will hallucinate signal. Prefer manual qualitative coding + adversarial verify, or expand N first.
- You'd report the regression coefficient **as a causal effect.** It is not.

## How it complements the rest of the toolkit

| Tool | Question | Relationship |
|---|---|---|
| **`extracting-from-media-corpus`** | "Extract these *known* fields reliably." | AutoMetrics **calls it** as its scoring primitive once a candidate feature is operationalized. Discovery → reliable measurement. |
| **AutoMetrics (this)** | "Which *unknown* document features associate with the outcome?" | Feature/cause **discovery + ranking** via the generate→fit→residual→loop engine. |
| **DiD / causal-lagging** | "Did a *program/rule change* cause an outcome change?" | AutoMetrics surfaces candidate treatment/outcome vars + covariates; DiD identifies the effect of a discrete change over time. |
| **Causal-forests** | "Heterogeneous causal effect of X on Y given covariates." | The surviving AutoMetrics shortlist becomes the **feature set / candidate treatment & moderators**. AutoMetrics ranks by *association*; the forest estimates *effects* + heterogeneity. |

Mental model: **AutoMetrics finds the variables; extracting-from-media-corpus measures them; DiD/causal-forests test whether they cause anything.**

## The loop, run as a Dynamic Workflow

Run as a **Workflow** (scout → parallel generators → score → fit/prune → residual-mine → adversarial verify → synthesis → loop-until-meta-plateau), with LLM **subagents** as the generators and per-document scorers. **This iterative-induction harness IS the method** — it is what discovers *unknown* features, so do not flatten it into a single fixed-field extraction pass (that flat pattern is for **`extracting-from-media-corpus`**, which measures *known* fields; autometrics *discovers* them). Dispatch one subagent per document for scoring and batch 50–100 in parallel. One robust efficiency that preserves the harness: extract rich read-once **fact sheets** first (include a `free_notes` field for emergent signals), then run the generate→score→fit→residual rounds over the fact sheets — and the regression itself can run in Python (local or in an analyst subagent). What you must keep is the **iterative residual-driven feature discovery**, never collapse it to one pass.

### 0. Frame (scout step)
- Pick **one outcome** with a clean, named definition and write it down as the dependent variable in your working notes (the system of record). The outcome must be (a) measurable, (b) defined from a specific source field or rule — not a vibe, and (c) genuinely *present* in your data.
- **Verify the field actually exists and is computable before you model it.** The most common quiet failure: a field that *looks* derivable but isn't. If you want a latency (`end_date − start_date`), confirm both dates are real and distinct across the corpus, not a populator artifact where one was backfilled from the other. If a date or label isn't in your data, it is **not derivable by wishing** — either extract it from the text, source it externally as an aggregate (and cite it as an aggregate), or drop that outcome. **Do not fabricate a field that doesn't exist**; "the schema looks like it supports this" is a hypothesis to check, not a fact.
- Assemble `(document_text, outcome)` pairs. Target the **smallest defensible labeled set ≥ ~30, aim ~80** (the paper's saturation point — treat it as a floor of hope, not a guarantee; validate N empirically with a learning curve). **Stratify so both outcome classes are present** — a starved minority class makes the regression hallucinate.
- Write down suspected **confounders** (time period, source/sub-corpus, size/magnitude covariates, represented-by-X) — needed both for causal ID later *and* to check that a surviving "feature" isn't just a proxy for one.

### 1. Generate candidate features (LLM, divergent)
Fan out **generator** subagents with deliberately different framings (e.g. "advocate for one side," "the adjudicator," "a skeptical economist") — *given this outcome and a sample of these documents, propose candidate characteristics of a document that might predict the outcome.* Mirror the paper's spread:
- **single-criterion** features (a boolean or count: `cites_X`, `mentions_prior_contact`, `is_insider`),
- **rubric** features (an ordinal score: `corroboration_strength_0_3`, `specificity_0_3`),
- **2–3 example-based** features grounded in hand-picked outcome-positive / outcome-negative exemplars.

Collect ~15–20 candidates, each with a one-line **Feature Card** (definition, why it might matter, how to score it, failure modes), saved to your working folder.

> **What we keep / drop vs. the paper.** Keep Generate, the (ElasticNet) Regress, Report, and the residual loop. **Drop the pre-built MetricBank/retrieval step** for a fresh domain — there is usually no bank of pre-built domain features to retrieve, and the paper shows "Generated-only" *wins* in the low-resource, OOD regime, which is where you'll be. This is a faithful use of the method's own finding. If a curated feature library accumulates across projects, reintroduce a retrieval step later.

### 2. Operationalize (each feature → a scoreable column)
For each candidate, write a **judge prompt** that scores one document on that single feature, returning a strict typed value (bool / 0–3 / float) + a one-sentence rationale + an evidence span. **Route every feature through `extracting-from-media-corpus`'s consensus ladder** (multi-sample / multi-model agreement) so each column is reliable, not a single noisy call. One column per feature.

### 3. Measure (build the matrix)
Score every labeled doc on every candidate → matrix `X` (docs × features) + outcome `y` → a CSV in your working folder. Hold out a `D_meta` split (or use k-fold) — **never tune on it.** z-score each column.

### 4. Fit + prune + residual-mine (the iterative core)
- Fit **ElasticNet** (`ElasticNetCV` for continuous `y`, or `LogisticRegression(penalty='elasticnet', solver='saga')` for binary `y`); it does **L1+L2** — the L1 part *is* the sparsity/pruning step (zeroes weak features), L2 handles collinearity. Keep nonzero-coefficient features.
- Compute residuals `r_i = y_i − ŷ_i`. **Mine the top-`n` highest-|residual| examples per class** — the cases the current features explain worst.
- Feed those high-residual documents back to the generators: *"these cases are mispredicted by the current features — what distinguishes them?"* Get `ΔM`, operationalize (step 2), rescore (step 3), refit.
- **Meta-eval + stop:** track meta-performance on `D_meta` (headline = **Kendall's τ**, the paper's conservative measure; also report Pearson r for comparability with the deck). Stop when improvement `< δ` for a patience window — **loop-until-plateau, not a fixed count.** Expect a ceiling (the deck plateaued around r≈0.33 by iteration 6–9).
- **Significance gate:** carry the paper's `p>0.05` warning. Any surviving feature whose association is not significant on `D_meta` is **"candidate, unconfirmed,"** never a finding.

> **PLS fallback:** if N is too small for ElasticNet to stabilize (coefficients swing wildly across folds), run the single-pass PLS variant instead: `PLSRegression(n_components=1)`, rank by `x_weights_[:,0]`, keep top-5, refit, drop wrong-sign generated features. Document which algorithm you used and why.

### 5. Report + adversarial verify
- Write a findings doc: ranked surviving features, ElasticNet weights, per-feature τ / odds-ratio + 95% CI, the held-out meta-performance curve, the Feature Cards, the **articulable-vs-inarticulable gap** (your metric-set correlation vs. a black-box baseline trained on raw text/embeddings — the deck's framing for "how much is taste"), and explicit confound caveats.
- **Adversarial verify:** spawn skeptic subagents to *refute* each surviving feature — argue it's (a) a **proxy for a known confounder** (time period, sub-corpus, magnitude), (b) a **leakage artifact** (the feature is downstream of the outcome), or (c) an **LLM-scoring artifact**. Kill any feature that fails a majority refutation vote.

**Leakage is the #1 failure mode and the check is mandatory.** The leakage line is subtle, and reading the document's *reasoning* is NOT itself leakage. A feature must capture information available *before* the outcome was determined. Recovering a **pre-outcome fact** from the document's factual recitation is fine even though it sits inside the text — e.g. "the document says the submission came after the deadline" makes *timeliness* a valid feature. The LEAK is using the **verdict / conclusion itself** (the holding, the decision category, or anything that only exists *because* the outcome already happened) as a feature — that just restates `y`. Distinguish *facts the document recites* (allowed) from *the document's own verdict* (forbidden). And note: for an obvious pattern ("denied because late"), you don't need autometrics at all — direct extraction suffices; autometrics earns its keep on the *unknown* features.

## Worked sketch (domain-agnostic)

**Question:** *Among customer support tickets, what characteristics of the ticket predict whether it escalated to a refund?* (Features unknown a priori → AutoMetrics.)

1. **Frame.** Binary `y = 1` if the ticket ended in a refund, else 0. Confirm "refund" is a real, dated field (not inferred). Confounders: product line, ticket month, customer tenure, agent. Assemble ~80 stratified tickets.
2. **Generate.** 3 generator subagents (angry-customer advocate, support-ops lead, skeptical economist) → ~18 candidate features (`names_specific_defect`, `cites_prior_ticket`, `emotional_intensity_0_3`, `mentions_competitor`, `requests_refund_explicitly`...). Cards → working folder.
3. **Operationalize.** One judge prompt per feature, routed through the consensus ladder, strict typed output + evidence span. **Leakage guard:** score "requests refund" from the *customer's opening message*, not from the resolution thread.
4. **Measure.** Stratified ~80-ticket matrix + `D_meta` split, z-scored.
5. **Iterate.** ElasticNet → nonzero features → residual-mine the worst-predicted refunds & non-refunds → regenerate → refit → stop at meta-τ plateau. Per-feature τ + 95% CI; `p>0.05` gate.
6. **Report/verify.** Findings doc + headline. Skeptics check leakage (`requests_refund_explicitly` is borderline — does it leak the outcome? It's a pre-outcome ask, so allowed, but flag it) and confounding (is `names_specific_defect` just a stand-in for product line?). Survivors become the candidate feature set for a causal-forest of refund probability, or a DiD around a policy-change date.

## Hard guardrails

- **Outputs go to a working/analysis folder, NEVER your canonical/production schema.** AutoMetrics features are exploratory artifacts; keep the source data canonical and minimal.
- **Association ≠ causation.** A surviving coefficient is a *candidate cause* to test with DiD / causal-forests. Never write a claim ("X drives outcome Y") on an AutoMetrics weight alone.
- **Leakage check is mandatory**, not optional. It is the single most common way this method produces a confident, useless answer.
- **Significance/`p>0.05` warnings travel with the number.** A low-significance recommendation is flagged, never laundered into a finding. A logged "weak/unconfirmed feature" is a TODO to expand N or refute, not a resolution.
- **Outcome definition is a first-class decision, not a default.** "The thing happened" vs. "the document discusses the thing" vs. "it happened on appeal" are different constructs. Pick one, define it from a named field/rule, and state which construct each finding speaks to.
- **Human oversight is in the loop by design.** Adversarial verify + a **manual review of the score matrix and a few scored documents** is required before any finding leaves the analysis — confirm the scores make sense; don't trust the regression because it ran.
- **Don't discard redacted/missing rows — two-sample design.** When a key field is heavily redacted/missing, run the analysis twice: (A) the **full sample with redaction/missingness as a (non-leaky) feature**, and (B) the **(biased) complete-case subsample**; compare to surface selection bias, and analyze *what gets redacted* as its own question. Caveat: a missingness flag that is outcome-determined is itself leakage — use it only when it isn't.
- **Quit only when the data GENUINELY doesn't exist — not when it's hard to reach.** A thousand documents is a grading job for batched subagents (an hour, not a human-year), not a reason to sample-and-stop; a field missing from the store may be extractable from text or available externally. Stop at *true absence*, and say so.
- **One claim ≠ one datapoint.** A single distributional fact is not convincing research — back each claim with multiple corroborating lines of evidence.
- **Reoptimize per model, don't swap.** Change the judge model → re-run the whole loop; surviving features and weights are model-conditioned.
- **Don't reintroduce an external metric library** unless a real curated domain-feature bank exists — generated-only wins in the low-n/OOD regime.

## Where the paper / deck claims look overstated

Flag these in your findings doc; do not inherit them as proven:
- **"~80 samples saturate"** is for *subjective text-quality* eval with continuous Likert outcomes. Many real problems are **binary and imbalanced** with long, heterogeneous documents. Validate N empirically with a learning curve on `D_meta` before trusting any shortlist.
- **The realistic correlation ceiling is modest** (deck plateaus near r≈0.33 and attributes the rest to "inarticulable / taste"). Don't expect a strong predictor; expect a *ranked list of candidate drivers* plus an honest articulable/inarticulable decomposition.
- **PLS / ElasticNet "handle" high-p/low-n** — they *mitigate* the blowup; they do **not** make spurious correlation vanish in a tiny, confounded corpus. Lean on held-out τ, the significance gate, and adversarial confound/leakage refutation — not the regression — to stay honest.
- **Criterion validity = correlation with a *reference standard*.** If your "outcome" is itself a human/agency *decision* (the very thing whose drivers you want), a feature may capture decision-maker behavior, not underlying merit. Be explicit about which construct it speaks to.
- The method is **promising but lightly externally validated** (no formal user study; the applied deck is an internal presentation). Your adversarial-verify + manual-review layer is doing real work, not ceremony.

## Minimal implementation pointers

- Regression (B): `sklearn.linear_model.ElasticNetCV` (continuous) or `LogisticRegression(penalty='elasticnet', solver='saga')` (binary); z-score with `StandardScaler`; keep nonzero-coefficient features; cap new features per iteration (`K_new`).
- Regression (fallback A): `sklearn.cross_decomposition.PLSRegression(n_components=1)`; rank by `x_weights_[:,0]`.
- Per-feature association: `scipy.stats.kendalltau` (headline, conservative) + Pearson r (deck comparability) + logistic OR / point-biserial w/ CI for binary.
- Articulable-vs-inarticulable gap: compare your metric-set correlation against a black-box baseline (e.g. logistic regression on text embeddings) on `D_meta`; the gap is the deck's "inarticulable / taste" residual — report it.
- Scoring: route every candidate through `extracting-from-media-corpus`'s consensus ladder; one subagent per document, batched 50–100.
- Persistence: working folder only — the matrix/scores in a `data/` subdir, plots in a `plt/` subdir, the analysis in a findings doc, and the headline + N/learning-curve check + meta-performance curve + any killed-by-refutation features summarized up top.
