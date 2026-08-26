# Cross-Thread Synthesis

The most important document in this repo. Updated by the manager agent whenever findings in one thread have implications for another.

## Convergences

Findings from multiple threads pointing to the same conclusion.

### Criticality reduces to timescale
- **Threads:** t1
- **Finding:** Chopra/Hengen's `d2` and Lee/Tiwary's expTM were read against each other. Both collapse onto the same underlying quantity from opposite directions. `d2 = 1/(√p·H(1))` is exactly the zero-frequency susceptibility, and the paper's own RNN model reduces to `d2 ≡ 1-µ` with credit gain `µ^k` — the vanishing-gradient theorem with `µ` relabelled. What survives is *intrinsic timescale sets the temporal credit-assignment horizon*, not *the brain sits near an RG critical fixed point*.
- **Confidence:** high (algebraic identity + numerical check, `t1/experiments/check_d2.py`)
- **Implication:** Treat "criticality" claims in brain dynamics as timescale claims until something distinguishes them. Under Bennett's razor the weak version is the one to carry forward — it permits more, and it survives the Hopf counterexample (C2) that kills the strong reading.

<!-- Format:
### [Short name]
- **Threads:** t1, t3
- **Finding:** What converged and why it matters
- **Confidence:** high/medium/low
- **Implication:** What to do about it
-->

## Contradictions

Threads producing conflicting evidence. These are high-priority — resolve or explain.

<!-- Format:
### [Short name]
- **Threads:** t2 vs t4
- **Conflict:** What disagrees
- **Resolution status:** unresolved / resolved (explain how)
- **Next step:** What experiment or analysis would resolve this
-->

## Cross-Pollinations

A finding in one thread that opens a new direction in another (or suggests a new thread entirely).

### Generative extrapolation needs a labelled knob
- **Source:** t1 — expTM's tilt is conjugate to the prior *mean*; under firing-rate homeostasis the neural order parameter lives entirely in the autocovariance, so the tilt carries no criticality information (`t1/experiments/check_exptm_map.py`).
- **Target:** new thread suggested
- **Idea:** The general lesson generalises past criticality. Any "train far from the boundary, generate at it" method inherits the same precondition: the control variable must act on a low-order moment of whatever features you chose, and it must be *labelled* in the training data. That is a cheap screening test to run before adopting any such method — name the conjugate pair, or don't start. Worth its own thread as a reusable filter.
- **Status:** unexplored

### `d2` is blind to oscillatory criticality
- **Source:** t1 C2 — a system sitting exactly on a Hopf bifurcation scores `d2 = 1.41` against white noise's `0.707`, i.e. twice as far from criticality as noise.
- **Target:** new thread suggested
- **Idea:** The whole `d2` literature measures distance to the zero-frequency face of the AR stability region. Cortical rhythms and seizure onset are normally modelled as oscillatory near-instability, which this measure reads backwards. Is there a companion distance-to-Hopf measure, and does it predict anything about learning that `d2` misses? Cheap to build — it is the distance to a different face of the same polytope.
- **Status:** unexplored

<!-- Format:
### [Short name]
- **Source:** t2 finding X
- **Target:** t5 (or "new thread suggested")
- **Idea:** What the connection is and why it matters
- **Status:** explored / unexplored
-->

## Attention Dashboard

Snapshot of thread health. Manager agent updates this periodically.

| Thread | Status | Last runlog update | Runlog entries | Open claims | Notes |
|--------|--------|--------------------|----------------|-------------|-------|
| t1-criticality-brain-dynamics | active | 2026-08-26 | 10 | C4, C5 (both confounds in the Chopra data) | Verdict written. Two spin-off threads suggested above; Q1 (synthetic-first expTM on a branching process) is the cheap next move. |
