"""Proyecciones locales (Jorda 2005): OLS con Newey-West (o EWC), horizontes negativos (pretendencias), contraste agregado h=a..b,
LP-IV (2SLS por horizonte) con F de primera etapa robusto
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
    """y_{t+h} (o y_{t+h}-y_{t-1} si acumulado). Vale tambien para h<0 (y_{t-|h|}); con acumulado y h=-1 es identicamente 0."""
    y = pd.Series(y)
    if acumulado:
        return y.shift(-h) - y.shift(1)
    return y.shift(-h)


def _desplaza(df, lags, cols, h=0):
    """Rezagos de las columnas. Para h<0 (pretendencias) los rezagos de 'y' se fechan respecto a la dependiente (t+h):
    y_{t+h-k}, de modo que sean predeterminados respecto a ella y no coincidan con ella; los de 'x' siguen siendo x_{t-k}."""
    out = {}
    for c in cols:
        for k in range(1, lags + 1):
            out[f"{c}_l{k}"] = df[c].shift(k - h if (c == "y" and h < 0) else k)
    return pd.DataFrame(out, index=df.index)


def _armar(y, shock, controles, h, rezagos, acumulado):
    y = pd.Series(np.asarray(y, float))
    D = pd.DataFrame({"x": np.asarray(shock, float)})
    W = _desplaza(pd.DataFrame({"y": y, "x": D["x"]}), rezagos, ["y", "x"], h) if rezagos > 0 else pd.DataFrame(index=y.index)
    if controles is not None:
        C = pd.DataFrame(np.asarray(controles, float).reshape(len(y), -1), index=y.index).add_prefix("c")
        W = pd.concat([W, C], axis=1)
    dep = _lead(y, h, acumulado).rename("dep")
    return dep, D, W


def _hac_L(hac, h):
    if hac == "h+1":
        return abs(h) + 1
    if hac == "2h+2":  # ancho de banda mayor (EE HAR mas robusto para n ~ 100)
        return 2 * (abs(h) + 1)
    return 0 if hac == "hc" else int(hac)


def _ols_unico(M, L, z):
    Y = M["dep"].values
    X = np.column_stack([M["x"].values, np.ones(len(M)), M.drop(columns=["dep", "x"]).values])
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ Y
    u = Y - X @ b
    S = _nw_lrv(X * u[:, None], L)
    V = n * XtXi @ S @ XtXi * (n / (n - k))
    se = float(np.sqrt(V[0, 0]))
    return {"beta": float(b[0]), "se": se, "lo": float(b[0] - z * se), "hi": float(b[0] + z * se), "n": n}


def lp(y, shock, controles=None, H=8, rezagos=2, acumulado=False, hac="h+1", nivel=0.95, H_min=0, ewc=False):
    """LP-OLS. hac: 'h+1' (Newey-West con |h|+1 retardos), '2h+2' (ancho de banda mayor), entero, o 'hc' (robusto a heterocedasticidad, para LP con
    rezagos aumentados de Montiel Olea-Plagborg-Moller). Devuelve DataFrame h, beta, se, lo, hi, n.

    H_min<0 anade horizontes negativos (pretendencias: y_{t+h} con h<0 sobre el shock_t; los rezagos de y se fechan
    respecto a t+h). Con acumulado=True el horizonte h=-1 es identicamente 0 y se omite.
    ewc=True: errores EWC (Equal-Weighted Cosine, Lazarus-Lewis-Stock-Watson 2018) con inferencia fixed-b (t de Student);
    es el EE HAR mas robusto que se ofrece para n ~ 100 (ver `_ols_ewc`).
    """
    z = stats.norm.ppf(0.5 + nivel / 2)
    rows = []
    for h in range(H_min, H + 1):
        if acumulado and h == -1:
            continue
        dep, D, W = _armar(y, shock, controles, h, rezagos, acumulado)
        M = pd.concat([dep, D[["x"]], W], axis=1).dropna()
        if ewc:
            r = _ols_ewc(M, nivel)
        else:
            r = _ols_unico(M, _hac_L(hac, h), z)
        rows.append({"h": h, **r})
    return pd.DataFrame(rows)


def _ols_ewc(M, nivel):
    """OLS con EE EWC (Equal-Weighted Cosine, Lazarus et al. 2018): S = (1/q) sum_j Lambda_j Lambda_j', con
    Lambda_j = T^{-1/2} sum_t psi_j(t/T) g_t, psi_j(s) = sqrt(2) cos(pi j s), q = max(floor(0,4 T^{2/3}), 2) (nu = q gl);
    IC con t(q) (inferencia fixed-b)."""
    Y = M["dep"].values
    X = np.column_stack([M["x"].values, np.ones(len(M)), M.drop(columns=["dep", "x"]).values])
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    b = XtXi @ X.T @ Y
    u = Y - X @ b
    G = X * u[:, None]
    q = max(int(np.floor(0.4 * n ** (2 / 3))), 2)
    t = (np.arange(1, n + 1) - 0.5) / n
    Lam = np.array([np.sqrt(2) * np.cos(np.pi * j * t) @ G / np.sqrt(n) for j in range(1, q + 1)])
    S = Lam.T @ Lam / q
    V = n * XtXi @ S @ XtXi
    se = float(np.sqrt(V[0, 0]))
    tc = stats.t.ppf(0.5 + nivel / 2, q)
    return {"beta": float(b[0]), "se": se, "lo": float(b[0] - tc * se), "hi": float(b[0] + tc * se), "n": n}


def lp_agregado(y, shock, controles=None, hs=(4, 8), rezagos=2, acumulado=False, hac="h+1", nivel=0.95, ewc=False):
    """Contraste agregado de LP-OLS: beta_bar = media de beta_h para h = hs[0]..hs[1] (cotas incluidas), estimada en la MUESTRA
    COMUN (filas con todos los horizontes disponibles) regresando la media de los y_{t+h} sobre los mismos regresores. Es un
    unico contraste de la hipotesis 'media de los efectos a h=4..8' (no hay multiplicidad de horizontes). HAC con hs[1]+1."""
    h1, h2 = hs
    z = stats.norm.ppf(0.5 + nivel / 2)
    dep, D, W = _armar(y, shock, controles, h1, rezagos, acumulado)
    dep = pd.concat([_lead(y, h, acumulado) for h in range(h1, h2 + 1)], axis=1).mean(axis=1, skipna=False).rename("dep")
    M = pd.concat([dep, D[["x"]], W], axis=1).dropna()
    r = _ols_ewc(M, nivel) if ewc else _ols_unico(M, _hac_L(hac, h2), z)
    return pd.DataFrame([{"h": f"{h1}-{h2}", **r}])


def _resid(M, cols_out, W):
    """Parcializa (FWL) las columnas de M[cols_out] respecto a W (matriz)."""
    out = {}
    for c in cols_out:
        v = M[c].values.astype(float)
        out[c] = v - W @ np.linalg.lstsq(W, v, rcond=None)[0]
    return out


def _iv_preparar(M, zc, L):
    """FWL + momentos del IV con `M` (columnas dep, x, z*, controles). Devuelve dict con lo necesario para 2SLS y AR."""
    n = len(M)
    Wm = np.column_stack([np.ones(n), M.drop(columns=["dep", "x"] + list(zc)).values])
    r = _resid(M, ["dep", "x"] + list(zc), Wm)
    yt, xt = r["dep"], r["x"]
    Zt = np.column_stack([r[c] for c in zc])
    A = Zt * yt[:, None]
    Cc = Zt * xt[:, None]
    return {"n": n, "L": L, "yt": yt, "xt": xt, "Zt": Zt, "kz": Zt.shape[1], "A": A, "Cc": Cc,
            "Saa": _nw_lrv(A, L), "Scc": _nw_lrv(Cc, L), "Sac": _cross_lrv(A, Cc, L), "abar": A.mean(0), "cbar": Cc.mean(0)}


def _iv_primera_etapa(P):
    Zt, xt, n, L = P["Zt"], P["xt"], P["n"], P["L"]
    ZtZi = np.linalg.inv(Zt.T @ Zt)
    pi = ZtZi @ Zt.T @ xt
    e1 = xt - Zt @ pi
    S1 = _nw_lrv(Zt * e1[:, None], L)
    Vpi = n * ZtZi @ S1 @ ZtZi
    return pi, float(pi @ np.linalg.solve(Vpi, pi) / P["kz"])


def _ar_en(P, b0):
    """Estadistico AR(b0) = n gbar' S(b0)^{-1} gbar (chi2(kz) bajo H0) y, con 1 instrumento, su version con signo t."""
    gbar = P["abar"] - b0 * P["cbar"]
    S = P["Saa"] - b0 * (P["Sac"] + P["Sac"].T) + b0 ** 2 * P["Scc"]
    try:
        ar = P["n"] * float(gbar @ np.linalg.solve(S, gbar))
    except np.linalg.LinAlgError:
        return np.inf, np.nan
    t = np.sqrt(P["n"]) * gbar[0] / np.sqrt(S[0, 0]) if P["kz"] == 1 else np.nan
    return ar, float(t)


