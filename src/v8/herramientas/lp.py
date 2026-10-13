"""Proyecciones locales (Jorda 2005): OLS con Newey-West, LP-IV (2SLS por horizonte) con F de primera etapa robusto
(efectivo de Olea-Pflueger con 1 instrumento; F tipo Kleibergen-Paap con >1) e intervalos Anderson-Rubin HAC;
version de panel con efectos fijos y errores Driscoll-Kraay o agrupados.

Convencion: para cada horizonte h, y_{t+h} (o y_{t+h}-y_{t-1} si acumulado) sobre shock_t y controles_t.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261010


def _nw_lrv(G, L):
    """Varianza de largo plazo Bartlett de las filas de G (T x m). Devuelve m x m."""
    T = G.shape[0]
    G = G - 0.0
    S = G.T @ G / T
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        Gam = G[l:].T @ G[:-l] / T
        S += w * (Gam + Gam.T)
    return S


def _lead(y, h, acumulado):
    y = pd.Series(y)
    if acumulado:
        return y.shift(-h) - y.shift(1)
    return y.shift(-h)


def _desplaza(df, lags, cols):
    out = {}
    for c in cols:
        for k in range(1, lags + 1):
            out[f"{c}_l{k}"] = df[c].shift(k)
    return pd.DataFrame(out, index=df.index)


def _armar(y, shock, controles, h, rezagos, acumulado):
    y = pd.Series(np.asarray(y, float))
    D = pd.DataFrame({"x": np.asarray(shock, float)})
    W = _desplaza(pd.DataFrame({"y": y, "x": D["x"]}), rezagos, ["y", "x"]) if rezagos > 0 else pd.DataFrame(index=y.index)
    if controles is not None:
        C = pd.DataFrame(np.asarray(controles, float).reshape(len(y), -1), index=y.index).add_prefix("c")
        W = pd.concat([W, C], axis=1)
    dep = _lead(y, h, acumulado).rename("dep")
    return dep, D, W


def lp(y, shock, controles=None, H=8, rezagos=2, acumulado=False, hac="h+1", nivel=0.95):
    """LP-OLS. hac: 'h+1' (Newey-West con h+1 retardos), entero, o 'hc' (robusto a heterocedasticidad, para LP con
    rezagos aumentados de Montiel Olea-Plagborg-Moller). Devuelve DataFrame h, beta, se, lo, hi, n."""
    z = stats.norm.ppf(0.5 + nivel / 2)
    rows = []
    for h in range(H + 1):
        dep, D, W = _armar(y, shock, controles, h, rezagos, acumulado)
        M = pd.concat([dep, D[["x"]], W], axis=1).dropna()
        Y = M["dep"].values
        X = np.column_stack([M["x"].values, np.ones(len(M)), M.drop(columns=["dep", "x"]).values])
        n, k = X.shape
        XtXi = np.linalg.inv(X.T @ X)
        b = XtXi @ X.T @ Y
        u = Y - X @ b
        L = h + 1 if hac == "h+1" else (0 if hac == "hc" else int(hac))
        S = _nw_lrv(X * u[:, None], L)
        V = n * XtXi @ S @ XtXi * (n / (n - k))
        se = float(np.sqrt(V[0, 0]))
        rows.append({"h": h, "beta": float(b[0]), "se": se, "lo": float(b[0] - z * se), "hi": float(b[0] + z * se), "n": n})
    return pd.DataFrame(rows)


def _resid(M, cols_out, W):
    """Parcializa (FWL) las columnas de M[cols_out] respecto a W (matriz)."""
    out = {}
    for c in cols_out:
        v = M[c].values.astype(float)
        out[c] = v - W @ np.linalg.lstsq(W, v, rcond=None)[0]
    return out


def lp_iv(y, endog, instr, controles=None, H=8, rezagos=2, acumulado=False, nivel=0.95, grid_n=4001, hac="h+1"):
    """LP-IV: 2SLS por horizonte (endogena = endog_t, instrumento(s) = instr_t, columnas de `instr`).

    Por horizonte devuelve beta 2SLS y su IC normal, F de primera etapa robusto HAC (efectivo de Olea-Pflueger si hay 1
    instrumento; Wald/k tipo Kleibergen-Paap si hay mas, aproximacion declarada) y el intervalo Anderson-Rubin HAC
    (conjunto de beta0 no rechazados por el contraste de coeficientes nulos de los instrumentos en y-beta0*x; robusto a
    instrumento debil). ar_acotado=False indica que el conjunto llega al borde de la rejilla (no acotado).
    """
    Z_all = np.asarray(instr, float)
    if Z_all.ndim == 1:
        Z_all = Z_all[:, None]
    z_crit = stats.norm.ppf(0.5 + nivel / 2)
    rows = []
    for h in range(H + 1):
        dep, D, W = _armar(y, endog, controles, h, rezagos, acumulado)
        Zdf = pd.DataFrame(Z_all, columns=[f"z{i}" for i in range(Z_all.shape[1])], index=dep.index)
        M = pd.concat([dep, D[["x"]], Zdf, W], axis=1).dropna()
        n = len(M)
        Wm = np.column_stack([np.ones(n), M.drop(columns=["dep", "x"] + list(Zdf.columns)).values])
        zc = list(Zdf.columns)
        r = _resid(M, ["dep", "x"] + zc, Wm)
        yt, xt = r["dep"], r["x"]
        Zt = np.column_stack([r[c] for c in zc])
        kz = Zt.shape[1]
        kw = Wm.shape[1]
        L = h + 1 if hac == "h+1" else int(hac)
        # primera etapa robusta
        ZtZi = np.linalg.inv(Zt.T @ Zt)
        pi = ZtZi @ Zt.T @ xt
        e1 = xt - Zt @ pi
        S1 = _nw_lrv(Zt * e1[:, None], L)
        Vpi = n * ZtZi @ S1 @ ZtZi
        Fr = float(pi @ np.linalg.solve(Vpi, pi) / kz)  # Wald/k
        # Olea-Pflueger efectivo: con 1 instrumento coincide con el F robusto; con >1 se usa Wald/k (aprox.)
        # 2SLS
        xhat = Zt @ pi
        b = float(xhat @ yt / (xhat @ xt))
        u = yt - b * xt
        # varianza 2SLS HAC (sandwich con xhat)
        s = _nw_lrv((xhat * u)[:, None], L)[0, 0]
        se = float(np.sqrt(n * s) / abs(xhat @ xt))
        # Anderson-Rubin: g_t(b0)=Zt_t*(yt - b0*xt) = a_t - b0*c_t
        A = Zt * yt[:, None]
        Cc = Zt * xt[:, None]
        Saa = _nw_lrv(A, L)
        Scc = _nw_lrv(Cc, L)
        Sac = _cross_lrv(A, Cc, L)
        abar = A.mean(0)
        cbar = Cc.mean(0)
        sc = max(se, 1e-3 * np.std(yt) / max(np.std(xt), 1e-12))
        u_ = np.linspace(-8, 8, grid_n)
        grid = b + sc * np.sinh(u_)
        crit = stats.chi2.ppf(nivel, kz)
        acept = np.zeros(grid_n, bool)
        for i, b0 in enumerate(grid):
            gbar = abar - b0 * cbar
            S = Saa - b0 * (Sac + Sac.T) + b0 ** 2 * Scc
            try:
                ar = n * float(gbar @ np.linalg.solve(S, gbar))
            except np.linalg.LinAlgError:
                ar = np.inf
            acept[i] = ar <= crit
        if acept.any():
            idx = np.where(acept)[0]
            lo, hi = grid[idx[0]], grid[idx[-1]]
            acot = not (idx[0] == 0 or idx[-1] == grid_n - 1)
            conexo = bool(np.all(np.diff(idx) == 1))
        else:
            lo = hi = np.nan
            acot, conexo = True, True
        rows.append({"h": h, "beta": b, "se": se, "lo": b - z_crit * se, "hi": b + z_crit * se, "F_robusto": Fr, "n": n,
                     "ar_lo": float(lo), "ar_hi": float(hi), "ar_acotado": acot, "ar_conexo": conexo,
                     "F_tipo": "OP-efectivo(=F robusto, 1 instr.)" if kz == 1 else "Wald/k tipo KP (aprox.)"})
    return pd.DataFrame(rows)


def _cross_lrv(A, B, L):
    T = A.shape[0]
    S = A.T @ B / T
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        S += w * (A[l:].T @ B[:-l] / T + A[:-l].T @ B[l:] / T)
    return S


def lp_panel(df, y, shock, entidad, tiempo, controles=(), H=8, rezagos=1, efectos_tiempo=False, cov="dk", nivel=0.95):
    """LP de panel con efectos fijos de entidad (y opcionalmente de tiempo). cov: 'dk' (Driscoll-Kraay, ancho h+1) o
    'cluster' (por entidad). Rezagos de y y shock dentro de cada entidad."""
    from linearmodels.panel import PanelOLS
    d = df.sort_values([entidad, tiempo]).copy()
    g = d.groupby(entidad)
    rows = []
    z = stats.norm.ppf(0.5 + nivel / 2)
    for h in range(H + 1):
        dd = pd.DataFrame({entidad: d[entidad].values, tiempo: d[tiempo].values})
        dd["dep"] = g[y].shift(-h).values
        dd["x"] = d[shock].values
        regs = ["x"]
        for k in range(1, rezagos + 1):
            dd[f"yl{k}"] = g[y].shift(k).values
            dd[f"xl{k}"] = g[shock].shift(k).values
            regs += [f"yl{k}", f"xl{k}"]
        for c in controles:
            dd[c] = d[c].values
            regs.append(c)
        dd = dd.dropna().set_index([entidad, tiempo])
        mod = PanelOLS(dd["dep"], dd[regs], entity_effects=True, time_effects=efectos_tiempo)
        if cov == "dk":
            r = mod.fit(cov_type="kernel", kernel="bartlett", bandwidth=h + 1)
        else:
            r = mod.fit(cov_type="clustered", cluster_entity=True)
        b, se = float(r.params["x"]), float(r.std_errors["x"])
        rows.append({"h": h, "beta": b, "se": se, "lo": b - z * se, "hi": b + z * se, "n": int(r.nobs)})
    return pd.DataFrame(rows)
