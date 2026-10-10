#!/usr/bin/env python3
"""Descarga v3 (D1) del INE a nivel municipal y de sección censal -> data/raw/v3 (formato largo).

Fuentes (ver docs/v3/fuentes_fallidas.md para lo inaccesible):
  1. VUT municipal, porcentaje sobre el total de viviendas (API tabla 39366, op. VTE).
     La sección censal no está publicada en la API ni en la página de la estadística.
  2. Censo de Población y Viviendas 2021, indicadores por sección censal
     (C2021_Indicadores.csv + diccionario indicadores_seccen_c2021.xlsx). Provisional (INE).
  3. Censo 2021 municipal: viviendas total / principales / no principales (tabla JAXI 59525).
     Se usa como referencia independiente para el cuadre sección -> municipio.
  4. Censo 2021 edad por sección censal (API /Censo2021/api, ID_RESIDENCIA_N5 x ID_EDAD),
     agregada en 0-15, 16-24, 25-34, 35-44, 45-64, 65+.
  5. Cartografía de secciones censales 2021 (Cartografia_secc.zip, 64 MB < 300 MB).
     Se guarda sin extraer en data/raw/v3/cartografia (gitignored, con sha256).

Caché: los originales van a data/raw/v3_orig (gitignored). No se rebaja si existe salvo FORCE=1.
Uso: python src/v3/fetch_ine_v3.py
"""
from __future__ import annotations

import datetime as dt
import fcntl
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests

SRC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC))
from utils_fetch import FORCE, HEADERS, MANIFEST, RAW, ROOT, download, save  # noqa: E402

B = "https://servicios.ine.es/wstempus/js/ES"
CENSO_API = "https://www.ine.es/Censo2021/api"
CENSO_CSV = "https://www.ine.es/censos2021/C2021_Indicadores.csv"
CENSO_IND_XLSX = "https://www.ine.es/censos2021/indicadores_seccen_c2021.xlsx"
CARTO_ZIP = "https://www.ine.es/censos2021/Cartografia_secc.zip"
ORIG = RAW / "v3_orig"
OUT = RAW / "v3"
CARTO = OUT / "cartografia"
SHA = ROOT / "data" / "CHECKSUMS.sha256"
GITIGNORE = ROOT / ".gitignore"
CENSO_FECHA = "2021-11-01"  # fecha de referencia del Censo 2021 (1 de noviembre de 2021)
MAX_CSV_BYTES = 50 * 1024 * 1024
UA_NOTE = HEADERS["User-Agent"]
FUENTE_VUT = "INE Medición del número de viviendas turísticas (estadística experimental)"
FUENTE_CENSO = "INE Censo de Población y Viviendas 2021 (provisional)"
COLS_OUT = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url",
            "territorio", "nivel", "codigo", "desglose"]


def load_json(url: str, name: str, timeout: int = 900):
    """Descarga JSON con caché en data/raw/v3_orig y lo devuelve parseado."""
    p = download(url, ORIG / name, timeout=timeout)
    return json.loads(p.read_bytes())


def post_json(body: dict, name: str, timeout: int = 1200):
    """POST a la API del Censo 2021 con caché. Devuelve el JSON parseado."""
    dest = ORIG / name
    if dest.exists() and dest.stat().st_size > 0 and not FORCE:
        print(f"[cache] {dest.relative_to(ROOT)}")
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = requests.post(CENSO_API, json=body,
                          headers={**HEADERS, "Accept": "application/json"}, timeout=timeout)
        r.raise_for_status()
        if not r.content.startswith(b"{"):
            raise RuntimeError("respuesta no JSON de la API del Censo")
        dest.write_bytes(r.content)
        print(f"[dl] {dest.name} ({len(r.content)} bytes)")
    return json.loads(dest.read_bytes())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def last_date(df: pd.DataFrame) -> str:
    return str(df["fecha"].max()) if len(df) else "NA"


def municipal_names(censo_mun: pd.DataFrame) -> tuple[dict, dict]:
    """Mapas nombre->lista de códigos y código->nombre, a partir de la tabla municipal del Censo."""
    mun = censo_mun[censo_mun["nivel"] == "municipio"][["codigo", "territorio"]].drop_duplicates()
    by_code = dict(zip(mun["codigo"], mun["territorio"]))
    by_name: dict[str, list[str]] = {}
    for c, n in by_code.items():
        by_name.setdefault(n, []).append(c)
    return by_name, by_code


