"""V16 · fase 6 · Q3-b: correlación transversal por sección (adenda, punto 3) y prueba conjunta BLP/GATES de Q3 (punto 13).

Especificación principal: Δlog SERPAVI €/m² (VC, mediana, 2021→2024) = β · cuota de extranjeros 2022 (estandarizada, DT entre secciones)
+ efectos fijos de municipio; inferencia: Conley a 2 km (núcleo de Bartlett, normal). APTO solo en el escenario principal y NO robusto a la
sensibilidad del rango espacial (veredicto K12): los radios 0,5 y 1,5 km NO pasan, y la estimación puntual no depende del radio.
BLP/GATES: NO APTO → solo estimación puntual descriptiva. Capa C4 (correlación). Ejecución: python src/v16/q3_seccion.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.spatial import cKDTree
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qb_comun as C  # noqa: E402
from econ_utils import Registry  # noqa: E402
import holdout as H  # noqa: E402

OUT = C.RAIZ / "output" / "v16" / "q3"
CORTE_KM = 2.0
VAR_X = "ine_padron_seccion_poblacion_personas"


def geometria() -> pd.DataFrame:
    s = pd.read_parquet(C.RAIZ / "data/base/geo/secciones.parquet", columns=["cod_seccion", "cod_municipio", "cod_provincia", "geometry"])
    s = s[~H.unidad_sellada_v16(s.cod_seccion, "seccion")].reset_index(drop=True)
    xyz = C.centroides(s)
    s["x_km"], s["y_km"], s["z_km"] = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    return s.drop(columns="geometry")


def serpavi(tip: str, años: list[int]) -> pd.DataFrame:
    a = C.cargar("base_alquiler", "serpavi_alquiler_m2_mediana", "seccion", f"tipologia={tip}")
    a = a.assign(t=a.periodo.astype(int))
    w = a[a.t.isin(años)].pivot_table(index="territorio_codigo", columns="t", values="valor", aggfunc="first")
    return np.log(w.where(w > 0))


def cuotas() -> pd.DataFrame:
    d = C.cargar("tension_social", VAR_X, "seccion")
    d = d[d.periodo.astype(str) == "2022"]
    p = d[d.desagregacion.str.startswith("sexo=ambos_sexos")].pivot_table(index="territorio_codigo", columns="desagregacion", values="valor", aggfunc="first")
    p.columns = [c.split("nacionalidad=")[1] for c in p.columns]
    out = pd.DataFrame(index=p.index)
    out["cuota_ext"] = 100 * p["total_extranjera"] / p["total"]
    out["cuota_no_europea"] = 100 * (p["africana"] + p["americana"] + p["asiatica"] + p["resto"]) / p["total"]
    out["pob2022"] = p["total"]
    return out.replace([np.inf, -np.inf], np.nan)


def moderadores(sec: pd.DataFrame) -> pd.DataFrame:
    m = pd.DataFrame(index=sec.index)
    r = C.cargar("base_oferta", "adrh_renta_neta_persona", "seccion")
    r = r[r.periodo.astype(str) == "2019"].groupby("territorio_codigo").valor.first()
    m["renta_adrh"] = np.log(r.reindex(m.index).where(lambda s: s > 0))
    m["poblacion"] = np.log(sec.pob2022.where(sec.pob2022 > 0))
    m["cuota_extranjeros"] = sec.cuota_ext
    v = C.cargar("base_turismo", "ine_vut_porcentaje_vivienda_turistica", "seccion")
    v = v[v.periodo.astype(str) == "2021-02"].groupby("territorio_codigo").valor.first()
    m["pct_vut"] = v.reindex(m.index)
    o = C.cargar("base_oferta", "obra_nueva_neta_catastro", "municipio")
    o = o[o.periodo.astype(int).between(2018, 2021)].groupby("territorio_codigo").valor.sum()
    pm = C.cargar("base_poblacion", "pob_censo_anual", "municipio", "nacionalidad=Total")
    pm = pm[pm.periodo.astype(int) == 2021].groupby("territorio_codigo").valor.first()
    ob = (o / pm).replace([np.inf, -np.inf], np.nan)
    m["obra_pc"] = pd.Series(m.index.str[:5], index=m.index).map(ob)
    return m


def conley(xt, res, K) -> dict:
    s = xt * res
    v = float(s @ (K @ s))
    sxx = float((xt ** 2).sum())
    if v <= 0:
        return {"se": np.nan, "var_no_positiva": True}
    return {"se": float(np.sqrt(v) / sxx), "var_no_positiva": False}


def kernel(xyz: np.ndarray, corte: float = CORTE_KM):
    tree = cKDTree(xyz)
    D = tree.sparse_distance_matrix(tree, corte, output_type="coo_matrix")
    n = len(xyz)
    ii = np.concatenate([D.row, np.arange(n)])
    jj = np.concatenate([D.col, np.arange(n)])
    dd = np.concatenate([D.data, np.zeros(n)])
    return sp.csr_matrix((np.maximum(0.0, 1 - dd / corte), (ii, jj)), shape=(n, n))


def ajustar(d: pd.DataFrame, ycol: str, xcol: str, con_conley: bool, controles: list[str] | None = None) -> dict | None:
    d = d.dropna(subset=[ycol, xcol] + (controles or []))
    n_mun = d.groupby("cod_municipio").cod_seccion.transform("size")
    d = d[n_mun > 1].sort_values(["cod_municipio", "cod_seccion"]).reset_index(drop=True)
    if len(d) < 50:
        return None
    x = (d[xcol] - d[xcol].mean()) / d[xcol].std()
    g = [C.codif(d.cod_municipio)]
    X = np.column_stack([x.values] + ([d[c].values for c in controles] if controles else []))
    r = C.mco_fe(d[ycol].values, X, g)
    b = float(r["beta"][0])
    out = {"beta_por_DT": b, "n": len(d), "n_mun": int(g[0].max() + 1), "r2_total": r["r2_total"], "r2_within": r["r2_within"],
           "sdx_t": float(r["sdx_t"][0]), "sdy_t": r["sdy_t"], "d": d, "r": r, "x": x}
    if con_conley:
        K = kernel(d[["x_km", "y_km", "z_km"]].values)
        c = conley(r["Xt"][:, 0], r["resid"], K)
        out.update(c)
        if not c["var_no_positiva"]:
            dof = len(d) - out["n_mun"] - 1
            out["t"] = b / c["se"]
            out["p"] = float(2 * (1 - norm.cdf(abs(out["t"]))))
            out["ic95"] = [b - 1.959964 * c["se"], b + 1.959964 * c["se"]]
            out["dof"] = dof
        out["vecinos_medios"] = K.nnz / len(d)
    return out


def blp_gates(d: pd.DataFrame, mods: list[str]) -> dict:
    """BLP lineal con interacciones y GATES por cuartiles con validación cruzada (2 mitades por municipio). Solo puntual."""
    d = d.dropna(subset=["dy", "x"] + mods).copy()
    n_mun = d.groupby("cod_municipio").cod_seccion.transform("size")
    d = d[n_mun > 1].reset_index(drop=True)
    Z = (d[mods] - d[mods].mean()) / d[mods].std()
    d["x"] = (d.x - d.x.mean()) / d.x.std()
    g = [C.codif(d.cod_municipio)]
    XI = np.column_stack([d.x.values] + [d.x.values * Z[m].values for m in mods] + [Z[m].values for m in mods])
    r = C.mco_fe(d.dy.values, XI, g)
    k = len(mods)
    b_int = dict(zip(mods, [float(v) for v in r["beta"][1:1 + k]]))
    r0 = C.mco_fe(d.dy.values, np.column_stack([d.x.values] + [Z[m].values for m in mods]), g)
    # GATES con validación cruzada
    rng = np.random.default_rng([C.SEED, 33])
    munis = d.cod_municipio.unique()
    mitad = dict(zip(munis, rng.integers(0, 2, len(munis))))
    f = d.cod_municipio.map(mitad).values
    res_g = {q: [] for q in range(4)}
    for a in (0, 1):
        A, B = d[f == a], d[f != a]
        ZA, ZB = Z[f == a], Z[f != a]
        gA = C.codif(A.cod_municipio)
        XA = np.column_stack([A.x.values] + [A.x.values * ZA[m].values for m in mods] + [ZA[m].values for m in mods])
        rA = C.mco_fe(A.dy.values, XA, [gA])
        gh = rA["beta"][1:1 + k]
        h = ZB[mods].values @ gh
        cuart = pd.qcut(h, 4, labels=False, duplicates="drop")
        for q in range(4):
            Bq = B[cuart == q]
            nq = Bq.groupby("cod_municipio").cod_seccion.transform("size")
            Bq = Bq[nq > 1]
            if len(Bq) > 30:
                rq = C.mco_fe(Bq.dy.values, Bq.x.values, [C.codif(Bq.cod_municipio)])
                res_g[q].append(float(rq["beta"][0]))
    gates = {f"cuartil_{q + 1}": (float(np.mean(v)) if v else None) for q, v in res_g.items()}
    dif = (gates["cuartil_4"] - gates["cuartil_1"]) if gates["cuartil_4"] is not None and gates["cuartil_1"] is not None else None
    return {"n": len(d), "beta_x_media": float(r["beta"][0]), "interacciones_x_moderador_por_DT": b_int,
            "r2_within_con_interacciones": r["r2_within"], "r2_within_sin_interacciones": r0["r2_within"],
            "ganancia_r2_within": r["r2_within"] - r0["r2_within"], "gates_beta_por_DT": gates, "gates_q4_menos_q1": dif,
            "estado": "NO APTO (blp_gates: tamaño 0,005, cobertura 0,9885): estimación puntual descriptiva, sin p-valor ni IC"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registro_q3b.csv")
    geo = geometria()
    cu = cuotas()
    vc = serpavi("VC", [2018, 2021, 2022, 2024])
    vu = serpavi("VU", [2021, 2024])
    D = geo.set_index("cod_seccion").join(cu, how="inner").join(vc.add_prefix("vc"), how="inner").join(vu.add_prefix("vu"), how="left")
    D["dy"] = D["vc2024"] - D["vc2021"]
    D["dy_pre"] = D["vc2021"] - D["vc2018"]
    D["dy22"] = D["vc2024"] - D["vc2022"]
    D["dyvu"] = D["vu2024"] - D["vu2021"]
    D["x"] = D.cuota_ext
    D = D.reset_index().rename(columns={"index": "cod_seccion"})
    D = D.rename(columns={D.columns[0]: "cod_seccion"}) if "cod_seccion" not in D.columns else D
    res: dict = {"especificaciones": []}

    def anotar(mid, formula, a, principal=False, nota="", p_lista=False):
        reg.log("v16-fase6", mid, formula, "2021", "2024", a["n"], a["r2_total"], np.nan, np.nan, np.nan, a["beta_por_DT"],
                a.get("p", np.nan) if p_lista else np.nan, nota)
        res["especificaciones"].append({"id": mid, "beta_por_DT": a["beta_por_DT"], "n": a["n"], "principal": principal,
                                         "se_conley": a.get("se") if p_lista else None, "p_conley": a.get("p") if p_lista else None})

    # principal
    P = ajustar(D, "dy", "x", True)
    anotar("Q3-b|VC|cuota_ext|2021-2024|Conley2km|PRINCIPAL", "dlogSERPAVI ~ cuota_ext_std + FE municipio", P, True, "Conley 2 km APTO solo escenario principal", True)
    res["principal"] = {k: P[k] for k in ["beta_por_DT", "se", "t", "p", "ic95", "n", "n_mun", "r2_total", "r2_within", "vecinos_medios", "dof"]}
    res["p_valores_para_BY"] = [{"id": "Q3-b|principal", "p": P["p"], "rama": "diseños"}]
    # multiverso (8): tipología × exposición × ventana (puntuales; Conley solo en la principal)
    for tip, xc, vent in [(t, x, v) for t in ["VC", "VU"] for x in ["cuota_ext", "cuota_no_europea"] for v in ["2021-2024", "2022-2024"]]:
        if (tip, xc, vent) == ("VC", "cuota_ext", "2021-2024"):
            continue
        yc = {("VC", "2021-2024"): "dy", ("VC", "2022-2024"): "dy22", ("VU", "2021-2024"): "dyvu"}.get((tip, vent))
        if yc is None:  # VU 2022-2024 no cargado
            continue
        a = ajustar(D.assign(x=D[xc]), yc, "x", False)
        if a:
            anotar(f"Q3-b|{tip}|{xc}|{vent}|puntual", "idem", a, False, "variante: solo estimación puntual")
    # VU 2022-2024: no cargado → registrado como omitido por datos
    reg.log("v16-fase6", "Q3-b|VU|*|2022-2024", "no estimada", "2022", "2024", 0, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, "VU 2022 no cargado (decisión de operativización D2); no se rellena")
    E = pd.DataFrame(res["especificaciones"])
    b0 = P["beta_por_DT"]
    res["multiverso"] = {"n_especificaciones": len(E), "mediana_beta_por_DT": float(E.beta_por_DT.median()), "min": float(E.beta_por_DT.min()),
                         "max": float(E.beta_por_DT.max()), "proporcion_mismo_signo": float((np.sign(E.beta_por_DT) == np.sign(b0)).mean()),
                         "nota": "variantes sin IC (Conley solo validado en el escenario principal)"}
    # sensibilidad al rango espacial
    res["sensibilidad_rango_espacial"] = {"radios_km_no_aptos": [0.5, 1.5], "beta_por_DT": b0,
                                           "nota": "la estimación puntual no depende del radio del núcleo; el EE a 0,5 y 1,5 km NO pasa el Monte Carlo y no se publica"}
    # diagnósticos
    dg = {}
    d, r = P["d"], P["r"]
    x0 = C.mco_fe(d.dy.values, P["x"].values, [np.zeros(len(d), int)])
    dg["oster"] = {"beta_sin_FE": float(x0["beta"][0]), "r2_sin_FE": x0["r2_total"], "beta_con_FE": b0, "r2_con_FE": P["r2_total"],
                   "delta_beta0_rmax1_3": C.oster_delta(float(x0["beta"][0]), x0["r2_total"], b0, P["r2_total"])}
    dl = dg["oster"]["delta_beta0_rmax1_3"]
    dg["oster"]["fragil_delta_lt_1"] = bool(np.isfinite(dl) and 0 <= dl < 1)
    dg["cinelli_hazlett_RV_q1"] = C.rv_q1(P["t"], P["dof"])
    dg["cinelli_hazlett_fragil_RV_lt_0_05"] = bool(dg["cinelli_hazlett_RV_q1"] < 0.05)
    dg["e_value_punto"] = C.e_value_puntual(b0, P["sdx_t"], P["sdy_t"])
    lim = min(P["ic95"], key=abs) if P["ic95"][0] * P["ic95"][1] > 0 else 0.0
    dg["e_value_limite_ic"] = C.e_value_puntual(lim, P["sdx_t"], P["sdy_t"]) if lim != 0.0 else 1.0
    dg["heterocedasticidad_BP_LM"] = C.heterocedasticidad_autocorr(r["resid"], r["Xt"][:, 0], np.arange(len(d)), np.zeros(len(d)))["breusch_pagan_LM"]
    dg["autocorrelacion_temporal"] = "no aplica (corte transversal)"
    dg["moran_residuos_secciones"] = C.moran(r["resid"], d[["x_km", "y_km", "z_km"]].values)
    # balance de covariables
    mods_all = moderadores(D.set_index("cod_seccion"))
    Dm = D.set_index("cod_seccion").join(mods_all.drop(columns=["cuota_extranjeros"]), how="left").reset_index()
    bal = {}
    for m in ["renta_adrh", "poblacion", "pct_vut"]:  # obra_pc es municipal: absorbida por el FE
        a = ajustar(Dm.assign(x=Dm.cuota_ext, **{m + "_s": (Dm[m] - Dm[m].mean()) / Dm[m].std()}), m + "_s", "x", False)
        bal[m] = {"coef_std_por_DT": a["beta_por_DT"], "n": a["n"]} if a else None
    dg["balance_covariables_con_FE_municipio"] = bal
    # pretendencia (placebo de fecha): Δlog 2018→2021
    pre = ajustar(D, "dy_pre", "x", True)
    dg["pretendencia_placebo_2018_2021"] = {"beta_por_DT": pre["beta_por_DT"], "se_conley": pre.get("se"), "ic95": pre.get("ic95"), "n": pre["n"],
                                           "nota": "mismo estimador y estructura que el principal, con otro periodo; diagnóstico, no entra en el control BY"}
    # sin grandes ciudades
    ex = ajustar(D[~D.cod_municipio.isin(C.GRANDES_MUN)], "dy", "x", True)
    dg["sin_grandes_ciudades"] = {"beta_por_DT": ex["beta_por_DT"], "se_conley": ex.get("se"), "n": ex["n"], "excluidas": sorted(C.GRANDES_MUN), "islas": "ninguna no sellada"}
    reg.log("v16-fase6", "Q3-b|excl_grandes", "idem sin Barcelona, València, Sevilla, Málaga", "2021", "2024", ex["n"], ex["r2_total"], np.nan, np.nan, np.nan, ex["beta_por_DT"], np.nan, "diagnóstico")
    reg.log("v16-fase6", "Q3-b|pretendencia", "Δlog 2018-2021 ~ cuota", "2018", "2021", pre["n"], pre["r2_total"], np.nan, np.nan, np.nan, pre["beta_por_DT"], np.nan, "diagnóstico")
    # TOST: sin magnitud de referencia
    dg["tost"] = "no concluyente: sin magnitud de referencia en la adenda (punto 3) y herramienta solo condicionada a Δ/EE ≥ 2"
    dg["magnitud_referencia"] = "ninguna (b no se cumple): a lo sumo una pista C4"
    res["diagnosticos"] = dg
    # BLP/GATES (Q3, punto 13)
    mods = ["renta_adrh", "poblacion", "cuota_extranjeros", "pct_vut", "obra_pc"]
    Dh = D.set_index("cod_seccion").join(mods_all[["renta_adrh", "poblacion", "pct_vut", "obra_pc"]], how="left").reset_index()
    Dh["cuota_extranjeros"] = Dh.cuota_ext
    res["blp_gates"] = blp_gates(Dh, mods)
    reg.log("v16-fase6", "Q3|BLP_GATES", "interacciones x·moderador + GATES cv", "2021", "2024", res["blp_gates"]["n"], np.nan, np.nan, np.nan, np.nan,
            res["blp_gates"]["beta_x_media"], np.nan, "NO APTO: puntual descriptivo")
    res["n_secciones_entrenamiento"] = len(geo)
    C.volcar(OUT / "q3b_resultado_parcial.json", res)
    reg.flush()
    print(res["principal"]); print(res["multiverso"]); print(dg["oster"], dg["cinelli_hazlett_RV_q1"], dg["e_value_punto"]); print(res["blp_gates"])
    print(dg["moran_residuos_secciones"], dg["balance_covariables_con_FE_municipio"], dg["pretendencia_placebo_2018_2021"], dg["sin_grandes_ciudades"])


if __name__ == "__main__":
    main()