def _ar_pvalor(P, b0=0.0, lado="dos", signo_pi=None):
    """p-valor de Anderson-Rubin para H0: beta = b0.

    lado='dos': chi2(kz) bilateral (valido con instrumento debil). lado='menor' (H1: beta < b0) o 'mayor' (H1: beta > b0):
    unilateral, solo con 1 instrumento; se usa el t_AR con signo multiplicado por el signo de la primera etapa
    (signo_pi; por defecto el estimado). Es valido si ese signo se da por conocido (instrumento no debil en signo): es la
    condicion declarada de la prueba unilateral."""
    ar, t = _ar_en(P, b0)
    if lado == "dos":
        return float(stats.chi2.sf(ar, P["kz"]))
    if P["kz"] != 1:
        return np.nan
    if signo_pi is None:
        signo_pi = np.sign(_iv_primera_etapa(P)[0][0])
    T = t * signo_pi
    return float(stats.norm.cdf(T)) if lado == "menor" else float(stats.norm.sf(T))


def _iv_core(M, zc, L, nivel, grid_n):
    """2SLS, F robusto y conjunto AR (con p-valores AR de H0: beta=0) para una muestra ya armada."""
    P = _iv_preparar(M, zc, L)
    n, kz, xt, yt, Zt = P["n"], P["kz"], P["xt"], P["yt"], P["Zt"]
    z_crit = stats.norm.ppf(0.5 + nivel / 2)
    pi, Fr = _iv_primera_etapa(P)
    xhat = Zt @ pi
    b = float(xhat @ yt / (xhat @ xt))
    u = yt - b * xt
    s = _nw_lrv((xhat * u)[:, None], L)[0, 0]
    se = float(np.sqrt(n * s) / abs(xhat @ xt))
    sc = max(se, 1e-3 * np.std(yt) / max(np.std(xt), 1e-12))
    grid = b + sc * np.sinh(np.linspace(-8, 8, grid_n))
    crit = stats.chi2.ppf(nivel, kz)
    acept = np.array([_ar_en(P, b0)[0] <= crit for b0 in grid])
    if acept.any():
        idx = np.where(acept)[0]
        lo, hi = grid[idx[0]], grid[idx[-1]]
        acot = not (idx[0] == 0 or idx[-1] == grid_n - 1)
        conexo = bool(np.all(np.diff(idx) == 1))
    else:
        lo = hi = np.nan
        acot, conexo = True, True
    sg = np.sign(pi[0]) if kz == 1 else None
    return {"beta": b, "se": se, "lo": b - z_crit * se, "hi": b + z_crit * se, "F_robusto": Fr, "n": n,
            "ar_lo": float(lo), "ar_hi": float(hi), "ar_acotado": acot, "ar_conexo": conexo,
            "ar_p_dos": _ar_pvalor(P, 0.0, "dos"), "ar_p_menor": _ar_pvalor(P, 0.0, "menor", sg),
            "ar_p_mayor": _ar_pvalor(P, 0.0, "mayor", sg),
            "F_tipo": "OP-efectivo(=F robusto, 1 instr.)" if kz == 1 else "Wald/k tipo KP (aprox.)"}


