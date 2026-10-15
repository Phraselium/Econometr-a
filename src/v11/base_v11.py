"""V11-DATOS (bloque 6): incorporación de las fuentes de V11 a la base única de V10 (`make base`).

src/v10/base.py llama a `partes()` y usa `META_V11` (variable -> unidad, fuente, capa, licencia, redistribuible).
Reglas:
- solo códigos territoriales INE (municipio de 5 dígitos, provincia de 2, sección de 10, barrio del Ajuntament);
  los restos agregados de los microdatos (PP999 «resto de provincia», PP991-PP993 tamaños de municipio del censo) y
  EXTR (residencia fuera de España) NO entran en la base y se quedan en data/raw/v11 (documentado);
- todas las capas son C4 (descriptivo); posterior_prereg lo vuelve a calcular la base con la fecha del dato;
- los recuentos muestrales (censo 2021, 10 % de hogares) llevan «muestra» en el nombre de la variable y no se elevan.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW11 = RAIZ / "data" / "raw" / "v11"
INE = "INE: reutilización con cita (Ley 37/2007)"
MUN = re.compile(r"^\d{5}$")


def _mun(s: pd.Series) -> pd.Series:
    s = s.astype(str)
    return s.str.fullmatch(r"\d{5}") & ~s.str[2:].isin(["999", "991", "992", "993"])


def partes() -> list[pd.DataFrame]:
    out = []

    def add(df, origen, prio=4):
        if df.empty:
            return
        df = df.copy()
        df["origen"], df["prioridad"] = origen, prio
        for c in ("metodo_dato", "desagregacion"):
            if c not in df:
                df[c] = "" if c == "desagregacion" else "observado"
        out.append(df)

    # EVR (1988-2021) y EMCR (2021-2024): flujos internos y exteriores por municipio y nacionalidad (suma de edades)
    for fuente, pref, y0 in (("ine_evr", "evr", None), ("ine_emcr", "emcr_md", None)):
        f = RAW11 / fuente / "saldos_internos_municipio.csv.gz"
        if f.exists():
            s = pd.read_csv(f, dtype={"cod_municipio": str})
            s = s[_mun(s.cod_municipio)].groupby(["anio", "cod_municipio", "nac"], as_index=False)[["altas", "bajas", "saldo"]].sum()
            for col in ("altas", "bajas", "saldo"):
                add(pd.DataFrame({"territorio_codigo": s.cod_municipio, "nivel": "municipio", "periodo_raw": s.anio.astype(str),
                                  "variable": f"{pref}_{col}_interno", "desagregacion": "nacionalidad=" + s.nac,
                                  "valor": s[col], "metodo_dato": "agregado de microdatos (municipios ≥10.000 hab.)"}),
                    f"data/raw/v11/{fuente}/saldos_internos_municipio.csv.gz")
        f = RAW11 / fuente / "flujos_exterior_municipio.csv.gz"
        if f.exists():
            e = pd.read_csv(f, dtype=str)
            pais = "cnac" if "cnac" in e else "pais_nacionalidad"
            e["nac"] = np.where(e[pais].str.strip() == "108", "ES", "EXT")
            cols = [c for c in e.columns if c not in ("anio", "cod_municipio", pais, "nac")]
            for c in cols:
                e[c] = pd.to_numeric(e[c])
            g = e[_mun(e.cod_municipio)].groupby(["anio", "cod_municipio", "nac"], as_index=False)[cols].sum()
            for c in cols:
                nombre = {"altas_desde_extranjero": "inmigracion_exterior", "bajas_al_extranjero": "emigracion_exterior"}.get(c, c)
                add(pd.DataFrame({"territorio_codigo": g.cod_municipio, "nivel": "municipio", "periodo_raw": g.anio,
                                  "variable": f"{pref}_{nombre}", "desagregacion": "nacionalidad=" + g.nac, "valor": g[c],
                                  "metodo_dato": "agregado de microdatos (municipios ≥10.000 hab.)"}),
                    f"data/raw/v11/{fuente}/flujos_exterior_municipio.csv.gz")
    # EMCR, tabla publicada 69767: saldos por municipio (todos los municipios) y tipo
    f = RAW11 / "ine_emcr/emcr_t69767.csv.gz"
    if f.exists():
        t = pd.read_csv(f, dtype=str)
        t = t[t.Municipios.fillna("").str.match(r"^\d{5} ")]
        add(pd.DataFrame({"territorio_codigo": t.Municipios.str[:5], "nivel": "municipio", "periodo_raw": t.Periodo,
                          "variable": "emcr_saldo_municipal", "desagregacion": "tipo=" + t["Tipo de saldo"],
                          "valor": pd.to_numeric(t.Total.str.replace(".", "", regex=False), errors="coerce")}).dropna(subset=["valor"]),
            "data/raw/v11/ine_emcr/emcr_t69767.csv.gz")
    # MNP: nacimientos, defunciones y saldo vegetativo por municipio de residencia
    f = RAW11 / "ine_mnp/mnp_municipio.csv.gz"
    if f.exists():
        m = pd.read_csv(f, dtype={"cod_municipio": str})
        m = m[_mun(m.cod_municipio)]
        for col in ("nacimientos", "defunciones", "saldo_vegetativo"):
            add(pd.DataFrame({"territorio_codigo": m.cod_municipio, "nivel": "municipio", "periodo_raw": m.anio.astype(str),
                              "variable": f"mnp_{col}", "desagregacion": "nacionalidad=" + m.nac, "valor": m[col],
                              "metodo_dato": "agregado de microdatos (municipios ≥10.000 hab.)"}), "data/raw/v11/ine_mnp/mnp_municipio.csv.gz")
    # ECP trimestral por provincia y nacionalidad (todas las edades)
    for t_, var, col_nac in ((56947, "ecp_pob_nacionalidad", "Nacionalidad"), (82104, "ecp_pob_nacionalidad", "Nacionalidad"),
                             (60129, "ecp_pob_viv_familiares_nacionalidad", "Nacionalidad")):
        f = RAW11 / f"ine_ecp/ecp_t{t_}.csv.gz"
        if not f.exists():
            continue
        d = pd.read_csv(f, dtype=str)
        edad = next(c for c in d.columns if "edad" in c.lower())
        d = d[d.Provincias.fillna("").str.match(r"^\d{2} ") & d[edad].isin(["Todas las edades", "Total"])]
        add(pd.DataFrame({"territorio_codigo": d.Provincias.str[:2], "nivel": "provincia", "periodo_raw": d.fecha,
                          "variable": var, "desagregacion": "nacionalidad=" + d[col_nac],
                          "valor": pd.to_numeric(d.Total.str.replace(".", "", regex=False), errors="coerce")}).dropna(subset=["valor"]),
            f"data/raw/v11/ine_ecp/ecp_t{t_}.csv.gz")
    # Eurostat: protección internacional y temporal, España (totales por nacionalidad = TOTAL)
    for tabla, var, filtro in (("migr_asyappctzm", "asilo_solicitantes", {"applicant": "TOTAL"}),
                               ("migr_asytpsm", "proteccion_temporal_beneficiarios", {}),
                               ("migr_asytpfm", "proteccion_temporal_concesiones", {})):
        f = RAW11 / f"eurostat_asilo/{tabla}_es.csv.gz"
        if not f.exists():
            continue
        d = pd.read_csv(f, dtype=str, keep_default_na=False)   # «NA» = Namibia
        d = d[d.citizen.isin(["TOTAL", "EXT_EU27_2020", "UA"])]
        for k, v in filtro.items():
            if k in d:
                d = d[d[k] == v]
        add(pd.DataFrame({"territorio_codigo": "00", "nivel": "nacional", "periodo_raw": d.periodo, "variable": var,
                          "desagregacion": "nacionalidad=" + d.citizen, "valor": pd.to_numeric(d.valor)}), f"data/raw/v11/eurostat_asilo/{tabla}_es.csv.gz")
    # Catastro INSPIRE: edificios, inmuebles y viviendas por sección (València, área metropolitana y capitales) y barrio
    for fich, nivel, col in (("edificios_seccion.csv.gz", "seccion", "cod_seccion"), ("edificios_barrio_valencia.csv.gz", "barrio", "cod_barrio")):
        f = RAW11 / "catastro_inspire" / fich
        if not f.exists():
            continue
        c = pd.read_csv(f, dtype={col: str}).dropna(subset=[col])
        c["uso"] = c.uso.fillna("sin_uso").str.replace(r"^\d+_", "", regex=True)
        g = c.groupby([col, "uso"], as_index=False)[["edificios", "inmuebles", "viviendas", "superficie_construida_m2"]].sum()
        for v in ("edificios", "inmuebles", "viviendas", "superficie_construida_m2"):
            add(pd.DataFrame({"territorio_codigo": g[col], "nivel": nivel, "periodo_raw": "2026-08-21",
                              "variable": f"catastro_inspire_{v}", "desagregacion": "uso=" + g.uso, "valor": g[v],
                              "metodo_dato": "agregado espacial (centro del envolvente del edificio)"}), f"data/raw/v11/catastro_inspire/{fich}")
        r = c[c.uso == "residential"].groupby([col, "periodo_construccion"], as_index=False).viviendas.sum()
        add(pd.DataFrame({"territorio_codigo": r[col], "nivel": nivel, "periodo_raw": "2026-08-21",
                          "variable": "catastro_inspire_viviendas_por_antiguedad", "desagregacion": "construccion=" + r.periodo_construccion,
                          "valor": r.viviendas, "metodo_dato": "agregado espacial"}), f"data/raw/v11/catastro_inspire/{fich}")
    # Seguridad Social: afiliados por municipio (cota inferior: suma de celdas numéricas) y celdas «<5»
    f = RAW11 / "ss_afiliacion_municipio/afiliacion_municipio_mensual.csv.gz"
    if f.exists():
        a = pd.read_csv(f, dtype={"cod_municipio": str, "mes": str})
        a = a[_mun(a.cod_municipio)]
        for col, var in (("afiliados_suma_numerica", "ss_afiliados_cota_inferior"), ("celdas_menor5", "ss_afiliados_celdas_menor5"),
                         ("construccion", "ss_afiliados_construccion_cota_inferior"), ("hosteleria", "ss_afiliados_hosteleria_cota_inferior"),
                         ("inmobiliarias", "ss_afiliados_inmobiliarias_cota_inferior")):
            add(pd.DataFrame({"territorio_codigo": a.cod_municipio, "nivel": "municipio", "periodo_raw": a.mes, "variable": var,
                              "desagregacion": "regimen=" + a.regimen, "valor": a[col],
                              "metodo_dato": "suma de celdas publicadas (excluye «<5»)"}), "data/raw/v11/ss_afiliacion_municipio/afiliacion_municipio_mensual.csv.gz")
    # Seguridad Social: afiliados extranjeros por provincia (foto anual)
    f = RAW11 / "ss_afiliacion_extranjeros/afiliados_extranjeros_provincia.csv.gz"
    if f.exists():
        x = pd.read_csv(f, dtype={"cod_provincia": str, "mes": str})
        add(pd.DataFrame({"territorio_codigo": x.cod_provincia, "nivel": "provincia", "periodo_raw": x.mes,
                          "variable": "ss_afiliados_extranjeros", "valor": x.total}),
            "data/raw/v11/ss_afiliacion_extranjeros/afiliados_extranjeros_provincia.csv.gz")
    # INE, turismo medido con móviles: turistas por municipio de destino y mes (suma de orígenes publicados)
    for nombre in ("receptor", "interno"):
        f = RAW11 / f"ine_turismo_moviles/turismo_moviles_{nombre}_municipio.csv.gz"
        if not f.exists():
            continue
        t = pd.read_csv(f, dtype={"cod_municipio": str, "mes": str})
        t = t[(t.concepto == "Turistas") & ~t.origen.fillna("").str.contains("Total", case=False)]
        g = t.groupby(["cod_municipio", "mes"], as_index=False).valor.sum()
        add(pd.DataFrame({"territorio_codigo": g.cod_municipio, "nivel": "municipio", "periodo_raw": g.mes,
                          "variable": f"ine_tmov_{nombre}_turistas", "valor": g.valor,
                          "metodo_dato": "suma de orígenes publicados (celdas secretas excluidas)"}),
            f"data/raw/v11/ine_turismo_moviles/turismo_moviles_{nombre}_municipio.csv.gz")
    # Censo 2021, microdatos (muestra 10 %): hogares por nacionalidad de la primera persona y tenencia
    f = RAW11 / "ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz"
    if f.exists():
        h = pd.read_csv(f, dtype=str)
        h["hogares_muestra"] = pd.to_numeric(h.hogares_muestra)
        h = h[_mun(h.cod_municipio)]
        g = h.groupby(["cod_municipio", "nac_primera_persona", "tenencia"], as_index=False).hogares_muestra.sum()
        add(pd.DataFrame({"territorio_codigo": g.cod_municipio, "nivel": "municipio", "periodo_raw": "2021-01-01",
                          "variable": "c21md_hogares_muestra", "desagregacion": "nacionalidad=" + g.nac_primera_persona + "|tenencia=" + g.tenencia,
                          "valor": g.hogares_muestra, "metodo_dato": "recuento muestral sin elevar (10 % de hogares)"}),
            "data/raw/v11/ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz")
    # Euskadi: viviendas y habitaciones de uso turístico inscritas (corte vigente) por municipio
    for f in sorted((RAW11 / "euskadi_vut").glob("reate_*_*.csv.gz")):
        tipo, fecha = f.name.split("_")[1], f.name.split("_")[2][:10]
        e = pd.read_csv(f, dtype=str)
        g = e.groupby("cod_municipio", as_index=False).size()
        add(pd.DataFrame({"territorio_codigo": g.cod_municipio, "nivel": "municipio", "periodo_raw": fecha,
                          "variable": f"reate_{tipo}_uso_turistico", "valor": g["size"]}), f"data/raw/v11/euskadi_vut/{f.name}")
    return out


_C = "C4"
META_V11 = {
    **{f"evr_{c}_interno": ("personas", "INE, Estadística de Variaciones Residenciales (microdatos 1988-2021; agregado propio)", _C, INE, True)
       for c in ("altas", "bajas", "saldo")},
    **{f"evr_{c}": ("personas", "INE, EVR (microdatos; altas desde y bajas al extranjero)", _C, INE, True)
       for c in ("inmigracion_exterior", "emigracion_exterior")},
    **{f"emcr_md_{c}_interno": ("personas", "INE, EMCR (microdatos 2021-2024; agregado propio)", _C, INE, True) for c in ("altas", "bajas", "saldo")},
    **{f"emcr_md_{c}": ("personas", "INE, EMCR (microdatos; migraciones exteriores)", _C, INE, True) for c in ("inmigracion_exterior", "emigracion_exterior")},
    "emcr_saldo_municipal": ("personas", "INE, EMCR, tabla 69767 (saldos por municipio)", _C, INE, True),
    **{f"mnp_{c}": ("personas", "INE, Movimiento Natural de la Población (microdatos; municipio de residencia)", _C, INE, True)
       for c in ("nacimientos", "defunciones", "saldo_vegetativo")},
    "ecp_pob_nacionalidad": ("personas", "INE, Estadística Continua de Población (56947, 82104; trimestral)", _C, INE, True),
    "ecp_pob_viv_familiares_nacionalidad": ("personas", "INE, ECP (60129; población en viviendas familiares)", _C, INE, True),
    "asilo_solicitantes": ("personas", "Eurostat, migr_asyappctzm (solicitantes de protección internacional, total de solicitudes)", _C, "Eurostat: reutilización con cita", True),
    "proteccion_temporal_beneficiarios": ("personas", "Eurostat, migr_asytpsm (beneficiarios a fin de mes)", _C, "Eurostat: reutilización con cita", True),
    "proteccion_temporal_concesiones": ("personas", "Eurostat, migr_asytpfm (concesiones mensuales)", _C, "Eurostat: reutilización con cita", True),
    **{f"catastro_inspire_{v}": (u, "Catastro, INSPIRE Buildings (agregado espacial propio a sección INE)", _C, "Catastro: reutilización con reconocimiento", True)
       for v, u in (("edificios", "edificios"), ("inmuebles", "inmuebles"), ("viviendas", "viviendas"), ("superficie_construida_m2", "m²"),
                    ("viviendas_por_antiguedad", "viviendas"))},
    "ss_afiliados_cota_inferior": ("afiliados", "Seguridad Social, afiliados por municipio (MUNCNAE; suma de celdas ≥5)", _C, "Seguridad Social: reutilización con cita", True),
    "ss_afiliados_celdas_menor5": ("celdas", "Seguridad Social, afiliados por municipio (nº de celdas «<5»)", _C, "Seguridad Social: reutilización con cita", True),
    **{f"ss_afiliados_{s}_cota_inferior": ("afiliados", f"Seguridad Social, afiliados por municipio, CNAE {s}", _C, "Seguridad Social: reutilización con cita", True)
       for s in ("construccion", "hosteleria", "inmobiliarias")},
    "ss_afiliados_extranjeros": ("afiliados", "Seguridad Social, afiliados extranjeros por provincia (último día del periodo)", _C, "Seguridad Social: reutilización con cita", True),
    "ine_tmov_receptor_turistas": ("turistas", "INE, turismo receptor medido con teléfonos móviles (52048; experimental)", _C, INE, True),
    "ine_tmov_interno_turistas": ("turistas", "INE, turismo interno medido con teléfonos móviles (53464; experimental)", _C, INE, True),
    "c21md_hogares_muestra": ("hogares (muestra 10 %)", "INE, Censo 2021, microdatos de personas (recuento muestral)", _C, INE, True),
    "reate_viviendas_uso_turistico": ("viviendas", "Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0)", _C, "CC BY 4.0", True),
    "reate_habitaciones_uso_turistico": ("habitaciones", "Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0)", _C, "CC BY 4.0", True),
}
