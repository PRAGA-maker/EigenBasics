# Chopra, Zhong et al. (2026) — *A single dynamical property can account for the capacity to learn*

bioRxiv 2026.07.09.737603 · Hengen (WashU) + Shew (Arkansas) + Van Hooser (Brandeis) · PDF in `context/`

## The claim in one line
Distance to criticality, measured once at baseline before any training, forecasts how fast a brain will learn — and nothing else about it.

## The measure
`d2`, from a renormalisation-group treatment of autoregressive models (their ref 40). Fit an AR(p) to a univariate time series, get `φ₁…φ_p`, and take the Euclidean distance from that point to the hyperplane of scale-invariant models:

    d2 = |1 - Σφ_τ| / √p ,  p = 10 throughout

Smaller = closer to criticality. White noise gives `1/√10 ≈ 0.32`.

Substrates: mouse M1 population spike counts in 15 ms bins, wake only, 5-min windows, Yule–Walker/MLE. Ferret V1 pooled multiunit, bin width `5 × mean ISI`. Human sEEG — AR fit to the *high-gamma envelope* (70–250 Hz, Hilbert, 100 ms Gaussian smoothing, z-scored) at 500 Hz, 180 s windows.

## What they found

| System | n | Effect |
|---|---|---|
| Mouse M1 → prey-capture learning rate (4-metric PC1) | 13 | ρ² = 0.74, p_perm = 0.0004 |
| Mouse M1 → early ladder learning (trot PC1) | 16 | ρ² = 0.61, p_perm = 0.0003 |
| Mouse M1 → late ladder speed refinement | 16 | ρ² = 0.31, p_perm = 0.027 |
| Ferret V1 → Δ direction selectivity | 14 kits / 33 blocks | r² = 0.54, LME β = −0.86 |
| Human frontal sEEG → full-scale IQ | 35 | partial r = −0.60, r² = 0.36 |

The dissociation is the good part, and it is the paper's strongest structural argument: `d2` predicts the *rate* of improvement but **not** naive first-trial performance (ρ² = 0.14, p = 0.23), **not** pre-trial neophobia, **not** athleticism, and **not** the asymptote (ρ = −0.29, p = 0.34). In machine-learning vocabulary it forecasts a learning rate, not an initialisation and not a converged loss.

Supporting results worth keeping: `d2` behaves like a trait (test–retest r = 0.83, ICC(1,k) = 0.94, though single-window ICC(1,1) is only 0.30); M1 and V1 set-points in the same animal share little variance (median ρ = 0.33), arguing for local rather than brain-wide regulation; animals closer to criticality pair a larger exploratory behavioural manifold with a tighter consolidated trot/walk core (`ALL/TW` ratio, r² = 0.55).

## The model
Reduce an RNN to its dominant real mode, `h_t = µ h_{t-1} + I_t` — an AR(1), for which their own Eq. 4 gives `d2 = 1 - µ`. Credit-assignment gain over `k` steps is `G(k) = µ^k = (1-d2)^k`. Gradient descent on a linear readout then needs

    M(d2, k) ∝ (1-d2)^{-2k}

trials to criterion, with a loss floor of zero *independent of `d2`*. That reproduces the empirical dissociation: `d2` sets the rate, not the endpoint, and the penalty compounds with the credit horizon `k`.

## What the authors themselves concede
- No causal manipulation of `d2` in a brain. Predictive across species, causal only inside the model.
- Human result is cross-sectional, in a paediatric epilepsy cohort (median FSIQ 77, range 40–127).
- Autocorrelation time, susceptibility, long-range temporal correlations and the branching ratio are all "not independent" of `d2`, and a panel of autocorrelation statistics also predicted learning across all three tasks.
- The lower-level machinery setting the set-point is unidentified.

## Where it is soft (see `claims.md` C1–C6 for the checks)
1. `d2 = 1/(√p·H(1))` exactly — it is the zero-frequency susceptibility reparametrised, and `(1-Σφ)` is the ADF unit-root coefficient. The Results overstate uniqueness relative to the Discussion.
2. It measures distance to the `Σφ=1` face only. A system *on* a Hopf bifurcation scores twice as far from criticality as white noise.
3. The RNN result is the vanishing-gradient theorem with `µ` relabelled. It supports "timescale sets the credit horizon", not "criticality" specifically.
4. Ensemble size (15–71 RSUs) and firing rate move the estimator across the entire observed between-animal range with the dynamics held fixed. Uncontrolled.
5. The human pipeline's 100 ms smoothing kernel sets the autocorrelation that AR(10) — reaching 20 ms at 500 Hz — then fits. White noise through the chain lands in the same decade as every patient.
6. n = 13. `d2`'s ρ² CI is [0.35, 0.92]; Fano-200's is [0.00, 0.74]. Williams' test cannot separate them.

## Read at the strength the evidence supports
A durable, individually-stable property of cortical population dynamics — well modelled as the intrinsic timescale — forecasts the rate of experience-dependent change, and specifically not its starting point or its endpoint. That is a real and interesting result. "Proximity to an RG critical fixed point accounts for the capacity to learn" is a strictly stronger reading that the same data do not force.
