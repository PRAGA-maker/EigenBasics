# t1 runlog — append-only

Format: claim → check → verdict.

---

## 2026-08-26 — Thread opened

**Input.** Two papers handed over together:
- Chopra, Zhong, Miller, Tolossa, Fosque, Janzen-Meza, DeKorver, Guerriero, Ritter, Lambo, Bhaskaran-Nair, Van Hooser, Shew, Hengen (2026). *A single dynamical property can account for the capacity to learn, from artificial networks to the mammalian brain.* bioRxiv 2026.07.09.737603. → `context/2026.07.09.737603_chopra_d2-learning.pdf`, synthesis in `papers/`.
- Lee, Wang, Herron, Tiwary (2025). *Exponentially Tilted Thermodynamic Maps (expTM).* arXiv:2503.15080. → `context/2503.15080_lee_exptm.pdf`, synthesis in `papers/`.

**Question posed.** Evaluate expTM for application to criticality as a brain-dynamics concept, with Chopra et al. supplying the target domain.

---

### Entry 1 — What is `d2`, exactly?
- **Claim (C1).** The paper presents `d2` as a *direct* measure of distance to criticality that no conventional statistic reconstructs.
- **Check.** `experiments/check_d2.py::CHECK A`. Sample random stable AR(10) processes by drawing roots inside the unit disc; compare `d2 = |1-Σφ|/√p` against the filter's DC gain `H(1)` and against `σ_innov/√S(0)`.
- **Result.** Identity to floating-point on every trial: `d2 = 1/(√p·H(1)) = σ_innov/(√p·√S(0))`. Separately, `(1-Σφ)` is the augmented Dickey–Fuller unit-root coefficient by inspection of the ADF regression.
- **Verdict.** CONFIRMED, and it cuts both ways. `d2` is a clean estimator of `1-m` for a branching process — that is a genuine virtue. But it *is* the zero-frequency susceptibility in different clothes, so the uniqueness framing in the Results is stronger than the Discussion, which concedes the point.

### Entry 2 — Distance to criticality, or distance to one face?
- **Claim (C2).** `d2` measures how far a system sits from criticality.
- **Check.** `experiments/check_d2.py::CHECK B`. Evaluate `d2` and the true spectral radius across the AR(2) stability triangle, including points on each face.
- **Result.** `φ=(0,-1)` — complex roots exactly on the unit circle at `θ=π/2`, i.e. a system sitting *on* a Hopf bifurcation — gives spectral radius 1.000 and `d2 = 1.414`. White noise gives `d2 = 0.707`. A marginally-stable oscillator therefore scores as twice as far from criticality as noise.
- **Verdict.** CONFIRMED. `d2` is distance to the `Σφ=1` face only. Restate the claim at that strength: distance to a zero-frequency critical manifold. Flagging as a tangent worth a look — Q3.

### Entry 3 — Is the RNN model evidence for criticality?
- **Claim (C3).** The minimal recurrent model "establishes causality" for criticality → learning rate.
- **Check.** Read the derivation line by line (Methods, Eqs. 3–8). For AR(1) the paper defines `d2 = 1-µ` (their Eq. 4); credit gain is `µ^k` (Eq. 5); trials-to-criterion is `M ∝ (1-d2)^{-2k}` (Eq. 8).
- **Result.** Substituting the definition back, `M ∝ µ^{-2k}`. The model says the intrinsic timescale sets the temporal credit-assignment horizon. That is the vanishing-gradient result, correctly derived and genuinely load-bearing — but `d2` enters only as a relabelling of `µ`, so any monotone reparametrisation gives the identical curve.
- **Verdict.** CONFIRMED. Under Bennett's razor the surviving hypothesis is the weak one — long intrinsic timescale accelerates learning under delayed credit. It permits more, it survives Entry 2's counterexample, and it transfers to RNNs and to LLM context-length work without committing to an RG fixed point. Report at that strength.

