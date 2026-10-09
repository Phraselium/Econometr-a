"""Padrón de València (municipio INE 46250): total y Comunitat Valenciana por nacionalidad.

Fuentes (API JSON wstempus del INE):
- Tabla 2903 (Cifras oficiales de población, op. DPOP, provincia de Valencia por municipios):
  València municipio (no la provincia) total, hombres y mujeres, anual. Series DPOP21796 /
  DPOP21797 / DPOP21798. La serie "Valencia/València" (DPOP21046) es la provincia y se descarta.
- Tabla 29005 (Cifras oficiales del padrón por municipio, op. DPOP): solo para validación
  cruzada del último año de València (DATOS_TABLA nult=1). No se guarda.
- Tabla 56942 (Estadística Continua de Población, op. ECP): Comunitat Valenciana por nacionalidad
  (grupos de países) y sexo, anual. Se seleccionan series por nombre.

Limitaciones (ver docs/fallidas/padron_valencia.md): la API no ofrece población por nacionalidad
a nivel municipal anual, así que el desglose por nacionalidad es solo a nivel Comunitat Valenciana.

Idempotente: si data/raw/ine_padron_valencia.csv existe no se vuelve a bajar (salvo FORCE=1).
Formato largo estándar (utils_fetch.save). Series = código INE; nombre = Nombre del INE.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import cached, get, save  # noqa: E402

BASE = "https://servicios.ine.es/wstempus/js/ES"
NAME = "ine_padron_valencia.csv"
NULT = 300
TOL = 0.5  # personas: tolerancia para identidades exactas (total = hombres + mujeres)
TOL_CV = 5  # personas: la ECP redondea cada celda, sumas de nacionalidades difieren 1-2 personas

# COD -> prefijo de Nombre esperado (se verifica para no confundir series)
MUNI = {
    "DPOP21796": "València. Total.",
    "DPOP21797": "València. Hombres.",
    "DPOP21798": "València. Mujeres.",
}
COD_VAL = "DPOP21796"


def fetch_serie(cod: str) -> dict:
    """Devuelve la serie INE completa (DATOS_SERIE/{cod})."""
    d = get(f"{BASE}/DATOS_SERIE/{cod}", params={"nult": NULT})
    if isinstance(d, list):
        d = d[0]
    if not d.get("Data"):
        raise RuntimeError(f"Serie {cod} sin datos: {str(d)[:200]}")
    return d


def rows_from_serie(s: dict, url: str) -> list[dict]:
    rows = []
    unidad = s["Nombre"].strip().rstrip(".").split(".")[-1].strip()
    for x in s["Data"]:
        # FK_Periodo: 28 = anual; 19-22 = T1-T4 (ECP trimestral, verificado en fetch_ine.py)
        fk, anyo = int(x["FK_Periodo"]), int(x["Anyo"])
        if fk == 28:
            fecha, lab = dt.date(anyo, 1, 1), str(anyo)
        elif fk in (19, 20, 21, 22):
            q = {19: 1, 20: 2, 21: 3, 22: 4}[fk]
            fecha, lab = dt.date(anyo, 3 * q - 2, 1), f"{anyo}T{q}"
        else:
            raise ValueError(f"{s['COD']}: FK_Periodo no reconocido ({fk})")
        rows.append({
            "fecha": fecha.isoformat(), "periodo": lab, "serie": s["COD"],
            "valor": None if x.get("Secreto") else x.get("Valor"), "unidad": unidad,
            "fuente": "INE", "url": url, "nombre": s["Nombre"].strip(),
            "fk_unidad": s.get("FK_Unidad"),
        })
    return rows


def pivot(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="fecha", columns="serie", values="valor", aggfunc="first")


def cv_series_codes() -> dict[str, str]:
    """Códigos de la Comunitat Valenciana en la tabla 56942 (nacionalidad x sexo, todas las edades)."""
    d = get(f"{BASE}/DATOS_TABLA/56942", params={"nult": 1})
    pat = re.compile(r"^Comunitat Valenciana\. Todas las edades\. (.+?)\. (Total|Hombres|Mujeres)\. Población\. Número\.")
    out = {}
    for x in d:
        m = pat.match(x["Nombre"])
        if not m:
            continue
        grupo, sexo = m.group(1), m.group(2)
        # Total de nacionalidades x sexo Total, y el desglose por sexo de Total / Española / Extranjera
        if sexo == "Total" or grupo in ("Total", "Española", "Extranjera"):
            out[x["COD"]] = f"{grupo}|{sexo}"
    return out


def cifras_municipio_ultimo() -> dict[str, float]:
    """Último año de València en 'Cifras oficiales del padrón por municipio' (tabla 29005)."""
    d = get(f"{BASE}/DATOS_TABLA/29005", params={"nult": 1})
    for x in d:
        if x["COD"] == COD_VAL and x["Nombre"].startswith("València. Total."):
            return {str(r["Anyo"]): r["Valor"] for r in x["Data"]}
    raise RuntimeError("Serie de València no encontrada en la tabla 29005")


def validate(df: pd.DataFrame, cv: pd.DataFrame, cifras: dict[str, float]) -> list[str]:
    msgs = []
    p = pivot(df[df.serie.isin(MUNI)])
    tot, h, m = p["DPOP21796"], p["DPOP21797"], p["DPOP21798"]
    d1 = (tot - (h + m)).abs().max()
    msgs.append(f"València: |total - (hombres+mujeres)| máx = {d1:.1f} personas "
                f"({'OK' if d1 <= TOL else 'FALLA'})")

    c = pivot(cv)
    # Total CV = Española + Extranjera (sexo Total)
    tot_cv = c[cv_code(cv, "Total", "Total")]
    esp = c[cv_code(cv, "Española", "Total")]
    ext = c[cv_code(cv, "Extranjera", "Total")]
    d2 = (tot_cv - (esp + ext)).abs().max()
    msgs.append(f"CV: |total - (española+extranjera)| máx = {d2:.1f} personas "
                f"({'OK' if d2 <= TOL_CV else 'FALLA'})")
    # Extranjera = suma de grupos (UE28 sin España + Europa resto + África + Am. Norte + Centro Am. y
    # Caribe + Sudamérica + Asia + Oceanía + Apátridas)
    grupos = ["País de la UE28 sin España", "País de Europa menos UE28", "De Africa",
              "De América del Norte", "De Centro América y Caribe", "De Sudamérica",
              "De Asia", "De Oceanía", "Apátridas"]
    try:
        suma = sum(c[cv_code(cv, g, "Total")] for g in grupos)
        d3 = (ext - suma).abs().max()
        msgs.append(f"CV: |extranjera - suma grupos de países| máx = {d3:.1f} personas "
                    f"({'OK' if d3 <= TOL_CV else 'FALLA: los grupos no suman el total, revisar'})")
    except KeyError as e:
        msgs.append(f"CV: grupo no encontrado para suma ({e})")
    # València total: tabla 2903 vs tabla 29005 (último año publicado)
    comp = {a: (tot.loc[f"{a}-01-01"], v) for a, v in cifras.items() if f"{a}-01-01" in tot.index}
    for a, (x, y) in comp.items():
        msgs.append(f"València total {a}: 2903={x:.0f} vs 29005={y:.0f}, diferencia = {x - y:.0f} "
                    f"({'OK' if abs(x - y) <= TOL else 'FALLA'})")
    return msgs


def cv_code(cv: pd.DataFrame, grupo: str, sexo: str) -> str:
    sub = cv[(cv["nombre"].str.contains(f"Todas las edades. {re.escape(grupo)}. {sexo}. ", regex=True))]
    if sub.empty:
        raise KeyError(f"{grupo}/{sexo}")
    return sub["serie"].iloc[0]


def main() -> None:
    if cached(NAME):
        return
    rows = []
    # 1) València municipio (serie de la tabla 2903)
    for cod, pref in MUNI.items():
        s = fetch_serie(cod)
        assert s["Nombre"].startswith(pref), (cod, s["Nombre"])
        rows += rows_from_serie(s, f"{BASE}/DATOS_SERIE/{cod}")
    # 2) Comunitat Valenciana por nacionalidad (tabla 56942)
    codes = cv_series_codes()
    print(f"[cv] {len(codes)} series de Comunitat Valenciana seleccionadas en 56942")
    for cod in codes:
        s = fetch_serie(cod)
        rows += rows_from_serie(s, f"{BASE}/DATOS_SERIE/{cod}")

    df = pd.DataFrame(rows)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    cv = df[df.serie.isin(codes)].copy()
    for msg in validate(df, cv, cifras_municipio_ultimo()):
        print("[val]", msg)
    print(f"[val] NaN: {int(df['valor'].isna().sum())} de {len(df)} observaciones")
    save(df, NAME, "INE")


# ===========================================================================
# Padrón municipal de València (46250) por nacionalidad: ficheros PC-Axis/CSV del INE
# ===========================================================================
# Fuente: ficheros CSV de INEbase (Estadística del Padrón continuo, explotación por municipios).
#   - 1998-2019: un fichero anual por año (p05/aAAAA/l0/0004600X.csv_bdsc).
#   - 2002-2019: el fichero 0004600 "nacionalidad" (principales nacionalidades, 2003+) y el
#     0004600 "español/extranjero" (Total, españoles, extranjeros) para totales.
#   - 2020-2022: tabla 33946 (jaxiT3, "Población por sexo, municipios y nacionalidad
#     (principales nacionalidades)", serie 2003-2022). Un único CSV para todos los años.
#   - 2023-2025: no publicado en ninguna de estas fuentes (ver docs/fallidas/padron_valencia.md).
# Mapeo año -> ficheros verificado el 2026-10-09 (tamaño y cabecera comprobados).
PX_BASE = "https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t20/e245/p05"
PX_T3 = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/33946.csv"
NAT_NAME = "ine_padron_vlc_nacionalidad.csv"
NAT_FUENTE = "INE Padrón continuo"
NAT_UNIDAD = "personas"
PX_RAW = RAW / "ine_padron_pcaxis"  # originales descargados (caché de utils_fetch.download)
MUNI_VLC = "46250"
PROV = "46"
PX_HEADERS = {"User-Agent": "econometria-vivienda-tfm/1.0 (investigacion academica)"}
TOL_NAT = 0.5  # personas: identidades exactas (total = españoles + extranjeros)
TOL_MUNI_SUM = 0.5  # personas: suma de municipios = total provincial (exacto en padrón)

PX_MAP: dict[int, list[tuple[str, str]]] = {}  # año -> [(url, papel)]; papel 'nac' | 'esp_ext' | 't3'
for _y in range(1998, 2002):  # 1998-2001: continentes y u.e. (no hay principales nacionalidades)
    PX_MAP[_y] = [(f"{PX_BASE}/a{_y}/l0/00046004.csv_bdsc", "nac"),
                  (f"{PX_BASE}/a{_y}/l0/00046005.csv_bdsc", "nac")]
PX_MAP[2002] = [(f"{PX_BASE}/a2002/l0/00046004.csv_bdsc", "nac"),
                (f"{PX_BASE}/a2002/l0/00046002.csv_bdsc", "esp_ext")]
for _y in range(2003, 2020):  # 2003-2019: principales nacionalidades + español/extranjero
    PX_MAP[_y] = [(f"{PX_BASE}/a{_y}/l0/00046003.csv_bdsc", "nac"),
                  (f"{PX_BASE}/a{_y}/l0/00046002.csv_bdsc", "esp_ext")]
for _y in (2020, 2021, 2022):  # 2020-2022: tabla 33946 (CSV multianual)
    PX_MAP[_y] = [(PX_T3, "t3")]

SEX_CANON = {"ambos sexos": "Ambos sexos", "total": "Ambos sexos", "hombres": "Hombres",
             "varones": "Hombres", "mujeres": "Mujeres"}


def _decode(b: bytes) -> str:
    """Codificación: UTF-8 con BOM (lo habitual) o cp1252/latin-1 si no decodifica."""
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("latin-1")


def _fix_text(s: str) -> str:
    """Corrige mojibake conocido ('Am‚rica' -> 'América') y espacios."""
    s = str(s).strip().replace("‚", "é")
    if "Ã" in s or "Â" in s:
        try:
            s = s.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return re.sub(r"\s+", " ", s)


def _num(x: str) -> float:
    """Miles con '.': '2.605.757' -> 2605757. Vacío o símbolo de secreto -> NaN (sin imputar)."""
    s = str(x).strip()
    if s in ("", "..", "-", "…", "*", "."):
        return float("nan")
    if not re.fullmatch(r"-?\d{1,3}(\.\d{3})*|-?\d+", s):
        raise ValueError(f"formato numérico no reconocido: {s!r}")
    return float(s.replace(".", ""))


def _canon_cat(raw: str) -> str:
    """Nombre canónico de nacionalidad/grupo. Las etiquetas cambian entre años (ver doc)."""
    s = _fix_text(raw)
    low = s.lower()
    if low in ("total", "total población", "total poblacion"):
        return "Total"
    if low in ("españoles", "españolas", "español", "española"):
        return "Española"
    if low in ("extranjeros", "extranjera", "total extranjeros", "total nacionalidades"):
        return "Extranjera"
    if low in ("total africa", "total áfrica", "africa", "áfrica"):
        return "Total África"
    if low in ("total américa", "total america", "américa", "america"):
        return "Total América"
    if low in ("total asia", "asia"):
        return "Total Asia"
    if low in ("total europa", "europa"):
        return "Total Europa"
    if low == "rep. dominicana":
        return "República Dominicana"
    return s


def _probe(url: str) -> str:
    """Petición pequeña previa a la descarga: estado, bytes y cabecera. Lanza si no hay contenido."""
    r = requests.get(url, headers=PX_HEADERS, timeout=60, stream=True)
    try:
        r.raise_for_status()
        chunk = next(r.iter_content(2000), b"")
    finally:
        r.close()
    if not chunk:
        raise RuntimeError(f"sin contenido (HTTP {r.status_code})")
    return _decode(chunk).splitlines()[0]


def _read_px(path: Path, year_hint: int | None) -> pd.DataFrame:
    """Lee un CSV PC-Axis del INE y devuelve formato largo (solo provincia 46)."""
    txt = _decode(path.read_bytes())
    df = pd.read_csv(io.StringIO(txt), sep=";", dtype=str, keep_default_na=False)
    cols = list(df.columns)
    sex_c, mun_c, val_c = cols[0], "Municipios", cols[-1]
    nat_c = next(c for c in cols if c.startswith("Nacionalidad"))
    if "Provincias" in cols:
        df = df[df["Provincias"].str.strip().str.startswith(PROV + " ")]
    for c in cols:
        if c.startswith("Edad"):  # 00046002: quedarse con edad 'Total'
            df = df[df[c].str.strip() == "Total"]
    out = pd.DataFrame({
        "anio": ([int(re.search(r"(\d{4})", p).group(1)) for p in df["Periodo"]]
                 if "Periodo" in cols else year_hint),
        "sexo": df[sex_c].map(lambda x: SEX_CANON[_fix_text(x).lower()]),
        "muni_raw": df[mun_c].map(_fix_text),
        "nac": df[nat_c].map(_canon_cat),
        "valor": df[val_c].map(_num),
    })
    m = out["muni_raw"].str.extract(r"^(\d{1,5})\s*[- ]?\s*(.*)$")
    code = m[0].fillna("")
    out["muni"] = code.map(lambda c: "" if c == "" else (PROV + c.zfill(3) if len(c) <= 3 else c))
    out["muni"] = out["muni"].where(out["muni"] != "", "PROV")  # fila 'Total' provincial
    out.loc[out["muni_raw"].isin(["Total", ""]), "muni"] = "PROV"
    out = out[out["muni"].isin(["PROV"]) | out["muni"].str.startswith(PROV)]
    return out.reset_index(drop=True)


def _load_year(year: int, cache: dict) -> tuple[pd.DataFrame, list[str]]:
    """Carga todas las tablas de un año (provincia 46). Devuelve (df, urls usadas)."""
    parts, urls = [], []
    for url, papel in PX_MAP[year]:
        if url not in cache:
            local = PX_RAW / re.sub(r"^https://www\.ine\.es/jaxi(T3)?/files/", "", url).replace("/", "_")
            print(f"[probe] {year} {url.rsplit('/', 1)[-1]}: {_probe(url)[:80]}")
            cache[url] = _read_px(download(url, local), None if papel == "t3" else year)
        d = cache[url].copy()
        if papel == "t3":
            d = d[d["anio"] == year]
        d["papel"] = papel
        d["url"] = url
        parts.append(d)
        urls.append(url)
    return pd.concat(parts, ignore_index=True), urls


def fetch_nacionalidad_pcaxis() -> Path | None:
    """Padrón de València (46250) por sexo y nacionalidad, 1998-2022, desde ficheros PC-Axis/CSV.

    Salida: data/raw/ine_padron_vlc_nacionalidad.csv (formato largo; utils_fetch.save).
    Series: vlc_46250|<sexo>|<nacionalidad> y prov_46|<sexo>|<nacionalidad> (fila 'Total' provincial).
    Huecos: años sin fichero (2023-2025) o sin el dato (1998-2001 sin principales nacionalidades).
    Sin imputación: los valores secretos/vacíos quedan como NaN.
    """
    if cached(NAT_NAME):
        return RAW / NAT_NAME
    cache: dict[str, pd.DataFrame] = {}
    full, huecos, val_rows = [], [], []
    for year in range(1998, 2026):
        if year not in PX_MAP:
            huecos.append(year)
            print(f"[hueco] {year}: sin fichero PC-Axis conocido (ver docs/fallidas/padron_valencia.md)")
            continue
        try:
            d, _ = _load_year(year, cache)
        except Exception as e:  # noqa: BLE001 - no inventar: el año queda como hueco
            huecos.append(year)
            print(f"[hueco] {year}: {e}")
            continue
        # Duplicados entre ficheros del mismo año: prevalece el primero (papel 'nac');
        # se registra la diferencia máxima entre fuentes para validar.
        d = d.drop_duplicates(["anio", "sexo", "muni", "nac", "papel"])
        full.append(d)
    if not full:
        raise RuntimeError("ningún año descargado para el padrón por nacionalidad")
    df = pd.concat(full, ignore_index=True)
    df["prio"] = df["papel"].map({"nac": 0, "t3": 0, "esp_ext": 1})
    df = df.sort_values("prio").drop_duplicates(["anio", "sexo", "muni", "nac"], keep="first")

    # ---- Validaciones ----
    msgs = []
    # (c) suma de municipios = total provincial, por año, sexo y nacionalidad
    cs = df.groupby(["anio", "sexo", "nac"]).apply(
        lambda g: pd.Series({
            "prov": g.loc[g.muni == "PROV", "valor"].sum(),
            "suma": g.loc[g.muni != "PROV", "valor"].sum(),
            "n_prov": int((g.muni == "PROV").sum()),
            "n_mun": int((g.muni != "PROV").sum()),
        }), include_groups=False).reset_index()
    cs = cs[cs.n_prov > 0]
    cs["diff"] = (cs["suma"] - cs["prov"]).abs()
    ok_c = cs.loc[cs.n_mun > 0, "diff"].max()
    msgs.append(f"(c) provincia 46: |suma municipios - total| máx = {ok_c:.1f} personas "
                f"({'OK' if ok_c <= TOL_MUNI_SUM else 'REVISAR'}; {len(cs)} combinaciones año×sexo×nac)")

    vlc = df[df.muni == MUNI_VLC].copy()
    # (a) españoles + extranjeros = total (València), por año y sexo
    p = vlc.pivot_table(index=["anio", "sexo"], columns="nac", values="valor", aggfunc="first")
    comp = p.dropna(subset=[c for c in ("Total", "Española", "Extranjera") if c in p.columns])
    comp = comp[["Total", "Española", "Extranjera"]].dropna()
    err_a = (comp["Total"] - comp["Española"] - comp["Extranjera"]).abs()
    msgs.append(f"(a) València: |total - (españoles+extranjeros)| máx = {err_a.max():.1f} personas "
                f"({'OK' if err_a.max() <= TOL_NAT else 'FALLA'}; {len(comp)} filas año×sexo)")
    # (b) total València vs DPOP21796 en data/raw/ine_padron_valencia.csv
    ref_path = RAW / "ine_padron_valencia.csv"
    if ref_path.exists():
        ref = pd.read_csv(ref_path, usecols=["fecha", "serie", "valor"])
        ref = ref[ref.serie.isin(["DPOP21796", "DPOP21797", "DPOP21798"])].copy()
        ref["anio"] = ref["fecha"].str.slice(0, 4).astype(int)
        mp = {"DPOP21796": "Ambos sexos", "DPOP21797": "Hombres", "DPOP21798": "Mujeres"}
        errs_b = []
        tot_vlc = vlc[vlc.nac == "Total"].set_index(["anio", "sexo"])["valor"]
        for serie, sexo in mp.items():
            r = ref[ref.serie == serie].set_index("anio")["valor"]
            idx = [a for a in r.index if (a, sexo) in tot_vlc.index]
            e = (tot_vlc.loc[[(a, sexo) for a in idx]].values - r.loc[idx].values)
            if len(e):
                errs_b.append((sexo, len(e), float(abs(e).max())))
        for sexo, n, mx in errs_b:
            msgs.append(f"(b) València total {sexo} vs DPOP: máx = {mx:.1f} personas en {n} años "
                        f"({'OK' if mx <= TOL_NAT else 'FALLA'})")
    else:
        msgs.append("(b) omitida: falta data/raw/ine_padron_valencia.csv")
    # Validación cruzada: 2003-2019 (ficheros anuales) vs tabla 33946 (2003-2022)
    try:
        t3, _ = _load_year(2020, cache)  # mismo CSV 33946, años 2003-2022 completos
        t3 = cache[PX_T3]
        t3 = t3[(t3.muni == MUNI_VLC) & (t3.anio.between(2003, 2019))]
        ann = vlc[vlc.anio.between(2003, 2019) & vlc.nac.isin(["Total", "Española", "Extranjera"])]
        m_ = ann.merge(t3[t3.nac.isin(["Total", "Española", "Extranjera"])], on=["anio", "sexo", "nac"],
                       suffixes=("", "_t3"))
        dd = (m_["valor"] - m_["valor_t3"]).abs().max()
        msgs.append(f"(d) cruce anual 2003-2019 vs tabla 33946: máx |dif| = {dd:.1f} personas "
                    f"({'OK' if dd <= TOL_NAT else 'REVISAR'}; {len(m_)} celdas)")
    except Exception as e:  # noqa: BLE001
        msgs.append(f"(d) cruce no disponible: {e}")

    for m_txt in msgs:
        print("[val]", m_txt)

    # ---- Salida larga (solo se guardan València y la fila Total provincial) ----
    out = df[df.muni.isin([MUNI_VLC, "PROV"])].copy()
    out["serie"] = out.apply(lambda r: ("vlc_46250" if r.muni == MUNI_VLC else "prov_46")
                             + f"|{r.sexo}|{r.nac}", axis=1)
    out["fecha"] = out["anio"].map(lambda a: f"{a}-01-01")
    out["periodo"] = out["anio"].astype(str)
    out["unidad"] = NAT_UNIDAD
    out["fuente"] = NAT_FUENTE
    out = out[["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url"]]
    out = out.sort_values(["serie", "fecha"]).reset_index(drop=True)
    n_nan = int(out["valor"].isna().sum())
    print(f"[nac] {out['serie'].nunique()} series, {len(out)} obs, NaN={n_nan}; "
          f"años con datos={sorted(out['periodo'].unique())}; huecos={huecos}")
    return save(out, NAT_NAME, NAT_FUENTE)


if __name__ == "__main__":
    main()
    fetch_nacionalidad_pcaxis()
