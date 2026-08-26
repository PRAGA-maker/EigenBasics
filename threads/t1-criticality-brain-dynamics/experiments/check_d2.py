"""
Numerical checks on the d2 'distance to criticality' measure used in
Chopra/Zhong et al. (bioRxiv 2026.07.09.737603) -- Eq (2): d2 = |1 - sum(phi)| / sqrt(p)

CHECK A: what is d2, algebraically? (identity with zero-frequency gain / ADF statistic)
CHECK B: is d2 'distance to criticality', or distance to ONE face of the stability boundary?
CHECK C: does the estimator confound ensemble size / firing rate with 'criticality'?
CHECK D: what does the human high-gamma-envelope pipeline actually measure?
CHECK E: does the specificity claim ('d2 beats the next-best feature by 40 pts of R2') survive n=13?
"""
import numpy as np
from scipy import signal
from statsmodels.regression.linear_model import yule_walker

rng = np.random.default_rng(0)
d2_of = lambda phi: abs(1.0 - np.sum(phi)) / np.sqrt(len(phi))

print("="*78); print("CHECK A -- what d2 actually is"); print("="*78)
p = 10
for trial in range(3):
    # random stable AR(10) via random roots inside unit disk
    r = rng.uniform(0.2, 0.985, 5); th = rng.uniform(0.05, np.pi-0.05, 5)
    roots = np.concatenate([r*np.exp(1j*th), r*np.exp(-1j*th)])
    poly = np.real(np.poly(roots))          # z^10 - phi1 z^9 - ... => coeffs
    phi = -poly[1:]
    S = phi.sum()
    dc_gain = 1.0/(1.0-S)                    # H(z=1) of 1/(1 - sum phi z^-tau)
    # long-run variance / innovation variance from the true spectrum at f=0
    w, h = signal.freqz([1.0], np.r_[1.0, -phi], worN=[0.0])
    lrv_ratio = abs(h[0])**2                 # S(0)/sigma^2
    print(f" trial {trial}: sum(phi)={S:+.6f}  d2={d2_of(phi):.6f}  "
          f"1/(sqrt(p)*DCgain)={1/(np.sqrt(p)*dc_gain):+.6f}  "
          f"1/(sqrt(p)*sqrt(S(0)/sig2))={1/(np.sqrt(p)*np.sqrt(lrv_ratio)):.6f}")
print("  => d2 == 1/(sqrt(p) * DC gain) == sigma_innov / (sqrt(p) * sqrt(S(0))) exactly.")
print("  => d2 is a monotone reparametrisation of the ZERO-FREQUENCY susceptibility.")
print("  => (1 - sum(phi)) is exactly the coefficient tested by an augmented Dickey-Fuller")
print("     unit-root test:  dy_t = rho*y_{t-1} + sum(gamma_i dy_{t-i}) + e_t, rho = sum(phi)-1.")

print(); print("="*78); print("CHECK B -- d2 vs true distance to instability, AR(2) stability triangle"); print("="*78)
def spectral_radius(phi):
    return np.max(np.abs(np.roots(np.r_[1.0, -np.asarray(phi)])))
cases = {
 "white noise            (0.00, 0.00)": (0.0, 0.0),
 "near zero-freq unit rt (0.90, 0.09)": (0.90, 0.09),
 "near Nyquist unit root (-0.90,0.09)": (-0.90, 0.09),
 "near Hopf, theta=pi/2  (0.00,-0.99)": (0.0, -0.99),
 "near Hopf, theta=2pi/3 (-0.99,-0.99)": (-0.99, -0.99),
 "EXACT Hopf, theta=pi/2 (0.00,-1.00)": (0.0, -1.0),
}
print(f"  {'model':38s} {'d2':>8s} {'spec.radius':>12s} {'1-rho (true dist)':>18s}")
for k,(a,b) in cases.items():
    print(f"  {k:38s} {d2_of([a,b]):8.4f} {spectral_radius([a,b]):12.4f} {1-spectral_radius([a,b]):18.4f}")
print("  => white noise d2 = 1/sqrt(2) = 0.7071 for p=2.")
print("  => a system EXACTLY on the Hopf edge (marginally stable, diverging susceptibility")
print("     at f=Nyquist/2) scores d2 = 1.41, i.e. TWICE as 'far from criticality' as white noise.")
print("  => d2 measures distance to the sum(phi)=1 face ONLY (zero-frequency / 'ferromagnetic'")
print("     critical manifold). It is NOT distance to the bifurcation set.")

print(); print("="*78); print("CHECK C -- does ensemble size fake a d2 difference?"); print("="*78)
def latent_ar1_pop(mu_latent, n_neurons, rate_hz, dt=0.015, T=300.0, seed=0):
    """Common AR(1) latent drive (identical dynamics for every condition),
    N conditionally-Poisson neurons, population spike count in 15 ms bins."""
    g = np.random.default_rng(seed)
    nb = int(T/dt)
    x = np.zeros(nb)
    for t in range(1, nb):
        x[t] = mu_latent*x[t-1] + g.normal()
    x = x/np.std(x)
    lam = rate_hz*dt*np.exp(0.5*x - 0.125)          # per-neuron rate, modulated by the SAME latent
    return g.poisson(np.repeat(lam[:,None], n_neurons, axis=1)).sum(1).astype(float)

def d2_hat(y, order=10):
    y = y - y.mean()
    phi, _ = yule_walker(y, order=order, method="mle")
    return d2_of(phi)

