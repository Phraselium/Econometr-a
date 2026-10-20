"""V18 · E2 · estimación y pruebas B4 de las especificaciones que superan la estimabilidad (adenda 1.3).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Se llama desde e2_topes.py después de e2_diseno.estimabilidad().
Inferencia (B2 + adenda 1.12): CR1 por municipio (t de G−1 gl) y wild cluster bootstrap de Webb con el nulo impuesto (principal; 9.999 réplicas),
Webb por conglomerado espacial de 42 grupos (sustituto de las comarcas, que no están en el repositorio), aleatorización entre municipios y dentro
del conglomerado, Conley a 10 km y Driscoll-Kraay (esta última «no fiable» según su Monte Carlo: solo se rotula).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_datos as D  # noqa: E402
import e2_diseno as DS  # noqa: E402
from herramientas import aleatorizacion as ALE  # noqa: E402
from herramientas.did import CallawaySantAnna  # noqa: E402
from herramientas.driscoll_kraay import fe_dk  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
SEED = K.SEMILLA
ANT_COL, BASE_COL, POST_COLS = 6, 3, list(range(7, 13))          # 2020T3, 2019T4 y 2020T4-2022T1 en PER13
TAM_WEBB_MUN = 0.071    # cs_webb · cat_trim_M · webb_WCR_t_cluster_principal (con valor crítico corregido)
TAM_ALEAT_MUN = 0.0635  # aleatorizacion · E2_cat_trim_M · permuta_entre_municipios_estudentizada


# --------------------------------------------------------------------------------------------- construcción
def extra_paro(d: dict, cods, per: list[str]) -> np.ndarray:
    """ln(1 + paro registrado) trimestral: media trimestral del fichero mensual del SEPE (adenda R-1; K9)."""
    pt = d["paro_trim"].reindex(cods)
    return np.column_stack([np.log1p(pt[p].values) for p in per])


def twfe_panel(Y, tr, post_cols, ant_cols=(), extras=(), w=None, cluster=None, drop_cols=()) -> K.Modelo:
    N, T = Y.shape
    keep = [j for j in range(T) if j not in set(drop_cols)]
    nuevo = {j: i for i, j in enumerate(keep)}
    Y = Y[:, keep]
    postv = np.zeros(len(keep))
    postv[[nuevo[j] for j in post_cols if j in nuevo]] = 1.0
    d = (tr[:, None] * postv[None, :]).ravel()
    ex = []
    if len(ant_cols):
        av = np.zeros(len(keep))
        av[[nuevo[j] for j in ant_cols if j in nuevo]] = 1.0
        ex.append((tr[:, None] * av[None, :]).ravel())
    for m in extras:
        ex.append(np.asarray(m, float)[:, keep].ravel())
    unit = np.repeat(np.arange(N), len(keep))
    time = np.tile(np.arange(len(keep)), N)
    return K.Modelo(Y.ravel(), d, unit, time, extra=np.column_stack(ex) if ex else None,
                    w=None if w is None else np.repeat(w, len(keep)), cluster=unit if cluster is None else np.repeat(cluster, len(keep)))


def inferir(m: K.Modelo, B: int, B_ic: int, ic: bool = True, semilla: int = SEED) -> dict:
    out = {"coef": m.beta, "se": m.se, "p_cr1": m.p_t, "ic_cr1": m.ic_t, "G": m.G, "n_obs": m.n,
           "p_webb": m.webb_p(0.0, B, np.random.default_rng(semilla))}
    out["p_webb_i7"] = K.p_corr(out["p_webb"], TAM_WEBB_MUN)
    out["ic_webb"] = m.webb_ic(B_ic, np.random.default_rng(semilla)) if ic else (np.nan, np.nan)
    return out


def aleatorizar(Y, tr, pre, post, B: int, estrato=None, semilla: int = SEED) -> dict:
    """Aleatorización de Fisher estudentizada sobre el cambio por unidad (media posterior − media previa); entre municipios o dentro de estrato."""
    d = Y[:, post].mean(1) - Y[:, pre].mean(1)
    rng = np.random.default_rng(semilla)
    lab = tr.astype(bool)
    perms = ALE.etiquetas_individual(rng, lab, B) if estrato is None else ALE.etiquetas_estrato(rng, lab, np.asarray(estrato), B)
    p = ALE.p_did(d, lab, 0.0, perms)
    a, s = ALE.did_welch(d, lab)
    ic = K.ic_por_p(lambda t0: ALE.p_did(d, lab, t0, perms), float(a), float(s))
    return {"p": p, "p_i7": K.p_corr(p, TAM_ALEAT_MUN), "att": float(a), "ic": ic}


def conglomerados(p: dict, d: dict) -> np.ndarray:
    return np.array([d["geo"]["conglomerado"][c] for c in p["cod"]])


def coords(p: dict, d: dict) -> np.ndarray:
    return d["geo"]["xy"][[d["geo"]["idx"][c] for c in p["cod"]]]


# --------------------------------------------------------------------------------------------- estudio de eventos y pruebas de I3
def evento_trimestral(Y, tr, extras=(), cols=None, base=BASE_COL) -> dict:
    """Estudio de eventos TWFE (coeficientes Reg × 1[t = k], base 2019T4), con la covarianza agrupada por municipio."""
    N, T = Y.shape
    cols = list(range(T)) if cols is None else cols
    ks = [k for k in cols if k != base]
    Dm = np.column_stack([(tr[:, None] * (np.arange(T) == k)[None, :]).ravel() for k in ks])
    unit = np.repeat(np.arange(N), T)
    time = np.tile(np.arange(T), N)
    ex = np.column_stack([np.asarray(m)[:, :].ravel() for m in extras]) if len(extras) else None
    ev = K.evento_multi(Y.ravel(), Dm, unit, time, extra=ex, cluster=unit)
    b, V = ev["b"], ev["V"]
    leads = [i for i, k in enumerate(ks) if k < ANT_COL and k != base]
    bl, Vl = b[leads], V[np.ix_(leads, leads)]
    W, p = K.wald_conjunto(bl, Vl, ev["G"])
    ell = np.array([ks[i] - base for i in leads], float)
    d80 = K.roth_pendiente(Vl, ell)
    sesgo = d80 * float(np.mean([k - base for k in POST_COLS]))
    tabla = pd.DataFrame({"k": ks, "coef": b, "se": np.sqrt(np.diag(V))})
    return {"tabla": tabla, "wald": W, "p_pretend": p, "n_leads": len(leads), "pendiente_detectable": d80, "sesgo_post": sesgo,
            "anticipacion": float(b[ks.index(ANT_COL)]) if ANT_COL in ks else np.nan}


def honest_trimestral(Y, tr) -> list[dict]:
    """Honest DiD (magnitudes relativas) con la muestra comprimida sin 2020T1-2020T3: previos 2019T1-T3, referencia 2019T4, posteriores 2020T4-2022T1.
    Monte Carlo de V18: solo M̄ = 0 es apto; con M̄ = 0,5 y 1 es válido pero conservador (tamaño ≈ 0): informativo, no criterio."""
    cols = [0, 1, 2, 3] + POST_COLS
    Y2 = Y[:, cols]
    cl = np.arange(len(Y2))
    out = []
    for Mbar in (0.0, 0.5, 1.0):
        r = K.honest_ic(Y2, tr.astype(bool), cl, 3, [0, 1, 2], list(range(4, 4 + len(POST_COLS))), Mbar)
        r["lectura"] = "apto (Monte Carlo)" if Mbar == 0 else "válido pero conservador: informativo, no criterio"
        out.append(r)
    return out


# --------------------------------------------------------------------------------------------- paneles anuales
def panel_anual(d: dict, serie: str, anios: list[str], post: list[str], con_barcelona: bool = False, por_mil_hab: bool = False,
                solo_tratados_en: set | None = None) -> dict:
    """Panel anual (equilibrado) de log(serie) o log(serie por 1.000 hab.). Tratados: Ley 11/2020 (sin Barcelona ciudad salvo con_barcelona);
    controles: no regulados con crecimiento de la renta 2014-2019 > 4,15 % (criterio de JMS)."""
    A = d[serie].reindex(columns=anios)
    ok = A.notna().all(axis=1) & (A > 0).all(axis=1)
    if por_mil_hab:
        ok &= d["pop"].reindex(A.index)[anios].notna().all(axis=1)
    gr = DS.crecimiento_2014_2019(d["rA"])
    ley = d["ley"]
    cods = [c for c in A.index[ok]]
    tr = [c for c in cods if c in ley and (con_barcelona or c != D.BARCELONA)]
    co = [c for c in cods if c not in ley and c != D.BARCELONA and gr.get(c, np.nan) > 0.0415]
    sel = tr + co
    Y = np.log(A.loc[sel].values)
    if por_mil_hab:
        Y = Y - np.log(d["pop"].loc[sel, anios].values) + np.log(1000)
    return {"cod": np.array(sel), "Y": Y, "tr": np.array([c in set(tr) for c in sel]), "cols": anios, "n_tr": len(tr), "n_co": len(co),
            "post_cols": [anios.index(a) for a in post]}


def twfe_anual(p: dict, post_cols=None, falso_desde: str | None = None) -> K.Modelo:
    cols = p["cols"]
    pc = p["post_cols"] if post_cols is None else post_cols
    if falso_desde is not None:
        pc = [i for i, a in enumerate(cols) if a >= falso_desde]
    return twfe_panel(p["Y"], p["tr"], pc)


def honest_anual(p: dict, pre: list[str], ref: str, post: list[str]) -> list[dict]:
    cols = p["cols"]
    out = []
    ix = lambda xs: [cols.index(x) for x in xs]  # noqa: E731
    for Mbar in (0.0, 0.5, 1.0):
        out.append(K.honest_ic(p["Y"], p["tr"], np.arange(len(p["Y"])), cols.index(ref), ix(pre), ix(post), Mbar))
    return out


# --------------------------------------------------------------------------------------------- especificaciones trimestrales (R1, R1c y variantes)
def panel_matching(d: dict, resultado: str) -> dict:
    """E2-R1-v3: controles por covariables. Para cada tratado, el municipio no regulado más cercano (con reposición) en ln(población 2019),
    distancia a Barcelona y ln(1 + paro 2019), estandarizados con la desviación típica del conjunto. Los controles llevan como peso el número de veces elegidos."""
    p = DS.panel_r1(d, resultado, grupo_control="todos")
    cods = list(p["cod"])
    geo = d["geo"]
    bcn = geo["xy"][geo["idx"][D.BARCELONA]]
    pop = d["pop"].reindex(cods)["2019"].values
    paro = DS.paro_interp(d["paro"]).reindex(cods)["2019"].values
    dist = np.array([np.sqrt(((geo["xy"][geo["idx"][c]] - bcn) ** 2).sum()) for c in cods])
    X = np.column_stack([np.log(pop), dist, np.log1p(paro)])
    ok = np.isfinite(X).all(axis=1)
    X = (X - np.nanmean(X[ok], 0)) / np.nanstd(X[ok], 0)
    tr = p["tr"] & ok
    co_idx = np.where(~p["tr"] & ok)[0]
    cuenta = np.zeros(len(cods))
    for i in np.where(tr)[0]:
        j = co_idx[np.argmin(((X[co_idx] - X[i]) ** 2).sum(1))]
        cuenta[j] += 1
    sel = tr | (cuenta > 0)
    q = {k: (v[sel] if isinstance(v, np.ndarray) else v) for k, v in p.items()}
    q["tr"] = tr[sel]
    q["w"] = np.where(tr[sel], 1.0, cuenta[sel])
    q["n_tr"], q["n_co"] = int(tr.sum()), int((cuenta > 0).sum())
    return q


def spec_trim(d: dict, resultado: str = "renta", *, con_barcelona=False, grupo="jms", drop=(), ant=(ANT_COL,), covar=None, pesos=None,
              sin_p99=False, matching=False, post=POST_COLS) -> tuple[K.Modelo, dict]:
    """K9: la principal de la renta lleva ln(1 + paro trimestral) como covariable (adenda R-1); covar="ninguna" es la variante sin paro (v5)."""
    if covar is None:
        covar = "paro" if resultado == "renta" else "ninguna"
    p = panel_matching(d, resultado) if matching else DS.panel_r1(d, resultado, con_barcelona=con_barcelona, grupo_control=grupo,
                                                                    con_paro=(covar in ("paro", "hut") and resultado == "renta"))
    keep = np.ones(len(p["cod"]), bool)
    c19 = d["cT"].reindex(p["cod"])[["2019T1", "2019T2", "2019T3", "2019T4"]].sum(axis=1).values
    if sin_p99:
        keep = c19 < np.quantile(c19, 0.99)
    q = {k: (v[keep] if isinstance(v, np.ndarray) and len(v) == len(keep) else v) for k, v in p.items()}
    q["n_tr"], q["n_co"] = int(q["tr"].sum()), int((~q["tr"]).sum())
    w = q.get("w")
    if pesos == "contratos2019":
        w = c19[keep]
    extras = []
    if covar in ("paro", "hut") and resultado == "renta":      # la variante HUT va sobre la principal (con paro)
        extras.append(extra_paro(d, q["cod"], q["cols"]))
    if covar == "hut":
        pop19 = d["pop"].reindex(q["cod"])["2019"].values
        hut = d["hut"].reindex(q["cod"]).get("2019", pd.Series(0.0, index=q["cod"])).fillna(0.0).values
        dens = hut / pop19 * 1000.0
        pv = np.zeros(len(q["cols"]))
        pv[[j for j in post]] = 1.0
        extras.append(dens[:, None] * pv[None, :])
    m = twfe_panel(q["Y"], q["tr"], post, ant, extras, w=w, drop_cols=drop)
    return m, q


def ppml(d: dict, p: dict, drop=()) -> dict:
    """PPML de los contratos (nivel) con efectos de municipio y trimestre y desplazamiento ln(población); coeficiente = semielasticidad."""
    per = p["cols"]
    cod = list(p["cod"])
    c = d["cT"].loc[cod, per].values
    lp = DS.ln_pop_trimestral(d["pop"], cod, per)
    keep = [j for j in range(len(per)) if j not in drop]
    N = len(cod)
    rows = []
    for j in keep:
        for i in range(N):
            rows.append((i, j, c[i, j], lp[i, j], float(p["tr"][i] and j in POST_COLS), float(p["tr"][i] and j == ANT_COL)))
    df = pd.DataFrame(rows, columns=["u", "t", "y", "off", "d", "ant"])
    X = pd.concat([df[["d", "ant"]], pd.get_dummies(df.u, prefix="u", drop_first=True, dtype=float), pd.get_dummies(df.t, prefix="t", drop_first=True, dtype=float)], axis=1)
    X.insert(0, "const", 1.0)
    r = sm.GLM(df.y.values, X.values, family=sm.families.Poisson(), offset=df.off.values).fit(cov_type="cluster", cov_kwds={"groups": df.u.values}, maxiter=100)
    return {"coef": float(r.params[1]), "se": float(r.bse[1]), "p_cr1": float(r.pvalues[1]), "G": N,
            "ic_cr1": (float(r.params[1] - 1.96 * r.bse[1]), float(r.params[1] + 1.96 * r.bse[1])), "n_obs": len(df)}


# --------------------------------------------------------------------------------------------- coprincipales de V9 (CS nunca tratados)
def panel_d1b(d: dict, resultado: str) -> dict:
    """V9-D1b exacta en la muestra V18: todos los municipios con la serie > 0 en los 13 trimestres 2019T1-2022T1 (sin criterio de crecimiento),
    Ley 11/2020 tratada desde 2020T4 (incluye Barcelona ciudad), resto nunca tratados."""
    per = D.PER13
    w = d["rT"][per] if resultado == "renta" else d["cT"][per]
    ok = w.notna().all(axis=1) & (w > 0).all(axis=1)
    cods = list(ok[ok].index)
    g = np.array([7 if c in d["ley"] else -1 for c in cods])
    return {"cod": np.array(cods), "Y": np.log(w.loc[cods].values), "g": g, "cols": per, "n_tr": int((g >= 0).sum()), "n_co": int((g < 0).sum())}


def cs_p(p: dict, B: int, B_ic: int, semilla: int = SEED) -> dict:
    T = p["Y"].shape[1]
    cs = CallawaySantAnna(p["g"], np.arange(len(p["g"])), T)
    pv, att, se = cs.p_valor(p["Y"], 0.0, np.random.default_rng(semilla), B)
    ic = K.ic_por_p(lambda b0: cs.p_valor(p["Y"], b0, np.random.default_rng(semilla), B_ic)[0], att, se)
    return {"coef": att, "se": se, "p_webb": pv, "p_webb_i7": K.p_corr(pv, TAM_WEBB_MUN), "ic_webb": ic, "G": len(p["g"]), "n_obs": p["Y"].size}


def dk_trimestral(m_p: dict, Y, tr, ant, extras=()) -> dict:
    """Driscoll-Kraay (rotulado «no fiable» por su Monte Carlo): coeficiente de Reg × Post con EE de Newey-West a través de los periodos."""
    N, T = Y.shape
    postv = np.zeros(T)
    postv[POST_COLS] = 1
    X = [tr[:, None] * postv[None, :], tr[:, None] * (np.arange(T) == ant)[None, :]] + list(extras)
    r = fe_dk(Y, np.stack(X, axis=2), tiempo=True)
    se = float(np.sqrt(r["V_dk"][0, 0]))
    from scipy import stats
    t = float(r["beta"][0] / se)
    return {"coef": float(r["beta"][0]), "se": se, "p": float(2 * stats.t.sf(abs(t), T - 1)), "m": r["m"]}
