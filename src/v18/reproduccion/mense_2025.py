"""Reproduccion de Mense (2025), JPE Macroeconomics 3(1), tabla 3 (paneles A y B).

Reproduccion del estudio original con sus datos; no usa datos del proyecto.

Traduccion a Python de reduced_form_replication.R (secciones 1.2, 2.1, 2.2 y 3.1.1):
  1. Agregacion de terminaciones y clima municipales a regiones de ordenacion (PR).
  2. Indice hedonico de alquiler por PR y ano (regresion por PR, base 2011).
  3. IV en panel con efectos fijos de ano y PR, error agrupado por PR.

Lee SOLO el paquete data/bib/replicacion/mense_2025/. Sin red. SEED 20261010.
Requiere pyreadr (pip install pyreadr; no estaba instalado), geopandas/pyogrio, linearmodels.
Los shapefiles se leen dentro de los .zip sin descomprimir en disco.
"""
ALCANCE_TERRITORIAL = "sin lectura de datos"  # no lee data/raw, data/processed ni la base del proyecto

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)

RAIZ = Path(__file__).resolve().parents[3]
PAQ = RAIZ / "data/bib/replicacion/mense_2025"
SAL = RAIZ / "output/v18/reproduccion/mense_2025"
CLAVE = "mense_2025"

# Tabla 3, panel A (pagina 18 del PDF): coeficiente, error tipico
PUBLICADO = {
    1: {"b": -0.199, "se": 0.072, "kp": 17.4, "n": 752, "prs": 94,
        "ctrl": {"log_empleo": (0.991, 0.143)}, "fs": (-0.009, 0.002)},
    2: {"b": -0.204, "se": 0.072, "kp": 17.4, "n": 752, "prs": 94,
        "ctrl": {"log_empleo": (1.009, 0.145), "log_paro": (-0.028, 0.038)}, "fs": (-0.009, 0.002)},
    3: {"b": -0.192, "se": 0.065, "kp": 19.0, "n": 752, "prs": 94,
        "ctrl": {"log_empleo": (0.949, 0.142), "log_paro": (-0.050, 0.040),
                 "estudiantes": (0.002, 0.001)}, "fs": (-0.010, 0.002)},
}


def leer_rds(nombre, cols=None):
    import pyreadr
    df = pyreadr.read_r(str(PAQ / nombre))[None]
    return df if cols is None else df[cols]


# ---------------------------------------------------------------- 1. oferta y clima en PR
def panel_pr():
    import geopandas as gpd
    d = leer_rds("buildings_weather_shocks_panel_municip.RDS")
    d["AGS"] = d["AGS"].astype(int)
    d["NX2U1_autumn"] = d["NX2U1_10"] + d["NX2U1_11"] + d["NX2U1"]
    mens = ["NX2U1"] + [f"NX2U1_{i:02d}" for i in range(1, 12)]
    d["NX2U1_tot"] = d[mens].sum(axis=1)
    d = d.merge(d.groupby("AGS", as_index=False)["NX2U1_tot"].mean().rename(columns={"NX2U1_tot": "NX2U1_tot_avg"}), on="AGS")

    gmd = gpd.read_file(f"zip://{PAQ/'VG250_GEM.zip'}!replication/data/orig/shapes/MUN/VG250_GEM.shp")
    gmd["area"] = gmd.geometry.area
    gmd["AGS"] = gmd["AGS"].astype(int)
    gmd["geometry"] = gmd.geometry.make_valid()
    pr = gpd.read_file(f"zip://{PAQ/'PR250.zip'}!replication/data/orig/shapes/PR/PR250.shp").to_crs(gmd.crs)

    suma = ["NX2U1"] + [f"NX2U1_{i:02d}" for i in range(1, 12)] + ["NX2U1_autumn", "NX2U1_tot_avg", "Einh"]
    medias = ["rainfall_spells_summer", "frost_depth_feb", "rainfall_t5_spells", "rainfall_longest_spell"]
    sidx = gmd.sindex
    filas = []
    for _, reg in pr.iterrows():
        g = reg.geometry
        area = g.area
        cand = gmd.iloc[sidx.query(g, predicate="intersects")]
        inter = cand.geometry.intersection(g)
        t = pd.DataFrame({"AGS": cand["AGS"].values, "new_area": inter.area.values, "area": cand["area"].values})
        t["gem_area_share"] = t.new_area / t.area
        t["area_share"] = t.new_area / area
        t = t.groupby("AGS", as_index=False)[["gem_area_share", "area_share"]].agg(lambda x: min(x.sum(), 1.0))
        t["area_share"] = t["area_share"] / t["area_share"].sum()
        m = d[d.AGS.isin(t.AGS)].merge(t, on="AGS")
        sel = m.gem_area_share > 0.95
        if not sel.any():
            continue
        s = m[sel].groupby("Jahr")[suma].sum()
        for v in medias:
            m[v] = m[v] * m["area_share"]
        mm = m.groupby("Jahr")[medias].sum(min_count=1)
        o = s.join(mm, how="inner").reset_index()
        o["SN_ROR"] = int(reg["SN_ROR"])
        o["ROR"] = reg["ROR"]
        filas.append(o)
    am = pd.concat(filas, ignore_index=True)
    am["Jahr"] = am["Jahr"] + 1  # oferta y clima son de t-1
    ctr = leer_rds("control_variables_panel_pr.RDS")
    return am.merge(ctr, on=["SN_ROR", "Jahr"])


