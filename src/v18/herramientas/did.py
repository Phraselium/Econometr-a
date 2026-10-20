"""V18 · Estimadores de diferencias en diferencias escalonadas con wild cluster bootstrap de Webb (Callaway-Sant'Anna y Sun-Abraham).

Sin lectura de datos: reciben arrays. Lo que corrige frente a V16 (cs_webb, NO APTO: tamaño 0,0655 y cobertura 0,9015 con
la variante «a»; 0,3145 y 0,6905 con la variante sin nulo impuesto y cohortes de una provincia):
  1. el contraste se hace con el NULO IMPUESTO sobre el agregado (los residuos de las tratadas se desplazan en θ0 − θ̂, de modo que
     el agregado de las celdas vale θ0 sin imponer que todas las celdas valgan lo mismo);
  2. el estadístico bootstrap se estudentiza con el EE de agrupación recalculado dentro de cada réplica bootstrap (WCR-t), no con
     un EE de la función de influencia fijo; así la distribución bootstrap incorpora la estimación de la varianza;
  3. la cobertura se mide invirtiendo ese mismo contraste (θ0 = verdad), no con un intervalo simétrico de la variante sin nulo.
Todo es lineal en los pesos de Webb de cada cluster, de modo que cada réplica bootstrap cuesta una multiplicación de matrices.
"""
from __future__ import annotations

import numpy as np

ALCANCE_TERRITORIAL = "sin lectura de datos"
SEMILLA = 20261010

_WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def pesos_webb(rng: np.random.Generator, G: int, B: int) -> np.ndarray:
    return _WEBB[rng.integers(0, 6, size=(G, B))]


def _onehot(cluster: np.ndarray) -> np.ndarray:
    cl = np.unique(cluster)
    return (cluster[:, None] == cl[None, :]).astype(float)


class CallawaySantAnna:
    """ATT(g, t) con nunca tratadas como control y periodo base g − 1; agregado «simple» (peso por tamaño de cohorte sobre t >= g).

    cohorte: (n,) con el primer periodo tratado (índice) o −1 si nunca tratada. cluster: (n,) etiquetas. T: periodos.
    """

    def __init__(self, cohorte: np.ndarray, cluster: np.ndarray, T: int):
        self.cohorte = np.asarray(cohorte)
        self.T = T
        self.M = _onehot(np.asarray(cluster))
        self.G = self.M.shape[1]
        gs = sorted(set(self.cohorte[self.cohorte >= 0].tolist()))
        self.celdas = [(g, t) for g in gs for t in range(g, T)]
        n_g = {g: int((self.cohorte == g).sum()) for g in gs}
        tot = sum(n_g[g] for g, _ in self.celdas)
        self.w = np.array([n_g[g] / tot for g, _ in self.celdas])
        self.mask_G = np.column_stack([self.cohorte == g for g, _ in self.celdas])
        nunca = self.cohorte < 0
        self.mask_C = np.repeat(nunca[:, None], len(self.celdas), axis=1)
        self.nG = self.mask_G.sum(0).astype(float)
        self.nC = self.mask_C.sum(0).astype(float)
        self.pG = (self.M.T @ self.mask_G) / self.nG
        self.pC = (self.M.T @ self.mask_C) / self.nC
        self.gi = np.array([g for g, _ in self.celdas])
        self.ti = np.array([t for _, t in self.celdas])

    def _d(self, Y: np.ndarray) -> np.ndarray:
        return Y[:, self.ti] - Y[:, self.gi - 1]

    def estimar(self, Y: np.ndarray) -> float:
        D = self._d(Y)
        mG = (D * self.mask_G).sum(0) / self.nG
        mC = (D * self.mask_C).sum(0) / self.nC
        return float(self.w @ (mG - mC))

    def verdad(self, efecto: np.ndarray) -> float:
        """Agregado verdadero con los mismos pesos: media de efectos de las tratadas de la cohorte en t, por celda."""
        e = efecto[:, self.ti]
        return float(self.w @ ((e * self.mask_G).sum(0) / self.nG))

    def estadisticos(self, Y: np.ndarray, theta0: float, V: np.ndarray, nulo_impuesto: bool = True) -> tuple[float, np.ndarray, float, float]:
        """(t observado, t bootstrap (B,), ATT, EE de agrupación) para pesos de cluster V (G, B) dados."""
        D = self._d(Y)
        mG = (D * self.mask_G).sum(0) / self.nG
        mC = (D * self.mask_C).sum(0) / self.nC
        att = float(self.w @ (mG - mC))
        rU_G = (D - mG) * self.mask_G
        rU_C = (D - mC) * self.mask_C
        a_obs = (self.M.T @ rU_G / self.nG - self.M.T @ rU_C / self.nC) @ self.w
        se = float(np.sqrt((a_obs ** 2).sum()))
        t_obs = (att - theta0) / max(se, 1e-300)
        despl = (att - theta0) if nulo_impuesto else 0.0      # residuos de las tratadas con el agregado impuesto en θ0
        rG = (D - mG + despl) * self.mask_G
        RG = self.M.T @ rG / self.nG          # (G, celdas)
        RC = self.M.T @ rU_C / self.nC
        MG = RG.T @ V
        MC = RC.T @ V
        num = self.w @ (MG - MC)
        a = (RG - RC) @ self.w
        psi = V * a[:, None] - (self.pG * self.w) @ MG + (self.pC * self.w) @ MC
        se_b = np.sqrt((psi ** 2).sum(0))
        return float(t_obs), num / np.maximum(se_b, 1e-300), att, se

    def p_valor(self, Y: np.ndarray, theta0: float, rng: np.random.Generator, B: int = 999, nulo_impuesto: bool = True) -> tuple[float, float, float]:
        """p-valor del wild cluster bootstrap-t (Webb) de H0: agregado = θ0. Devuelve (p, att, EE de agrupación)."""
        V = pesos_webb(rng, self.G, B)
        t_obs, t_b, att, se = self.estadisticos(Y, theta0, V, nulo_impuesto)
        p = (1 + np.sum(np.abs(t_b) >= abs(t_obs))) / (B + 1)
        return float(p), att, se


