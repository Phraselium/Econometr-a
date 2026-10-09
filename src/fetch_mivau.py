"""Descarga MIVAU (tablas XLS del Boletin Online de Fomento, carpeta sedal/) e INE (viviendas turisticas).

Salidas (formato largo, data/raw):
  mivau_valor_tasado_nacional_ccaa_prov.csv   tabla 35101000 (trimestral, 1995-)
  mivau_valor_tasado_municipios.csv           tabla 35103500 (trimestral, >25.000 hab., 2005-)
  mivau_visados.csv                           tabla 32100500 (viviendas libres iniciadas, mensual, 2008-)
  mivau_fin_obra.csv                          tabla 32101000 (viviendas libres terminadas, mensual, 2008-)
  mivau_parque.csv                            tabla 33100500 (total viviendas, anual, 2001-)
  mivau_transacciones_*.csv                   tablas 34010110 (total), 340101i0/j0/k0 (extranjeros residentes),
                                              340101d0 (residencia del comprador: residentes / no residentes),
                                              34010210 (todos los municipios publicados)
  ine_vut_*.csv                               INE tablas 39363-39366 (experimental, VUT)

Los XLS originales se guardan sin editar en data/raw/mivau_xls/ (algunos llevan extension .XLS
pero son xlsx; el lector detecta el formato por la cabecera del fichero).
Idempotente: si el CSV de salida existe no se vuelve a descargar (FORCE=1 para rehacer).
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

from utils_fetch import RAW, cached, download, get, read_excel_any, save

BASE = "https://apps.fomento.gob.es/BoletinOnline2/sedal"
XLS_DIR = RAW / "mivau_xls"
FUENTE_MIVAU = "MIVAU - Boletin Online Fomento (sedal)"
FUENTE_INE = "INE - Estadistica experimental viviendas turisticas"
INE_API = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{code}"
TZ = ZoneInfo("Europe/Madrid")

CCAA = {
    "Andalucía", "Aragón", "Asturias (Principado de )", "Balears (Illes)", "Canarias",
    "Cantabria", "Castilla y León", "Castilla-La Mancha", "Cataluña", "Comunitat Valenciana",
    "Extremadura", "Galicia", "Madrid (Comunidad de)", "Murcia (Región de)",
    "Navarra (Comunidad Foral de)", "País Vasco", "Rioja (La)",
    # variantes de etiqueta que aparecen en otras hojas/tablas del mismo MIVAU
    "Comunidad Valenciana", "Asturias (Principado de)", "Navarra (C. Foral de)", "Navarra (Com. Foral de)",
}
CIUDADES = {"Ceuta y Melilla", "Ceuta", "Melilla"}
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
# Filas que no son territorios (notas, pies, cabeceras)
NO_TERRITORIO = re.compile(r"^(n\.r|nota|nd[\s\-.:]|\(|fuente|unidad|tabla|n\.º|número|años|año|"
                           r"primer|segundo|tercer|cuarto|total de|para |\*|ver |ce )", re.I)


def _s(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return re.sub(r"\s+", " ", str(x)).strip()


def _num(x) -> float:
    if isinstance(x, (int, float, np.integer, np.floating)) and not pd.isna(x):
        return float(x)
    s = _s(x).replace(" ", "").replace("\xa0", "")
    if not re.fullmatch(r"-?\d+(\.\d+)?", s):
        return np.nan  # 'n.r', '---', 'ND', vacio
    return float(s)


def _slug(s: str) -> str:
    s = s.lower()
    rep = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n", "à": "a", "è": "e", "ò": "o", "ç": "c", "·": ""}
    for a, b in rep.items():
        s = s.replace(a, b)
    s = re.sub(r"\(.*?\)", lambda m: " " + m.group(0)[1:-1] + " ", s)
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _sufijo(niv: str, nombre: str) -> str:
    """Parte territorial del nombre de serie: 'nacional' o '<nivel>_<territorio>'."""
    return "nacional" if nombre == "TOTAL NACIONAL" else f"{niv}_{_slug(nombre)}"


def nivel_de(nombre: str) -> str:
    if nombre == "TOTAL NACIONAL":
        return "nacional"
    if nombre in CCAA:
        return "ccaa"
    if nombre in CIUDADES:
        return "ciudad_autonoma"
    return "provincia"


def titulo(sh: pd.DataFrame) -> str:
    """Titulo de la tabla: primeras lineas de texto a partir de 'Tabla ...'."""
    txt = [_s(sh.iat[r, 1]) for r in range(min(14, sh.shape[0])) if sh.shape[1] > 1]
    txt = [t for t in txt if len(t) > 2]
    i = next((k for k, t in enumerate(txt) if t.lower().startswith("tabla")), 0)
    return " | ".join(txt[i:i + 3])[:300]


def xls_path(code: str) -> Path:
    return XLS_DIR / f"{code}.XLS"


def ensure_xls(code: str) -> Path:
    return download(f"{BASE}/{code}.XLS", xls_path(code))


def _label_col(sh: pd.DataFrame) -> int:
    return 1 if sh.shape[1] > 1 and sh.iloc[:, 1].map(lambda v: isinstance(v, str)).sum() > 3 else 0


# ---------------------------------------------------------------- parsers
def parse_trimestral_ancho(sheets: dict, code: str, prefijo: str, unidad: str) -> pd.DataFrame:
    """Tablas con bloques 'Año YYYY' y columnas 1º..4º (trimestre). Filas = territorios."""
    out = []
    url = f"{BASE}/{code}.XLS"
    for sname, sh in sheets.items():
        year_row = q_row = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if year_row is None and any(re.fullmatch(r"Año \d{4}", v) for v in vals):
                year_row = r
            if q_row is None and sum(bool(re.fullmatch(r"[1-4]º", v)) for v in vals) >= 2:
                q_row = r
        if year_row is None or q_row is None:
            print(f"  [aviso] {code} hoja '{sname}': sin cabecera de año/trimestre, se omite")
            continue
        ycol, cur = {}, None
        for c in range(sh.shape[1]):
            m = re.fullmatch(r"Año (\d{4})", _s(sh.iat[year_row, c]))
            if m:
                cur = int(m.group(1))
            ycol[c] = cur
        qcol = {c: int(_s(sh.iat[q_row, c])[0]) for c in range(sh.shape[1])
                if re.fullmatch(r"[1-4]º", _s(sh.iat[q_row, c]))}
        lc = _label_col(sh)
        tit = titulo(sh)
        for r in range(q_row + 1, sh.shape[0]):
            nombre = _s(sh.iat[r, lc])
            if not nombre or NO_TERRITORIO.match(nombre):
                continue
            niv = nivel_de(nombre)
            for c, q in qcol.items():
                y = ycol.get(c)
                if y is None:
                    continue
                v = _num(sh.iat[r, c])
                if np.isnan(v):
                    continue
                out.append({
                    "fecha": f"{y}-{3 * q - 2:02d}-01", "periodo": f"{y}T{q}",
                    "serie": f"{prefijo}_{_sufijo(niv, nombre)}", "valor": v, "unidad": unidad,
                    "fuente": FUENTE_MIVAU, "url": url, "territorio": nombre, "nivel": niv,
                    "tabla_codigo": code, "tabla_titulo": tit,
                })
    return pd.DataFrame(out)


def parse_mensual_por_meses(sheets: dict, code: str, prefijo: str, unidad: str) -> pd.DataFrame:
    """Tablas con bloques 'YYYY por meses' y columnas Ene.-Dic. Filas = territorios."""
    out = []
    url = f"{BASE}/{code}.XLS"
    for sname, sh in sheets.items():
        ymes = mrow = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if ymes is None and any(re.match(r"^\d{4} por meses", v) for v in vals):
                ymes = r
            if mrow is None and sum(v[:3].lower() in MESES and v.endswith(".") for v in vals) >= 6:
                mrow = r
        if ymes is None or mrow is None:
            print(f"  [aviso] {code}: sin cabecera mensual en '{sname}'")
            continue
        ycol, cur = {}, None
        for c in range(sh.shape[1]):
            m = re.match(r"^(\d{4}) por meses", _s(sh.iat[ymes, c]))
            if m:
                cur = int(m.group(1))
            ycol[c] = cur
        mcol = {}
        for c in range(sh.shape[1]):
            v = _s(sh.iat[mrow, c]).lower()
            if v[:3] in MESES and v.endswith("."):
                mcol[c] = MESES[v[:3]]
        lc = _label_col(sh)
        tit = titulo(sh)
        for r in range(mrow + 1, sh.shape[0]):
            nombre = _s(sh.iat[r, lc])
            if not nombre or NO_TERRITORIO.match(nombre):
                continue
            niv = nivel_de(nombre)
            for c, mes in mcol.items():
                y = ycol.get(c)
                if y is None:
                    continue
                v = _num(sh.iat[r, c])
                if np.isnan(v):
                    continue
                out.append({
                    "fecha": f"{y}-{mes:02d}-01", "periodo": f"{y}-{mes:02d}",
                    "serie": f"{prefijo}_{_sufijo(niv, nombre)}", "valor": v, "unidad": unidad,
                    "fuente": FUENTE_MIVAU, "url": url, "territorio": nombre, "nivel": niv,
                    "tabla_codigo": code, "tabla_titulo": tit,
                })
    return pd.DataFrame(out)


def parse_anual_parque(sheets: dict, code: str, prefijo: str, unidad: str) -> pd.DataFrame:
    """Estimacion del parque: fila de anos (2001, 2002...) y filas = territorios. Stock a 31-dic."""
    out = []
    url = f"{BASE}/{code}.XLS"
    for sname, sh in sheets.items():
        yrow = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            yrs = [v for v in vals if re.fullmatch(r"(19|20)\d{2}(\.0)?", v)]
            if len(yrs) >= 5:
                yrow = r
                break
        if yrow is None:
            print(f"  [aviso] {code}: sin fila de anos en '{sname}'")
            continue
        ycol = {c: int(float(_s(sh.iat[yrow, c]))) for c in range(sh.shape[1])
                if re.fullmatch(r"(19|20)\d{2}(\.0)?", _s(sh.iat[yrow, c]))}
        lc = _label_col(sh)
        tit = titulo(sh)
        for r in range(yrow + 1, sh.shape[0]):
            nombre = _s(sh.iat[r, lc])
            if not nombre or NO_TERRITORIO.match(nombre):
                continue
            niv = nivel_de(nombre)
            for c, y in ycol.items():
                v = _num(sh.iat[r, c])
                if np.isnan(v):
                    continue
                out.append({
                    "fecha": f"{y}-12-31", "periodo": str(y),
                    "serie": f"{prefijo}_{_sufijo(niv, nombre)}", "valor": v, "unidad": unidad,
                    "fuente": FUENTE_MIVAU, "url": url, "territorio": nombre, "nivel": niv,
                    "tabla_codigo": code, "tabla_titulo": tit,
                })
    return pd.DataFrame(out)


def parse_municipios(sheets: dict, code: str) -> pd.DataFrame:
    """Valor tasado medio municipios >25.000 hab.: una hoja por trimestre (T1A2005...).
    El formato de columnas cambia entre trimestres; se localiza la columna 'valor ... Total'."""
    out, vistos = [], {}
    url = f"{BASE}/{code}.XLS"
    for sname, sh in sheets.items():
        m = re.search(r"T(\d)A(\d{4})", str(sname))
        if not m:
            continue
        q, y = int(m.group(1)), int(m.group(2))
        hr = None
        for r in range(min(40, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if "Provincia" in vals and "Municipio" in vals:
                hr = r
                pc, mc = vals.index("Provincia"), vals.index("Municipio")
                break
        if hr is None:
            print(f"  [aviso] {code} hoja '{sname}': sin cabecera Provincia/Municipio")
            continue
        # Etiqueta de columna = texto de la fila de grupo (con relleno horizontal) + subcabeceras
        grupo, last = {}, ""
        for c in range(sh.shape[1]):
            t = _s(sh.iat[hr, c])
            last = t if t else last
            grupo[c] = last
        vc = None
        for c in range(sh.shape[1]):
            if c in (pc, mc):
                continue
            etiqueta = " ".join(
                [grupo.get(c, "")] + [_s(sh.iat[rr, c]) for rr in range(hr + 1, min(hr + 4, sh.shape[0]))]
            ).lower()
            if "valor" in etiqueta and "total" in etiqueta and "tasaci" not in etiqueta and "número" not in etiqueta:
                vc = c
                break
        if vc is None:
            print(f"  [aviso] {code} hoja '{sname}': no encuentro columna de valor total")
            continue
        prov = ""
        for r in range(hr + 1, sh.shape[0]):
            muni = _s(sh.iat[r, mc])
            if not muni or NO_TERRITORIO.match(muni) or muni.lower() == "municipio":
                continue
            p = _s(sh.iat[r, pc])
            prov = p or prov
            v = _num(sh.iat[r, vc])
            if np.isnan(v):
                continue
            serie = f"valor_tasado_mun_{_slug(muni)}"
            if vistos.get(serie, prov) != prov:  # colision de nombre entre provincias
                serie = f"{serie}_{_slug(prov)}"
            vistos.setdefault(serie, prov)
            out.append({
                "fecha": f"{y}-{3 * q - 2:02d}-01", "periodo": f"{y}T{q}",
                "serie": serie, "valor": v, "unidad": "euros/m2",
                "fuente": FUENTE_MIVAU, "url": url, "territorio": muni, "nivel": "municipio",
                "provincia": prov, "tabla_codigo": code,
                "tabla_titulo": "Valor tasado medio de vivienda libre, municipios >25.000 hab.",
            })
    return pd.DataFrame(out)


def parse_residencia(sheets: dict, code: str) -> pd.DataFrame:
    """Transacciones por residencia del comprador (Tabla 1.6): cabecera de dos filas
    (grupo: TOTAL / Residentes en España / No residentes en España / No consta; subgrupo: Total / Españoles / Extranjeros / No consta)."""
    out = []
    url = f"{BASE}/{code}.XLS"
    grp_map = {"TOTAL": "total", "Residentes en España": "residentes", "No residentes en España": "no_residentes",
               "No consta": "no_consta"}
    sub_map = {"Total": "total", "Españoles": "espanoles", "Extranjeros": "extranjeros", "No consta": "no_consta"}
    for sname, sh in sheets.items():
        m = re.match(r"^\s*(\d)t (\d{4})", str(sname))
        if not m:
            continue
        q, y = int(m.group(1)), int(m.group(2))
        hr = next((r for r in range(min(25, sh.shape[0])) if "TOTAL" in [_s(v) for v in sh.iloc[r]]), None)
        if hr is None:
            print(f"  [aviso] {code} hoja '{sname}': sin cabecera TOTAL")
            continue
        claves, last = {}, ""
        for c in range(sh.shape[1]):
            g = _s(sh.iat[hr, c])
            last = g if g else last
            sub = _s(sh.iat[hr + 1, c]) if hr + 1 < sh.shape[0] else ""
            if last in grp_map:
                clave = grp_map[last] + ("_" + sub_map[sub] if sub in sub_map and last != "TOTAL" else "")
                if last == "TOTAL" and sub in sub_map:
                    clave = "total_" + sub_map[sub]
                claves[c] = clave
        lc = _label_col(sh)
        tit = titulo(sh)
        for r in range(hr + 2, sh.shape[0]):
            nombre = _s(sh.iat[r, lc])
            if not nombre or NO_TERRITORIO.match(nombre):
                continue
            niv = nivel_de(nombre)
            for c, clave in claves.items():
                v = _num(sh.iat[r, c])
                if np.isnan(v):
                    continue
                out.append({
                    "fecha": f"{y}-{3 * q - 2:02d}-01", "periodo": f"{y}T{q}",
                    "serie": f"tx_residencia_{clave}_{_sufijo(niv, nombre)}", "valor": v,
                    "unidad": "transacciones", "fuente": FUENTE_MIVAU, "url": url,
                    "territorio": nombre, "nivel": niv, "tabla_codigo": code, "tabla_titulo": tit,
                })
    return pd.DataFrame(out)


def parse_tx_municipios(sheets: dict, code: str) -> pd.DataFrame:
    """Transacciones de vivienda por municipio (Tabla 2 del Boletin, trimestral, todos los municipios publicados).
    Filas: CCAA (mayusculas, sin valores), provincia (sin valores) y municipio (con valores).
    No se filtra por poblacion: la tabla no la incluye (el filtro >25.000 requiere padron INE)."""
    out, vistos = [], {}
    url = f"{BASE}/{code}.XLS"
    sh = list(sheets.values())[0]
    year_row = q_row = None
    for r in range(min(25, sh.shape[0])):
        vals = [_s(v) for v in sh.iloc[r]]
        if year_row is None and any(re.fullmatch(r"Año \d{4}", v) for v in vals):
            year_row = r
        if q_row is None and sum(bool(re.fullmatch(r"[1-4]º", v)) for v in vals) >= 2:
            q_row = r
    ycol, cur = {}, None
    for c in range(sh.shape[1]):
        m = re.fullmatch(r"Año (\d{4})", _s(sh.iat[year_row, c]))
        if m:
            cur = int(m.group(1))
        ycol[c] = cur
    qcol = {c: int(_s(sh.iat[q_row, c])[0]) for c in range(sh.shape[1]) if re.fullmatch(r"[1-4]º", _s(sh.iat[q_row, c]))}
    tit = titulo(sh)
    ccaa = prov = ""
    for r in range(q_row + 1, sh.shape[0]):
        nombre = _s(sh.iat[r, 1])
        if not nombre or NO_TERRITORIO.match(nombre):
            continue
        valores = {c: _num(sh.iat[r, c]) for c in qcol}
        if all(np.isnan(v) for v in valores.values()):
            if nombre.isupper():
                ccaa, prov = nombre.title(), ""
            else:
                prov = nombre
            continue
        for c, q in qcol.items():
            y, v = ycol.get(c), valores[c]
            if y is None or np.isnan(v):
                continue
            serie = f"tx_municipio_{_slug(nombre)}"
            if vistos.get(serie, prov) != prov:  # mismo nombre en otra provincia
                serie = f"{serie}_{_slug(prov)}"
            vistos.setdefault(serie, prov)
            out.append({
                "fecha": f"{y}-{3 * q - 2:02d}-01", "periodo": f"{y}T{q}", "serie": serie, "valor": v,
                "unidad": "transacciones", "fuente": FUENTE_MIVAU, "url": url,
                "territorio": nombre, "nivel": "municipio", "ccaa": ccaa, "provincia": prov,
                "tabla_codigo": code, "tabla_titulo": tit,
            })
    return pd.DataFrame(out)


_STOP = {"de", "la", "el", "del", "los", "las", "y", "en", "do", "da"}


def clave_municipio(nombre: str) -> str:
    """Clave para emparejar nombres de municipio entre tablas MIVAU (acentos, articulos, barras)."""
    s = unicodedata.normalize("NFKD", str(nombre)).encode("ascii", "ignore").decode().lower()
    s = s.split("/")[0]
    s = re.sub(r"\(.*?\)|,", " ", s)
    toks = [t for t in re.split(r"[^a-z]+", s) if t and t not in _STOP]
    return " ".join(sorted(toks))


# Nombres de la tabla 35103500 que en la tabla 34010210 aparecen con otra grafia (valenciano, euskera...)
ALIAS_MUNICIPIO = {
    "Burriana": "Borriana/Burriana", "Mahón": "Maó", "Calpe/Calp": "Calp",
    "San Sebastián/Donostia": "Donostia-San Sebastián", "Vitoria": "Vitoria-Gasteiz",
    "Santa Coloma Gramanet": "Santa Coloma de Gramenet", "Santa Cruz deTenerife": "Santa Cruz de Tenerife",
}


def filtrar_municipios_grandes(tx: pd.DataFrame) -> pd.DataFrame:
    """Conserva los municipios de la lista >25.000 hab. (tabla 35103500), emparejados por nombre.
    Si un nombre aparece en varias secciones (p. ej. Cieza en Murcia y en Cantabria), se elige la
    sección cuya provincia coincide con la de la lista; si la sección no trae provincia, la CCAA."""
    val = pd.read_csv(RAW / "mivau_valor_tasado_municipios.csv", usecols=["territorio", "provincia"]).drop_duplicates()
    val["k"] = val["territorio"].map(lambda t: clave_municipio(ALIAS_MUNICIPIO.get(t, t)))
    prov_de = val.groupby("k")["provincia"].agg(lambda x: {clave_municipio(p) for p in x.dropna()})
    tx = tx.copy()
    tx["k"] = tx["territorio"].map(clave_municipio)
    tx = tx[tx["k"].isin(prov_de.index)]
    ok = []
    for k, prov, ccaa in zip(tx["k"], tx["provincia"].fillna(""), tx["ccaa"].fillna("")):
        provs = prov_de[k]
        if prov:
            ok.append(clave_municipio(prov) in provs)
        else:
            ok.append(any(pp and pp in clave_municipio(ccaa) for pp in provs))
    tx["_ok"] = ok
    partes = []
    for k, g in tx.groupby("k", sort=False):
        if g["ccaa"].fillna("").nunique() <= 1:
            partes.append(g)  # un solo municipio con ese nombre: se mantiene
            continue
        cuadra = g[g["_ok"]]
        if cuadra.empty:
            raise ValueError(f"municipio ambiguo sin resolver: {k}")
        partes.append(cuadra)  # varios: solo la seccion cuya provincia coincide
    out = pd.concat(partes).drop(columns=["k", "_ok"])
    if out.duplicated(["serie", "fecha"]).any():
        raise ValueError("duplicados serie/fecha en transacciones municipales tras el filtro")
    return out


def parse_extranjeros(sheets: dict, code: str, prefijo: str) -> pd.DataFrame:
    """Transacciones de extranjeros: una hoja por trimestre ('1t 2019'); columnas TOTAL / libre / protegida."""
    out = []
    url = f"{BASE}/{code}.XLS"
    for sname, sh in sheets.items():
        m = re.match(r"^\s*(\d)t (\d{4})", str(sname))
        if not m:
            continue
        q, y = int(m.group(1)), int(m.group(2))
        hr = cols = None
        for r in range(min(25, sh.shape[0])):
            vals = [_s(v) for v in sh.iloc[r]]
            if "TOTAL" in vals and any(v.startswith("Vivienda libre") for v in vals):
                hr = r
                cols = {"total": vals.index("TOTAL")}
                cols["libre"] = next(i for i, v in enumerate(vals) if v.startswith("Vivienda libre"))
                cols["protegida"] = next(i for i, v in enumerate(vals) if v.startswith("Vivienda protegida"))
                break
        if hr is None:
            print(f"  [aviso] {code} hoja '{sname}': sin cabecera TOTAL")
            continue
        lc = _label_col(sh)
        tit = titulo(sh)
        for r in range(hr + 1, sh.shape[0]):
            nombre = _s(sh.iat[r, lc])
            if not nombre or NO_TERRITORIO.match(nombre):
                continue
            niv = nivel_de(nombre)
            for tipo, c in cols.items():
                v = _num(sh.iat[r, c])
                if np.isnan(v):
                    continue
                out.append({
                    "fecha": f"{y}-{3 * q - 2:02d}-01", "periodo": f"{y}T{q}",
                    "serie": f"{prefijo}_{tipo}_{_sufijo(niv, nombre)}", "valor": v, "unidad": "transacciones",
                    "fuente": FUENTE_MIVAU, "url": url, "territorio": nombre, "nivel": niv,
                    "tabla_codigo": code, "tabla_titulo": tit,
                })
    return pd.DataFrame(out)


# ---------------------------------------------------------------- INE
def ine_long(data: list, url: str, filtro=None) -> pd.DataFrame:
    rows = []
    for s in data:
        nombre = s["Nombre"]
        partes = [p.strip() for p in nombre.split(". ")]
        territorio = partes[0]
        variable = partes[1] if len(partes) > 1 else ""
        if filtro and not filtro(territorio):
            continue
        vl = variable.lower()
        if "porcentaje" in vl:
            unidad, vslug = "%", "pct_viv_turisticas_sobre_total"
        elif "por vivienda" in vl:
            unidad, vslug = "plazas/vivienda", "plazas_por_vivienda"
        elif "plazas" in vl:
            unidad, vslug = "plazas", "plazas"
        elif "viviendas" in vl:
            unidad, vslug = "viviendas", "viviendas_turisticas"
        else:
            unidad, vslug = "", _slug(variable)
        for d in s["Data"]:
            f = dt.datetime.fromtimestamp(d["Fecha"] / 1000, tz=TZ).date()
            rows.append({
                "fecha": f.isoformat(), "periodo": f"{f.year}-{f.month:02d}",
                "serie": f"ine_vut_{_slug(territorio)}_{vslug}", "valor": d.get("Valor"),
                "unidad": unidad, "fuente": FUENTE_INE, "url": url,
                "territorio": territorio, "fk_periodo": d.get("FK_Periodo"), "cod_serie": s.get("COD"),
            })
    df = pd.DataFrame(rows)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df


def _sin_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Quita filas repetidas idénticas (INE 39364 y 39365 solapan series); falla si hay valores distintos."""
    df = df.drop_duplicates(subset=["serie", "fecha", "valor"])
    if df.duplicated(["serie", "fecha"]).any():
        raise ValueError("series con valores distintos para la misma fecha")
    return df