# ---------------------------------------------------------------- 1. VUT municipal (% viviendas)
def vut_pct_municipio(by_name: dict) -> pd.DataFrame:
    d = load_json(f"{B}/DATOS_TABLA/39366?nult=400", "ine_t39366.json")
    rows = []
    n_sin_codigo = 0
    for s in d:
        terr, _, resto = s["Nombre"].partition(". ")
        medida = resto.rstrip(".").strip()
        codes = by_name.get(terr, [])
        if len(codes) == 1:
            codigo, nivel = codes[0], "municipio"
        else:
            codigo, nivel = "", "municipio"
            n_sin_codigo += 1
        unidad = "%" if "orcentaje" in medida or "%" in medida else "número"
        for o in s.get("Data") or []:
            ts = pd.to_datetime(o["Fecha"], unit="ms", utc=True).tz_convert("Europe/Madrid")
            fecha = ts.strftime("%Y-%m-01")
            periodo = f"{o['Anyo']}M{int(o['FK_Periodo']):02d}"
            rows.append({
                "fecha": fecha, "periodo": periodo, "serie": s["COD"],
                "valor": o.get("Valor"), "unidad": unidad, "fuente": FUENTE_VUT,
                "url": f"{B}/DATOS_TABLA/39366?nult=400", "territorio": terr,
                "nivel": nivel, "codigo": codigo, "desglose": medida,
            })
    df = pd.DataFrame(rows)
    print(f"[vut] series={df['serie'].nunique()} obs={len(df)} sin_codigo_unico={n_sin_codigo}")
    return df


# ---------------------------------------------------------------- 3. Censo municipal (viviendas)
TIPO_VIV = {"Total": "V_TOTAL", "Vivienda principal": "V_PRINCIPAL",
            "Vivienda no principal": "V_NOPRINCIPAL"}


def censo_municipal() -> pd.DataFrame:
    d = load_json(f"{B}/DATOS_TABLA/59525?nult=1", "ine_t59525.json")
    rows = []
    url = f"{B}/DATOS_TABLA/59525?nult=1"
    for s in d:
        base, _, tipo = s["Nombre"].rpartition(", ")
        if tipo not in TIPO_VIV:
            continue
        m = re.match(r"^(\d{5}) (.+)$", base)
        if m:
            codigo, terr, nivel = m.group(1), m.group(2), "municipio"
        elif base == "Total Nacional":
            codigo, terr, nivel = "ES", "Total Nacional", "nacional"
        else:
            continue
        o = (s.get("Data") or [None])[-1]
        if o is None:
            continue
        rows.append({
            "fecha": CENSO_FECHA, "periodo": "2021", "serie": TIPO_VIV[tipo],
            "valor": o.get("Valor"), "unidad": "viviendas", "fuente": FUENTE_CENSO,
            "url": url, "territorio": terr, "nivel": nivel, "codigo": codigo,
            "desglose": f"Viviendas familiares convencionales: {tipo.lower()}",
        })
    df = pd.DataFrame(rows)
    print(f"[censo_mun] municipios={df.loc[df.nivel == 'municipio', 'codigo'].nunique()} obs={len(df)}")
    return df


# ---------------------------------------------------------------- 2. Censo por sección (indicadores)
def unidad_de(desc: str) -> str:
    d = desc.lower()
    if "porcentaje" in d:
        return "%"
    if "edad media" in d:
        return "años"
    if "hogares" in d:
        return "hogares"
    if "viviendas" in d:
        return "viviendas"
    return "personas"


def censo_seccion(by_code: dict) -> pd.DataFrame:
    csv_p = download(CENSO_CSV, ORIG / "C2021_Indicadores.csv", timeout=600)
    xls_p = download(CENSO_IND_XLSX, ORIG / "indicadores_seccen_c2021.xlsx")
    ind = pd.read_excel(xls_p, sheet_name="indicadores", header=None).iloc[:, :2]
    ind.columns = ["serie", "desc"]
    ind = ind[ind["serie"].astype(str).str.match(r"^t\d+_\d+$")]
    desc = dict(zip(ind["serie"], ind["desc"].astype(str).str.strip()))

    raw = pd.read_csv(csv_p, dtype=str)
    raw["codigo"] = raw["cpro"] + raw["cmun"] + raw["dist"] + raw["secc"]
    raw["cod_mun"] = raw["cpro"] + raw["cmun"]
    cols = [c for c in raw.columns if re.match(r"^t\d+_\d+$", c)]
    missing_desc = [c for c in cols if c not in desc]
    if missing_desc:
        raise RuntimeError(f"indicadores sin descripción: {missing_desc}")
    long = raw.melt(id_vars=["codigo", "cod_mun"], value_vars=cols,
                    var_name="serie", value_name="valor_txt")
    long["valor"] = pd.to_numeric(long["valor_txt"], errors="coerce")
    n_nan_por_serie = long.assign(n=long["valor"].isna()).groupby("serie")["n"].sum()
    n_vacios = int((long["valor_txt"].isna() | (long["valor_txt"].astype(str).str.strip() == "")).sum())
    print(f"[censo_sec] secciones={raw['codigo'].nunique()} series={len(cols)} "
          f"NaN={int(long['valor'].isna().sum())} (vacíos/secreto={n_vacios})")
    long["fecha"] = CENSO_FECHA
    long["periodo"] = "2021"
    long["unidad"] = long["serie"].map(lambda s: unidad_de(desc[s]))
    long["fuente"] = FUENTE_CENSO
    long["url"] = CENSO_CSV
    long["territorio"] = long["cod_mun"].map(lambda c: by_code.get(c, ""))
    long["nivel"] = "seccion"
    long["desglose"] = long["serie"].map(desc)
    out = long[["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url",
                "territorio", "nivel", "codigo", "desglose"]]
    return out, n_nan_por_serie


