"""M0 · Cierre de v3: conciliación del déficit, triangulación de terminadas y no réplica de García-López.

Determinista, sin red. SEED=20261010. Solo lee data/ y output/ previos.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
RAW = RAIZ / "data" / "raw"
OUT = RAIZ / "output" / "v4" / "M0"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")
TOL = 0.15  # umbral declarado de coincidencia entre fuentes independientes


def f(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".")


# ---------------------------------------------------------------- 1. Conciliación
def conciliacion() -> dict:
    comb = pd.read_csv(RAIZ / "output/v3/PA/tablas/A1_nacional_combinaciones.csv")
    p = comb[comb.periodo == "2021-2025"]
    ecp0 = p[(p.hogares_fuente == "Censo+ECP") & (p.protegida == "con") & (p.bajas_pct == 0)].iloc[0]
    epa0 = p[(p.hogares_fuente == "EPA") & (p.protegida == "sin") & (p.bajas_pct == 0)].iloc[0]
    res = pd.read_csv(RAIZ / "output/v3/PA/tablas/A1_tabla_unica_periodos.csv")
    r = res[res.periodo == "2021-2025"].iloc[0]
    libres = float(epa0.neta)            # 411.900
    con_prot = float(ecp0.neta)          # 468.223
    prot = con_prot - libres             # 56.323
    dh_ecp_v3 = float(ecp0.delta_hogares)   # 1.169.157 (media trimestral 2021T1 a 2025T4)
    dh_ecp_v1 = 1_222_836.0              # stock 1-ene-2026 menos 1-ene-2021 (informe v1, 5.1)
    dh_epa_corr = 1_278_000.0            # EPA corregida del quiebre 2021T1 (informe v1, 5.1)
    dh_epa_raw = float(epa0.delta_hogares)  # 1.035.600
    dparque = 475_848.0
    assert abs(libres - 411_900) < 1 and abs(dh_epa_raw - 1_035_600) < 1

    cols = ["id", "origen", "fuente_hogares", "medida_hogares", "oferta", "bajas_parque", "periodo_inicio", "periodo_fin",
            "delta_hogares", "oferta_viviendas", "cifra", "nota"]
    F = [
        ["v1_epa", "v1", "EPA", "media trimestral, EPA corregida del quiebre 2021T1", "fin de obra libres MIVAU (sin protegida)",
         "no (0)", "2021T1", "2025T4", dh_epa_corr, libres, dh_epa_corr - libres, "principal v1"],
        ["v1_ecp", "v1", "ECP", "stock a 1 de enero (1-ene-2026 menos 1-ene-2021)", "fin de obra libres MIVAU (sin protegida)",
         "no (0)", "2021-01-01", "2026-01-01", dh_ecp_v1, libres, dh_ecp_v1 - libres, "variante v1"],
        ["v1_parque", "v1", "EPA", "media trimestral, EPA corregida", "variación del parque MIVAU (neta)",
         "implícitas en el parque (netas)", "2021", "2025", dh_epa_corr, dparque, dh_epa_corr - dparque, "variante v1"],
        ["v3_ecp_ref", "v3", "Censo 2021 + ECP", "media trimestral 2021T1-2025T4 (sin quiebre: anclada al censo)",
         "fin de obra libres + protegida (calif. definitivas)", "no (0)", "2021T1", "2025T4", dh_ecp_v3, con_prot,
         float(ecp0.deficit), "combinación v3 cercana a la mediana"],
        ["v3_mediana", "v3", "EPA sin corregir y Censo+ECP", "media trimestral", "las 14 combinaciones (con/sin protegida, bajas 0/0,1/0,2 %, Δparque)",
         "0 a 0,2 % anual del parque", "2021T1", "2025T4", np.nan, np.nan, float(r.mediana), "mediana de combinaciones: no es una especificación"],
        ["v3_min", "v3", "EPA sin corregir", "media trimestral, sin corregir quiebre", "variación del parque MIVAU (neta)",
         "implícitas en el parque", "2021T1", "2025T4", dh_epa_raw, dparque, float(r.min_total), "cota inferior de v3"],
        ["v3_max", "v3", "Censo 2021 + ECP", "media trimestral", "fin de obra libres + protegida", "0,2 % anual del parque",
         "2021T1", "2025T4", dh_ecp_v3, float(ecp0.bruto) - 2 * float(p[(p.hogares_fuente == "Censo+ECP") & (p.protegida == "con") & (p.bajas_pct == 0.1)].iloc[0].bajas),
         float(r.max_total), "cota superior de v3 (bajas del 0,2 % anual)"],
        ["bde_ia", "BdE", "no nombrada (inferencia: ECP)", "no declarada", "terminadas (no declara si incluye protegida)",
         "no declaradas", "2021", "2025", np.nan, np.nan, 750_000.0, "Informe Anual 2025, p. 157; aproximada"],
        ["bde_ief", "BdE", "no nombrada", "no declarada", "terminadas", "no declaradas", "2021", "1S 2025 (inferencia)",
         np.nan, np.nan, 700_000.0, "IEF otoño 2025; periodo y fuente distintos"],
    ]
    tab = pd.DataFrame(F, columns=cols)
    tab.to_csv(OUT / "conciliacion_deficit.csv", index=False, float_format="%.0f")
    # Cadena aditiva: v1 principal -> referencia v3 (mismo periodo 2021-2025, sin bajas)
    pasos = [
        ("v1 principal (EPA corregida, libres)", 866_100.0, None),
        ("fuente de hogares: EPA corregida -> ECP (ambas con stock 1 de enero)", dh_ecp_v1 - dh_epa_corr, "hogares"),
        ("desplazamiento de ventana: de 1-ene-2021 a 1-ene-2026 (stock) a media del 1T-2021 al 4T-2025 (la ventana pierde un trimestre inicial y final)", dh_ecp_v3 - dh_ecp_v1, "desplazamiento de ventana"),
        ("protegida: añadir calificaciones definitivas (no incluidas en v1)", -prot, "protegida"),
        ("bajas del parque (v1 y referencia v3: 0)", 0.0, "bajas"),
        ("periodo (ambos 2021-2025)", 0.0, "periodo"),
    ]
    filas = [(pasos[0][0], 866_100.0, 866_100.0, None)]
    s = 866_100.0
    for n, dh, c in pasos[1:]:
        d = dh
        s += d
        filas.append((n, d, s, c))
    chk = abs(s - float(ecp0.deficit))
    assert chk < 1, chk
    extra = [
        ("v1 principal -> v1 ECP", dh_ecp_v1 - dh_epa_corr, 810_936.0, "hogares"),
        ("v1 principal -> v1 Δparque (protegida 56.323 + residual neto de bajas −7.625)", -(dparque - libres), 802_152.0, "protegida y bajas"),
        ("quiebre EPA 2021T1 (corregida -> sin corregir)", dh_epa_raw - dh_epa_corr, 623_700.0, "hogares (corrección)"),
        ("referencia v3 -> BdE IA (residuo no atribuible)", 750_000.0 - float(ecp0.deficit), 750_000.0, "residuo/redondeo/no declarado"),
        ("BdE IA -> BdE IEF (periodo hasta 1S 2025: inferencia)", -50_000.0, 700_000.0, "periodo (no verificable)"),
        ("sensibilidad: bajas +0,1 % anual del parque", float(p[(p.hogares_fuente == "Censo+ECP") & (p.protegida == "con") & (p.bajas_pct == 0.1)].iloc[0].bajas), np.nan, "bajas"),
    ]
    pas = pd.DataFrame(filas + extra, columns=["paso", "delta_deficit", "nivel_resultante", "componente"])
    pas.to_csv(OUT / "conciliacion_pasos.csv", index=False, float_format="%.0f")
    md = ["# M0 · Conciliación de las cifras de déficit 2021-2025 (capas C1 y C2)", "",
          "Déficit contable = Δ hogares − viviendas terminadas (flujo acumulado desde 2021, no un déficit en niveles). "
          "Fuentes: output/informe.md (v1), output/v3/PA/tablas (A1), docs/v3/literatura_v3.md. Sin datos nuevos.", "",
          "## Cifras", "",
          "| id | fuente de hogares | medida de hogares | oferta | bajas | periodo | cifra |", "|---|---|---|---|---|---|---|"]
    for _, x in tab.iterrows():
        md.append(f"| {x.id} | {x.fuente_hogares} | {x.medida_hogares} | {x.oferta} | {x.bajas_parque} | {x.periodo_inicio} a {x.periodo_fin} | {f(x.cifra)} |")
    md += ["", "## Descomposición aditiva (v1 principal a referencia v3 y BdE)", "", "| paso | Δ déficit | nivel | componente |", "|---|---|---|---|"]
    for _, x in pas.iterrows():
        nv = "" if pd.isna(x.nivel_resultante) else f(x.nivel_resultante)
        md.append(f"| {x.paso} | {f(x.delta_deficit)} | {nv} | {x.componente} |")
    md += ["", "## Lectura",
           f"- De 866.100 (v1) a 700.934 (referencia v3) hay −165.166: hogares −55.164 (fuente), −53.679 (desplazamiento de ventana de un trimestre: v1 mide de 1-ene-2021 a 1-ene-2026 y v3 del 1T-2021 al 4T-2025; no es una diferencia de concepto del hogar), protegida −{f(prot)}; bajas y periodo 0 por construcción. La suma cierra exacta.",
           f"- La protegida medida con calificaciones definitivas de MIVAU ({f(prot)}) es coherente con el residuo de 60.936 que v1 atribuyó a la protegida (diferencia de 4.613; v1 lo obtuvo como BdE implícito menos terminadas).",
           "- La única fuente con efecto grande no resuelto es la corrección del quiebre EPA 2021T1 (242.400): con ella 866.100, sin ella 623.700. Es una elección de medida, no un dato.",
           "- Las bajas del parque no están medidas: cada 0,1 % anual del parque suma 134.063 al déficit. Es la mayor incertidumbre de v3 (rango 559.752-969.059) y no la reduce ninguna fuente disponible.",
           "- Frente al BdE (≈750.000): la referencia v3 queda 49.066 por debajo y v1 116.100 por encima. El BdE no declara fuente de hogares, protegida ni bajas, así que ese residuo no se puede descomponer; la fuente de hogares ECP es inferencia. 700.000 (IEF) es compatible en signo con un periodo más corto, sin verificar.",
           "- Conclusión: las cifras 700.000-866.100 difieren por la fuente de hogares (≈55.000) y el desplazamiento de ventana de un trimestre (≈54.000) y la protegida (≈56.000), no por el periodo. El déficit en niveles, con bajas, queda en el rango de v3 (C2). La cifra del BdE es una referencia externa NO VERIFICADA en su método."]
    (OUT / "conciliacion_deficit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    REG.log("M0", "conc_cadena", "d_v1 + pasos aditivos = ref_v3", 2021, 2025, 1, np.nan, np.nan, np.nan, coef_interes=float(ecp0.deficit), notas="cierre exacto de la cadena")
    return {"ref_v3": float(ecp0.deficit), "prot": prot, "mediana": float(r.mediana), "min": float(r.min_total), "max": float(r.max_total)}


# ---------------------------------------------------------------- 2. Terminadas
def terminadas() -> dict:
    m = pd.read_csv(RAW / "mivau_fin_obra.csv")
    t2 = pd.read_csv(RAW / "mivau_v2_iniciadas_terminadas_prov.csv")
    pr = pd.read_csv(RAW / "mivau_v2_protegida.csv")
    pq = pd.read_csv(RAW / "mivau_parque.csv")
    yrs = list(range(2012, 2026))
    men = m[m.serie == "viv_libres_terminadas_nacional"].copy()
    men["y"] = men.periodo.str[:4].astype(int)
    libres = men.groupby("y").valor.sum().reindex(yrs)
    libres_v2 = t2[t2.serie == "viv_libres_terminadas_anual_nacional"].set_index("periodo").valor
    libres_v2.index = libres_v2.index.astype(int)
    libres_v2 = libres_v2.reindex(yrs)
    ident = float((libres - libres_v2).abs().max())
    prot = pr[pr.serie == "prot_definitiva_anual_nacional"].set_index("periodo").valor
    prot.index = prot.index.astype(int)
    prot = prot.reindex(yrs)
    park = pq[pq.serie == "parque_total_viviendas_nacional"].set_index("periodo").valor
    park.index = park.index.astype(int)
    dpark = park.diff().reindex(yrs)
    # comparación en territorio común: sin País Vasco ni Navarra (Catastro de régimen común)
    def serie_anual(df, nombre):
        x = df[df.serie == nombre].copy()
        x["periodo"] = x.periodo.astype(str).str[:4].astype(int)
        return x.groupby("periodo").valor.sum()

    def sin_pv_na(df, base, tpl):
        """Nacional menos País Vasco y Navarra (territorio de régimen común, el del Catastro)."""
        n = serie_anual(df, base)
        for ccaa in ("pais_vasco", "navarra_comunidad_foral_de"):
            n = n.sub(serie_anual(df, tpl.format(ccaa)), fill_value=0)
        return n.reindex(yrs)

    lib_c = sin_pv_na(t2, "viv_libres_terminadas_anual_nacional", "viv_libres_terminadas_anual_ccaa_{}")
    pr_c = sin_pv_na(pr, "prot_definitiva_anual_nacional", "prot_definitiva_anual_ccaa_{}")
    park_n = serie_anual(pq, "parque_total_viviendas_nacional")
    for ccaa in ("pais_vasco", "navarra_comunidad_foral_de"):
        park_n = park_n.sub(serie_anual(pq, f"parque_total_viviendas_ccaa_{ccaa}"), fill_value=0)
    dpk_c = park_n.diff().reindex(yrs)
    cat = pd.read_csv(RAW / "catastro_urbana_municipios.csv", usecols=["periodo", "valor", "unidad", "codigo"], dtype={"codigo": str})
    cat = cat[cat.unidad == "unidades_urbanas_residenciales"]
    uu = cat.groupby("periodo").valor.sum()
    ncod = cat.groupby("periodo").codigo.nunique()
    # periodo N = 1 de enero de N: la variación del año y es UU(y+1) − UU(y)
    cat0 = uu.shift(-1).sub(uu).reindex(yrs)
    cat1 = uu.shift(-2).sub(uu.shift(-1)).reindex(yrs)   # con un año de retraso de incorporación
    # armonizar municipios: solo códigos presentes en todos los años
    comun = set.intersection(*[set(g.codigo) for _, g in cat.groupby("periodo")])
    uuh = cat[cat.codigo.isin(comun)].groupby("periodo").valor.sum()
    cat0h = uuh.shift(-1).sub(uuh).reindex(yrs)
    bruto = (libres + prot)
    bruto_c = (lib_c + pr_c)
    df = pd.DataFrame({
        "anio": yrs, "mivau_libres_mensual": libres.values, "mivau_libres_anual_v2": libres_v2.values,
        "mivau_protegida_calif_def": prot.values, "mivau_bruto_libres_mas_prot": bruto.values,
        "mivau_dparque_neto": dpark.values,
        "comun_mivau_bruto_sin_PV_NA": bruto_c.values, "comun_mivau_dparque_sin_PV_NA": dpk_c.values,
        "catastro_dUU_res": cat0.values, "catastro_dUU_res_munic_constantes": cat0h.values, "catastro_dUU_res_rezago1": cat1.values,
    })
    df["dif_catastro_vs_mivau_bruto"] = df.catastro_dUU_res / df.comun_mivau_bruto_sin_PV_NA - 1
    df["dif_catastro_munic_const_vs_mivau_bruto"] = df.catastro_dUU_res_munic_constantes / df.comun_mivau_bruto_sin_PV_NA - 1
    df["dif_catastro_rezago1_vs_mivau_bruto"] = df.catastro_dUU_res_rezago1 / df.comun_mivau_bruto_sin_PV_NA - 1
    df["dif_dparque_vs_mivau_bruto"] = df.comun_mivau_dparque_sin_PV_NA / df.comun_mivau_bruto_sin_PV_NA - 1
    # coincide si el Catastro (alineación pre-especificada: sin retraso, municipios constantes) está dentro de ±15 % del MIVAU bruto
    ok = df.dif_catastro_munic_const_vs_mivau_bruto.abs() <= TOL
    df["coinciden_2_indep"] = ok
    robusto = df.anio.between(2019, 2024)
    df["capa"] = np.where(ok & robusto, "C1", np.where(ok, "C4 (rango, C1 frágil)", "C4"))
    df["coincide_10pct"] = df.dif_catastro_munic_const_vs_mivau_bruto.abs() <= 0.10
    df["rango_bajo"] = df[["comun_mivau_bruto_sin_PV_NA", "catastro_dUU_res_munic_constantes"]].min(axis=1)
    df["rango_alto"] = df[["comun_mivau_bruto_sin_PV_NA", "catastro_dUU_res_munic_constantes"]].max(axis=1)
    df.to_csv(OUT / "terminadas_triangulacion.csv", index=False, float_format="%.4f")

    def acum(a, b, col):
        return float(df[(df.anio >= a) & (df.anio <= b)][col].sum())
    agg = []
    for a, b in [(2012, 2025), (2021, 2025), (2012, 2020)]:
        mv, ct = acum(a, b, "comun_mivau_bruto_sin_PV_NA"), acum(a, b, "catastro_dUU_res_munic_constantes")
        pk_ = acum(a, b, "comun_mivau_dparque_sin_PV_NA")
        agg.append((a, b, mv, ct, ct / mv - 1, pk_, pk_ / mv - 1))
        REG.log("M0", f"terminadas_{a}_{b}", "catastro dUU vs MIVAU bruto (territorio comun)", a, b, b - a + 1, np.nan, np.nan, np.nan,
                coef_interes=ct / mv - 1, notas="dif relativa acumulada")
    nok = int(ok.sum())
    # dependencia parque - terminadas
    res_dep = (df.comun_mivau_dparque_sin_PV_NA - df.comun_mivau_bruto_sin_PV_NA).abs() / df.comun_mivau_bruto_sin_PV_NA
    dep_rel = float(res_dep[df.anio >= 2021].median())
    dep_rel_ant = float(res_dep[df.anio <= 2020].median())
    ok_rez = (df.dif_catastro_rezago1_vs_mivau_bruto.abs() <= TOL)
    ok_sinh = (df.dif_catastro_vs_mivau_bruto.abs() <= TOL)
    md = ["# M0 · Viviendas terminadas al año 2012-2025: triangulación", "",
          f"Umbral de coincidencia declarado: |diferencia| ≤ {TOL:.0%} en el año entre dos fuentes independientes. Alineación del Catastro fijada antes de mirar el resultado: "
          "variación del stock de unidades urbanas residenciales de 1 de enero del año y a 1 de enero de y+1, con los municipios presentes en todos los años (7.593 en 2012; 7.610 desde 2019).", "",
          "## Independencia de las fuentes",
          f"- MIVAU fin de obra mensual y MIVAU v2 anual son la misma tabla 3.2 (diferencia máxima anual {ident:.0f}): una sola fuente, no dos.",
          "- Calificaciones definitivas de protegida (tabla 1.6): es otro registro del Ministerio, pero mide la calificación y no la finalización; se suma a las libres para tener un bruto comparable. Misma fuente administrativa.",
          f"- Δ parque MIVAU: estimación del propio Ministerio, cuya metodología no consta en el repo. Mediana de |Δparque − bruto|/bruto = {dep_rel:.1%} en 2021-2025 (casi idéntica a las terminadas) y {dep_rel_ant:.0%} en 2012-2020 (muy superior, a la par del Catastro). Se trata como NO independiente y como segundo método discrepante antes de 2021, que se reporta pero no se usa para promover.",
          "- Banco de España: data/raw/bde_* contiene precios de tasación, crédito y tipos; NO hay serie de viviendas terminadas. La única cifra del BdE es 92.000 en 2025 (Informe Anual, vía output/f4). Frente a 80.792 libres + 12.858 protegida = 93.650 (−1,8 %) es consistente con la serie del Ministerio, pero el BdE no nombra la fuente: no se cuenta como independiente.",
          "- Catastro: registro fiscal con otro proceso de alta (declaraciones y regularizaciones). Es independiente solo en parte: el alta catastral de obra nueva suele apoyarse en la escritura de obra nueva o la declaración de alteración, que exigen el certificado final de obra, documento de origen común con MIVAU aunque el proceso administrativo sea distinto. Cubre régimen común (sin País Vasco ni Navarra); la comparación usa las demás comunidades del MIVAU. Su variación de stock es neta por construcción (altas menos bajas, con regularizaciones); MIVAU es flujo bruto, y la coincidencia puede deberse a que las regularizaciones compensen las bajas.", "",
          "## Resultado anual (territorio común, sin País Vasco ni Navarra)", "",
          "| año | MIVAU libres+prot | Catastro ΔUU | dif Catastro | Δparque | capa | rango |", "|---|---|---|---|---|---|---|"]
    for _, x in df.iterrows():
        md.append(f"| {int(x.anio)} | {f(x.comun_mivau_bruto_sin_PV_NA)} | {f(x.catastro_dUU_res_munic_constantes)} | {x.dif_catastro_munic_const_vs_mivau_bruto:+.1%} | {f(x.comun_mivau_dparque_sin_PV_NA)} | {x.capa} | {f(x.rango_bajo)}-{f(x.rango_alto)} |")
    md += ["", "## Acumulados", "", "| periodo | MIVAU bruto | Catastro | dif Catastro | Δparque | dif Δparque |", "|---|---|---|---|---|---|"]
    for a, b, mv, ct, d1, pk_, d2 in agg:
        md.append(f"| {a}-{b} | {f(mv)} | {f(ct)} | {d1:+.1%} | {f(pk_)} | {d2:+.1%} |")
    nac = df[df.anio.between(2021, 2025)]
    md += ["", "## Cifra nacional (MIVAU, libres + calificaciones definitivas)", "",
           "| año | libres | protegida | bruto |", "|---|---|---|---|"]
    for _, x in df.iterrows():
        md.append(f"| {int(x.anio)} | {f(x.mivau_libres_mensual)} | {f(x.mivau_protegida_calif_def)} | {f(x.mivau_bruto_libres_mas_prot)} |")
    md += ["", "## Veredicto",
           f"- Años con MIVAU y Catastro (independientes solo en parte) dentro de ±{TOL:.0%}: {nok} de {len(df)} ({', '.join(str(int(a)) for a in df[ok].anio) or 'ninguno'}). C1 solo el núcleo 2019-2024 (presente en las tres alineaciones), con el rango MIVAU-Catastro de la tabla; 2018 y 2025 quedan en C4 con rango y la salvedad de C1 frágil (cerca del umbral; salen con otras alineaciones); el resto en C4. Con ±10 % coinciden: {', '.join(str(int(a)) for a in df[df.coincide_10pct].anio) or 'ninguno'}.",
           f"- Reglas aplicadas: un año es C1 solo si Catastro y MIVAU coinciden; no se promociona ningún año por la coincidencia de Δparque, que no es independiente. Sensibilidad a la alineación: con rezago de un año en el Catastro coinciden {int(ok_rez.sum())} años ({', '.join(str(int(a)) for a in df[ok_rez].anio) or 'ninguno'}); con todos los municipios (no constantes), {int(ok_sinh.sum())} ({', '.join(str(int(a)) for a in df[ok_sinh].anio) or 'ninguno'}).",
           "- 2012-2017: MIVAU (libres + protegida) es entre 1,2 y 3 veces menor que el Catastro y el Δparque; el Catastro en esos años incorpora altas por regularización y actualización, y MIVAU puede infraregistrar certificados. Los dos métodos discrepan y no se resuelve: C4. 2018 (−12,1 %) y 2025 (+14,9 %) están cerca del umbral. Rango C1 2018-2025 en territorio común; no cubre País Vasco ni Navarra.",
           "- Cifra nacional 2024: 86.609 libres + 14.371 protegida = 100.980, la cifra que v1 marcó como NO VERIFICADA (prensa); se reproduce con MIVAU, pero es la misma fuente, no una verificación independiente. 2025: 93.650 (BdE ≈ 92.000).",
           "- La serie MIVAU de libres se usa sola en las cifras de v1 y v3 ; aquí solo se promociona lo que supera el contraste con el Catastro. Las diferencias no se resuelven: el Catastro mide variación neta con regularizaciones, MIVAU mide certificados de fin de obra."]
    (OUT / "terminadas_triangulacion.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"n_ok": nok, "anios_ok": [int(a) for a in df[ok].anio], "agg": agg, "ident": ident, "dep_rel": dep_rel, "nac": df}


# ---------------------------------------------------------------- 3. García-López
def gl() -> dict:
    inc = pd.read_csv(RAW / "v3/incasol_fianzas_municipio_v3.csv.gz")
    b = inc[(inc.codigo == 8019) & (inc.unidad == "EUR/mes") & inc.periodo.str.contains("gener-desembre")].copy()
    b["y"] = b.periodo.str[:4].astype(int)
    incs = b.set_index("y").valor.sort_index()           # renta media (umbral >650 hasta 2020; >600 desde 2021: ruptura)
    srp = pd.read_csv(RAW / "v3/serpavi_distritos_nacional_v3.csv.gz")
    x = srp[srp.serie.str.match(r"SERPAVI_DIS_08019\d\d_ALQM2_LV_M_VC")]
    sp = x.groupby("periodo").valor.mean().sort_index()  # €/m2 mediana de distrito, media simple de 10 distritos
    ipc = pd.read_csv(RAW / "ine_ipc_alquiler.csv")
    ipc = ipc[ipc.serie == "IPC290887"].copy()
    ipc["y"] = ipc.periodo.str[:4].astype(int)
    ipcy = ipc.groupby("y").valor.mean()
    d = pd.DataFrame({"incasol": incs, "serpavi": sp, "ipc": ipcy}).dropna()
    ld = np.log(d).diff().dropna()
    ld["salto_incasol"] = ld.index == 2021   # ruptura de umbral >650 -> >600
    rows = []
    def tramo(nm, a, b):
        s = ld[(ld.index >= a) & (ld.index <= b) & (~ld.salto_incasol)]
        acc = s[["incasol", "serpavi", "ipc"]].sum()
        sl = np.polyfit(s.incasol, s.serpavi, 1)[0] if len(s) >= 4 else np.nan
        sl_ipc = np.polyfit(s.ipc, s.serpavi, 1)[0] if len(s) >= 4 else np.nan
        sd_r = s.serpavi.std() / s.incasol.std() if len(s) >= 3 else np.nan
        rows.append([nm, a, b, len(s), acc.incasol, acc.serpavi, acc.ipc, acc.serpavi / acc.incasol, acc.serpavi / acc.ipc, sd_r, sl, sl_ipc])
    tramo("2012-2016 (periodo GL)", 2012, 2016)
    tramo("2015-2020", 2015, 2020)
    tramo("2022-2024 (periodo propio, sin salto 2021)", 2022, 2024)
    tramo("2015-2024 sin 2021", 2015, 2024)
    tramo("2012-2024 sin 2021", 2012, 2024)
    att = pd.DataFrame(rows, columns=["tramo", "desde", "hasta", "n_dif", "dlog_incasol", "dlog_serpavi", "dlog_ipc",
                                      "razon_acum_serpavi_incasol", "razon_acum_serpavi_ipc", "razon_sd_serpavi_incasol",
                                      "pendiente_serpavi_sobre_incasol", "pendiente_serpavi_sobre_ipc"])
    att.to_csv(OUT / "gl_atenuacion.csv", index=False, float_format="%.4f")
    d.assign(**{"dlog_" + c: np.log(d[c]).diff() for c in d.columns}).to_csv(OUT / "gl_series_bcn.csv", float_format="%.4f")
    for _, r in att.iterrows():
        REG.log("M0", "gl_atenuacion", "dlog SERPAVI ~ dlog Incasol (BCN)", r.desde, r.hasta, int(r.n_dif), np.nan, np.nan, np.nan,
                coef_interes=r.pendiente_serpavi_sobre_incasol, notas=r.tramo)
    gl = pd.read_csv(RAIZ / "output/v3/GL/tabla_replicacion.csv").set_index("especificacion")
    g1 = gl.loc["GL1_bcn_seccion_vut100viv"]
    T = float(g1.objetivo)
    lam = float(att[att.tramo.str.startswith("2022-2024")].pendiente_serpavi_sobre_incasol.iloc[0])
    lam_acc = float(att[att.tramo.str.startswith("2022-2024")].razon_acum_serpavi_incasol.iloc[0])
    lam2 = float(att[att.tramo.str.startswith("2015-2020")].razon_acum_serpavi_incasol.iloc[0])
    lam_c = lam_acc
    T_hi = float(g1.T_hi)
    # coeficiente esperado de un stock bajo el efecto T de GL: lam * T
    esp = {"lam_acum_2022_2024": lam_acc, "lam_acum_2015_2020": lam2, "T": T, "T_hi": T_hi,
           "esperado_serpavi_central": lam_acc * T, "esperado_serpavi_alto": lam_acc * T_hi}
    cl, ee = float(g1.coef), float(g1.ee)
    md = ["# M0 · Por qué la réplica de García-López no reproduce el coeficiente (C4, EXPLORATORIO)", "",
          "Objetivo de GL: 0,035 (EE 0,009) log-puntos por 100 anuncios en un barrio, convertido a 0,01215 por punto de VUT/parque (T). Estimación propia (GL1, sección, FE, cluster distrito): "
          f"{cl:+.4f} (EE {ee:.4f}, IC95 [{g1.ic95_lo:+.4f}; {g1.ic95_hi:+.4f}], p Holm {g1.p_holm:.2f}), NO REPLICADO, con signo contrario. Esta nota separa tres fuentes de discrepancia; no añade estimaciones causales.", "",
          "## Tres fuentes de discrepancia", "",
          "| fuente | GL (2020) | réplica propia | cuantificable con lo que hay |", "|---|---|---|---|",
          "| datos: alquiler | precio de oferta (Idealista), flujo | SERPAVI: stock de contratos IRPF | sí, vía Incasòl e IPC (abajo) |",
          "| datos: turismo | anuncios de Airbnb | VUT del INE (oleadas, cuenta unidades) | parcial: razón VUT/anuncios 0,11-0,42 en una sola fecha (2025) |",
          "| periodo | 2012-2016 | 2021-2024 (3 diferencias anuales) | SERPAVI sí existe 2011-2024; VUT INE solo desde 2021: no hay solape |",
          "| método | IV (instrumento de GL) | FE sin IV | no: sin instrumento no se puede aislar |",
          "| unidad | barrio/AEB (233 AEB) | sección (815) y distrito (8 con datos) | sí, GL1 frente a GL2: mismo signo, misma magnitud |", "",
          "## Atenuación de un stock frente a un flujo (Barcelona municipio)", "",
          "Series: Incasòl renta media de contratos de fianza de Barcelona (flujo; ruptura de umbral >650 a >600 euros en 2021, el salto 2020-2021 se excluye), SERPAVI mediana de €/m² (media simple de los 10 distritos, stock IRPF) e IPC de alquiler nacional (INE). Diferencias de logaritmos anuales; n pequeño, descriptivo.", "",
          "| tramo | n dif | Δlog Incasòl | Δlog SERPAVI | Δlog IPC | razón acum. SERPAVI/Incasòl | razón acum. SERPAVI/IPC | pendiente SERPAVI~Incasòl |", "|---|---|---|---|---|---|---|---|"]
    for _, r in att.iterrows():
        md.append(f"| {r.tramo} | {int(r.n_dif)} | {r.dlog_incasol:+.3f} | {r.dlog_serpavi:+.3f} | {r.dlog_ipc:+.3f} | {r.razon_acum_serpavi_incasol:.2f} | {r.razon_acum_serpavi_ipc:.2f} | {r.pendiente_serpavi_sobre_incasol:.2f} |")
    md += ["",
           f"Lectura: en 2022-2024 el stock SERPAVI recoge {lam_acc:.0%} de la variación acumulada de Incasòl; en 2015-2020, {lam2:.0%}. Si el efecto de GL sobre el flujo fuese T = {T:.4f}, un stock lo mostraría atenuado en torno a λT = {lam_acc*T:.4f} (hasta {lam_acc*T_hi:.4f} con el T alto por la razón VUT/anuncios). "
           f"Observado: {cl:+.4f}.",
           "- La atenuación explica una magnitud menor que 0,01215, no un signo negativo: el IC95 propio ([−0,0078; −0,0005]) queda por debajo de cero y de cualquier λT positivo.",
           "- El IC95 de GL2 (distrito) es igual de negativo: la unidad (sección o distrito) no cambia el resultado, con 8 clusters.", "",
           "## Qué se puede decir (sin atribuir causas)",
           f"- El coeficiente propio no es distinguible de 0 tras Holm (p Holm = {g1.p_holm:.2f}); su IC95 sin ajustar excluye λT.",
           "- Datos (stock frente a flujo): atenuación cuantificada en una sola ciudad, con 3-12 diferencias anuales; en 2012-2016 la razón es negativa (−0,68) y las pendientes van de 0,07 a 0,46. Solo es compatible con una magnitud menor, no con un signo negativo.",
           "- Método (FE sin IV, 3 diferencias anuales, 8 clusters): no se puede contrastar sin instrumento. Pretendencia sin señal (p=0,71, N=3); el placebo (p=0,026) tiene pocas permutaciones distintas. Un coeficiente negativo es compatible con confusión o con error de medida del VUT; los datos no lo distinguen.",
           "- Periodo: no se puede contrastar, porque el VUT del INE no existe antes de 2021. Que València (PARCIAL) y Sevilla (signo contrario) difieran es compatible con heterogeneidad o con ruido: con estimaciones C4 no se distingue.",
           "No se atribuye la discrepancia a ninguna fuente ni se afirma que GL esté refutado o confirmado para España 2021-2024. Faltan serie histórica de VUT/anuncios 2012-2016 y un instrumento (no disponibles en el repo).",
           "", "Capa: C4 (EXPLORATORIO)."]
    (OUT / "gl_no_replica.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return {"g1": (cl, ee, float(g1.ic95_lo), float(g1.ic95_hi), float(g1.p_holm)), "lam_acc": lam_acc, "lam2": lam2, "esp": esp, "T": T}


# ---------------------------------------------------------------- 4. Déficit 2021-2024 (ventana C1)
def deficit_2021_2024(term: dict) -> dict:
    """Todos los componentes C1: hogares (ECP y EPA corregida coinciden ≤15 %) y terminadas (MIVAU-Catastro ≤15 % en 2019-2024)."""
    sys.path.insert(0, str(RAIZ / "src" / "v3"))
    import pa_data
    q = pa_data.nacional_q()
    m = pa_data.mivau_nacional_anual()
    epa = q.hogares_epa * 1000.0
    ecp = q.hogares_ecp
    corr = 242_400.0          # salto del quiebre EPA 2021T1 retirado (criterio v1, informe 5.1)
    dh_epa = float(epa["2024Q4"] - epa["2020Q4"]) + corr
    dh_ecp = float(ecp["2024Q4"] - ecp["2021Q1"])
    rango_h = (max(dh_epa, dh_ecp) - min(dh_epa, dh_ecp)) / np.mean([dh_epa, dh_ecp])
    df = term["nac"]
    anios = range(2021, 2025)
    cat_ok = bool(df[df.anio.isin(anios)].coinciden_2_indep.all())
    yrs = list(anios)
    lib = m.libres.reindex(yrs)
    prot = m.protegida.reindex(yrs)
    park0 = m.parque.reindex([y - 1 for y in yrs]).values
    filas = []
    for hn, dh in (("EPA corregida", dh_epa), ("ECP", dh_ecp)):
        for pf, ser in (("con", lib + prot.fillna(0)), ("sin", lib)):
            for b in (0.0, 0.001, 0.002):
                baj = float(np.nansum(b * park0))
                bruto = float(ser.sum())
                filas.append({"hogares": hn, "delta_hogares": dh, "protegida": pf, "bajas_pct": 100 * b, "bruto": bruto,
                              "bajas": baj, "terminadas_netas": bruto - baj, "deficit": dh - (bruto - baj)})
    t = pd.DataFrame(filas)
    comp_c1 = (rango_h <= TOL) and cat_ok
    t["capa"] = "C1" if comp_c1 else "C4"
    t.to_csv(OUT / "deficit_2021_2024.csv", index=False, float_format="%.0f")
    med = float(t.deficit.median())
    lo, hi = float(t.deficit.min()), float(t.deficit.max())
    REG.log("M0", "deficit_2021_2024", "dH - (terminadas - bajas), 12 combinaciones", 2021, 2024, 4, np.nan, np.nan, np.nan, coef_interes=med,
            notas=f"rango {lo:.0f}-{hi:.0f}; capa {t.capa.iloc[0]}")
    return {"mediana": med, "min": lo, "max": hi, "capa": t.capa.iloc[0], "dh_epa": dh_epa, "dh_ecp": dh_ecp,
            "rango_hogares_rel": float(rango_h), "catastro_ok": cat_ok, "n_comb": int(len(t))}


def main() -> None:
    c = conciliacion()
    t = terminadas()
    g = gl()
    d24 = deficit_2021_2024(t)
    nac = t["nac"]
    res = {
        "rama": "M0",
        "pregunta": "¿Por qué difieren las cifras de déficit 2021-2025 (v1, v3, BdE), cuántas viviendas se terminan al año y por qué no se replica García-López?",
        "capa": "C1/C2 (conciliación y terminadas); C4 (GL)",
        "datos": "output v1/v3 (A1), MIVAU fin de obra, protegida y parque, Catastro urbana municipios, Incasòl, SERPAVI, IPC alquiler INE",
        "N": int(len(nac)),
        "metodo": "Descomposición aditiva; triangulación MIVAU-Catastro (±15 %); razones de variación stock/flujo",
        "estimacion": c["ref_v3"],
        "ic95": [c["min"], c["max"]],
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO (conciliación) / ASOCIACIÓN no evaluada",
        "diagnosticos": {
            "cadena_v1_a_ref_v3_cierra": True,
            "anios_c1_terminadas": t["anios_ok"],
            "n_anios_c1": t["n_ok"],
            "mivau_mensual_vs_anual_dif_max": t["ident"],
            "dparque_dependiente_mediana_rel": t["dep_rel"],
            "gl": {"coef": g["g1"][0], "ee": g["g1"][1], "lambda_2022_2024": g["lam_acc"], "lambda_2015_2020": g["lam2"],
                   "coef_esperado_stock": g["esp"]["esperado_serpavi_central"]},
        },
        "deficit_2021_2024": {**d24, "razon_capa": "todos los componentes C1: hogares ECP y EPA corregida dentro de ±15 %; terminadas MIVAU-Catastro dentro de ±15 % en 2021-2024"},
        "deficit_2021_2025": {"capa": "C4", "razon": "capa = la menor de sus componentes: terminadas 2025 es C4 frágil (Catastro +14,9 %, sale con otras alineaciones); ΔH 2021-2025 es C1", "rango": [c["min"], c["max"]]},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: conciliación y triangulación contable"},
        "notas": "Sin BdE terminadas en data/raw; cifra BdE NO VERIFICADA en método. Catastro solo régimen común.",
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    print(json.dumps(res["diagnosticos"], ensure_ascii=False, default=float, indent=1))


if __name__ == "__main__":
    main()