def main() -> None:
    XLS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Valor tasado (prioridad 1)
    if not cached("mivau_valor_tasado_nacional_ccaa_prov.csv"):
        p = ensure_xls("35101000")
        df = parse_trimestral_ancho(read_excel_any(p), "35101000", "valor_tasado_libre", "euros/m2")
        save(df, "mivau_valor_tasado_nacional_ccaa_prov.csv", FUENTE_MIVAU)
    if not cached("mivau_valor_tasado_municipios.csv"):
        p = ensure_xls("35103500")
        df = parse_municipios(read_excel_any(p), "35103500")
        save(df, "mivau_valor_tasado_municipios.csv", FUENTE_MIVAU)

    # 2. Visados / fin de obra (viviendas libres iniciadas y terminadas, mensual)
    if not cached("mivau_visados.csv"):
        p = ensure_xls("32100500")
        save(parse_mensual_por_meses(read_excel_any(p), "32100500", "viv_libres_iniciadas", "viviendas"),
             "mivau_visados.csv", FUENTE_MIVAU)
    if not cached("mivau_fin_obra.csv"):
        p = ensure_xls("32101000")
        save(parse_mensual_por_meses(read_excel_any(p), "32101000", "viv_libres_terminadas", "viviendas"),
             "mivau_fin_obra.csv", FUENTE_MIVAU)

    # 3. Parque de viviendas (anual)
    if not cached("mivau_parque.csv"):
        p = ensure_xls("33100500")
        save(parse_anual_parque(read_excel_any(p), "33100500", "parque_total_viviendas", "viviendas"),
             "mivau_parque.csv", FUENTE_MIVAU)

    # 5. Transacciones (notarios): total y extranjeros
    if not cached("mivau_transacciones_total.csv"):
        p = ensure_xls("34010110")
        save(parse_trimestral_ancho(read_excel_any(p), "34010110", "tx_total", "transacciones"),
             "mivau_transacciones_total.csv", FUENTE_MIVAU)
    if not cached("mivau_transacciones_extranjeros.csv"):
        partes = []
        # 1.6.5 total, 1.6.5.1 vivienda nueva, 1.6.5.2 segunda mano (compradores extranjeros residentes)
        for code, pref in [("340101i0", "tx_extranj_residentes"),
                           ("340101j0", "tx_extranj_residentes_nuevas"),
                           ("340101k0", "tx_extranj_residentes_segunda_mano")]:
            p = ensure_xls(code)
            partes.append(parse_extranjeros(read_excel_any(p), code, pref))
        save(pd.concat(partes, ignore_index=True), "mivau_transacciones_extranjeros.csv", FUENTE_MIVAU)

    if not cached("mivau_transacciones_municipios.csv"):
        p = ensure_xls("34010210")
        tx = parse_tx_municipios(read_excel_any(p), "34010210")
        # Solo municipios >25.000 hab. (lista de la tabla 35103500); el resto del Boletin pesa ~240 MB
        tx = filtrar_municipios_grandes(tx)
        save(tx, "mivau_transacciones_municipios.csv", FUENTE_MIVAU)
    if not cached("mivau_transacciones_residencia.csv"):
        p = ensure_xls("340101d0")
        save(parse_residencia(read_excel_any(p), "340101d0"), "mivau_transacciones_residencia.csv", FUENTE_MIVAU)

    # 6. INE viviendas turisticas (experimental)
    if not cached("ine_vut_nacional_ccaa_prov.csv"):
        frames = []
        for code in ["39364", "39365"]:
            data = get(INE_API.format(code=code), as_json=True)
            frames.append(ine_long(data, INE_API.format(code=code)))
        save(_sin_duplicados(pd.concat(frames, ignore_index=True)), "ine_vut_nacional_ccaa_prov.csv", FUENTE_INE)
    if not cached("ine_vut_valencia_municipio.csv"):
        frames = []
        for code in ["39363", "39366"]:
            data = get(INE_API.format(code=code), as_json=True)
            frames.append(ine_long(data, INE_API.format(code=code),
                                   filtro=lambda t: t == "Valencia/València"))
        save(pd.concat(frames, ignore_index=True), "ine_vut_valencia_municipio.csv", FUENTE_INE)


if __name__ == "__main__":
    main()