class SunAbraham:
    """Estimador de interacciones ponderadas de Sun y Abraham (2021): MCO con efectos fijos de unidad y de periodo y dummies
    cohorte × tiempo relativo para todo e ≠ −1 (nunca tratadas como control); ATT_e = media ponderada por tamaño de cohorte de
    los CATT(g, e); agregado = media simple de ATT_e sobre e >= 0. Inferencia por wild cluster bootstrap de Webb con el nulo impuesto
    (mínimos cuadrados restringidos en el agregado) y EE de agrupación recalculado en cada réplica (WCR-t).
    """

    def __init__(self, cohorte: np.ndarray, cluster: np.ndarray, T: int):
        self.cohorte = np.asarray(cohorte)
        self.n = len(self.cohorte)
        self.T = T
        cl = np.asarray(cluster)
        self.M = _onehot(cl)
        self.G = self.M.shape[1]
        gs = sorted(set(self.cohorte[self.cohorte >= 0].tolist()))
        self.gs = gs
        cols = [(g, t) for g in gs for t in range(T) if t != g - 1]
        self.cols = cols
        K = len(cols)
        X = np.zeros((self.n, T, K))
        for k, (g, t) in enumerate(cols):
            X[self.cohorte == g, t, k] = 1.0
        self.Xt = self._desmedia(X.reshape(self.n, T, K)).reshape(self.n * T, K)
        XtX_inv = np.linalg.pinv(self.Xt.T @ self.Xt)
        self.H = XtX_inv @ self.Xt.T                 # (K, nT)
        n_g = {g: int((self.cohorte == g).sum()) for g in gs}
        es = sorted({t - g for g, t in cols if t - g >= 0})
        a = np.zeros(K)
        for e in es:
            disp = [g for g in gs if (g + e) < T]
            tot = sum(n_g[g] for g in disp)
            for g in disp:
                a[cols.index((g, g + e))] += n_g[g] / tot / len(es)
        self.a = a
        self.h = a @ self.H                          # (nT,)
        self.rows_cl = np.repeat(self.M, T, axis=0)  # (nT, G)
        self.n_g = n_g
        self.q = XtX_inv @ a / float(a @ XtX_inv @ a)

    @staticmethod
    def _desmedia(Z: np.ndarray) -> np.ndarray:
        """Residuo de las dummies de unidad y de periodo (panel equilibrado) en el eje 0 (unidad) y 1 (tiempo)."""
        return Z - Z.mean(axis=0, keepdims=True) - Z.mean(axis=1, keepdims=True) + Z.mean(axis=(0, 1), keepdims=True)

    def estimar(self, Y: np.ndarray) -> float:
        return float(self.h @ self._desmedia(Y[:, :, None])[:, :, 0].ravel())

    def verdad(self, efecto: np.ndarray) -> float:
        cat = np.array([efecto[self.cohorte == g, t].mean() for g, t in self.cols])
        return float(self.a @ cat)

    def p_valor(self, Y: np.ndarray, theta0: float, rng: np.random.Generator, B: int = 499, nulo_impuesto: bool = True) -> tuple[float, float, float]:
        n, T = self.n, self.T
        yt = self._desmedia(Y[:, :, None])[:, :, 0].ravel()
        beta = self.H @ yt
        u = yt - self.Xt @ beta
        att = float(self.a @ beta)
        psi_obs = self.rows_cl.T @ (self.h * u)
        se = float(np.sqrt((psi_obs ** 2).sum()))
        t_obs = (att - theta0) / max(se, 1e-300)
        if nulo_impuesto:
            beta_r = beta - self.q * (att - theta0)
        else:
            beta_r = beta
        u_r = yt - self.Xt @ beta_r
        V = pesos_webb(rng, self.G, B)                       # (G, B)
        vu = (self.rows_cl @ V) * u_r[:, None]               # (nT, B)
        ys = (self.Xt @ beta_r)[:, None] + self._desmedia(vu.reshape(n, T, B)).reshape(n * T, B)
        bs = self.H @ ys
        us = ys - self.Xt @ bs
        psi = self.rows_cl.T @ (self.h[:, None] * us)        # (G, B)
        se_b = np.sqrt((psi ** 2).sum(0))
        t_b = (self.a @ bs - theta0) / np.maximum(se_b, 1e-300)
        p = (1 + np.sum(np.abs(t_b) >= abs(t_obs))) / (B + 1)
        return float(p), att, se
