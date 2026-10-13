"""Identificacion de VAR estructurales por restricciones de signo y de cero (V8-F3). Capa C4.

* Solo signos: Rubio-Ramirez, Waggoner y Zha (2010): Q de Haar por QR de matrices gaussianas; se acepta la rotacion si todas las
  restricciones se cumplen. Matriz de impacto A0inv = chol(Sigma) Q; IRF = Phi_h A0inv (indices [h, variable, shock]).
* Signos + ceros: Arias, Rubio-Ramirez y Waggoner (2018): las columnas de Q se generan secuencialmente en el subespacio ortogonal
  a las filas de las restricciones de cero del shock y a las columnas ya fijadas (los shocks se ordenan por numero decreciente de
  ceros; se exige z_j <= n - j). Los ceros se cumplen exactamente por construccion.
* MUESTREO (correccion H2): para CADA sorteo theta de la posterior se prueba un numero FIJO `rotaciones` de rotaciones y se conservan
  TODAS las aceptadas (con `rotaciones=1` se prueba una sola por theta, sin reintentar). Asi la distribucion marginal de theta entre los
  aceptados es proporcional a p(theta) P(S|theta), como exige la posterior condicionada a los signos. NO se reintenta hasta aceptar
  (eso daria el mismo peso a todo theta con alguna aceptacion). Un theta sin aceptadas no aporta nada y cuenta en `frac_theta_acept`.
* PESOS DE IMPORTANCIA PROPIOS (Haar condicionado a los ceros; NO se afirman identicos a los de ARW, ver revision F3 H3). La formula del articulo NO se ha podido contrastar (sin acceso). Los pesos implementados
  los he derivado por coarea en el espacio (forma reducida theta, Q): objetivo = p(theta) Haar(Q) condicionado a c(theta,Q)=0;
  muestreador = theta ~ p, Q secuencial uniforme. Resulta w ∝ 1 / ( J_Q * |det(P V)| ), con J_Q = sqrt(det(Dc Dc')) (derivada de las
  restricciones respecto de Q), V base ortonormal del nucleo de Dc y P la proyeccion a las coordenadas secuenciales. Si no hay ceros,
  w = 1 (RWZ). Estado: IMPLEMENTADO Y VALIDADO SOLO POR SIMULACION; no equivale necesariamente a la formula ARW. Referencias NO VERIFICADAS.
Descomposicion historica: y_t = d_t + sum_j contrib_j,t con d_t la trayectoria determinista (condiciones iniciales + constante) y
contrib por convolucion de la IRF con los shocks estructurales recuperados eps_t = A0inv^-1 u_t.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import null_space

from . import bvar

SEED = 20261010
HORIZ_FEVD = (4, 8, 12, 20)


class Restricciones:
    """Restricciones por variable, shock y horizontes. var/shock por nombre o por indice."""

    def __init__(self, variables, shocks):
        self.variables, self.shocks = list(variables), list(shocks)
        self.n = len(self.variables)
        assert len(self.shocks) == self.n, "shocks y variables: mismo numero (modelo cuadrado)"
        self.signos, self.ceros = [], []

    def _i(self, lista, x):
        return x if isinstance(x, (int, np.integer)) else lista.index(x)

    def signo(self, var, shock, signo, h=0):
        for hh in np.atleast_1d(h):
            self.signos.append((self._i(self.variables, var), self._i(self.shocks, shock), int(np.sign(signo)), int(hh)))
        return self

    def cero(self, var, shock, h=0):
        for hh in np.atleast_1d(h):
            self.ceros.append((self._i(self.variables, var), self._i(self.shocks, shock), int(hh)))
        return self

    @property
    def H_restr(self):
        return max([s[3] for s in self.signos] + [c[2] for c in self.ceros] + [0])

    def orden_shocks(self):
        z = np.array([sum(1 for c in self.ceros if c[1] == j) for j in range(self.n)])
        orden = sorted(range(self.n), key=lambda j: (-z[j], j))
        for pos, j in enumerate(orden):
            if z[j] > self.n - 1 - pos:
                raise ValueError(f"ceros inadmisibles (shock {self.shocks[j]}: {z[j]} ceros en la posicion {pos}); se exige z_j <= n-j")
        return orden, z


def _pesos_arw(Qp, Mp):
    """log-peso de una rotacion (en coordenadas permutadas). Qp (n,n) columnas ordenadas; Mp[pos] (z_pos, n)."""
    n = Qp.shape[0]
    pares = [(a, b) for a in range(n) for b in range(a + 1, n)]
    idx = {pb: m for m, pb in enumerate(pares)}
    z = [M.shape[0] for M in Mp]
    zt = sum(z)
    if zt == 0:
        return 0.0
    Dc = np.zeros((zt, len(pares)))
    r0 = 0
    for j in range(n):
        if z[j]:
            for (a, b), m in idx.items():
                if b == j:
                    Dc[r0:r0 + z[j], m] = Mp[j] @ Qp[:, a]
                elif a == j:
                    Dc[r0:r0 + z[j], m] = -(Mp[j] @ Qp[:, b])
        r0 += z[j]
    U, sv, Vt = np.linalg.svd(Dc, full_matrices=True)
    logJ = np.sum(np.log(sv[:zt]))
    V = Vt[zt:].T  # (Ns, dF)
    dF = V.shape[1]
    if dF == 0:
        return -logJ
    P = np.zeros((dF, len(pares)))
    r = 0
    for j in range(n):
        cols = [idx[(j, b)] for b in range(j + 1, n)]
        if not cols:
            continue
        K = np.eye(len(cols)) if z[j] == 0 else null_space(Mp[j] @ Qp[:, j + 1:])
        P[r:r + K.shape[1], cols] = K.T
        r += K.shape[1]
    assert r == dF, (r, dF)
    return -logJ - np.linalg.slogdet(P @ V)[1]


def identificar(B, Sigma, n, p, restr, H=20, n_objetivo=None, rotaciones=512, lote=256, rng=None, pesos=True, orden=None):
    """Aplica las restricciones a sorteos (B, Sigma) de la posterior (D,k,n), (D,n,n).
    Por cada theta prueba exactamente `rotaciones` rotaciones y conserva todas las aceptadas (ver cabecera). Si n_objetivo no es None,
    se deja de recorrer thetas cuando se alcanzan n_objetivo aceptadas (al terminar el theta en curso).
    Devuelve dict: irf (N,H+1,n,n), Q, A0inv, B, Sigma, peso (suma 1), ess, acept (aceptadas/rotaciones), n_sorteos_usados,
    frac_theta_acept (thetas con alguna aceptada / thetas usados), rot_total, idx."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    orden0, zc = restr.orden_shocks()
    if orden is None:
        orden = orden0
    elif any(zc[j] > n - 1 - pos for pos, j in enumerate(orden)):
        raise ValueError("orden forzado incompatible con los ceros")
    D = B.shape[0]
    Phi = bvar.ma_coefs(B, n, p, max(H, restr.H_restr))
    P = np.linalg.cholesky(Sigma)
    out = dict(irf=[], Q=[], A0inv=[], B=[], Sigma=[], idx=[], logw=[])
    tried = acc = 0
    usados = con_acept = 0
    for d in range(D):
        if n_objetivo is not None and len(out["Q"]) >= n_objetivo:
            break
        usados += 1
        L = Phi[d] @ P[d]
        Zm = [np.array([L[h, i, :] for (i, s, h) in restr.ceros if s == j]).reshape(-1, n) for j in range(n)]
        Sm = [np.array([sg * L[h, i, :] for (i, s, sg, h) in restr.signos if s == j]).reshape(-1, n) for j in range(n)]
        rots, got = 0, 0
        while rots < rotaciones:
            K = min(lote, rotaciones - rots)
            rots += K
            Qp = np.zeros((K, n, n))
            for pos, j in enumerate(orden):
                x = rng.standard_normal((K, n))
                rows = [np.broadcast_to(Zm[j], (K,) + Zm[j].shape)] if Zm[j].shape[0] else []
                if pos:
                    rows.append(Qp[:, :, :pos].transpose(0, 2, 1))
                if rows:
                    N = np.concatenate(rows, axis=1)
                    M = N @ N.transpose(0, 2, 1)
                    try:
                        lam = np.linalg.solve(M, (N @ x[:, :, None]))
                    except np.linalg.LinAlgError:
                        lam = np.linalg.pinv(M) @ (N @ x[:, :, None])
                    x = x - (N.transpose(0, 2, 1) @ lam)[:, :, 0]
                Qp[:, :, pos] = x / np.linalg.norm(x, axis=1, keepdims=True)
            ok = np.ones(K, bool)
            for pos, j in enumerate(orden):
                if Sm[j].shape[0]:
                    ok &= np.all(Sm[j] @ Qp[:, :, pos].T > 0, axis=0)  # (s_j, K)
            for kk in np.flatnonzero(ok):
                Qk = np.zeros((n, n))
                for pos, j in enumerate(orden):
                    Qk[:, j] = Qp[kk, :, pos]
                lw = 0.0
                if pesos and zc.sum():
                    lw = _pesos_arw(Qp[kk], [Zm[j] for j in orden])
                A0 = P[d] @ Qk
                out["Q"].append(Qk)
                out["A0inv"].append(A0)
                out["irf"].append(Phi[d][:H + 1] @ A0)
                out["B"].append(B[d])
                out["Sigma"].append(Sigma[d])
                out["idx"].append(d)
                out["logw"].append(lw)
                got += 1
            acc += int(ok.sum())
        tried += rots
        con_acept += int(got > 0)
    res = {k: np.array(v) for k, v in out.items()}
    N = len(res["Q"])
    if N:
        w = np.exp(res["logw"] - res["logw"].max())
        w /= w.sum()
    else:
        w = np.array([])
    res["peso"] = w
    res["ess"] = float(1.0 / np.sum(w ** 2)) if N else 0.0
    res["acept"] = acc / max(tried, 1)
    res["n_sorteos_usados"] = usados
    res["frac_theta_acept"] = con_acept / max(usados, 1)
    res["rot_total"] = tried
    res.pop("logw")
    res.update(n=n, p=p, H=H)
    return res


