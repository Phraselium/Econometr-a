"""V16-F2.3 · Atlas: constructores de indicadores (cada función devuelve un DataFrame en formato largo, ya con supresión).

Todas las lecturas pasan por f2_atlas_datos.leer (filtros de muestra sellada v6 y de sellado V16).
"""
from __future__ import annotations

import unicodedata

import numpy as np
import pandas as pd

import f2_atlas_datos as D
from f2_atlas_datos import (BASE, COLS, FECHA, P16, SUPERFICIE_M2, estandar, leer, periodos_finos, sin_sellados, suprimir)

KEY = ["territorio_codigo", "nivel", "periodo"]
F_ADRH = "INE, Atlas de Distribución de Renta de los Hogares (ADRH) 2015-2023"
F_SERP = "MIVAU, SERPAVI (AEAT-IRPF, stock de contratos de alquiler declarados; tipología colectiva)"
F_TAS = "MIVAU, valor tasado de vivienda libre (€/m², media anual de los 4 trimestres)"
F_VTE = "INE, Viviendas turísticas en España (VTE), medición experimental"
F_IA = "Inside Airbnb (rastreo de anuncios de plataforma; no exhaustivo)"
F_CENSO = "INE, Censo de Población y Viviendas 2021"
F_PAD = "INE, Padrón continuo, población por sección y nacionalidad 2022"
F_EMCR = "INE, Estadística de Migraciones y Cambios de Residencia (EMCR)"
F_CGPJ = "CGPJ, estadística judicial (agregado propio; tercero no redistribuible, sin microdatos)"


def _norm(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s.upper()) if not unicodedata.combining(c))


# ------------------------------------------------------------------------------------------------ renta (ADRH)
ADRH_VARS = {
    "ine_adrh_renta_neta_media_persona_eur": ("renta_media_persona", "€ por persona y año"),
    "ine_adrh_renta_neta_media_hogar_eur": ("renta_media_hogar", "€ por hogar y año"),
    "ine_adrh_renta_mediana_uc_eur": ("renta_mediana_uc", "€ por unidad de consumo y año"),
    "ine_adrh_gini_indice": ("gini", "índice 0-100"),
    "ine_adrh_p80p20_ratio": ("p80_p20", "cociente"),
}


