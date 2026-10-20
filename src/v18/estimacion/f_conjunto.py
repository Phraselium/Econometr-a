"""V18 · fase 4 · modelos de conjunto F1 (precio de largo plazo), F2 (alquiler equivalente), F3 (oferta) y F4 (coherencia, solo si procede).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md, sección 2, y adenda: regla AD-F).
Determinista (SEED = 20261010), sin red. Los datos pasan siempre por src/v18/sellado.filtrar (f_datos.py), que aplica holdout.excluir_sellados_v6() y los bloques de
V15 y V16; nunca data/sealed.

Regla de la adenda (AD-F): si el contraste de límites del ARDL (F1-R1, F1-A2) o el contraste de cointegración de panel (F1-R2, F1-A1, F2-R1, F2-A1,
F3-A2) no rechaza la ausencia de cointegración al 5 % tras Holm (valores críticos por Monte Carlo del propio diseño), no se publican elasticidades
de largo plazo de ese modelo, ni la sobrevaloración (F1-A3), ni las comparaciones de F4 que lo usan; solo se publica la dinámica de corto plazo,
como ASOCIACIÓN. Herramientas NO APTAS en el Monte Carlo previo (Driscoll-Kraay con T <= 30, CS-ARDL, Westerlund, CIPS) no clasifican: se publican con
su etiqueta.

Uso: python3 src/v18/estimacion/f_conjunto.py [--rapido]   (--rapido: menos réplicas, solo para pruebas; la salida oficial es la completa)
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_datos as D  # noqa: E402
import f_nucleo as N  # noqa: E402

RAIZ = N.RAIZ
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, dm_test, holm  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = RAIZ / "output" / "v18" / "estimacion" / "f_conjunto"
ROTULO = "análisis V18; capa C4; pre-registro interno plan-replicacion-v18"
CAPA = "C4"
EXCL_0813 = ("2008Q1", "2013Q4")
NO_APTO = {"driscoll_kraay_T<=30": "NO APTO (tamaño 0,16-0,28 con T = 14-30; V18 montecarlo/driscoll_kraay)",
           "csardl": "NO APTO (tamaño 0,10; V16 montecarlo/csardl y V15 westerlund_csardl)",
           "westerlund_cips": "NO APTO (tamaño 0,09-0,20 y 0,01; V15/V16)",
           "cluster_sin_efectos_de_anio": "NO APTO (tamaño 0,48-0,51 sin efectos de año; V18 montecarlo/driscoll_kraay)"}

FUENTE_NAC = ["base:p_tasado (MIVAU, valor tasado nacional) hasta 2026T2", "base:deflactor hasta 2026T2", "base:renta_hog_real (INE CNT; cálculo propio) hasta 2026T2",
              "base:tipo_hip_real_bde hasta 2026T2", "base:pob_total (INE ECP; 44 trimestres interpolados 1999-2020)"]
FUENTE_PAN = ["base:valor_tasado provincial anual (MIVAU) hasta 2024", "data/raw/ine_v2_cre.csv (PIB provincial, sustituto de la renta de los hogares)",
              "base:parados_epa y base:ocupados_epa provinciales (INE EPA) hasta 2024", "base:pob_total provincial (INE ECP) hasta 2024",
              "base:tipo_hip_bde nacional", "data/raw/mivau_parque.csv (parque de viviendas provincial)", "base:deflactor nacional"]

REG: Registry | None = None
FILAS: list[dict] = []
HECHOS: list[dict] = []
RES: dict[str, dict] = {}
PVALS_COINT: dict[str, float] = {}


def num(x, d=4):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), d)


def log_pre(id_, formula, ini, fin, notas=""):
    """Registro en el Registry ANTES de leer ningún resultado (adenda 1.3, regla de registro)."""
    REG.log("F-prereg", id_, formula, ini, fin, 0, np.nan, np.nan, np.nan, notas=notas)


def log_post(id_, formula, ini, fin, n, coef, p, notas=""):
    REG.log("F", id_, formula, ini, fin, n, np.nan, np.nan, np.nan, coef_interes=coef, p_interes=p, notas=notas)


def by_adjust(p: list[float]) -> list[float]:
    """Benjamini-Yekutieli (dependencia arbitraria) para las variantes de un identificador."""
    p = np.asarray(p, float)
    m = len(p)
    if m == 0:
        return []
    c = np.sum(1.0 / np.arange(1, m + 1))
    o = np.argsort(p)
    q = np.empty(m)
    run = 1.0
    for rank in range(m, 0, -1):
        i = o[rank - 1]
        run = min(run, p[i] * m * c / rank)
        q[i] = run
    return q.tolist()


# ---------------------------------------------------------------------------------------------- diagnósticos de serie temporal
def adf_kpss(s: pd.Series) -> dict:
    from statsmodels.tsa.stattools import adfuller, kpss
    s = s.dropna()
    a = adfuller(s, regression="c", autolag="AIC")
    ad = adfuller(s.diff().dropna(), regression="c", autolag="AIC")
    try:
        k = kpss(s, regression="c", nlags="auto")[1]
    except Exception:
        k = np.nan
    return {"adf_p_niveles": num(a[1]), "adf_p_diferencias": num(ad[1]), "kpss_p_niveles": num(k)}


def sup_f_ruptura(W, dep, fechas_idx: list[int], trim: float = 0.15):
    n, m = W.shape
    b = np.linalg.lstsq(W, dep, rcond=None)[0]
    rss_r = float(((dep - W @ b) ** 2).sum())

    def chow(s):
        b1 = np.linalg.lstsq(W[:s], dep[:s], rcond=None)[0]
        b2 = np.linalg.lstsq(W[s:], dep[s:], rcond=None)[0]
        rss_u = float(((dep[:s] - W[:s] @ b1) ** 2).sum() + ((dep[s:] - W[s:] @ b2) ** 2).sum())
        return ((rss_r - rss_u) / m) / (rss_u / (n - 2 * m))
    fijos = {i: chow(i) for i in fechas_idx if m + 2 < i < n - m - 2}
    lo, hi = int(trim * n), int((1 - trim) * n)
    sup = max(chow(s) for s in range(max(lo, m + 2), min(hi, n - m - 2)))
    return fijos, float(sup)


def cd_pesaran(E: np.ndarray) -> dict:
    """CD de Pesaran (2004) sobre una matriz de residuos (N, T)."""
    n, t = E.shape
    c = np.corrcoef(E)
    r = c[np.triu_indices(n, 1)]
    cd = np.sqrt(2 * t / (n * (n - 1))) * r.sum()
    return {"CD": num(cd), "p": num(2 * stats.norm.sf(abs(cd))), "rho_medio": num(r.mean())}


# ---------------------------------------------------------------------------------------------- MDE
def mde_serie(y, X, rho: float = 0.8, R: int = 2000) -> dict:
    """MDE de la elasticidad del primer regresor en niveles (OLS con errores de Newey-West 4) con la variación real de X y ruido AR(1)
    de σ igual a la desviación típica del residuo estático del resultado (declarado «ya visto»: no hay σ de V15/V16 para esta unidad)."""
    X1 = np.column_stack([np.ones(len(y)), X])
    b, e, _, _ = N.mco(y, X1)
    sd = float(e.std(ddof=X1.shape[1]))
    n = len(y)
    P = np.linalg.pinv(X1.T @ X1)

    def sim(rng):
        u = rng.normal(size=n) * sd * np.sqrt(1 - rho ** 2)
        z = np.empty(n)
        z[0] = rng.normal() * sd
        for i in range(1, n):
            z[i] = rho * z[i - 1] + u[i]
        bb = P @ (X1.T @ z)
        ee = z - X1 @ bb
        s = X1 * ee[:, None]
        S = s.T @ s
        for j in range(1, 5):
            G = s[j:].T @ s[:-j]
            S += (1 - j / 5) * (G + G.T)
        V = P @ S @ P
        return bb[1], float(np.sqrt(V[1, 1]))
    r = N.mde_mc(sim, R, SEED)
    r.update({"sigma_declarado": num(sd), "rho_declarado": rho, "origen_sigma": "residuo estático de la misma muestra (ya visto)"})
    return r


def mde_panel(Y, X, R: int = 2000) -> dict:
    """MDE de la elasticidad del primer regresor en el DOLS de panel con efectos fijos y Driscoll-Kraay: ruido AR(1) (ρ = 0,8) por unidad con σ de
    los residuos del DOLS de la propia muestra («ya visto»; no hay σ de V15/V16 para el valor tasado provincial anual)."""
    n, t, k = X.shape
    tt = np.arange(2, t - 1)
    Xa = np.concatenate([X[:, tt, :]] + [N.lead_lag(X, j) for j in (-1, 0, 1)], axis=2)
    r0 = DK_fit(Y[:, tt], Xa)
    sd = float(np.sqrt(np.mean(r0["e"] ** 2)))
    rho = 0.8

    def sim(rng):
        u = rng.normal(size=(n, len(tt))) * sd * np.sqrt(1 - rho ** 2)
        z = np.empty_like(u)
        z[:, 0] = rng.normal(size=n) * sd
        for i in range(1, u.shape[1]):
            z[:, i] = rho * z[:, i - 1] + u[:, i]
        r = N.DK.fe_dk(z, Xa)
        return float(r["beta"][0]), float(np.sqrt(r["V_dk"][0, 0]))
    out = N.mde_mc(sim, R, SEED)
    out.update({"sigma_declarado": num(sd), "rho_declarado": rho, "origen_sigma": "residuos del DOLS de la propia muestra (ya visto)"})
    return out


def DK_fit(y, X):
    yt = y - y.mean(1, keepdims=True)
    Xt = X - X.mean(1, keepdims=True)
    b = np.linalg.solve(np.einsum("itp,itq->pq", Xt, Xt), np.einsum("itp,it->p", Xt, yt))
    return {"beta": b, "e": yt - Xt @ b}


# ---------------------------------------------------------------------------------------------- F1 nacional
def fuera_de_muestra(n: pd.DataFrame, xs: list[str], ini: str, fin: str) -> dict:
    """Predicción a un paso de Δ ln precio real en bloques con embargo (K = 5, embargo 4 trimestres), misma muestra para todos los modelos:
    AR(4); ECM v1 aproximado (Δy sobre y_{t-1} y X_{t-1}, como en v6); F1-ECM = AR(4) + y_{t-1}, X_{t-1}, ΔX_{t-1} (anida al AR(4): Clark-West);
    y deriva constante. Pérdida cuadrática; DM con HLN, CW, GW y MCS (T_max, bloques de 4)."""
    d = n.loc[ini:fin]
    y = d["y"].to_numpy()
    X = d[xs].to_numpy()
    T = len(y)
    dy = np.full(T, np.nan)
    dy[1:] = np.diff(y)
    dX = np.vstack([np.full((1, len(xs)), np.nan), np.diff(X, axis=0)])

    def lag(a, l):
        o = np.full_like(a, np.nan, dtype=float)
        o[l:] = a[:-l]
        return o
    L = [lag(dy, l) for l in range(1, 5)]
    ar4 = np.column_stack([np.ones(T)] + L)
    ecm1 = np.column_stack([np.ones(T), lag(y, 1), lag(X, 1)])
    f1 = np.column_stack([ar4, lag(y, 1), lag(X, 1), lag(dX, 1)])
    deriva = np.ones((T, 1))
    err, pred, idx = N.pred_bloques(dy, {"AR(4)": ar4, "ECM v1 (aprox.)": ecm1, "F1-ECM": f1, "deriva": deriva}, K=5, embargo=4)
    rmse = {k: num(np.sqrt(np.mean(v ** 2)) * 100) for k, v in err.items()}
    dm = {k: dm_test(err["F1-ECM"], err[k], h=1) for k in ("AR(4)", "ECM v1 (aprox.)")}
    cw = N.clark_west(err["AR(4)"], err["F1-ECM"], pred["AR(4)"], pred["F1-ECM"])
    gw = {k: N.giacomini_white(err["F1-ECM"], err[k]) for k in ("AR(4)", "ECM v1 (aprox.)")}
    m = N.mcs({k: v ** 2 for k, v in err.items()}, B=999, alfa=0.10, seed=SEED)
    return {"n_prueba": int(len(idx)), "rmse_pct": rmse, "dm_F1ECM_vs_AR4": {k: num(v) for k, v in dm["AR(4)"].items()},
            "dm_F1ECM_vs_ECMv1": {k: num(v) for k, v in dm["ECM v1 (aprox.)"].items()}, "cw_AR4_vs_F1ECM": {k: num(v) for k, v in cw.items()},
            "gw_vs_AR4": {k: num(v) for k, v in gw["AR(4)"].items()}, "gw_vs_ECMv1": {k: num(v) for k, v in gw["ECM v1 (aprox.)"].items()},
            "mcs": {"p": {k: num(v) for k, v in m["p_mcs"].items()}, "dentro_90": m["en_mcs"]},
            "diseno": "K = 5 bloques contiguos, embargo de 4 trimestres, un paso, ECM v1 aproximado (v6), misma muestra; ninguna selección por p"}


def sobrevaloracion_ultima(y: np.ndarray, X: np.ndarray, beta: np.ndarray) -> float:
    """Desviación (%) del último trimestre respecto del equilibrio estático con constante de la propia muestra."""
    z = y - X @ beta
    return float(100 * (z[-1] - z.mean()))


def spec_nacional(id_: str, d: pd.DataFrame, xs: list[str], estado: str, repite: str, desc: str, p: int, mask_excl: tuple[str, str] | None,
                  reps: dict, nombre_x: dict) -> dict:
    """Una especificación nacional: MDE → registro previo → UECM con contraste de límites → DOLS → Engle-Granger."""
    from statsmodels.tsa.stattools import coint
    y = d["y"].to_numpy()
    X = d[xs].to_numpy()
    ini, fin = str(d.index[0]), str(d.index[-1])
    formula = f"y = ln(p_tasado/deflactor) ~ {' + '.join(xs)}; UECM p = {p}; sin {mask_excl[0]}-{mask_excl[1]}" if mask_excl else \
        f"y = ln(p_tasado/deflactor) ~ {' + '.join(xs)}; UECM p = {p}"
    mde = mde_serie(y, X, R=reps["mde"])
    log_pre(id_, formula, ini, fin, f"{estado}; repite_visto={repite}; MDE={mde['mde']:.3f} (sin umbral en el Anexo B para F)")
    mask = None
    if mask_excl:
        per = d.index
        lo, hi = (pd.Period(mask_excl[0], "Q"), pd.Period(mask_excl[1], "Q")) if isinstance(per, pd.PeriodIndex) else mask_excl
        mask = ~((per >= lo) & (per <= hi))
    cl = N.contraste_limites(y, X, p, B=reps["b_lim"], seed=SEED, B_val=reps["b_val"], mask=mask)
    r = N.uecm(y, X, p, mask)
    Dls = N.dols_ts(y, X, k=1, mask=mask, maxlags=4)
    beta_d = Dls["beta"]
    se_d = Dls["se"]
    try:
        eg = coint(y, X, trend="c", autolag="aic")
        eg_p = float(eg[1])
    except Exception:
        eg_p = float("nan")
    # corto plazo: coeficientes de ΔX_t en el UECM (últimos k de W)
    k = len(xs)
    corto = r["coef"][-k:]
    idx_a = 1
    ncoef = len(r["coef"])
    V = N.mco(r["W"] @ r["coef"] + r["resid"], r["W"])[2]
    se_corto = np.sqrt(np.diag(V))[-k:]
    out = {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "ini": ini, "fin": fin, "n": r["n"], "xs": xs, "mde": mde,
           "cl": cl, "alpha": r["alpha"], "se_alpha": r["se_alpha"], "beta_uecm": r["beta_lp"].tolist(), "se_beta_uecm": r["se_beta_lp"].tolist(),
           "beta_dols": beta_d.tolist(), "se_dols": se_d.tolist(), "eg_p": eg_p, "corto": corto.tolist(), "se_corto": se_corto.tolist(), "p": p,
           "aic": r["aic"], "W": r["W"], "dep": r["W"] @ r["coef"] + r["resid"], "nombre_x": nombre_x, "ncoef": ncoef, "idx_a": idx_a,
           "mask_excl": mask_excl, "interpolada": bool(d["pob_interpolada"].any()) if "pob" in xs else False}
    PVALS_COINT[id_] = cl["p"] if estado == "principal" else np.nan
    return out


# ---------------------------------------------------------------------------------------------- paneles
def spec_panel(id_: str, P: pd.DataFrame, y: str, xs: list[str], ini: int, fin: int, estado: str, repite: str, desc: str, reps: dict,
               usa_dols: bool, usa_pmg: bool, usa_cs: bool, nombres: list[str], cce_estatico: bool = False) -> dict:
    Y, X, cod, yrs, info = D.a_arrays(P, y, xs, ini, fin)
    T = info["T"]
    formula = f"{y} ~ {' + '.join(xs)}; {ini}-{fin}; N = {info['N']}, T = {T}; DOLS {usa_dols}, PMG {usa_pmg}, CS-ARDL {usa_cs}"
    if T < 12 or info["N"] < 20:
        log_pre(id_, formula, ini, fin, "NO ESTIMABLE: T < 12 o N < 20 tras el recorte")
        motivo = (f"sin provincias con serie completa en la ventana {ini}-{fin} (los datos provinciales empiezan en 2002)" if info["N"] == 0 else
                  f"T = {T} años (mínimo 12 para estimar un ECM por provincia con los regresores del vector) o N = {info['N']} (< 20) tras el recorte de la ventana")
        return {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "ini": ini, "fin": fin, "no_estimable": True,
                "motivo": motivo, "info": info, "nombres": nombres}
    mde = mde_panel(Y, X, R=reps["mde"])
    log_pre(id_, formula, ini, fin, f"{estado}; repite_visto={repite}; MDE={mde['mde']:.3f} (sin umbral en el Anexo B para F)")
    out = {"id": id_, "estado": estado, "repite_visto": repite, "desc": desc, "ini": ini, "fin": fin, "info": info, "mde": mde, "nombres": nombres,
           "codigos": cod, "xs": xs, "y": y, "T": T}
    # contraste de cointegración de panel (Gτ) con bootstrap conjunto en el tiempo
    cp = N.coint_panel_bootstrap(Y, X, reps["b_panel"], SEED)
    out["coint"] = cp
    PVALS_COINT[id_] = cp["p"] if estado == "principal" else np.nan
    # dependencia transversal y raíces unitarias por unidad (descriptivo: CIPS es NO APTO)
    if usa_dols or usa_pmg:
        out["cd"] = cd_pesaran(N.residuo_equilibrio(Y, X, np.linalg.lstsq((X - X.mean(1, keepdims=True)).reshape(-1, X.shape[2]),
                                                                          (Y - Y.mean(1, keepdims=True)).reshape(-1), rcond=None)[0]))
    if usa_dols:
        dl = N.panel_dols(Y, X)
        out["dols"] = {"beta": dl["beta"].tolist(), "se_dk": dl["se_dk"].tolist(), "se_cluster": dl["se_cluster"].tolist(), "m": dl["m"],
                       "T_efectivo": dl["T_efectivo"]}
        beta_eq = dl["beta"]
        out["gap_dols"] = N.residuo_equilibrio(Y, X, beta_eq)
    if usa_pmg:
        pm = N.pmg(Y, X)
        bt = N.pmg_bootstrap(Y, X, reps["b_pmg"], SEED + 7)
        out["pmg"] = {"theta": pm["theta"].tolist(), "se_asint": pm["se_theta"].tolist(), "se_boot": bt["se_theta"].tolist(),
                      "ic95_boot": [bt["ic95_theta"][0].tolist(), bt["ic95_theta"][1].tolist()], "phi_medio": pm["phi_medio"], "se_phi": pm["se_phi_medio"],
                      "ic95_phi_boot": bt["ic95_phi"], "semivida": pm["semivida"], "psi_medio": pm["psi_medio"].tolist(),
                      "ic95_psi_boot": [bt["ic95_psi"][0].tolist(), bt["ic95_psi"][1].tolist()], "B_boot": bt["B"]}
    if usa_cs:
        cs = N.csardl_mg(Y, X, estatico=cce_estatico)
        out["cs"] = {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in cs.items()}
    return out


def validar_paneles(especs: list[dict], reps: dict) -> dict:
    """Tamaño y potencia del contraste de cointegración de panel en procesos generadores con la estructura de cada diseño (N, T, k)."""
    cache: dict[tuple, dict] = {}
    for e in especs:
        if e.get("no_estimable"):
            continue
        clave = (e["info"]["N"], e["info"]["T"], len(e["xs"]))
        if clave not in cache:
            cache[clave] = N.validar_coint_panel(*clave, R=reps["r_val"], B=reps["b_val_panel"], seed=SEED + 11)
        e["validacion"] = cache[clave]
    return cache


def banda_tamano(t: float) -> str:
    if 0.04 <= t <= 0.06:
        return "apta"
    if 0.02 <= t < 0.04 or 0.06 < t <= 0.15:
        return "con valor crítico corregido"
    return "no fiable"


# ---------------------------------------------------------------------------------------------- publicación de filas y hechos
def hecho(id_, indicador, valor, lo, hi, unidad, periodo, cobertura, fuentes, clase, nota):
    HECHOS.append({"id": id_, "indicador": indicador, "valor": num(valor), "min": num(lo), "max": num(hi), "unidad": unidad, "periodo": periodo,
                   "cobertura": cobertura, "fuentes": fuentes, "capa": CAPA, "clasificacion_v18": clase, "nota": f"{nota} [{ROTULO}]"})


def ic95(b, se):
    return (b - 1.96 * se, b + 1.96 * se)


def publicar_nacional(e: dict, fam: str, rechaza: bool, p_aj: float | None, q_by: float | None, fuentes: list[str], aviso: str = ""):
    """Fila de tabla y cifra de una especificación nacional según la regla AD-F (sin cointegración: solo corto plazo)."""
    cl = e["cl"]
    xs = e["xs"]
    k = len(xs)
    nx = e["nombre_x"]
    clase = "ASOCIACIÓN"
    nota_base = (f"F1 nacional; ASOCIACIÓN como máximo (sin diseño cuasi experimental). Contraste de límites con valores críticos simulados por Monte Carlo "
                 f"(F {cl['F']:.2f} frente a {cl['cv_F95']:.2f}; t {cl['t']:.2f} frente a {cl['cv_t05']:.2f}; tamaño conjunto {cl['tamano_conjunto_5pct']:.3f}; "
                 f"potencia frente a α = −0,10: {cl['potencia_alpha_-0,10']:.2f}; p = {cl['p']:.3f}). Engle-Granger p = {e['eg_p']:.3f}.")
    if e.get("interpolada"):
        nota_base += " Población con trimestres interpolados (CLAUDE.md: la interpolación solo entra en robustez; se rotula)."
    if rechaza:
        b, se = e["beta_dols"][0], e["se_dols"][0]
        lo, hi = ic95(b, se)
        valor, unidad = b, "elasticidad de largo plazo (DOLS; Newey-West 4, sin validación Monte Carlo)"
        ind = f"Elasticidad de largo plazo del precio real de la vivienda respecto de {nx[xs[0]]} (modelo {e['id']})"
        nota = nota_base + f" Se rechaza la ausencia de cointegración (Holm p = {p_aj:.3f}): se publica el largo plazo. Velocidad de ajuste trimestral {e['alpha']:.3f}."
        pub = True
    else:
        b, se = e["corto"][0], e["se_corto"][0]
        lo, hi = ic95(b, se)
        valor, unidad = b, "elasticidad de impacto en variaciones (corto plazo; MCO clásico)"
        ind = f"Respuesta de corto plazo de la variación del precio real a la variación de {nx[xs[0]]} (modelo {e['id']})"
        nota = nota_base + (f" No se rechaza la ausencia de cointegración al 5 % ({'Holm p = %.3f' % p_aj if p_aj is not None else 'BY q = %.3f' % q_by}): "
                            "no se publican elasticidades de largo plazo ni sobrevaloración; solo la dinámica de corto plazo.")
        pub = False
    nota += aviso
    FILAS.append({"id": e["id"], "familia": fam, "estado": e["estado"], "repite_visto": e["repite_visto"], "muestra": f"{e['ini']}-{e['fin']}", "N": e["n"],
                  "estimador": f"UECM p = {e['p']}; DOLS k = 1; EG", "coint_F": num(cl["F"]), "coint_t": num(cl["t"]), "coint_p_mc": num(cl["p"], 4),
                  "p_ajustado": num(p_aj if p_aj is not None else q_by, 4), "ajuste": "Holm (familia F)" if p_aj is not None else "BY (variantes)",
                  "coint_rechaza_5pct": bool(rechaza), "publica_largo_plazo": pub, "valor": num(valor), "ic95_lo": num(lo), "ic95_hi": num(hi), "unidad": unidad,
                  "mde": num(e["mde"]["mde"]), "umbral_mde": "sin referencia en el Anexo B para F", "clasificacion_v18": clase,
                  "inferencia": "sin validación Monte Carlo apta para DOLS-HAC/MCO de series; contraste de límites con CV simulados", "nota": nota})
    if e["estado"] != "coprincipal":
        hecho(f"V18-{e['id']}", ind, valor, lo, hi, unidad, f"{e['ini']}-{e['fin']}", "nacional", fuentes, clase, nota)
    log_post(e["id"], f"UECM {xs}", e["ini"], e["fin"], e["n"], valor, cl["p"], f"rechaza={rechaza}")


def publicar_panel(e: dict, fam: str, rechaza: bool, p_aj: float | None, q_by: float | None, fuentes: list[str], pmg_principal: bool, aviso: str = ""):
    if e.get("no_estimable"):
        FILAS.append({"id": e["id"], "familia": fam, "estado": e["estado"], "repite_visto": e["repite_visto"], "muestra": f"{e['ini']}-{e['fin']}",
                      "N": e["info"]["N"], "estimador": "—", "publica_largo_plazo": False, "clasificacion_v18": "NO ESTIMABLE", "nota": e["motivo"]})
        hecho(f"V18-{e['id']}", f"{e['desc']}: no estimable", None, None, None, "—", f"{e['ini']}-{e['fin']}", "provincias", fuentes, "NO ESTIMABLE", e["motivo"])
        return
    cp = e["coint"]
    nm = e["nombres"]
    v = e.get("validacion", {})
    tam = v.get("tamano_5pct")
    banda = banda_tamano(tam) if tam is not None else "sin validar"
    nota = (f"{fam} panel provincial; ASOCIACIÓN como máximo. N = {e['info']['N']} provincias no selladas con serie completa (se descartan {e['info']['descartadas']} "
            f"por huecos), T = {e['T']}. Contraste de cointegración de panel tipo Westerlund (Gτ = {cp['gtau']:.2f}; valor crítico 5 % por bootstrap conjunto "
            f"{cp['cv_5pct']:.2f}; p = {cp['p']:.3f}); validación Monte Carlo propia con la estructura del diseño: tamaño {tam if tam is not None else float('nan'):.3f} "
            f"(banda {banda}), potencia {v.get('potencia', float('nan')):.2f} (R = {v.get('R')}, B = {v.get('B')}; no sustituye al Monte Carlo del agente montecarlo). "
            f"Westerlund, CIPS y CS-ARDL: NO APTOS en V15/V16. Driscoll-Kraay con T <= 30: NO APTO (tamaño 0,16-0,28): no clasifica.")
    if banda == "no fiable":
        rechaza = False
        nota += " Contraste de cointegración «no fiable»: la clasificación no se apoya en él y no se publican elasticidades de largo plazo."
    if "cd" in e:
        nota += f" CD de Pesaran sobre residuos: {e['cd']['CD']} (p = {e['cd']['p']}); correlación media {e['cd']['rho_medio']}."
    clase = "ASOCIACIÓN"
    valor = lo = hi = None
    unidad = "—"
    ind = f"{e['desc']}"
    x0 = nm[0]
    if rechaza:
        nota += f" Se rechaza la ausencia de cointegración ({'Holm p = %.3f' % p_aj if p_aj is not None else 'BY q = %.3f' % q_by}): se publica el largo plazo."
        if pmg_principal and "pmg" in e:
            valor = e["pmg"]["theta"][0]
            lo, hi = e["pmg"]["ic95_boot"][0][0], e["pmg"]["ic95_boot"][1][0]
            unidad = "elasticidad de largo plazo (PMG; IC95 por bootstrap de provincias, sin validación Monte Carlo)"
        elif "dols" in e:
            valor = e["dols"]["beta"][0]
            se = e["dols"]["se_cluster"][0]
            lo, hi = ic95(valor, se)
            unidad = "elasticidad de largo plazo (DOLS-FE; IC95 agrupado por provincia: NO APTO sin efectos de año; DK NO APTO)"
        elif "cs" in e:
            valor = e["cs"]["theta_mg"][0]
            lo, hi = ic95(valor, e["cs"]["se_mg"][0])
            unidad = "elasticidad de largo plazo (CS-ARDL grupo medio; NO APTO, solo descriptivo)"
        ind = f"Elasticidad de largo plazo respecto de {x0} ({e['id']})"
    else:
        nota += (f" No se rechaza la ausencia de cointegración al 5 % ({'Holm p = %.3f' % p_aj if p_aj is not None else 'BY q = %.3f' % q_by}): no se publican "
                 "elasticidades de largo plazo, sobrevaloración ni comparaciones de F4 con este modelo; solo la dinámica de corto plazo.")
        if "pmg" in e:
            valor = e["pmg"]["psi_medio"][0]
            lo, hi = e["pmg"]["ic95_psi_boot"][0][0], e["pmg"]["ic95_psi_boot"][1][0]
            unidad = "elasticidad de impacto en variaciones (PMG, grupo medio; IC95 por bootstrap de provincias)"
            ind = f"Respuesta de corto plazo del {e['y'].replace('ln_', 'ln ')} a la variación de {x0} ({e['id']})"
        else:
            nota += " Este contraste no estima por sí mismo la dinámica de corto plazo (está en el modelo PMG del mismo vector)."
            ind = f"{e['desc']}: sin cointegración, sin cifra de largo plazo"
    nota += aviso
    FILAS.append({"id": e["id"], "familia": fam, "estado": e["estado"], "repite_visto": e["repite_visto"], "muestra": f"{e['ini']}-{e['fin']}", "N": e["info"]["N"],
                  "T": e["T"], "estimador": e["desc"], "coint_F": None, "coint_t": num(cp["gtau"]), "coint_p_mc": num(cp["p"], 4),
                  "p_ajustado": num(p_aj if p_aj is not None else q_by, 4), "ajuste": "Holm (familia F)" if p_aj is not None else "BY (variantes)",
                  "coint_rechaza_5pct": bool(rechaza), "publica_largo_plazo": bool(rechaza), "valor": num(valor), "ic95_lo": num(lo), "ic95_hi": num(hi), "unidad": unidad,
                  "mde": num(e["mde"]["mde"]), "umbral_mde": "sin referencia en el Anexo B para F", "clasificacion_v18": clase,
                  "inferencia": f"contraste de panel: tamaño {tam} ({banda}); DK/CR1/PMG: sin banda apta", "nota": nota})
    if e["estado"] != "coprincipal":
        hecho(f"V18-{e['id']}", ind, valor, lo, hi, unidad, f"{e['ini']}-{e['fin']}", f"{e['info']['N']} provincias", fuentes, clase, nota)
    log_post(e["id"], e["desc"], e["ini"], e["fin"], e["info"]["N"] * e["T"], valor if valor is not None else np.nan, cp["p"], f"rechaza={rechaza}; banda={banda}")


def no_estimable(id_: str, fam: str, estado: str, repite: str, desc: str, motivo: str, ini="", fin="", fuentes=None):
    log_pre(id_, desc, ini, fin, f"NO ESTIMABLE: {motivo}")
    FILAS.append({"id": id_, "familia": fam, "estado": estado, "repite_visto": repite, "muestra": f"{ini}-{fin}", "estimador": "—", "publica_largo_plazo": False,
                  "clasificacion_v18": "NO ESTIMABLE" if estado != "coprincipal" else "no se clasifica", "nota": motivo})
    if estado != "coprincipal":
        hecho(f"V18-{id_}", f"{desc}: no estimable", None, None, None, "—", f"{ini}-{fin}", "—", fuentes or ["docs/v18/plan_replicacion.md"], "NO ESTIMABLE", motivo)


# ---------------------------------------------------------------------------------------------- F2-A2 y F3-R1
def spec_f2a2(P: pd.DataFrame, reps: dict) -> list[dict]:
    """Ratio precio/alquiler y coste de uso en el panel provincial (2011-2024), como en E1 de V15 (repite_visto). Efectos fijos; ASOCIACIÓN."""
    d = P.copy().sort_values(["prov", "anio"])
    d["ln_ratio"] = np.log(d.vt / (12 * d.serpavi_vc))
    g = d.groupby("prov").ln_p
    d["gan"] = 100 * (g.shift(1) - g.shift(3)) / 2          # media de la variación anual de los dos años previos (8 trimestres)
    out = []
    variantes = [("F2-A2", 2.0, False, "principal"), ("F2-A2-v1", 3.0, False, "variante"), ("F2-A2-v2", 2.0, True, "variante")]
    for id_, amort, gan0, estado in variantes:
        d["coste"] = d.tipo_real + amort - (0.0 if gan0 else d.gan)
        Y, X, cod, yrs, info = D.a_arrays(d, "ln_ratio", ["coste"], 2013, 2024)
        formula = f"ln(precio/(12 alquiler SERPAVI)) ~ coste de uso (tipo real + {amort} − ganancia {'nula' if gan0 else 'esperada'}); FE; 2013-2024"
        log_pre(id_, formula, 2013, 2024, f"{estado}; repite_visto=sí (V15 E1)")
        r = N.DK.fe_dk(Y, X)
        b = float(r["beta"][0])
        se_cl, se_dk = float(np.sqrt(r["V_cluster"][0, 0])), float(np.sqrt(r["V_dk"][0, 0]))
        out.append({"id": id_, "estado": estado, "beta": b, "se_cluster": se_cl, "se_dk": se_dk, "info": info, "amort": amort, "gan0": gan0, "formula": formula})
        log_post(id_, formula, 2013, 2024, info["N"] * info["T"], b, np.nan, "DK y CR1 sin banda apta")
    return out


def spec_f3_ccaa(C: pd.DataFrame, id_: str, ini: int, fin: int, estado: str, sin_coste: bool, ols: bool, reps: dict, omitir: tuple[int, int] | None = None) -> dict:
    """F3-R1/A1: MC2E con efectos fijos en el panel de las 9 CCAA no selladas; instrumentos: precio retardado 1 y 2 años (y coste retardado)."""
    d = C[(C.anio >= ini - 2) & (C.anio <= fin)].copy().sort_values(["ccaa", "anio"])
    g = d.groupby("ccaa")
    d["p1"], d["p2"], d["c1"] = g.ln_p.shift(1), g.ln_p.shift(2), g.ln_coste.shift(1)
    d = d[(d.anio >= ini) & (d.anio <= fin)].dropna(subset=["ln_ini", "ln_p", "p1", "p2", "ln_coste", "c1"])
    if omitir:                                  # filas omitidas (los rezagos usan los niveles reales)
        d = d[(d.anio < omitir[0]) | (d.anio > omitir[1])]
    cc = sorted(d.ccaa.unique())
    T = fin - ini + 1 - ((omitir[1] - omitir[0] + 1) if omitir else 0)
    d = d[d.ccaa.isin([c for c in cc if (d.ccaa == c).sum() == T])]
    cc = sorted(d.ccaa.unique())
    n = len(cc)
    arr = lambda col: d.pivot(index="ccaa", columns="anio", values=col).loc[cc].to_numpy()      # noqa: E731
    y, p, p1, p2, c0, c1 = (arr(c) for c in ("ln_ini", "ln_p", "p1", "p2", "ln_coste", "c1"))
    exog = None if sin_coste else c0[:, :, None]
    inst = np.stack([p1, p2] + ([] if sin_coste else [c1]), axis=2)
    formula = (f"ln(iniciadas libres) ~ ln(valor tasado real) {'' if sin_coste else '+ ln(coste real) '}; FE; {'MCO' if ols else 'MC2E'}; {ini}-{fin}"
               + (f" sin {omitir[0]}-{omitir[1]}" if omitir else ""))
    sd = float(np.std(y - y.mean(1, keepdims=True)))
    # MDE por Monte Carlo (ruido AR(1) ρ = 0,5 con σ del residuo intra-CCAA del resultado, declarado «ya visto»)
    def sim(rng):
        u = rng.normal(size=y.shape) * sd * np.sqrt(0.75)
        z = u.copy()
        for i in range(1, z.shape[1]):
            z[:, i] = 0.5 * z[:, i - 1] + u[:, i]
        if ols:
            r = N.iv_panel_fe(z, p, exog, p[:, :, None])
        else:
            r = N.iv_panel_fe(z, p, exog, inst)
        return r["beta"], r["se"]
    mde = N.mde_mc(sim, reps["mde_iv"], SEED)
    log_pre(id_, formula, ini, fin, f"{estado}; MDE={mde['mde']:.3f}; σ = {sd:.3f} (ya visto); sin referencia en el Anexo B para F")
    r = N.iv_panel_fe(y, p, exog, p[:, :, None] if ols else inst)
    out = {"id": id_, "estado": estado, "ini": ini, "fin": fin, "n_ccaa": n, "T": T, "mde": mde, "res": r, "formula": formula, "ols": ols, "sin_coste": sin_coste}
    log_post(id_, formula, ini, fin, r["n_obs"], r["beta"], r["p"], "CR1 con 9 clusters: no fiable")
    return out


# ---------------------------------------------------------------------------------------------- principal
REPS_FULL = {"mde": 2000, "mde_iv": 1000, "b_lim": 2000, "b_val": 1000, "b_panel": 999, "b_pmg": 199, "r_val": 200, "b_val_panel": 99}
REPS_RAPIDO = {"mde": 100, "mde_iv": 60, "b_lim": 200, "b_val": 100, "b_panel": 99, "b_pmg": 10, "r_val": 10, "b_val_panel": 19}




# ---------------------------------------------------------------------------------------------- P-E1P2 (CS-ARDL trimestral provincial)
def cs_e1p2(reps: dict) -> dict:
    """Coprincipal F1-P-E1P2: CS-ARDL de V15 (E1-P2) en la muestra V18: ln valor tasado real frente a ln IPC de alquiler real, provincias no selladas,
    trimestral. Herramienta NO APTA: solo descriptiva. Referencias publicadas: θ = 0,64 (V15 E1-P2) y 0,84 (V16 Q9-c)."""
    d = D.panel_prov_trimestral_alquiler()
    Y, X = d["y"].T, d["x"].T
    ok = np.all(np.isfinite(Y), axis=1) & np.all(np.isfinite(X), axis=1)
    Y, X = Y[ok], X[ok][:, :, None]
    log_pre("F1-P-E1P2", "CS-ARDL(1,0) trimestral: ln valor tasado real ~ ln IPC alquiler real; provincias no selladas", d["idx"][0], d["idx"][-1],
            "coprincipal; repite_visto=sí (V15 E1-P2 y V16 Q9-c)")
    r = N.csardl_mg(Y, X)
    out = {"N": int(Y.shape[0]), "T": int(Y.shape[1]), "ini": d["idx"][0], "fin": d["idx"][-1], "theta_mg": float(r["theta_mg"][0]),
           "theta_recortada": float(r["theta_recortada"][0]), "theta_mediana": float(r["theta_mediana"][0]), "se_mg": float(r["se_mg"][0]),
           "phi_medio": r["phi_medio"], "publicado_V15": 0.64, "publicado_V16_q9c": 0.84}
    log_post("F1-P-E1P2", "CS-ARDL(1,0)", out["ini"], out["fin"], Y.size, out["theta_mg"], np.nan, "NO APTO: descriptivo")
    return out


def recursivo_dols(d: pd.DataFrame, xs: list[str], desde: int = 60, paso: int = 4) -> dict:
    y, X = d["y"].to_numpy(), d[xs].to_numpy()
    fin = list(range(desde, len(y) + 1, paso))
    b = [float(N.dols_ts(y[:e], X[:e], 1)["beta"][0]) for e in fin]
    return {"ultimos": [round(v, 3) for v in b[-3:]], "min": num(min(b)), "max": num(max(b)), "primero": num(b[0]), "n_ventanas": len(b)}


def main(rapido: bool = False, salida: Path | None = None) -> dict:
    global REG, OUT
    reps = REPS_RAPIDO if rapido else REPS_FULL
    if salida:
        OUT = salida
    OUT.mkdir(parents=True, exist_ok=True)
    FILAS.clear()
    HECHOS.clear()
    PVALS_COINT.clear()
    REG = Registry(OUT / "registro.csv")
    n = D.nacional_t(con_ipv=True)
    a = D.nacional_a()
    P = D.panel_prov()
    P["ln_serp"] = np.log(P.serpavi_vc / P.defl * 100)
    C = D.panel_ccaa_oferta()
    nomx = {"renta": "la renta real de los hogares (ln)", "tipo_real": "el tipo hipotecario real (pp)", "pob": "la población (ln)",
            "tipo_nom": "el tipo hipotecario nominal (pp)", "pib": "el PIB real (ln)", "parque_pc": "el parque de viviendas per cápita (ln)"}
    diag: dict = {"series_nacionales": {c: adf_kpss(n[c]) for c in ("y", "renta", "tipo_real", "pob")}}

    # ------------------------------------------------------------ F1 nacional (especificaciones)
    xs0 = ["renta", "tipo_real", "pob"]
    nac: list[dict] = []
    nac.append(spec_nacional("F1-R1", n, xs0, "principal", "sí (V7.2, V8-M4)", "F1-R1 nacional trimestral 1999T1-2026T2", 2, None, reps, nomx))
    nac.append(spec_nacional("F1-R1-v2", n, xs0, "variante", "sí", "sin 2008T1-2013T4", 2, EXCL_0813, reps, nomx))
    n3 = n.loc["2007Q1":].copy()
    n3["y"] = n3["ipv_real"]
    nac.append(spec_nacional("F1-R1-v3", n3, xs0, "variante", "sí", "IPV real desde 2007T1", 2, None, reps, nomx))
    nac.append(spec_nacional("F1-R1-v4", n, ["renta", "tipo_nom", "pob"], "variante", "sí", "tipo hipotecario nominal", 2, None, reps, nomx))
    nac.append(spec_nacional("F1-R1-v5", n, ["renta", "tipo_real"], "variante", "sí", "sin población (parte interpolada; holgura 1)", 2, None, reps, nomx))
    nac.append(spec_nacional("F1-P-M4", n, ["pib", "tipo_real", "pob"], "coprincipal", "sí (V8-M4)",
                             "coprincipal V8-M4: UECM p = 2 caso III y DOLS k = 1 con ln PIB, tipo real y población", 2, None, reps, nomx))
    aa = a.copy()
    aa["pob_interpolada"] = False
    xs_a = ["renta", "tipo_real", "pob", "parque_pc"]
    nac.append(spec_nacional("F1-A2", aa, xs_a, "principal", "sí (V7.2, V8-M4)", "F1-A2 nacional anual 2001-2025 con parque per cápita (el parque por hogar no existe antes de 2021)",
                             1, None, reps, nomx))
    nac.append(spec_nacional("F1-A2-v1", aa, ["renta", "tipo_real", "pob"], "variante", "sí", "sin parque", 1, None, reps, nomx))
    nac.append(spec_nacional("F1-A2-v2", aa, xs_a, "variante", "sí", "sin 2008-2013", 1, (2008, 2013), reps, nomx))

    # ------------------------------------------------------------ paneles F1, F2, F3
    base3 = ["ln_renta", "paro", "ln_pob"]
    alt5 = ["ln_renta", "paro", "tipo_nom", "ln_parque_pc", "ln_pob"]
    nm3 = ["la renta real per cápita (ln; PIB provincial como sustituto)", "el paro (pp)", "la población (ln)"]
    nm5 = nm3[:2] + ["el tipo hipotecario nominal (pp)", "el parque per cápita (ln)", "la población (ln)"]
    pan: list[dict] = []
    pan.append(spec_panel("F1-R2", P, "ln_p", base3, 2002, 2018, "principal", "sí (V7.2)", "F1-R2 DOLS-FE vector básico 2002-2018 (2000-2018 no existe)", reps, True, False, False, nm3))
    pan.append(spec_panel("F1-R2-alt", P, "ln_p", alt5, 2002, 2018, "principal", "sí (V7.2)", "F1-R2-alt DOLS-FE vector alternativo 2002-2018", reps, True, False, False, nm5))
    pan.append(spec_panel("F1-R2-pmg", P, "ln_p", base3, 2002, 2018, "principal", "sí (V7.2)", "F1-R2-pmg ECM por PMG vector básico 2002-2018", reps, False, True, False, nm3))
    pan.append(spec_panel("F1-A1", P, "ln_p", base3, 2002, 2024, "principal", "sí (V15 E1-P2, Q9-c)", "F1-A1 DOLS-FE y PMG hasta 2024 y CS-ARDL", reps, True, True, True, nm3))
    for base_id, xs, nm, lab in (("F1-R2", base3, nm3, "DOLS-FE"), ("F1-R2-alt", alt5, nm5, "DOLS-FE alt"), ("F1-R2-pmg", base3, nm3, "PMG")):
        pan.append(spec_panel(f"{base_id}-v2", P, "ln_p", xs, 2000, 2008, "variante", "sí", f"{base_id} ventana 2000-2008 (en datos 2002-2008)", reps, False, False, False, nm))
    pan.append(spec_panel("F1-A1-v1", P, "ln_p", base3, 2014, 2024, "variante", "sí", "F1-A1 sin 2008-2013 (queda 2014-2024)", reps, False, False, False, nm3))
    pan.append(spec_panel("F1-A1-v3", P, "ln_p", base3, 2002, 2024, "variante", "sí", "F1-A1 con CCE-MG (estático)", reps, False, False, True, nm3, cce_estatico=True))
    xs_f2 = ["ln_renta", "ln_pob", "ln_parque_pc", "tipo_real"]
    nm_f2 = ["la renta real per cápita (ln)", "la población (sustituto de los hogares; ln)", "el parque per cápita (ln)", "el tipo hipotecario real (pp)"]
    pan.append(spec_panel("F2-R1", P, "ln_alq", xs_f2, 2002, 2024, "principal", "no", "F2-R1 PMG del IPC de alquiler real (hogares: población como sustituto)", reps, False, True, False, nm_f2))
    pan.append(spec_panel("F2-R1-v1", P, "ln_serp", xs_f2, 2011, 2024, "variante", "no", "F2-R1 con SERPAVI (alquiler €/m², 2011-2024)", reps, False, True, False, nm_f2))
    pan.append(spec_panel("F2-R1-v2", P, "ln_alq", ["ln_renta", "ln_parque_pc", "tipo_real"], 2002, 2024, "variante", "no", "F2-R1 sin hogares", reps, False, True, False,
                          [nm_f2[0], nm_f2[2], nm_f2[3]]))
    pan.append(spec_panel("F2-R1-v3", P, "ln_alq", xs_f2, 2014, 2024, "variante", "no", "F2-R1 sin 2008-2013 (queda 2014-2024)", reps, False, False, False, nm_f2))
    pan.append(spec_panel("F2-A1", P, "ln_alq", xs_f2, 2002, 2024, "principal", "no", "F2-A1 CS-ARDL del IPC de alquiler real", reps, False, False, True, nm_f2))
    pan.append(spec_panel("F2-A1-v1", P, "ln_serp", xs_f2, 2011, 2024, "variante", "no", "F2-A1 con SERPAVI", reps, False, False, True, nm_f2))
    pan.append(spec_panel("F2-A1-v2", P, "ln_alq", xs_f2, 2014, 2024, "variante", "no", "F2-A1 sin 2008-2013", reps, False, False, True, nm_f2))
    xs_f3 = ["ln_p", "ln_suelo", "ln_credprom"]
    nm_f3 = ["el valor tasado real (ln)", "el precio real del suelo (ln)", "el crédito real a promotores (ln)"]
    pan.append(spec_panel("F3-A2", P, "ln_ini", xs_f3, 2004, 2024, "principal", "no", "F3-A2 PMG de ln iniciadas", reps, False, True, False, nm_f3))
    pan.append(spec_panel("F3-A2-v1", P, "ln_ini", ["ln_p", "ln_credprom"], 2004, 2024, "variante", "no", "F3-A2 sin suelo", reps, False, True, False, [nm_f3[0], nm_f3[2]]))
    pan.append(spec_panel("F3-A2-v2", P, "ln_ini", ["ln_p", "ln_suelo"], 2004, 2024, "variante", "no", "F3-A2 sin crédito", reps, False, True, False, nm_f3[:2]))
    pan.append(spec_panel("F3-A2-v3", P, "ln_ini", xs_f3, 2014, 2024, "variante", "no", "F3-A2 sin 2008-2013 (queda 2014-2024)", reps, False, False, False, nm_f3))
    validacion = validar_paneles(pan, reps)

    # ------------------------------------------------------------ Holm (familia F: contrastes de cointegración de las especificaciones principales)
    princ = {k: v for k, v in PVALS_COINT.items() if np.isfinite(v)}
    hp = holm(princ)
    rech_h = {k: hp[k] < 0.05 for k in hp}
    # variantes: BY dentro de cada identificador
    grupos: dict[str, list[tuple[str, float]]] = {}
    for e in nac + [x for x in pan if not x.get("no_estimable")]:
        base_id = e["id"].split("-v")[0]
        if e["estado"] == "variante":
            pv = e["cl"]["p"] if "cl" in e else e["coint"]["p"]
            grupos.setdefault(base_id, []).append((e["id"], pv))
    qby: dict[str, float] = {}
    for g, lst in grupos.items():
        q = by_adjust([p for _, p in lst])
        for (i, _), qq in zip(lst, q):
            qby[i] = qq

    # ------------------------------------------------------------ fuera de muestra y diagnósticos del F1-R1 principal
    e0 = nac[0]
    fom = fuera_de_muestra(n, xs0, "1999Q1", "2026Q2")
    per = n.index[2:]
    fechas = [i for i, q in enumerate(per) if str(q) in ("2008Q1", "2015Q1")]
    fijos, supf = sup_f_ruptura(e0["W"], e0["dep"], fechas)
    diag["estabilidad_F1_R1"] = {"chow_en_fechas_fijas": {str(per[i]): num(v) for i, v in fijos.items()}, "sup_F_ruptura_unica": num(supf),
                                 "nota": "sin valor crítico validado: se publica como descriptivo", "dols_recursivo_primer_regresor": recursivo_dols(n, xs0)}
    diag["dependencia_transversal"] = {e["id"]: e["cd"] for e in pan if not e.get("no_estimable") and "cd" in e}
    diag["raices_unitarias_panel"] = "CIPS es NO APTO (V16 montecarlo/cips_bootstrap, tamaño 0,006): no se usa; ADF nacional arriba. El contraste de panel es Gτ con bootstrap conjunto."
    diag["moran"] = ("no se calcula aquí: no hay matriz de contigüidad provincial versionada para V18; la dependencia transversal se mide con el CD de Pesaran "
                     "y el bootstrap del contraste de panel conserva la dependencia entre provincias")
    diag["exclusiones"] = "Madrid, Baleares y Canarias ya están fuera por el sellado de v6; Barcelona permanece (sin variante propia: holgura no usada)."

    # ------------------------------------------------------------ publicación de F1-F3 (regla AD-F)
    fuentes_nac, fuentes_pan = FUENTE_NAC, FUENTE_PAN
    def aviso_var(propio: bool, base_id: str, pv: float, q: float) -> str:
        if propio and not rech_h.get(base_id, False):
            return (f" La variante rechaza por sí sola (p = {pv:.3f}; BY q = {q:.3f}) pero su principal ({base_id}) no rechaza tras Holm ({hp.get(base_id, float('nan')):.3f}): "
                    "no se publica largo plazo (AD-F es por modelo); queda como señal exploratoria para I5, sin clase propia.")
        return ""
    for e in nac:
        if e["estado"] == "principal":
            rech = bool(rech_h[e["id"]])
            publicar_nacional(e, "F1", rech, hp[e["id"]], None, fuentes_nac)
        elif e["estado"] == "variante":
            q = qby[e["id"]]
            base_id = e["id"].split("-v")[0]
            propio = bool(e["cl"]["p"] < 0.05 and q < 0.10)
            publicar_nacional(e, "F1", propio and rech_h.get(base_id, False), None, q, fuentes_nac, aviso_var(propio, base_id, e["cl"]["p"], q))
        else:
            publicar_nacional(e, "F1", e["cl"]["p"] < 0.05, None, e["cl"]["p"], fuentes_nac)
    for e in pan:
        fam = e["id"][:2]
        pmg_p = "pmg" in e and "dols" not in e
        if e.get("no_estimable"):
            publicar_panel(e, fam, False, None, None, fuentes_pan, False)
        elif e["estado"] == "principal":
            publicar_panel(e, fam, bool(rech_h[e["id"]]), hp[e["id"]], None, fuentes_pan, pmg_p)
        else:
            base_id = e["id"].split("-v")[0]
            propio = bool(e["coint"]["p"] < 0.05 and qby[e["id"]] < 0.10)
            publicar_panel(e, fam, propio and rech_h.get(base_id, False), None, qby[e["id"]], fuentes_pan, pmg_p, aviso_var(propio, base_id, e["coint"]["p"], qby[e["id"]]))
    # coprincipales sin hecho propio
    pe = cs_e1p2(reps)
    FILAS.append({"id": "F1-P-E1P2", "familia": "F1", "estado": "coprincipal", "repite_visto": "sí (V15 E1-P2, V16 Q9-c)", "muestra": f"{pe['ini']}-{pe['fin']}", "N": pe["N"],
                  "T": pe["T"], "estimador": "CS-ARDL(1,0) grupo medio, trimestral", "valor": num(pe["theta_mg"]), "unidad": "θ de largo plazo (NO APTO: descriptivo)",
                  "clasificacion_v18": "no se clasifica", "publica_largo_plazo": False,
                  "nota": f"θ MG = {pe['theta_mg']:.2f} (recortada {pe['theta_recortada']:.2f}; mediana {pe['theta_mediana']:.2f}; φ medio {pe['phi_medio']:.2f}) frente a "
                          f"0,64 (V15 E1-P2) y 0,84 (V16 Q9-c); CS-ARDL NO APTO: sin IC ni clasificación"})
    no_estimable("F1-P-V72", "F1", "coprincipal", "sí (V7.2)", "coprincipal V7.2: contraste de cointegración de panel de CCAA (Westerlund/Pedroni)",
                 "no reproducible en la muestra V18: el panel de V7.2 usa las 17 CCAA y 8 están selladas por v6; con las 9 no selladas la especificación deja de ser la de origen. "
                 "La conclusión publicada (no se establece cointegración) se contrasta en F1-R1 y F1-R2 de forma independiente.")

    # F2-A2 (ratio precio/alquiler y coste de uso)
    f2a2 = spec_f2a2(P, reps)
    for s_ in f2a2:
        lo, hi = ic95(s_["beta"], s_["se_cluster"])
        nota = (f"Panel provincial 2013-2024, N = {s_['info']['N']}, T = {s_['info']['T']}; ln(ratio) sobre coste de uso con efectos fijos. repite_visto (V15 E1). "
                f"IC95 con error agrupado por provincia ({s_['se_cluster']:.3f}); DK ({s_['se_dk']:.3f}): ambos NO APTOS con T <= 30 y sin efectos de año; "
                "ASOCIACIÓN como máximo, sin cifra clasificable por inferencia.")
        if s_["id"] == "F2-A2-v1":
            nota += " La amortización del 3 % solo desplaza el coste de uso en una constante, absorbida por los efectos fijos: el coeficiente coincide con el de la principal."
        FILAS.append({"id": s_["id"], "familia": "F2", "estado": s_["estado"], "repite_visto": "sí (V15 E1)", "muestra": "2013-2024", "N": s_["info"]["N"], "T": s_["info"]["T"],
                      "estimador": "FE; DK/CR1 sin banda apta", "valor": num(s_["beta"]), "ic95_lo": num(lo), "ic95_hi": num(hi), "unidad": "semielasticidad del ratio por pp de coste de uso",
                      "clasificacion_v18": "ASOCIACIÓN", "publica_largo_plazo": False, "nota": nota})
        hecho(f"V18-{s_['id']}", "Semielasticidad del ratio precio/alquiler respecto del coste de uso (panel provincial)", s_["beta"], lo, hi, "ln del ratio por pp de coste de uso",
              "2013-2024", f"{s_['info']['N']} provincias", ["base:valor_tasado", "base:serpavi_alquiler_m2_mediana (tipologia=VC)", "base:tipo_hip_real_bde"], "ASOCIACIÓN", nota)

    # F3-R1 y A1 (MC2E en CCAA no selladas)
    f3 = [spec_f3_ccaa(C, "F3-R1", 1997, 2004, "principal", False, False, reps),
          spec_f3_ccaa(C, "F3-R1-v1", 1997, 2004, "variante", True, False, reps),
          spec_f3_ccaa(C, "F3-R1-v2", 1997, 2004, "variante", False, True, reps),
          spec_f3_ccaa(C, "F3-A1", 1997, 2024, "principal", False, False, reps),
          spec_f3_ccaa(C, "F3-A1-v1", 1997, 2024, "variante", True, False, reps),
          spec_f3_ccaa(C, "F3-A1-v2", 1997, 2024, "variante", False, False, reps, omitir=(2008, 2013))]
    for s_ in f3:
        r = s_["res"]
        lo, hi = r["beta"] - stats.t.ppf(0.975, r["gl"]) * r["se"], r["beta"] + stats.t.ppf(0.975, r["gl"]) * r["se"]
        nota = (f"Panel de {s_['n_ccaa']} CCAA no selladas, {s_['ini']}-{s_['fin']} (1995 y 1996 solo como retardos); viviendas libres iniciadas (MIVAU). "
                f"{'MCO con efectos fijos (sin instrumentos)' if s_['ols'] else 'MC2E con efectos fijos, instrumentos de precio y coste retardados (no exógenos)'}; "
                f"F de primera etapa agrupado {r['F_primera_etapa']:.1f}; IC95 con t({r['gl']}) y varianza agrupada por CCAA con 9 clusters: sin banda apta (no fiable). "
                f"MDE {s_['mde']['mde']:.2f} (sin referencia en el Anexo B para F; Taltavull 0,87 solo orientativa). ASOCIACIÓN: instrumentos retardados no exógenos.")
        FILAS.append({"id": s_["id"], "familia": "F3", "estado": s_["estado"], "repite_visto": "no", "muestra": f"{s_['ini']}-{s_['fin']}", "N": r["n_obs"], "estimador": s_["formula"],
                      "valor": num(r["beta"]), "ic95_lo": num(lo), "ic95_hi": num(hi), "unidad": "elasticidad de las iniciadas respecto del precio real", "mde": num(s_["mde"]["mde"]),
                      "umbral_mde": "sin referencia en el Anexo B para F", "clasificacion_v18": "ASOCIACIÓN", "publica_largo_plazo": False, "p_ajustado": None, "nota": nota})
        hecho(f"V18-{s_['id']}", "Elasticidad de las viviendas libres iniciadas respecto del valor tasado real (CCAA no selladas)", r["beta"], lo, hi,
              "elasticidad (log-log)", f"{s_['ini']}-{s_['fin']}", f"{s_['n_ccaa']} CCAA", ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv", "base:valor_tasado_ccaa", "base:costes_constr"],
              "ASOCIACIÓN", nota)
    no_estimable("F3-A3", "F3", "principal", "no", "F3-A3 PMG con el precio instrumentado por el Bartik de E5-R1",
                 "falta el dato imprescindible: la afiliación provincial por sector de 2001 (ss_afiliacion_provincial_cnae_2001, `posterior_prereg`) no está en el repositorio y no hay red; "
                 "tampoco existe aún la estimación E5-R1 que la versión de conjunto hereda", "2004", "2024", ["docs/v18/sellado_v18.json (posterior_prereg)"])

    # F1-A3 (sobrevaloración) y F4 (coherencia): solo con cointegración
    cands = [e for e in nac if e["id"] in ("F1-R1", "F1-A2") and rech_h.get(e["id"])] + [e for e in pan if e["id"] == "F1-R2" and rech_h.get("F1-R2")]
    if cands:
        sv = []
        for e in cands:
            if e["id"].startswith("F1-R1") or e["id"].startswith("F1-A2"):
                d_ = n if e["id"] == "F1-R1" else aa
                sv.append(sobrevaloracion_ultima(d_["y"].to_numpy(), d_[e["xs"]].to_numpy(), np.array(e["beta_dols"])))
            elif "gap_dols" in e:
                sv.append(float(100 * e["gap_dols"][:, -1].mean()))
        FILAS.append({"id": "F1-A3", "familia": "F1", "estado": "principal", "repite_visto": "sí", "valor": num(float(np.mean(sv))) if sv else None,
                      "unidad": "% de desviación al último periodo (IEF: 10-15 % a dic. 2025; 5,3-12,7 % a jun. 2025)", "clasificacion_v18": "ASOCIACIÓN",
                      "nota": "calculada solo con los modelos que rechazan la ausencia de cointegración"})
        hecho("V18-F1-A3", "Desviación del precio real respecto del equilibrio de largo plazo", float(np.mean(sv)) if sv else None, min(sv) if sv else None, max(sv) if sv else None,
              "% (log-puntos)", "último periodo", "nacional", fuentes_nac, "ASOCIACIÓN", "rango entre los modelos con cointegración; se compara en rango con el IEF")
    else:
        no_estimable("F1-A3", "F1", "principal", "sí (como R1)", "F1-A3 sobrevaloración frente al equilibrio de F1",
                     "no se publica por la regla AD-F de la adenda: ni el contraste de límites (F1-R1, F1-A2) ni el de panel (F1-R2) rechazan la ausencia de cointegración al 5 % tras Holm; "
                     "una desviación respecto de un equilibrio sin cointegración es espuria y no se compara con el rango del IEF", "1999", "2026")
    f4 = [("F4-1", "población en F1 (precio)", "E3-R2 y E3-A1", ["F1-R1", "F1-R2", "F1-A1"]), ("F4-2", "hogares en F2 (alquiler)", "E3-A2", ["F2-R1", "F2-A1"]),
          ("F4-3", "tipo real en F1 (semielasticidad)", "E7-R1 y E7-R2 convertidas con la velocidad de F1", ["F1-R1", "F1-A2"]),
          ("F4-4", "precio en F3", "E5-R1", ["F3-A2"]), ("F4-5", "parque per cápita en F1", "E6-R2 y E5-R1 (solo signo)", ["F1-A2", "F1-R2-alt"])]
    f4_estado = {}
    for id_, a_, b_, deps in f4:
        ok = [d_ for d_ in deps if rech_h.get(d_)]
        if not ok:
            motivo = (f"no se hace: el modelo de conjunto ({', '.join(deps)}) no rechaza la ausencia de cointegración al 5 % tras Holm (regla AD-F); "
                      f"una elasticidad de largo plazo sin cointegración no se compara con {b_}")
            f4_estado[id_] = {"hecho": False, "motivo": motivo}
            no_estimable(id_, "F4", "derivada", "—", f"{id_}: {a_} frente a {b_}", motivo, "", "")
        else:
            f4_estado[id_] = {"hecho": False, "motivo": f"procede ({', '.join(ok)} rechaza), pero la contraparte ({b_}) pertenece a otro modelizador y no está en output/v18/estimacion: pendiente"}
            no_estimable(id_, "F4", "derivada", "—", f"{id_}: {a_} frente a {b_}", f4_estado[id_]["motivo"], "", "")

    return {"reps": reps, "nac": nac, "pan": pan, "f2a2": f2a2, "f3": f3, "pe": pe, "fom": fom, "diag": diag, "validacion": validacion, "hp": hp, "qby": qby, "f4": f4_estado,
            "nomx": nomx}


# ---------------------------------------------------------------------------------------------- salidas
def md_tabla(df: pd.DataFrame, cols: list[str]) -> str:
    d = df[[c for c in cols if c in df.columns]].copy()
    d = d.astype(object).where(d.notna(), "—")
    d = d.map(lambda v: int(v) if isinstance(v, float) and v == v and float(v).is_integer() else v)
    enc = "| " + " | ".join(d.columns) + " |\n|" + "|".join("---" for _ in d.columns) + "|\n"
    return enc + "\n".join("| " + " | ".join(str(v) for v in r) + " |" for r in d.itertuples(index=False)) + "\n"


def escribir(res: dict, salida: Path) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    tabla = pd.DataFrame(FILAS)
    tabla.to_csv(salida / "tabla.csv", index=False)
    (salida / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1), encoding="utf-8")
    fom = res["fom"]
    princ = tabla[tabla.estado == "principal"]
    estim = {r.id: {"valor": r.valor, "ic95": [r.ic95_lo, r.ic95_hi], "unidad": r.unidad, "clasificacion_v18": r.clasificacion_v18, "coint_p_mc": r.coint_p_mc,
                    "p_ajustado": r.p_ajustado, "publica_largo_plazo": bool(r.publica_largo_plazo) if r.publica_largo_plazo == r.publica_largo_plazo else False}
             for r in tabla.itertuples() if r.estado in ("principal", "variante", "coprincipal")}
    n_rech = int(princ.coint_rechaza_5pct.fillna(False).astype(bool).sum()) if "coint_rechaza_5pct" in princ else 0
    resultado = {
        "rama": "v18/estimacion/f_conjunto",
        "pregunta": "¿Hay una relación de largo plazo (cointegración) del precio real, el alquiler real y las iniciadas con sus fundamentales, a escala nacional y provincial, "
                    "y qué dice la dinámica de corto plazo cuando no la hay? (F1, F2, F3 y F4 del plan de replicación V18)",
        "capa": CAPA,
        "datos": "base (hechos.parquet) y data/raw filtrados con src/v18/sellado.filtrar: nacional trimestral 1999T1-2026T2 y anual 2001-2025; provincias no selladas (v6, V15, V16) "
                 "anual hasta 2024; 9 CCAA no selladas para F3-R1",
        "N": {"nacional_trimestral": res["nac"][0]["n"], "nacional_anual": res["nac"][6]["n"],
              "paneles": {e["id"]: (e["info"]["N"], e["T"]) for e in res["pan"] if not e.get("no_estimable")}},
        "metodo": "UECM de Pesaran-Shin-Smith con valores críticos simulados; DOLS (series y panel), PMG, CS-ARDL/CCE-MG; contraste de panel tipo Westerlund con bootstrap conjunto; "
                  "MC2E de panel en F3-R1; Holm en la familia F (contrastes de cointegración); BY en variantes; fuera de muestra en bloques con embargo",
        "estimacion": estim,
        "ic95": {k: v["ic95"] for k, v in estim.items()},
        "p_ajustado": {"metodo": "Holm sobre los contrastes de cointegración de las especificaciones principales (familia F); BY en las variantes", "valores": res["hp"],
                       "q_by_variantes": res["qby"]},
        "nivel_evidencia": "EXPLORATORIO",
        "clasificacion_v18": "ASOCIACIÓN (tope de la familia F; sin diseño cuasi experimental). Clase provisional: falta I8 (réplica ciega, B6)",
        "clasificacion_v18_por_especificacion": {r.id: r.clasificacion_v18 for r in tabla.itertuples()},
        "diagnosticos": {**res["diag"], "mde_por_especificacion": {r.id: r.mde for r in tabla.itertuples() if getattr(r, "mde", None) == getattr(r, "mde", None) and r.mde is not None},
                         "validacion_contraste_panel": {f"N{k[0]}_T{k[1]}_k{k[2]}": v for k, v in res["validacion"].items()},
                         "herramientas_no_aptas": NO_APTO, "f4": res["f4"],
                         "F1_P_E1P2": res["pe"], "especificaciones_con_cointegracion_rechazada": n_rech},
        "fuera_muestra": {"modelo": "F1-ECM (AR(4) + y_{t-1}, X_{t-1}, ΔX_{t-1}); trimestral nacional; bloques con embargo (K = 5, 4 trimestres); misma muestra",
                          "rmse": fom["rmse_pct"], "dm_vs_ar4": fom["dm_F1ECM_vs_AR4"], "dm_vs_ecm_v1": fom["dm_F1ECM_vs_ECMv1"], "cw": fom["cw_AR4_vs_F1ECM"],
                          "gw_vs_ar4": fom["gw_vs_AR4"], "mcs": fom["mcs"], "n_prueba": fom["n_prueba"], "diseno": fom["diseno"]},
        "notas": [ROTULO, "Sin lenguaje causal: ninguna estimación de F tiene diseño cuasi experimental (tope ASOCIACIÓN).",
                  "Clase provisional: I8 (réplica ciega) la hace el orquestador (B6).",
                  "Desviaciones y motivos: docs/v18/desviaciones_f_e7.md.",
                  "El panel provincial tiene 33-38 provincias (no 39): huecos en el valor tasado anual y sellado de v6/V15/V16."],
    }
    (salida / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    informe(res, tabla, salida)


def informe(res: dict, tabla: pd.DataFrame, salida: Path) -> None:
    fom = res["fom"]
    hp = res["hp"]
    L = [f"# F1-F4 · Modelos de conjunto (precio, alquiler, oferta y coherencia)\n\n*{ROTULO}.*\n"]
    L.append("## Lo que dicen los datos, sin lenguaje causal\n")
    rech = [k for k, v in hp.items() if v < 0.05]
    if not rech:
        L.append("En ninguno de los nueve contrastes de cointegración de la familia F (Holm, 5 %) se rechaza la ausencia de cointegración. Por la regla AD-F de la adenda no se publican "
                 "elasticidades de largo plazo de F1, F2 ni F3, ni la sobrevaloración (F1-A3), y no se hacen las comparaciones de F4. Solo se publica la dinámica de corto plazo, como ASOCIACIÓN. "
                 "El resultado coincide con lo ya publicado (V7.2 y V8-M4: no se demuestra cointegración) y no cambia ninguna cifra ni conclusión publicada.\n")
    else:
        L.append(f"Se rechaza la ausencia de cointegración en: {', '.join(rech)} (Holm, 5 %). Solo esos modelos publican largo plazo.\n")
    cerca = [f"{r.id} (p bruto {r.coint_p_mc:.3f}; Holm {r.p_ajustado:.3f})" for r in tabla[(tabla.estado == "principal") & tabla.coint_p_mc.notna()].itertuples()
             if r.p_ajustado == r.p_ajustado and 0.05 <= r.p_ajustado < 0.10]
    sola = [f"{r.id} (p {r.coint_p_mc:.3f}; BY q {r.p_ajustado:.3f})" for r in tabla[(tabla.estado == "variante") & tabla.coint_p_mc.notna()].itertuples()
            if r.coint_p_mc < 0.05 and r.p_ajustado == r.p_ajustado and r.p_ajustado < 0.10 and not bool(r.publica_largo_plazo)]
    if cerca or sola:
        L.append("**Señales cercanas, declaradas para que conste (ninguna se publica como largo plazo).** "
                 + (f"Principales entre 0,05 y 0,10 tras Holm: {', '.join(cerca)}. " if cerca else "")
                 + (f"Variantes que rechazan por sí solas mientras su principal no: {', '.join(sola)}. " if sola else "")
                 + "La regla AD-F es por modelo y la familia de Holm solo cuenta los contrastes de las principales; con T = 21 y N = 31 la validación propia da tamaño 0,05 y potencia 1,0 frente a un ajuste fuerte, "
                   "y menos frente a un ajuste lento. Queda como señal exploratoria para la fase de revisión.\n")
    L.append("## Contrastes de cointegración (familia F, Holm)\n")
    c = tabla[(tabla.estado == "principal") & tabla.coint_p_mc.notna()][["id", "muestra", "N", "estimador", "coint_t", "coint_F", "coint_p_mc", "p_ajustado", "coint_rechaza_5pct", "mde"]]
    L.append(md_tabla(c, list(c.columns)))
    L.append("\nVariantes (BY al 10 % dentro de cada identificador) y coprincipales:\n")
    v = tabla[tabla.estado.isin(["variante", "coprincipal"])][["id", "estado", "muestra", "N", "coint_p_mc", "p_ajustado", "coint_rechaza_5pct", "valor", "unidad", "clasificacion_v18"]]
    L.append(md_tabla(v, list(v.columns)))
    L.append("\n## Herramientas y banda de inferencia (Monte Carlo previo)\n")
    for k, t in NO_APTO.items():
        L.append(f"- {k}: {t}.")
    L.append("- Contraste de límites del UECM: valores críticos simulados con la muestra de cada especificación (bloques de 4, B = 2.000), tamaño en réplicas independientes y potencia "
             "frente a α = −0,10 en la tabla de contrastes y en tabla.csv.")
    L.append("- Contraste de panel: validación propia con la estructura de cada diseño (factor común, N, T, k); no sustituye al Monte Carlo del agente montecarlo:\n")
    vd = pd.DataFrame([{"N": k[0], "T": k[1], "k": k[2], "tamano_5pct": v_["tamano_5pct"], "potencia": v_["potencia"], "R": v_["R"], "B": v_["B"],
                        "banda": banda_tamano(v_["tamano_5pct"])} for k, v_ in res["validacion"].items()])
    L.append(md_tabla(vd, list(vd.columns)))
    L.append("\n## Comprobación previa por MDE (adenda 1.3)\n")
    L.append("El Anexo B no fija referencia ni δ para la familia F: no hay umbral con el que declarar NO ESTIMABLE por variación; el MDE (al 80 %, bilateral 5 %, R = 2.000, SEED 20261010, σ ya vista y "
             "declarada) se publica como diagnóstico y está en la columna `mde` de tabla.csv. Se calculó y registró antes de estimar.\n")
    L.append("## Fuera de muestra (misma muestra, bloques con embargo)\n")
    L.append(f"Modelo F1-ECM frente a AR(4) y ECM v1 aproximado; {fom['n_prueba']} observaciones de prueba. RMSE (en %, un paso): {fom['rmse_pct']}.\n")
    L.append(f"- DM-HLN F1-ECM frente a AR(4): {fom['dm_F1ECM_vs_AR4']}; frente a ECM v1: {fom['dm_F1ECM_vs_ECMv1']}.")
    L.append(f"- Clark-West (AR(4) anidado en F1-ECM): {fom['cw_AR4_vs_F1ECM']}; Giacomini-White frente a AR(4): {fom['gw_vs_AR4']}.")
    L.append(f"- Conjunto de confianza de modelos (10 %): {fom['mcs']['dentro_90']}; p del MCS: {fom['mcs']['p']}.\n")
    L.append("## F2-A2, F3 y F4\n")
    o = tabla[tabla.id.str.match(r"^(F2-A2|F3|F4)")][["id", "estado", "muestra", "valor", "ic95_lo", "ic95_hi", "clasificacion_v18"]]
    L.append(md_tabla(o, list(o.columns)))
    L.append("\n## F1-P-E1P2 (CS-ARDL, NO APTO, descriptivo)\n")
    pe = res["pe"]
    L.append(f"N = {pe['N']}, T = {pe['T']}: θ grupo medio {pe['theta_mg']:.2f}, recortada {pe['theta_recortada']:.2f}, mediana {pe['theta_mediana']:.2f}; publicado en V15 E1-P2: 0,64 y en V16 Q9-c: 0,84.\n")
    L.append("## Raíces unitarias nacionales (ADF y KPSS)\n")
    sn = pd.DataFrame(res["diag"]["series_nacionales"]).T.reset_index().rename(columns={"index": "serie"})
    L.append(md_tabla(sn, list(sn.columns)))
    L.append("\nLectura: si una serie del vector no es I(1), la cointegración no está bien definida; el ln del precio real rechaza la raíz unitaria en niveles (ADF) y no rechaza la "
             "estacionariedad (KPSS), de modo que el contraste de límites se interpreta con esa cautela. Placebos, pretendencias y F efectivo de Montiel Olea-Pflueger no aplican a F1-F2 "
             "(sin instrumento ni evento); en F3-R1 se publica el F de primera etapa agrupado.\n")
    L.append("## Diagnósticos\n")
    L.append("```json\n" + json.dumps(res["diag"], ensure_ascii=False, indent=1, default=str) + "\n```\n")
    L.append("## Notas de lectura\n- Panel de 33-38 provincias (no 39): el valor tasado anual tiene huecos en cinco provincias y 11 están selladas (v6); las unidades de V15/V16 no afectan al nivel provincial.\n"
             "- Renta de los hogares provincial y hogares provinciales anteriores a 2021 no están en el repositorio (`posterior_prereg`, sin red): se usa el PIB provincial corriente por habitante, "
             "real, como sustituto declarado, y la población como sustituto de los hogares en F2.\n"
             "- Población nacional trimestral: 44 de los 110 trimestres de la ventana están interpolados; CLAUDE.md los limita a robustez, y F1-R1-v5 repite el modelo sin población.\n"
             "- Clase provisional hasta I8 (réplica ciega, B6). Desviaciones: docs/v18/desviaciones_f_e7.md.\n")
    (salida / "informe.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    out = Path(args.salida) if args.salida else OUT
    resu = main(rapido=args.rapido, salida=out)
    escribir(resu, out)
    REG.flush()
    print(f"f_conjunto: {len(FILAS)} filas, {len(HECHOS)} cifras -> {out}")
