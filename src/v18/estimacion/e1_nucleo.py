"""V18 · fase 4 · E1 y E6 · núcleo econométrico común: ajuste de paneles con efectos fijos (OLS y 2SLS con AR), efecto mínimo detectable por Monte Carlo
con remuestreo de residuos del periodo previo, estudios de eventos de dosis, placebos y resúmenes.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. SEED = 20261010. Solo importa piezas de _e2e8_comun (Modelo, evento_multi, Webb,
Conley, Moran, Roth, TOST, Honest) y de src/v18/herr18 (iv_debil). Sin lectura de datos: recibe tablas y arrays.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
from herr18 import iv_debil as IV  # noqa: E402

SEMILLA = K.SEMILLA
ALCANCE_TERRITORIAL = "sin lectura de datos"


def codif(a) -> np.ndarray:
    return pd.factorize(pd.Series(np.asarray(a)).astype(str))[0].astype(int)


def dummies(a, base_ultimo: bool = False) -> np.ndarray:
    """Matriz de indicadores de los niveles de a (todas las columnas; Modelo descarta lo colineal)."""
    c = codif(a)
    return (c[:, None] == np.arange(c.max() + 1)[None, :]).astype(float)


def tendencias(grupo, t) -> np.ndarray:
    """Tendencia lineal propia de cada grupo (indicador × t centrado)."""
    t = np.asarray(t, float)
    return dummies(grupo) * (t - t.mean())[:, None]


def interaccion_anio(x, anio) -> np.ndarray:
    """x × indicadores de año (una columna por año): control «distancia al centro × año»."""
    x = np.asarray(x, float)
    return dummies(anio) * x[:, None]


# ------------------------------------------------------------------------------------------------ OLS con efectos fijos
def ajustar(df: pd.DataFrame, y: str, d: str, extra: np.ndarray | None = None, unit: str = "u", time: str = "t", cluster: str = "cl", w: str | None = None,
            webb_B: int = 0, rng: np.random.Generator | None = None, ic_webb: bool = False) -> dict:
    """OLS con efectos fijos de unidad y de periodo (+ extra). CR1 con t(G−1); Webb con el nulo impuesto si webb_B > 0."""
    M = K.Modelo(df[y].values, df[d].values, df[unit].values, df[time].values, extra=extra, w=None if w is None else df[w].values, cluster=df[cluster].values)
    out = {"coef": M.beta, "se": M.se, "t": M.t, "p_t": M.p_t, "ic_t": M.ic_t, "G": M.G, "n": M.n, "k": M.k, "dd": M.dd, "modelo": M}
    if webb_B:
        rng = rng or np.random.default_rng(SEMILLA)
        out["p_webb"] = M.webb_p(0.0, webb_B, rng)
        if ic_webb:
            out["ic_webb"] = M.webb_ic(min(webb_B, 1999), np.random.default_rng(SEMILLA))
    return out


def conley_se(M: "K.Modelo", coords_km: np.ndarray, corte_km: float) -> float:
    return M.conley(coords_km, corte_km)


def sd_intra(df: pd.DataFrame, x: str, unit: str = "u") -> float:
    """Desviación típica intra-unidad de x (de las desviaciones respecto a la media de su unidad)."""
    z = df[x] - df.groupby(unit)[x].transform("mean")
    return float(z.std(ddof=1))


# ------------------------------------------------------------------------------------------------ 2SLS con AR
def iv_ajustar(df: pd.DataFrame, y: str, x: str, z: str, extra: np.ndarray | None = None, unit: str = "u", time: str = "t", cluster: str = "cl",
               w: str | None = None) -> dict:
    """2SLS (una endógena, un instrumento) con efectos fijos y controles parcializados: F efectivo (MOP), 2SLS con t(G−1), AR de Anderson-Rubin por cluster
    (IC exacto y p en β = 0). Devuelve también los vectores parcializados y sumas por cluster para el MDE del AR."""
    M = K.Modelo(df[y].values, df[x].values, df[unit].values, df[time].values, extra=extra, w=None if w is None else df[w].values, cluster=df[cluster].values)
    zt = M._m(M.sw * df[z].values[M.orden])
    cl = np.unique(M.cl_ord, return_inverse=True)[1]
    G = int(cl.max()) + 1
    yt, xt = M.ytil, M.dtil
    Y, X, Z, cl_, G = IV.preparar(yt, xt[:, None], zt[:, None], cl)
    f = float(IV.f_efectivo(X, Z, cl_, G)[0])
    beta, V = IV.dos_sls(Y, X, Z, cl_, G)
    se = float(np.sqrt(V[0, 0]))
    A, C = IV.sumas_ar(Y, X, Z, cl_, G)
    ic = IV.ar_ic_1(A, C, G)
    p_ar = IV.ar_p(A, C, [0.0], G)
    pi = float((Z[:, 0] @ X[:, 0]) / (Z[:, 0] @ Z[:, 0]))        # coeficiente de la primera etapa (con controles parcializados)
    e1 = X[:, 0] - pi * Z[:, 0]
    sc = np.zeros(G)
    np.add.at(sc, cl_, Z[:, 0] * e1)
    se_pi = float(np.sqrt((sc ** 2).sum() * G / (G - 1)) / (Z[:, 0] @ Z[:, 0]))
    rf = float((Z[:, 0] @ Y) / (Z[:, 0] @ Z[:, 0]))               # forma reducida: y sobre z
    e2 = Y - rf * Z[:, 0]
    sc2 = np.zeros(G)
    np.add.at(sc2, cl_, Z[:, 0] * e2)
    se_rf = float(np.sqrt((sc2 ** 2).sum() * G / (G - 1)) / (Z[:, 0] @ Z[:, 0]))
    q = stats.t.ppf(0.975, G - 1)
    return {"beta": float(beta[0]), "se": se, "p_t": float(2 * stats.t.sf(abs(beta[0] / se), G - 1)) if se > 0 else float("nan"), "ic_t": (float(beta[0] - q * se), float(beta[0] + q * se)), "F_efectivo": f,
            "ar_ic": ic, "p_ar": float(p_ar), "pi": pi, "se_pi": se_pi, "rf": rf, "se_rf": se_rf, "p_rf": float(2 * stats.t.sf(abs(rf / se_rf), G - 1)) if se_rf > 0 else float("nan"), "G": G, "n": M.n,
            "A": A, "C": C, "cl": cl_, "Zt": Z[:, 0], "Xt": X[:, 0], "Yt": Y, "modelo": M}


def ar_ic_texto(ic) -> str:
    tipo, lo, hi = ic
    if tipo == "intervalo":
        return f"({lo:.4f}; {hi:.4f})"
    if tipo == "complemento":
        return f"(−∞; {lo:.4f}) ∪ ({hi:.4f}; ∞): no acotado"
    if tipo == "recta":
        return "(−∞; ∞): no acotado"
    return "vacío"


# ------------------------------------------------------------------------------------------------ remuestreo de residuos del periodo previo (MDE)
class PoolResiduos:
    """Residuos de la regresión del PERIODO PREVIO (sección × año), agrupados por cluster. Cada réplica asigna a cada cluster objetivo un cluster donante al azar,
    una ventana temporal circular de longitud T al azar y una sección donante al azar de ese cluster por cada sección objetivo: conserva la correlación serial y la
    correlación dentro del cluster del residuo real, sin mirar el periodo de tratamiento."""

    def __init__(self, R: np.ndarray, cluster_unidad: np.ndarray):
        self.R = np.nan_to_num(np.asarray(R, float))          # (n_unidades, T_pre)
        self.cl = np.asarray(cluster_unidad)
        self.T_pre = self.R.shape[1]
        self.clusters = np.unique(self.cl)
        self.miembros = {c: np.where(self.cl == c)[0] for c in self.clusters}
        self.sd = float(np.sqrt(np.mean(self.R ** 2)))

    def sortear(self, rng: np.random.Generator, T: int) -> np.ndarray:
        n = len(self.cl)
        E = np.empty((n, T))
        donantes = rng.integers(0, len(self.clusters), size=len(self.clusters))
        off = rng.integers(0, self.T_pre, size=len(self.clusters))
        for i, c in enumerate(self.clusters):
            obj = self.miembros[c]
            don = self.miembros[self.clusters[donantes[i]]]
            sel = don[rng.integers(0, len(don), size=len(obj))]
            cols = (off[i] + np.arange(T)) % self.T_pre
            E[obj] = self.R[np.ix_(sel, cols)]
        return E


def mde_ols(M: "K.Modelo", pool: PoolResiduos, unidad_obs: np.ndarray, t_obs: np.ndarray, T: int, R: int = 2000, semilla: int = SEMILLA, lote: int = 100) -> dict:
    """MDE al 80 % (bilateral al 5 %) del coeficiente de M con la inferencia CR1 t(G−1) y la variación REAL del tratamiento (la del diseño M).
    unidad_obs: posición (0..n_unidades−1) de la unidad de cada observación en el orden ORIGINAL de la muestra; t_obs: posición temporal (0..T−1) en la ventana de estimación.
    El resultado simulado es solo el ruido remuestreado: y* = τ·d + e*; β̂(τ) = β̂(0) + τ y el EE no depende de τ (residuo invariante), de modo que la potencia en una rejilla es exacta."""
    rng = np.random.default_rng(semilla)
    ord_ = M.orden
    q = stats.t.ppf(0.975, M.G - 1)
    b0 = np.empty(R)
    se0 = np.empty(R)
    h = 0
    while h < R:
        m = min(lote, R - h)
        Ys = np.empty((M.n, m))
        for j in range(m):
            E = pool.sortear(rng, T)
            Ys[:, j] = E[unidad_obs, t_obs][ord_]
        Z = M.sw[:, None] * Ys
        Zt = Z - M.Q @ (M.Q.T @ Z)
        bb = (M.dtil @ Zt) / M.dd
        ee = Zt - bb[None, :] * M.dtil[:, None]
        s = np.add.reduceat(M.dtil[:, None] * ee, M.inicio, axis=0)
        se = np.sqrt(M.c * (s ** 2).sum(0)) / M.dd
        b0[h:h + m], se0[h:h + m] = bb, se
        h += m
    sd = float(b0.std(ddof=1))
    t0 = np.abs(b0) / se0
    crit_emp = float(np.quantile(t0, 0.95))

    def mde_con(crit: float) -> float:
        grid = np.linspace(0, 8 * max(sd, 1e-9) + crit * float(np.median(se0)) * 2, 3001)
        pot = np.array([np.mean(np.abs(b0 + t) / se0 > crit) for t in grid])
        ok = np.where(pot >= 0.8)[0]
        return float(grid[ok[0]]) if len(ok) else float("nan")

    nominal, corregido = mde_con(q), mde_con(max(q, crit_emp))
    return {"mde80": float(np.nanmax([nominal, corregido])), "mde80_nominal": nominal, "mde80_corregido_tamano": corregido, "sd_beta_placebo": sd, "se_mediana": float(np.median(se0)),
            "tamano_nominal": float(np.mean(t0 > q)), "critico_empirico": crit_emp, "R": int(R), "sigma_residual_previo": pool.sd}


def tamano_webb(d: pd.DataFrame, dcol: str, extra: np.ndarray | None, pool: PoolResiduos, unidad_obs: np.ndarray, t_obs: np.ndarray, T: int, R: int = 400, B: int = 499,
                semilla: int = SEMILLA, unit: str = "u", time: str = "t", cluster: str = "cl") -> dict:
    """Tamaño al 5 % del wild cluster bootstrap de Webb (nulo impuesto) del diseño REAL con el ruido remuestreado del periodo previo (R réplicas, B réplicas bootstrap)."""
    rng = np.random.default_rng(semilla)
    rej = 0
    ps = np.empty(R)
    for r in range(R):
        E = pool.sortear(rng, T)
        y = E[unidad_obs, t_obs]
        M = K.Modelo(y, d[dcol].values, d[unit].values, d[time].values, extra=extra, cluster=d[cluster].values)
        ps[r] = M.webb_p(0.0, B, rng)
    return {"tamano_webb_5pct": float(np.mean(ps < 0.05)), "R_webb": int(R), "B_webb": int(B)}


def mde_iv_ar(res: dict, pool: PoolResiduos, unidad_obs: np.ndarray, t_obs: np.ndarray, T: int, R: int = 2000, semilla: int = SEMILLA, lote: int = 100) -> dict:
    """MDE al 80 % del contraste de Anderson-Rubin de β = 0 (cluster) con la primera etapa y el instrumento REALES; resultado = τ·x + e*. Como A_g(τ) = A_g(e*) + τ·C_g,
    la potencia en una rejilla de τ es exacta. Si el AR no puede alcanzar el 80 % en la rejilla, MDE = NaN («no estimable por variación»)."""
    M = res["modelo"]
    rng = np.random.default_rng(semilla)
    ord_ = M.orden
    cl, G, Zt, Xt = res["cl"], res["G"], res["Zt"], res["Xt"]
    C = np.zeros(G)
    np.add.at(C, cl, Zt * Xt)
    crit = stats.chi2.ppf(0.95, 1) * G / (G - 1)
    Ae = np.zeros((R, G))
    h = 0
    while h < R:
        m = min(lote, R - h)
        Ys = np.empty((M.n, m))
        for j in range(m):
            E = pool.sortear(rng, T)
            Ys[:, j] = E[unidad_obs, t_obs][ord_]
        Z = M.sw[:, None] * Ys
        Yt = Z - M.Q @ (M.Q.T @ Z)
        for j in range(m):
            np.add.at(Ae[h + j], cl, Zt * Yt[:, j])
        h += m
    cs = C.sum()
    scale = float(np.sqrt((Ae.sum(1) ** 2).mean()) / max(abs(cs), 1e-6))
    grid = np.concatenate([[0.0], np.geomspace(0.02 * scale, 600 * scale, 1500)])
    pot = np.empty(len(grid))
    for i, t in enumerate(grid):
        A = Ae + t * C[None, :]
        num = A.sum(1) ** 2
        den = (A ** 2).sum(1)
        pot[i] = np.mean(num > crit * den)
    ok = np.where(pot >= 0.8)[0]
    mde = float(grid[ok[0]]) if len(ok) else float("nan")
    return {"mde80": mde, "tamano_nominal": float(pot[0]), "R": int(R), "sigma_residual_previo": pool.sd, "potencia_max": float(pot.max()), "rejilla_max": float(grid[-1]), "potencia_en_umbral": None}


def residuos_previos_fe(d: pd.DataFrame, y: str, unit: str, anio: str, anios: list[int], extra_fun=None) -> tuple[np.ndarray, list]:
    """Residuos de y tras efectos fijos de unidad y de año (+ columnas extra opcionales por función de d) en el periodo previo, panel desequilibrado permitido
    (los huecos quedan en 0 en la matriz). Devuelve (R unidades × años, unidades)."""
    d = d[d[anio].isin(anios)].reset_index(drop=True)
    u = codif(d[unit])
    t = codif(d[anio])
    ex = None if extra_fun is None else extra_fun(d)
    ruido = np.random.default_rng(1).normal(size=len(d))           # regresor ficticio: solo se quiere el residuo de los efectos fijos y extra
    M = K.Modelo(d[y].values, ruido, u, t, extra=ex)
    res = M.ytil                                                    # y residualizado respecto de los efectos fijos y extra (sin el regresor ficticio)
    r = pd.DataFrame({"u": u[M.orden], "t": t[M.orden], "r": res})
    mat = r.pivot_table(index="u", columns="t", values="r", aggfunc="first").reindex(range(u.max() + 1)).reindex(columns=range(t.max() + 1))
    unidades = pd.Series(d[unit].values, index=u).groupby(level=0).first().reindex(range(u.max() + 1)).tolist()
    return mat.values, unidades


# ------------------------------------------------------------------------------------------------ estudios de eventos de dosis
def evento_dosis(df: pd.DataFrame, y: str, dosis: str, anios: list[int], base: int, unit: str = "u", time: str = "t", cluster: str = "cl", col_anio: str = "anio",
                 extra: np.ndarray | None = None) -> dict:
    """Coeficientes β_k de dosis × 1[año = k] (k ≠ base) con efectos fijos de unidad y de año; covarianza agrupada. Devuelve b, V, años, G, y la diferencia de la
    media de los coeficientes posteriores (k > base) si se pide aparte."""
    ks = [k for k in anios if k != base]
    D = np.column_stack([(df[col_anio].values == k) * df[dosis].values for k in ks])
    r = K.evento_multi(df[y].values, D, df[unit].values, df[time].values, extra=extra, cluster=df[cluster].values)
    return {"anios": ks, "b": r["b"], "V": r["V"], "G": r["G"], "k": r["k"]}


def pretendencias(ev: dict, base: int) -> dict:
    """Contraste conjunto de los adelantos (k < base) con F(k, G−1) y pendiente lineal previa detectable al 80 % (Roth, 2022); sesgo implicado en el posterior."""
    ks = np.array(ev["anios"])
    pre = ks < base
    post = ks > base
    b, V = ev["b"], ev["V"]
    out = {"n_pre": int(pre.sum()), "n_post": int(post.sum())}
    if pre.sum() == 0:
        out.update({"p": float("nan"), "pendiente_detectable": float("nan"), "sesgo_post": float("nan")})
        return out
    W, p = K.wald_conjunto(b[pre], V[np.ix_(pre, pre)], ev["G"])
    ell = (ks[pre] - base).astype(float)               # pendiente lineal: efecto = δ (k − base)
    delta = K.roth_pendiente(V[np.ix_(pre, pre)], ell)
    sesgo = float(np.mean(delta * (ks[post] - base))) if post.sum() else float("nan")
    out.update({"p": p, "wald": W, "pendiente_detectable": delta, "sesgo_post": sesgo})
    return out


def media_posterior(ev: dict, base: int) -> dict:
    ks = np.array(ev["anios"])
    post = ks > base
    l = np.zeros(len(ks))
    l[post] = 1.0 / post.sum()
    b = float(l @ ev["b"])
    se = float(np.sqrt(l @ ev["V"] @ l))
    gl = ev["G"] - 1
    q = stats.t.ppf(0.975, gl)
    return {"coef": b, "se": se, "p_t": float(2 * stats.t.sf(abs(b / se), gl)), "ic_t": (b - q * se, b + q * se), "G": ev["G"]}


def honest_dosis(ev: dict, base: int, Mbars=(0.0, 0.5, 1.0)) -> list[dict]:
    """Honest DiD (Rambachan-Roth, magnitudes relativas) con la covarianza agrupada del estudio de eventos de dosis. Solo informativo (M̄ = 0 apto en el Monte Carlo de V18)."""
    from herr18 import honest_did as HON
    ks = np.array(ev["anios"])
    pre, post = np.where(ks < base)[0], np.where(ks > base)[0]
    idx = list(pre) + list(post)
    b, V = ev["b"][idx], ev["V"][np.ix_(idx, idx)]
    G, k = ev["G"], len(idx)
    if G > k + 1:
        V = V * (G - 1) / (G - k)
    out = []
    for Mb in Mbars:
        lo, hi = HON.ic(b, V, len(pre), len(post), Mb)
        out.append({"Mbar": Mb, "ic95": (lo, hi), "excluye_cero": bool(np.isfinite(lo) and (lo > 0 or hi < 0)), "G": G, "k": k, "rango_V": int(np.linalg.matrix_rank(V)),
                    "lectura": "apto (M̄ = 0)" if Mb == 0 else "válido pero conservador; informativo"})
    return out


# ------------------------------------------------------------------------------------------------ utilidades de resumen
def by(pvals: list[float], q: float = 0.10) -> list[float]:
    """q-valores de Benjamini-Yekutieli."""
    from statsmodels.stats.multitest import multipletests
    p = np.array(pvals, float)
    ok = np.isfinite(p)
    out = np.full(len(p), np.nan)
    if ok.sum():
        out[ok] = multipletests(p[ok], method="fdr_by")[1]
    return out.tolist()


def hechos_tabla(filas: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(filas)