def comprobar(res, restr):
    """Maximo |IRF| en las restricciones de cero y fraccion de (sorteo, restriccion de signo) que se cumplen."""
    I = res["irf"]
    mz = max([np.max(np.abs(I[:, h, i, j])) for (i, j, h) in restr.ceros] + [0.0])
    fs = np.mean([np.all(sg * I[:, h, i, j] > 0) for (i, j, sg, h) in restr.signos]) if restr.signos else 1.0
    return mz, float(fs)


def fevd(irf, hs=HORIZ_FEVD):
    """FEVD a h pasos (suma de IRF^2 de 0 a h-1): (..., len(hs), variable, shock), filas suman 1."""
    out = []
    for h in hs:
        th = np.sum(irf[..., :h, :, :] ** 2, axis=-3)
        out.append(th / th.sum(-1, keepdims=True))
    return np.stack(out, axis=-3)


def resumen(res, hs=HORIZ_FEVD):
    """Bandas 68/90 de la IRF y de la FEVD (cuantiles ponderados por res['peso'])."""
    w = res["peso"]
    return dict(irf=bvar.bandas(res["irf"], 0, w), fevd=bvar.bandas(fevd(res["irf"], hs), 0, w))


def remuestrear(res, n, rng=None):
    """Remuestreo ponderado (deterministico con rng) de los sorteos; devuelve indices."""
    rng = np.random.default_rng(SEED) if rng is None else rng
    return rng.choice(len(res["peso"]), size=n, replace=True, p=res["peso"])


