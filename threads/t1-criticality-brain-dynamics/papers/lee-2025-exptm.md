# Lee, Wang, Herron, Tiwary (2025) — *Exponentially Tilted Thermodynamic Maps (expTM)*

arXiv:2503.15080 · cond-mat.stat-mech · UMD · PDF in `context/`

## The claim in one line
Train a diffusion model on a handful of samples collected *far* from a phase boundary, then generate thermodynamically correct samples *at* it — including at temperatures, pressures and chemical potentials you never simulated.

## The mechanism
A diffusion model's forward process is an Ornstein–Uhlenbeck SDE relaxing to a Gaussian prior. The original Thermodynamic Maps (TM, their ref 18) noticed that if you assume a harmonic prior energy `E(x) = x²/2`, the canonical ensemble `p(x) ∝ e^{-βE(x)}` *is* a Gaussian whose variance is `β⁻¹`. So temperature is already sitting in the prior, and you can sample at any `β` by changing the prior's variance.

expTM extends this by tilting. Multiply the Gaussian prior by `e^{βαx}`:

    p(x) ∝ e^{-βx²/2} · e^{βαx}   ⇒   ⟨x⟩ = α ,  ⟨x²⟩ = β⁻¹

and the tilt parameter lands on ensembles with a linear conjugate term:
- **NPT**: `p(x) ∝ e^{-βE}e^{-λV}`, `λ = βP` ⇒ `α = -P`. Prior becomes `e^{-β(x+α)²/2}`.
- **µVT**: `p(x) ∝ e^{-βE}e^{λN}`, `λ = βµ` ⇒ `α = µ`. Prior becomes `e^{-β(x-α)²/2}`.

Mechanically the tilt is just an added drift in the OU process: `dx_t = -g(t)(x_t - α)dt + √(2g(t))dB_t`. Training runs in the joint space `(x, η)` with `η = {α, β⁻¹}`, so the score network sees the control variables directly.

## The demonstrations
- **Lattice gas, grand canonical.** 20×20 lattice, `x` = occupancy vector. Trained on **two** points only — `T=7`, `µ=-16` and `µ=0`, deliberately straddling the analytically known `µ_c = -8`. Generates across `µ ∈ [-20, 4]`, `T ∈ [1, 13]` and recovers the critical boundary. `Δρ < 0.05` **except in the immediate vicinity of `µ_c`**.
- **CO₂, isothermal-isobaric.** Phase I (cubic Pa3) ↔ Phase III (orthorhombic Cmca), boundary near 11.8 GPa. Trained on MD at 350 K and 1/3/5/8 GPa; recovers phase boundaries and intermediates.

## Assumptions this rests on, stated plainly
1. There *is* a Boltzmann ensemble, `p(x) ∝ e^{-βE(x)}`.
2. The control variable enters that ensemble through a **linear** conjugate term (`-λV`, `+λN`) — this is what makes the tilt a pure mean-shift.
3. A harmonic prior energy is an adequate stand-in.
4. Prior components factorise: each `x_i` fluctuates independently (their Eqs. 13, 16).
5. Training data carry **labelled** control values at ≥2 well-separated conditions.
6. Ground truth exists to validate against — MC or MD.

Assumptions 1, 2 and 4 are where the physics lives. Strip them and expTM is a conditional diffusion model with an affine prior: still useful engineering, no longer a statement about thermodynamics.

## Limits
- Error concentrates at the critical point — the authors' own Fig. 2(c). Good for *localising* a boundary, bad for *generating* near-critical samples.
- No uncertainty quantification.
- Validation is entirely against simulation ground truth.
- The strong extrapolation performance is powered by an inductive bias that happens to be exactly correct for a lattice gas. That is a feature there and a hazard anywhere the ensemble is unknown.

## Relation to brain criticality
See `claims.md` C7–C10. Short version: assumption 2 fails under firing-rate homeostasis, assumption 5 fails on the Chopra dataset, and the accuracy limit bites exactly where a brain application would need it.
