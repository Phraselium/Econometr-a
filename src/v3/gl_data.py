"""Panel sección-año 2021-2024 (alquiler SERPAVI + VUT INE) sin observaciones selladas v3."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

D = RAIZ / "data/raw/v3/"
SEED = 20261010
ANIOS = [2021, 2022, 2023, 2024]
MEDIDA_ALQ = "ALQM2_LV_M_VC"


def _anio(p):
    return p.str[:4].astype(int)


def carga(nivel="seccion", provincias=None):
    """Devuelve (panel balanceado, dict de pérdidas). Excluye sellados ANTES de calcular."""
    n = 10 if nivel == "seccion" else 7
    ruta = D / ("serpavi_secciones_nacional_v3.csv.gz" if nivel == "seccion" else "serpavi_distritos_nacional_v3.csv.gz")
    s = pd.read_csv(ruta, usecols=["periodo", "serie", "valor", "codigo"], dtype={"codigo": str})
    s = s[s.serie.str.endswith(MEDIDA_ALQ) & s.periodo.isin(ANIOS)].copy()
    s["codigo"] = s.codigo.str.zfill(n)
    if provincias:
        s = s[s.codigo.str[:2].isin(provincias)]
    s = s[~holdout.es_sellado_v3(s.codigo)]
    alq = s.rename(columns={"periodo": "anio", "valor": "alq"})[["codigo", "anio", "alq"]]
    v = pd.read_csv(D / "ine_v3_vut_seccion.csv.gz", usecols=["periodo", "nivel", "codigo", "medida", "valor"],
                    dtype={"codigo": str})
    v = v[(v.nivel == nivel) & (v.medida == "vivienda_turistica") & (v.periodo < "2025")]  # nunca 2026M05
    v["codigo"] = v.codigo.str.zfill(n)
    if provincias:
        v = v[v.codigo.str[:2].isin(provincias)]
    v = v[~holdout.es_sellado_v3(v.codigo, v.periodo)]
    v["anio"] = _anio(v.periodo)
    vut = v.groupby(["codigo", "anio"], as_index=False).valor.mean().rename(columns={"valor": "vut"})
    c = pd.read_csv(D / "ine_v3_censo2021_seccion_indicadores.csv.gz",
                    usecols=["serie", "codigo", "valor"], dtype={"codigo": str})
    c = c[c.serie.isin(["t18_1", "t21_1"])].pivot_table(index="codigo", columns="serie", values="valor").reset_index()
    c["codigo"] = c.codigo.str.zfill(10)
    if nivel == "distrito":
        c["codigo"] = c.codigo.str[:7]
        c = c.groupby("codigo", as_index=False)[["t18_1", "t21_1"]].sum()
    elif True:
        pass
    c = c.rename(columns={"t18_1": "viv", "t21_1": "hog"})
    p = alq.merge(vut, on=["codigo", "anio"]).merge(c, on="codigo")
    pierde = {"unidades_alq_sin_vut_o_censo": int(alq.codigo.nunique() - p.codigo.nunique())}
    p = p[(p.alq > 0) & (p.viv > 0)]
    ok = p.groupby("codigo").anio.nunique()
    ok = ok[ok == len(ANIOS)].index
    pierde["unidades_no_balanceadas_o_sin_alq"] = int(p.codigo.nunique() - len(ok))
    p = p[p.codigo.isin(ok)].copy()
    pierde["unidades_finales"] = int(p.codigo.nunique())
    p["lnalq"] = np.log(p.alq)
    p["vut100"] = 100 * p.vut / p.viv      # VUT por 100 viviendas
    p["distrito"] = p.codigo.str[:7]
    p["muni"] = p.codigo.str[:5]
    p["prov"] = p.codigo.str[:2]
    return p.reset_index(drop=True), pierde


def demean2(df, cols, u="codigo", t="anio"):
    """Within bidireccional (panel balanceado, exacto)."""
    x = df[cols].astype(float)
    return x - x.groupby(df[u]).transform("mean") - x.groupby(df[t]).transform("mean") + x.mean()


def fe_cluster(df, y, x, cl="distrito", w=None, u="codigo", t="anio"):
    """MCO con FE de unidad y año (balanceado), EE agrupados CR1. x lista. Devuelve dict."""
    z = demean2(df, [y] + x, u, t)
    Y = z[y].values
    X = z[x].values
    if w is not None:
        sw = np.sqrt(w)
        Y, X = Y * sw, X * sw[:, None]
    XtX = X.T @ X
    b = np.linalg.solve(XtX, X.T @ Y)
    e = Y - X @ b
    g = pd.factorize(df[cl])[0]
    G = g.max() + 1
    sc = np.zeros((G, X.shape[1]))
    np.add.at(sc, g, X * e[:, None])
    bread = np.linalg.inv(XtX)
    V = bread @ (sc.T @ sc) @ bread
    n, k = len(Y), len(x)
    N = df[u].nunique()
    V *= (G / (G - 1)) * ((n - 1) / (n - k - N - df[t].nunique() + 1))
    se = np.sqrt(np.diag(V))
    from scipy import stats
    tc = stats.t.ppf(0.975, G - 1)
    return {"b": b, "se": se, "lo": b - tc * se, "hi": b + tc * se,
            "p": 2 * stats.t.sf(np.abs(b / se), G - 1), "n": n, "G": int(G), "resid": e, "Xw": X}
