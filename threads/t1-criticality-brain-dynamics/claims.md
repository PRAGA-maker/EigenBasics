# t1 — Criticality in brain dynamics: is it a well-posed target for generative extrapolation?

**Frame.**
- **Problem.** Chopra et al. claim one dynamical number, `d2`, forecasts learning rate across mouse, ferret, human and an RNN. Lee/Tiwary's expTM claims you can train a diffusion model far from a phase boundary and generate correct samples *at* it. The obvious move is to point expTM at brain criticality — you would get the causal manipulation Chopra et al. say they lack. Hardest constraint: expTM's physics is an *ensemble identification*, and the brain has no ensemble.
- **Why.** If it works, you can synthesise cortical population activity at a *chosen* distance from criticality and test the learning claim causally, without tuning a live animal.
- **Core question.** Does the brain-criticality setting have the structure expTM needs, and is `d2` a solid enough target to aim at?
- **Scope.** Read both papers to the equations; check the `d2` estimator numerically; test the structural mapping on a synthetic world with a known answer.
- **Out of scope.** Re-implementing and training expTM; wet-lab anything; deciding the criticality debate.

**Done =** every claim below carries a reproducible check in `experiments/`, and each is reported at the weakest strength the evidence supports.

---

## Claims

### C1 — `d2` is a monotone reparametrisation of the zero-frequency susceptibility
**Status: CONFIRMED (exact identity).** `d2 = |1 - Σφ|/√p = 1/(√p · H(1)) = σ_innov/(√p·√S(0))`, where `H(1)` is the AR filter's DC gain. `(1 - Σφ)` is exactly the coefficient an augmented Dickey–Fuller test puts a t-statistic on. Check: `experiments/check_d2.py::CHECK A`.
**Implication.** `d2` is principled — for a branching process it estimates `1-m` cleanly — but the paper's "no single statistic tracks the critical boundary" overstates. The zero-frequency susceptibility tracks it by construction. The paper concedes this in its Discussion and not in its Results.

### C2 — `d2` is distance to one face of the stability boundary, not distance to criticality
**Status: CONFIRMED (counterexample).** The stability region of an AR(p) has several faces; `Σφ=1` is the one with a root at `z=+1`. A system sitting *exactly* on the Hopf face (complex roots on the unit circle, `φ=(0,-1)`) is marginally stable with diverging susceptibility at `f = f_Nyq/2`, and scores `d2 = 1.414` — twice the white-noise value of `0.707`. Check: `experiments/check_d2.py::CHECK B`.
**Implication.** `d2` is distance to the zero-frequency, "ferromagnetic" critical manifold. Oscillatory near-instability — the standard picture of cortical rhythms and of seizure onset — reads as *maximally far from criticality*. The claim should be stated at that strength.

### C3 — The RNN model restates the vanishing-gradient problem, and does not isolate criticality
**Status: CONFIRMED (algebraic).** For AR(1), `d2 ≡ 1-µ` by the paper's own Eq. 4. Credit-assignment gain is `µ^k`. So `M ∝ (1-d2)^{-2k}` is `M ∝ µ^{-2k}` — "the intrinsic timescale sets the temporal credit-assignment horizon." True, load-bearing, and independent of whether any critical fixed point exists.
**Implication (weakest-not-shortest).** The data force the weak hypothesis — *long intrinsic timescale accelerates learning on delayed-credit tasks*. The paper reports the strong one — *proximity to an RG critical fixed point accounts for the capacity to learn*. The weak version survives the C2 counterexample and transfers to RNNs and to context-length work in LLMs; the strong one does neither. Prefer the weak one.

### C4 — Ensemble size and firing rate can manufacture the mouse effect's entire dynamic range
**Status: OPEN — unaddressed confound, not a refutation.** Holding the underlying dynamics *identical* (latent AR(1), `µ=0.9`, true `d2 = 0.0316`), the paper's estimator returns `0.140` at 15 units and `0.076` at 71 units; `0.185` at 1 Hz and `0.077` at 10 Hz. Poisson sampling noise whitens the population count and inflates `d2` monotonically in `1/(N·rate)`. Check: `experiments/check_d2b.py::C2`.
**Scale.** Artifact range 0.064 wide. Paper's between-animal range 0.111–0.176, i.e. 0.065 wide, from ensembles of 15–71 RSUs. The paper applies a hard `n>15` cutoff and no correction.
**What would settle it.** Report `d2` against unit count and mean rate across the 18 animals; re-estimate with every animal subsampled to a common `N` and rate-matched.

