"""
Does the structure expTM NEEDS exist in the brain-criticality setting?

expTM's whole content is an ensemble identification:
    p(x) ~ exp(-beta/2 * x^2) * exp(beta*alpha*x)   =>   <x> = alpha,  <x^2> = 1/beta
i.e. the CONTROL VARIABLE (mu or -P) enters as the MEAN of the prior over features x,
and temperature enters as the VARIANCE.  That is what lets it train at two mu far from
mu_c and generate at mu_c.

So the transfer question is exactly:  in neural data, is the criticality control parameter
a MEAN-SHIFT in the feature space?
"""
import numpy as np
from statsmodels.regression.linear_model import yule_walker
d2_of = lambda phi: abs(1-np.sum(phi))/np.sqrt(len(phi))
def d2_hat(y,order=10):
    y=np.asarray(y,float); y=y-y.mean()
    phi,_=yule_walker(y,order=order,method="mle"); return d2_of(phi)

def branching(m, h, T=40000, seed=0):
    """critical branching process: A_t ~ Poisson(m*A_{t-1} + h). Critical at m=1."""
    g=np.random.default_rng(seed); A=np.zeros(T); A[0]=h/max(1e-9,(1-m))
    for t in range(1,T):
        A[t]=g.poisson(max(0.0, m*A[t-1]+h))
    return A

print("="*80)
print("E1 -- UNREGULATED branching process: is the control parameter a mean-shift?")
print("="*80)
print(f"  {'m (branching ratio)':>20s} {'1-m (true dist)':>16s} {'mean rate':>11s} {'d2_hat*sqrt(10)':>17s}")
for m in [0.70,0.80,0.90,0.95,0.99]:
    A=branching(m, h=1.0, seed=1)
    print(f"  {m:20.3f} {1-m:16.3f} {A.mean():11.2f} {d2_hat(A)*np.sqrt(10):17.4f}")
print("  => YES here: mean rate = h/(1-m) diverges as m->1. Mean IS the order parameter,")
print("     exactly as lattice-gas density is monotone in mu. d2*sqrt(10) recovers 1-m well.")

print()
print("="*80)
print("E2 -- HOMEOSTATICALLY REGULATED rate (what the brain actually does)")
print("="*80)
print("  Same process, but external drive h is set so that mean rate is CLAMPED to 5.0")
print("  (firing-rate homeostasis -- the central premise of the Hengen paper).")
print(f"  {'m':>8s} {'h required':>12s} {'mean rate':>11s} {'var/mean (Fano)':>17s} {'d2_hat*sqrt(10)':>17s}")
TARGET=5.0
for m in [0.70,0.80,0.90,0.95,0.99]:
    h=TARGET*(1-m)                      # exact homeostatic setpoint
    A=branching(m,h=h,seed=1)
    print(f"  {m:8.3f} {h:12.3f} {A.mean():11.3f} {A.var()/A.mean():17.3f} {d2_hat(A)*np.sqrt(10):17.4f}")
print("  => Mean rate is FLAT across the entire approach to criticality, while d2 still")
print("     tracks 1-m. The control parameter has moved entirely out of the first moment")
print("     and into the AUTOCOVARIANCE.")
print()
print("  CONSEQUENCE for expTM: its exponential tilt exp(beta*alpha*x) shifts <x>. Under")
print("  rate homeostasis the tilt is conjugate to a quantity that carries NO criticality")
print("  information. The added machinery of expTM over plain conditional diffusion is")
print("  orthogonal to the order parameter in exactly the regime of interest.")

print()
print("="*80)
print("E3 -- the repair: pick features where criticality IS a mean-shift")
print("="*80)
print("  Take the feature vector to be the AR coefficients themselves, x = phi in R^10.")
print("  The critical manifold is then the HYPERPLANE sum(phi)=1 and d2 is the distance")
print("  of <x> from it. A tilt alpha conjugate to sum(phi) is then exactly a field")
print("  conjugate to the order parameter -- the same structure as mu in the lattice gas.")
print(f"  {'m':>8s} {'sum(phi_hat)':>14s} {'d2 from <phi>':>16s}")
for m in [0.70,0.80,0.90,0.95,0.99]:
    h=TARGET*(1-m); A=branching(m,h=h,seed=1); A=A-A.mean()
    phi,_=yule_walker(A,order=10,method="mle")
    print(f"  {m:8.3f} {phi.sum():14.4f} {d2_of(phi):16.4f}")
print("  => in THIS feature space the control parameter is a clean mean-shift, and an")
print("     expTM-style tilted prior is structurally well posed. Cost: you have thrown")
print("     away the generative model of the activity itself and are now only modelling")
print("     a 10-number summary -- which is a density-estimation problem, not one that")
print("     needs a diffusion model.")