### Entry 4 — Does the estimator confound sampling with dynamics?
- **Claim (C4).** Between-animal differences in `d2` reflect between-animal differences in dynamics.
- **Check.** `experiments/check_d2b.py::C2`. Drive `N` conditionally-Poisson neurons from one shared latent AR(1) (`µ=0.9`, true `d2=0.0316`), bin at 15 ms, fit AR(10) by Yule–Walker exactly as the paper does. Sweep `N` over the paper's actual range and sweep rate.
- **Result.** Noiseless latent recovers `0.0312 ± 0.0008` — the estimator is unbiased on clean data. Through the spike-counting pipeline: `N=15 → 0.140`, `N=71 → 0.076`; `1 Hz → 0.185`, `10 Hz → 0.077`. Monotone in `1/(N·rate)`.
- **Verdict.** OPEN, and this is the most actionable criticism in the thread. Artifact range 0.064 wide against an observed between-animal range 0.065 wide, over ensembles the paper reports as 15–71 RSUs. It does not refute the learning correlation — it means an uncontrolled nuisance has enough leverage to produce it. Needs `d2` vs unit-count reported, and a rate- and `N`-matched re-estimate.

### Entry 5 — What does the human pipeline measure?
- **Claim (C5).** Frontal `d2` from sEEG indexes the same quantity as `d2` from mouse spikes.
- **Check.** `experiments/check_d2b.py::D2, D3`. Reimplement the human chain (resample 500 Hz → 70–250 Hz 4th-order Butterworth → Hilbert envelope → 100 ms Gaussian → z-score → AR(10) Yule–Walker) and push white noise, pink noise, and a synthetic signal with a genuine 1 s envelope correlation through it at varying instrumental SNR.
- **Result.** White noise → `2.3e-4`. Pink noise → `2.2e-4`. Reported patient cohort → 0.6–1.8e-4. Sweeping added instrumental noise 0×→8× signal RMS moves `d2` across 4.9e-5 → 2.4e-4, spanning the whole patient axis. Kernel sweep: unsmoothed white noise gives `1.2e-1`, at 100 ms it gives `2.3e-4` — the kernel moves `d2` by three orders of magnitude, and AR(10) at 500 Hz reaches only 20 ms of lag, entirely inside it.
- **Verdict.** OPEN, strong alternative explanation. The measurement is dominated by the smoothing kernel, and patient-to-patient spread sits inside the band that recording SNR alone sweeps. Separately: human `d2 ~ 1e-4` vs mouse/ferret `d2 ~ 1e-1` means the cross-species claim is a rank correlation, not one quantity measured three times.

### Entry 6 — Is `d2` distinguishable from its competitors at n=13?
- **Claim (C6).** `d2` is the only baseline feature that predicts learning, beating the next best by 40 points of explained variance.
- **Check.** `experiments/check_d2.py::CHECK E`. Fisher-z CIs on the reported ρ², and Williams' test for two dependent correlations sharing an outcome, swept over plausible `r(d2, Fano-200)`.
- **Result.** `d2` ρ² CI [0.35, 0.92]; Fano-200 ρ² CI [0.00, 0.74]. Overlapping. Williams p = 0.125 / 0.150 / 0.119 / 0.055 at `r = 0.0 / 0.3 / 0.5 / 0.7`, and p < 0.001 only at `r = 0.9`.
- **Verdict.** CONFIRMED as a pincer. Either the two features are near-identical — in which case singling out `d2` is vacuous — or the difference in predictive power is not resolvable at this n. The permutation nulls the paper reports establish that `d2` beats *chance*; they do not establish that it beats *Fano*.

