# expTM applied to brain criticality — verdict

**Question.** Lee/Tiwary's Exponentially Tilted Thermodynamic Maps (arXiv:2503.15080) trains a diffusion model far from a phase boundary and generates correct samples at it. Chopra/Hengen et al. (bioRxiv 2026.07.09.737603) say distance to criticality forecasts learning rate in three mammals, and say outright that they cannot manipulate it. Can the first fill the gap in the second?

**Verdict.** Not on this data and not in this form. The obstruction is structural, it is checkable in ten lines, and it survives every reframing I tried. But one narrow version is worth a cheap shot, and the reason it is narrow is the useful part.

---

## 1. The obstruction

expTM's entire physics content is a single identification:

    p(x) ∝ e^{-βx²/2} · e^{βαx}   ⇒   ⟨x⟩ = α ,  ⟨x²⟩ = β⁻¹

The control variable is the **mean** of the prior over features. Temperature is the **variance**. That is what lets it train at `µ = -16` and `µ = 0` and generate at `µ_c = -8` — lattice-gas density is the order parameter, and density is monotone in `µ`.

So the transfer question is not "does diffusion work on neural data." It is: **in the brain, is the criticality control parameter a mean-shift?**

Run it on the canonical brain-criticality model. A critical branching process, `A_t ~ Poisson(m·A_{t-1} + h)`, critical at `m = 1`:

| | m = 0.70 | 0.80 | 0.90 | 0.95 | 0.99 |
|---|---|---|---|---|---|
| **unregulated** — mean rate | 3.3 | 5.0 | 10.0 | 19.6 | 100.2 |
| **rate-clamped** — mean rate | 4.96 | 5.04 | 4.94 | 4.95 | 4.66 |
| **rate-clamped** — Fano | 1.9 | 2.8 | 4.9 | 10.0 | 36.2 |
| **rate-clamped** — `d2·√10` | 0.307 | 0.196 | 0.106 | 0.050 | 0.014 |

Unregulated, the mean rate is `h/(1-m)` and diverges at criticality — a clean structural match to the lattice gas. Clamp the rate by homeostasis and the mean goes flat while the system walks the whole way to the critical point. The order parameter has moved entirely into the autocovariance.

Firing-rate homeostasis is not an edge case here. It is the premise of the Chopra paper — the whole argument is that `d2` is a homeostatic set-point, like body temperature. Under that premise, **exponential tilting is conjugate to a quantity carrying no criticality information.** You keep expTM's engineering and lose its physics: what remains is a conditional diffusion model with an affine prior, and the "thermodynamically correct samples" guarantee goes with the ensemble.

Check: `experiments/check_exptm_map.py::E1, E2`.

## 2. Three more gates, any one of which is disqualifying on its own

**No labelled knob.** expTM trains at *known* control values. Chopra et al. measure `d2` passively and state that the machinery setting the set-point is unidentified. There is no `µ` to condition on. You cannot even assemble the training set.

**Wrong failure location.** Their Fig. 2(c): `Δρ < 0.05` everywhere *"except in the immediate vicinity of `µ_c = -8`."* For localising a boundary that is fine — the error blow-up is itself the signal. For generating near-critical activity to drive a learning model, it fails exactly where you need it.

**No ground truth.** Every validation in the paper is against MC or MD. Cortex has none, and expTM ships no uncertainty quantification, so a wrong answer arrives looking like a right one.

## 3. The repair, and why it eats itself

There *is* a feature space where the mapping is well posed. Take `x = φ ∈ R^p`, the AR coefficients themselves. Then the critical manifold is the hyperplane `Σφ = 1`, `d2` is the distance of `⟨x⟩` from it, and a tilt conjugate to `Σφ` is exactly a field conjugate to the order parameter — structurally identical to `µ` in the lattice gas. Numerically `Σφ̂` recovers `m` to within a few percent across the sweep.

The cost is that you are now modelling ten numbers. That is density estimation. It does not earn a score network.

## 4. The narrow version worth trying

Everything above says: applicability is gated on a **graded, labelled control variable** that is known to move a neural system along a criticality axis. Those datasets exist, and the best one is in Hengen's own lab.

- **Sleep pressure.** Their ref 23 already shows `d2` erodes across waking and is restored by sleep. Time-awake is a continuous, labelled, non-invasive knob, and the effect direction is published.
- **Anaesthetic depth.** The ferret prep already grades plane by spontaneous/evoked ratio — and discards it as a nuisance variable. That is a control parameter being thrown away.
- **Pharmacological E/I**, and **developmental age** (the kits are P31–34, right at eye-opening).

