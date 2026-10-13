"""V8-F1: descarga de series nuevas a data/raw/v8/ (formato largo).

Columnas: fecha, periodo, serie, valor, unidad, fuente, url, nombre, territorio, nivel, codigo.

Fuentes (todas de acceso público):
  1. Shocks de política monetaria BCE (Jarocinski y Karadi, repositorio público, licencia CC BY 4.0 para datos).
  2. Encuesta de préstamos bancarios (BLS, BCE data-api): España, hogares, préstamos para vivienda.
  3. Precios de vivienda Eurostat prc_hpi_q (EA20, EA19, ES, DE, FR, IT, PT, NL; TOTAL; I15_Q).
  4. INE FRONTUR (Movimientos turísticos en fronteras): tabla 10822 (país de residencia) y 10823 (CCAA destino).
  5. INE ETCL: tabla 6067 (nacional, coste laboral) y 79662 (CCAA); IPC general nacional, INE tabla 24077.
  6. Eurostat migr_imm1ctz (inmigración por ciudadanía, ES) y migr_pop1ctz (población por ciudadanía, ES).
  7. Visados: NO se descarga; data/raw/mivau_v2_iniciadas_terminadas_prov.csv ya cubre 1991-2026.
  8. Tipos: Euríbor 3m (FM.M...EURIBOR3MD_) y tipo depósito DFR (FM.B...DFR.LEV) del BCE.
     MRO y Euríbor 1 año ya existen (ecb_tipo_oficial.csv, ecb_euribor1y.csv): no se repiten.

Reglas:
  - Caché: si el fichero de destino existe y no hay FORCE=1, no se descarga (se valida el existente).
  - RAW_DIR se respeta como en src/utils_fetch.py (por defecto data/raw). Salida: <RAW>/v8/.
  - No se toca ningún fichero existente de data/raw: solo se escribe en data/raw/v8/.
  - Fallos: se anotan en docs/v6/fuentes_fallidas.md y el script sigue.
  - Uso: python3 src/v8/fetch_v8.py   (FORCE=1 para rebajar de nuevo)
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import utils_fetch as uf  # noqa: E402  (caché, RAW_DIR, FORCE, get con reintentos)

RAW = uf.RAW
OUT = RAW / "v8"
MANIFEST = OUT / "_manifest.csv"
FALLIDAS = ROOT / "docs" / "v6" / "fuentes_fallidas.md"
RESULTADO = ROOT / "output" / "v8" / "F1_fetch" / "resultado.json"
FORCE = uf.FORCE
COLS = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "nombre", "territorio", "nivel", "codigo"]
HOY = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

FALLOS: list[dict] = []


# ----------------------------------------------------------------- utilidades
def periodo_norm(fecha: pd.Timestamp, freq: str) -> str:
    if freq == "A":
        return f"{fecha.year}"
    if freq == "Q":
        return f"{fecha.year}-Q{(fecha.month - 1) // 3 + 1}"
    if freq == "M":
        return f"{fecha.year}-{fecha.month:02d}"
    return fecha.strftime("%Y-%m-%d")


def fecha_de_periodo(p: str, freq_hint: str | None = None) -> pd.Timestamp:
    p = str(p).strip()
    if re.fullmatch(r"\d{4}", p):
        return pd.Timestamp(int(p), 1, 1)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", p)
    if m:
        return pd.Timestamp(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)
    m = re.fullmatch(r"(\d{4})-(\d{2})", p)
    if m:
        return pd.Timestamp(int(m.group(1)), int(m.group(2)), 1)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", p)
    if m:
        return pd.Timestamp(p)
    raise ValueError(f"periodo no reconocido: {p}")


def ms_a_fecha_madrid(ms) -> pd.Timestamp:
    ts = pd.to_datetime(int(ms), unit="ms", utc=True).tz_convert("Europe/Madrid")
    return pd.Timestamp(ts.tz_localize(None).normalize())


def registro(fecha, freq, serie, valor, unidad, fuente, url, nombre="", territorio="", nivel="", codigo=""):
    return {
        "fecha": pd.Timestamp(fecha).strftime("%Y-%m-%d"),
        "periodo": periodo_norm(pd.Timestamp(fecha), freq),
        "serie": serie,
        "valor": np.nan if valor is None or valor == "" else float(valor),
        "unidad": unidad,
        "fuente": fuente,
        "url": url,
        "nombre": nombre,
        "territorio": territorio,
        "nivel": nivel,
        "codigo": codigo,
    }


def unidad_ine(nombre: str) -> str:
    n = nombre.lower()
    if "euros" in n:
        return "euros"
    if "tasa de variación" in n or "tasa de variacion" in n or "variación anual" in n:
        return "% variación"
    if "índice" in n or "indice" in n:
        return "índice"
    if "turista" in n or "visitante" in n:
        return "número"
    return "sin_especificar"


def ine_serie(tabla: str, nult: int = 2000) -> list[dict]:
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla}?nult={nult}"
    data = uf.get(url, as_json=True)
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"respuesta INE vacía para tabla {tabla}")
    return data


def tabla_ine_a_largo(series: list[dict], tabla: str, freq: str, fuente: str, url: str,
                      nivel_fn, territorio_fn) -> pd.DataFrame:
    rows = []
    for s in series:
        nombre = s.get("Nombre", "")
        cod = s.get("COD", "")
        terr = territorio_fn(nombre)
        niv = nivel_fn(nombre)
        uni = unidad_ine(nombre)
        for x in s.get("Data", []):
            f = ms_a_fecha_madrid(x["Fecha"])
            val = None if x.get("Secreto") else x.get("Valor")
            rows.append(registro(f, freq, cod, val, uni, fuente, url, nombre, terr, niv, cod))
    return pd.DataFrame(rows, columns=COLS)


def ecb_csv(url: str) -> pd.DataFrame:
    txt = uf.get(url, as_json=False)
    if txt.lstrip().startswith("<"):
        raise RuntimeError("el endpoint devolvió HTML/XML en vez de CSV")
    return pd.read_csv(io.StringIO(txt), dtype=str)


def jsonstat_filas(d: dict) -> list[dict]:
    ids = d["id"]
    sizes = d["size"]
    cats = {k: sorted(d["dimension"][k]["category"]["index"].items(), key=lambda kv: kv[1]) for k in ids}
    labels = {k: d["dimension"][k]["category"].get("label", {}) for k in ids}
    vals = d["value"]
    it = vals.items() if isinstance(vals, dict) else enumerate(vals)
    stride = [1] * len(ids)
    for k in range(len(ids) - 2, -1, -1):
        stride[k] = stride[k + 1] * sizes[k + 1]
    out = []
    for i, v in it:
        i = int(i)
        fila = {}
        for k, dim in enumerate(ids):
            pos = (i // stride[k]) % sizes[k]
            code = cats[dim][pos][0]
            fila[dim] = code
            fila[dim + "_label"] = labels[dim].get(code, code)
        fila["value"] = v
        out.append(fila)
    return out


def eurostat_json(url: str) -> dict:
    txt = uf.get(url, as_json=False)
    return json.loads(txt)


# ----------------------------------------------------------------- fuentes
def serie_jk() -> pd.DataFrame:
    base = "https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/main/"
    url = base + "shocks_ecb_mpd_me_m.csv"
    txt = uf.get(url, as_json=False)
    df = pd.read_csv(io.StringIO(txt))
    desc = {
        "pc1_hf": "factor de política (pc1, alta frecuencia, mensual agregado)",
        "STOXX50_hf": "STOXX 50 (alta frecuencia, mensual agregado)",
        "MP_pm": "shock de política monetaria (restricción de signo, versión pura)",
        "CBI_pm": "shock de información del banco central (restricción de signo, versión pura)",
        "MP_median": "shock de política monetaria (mediana de rotaciones)",
        "CBI_median": "shock de información del banco central (mediana de rotaciones)",
    }
    rows = []
    for _, r in df.iterrows():
        f = pd.Timestamp(int(r["year"]), int(r["month"]), 1)
        for c in df.columns:
            if c in ("year", "month"):
                continue
            rows.append(registro(f, "M", c, r[c], "shock (unidad original del repositorio)", "JK-ECB shocks (Jarocinski y Karadi, actualizado)",
                                 url, desc.get(c, c), "Euro area", "zona_euro", "JK_ECB_mensual"))
    return pd.DataFrame(rows, columns=COLS)


def serie_bls() -> pd.DataFrame:
    url = ("https://data-api.ecb.europa.eu/service/data/BLS/Q.ES.ALL.Z.H.H.B3...?format=csvdata"
           "&startPeriod=2000-01-01")
    df = ecb_csv(url)
    rows = []
    # Códigos de unidad del BCE: FNET = saldo neto (%) ; DINX = índice de difusión (UNIT=PC).
    uni_bls = {"FNET": "% saldo neto (restrictivo menos expansivo)", "DINX": "índice de difusión (PC)"}
    for _, r in df.iterrows():
        key = r["KEY"].replace("BLS.", "", 1)
        agg = key.split(".")[-1]
        uni = uni_bls.get(agg, f"sin_especificar (UNIT={r.get('UNIT', '')})")
        f = fecha_de_periodo(r["TIME_PERIOD"])
        nombre = r.get("TITLE_COMPL") or r.get("TITLE", "")
        rows.append(registro(f, "Q", key, r["OBS_VALUE"], uni, "BCE - Bank Lending Survey (BLS)", url,
                             nombre, "ES", "pais", key))
    return pd.DataFrame(rows, columns=COLS)


def serie_hpi() -> pd.DataFrame:
    rows = []
    for geo in ["EA20", "EA19", "ES", "DE", "FR", "IT", "PT", "NL"]:
        url = (f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hpi_q"
               f"?geo={geo}&purchase=TOTAL&unit=I15_Q&lang=EN")
        d = eurostat_json(url)
        for f in jsonstat_filas(d):
            if f["value"] is None:
                continue
            fe = fecha_de_periodo(f["time"])
            serie = f"prc_hpi_q|TOTAL|I15_Q|{geo}"
            rows.append(registro(fe, "Q", serie, f["value"], "índice 2015=100 (trimestral)", "Eurostat prc_hpi_q",
                                 url, f"House price index, total, I15_Q, {f['geo_label']}", geo, "pais_o_agregado", geo))
        # observaciones nulas: se registran con NaN para no ocultar huecos
        for f in jsonstat_filas(d):
            if f["value"] is None:
                fe = fecha_de_periodo(f["time"])
                serie = f"prc_hpi_q|TOTAL|I15_Q|{geo}"
                rows.append(registro(fe, "Q", serie, None, "índice 2015=100 (trimestral)", "Eurostat prc_hpi_q",
                                     url, f"House price index, total, I15_Q, {f['geo_label']}", geo, "pais_o_agregado", geo))
    return pd.DataFrame(rows, columns=COLS)


def serie_eurostat_ciudadania(dataset: str, params: str, nombre_base: str) -> pd.DataFrame:
    url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{dataset}?{params}&lang=EN"
    d = eurostat_json(url)
    rows = []
    for f in jsonstat_filas(d):
        if f["value"] is None:
            continue
        fe = fecha_de_periodo(f["time"])
        cit = f["citizen"]
        serie = f"{dataset}|{cit}|ES"
        rows.append(registro(fe, "A", serie, f["value"], "personas", f"Eurostat {dataset}", url,
                             f"{nombre_base}; ciudadanía: {f['citizen_label']}", "ES", "pais", cit))
    return pd.DataFrame(rows, columns=COLS)


def serie_tipos_ecb() -> pd.DataFrame:
    rows = []
    for nombre_serie, key, uni_txt in [
        ("euribor_3m", "FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA", "% anual"),
        ("depo_dfr", "FM/B.U2.EUR.4F.KR.DFR.LEV", "% anual"),
    ]:
        url = f"https://data-api.ecb.europa.eu/service/data/{key}?format=csvdata"
        df = ecb_csv(url)
        for _, r in df.iterrows():
            f = fecha_de_periodo(r["TIME_PERIOD"])
            freq = "D" if len(r["TIME_PERIOD"]) == 10 else "M"
            rows.append(registro(f, freq, r["KEY"], r["OBS_VALUE"], uni_txt, "BCE data-api (FM)", url,
                                 r.get("TITLE", nombre_serie), "EA", "zona_euro", r["KEY"]))
    return pd.DataFrame(rows, columns=COLS)


# ----------------------------------------------------------------- validación
def validar(df: pd.DataFrame, nombre_fichero: str) -> dict:
    nduplicados = int(df.duplicated(subset=["fecha", "serie"]).sum())
    nnan = int(df["valor"].isna().sum())
    sin_unidad = int((df["unidad"].fillna("") == "").sum())
    fechas_ok = bool(pd.to_datetime(df["fecha"], errors="coerce").notna().all())
    return {"fichero": nombre_fichero, "n": len(df), "duplicados": nduplicados, "nan": nnan,
            "sin_unidad": sin_unidad, "fechas_ok": fechas_ok}


def guardar(df: pd.DataFrame, nombre: str) -> dict:
    df = df.sort_values(["serie", "fecha"]).reset_index(drop=True)
    df = df.drop_duplicates(subset=["fecha", "serie", "valor"], keep="first")
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / nombre, index=False, encoding="utf-8")
    return validar(df, nombre)


def existe(nombre: str) -> bool:
    p = OUT / nombre
    if p.exists() and p.stat().st_size > 0 and not FORCE:
        print(f"[cache] v8/{nombre}")
        return True
    return False


def fallo(endpoint: str, motivo: str, alternativa: str):
    FALLOS.append({"endpoint": endpoint, "motivo": motivo, "alternativa": alternativa})
    print(f"[FALLO] {endpoint}: {motivo}")


def tarea(nombre: str, fn, endpoint: str, alternativa: str):
    if existe(nombre):
        return
    try:
        df = fn()
        print(f"[ok] v8/{nombre}: {len(df)} filas")
        guardar(df, nombre)
    except Exception as e:  # noqa: BLE001
        fallo(endpoint, f"{type(e).__name__}: {e}", alternativa)


def reutilizado(nombre_existente: str, motivo: str) -> dict:
    p = RAW / nombre_existente
    if not p.exists():
        return {"fichero": f"data/raw/{nombre_existente}", "serie": "(no existe)", "n": 0,
                "periodo_min": "", "periodo_max": "", "estado": "no_encontrado", "url": "", "fecha_descarga": "",
                "motivo": motivo}
    df = pd.read_csv(p, dtype=str)
    df = df.assign(_f=pd.to_datetime(df["fecha"], errors="coerce")).sort_values("_f")
    series = df["serie"].unique()
    return {"fichero": f"data/raw/{nombre_existente}",
            "serie": series[0] if len(series) == 1 else f"varias ({len(series)})",
            "n": len(df), "periodo_min": df["periodo"].iloc[0], "periodo_max": df["periodo"].iloc[-1],
            "estado": "reutilizado_existente_no_descargado", "url": df["url"].iloc[0] if "url" in df else "",
            "fecha_descarga": "", "motivo": motivo}


# ----------------------------------------------------------------- principal
def main() -> None:
    print(f"RAW={RAW}  OUT={OUT}  FORCE={int(FORCE)}")
    OUT.mkdir(parents=True, exist_ok=True)

    tarea("jk_shocks_ecb_mensual.csv", serie_jk,
          "https://raw.githubusercontent.com/marekjarocinski/jkshocks_update_ecb/main/shocks_ecb_mpd_me_m.csv",
          "Descargar el Dataset_EA-MPD (BCE) y recalcular con code/main.m del repositorio")
    tarea("ecb_bls_es_vivienda.csv", serie_bls,
          "https://data-api.ecb.europa.eu/service/data/BLS/Q.ES.ALL.Z.H.H.B3...?format=csvdata",
          "Descarga manual desde la web del BCE (Bank Lending Survey statistics)")
    tarea("eurostat_prc_hpi_q_multi.csv", serie_hpi,
          "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hpi_q?geo=<GEO>&purchase=TOTAL&unit=I15_Q",
          "BIS (data/raw/bis_rpp.csv ya cubre varios países)")
    tarea("ine_frontur_10822_pais.csv",
          lambda: tabla_ine_a_largo(ine_serie("10822"), "10822", "M", "INE FRONTUR (tabla 10822)",
                                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10822?nult=2000",
                                    lambda n: "nacional" if "Total Nacional" in n else "pais_residencia",
                                    lambda n: "España"),
          "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10822?nult=2000",
          "Eurostat tur_* (no verificado en esta fase)")
    tarea("ine_frontur_10823_ccaa.csv",
          lambda: tabla_ine_a_largo(ine_serie("10823"), "10823", "M", "INE FRONTUR (tabla 10823)",
                                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10823?nult=2000",
                                    lambda n: "nacional" if "Total Nacional" in n else "ccaa",
                                    lambda n: n.split(".")[1].strip() if "." in n else n),
          "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10823?nult=2000",
          "Tabla 75720 (CCAA destino, misma operación) si 10823 falla")
    tarea("ine_etcl_6067_nacional.csv",
          lambda: tabla_ine_a_largo(ine_serie("6067"), "6067", "Q", "INE ETCL (tabla 6067)",
                                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/6067?nult=2000",
                                    lambda n: "nacional", lambda n: "España"),
          "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/6067?nult=2000",
          "Tabla 79660 (coste salarial por sectores) si 6067 falla")
    tarea("ine_etcl_79662_ccaa.csv",
          lambda: tabla_ine_a_largo(ine_serie("79662"), "79662", "Q", "INE ETCL (tabla 79662)",
                                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/79662?nult=2000",
                                    lambda n: "nacional" if n.startswith("Total Nacional") else "ccaa",
                                    lambda n: n.split(".")[0].strip()),
          "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/79662?nult=2000",
          "Tabla 6061/79659 (coste laboral CCAA, otra edición)")
    tarea("ine_ipc_24077_general.csv",
          lambda: tabla_ine_a_largo(ine_serie("24077"), "24077", "M", "INE IPC (tabla 24077)",
                                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24077?nult=2000",
                                    lambda n: "nacional", lambda n: "España"),
          "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24077?nult=2000",
          "ecb_hicp_es.csv (IPCA ya existente)")
    # migr_imm1ctz (ES, 1998-2024) ya existe en data/raw/eurostat_inmigracion_anual.csv con la misma
    # cobertura y las mismas 283 series: no se repite.
    tarea("eurostat_migr_pop1ctz_es.csv",
          lambda: serie_eurostat_ciudadania("migr_pop1ctz", "geo=ES&sex=T&age=TOTAL",
                                            "Población por ciudadanía (migr_pop1ctz)"),
          "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/migr_pop1ctz?geo=ES&sex=T&age=TOTAL",
          "INE Padrón por nacionalidad (data/raw/ine_padron_*)")
    tarea("ecb_tipos_euribor3m_depo.csv", serie_tipos_ecb,
          "https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.DFR.LEV?format=csvdata",
          "Existente: MRO en data/raw/ecb_tipo_oficial.csv; Euríbor 1 año en ecb_euribor1y.csv")

    # Existentes reutilizados (no se repiten): se documentan en el manifiesto.
    reuse = [
        ("mivau_v2_iniciadas_terminadas_prov.csv", "Visados/iniciadas 1991-2026 (item 7): ya existe, no repetido"),
        ("ine_migraciones_nacionalidad.csv", "Migraciones por nacionalidad INE (item 6): ya existe"),
        ("eurostat_inmigracion_anual.csv", "Inmigración anual Eurostat migr_imm1ctz 1998-2024 (item 6): ya existe, no repetida"),
        ("bis_rpp.csv", "BIS precios vivienda (item 3): ya existe, no repetido"),
        ("ecb_hicp_es.csv", "IPCA ES BCE (item 5): ya existe"),
        ("ecb_tipo_oficial.csv", "Tipo MRO BCE (item 8): ya existe"),
        ("ecb_euribor1y.csv", "Euríbor 1 año (item 8): ya existe"),
        ("bde_tipo_hipotecario_referencia.csv", "Tipo hipotecario BdE desde 1973 (item 8): ya existe"),
    ]
    reuso_filas = [reutilizado(n, m) for n, m in reuse]

    # Manifiesto a nivel de serie para los ficheros generados en v8
    fecha_prev = {}
    if MANIFEST.exists() and not FORCE:
        prev = pd.read_csv(MANIFEST, dtype=str)
        fecha_prev = dict(zip(prev["fichero"], prev["fecha_descarga"]))
    filas = []
    for p in sorted(q for q in OUT.glob("*.csv") if not q.name.startswith("_")):
        df = pd.read_csv(p, dtype=str)
        if df.empty:
            continue
        df["_f"] = pd.to_datetime(df["fecha"], errors="coerce")
        df["_v"] = pd.to_numeric(df["valor"], errors="coerce")
        url_fichero = df["url"].iloc[0] if "url" in df else ""
        for serie, g in df.groupby("serie", sort=True):
            g = g.sort_values("_f")
            estado = "ok" if g["_v"].notna().all() else "ok_con_NaN"
            if g["_f"].duplicated().any():
                estado = "error_duplicados"
            filas.append({
                "fichero": f"data/raw/v8/{p.name}",
                "serie": serie,
                "url": g["url"].iloc[0] if "url" in g else url_fichero,
                "fecha_descarga": fecha_prev.get(f"data/raw/v8/{p.name}", HOY),
                "periodo_min": g["periodo"].iloc[0],
                "periodo_max": g["periodo"].iloc[-1],
                "n": len(g),
                "estado": estado + f" ({int(g['_v'].isna().sum())} NaN)",
            })
    for r in reuso_filas:
        filas.append({k: r.get(k, "") for k in ["fichero", "serie", "url", "fecha_descarga", "periodo_min",
                                               "periodo_max", "n", "estado"]})
    pd.DataFrame(filas, columns=["fichero", "serie", "url", "fecha_descarga", "periodo_min", "periodo_max",
                                 "n", "estado"]).to_csv(MANIFEST, index=False, encoding="utf-8")
    print(f"[manifest] {MANIFEST} ({len(filas)} filas)")

    # Limitaciones de cobertura verificadas (no son fallos de acceso): se anotan una vez por endpoint.
    FALLOS.extend([
        {"endpoint": "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24077?nult=2000",
         "motivo": "LIMITACIÓN PARCIAL: el WS devuelve 296 obs. mensuales (2001-12 a 2026-07) aunque la tabla "
                   "se anuncia desde 1961; nult=5000 y date= no amplían la serie (probado 2026-10-13)",
         "alternativa": "IPCA BCE (data/raw/ecb_hicp_es.csv, desde 1996) como serie larga; IPC 1961+ por descarga manual"},
        {"endpoint": "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/10822?nult=5000",
         "motivo": "LIMITACIÓN PARCIAL: FRONTUR en 10822, 10823, 75719, 75720 y 23984 empieza en 2015-09 "
                   "(serie actual); sin FRONTUR 1999-2015 por WS",
         "alternativa": "Sin alternativa automatizada; edición antigua de la operación 330 no localizada"},
        {"endpoint": "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/6067?nult=2000",
         "motivo": "LIMITACIÓN PARCIAL: 6067 (retrospectivas) termina en 2007-Q3; la nacional actual (79662, "
                   "'Total Nacional') empieza en 2008-Q1; sin empalme aplicado",
         "alternativa": "Usar ambas tablas con la discontinuidad marcada en el nombre; empalme solo validado"},
    ])
    # Fuentes fallidas: se añade una sola vez por endpoint
    if FALLOS:
        txt = FALLIDAS.read_text(encoding="utf-8") if FALLIDAS.exists() else ""
        nuevas = [f for f in FALLOS if f["endpoint"] not in txt]
        if nuevas:
            with FALLIDAS.open("a", encoding="utf-8") as fh:
                fh.write(f"\n## V8-F1 (descarga, {HOY[:10]})\n\n")
                for f in nuevas:
                    fh.write(f"- Endpoint: {f['endpoint']}. Error: {f['motivo']}. Alternativa: {f['alternativa']}.\n")
            print(f"[fallidas] anotadas {len(nuevas)} en {FALLIDAS}")


if __name__ == "__main__":
    main()
