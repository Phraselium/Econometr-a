"""MIVAU v2: tablas XLS del Boletin Online (carpeta sedal/) no incluidas en v1.

Salidas (formato largo, data/raw):
  mivau_v2_suelo.csv                       (a) precio medio €/m2 suelo urbano, trimestral, 2004-.
        36400500 = por CCAA y provincias (todos los municipios)
        36403000 = por CCAA y provincias, municipios de mas de 50.000 hab. (agregado provincial;
                   el Boletin NO publica el dato municipio a municipio)
  mivau_v2_protegida.csv                   (b) vivienda protegida: calificaciones provisionales (~iniciadas)
        y definitivas (~terminadas), por CCAA/provincia. Anual 1991- (31303000, 31306000) y
        mensual 2008- (31202000, 31205000).
  mivau_v2_iniciadas_terminadas_prov.csv   (d) viviendas libres iniciadas y terminadas por CCAA/provincia.
        Anual 1991-2025 (32200500, 32201000) y mensual 2008-2026 (32100500, 32101000).
  (c) licencias municipales: NO disponible en el Boletin Online; ver docs/v2/fuentes_fallidas.md.
  (e) valor tasado por provincia/municipio: ya en v1 (no se repite).

Cada tabla se verifica por su titulo (no solo por el codigo). Los XLS originales se guardan sin editar
en data/raw/v2_orig/mivau/. Cache: si el CSV de salida existe no se vuelve a descargar (FORCE=1 rehace).
Los huecos (ND, n.r., celdas vacias) se conservan como NaN hasta el ultimo periodo con dato de la tabla;
no se rellenan.
"""
from __future__ import annotations

import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import HEADERS, RAW, cached, download, read_excel_any, save  # noqa: E402

warnings.filterwarnings("ignore")

BASE = "https://apps.fomento.gob.es/BoletinOnline2/sedal"
XLS_DIR = RAW / "v2_orig" / "mivau"
FUENTE = "MIVAU - Boletin Online Fomento/Transportes (sedal)"
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}

CCAA = {
    "Andalucía", "Aragón", "Asturias (Principado de )", "Asturias (Principado de)", "Balears (Illes)",
    "Canarias", "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña", "Comunidad Valenciana",
    "Comunitat Valenciana", "Extremadura", "Galicia", "Madrid (Comunidad de)", "Murcia (Región de)",
    "Navarra (Comunidad Foral de)", "Navarra (C. Foral de)", "País Vasco", "Rioja (La)",
}
CIUDADES = {"Ceuta y Melilla", "Ceuta", "Melilla"}
NO_TERRITORIO = re.compile(r"^(nota|nd[\s\-.:]|fuente|unidad|tabla|\(|\*)", re.I)


