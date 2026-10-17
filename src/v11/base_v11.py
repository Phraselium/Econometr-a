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
    # Seguridad Social: afiliados por municipio (cota inferior: suma de celdas numéricas) y celdas «<5». En la base solo el
    # total de regímenes (tamaño de la capa pública < 50 MB); el desglose por régimen queda en data/raw/v11
    f = RAW11 / "ss_afiliacion_municipio/afiliacion_municipio_mensual.csv.gz"
    if f.exists():
        a = pd.read_csv(f, dtype={"cod_municipio": str, "mes": str})
        a = a[_mun(a.cod_municipio)]
        cols = ["afiliados_suma_numerica", "celdas_menor5", "construccion", "hosteleria", "inmobiliarias"]
        a = a.groupby(["cod_municipio", "mes"], as_index=False)[cols].sum(min_count=1)
        for col, var in (("afiliados_suma_numerica", "ss_afiliados_cota_inferior"), ("celdas_menor5", "ss_afiliados_celdas_menor5"),
                         ("construccion", "ss_afiliados_construccion_cota_inferior"), ("hosteleria", "ss_afiliados_hosteleria_cota_inferior"),
                         ("inmobiliarias", "ss_afiliados_inmobiliarias_cota_inferior")):
            x = a[a[col].notna() & ((a[col] != 0) | (col == "afiliados_suma_numerica"))]
            add(pd.DataFrame({"territorio_codigo": x.cod_municipio, "nivel": "municipio", "periodo_raw": x.mes, "variable": var,
                              "valor": x[col], "metodo_dato": "suma de celdas publicadas (excluye «<5»); total de regímenes"}),
                "data/raw/v11/ss_afiliacion_municipio/afiliacion_municipio_mensual.csv.gz")
    # Seguridad Social: afiliados extranjeros por provincia (foto anual)
    f = RAW11 / "ss_afiliacion_extranjeros/afiliados_extranjeros_provincia.csv.gz"
    if f.exists():
        x = pd.read_csv(f, dtype={"cod_provincia": str, "mes": str})
        add(pd.DataFrame({"territorio_codigo": x.cod_provincia, "nivel": "provincia", "periodo_raw": x.mes,
                          "variable": "ss_afiliados_extranjeros", "valor": x.total}),
            "data/raw/v11/ss_afiliacion_extranjeros/afiliados_extranjeros_provincia.csv.gz")
    # OPI (réplica de la Comunidad de Madrid): certificados de registro o tarjetas en vigor, provincia 28, por nacionalidad
    f = RAW11 / "opi_replica_madrid/opi_madrid_pais_sexo.csv.gz"
    if f.exists():
        o = pd.read_csv(f, dtype=str, keep_default_na=False)
        o = o[o.sexo == "Total"]
        nac = np.where(o.concepto.str.startswith("Total"), "Total",
                       o.concepto.str.replace(r"^.*? en vigor (con nacionalidad de |de |del |con )?", "", regex=True))
        nac = pd.Series(nac, index=o.index)
        add(pd.DataFrame({"territorio_codigo": "28", "nivel": "provincia", "periodo_raw": o.anio, "variable": "opi_residentes_documentados",
                          "desagregacion": "nacionalidad=" + nac.str.strip(),
                          "valor": pd.to_numeric(o.valor, errors="coerce")}).dropna(subset=["valor"]).drop_duplicates(["periodo_raw", "desagregacion"]),
            "data/raw/v11/opi_replica_madrid/opi_madrid_pais_sexo.csv.gz")
    # Catastro, titularidad (padrón IBI): titulares y viviendas por tramo de nº de inmuebles del titular y tipo de persona
    # (se omiten las celdas a 0: ausencia de fila con total presente = 0)
    f = RAW11 / "catastro_titularidad/p_spi_mun_v.csv.gz"
    if f.exists():
        t = pd.read_csv(f, dtype=str, keep_default_na=False)
        t = t[_mun(t.CODINE)]
        persona = {"PF": "fisica", "PJ": "juridica", "PE": "entidad", "PD": "otros"}
        for pref, var in (("U_", "catastro_tit_titulares"), ("I_U_", "catastro_tit_viviendas")):
            tot = "NUM_SUJETOS_PASIVOS" if pref == "U_" else "INMUEBLES"
            cols = [c for c in t.columns if re.fullmatch(pref + r"P[FJED]_(HASTA|MAYOR)_\d+", c)]
            L = t.melt(id_vars=["CODINE", "anio_fichero"], value_vars=cols + [tot], var_name="col", value_name="v")
            m = L.col.str.extract(r"P([FJED])_(HASTA|MAYOR)_(\d+)$")
            L["desag"] = np.where(L.col == tot, "total",
                                  "persona=" + ("P" + m[0]).map(persona).fillna("") + "|tramo_inmuebles=" + m[1].str.lower().fillna("") + "_" + m[2].fillna(""))
            add(pd.DataFrame({"territorio_codigo": L.CODINE, "nivel": "municipio", "periodo_raw": L.anio_fichero, "variable": var,
                              "desagregacion": L.desag, "valor": pd.to_numeric(L.v, errors="coerce")}).query("valor != 0").dropna(subset=["valor"]),
                "data/raw/v11/catastro_titularidad/p_spi_mun_v.csv.gz")
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
    # --- Histórico (continuación V11) ---------------------------------------------------------------------------------
    # Catastro: titulares por municipio 2012-2023 (JAXI; definición distinta de los CSV 2024-2026: no se encadenan)
    f = RAW11 / "catastro_titularidad/titulares_municipio_2006_2023.csv.gz"
    if f.exists():
        t = pd.read_csv(f, dtype={"cod_municipio": str})
        t = t[_mun(t.cod_municipio)]
        for col in [c for c in ("titulares_urbano", "titulares_rustico", "titulares_total") if c in t]:
            add(pd.DataFrame({"territorio_codigo": t.cod_municipio, "nivel": "municipio", "periodo_raw": t.anio.astype(str),
                              "variable": "catastro_titulares_jaxi", "desagregacion": "clase=" + col.split("_")[1], "valor": t[col]}).dropna(subset=["valor"]),
                "data/raw/v11/catastro_titularidad/titulares_municipio_2006_2023.csv.gz")
    # Catastro, otras estadísticas 2019: viviendas por tramo de año de construcción y de reforma, y tipo
    f = RAW11 / "catastro_otras/catastro_otras_municipio.csv.gz"
    if f.exists():
        o = pd.read_csv(f, dtype={"cod_municipio": str})
        o = o[o.tabla.isin(["aant", "aref"]) & _mun(o.cod_municipio)]
        o["desag"] = "tipo=" + o.grupo.str.replace(r"^NUMERO VIVIENDAS ", "", regex=True).str.lower() + "|tramo=" + o.categoria
        o = o.drop_duplicates(["cod_municipio", "anio_fichero", "tabla", "desag"])
        add(pd.DataFrame({"territorio_codigo": o.cod_municipio, "nivel": "municipio", "periodo_raw": o.anio_fichero.astype(str),
                          "variable": np.where(o.tabla == "aant", "catastro_viviendas_por_anio_construccion", "catastro_viviendas_por_anio_reforma"),
                          "desagregacion": o.desag, "valor": o.valor}), "data/raw/v11/catastro_otras/catastro_otras_municipio.csv.gz")
    # Obra nueva (1): INSPIRE, viviendas por año exacto de construcción (stock superviviente), 94 municipios
    f = RAW11 / "catastro_inspire/viviendas_por_anio_construccion_municipio.csv.gz"
    if f.exists():
        v = pd.read_csv(f, dtype={"cod_municipio": str})
        v = v[_mun(v.cod_municipio) & (v.anio_construccion >= 1900) & (v.anio_construccion <= 2026)]
        add(pd.DataFrame({"territorio_codigo": v.cod_municipio, "nivel": "municipio", "periodo_raw": v.anio_construccion.astype(str),
                          "variable": "obra_nueva_viviendas_inspire", "valor": v.viviendas,
                          "metodo_dato": "stock superviviente por año de construcción (cota inferior)"}),
            "data/raw/v11/catastro_inspire/viviendas_por_anio_construccion_municipio.csv.gz")
    # Obra nueva (2): variación anual de unidades urbanas residenciales del Catastro (neta de bajas; todos los municipios)
    f = RAIZ / "data/raw/catastro_urbana_municipios.csv.gz"   # versión versionada (regla v5: no leer ficheros no versionados)
    if f.exists():
        u = pd.read_csv(f, dtype={"codigo": str, "periodo": str})
        u = u[u.serie.str.startswith("catastro_uu_res_") & _mun(u.codigo)].sort_values(["codigo", "periodo"])
        u["valor"] = pd.to_numeric(u.valor, errors="coerce")
        u["dif"] = u.groupby("codigo").valor.diff()
        u["salto"] = u.groupby("codigo").periodo.transform(lambda p: p.astype(int).diff())
        u = u[u.salto == 1].dropna(subset=["dif"])
        # V15 (ERRATA): el fichero «año t» es el stock a 31-12-(t−1) (columna `fecha` del crudo), así que la diferencia
        # entre los ficheros t y t−1 es la obra neta del año natural t−1, y con ese año se etiqueta (antes llevaba el año t)
        add(pd.DataFrame({"territorio_codigo": u.codigo, "nivel": "municipio", "periodo_raw": (u.periodo.astype(int) - 1).astype(str),
                          "variable": "obra_nueva_neta_catastro",
                          "valor": u.dif, "metodo_dato": "diferencia anual de unidades urbanas residenciales (cálculo propio)"}),
            "data/raw/catastro_urbana_municipios.csv.gz")
    # AEAT, IRPF por municipios (Comunitat Valenciana): conceptos principales
    f = RAW11 / "aeat_irpf_municipios/irpf_municipios_cv.csv.gz"
    if f.exists():
        a = pd.read_csv(f, dtype={"cod_municipio": str})
        claves = {"NÚMERO DE DECLARACIONES": "declaraciones", "RENTA BRUTA MEDIA": "renta_bruta_media",
                  "RENTA DISPONIBLE MEDIA": "renta_disponible_media",
                  "RENTAS DE BIENES INMUEBLES NO AFECTOS A ACTIV. ECONÓMICAS": "rentas_inmuebles_importe",
                  "Media de las rentas derivadas de bienes inmuebles no afectos a activ. económicas": "rentas_inmuebles_media",
                  "RENTAS DEL TRABAJO": "rentas_trabajo_importe"}
        a = a[a.variable.isin(claves) & _mun(a.cod_municipio)].drop_duplicates(["cod_municipio", "ejercicio", "variable"])
        add(pd.DataFrame({"territorio_codigo": a.cod_municipio, "nivel": "municipio", "periodo_raw": a.ejercicio.astype(str),
                          "variable": "aeat_irpf_" + a.variable.map(claves), "valor": a.valor}).dropna(subset=["valor"]),
            "data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz")
    # V12-F0: declarantes aproximados con rentas de bienes inmuebles (importe ÷ media; alquileres + imputaciones)
    f = RAIZ / "output/v12/f0/aeat_declarantes_inmuebles_aprox.csv"
    if f.exists():
        q = pd.read_csv(f, dtype={"cod_municipio": str})
        q = q[_mun(q.cod_municipio) & (q.marca.fillna("") == "")]
        add(pd.DataFrame({"territorio_codigo": q.cod_municipio, "nivel": "municipio", "periodo_raw": q.ejercicio.astype(str),
                          "variable": "aeat_irpf_declarantes_inmuebles_aprox", "valor": q.declarantes_rentas_inmuebles_aprox,
                          "metodo_dato": "importe ÷ media (cálculo propio; error relativo ≤ 0,5/media)"}),
            "output/v12/f0/aeat_declarantes_inmuebles_aprox.csv")
    # INE IPVA por municipio (> 10.000 hab.) y distrito de capitales, por tamaño de la vivienda (códigos de los metadatos)
    for nivel in ("municipio", "distrito"):
        f = RAW11 / f"ine_ipva/ipva_{nivel}_tamano.csv.gz"
        if not f.exists():
            continue
        q = pd.read_csv(f, dtype={"codigo": str, "anio": str})
        q = q[q.nivel == nivel]
        add(pd.DataFrame({"territorio_codigo": q.codigo, "nivel": nivel, "periodo_raw": q.anio,
                          "variable": np.where(q.tipo_dato.str.startswith("Índice"), "ipva_tam_indice", "ipva_tam_var_anual"),
                          "desagregacion": "tamano=" + q.tamano_vivienda.fillna("Total"), "valor": q.valor}),
            f"data/raw/v11/ine_ipva/ipva_{nivel}_tamano.csv.gz")
    # Descargas manuales del autor normalizadas por src/v11/incorporar_manual.py (si existen)
    f = RAW11 / "manual/bcn_hut_trimestral.csv.gz"
    if f.exists():
        b = pd.read_csv(f, dtype=str)
        add(pd.DataFrame({"territorio_codigo": "08019", "nivel": "municipio", "periodo_raw": b.trimestre,
                          "variable": "bcn_hut_registro", "desagregacion": "barrio_bcn=" + b.cod_barrio_bcn.astype(str),
                          "valor": pd.to_numeric(b.hut), "metodo_dato": "descarga manual del autor"}), "data/raw/v11/manual/bcn_hut_trimestral.csv.gz")
    f = RAW11 / "manual/gva_bdo_afiliacion.csv.gz"
    if f.exists():   # GVA BDO: afiliados por municipio y nacionalidad (ambos sexos; el desglose por sexo queda en data/raw)
        b = pd.read_csv(f, dtype={"cod_municipio": str})
        b = b[(b.sexo == "Ambos sexos") & _mun(b.cod_municipio) & b.valor.notna()]
        add(pd.DataFrame({"territorio_codigo": b.cod_municipio, "nivel": "municipio", "periodo_raw": b.trimestre,
                          "variable": "gva_bdo_afiliados", "desagregacion": "nacionalidad=" + b.nacionalidad,
                          "valor": b.valor, "metodo_dato": "descarga manual del autor (BDO GVA, V0201_C2D0244)"}),
            "data/raw/v11/manual/gva_bdo_afiliacion.csv.gz")
    # Padrón municipal de València (PDF del Ajuntament; extracción propia validada contra INE): barrio y distrito por código
    for fich, nivel in (("vlc_padron_barrio.csv.gz", "barrio"), ("vlc_padron_distrito.csv.gz", "distrito")):
        f = RAW11 / "vlc_padron" / fich
        if f.exists():
            b = pd.read_csv(f, dtype={"codigo": str})
            b = b[b.control_suma.astype(bool) & (b.codigo != "462501106")]   # Les Moreres (solo 2002): sin código vigente
            add(pd.DataFrame({"territorio_codigo": b.codigo, "nivel": nivel, "periodo_raw": b.anio.astype(str) + "-01-01",
                              "variable": b.variable, "desagregacion": b.desagregacion, "valor": b.valor,
                              "metodo_dato": np.where(b.ocr.astype(bool), "extracción de PDF con OCR", "extracción de PDF")}),
                f"data/raw/v11/vlc_padron/{fich}")
    f = RAW11 / "vlc_padron" / "vlc_altas_bajas_distrito.csv.gz"
    if f.exists():
        a = pd.read_csv(f, dtype={"cod_distrito": str})
        add(pd.DataFrame({"territorio_codigo": a.cod_distrito, "nivel": "distrito", "periodo_raw": a.anio.astype(str),
                          "variable": "vlc_altas_bajas", "desagregacion": "componente=" + a.componente, "valor": a.valor,
                          "metodo_dato": "extracción de PDF (informe más reciente)"}), "data/raw/v11/vlc_padron/vlc_altas_bajas_distrito.csv.gz")
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
    "opi_residentes_documentados": ("personas", "OPI (Ministerio de Inclusión), extranjeros con certificado de registro o tarjeta en vigor; réplica de la Comunidad de Madrid", _C, "CC BY 4.0 (Comunidad de Madrid)", True),
    "catastro_tit_titulares": ("titulares (sujetos pasivos)", "Catastro, estadística de titularidad (padrón IBI urbano, uso residencial; sujetos pasivos; tramos dentro del municipio; NO encadenar con catastro_titulares_jaxi: salto 2023→2024 de −32 % por cambio de definición)", _C, "Catastro: reutilización con reconocimiento", True),
    "catastro_tit_viviendas": ("inmuebles residenciales", "Catastro, estadística de titularidad (padrón IBI urbano, uso residencial)", _C, "Catastro: reutilización con reconocimiento", True),
    "gva_bdo_afiliados": ("afiliados", "GVA, Banco de Datos Municipal (consulta V0201_C2D0244): afiliados a la Seguridad Social por nacionalidad (descarga manual del autor)", _C, "Generalitat Valenciana: CC BY 4.0", True),
    **{v: ("personas", f"Ajuntament de València, Oficina d'Estadística, padrón municipal a 1 de enero (PDF; extracción propia; {d})", _C,
           "Ajuntament de València: reutilización con cita", True)
       for v, d in (("vlc_padron_pob", "sexo"), ("vlc_padron_pob_edad", "edad en tres grupos y sexo"),
                    ("vlc_padron_ext_continente", "población extranjera por continente"))},
    "vlc_altas_bajas": ("personas", "Ajuntament de València, informe anual de altas y bajas del padrón (PDF 2004-2016; extracción propia)", _C,
                        "Ajuntament de València: reutilización con cita", True),
    "bcn_hut_registro": ("viviendas", "Ajuntament de Barcelona, registro HUT, cortes trimestrales (descarga manual del autor)", _C, "CC BY 4.0", True),
    "catastro_titulares_jaxi": ("titulares", "Catastro, titulares catastrales por municipio y clase (visor JAXI; 2012-2023; NO encadenar con catastro_tit_*: serie de sujetos pasivos desde 2024)", _C, "Catastro: reutilización con reconocimiento", True),
    "catastro_viviendas_por_anio_construccion": ("viviendas", "Catastro, otras estadísticas (2019): viviendas por año de construcción", _C, "Catastro: reutilización con reconocimiento", True),
    "catastro_viviendas_por_anio_reforma": ("viviendas", "Catastro, otras estadísticas (2019): viviendas por año de reforma", _C, "Catastro: reutilización con reconocimiento", True),
    "obra_nueva_viviendas_inspire": ("viviendas", "Catastro INSPIRE: viviendas por año de construcción (stock superviviente; agregado propio)", _C, "Catastro: reutilización con reconocimiento", True),
    "obra_nueva_neta_catastro": ("unidades urbanas residenciales", "Catastro, estadística URBANA: diferencia anual (cálculo propio)", _C, "Catastro: reutilización con reconocimiento", True),
    **{f"aeat_irpf_{k}": (u, "AEAT, estadística de declarantes del IRPF por municipios", _C, "AEAT: reutilización con cita", True)
       for k, u in (("declaraciones", "declaraciones"), ("renta_bruta_media", "€"), ("renta_disponible_media", "€"),
                    ("rentas_inmuebles_importe", "€"), ("rentas_inmuebles_media", "€"), ("rentas_trabajo_importe", "€"))},
    "aeat_irpf_declarantes_inmuebles_aprox": ("declarantes (aprox.)", "AEAT, IRPF por municipios: importe ÷ media de rentas de bienes inmuebles no afectos (incluye alquileres e imputación de inmuebles no alquilados; no identifica caseros)", _C, "AEAT: reutilización con cita", True),
    "ipva_tam_indice": ("índice 2015=100", "INE, IPVA por municipio y distrito (59060, 59061) por tamaño de la vivienda", _C, INE, True),
    "ipva_tam_var_anual": ("%", "INE, IPVA por municipio y distrito (59060, 59061)", _C, INE, True),
    "ine_tmov_receptor_turistas": ("turistas", "INE, turismo receptor medido con teléfonos móviles (52048; experimental)", _C, INE, True),
    "ine_tmov_interno_turistas": ("turistas", "INE, turismo interno medido con teléfonos móviles (53464; experimental)", _C, INE, True),
    "c21md_hogares_muestra": ("hogares (muestra 10 %)", "INE, Censo 2021, microdatos de personas (recuento muestral)", _C, INE, True),
    "reate_viviendas_uso_turistico": ("viviendas", "Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0)", _C, "CC BY 4.0", True),
    "reate_habitaciones_uso_turistico": ("habitaciones", "Gobierno Vasco, REATE (Open Data Euskadi, CC BY 4.0)", _C, "CC BY 4.0", True),
}
