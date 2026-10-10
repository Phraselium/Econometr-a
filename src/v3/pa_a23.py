"""A2 (demanda latente) y A3 (desajuste de la vacancia)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import pa_data as pdat

TAMANO = (1.5, 2.0)


def a2(reg) -> tuple[pd.DataFrame, pd.DataFrame]:
    e = pd.read_csv(pdat.V3 / "eurostat_emancipacion_tenencia_v3.csv")
    e = e[e.fuente.str.contains("lvps08") & e.serie.str.contains("Y25-34_T_con_padres")]
    es = e[e.codigo == "ES"].set_index("periodo").valor
    ue = e[e.codigo == "EU27_2020"].set_index("periodo").valor
    epa = pdat.epa_parentesco()
    filas = []
    for y in range(2008, 2026):
        filas.append({"anio": y, "tasa_eurostat_ecv_ES": es.get(y, np.nan), "tasa_eurostat_ecv_UE27": ue.get(y, np.nan),
                      "tasa_epa_hijo_persona_ref_ES": epa.tasa_epa.get(y, np.nan), "pob_25_34_epa": epa.pob_25_34.get(y, np.nan)})
    serie = pd.DataFrame(filas)
    ult = int(min(es.index.max(), epa.index.max()))
    pob = float(epa.pob_25_34[ult])
    fuentes = {"Eurostat ilc_lvps08 (ECV)": float(es[ult]), "EPA 65944 (hijo/a de la persona de referencia)": float(epa.tasa_epa[ult])}
    refs = {
        "Eurostat ilc_lvps08 (ECV)": {"España 2008": float(es[2008]), f"UE-27 {ult}": float(ue[ult])},
        "EPA 65944 (hijo/a de la persona de referencia)": {"España 2008": float(epa.tasa_epa[2008])},
    }
    res = []
    for fn, obs in fuentes.items():
        for rn, ref in refs[fn].items():
            for tam in (TAMANO[0], 1.75, TAMANO[1]):
                hog = (obs - ref) / 100.0 * pob / tam
                res.append({"anio": ult, "fuente": fn, "tasa_observada": obs, "referencia": rn, "tasa_referencia": ref,
                            "pob_25_34": pob, "personas_por_hogar_joven": tam, "hogares_implicitos": hog,
                            "viviendas_implicitas": hog})
                reg.log("A2", f"A2_{fn[:8]}_{rn}_{tam}", "(tasa − ref) × pob25-34 / tamaño", ult, ult, 1, np.nan, np.nan,
                        np.nan, np.nan, hog, np.nan, f"{fn}; ref {rn}; tamaño {tam}")
    return serie, pd.DataFrame(res)


def _muni_base() -> pd.DataFrame:
    v = pdat.vacias2021()
    v = v[~v.index.str.endswith("999")].copy()
    c = pdat.censo2021_municipios()
    v = v.join(c[["V_PRINCIPAL"]])
    sec = pdat.censo2021_secciones()
    sec["cod"] = sec.index.str[:5]
    mun = sec.groupby("cod")[["personas", "hogares"]].sum()
    v = v.join(mun)
    pm = pdat.panel("panel_muni_a")
    pm["cod"] = pm.cod_muni.astype(int).astype(str).str.zfill(5)
    p = pm.set_index(["cod", "anio"])
    def g(col, y):
        s = p[col].xs(y, level="anio")
        return s[~s.index.duplicated()]
    v["ln_tasado_15_21"] = np.log(g("p_tasado", 2021)) - np.log(g("p_tasado", 2015))
    v["ln_tasado_21_25"] = np.log(g("p_tasado", 2025)) - np.log(g("p_tasado", 2021))
    v["ln_alq_15_21"] = np.log(g("serpavi_mediana_vc", 2021)) - np.log(g("serpavi_mediana_vc", 2015))
    zt = g("zona_tensionada", 2024)
    v["zona_tensionada"] = zt
    v["vut_2021"] = g("vut_viviendas", 2021)
    cat = pdat.catastro()
    cat = cat[cat.periodo == 2022].set_index("codigo").uu_res
    cat12 = pdat.catastro()
    cat12 = cat12[cat12.periodo == 2012].set_index("codigo").uu_res
    v["uu_res_2021"] = cat
    v["d_uu_res_12_21"] = cat - cat12
    v["vacia_catastro"] = v.uu_res_2021 - v.V_PRINCIPAL - v.vut_2021.fillna(0)
    c11 = pdat.censo2011_municipios()
    c11.index = [pdat.clave(str(i).split("(")[0]) for i in c11.index]
    dup = c11.index.duplicated(keep=False)
    c11 = c11[~dup]
    v["clave"] = [pdat.clave(str(n).split("(")[0]) for n in v.nombre]
    vk = v.clave.duplicated(keep=False)
    v["hog11"] = np.where(~vk, v.clave.map(c11["Vivienda principal"]), np.nan)
    v["hogares_nuevos_11_21"] = v.V_PRINCIPAL - v.hog11
    return v


def _terciles(x: pd.Series) -> pd.Series:
    q = x.rank(method="first")
    return pd.qcut(q, 3, labels=["bajo", "medio", "alto"])


def a3(reg) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    v = _muni_base()
    nac = pdat.vacias2021_nacional()
    medidas = {"Censo 2021: vacías": "vacias", "Censo 2021: vacías + uso esporádico": "vac_esp",
               "Catastro − hogares − VUT": "vacia_catastro"}
    v["vac_esp"] = v.vacias + v.esporadico
    presiones = {"Δ ln valor tasado 2015-2021": "ln_tasado_15_21", "Δ ln valor tasado 2021-2025": "ln_tasado_21_25",
                 "Δ ln alquiler SERPAVI 2015-2021": "ln_alq_15_21"}
    filas = []
    for pn, pc in presiones.items():
        for mu in (False, True):
            base = v[v[pc].notna()]
            if mu:
                base = base[base.personas > 50000]
            if len(base) < 30:
                continue
            base = base.assign(t=_terciles(base[pc]))
            for mn, mc in medidas.items():
                bm = base[base[mc].notna()]
                tot = bm[mc].sum()
                den = {"vacias": nac["vacias"], "vac_esp": nac["vacias"] + nac["esporadico"]}.get(mc, np.nan)
                for t, g in bm.groupby("t", observed=True):
                    nuevos = g.hogares_nuevos_11_21
                    gn = g[nuevos.notna()]
                    por100 = 100 * gn[mc].sum() / gn.hogares_nuevos_11_21.sum() if gn.hogares_nuevos_11_21.sum() > 0 else np.nan
                    filas.append({"presion": pn, "muestra": ">50.000 hab." if mu else "todos con dato", "medida_vacia": mn,
                                  "tercil": t, "n_municipios": len(g), "vacias": g[mc].sum(),
                                  "pct_vacias_de_la_muestra": 100 * g[mc].sum() / tot,
                                  "pct_vacias_del_pais": 100 * g[mc].sum() / den,
                                  "vacias_por_100_viviendas": 100 * g[mc].sum() / g.total.sum(),
                                  "vacias_por_100_hogares_nuevos_11_21": por100,
                                  "n_con_hogares_nuevos": int(nuevos.notna().sum())})
                    reg.log("A3", f"A3_{pn[:20]}_{mn[:14]}_{t}_{int(mu)}", "reparto de vacías por tercil de presión",
                            2015, 2021, len(g), np.nan, np.nan, np.nan, np.nan, g[mc].sum(), np.nan, mn)
    # zona tensionada (2024)
    zt = v[v.zona_tensionada.notna()].copy()
    zt["zt"] = np.where(zt.zona_tensionada <= 0, "sin zona", np.where(zt.zona_tensionada >= 1, "toda en zona", "parcial"))
    for mn, mc in medidas.items():
        den = {"vacias": nac["vacias"], "vac_esp": nac["vacias"] + nac["esporadico"]}.get(mc, np.nan)
        for z, g in zt.groupby("zt"):
            filas.append({"presion": "Zona tensionada (2024)", "muestra": "todos con dato", "medida_vacia": mn,
                          "tercil": z, "n_municipios": len(g), "vacias": g[mc].sum(),
                          "pct_vacias_de_la_muestra": 100 * g[mc].sum() / zt[mc].sum(),
                          "pct_vacias_del_pais": 100 * g[mc].sum() / den,
                          "vacias_por_100_viviendas": 100 * g[mc].sum() / g.total.sum(),
                          "vacias_por_100_hogares_nuevos_11_21": np.nan, "n_con_hogares_nuevos": 0})
    t = pd.DataFrame(filas)
    cob = {"n_municipios_publicados": int(len(v)), "vacias_total_pais": nac["vacias"], "esporadico_total_pais": nac["esporadico"],
           "vacias_en_municipios_publicados": float(v.vacias.sum()), "vacias_total_nacional_censo2011": pdat.censo2011_nacional()["vacia"],
           "n_municipios_nombre_unico_2011": int(v.hog11.notna().sum()), "n_ptasado": int(v.ln_tasado_15_21.notna().sum()),
           "n_serpavi": int(v.ln_alq_15_21.notna().sum())}
    return v, t, cob