def _iv_muestra(y, endog, instr, controles, h, rezagos, acumulado, agregado=None):
    Z_all = np.asarray(instr, float)
    if Z_all.ndim == 1:
        Z_all = Z_all[:, None]
    dep, D, W = _armar(y, endog, controles, agregado[0] if agregado else h, rezagos, acumulado)
    if agregado:
        dep = pd.concat([_lead(y, k, acumulado) for k in range(agregado[0], agregado[1] + 1)], axis=1).mean(axis=1, skipna=False).rename("dep")
    zc = [f"z{i}" for i in range(Z_all.shape[1])]
    Zdf = pd.DataFrame(Z_all, columns=zc, index=dep.index)
    M = pd.concat([dep, D[["x"]], Zdf, W], axis=1).dropna()
    return M, zc


def lp_iv(y, endog, instr, controles=None, H=8, rezagos=2, acumulado=False, nivel=0.95, grid_n=4001, hac="h+1", H_min=0):
    """LP-IV: 2SLS por horizonte (endogena = endog_t, instrumento(s) = instr_t, columnas de `instr`).

    Por horizonte devuelve beta 2SLS y su IC normal, F de primera etapa robusto HAC (efectivo de Olea-Pflueger si hay 1
    instrumento; Wald/k tipo Kleibergen-Paap si hay mas, aproximacion declarada), el intervalo Anderson-Rubin HAC
    (conjunto de beta0 no rechazados por el contraste de coeficientes nulos de los instrumentos en y-beta0*x; robusto a
    instrumento debil) y los p-valores AR de H0: beta=0 (`ar_p_dos`; `ar_p_menor` y `ar_p_mayor` unilaterales con 1
    instrumento, ver `ar_p`). ar_acotado=False indica que el conjunto llega al borde de la rejilla (no acotado).
    H_min<0 anade horizontes negativos (pretendencias): y_{t+h}, h<0, sobre el instrumento/endogena en t.
    """
    rows = []
    for h in range(H_min, H + 1):
        if acumulado and h == -1:
            continue
        M, zc = _iv_muestra(y, endog, instr, controles, h, rezagos, acumulado)
        rows.append({"h": h, **_iv_core(M, zc, _hac_L(hac, h), nivel, grid_n)})
    return pd.DataFrame(rows)