def cuadre_seccion_municipio(sec: pd.DataFrame, mun: pd.DataFrame) -> dict:
    """Suma de secciones == total municipal (tabla 59525) para viviendas total/principal/no principal."""
    mapa = {"t18_1": "V_TOTAL", "t19_1": "V_PRINCIPAL", "t19_2": "V_NOPRINCIPAL"}
    s = sec[sec["serie"].isin(mapa)].copy()
    s["cod_mun"] = s["codigo"].str[:5]
    s["tipo"] = s["serie"].map(mapa)
    suma = s.groupby(["cod_mun", "tipo"])["valor"].sum()
    nan_sec = s.groupby(["cod_mun", "tipo"])["valor"].apply(lambda x: int(x.isna().sum()))
    m = mun[(mun["nivel"] == "municipio") & mun["serie"].isin(mapa.values())]
    ref = m.set_index(["codigo", "serie"])["valor"]
    res = {"n_comparaciones": 0, "ok": 0, "ko": 0, "ko_con_nan_seccion": 0, "ejemplos_ko": []}
    for (cod, tipo), tot in ref.items():
        if (cod, tipo) not in suma.index:
            continue
        res["n_comparaciones"] += 1
        diff = suma[(cod, tipo)] - tot
        if abs(diff) < 0.5 and nan_sec.get((cod, tipo), 0) == 0:
            res["ok"] += 1
        else:
            res["ko"] += 1
            if nan_sec.get((cod, tipo), 0) > 0:
                res["ko_con_nan_seccion"] += 1
            if len(res["ejemplos_ko"]) < 5:
                res["ejemplos_ko"].append(f"{cod} {tipo}: secc={suma[(cod, tipo)]} mun={tot}")
    return res


# ---------------------------------------------------------------- 4. Edad por sección (API Censo)
GRUPOS_EDAD = [(0, 15, "0-15"), (16, 24, "16-24"), (25, 34, "25-34"),
               (35, 44, "35-44"), (45, 64, "45-64"), (65, 200, "65+")]


def edad_de(txt: str):
    t = str(txt).strip()
    if t.startswith("Menos de 1"):
        return 0
    m = re.match(r"^(\d+)", t)
    return int(m.group(1)) if m else None


def censo_edad_seccion(sec_pob: pd.Series) -> tuple[pd.DataFrame, dict]:
    body = {"idioma": "ES", "metrica": ["SPERSONAS"], "tabla": "per.ppal",
            "variables": ["ID_RESIDENCIA_N5", "ID_EDAD"]}
    d = post_json(body, "censo_api_seccion_edad.json")
    rows = []
    for r in d["data"]:
        m = re.search(r"(\d{10})$", str(r.get("ID_RESIDENCIA_N5", "")))
        edad = edad_de(r.get("ID_EDAD"))
        if not m or edad is None or r.get("SPERSONAS") is None:
            continue
        rows.append((m.group(1), edad, float(r["SPERSONAS"])))
    del d
    pob = pd.DataFrame(rows, columns=["codigo", "edad", "pob"])
    pob["grupo"] = None
    for lo, hi, lab in GRUPOS_EDAD:
        pob.loc[pob["edad"].between(lo, hi), "grupo"] = lab
    agg = pob.groupby(["codigo", "grupo"])["pob"].sum().reset_index()
    tot = pob.groupby("codigo")["pob"].sum()
    ref = sec_pob.reindex(tot.index)
    diff = (tot - ref).abs()
    cuadre = {"secciones": int(len(tot)), "ok_total_vs_t1_1": int((diff < 0.5).sum()),
              "ko_total_vs_t1_1": int((diff >= 0.5).sum()), "sin_t1_1": int(ref.isna().sum())}
    out = pd.DataFrame({
        "fecha": CENSO_FECHA, "periodo": "2021",
        "serie": "EDAD_" + agg["grupo"].astype(str),
        "valor": agg["pob"], "unidad": "personas", "fuente": FUENTE_CENSO,
        "url": CENSO_API, "territorio": "", "nivel": "seccion", "codigo": agg["codigo"],
        "desglose": "Población por grupo de edad (ID_EDAD, Censo 2021), suma de años simples",
    })
    return out, cuadre


