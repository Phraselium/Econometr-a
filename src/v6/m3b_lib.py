"""M3b: utilidades (modelos, líneas base, DM-HLN, ALE, DL). Sin red; un hilo; SEED=20261010."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.tree import DecisionTreeRegressor

SEED = 20261010


# ------------------------------------------------------------------ DM con corrección HLN
def dm_hln(l1, l2, h: int = 1) -> dict:
    """DM (pérdida cuadrática ya agregada por periodo: l = MSE_t). d = l1 - l2; estadístico < 0 => modelo 1 mejor.
    Varianza de largo plazo Bartlett con h-1 retardos; corrección HLN; t(n-1)."""
    d = np.asarray(l1, float) - np.asarray(l2, float)
    n = len(d)
    dc = d - d.mean()
    lrv = dc @ dc / n
    for k in range(1, h):
        lrv += 2 * (1 - k / h) * (dc[k:] @ dc[:-k]) / n
    if lrv <= 0:
        return {"DM": np.nan, "p": np.nan, "n": n}
    dm = d.mean() / np.sqrt(lrv / n)
    st = dm * np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    return {"DM": float(st), "p": float(2 * stats.t.sf(abs(st), n - 1)), "n": n}


def bh(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 1.0
    for rank, i in zip(range(m, 0, -1), o[::-1]):
        run = min(run, p[i] * m / rank)
        adj[i] = run
    return adj


# ------------------------------------------------------------------ líneas base (FE agrupado, como M1b)
def fe_baseline(trn: pd.DataFrame, val: pd.DataFrame, xs: list[str], tgt: str, y1: str = "y1") -> np.ndarray:
    """Pendientes comunes e intercepto por unidad (idéntico a M1b oos). Devuelve nivel predicho de y."""
    A = trn[xs + [tgt]].to_numpy(float)
    u = pd.factorize(trn.unit)[0]
    Mt = A - pd.DataFrame(A).groupby(u).transform("mean").to_numpy()
    b = np.linalg.lstsq(Mt[:, :-1], Mt[:, -1], rcond=None)[0]
    mu = trn.groupby("unit")[xs + [tgt]].mean()
    a_i = mu[tgt] - mu[xs].to_numpy() @ b
    pr = val.unit.map(a_i).to_numpy() + val[xs].to_numpy(float) @ b
    return pr + val[y1].to_numpy() if tgt == "dy" else pr


# ------------------------------------------------------------------ BART sustituto: bosque con bootstrap bayesiano
class BBF:
    """Sustituto declarado de BART: promedio de B árboles poco profundos, cada uno ajustado con pesos de bootstrap
    bayesiano (Dirichlet(1)); la dispersión entre árboles da una banda tipo posterior. NO es BART (sin prior sobre
    la estructura ni backfitting)."""

    def __init__(self, n_trees=100, max_depth=3, min_samples_leaf=5, max_features=0.7, seed=SEED):
        self.n_trees, self.max_depth, self.min_samples_leaf, self.max_features, self.seed = n_trees, max_depth, min_samples_leaf, max_features, seed

    def fit(self, X, y):
        X = np.asarray(X, float)
        rng = np.random.default_rng(self.seed)
        n = len(y)
        self.trees_ = []
        for b in range(self.n_trees):
            w = rng.dirichlet(np.ones(n)) * n
            t = DecisionTreeRegressor(max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf,
                                      max_features=self.max_features, random_state=self.seed + b)
            self.trees_.append(t.fit(X, y, sample_weight=w))
        return self

    def predict(self, X, return_std=False):
        P = np.column_stack([t.predict(np.asarray(X, float)) for t in self.trees_])
        return (P.mean(1), P.std(1)) if return_std else P.mean(1)


# ------------------------------------------------------------------ ALE y PDP 1D
def ale_1d(predict, X: pd.DataFrame, col: str, K: int = 10):
    x = X[col].to_numpy(float)
    ok = ~np.isnan(x)
    edges = np.unique(np.quantile(x[ok], np.linspace(0, 1, K + 1)))
    if len(edges) < 3:
        return None
    idx = np.clip(np.searchsorted(edges, x, side="right") - 1, 0, len(edges) - 2)
    eff, cnt = [], []
    for k in range(len(edges) - 1):
        m = ok & (idx == k)
        if not m.any():
            eff.append(0.0)
            cnt.append(0)
            continue
        lo, hi = X[m].copy(), X[m].copy()
        lo[col], hi[col] = edges[k], edges[k + 1]
        eff.append(float(np.mean(predict(hi) - predict(lo))))
        cnt.append(int(m.sum()))
    cnt = np.array(cnt)
    ale = np.concatenate([[0.0], np.cumsum(eff)])
    mid = (ale[:-1] + ale[1:]) / 2
    ale = ale - (mid * cnt).sum() / cnt.sum()
    return pd.DataFrame({"x": edges, "ale": ale})


def pdp_1d(predict, X: pd.DataFrame, col: str, n: int = 20):
    g = np.unique(np.quantile(X[col].dropna(), np.linspace(0.02, 0.98, n)))
    out = []
    for v in g:
        Z = X.copy()
        Z[col] = v
        out.append(float(np.mean(predict(Z))))
    return pd.DataFrame({"x": g, "pdp": out})


# ------------------------------------------------------------------ deep learning (torch, un hilo)
def _torch():
    import torch
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    return torch


class Tab:
    """MLP tabular sobre delta de ln precio."""

    def __init__(self, hidden=64, dropout=0.1, wd=1e-3, lr=3e-3, epochs=150, seed=SEED, n_seeds=1):
        self.p = dict(hidden=hidden, dropout=dropout, wd=wd, lr=lr, epochs=epochs)
        self.seed, self.n_seeds = seed, n_seeds

    def _prep(self, X):
        X = np.asarray(X, float)
        X = np.where(np.isnan(X), self.med_, X)
        return (X - self.mu_) / self.sd_

    def fit(self, X, y):
        torch = _torch()
        X = np.asarray(X, float)
        self.med_ = np.nan_to_num(np.nanmedian(X, 0))
        Xf = np.where(np.isnan(X), self.med_, X)
        self.mu_, self.sd_ = Xf.mean(0), Xf.std(0) + 1e-9
        self.ys_ = float(np.std(y) + 1e-9)
        Xt = torch.tensor(self._prep(X), dtype=torch.float32)
        yt = torch.tensor(np.asarray(y) / self.ys_, dtype=torch.float32)[:, None]
        self.nets_ = []
        for s in range(self.n_seeds):
            torch.manual_seed(self.seed + s)
            net = torch.nn.Sequential(torch.nn.Linear(Xt.shape[1], self.p["hidden"]), torch.nn.ReLU(), torch.nn.Dropout(self.p["dropout"]),
                                      torch.nn.Linear(self.p["hidden"], self.p["hidden"]), torch.nn.ReLU(), torch.nn.Linear(self.p["hidden"], 1))
            opt = torch.optim.AdamW(net.parameters(), lr=self.p["lr"], weight_decay=self.p["wd"])
            for _ in range(self.p["epochs"]):
                net.train()
                opt.zero_grad()
                torch.nn.functional.mse_loss(net(Xt), yt).backward()
                opt.step()
            self.nets_.append(net.eval())
        return self

    def predict(self, X):
        torch = _torch()
        Xt = torch.tensor(self._prep(X), dtype=torch.float32)
        with torch.no_grad():
            return np.mean([n(Xt).numpy().ravel() for n in self.nets_], 0) * self.ys_


def knn_adj(coords: np.ndarray, k: int = 5) -> np.ndarray:
    d = ((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d, np.inf)
    A = np.zeros_like(d)
    for i in range(len(d)):
        A[i, np.argsort(d[i])[:k]] = 1
    A = np.maximum(A, A.T) + np.eye(len(d))
    dg = A.sum(1)
    return A / np.sqrt(dg[:, None] * dg[None, :])


class GCN:
    """Red de grafos espacial (grafo k-vecinos por centroides). Una capa propia + una capa con agregación de vecinos.
    Entrada: tensor [T, N, F] con máscara de nodos observados; pérdida solo en nodos de entrenamiento."""

    def __init__(self, A, hidden=32, dropout=0.1, wd=1e-3, lr=3e-3, epochs=150, seed=SEED):
        self.A = A
        self.p = dict(hidden=hidden, dropout=dropout, wd=wd, lr=lr, epochs=epochs)
        self.seed = seed

    def _net(self, F):
        torch = _torch()
        h = self.p["hidden"]

        class Net(torch.nn.Module):
            def __init__(s, A):
                super().__init__()
                s.register_buffer("A", torch.tensor(A, dtype=torch.float32))
                s.l0 = torch.nn.Linear(F, h)
                s.l1 = torch.nn.Linear(2 * h, h)
                s.out = torch.nn.Linear(h, 1)
                s.dr = torch.nn.Dropout(self.p["dropout"])

            def forward(s, X):  # X [T,N,F]
                z = torch.relu(s.l0(X))
                z = torch.relu(s.l1(torch.cat([z, torch.matmul(s.A, z)], -1)))
                return s.out(s.dr(z)).squeeze(-1)

        return Net(self.A)

    def fit(self, X, y, train_mask):
        torch = _torch()
        torch.manual_seed(self.seed)
        self.net_ = self._net(X.shape[-1])
        Xt, yt, m = torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32), torch.tensor(train_mask)
        opt = torch.optim.AdamW(self.net_.parameters(), lr=self.p["lr"], weight_decay=self.p["wd"])
        for _ in range(self.p["epochs"]):
            self.net_.train()
            opt.zero_grad()
            ((self.net_(Xt) - yt)[m] ** 2).mean().backward()
            opt.step()
        self.net_.eval()
        return self

    def predict(self, X):
        torch = _torch()
        with torch.no_grad():
            return self.net_(torch.tensor(X, dtype=torch.float32)).numpy()
