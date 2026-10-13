"""V8-F4 M6/M7: preparacion comun de datos (ecuacion del crecimiento nacional, una variable por familia de factores).

Convenciones (docs/v8/hipotesis.md §3-§4; diccionario F1):
- Dependiente: precio real de compra (principal: valor tasado; alternativa: IPV) o alquiler real (IPC de alquiler), deflactado con el IPC
  general (principal) o el deflactor del PIB, en tasa log x 100: interanual (d4) o trimestral (d1).
- Cada familia tiene una lista ORDENADA de variables candidatas (la primera es la principal). Las variables en logaritmo entran en tasa log x 100
  con la misma transformacion que la dependiente; las variables en nivel (tipo real, shock monetario) entran en nivel.
- Una variable se considera INTERPOLADA en una ventana si mas del 60 % de sus observaciones transformadas tienen algun extremo marcado como
  interpolado (columnas *_interp del diccionario; la poblacion semestral queda en ~50 % en tasa interanual y ~100 % en tasa trimestral). Las interpoladas solo entran en robustez (M7, como variable focal alternativa).
- Una familia entra en un periodo solo si alguna candidata cubre al menos el 70 % de los trimestres en que existe la dependiente en la ventana.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
SEED = 20261010
DATOS = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"

PERIODOS = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"),
            "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", "2026Q2"), "completo": ("1995Q1", "2026Q2")}
FAM_ORDEN = ["demografia", "empleo_renta", "credito_tipos", "oferta", "demanda_externa", "turismo", "factor_europeo"]
UMBRAL_COBERTURA = 0.70
UMBRAL_INTERP = 0.60   # >60 % de observaciones transformadas con algun extremo interpolado (la poblacion semestral queda en ~50 % interanual)
GL_MIN = 5            # grados de libertad residuales minimos de cualquier ajuste
EPA_VARS = {"ocupados", "hogares_epa"}


@dataclass(frozen=True)
class Cand:
    clave: str
    familia: str
    tipo: str            # 'ln' (tasa log x 100) | 'nivel'
    desde: str           # primer trimestre con dato del nivel (documentacion)
    descripcion: str
    interp: str | None = None


CANDIDATAS = [
    Cand("pob_total", "demografia", "ln", "1995Q1", "poblacion total (INE; interpolada entre fechas semestrales)", "pob_total_interp"),
    Cand("pob_extranj_ine", "demografia", "ln", "2002Q1", "poblacion extranjera (INE)", "pob_extranj_ine_interp"),
    Cand("hogares_epa", "demografia", "ln", "2002Q1", "hogares (EPA)", None),
    Cand("pib_vol", "empleo_renta", "ln", "1995Q1", "PIB en volumen (indice)", None),
    Cand("rdb_real", "empleo_renta", "ln", "1999Q1", "renta disponible bruta real", None),
    Cand("ocupados", "empleo_renta", "ln", "2002Q1", "ocupados (EPA)", None),
    Cand("salario_real", "empleo_renta", "ln", "2000Q1", "salario real", None),
    Cand("tipo_hip_real", "credito_tipos", "nivel", "1996Q1", "tipo hipotecario real (BdE, nivel, pp)", None),
    Cand("credito_stock_real", "credito_tipos", "ln", "1997Q3", "stock de credito (BdE) real", None),
    Cand("credito_nuevo_real", "credito_tipos", "ln", "2003Q1", "credito nuevo real", None),
    Cand("terminadas", "oferta", "ln", "1995Q1", "viviendas terminadas (anual/4 antes de 2008)", "terminadas_interp"),
    Cand("visados", "oferta", "ln", "1995Q1", "viviendas iniciadas, visados (anual/4 antes de 2008)", "visados_interp"),
    Cand("costes_constr", "oferta", "ln", "1995Q1", "costes de construccion reales", None),
    Cand("tx_extranj", "demanda_externa", "ln", "2007Q1", "compraventas por extranjeros residentes (MIVAU)", None),
    Cand("cuota_extranj", "demanda_externa", "ln", "2007Q1", "ln(compras de extranjeros / compraventas totales)", None),
    Cand("turistas", "turismo", "ln", "2015Q4", "turistas internacionales (FRONTUR)", None),
    Cand("vut_viviendas", "turismo", "ln", "2020Q3", "viviendas de uso turistico (desde 2020)", "vut_viviendas_interp"),
    Cand("bis_hpi_xm_real", "factor_europeo", "ln", "2000Q1", "precio real de la vivienda, zona euro (BIS)", None),
    Cand("hpi_ea19", "factor_europeo", "ln", "2005Q1", "indice de precios de la vivienda EA19 (Eurostat, nominal)", None),
    Cand("jk_mp", "factor_europeo", "nivel", "1999Q1", "shock monetario BCE (Jarocinski-Karadi), suma trimestral", None),
]
POR_FAMILIA = {f: [c for c in CANDIDATAS if c.familia == f] for f in FAM_ORDEN}
POR_CLAVE = {c.clave: c for c in CANDIDATAS}
NOMINAL = {("compra", "tasado"): "ln_p_tasado", ("compra", "ipv"): "ln_ipv", ("alquiler", "ipc_alquiler"): "ln_ipc_alquiler"}
MEDIDAS = {"compra": ["tasado", "ipv"], "alquiler": ["ipc_alquiler"]}


def cargar() -> pd.DataFrame:
    d = pd.read_csv(DATOS).set_index("trimestre")
    for c in d.columns:
        if c.endswith("_interp"):
            d[c] = d[c].astype(str).str.lower().eq("true")
    # 2026T1 y 2026T2 de tx_extranj repiten el mismo valor en el origen (diccionario): se anula 2026T2 como dato no valido
    d.loc["2026Q2", "ln_tx_extranj"] = np.nan
    # J1/J17 (revision F4): la ficticia EPA 2021 es un salto de NIVEL en las variables EPA; en tasas es un IMPULSO.
    # Interanual (d4): 1 en 2021T1-2021T4; trimestral (d1): 1 solo en 2021T1 (columna epa2021_q).
    d = d.copy()
    d["epa2021"] = d.index.isin(["2021Q1", "2021Q2", "2021Q3", "2021Q4"]).astype(int)
    d["epa2021_q"] = (d.index == "2021Q1").astype(int)
    return d


def col_epa(transf: str) -> str:
    """Nombre de la columna de la ficticia EPA 2021 segun la transformacion (impulso de 4 trimestres en interanual; de 1 en trimestral)."""
    return "epa2021" if transf == "interanual" else "epa2021_q"


def transformar(s: pd.Series, tipo: str, transf: str) -> pd.Series:
    k = 4 if transf == "interanual" else 1
    if tipo == "ln":
        return 100.0 * s.diff(k)
    return s


def preparar(d: pd.DataFrame, mercado: str, medida: str, deflactor: str, transf: str):
    """Devuelve (dep, X, interp, niveles). X: todas las candidatas transformadas; interp: marcas booleanas; niveles: series en
    nivel log para el ECM v1 aproximado."""
    ln_def = d["ln_ipc_general" if deflactor == "ipc" else "ln_deflactor_pib"]
    lnp = d[NOMINAL[(mercado, medida)]] - ln_def
    dep = transformar(lnp, "ln", transf).rename("dep")
    base = {
        "pob_total": d["ln_pob_total"], "pob_extranj_ine": d["ln_pob_extranj_ine"], "hogares_epa": d["ln_hogares_epa"],
        "pib_vol": d["ln_pib_vol_idx"], "rdb_real": d["ln_rdb"] - ln_def, "ocupados": d["ln_ocupados"],
        "salario_real": d["ln_salario"] - ln_def,
        "tipo_hip_real": d["tipo_hip_bde"] - 100.0 * ln_def.diff(4),
        "credito_stock_real": d["ln_credito_stock_bde"] - ln_def, "credito_nuevo_real": d["ln_credito_nuevo"] - ln_def,
        "terminadas": d["ln_terminadas"], "visados": d["ln_visados"], "costes_constr": d["ln_costes_constr"] - ln_def,
        "tx_extranj": d["ln_tx_extranj"], "cuota_extranj": d["ln_tx_extranj"] - d["ln_compraventas_ine"],
        "turistas": d["ln_turistas"], "vut_viviendas": d["ln_vut_viviendas"],
        "bis_hpi_xm_real": d["ln_bis_hpi_xm_real"], "hpi_ea19": d["ln_hpi_ea19"],
        "jk_mp": d["jk_mp"].rolling(4).sum() if transf == "interanual" else d["jk_mp"],
    }
    X = pd.DataFrame({c.clave: transformar(base[c.clave], c.tipo, transf) for c in CANDIDATAS})
    k = 4 if transf == "interanual" else 1
    interp = pd.DataFrame({c.clave: ((d[c.interp] | d[c.interp].shift(k, fill_value=False)) if (c.interp and c.tipo == "ln")
                                     else (d[c.interp] if c.interp else pd.Series(False, index=d.index))) for c in CANDIDATAS})
    niveles = pd.DataFrame({"y": lnp * 1.0, "ocupados": d["ln_ocupados"], "costes": d["ln_costes_constr"] - ln_def,
                            "rdb": d["ln_rdb"] - ln_def})
    return dep, X, interp, niveles


def ventana(idx, periodo: str) -> list[str]:
    a, b = PERIODOS[periodo]
    return [t for t in idx if a <= t <= b]


def cobertura(dep: pd.Series, x: pd.Series, win) -> float:
    w = dep.loc[win].notna()
    if w.sum() == 0:
        return 0.0
    return float((x.loc[win].notna() & w).sum() / w.sum())


def es_interpolada(x: pd.Series, interp: pd.Series, win) -> bool:
    ok = x.loc[win].notna()
    if ok.sum() == 0:
        return False
    return bool(interp.loc[win][ok].mean() > UMBRAL_INTERP)


def candidatas_viables(fam, dep, X, interp, win, permitir_interp=False, umbral=UMBRAL_COBERTURA):
    """Candidatas de la familia con cobertura suficiente en la ventana, en orden de prioridad. Devuelve lista de (clave, interpolada)."""
    out = []
    for c in POR_FAMILIA[fam]:
        if cobertura(dep, X[c.clave], win) < umbral:
            continue
        ip = es_interpolada(X[c.clave], interp[c.clave], win)
        if ip and not permitir_interp:
            continue
        out.append((c.clave, ip))
    return out


def elegir_principales(dep, X, interp, win):
    """Una variable por familia (la primera viable no interpolada). Devuelve (dict familia->clave, dict familia->motivo_exclusion)."""
    sel, exc = {}, {}
    for f in FAM_ORDEN:
        v = candidatas_viables(f, dep, X, interp, win)
        if v:
            sel[f] = v[0][0]
        else:
            alt = candidatas_viables(f, dep, X, interp, win, permitir_interp=True)
            exc[f] = ("solo candidatas interpoladas (>50 % interpoladas; solo robustez)" if alt
                      else "cobertura < 70 % de los trimestres del periodo en todas las candidatas")
    return sel, exc


def limitar_por_gl(dep, X, sel: dict, win, n_dummies=0):
    """Si la muestra comun no permite todas las familias con GL >= GL_MIN, se retiran las ULTIMAS en el orden de prioridad del
    pre-registro (§1). Devuelve (sel_final, muestra DataFrame, motivos)."""
    sel = dict(sel)
    motivos = {}
    while True:
        cols = list(sel.values())
        D = pd.concat([dep, X[cols]], axis=1).loc[win].dropna() if cols else pd.DataFrame()
        n = len(D)
        if not cols or n - (len(cols) + 1 + n_dummies) >= GL_MIN:
            return sel, D, motivos
        f = [k for k in FAM_ORDEN if k in sel][-1]
        motivos[f] = f"muestra insuficiente (n={n}, k={len(cols)}): GL < {GL_MIN}; se retira por el orden de prioridad del pre-registro"
        sel.pop(f)


def dummies_relevantes(D: pd.DataFrame, d: pd.DataFrame, vars_epa: bool, k: int, transf: str = "interanual"):
    """Ficticias COVID / EPA2021 que varian en la muestra y dejan GL >= GL_MIN."""
    out = []
    n = len(D)
    for c, aplica in (("covid", True), (col_epa(transf), vars_epa)):
        if aplica and d.loc[D.index, c].std() > 0 and n - (k + 1 + len(out) + 1) >= GL_MIN:
            out.append(c)
    return out


def ewc_ols(y, X, nivel=0.95):
    """OLS con constante (X ya incluye la constante en la columna 0 de A) y EE EWC (Lazarus et al. 2018), identica a lp._ols_ewc.
    Devuelve dict beta, se, p, q, resid."""
    from scipy import stats
    y = np.asarray(y, float)
    A = np.asarray(X, float)
    n = len(y)
    XtXi = np.linalg.pinv(A.T @ A)
    b = XtXi @ A.T @ y
    u = y - A @ b
    G = A * u[:, None]
    q = max(int(np.floor(0.4 * n ** (2 / 3))), 2)
    t = (np.arange(1, n + 1) - 0.5) / n
    Lam = np.array([np.sqrt(2) * np.cos(np.pi * j * t) @ G / np.sqrt(n) for j in range(1, q + 1)])
    S = Lam.T @ Lam / q
    V = n * XtXi @ S @ XtXi
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    with np.errstate(divide="ignore", invalid="ignore"):
        tt = b / se
    p = 2 * stats.t.sf(np.abs(tt), q)
    return {"beta": b, "se": se, "t": tt, "p": p, "q": q, "resid": u, "n": n}


def bh(p, q=0.10):
    """Ajuste de Benjamini-Hochberg (valores p ajustados)."""
    from statsmodels.stats.multitest import multipletests
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    if ok.sum():
        out[ok] = multipletests(p[ok], method="fdr_bh")[1]
    return out