# ---------------------------------------------------------------- 5. Cartografía
def cartografia() -> Path:
    p = download(CARTO_ZIP, CARTO / "Cartografia_secc.zip", timeout=900)
    if not zipfile.is_zipfile(p):
        raise RuntimeError("Cartografia_secc.zip no es un ZIP válido")
    with zipfile.ZipFile(p) as z:
        n = len(z.namelist())
    print(f"[carto] {p.name}: {n} entradas en el ZIP (sin extraer)")
    return p


def manifest_extra(archivo: str, fuente: str, n_obs: int | str, ultima: str) -> None:
    row = pd.DataFrame([{
        "archivo": archivo, "fuente": fuente, "n_series": "", "primera_fecha": "",
        "ultima_fecha": ultima, "n_obs": n_obs, "n_nan": "",
        "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }])
    with open(RAW / ".manifest.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        man = pd.read_csv(MANIFEST)
        man = pd.concat([man[man["archivo"] != archivo], row], ignore_index=True)
        man.sort_values("archivo").to_csv(MANIFEST, index=False)


def add_checksum(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    lines = SHA.read_text().splitlines() if SHA.exists() else []
    lines = [ln for ln in lines if not ln.endswith(f"  {rel}")]
    lines.append(f"{sha256(path)}  {rel}")
    SHA.write_text("\n".join(lines) + "\n")
    print(f"[sha] {rel}")


def add_gitignore(pattern: str) -> None:
    txt = GITIGNORE.read_text() if GITIGNORE.exists() else ""
    if pattern not in txt.splitlines():
        with open(GITIGNORE, "a") as fh:
            fh.write(f"# v3 D1 (INE): >50 MB o originales re-descargables\n{pattern}\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CARTO.mkdir(parents=True, exist_ok=True)
    ORIG.mkdir(parents=True, exist_ok=True)

    censo_mun = censo_municipal()
    by_name, by_code = municipal_names(censo_mun)
    mun_path = save(censo_mun[COLS_OUT], "v3/ine_v3_censo2021_municipio_viviendas.csv", FUENTE_CENSO)
    ult = {"censo_municipio": last_date(censo_mun)}

    vut = vut_pct_municipio(by_name)
    save(vut[COLS_OUT], "v3/ine_v3_vut_municipio_pct.csv", FUENTE_VUT)
    ult["vut_municipio_pct"] = last_date(vut)

    sec, nan_serie = censo_seccion(by_code)
    sec_name = "v3/ine_v3_censo2021_seccion_indicadores.csv.gz"
    save(sec, sec_name, FUENTE_CENSO)
    gz = RAW / sec_name
    if gz.stat().st_size > MAX_CSV_BYTES:
        add_gitignore(f"data/raw/{sec_name}")
    if gz.stat().st_size > MAX_CSV_BYTES:
        add_checksum(gz)
    ult["censo_seccion"] = CENSO_FECHA

    cuadre_v = cuadre_seccion_municipio(sec, censo_mun)
    sec_pob = sec[sec["serie"] == "t1_1"].set_index("codigo")["valor"]

    edad, cuadre_e = censo_edad_seccion(sec_pob)
    save(edad[COLS_OUT], "v3/ine_v3_censo2021_seccion_edad.csv", FUENTE_CENSO)

    carto = cartografia()
    add_gitignore("data/raw/v3/cartografia/")
    add_checksum(carto)
    manifest_extra("v3/cartografia/Cartografia_secc.zip",
                   "INE Cartografía secciones censales 2021 (ZIP, sin extraer)",
                   "", "2021-01-01")

    print("RESUMEN", json.dumps({
        "ultima_fecha": ult,
        "censo_seccion_nan_por_serie_max": int(nan_serie.max()),
        "cuadre_viviendas_seccion_vs_municipio": cuadre_v,
        "cuadre_edad_vs_t1_1": cuadre_e,
        "mun_path": str(mun_path),
    }, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
