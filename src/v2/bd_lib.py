"""Rama BD (descomposición por periodos con contrafactuales e intervalos) - biblioteca.

Modelos (EXPLORATORIOS; asociaciones, no causalidad):
  M1  Δ4 y_it = a_i + l_t + Σ_f Σ_P b_{f,P} x_{f,it} + (política: coef. global) + e_it
      (FE de provincia y de trimestre; coeficientes POR PERIODO como BA y BV). El componente común de
      todas las variables que se mueven igual en todas las provincias queda en l_t ("efectos de tiempo").
  M2  igual pero SIN efectos de trimestre: FE de provincia + dummies de trimestre del año + intercepto por
      periodo + Δ4 coste de uso NACIONAL con coeficiente GLOBAL (la serie es única: no hay variación
      transversal; identificación solo temporal, EE cluster no válidos -> se usa bootstrap por bloques de tiempo).
Identidad contable (ponderada por población): media_w(y)_t = Σ b·media_w(x)_t + media_w(y - Xb - e)_t + media_w(e)_t.
Contribución acumulada de un periodo P = 100 · (n_trim_P/4) · media_t∈P [ contribución trimestral ]  (pp de
ln; Σ_t Δ4 ≈ 4 × crecimiento acumulado, aproximación con efectos de borde).
Datos SOLO vía v2_common.load (= holdout.load_train). Sin red. SEED = 20261010. 1 hilo BLAS.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v2"))
import v2_common as vc  # noqa: E402
import bv_lib as bvl  # noqa: E402  (solo preparar_panel: precio real, exposición, cu_x_expo)

SEED = vc.SEED
OUT = ROOT / "output" / "v2" / "BD"
PERIODOS = {"P1": ("2008Q1", "2013Q4"), "P2": ("2014Q1", "2019Q4"), "P3": ("2020Q1", "2021Q4"),
            "P4": ("2022Q1", "2024Q2")}
PNAMES = list(PERIODOS)
Q_FIN_MUESTRA = "2024Q1"      # la población de 2024Q2 está anulada (fuga del sellado) -> muestra completa hasta 2024Q1
TOPE = ("2020Q4", "2022Q1")
CATALANAS = ("08", "17", "25", "43")

FAMILIAS = ["demografia", "empleo_renta", "credito_tipos_cu", "oferta", "politica"]
# (variable, familia, por_periodo)
SPEC_VARS = {
    "alquiler": [("d4_ln_pob_20_34", "demografia_20_34", True), ("d4_ln_pob_extranj", "demografia_extranj", True),
                 ("d4_ln_ocupados", "empleo_renta", True), ("d4_ln_hipotecas_importe", "credito_tipos_cu", True),
                 ("d4_ln_terminadas_libres0", "oferta", True), ("tope_cat", "politica", False)],
    "compra": [("d4_ln_pob_20_34", "demografia_20_34", True), ("d4_ln_pob_extranj", "demografia_extranj", True),
               ("d4_ln_ocupados", "empleo_renta", True), ("d4_ln_hipotecas_importe", "credito_tipos_cu", True),
               ("cu_x_expo", "credito_tipos_cu", True), ("d4_ln_terminadas_libres0", "oferta", True)],
}
SPEC_VARS["alquiler_turismo"] = [("d4_ln_pob_20_34", "demografia_20_34", False), ("d4_ln_pob_extranj", "demografia_extranj", False),
                                 ("d4_ln_ocupados", "empleo_renta", False),
                                 ("d4_ln_vut_viviendas", "turismo", False)]
YVAR = {"alquiler": "d4_ln_ipc_alquiler", "compra": "d4_ln_p_real", "alquiler_turismo": "d4_ln_ipc_alquiler"}
NIVEL_LEVEL = {"alquiler": "ln_ipc_alquiler", "compra": "ln_p_real", "alquiler_turismo": "ln_ipc_alquiler"}


# ------------------------------------------------------------------ datos
def cargar_panel() -> pd.DataFrame:
    pan, nac = vc.load("panel_prov_q"), vc.load("nacional_q_v2")
    d = bvl.preparar_panel(pan, nac)
    d["cod_prov"] = d["cod_prov"].astype(str)
    d = d.replace([np.inf, -np.inf], np.nan).sort_values(["cod_prov", "trimestre"]).reset_index(drop=True)
    d["d4_ln_terminadas_libres0"] = d["d4_ln_terminadas_libres"].fillna(0.0)
    d["miss_oferta"] = d["d4_ln_terminadas_libres"].isna().astype(float)
    d["x_cu"] = d["coste_uso_aprox"] - d.groupby("cod_prov")["coste_uso_aprox"].shift(4)
    d["tope_cat"] = (d["cod_prov"].isin(CATALANAS) & d["trimestre"].between(*TOPE)).astype(float)
    d["pob_w"] = d.groupby("cod_prov")["pob_total"].ffill()
    return d


def cu_nacional(d: pd.DataFrame) -> pd.Series:
    s = d.groupby("trimestre")["coste_uso_aprox"].agg(["min", "max"])
    assert float((s["max"] - s["min"]).max()) < 1e-9, "coste_uso_aprox no es nacional"
    return s["min"]


def contrafactual_vars(d: pd.DataFrame) -> dict:
    """Devuelve {escenario: DataFrame con las variables modificadas} (a nivel de panel completo, antes de recortar).
    a: sin crecimiento de pob 20-34 ni extranjera desde 2014Q1 (Δ4 ln = 0).
    b: crédito (ln importe hipotecario provincial) y coste de uso congelados en su nivel de 2013Q4 desde 2014Q1.
    c: coste de uso = nivel de 2021Q4 desde 2022Q1 (durante P4)."""
    out = {}
    t = d["trimestre"]
    a = d.copy()
    for v in ("d4_ln_pob_20_34", "d4_ln_pob_extranj"):
        a.loc[t >= "2014Q1", v] = 0.0
    out["a_ambas_sin_variacion_desde_2014"] = a
    for nm, v in (("a1_solo_pob_20_34_sin_variacion", "d4_ln_pob_20_34"),
                  ("a2_solo_pob_extranj_sin_variacion", "d4_ln_pob_extranj")):
        a1 = d.copy()
        a1.loc[t >= "2014Q1", v] = 0.0
        out[nm] = a1
    a3 = d.copy()
    for v in ("d4_ln_pob_20_34", "d4_ln_pob_extranj"):
        a3.loc[t >= "2014Q1", v] = a3.loc[t >= "2014Q1", v].clip(upper=0.0)
    out["a3_ambas_sin_crecimiento_positivo_desde_2014"] = a3
    cu = cu_nacional(d)

    def cu_cf(q0, q1):
        s = cu.copy()
        s[s.index >= q1] = cu[q0]
        return s

    P = d.pivot(index="trimestre", columns="cod_prov", values="ln_hipotecas_importe")
    Pc = P.copy()
    Pc.loc[Pc.index >= "2014Q1"] = P.loc["2013Q4"].values
    d4c = (Pc - Pc.shift(4)).stack().rename("d4_hip_cf").reset_index()
    b = d.merge(d4c, on=["trimestre", "cod_prov"], how="left")
    b["d4_ln_hipotecas_importe"] = b["d4_hip_cf"]
    s = cu_cf("2013Q4", "2014Q1")
    b["cu_x_expo"] = b["trimestre"].map(s) * b["expo"]
    b["x_cu"] = b["trimestre"].map(s - s.shift(4))
    out["b_credito_y_cu_congelados_2013Q4"] = b.drop(columns="d4_hip_cf").sort_values(
        ["cod_prov", "trimestre"]).reset_index(drop=True)
    c = d.copy()
    s = cu_cf("2021Q4", "2022Q1")
    c["cu_x_expo"] = c["trimestre"].map(s) * c["expo"]
    c["x_cu"] = c["trimestre"].map(s - s.shift(4))
    out["c_cu_2021Q4_en_P4"] = c
    return out


def periodo_de(q: str):
    for k, (a, b) in PERIODOS.items():
        if a <= q <= b:
            return k
    return None


# ------------------------------------------------------------------ diseño
def muestra(d: pd.DataFrame, mercado: str) -> pd.DataFrame:
    y = YVAR[mercado]
    v = [x[0] for x in SPEC_VARS[mercado] if x[0] not in ("d4_ln_terminadas_libres0", "tope_cat")]
    # (turismo: la ventana queda limitada por la disponibilidad de d4_ln_vut_viviendas)
    s = d[(d["trimestre"] >= "2008Q1") & (d["trimestre"] <= Q_FIN_MUESTRA)].copy()
    s = s.dropna(subset=[y, "pob_w", "x_cu"] + v)
    s["per"] = s["trimestre"].map(periodo_de)
    return s


def construir_X(s: pd.DataFrame, mercado: str, modelo: str):
    """Devuelve Xc (contribuciones), meta (DataFrame col, var, familia, periodo), Xn (molestia)."""
    per = s["per"].values
    cols, meta = [], []
    for v, fam, por in SPEC_VARS[mercado]:
        x = s[v].values.astype(float)
        if por:
            for p in PNAMES:
                cols.append(np.where(per == p, x, 0.0))
                meta.append((f"{v}__{p}", v, fam, p))
        else:
            cols.append(x)
            meta.append((v, v, fam, "global"))
    if modelo == "M2":
        cols.append(s["x_cu"].values.astype(float))
        meta.append(("x_cu", "x_cu", "credito_tipos_cu", "global"))
    Xc = np.column_stack(cols)
    nu = [s["miss_oferta"].values.astype(float)]
    if modelo == "M2":
        q = s["trimestre"].str[-1].values
        for k in ("2", "3", "4"):
            nu.append((q == k).astype(float))
        for p in PNAMES[1:]:
            nu.append((per == p).astype(float))
    Xn = np.column_stack(nu)
    return Xc, pd.DataFrame(meta, columns=["col", "var", "familia", "periodo"]), Xn


# ------------------------------------------------------------------ estimación FE
def _grp(ids):
    ids = np.asarray(ids)
    n = ids.max() + 1
    G = sparse.csr_matrix((np.ones(len(ids)), (ids, np.arange(len(ids)))), shape=(n, len(ids)))
    return G, np.asarray(G.sum(axis=1)).ravel()


def demean(A, groups, tol=1e-11, maxit=300):
    A = A.copy()
    gs = [_grp(g) for g in groups]
    for _ in range(maxit):
        mx = 0.0
        for G, c in gs:
            m = (G @ A) / c[:, None]
            A -= G.T @ m
            mx = max(mx, float(np.abs(m).max()))
        if mx < tol or len(gs) == 1:
            break
    return A


def ajustar(Y, Xc, Xn, uid, tid, modelo):
    Z = np.column_stack([Xc, Xn])
    A = np.column_stack([Y, Z])
    A = demean(A, [uid, tid] if modelo == "M1" else [uid])
    yt, Zt = A[:, 0], A[:, 1:]
    b = np.linalg.lstsq(Zt, yt, rcond=None)[0]
    e = yt - Zt @ b
    return b[:Xc.shape[1]], e


def agregar(Y, Xc, beta, e, w, tid, nslot, slot_per, fam_idx, extra_X=None):
    """Descomposición ponderada. Devuelve dict componente -> vector (4 periodos) en pp acumulados."""
    wn = w / np.bincount(tid, w, minlength=nslot)[tid]
    contrib_rows = Xc * beta
    fe = Y - contrib_rows.sum(1) - e
    comps = {f: contrib_rows[:, idx].sum(1) for f, idx in fam_idx.items()}
    comps["explicado_familias"] = contrib_rows.sum(1)
    comps["comun_efectos_tiempo"] = fe
    comps["residuo"] = e
    comps["observado"] = Y
    if extra_X is not None:
        for nm, Xcf in extra_X.items():
            comps["cf__" + nm] = ((Xcf - Xc) * beta).sum(1)
    out = {}
    nper = np.array([(slot_per == p).sum() for p in range(4)])
    for k, v in comps.items():
        sl = np.bincount(tid, wn * v, minlength=nslot)
        out[k] = np.array([100.0 * sl[slot_per == p].mean() * nper[p] / 4.0 if nper[p] else np.nan
                           for p in range(4)])
    return out


class Panel:
    """Contenedor numérico de una muestra (mercado, modelo) con sus índices para los remuestreos."""

    def __init__(self, s, mercado, modelo, cf_dfs):
        self.s, self.mercado, self.modelo = s, mercado, modelo
        self.Y = s[YVAR[mercado]].values.astype(float)
        self.Xc, self.meta, self.Xn = construir_X(s, mercado, modelo)
        self.w = s["pob_w"].values.astype(float)
        self.uid0 = pd.factorize(s["cod_prov"])[0]
        tq = sorted(s["trimestre"].unique())
        self.tq = tq
        self.tid0 = s["trimestre"].map({q: i for i, q in enumerate(tq)}).values
        self.tper = np.array([PNAMES.index(periodo_de(q)) for q in tq])
        self.G = self.uid0.max() + 1
        self.T = len(tq)
        self.rows_u = [np.flatnonzero(self.uid0 == g) for g in range(self.G)]
        self.rows_t = [np.flatnonzero(self.tid0 == t) for t in range(self.T)]
        self.fam_idx = {f: np.flatnonzero(self.meta["familia"].values == f).tolist()
                        for f in dict.fromkeys(self.meta["familia"])}
        self.fam_idx["demografia"] = sorted(self.fam_idx.get("demografia_20_34", []) + self.fam_idx.get("demografia_extranj", []))
        self.cf = {}
        for nm, dfc in cf_dfs.items():
            sc = dfc.set_index(["cod_prov", "trimestre"]).loc[list(zip(s["cod_prov"], s["trimestre"]))].reset_index()
            sc["per"] = s["per"].values
            sc["x_cu"] = sc["x_cu"].values
            Xcf, _, _ = construir_X(sc, mercado, modelo)
            self.cf[nm] = Xcf

    # -- una "realización": remuestreo de filas
    def corre(self, rows=None, uid=None, tid=None, nslot=None, slot_per=None):
        if rows is None:
            rows, uid, tid, nslot, slot_per = np.arange(len(self.Y)), self.uid0, self.tid0, self.T, self.tper
        Y, Xc, Xn, w = self.Y[rows], self.Xc[rows], self.Xn[rows], self.w[rows]
        beta, e = ajustar(Y, Xc, Xn, uid, tid, self.modelo)
        extra = {k: v[rows] for k, v in self.cf.items()}
        agg = agregar(Y, Xc, beta, e, w, tid, nslot, slot_per, self.fam_idx, extra)
        return beta, agg

    def draw_cluster(self, rng):
        g = rng.integers(0, self.G, self.G)
        rows = np.concatenate([self.rows_u[i] for i in g])
        uid = np.concatenate([np.full(len(self.rows_u[i]), k) for k, i in enumerate(g)])
        return rows, uid, self.tid0[rows], self.T, self.tper

    def draw_time(self, rng, L=4):
        qsel = []
        for p in range(4):
            qs = np.flatnonzero(self.tper == p)
            n = len(qs)
            if n == 0:
                continue
            Lb = min(L, n)
            nb = int(np.ceil(n / Lb))
            st = rng.integers(0, n - Lb + 1, nb)
            qsel.append(np.concatenate([qs[s0:s0 + Lb] for s0 in st])[:n])
        qsel = np.concatenate(qsel)
        rows = np.concatenate([self.rows_t[q] for q in qsel])
        tid = np.concatenate([np.full(len(self.rows_t[q]), k) for k, q in enumerate(qsel)])
        slot_per = self.tper[qsel]
        return rows, self.uid0[rows], tid, len(qsel), slot_per


def bootstrap(panel: Panel, kind: str, B: int, seed: int):
    rng = np.random.default_rng(seed)
    acc, betas = {}, []
    for _ in range(B):
        r = panel.draw_cluster(rng) if kind == "cluster" else panel.draw_time(rng)
        beta, agg = panel.corre(*r)
        betas.append(beta)
        for k, v in agg.items():
            acc.setdefault(k, []).append(v)
    return {k: np.array(v) for k, v in acc.items()}, np.array(betas)


def ic(a, lo=2.5, hi=97.5):
    return np.nanpercentile(a, [lo, hi], axis=0)