### Entry 7 — Does the brain-criticality setting have the structure expTM needs?
- **Claim (C7).** expTM's tilted prior transfers to neural data.
- **Check.** `experiments/check_exptm_map.py::E1, E2`. expTM's content is `⟨x⟩ = α` (control variable → prior mean), `⟨x²⟩ = β⁻¹` (temperature → prior variance). Test whether the criticality control parameter is a mean-shift, in a critical branching process, with and without firing-rate homeostasis.
- **Result.** Unregulated: mean rate `= h/(1-m)` runs 3.3 → 100 as `m` goes 0.70 → 0.99, so the mean *is* the order parameter — a clean structural match to lattice-gas density in `µ`. Rate-clamped at 5.0: mean rate 4.96 → 4.66 (flat) while Fano goes 1.9 → 36 and `d2·√10` tracks `1-m` across 0.307 → 0.014.
- **Verdict.** CONFIRMED, and this is the thread's central finding. Homeostasis is the premise of the Chopra paper. Under it the order parameter has left the first moment entirely, so exponential tilting — a mean shift — is conjugate to a quantity carrying no criticality information. expTM's machinery transfers; its physics does not. What survives is a conditional diffusion model with an affine prior, and the "thermodynamically correct samples" guarantee is gone with the ensemble.

### Entry 8 — Is there a repair?
- **Claim (C8).** No feature space rescues the mapping.
- **Check.** `experiments/check_exptm_map.py::E3`. Set `x = φ ∈ R^p`, the AR coefficients themselves, and re-ask whether the control parameter is a mean-shift.
- **Result.** It is, cleanly: `Σφ̂` recovers 0.693 / 0.804 / 0.894 / 0.950 / 0.987 for `m` = 0.70 / 0.80 / 0.90 / 0.95 / 0.99. The critical manifold is the hyperplane `Σφ=1` and `d2` is the distance of `⟨x⟩` from it, so a tilt conjugate to `Σφ` is a field conjugate to the order parameter — structurally identical to `µ` in the lattice gas.
- **Verdict.** CONFIRMED but self-limiting. In that space you are modelling ten numbers. That is density estimation; it does not earn a score network. Negative result, not a dead end — the useful content is that the *conjugate pair* exists once you name the right features.

### Entry 9 — Could expTM be pointed at the Chopra data as it stands?
- **Claim (C9).** Yes.
- **Check.** Read expTM's training protocol against Chopra's dataset description.
- **Result.** No. expTM trains at *labelled* control values — `(T=7, µ=-16)` and `(T=7, µ=0)`. Chopra et al. measure `d2` passively and state that the machinery setting the set-point is unidentified. There is no `µ` to condition on.
- **Verdict.** CONFIRMED. Applicability is gated on a graded, labelled knob. Candidates that already exist: time-awake/sleep pressure (Hengen ref 23), anaesthetic depth (already graded and discarded as nuisance in the ferret prep), pharmacological E/I, developmental age.

### Entry 10 — Where does expTM break on its own terms?
- **Claim (C10).** expTM is accurate near phase boundaries.
- **Check.** Read their Fig. 2(c) and Results text.
- **Result.** `Δρ < 0.05` across the whole `(T, µ)` grid "except in the immediate vicinity of `µc = -8`." No uncertainty quantification. Validation is against MC ground truth throughout.
- **Verdict.** CONFIRMED, from the authors' own figure. Fine for *localising* a boundary — the error blow-up is the signal. Fatal for *generating near-critical samples*, which is the thing a brain-criticality application would actually want. And cortex has no MC ground truth, so their only validation route is unavailable.

---

### Surprises and tangents (flagged)

- **The Hopf blind spot (Entry 2)** is the most interesting thing here and nobody in the criticality literature seems to be pricing it. `d2` cannot see oscillatory near-instability at all. Cortical rhythms and seizure onset are usually modelled as exactly that. → Q3.
- **The estimator is unbiased on clean data and badly biased through the spike-count pipeline (Entry 4).** The measure is fine; the measurement is fragile. Those are different problems and the paper treats them as one.
- **Chopra et al.'s own weakest point is a strength for the expTM idea.** They say plainly that a direct manipulation of `d2` remains untested. That is precisely the gap a generative extrapolator would fill — which is why the negative structural result in Entry 7 matters rather than being a technicality.