def adrh(smoke: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (indicadores ADRH ya suprimidos, renta media del hogar con base de hogares, para el esfuerzo)."""
    vs = ",".join(f"'{v}'" for v in list(ADRH_VARS) + ["ine_adrh_poblacion_personas", "ine_adrh_tamano_medio_hogar_personas"])
    d = leer(P16 / "renta_parque_adrh_completo.parquet", f"variable in ({vs})", smoke)
    pob = d[d.variable == "ine_adrh_poblacion_personas"][KEY + ["valor"]].rename(columns={"valor": "pob"})
    tam = d[d.variable == "ine_adrh_tamano_medio_hogar_personas"][KEY + ["valor"]].rename(columns={"valor": "tam"})
    aux = pob.merge(tam, on=KEY, how="left")
    aux["hog"] = aux.pob / aux.tam.where(aux.tam > 0)
    salida, hogar = [], None
    for var, (ind, uni) in ADRH_VARS.items():
        s = d[d.variable == var].merge(aux[KEY + ["pob", "hog"]], on=KEY, how="left")
        met = s.metodo_dato.fillna("")
        sust = met.str.startswith("valor_sustituto") | met.str.startswith("valor_subarea")
        cal = pd.Series(np.select(
            [sust, met.str.startswith("cota_inferior"), met.str.startswith("cota_superior")],
            ["valor sustituto de provincia/comarca: no se muestra como municipal", "cota inferior por secreto estadístico",
             "cota superior por secreto estadístico"], "registro administrativo (sin intervalo)"), index=s.index)
        s["valor"] = s.valor.where(~sust)
        s["suprimida"] = sust
        s["n_base"] = np.where(s.hog.notna(), s.hog, np.where(s.pob < D.N_MIN, s.pob, np.nan))
        o = suprimir(estandar(s, ind, uni, F_ADRH, cal))
        salida.append(o)
        if ind == "renta_media_hogar":
            hogar = o
    return periodos_finos(pd.concat(salida, ignore_index=True)), hogar


# ------------------------------------------------------------------------------------------------ alquiler (SERPAVI)
def serpavi(smoke: bool) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (alquiler €/m²·mes con IC aproximado, tabla auxiliar mediana/se/n para el esfuerzo)."""
    d = leer(BASE, "variable in ('serpavi_alquiler_m2_mediana','serpavi_alquiler_m2_p25','serpavi_alquiler_m2_p75',"
                   "'serpavi_n_contratos_recuento') AND desagregacion = 'tipologia=VC' AND periodo BETWEEN '2015' AND '2024'", smoke)
    w = d.pivot_table(index=KEY, columns="variable", values="valor", aggfunc="first").reset_index()
    w = w.rename(columns={"serpavi_alquiler_m2_mediana": "med", "serpavi_alquiler_m2_p25": "p25", "serpavi_alquiler_m2_p75": "p75",
                          "serpavi_n_contratos_recuento": "n"})
    for c in ("p25", "p75", "n"):
        if c not in w:
            w[c] = np.nan
    w = w[w.med.notna()].copy()
    # n propio (municipio, provincia) o cota del municipio (distrito, sección): si el municipio tiene n < 10, la celda también
    nm = w[w.nivel == "municipio"].set_index(["territorio_codigo", "periodo"]).n
    fino = w.nivel.isin(["distrito", "seccion"])
    clave = pd.MultiIndex.from_arrays([w.territorio_codigo.str[:5], w.periodo])
    w["n_mun"] = np.where(fino, nm.reindex(clave).values, np.nan)
    w["n_celda"] = np.where(fino, w.n_mun, w.n)
    se = 1.2533 * ((w.p75 - w.p25) / 1.349) / np.sqrt(w.n.where(w.n > 0))
    w["se"] = se.where(~fino)
    w["ic_inf"] = (w.med - 1.96 * w.se).clip(lower=0)
    w["ic_sup"] = w.med + 1.96 * w.se
    w["cv"] = w.se / w.med
    cal = pd.Series(np.where(fino, "registro AEAT-IRPF; sin n ni IC por celda (n de base acotado por el municipio)",
                             "registro AEAT-IRPF; IC 95 % aproximado (normal sobre la mediana con cuartiles y n)"), index=w.index)
    b = w.rename(columns={"med": "valor"})
    b["n_base"] = w.n_celda
    o = suprimir(estandar(b, "alquiler_m2_mediana", "€/m² y mes", F_SERP, cal))
    return periodos_finos(o), w


def esfuerzo(w: pd.DataFrame, hogar: pd.DataFrame) -> pd.DataFrame:
    """Ratio descriptiva: alquiler mediano anual (SERPAVI, €/m²·mes × 12) × 80 m² / renta neta media del hogar (ADRH)."""
    r = hogar[["territorio_codigo", "nivel", "periodo", "valor", "n_base", "suprimida", "calidad"]].rename(
        columns={"valor": "renta", "n_base": "hog", "suprimida": "renta_sup", "calidad": "cal_renta"})
    m = w[w.nivel.isin(["provincia", "municipio", "distrito", "seccion"])].merge(r, on=KEY, how="inner")
    k = 100.0 * 12.0 * SUPERFICIE_M2 / m.renta.where(m.renta > 0)
    m["valor"] = m.med * k
    m["ic_inf"], m["ic_sup"] = m.ic_inf * k, m.ic_sup * k
    m["n_base"] = np.fmin(m.n_celda, m.hog.fillna(np.inf)).where(m.n_celda.notna() | m.hog.notna())
    m["suprimida"] = m.renta_sup.astype(bool) | m.renta.isna()
    nota = np.where(m.cal_renta.str.contains("cota"), "; renta con cota por secreto", "")
    cal = pd.Series(np.where(m.nivel.isin(["distrito", "seccion"]),
                             "ratio descriptiva sin IC (renta ADRH registro; alquiler sin n por celda)",
                             "ratio descriptiva; IC 95 % propaga solo el del alquiler (renta ADRH = registro)") + nota, index=m.index)
    o = suprimir(estandar(m, "esfuerzo_alquiler_renta_hogar", "% de la renta neta media del hogar", F_SERP + " / " + F_ADRH, cal))
    o = o[(o.periodo <= "2023")]
    return periodos_finos(o)


# ------------------------------------------------------------------------------------------------ precio (valor tasado)
def precio(smoke: bool) -> pd.DataFrame:
    d = leer(BASE, "(variable='valor_tasado' AND nivel='provincia') OR (variable='valor_tasado_ccaa' AND nivel='ccaa') OR "
                   "(variable='p_tasado' AND nivel IN ('municipio','nacional'))", smoke)
    d = d[d.periodo.str.contains("T")].copy()
    d["anio"], d["tri"] = d.periodo.str[:4], d.periodo.str[-1]
    a = d.groupby(["territorio_codigo", "nivel", "anio"]).agg(valor=("valor", "mean"), nt=("tri", "nunique")).reset_index()
    a = a[(a.nt == 4) & (a.anio.between("2015", "2025"))].rename(columns={"anio": "periodo"})
    ult = d[d.periodo == d.periodo.max()].copy()
    o = pd.concat([a, ult[KEY + ["valor"]]], ignore_index=True)
    cal = pd.Series(np.where(o.nivel == "municipio", "registro de tasaciones; sin n publicado; municipal: solo donde la base lo tiene",
                             "registro de tasaciones; sin n publicado"), index=o.index)
    return suprimir(estandar(o, "valor_tasado_m2", "€/m²", F_TAS, cal))


# ------------------------------------------------------------------------------------------------ viviendas turísticas
def vte(smoke: bool, viv: pd.Series) -> pd.DataFrame:
    d = leer(P16 / "alquiler_turismo.parquet", "(variable in ('ine_vte_viviendas_turisticas','ine_vte_plazas') OR variable LIKE "
             "'ine_vte_porcentaje%') AND periodo IN ('2020-08','2022-08','2024-08','2026-05')", smoke)
    c = d[d.variable == "ine_vte_viviendas_turisticas"][KEY + ["valor"]].rename(columns={"valor": "n"})
    sal = []
    cal = "estimación experimental del INE (fuentes de plataformas); sin intervalo publicado"
    for var, ind, uni in (("ine_vte_viviendas_turisticas", "viviendas_turisticas_ine", "viviendas"),
                          ("ine_vte_plazas", "plazas_turisticas_ine", "plazas")):
        s = d[d.variable == var].merge(c, on=KEY, how="left")
        s["n_base"] = s.n
        sal.append(suprimir(estandar(s, ind, uni, F_VTE, cal)))
    s = d[d.variable.str.startswith("ine_vte_porcentaje")].merge(c, on=KEY, how="left")
    s["n_base"] = s.n
    sal.append(suprimir(estandar(s, "viviendas_turisticas_pct_ine", "% de las viviendas", F_VTE, cal)))
    return pd.concat(sal, ignore_index=True)


def inside_airbnb(smoke: bool, viv_mun: pd.Series) -> pd.DataFrame:
    d = leer(P16 / "alquiler_turismo.parquet", "variable IN ('ia_anuncios_activos_numero','ia_anuncios_vivienda_entera_numero',"
             "'ia_precio_noche_mediana','ia_precio_noche_n_numero') AND nivel IN ('municipio','seccion')", smoke)
    d = d.sort_values("periodo")
    ult = d.groupby(["territorio_codigo", "nivel", "variable"], as_index=False).tail(1)
    cal = "rastreo de plataforma, no validado y no exhaustivo: solo descriptivo; sin intervalo"
    sal = []
    for var, ind in (("ia_anuncios_activos_numero", "anuncios_activos_ia"), ("ia_anuncios_vivienda_entera_numero", "anuncios_vivienda_entera_ia")):
        s = ult[ult.variable == var].copy()
        s["n_base"] = s.valor
        sal.append(suprimir(estandar(s, ind, "anuncios", F_IA, cal)))
    p = ult[ult.variable == "ia_precio_noche_mediana"].merge(
        d[d.variable == "ia_precio_noche_n_numero"][KEY + ["valor"]].rename(columns={"valor": "n"}), on=KEY, how="left")
    p["n_base"] = p.n
    sal.append(suprimir(estandar(p, "precio_noche_mediana_ia", "€ por noche", F_IA, cal)))
    # anuncios por 100 viviendas (Censo 2021): sección con t18_1, municipio con 59525
    a = ult[ult.variable == "ia_anuncios_activos_numero"].copy()
    v = leer(BASE, "variable='censo2021_t18_1' AND nivel='seccion'", smoke).set_index("territorio_codigo").valor
    a["viv"] = np.where(a.nivel == "seccion", a.territorio_codigo.map(v), a.territorio_codigo.map(viv_mun))
    a = a[a.viv.notna() & (a.viv > 0)]
    a["n_base"] = np.fmin(a.valor, a.viv)
    a["valor"] = 100.0 * a.valor / a.viv
    sal.append(suprimir(estandar(a, "anuncios_activos_ia_por_100_viviendas", "anuncios por 100 viviendas (Censo 2021)", F_IA + "; " + F_CENSO, cal)))
    return periodos_finos(pd.concat(sal, ignore_index=True))


# ------------------------------------------------------------------------------------------------ población extranjera
def extranjera(smoke: bool) -> pd.DataFrame:
    sal = []
    t = P16 / "tension_social.parquet"
    d = leer(t, "variable='ine_padron_seccion_poblacion_personas' AND periodo='2022' AND (desagregacion LIKE '%nacionalidad=total' "
                "OR desagregacion LIKE '%nacionalidad=total_extranjera') AND desagregacion LIKE 'sexo=ambos_sexos%'", smoke)
    w = d.pivot_table(index=KEY, columns="desagregacion", values="valor", aggfunc="first").reset_index()
    w.columns = [c.split("nacionalidad=")[-1] if "nacionalidad" in c else c for c in w.columns]
    w["n_base"] = w["total"]
    w["valor"] = 100.0 * w.total_extranjera / w.total.where(w.total > 0)
    sal.append(suprimir(estandar(w.dropna(subset=["valor"]), "poblacion_extranjera_pct", "% de la población empadronada", F_PAD,
                                 "registro administrativo (padrón); sin intervalo")))
    c = leer(BASE, "variable='pob_censo_anual' AND nivel IN ('municipio','provincia') AND desagregacion IN ('nacionalidad=Total',"
                   "'nacionalidad=España') AND periodo IN ('2021','2023','2025')", smoke)
    w = c.pivot_table(index=KEY, columns="desagregacion", values="valor", aggfunc="first").reset_index()
    w = w.rename(columns={"nacionalidad=Total": "total", "nacionalidad=España": "esp"}).dropna(subset=["total", "esp"])
    w["n_base"] = w.total
    w["valor"] = 100.0 * (w.total - w.esp) / w.total.where(w.total > 0)
    sal.append(suprimir(estandar(w, "poblacion_extranjera_pct", "% de la población (censo anual)", "INE, Censo anual de población",
                                 "registro administrativo (censo anual); sin intervalo")))
    e = leer(t, "variable='ine_emcr_saldo_migratorio_personas' AND desagregacion='sexo=ambos_sexos;tipo_saldo=saldo_exterior' "
                "AND nivel IN ('municipio','provincia')", smoke)
    p = leer(t, "variable='ine_padron_poblacion_personas' AND desagregacion='sexo=total' AND nivel IN ('municipio','provincia')", smoke)
    m = e.merge(p[KEY + ["valor"]].rename(columns={"valor": "pob"}), on=KEY, how="inner")
    m["n_base"] = m.pob
    m["valor"] = 1000.0 * m.valor / m.pob.where(m.pob > 0)
    sal.append(suprimir(estandar(m, "saldo_migratorio_exterior_por_mil", "personas por 1.000 habitantes", F_EMCR,
                                 "registro administrativo (EMCR); sin intervalo")))
    return periodos_finos(pd.concat(sal, ignore_index=True))


# ------------------------------------------------------------------------------------------------ parque y vacías (Censo 2021)
def parque(smoke: bool) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    tb = D.censo_tablas()
    a = tb["p59525"].copy()
    a["prov"] = a.cod.str[:2]
    a["ccaa"] = a.prov.map(D._prov_ccaa())
    sal = []
    cal = "recuento del Censo 2021; sin intervalo"
    filas = []
    for nivel, col in (("municipio", "cod"), ("provincia", "prov"), ("ccaa", "ccaa")):
        g = a.groupby(col)[["total", "no_principal"]].sum(min_count=1).reset_index().rename(columns={col: "territorio_codigo"})
        g["nivel"] = nivel
        filas.append(g)
    n = a[["total", "no_principal"]].sum()
    filas.append(pd.DataFrame({"territorio_codigo": ["00"], "total": [n.total], "no_principal": [n.no_principal], "nivel": ["nacional"]}))
    g = pd.concat(filas, ignore_index=True)
    g["periodo"] = "2021"
    viv_prov = g[g.nivel == "provincia"].set_index("territorio_codigo").total
    g = sin_sellados(D._smoke_df(g, smoke))
    g["n_base"] = g.total
    g["valor"] = 100.0 * g.no_principal / g.total.where(g.total > 0)
    sal.append(suprimir(estandar(g, "viviendas_no_principales_pct", "% de las viviendas", F_CENSO, cal)))
    p = tb["p59531"]
    p = p[p.tipo.isin(["Viviendas totales", "Viviendas vacías", "Viviendas de uso esporádico"])].copy()
    p["nivel"] = np.select([p.mun.notna(), p.prov.notna(), p.ccaa.notna()], ["municipio", "provincia", "ccaa"], "nacional")
    p["territorio_codigo"] = np.select([p.mun.notna(), p.prov.notna(), p.ccaa.notna()],
                                       [p.mun.astype(str).str[:5], p.prov.astype(str).str[:2], p.ccaa.astype(str).str[:2]], "00")
    w = p.pivot_table(index=["territorio_codigo", "nivel"], columns="tipo", values="total", aggfunc="first").reset_index()
    w["periodo"] = "2021"
    w = sin_sellados(D._smoke_df(w, smoke))
    for col, ind in (("Viviendas vacías", "viviendas_vacias_pct"), ("Viviendas de uso esporádico", "viviendas_uso_esporadico_pct")):
        s = w.copy()
        s["n_base"] = s["Viviendas totales"]
        s["valor"] = 100.0 * s[col] / s["Viviendas totales"].where(s["Viviendas totales"] > 0)
        s["suprimida"] = s.valor.isna()
        sal.append(suprimir(estandar(s, ind, "% de las viviendas", F_CENSO + ", tabla 59531 (consumo eléctrico)",
                                     "recuento del Censo 2021 (clasificación por consumo eléctrico); sin intervalo; la vacía del Censo y la "
                                     "vacía por consumo son la misma cifra")))
    c = leer(BASE, "variable IN ('censo2021_t18_1','censo2021_t19_2') AND nivel='seccion'", smoke)
    s = c.pivot_table(index=KEY, columns="variable", values="valor", aggfunc="first").reset_index()
    s["n_base"] = s.censo2021_t18_1
    s["valor"] = 100.0 * s.censo2021_t19_2 / s.censo2021_t18_1.where(s.censo2021_t18_1 > 0)
    sal.append(suprimir(estandar(s.dropna(subset=["valor"]), "viviendas_no_principales_pct", "% de las viviendas", F_CENSO + " (indicadores por sección)", cal)))
    return pd.concat(sal, ignore_index=True), a.set_index("cod").total, viv_prov


# ------------------------------------------------------------------------------------------------ lanzamientos (CGPJ)
def lanzamientos(smoke: bool, viv_mun: pd.Series) -> pd.DataFrame:
    t = P16 / "tension_social_terceros.parquet"
    sal = []
    cal_p = "recuento judicial agregado (CGPJ); sin intervalo; Cádiz incluye Ceuta y Málaga incluye Melilla"
    d = leer(t, "variable IN ('cgpj_lanzamientos_total_numero','cgpj_lanzamientos_lau_numero','cgpj_lanzamientos_hipotecaria_numero') "
                "AND nivel='provincia'", smoke)
    d["anio"], d["tri"] = d.periodo.str[:4], d.periodo.str[-1]
    a = d.groupby(["territorio_codigo", "nivel", "variable", "anio"]).agg(valor=("valor", "sum"), nt=("tri", "nunique")).reset_index()
    a = a[(a.nt == 4) & (a.anio.between("2013", "2025"))].rename(columns={"anio": "periodo"})
    mp = viv_mun.reset_index()
    mp["prov"] = mp.cod.str[:2]
    vprov = mp.groupby("prov").total.sum()
    nombres = {"cgpj_lanzamientos_total_numero": "lanzamientos_total", "cgpj_lanzamientos_lau_numero": "lanzamientos_lau",
               "cgpj_lanzamientos_hipotecaria_numero": "lanzamientos_hipotecaria"}
    for var, ind in nombres.items():
        s = a[a.variable == var].copy()
        s["n_base"] = s.valor
        sal.append(suprimir(estandar(s, ind, "lanzamientos practicados al año", F_CGPJ, cal_p)))
    s = a[a.variable == "cgpj_lanzamientos_total_numero"].copy()
    s["viv"] = s.territorio_codigo.map(vprov)
    s["n_base"] = np.fmin(s.valor, s.viv)
    s["valor"] = 10000.0 * s.valor / s.viv
    sal.append(suprimir(estandar(s.dropna(subset=["valor"]), "lanzamientos_total_por_10000_viviendas", "por 10.000 viviendas (Censo 2021) y año",
                                 F_CGPJ, cal_p + "; denominador: viviendas totales del Censo 2021")))
    # partidos judiciales: acumulado 2013-2024 (agregado propio)
    q = leer(t, "variable IN ('cgpj_lanzamientos_total_numero','cgpj_lanzamientos_lau_numero','cgpj_lanzamientos_hipotecaria_numero') "
                "AND nivel='partido_judicial' AND periodo BETWEEN '2013' AND '2024'", smoke)
    ac = q.groupby(["territorio_codigo", "nivel", "variable"]).agg(valor=("valor", "sum"), na=("periodo", "nunique")).reset_index()
    ac = ac[ac.na == 12].copy()
    ac["periodo"] = "2013-2024"
    cal_pj = "recuento judicial agregado (CGPJ), suma 2013-2024; partido identificado por cabecera; sin intervalo"
    for var, ind in nombres.items():
        s = ac[ac.variable == var].copy()
        s["n_base"] = s.valor
        sal.append(suprimir(estandar(s, ind + "_acum_2013_2024", "lanzamientos practicados, suma 2013-2024", F_CGPJ, cal_pj)))
    pm = pd.read_parquet(P16 / "tension_social_partidos_municipios_terceros.parquet")
    pm = pm[pm.estado == "partido_con_serie_cgpj"]
    vpj = pm.assign(viv=pm.cod_municipio_ine.map(viv_mun)).groupby("territorio_codigo").viv.sum(min_count=1)
    s = ac[ac.variable == "cgpj_lanzamientos_total_numero"].copy()
    s["viv"] = s.territorio_codigo.map(vpj)
    s = s[s.viv.notna()]
    s["n_base"] = np.fmin(s.valor, s.viv)
    s["valor"] = 10000.0 * s.valor / s.viv
    sal.append(suprimir(estandar(s, "lanzamientos_total_por_10000_viviendas_acum_2013_2024", "por 10.000 viviendas (Censo 2021), suma 2013-2024",
                                 F_CGPJ, cal_pj + "; denominador: viviendas totales del Censo 2021 de los municipios del partido")))
    # CCAA: series de TSJ ya agregadas en output/v16/f2_hechos
    c = pd.read_csv(D.LANZ_CCAA)
    c = c[c.tsj.str.upper() != "TOTAL"].copy()
    c["nm"] = c.tsj.map(_norm)
    c["territorio_codigo"] = c.nm.map(lambda x: next((cod for k, cod in D.TSJ if k in x), None))
    c = c.dropna(subset=["territorio_codigo"])
    for col, per in (("total_2013", "2013"), ("total_2025", "2025")):
        s = pd.DataFrame({"territorio_codigo": c.territorio_codigo, "nivel": "ccaa", "periodo": per, "valor": c[col], "n_base": c[col]})
        sal.append(suprimir(estandar(s, "lanzamientos_total", "lanzamientos practicados al año", F_CGPJ + " (series por TSJ)",
                                     "recuento judicial agregado por TSJ; sin intervalo; el TSJ de Andalucía incluye Ceuta y Melilla")))
    return pd.concat(sal, ignore_index=True)


# ------------------------------------------------------------------------------------------------ intervenciones y ECV
def intervenciones(smoke: bool) -> pd.DataFrame:
    i = pd.read_csv(D.INTERV, dtype={"cod_ine": str})
    i = i[i.ambito == "municipio"].copy()
    i["cod_ine"] = i.cod_ine.str.zfill(5)
    ef, fin = pd.to_datetime(i.fecha_efecto, errors="coerce"), pd.to_datetime(i.fecha_fin, errors="coerce")
    ref = pd.Timestamp(FECHA)
    i = i[(ef <= ref) & (fin.isna() | (fin >= ref))]
    sal = []
    for nombre, ins in (("intervencion_zona_tensionada_vigente", ["zona_tensionada"]),
                        ("intervencion_vut_municipal_vigente", ["vut_moratoria", "vut_regulacion"])):
        s = i[i.instrumento.isin(ins)].drop_duplicates("cod_ine")
        d = pd.DataFrame({"territorio_codigo": s.cod_ine, "nivel": "municipio", "periodo": FECHA, "valor": 1.0})
        d = sin_sellados(D._smoke_df(d, smoke))
        sal.append(estandar(d, nombre, "1 = vigente a la fecha del dato", "output/v16/f1/intervenciones.csv (normativa verificada en F1)",
                            "registro normativo; la ausencia de fila no equivale a ausencia de regulación"))
    return pd.concat(sal, ignore_index=True)


def ecv_ccaa() -> pd.DataFrame:
    e = pd.read_csv(D.ESFUERZO_ECV)
    e = e[(e.dimension == "CCAA") & e.indicador.isin(["sobre40", "sobre30"])].copy()
    e["territorio_codigo"] = e.categoria.map(D.NUTS2)
    e = e.dropna(subset=["territorio_codigo"])
    e["nivel"], e["periodo"] = "ccaa", e.anio.astype(str)
    e["valor"], e["ic_inf"], e["ic_sup"] = e.estimacion, e.ic_lo, e.ic_hi
    e["n_base"], e["cv"] = e.n_hogares, e.cv
    e["suprimida"] = e.estado.eq("suprimida")
    sal = []
    for ind in ("sobre40", "sobre30"):
        s = e[e.indicador == ind]
        pct = ind[-2:]
        sal.append(suprimir(estandar(s, f"ecv_sobreesfuerzo_{pct}_ccaa", "% de la población", "INE, ECV (microdatos; f2_esfuerzo)",
                                     "encuesta ECV; IC 95 % bootstrap (f2_esfuerzo); no es la ratio descriptiva de esfuerzo del atlas")))
    return pd.concat(sal, ignore_index=True)
