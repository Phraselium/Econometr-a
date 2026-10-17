import sys, numpy as np
sys.path.insert(0,'/home/user/Econometr-a')
from src.v16.montecarlo import cips_bootstrap as m, _comun_series as C
def sieve(Y, rng, B):
    dy=np.diff(Y,axis=1); dy=dy-dy.mean(1,keepdims=True)
    # AR(1) por unidad en las diferencias
    a=(dy[:,1:]*dy[:,:-1]).sum(1)/(dy[:,:-1]**2).sum(1)
    e=dy[:,1:]-a[:,None]*dy[:,:-1]; e=e-e.mean(1,keepdims=True)
    out=np.empty(B)
    for b in range(B):
        idx=rng.integers(0,e.shape[1],dy.shape[1])
        eb=e[:,idx]; d=np.zeros_like(dy); d[:,0]=dy[:,0]
        for t in range(1,dy.shape[1]): d[:,t]=a*d[:,t-1]+eb[:,t]
        out[b]=m.cips(np.concatenate([Y[:,:1],Y[:,:1]+np.cumsum(d,1)],1))
    return out
res={}
for k in range(120):
    rng=C.rng(77,k); Y=m.generar(rng); s=m.cips(Y)
    for L in (9,20,40):
        res.setdefault(f'L{L}',[]).append((s<np.quantile(m.cips_boot(Y,rng,149,L),.05), np.mean(m.cips_boot(Y,rng,20,L))))
    bs=sieve(Y,rng,149); res.setdefault('sieve',[]).append((s<np.quantile(bs,.05),bs.mean()))
    res.setdefault('cips',[]).append((s<-2.11,s))
for k,v in res.items(): print(k, np.mean([x[0] for x in v]), np.mean([x[1] for x in v]))