def ar_p(y, endog, instr, h, b0=0.0, lado="dos", controles=None, rezagos=2, acumulado=False, hac="h+1", agregado=None):
    """p-valor de Anderson-Rubin de H0: beta_h = b0 (`lado` en {'dos','menor','mayor'}; ver `_ar_pvalor`). Con
    `agregado=(h1,h2)` contrasta la media de los efectos h1..h2 (muestra comun)."""
    M, zc = _iv_muestra(y, endog, instr, controles, h, rezagos, acumulado, agregado)
    L = _hac_L(hac, agregado[1]) if agregado else _hac_L(hac, h)
    return _ar_pvalor(_iv_preparar(M, zc, L), b0, lado)


def lp_iv_agregado(y, endog, instr, controles=None, hs=(4, 8), rezagos=2, acumulado=False, nivel=0.95, grid_n=4001, hac="h+1"):
    """Contraste agregado de LP-IV: beta_bar = media de beta_h, h = hs[0]..hs[1], en la muestra comun (regresion de la
    media de los y_{t+h}); 2SLS, F robusto y conjunto AR + p-valores AR de H0: beta_bar=0 (bilateral y unilaterales) con
    HAC de ancho hs[1]+1. Es el contraste de la regla de agregacion h=4-8 del pre-registro (un unico contraste)."""
    M, zc = _iv_muestra(y, endog, instr, controles, None, rezagos, acumulado, agregado=hs)
    L = _hac_L(hac, hs[1])
    r = _iv_core(M, zc, L, nivel, grid_n)
    return pd.DataFrame([{"h": f"{hs[0]}-{hs[1]}", **r}])


def placebo_permutacion_iv(y, endog, instr, h=0, controles=None, rezagos=2, acumulado=False, hac="h+1", n_perm=499,
                           modo="iid", seed=SEED, agregado=None):
    """Placebo por permutacion del instrumento (1 instrumento). Recalcula |t_AR(0)| (HAC) y beta 2SLS con el instrumento
    permutado y compara con lo observado: p_perm = (1 + #{|t_perm| >= |t_obs|}) / (1 + n_perm).

    modo='iid': permutacion libre en el tiempo (destruye la autocorrelacion del instrumento; adecuado para shocks sin
    autocorrelacion); modo='desplazamiento': desplazamiento circular aleatorio (conserva la autocorrelacion del instrumento).
    Si el instrumento y el resultado no estan relacionados, p_perm ~ U(0,1) (placebo 'pasa' si el efecto observado cae
    dentro de la nube permutada; la nube permutada centra en 0 por construccion). Devuelve dict con p_perm, t_obs, beta_obs,
    cuantiles 2,5/97,5 % de beta bajo permutacion y n_perm."""
    M, zc = _iv_muestra(y, endog, instr, controles, h, rezagos, acumulado, agregado)
    if len(zc) != 1:
        raise ValueError("placebo_permutacion_iv: solo un instrumento")
    L = _hac_L(hac, agregado[1]) if agregado else _hac_L(hac, h)
    P = _iv_preparar(M, zc, L)
    n = P["n"]
    Wm = np.column_stack([np.ones(n), M.drop(columns=["dep", "x"] + zc).values])
    Hat = Wm @ np.linalg.pinv(Wm)
    yt, xt = P["yt"], P["xt"]
    z0 = M[zc[0]].values.astype(float)

    def estad(z):
        zt = z - Hat @ z
        a = zt * yt
        s = _nw_lrv(a[:, None], L)[0, 0]
        t = np.sqrt(n) * a.mean() / np.sqrt(s)
        return t, float(zt @ yt / (zt @ xt))
    t_obs, b_obs = estad(z0)
    rng = np.random.default_rng(seed)
    ts, bs = np.empty(n_perm), np.empty(n_perm)
    for i in range(n_perm):
        if modo == "iid":
            zp = z0[rng.permutation(n)]
        else:
            zp = np.roll(z0, int(rng.integers(L + 1, n - L)))
        ts[i], bs[i] = estad(zp)
    return {"t_obs": float(t_obs), "beta_obs": float(b_obs), "p_perm": float((1 + np.sum(np.abs(ts) >= abs(t_obs))) / (1 + n_perm)),
            "beta_perm_q025": float(np.quantile(bs, 0.025)), "beta_perm_q975": float(np.quantile(bs, 0.975)), "n_perm": n_perm,
            "modo": modo, "n": n}


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