# ---------------------------------------------------------------- 2. indice hedonico por PR
def indices_hedonicos():
    cols = ["Jahr", "Baujahr", "Flaeche", "Typ", "Kaltmiete", "Fussbodenheizung", "Parkett", "Aufzug", "EBK",
            "GaesteWC", "BalkonTerrasse", "Gartenmit", "Ausstattung", "SN_ROR", "SN_AMR"]
    y = leer_rds("rent_data.RDS", cols)
    y = y[y.SN_ROR.notna() & y.SN_AMR.notna()].drop(columns="SN_AMR")
    y["SN_ROR"] = y["SN_ROR"].astype(str).astype(int)
    y["Baujahr_NA"] = y.Baujahr.isna().astype(float)
    y["Baujahr"] = y.Baujahr.fillna(0.0)
    y["lr"] = np.log(y.Kaltmiete / y.Flaeche)
    y["lf"] = np.log(y.Flaeche)
    y["Jahr"] = y.Jahr.astype(int)
    out = []
    ctrl = ["lf", "Baujahr_NA", "Fussbodenheizung", "Parkett", "Aufzug", "EBK", "GaesteWC", "BalkonTerrasse", "Gartenmit"]
    for sn, g in y.groupby("SN_ROR"):
        if len(g) <= 100:
            continue
        g = g.dropna(subset=ctrl + ["lr", "Typ", "Ausstattung", "Jahr"])
        g = g[np.isfinite(g.lr)]
        # poly(Baujahr, 2) ortogonal: mismo subespacio que (Baujahr, Baujahr^2); el coeficiente de ano es identico
        bj = (g.Baujahr - 1900.0) / 100.0
        X = [np.ones(len(g))] + [g[c].values.astype(float) for c in ctrl] + [bj.values, bj.values ** 2]
        nombres = ["const"] + ctrl + ["bj", "bj2"]
        for a in range(2012, 2019):
            X.append((g.Jahr.values == a).astype(float)); nombres.append(f"J{a}")
        for v in ("Typ", "Ausstattung"):
            for lev in sorted(g[v].unique())[1:]:
                X.append((g[v].values == lev).astype(float)); nombres.append(f"{v}{lev}")
        X = np.column_stack(X)
        keep = X.std(axis=0) > 0
        keep[0] = True
        # columnas sin variacion (p. ej. ano ausente) se eliminan; su indice queda NaN
        Xk = X[:, keep]
        nk = [n for n, k in zip(nombres, keep) if k]
        beta, *_ = np.linalg.lstsq(Xk, g.lr.values, rcond=None)
        co = dict(zip(nk, beta))
        for a in range(2011, 2019):
            out.append({"SN_ROR": sn, "Jahr": a, "Index": 0.0 if a == 2011 else co.get(f"J{a}", np.nan)})
    return pd.DataFrame(out)