MU = 0.90   # identical underlying dynamics in every row below
print(f"  latent AR(1) mu = {MU} (identical for every row); only N neurons / rate change")
print(f"  {'N neurons':>10s} {'rate Hz':>8s} {'d2_hat (mean+/-sd over 8 seeds)':>34s}")
for N in [15, 25, 34, 50, 71]:
    v = [d2_hat(latent_ar1_pop(MU, N, 5.0, seed=s)) for s in range(8)]
    print(f"  {N:10d} {5.0:8.1f} {np.mean(v):20.4f} +/- {np.std(v):.4f}")
for rate in [1.0, 2.5, 5.0, 10.0]:
    v = [d2_hat(latent_ar1_pop(MU, 34, rate, seed=s)) for s in range(8)]
    print(f"  {34:10d} {rate:8.1f} {np.mean(v):20.4f} +/- {np.std(v):.4f}")
print("  paper's reported between-animal range: 0.111 - 0.176 (between-animal SD = 0.015)")
print("  paper's reported per-animal ensemble sizes: 15 - 71 RSUs (mean 34)")

print(); print("="*78); print("CHECK D -- the human high-gamma-envelope pipeline"); print("="*78)
fs = 500.0
def human_pipeline(sig_in, fs=500.0, smooth_ms=100.0):
    b,a = signal.butter(4, [70/(fs/2), min(249.0,fs/2*0.998)/(fs/2)], btype="band")
    xb = signal.filtfilt(b,a,sig_in)
    env = np.abs(signal.hilbert(xb))
    n = int(round(6*smooth_ms/1000.0*fs)) | 1
    k = signal.windows.gaussian(n, std=smooth_ms/1000.0*fs); k/=k.sum()
    env = np.convolve(env, k, mode="same")[n:-n]
    env = (env-env.mean())/env.std()
    return d2_hat(env, order=10)
print("  NOTE: paper resamples to 500 Hz, band-passes 70-250 Hz, Hilbert envelope,")
print("        smooths with a 100 ms Gaussian, z-scores, then fits AR(10).")
print("        AR(10) at 500 Hz spans lags of only 20 ms -- far inside the 100 ms kernel.")
n = int(180*fs)
for label, gen in [("pure white noise", lambda s: np.random.default_rng(s).normal(size=n)),
                   ("1/f noise (pink)", None),
                   ("white + 5x amplitude", lambda s: 5*np.random.default_rng(s).normal(size=n))]:
    if gen is None:
        vals=[]
        for s in range(5):
            g=np.random.default_rng(s); w=g.normal(size=n)
            X=np.fft.rfft(w); f=np.fft.rfftfreq(n,1/fs); f[0]=f[1]
            vals.append(human_pipeline(np.fft.irfft(X/np.sqrt(f), n)))
    else:
        vals=[human_pipeline(gen(s)) for s in range(5)]
    print(f"  {label:24s} d2 = {np.mean(vals):.3e} +/- {np.std(vals):.1e}")
print("  paper's reported human d2 range (Fig 4C x-axis): 0.6e-4 to 1.8e-4")
print("  paper's mouse/ferret d2 range: 0.087 - 0.187  (~1000x larger)")

print(); print("="*78); print("CHECK E -- is the specificity claim statistically supported at n=13?"); print("="*78)
def fisher_ci(r, n, a=0.05):
    from scipy.stats import norm
    z=np.arctanh(r); se=1/np.sqrt(n-3); q=norm.ppf(1-a/2)
    return np.tanh(z-q*se), np.tanh(z+q*se)
r_d2   = -np.sqrt(0.74)   # reported rho^2 = 0.74
r_fano =  np.sqrt(0.34)   # reported next-best rho^2 = 0.34
n = 13
lo,hi = fisher_ci(abs(r_d2), n);   print(f"  d2       |rho|={abs(r_d2):.3f}  rho^2=0.74  95% CI on rho^2 = [{lo**2:.2f}, {hi**2:.2f}]")
lo2,hi2= fisher_ci(r_fano, n);     print(f"  Fano200  |rho|={r_fano:.3f}  rho^2=0.34  95% CI on rho^2 = [{lo2**2:.2f}, {hi2**2:.2f}]")
# Williams/Steiger test for two DEPENDENT correlations sharing the outcome, for a range of r_12
from scipy.stats import t as tdist
def williams(r_jk, r_jh, r_kh, n):
    R = 1 - r_jk**2 - r_jh**2 - r_kh**2 + 2*r_jk*r_jh*r_kh
    num = (r_jk-r_jh)*np.sqrt((n-1)*(1+r_kh))
    den = np.sqrt(2*(n-1)/(n-3)*R + ((r_jk+r_jh)**2/4)*(1-r_kh)**3)
    return num/den
print("  Williams test, H0: rho(d2,learning) == rho(Fano,learning), as a function of")
print("  how strongly d2 and Fano themselves correlate (r_kh):")
for r_kh in [0.0, 0.3, 0.5, 0.7, 0.9]:
    tt = williams(abs(r_d2), r_fano, r_kh, n)
    pp = 2*(1-tdist.cdf(abs(tt), n-3))
    print(f"    r(d2,Fano)={r_kh:.1f}  t={tt:5.2f}  p={pp:.3f}  {'DIFFERENT' if pp<0.05 else 'NOT distinguishable'}")
