"""V8-F1: paneles de datos (nacional trimestral 1995T1-2026T2, 17 CCAA, Comunitat Valenciana por provincias, València ciudad).

Determinista y sin red. SEED=20261010. Lee SOLO data/raw y los paneles v7 ya versionados (data/processed/v7, data/processed/valencia.csv).
Escribe en data/processed/v8 y docs/v8/diccionario.md. Nunca toca data/sealed.

Cruces territoriales SOLO por código INE. Las fuentes que traen únicamente nombre (MIVAU valor tasado, ETCL, Registradores,
Notariado CV, INE VUT) se traducen con diccionarios explícitos nombre -> código (constantes COD_*), con comprobación de que
todo nombre queda asignado y de que no hay duplicados (código, periodo). Nunca se cruza por nombre.
Interpolaciones: siempre marcadas con la columna booleana <variable>_interp y documentadas en docs/v8/diccionario.md.
No se extrapola fuera del rango observado.
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
SEED = 20261010
RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"
V7 = RAIZ / "data" / "processed" / "v7"
OUT = RAIZ / "data" / "processed" / "v8"
OUT_R = RAIZ / "output" / "v8" / "F1"
DOC = RAIZ / "docs" / "v8" / "diccionario.md"
np.random.seed(SEED)

INI, FIN = "1995Q1", "2026Q2"
PER = pd.period_range(INI, FIN, freq="Q")

CCAA17 = [f"{i:02d}" for i in range(1, 18)]
CV_PROV = ["03", "12", "46"]
CCAA_COD_NOMBRE = {  # solo para etiquetar la salida (código -> nombre), nunca para cruzar
    "01": "Andalucía", "02": "Aragón", "03": "Asturias", "04": "Illes Balears", "05": "Canarias", "06": "Cantabria",
    "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña", "10": "Comunitat Valenciana", "11": "Extremadura",
    "12": "Galicia", "13": "Comunidad de Madrid", "14": "Región de Murcia", "15": "Comunidad Foral de Navarra",
    "16": "País Vasco", "17": "La Rioja"}

# ---------------------------------------------------------------------------------------------------------------------------
# Diccionarios explícitos nombre -> código INE (fuentes sin código). Cada uno cubre exactamente las cadenas halladas en data/raw.
COD_MIVAU_CCAA = {
    "Andalucía": "01", "Aragón": "02", "Asturias (Principado de )": "03", "Balears (Illes)": "04", "Canarias": "05",
    "Cantabria": "06", "Castilla y León": "07", "Castilla-La Mancha": "08", "Cataluña": "09", "Comunidad Valenciana": "10",
    "Extremadura": "11", "Galicia": "12", "Madrid (Comunidad de)": "13", "Murcia (Región de)": "14", "Comunitat Valenciana": "10",
    "Navarra (Com. Foral de)": "15", "Navarra (Comunidad Foral de)": "15", "País Vasco": "16", "Rioja (La)": "17"}
COD_MIVAU_PROV = {"Alicante/Alacant": "03", "Castellón/Castelló": "12", "Valencia/València": "46"}
COD_ETCL_CCAA = {
    "Andalucía": "01", "Aragón": "02", "Asturias, Principado de": "03", "Balears, Illes": "04", "Canarias": "05",
    "Cantabria": "06", "Castilla y León": "07", "Castilla - La Mancha": "08", "Cataluña": "09", "Comunitat Valenciana": "10",
    "Extremadura": "11", "Galicia": "12", "Madrid, Comunidad de": "13", "Murcia, Región de": "14",
    "Navarra, Comunidad Foral de": "15", "País Vasco": "16", "Rioja, La": "17"}
COD_FRONTUR_SERIE = {  # códigos de serie INE (FREG...) -> CCAA; FRONTUR solo publica 6 CCAA + «Otras»
    "FREG346": "13", "FREG347": "10", "FREG348": "09", "FREG349": "05", "FREG350": "04", "FREG351": "01"}
COD_VUT_PROV = {"Alicante/Alacant": "03", "Castellón/Castelló": "12", "Valencia/València": "46"}
COD_REGISTR_PROV = {"Alicante / Alacant": "03", "Castellón / Castelló": "12", "Valencia / València": "46"}
COD_NOTARIADO_PROV = {"Alicante": "03", "Castellón": "12", "Valencia": "46"}
COD_VALENCIA_TERR = {"València (municipio)": "46250"}   # los distritos traen el código INE de 7 dígitos en la propia etiqueta

META: dict[str, dict] = {}      # variable -> metadatos del diccionario
INTERP_INFO: dict[str, dict] = {}


def reg(var, definicion, unidad, fuente, metodo="original (sin transformación)", rupturas="—", capa=None):
    META[var] = dict(definicion=definicion, unidad=unidad, fuente=fuente, metodo=metodo, rupturas=rupturas, capa=capa)


# ----------------------------------------------------------------------------------------------------------- lectores
def rd(rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(RAW / rel, low_memory=False, **kw)


def per_q(fecha: pd.Series) -> pd.PeriodIndex:
    return pd.PeriodIndex(pd.to_datetime(fecha), freq="Q")


def sq(df: pd.DataFrame, serie: str, col: str = "valor") -> pd.Series:
    """Serie trimestral (índice Period Q) de una serie del CSV largo."""
    s = df.loc[df["serie"] == serie].dropna(subset=[col])
    out = pd.Series(s[col].to_numpy(float), index=per_q(s["fecha"])).sort_index()
    assert out.index.is_unique, f"periodos duplicados en {serie}"
    return out


def sm(df: pd.DataFrame, serie: str, col: str = "valor") -> pd.Series:
    """Serie mensual (índice Period M)."""
    s = df.loc[df["serie"] == serie].dropna(subset=[col])
    out = pd.Series(s[col].to_numpy(float), index=pd.PeriodIndex(pd.to_datetime(s["fecha"]), freq="M")).sort_index()
    assert out.index.is_unique, f"meses duplicados en {serie}"
    return out


def m2q(s: pd.Series, how: str) -> pd.Series:
    """Mensual -> trimestral (mean/sum/last). NaN si faltan meses del trimestre (no se completa)."""
    q = pd.PeriodIndex(s.index.to_timestamp(), freq="Q")
    g = s.groupby(q)
    r = getattr(g, how)()
    r[g.count() < 3] = np.nan
    return r.reindex(PER)


def fin_trim(s: pd.Series) -> pd.Series:
    """Saldo de fin de trimestre: valor del último mes del trimestre (marzo, junio, septiembre, diciembre); sirve también para series trimestrales."""
    s = s[s.index.month % 3 == 0]
    return pd.Series(s.to_numpy(), index=pd.PeriodIndex(s.index.to_timestamp(), freq="Q")).reindex(PER)


def y2q_asignado(s: pd.Series, anios: bool = True) -> pd.Series:
    """Anual (índice año) -> trimestral asignando el valor anual a los cuatro trimestres (desagregación en escalón)."""
    idx = pd.period_range(f"{int(s.index.min())}Q1", f"{int(s.index.max())}Q4", freq="Q")
    return pd.Series([s[p.year] for p in idx], index=idx).reindex(PER)


def interp_lin(s: pd.Series, log: bool = False) -> tuple[pd.Series, pd.Series]:
    """Interpolación lineal (o log-lineal) SOLO entre observaciones; sin extrapolar. Devuelve (serie, marca)."""
    s = s.dropna().sort_index()
    full = s.reindex(pd.period_range(s.index.min(), s.index.max(), freq="Q"))
    x = np.log(full) if log else full
    xi = x.interpolate(method="linear", limit_area="inside")
    out = np.exp(xi) if log else xi
    marca = full.isna() & out.notna()
    return out.reindex(PER), marca.reindex(PER, fill_value=False).astype(bool)


def nivel_dia(df: pd.DataFrame, serie: str) -> pd.Series:
    """Tipos oficiales con fechas de cambio -> media trimestral ponderada por días (nivel vigente cada día)."""
    s = df.loc[df["serie"] == serie].dropna(subset=["valor"]).copy()
    s["f"] = pd.to_datetime(s["fecha"])
    s = s.sort_values("f").drop_duplicates("f", keep="last").set_index("f")["valor"]
    d = s.reindex(pd.date_range(s.index.min(), f"{FIN[:4]}-06-30", freq="D")).ffill()
    return d.groupby(d.index.to_period("Q")).mean().reindex(PER)


def anade_interp(N: pd.DataFrame, var: str, serie: pd.Series, marca: pd.Series, metodo: str) -> None:
    N[var] = serie.reindex(PER)
    N[var + "_interp"] = marca.reindex(PER, fill_value=False).astype(bool)
    INTERP_INFO[var] = dict(metodo=metodo, n=int(N[var + "_interp"].sum()))


def clave_trim(idx) -> list[str]:
    return [f"{p.year}Q{p.quarter}" for p in idx]


# ------------------------------------------------------------------------------------------------------------- NACIONAL
def construir_nacional() -> pd.DataFrame:
    N = pd.DataFrame(index=PER)

    # ---- precio de compra
    vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
    N["p_tasado"] = sq(vt, "valor_tasado_libre_nacional")
    reg("p_tasado", "Valor tasado medio de la vivienda libre, total nacional (medida principal de precio de compra)", "euros/m2",
        "mivau_valor_tasado_nacional_ccaa_prov.csv (serie valor_tasado_libre_nacional)", rupturas="ninguna conocida")
    bde = rd("bde_precio_vivienda_libre.csv")
    N["p_bde"] = sq(bde, "DHIVTNOAPLPMMUVT_RLI.T")
    reg("p_bde", "Precio medio m2 viviendas libres tasadas, total nacional (BdE; trimestre = mes de cierre)", "euros/m2",
        "bde_precio_vivienda_libre.csv (DHIVTNOAPLPMMUVT_RLI.T)", rupturas="ninguna conocida")
    N["p_bde_nueva"] = sq(bde, "DHIVTNOAPLPMMUVT_VVN_RLI.T")
    N["p_bde_usada"] = sq(bde, "DHIVTNOAPLPMMUVT_VVU_RLI.T")
    reg("p_bde_nueva", "Precio medio m2 tasado, viviendas hasta 5 años (BdE)", "euros/m2", "bde_precio_vivienda_libre.csv (VVN)")
    reg("p_bde_usada", "Precio medio m2 tasado, viviendas de más de 5 años (BdE)", "euros/m2", "bde_precio_vivienda_libre.csv (VVU)")
    ipv = rd("ine_ipv_80270.csv")
    N["ipv"] = sq(ipv, "IPV1209")
    N["ipv_nueva"] = sq(ipv, "IPV1613")
    N["ipv_usada"] = sq(ipv, "IPV1618")
    reg("ipv", "Índice de precios de vivienda INE, general, nacional (base 2015=100)", "índice", "ine_ipv_80270.csv (IPV1209)",
        metodo="original; la tabla 25171 (base 2007) es la misma serie reescalada (cociente constante 1,7990) y no añade historia anterior a 2007T1: sin enlace necesario",
        rupturas="cambio de base ya resuelto por INE")
    reg("ipv_nueva", "IPV INE, vivienda nueva, nacional", "índice", "ine_ipv_80270.csv (IPV1613)")
    reg("ipv_usada", "IPV INE, vivienda segunda mano, nacional", "índice", "ine_ipv_80270.csv (IPV1618)")
    # Registradores (compraventas, media móvil 4T) y Notariado (semestral)
    rg = rd("pdf/registradores_opendata_compraventas.csv")
    rg = rg[rg["nivel"] == "nacional"]
    N["registr_pm2_4tm"] = sq(rg, "compraventas_viv_pm2_4T_movil")
    N["registr_num_4tm"] = sq(rg, "compraventas_viv_num_4T_movil")
    reg("registr_pm2_4tm", "Precio medio m2 de las compraventas de vivienda inscritas, media móvil de 4 trimestres (Registradores)", "euros/m2",
        "pdf/registradores_opendata_compraventas.csv", metodo="media móvil de 4T ya calculada en origen (suaviza; no interpolada por nosotros)",
        rupturas="suavizado de 4T en origen")
    reg("registr_num_4tm", "Compraventas de vivienda inscritas, suma móvil de 4 trimestres (Registradores)", "número",
        "pdf/registradores_opendata_compraventas.csv", metodo="suma móvil 4T en origen")
    nt = rd("pdf/notariado_cgn_extranjeros_semestral.csv")
    nt = nt[(nt["territorio"] == "Espana") & (nt["categoria"] == "Total general")]
    for ser, var in (("precio_m2", "notariado_pm2_sem"), ("op_viv_libre", "notariado_op_sem")):
        s = nt[nt["serie"] == ser]
        # semestre S1 -> Q2, S2 -> Q4 (dato referido al semestre, asignado a su último trimestre; sin interpolar)
        idx = pd.PeriodIndex([f"{p[:4]}Q{2 if p.endswith('S1') else 4}" for p in s["periodo"]], freq="Q")
        N[var] = pd.Series(s["valor"].to_numpy(float), index=idx).sort_index().reindex(PER)
    reg("notariado_pm2_sem", "Precio medio m2 de las compraventas de vivienda libre ante notario, total, dato semestral asignado al último trimestre del semestre (T2, T4)",
        "euros/m2", "pdf/notariado_cgn_extranjeros_semestral.csv (precio_m2, Total general)",
        metodo="semestral; sin interpolación (NaN en T1 y T3)", rupturas="frecuencia semestral")
    reg("notariado_op_sem", "Operaciones de compraventa de vivienda libre ante notario, total, semestral (T2, T4)", "número",
        "pdf/notariado_cgn_extranjeros_semestral.csv (op_viv_libre)", metodo="semestral; sin interpolación")

    # ---- alquiler
    al = rd("ine_ipc_alquiler.csv")
    N["ipc_alquiler"] = m2q(sm(al, "IPC290887"), "mean")
    reg("ipc_alquiler", "IPC, alquiler de vivienda, nacional (índice; media trimestral de los 3 índices mensuales)", "índice (base INE)",
        "ine_ipc_alquiler.csv (IPC290887)", metodo="agregación temporal: media de 3 meses; NaN si falta algún mes", rupturas="cambio metodológico IPC base 2021 resuelto por INE")

    # ---- deflactores
    ipc_m = sm(rd("v8/ine_ipc_24077_general.csv"), "IPC290751")
    hic = sm(rd("ecb_hicp_es.csv"), "ICP.M.ES.N.000000.4.ANR")
    mensual = ipc_m.copy()
    for m in pd.period_range("1995-01", "2001-12", freq="M")[::-1]:   # retropolación con la tasa interanual del IPCA (BCE)
        mensual[m] = mensual[m + 12] / (1 + hic[m + 12] / 100)
    mensual = mensual.sort_index()
    retro = pd.Series(mensual.index < pd.Period("2002-01", "M"), index=mensual.index)
    ipc_q = m2q(mensual, "mean")
    base = ipc_q[(ipc_q.index.year == 2015)].mean()
    N["ipc_general"] = ipc_q / base * 100
    marca = pd.Series(pd.PeriodIndex(retro.index.to_timestamp(), freq="Q"), index=retro.index)
    q_retro = retro.groupby(marca.values).any().reindex(PER, fill_value=False)
    N["ipc_general_interp"] = q_retro.astype(bool)
    INTERP_INFO["ipc_general"] = dict(metodo="retropolación 1995T1-2001T4 con tasas interanuales del IPCA de España (ecb_hicp_es); 2002+ índice INE", n=int(N["ipc_general_interp"].sum()))
    reg("ipc_general", "IPC general nacional, media trimestral, 2015=100 (deflactor principal)", "índice 2015=100",
        "v8/ine_ipc_24077_general.csv (IPC290751) 2002+; ecb_hicp_es.csv (tasa interanual IPCA) para 1995-2001",
        metodo="media trimestral de índices mensuales; antes de 2002 se encadena hacia atrás P(t-12)=P(t)/(1+tasa IPCA(t)); marcada ipc_general_interp",
        rupturas="empalme IPC/IPCA en 2002T1")
    hq = m2q(hic, "mean")
    N["hicp_yoy"] = hq
    reg("hicp_yoy", "Tasa de variación anual del IPCA de España, media trimestral", "% anual", "ecb_hicp_es.csv", metodo="media de 3 meses; la serie termina en 2025T4")

    # ---- CNT: PIB, deflactor, renta
    cc = rd("ine_cnt_demanda_corrientes.csv")
    cv = rd("ine_cnt_demanda_volumen.csv")
    N["pib_nom"] = sq(cc, "CNTR6597")
    N["pib_vol_idx"] = sq(cv, "CNTR6652")
    defl = N["pib_nom"] / N["pib_vol_idx"]
    N["deflactor_pib"] = defl / defl[defl.index.year == 2015].mean() * 100
    reg("pib_nom", "PIB a precios de mercado, precios corrientes, ajustado de estacionalidad y calendario (INE)", "millones de euros",
        "ine_cnt_demanda_corrientes.csv (CNTR6597)", metodo="ajuste estacional realizado por INE")
    reg("pib_vol_idx", "PIB, índice de volumen encadenado, ajustado de estacionalidad y calendario (INE)", "índice", "ine_cnt_demanda_volumen.csv (CNTR6652)")
    reg("deflactor_pib", "Deflactor implícito del PIB = PIB corriente / índice de volumen, 2015=100 (deflactor alternativo)", "índice 2015=100",
        "ine_cnt_demanda_corrientes.csv + ine_cnt_demanda_volumen.csv", metodo="cociente y reescalado a la media de 2015")
    rd_ = rd("ine_cnt_renta_disponible.csv")
    N["rdb"] = sq(rd_, "CTNFSI11113")
    reg("rdb", "Renta disponible bruta del total de la economía, ajustada de estacionalidad (INE); NO es renta de los hogares", "millones de euros",
        "ine_cnt_renta_disponible.csv (CTNFSI11113)", metodo="ajuste estacional por INE; el fichero solo contiene el total de la economía (límite: no hay sector hogares)")

    # ---- demanda: empleo, población, hogares, salarios
    N["ocupados"] = sq(rd("ine_epa_ocupados.csv"), "EPA387796")
    reg("ocupados", "Ocupados EPA, total nacional (media del trimestre)", "miles de personas", "ine_epa_ocupados.csv (EPA387796)",
        rupturas="2021T1: cambio de base poblacional y metodología de la EPA (variable ficticia epa2021)")
    ecp = rd("ine_ecp_nacional.csv")
    pt, f_pt = interp_lin(sq(ecp, "ECP320"))
    anade_interp(N, "pob_total", pt, f_pt, "interpolación lineal entre fechas observadas (semestrales hasta 2020, trimestrales después)")
    reg("pob_total", "Población residente total (ECP/INE)", "personas", "ine_ecp_nacional.csv (ECP320)",
        metodo="interpolación lineal trimestral entre observaciones semestrales; sin extrapolar", rupturas="ninguna")
    pe_ine, f_ine = interp_lin(sq(ecp, "ECP701"))
    anade_interp(N, "pob_extranj_ine", pe_ine, f_ine, "interpolación lineal entre fechas observadas (semestrales hasta 2020)")
    reg("pob_extranj_ine", "Población residente de nacionalidad extranjera (ECP/INE)", "personas", "ine_ecp_nacional.csv (ECP701)",
        metodo="interpolación lineal trimestral entre observaciones semestrales; sin extrapolar", rupturas="ninguna")
    eu = rd("v8/eurostat_migr_pop1ctz_es.csv")
    tot = eu[eu["codigo"] == "TOTAL"].set_index(pd.to_datetime(eu[eu["codigo"] == "TOTAL"]["fecha"]).dt.year)["valor"]
    nat = eu[eu["codigo"] == "NAT"].set_index(pd.to_datetime(eu[eu["codigo"] == "NAT"]["fecha"]).dt.year)["valor"]
    ext_a = (tot - nat).dropna()
    ext_a.index = pd.PeriodIndex([f"{y}Q1" for y in ext_a.index], freq="Q")     # stock a 1 de enero -> Q1
    pe_eu, f_eu = interp_lin(ext_a)
    anade_interp(N, "pob_extranj", pe_eu, f_eu, "interpolación lineal entre stocks anuales de 1 de enero (Q1)")
    reg("pob_extranj", "Población extranjera = total - nacionales, a 1 de enero (Eurostat migr_pop1ctz), interpolada linealmente a trimestral",
        "personas", "v8/eurostat_migr_pop1ctz_es.csv (códigos TOTAL y NAT)",
        metodo="stock de 1 de enero asignado a Q1 e interpolación lineal trimestral entre años; sin extrapolar (termina en 2025T1); marcada pob_extranj_interp",
        rupturas="ninguna")
    im = rd("eurostat_inmigracion_anual.csv")
    ima = im[im["serie"] == "A|TOTAL|REACH|TOTAL|NR|T|ES"]
    ima = pd.Series(ima["valor"].to_numpy(float), index=pd.to_datetime(ima["fecha"]).dt.year).sort_index()
    anade_interp(N, "inmig_anual", y2q_asignado(ima), y2q_asignado(ima).notna(), "valor anual asignado a los 4 trimestres (escalón)")
    reg("inmig_anual", "Inmigración anual desde el extranjero, total (Eurostat migr_imm1ctz), valor anual asignado a cada trimestre del año", "personas/año",
        "eurostat_inmigracion_anual.csv (A|TOTAL|REACH|TOTAL|NR|T|ES)",
        metodo="desagregación en escalón (mismo valor anual en los 4 trimestres); todos los valores marcados inmig_anual_interp; 1998-2024",
        rupturas="posibles cambios de definición de residente entre años")
    hog = rd("ine_epa_hogares.csv")
    N["hogares_epa"] = sq(hog, "EPA430446")
    reg("hogares_epa", "Hogares (EPA), total nacional", "miles de hogares", "ine_epa_hogares.csv (EPA430446)", rupturas="2021T1: cambio EPA (epa2021)")
    hg = rd("ine_hogares_60131.csv")
    N["hogares_ecp"] = sq(hg, "ECP355533") / 1000
    reg("hogares_ecp", "Hogares en viviendas familiares (ECP, proyección/estimación INE), total nacional", "miles de hogares", "ine_hogares_60131.csv (ECP355533)",
        metodo="dividido por 1000 desde número de hogares", rupturas="serie corta desde 2021T1")
    sal_old = sq(rd("v8/ine_etcl_6067_nacional.csv"), "ETCL5741")
    et = rd("v8/ine_etcl_79662_ccaa.csv")
    snew = et[(et["territorio"] == "Total Nacional") & et["nombre"].str.contains("Industria, construcción y servicios") & et["nombre"].str.contains("Coste salarial total")]
    assert snew["serie"].nunique() == 1
    sal_new = sq(snew, snew["serie"].iloc[0])
    assert sal_old.index.max() < sal_new.index.min(), "ETCL: hay solape, revisar enlace por ratio"
    N["salario"] = pd.concat([sal_old, sal_new]).reindex(PER)
    N["etcl2008"] = (N.index >= pd.Period("2008Q1", "Q")).astype(int)
    N["salario_enlace_sin_solape"] = pd.Series(N.index < pd.Period("2008Q1", "Q"), index=N.index)
    N.loc[N["salario"].isna(), "salario_enlace_sin_solape"] = False
    reg("salario", "Coste salarial total por trabajador y mes, industria, construcción y servicios (ETCL, INE); 2000T1-2007T4 tabla 6067 y 2008T1+ tabla 79662",
        "euros/mes", "v8/ine_etcl_6067_nacional.csv (ETCL5741) + v8/ine_etcl_79662_ccaa.csv (Total Nacional)",
        metodo="concatenación SIN enlace: las dos tablas no se solapan (2000T1-2007T4 frente a 2008T1+), así que no hay ratio; ruptura declarada con etcl2008; marca salario_enlace_sin_solape en el tramo previo",
        rupturas="2008T1: cambio de base/clasificación (CNAE-93 a CNAE-2009) y de tabla; niveles no comparables sin cautela")
    reg("etcl2008", "Variable ficticia 1 desde 2008T1 (ruptura de la serie de salarios ETCL)", "0/1", "construida")
    reg("salario_enlace_sin_solape", "Marca: valor de salario del tramo 2000T1-2007T4 concatenado sin enlace por ratio", "booleano", "construida")

    # ---- financieras
    N["tipo_hip_bde"] = m2q(sm(rd("bde_tipo_hipotecario_referencia.csv"), "D_1T9H0000"), "mean")
    reg("tipo_hip_bde", "Tipo medio de adquisición de vivienda libre, más de 3 años, conjunto de entidades (BdE), media trimestral", "% anual",
        "bde_tipo_hipotecario_referencia.csv (D_1T9H0000)", metodo="media de 3 meses (NaN si falta alguno); desde 1990T4",
        rupturas="posible cambio de definición del tipo de referencia en 2003 (circular BdE)")
    N["tipo_hip_bce"] = m2q(sm(rd("ecb_tipo_hipotecario_es.csv"), "MIR.M.ES.B.A2C.AM.R.A.2250.EUR.N"), "mean")
    reg("tipo_hip_bce", "Tipo de interés (TAE) de nuevas operaciones de crédito para adquisición de vivienda, España (BCE MIR), media trimestral", "% anual",
        "ecb_tipo_hipotecario_es.csv", metodo="media de 3 meses; desde 2003")
    N["tipo_hip_nuevas_tae"] = m2q(sm(rd("bde_tipos_hipotecas_nuevas.csv"), "DN_1TI2T0082"), "mean")
    reg("tipo_hip_nuevas_tae", "TAE de nuevas operaciones de crédito a la vivienda, hogares (BdE), media trimestral", "% anual",
        "bde_tipos_hipotecas_nuevas.csv (DN_1TI2T0082)", metodo="media de 3 meses; desde 2003")
    N["euribor_1y"] = m2q(sm(rd("ecb_euribor1y.csv"), "FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"), "mean")
    reg("euribor_1y", "Euríbor a 1 año, media trimestral", "% anual", "ecb_euribor1y.csv", metodo="media de 3 meses")
    e3 = rd("v8/ecb_tipos_euribor3m_depo.csv")
    N["euribor_3m"] = m2q(sm(e3, "FM.M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA"), "mean")
    reg("euribor_3m", "Euríbor a 3 meses, media trimestral", "% anual", "v8/ecb_tipos_euribor3m_depo.csv", metodo="media de 3 meses")
    N["tipo_dfr"] = nivel_dia(e3, "FM.B.U2.EUR.4F.KR.DFR.LEV")
    N["tipo_mro"] = nivel_dia(rd("ecb_tipo_oficial.csv"), "FM.B.U2.EUR.4F.KR.MRR_FR.LEV")
    reg("tipo_dfr", "Tipo de la facilidad de depósito del BCE, media trimestral ponderada por días", "% anual", "v8/ecb_tipos_euribor3m_depo.csv",
        metodo="el fichero trae fechas de cambio: nivel vigente cada día y media del trimestre (no interpolación)", rupturas="política de tipos negativos desde 2014T2")
    reg("tipo_mro", "Tipo de las operaciones principales de financiación (MRO) del BCE, media trimestral ponderada por días", "% anual", "ecb_tipo_oficial.csv",
        metodo="fechas de cambio -> nivel diario -> media trimestral")
    cn = sm(rd("ecb_nuevo_credito_vivienda_es.csv"), "MIR.M.ES.B.A2C.A.B.A.2250.EUR.N")
    N["credito_nuevo"] = m2q(cn, "sum")
    reg("credito_nuevo", "Nuevo crédito a la vivienda (volumen de nuevas operaciones), España, suma trimestral", "millones de euros",
        "ecb_nuevo_credito_vivienda_es.csv", metodo="suma de 3 meses; desde 2003")
    N["credito_stock_ecb"] = fin_trim(sm(rd("ecb_stock_credito_vivienda_es.csv"), "BSI.M.ES.N.A.A22.A.1.U2.2250.Z01.E"))
    reg("credito_stock_ecb", "Saldo vivo de crédito a la vivienda, IFM España (BCE BSI), fin de trimestre", "millones de euros",
        "ecb_stock_credito_vivienda_es.csv", metodo="valor del último mes del trimestre (mar/jun/sep/dic)")
    bc = rd("bde_credito_finalidad.csv")
    bl = bc[bc["serie"] == "DF_MESNAA22A1U62251Z01E"]
    unidad = bl["unidad"].iloc[0]
    esc = 1.0 if "illones" in unidad else 1e-3    # miles de euros -> millones
    N["credito_stock_bde"] = fin_trim(sm(bc, "DF_MESNAA22A1U62251Z01E") * esc)
    reg("credito_stock_bde", "Saldo de crédito a la vivienda de hogares, entidades de crédito (BdE be1916), fin de trimestre (primer dato 1997T3)", "millones de euros",
        "bde_credito_finalidad.csv (DF_MESNAA22A1U62251Z01E)", metodo=f"valor del último mes del trimestre (los primeros años solo traen meses de cierre); unidad original: {unidad}; escalado a millones")
    ca = rd("v5/ca_bde_be0418_credito_actividad.csv")
    for ser, var, txt in (("D_MEE61010", "credito_construccion", "construcción"), ("D_MEE61013", "credito_inmobiliario", "actividades inmobiliarias")):
        sq_ = ca[ca["serie"] == ser]
        u = sq_["unidad"].iloc[0]
        s = sq(ca, ser) * (1e-3 if "iles" in u else 1.0)
        N[var] = s.reindex(PER)
        reg(var, f"Saldo de crédito de entidades de crédito a {txt} (promotores y constructoras), fin de trimestre", "millones de euros",
            "v5/ca_bde_be0418_credito_actividad.csv (" + ser + ")",
            metodo=f"dato trimestral de fin de periodo; unidad original {u}; escalado a millones. NO está en bde_credito_finalidad.csv (solo hogares); se toma del fichero de v5")
    N["credito_promotor"] = N["credito_construccion"] + N["credito_inmobiliario"]
    reg("credito_promotor", "Crédito a construcción + actividades inmobiliarias (proxy de crédito a promotores)", "millones de euros", "v5/ca_bde_be0418_credito_actividad.csv",
        metodo="suma de las dos series")
    bls = rd("v8/ecb_bls_es_vivienda.csv")
    for ser, var, txt in (("Q.ES.ALL.Z.H.H.B3.ST.S.FNET", "bls_criterios_neto", "criterios de concesión (oferta), porcentaje neto (endurecimiento menos relajación)"),
                          ("Q.ES.ALL.Z.H.H.B3.ST.S.DINX", "bls_criterios_dif", "criterios de concesión (oferta), índice de difusión"),
                          ("Q.ES.ALL.Z.H.H.B3.ZZ.D.FNET", "bls_demanda_neto", "demanda de préstamos, porcentaje neto"),
                          ("Q.ES.ALL.Z.H.H.B3.ZZ.D.DINX", "bls_demanda_dif", "demanda de préstamos, índice de difusión"),
                          ("Q.ES.ALL.Z.H.H.B3.RA.D.FNET", "bls_rechazo_neto", "solicitudes rechazadas, porcentaje neto (desde 2015T2)"),
                          ("Q.ES.ALL.Z.H.H.B3.RA.D.DINX", "bls_rechazo_dif", "solicitudes rechazadas, índice de difusión (desde 2015T2)")):
        N[var] = sq(bls, ser)
        reg(var, "Encuesta de préstamos bancarios (BLS), préstamos a hogares para vivienda, " + txt, "puntos", "v8/ecb_bls_es_vivienda.csv (" + ser + ")",
            metodo="trimestre de la ronda de la encuesta (referido a los 3 meses previos); la ronda de 2026T3 queda fuera de la ventana")

    # ---- externas
    jk = rd("v8/jk_shocks_ecb_mensual.csv")
    N["jk_mp"] = m2q(sm(jk, "MP_median"), "sum")
    N["jk_cbi"] = m2q(sm(jk, "CBI_median"), "sum")
    for v, t in (("jk_mp", "política monetaria (mediana)"), ("jk_cbi", "información del banco central (mediana)")):
        reg(v, f"Shock de alta frecuencia del BCE (Jarociński-Karadi), {t}, SUMA trimestral de los 3 meses", "unidad original del repositorio",
            "v8/jk_shocks_ecb_mensual.csv", metodo="suma de 3 meses; NaN si el trimestre no está completo (la serie acaba en 2025-10: 2025T4 queda NaN)")
    hpi = rd("v8/eurostat_prc_hpi_q_multi.csv")
    for g, var in (("EA19", "hpi_ea19"), ("EA20", "hpi_ea20"), ("ES", "hpi_es_eurostat")):
        N[var] = sq(hpi, f"prc_hpi_q|TOTAL|I15_Q|{g}")
        reg(var, f"Índice de precios de la vivienda Eurostat (total, 2015=100), {g}", "índice 2015=100", "v8/eurostat_prc_hpi_q_multi.csv", metodo="desde 2005T1 (ES desde 2005T4)")
    bis = rd("bis_rpp.csv")
    N["bis_hpi_xm_nom"] = sq(bis, "BIS|WS_SPP|N|628|XM|Q")
    N["bis_hpi_xm_real"] = sq(bis, "BIS|WS_SPP|R|628|XM|Q")
    N["bis_hpi_es_nom"] = sq(bis, "BIS|WS_SPP|N|628|ES|Q")
    reg("bis_hpi_xm_nom", "Precios residenciales BIS, zona euro (XM), nominal, 2010=100", "índice 2010=100", "bis_rpp.csv (BIS|WS_SPP|N|628|XM|Q)", metodo="desde 2000T1 hasta 2026T1")
    reg("bis_hpi_xm_real", "Precios residenciales BIS, zona euro (XM), real, 2010=100", "índice 2010=100", "bis_rpp.csv (BIS|WS_SPP|R|628|XM|Q)")
    reg("bis_hpi_es_nom", "Precios residenciales BIS, España, nominal, 2010=100", "índice 2010=100", "bis_rpp.csv (BIS|WS_SPP|N|628|ES|Q)")
    tx_e = rd("mivau_transacciones_extranjeros.csv")
    N["tx_extranj"] = sq(tx_e, "tx_extranj_residentes_total_nacional")
    reg("tx_extranj", "Transacciones de vivienda adquiridas por extranjeros residentes, total nacional (MIVAU, tabla 1.6.5)", "número",
        "mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_nacional)",
        metodo="original trimestral desde 2007T1; OBSERVACIÓN: 2026T1 y 2026T2 de la serie libre nacional repiten el mismo valor (15981) en el origen",
        rupturas="solo residentes (no incluye no residentes)")
    fr = rd("v8/ine_frontur_10823_ccaa.csv")
    N["turistas"] = m2q(sm(fr, "FREG286"), "sum")
    reg("turistas", "Turistas internacionales llegados a España, total (FRONTUR, dato base mensual), suma trimestral", "personas",
        "v8/ine_frontur_10823_ccaa.csv (FREG286, Total Nacional); el fichero ine_frontur_10822_pais.csv solo trae desglose por país de residencia (no el total)",
        metodo="suma de 3 meses; desde 2015T4", rupturas="serie corta (desde 2015-10)")

    # ---- oferta
    vi = rd("mivau_visados.csv")
    vi_m = m2q(sm(vi[vi["nivel"] == "nacional"], "viv_libres_iniciadas_nacional"), "sum")
    w2 = rd("mivau_v2_iniciadas_terminadas_prov.csv")
    ini_a = w2[w2["serie"] == "viv_libres_iniciadas_anual_nacional"]
    ini_a = pd.Series(ini_a["valor"].to_numpy(float), index=pd.to_datetime(ini_a["fecha"]).dt.year).sort_index()
    vis_a = y2q_asignado(ini_a) / 4
    vis = vi_m.copy()
    marca = vis.isna() & (N.index < pd.Period("2008Q1", "Q")) & vis_a.notna()
    vis[marca] = vis_a[marca]
    anade_interp(N, "visados", vis, marca, "anual/4 para 1995T1-2007T4 (tabla anual 3.1 del MIVAU); mensual agregado desde 2008")
    reg("visados", "Viviendas libres iniciadas (visados de dirección de obra), nacional, flujo trimestral (MIVAU tabla 3.1)", "viviendas",
        "mivau_visados.csv (mensual 2008+, suma de 3 meses) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025)",
        metodo="2008T1+: suma de 3 meses (NaN si falta alguno); 1995T1-2007T4: total anual / 4 (desagregación uniforme, marcada visados_interp); sin extrapolar",
        rupturas="enlace anual/mensual en 2008T1; perfil trimestral previo a 2008 plano dentro de cada año")
    te = rd("mivau_fin_obra.csv")
    te_m = m2q(sm(te[te["nivel"] == "nacional"], "viv_libres_terminadas_nacional"), "sum")
    ter_a = w2[w2["serie"] == "viv_libres_terminadas_anual_nacional"]
    ter_a = pd.Series(ter_a["valor"].to_numpy(float), index=pd.to_datetime(ter_a["fecha"]).dt.year).sort_index()
    ter_q = y2q_asignado(ter_a) / 4
    mt = te_m.isna() & (N.index < pd.Period("2008Q1", "Q")) & ter_q.notna()
    te_m[mt] = ter_q[mt]
    anade_interp(N, "terminadas", te_m, mt, "anual/4 para 1995T1-2007T4 (tabla anual 3.2 del MIVAU); mensual agregado desde 2008")
    reg("terminadas", "Viviendas libres terminadas, nacional, flujo trimestral (MIVAU tabla 3.2)", "viviendas",
        "mivau_fin_obra.csv (mensual 2008+) y mivau_v2_iniciadas_terminadas_prov.csv (anual 1991-2025)",
        metodo="2008T1+: suma de 3 meses; 1995T1-2007T4: total anual / 4, marcada terminadas_interp", rupturas="enlace anual/mensual en 2008T1")
    cos = rd("eurostat_costes.csv")
    N["costes_constr"] = sq(cos, "Q|COST|CPA_F41001_X_410014|NSA|I21|ES")
    reg("costes_constr", "Índice de costes de construcción de edificios residenciales, España (Eurostat sts_copi_q, 2021=100, sin ajustar)", "índice 2021=100", "eurostat_costes.csv")
    tt = rd("mivau_transacciones_total.csv")
    N["tx_total"] = sq(tt[tt["nivel"] == "nacional"], "tx_total_nacional")
    reg("tx_total", "Transacciones inmobiliarias de vivienda, total nacional (MIVAU)", "número", "mivau_transacciones_total.csv", metodo="trimestral original; termina en 2026T1")
    et_ = rd("ine_etdp_compraventas.csv")
    cvta = et_[et_["serie"] == "ETDP1826"].dropna(subset=["valor"]).copy()
    cvta["f"] = pd.to_datetime(cvta["fecha"])
    N["compraventas_ine"] = m2q(pd.Series(cvta["valor"].to_numpy(float), index=pd.PeriodIndex(cvta["f"], freq="M")).sort_index(), "sum")
    reg("compraventas_ine", "Compraventas de vivienda, total nacional (ETDP, INE), suma trimestral", "número", "ine_etdp_compraventas.csv (ETDP1826)",
        metodo="suma de 3 meses; desde 2007T1")
    vu = rd("ine_vut_nacional_ccaa_prov.csv")
    for ser, var, txt, uni in (("ine_vut_total_nacional_viviendas_turisticas", "vut_viviendas", "Viviendas de uso turístico (VUT), total nacional", "viviendas"),
                               ("ine_vut_total_nacional_plazas", "vut_plazas", "Plazas en VUT, total nacional", "plazas")):
        s = vu[vu["serie"] == ser].dropna(subset=["valor"])
        so = pd.Series(s["valor"].to_numpy(float), index=pd.PeriodIndex(s["periodo"], freq="M").asfreq("Q")).sort_index()
        so = so[~so.index.duplicated(keep="last")]
        x, m = interp_lin(so, log=True)
        anade_interp(N, var, x, m, "interpolación log-lineal entre cortes semestrales (2020-08 ... 2026-05); sin extrapolar")
        reg(var, txt + " (estadística experimental INE)", uni, "ine_vut_nacional_ccaa_prov.csv (" + ser + ")",
            metodo="cortes semestrales asignados a su trimestre e interpolación log-lineal entre cortes; observaciones originales con _interp = False; antes de 2020T3 NaN",
            rupturas="serie experimental desde 2020-08; la edición 2024-11 es un corte extra")

    return N


# ------------------------------------------------------------------------------------------------------------- derivadas
def derivadas_nacional(N: pd.DataFrame) -> pd.DataFrame:
    N = N.copy()
    ipc = N["ipc_general"] / 100
    dfl = N["deflactor_pib"] / 100
    # logs de niveles
    niveles = ["p_tasado", "p_bde", "p_bde_nueva", "p_bde_usada", "ipv", "ipv_nueva", "ipv_usada", "registr_pm2_4tm", "notariado_pm2_sem", "ipc_alquiler", "ipc_general",
               "deflactor_pib", "pib_nom", "pib_vol_idx", "rdb", "ocupados", "pob_total", "pob_extranj", "pob_extranj_ine", "hogares_epa", "hogares_ecp", "salario",
               "credito_nuevo", "credito_stock_ecb", "credito_stock_bde", "credito_construccion", "credito_inmobiliario", "credito_promotor", "visados", "terminadas",
               "costes_constr", "tx_total", "compraventas_ine", "tx_extranj", "turistas", "hpi_ea19", "hpi_ea20", "hpi_es_eurostat", "bis_hpi_xm_nom", "bis_hpi_xm_real",
               "bis_hpi_es_nom", "vut_viviendas", "vut_plazas", "inmig_anual"]
    for c in niveles:
        N["ln_" + c] = np.log(N[c].where(N[c] > 0))
    # logs reales (precio / IPC) y con deflactor alternativo
    for c in ("p_tasado", "p_bde", "ipv", "ipc_alquiler", "registr_pm2_4tm"):
        N["ln_" + c + "_real"] = np.log((N[c] / ipc).where(N[c] > 0))
    N["ln_p_tasado_realpib"] = np.log(N["p_tasado"] / dfl)
    N["ln_rdb_real"] = np.log(N["rdb"] / dfl)
    N["ln_salario_real"] = np.log(N["salario"] / ipc)
    N["ln_credito_nuevo_real"] = np.log(N["credito_nuevo"] / ipc)
    N["ln_credito_stock_bde_real"] = np.log(N["credito_stock_bde"] / ipc)
    # tipos: real, diferencial
    infl = 100 * (np.log(N["ipc_general"]) - np.log(N["ipc_general"].shift(4)))
    N["inflacion_ipc_yoy"] = infl
    N["tipo_hip_real_bde"] = N["tipo_hip_bde"] - infl
    N["tipo_hip_real_bce"] = N["tipo_hip_bce"] - infl
    N["dif_hip_euribor_bde"] = N["tipo_hip_bde"] - N["euribor_1y"]
    N["dif_hip_euribor_bce"] = N["tipo_hip_bce"] - N["euribor_1y"]
    # diferencias (tasas en puntos logarítmicos): d_ = trimestral, d4_ = interanual
    base_ln = [c for c in N.columns if c.startswith("ln_")]
    for c in base_ln:
        N["d_" + c] = N[c].diff(1)
        N["d4_" + c] = N[c].diff(4)
    # dummies y periodos
    N["covid"] = ((N.index >= pd.Period("2020Q2", "Q")) & (N.index <= pd.Period("2020Q4", "Q"))).astype(int)
    N["epa2021"] = (N.index >= pd.Period("2021Q1", "Q")).astype(int)
    rangos = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"), "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", FIN)}
    for p, (a, b) in rangos.items():
        N[p] = ((N.index >= pd.Period(a, "Q")) & (N.index <= pd.Period(b, "Q"))).astype(int)
    N["P_transicion"] = (N[list(rangos)].sum(axis=1) == 0).astype(int)
    N["periodo_h8"] = np.select([N[p] == 1 for p in rangos], list(rangos), default="T")
    # Tasa de paro nacional EPA (revisión F4, J8): se AÑADE al final; el resto de columnas no cambia
    ep = rd("ine_v2_epa_prov.csv", dtype={"codigo": str})
    ep = ep[(ep["codigo"] == "00") & (ep["nivel"] == "nacional")]
    par = pd.Series(ep.loc[ep["medida"] == "EPA_parados", "valor"].to_numpy(float),
                    index=per_q(ep.loc[ep["medida"] == "EPA_parados", "fecha"])).sort_index()
    ocu = pd.Series(ep.loc[ep["medida"] == "EPA_ocupados", "valor"].to_numpy(float),
                    index=per_q(ep.loc[ep["medida"] == "EPA_ocupados", "fecha"])).sort_index()
    N["tasa_paro_epa"] = (par / (par + ocu) * 100).reindex(PER)
    reg("tasa_paro_epa", "Tasa de paro nacional EPA = parados/(parados+ocupados)×100 (código INE 00)", "%", "ine_v2_epa_prov.csv (EPA_parados, EPA_ocupados)",
        rupturas="2021T1: cambio de base poblacional y metodología de la EPA (epa2021)")
    return N


def metadatos_derivadas() -> None:
    reg("inflacion_ipc_yoy", "Inflación interanual = 100 x (ln IPC_t - ln IPC_t-4)", "% (puntos log)", "derivada de ipc_general", metodo="diferencia de 4 trimestres del log del IPC; hereda retropolación de ipc_general")
    reg("tipo_hip_real_bde", "Tipo hipotecario BdE menos inflación interanual del IPC", "puntos porcentuales", "derivada de tipo_hip_bde e ipc_general")
    reg("tipo_hip_real_bce", "Tipo hipotecario BCE (TAE nuevas operaciones) menos inflación interanual", "puntos porcentuales", "derivada de tipo_hip_bce e ipc_general")
    reg("dif_hip_euribor_bde", "Diferencial tipo hipotecario BdE - Euríbor 1 año", "puntos porcentuales", "derivada")
    reg("dif_hip_euribor_bce", "Diferencial tipo hipotecario BCE - Euríbor 1 año", "puntos porcentuales", "derivada")
    reg("covid", "Variable ficticia COVID: 1 en 2020T2-2020T4", "0/1", "construida")
    reg("epa2021", "Variable ficticia de nivel: 1 desde 2021T1 (cambio metodológico de la EPA)", "0/1", "construida")
    for p, t in (("P1", "1995T1-2007T4 expansión y crédito"), ("P2", "2008T3-2013T4 crisis financiera y ajuste"), ("P3", "2014T1-2019T4 recuperación"),
                 ("P4", "2020T2-2022T2 pandemia y reapertura"), ("P5", "2022T3-2026T2 subida de tipos y presión demográfica")):
        reg(p, f"Indicador del periodo pre-registrado {t} (hipotesis.md §3)", "0/1", "construida")
    reg("P_transicion", "Indicador de trimestres fuera de todo periodo (2008T1-2008T2 y 2020T1): se reportan, no entran en la atribución", "0/1", "construida")
    reg("periodo_h8", "Etiqueta del periodo pre-registrado (P1..P5; T = transición)", "texto", "construida")


# ------------------------------------------------------------------------------------------------------------- CCAA
def grid_ccaa() -> pd.DataFrame:
    g = pd.MultiIndex.from_product([CCAA17, PER], names=["codigo_ine_ccaa", "per"]).to_frame(index=False)
    g["trimestre"] = clave_trim(g["per"])
    return g


def a_panel(df_long: pd.DataFrame, cod: str, val: str) -> pd.DataFrame:
    out = df_long[[cod, "per", val]].copy()
    assert not out.duplicated([cod, "per"]).any(), f"duplicados (código, periodo) en {val}"
    return out


def construir_ccaa(N: pd.DataFrame) -> pd.DataFrame:
    base = pd.read_csv(V7 / "panel_ccaa_q_v7.csv", dtype={"codigo_ine_ccaa": str})
    assert set(base["codigo_ine_ccaa"]) == set(CCAA17) and not base.duplicated(["codigo_ine_ccaa", "trimestre"]).any()
    base["per"] = [pd.Period(t.replace("Q", "Q"), freq="Q") for t in base["trimestre"]]
    g = grid_ccaa()
    P = g.merge(base.drop(columns=["trimestre"]), on=["codigo_ine_ccaa", "per"], how="left")
    P["ccaa"] = [CCAA_COD_NOMBRE[c] for c in P["codigo_ine_ccaa"]]
    P["fecha"] = [p.start_time.strftime("%Y-%m-%d") for p in P["per"]]

    # valor tasado CCAA 1995+ (MIVAU; nombre -> código por diccionario)
    vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
    vt = vt[vt["nivel"] == "ccaa"].dropna(subset=["valor"]).copy()
    vt["codigo_ine_ccaa"] = [COD_MIVAU_CCAA[t] for t in vt["territorio"]]
    vt["per"] = per_q(vt["fecha"])
    vt = vt.rename(columns={"valor": "valor_tasado_ccaa"})
    P = P.merge(a_panel(vt, "codigo_ine_ccaa", "valor_tasado_ccaa"), on=["codigo_ine_ccaa", "per"], how="left")
    # turistas FRONTUR (serie INE -> código)
    fr = rd("v8/ine_frontur_10823_ccaa.csv")
    filas = []
    for ser, cod in COD_FRONTUR_SERIE.items():
        sub = fr[fr["serie"] == ser]
        # dato base: las series de dato base son FREG346.. (mensual); verificación de que son «Dato base»
        assert sub["nombre"].str.contains("Dato base").all(), ser
        qs = m2q(sm(fr, ser), "sum")
        filas.append(pd.DataFrame({"codigo_ine_ccaa": cod, "per": qs.index, "turistas_ccaa": qs.to_numpy()}))
    P = P.merge(a_panel(pd.concat(filas), "codigo_ine_ccaa", "turistas_ccaa"), on=["codigo_ine_ccaa", "per"], how="left")
    # salarios ETCL por CCAA
    et = rd("v8/ine_etcl_79662_ccaa.csv")
    et = et[et["nombre"].str.contains("Industria, construcción y servicios") & et["nombre"].str.contains("Coste salarial total")]
    filas = []
    for nombre, gdf in et.groupby("territorio"):
        if nombre not in COD_ETCL_CCAA:
            continue          # «Total Nacional» u otros agregados
        assert gdf["serie"].nunique() == 1, nombre
        s = sq(gdf, gdf["serie"].iloc[0])
        filas.append(pd.DataFrame({"codigo_ine_ccaa": COD_ETCL_CCAA[nombre], "per": s.index, "salario_ccaa": s.to_numpy()}))
    sal = pd.concat(filas)
    assert sal["codigo_ine_ccaa"].nunique() == 17
    P = P.merge(a_panel(sal, "codigo_ine_ccaa", "salario_ccaa"), on=["codigo_ine_ccaa", "per"], how="left")
    # compras de extranjeros residentes por CCAA (total)
    tx = rd("mivau_transacciones_extranjeros.csv")
    tx = tx[(tx["nivel"] == "ccaa") & tx["serie"].str.startswith("tx_extranj_residentes_total_ccaa_")].dropna(subset=["valor"]).copy()
    tx["codigo_ine_ccaa"] = [COD_MIVAU_CCAA[t] for t in tx["territorio"]]
    tx["per"] = per_q(tx["fecha"])
    tx = tx.rename(columns={"valor": "tx_extranj_ccaa"})
    P = P.merge(a_panel(tx, "codigo_ine_ccaa", "tx_extranj_ccaa"), on=["codigo_ine_ccaa", "per"], how="left")
    # columnas comunes nacionales (misma para las 17 CCAA)
    comunes = ["hpi_ea19", "hpi_ea20", "bis_hpi_xm_nom", "bis_hpi_xm_real", "ipc_general", "deflactor_pib", "jk_mp", "jk_cbi"]
    com = N[comunes].copy()
    com["per"] = com.index
    P = P.merge(com, on="per", how="left")
    for v, q in (("hpi_ea19", "Índice HPI Eurostat zona euro EA19 (común a todas las CCAA)"), ("hpi_ea20", "Índice HPI Eurostat zona euro EA20 (común)"),
                 ("bis_hpi_xm_nom", "Precios residenciales BIS zona euro, nominal (común)"), ("bis_hpi_xm_real", "Precios residenciales BIS zona euro, real (común)"),
                 ("ipc_general", "IPC general nacional 2015=100 (común, deflactor)"), ("deflactor_pib", "Deflactor del PIB 2015=100 (común)"),
                 ("jk_mp", "Shock monetario JK, suma trimestral (común)"), ("jk_cbi", "Shock de información JK, suma trimestral (común)")):
        reg("ccaa:" + v, q, META[v]["unidad"], META[v]["fuente"], metodo="columna nacional replicada en cada CCAA (mismo valor)")
    # derivadas nuevas
    P = P.sort_values(["codigo_ine_ccaa", "per"]).reset_index(drop=True)
    P["ln_valor_tasado_ccaa"] = np.log(P["valor_tasado_ccaa"])
    P["ln_valor_tasado_ccaa_real"] = np.log(P["valor_tasado_ccaa"] / (P["ipc_general"] / 100))
    P["ln_turistas_ccaa"] = np.log(P["turistas_ccaa"].where(P["turistas_ccaa"] > 0))
    P["ln_salario_ccaa"] = np.log(P["salario_ccaa"])
    P["ln_tx_extranj_ccaa"] = np.log(P["tx_extranj_ccaa"].where(P["tx_extranj_ccaa"] > 0))
    P["ln_hpi_ea20"] = np.log(P["hpi_ea20"])
    for c in ("ln_valor_tasado_ccaa", "ln_valor_tasado_ccaa_real", "ln_turistas_ccaa", "ln_salario_ccaa", "ln_tx_extranj_ccaa", "ln_hpi_ea20"):
        grp = P.groupby("codigo_ine_ccaa")[c]
        P["d_" + c] = grp.diff(1)
        P["d4_" + c] = grp.diff(4)
    # dummies y periodos (los mismos que en el nacional)
    D = N[["covid", "epa2021", "etcl2008", "P1", "P2", "P3", "P4", "P5", "P_transicion", "periodo_h8"]].copy()
    D["per"] = D.index
    P = P.merge(D, on="per", how="left")
    P["trimestre"] = clave_trim(P["per"])
    P = P.drop(columns=["per"])
    cols = ["codigo_ine_ccaa", "ccaa", "trimestre", "fecha"] + [c for c in P.columns if c not in ("codigo_ine_ccaa", "ccaa", "trimestre", "fecha")]
    return P[cols]


def meta_ccaa() -> None:
    reg("ccaa:valor_tasado_ccaa", "Valor tasado medio de vivienda libre por CCAA, desde 1995T1", "euros/m2", "mivau_valor_tasado_nacional_ccaa_prov.csv (nivel ccaa)",
        metodo="nombre -> código INE con diccionario explícito COD_MIVAU_CCAA (Navarra figura con dos grafías)", rupturas="ninguna conocida")
    reg("ccaa:turistas_ccaa", "Turistas internacionales por CCAA de destino (FRONTUR, dato base mensual), suma trimestral", "personas",
        "v8/ine_frontur_10823_ccaa.csv", metodo="FRONTUR solo publica 6 CCAA (Andalucía, Canarias, Cataluña, Illes Balears, C. Valenciana, Madrid); las 11 restantes NaN (solo «Otras CCAA» agregada, no asignable). Desde 2015T4",
        rupturas="cobertura de 6 de 17 CCAA")
    reg("ccaa:salario_ccaa", "Coste salarial total por trabajador y mes, industria, construcción y servicios, por CCAA (ETCL tabla 79662)", "euros/mes", "v8/ine_etcl_79662_ccaa.csv",
        metodo="nombre -> código INE con diccionario explícito COD_ETCL_CCAA; desde 2008T1", rupturas="2008T1 inicio de la tabla; sin enlace con la serie 2000-2007 (tabla 6067 solo nacional)")
    reg("ccaa:tx_extranj_ccaa", "Transacciones de vivienda adquiridas por extranjeros residentes por CCAA (MIVAU 1.6.5), total", "número",
        "mivau_transacciones_extranjeros.csv (tx_extranj_residentes_total_ccaa_*)", metodo="nombre -> código con COD_MIVAU_CCAA; desde 2007T1")


# ------------------------------------------------------------------------------------------------------------- CV provincias
def construir_cv(N: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    pq = pd.read_csv(V7 / "panel_prov_q_v7.csv", dtype={"cod_prov": str, "cod_ccaa": str})
    pa = pd.read_csv(V7 / "panel_prov_a_v7.csv", dtype={"cod_prov": str, "cod_ccaa": str})
    pq = pq[pq["cod_prov"].isin(CV_PROV)].copy()
    pa = pa[pa["cod_prov"].isin(CV_PROV)].copy()
    pq["per"] = [pd.Period(t, freq="Q") for t in pq["trimestre"]]
    g = pd.MultiIndex.from_product([CV_PROV, PER], names=["cod_prov", "per"]).to_frame(index=False)
    Q = g.merge(pq.drop(columns=["trimestre"]), on=["cod_prov", "per"], how="left")
    Q["cod_ccaa"] = "10"
    # valor tasado desde 1995 (MIVAU provincia; nombre -> código con diccionario)
    vt = rd("mivau_valor_tasado_nacional_ccaa_prov.csv")
    vt = vt[(vt["nivel"] == "provincia") & vt["territorio"].isin(list(COD_MIVAU_PROV))].dropna(subset=["valor"]).copy()
    vt["cod_prov"] = [COD_MIVAU_PROV[t] for t in vt["territorio"]]
    vt["per"] = per_q(vt["fecha"])
    vt = a_panel(vt.rename(columns={"valor": "vt_raw"}), "cod_prov", "vt_raw")
    Q = Q.merge(vt, on=["cod_prov", "per"], how="left")
    comp = Q.dropna(subset=["valor_tasado", "vt_raw"])
    dif = float((comp["valor_tasado"] - comp["vt_raw"]).abs().max())
    assert dif < 1e-6, f"valor_tasado v7 difiere de raw ({dif})"
    Q["valor_tasado"] = Q["vt_raw"]
    Q = Q.drop(columns=["vt_raw"])
    # VUT provincial (INE, cortes semestrales; log-lineal entre cortes, marcada)
    vu = rd("ine_vut_nacional_ccaa_prov.csv")
    for sufijo, var in (("viviendas_turisticas", "vut_viviendas"), ("plazas", "vut_plazas")):
        filas = []
        for nombre, cod in COD_VUT_PROV.items():
            s = vu[(vu["territorio"] == nombre) & vu["serie"].str.endswith("_" + sufijo) & ~vu["serie"].str.endswith("plazas_por_vivienda")].dropna(subset=["valor"])
            assert s["serie"].nunique() == 1, (nombre, sufijo)
            so = pd.Series(s["valor"].to_numpy(float), index=pd.PeriodIndex(s["periodo"], freq="M").asfreq("Q"))
            so = so[~so.index.duplicated(keep="last")].sort_index()
            x, m = interp_lin(so, log=True)
            filas.append(pd.DataFrame({"cod_prov": cod, "per": PER, var: x.to_numpy(), var + "_interp": m.to_numpy()}))
        Q = Q.merge(pd.concat(filas), on=["cod_prov", "per"], how="left")
        INTERP_INFO["cv_q:" + var] = dict(metodo="interpolación log-lineal entre cortes semestrales", n=int(Q[var + "_interp"].sum()))
        reg("cv_q:" + var, ("Viviendas de uso turístico" if sufijo.startswith("v") else "Plazas turísticas") + " por provincia (INE experimental)", "viviendas" if sufijo.startswith("v") else "plazas",
            "ine_vut_nacional_ccaa_prov.csv", metodo="nombre -> código con COD_VUT_PROV; cortes semestrales + interpolación log-lineal inside; marcada _interp", rupturas="desde 2020T3")
    # Registradores provincial (media móvil 4T)
    rg = rd("pdf/registradores_opendata_compraventas.csv")
    rg = rg[(rg["nivel"] == "provincia") & rg["territorio"].isin(list(COD_REGISTR_PROV))].copy()
    rg["cod_prov"] = [COD_REGISTR_PROV[t] for t in rg["territorio"]]
    rg["per"] = per_q(rg["fecha"])
    for ser, var in (("compraventas_viv_pm2_4T_movil", "registr_pm2_4tm"), ("compraventas_viv_num_4T_movil", "registr_num_4tm")):
        s = rg[rg["serie"] == ser].rename(columns={"valor": var})
        Q = Q.merge(a_panel(s, "cod_prov", var), on=["cod_prov", "per"], how="left")
        reg("cv_q:" + var, META[var]["definicion"] + " (provincia)", META[var]["unidad"], "pdf/registradores_opendata_compraventas.csv", metodo="nombre -> código con COD_REGISTR_PROV; media/suma móvil 4T en origen")
    # Notariado CV provincial trimestral
    nt = rd("pdf/notariado_cv_prov_trimestral.csv")
    nt = nt[nt["territorio"].isin(list(COD_NOTARIADO_PROV))].copy()
    nt["cod_prov"] = [COD_NOTARIADO_PROV[t] for t in nt["territorio"]]
    nt["per"] = per_q(nt["fecha"])
    for ser in ("viv_vendidas_esp", "viv_vendidas_ext", "cuantia_media_esp", "cuantia_media_ext"):
        var = "notariado_" + ser
        s = nt[nt["serie"] == ser].rename(columns={"valor": var})
        Q = Q.merge(a_panel(s, "cod_prov", var), on=["cod_prov", "per"], how="left")
        reg("cv_q:" + var, f"Notariado CV, {ser} (provincia)", "viviendas" if "viv" in ser else "euros", "pdf/notariado_cv_prov_trimestral.csv", metodo="nombre -> código con COD_NOTARIADO_PROV; desde 2018T1")
    # derivadas
    Q = Q.sort_values(["cod_prov", "per"]).reset_index(drop=True)
    Q["ln_valor_tasado"] = np.log(Q["valor_tasado"])
    ipc = N["ipc_general"].reindex(Q["per"]).to_numpy() / 100
    Q["ln_valor_tasado_real"] = np.log(Q["valor_tasado"] / ipc)
    for c in ("ln_valor_tasado", "ln_valor_tasado_real"):
        grp = Q.groupby("cod_prov")[c]
        Q["d_" + c] = grp.diff(1)
        Q["d4_" + c] = grp.diff(4)
    Q["trimestre"] = clave_trim(Q["per"])
    Q["fecha"] = [p.start_time.strftime("%Y-%m-%d") for p in Q["per"]]
    Q["ipc_general"] = ipc * 100
    Q = Q.drop(columns=["per"])
    Q = Q[["cod_prov", "cod_ccaa", "trimestre", "fecha"] + [c for c in Q.columns if c not in ("cod_prov", "cod_ccaa", "trimestre", "fecha")]]

    # ---- anual
    A = pa.copy()
    ser = rd("pdf/serpavi_provincias.csv", dtype={"codigo": str})
    ser = ser[ser["codigo"].isin(CV_PROV)].copy()
    ser["anio"] = pd.to_datetime(ser["fecha"]).dt.year
    for tip in ("VC", "VU"):
        for var, est, nom in (("alquiler_m2", "mediana", "serpavi_%s_alq_m2_mediana"), ("alquiler_m2", "p25", "serpavi_%s_alq_m2_p25"), ("alquiler_m2", "p75", "serpavi_%s_alq_m2_p75"),
                              ("n_contratos", "recuento", "serpavi_%s_n_contratos")):
            s = ser[(ser["tipologia"] == tip) & (ser["variable"] == var) & (ser["estadistico"] == est)][["codigo", "anio", "valor"]].rename(columns={"codigo": "cod_prov", "valor": nom % tip.lower()})
            assert not s.duplicated(["cod_prov", "anio"]).any()
            A = A.merge(s, on=["cod_prov", "anio"], how="left")
            reg("cv_a:" + nom % tip.lower(), f"SERPAVI provincia, {tip} ({'vivienda colectiva' if tip == 'VC' else 'vivienda unifamiliar'}), {var} {est}", "euros/m2/mes" if var == "alquiler_m2" else "contratos",
                "pdf/serpavi_provincias.csv", metodo="código INE de provincia directo; anual 2011-2024")
    fl = []
    for y in range(2020, 2027):
        f = pd.read_csv(RAW / "v5" / f"gva_fianzas_{y}.csv", sep=";", dtype=str)
        f["importe"] = pd.to_numeric(f["importe_fianza"], errors="coerce")
        f = f[f["cod_provincia"].isin(CV_PROV)]
        g_ = f.groupby("cod_provincia")["importe"].agg(fianzas_n="count", fianzas_importe_mediana="median", fianzas_importe_media="mean").reset_index().rename(columns={"cod_provincia": "cod_prov"})
        g_["anio"] = y
        fl.append(g_)
    fl = pd.concat(fl)
    fl["fianzas_parcial"] = fl["anio"] == 2026
    A = A.merge(fl, on=["cod_prov", "anio"], how="left")
    A["fianzas_parcial"] = A["fianzas_parcial"].fillna(False).astype(bool)
    reg("cv_a:fianzas_n", "Fianzas de arrendamiento depositadas en la GVA (número de contratos), por provincia y año", "número", "v5/gva_fianzas_AAAA.csv", metodo="recuento de filas por cod_provincia (código INE); 2026 parcial (fianzas_parcial)", rupturas="2026 incompleto")
    reg("cv_a:fianzas_importe_mediana", "Importe mediano de la fianza (proxy de una mensualidad de alquiler)", "euros", "v5/gva_fianzas_AAAA.csv")
    reg("cv_a:fianzas_importe_media", "Importe medio de la fianza", "euros", "v5/gva_fianzas_AAAA.csv")
    reg("cv_a:fianzas_parcial", "Marca: año con datos parciales (2026)", "booleano", "construida")
    A = A.sort_values(["cod_prov", "anio"]).reset_index(drop=True)
    return Q, A


# ------------------------------------------------------------------------------------------------------------- València ciudad
def construir_valencia() -> pd.DataFrame:
    v = pd.read_csv(V7.parent / "valencia.csv", dtype=str)
    v["codigo_ine"] = [COD_VALENCIA_TERR[t] if t in COD_VALENCIA_TERR else (re.search(r"(\d{7})$", t).group(1) if re.search(r"(\d{7})$", t) else None) for t in v["territorio"]]
    v = v[v["codigo_ine"].notna()].copy()
    v["nivel"] = np.where(v["codigo_ine"].str.len() == 5, "municipio", "distrito")
    v["valor"] = pd.to_numeric(v["valor"])
    v["interp"] = v["interp"].astype(str).str.lower().eq("true")
    v["parcial"] = False
    out = v[["codigo_ine", "nivel", "territorio", "periodo", "frecuencia", "variable", "valor", "origen", "rol", "metodo", "interp", "parcial"]].copy()
    out["territorio"] = out["territorio"]   # etiqueta informativa; no se usa como clave
    # fianzas GVA del municipio 46/250 (anual)
    fl = []
    for y in range(2020, 2027):
        f = pd.read_csv(RAW / "v5" / f"gva_fianzas_{y}.csv", sep=";", dtype=str)
        f = f[(f["cod_provincia"] == "46") & (f["cod_municipio"] == "250")].copy()
        f["importe"] = pd.to_numeric(f["importe_fianza"], errors="coerce")
        for var, val in (("fianzas_n", f["importe"].count()), ("fianzas_importe_mediana", f["importe"].median()), ("fianzas_importe_media", f["importe"].mean())):
            fl.append(dict(codigo_ine="46250", nivel="municipio", territorio="València (municipio)", periodo=str(y), frecuencia="anual", variable=var, valor=float(val),
                           origen="v5/gva_fianzas_AAAA.csv", rol="principal", metodo="agregado por cod_provincia=46 y cod_municipio=250", interp=False, parcial=(y == 2026)))
    out = pd.concat([out, pd.DataFrame(fl)], ignore_index=True)
    out = out.sort_values(["codigo_ine", "variable", "periodo"]).reset_index(drop=True)
    assert not out.duplicated(["codigo_ine", "variable", "periodo"]).any(), "duplicados (código, variable, periodo) en València"
    return out


# ------------------------------------------------------------------------------------------------------------- C1 / diccionario
def coincidencias(N: pd.DataFrame) -> dict:
    """Capa: C1 si dos fuentes coinciden (criterio explícito por pareja); si no, C4 de fuente única."""
    res = {}

    def niv(a, b, tol=0.05):
        x = pd.concat([N[a], N[b]], axis=1).dropna()
        return float(np.log(x.iloc[:, 0] / x.iloc[:, 1]).abs().median()) if len(x) >= 8 else np.nan, tol

    def dif(a, b, tol=0.3):
        x = pd.concat([N[a], N[b]], axis=1).dropna()
        return float((x.iloc[:, 0] - x.iloc[:, 1]).abs().median()) if len(x) >= 8 else np.nan, tol

    def cor(a, b, tol=0.9):
        x = pd.concat([np.log(N[a]).diff(4), np.log(N[b]).diff(4)], axis=1).dropna()
        return float(x.corr().iloc[0, 1]) if len(x) >= 8 else np.nan, tol

    pares = [("p_tasado", "p_bde", niv, "nivel (mediana |ln ratio|<0,05)"), ("tipo_hip_bde", "tipo_hip_bce", dif, "mediana |dif|<0,3 pp"),
             ("tipo_hip_bce", "tipo_hip_nuevas_tae", dif, "mediana |dif|<0,3 pp"), ("credito_stock_ecb", "credito_stock_bde", niv, "nivel (mediana |ln ratio|<0,05)"),
             ("pob_extranj", "pob_extranj_ine", niv, "nivel (mediana |ln ratio|<0,05)"), ("hogares_epa", "hogares_ecp", niv, "nivel (mediana |ln ratio|<0,05)"),
             ("tx_total", "compraventas_ine", niv, "nivel (mediana |ln ratio|<0,05)"), ("ipv", "p_tasado", cor, "correlación de tasas interanuales >0,9 (índice frente a nivel)"),
             ("hpi_es_eurostat", "bis_hpi_es_nom", cor, "correlación de tasas interanuales >0,9"), ("registr_pm2_4tm", "p_bde", cor, "correlación de tasas interanuales >0,9")]
    for a, b, f, txt in pares:
        val, tol = f(a, b)
        ok = (not np.isnan(val)) and ((val >= tol) if f is cor else (val < tol))
        res[(a, b)] = dict(valor=val, criterio=txt, coincide=bool(ok))
    # IPC general (INE) frente a IPCA (BCE): tasa interanual 2003-2025
    x = pd.concat([N["inflacion_ipc_yoy"], N["hicp_yoy"]], axis=1).dropna()
    val = float((x.iloc[:, 0] - x.iloc[:, 1]).abs().median())
    res[("ipc_general", "hicp_yoy")] = dict(valor=val, criterio="mediana |dif| de la inflación interanual <0,5 pp", coincide=bool(val < 0.5))
    return res


def capas(res: dict) -> dict:
    ok: dict[str, list[str]] = {}
    mal: dict[str, list[str]] = {}
    for (a, b), r in res.items():
        nota = " [valores idénticos: posible republicación de la misma serie; independencia no verificada]" if r["valor"] == 0 else ""
        for v, o in ((a, b), (b, a)):
            txt = f"{o}: {r['criterio'].replace('|', '/')}, valor {r['valor']:.3g}{nota}"
            (ok if r["coincide"] else mal).setdefault(v, []).append(txt)
    capa = {}
    for v in set(ok) | set(mal):
        capa[v] = ("C1 (coincide con " + "; ".join(ok[v]) + ")") if v in ok else ("C4 (discrepa de " + "; ".join(mal[v]) + ")")
        if v in ok and v in mal:
            capa[v] += " | discrepa de " + "; ".join(mal[v])
    return capa


def cobertura(s: pd.Series, idx_label: pd.Series) -> str:
    v = s.dropna()
    if v.empty:
        return "sin datos"
    return f"{idx_label[v.index[0]]}–{idx_label[v.index[-1]]} (N={len(v)})"


def escribe_dic(N: pd.DataFrame, P: pd.DataFrame, Q: pd.DataFrame, A: pd.DataFrame, V: pd.DataFrame, capa: dict, res: dict) -> None:
    def fila(var, meta, df, lab, prefijo=""):
        cob = cobertura(df[var], lab) if var in df.columns else "—"
        c = meta.get("capa") or capa.get(var.replace(prefijo, "")) or ("no aplica (variable construida)" if meta["fuente"] == "construida" else "C4 (fuente única)")
        t = lambda s: str(s).replace("|", "/").replace("\n", " ")
        return f"| `{var}` | {t(meta['definicion'])} | {t(meta['unidad'])} | {t(meta['fuente'])} | {cob} | {t(c)} | {t(meta['metodo'])} | {t(meta['rupturas'])} |"

    def deriva(var):
        m = re.match(r"^(d4_|d_)?(ln_)(.+)$", var)
        if not m:
            return None
        pref, _, resto = m.groups()
        defl = "realpib" if resto.endswith("_realpib") else ("real" if resto.endswith("_real") else None)
        b0 = re.sub(r"_real(pib)?$", "", resto)
        b = META.get(b0) or META.get("ccaa:" + b0) or META.get("cv_q:" + b0)
        suj = {None: f"{b0} deflactado por IPC general (2015=100)", "real": f"{b0} deflactado por IPC general (2015=100)",
               "realpib": f"{b0} deflactado por el deflactor del PIB (2015=100)"}[defl] if defl else b0
        if defl is None:
            suj = b0
        txt = {"d4_": "diferencia interanual (4 trimestres) del logaritmo natural de ", "d_": "diferencia trimestral del logaritmo natural de ", None: "logaritmo natural de "}[pref]
        return dict(definicion=f"{txt}{suj}", unidad="puntos log" if pref else "log", fuente=(b or {}).get("fuente", "derivada"), metodo="transformación; NaN donde falte el nivel",
                    rupturas=(b or {}).get("rupturas", "—"), capa=capa.get(b0), base=b0)

    hdr = "| variable | definición | unidad | fuente (data/raw) | cobertura | capa | método (enlaces, interpolaciones) | rupturas |\n|---|---|---|---|---|---|---|---|"
    L = ["# Diccionario V8-F1: paneles de datos", "",
         "Generado por `src/v8/f1_paneles.py` (no editar a mano). Muestra nacional 1995T1-2026T2 (cada variable desde su inicio disponible, NaN antes). "
         "Sin extrapolación: los huecos finales se dejan NaN. Cruces territoriales solo por código INE.", "",
         "Convenciones: `ln_` = logaritmo natural; `d_ln_` = diferencia trimestral (puntos log); `d4_ln_` = diferencia interanual; `*_interp` = booleana, True si el valor no es observado "
         "(interpolado, desagregado o retropolado). Capa: C1 si dos fuentes independientes coinciden según el criterio de la tabla de coincidencias; si no, C4 de fuente única.", "",
         "## Interpolaciones, enlaces y agregaciones temporales", "",
         "| variable | método | observaciones marcadas |", "|---|---|---|"]
    for k, i in INTERP_INFO.items():
        L.append(f"| `{k}` | {i['metodo'].replace('|', '/')} | {i['n']} |")
    L += ["", "Agregación temporal sin interpolación: mensual a trimestral por media (índices, tipos), suma (flujos, shocks JK, turistas, crédito nuevo) o último mes (saldos); "
          "se exige el trimestre completo (3 meses), si no NaN. Tipos oficiales del BCE: media del trimestre ponderada por días de vigencia.", "",
          "Huecos intermedios: visados 2016T2 y 2017T2 (faltan meses en el origen; no se completan). Huecos al final: BLS acaba en 2026T2 (la ronda 2026T3 queda fuera); JK en 2025T3 (2025T4 incompleto); IPCA en 2025T4; HPI Eurostat/BIS: BIS en 2026T1; "
          "población extranjera Eurostat en 2025T1; inmigración anual en 2024; tx_total en 2026T1.", "",
          "## Tabla de coincidencias entre fuentes (criterio de capa C1)", "", "| pareja | criterio | valor | coincide |", "|---|---|---|---|"]
    for (a, b), r in res.items():
        L.append(f"| `{a}` vs `{b}` | {r['criterio'].replace('|', '/')} | {r['valor']:.4g} | {'sí' if r['coincide'] else 'no'} |")
    L += ["", "## No encontrado / limitaciones", "",
          "- Notariado y Registradores: no hay serie trimestral nacional de precios con historia larga; se incluyen Registradores (media móvil de 4T desde 2007T1) y Notariado (semestral desde 2007S1).",
          "- Renta de los hogares: el fichero de CNT solo contiene el total de la economía (`rdb`); no hay sector hogares.",
          "- Crédito a promotores: `bde_credito_finalidad.csv` solo contiene hogares; construcción e inmobiliarias salen de `v5/ca_bde_be0418_credito_actividad.csv`.",
          "- FRONTUR por CCAA: solo 6 CCAA publicadas (resto NaN). `ine_frontur_10822_pais.csv` no trae total; el total nacional sale de la tabla 10823.",
          "- Salarios: la serie ETCL 2000-2007 (tabla 6067) y 2008+ (tabla 79662) no se solapan: no hay enlace por ratio; ruptura declarada.",
          "- Visados/terminadas antes de 2008: solo anuales (1991-2025); se reparten uniformemente por trimestre (marcado).",
          "- Compras de extranjeros: los valores de 2026T2 repiten los de 2026T1 en el origen (nacional libre y por CCAA); tratar 2026T2 con cautela.",
          "- Fianzas de Cataluña no se incluyen en este alcance (solo Comunitat Valenciana).", "",
          "## nacional_q_v8.csv (clave: trimestre)", "", hdr]
    lab = N["trimestre"]
    for c in N.columns:
        if c in ("trimestre", "fecha"):
            continue
        if c.endswith("_interp"):
            L.append(f"| `{c}` | Marca booleana: True si `{c[:-7]}` no es observado (interpolado/desagregado/retropolado) | booleano | construida | — | — | ver sección de interpolaciones | — |")
            continue
        meta = META.get(c) or deriva(c)
        if meta is None:
            meta = dict(definicion=c, unidad="—", fuente="derivada", metodo="—", rupturas="—")
        L.append(fila(c, meta, N, lab))
    L += ["", "## panel_ccaa_q_v8.csv (clave: codigo_ine_ccaa, trimestre)", "",
          "Contiene las columnas del panel v7 (ver docs/v7/diccionario.md) ampliadas a 1995T1-2026T2 (filas previas a 2007T1 con NaN en variables v7) y las siguientes.", "", hdr]
    lab = P["trimestre"]
    nuevas = [c for c in P.columns if ("ccaa:" + c) in META or c.endswith("_ccaa") or re.match(r"^(d4_|d_)?ln_(valor_tasado_ccaa|turistas_ccaa|salario_ccaa|tx_extranj_ccaa|hpi_ea20)", c)]
    nuevas += [c for c in ("covid", "epa2021", "etcl2008", "P1", "P2", "P3", "P4", "P5", "P_transicion", "periodo_h8") if c in P.columns]
    for c in dict.fromkeys(nuevas):
        meta = META.get("ccaa:" + c) or META.get(c) or deriva(c)
        L.append(fila(c, meta, P, lab, "ccaa:") if meta else f"| `{c}` | — | — | — | — | — | — | — |")
    L += ["", "## cv_prov_q_v8.csv (clave: cod_prov, trimestre; provincias 03, 12, 46)", "",
          "Panel v7 provincial (ocupados EPA, hipotecas, compraventas, IPC alquiler, iniciadas, terminadas; ver docs/v7/diccionario.md) extendido a 1995T1 y ampliado con:", "", hdr]
    lab = Q["trimestre"]
    for c in Q.columns:
        meta = META.get("cv_q:" + c)
        if meta is None and c in ("valor_tasado", "ln_valor_tasado", "ln_valor_tasado_real", "d_ln_valor_tasado", "d4_ln_valor_tasado", "d_ln_valor_tasado_real", "d4_ln_valor_tasado_real", "ipc_general"):
            meta = META.get(c) or deriva(c) or dict(definicion="Valor tasado provincial MIVAU desde 1995T1 (nombre -> código con COD_MIVAU_PROV); coincide con v7 en el solape", unidad="euros/m2",
                                                   fuente="mivau_valor_tasado_nacional_ccaa_prov.csv", metodo="original", rupturas="—")
            if c == "valor_tasado":
                meta = dict(definicion="Valor tasado medio vivienda libre provincial (MIVAU) desde 1995T1; coincide con v7 en el solape", unidad="euros/m2",
                            fuente="mivau_valor_tasado_nacional_ccaa_prov.csv", metodo="nombre -> código con COD_MIVAU_PROV", rupturas="—")
        if meta is None:
            continue
        L.append(fila(c, meta, Q, lab, "cv_q:"))
    L += ["", "## cv_prov_a_v8.csv (clave: cod_prov, anio)", "",
          "Panel anual v7 (padrón total y extranjero, hipotecas, compraventas, iniciadas/terminadas, EPA, IPC alquiler, PIB provincial, IPVA, VUT) más:", "", hdr]
    lab = A["anio"].astype(str)
    for c in A.columns:
        meta = META.get("cv_a:" + c)
        if meta is not None:
            L.append(fila(c, meta, A, lab, "cv_a:"))
    L += ["", "## valencia_ciudad_v8.csv (formato largo; clave: codigo_ine, variable, periodo)", "",
          "Códigos INE: municipio 46250 (València); distritos 46250NN con el código de 7 dígitos que trae la propia etiqueta del origen. "
          "Se reutiliza `data/processed/valencia.csv` (variables ya documentadas en docs/v5 y docs/v7) y se añaden fianzas GVA (anual, 2026 parcial).", "",
          "| variable | frecuencia | cobertura (N filas, periodos) | origen |", "|---|---|---|---|"]
    for (var, fr), g_ in V.groupby(["variable", "frecuencia"]):
        L.append(f"| `{var}` | {fr[:10]} | N={len(g_)}, {g_['periodo'].min()}–{g_['periodo'].max()}, unidades: {g_['codigo_ine'].nunique()} | {g_['origen'].iloc[0]} |")
    DOC.parent.mkdir(parents=True, exist_ok=True)
    extra = DOC.parent / "diccionario_m5.md"   # sección de los datos que descarga M5 (F4), mantenida aparte
    if extra.exists():
        L += [""] + [ln for ln in extra.read_text(encoding="utf-8").splitlines() if not ln.startswith("<!--")]
    DOC.write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------------------- main
def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    OUT_R.mkdir(parents=True, exist_ok=True)
    N = construir_nacional()
    N = derivadas_nacional(N)
    metadatos_derivadas()
    res = coincidencias(N)
    capa = capas(res)
    N = N.reset_index().rename(columns={"index": "per"})
    N["trimestre"] = clave_trim(N["per"])
    N["fecha"] = [p.start_time.strftime("%Y-%m-%d") for p in N["per"]]
    Nidx = N.set_index("per")
    Nidx.index.name = None
    meta_ccaa()
    P = construir_ccaa(Nidx)
    Q, A = construir_cv(Nidx)
    V = construir_valencia()
    N = N.drop(columns=["per"])
    N = N[["trimestre", "fecha"] + [c for c in N.columns if c not in ("trimestre", "fecha")]]
    assert not N.duplicated("trimestre").any() and len(N) == len(PER)
    N.to_csv(OUT / "nacional_q_v8.csv", index=False, float_format="%.10g")
    P.to_csv(OUT / "panel_ccaa_q_v8.csv", index=False, float_format="%.10g")
    Q.to_csv(OUT / "cv_prov_q_v8.csv", index=False, float_format="%.10g")
    A.to_csv(OUT / "cv_prov_a_v8.csv", index=False, float_format="%.10g")
    V.to_csv(OUT / "valencia_ciudad_v8.csv", index=False, float_format="%.10g")
    escribe_dic(N, P, Q, A, V, capa, res)
    claves = ["p_tasado", "p_bde", "ipv", "ipc_alquiler", "ocupados", "pob_total", "pob_extranj", "hogares_epa", "pib_nom", "rdb", "salario", "tipo_hip_bde", "tipo_hip_bce",
              "euribor_1y", "credito_nuevo", "credito_stock_bde", "credito_promotor", "bls_criterios_neto", "jk_mp", "hpi_ea20", "bis_hpi_xm_nom", "tx_extranj", "turistas",
              "visados", "terminadas", "costes_constr", "tx_total", "compraventas_ine", "vut_viviendas", "ipc_general", "deflactor_pib"]
    cob = {}
    for c in claves:
        v = N.loc[N[c].notna(), "trimestre"]
        cob[c] = dict(desde=v.iloc[0], hasta=v.iloc[-1], n=int(len(v)))
    out = dict(
        rama="v8/F1", pregunta="Construcción de los paneles de datos V8: nacional trimestral 1995T1-2026T2, 17 CCAA, Comunitat Valenciana por provincias y València ciudad",
        capa="C4", datos=[str((OUT / f).relative_to(RAIZ)) for f in ("nacional_q_v8.csv", "panel_ccaa_q_v8.csv", "cv_prov_q_v8.csv", "cv_prov_a_v8.csv", "valencia_ciudad_v8.csv")] + ["docs/v8/diccionario.md"],
        N=dict(nacional_q=len(N), ccaa_q=len(P), cv_prov_q=len(Q), cv_prov_a=len(A), valencia_ciudad=len(V)),
        metodo="reutiliza paneles v7; cruces por código INE (diccionarios nombre->código explícitos); interpolaciones marcadas *_interp", estimacion=None, ic95=None, p_ajustado=None,
        nivel_evidencia="DESCRIPTIVO",
        diagnosticos=dict(cobertura=cob, interpolaciones=INTERP_INFO, coincidencias={f"{a}|{b}": r for (a, b), r in res.items()},
                          n_vars_nacional=int(N.shape[1]), n_vars_ccaa=int(P.shape[1])),
        fuera_muestra=dict(modelo=None, rmse=None, dm_vs_ar4=None),
        notas=["sin estimación; solo datos", "salarios ETCL sin solape: ruptura 2008T1 declarada", "crédito a promotores desde v5/ca_bde_be0418_credito_actividad.csv",
               "FRONTUR por CCAA solo 6 CCAA", "ver docs/v8/diccionario.md"])
    (OUT_R / "resultado.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    return out


if __name__ == "__main__":
    r = main()
    print(json.dumps({"N": r["N"], "cobertura": r["diagnosticos"]["cobertura"]}, ensure_ascii=False, indent=1))
    sys.exit(0)
