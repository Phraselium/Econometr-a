#!/usr/bin/env python3
"""V8-F4 M5: instrumentos externos (candidatos a C3). IV1 shocks JK, IV2 empuje migratorio (shift-share), IV3 Bartik (panel CCAA).

Hipotesis confirmatorias H8-5, H8-6, H8-7 (familia Holm). Usa src/v8/herramientas/lp.py (lp_iv, lp_iv_agregado, placebo_permutacion_iv, lp_panel).
SIN red: los datos de Eurostat los descarga una sola vez src/v8/fetch_m5.py (data/raw/v8/eurostat_migr/).
Determinista (SEED=20261010, un hilo). Uso: python3 src/v8/m5_lpiv.py [--rapido] [--salida DIR]
Referencias de metodo NO VERIFICADAS (sin acceso a Crossref): Stock-Watson (2018); Anderson-Rubin (1949); Goldsmith-Pinkham, Sorkin y Swift (2020);
Borusyak, Hull y Jaravel (2022); Jarocinski y Karadi (2020); Driscoll-Kraay (1998).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry, holm  # noqa: E402
from herramientas import lp as LP  # noqa: E402

SEED = 20261010
NAC = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
PAN = RAIZ / "data" / "processed" / "v8" / "panel_ccaa_q_v8.csv"
EUR = RAIZ / "data" / "raw" / "v8" / "eurostat_migr"
POP = RAIZ / "data" / "raw" / "v8" / "eurostat_migr_pop1ctz_es.csv"
SCRIPT = "src/v8/m5_lpiv.py"
PERIODOS = ["P1", "P2", "P3", "P4", "P5"]
NUTS_INE = {"ES11": 12, "ES12": 3, "ES13": 6, "ES21": 16, "ES22": 15, "ES23": 17, "ES24": 2, "ES30": 13, "ES41": 7, "ES42": 8,
            "ES43": 11, "ES51": 9, "ES52": 10, "ES53": 4, "ES61": 1, "ES62": 14, "ES70": 5}
NUTS_TODOS = list(NUTS_INE) + ["ES63", "ES64"]
SECTORES = ["A", "B-E", "F", "G-I", "J", "K", "L", "M_N", "O-Q", "R-U"]
AVISO = ("Capa C3 solo si cumple los cuatro requisitos de §6 (F efectivo >= 10, AR que excluye el 0, pretendencias no significativas, permutacion del instrumento); "
         "si no, C4 y sin lenguaje causal. La permutacion del instrumento (antes «placebo») es un contraste de significacion de la forma reducida de baja potencia (Y7), "
         "no una prueba independiente de exogeneidad; pretendencias y permutacion son condiciones necesarias, no suficientes. Exclusion del instrumento no verificable con los datos. "
         "Los p unilaterales de AR usan el signo A PRIORI de la primera etapa (pi > 0), no el estimado.")
COLS_COEF = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio",
             "variable", "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad",
             "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable",
             "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0",
             "cumple_multiverso", "destacado", "motivo_destacado", "script", "horizonte", "p_ar_unilateral", "p_ar_bilateral", "ar_acotado"]
COLS_ATR = ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "capa", "notas",
            "variante", "principal", "vota_s9", "motivo_vota_s9"]


# ---------------------------------------------------------------- utilidades generales
def bh(pvals: dict, q: float = 0.10) -> dict:
    """Benjamini-Hochberg: devuelve p ajustados (q-values) por nombre."""
    items = sorted(((k, v) for k, v in pvals.items() if np.isfinite(v)), key=lambda kv: kv[1])
    m = len(items)
    out, run = {k: np.nan for k in pvals}, 1.0
    for i in range(m - 1, -1, -1):
        k, p = items[i]
        run = min(run, p * m / (i + 1))
        out[k] = min(1.0, run)
    return out


def ar_ext(lo, hi, acotado, beta, se):
    """Conjunto AR con extremos +-inf cuando el conjunto llega al borde de la rejilla (no acotado)."""
    if acotado is None or (isinstance(acotado, float) and np.isnan(acotado)) or bool(acotado):
        return lo, hi
    umbral = 1000 * se if (se is not None and np.isfinite(se) and se > 0) else 0.0
    cen = beta if np.isfinite(beta) else 0.0
    lo2 = -np.inf if (not np.isfinite(lo) or lo < cen - umbral) else lo
    hi2 = np.inf if (not np.isfinite(hi) or hi > cen + umbral) else hi
    return lo2, hi2


def _prep(y, endog, instr, controles, rezagos, acumulado, h=None, agregado=None, hac="h+1"):
    M, zc = LP._iv_muestra(y, endog, instr, controles, h, rezagos, acumulado, agregado)
    L = LP._hac_L(hac, agregado[1]) if agregado else LP._hac_L(hac, h)
    return LP._iv_preparar(M, zc, L)


def p_uni_apriori(y, endog, instr, lado, controles=None, rezagos=2, acumulado=True, h=None, agregado=None):
    """p unilateral de Anderson-Rubin (H0: beta=0) con el signo A PRIORI de la primera etapa (pi > 0; §6), no el estimado (revision F4, J3).
    Misma muestra y HAC que lp_iv / lp_iv_agregado (se usa la utilidad de la herramienta con signo_pi=+1; la herramienta no se modifica)."""
    P = _prep(y, endog, instr, controles, rezagos, acumulado, h, agregado)
    return float(LP._ar_pvalor(P, 0.0, lado, signo_pi=1.0))


def etapa_agregada(y, endog, instr, controles=None, rezagos=2, acumulado=True, agregado=(4, 8)):
    """UNA sola regresion (la agregada, la de F y AR): pi y t de la primera etapa (z parcializado), F efectivo y t de la forma reducida (t_AR(0))."""
    P = _prep(y, endog, instr, controles, rezagos, acumulado, None, agregado)
    pi, F = LP._iv_primera_etapa(P)
    t_rf = LP._ar_en(P, 0.0)[1]
    pi0 = float(pi[0])
    return {"pi": pi0, "t_pi": float(np.sign(pi0) * np.sqrt(F)), "F": float(F), "t_rf": float(t_rf), "signo_rf": int(np.sign(t_rf)), "n": int(P["n"])}


def aplica_apriori(por_h, ags, lado, y, x, z, controles, rezagos, hs):
    """Sustituye ar_p_menor/ar_p_mayor (signo estimado) por los de signo a priori en las filas por horizonte y en los agregados."""
    col = "ar_p_menor" if lado == "menor" else "ar_p_mayor"
    por_h[col + "_estimado"] = por_h[col]
    por_h[col] = [p_uni_apriori(y, x, z, lado, controles, rezagos, True, h=int(h)) for h in por_h["h"]]
    pa = p_uni_apriori(y, x, z, lado, controles, rezagos, True, agregado=hs)
    for ag in ags:
        ag[col + "_estimado"] = ag[col]
        ag[col] = pa
    return por_h


def evalua_c3(F: float, ar_lo: float, ar_hi: float, acotado: bool, pre_p: list, p_perm: float) -> dict:
    """Requisitos de C3 de §6 (los cuatro a la vez) + variante laxa informativa. `perm_instrumento_ok` = permutacion del instrumento (J18):
    no es una prueba independiente de exogeneidad."""
    f_ok = bool(np.isfinite(F) and F >= 10)
    ar_excl = bool(acotado and np.isfinite(ar_lo) and (ar_lo > 0 or ar_hi < 0))
    pre = [p for p in pre_p if np.isfinite(p)]
    pre_ok = bool(len(pre) > 0 and all(p >= 0.05 for p in pre))
    pl_ok = bool(np.isfinite(p_perm) and p_perm < 0.05)
    return {"f_ok": f_ok, "ar_excluye_0": ar_excl, "pretendencias_ok": pre_ok, "perm_instrumento_ok": pl_ok,
            "cumple_c3": bool(f_ok and ar_excl and pre_ok and pl_ok),
            "c3_laxo": bool((f_ok or ar_excl) and pre_ok and pl_ok)}


UMBRAL_DY = 1.0   # |variacion observada| < 1 pp (log x100): pct_total vacio (J4)


def pct_total(contrib, dy):
    return 100 * contrib / dy if (np.isfinite(dy) and abs(dy) >= UMBRAL_DY) else np.nan


def voto_s9(F, acot68, ambito="nacional"):
    """Regla R4 de §9 (desviaciones.md): lpiv vota solo con F >= 10 o AR 68 % acotado; si no, se abstiene (vota_s9 = 'no')."""
    if ambito == "ccaa_panel":
        return "no", "efecto relativo entre CCAA (efectos de anio absorben lo nacional): no comparable con una contribucion nacional"
    if (np.isfinite(F) and F >= 10) or bool(acot68):
        return "si", ""
    return "no", f"F={F:.2f} < 10 y AR 68 % no acotado: se abstiene (C4 informativa)"


def anual_media(df: pd.DataFrame, col: str, grupo=None) -> pd.Series:
    """Media anual de una serie trimestral solo con los 4 trimestres presentes."""
    d = df.copy()
    d["anio"] = d["trimestre"].str[:4].astype(int)
    gb = [grupo, "anio"] if grupo else ["anio"]
    g = d.groupby(gb)[col]
    return g.mean().where(g.count() == 4)


def trimestres_periodo(nac: pd.DataFrame) -> dict:
    return {p: nac.loc[nac["periodo_h8"] == p, "trimestre"].tolist() for p in PERIODOS}


def anios_periodo(nac: pd.DataFrame) -> dict:
    """Anios con >= 3 trimestres dentro del periodo."""
    out = {}
    for p in PERIODOS:
        q = nac.loc[nac["periodo_h8"] == p, "trimestre"].str[:4].astype(int)
        c = q.value_counts()
        out[p] = sorted(c[c >= 3].index.tolist())
    return out


# ---------------------------------------------------------------- IV1
def spec_iv1(y, x, z, ctrl, hs, h_max, h_min, n_perm, seed):
    por_h = LP.lp_iv(y, x, z, controles=ctrl, H=h_max, rezagos=2, acumulado=True, H_min=h_min)
    ag95 = LP.lp_iv_agregado(y, x, z, controles=ctrl, hs=hs, rezagos=2, acumulado=True, nivel=0.95)
    ag90 = LP.lp_iv_agregado(y, x, z, controles=ctrl, hs=hs, rezagos=2, acumulado=True, nivel=0.90)
    ag68 = LP.lp_iv_agregado(y, x, z, controles=ctrl, hs=hs, rezagos=2, acumulado=True, nivel=0.68)
    pl = LP.placebo_permutacion_iv(y, x, z, controles=ctrl, rezagos=2, acumulado=True, agregado=hs, modo="iid", n_perm=n_perm, seed=seed)
    return por_h, ag95.iloc[0], ag90.iloc[0], ag68.iloc[0], pl


def evalua_spec(por_h, ag95, pl):
    pre = por_h.loc[por_h["h"] < 0, "ar_p_dos"].tolist()
    return evalua_c3(ag95["F_robusto"], ag95["ar_lo"], ag95["ar_hi"], bool(ag95["ar_acotado"]), pre, pl["p_perm"])


# ---------------------------------------------------------------- IV2
def construye_iv2(imm: pd.DataFrame, pop: pd.DataFrame, a_es: pd.Series, anio0=2002, anio1=2024,
                  stock_min=5000, flujo_min=300, normalizar=True):
    """Instrumento shift-share anual. imm: geo, citizen, anio, valor; pop: stock por ciudadania en ES a 1-1-2002 (Serie citizen, valor).
    Devuelve (Z serie por anio, tabla de origenes, destinos usados)."""
    anios = list(range(anio0, anio1 + 1))
    tot = imm[(imm["citizen"] == "TOTAL") & (imm["geo"] != "ES")]
    cnt = tot.groupby("geo")["anio"].apply(lambda s: set(anios) <= set(s))
    destinos = sorted(cnt[cnt].index)
    stock = pop[(pop["citizen"].str.len() == 2) & (pop["citizen"] != "ES") & (pop["valor"] >= stock_min)].set_index("citizen")["valor"]
    sub = imm[imm["geo"].isin(destinos) & imm["citizen"].isin(stock.index)]
    filas = []
    for c in stock.index:
        s = sub[(sub["citizen"] == c) & (sub["geo"] != c)].groupby("anio")["valor"].sum().reindex(anios)
        if s.notna().sum() < len(anios):
            s = s.fillna(0.0)
        filas.append(s.rename(c))
    F = pd.concat(filas, axis=1)
    base = F.loc[anio0:anio0 + 2].mean()
    orig = base[base >= flujo_min].index
    share = stock.loc[orig] / stock.loc[orig].sum()
    dF = F[orig].diff() / base[orig] if normalizar else F[orig].diff() / 1e5
    Z = (dF * share).sum(axis=1, min_count=1)
    Z.iloc[0] = np.nan
    tabla = pd.DataFrame({"origen": orig, "cuota_2002": share.values, "stock_2002": stock.loc[orig].values, "flujo_medio_0204": base[orig].values})
    return Z, tabla.sort_values("cuota_2002", ascending=False), destinos


# ---------------------------------------------------------------- IV3: panel Bartik
def construye_bartik(sec: pd.DataFrame, anio_base=2008):
    """Bartik leave-one-out por NUTS2. sec: geo, nace_r2, anio, valor (miles). Devuelve (B total, B por sector, cuotas, E total)."""
    s = sec[sec["geo"].isin(NUTS_TODOS) & sec["nace_r2"].isin(SECTORES)]
    E = s.pivot_table(index=["geo", "nace_r2"], columns="anio", values="valor", aggfunc="sum").reindex(
        pd.MultiIndex.from_product([NUTS_TODOS, SECTORES], names=["geo", "nace_r2"]))
    sin_base = E[anio_base].isna().groupby(level="geo").any()   # alguna celda sin dato (confidencial) en el año base
    E = E.fillna(0.0)   # el 0 solo entra en el total nacional del leave-one-out
    anios = sorted(E.columns)
    cuotas = E[anio_base].unstack("nace_r2")[SECTORES]
    cuotas = cuotas.div(cuotas.sum(axis=1), axis=0)
    # Sin cuota del año base el instrumento no está definido: la unidad queda fuera (NaN), no con cuota 0
    # (errata V8-M5, B-3 de V16, orden expresa del autor: Navarra ES22 y La Rioja ES23, sector L de 2008).
    cuotas.loc[sin_base[sin_base].index.intersection(cuotas.index)] = np.nan
    nac = E.groupby(level="nace_r2").sum()   # (sector x anio)
    out = {}
    for c in NUTS_INE:
        Ec = E.loc[c]                         # sector x anio
        resto = (nac - Ec).clip(lower=1e-6)   # resto de NUTS2 (leave-one-out)
        g = 100 * np.log(resto).diff(axis=1)
        out[c] = g.mul(cuotas.loc[c], axis=0)  # contribucion por sector
    Bs = pd.concat(out, names=["geo", "nace_r2"])   # (geo,sector) x anio
    B = Bs.groupby(level="geo").sum(min_count=1)
    tot = sec[(sec["nace_r2"] == "TOTAL") & sec["geo"].isin(NUTS_TODOS)].pivot_table(index="geo", columns="anio", values="valor", aggfunc="sum")
    return B, Bs, cuotas, tot


def panel_anual(nac_q: pd.DataFrame, pan_q: pd.DataFrame, B: pd.DataFrame, Etot: pd.DataFrame) -> pd.DataFrame:
    p = pan_q.copy()
    p["l_precio"] = 100 * np.log(p["valor_tasado_ccaa"] / p["ipc_general"])
    p["l_ipv"] = 100 * np.log(p["ipv"] / p["ipc_general"])
    p["l_alq"] = 100 * np.log(p["ipc_alquiler"] / p["ipc_general"])
    cols = {}
    for c in ["l_precio", "l_ipv", "l_alq"]:
        cols[c] = anual_media(p, c, grupo="codigo_ine_ccaa")
    A = pd.DataFrame(cols).reset_index().rename(columns={"codigo_ine_ccaa": "ent", "anio": "t"})
    filas = []
    for nuts, ine in NUTS_INE.items():
        lnE = 100 * np.log(Etot.loc[nuts])
        d = pd.DataFrame({"ent": ine, "t": lnE.index.astype(int), "lnE": lnE.values, "x": lnE.diff().values,
                          "z": B.loc[nuts].reindex(lnE.index).values})
        filas.append(d)
    return A.merge(pd.concat(filas), on=["ent", "t"], how="inner").sort_values(["ent", "t"]).reset_index(drop=True)


def _diseno(d: pd.DataFrame, y: str, hs, x="x", z="z", ctrl=True):
    """Dependiente (media de y_{t+k}, k en hs; o y_{t+h} si hs es int), z_t, x_t y controles y_{t-1}(o relativo al dep), x_{t-1}, z_{t-1}."""
    g = d.groupby("ent")
    if isinstance(hs, (int, np.integer)):
        hs = [int(hs)]
    dep = pd.concat([g[y].shift(-k) for k in hs], axis=1).mean(axis=1, skipna=False)
    hmin = min(hs)
    out = pd.DataFrame({"ent": d["ent"], "t": d["t"], "dep": dep, "x": d[x], "z": d[z]})
    if ctrl:
        out["yl"] = g[y].shift(1 - min(hmin, 0))
        out["xl"] = g[x].shift(1)
        out["zl"] = g[z].shift(1)
    return out.dropna().set_index(["ent", "t"])


def _ajusta(dd, depcol, regs, bw):
    from linearmodels.panel import PanelOLS
    r = PanelOLS(dd[depcol], dd[regs], entity_effects=True, time_effects=True).fit(cov_type="kernel", kernel="bartlett", bandwidth=bw)
    return float(r.params["z"]), float(r.std_errors["z"]), int(r.nobs)


def panel_iv(d: pd.DataFrame, y: str, hs, bw: int, nivel_lista=(0.68, 0.90, 0.95), grid_n=4001):
    """LP-IV de panel (efectos fijos de CCAA y de anio, Driscoll-Kraay). Un instrumento (z).
    La forma reducida de y - b0*x sobre z es lineal en b0; el error DK es cuadratico en b0: se calcula exacto con 3 ajustes (b0=0,1,-1).
    Devuelve dict con beta (Wald), F primera etapa (t^2 de z sobre x), p AR bilateral/unilaterales y conjuntos AR."""
    dd = _diseno(d, y, hs)
    regs = ["z"] + [c for c in ("yl", "xl", "zl") if c in dd.columns]
    res = {}
    for b0 in (0.0, 1.0, -1.0):
        dd["w"] = dd["dep"] - b0 * dd["x"]
        res[b0] = _ajusta(dd, "w", regs, bw)
    c0, c1, cm = res[0.0][0], res[1.0][0], res[-1.0][0]
    s0, s1, sm = res[0.0][1], res[1.0][1], res[-1.0][1]
    pix = c0 - c1          # primera etapa por identidad: coef(z; x) = c0 - c1
    a = s0 ** 2
    n = res[0.0][2]
    # primera etapa directa (F efectivo con 1 instrumento = t^2 robusto)
    dd["w"] = dd["x"]
    b_fs, se_fs, _ = _ajusta(dd, "w", regs, bw)
    F = (b_fs / se_fs) ** 2

    # varianza de (pi_y - b0 pi_x) como forma cuadratica en b0: V(b0) = Vyy - 2 b0 Vyx + b0^2 Vxx;  V(1)=a'+..., ver derivacion:
    # s(b)^2 con dep = y - b x -> V(b) = Vyy - 2 b Vyx + b^2 Vxx. V(0)=Vyy=a; V(1)-V(-1) = -4 Vyx; V(1)+V(-1)-2V(0) = 2 Vxx.
    Vyy = a
    Vyx = -(s1 ** 2 - sm ** 2) / 4.0
    Vxx = (s1 ** 2 + sm ** 2 - 2 * a) / 2.0

    def estad(b0):
        coef = c0 - b0 * pix
        var = Vyy - 2 * b0 * Vyx + b0 ** 2 * Vxx
        return coef / np.sqrt(max(var, 1e-300))

    beta = c0 / pix if abs(pix) > 1e-12 else np.nan
    se_d = np.sqrt(max(Vyy - 2 * beta * Vyx + beta ** 2 * Vxx, 0)) / abs(pix) if np.isfinite(beta) else np.nan
    t0 = estad(0.0)
    T = t0 * 1.0     # signo A PRIORI de la primera etapa (pi > 0; revision F4, J3), no el estimado
    sc = max(se_d, 1e-3) if np.isfinite(se_d) else 1.0
    cen = beta if np.isfinite(beta) else 0.0
    grid = cen + sc * np.sinh(np.linspace(-12, 12, grid_n))
    tg = np.array([estad(g) for g in grid])
    out = {"beta": beta, "se": se_d, "F_robusto": F, "pi_x": pix, "pi_y": c0, "n": n, "ar_p_dos": float(2 * stats.norm.sf(abs(t0))),
           "ar_p_menor": float(stats.norm.cdf(T)), "ar_p_mayor": float(stats.norm.sf(T)), "t_rf": float(t0)}
    for nv in nivel_lista:
        crit = stats.norm.ppf(0.5 + nv / 2)
        idx = np.where(np.abs(tg) <= crit)[0]
        k = f"{int(round(nv * 100))}"
        if len(idx):
            acot = not (idx[0] == 0 or idx[-1] == grid_n - 1)
            out[f"ar_lo{k}"], out[f"ar_hi{k}"], out[f"ar_acotado{k}"] = float(grid[idx[0]]), float(grid[idx[-1]]), bool(acot)
        else:
            out[f"ar_lo{k}"] = out[f"ar_hi{k}"] = np.nan
            out[f"ar_acotado{k}"] = True
    return out


def panel_permutacion(d: pd.DataFrame, y: str, hs, bw: int, n_perm: int, seed: int):
    """Permutacion de los anios del Bartik (todas las CCAA a la vez, conserva la seccion cruzada): p_perm de |t| de forma reducida."""
    rng = np.random.default_rng(seed)
    base = d.copy()
    anios = np.sort(base["t"].unique())
    zpiv = base.pivot(index="t", columns="ent", values="z")

    def t_rf(dat):
        dd = _diseno(dat, y, hs)
        regs = ["z"] + [c for c in ("yl", "xl", "zl") if c in dd.columns]
        b, se, _ = _ajusta(dd, "dep", regs, bw)
        return b / se

    t_obs = t_rf(base)
    ts = np.empty(n_perm)
    for i in range(n_perm):
        perm = rng.permutation(len(anios))
        zp = pd.DataFrame(zpiv.values[perm], index=zpiv.index, columns=zpiv.columns).stack().rename("z").reset_index()
        dat = base.drop(columns="z").merge(zp, on=["t", "ent"], how="left")
        ts[i] = t_rf(dat)
    return {"t_obs": float(t_obs), "p_perm": float((1 + np.sum(np.abs(ts) >= abs(t_obs))) / (1 + n_perm)), "n_perm": n_perm}


def rotemberg(d: pd.DataFrame, Bs: pd.DataFrame) -> pd.DataFrame:
    """Pesos de Rotemberg (Goldsmith-Pinkham et al., 2020) del Bartik con efectos fijos de CCAA y anio:
    alpha_s = (B~_s' x~) / (B~' x~), con B~, x~ sin efectos de CCAA y de anio (panel equilibrado tras recorte)."""
    base = d.dropna(subset=["x", "z"]).copy()
    ents = sorted(base["ent"].unique())
    ts_ = sorted(base["t"].unique())
    inv = {v: k for k, v in NUTS_INE.items()}

    def dm(M):
        M = np.asarray(M, float)
        return M - M.mean(0, keepdims=True) - M.mean(1, keepdims=True) + M.mean()

    X = dm(base.pivot(index="t", columns="ent", values="x").reindex(index=ts_, columns=ents).values)
    filas = []
    for s_ in SECTORES:
        M = np.column_stack([Bs.loc[(inv[e], s_)].reindex(ts_).values for e in ents])
        Mt = dm(M)
        filas.append({"sector": s_, "num": float((Mt * X).sum()), "g_medio": float(np.nanmean(M))})
    r = pd.DataFrame(filas)
    r["alpha"] = r["num"] / r["num"].sum()
    return r.drop(columns="num").sort_values("alpha", key=abs, ascending=False)


# ---------------------------------------------------------------- escritura de filas
def fila_coef(modelo_id, familia, mercado, ambito, periodo, dep, transf, medida, variable, r, n, f1, capa, hlab, script=SCRIPT,
              p_aj=np.nan, met_aj="", pu=np.nan, tipo_ee="HAC Newey-West (h+1); IC AR"):
    beta, se = r.get("beta", np.nan), r.get("se", np.nan)
    z = stats.norm.ppf(0.975)
    lo = r.get("lo", beta - z * se if np.isfinite(se) else np.nan)
    hi = r.get("hi", beta + z * se if np.isfinite(se) else np.nan)
    arl, arh = r.get("ar_lo", r.get("ar_lo95", np.nan)), r.get("ar_hi", r.get("ar_hi95", np.nan))
    arl, arh = ar_ext(arl, arh, r.get("ar_acotado", r.get("ar_acotado95", np.nan)), beta, se)
    pb = r.get("ar_p_dos", np.nan)
    d = {c: np.nan for c in COLS_COEF}
    d.update({"modelo_id": modelo_id, "modulo": "M5", "familia_modelo": familia, "mercado": mercado, "ambito": ambito, "periodo": periodo,
              "dependiente": dep, "transformacion": transf, "medida_precio": medida, "variable": variable, "beta": beta, "ee": se,
              "tipo_ee": tipo_ee, "t": beta / se if (np.isfinite(se) and se > 0) else np.nan, "p": pb, "p_ajustado": p_aj, "metodo_ajuste": met_aj,
              "ic95_lo": lo, "ic95_hi": hi, "n": n, "f1_etapa": f1, "ar_lo": arl, "ar_hi": arh, "capa": capa, "script": script,
              "horizonte": hlab, "p_ar_unilateral": pu, "p_ar_bilateral": pb,
              "ar_acotado": r.get("ar_acotado", r.get("ar_acotado95", np.nan))})
    return d


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M5"))
    a = ap.parse_args()
    t_ini = time.time()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    n_perm = 99 if a.rapido else 499
    n_perm_pan = 49 if a.rapido else 199
    reg = Registry(out / "registro.csv")
    np.random.seed(SEED)

    nac = pd.read_csv(NAC)
    pan = pd.read_csv(PAN)
    nac["anio"] = nac["trimestre"].str[:4].astype(int)
    filas_coef, filas_atr, notas, hip_rows = [], [], [], []
    per_q = trimestres_periodo(nac)
    per_a = anios_periodo(nac)
    detalle = {}

    # ===================== IV1
    z1 = nac["jk_mp"].values
    ctrl = nac[["covid"]].values
    x_eur = nac["euribor_1y"].diff().values
    x_hip = nac["tipo_hip_bde"].diff().values
    mercados = {"compra": ("ln_p_tasado_real", "valor tasado MIVAU real (IPC general)"),
                "alquiler": ("ln_ipc_alquiler_real", "IPC alquiler real (IPC general)")}
    specs1 = [("compra", "euribor", x_eur, "ln_p_tasado_real"), ("alquiler", "euribor", x_eur, "ln_ipc_alquiler_real"),
              ("compra", "hip_bde", x_hip, "ln_p_tasado_real"), ("alquiler", "hip_bde", x_hip, "ln_ipc_alquiler_real"),
              ("compra", "euribor", x_eur, "ln_ipv_real"), ("compra", "euribor_sin_covid", x_eur, "ln_p_tasado_real")]
    iv1 = {}
    for mercado, endog, x, col in specs1:
        y = 100 * nac[col].values
        medida = {"ln_p_tasado_real": "valor tasado real", "ln_ipc_alquiler_real": "IPC alquiler real", "ln_ipv_real": "IPV INE real"}[col]
        c_ = None if endog == "euribor_sin_covid" else ctrl
        if endog == "euribor_sin_covid":   # robustez: sin la ficticia COVID
            pass
        por_h, ag95, ag90, ag68, pl = spec_iv1(y, x, z1, c_, (4, 8), 12, -4, n_perm, SEED)
        por_h = aplica_apriori(por_h, [ag95, ag90, ag68], "menor", y, x, z1, c_, 2, (4, 8))
        etapa = etapa_agregada(y, x, z1, c_, 2, True, (4, 8))
        ev = evalua_spec(por_h, ag95, pl)
        mid = f"M5_IV1_{mercado}_{endog}_{col}"
        iv1[mid] = (por_h, ag95, ag90, ag68, pl, ev, mercado, endog, col, etapa)
        notas_spec = (f"endogena={endog}; 2 rezagos; acumulado y_(t+h)-y_(t-1); jk_mp 1999Q1-2025Q3; pretendencias h=-4..-2; "
                      f"permutacion del instrumento p_perm={pl['p_perm']:.3f} (permutacion libre, {n_perm}); {ev}")
        for _, r in por_h.iterrows():
            capa_h = "C4"
            f = fila_coef(f"{mid}_h{int(r['h'])}", "lp_iv", mercado, "nacional", "completo", col, "100*ln real; acumulado desde t-1", medida,
                          endog, r.to_dict(), int(r["n"]), r["F_robusto"], capa_h, str(int(r["h"])),
                          pu=r["ar_p_menor"])
            filas_coef.append(f)
            reg.log("V8-M5", f"{mid}_h{int(r['h'])}", f"LP-IV {col} ~ d({endog}) | jk_mp, h={int(r['h'])}", "", "", int(r["n"]), np.nan, np.nan,
                    np.nan, np.nan, r["beta"], r["ar_p_dos"], notas_spec if r["h"] == 0 else "")
        rag = ag95.to_dict()
        capa_ag = "C3" if ev["cumple_c3"] else "C4"
        f = fila_coef(f"{mid}_h4-8", "lp_iv_agregado", mercado, "nacional", "completo", col, "100*ln real; media h=4-8 acumulada", medida, endog,
                      rag, int(ag95["n"]), ag95["F_robusto"], capa_ag, "4-8", pu=ag95["ar_p_menor"])
        filas_coef.append(f)
        reg.log("V8-M5", f"{mid}_h4-8", f"LP-IV agregado h=4-8 {col} ~ d({endog}) | jk_mp", "", "", int(ag95["n"]), np.nan, np.nan, np.nan, np.nan,
                ag95["beta"], ag95["ar_p_dos"], notas_spec)

    # --- IV1: hipotesis H8-5, H8-6 (spec principal: euribor, valor tasado / alquiler)
    base5 = iv1["M5_IV1_compra_euribor_ln_p_tasado_real"]
    base6 = iv1["M5_IV1_alquiler_euribor_ln_ipc_alquiler_real"]

    # ===================== IV2
    iv2_fallo = None
    iv2 = None
    try:
        imm = pd.read_csv(EUR / "migr_imm1ctz_ue.csv")
        pop0 = pd.read_csv(POP)
        pop0["citizen"] = pop0["serie"].str.split("|").str[1]
        pop0 = pop0[pop0["periodo"] == 2002][["citizen", "valor"]]
        a_es = imm[(imm["geo"] == "ES") & (imm["citizen"] == "TOTAL")].set_index("anio")["valor"].sort_index()
        Z2, tab_orig, dest = construye_iv2(imm, pop0, a_es)
        tab_orig.to_csv(out / "iv2_origenes.csv", index=False)
        A = a_es.reindex(range(2002, 2025))
        x2 = (A.diff() / 1e5)
        yq = anual_media(nac, "ln_ipc_alquiler_real") * 100
        anios = list(range(2002, 2026))
        y2 = yq.reindex(anios).values
        x2v = x2.reindex(anios).values
        z2v = Z2.reindex(anios).values
        hs2 = (1, 2)
        por_h2 = LP.lp_iv(y2, x2v, z2v, controles=None, H=4, rezagos=1, acumulado=True, H_min=-2)
        ag2 = {nv: LP.lp_iv_agregado(y2, x2v, z2v, hs=hs2, rezagos=1, acumulado=True, nivel=nv).iloc[0] for nv in (0.68, 0.90, 0.95)}
        por_h2 = aplica_apriori(por_h2, list(ag2.values()), "mayor", y2, x2v, z2v, None, 1, hs2)
        etapa2 = etapa_agregada(y2, x2v, z2v, None, 1, True, hs2)
        pl2 = LP.placebo_permutacion_iv(y2, x2v, z2v, rezagos=1, acumulado=True, agregado=hs2, modo="desplazamiento", n_perm=n_perm, seed=SEED)
        pre2 = por_h2.loc[por_h2["h"] < 0, "ar_p_dos"].tolist()
        ev2 = evalua_c3(ag2[0.95]["F_robusto"], ag2[0.95]["ar_lo"], ag2[0.95]["ar_hi"], bool(ag2[0.95]["ar_acotado"]), pre2, pl2["p_perm"])
        iv2 = (por_h2, ag2, pl2, ev2, tab_orig, dest, etapa2)
        n2 = 4
        for _, r in por_h2.iterrows():
            filas_coef.append(fila_coef(f"M5_IV2_alquiler_h{int(r['h'])}", "lp_iv", "alquiler", "nacional", "completo", "ln_ipc_alquiler_real",
                                        "100*ln real anual; acumulado desde t-1; por 100.000 llegadas", "IPC alquiler real", "d_llegadas_100k", r.to_dict(),
                                        int(r["n"]), r["F_robusto"], "C4", str(int(r["h"])), pu=r["ar_p_mayor"]))
            reg.log("V8-M5", f"M5_IV2_alquiler_h{int(r['h'])}", f"LP-IV anual alquiler ~ d(llegadas) | shift-share UE, h={int(r['h'])}", "2002", "2025",
                    int(r["n"]), np.nan, np.nan, np.nan, np.nan, r["beta"], r["ar_p_dos"], "")
        rag = ag2[0.95].to_dict()
        filas_coef.append(fila_coef("M5_IV2_alquiler_h1-2", "lp_iv_agregado", "alquiler", "nacional", "completo", "ln_ipc_alquiler_real",
                                    "100*ln real anual; media h=1-2 acumulada; por 100.000 llegadas", "IPC alquiler real", "d_llegadas_100k", rag,
                                    int(ag2[0.95]["n"]), ag2[0.95]["F_robusto"], "C3" if ev2["cumple_c3"] else "C4", "1-2", pu=ag2[0.95]["ar_p_mayor"]))
        reg.log("V8-M5", "M5_IV2_alquiler_h1-2", "LP-IV agregado anual h=1-2 alquiler ~ d(llegadas)", "2002", "2025", int(ag2[0.95]["n"]), np.nan,
                np.nan, np.nan, np.nan, ag2[0.95]["beta"], ag2[0.95]["ar_p_dos"], f"{ev2}; permutacion del instrumento p_perm={pl2['p_perm']:.3f}")
        n2 = int(ag2[0.95]["n"])
    except Exception as e:  # noqa: BLE001
        iv2_fallo = f"{type(e).__name__}: {e}"
        n2 = 0

    # --- IV2b (robustez, exploratorio): instrumento sin normalizar por el flujo base (variacion en 100.000 personas ponderada por cuota)
    iv2b = None
    if iv2 is not None:
        try:
            Z2b, _, _ = construye_iv2(imm, pop0, a_es, normalizar=False)
            z2bv = Z2b.reindex(anios).values
            por_h2b = LP.lp_iv(y2, x2v, z2bv, controles=None, H=4, rezagos=1, acumulado=True, H_min=-2)
            ag2b = {nv: LP.lp_iv_agregado(y2, x2v, z2bv, hs=hs2, rezagos=1, acumulado=True, nivel=nv).iloc[0] for nv in (0.68, 0.90, 0.95)}
            por_h2b = aplica_apriori(por_h2b, list(ag2b.values()), "mayor", y2, x2v, z2bv, None, 1, hs2)
            pl2b = LP.placebo_permutacion_iv(y2, x2v, z2bv, rezagos=1, acumulado=True, agregado=hs2, modo="desplazamiento", n_perm=n_perm, seed=SEED)
            ev2b = evalua_c3(ag2b[0.95]["F_robusto"], ag2b[0.95]["ar_lo"], ag2b[0.95]["ar_hi"], bool(ag2b[0.95]["ar_acotado"]),
                             por_h2b.loc[por_h2b["h"] < 0, "ar_p_dos"].tolist(), pl2b["p_perm"])
            iv2b = (por_h2b, ag2b, pl2b, ev2b)
            for _, r in por_h2b.iterrows():
                filas_coef.append(fila_coef(f"M5_IV2b_alquiler_h{int(r['h'])}", "lp_iv", "alquiler", "nacional", "completo", "ln_ipc_alquiler_real",
                                            "100*ln real anual; acumulado; por 100.000 llegadas; instrumento sin normalizar (IV2b: anadida tras construir el instrumento)", "IPC alquiler real", "d_llegadas_100k",
                                            r.to_dict(), int(r["n"]), r["F_robusto"], "C4", str(int(r["h"])), pu=r["ar_p_mayor"]))
                reg.log("V8-M5", f"M5_IV2b_alquiler_h{int(r['h'])}", f"LP-IV anual alquiler ~ d(llegadas) | shift-share sin normalizar, h={int(r['h'])}", "2002",
                        "2025", int(r["n"]), np.nan, np.nan, np.nan, np.nan, r["beta"], r["ar_p_dos"], "robustez exploratoria; anadida tras construir el instrumento")
            filas_coef.append(fila_coef("M5_IV2b_alquiler_h1-2", "lp_iv_agregado", "alquiler", "nacional", "completo", "ln_ipc_alquiler_real",
                                        "100*ln real anual; media h=1-2; instrumento sin normalizar (IV2b: anadida tras construir el instrumento)", "IPC alquiler real", "d_llegadas_100k", ag2b[0.95].to_dict(),
                                        int(ag2b[0.95]["n"]), ag2b[0.95]["F_robusto"], "C3" if ev2b["cumple_c3"] else "C4", "1-2", pu=ag2b[0.95]["ar_p_mayor"]))
            reg.log("V8-M5", "M5_IV2b_alquiler_h1-2", "LP-IV agregado anual h=1-2 | shift-share sin normalizar", "2002", "2025", int(ag2b[0.95]["n"]), np.nan,
                    np.nan, np.nan, np.nan, ag2b[0.95]["beta"], ag2b[0.95]["ar_p_dos"], f"robustez exploratoria, ANADIDA TRAS CONSTRUIR EL INSTRUMENTO (desviaciones.md); {ev2b}; p_perm={pl2b['p_perm']:.3f}")
        except Exception as e:  # noqa: BLE001
            notas.append(f"IV2b fallido: {e}")

    # ===================== IV3
    iv3 = {}
    iv3_fallo = None
    try:
        sec = pd.read_csv(EUR / "lfst_r_lfe2en2_sector.csv")
        B, Bs, cuotas, Etot = construye_bartik(sec)
        P3 = panel_anual(nac, pan, B, Etot)
        _m3 = P3.reset_index().dropna(subset=["x", "z"])
        n3 = int(_m3["ent"].nunique())  # CCAA con instrumento definido (sin Navarra ni La Rioja: errata B-3)
        hs3 = {"h0": 0, "h1": 1, "h2": 2, "h3": 3, "h4": 4, "h1-2": [1, 2]}
        resultados3 = {}
        for mercado, col, medida in (("compra", "l_precio", "valor tasado real"), ("alquiler", "l_alq", "IPC alquiler real"),
                                     ("compra", "l_ipv", "IPV INE real")):
            for lab, hs in hs3.items():
                bw = (max(hs) if isinstance(hs, list) else hs) + 1
                r = panel_iv(P3, col, hs, bw)
                resultados3[(mercado, col, lab)] = r
            # pretendencia: h=-1 y -2 (forma reducida, mismos controles)
            for lab, hh in (("h-1", -1), ("h-2", -2)):
                resultados3[(mercado, col, lab)] = panel_iv(P3, col, hh, 1)
            if col != "l_ipv":
                resultados3[(mercado, col, "permutacion")] = panel_permutacion(P3, col, [1, 2], 3, n_perm_pan, SEED)
        rot = rotemberg(P3, Bs)
        rot.to_csv(out / "iv3_rotemberg.csv", index=False)
        iv3 = {"res": resultados3, "rot": rot, "P3": P3, "n": n3}
        pvals_bh = {}
        for (mercado, col, lab), r in resultados3.items():
            if lab in ("permutacion",) or lab.startswith("h-"):
                continue
            pvals_bh[f"M5_IV3_{col}_{lab}"] = r["ar_p_dos"]
        padj = bh(pvals_bh)
        for (mercado, col, lab), r in resultados3.items():
            if lab == "permutacion":
                continue
            mid = f"M5_IV3_{col}_{lab}"
            medida = {"l_precio": "valor tasado real", "l_alq": "IPC alquiler real", "l_ipv": "IPV INE real"}[col]
            pre = [resultados3[(mercado, col, k)]["ar_p_dos"] for k in ("h-1", "h-2")]
            plc = resultados3.get((mercado, col, "permutacion"), {"p_perm": np.nan})
            ev = evalua_c3(r["F_robusto"], r["ar_lo95"], r["ar_hi95"], r["ar_acotado95"], pre, plc["p_perm"])
            r["ev"] = ev
            capa = "C3" if (ev["cumple_c3"] and not lab.startswith("h-")) else "C4"
            rr = dict(r)
            rr["ar_lo"], rr["ar_hi"], rr["ar_acotado"] = r["ar_lo95"], r["ar_hi95"], r["ar_acotado95"]
            filas_coef.append(fila_coef(mid, "lp_iv_panel", mercado, "ccaa_panel", "completo", col, "100*ln real anual; por pp de crecimiento del empleo",
                                        medida, "d_ln_empleo", rr, r["n"], r["F_robusto"], capa, lab.replace("h", "", 1) if lab.startswith("h") else lab,
                                        p_aj=padj.get(mid, np.nan), met_aj="BH" if mid in padj else "", pu=r["ar_p_mayor"],
                                        tipo_ee="Driscoll-Kraay (Bartlett, h+1); IC AR"))
            reg.log("V8-M5", mid, f"LP-IV panel {n3} CCAA {col} ~ d_ln_empleo | Bartik 2008 leave-one-out, FE CCAA+anio, DK, h={lab}", "2009", "2025",
                    r["n"], np.nan, np.nan, np.nan, np.nan, r["beta"], r["ar_p_dos"], f"{ev}" if lab == "h1-2" else "")
    except Exception as e:  # noqa: BLE001
        iv3_fallo = f"{type(e).__name__}: {e}"

    # ===================== hipotesis (familia Holm)
    def hip_fila(hid, texto, mercado, p_uni, est, ic, ev, extra, et=None, estado_iv=""):
        et = et or {"pi": np.nan, "t_pi": np.nan, "F": np.nan, "t_rf": np.nan, "signo_rf": 0, "n": 0}
        return {"id": hid, "hipotesis": texto, "mercado": mercado, "estimacion": est, "ar_lo": ic[0], "ar_hi": ic[1],
                "ar_p": p_uni, "signo_pi_apriori": "+ (a priori, §6)", "pi_primera_etapa": et["pi"], "t_primera_etapa": et["t_pi"],
                "F_efectivo": et["F"], "signo_forma_reducida": et["signo_rf"], "t_forma_reducida": et["t_rf"],
                "signo_esperado_forma_reducida": -1 if hid in ("H8-5", "H8-6") else 1,
                **ev, "extra": extra, "estado_iv": estado_iv}

    fs5, fs6 = base5[9], base6[9]
    h5 = hip_fila("H8-5", "Un shock monetario contractivo del BCE reduce el precio real de compra a h = 4-8", "compra",
                  base5[1]["ar_p_menor"], base5[1]["beta"], ar_ext(base5[1]["ar_lo"], base5[1]["ar_hi"], bool(base5[1]["ar_acotado"]), base5[1]["beta"], base5[1]["se"]), base5[5],
                  f"regresion agregada h=4-8 (la de F y AR): pi={fs5['pi']:.3f} (t={fs5['t_pi']:.2f}; esperado > 0), F={fs5['F']:.2f}; forma reducida t_AR(0)={fs5['t_rf']:.2f} (signo esperado negativo); n={int(base5[1]['n'])}; p_perm={base5[4]['p_perm']:.3f}; AR acotado={bool(base5[1]['ar_acotado'])}", fs5)
    h6 = hip_fila("H8-6", "Un shock monetario contractivo del BCE reduce el alquiler real a h = 4-8", "alquiler",
                  base6[1]["ar_p_menor"], base6[1]["beta"], ar_ext(base6[1]["ar_lo"], base6[1]["ar_hi"], bool(base6[1]["ar_acotado"]), base6[1]["beta"], base6[1]["se"]), base6[5],
                  f"regresion agregada h=4-8 (la de F y AR): pi={fs6['pi']:.3f} (t={fs6['t_pi']:.2f}; esperado > 0), F={fs6['F']:.2f}; forma reducida t_AR(0)={fs6['t_rf']:.2f} (signo esperado negativo); n={int(base6[1]['n'])}; p_perm={base6[4]['p_perm']:.3f}; AR acotado={bool(base6[1]['ar_acotado'])}", fs6)
    if iv2 is not None:
        g = iv2[1][0.95]
        h7 = hip_fila("H8-7", "El empuje migratorio aumenta el alquiler real", "alquiler", g["ar_p_mayor"], g["beta"], ar_ext(g["ar_lo"], g["ar_hi"], bool(g["ar_acotado"]), g["beta"], g["se"]), iv2[3],
                      f"regresion agregada anual h=1-2: pi={iv2[6]['pi']:.3f} (t={iv2[6]['t_pi']:.2f}; esperado > 0), F={g['F_robusto']:.2f}; forma reducida t_AR(0)={iv2[6]['t_rf']:.2f} (signo esperado positivo); n={int(g['n'])}; p_perm={iv2[2]['p_perm']:.3f}; AR acotado={bool(g['ar_acotado'])}", iv2[6])
    else:
        ev_nan = {"f_ok": False, "ar_excluye_0": False, "pretendencias_ok": False, "perm_instrumento_ok": False, "cumple_c3": False, "c3_laxo": False}
        h7 = hip_fila("H8-7", "El empuje migratorio aumenta el alquiler real", "alquiler", 1.0, np.nan, (np.nan, np.nan), ev_nan,
                      f"IV2 fallido: {iv2_fallo}", estado_iv="fallido")
    hips = [h5, h6, h7]
    ph = holm({h["id"]: (h["ar_p"] if np.isfinite(h["ar_p"]) else 1.0) for h in hips})   # p AR unilateral con signo a priori de pi (J3)
    for h in hips:
        h["p_holm"] = ph[h["id"]]
        h["rechaza_H0_alfa05"] = bool(h["p_holm"] < 0.05)
        h["capa"] = "C3" if (h["cumple_c3"] and h["rechaza_H0_alfa05"]) else "C4"
        if h["cumple_c3"] and not h["rechaza_H0_alfa05"]:
            h["capa"] = "C3 (identificacion valida; H0 no rechazada)"
        if h["rechaza_H0_alfa05"] and h["cumple_c3"]:
            h["lectura"] = "respaldada tras Holm bajo C3 (efecto causal condicionado a la validez del instrumento)"
        elif h["rechaza_H0_alfa05"]:
            h["lectura"] = "p ajustado < 0,05 pero NO cumple los requisitos de C3: asociacion C4, sin lectura causal"
        else:
            h["lectura"] = "no respaldada tras Holm" + (" (identificacion C3 valida)" if h["cumple_c3"] else " (instrumento no supera C3)")
        h["metodo_ajuste"] = "Holm"
    hdf = pd.DataFrame(hips)
    hdf = hdf.rename(columns={"estimacion": "beta_descriptivo"})
    hdf["nota_beta"] = "beta = cociente de dos estimaciones (forma reducida / primera etapa); descriptivo, NO es evidencia a favor o en contra: la evidencia es el signo y el t de la forma reducida y el p AR con signo a priori"
    hdf.to_csv(out / "hipotesis_m5.csv", index=False)
    # p ajustado de las filas agregadas confirmatorias en coeficientes
    ids_filas = {"H8-5": "M5_IV1_compra_euribor_ln_p_tasado_real_h4-8", "H8-6": "M5_IV1_alquiler_euribor_ln_ipc_alquiler_real_h4-8",
                 "H8-7": "M5_IV2_alquiler_h1-2"}
    for f in filas_coef:
        for hid, mid in ids_filas.items():
            if f["modelo_id"] == mid:
                f["p_ajustado"] = ph[hid]
                f["metodo_ajuste"] = "Holm"
    # BH para el resto de filas IV1 agregadas (exploratorias)
    expl = {f["modelo_id"]: f["p_ar_bilateral"] for f in filas_coef
            if f["familia_modelo"] in ("lp_iv_agregado",) and f["modelo_id"] not in ids_filas.values()}
    pb = bh(expl)
    for f in filas_coef:
        if f["modelo_id"] in pb:
            f["p_ajustado"], f["metodo_ajuste"] = pb[f["modelo_id"]], "BH"
    # J21: todo p exploratorio restante (por horizonte, pretendencias, IV3 sin ajustar) con BH (q = 0,10) en una segunda familia
    resto = {f["modelo_id"]: f["p_ar_bilateral"] for f in filas_coef
             if not (isinstance(f["p_ajustado"], float) and np.isfinite(f["p_ajustado"])) and np.isfinite(f["p_ar_bilateral"])}
    pb2 = bh(resto)
    for f in filas_coef:
        if f["modelo_id"] in pb2:
            f["p_ajustado"], f["metodo_ajuste"] = pb2[f["modelo_id"]], "BH"

    # ===================== atribucion
    for key, (mercado, endog, col) in {"M5_IV1_compra_euribor_ln_p_tasado_real": ("compra", "euribor", "ln_p_tasado_real"),
                                       "M5_IV1_alquiler_euribor_ln_ipc_alquiler_real": ("alquiler", "euribor", "ln_alq")}.items():
        por_h, ag95, ag90, ag68, pl, ev, m_, e_, c_, etapa = iv1[key]
        ycol = "ln_p_tasado_real" if mercado == "compra" else "ln_ipc_alquiler_real"
        capa = "C3" if ev["cumple_c3"] else "C4"
        for p in PERIODOS:
            m = nac["periodo_h8"] == p
            dx = float(np.nansum(nac.loc[m, "euribor_1y"].diff().values)) if m.any() else np.nan
            dy = float(100 * nac[ycol].diff()[m].sum(skipna=True))
            contrib = ag95["beta"] * dx
            lo68 = sorted([ag68["ar_lo"] * dx, ag68["ar_hi"] * dx]) if (ag68["ar_acotado"] and np.isfinite(ag68["ar_lo"])) else [np.nan, np.nan]
            lo90 = sorted([ag90["ar_lo"] * dx, ag90["ar_hi"] * dx]) if (ag90["ar_acotado"] and np.isfinite(ag90["ar_lo"])) else [np.nan, np.nan]
            vs, vm = voto_s9(ag95["F_robusto"], ag68["ar_acotado"])
            filas_atr.append({"metodo": "lpiv", "mercado": mercado, "ambito": "nacional", "periodo": p, "factor": "credito_tipos",
                              "contribucion_pp": contrib, "pct_total": pct_total(contrib, dy), "b68_lo": lo68[0], "b68_hi": lo68[1],
                              "b90_lo": lo90[0], "b90_hi": lo90[1], "capa": capa,
                              "variante": "IV1_euribor_jk_h4-8", "principal": "si", "vota_s9": vs, "motivo_vota_s9": vm,
                              "notas": (f"IV1 JK; beta(h=4-8)={ag95['beta']:.3f} pp log por pp de Euribor x variacion acumulada del Euribor 1a en el periodo "
                                        f"({dx:.2f} pp); total observado={dy:.2f} pp; supone el mismo multiplicador para toda la variacion del tipo (no solo la "
                                        f"parte instrumentada); bandas = intervalo AR 68/90 x variacion (vacias si AR no acotado); "
                                        f"{'C3: ' if capa == 'C3' else 'C4: '}asociacion, sin lectura causal salvo C3")})
    if iv2 is not None:
        g68, g90, g95 = iv2[1][0.68], iv2[1][0.90], iv2[1][0.95]
        capa = "C3" if iv2[3]["cumple_c3"] else "C4"
        A_ = a_es.reindex(range(2002, 2025))
        dA = (A_.diff() / 1e5)
        yq_ = anual_media(nac, "ln_ipc_alquiler_real") * 100
        for p in PERIODOS:
            an = [a_ for a_ in per_a[p] if 2003 <= a_ <= 2024]
            dx = float(dA.reindex(an).sum()) if an else np.nan
            dy = float(yq_.diff().reindex(an).sum()) if an else np.nan
            if not an:
                continue
            contrib = g95["beta"] * dx
            l68 = sorted([g68["ar_lo"] * dx, g68["ar_hi"] * dx]) if (g68["ar_acotado"] and np.isfinite(g68["ar_lo"])) else [np.nan, np.nan]
            l90 = sorted([g90["ar_lo"] * dx, g90["ar_hi"] * dx]) if (g90["ar_acotado"] and np.isfinite(g90["ar_lo"])) else [np.nan, np.nan]
            vs, vm = voto_s9(g95["F_robusto"], g68["ar_acotado"])
            filas_atr.append({"metodo": "lpiv", "mercado": "alquiler", "ambito": "nacional", "periodo": p, "factor": "demografia",
                              "contribucion_pp": contrib, "pct_total": pct_total(contrib, dy), "b68_lo": l68[0], "b68_hi": l68[1],
                              "b90_lo": l90[0], "b90_hi": l90[1], "capa": capa,
                              "variante": "IV2_shiftshare_h1-2", "principal": "si", "vota_s9": vs, "motivo_vota_s9": vm,
                              "notas": (f"IV2 shift-share anual; beta(h=1-2)={g95['beta']:.3f} pp log por 100.000 llegadas x variacion acumulada de llegadas "
                                        f"({dx:.2f} x100.000; anios {an[0]}-{an[-1]}); variacion total del alquiler real en esos anios={dy:.2f} pp; "
                                        f"bandas AR 68/90 (vacias si no acotado); llegadas = total Eurostat (incluye espanoles que retornan)")})
    if iv3:
        Pm = iv3["P3"].reset_index().dropna(subset=["x", "z"])  # muestra de estimación (sin CCAA sin cuota del año base: errata B-3)
        dlnE = Pm.pivot(index="t", columns="ent", values="x").mean(axis=1)
        for mercado, col in (("compra", "l_precio"), ("alquiler", "l_alq")):
            r = iv3["res"][(mercado, col, "h1-2")]
            capa = "C3" if r["ev"]["cumple_c3"] else "C4"
            for p in PERIODOS:
                an = [a_ for a_ in per_a[p] if a_ >= 2009]
                if not an:
                    continue
                dx = float(dlnE.reindex(an).sum())
                contrib = r["beta"] * dx
                l68 = sorted([r["ar_lo68"] * dx, r["ar_hi68"] * dx]) if (r["ar_acotado68"] and np.isfinite(r["ar_lo68"])) else [np.nan, np.nan]
                l90 = sorted([r["ar_lo90"] * dx, r["ar_hi90"] * dx]) if (r["ar_acotado90"] and np.isfinite(r["ar_lo90"])) else [np.nan, np.nan]
                yy = Pm.pivot(index="t", columns="ent", values=col).mean(axis=1).diff().reindex(an).sum()
                vs, vm = voto_s9(r["F_robusto"], r["ar_acotado68"], "ccaa_panel")
                filas_atr.append({"metodo": "lpiv", "mercado": mercado, "ambito": "ccaa_panel", "periodo": p, "factor": "empleo_renta",
                                  "contribucion_pp": contrib, "pct_total": pct_total(contrib, float(yy)), "b68_lo": l68[0], "b68_hi": l68[1],
                                  "b90_lo": l90[0], "b90_hi": l90[1], "capa": capa,
                                  "variante": "IV3_bartik_h1-2", "principal": "si", "vota_s9": vs, "motivo_vota_s9": vm,
                                  "notas": (f"IV3 Bartik 2008, panel {iv3['n']} CCAA (sin Navarra ni La Rioja: sin cuota en 2008), efecto relativo entre CCAA (efectos de anio absorben lo nacional); "
                                            f"beta(h=1-2)={r['beta']:.3f} x variacion media acumulada del empleo ({dx:.2f} pp, anios {an[0]}-{an[-1]}); "
                                            f"variacion media observada={yy:.2f} pp; NO es la contribucion nacional del empleo; bandas AR 68/90")})
    atr = pd.DataFrame(filas_atr, columns=COLS_ATR)
    atr.to_csv(out / "atribucion.csv", index=False)
    coef = pd.DataFrame(filas_coef, columns=COLS_COEF)
    coef.to_csv(out / "coeficientes.csv", index=False)
    reg.flush()

    # ===================== resultado.json
    iv1_json = {}
    for mid, (por_h, ag95, ag90, ag68, pl, ev, m_, e_, c_, _etapa) in iv1.items():
        iv1_json[mid] = {"beta_h4_8": float(ag95["beta"]), "ar95": [float(ag95["ar_lo"]), float(ag95["ar_hi"])], "ar_acotado": bool(ag95["ar_acotado"]),
                         "F_efectivo": float(ag95["F_robusto"]), "p_ar_menor": float(ag95["ar_p_menor"]), "p_ar_dos": float(ag95["ar_p_dos"]),
                         "pretendencias_ar_p": {int(h): float(p) for h, p in zip(por_h.loc[por_h.h < 0, "h"], por_h.loc[por_h.h < 0, "ar_p_dos"])},
                         "perm_instrumento_p_perm": float(pl["p_perm"]), "n": int(ag95["n"]), **{k: bool(v) for k, v in ev.items()}}
    iv3_json = {}
    if iv3:
        for (mercado, col, lab), r in iv3["res"].items():
            if lab in ("h1-2", "h0", "h1", "h2") and "ev" in r:
                iv3_json[f"{col}_{lab}"] = {"beta": float(r["beta"]), "ar95": [float(r["ar_lo95"]), float(r["ar_hi95"])], "ar_acotado": bool(r["ar_acotado95"]),
                                            "F_efectivo": float(r["F_robusto"]), "p_ar_dos": float(r["ar_p_dos"]), "n": int(r["n"]),
                                            **{k: bool(v) for k, v in r["ev"].items()}}
        iv3_json["rotemberg_top"] = iv3["rot"].head(4).to_dict("records")
    h_json = {h["id"]: {"beta_descriptivo": None if not np.isfinite(h["estimacion"]) else float(h["estimacion"]), "signo_forma_reducida": int(h["signo_forma_reducida"]),
                        "t_forma_reducida": None if not np.isfinite(h["t_forma_reducida"]) else float(h["t_forma_reducida"]),
                        "pi": None if not np.isfinite(h["pi_primera_etapa"]) else float(h["pi_primera_etapa"]),
                        "t_pi": None if not np.isfinite(h["t_primera_etapa"]) else float(h["t_primera_etapa"]),
                        "F_efectivo": None if not np.isfinite(h["F_efectivo"]) else float(h["F_efectivo"]),
                        "ar_p_unilateral_signo_apriori": float(h["ar_p"]),
                        "p_holm": float(h["p_holm"]), "capa": h["capa"], "cumple_c3": bool(h["cumple_c3"]), "lectura": h["lectura"]} for h in hips}
    res = {"rama": "M5", "pregunta": "Efecto de un shock monetario del BCE (IV1), del empuje migratorio (IV2) y del empleo regional (IV3) sobre el precio real de compra y el alquiler real",
           "capa": "C4" if not any(h["cumple_c3"] for h in hips) else "C3 solo donde cumple_c3 (ver estimacion)",
           "datos": "data/processed/v8/nacional_q_v8.csv, panel_ccaa_q_v8.csv; data/raw/v8/eurostat_migr (migr_imm1ctz, lfst_r_lfe2en2, descargados con src/v8/fetch_m5.py); data/raw/v8/eurostat_migr_pop1ctz_es.csv",
           "N": {"IV1_compra": int(base5[1]["n"]), "IV1_alquiler": int(base6[1]["n"]), "IV2": n2,
                 "IV3": int(iv3["res"][("alquiler", "l_alq", "h1-2")]["n"]) if iv3 else 0},
           "metodo": "LP-IV acumulado (2SLS por horizonte, F efectivo Olea-Pflueger, intervalos Anderson-Rubin HAC), agregado h=4-8 (IV1) y h=1-2 anual (IV2, IV3); "
                     "panel Driscoll-Kraay con AR exacto (IV3); Holm en {H8-5, H8-6, H8-7}; BH (q=0,10) en lo exploratorio",
           "estimacion": {"hipotesis": h_json, "IV1": iv1_json, "IV2": ({"estado": "ok", "beta_h1_2": float(iv2[1][0.95]["beta"]),
                                                                     "ar95": [float(iv2[1][0.95]["ar_lo"]), float(iv2[1][0.95]["ar_hi"])],
                                                                     "F_efectivo": float(iv2[1][0.95]["F_robusto"]),
                                                                     "perm_instrumento_p_perm": float(iv2[2]["p_perm"]), "n_origenes": int(len(iv2[4])),
                                                                     "n_destinos": len(iv2[5]), **{k: bool(v) for k, v in iv2[3].items()}}
                                                                    if iv2 else {"estado": "fallido", "motivo": iv2_fallo}),
                          "IV2b_sin_normalizar": ({"beta_h1_2": float(iv2b[1][0.95]["beta"]), "F_efectivo": float(iv2b[1][0.95]["F_robusto"]),
                                                   "p_ar_mayor": float(iv2b[1][0.95]["ar_p_mayor"]), "ar_acotado": bool(iv2b[1][0.95]["ar_acotado"]),
                                                   "perm_instrumento_p_perm": float(iv2b[2]["p_perm"]), **{k: bool(v) for k, v in iv2b[3].items()}} if iv2b else None),
                          "IV3": iv3_json if iv3 else {"estado": "fallido", "motivo": iv3_fallo}},
           "ic95": {h["id"]: [None if not np.isfinite(h["ar_lo"]) else float(h["ar_lo"]), None if not np.isfinite(h["ar_hi"]) else float(h["ar_hi"])] for h in hips},
           "ic95_nota": "Intervalo Anderson-Rubin al 95 %; null = extremo no acotado (la rejilla llega al borde: instrumento debil, intervalo no informativo)",
           "p_ajustado": {h["id"]: float(h["p_holm"]) for h in hips},
           "nivel_evidencia": "C3 solo en las filas con cumple_c3=True; el resto C4 (asociacion, sin lenguaje causal). " + AVISO,
           "diagnosticos": {"primera_etapa_IV1": {"compra": {k: fs5[k] for k in ("pi", "t_pi", "F", "t_rf")}, "alquiler": {k: fs6[k] for k in ("pi", "t_pi", "F", "t_rf")},
                                                  "nota": "misma regresion agregada h=4-8 que el F y el AR; signo a priori pi > 0 (shock contractivo sube el Euribor); el p AR unilateral usa ese signo, no el estimado"}, "F_efectivo_agregado": {k: v["F_efectivo"] for k, v in iv1_json.items()}, "iv2_fallo": iv2_fallo, "iv3_fallo": iv3_fallo,
                            "tamano_AR_panel": "AR de panel calculado con 3 ajustes DK exactos (contrastado con lp_panel en beta0=0 en tests). Monte Carlo minimo propio (N=17, T=14, 150 reps, beta=0, instrumento fuerte, factor comun temporal): tamano del AR al 5 % = 0,113 y cobertura del AR95 = 0,887: Driscoll-Kraay con T pequeno es anticonservador; los p de IV3 se leen con ese sesgo"},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "No aplica: modulo de identificacion (efectos), no de prediccion; no se compara con AR(4) ni ECM v1."},
           "notas": ("Fallido = no rechazada en Holm. Muestras: IV1 precio 1999Q2-2025Q3 menos horizontes, alquiler desde 2002Q3; IV2 anual 2003-2024; IV3 " + (f"{iv3['n']} CCAA (sin Navarra ni La Rioja: sin cuota del año base 2008)" if iv3 else "no estimado") + " 2009-2025. "
                     "Cuotas IV2 = stock de residentes por ciudadania a 1-1-2002 (no flujo). Eurostat LFS NUTS2: posibles rupturas de serie no tratadas. "
                     "IV2b (instrumento sin normalizar): anadida tras construir el instrumento, exploratoria, fuera de Holm. "
                     "Permutacion del instrumento (antes «placebo»): contraste de significacion de la forma reducida, no prueba independiente. "
                     f"Modo rapido={a.rapido}.")}
    (out / "tiempos.json").write_text(json.dumps({"segundos": round(time.time() - t_ini, 1)}))
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=lambda o: None if (isinstance(o, float) and not np.isfinite(o)) else str(o)))

    # ===================== resumen.md
    L = ["# M5: instrumentos externos (IV1 JK, IV2 migratorio, IV3 Bartik)", "",
         "Capa: C3 solo donde se cumplen los cuatro requisitos de §6; si no, C4 (asociacion, sin lenguaje causal).", "",
         "## Hipotesis (Holm, familia {H8-5, H8-6, H8-7})", "",
         "p AR unilateral con el signo A PRIORI de la primera etapa (pi > 0); beta (cociente de dos estimaciones) no se lee como evidencia.", "",
         "| id | pi (t) | F | forma reducida: signo (t) | AR p unilateral | p Holm | F>=10 | AR excl. 0 | pretend. | permutacion instr. | capa |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for h in hips:
        L.append(f"| {h['id']} | {h['pi_primera_etapa']:.3f} ({h['t_primera_etapa']:.2f}) | {h['F_efectivo']:.2f} | "
                 f"{'+' if h['signo_forma_reducida'] > 0 else '-'} ({h['t_forma_reducida']:.2f}; esperado {'+' if h['signo_esperado_forma_reducida'] > 0 else '-'}) | "
                 f"{h['ar_p']:.3f} | {h['p_holm']:.3f} | {'si' if h['f_ok'] else 'no'} | "
                 f"{'si' if h['ar_excluye_0'] else 'no'} | {'si' if h['pretendencias_ok'] else 'no'} | {'si' if h['perm_instrumento_ok'] else 'no'} | {h['capa']} |"
                 if np.isfinite(h["estimacion"]) else f"| {h['id']} | n/d | n/d | n/d | 1,000 | {h['p_holm']:.3f} | - | - | - | - | C4 (fallido) |")
    L += ["", "Detalle por hipotesis: " + " / ".join(f"{h['id']}: {h['extra']}; {h['lectura']}" for h in hips), ""]
    if iv2 is None:
        L += [f"IV2 fallido: {iv2_fallo}", ""]
    if iv3:
        r = iv3["res"][("alquiler", "l_alq", "h1-2")]
        r2 = iv3["res"][("compra", "l_precio", "h1-2")]
        L += [f"## IV3 (Bartik, panel {iv3['n']} CCAA sin Navarra ni La Rioja por falta de cuota en 2008, exploratorio; BH)", "",
              f"- Alquiler h=1-2: beta={r['beta']:.3f}, AR95=[{r['ar_lo95']:.2f}, {r['ar_hi95']:.2f}], F={r['F_robusto']:.1f}, p AR={r['ar_p_dos']:.3f}, cumple C3={r['ev']['cumple_c3']}.",
              f"- Precio h=1-2: beta={r2['beta']:.3f}, AR95=[{r2['ar_lo95']:.2f}, {r2['ar_hi95']:.2f}], F={r2['F_robusto']:.1f}, p AR={r2['ar_p_dos']:.3f}, cumple C3={r2['ev']['cumple_c3']}.",
              "- Rotemberg (pesos principales): " + "; ".join(f"{x['sector']} {x['alpha']:.2f}" for x in iv3["rot"].head(4).to_dict("records")) + ".", ""]
    if iv2b:
        gb = iv2b[1][0.95]
        L += ["## IV2b (instrumento sin normalizar; exploratoria, ANADIDA TRAS CONSTRUIR EL INSTRUMENTO)", "",
              f"- Alquiler h=1-2: beta={gb['beta']:.3f}, F={gb['F_robusto']:.1f}, p AR unilateral (signo a priori)={gb['ar_p_mayor']:.3f}, AR acotado={bool(gb['ar_acotado'])}, cumple C3={iv2b[3]['cumple_c3']}. Fuera de Holm.", ""]
    L += ["## Atribucion lpiv y regla de §9", "", "Las filas `lpiv` de atribucion.csv son C4 informativas: `vota_s9` = no cuando F < 10 y el AR 68 % no esta acotado (se abstiene) y siempre en IV3 (efecto relativo entre CCAA). `pct_total` queda vacio si |variacion observada| < 1 pp.", ""]
    L += ["## Limites", "", "- Instrumento valido solo si es exogeno (no verificable): los shocks JK pueden contener informacion del BCE sobre la economia (JK los depuran con signos).",
          "- IV2: shocks comunes a la UE (ciclo) pueden afectar a Espana; llegadas = total Eurostat; cuotas = stock 2002; frecuencia anual (n pequeno).",
          "- IV3: efectos relativos entre CCAA, no nacionales; posibles rupturas de serie en la EPA/LFS.",
          "- Atribucion lpiv: multiplicador constante extrapolado a toda la variacion de la endogena; bandas AR.", "- Fuera de muestra: no aplica.",
          "- La permutacion del instrumento (antes «placebo») contrasta la significacion de la forma reducida; no es una prueba independiente de validez del instrumento. Las pretendencias tampoco lo son (baja potencia).", ""]
    (out / "resumen.md").write_text("\n".join(L) + "\n")
    print(f"M5 listo en {time.time() - t_ini:.0f} s -> {out}")


if __name__ == "__main__":
    main()
