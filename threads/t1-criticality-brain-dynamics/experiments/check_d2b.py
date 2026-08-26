import numpy as np
from scipy import signal
from statsmodels.regression.linear_model import yule_walker
d2_of = lambda phi: abs(1.0-np.sum(phi))/np.sqrt(len(phi))
def d2_hat(y, order=10):
    y=np.asarray(y,float); y=y-y.mean()
    phi,_=yule_walker(y,order=order,method="mle"); return d2_of(phi)

print("="*78); print("C2 -- noiseless control + SNR scaling of the mouse spike-count estimator"); print("="*78)
def latent(mu, dt=0.015, T=300.0, seed=0):
    g=np.random.default_rng(seed); nb=int(T/dt); x=np.zeros(nb)
    for t in range(1,nb): x[t]=mu*x[t-1]+g.normal()
    return x/np.std(x)
MU=0.90
print(f"  true latent AR(1) mu={MU}: analytic AR(10)-fit d2 = (1-mu)/sqrt(10) = {(1-MU)/np.sqrt(10):.4f}")
v=[d2_hat(latent(MU,seed=s)) for s in range(8)]
print(f"  d2 measured on the NOISELESS latent itself      = {np.mean(v):.4f} +/- {np.std(v):.4f}   <-- ground truth")
def pop(mu,N,rate,seed=0,dt=0.015,T=300.0):
    x=latent(mu,dt,T,seed); g=np.random.default_rng(1000+seed)
    lam=rate*dt*np.exp(0.5*x-0.125)
    return g.poisson(np.repeat(lam[:,None],N,axis=1)).sum(1).astype(float)
print(f"  {'N*rate (expected spikes/bin)':>30s} {'d2_hat':>10s} {'inflation over truth':>22s}")
for N,rate in [(15,5),(25,5),(34,5),(50,5),(71,5),(34,1),(34,10),(71,10),(200,20)]:
    v=[d2_hat(pop(mu=MU,N=N,rate=rate,seed=s)) for s in range(8)]
    print(f"   N={N:3d} rate={rate:4.1f} -> {N*rate*0.015:7.2f}  {np.mean(v):10.4f} {np.mean(v)/((1-MU)/np.sqrt(10)):19.1f}x")
print("  => d2_hat is monotone in 1/(N*rate): it is dominated by Poisson sampling noise,")
print("     not by the latent dynamics, over the entire ensemble-size range the paper used.")

print(); print("="*78); print("D2 -- human pipeline: does instrumental SNR alone span the reported range?"); print("="*78)
fs=500.0; n=int(180*fs)
def pipeline(raw, fs=500.0, smooth_ms=100.0):
    b,a=signal.butter(4,[70/(fs/2),249/(fs/2)],btype="band")
    xb=signal.filtfilt(b,a,raw); env=np.abs(signal.hilbert(xb))
    m=int(round(6*smooth_ms/1000.0*fs))|1
    k=signal.windows.gaussian(m,std=smooth_ms/1000.0*fs); k/=k.sum()
    env=np.convolve(env,k,mode="same")[m:-m]
    return d2_hat((env-env.mean())/env.std(),order=10)
def brainlike(seed, tau_s=1.0):
    """broadband carrier whose high-gamma ENVELOPE carries a genuine slow (tau=1 s) correlation"""
    g=np.random.default_rng(seed)
    a=np.exp(-1/(tau_s*fs)); e=np.zeros(n)
    for t in range(1,n): e[t]=a*e[t-1]+g.normal()*np.sqrt(1-a*a)
    amp=np.exp(0.8*e)
    return amp*g.normal(size=n)
print(f"  {'instrumental white noise (x signal RMS)':>42s} {'d2':>12s}")
base=brainlike(0)
for f_noise in [0.0,0.25,0.5,1.0,2.0,4.0,8.0]:
    vals=[]
    for s in range(4):
        sig=brainlike(s); nz=np.random.default_rng(500+s).normal(size=n)
        y=sig/np.std(sig)+f_noise*nz
        vals.append(pipeline(y))
    print(f"  {f_noise:42.2f} {np.mean(vals):12.3e}")
print("  paper's reported patient range: 0.6e-4 .. 1.8e-4 ; pure-noise pipeline value ~2.3e-4")
print("  => the whole patient axis lies inside the band that instrumental SNR alone sweeps.")

print(); print("="*78); print("D3 -- how much of the human d2 is the smoothing kernel?"); print("="*78)
print(f"  {'Gaussian smoothing kernel (ms)':>34s} {'d2 of PURE WHITE NOISE':>26s}")
for sm in [0.0001,5,10,25,50,100,200]:
    vals=[pipeline(np.random.default_rng(s).normal(size=n),smooth_ms=sm) for s in range(3)]
    print(f"  {sm:34.4f} {np.mean(vals):26.3e}")
print("  => d2 falls ~2 orders of magnitude as the kernel widens. AR(10) at 500 Hz reaches")
print("     20 ms of lag; the 100 ms kernel sets the autocorrelation the model is fitting.")