# ------------------------------------------------------------ descomposicion historica
def descomposicion_historica(res, Y, const=True, exog=None):
    """Contribucion de cada shock a cada variable en cada periodo, para cada sorteo aceptado.
    exog: (T, m) ficticias deterministas usadas al estimar (mismas filas que Y); su efecto (directo y propagado por los retardos) va en
    la parte determinista `det`, junto con la constante y las condiciones iniciales. `det_exog` = parte de `det` debida a las exogenas.
    Devuelve dict: contrib (N, Te, variable, shock), det (N, Te, n), det_exog, eps (N, Te, n), y (Te, n),
    error (max |y - det - sum contrib|)."""
    n, p = res["n"], res["p"]
    Y = np.asarray(Y, float)
    yy, X = bvar.retardos(Y, p, const, exog)
    m = 0 if exog is None else X.shape[1] - n * p - int(const)
    Te = yy.shape[0]
    B, A0 = res["B"], res["A0inv"]
    N = B.shape[0]
    A, c = bvar.coef_matrices(B, n, p, m, const)
    U = yy[None] - np.einsum("tk,dkn->dtn", X, B)
    eps = np.einsum("dij,dtj->dti", np.linalg.inv(A0), U)
    Phi = bvar.ma_coefs(B, n, p, Te - 1)
    G = Phi @ A0[:, None]  # (N, Te, n, n)
    ex = np.zeros((Te, 0)) if m == 0 else X[:, n * p:n * p + m]
    bx = bvar.coef_exog(B, n, p, m) if m else np.zeros((N, 0, n))

    def det_path(con_exog):
        hist = np.zeros((N, p + Te, n))
        hist[:, :p] = Y[:p][None]
        for t in range(Te):
            d = c.copy()
            if m and con_exog:
                d = d + np.einsum("k,dkn->dn", ex[t], bx)
            for l in range(1, p + 1):
                d = d + np.einsum("dij,dj->di", A[:, l - 1], hist[:, p + t - l])
            hist[:, p + t] = d
        return hist[:, p:]
    det = det_path(True)
    det_exog = det - det_path(False) if m else np.zeros_like(det)
    idx = np.arange(Te)[:, None] - np.arange(Te)[None, :]
    mask = (idx >= 0)
    ic = np.clip(idx, 0, None)
    contrib = np.empty((N, Te, n, n))
    for d_ in range(N):
        Gt = G[d_][ic] * mask[:, :, None, None]  # (t, s, i, j)
        contrib[d_] = np.einsum("tsij,sj->tij", Gt, eps[d_])
    error = float(np.max(np.abs(yy[None] - det - contrib.sum(-1))))
    return dict(contrib=contrib, det=det, det_exog=det_exog, eps=eps, y=yy, error=error)


def sumar_tramos(contrib, fechas, tramos):
    """Suma contribuciones por tramos de fechas. contrib (..., Te, variable, shock); fechas (Te,) comparables;
    tramos [(ini, fin), ...] inclusivos. Devuelve (..., n_tramos, variable, shock)."""
    out = []
    for (a, b) in tramos:
        m = np.array([(f >= a) and (f <= b) for f in fechas])
        out.append(contrib[..., m, :, :].sum(axis=-3))
    return np.stack(out, axis=-3)


def historica_bandas(hd, peso=None, fechas=None, tramos=None):
    """Bandas 68/90 de las contribuciones (por periodo o por tramos si se dan fechas y tramos)."""
    c = hd["contrib"] if tramos is None else sumar_tramos(hd["contrib"], fechas, tramos)
    return bvar.bandas(c, 0, peso)
