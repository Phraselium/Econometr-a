"""V18 · réplica ciega de E1-R4 (Sagrada Família). Rótulo: réplica ciega V18; capa C4.

Implementada solo desde docs/v18/plan_replicacion.md (1.1, E1-R4) y docs/v18/plan_replicacion_adenda.md (1.5, R-15, Anexo B).
Diseño: DiD de las secciones censales de Barcelona a menos de 500 m del templo frente al anillo de 500-1.000 m, SERPAVI
(mediana €/m², vivienda colectiva, ALQM2_LV_M_VC) por sección, 2011-2019, base 2013, tratamiento desde 2014.
Inferencia: cluster por barrio con wild cluster bootstrap de Webb (WCR, 9.999 réplicas, SEED 20261010); IC por inversión del test.
TOST con delta = 0,05 en log (Anexo B, E1-R4). Sin red. No abre data/sealed ni src/v18/estimacion.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import stats
from shapely import wkt
from shapely.geometry import Point

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
from src.v18 import sellado  # noqa: E402

SEED = 20261010
B = 9999
DELTA = 0.05
ORQ = {"est": 0.0018, "lo": -0.0446, "hi": 0.0418, "n_rad": 77, "n_ani": 693, "clusters": 6}
SALIDA = RAIZ / "output" / "v18" / "replica" / "e1_r4"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
ANIOS = list(range(2011, 2020))
PRE, POST, BASE = [2011, 2012, 2013], list(range(2014, 2020)), 2013


def dm2(A):
    return A - A.mean(-1, keepdims=True) - A.mean(-2, keepdims=True) + A.mean((-2, -1), keepdims=True)


def cr1(Dt, e, cl):
    G = len(np.unique(cl))
    N = e.size
    sc = np.zeros(G)
    idx = np.unique(cl, return_inverse=True)[1]
    np.add.at(sc, idx, (Dt * e).sum(1))
    sdd = float((Dt ** 2).sum())
    c = G / (G - 1) * (N - 1) / (N - e.shape[1])
    return float(np.sqrt(c * (sc ** 2).sum()) / sdd), idx, G


def did(y, D, cl):
    Dt, yt = dm2(D), dm2(y)
    sdd = float((Dt ** 2).sum())
    b = float((Dt * yt).sum() / sdd)
    se, idx, G = cr1(Dt, yt - b * Dt, cl)
    return b, se, Dt, idx, G


def wcr_p(y, D, cl, b0, rng, B=B):
    b, se, Dt, idx, G = did(y, D, cl)
    t = (b - b0) / se
    er = dm2(y - b0 * D)
    sdd = float((Dt ** 2).sum())
    N, T = y.shape[0] * y.shape[1], y.shape[1]
    c = G / (G - 1) * (N - 1) / (N - T)
    cnt, hecho = 0, 0
    while hecho < B:
        n = min(2500, B - hecho)
        w = WEBB[rng.integers(0, 6, size=(n, G))][:, idx]          # (n, S)
        ys = dm2(w[:, :, None] * er[None])
        bs = (Dt[None] * ys).sum((1, 2)) / sdd
        es = ys - bs[:, None, None] * Dt[None]
        sc = np.zeros((n, G))
        for g in range(G):
            sc[:, g] = (Dt[None, idx == g] * es[:, idx == g]).sum((1, 2))
        ses = np.sqrt(c * (sc ** 2).sum(1)) / sdd
        cnt += int(np.sum(np.abs(bs / ses) >= abs(t) - 1e-12))
        hecho += n
    return cnt / B


def ic_webb(y, D, cl, alfa, rng, B=B):
    b, se, *_ = did(y, D, cl)
    grid = np.linspace(b - 40 * se, b + 40 * se, 321)
    ps = np.array([wcr_p(y, D, cl, g, rng, B=3999) for g in grid])
    ok = grid[ps >= alfa]
    return float(ok.min()), float(ok.max())


def construir():
    b = pd.read_csv(RAIZ / "data/raw/v18/e1e6/bcn_seccions_censals_barri.csv", dtype=str)
    b["cod"] = "08019" + b.codi_districte.str.zfill(2) + b.codi_seccio_censal.str.zfill(3)
    g = gpd.GeoDataFrame(b[["cod", "nom_barri", "codi_barri", "codi_districte"]],
                         geometry=b.geometria_etrs89.map(wkt.loads), crs=25831)
    p = gpd.GeoSeries([Point(2.1744, 41.4036)], crs=4326).to_crs(25831).iloc[0]    # Sagrada Família (basílica)
    g["dc"], g["dmin"] = g.geometry.centroid.distance(p), g.distance(p)
    s = pd.read_csv(RAIZ / "data/raw/v3/serpavi_secciones_nacional_v3.csv.gz", dtype={"codigo": str})
    s = s[s.serie.str.endswith("_ALQM2_LV_M_VC") & s.serie.str.startswith("SERPAVI_SEC_08019")].copy()
    s["cod"] = s.serie.str.extract(r"SEC_(\d{10})")[0]
    s["periodo"] = s.periodo.astype(str)
    s = sellado.filtrar(s, "cod", "seccion", "periodo", "serpavi_alquiler_m2_mediana", "A")
    s = s[s.periodo.astype(int).between(2011, 2019)]
    n = s.groupby("cod").periodo.nunique()
    s = s[s.cod.isin(n[n == 9].index)]
    s = s[s.valor > 0]
    n = s.groupby("cod").periodo.nunique()
    s = s[s.cod.isin(n[n == 9].index)]
    return g, s


def panel(g, s, tr, co):
    sel = g[g.cod.isin(s.cod) & (tr | co)].copy()
    sel["D"] = tr[sel.index].astype(float)
    P = s[s.cod.isin(sel.cod)].pivot(index="cod", columns="periodo", values="valor")
    P = np.log(P.loc[sel.cod]); P.columns = P.columns.astype(int)
    y = P[ANIOS].to_numpy()
    d = sel.D.to_numpy()
    cl = sel.codi_barri.to_numpy()
    return sel, y, d, cl


def estimar(g, s, tr, co, rng, completo=True):
    sel, y, d, cl = panel(g, s, tr, co)
    Dpost = d[:, None] * np.array([[t in POST for t in ANIOS]], float)
    b, se, Dt, idx, G = did(y, Dpost, cl)
    out = {"n_tratadas": int(d.sum()), "n_control": int((1 - d).sum()), "clusters": int(G),
           "beta": b, "se_cr1": se, "G": G}
    if not completo:
        return out, (sel, y, d, cl)
    out["p_webb"] = wcr_p(y, Dpost, cl, 0.0, rng)
    out["ic95_webb"] = ic_webb(y, Dpost, cl, 0.05, rng)
    out["ic90_webb"] = ic_webb(y, Dpost, cl, 0.10, rng)
    lo, hi = out["ic90_webb"]
    out["tost_equivalencia"] = bool(lo > -DELTA and hi < DELTA)
    return out, (sel, y, d, cl)


def evento(y, d, cl):
    """Coeficientes por año (base 2013) con TWFE y covarianza CR1 por barrio; contraste conjunto de adelantos."""
    ks = [k for k in ANIOS if k != BASE]
    S, T = y.shape
    X = np.stack([d[:, None] * np.array([[t == k for t in ANIOS]], float) for k in ks], -1)   # S,T,K
    Xt = np.stack([dm2(X[..., j]) for j in range(len(ks))], -1)
    yt = dm2(y)
    XtX = np.einsum("stj,stk->jk", Xt, Xt)
    bet = np.linalg.solve(XtX, np.einsum("stj,st->j", Xt, yt))
    e = yt - np.einsum("stj,j->st", Xt, bet)
    idx = np.unique(cl, return_inverse=True)[1]
    G = idx.max() + 1
    sc = np.zeros((G, len(ks)))
    np.add.at(sc, idx, np.einsum("stj,st->sj", Xt, e))
    c = G / (G - 1) * (S * T - 1) / (S * T - T - len(ks) + 1)
    inv = np.linalg.inv(XtX)
    V = c * inv @ (sc.T @ sc) @ inv
    lead = [ks.index(k) for k in (2011, 2012)]
    bl, Vl = bet[lead], V[np.ix_(lead, lead)]
    try:
        W = float(bl @ np.linalg.solve(Vl, bl))
        p_adel = float(1 - stats.f.cdf(W / 2, 2, G - 1))
    except np.linalg.LinAlgError:
        W, p_adel = float("nan"), float("nan")
    return dict(zip(map(str, ks), bet)), dict(zip(map(str, ks), np.sqrt(np.diag(V)))), W, p_adel


def main():
    rng = np.random.default_rng(SEED)
    g, s = construir()
    r_all = g.dc < 500
    ani_all = (g.dc >= 500) & (g.dc < 1000)
    gracia = g.codi_districte.isin(["6", "06"])
    # regla de estimabilidad (adenda 1.5): radio y anillo conservan >= 75 % tras excluir Gràcia
    ret_r = float((r_all & ~gracia).sum() / r_all.sum())
    ret_a = float((ani_all & ~gracia).sum() / ani_all.sum())
    tr, co = r_all & g.cod.isin(s.cod), ani_all & g.cod.isin(s.cod)
    res = {"recuento_total_geometria": {"radio": int(r_all.sum()), "anillo": int(ani_all.sum()),
                                        "retencion_radio_sin_gracia": ret_r, "retencion_anillo_sin_gracia": ret_a,
                                        "gracia_en_radio": int((r_all & gracia).sum()), "gracia_en_anillo": int((ani_all & gracia).sum())}}
    res["estimable"] = bool(ret_r >= 0.75 and ret_a >= 0.75)
    pri, (sel, y, d, cl) = estimar(g, s, tr, co, rng)
    res["principal"] = pri
    ev, evse, W, p_adel = evento(y, d, cl)
    res["evento"] = {"coef": ev, "se_cr1": evse, "wald_adelantos": W, "p_adelantos_F": p_adel}
    # placebo de fecha: adopción falsa en 2012, ventana 2011-2013
    yy = y[:, :3]
    Dfalso = d[:, None] * np.array([[0, 1, 1]], float)
    bp, sep, *_ = did(yy, Dfalso, cl)
    res["placebo_fecha_2012"] = {"beta": bp, "se_cr1": sep, "p_webb": wcr_p(yy, Dfalso, cl, 0.0, rng)}
    # variantes (no principales, declaradas): control = resto de Barcelona no sellada (v1 del Anexo A); radios 300 m / 300-800 m (v2);
    # distancia al polígono en lugar del centroide; diagnóstico de recuento (centroide < 1.000 m).
    var = {}
    v, _ = estimar(g, s, r_all & g.cod.isin(s.cod), (~r_all) & g.cod.isin(s.cod), rng, completo=False)
    var["v1_resto_de_Barcelona"] = v
    v, _ = estimar(g, s, (g.dc < 300) & g.cod.isin(s.cod), (g.dc >= 300) & (g.dc < 800) & g.cod.isin(s.cod), rng, completo=False)
    var["v2_300m_vs_300_800m"] = v
    v, _ = estimar(g, s, (g.dmin < 500) & g.cod.isin(s.cod), (g.dmin >= 500) & (g.dmin < 1000) & g.cod.isin(s.cod), rng, completo=False)
    var["poligono_dmin"] = v
    v, _ = estimar(g, s, (g.dc < 1000) & g.cod.isin(s.cod), (~(g.dc < 1000)) & g.cod.isin(s.cod), rng, completo=False)
    var["diagnostico_recuento_dc_menor_1000_vs_resto"] = v
    res["variantes"] = var
    # comparación con el orquestador
    b, se = pri["beta"], pri["se_cr1"]
    se_orq = (ORQ["hi"] - ORQ["lo"]) / (2 * 1.96)
    dif = b - ORQ["est"]
    res["comparacion"] = {"orquestador": ORQ, "diferencia_abs": dif,
                          "diferencia_rel": dif / abs(ORQ["est"]),
                          "dif_sobre_se_propio": dif / se, "dif_sobre_se_orq_aprox": dif / se_orq,
                          "coincide_redondeo_4dec": round(b, 4) == round(ORQ["est"], 4),
                          "estimacion_en_ic_orq": bool(ORQ["lo"] <= b <= ORQ["hi"]),
                          "orq_en_ic_propio_webb": bool(pri["ic95_webb"][0] <= ORQ["est"] <= pri["ic95_webb"][1]),
                          "veredicto": "coincide" if (abs(dif) < 0.1 * min(se, se_orq) or round(b, 4) == round(ORQ["est"], 4)) else "difiere"}
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "datos_intermedios.json").write_text(json.dumps(res, indent=1, default=float, ensure_ascii=False), encoding="utf-8")
    rj = {"rama": "v18", "pregunta": "E1-R4 réplica ciega V18; capa C4: Sagrada Família, radio 500 m frente a anillo 500-1.000 m",
          "capa": "C4", "datos": "SERPAVI alquiler €/m² mediana vivienda colectiva por sección, Barcelona 2011-2019; geometría Ajuntament (secciones-barrio)",
          "N": int(len(sel) * len(ANIOS)), "metodo": "DiD TWFE (sección y año), tratamiento 2014-2019, base 2013, cluster barrio, WCR Webb 9.999",
          "estimacion": b, "ic95": list(pri["ic95_webb"]), "p_ajustado": pri["p_webb"],
          "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "no se clasifica (réplica ciega)",
          "diagnosticos": {"evento": res["evento"], "placebo_fecha_2012": res["placebo_fecha_2012"],
                           "tost_delta_0.05": {"ic90_webb": pri["ic90_webb"], "equivalencia": pri["tost_equivalencia"]},
                           "n_tratadas": pri["n_tratadas"], "n_control": pri["n_control"], "clusters": pri["clusters"],
                           "se_cr1": se},
          "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
          "notas": "Réplica ciega; comparación con el orquestador en comparacion de datos_intermedios.json", "comparacion": res["comparacion"]}
    (SALIDA / "resultado.json").write_text(json.dumps(rj, indent=1, default=float, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, default=float, ensure_ascii=False))


if __name__ == "__main__":
    main()
