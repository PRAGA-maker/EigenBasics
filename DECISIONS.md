# Decisions

Human decisions and agent status updates go here.

---

## 2026-08-26 — Agent status: t1 opened and answered

**Asked:** evaluate expTM (arXiv:2503.15080) for application to criticality as a brain-dynamics concept, with Chopra/Hengen et al. (bioRxiv 2026.07.09.737603) as the target domain. Both PDFs are now in `context/`.

**Answer:** `threads/t1-criticality-brain-dynamics/VERDICT.md`. Short form — no, not on this data and not in this form. expTM's tilt is conjugate to the prior *mean*; under firing-rate homeostasis the neural order parameter sits entirely in the autocovariance, so the tilt carries no criticality information. Three further gates fail independently (no labelled control variable in the Chopra dataset; expTM's accuracy collapses exactly at the critical point by the authors' own Fig. 2c; no ground truth for cortex).

**Also found, and worth a human decision:** two open confounds in the Chopra paper that the checks in `experiments/` reproduce.
- **C4** — ensemble size (15–71 RSUs) and firing rate move the `d2` estimator across the paper's entire between-animal range with the underlying dynamics held fixed.
- **C5** — pure white noise through their human sEEG pipeline lands in the same decade as every patient in the cohort; the 100 ms smoothing kernel sets the autocorrelation that AR(10) then fits.

Neither refutes the learning result. Both are first-order alternative explanations that the preprint does not address.

### Awaiting human decision
1. **Q1 — run the synthetic-first check?** Critical branching process, train an expTM-style tilted-prior diffusion at `m=0.7` and `m=1.3`, generate at `m=1.0`, look for `P(S) ~ S^{-3/2}`. Known answer, hours of work. This is the honest test of whether the method transfers at all, and it is cheap. Recommend yes.
2. **Spin off the two suggested threads?** Both are logged in `CROSS_THREAD_SYNTHESIS.md` — (a) "generative extrapolation needs a labelled knob" as a reusable screening filter for any train-far/generate-at-boundary method, (b) "distance to the Hopf face" as a companion measure `d2` is structurally blind to. (b) is the more interesting one.
3. **Contact the authors?** The C4 confound needs per-animal unit counts, which are not in the preprint. Hengen lab code is at github.com/hengenlab. Say the word and I'll draft.