# ---------------------------------------------------------------- 3. IV
def iv_fe(df, controles, etiquetas):
    """2SLS con efectos fijos de ano y PR (variables ficticias), error agrupado por PR (SN_ROR)."""
    from linearmodels.iv import IV2SLS
    d = df.dropna(subset=["Index", "x", "z"] + controles).copy()
    F = pd.get_dummies(d["Jahr"].astype(str), prefix="y", drop_first=True, dtype=float)
    P = pd.get_dummies(d["SN_ROR"].astype(str), prefix="p", drop_first=True, dtype=float)
    exog = pd.concat([pd.Series(1.0, index=d.index, name="const"), d[controles], F, P], axis=1)
    res = {}
    for dif, nombre in ((False, "sin_ajuste_muestra_pequena"), (True, "con_ajuste_gl")):
        m = IV2SLS(d["Index"], exog, d[["x"]], d[["z"]]).fit(cov_type="clustered", clusters=d["SN_ROR"], debiased=dif)
        res[nombre] = m
    m0 = res["sin_ajuste_muestra_pequena"]
    # primera etapa
    from linearmodels.iv import IV2SLS as _I
    fs = _I(d["x"], exog.join(d[["z"]]), None, None).fit(cov_type="clustered", clusters=d["SN_ROR"])
    tz = float(fs.params["z"] / fs.std_errors["z"])
    out = {
        "N": int(len(d)), "PRs": int(d.SN_ROR.nunique()),
        "b": float(m0.params["x"]), "se": float(m0.std_errors["x"]),
        "se_gl": float(res["con_ajuste_gl"].std_errors["x"]),
        "ic95": [float(m0.params["x"] - 1.96 * m0.std_errors["x"]), float(m0.params["x"] + 1.96 * m0.std_errors["x"])],
        "F_cluster_1a_etapa": tz ** 2,
        "F_cluster_1a_etapa_gl": float((fs.params["z"] / (fs.std_errors["z"] * np.sqrt(len(d) / (len(d) - exog.shape[1] - 1) * (d.SN_ROR.nunique() / (d.SN_ROR.nunique() - 1)))))) ** 2,
        "fs_b": float(fs.params["z"]), "fs_se": float(fs.std_errors["z"]),
        "ctrl": {etiquetas[c]: (float(m0.params[c]), float(m0.std_errors[c])) for c in controles},
    }
    try:
        out["F_kp_linearmodels"] = float(m0.first_stage.diagnostics.loc["x", "f.stat"])
    except Exception:
        out["F_kp_linearmodels"] = None
    return out


def veredicto(b, se, pb, pse):
    dif = b - pb
    rel = abs(dif) / abs(pb)
    redondeo = round(b, 3) == pb
    dentro = abs(dif) < 1.96 * pse
    if redondeo or (rel < 0.05 and dentro):
        return "coincide", dif, rel
    return "difiere", dif, rel