def _s(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return re.sub(r"\s+", " ", str(x)).strip()


def _num(x) -> float:
    if isinstance(x, (int, float, np.integer, np.floating)) and not pd.isna(x):
        return float(x)
    s = _s(x).replace(" ", "").replace("\xa0", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return np.nan  # 'ND', 'n.r.', '---', vacio
    return float(s)


def _slug(s: str) -> str:
    s = s.lower()
    for a, b in {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n", "à": "a",
                 "è": "e", "ò": "o", "ç": "c", "·": ""}.items():
        s = s.replace(a, b)
    s = re.sub(r"\(.*?\)", lambda m: " " + m.group(0)[1:-1] + " ", s)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def nivel_de(nombre: str) -> str:
    if nombre == "TOTAL NACIONAL":
        return "nacional"
    if nombre in CCAA:
        return "ccaa"
    if nombre in CIUDADES:
        return "ciudad_autonoma"
    return "provincia"


def titulo(sh: pd.DataFrame) -> str:
    txt = [_s(sh.iat[r, 1]) for r in range(min(14, sh.shape[0])) if sh.shape[1] > 1]
    txt = [t for t in txt if len(t) > 2]
    i = next((k for k, t in enumerate(txt) if t.lower().startswith("tabla")), 0)
    return " | ".join(txt[i:i + 3])[:300]


def label_col(sh: pd.DataFrame) -> int:
    return 1 if sh.shape[1] > 1 and sh.iloc[:, 1].map(lambda v: isinstance(v, str)).sum() > 3 else 0


def encabezado(sh: pd.DataFrame, tipo: str):
    """Devuelve (fila_inicio_datos, {col: (anio, periodo_str)}) segun el formato de la tabla."""
    if tipo == "trimestral":
        yr = qr = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if yr is None and any(re.fullmatch(r"Año \d{4}", v) for v in vals):
                yr = r
            if qr is None and sum(bool(re.fullmatch(r"[1-4]º", v)) for v in vals) >= 2:
                qr = r
        if yr is None or qr is None:
            raise ValueError("cabecera trimestral no encontrada")
        anio, cur = {}, None
        for c in range(sh.shape[1]):
            m = re.fullmatch(r"Año (\d{4})", _s(sh.iat[yr, c]))
            if m:
                cur = int(m.group(1))
            anio[c] = cur
        cols = {}
        for c in range(sh.shape[1]):
            v = _s(sh.iat[qr, c])
            if re.fullmatch(r"[1-4]º", v) and anio.get(c):
                cols[c] = (anio[c], int(v[0]))
        return qr + 1, cols
    if tipo == "mensual":
        ym = mr = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if ym is None and any(re.match(r"^\d{4} por meses", v) for v in vals):
                ym = r
            if mr is None and sum(v[:3].lower() in MESES and v.endswith(".") for v in vals) >= 6:
                mr = r
        if ym is None or mr is None:
            raise ValueError("cabecera mensual no encontrada")
        anio, cur = {}, None
        for c in range(sh.shape[1]):
            m = re.match(r"^(\d{4}) por meses", _s(sh.iat[ym, c]))
            if m:
                cur = int(m.group(1))
            anio[c] = cur
        cols = {}
        for c in range(sh.shape[1]):
            v = _s(sh.iat[mr, c]).lower()
            if v[:3] in MESES and v.endswith(".") and anio.get(c):
                cols[c] = (anio[c], MESES[v[:3]])
        return mr + 1, cols
    if tipo == "anual":
        yr = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if len([v for v in vals if re.fullmatch(r"(19|20)\d{2}(\.0)?", v)]) >= 5:
                yr = r
                break
        if yr is None:
            raise ValueError("fila de años no encontrada")
        cols = {c: (int(float(_s(sh.iat[yr, c]))), 1) for c in range(sh.shape[1])
                if re.fullmatch(r"(19|20)\d{2}(\.0)?", _s(sh.iat[yr, c]))}
        return yr + 1, cols
    raise ValueError(tipo)


def parse_tabla(sheet: pd.DataFrame, code: str, tipo: str, prefijo: str, unidad: str,
                esperado: str) -> pd.DataFrame:
    """Parsea una tabla del Boletin. `esperado` = fragmento del titulo que DEBE aparecer (verificacion)."""
    tit = titulo(sheet)
    cab = " ".join(_s(sheet.iat[r, c]) for r in range(0, 12) for c in range(min(3, sheet.shape[1])))
    if esperado.lower() not in (tit + " " + cab).lower():
        raise ValueError(f"{code}: el titulo no coincide con '{esperado}' -> '{tit}'")
    inicio, cols = encabezado(sheet, tipo)
    lc = label_col(sheet)
    url = f"{BASE}/{code}.XLS"
    recs, ccaa_act = [], ""
    for r in range(inicio, sheet.shape[0]):
        nombre = _s(sheet.iat[r, lc])
        if not nombre or NO_TERRITORIO.match(nombre):
            continue
        celdas = {c: sheet.iat[r, c] for c in cols}
        if all(_s(v) == "" for v in celdas.values()):
            continue  # fila de texto (titulo, nota) sin valores
        if nombre in CCAA or nombre == "TOTAL NACIONAL" or nombre in CIUDADES:
            if nombre in CCAA:
                ccaa_act = nombre
        niv = nivel_de(nombre)
        if niv == "provincia" and not ccaa_act:
            print(f"  [aviso] {code}: provincia '{nombre}' sin CCAA previa")
        if niv == "nacional":
            serie = f"{prefijo}_nacional"
        else:
            serie = f"{prefijo}_{niv}_{_slug(nombre)}"
        for c, (y, p) in cols.items():
            v = _num(celdas[c])
            if tipo == "trimestral":
                fecha, periodo = f"{y}-{3 * p - 2:02d}-01", f"{y}T{p}"
            elif tipo == "mensual":
                fecha, periodo = f"{y}-{p:02d}-01", f"{y}-{p:02d}"
            else:
                fecha, periodo = f"{y}-01-01", str(y)
            recs.append({
                "fecha": fecha, "periodo": periodo, "serie": serie, "valor": v, "unidad": unidad,
                "fuente": FUENTE, "url": url, "territorio": nombre, "nivel": niv,
                "ccaa": ccaa_act if niv == "provincia" else (nombre if niv == "ccaa" else ""),
                "tabla_codigo": code, "tabla_titulo": tit,
            })
    df = pd.DataFrame(recs)
    if df.empty:
        raise ValueError(f"{code}: sin filas parseadas")
    # Se conservan NaN (ND) hasta el ultimo periodo con dato de la tabla; no se rellenan.
    ultimo = df.loc[df.valor.notna(), "fecha"].max()
    df = df[df.fecha <= ultimo].reset_index(drop=True)
    n_ser = df.serie.nunique()
    print(f"  [parse] {code} '{tit[:70]}': {n_ser} series, {df.fecha.min()} -> {ultimo}, "
          f"NaN={int(df.valor.isna().sum())}")
    return df


def descargar(code: str) -> pd.DataFrame:
    """Verifica el endpoint (peticion pequeña: cabecera XLS) y descarga el original sin editar."""
    url = f"{BASE}/{code}.XLS"
    dest = XLS_DIR / f"{code}.XLS"
    if not (dest.exists() and dest.stat().st_size > 0):
        r = requests.get(url, headers=HEADERS, timeout=60, stream=True)
        magic = next(r.iter_content(4), b"")
        r.close()
        if r.status_code != 200 or not magic.startswith((b"\xd0\xcf\x11\xe0", b"PK\x03\x04")):
            raise RuntimeError(f"endpoint {url}: HTTP {r.status_code}, cabecera {magic!r}")
    p = download(url, dest)
    return read_excel_any(p)


TABLAS_SUELO = [
    ("36400500", "suelo_pm2", "trimestral", "euros/m2", "Precio medio del metro cuadrado de suelo urbano por comunidades"),
    ("36403000", "suelo_pm2_m50k", "trimestral", "euros/m2",
     "Precio medio del metro cuadrado de suelo urbano en municipios de más de 50.000"),
]
TABLAS_PROTEGIDA = [
    ("31303000", "prot_provisional_anual", "anual", "viviendas", "Número de calificaciones provisionales. Planes estatales y planes autonómicos"),
    ("31306000", "prot_definitiva_anual", "anual", "viviendas", "Número de calificaciones definitivas. Planes estatales y planes autonómicos"),
    ("31202000", "prot_provisional_mensual", "mensual", "viviendas", "Número de calificaciones provisionales. Planes estatales y planes autónomicos"),
    ("31205000", "prot_definitiva_mensual", "mensual", "viviendas", "Número de calificaciones definitivas. Planes estatales y autonómicos"),
]
TABLAS_INICIADAS = [
    ("32200500", "viv_libres_iniciadas_anual", "anual", "viviendas", "Número de viviendas libres iniciadas."),
    ("32201000", "viv_libres_terminadas_anual", "anual", "viviendas", "Número de viviendas libres terminadas."),
    ("32100500", "viv_libres_iniciadas_mensual", "mensual", "viviendas", "Número de viviendas libres iniciadas. Series mensuales"),
    ("32101000", "viv_libres_terminadas_mensual", "mensual", "viviendas", "Número de viviendas libres terminadas. Series mensuales"),
]


def construir(nombre_csv: str, tablas: list) -> pd.DataFrame:
    partes = []
    for code, prefijo, tipo, unidad, esperado in tablas:
        sheet = list(descargar(code).values())[0]
        partes.append(parse_tabla(sheet, code, tipo, prefijo, unidad, esperado))
    return pd.concat(partes, ignore_index=True)


def validar_iniciadas(df: pd.DataFrame) -> None:
    """Control: total nacional anual (32200500) frente a la suma de meses (32100500) en años comunes."""
    a = df[(df.serie == "viv_libres_iniciadas_anual_nacional")].set_index("periodo")["valor"]
    m = df[(df.serie == "viv_libres_iniciadas_mensual_nacional")].copy()
    m["y"] = m.periodo.str[:4]
    s = m.groupby("y")["valor"].sum(min_count=12)
    comunes = [y for y in s.index if y in a.index and pd.notna(s[y]) and pd.notna(a[y])]
    if comunes:
        dif = max(abs(a[y] - s[y]) / a[y] for y in comunes) * 100
        print(f"  [control] iniciadas nacional anual vs suma mensual {comunes[0]}-{comunes[-1]}: "
              f"dif. relativa máxima {dif:.2f}% (años {len(comunes)})")


def main() -> None:
    if not cached("mivau_v2_suelo.csv"):
        save(construir("mivau_v2_suelo.csv", TABLAS_SUELO), "mivau_v2_suelo.csv", FUENTE)
    if not cached("mivau_v2_protegida.csv"):
        save(construir("mivau_v2_protegida.csv", TABLAS_PROTEGIDA), "mivau_v2_protegida.csv", FUENTE)
    if not cached("mivau_v2_iniciadas_terminadas_prov.csv"):
        df = construir("mivau_v2_iniciadas_terminadas_prov.csv", TABLAS_INICIADAS)
        validar_iniciadas(df)
        save(df, "mivau_v2_iniciadas_terminadas_prov.csv", FUENTE)
    # (c) licencias municipales de obra: no publicadas en el Boletin Online; ver docs/v2/fuentes_fallidas.md


if __name__ == "__main__":
    main()