### C5 — The human `d2` is set by the preprocessing chain, not by cortex
**Status: OPEN — strong alternative explanation.** Pure white noise through the paper's exact human pipeline (500 Hz → 70–250 Hz Butterworth → Hilbert envelope → 100 ms Gaussian → z-score → AR(10)) returns `d2 = 2.3e-4`, the same order as the entire patient cohort (0.6–1.8e-4). AR(10) at 500 Hz reaches 20 ms of lag — wholly inside the 100 ms kernel, so the kernel sets the autocorrelation being fitted. Sweeping instrumental white noise from 0× to 8× signal RMS moves `d2` across 4.9e-5 → 2.4e-4, covering the whole patient axis. Check: `experiments/check_d2b.py::D2, D3`.
**Also.** Human `d2 ~ 1e-4` against mouse/ferret `d2 ~ 1e-1`. Three orders of magnitude. "Conserved from mouse to human" holds as a rank correlation, not as the same measured quantity.
**What would settle it.** Show `d2` is uncorrelated with a broadband noise-floor proxy (power above 250 Hz, impedance, amplifier era); repeat at 25/50/200 ms kernels and show the IQ effect is kernel-invariant.

### C6 — The specificity claim is not statistically established at n=13
**Status: CONFIRMED.** 95% CI on `d2`'s ρ² is [0.35, 0.92]; on Fano-200's is [0.00, 0.74]. They overlap. Williams' test for two dependent correlations sharing an outcome gives p = 0.06–0.15 across plausible `r(d2, Fano)`, reaching significance only at `r ≥ 0.9` — where the two are the same measurement and the specificity claim is vacuous anyway. Check: `experiments/check_d2.py::CHECK E`.
**Implication.** The pincer holds either way. Declining multiple-comparison correction is defensible for a negative prediction; "outperformed the best of these by more than 40 points of explained variance" is a claim about a *difference* and needs a test of that difference.

### C7 — expTM's exponential tilt is conjugate to a quantity that carries no criticality information in a rate-homeostatic system
**Status: CONFIRMED (synthetic, known answer).** expTM's whole physics content is `p(x) ∝ e^{-β x²/2} e^{βαx}` ⇒ `⟨x⟩ = α`, `⟨x²⟩ = β⁻¹`: the control variable is the *mean* of the prior over features, temperature is the *variance*. In an unregulated branching process that identification is clean — mean rate `= h/(1-m)` diverges at criticality, exactly as lattice-gas density is monotone in `µ`. Clamp the mean rate to 5.0 by homeostasis, sweep `m` 0.70 → 0.99: mean rate stays flat (4.96 → 4.66) while Fano goes 1.9 → 36 and `d2·√10` still tracks `1-m` (0.307 → 0.014). Check: `experiments/check_exptm_map.py::E1, E2`.
**Implication.** Firing-rate homeostasis is the premise of Chopra et al. Under it the order parameter has left the first moment entirely. Tilting the prior mean is orthogonal to criticality in exactly the regime of interest — you keep expTM's engineering and lose its physics.

### C8 — There is a feature space where the mapping is well posed, and it does not need a diffusion model
**Status: CONFIRMED (constructive).** Take `x = φ ∈ R^p`, the AR coefficients. The critical manifold is then the hyperplane `Σφ = 1`, `d2` is the distance of `⟨x⟩` from it, and a tilt `α` conjugate to `Σφ` is exactly a field conjugate to the order parameter — the same structure `µ` has in the lattice gas. Check: `experiments/check_exptm_map.py::E3`.
**Cost.** You are now modelling a 10-number summary. That is density estimation, not a problem that earns a score network.

### C9 — expTM cannot be set up on the Chopra dataset at all
**Status: CONFIRMED (by inspection).** expTM requires *labelled* control variables at ≥2 well-separated values — it trains at `(T=7, µ=-16)` and `(T=7, µ=0)`. Chopra et al. have no measured control variable: `d2` is a passive readout, and the paper says outright that it "does not specify the lower-level machinery that establishes the set-point."
**Where it could be set up.** Datasets carrying a graded, labelled knob: time-awake/sleep pressure (Hengen ref 23 — `d2` erodes across waking, restored by sleep); anaesthetic depth (the ferret prep already grades plane by spontaneous/evoked ratio and discards it as nuisance); pharmacological E/I manipulation; developmental age.

### C10 — expTM's accuracy fails precisely at the critical point
**Status: CONFIRMED (the authors' own result).** Their Fig 2(c): `Δρ < 0.05` everywhere "except in the immediate vicinity of `µc = -8`." No uncertainty quantification anywhere, and validation is against MC ground truth.
**Implication.** Use it to *localise* a boundary — the error blow-up is itself the signal. Do not use it to *generate near-critical samples*, which is what a brain-criticality application would want. And there is no MC ground truth for cortex, so the one validation route the paper uses is unavailable.

---

## Open questions (unexplored)

- **Q1.** Does expTM survive its own synthetic-first test on a *brain* model? Critical branching process, train at `m=0.7` and `m=1.3`, generate at `m=1.0`, look for `P(S) ~ S^{-3/2}`. Known answer, hours of work. If it fails here it will not work on cortex.
- **Q2.** Does the C4 confound actually explain the mouse effect, or merely permit it? Needs the per-animal unit counts, which are not in the preprint.
- **Q3.** `d2` is distance to the zero-frequency face. Is there a companion measure for distance to the Hopf face, and does *that* predict anything about learning? C2 says the current measure cannot see it.