The experiment, mirroring the lattice-gas protocol exactly: train a tilted-prior diffusion on population activity at two well-separated values of the knob — say 1 h awake and 14 h awake — and generate at unobserved intermediate values. Known-answer test: does generated `d2` interpolate correctly against held-out recordings at those intermediate times?

What it buys is the thing the paper says it lacks: *"a direct demonstration that manipulating proximity to criticality alters learning rate in the brain remains untested."* You cannot tune a mouse's `d2`. You can generate population activity at a chosen `d2` and feed it to their learning model.

**Do the synthetic-first check before any of this.** Critical branching process, train expTM at `m = 0.7` and `m = 1.3`, generate at `m = 1.0`, look for `P(S) ~ S^{-3/2}`. Known answer, hours of work, and it is the same experiment as the lattice gas with a neural order parameter. If it fails there it will not work on cortex.

## 5. The target has its own problems

Before pointing anything expensive at `d2`, four things about it that the checks turned up. Details and code in `claims.md` C1–C6.

**It is the zero-frequency susceptibility.** `d2 = 1/(√p·H(1)) = σ_innov/(√p·√S(0))`, exactly, and `(1-Σφ)` is the coefficient an augmented Dickey–Fuller test puts a t-statistic on. That makes it a clean estimator of `1-m` for a branching process — a real virtue — but the Results' framing that no conventional statistic reconstructs it is stronger than the Discussion, which concedes the point.

**It is blind to oscillatory criticality.** `Σφ = 1` is one face of the AR stability region. A system sitting *exactly* on the Hopf face — complex roots on the unit circle, marginally stable, susceptibility diverging at nonzero frequency — scores `d2 = 1.41` against white noise's `0.707`. Twice as far from criticality as noise. Cortical rhythms and seizure onset are usually modelled as precisely that kind of near-instability. This is the most interesting loose thread in the thread.

**Ensemble size can manufacture the mouse result.** Hold the dynamics fixed (latent AR(1), `µ=0.9`, true `d2 = 0.0316`) and push it through the paper's own pipeline: 15 units gives `0.140`, 71 units gives `0.076`; 1 Hz gives `0.185`, 10 Hz gives `0.077`. The artifact range is 0.064 wide. The reported between-animal range is 0.065 wide, over ensembles of 15–71 RSUs. The estimator is unbiased on the clean latent — the measure is fine, the measurement is fragile, and the paper treats those as one problem. This does not refute the correlation. It means an uncontrolled nuisance has enough leverage to produce it.

**The human number is mostly the smoothing kernel.** Push white noise through their exact human chain — 500 Hz, 70–250 Hz Butterworth, Hilbert envelope, 100 ms Gaussian, z-score, AR(10) — and you get `d2 = 2.3e-4`. The entire patient cohort spans 0.6–1.8e-4. AR(10) at 500 Hz reaches 20 ms of lag, wholly inside the kernel that is setting the autocorrelation it fits. Varying instrumental noise alone from 0× to 8× signal RMS sweeps `d2` from 4.9e-5 to 2.4e-4, covering the whole patient axis. And human `d2 ~ 1e-4` against mouse `d2 ~ 1e-1` means the cross-species claim is a rank correlation, not one quantity measured three times.

## 6. What the Chopra paper actually establishes

Read at the weakest strength the evidence supports — which is also the reading that transfers:

> A durable, individually stable property of cortical population dynamics — best described as the intrinsic timescale — forecasts the *rate* of experience-dependent change, and specifically not its starting point and not its endpoint.

The dissociation is the strong part and it is genuinely well made: `d2` predicts learning rate but not naive first-trial performance (ρ² = 0.14, p = 0.23), not neophobia, not athleticism, not the asymptote (ρ = −0.29, p = 0.34). Their own model says why — `d2 ≡ 1-µ` for AR(1), credit gain is `µ^k`, so `M ∝ µ^{-2k}` with a loss floor independent of `d2`. That is the vanishing-gradient theorem, correctly derived, and it makes the empirical dissociation predicted rather than lucky.

But it is the vanishing-gradient theorem. `d2` enters only as a relabelling of `µ`, so any monotone reparametrisation gives the identical curve. The weak hypothesis — *long intrinsic timescale accelerates learning under delayed credit* — permits more, survives the Hopf counterexample that kills the strong reading, and transfers to RNNs and to LLM context-length work without committing to an RG fixed point. Bennett's razor says take that one.

The title says "a single dynamical property." That part is right. The property is a timescale.