def main():
    SAL.mkdir(parents=True, exist_ok=True)
    pan = panel_pr()
    idx = indices_hedonicos()
    ror = idx.merge(pan, on=["SN_ROR", "Jahr"])
    ror["x"] = ror["NX2U1_autumn"] / ror["NX2U1_tot_avg"]
    ror["z"] = ror["rainfall_spells_summer"]
    ror["log_empleo"] = np.log(ror["employment_lag"])
    ror["log_paro"] = np.log(ror["unemprate_lag"])
    ror["estudiantes"] = ror["students_per1000_lag"]
    ror = ror.replace([np.inf, -np.inf], np.nan)
    etiq = {"log_empleo": "log_empleo", "log_paro": "log_paro", "estudiantes": "estudiantes"}
    espec = {1: ["log_empleo"], 2: ["log_empleo", "log_paro"], 3: ["log_empleo", "estudiantes", "log_paro"]}
    filas, res = [], {}
    for k, ctrl in espec.items():
        r = iv_fe(ror, ctrl, etiq)
        res[k] = r
        p = PUBLICADO[k]
        v, dif, rel = veredicto(r["b"], r["se"], p["b"], p["se"])
        r["veredicto"], r["dif_abs"], r["dif_rel"] = v, dif, rel
        filas.append({"columna": k, "parametro": "oferta_nueva_oct_dic (IV)", "publicado": p["b"], "se_publicado": p["se"],
                      "reproducido": r["b"], "se_reproducido": r["se"], "se_reproducido_ajuste_gl": r["se_gl"],
                      "dif_abs": dif, "dif_rel": rel, "veredicto": v, "N": r["N"], "PRs": r["PRs"],
                      "F_publicado": p["kp"], "F_reproducido_cluster": r["F_cluster_1a_etapa"], "tabla_pagina": "Tabla 3A, p. 18 del PDF"})
        for c, (pb, pse) in p["ctrl"].items():
            b, se = r["ctrl"][c]
            filas.append({"columna": k, "parametro": c, "publicado": pb, "se_publicado": pse, "reproducido": b,
                          "se_reproducido": se, "dif_abs": b - pb, "dif_rel": abs(b - pb) / abs(pb),
                          "veredicto": veredicto(b, se, pb, pse)[0], "N": r["N"], "PRs": r["PRs"], "tabla_pagina": "Tabla 3A, p. 18 del PDF"})
        filas.append({"columna": k, "parametro": "primera_etapa_lluvia", "publicado": p["fs"][0], "se_publicado": p["fs"][1],
                      "reproducido": r["fs_b"], "se_reproducido": r["fs_se"], "dif_abs": r["fs_b"] - p["fs"][0],
                      "dif_rel": abs(r["fs_b"] - p["fs"][0]) / abs(p["fs"][0]), "veredicto": "",
                      "N": r["N"], "PRs": r["PRs"], "tabla_pagina": "Tabla 3B, p. 18 del PDF"})
    tabla = pd.DataFrame(filas)
    tabla.to_csv(SAL / "tabla.csv", index=False, float_format="%.5f")

    r3 = res[3]
    ver = [res[k]["veredicto"] for k in res]
    resumen = ("coincide" if all(v == "coincide" for v in ver) else
               "difiere (ver informe)")
    json.dump({
        "rama": "v18-reproduccion", "pregunta": CLAVE, "capa": "C4",
        "datos": "paquete de replicacion Mense (2025), Harvard Dataverse doi:10.7910/DVN/LWRXA9 (CC0); Alemania, 94 PR, 2011-2018",
        "N": r3["N"],
        "metodo": "IV-2SLS en panel con efectos fijos de PR y ano, error agrupado por PR; instrumento: duracion media de rachas de lluvia jul-sep (t-1); indice hedonico de alquiler por PR; columna 3 de la tabla 3",
        "estimacion": round(r3["b"], 4),
        "ic95": [round(x, 4) for x in r3["ic95"]],
        "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO",
        "diagnosticos": {"F_1a_etapa_cluster": {k: round(res[k]["F_cluster_1a_etapa"], 1) for k in res},
                         "F_KP_publicado": {k: PUBLICADO[k]["kp"] for k in res},
                         "estimaciones": {k: {"b": round(res[k]["b"], 4), "se": round(res[k]["se"], 4),
                                              "publicado": PUBLICADO[k]["b"], "se_publicado": PUBLICADO[k]["se"],
                                              "veredicto": res[k]["veredicto"]} for k in res}},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": f"Veredicto: {resumen}. Reproduccion del estudio original con sus datos; no usa datos del proyecto. Elasticidad oferta nueva anual -> log alquiler, Alemania.",
    }, open(SAL / "resultado.json", "w"), ensure_ascii=False, indent=2)

    # informe
    L = []
    L.append("# Reproduccion de Mense (2025), tabla 3 (efecto de la oferta nueva sobre el alquiler medio)\n")
    L.append("**Reproduccion del estudio original con sus datos; no usa datos del proyecto.**\n")
    L.append("Estudio: Mense, A. (2025), The Impact of New Housing Supply on the Distribution of Rents, JPE Macroeconomics 3(1), doi 10.1086/733977. "
             "Paquete: Harvard Dataverse doi 10.7910/DVN/LWRXA9 (CC0 1.0). Capa C4 (reproduccion; no promueve de capa).\n")
    L.append("## Especificacion y decisiones de traduccion (R a Python)\n")
    L.append("- No hay R. Se traduce `reduced_form_replication.R` (secciones 1.2, 2.2 y 3.1.1) a Python. Se instalo `pyreadr` (no estaba) para leer los .RDS. "
             "Los shapefiles se leen dentro de los .zip, sin descomprimir.")
    L.append("- Variable dependiente: indice hedonico de alquiler por region de ordenacion (PR) y ano, base 2011: regresion por PR de log(alquiler/m2) sobre "
             "log(superficie), polinomio de segundo grado del ano de construccion, indicador de ano de construccion ausente, calefaccion de suelo, parquet, ascensor, cocina equipada, "
             "WC de invitados, balcon/terraza, jardin, ano (ficticias) y efectos fijos de tipo y equipamiento; solo PR con mas de 100 anuncios. "
             "`poly(Baujahr,2)` ortogonal de R se sustituye por un polinomio bruto reescalado (mismo subespacio, mismos coeficientes de ano). "
             "Las ficticias absorbidas se construyen explicitamente (lstsq) en lugar de la absorcion de `lfe`.")
    L.append("- Oferta y clima: agregacion de municipios a PR por interseccion de poligonos (`sf::st_intersection` sustituido por shapely/geopandas): "
             "se suma la oferta de municipios con mas del 95 % de su area dentro de la PR; el clima se pondera por la cuota de area de la PR. Se desplaza un ano (t-1).")
    L.append("- Endogena: unidades terminadas oct-dic de t-1 / media anual de terminaciones. Instrumento: duracion media de rachas de lluvia jul-sep de t-1. "
             "Controles: log empleo (t-1), log paro (t-1), estudiantes por 1.000 hab. (t-1). Efectos fijos de ano y PR (ficticias). "
             "Error agrupado por PR. El original usa `lfe::felm` con `robust=T`; aqui `linearmodels.IV2SLS` agrupado, sin correccion de muestra pequena (principal) y con ella (columna `se_reproducido_ajuste_gl`).")
    L.append("- El F de Kleibergen-Paap del original es el F de instrumentos de la primera etapa agrupada; aqui se aproxima con el cuadrado del estadistico t del instrumento (un solo instrumento, error agrupado).\n")
    L.append("## Comparacion con la tabla 3A (p. 18)\n")
    L.append("| col. | parametro | publicado (EE) | reproducido (EE) | dif. abs. | dif. rel. | veredicto |\n|---|---|---|---|---|---|---|")
    for _, f in tabla.iterrows():
        if f.parametro.startswith("primera"):
            continue
        L.append(f"| {int(f.columna)} | {f.parametro} | {f.publicado:.3f} ({f.se_publicado:.3f}) | {f.reproducido:.3f} ({f.se_reproducido:.3f}) | {f.dif_abs:+.3f} | {100*f.dif_rel:.1f} % | {f.veredicto} |")
    L.append("\n## Diagnosticos\n")
    L.append("| col. | N (pub. 752) | PR (pub. 94) | F KP publicado | F 1a etapa agrupada | coef. 1a etapa (pub. -0,009/-0,010) |\n|---|---|---|---|---|---|")
    for k in res:
        r = res[k]
        L.append(f"| {k} | {r['N']} | {r['PRs']} | {PUBLICADO[k]['kp']} | {r['F_cluster_1a_etapa']:.1f} | {r['fs_b']:.3f} ({r['fs_se']:.3f}) |")
    L.append("\n## Veredicto\n")
    L.append(f"Columna 1: {res[1]['veredicto']}; columna 2: {res[2]['veredicto']}; columna 3: {res[3]['veredicto']}. Resumen: {resumen}.\n")
    L.append("Lectura: elasticidad de corto plazo del alquiler medio a la oferta nueva anual (Alemania, 2011-2018). No es evidencia para Espana; la validez externa se evalua en la fase 3.\n")
    (SAL / "informe.md").write_text("\n".join(L), encoding="utf-8")
    print(tabla.to_string())


if __name__ == "__main__":
    sys.exit(main())
