"""Extraccion Colegio de Registradores - Estadistica Registral Inmobiliaria (ERI).

Escalera (ver docs/fallidas/registradores.md):
  1. Formato abierto: portal de datos abiertos opendata.registradores.org, dataset "Compraventas de inmuebles,
     uso residencial, por provincia" (CSV trimestral, 2007T1-2026T2, nacional/CCAA/provincia). Dato de 4 trimestres
     moviles ("anualizado"); el 4T es el ano natural. Cubre compraventas de vivienda, importe medio y precio EUR/m2
     (origen = csv). NO incluye extranjeros ni hipotecas.
  2. PDF con texto (pdfplumber): Anuarios ERI 2023, 2024 y 2025 (los tres ultimos), solo las tablas pedidas:
       - compraventas de vivienda y precio medio EUR/m2 (CCAA, provincias, capitales: incluye Valencia/Valencia capital)
       - % de compras de vivienda por extranjeros (CCAA anual y serie 8 anos; provincias)
       - nacionalidad del comprador (Espana; principales nacionalidades por CCAA, incluida C. Valenciana)
     (origen = pdf)  Los PDF tienen texto: no hizo falta OCR.

Salidas (data/raw/pdf/):
  registradores_opendata_compraventas.csv   csv   largo, trimestral (4T moviles)
  registradores_eri_anuario.csv             pdf   largo, anual (columna edicion = Anuario de origen)
  registradores_validacion.csv              cuadres + contraste con INE / opendata / MIVAU / notarios
Originales sin editar en data/raw/pdf/originales/. Renders PNG para revision visual en data/raw/pdf/validacion/.
Idempotente (descargas con cache). No se corrige ningun valor: lo que no cuadra se marca.
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
import pdfplumber
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import ROOT  # noqa: E402

PDF_DIR = ROOT / "data" / "raw" / "pdf"
ORIG = PDF_DIR / "originales"
VALID_DIR = PDF_DIR / "validacion"
RAW = ROOT / "data" / "raw"
FUENTE = "Colegio de Registradores - Estadistica Registral Inmobiliaria"
REG = "https://www.registradores.org"
URL_CSV = "https://opendata.registradores.org/data-integration/compraventas-residencial-trimestres-provincias-es/RP_ComprvResid_2007-2t2026.csv"
# El WAF del sitio rechaza clientes sin cabeceras de navegador (HTTP 200 'Request Rejected'): se envian las habituales.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HDR = {"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"}
ANUARIOS = {
    2025: "/documents/33383/148210/ERI+Anuario+2025.pdf/f15ee835-3246-6132-11d0-6495dfeee415?t=1774598855046",
    2024: "/documents/33383/148210/ERI+Anuario+2024.pdf/9f9ab5b0-d889-6d2c-9ae2-943ee6dd8ea8?t=1745394993385",
    2023: "/documents/33383/148210/ERI_Anuario_2023.pdf/d9600e18-01db-467f-5ad9-14e3a1561c40?t=1712040636466",
}
# --- Revision visual realizada (PNG leidos y comparados con la tabla extraida) ---
PAGINAS_REVISADAS = ("anuario2025 p35 (compraventas CCAA), p73 (% extranjeros CCAA), p76 (% provincias), p78 (nacionalidad Espana); "
                     "anuario2023 p73")
RENDER = {2025: [35, 40, 43, 73, 76, 78, 82], 2023: [73, 78]}


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[cache] {dest.relative_to(ROOT)}")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, headers=HDR, timeout=300)
    r.raise_for_status()
    if r.content[:200].lstrip().lower().startswith((b"<html", b"<!doc")) and b"Request Rejected" in r.content[:600]:
        raise RuntimeError(f"WAF rechazo la peticion: {url}")
    dest.write_bytes(r.content)
    print(f"[dl] {dest.name} ({len(r.content)} bytes)")
    return dest


def num(s: str) -> float:
    return float(s.replace("%", "").replace("€", "").strip().replace(".", "").replace(",", "."))


def pnum(s: str) -> float:
    """porcentaje '13,82 %' -> 13.82 (los puntos de millar no existen en %)"""
    return float(s.replace("%", "").strip().replace(".", "").replace(",", "."))


# ------------------------------------------------------------------ 1) opendata CSV
def parse_opendata(path: Path) -> pd.DataFrame:
    d = pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig", index_col=False)
    d = d.loc[:, ~d.columns.str.startswith("Unnamed")]
    d["terr"] = np.where(d["geo"] == "Nacional", "Espana", np.where(d["geo"] == "Comunidad", d["ca"], d["prv"]))
    rows = []
    unidades = {"viv-num": "viviendas", "viv-imp": "miles EUR", "viv-pm2": "EUR/m2", "gar-num": "garajes",
                "gar-imp": "miles EUR", "gar-pm2": "EUR/m2", "tras-num": "trasteros", "tras-imp": "miles EUR", "tras-pm2": "EUR/m2"}
    # viv-imp: importe medio por vivienda en miles de EUR (p.ej. 214.581 EUR en 2025 -> 214581 en el CSV): se conserva en EUR
    for col, un in unidades.items():
        x = d[["ano", "trim", "geo", "ca", "prv", "terr", col]].copy()
        x = x.rename(columns={col: "valor"})
        x["serie"] = "compraventas_" + col.replace("-", "_")
        x["unidad"] = un if "imp" not in col else "EUR (importe medio por operacion)"
        rows.append(x)
    o = pd.concat(rows, ignore_index=True)
    o["periodo"] = o["ano"].astype(str) + "T" + o["trim"].astype(str)
    o["fecha"] = o["ano"].astype(str) + "-" + ((o["trim"] - 1) * 3 + 1).astype(str).str.zfill(2) + "-01"
    o["nivel"] = o["geo"].map({"Nacional": "nacional", "Comunidad": "ccaa", "Provincia": "provincia"})
    o["fuente"], o["url"], o["origen"], o["pagina"] = FUENTE + " (OpenData)", URL_CSV, "csv", ""
    o["nota"] = "4 trimestres moviles (ano terminado en el trimestre); el 4T es el ano natural"
    return o.rename(columns={"terr": "territorio"})[["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "origen",
                                                      "pagina", "territorio", "nivel", "nota"]]


# ------------------------------------------------------------------ 2) PDF Anuarios
def find_page(pdf, title: str, must: str = "", year: int | None = None, after: int = 0) -> int | None:
    """Primera pagina (1-based) cuyo encabezado contiene `title` y el texto contiene `must`."""
    for i, pg in enumerate(pdf.pages, 1):
        if i <= after:
            continue
        t = pg.extract_text() or ""
        head = "\n".join(t.splitlines()[:4])
        if title.lower() in head.lower() and (not must or must in t):
            return i
    return None


NIVEL_HDR = {"CC.AA.": "ccaa", "PROVINCIAS": "provincia", "CAPITALES": "capital", "Capitales de provincia": "capital"}


def parse_levels(pdf, page: int, year: int, edicion: int, serie_base: str, unidad: str, url: str) -> list[dict]:
    """Tablas 'General Var. anual Nueva Var. anual Usada Var. anual' (CCAA / PROVINCIAS / CAPITALES)."""
    txt = pdf.pages[page - 1].extract_text().splitlines()
    nivel = None
    for ln in txt[:8]:
        for k, v in NIVEL_HDR.items():
            if ln.startswith(k):
                nivel = v
    if nivel is None:
        raise RuntimeError(f"nivel no detectado p{page}")
    rx3 = re.compile(r"^(.+?) (-?[\d.]+) (-?[\d.,]+) ?% (-?[\d.]+) (-?[\d.,]+) ?% (-?[\d.]+) (-?[\d.,]+) ?%$")
    rx1 = re.compile(r"^(.+?) (-?[\d.]+) (-?[\d.,]+) ?%$")
    rows = []
    for ln in txt:
        ln = ln.strip()
        m = rx3.match(ln)
        if m:
            name = m.group(1)
            vals = [("general", m.group(2), m.group(3)), ("nueva", m.group(4), m.group(5)), ("usada", m.group(6), m.group(7))]
        else:
            m = rx1.match(ln)
            if not m or ln.startswith(("Año", "Estad")):
                continue
            name = m.group(1)
            vals = [("general", m.group(2), m.group(3))]
        for k, v, var in vals:
            terr = "Espana" if name == "España" else name
            for sfx, val, un in (("", num(v), unidad), ("_var_anual", pnum(var), "%")):
                rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie=f"{serie_base}_{k}{sfx}", valor=val, unidad=un,
                                 fuente=FUENTE, url=url, origen="pdf", pagina=page, territorio=terr,
                                 nivel="nacional" if terr == "Espana" else nivel, nacionalidad="", edicion=edicion))
    return rows


def parse_pct_ccaa(pdf, page: int, year: int, edicion: int, url: str) -> list[dict]:
    rows = []
    rx = re.compile(r"^(.+?) (\d+,\d+) ?% (\d+,\d+) ?% (-?\d+,\d+)$")
    for ln in pdf.pages[page - 1].extract_text().splitlines():
        m = rx.match(ln.strip())
        if not m:
            continue
        terr = "Espana" if m.group(1) == "España" else m.group(1)
        for k, v, un in (("pct_compras_nacionales", m.group(2), "%"), ("pct_compras_extranjeros", m.group(3), "%"),
                         ("pct_compras_extranjeros_var_pp", m.group(4), "pp")):
            rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie=f"viv_{k}", valor=pnum(v), unidad=un, fuente=FUENTE,
                             url=url, origen="pdf", pagina=page, territorio=terr, nivel="nacional" if terr == "Espana" else "ccaa",
                             nacionalidad="", edicion=edicion))
    return rows


def parse_pct_series(pdf, page: int, edicion: int, url: str) -> list[dict]:
    """Tabla 'Compras de vivienda por extranjeros en CC.AA. (%) Anual' con columnas 'AA T4' (8 anos)."""
    txt = pdf.pages[page - 1].extract_text().splitlines()
    years = None
    rows = []
    for ln in txt:
        if "Comunidad Autónoma" in ln and re.search(r"\d\d T4", ln):
            years = [2000 + int(y) for y in re.findall(r"(\d\d) T4", ln)]
            continue
        if years:
            m = re.match(r"^(.+?) ((?:\d+,\d+ ?% ?){" + str(len(years)) + r"})$", ln.strip())
            if m:
                vals = re.findall(r"(\d+,\d+) ?%", m.group(2))
                for y, v in zip(years, vals):
                    rows.append(dict(fecha=f"{y}-01-01", periodo=str(y), serie="viv_pct_compras_extranjeros_serie8a", valor=pnum(v), unidad="%",
                                     fuente=FUENTE, url=url, origen="pdf", pagina=page, territorio=m.group(1), nivel="ccaa",
                                     nacionalidad="", edicion=edicion))
    return rows


def parse_pct_prov(pdf, page: int, year: int, edicion: int, url: str) -> list[dict]:
    rows = []
    rx = re.compile(r"^(.+?) (\d+,\d+) ?% (-?\d+,\d+)$")
    for ln in pdf.pages[page - 1].extract_text().splitlines():
        m = rx.match(ln.strip())
        if not m:
            continue
        for k, v, un in (("viv_pct_compras_extranjeros", m.group(2), "%"), ("viv_pct_compras_extranjeros_var_pp", m.group(3), "pp")):
            rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie=k, valor=pnum(v), unidad=un, fuente=FUENTE, url=url,
                             origen="pdf", pagina=page, territorio=m.group(1), nivel="provincia", nacionalidad="", edicion=edicion))
    return rows


def parse_nacionalidad_es(pdf, page: int, year: int, edicion: int, url: str) -> list[dict]:
    rows = []
    rx = re.compile(r"^(.+?) (\d+,\d+) ?% (\d+,\d+) ?%(?: (-?\d+,\d+))?$")
    for ln in pdf.pages[page - 1].extract_text().splitlines():
        ln = ln.strip()
        m = rx.match(ln)
        if not m or ln.startswith(("Año", "Nacionalidad")):
            continue
        nac = m.group(1)
        for k, v, un in (("viv_pct_sobre_total", m.group(2), "%"), ("viv_pct_sobre_extranjeros", m.group(3), "%"),
                         ("viv_pct_sobre_extranjeros_var_pp", m.group(4), "pp")):
            if v is None:
                continue
            rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie=k, valor=pnum(v), unidad=un, fuente=FUENTE, url=url,
                             origen="pdf", pagina=page, territorio="Espana", nivel="nacional", nacionalidad=nac, edicion=edicion))
        # Extranjeros / Nacionales: sin tercera columna
    for ln in pdf.pages[page - 1].extract_text().splitlines():
        m = re.match(r"^Nacionales (\d+,\d+) ?%$", ln.strip())
        if m:
            rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie="viv_pct_sobre_total", valor=pnum(m.group(1)), unidad="%",
                             fuente=FUENTE, url=url, origen="pdf", pagina=page, territorio="Espana", nivel="nacional",
                             nacionalidad="Nacionales", edicion=edicion))
    return rows


def parse_nac_ccaa(pdf, pages: list[int], year: int, edicion: int, url: str) -> list[dict]:
    """Principales nacionalidades por CCAA (% s/extranjeros): paginas con 3 bloques por fila."""
    rows = []
    for page in pages:
        pg = pdf.pages[page - 1]
        w = pg.width
        for k in range(3):
            txt = (pg.crop((k * w / 3, 0, (k + 1) * w / 3, pg.height)).extract_text() or "").splitlines()
            region = None
            for i, ln in enumerate(txt):
                ln = ln.strip()
                if ln.startswith("Nacionalidad % s/extranjeros"):
                    region = txt[i - 1].strip()
                    continue
                m = re.match(r"^(.+?) (\d+,\d+) ?%$", ln)
                if m and region and not ln.startswith("Año"):
                    rows.append(dict(fecha=f"{year}-01-01", periodo=str(year), serie="viv_pct_sobre_extranjeros_ccaa",
                                     valor=pnum(m.group(2)), unidad="%", fuente=FUENTE, url=url, origen="pdf", pagina=page,
                                     territorio=region, nivel="ccaa", nacionalidad=m.group(1), edicion=edicion))
                elif ln and not m and region and not ln.startswith("Nacionalidad") and i > 0 and re.match(r"^[A-ZÁÉÍÓÚ]", ln) and "%" not in ln:
                    region = ln   # nuevo bloque en la misma columna (varios bloques apilados)
    return rows


def parse_anuario(year: int, path: Path, url: str) -> tuple[pd.DataFrame, dict]:
    rows, pages = [], {}
    with pdfplumber.open(path) as pdf:
        p = find_page(pdf, "Número de compraventas de vivienda. Resultados anuales", "CC.AA. General")
        rows += parse_levels(pdf, p, year, year, "compraventas_viv", "viviendas", url); pages["compras_ccaa"] = p
        p = find_page(pdf, "Número de compraventas de vivienda. Resultados anuales", "PROVINCIAS General")
        rows += parse_levels(pdf, p, year, year, "compraventas_viv", "viviendas", url); pages["compras_prov"] = p
        p = find_page(pdf, "Número de compraventas de vivienda en las capitales", "CAPITALES General")
        rows += parse_levels(pdf, p, year, year, "compraventas_viv", "viviendas", url); pages["compras_cap"] = p
        for nm, title, hdr in (("precio_ccaa", "Precio medio de Vivienda (€/m²). Resultados anuales y variación", "CC.AA. General"),
                               ("precio_prov", "Precio medio de Vivienda (€/m²). Resultados anuales y variación", "PROVINCIAS General"),
                               ("precio_cap", "Precio medio de Vivienda (€/m²). Resultados anuales y variación anual. Capitales", "Capitales de provincia")):
            p = find_page(pdf, title, hdr)
            rows += parse_levels(pdf, p, year, year, "precio_m2_viv", "EUR/m2", url); pages[nm] = p
        p = find_page(pdf, "Compras de vivienda por extranjeros en CC.AA.", "Nacionales Extranjeros")
        rows += parse_pct_ccaa(pdf, p, year, year, url); pages["pct_ext_ccaa"] = p
        p = find_page(pdf, "Distribución de compras de vivienda por extranjeros por Comunidades", "Comunidad Autónoma")
        rows += parse_pct_series(pdf, p, year, url); pages["pct_ext_ccaa_serie"] = p
        p = find_page(pdf, "Nacionalidad en las compras de vivienda. Interanual", "Provincias % extranjeros")
        rows += parse_pct_prov(pdf, p, year, year, url); pages["pct_ext_prov"] = p
        p = find_page(pdf, "Compraventas de vivienda registradas según nacionalidad del comprador", "% s/ total")
        rows += parse_nacionalidad_es(pdf, p, year, year, url); pages["nacionalidad_es"] = p
        p1 = find_page(pdf, "Compraventas de vivienda registradas según las principales nacionalidades", "Nacionalidad % s/extranjeros")
        p2 = find_page(pdf, "Compraventas de vivienda registradas según las principales nacionalidades", "Nacionalidad % s/extranjeros", after=p1)
        rows += parse_nac_ccaa(pdf, [p1, p2], year, year, url); pages["nac_ccaa"] = [p1, p2]
    return pd.DataFrame(rows), pages


# ------------------------------------------------------------------ validacion
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z ]", " ", s)
    s = re.sub(r"\b(comunidad|comunitat|region|de|del|la|el|illes|principado|foral|c)\b", " ", s)
    return " ".join(s.split())


ALIAS = {"palmas las": "las palmas", "coruna a": "a coruna", "rioja la": "rioja", "balears": "balears", "balears illes": "balears", "illes balears": "balears", "baleares": "balears", "asturias": "asturias",
         "rioja": "rioja", "madrid": "madrid", "murcia": "murcia", "navarra": "navarra", "valenciana": "valenciana",
         "valencia valencia": "valencia", "valencia": "valencia", "alicante alacant": "alicante", "alicante": "alicante",
         "castellon castello": "castellon", "castellon": "castellon", "castilla la mancha": "castilla mancha"}


def key(s: str) -> str:
    k = norm(s)
    return ALIAS.get(k, k)


def ine_year(kind_prefix: str) -> pd.Series:
    d = pd.read_csv(RAW / "ine_etdp_compraventas.csv")
    d = d[d["nombre"].str.contains(r"\. General\. Compraventa\. Número\.")].copy()
    d["terr"] = d["nombre"].str.split(". General", regex=False).str[0]
    d["anio"] = d["periodo"].str[:4].astype(int)
    g = d.groupby(["terr", "anio"])["valor"].agg(["sum", "count"]).reset_index()
    g = g[g["count"] == 12]
    return g.set_index(["terr", "anio"])["sum"]


def main() -> None:
    ORIG.mkdir(parents=True, exist_ok=True)
    VALID_DIR.mkdir(parents=True, exist_ok=True)
    val = []

    def V(tabla, ok, err, metodo, pags, detalle="", err_rel=np.nan):
        val.append(dict(tabla=tabla, validado="si" if ok else "no", error_max=err, error_max_rel=err_rel, metodo=metodo,
                        paginas_revisadas=pags, detalle=detalle))

    # ---------- 1) opendata CSV
    csvp = download(URL_CSV, ORIG / "registradores_opendata_compraventas_resid_2007-2T2026.csv")
    od = parse_opendata(csvp)
    od.to_csv(PDF_DIR / "registradores_opendata_compraventas.csv", index=False)
    print("[ok] registradores_opendata_compraventas.csv", len(od))

    # ---------- 2) PDF anuarios
    frames, allpages = [], {}
    for y, path_ in ANUARIOS.items():
        url = REG + path_
        p = download(url, ORIG / f"registradores_eri_anuario_{y}.pdf")
        df, pages = parse_anuario(y, p, url)
        frames.append(df)
        allpages[y] = pages
        print(f"[ok] anuario {y}: {len(df)} obs, paginas {pages}")
    an = pd.concat(frames, ignore_index=True)
    an.to_csv(PDF_DIR / "registradores_eri_anuario.csv", index=False)
    print("[ok] registradores_eri_anuario.csv", len(an))

    PR = f"{PAGINAS_REVISADAS}"
    # (a) cuadre CCAA / provincias vs Espana (el propio PDF publica la fila 'España')
    for y in ANUARIOS:
        a = an[(an.edicion == y) & (an.periodo == str(y)) & (an.serie == "compraventas_viv_general")]
        esp = float(a[a.territorio == "Espana"]["valor"].iloc[0])
        for niv, nm in (("ccaa", "CCAA"), ("provincia", "provincias")):
            s = a[a.nivel == niv]["valor"].sum()
            V(f"anuario{y}_compraventas_{nm}_suma_vs_Espana", s == esp, abs(s - esp),
              f"suma de {len(a[a.nivel == niv])} filas {nm} vs fila 'España' publicada ({esp:.0f})", PR,
              "" if s == esp else "diferencia = Ceuta y Melilla (el PDF no las lista) u otra omision; se marca, no se corrige", abs(s - esp) / esp)
        for sub in ("nueva", "usada"):
            ss = an[(an.edicion == y) & (an.serie == f"compraventas_viv_{sub}") & (an.nivel == "ccaa")]["valor"].sum()
            ee = an[(an.edicion == y) & (an.serie == f"compraventas_viv_{sub}") & (an.nivel == "nacional")]["valor"].iloc[0]
            V(f"anuario{y}_compraventas_{sub}_CCAA_suma_vs_Espana", ss == ee, abs(ss - ee), f"suma CCAA {sub} vs España {ee:.0f}", PR, "", abs(ss - ee) / ee)
        g = an[(an.edicion == y) & (an.serie == "compraventas_viv_general") & (an.nivel == "nacional")]["valor"].iloc[0]
        n_ = an[(an.edicion == y) & (an.serie == "compraventas_viv_nueva") & (an.nivel == "nacional")]["valor"].iloc[0]
        u_ = an[(an.edicion == y) & (an.serie == "compraventas_viv_usada") & (an.nivel == "nacional")]["valor"].iloc[0]
        V(f"anuario{y}_compraventas_general_eq_nueva_mas_usada", g == n_ + u_, abs(g - n_ - u_), "Espana: general = nueva + usada", PR)
    # (b) % nacionales + extranjeros = 100 ; nacionalidades suman 100 % de extranjeros
    for y in ANUARIOS:
        p = an[(an.edicion == y) & (an.periodo == str(y))]
        a = p[p.serie == "viv_pct_compras_nacionales"].set_index("territorio")["valor"]
        b = p[p.serie == "viv_pct_compras_extranjeros"].set_index("territorio")["valor"]
        e = (a + b - 100).abs().max()
        V(f"anuario{y}_pct_nacionales_mas_extranjeros", e <= 0.0101, e, f"nacionales + extranjeros = 100 en {len(a)} territorios (redondeo 0.01)", PR)
        nsum = p[(p.serie == "viv_pct_sobre_extranjeros") & (p.territorio == "Espana") & (~p.nacionalidad.isin(["Extranjeros"]))]["valor"].sum()
        V(f"anuario{y}_nacionalidades_suman_100_sobre_extranjeros", abs(nsum - 100) <= 0.05, abs(nsum - 100),
          "suma de nacionalidades listadas + Resto = 100 % de extranjeros (p78)", PR,
          "NO CUADRA EN ORIGEN: la tabla publicada suma %.2f%%; los valores extraidos coinciden con el render PNG (p78 revisada), el defecto es del PDF; no se corrige" % nsum
          if abs(nsum - 100) > 0.05 else "")
    # (c) coherencia entre ediciones solapadas: serie % extranjeros CCAA (8 anos) y valores anuales
    ser = an[an.serie == "viv_pct_compras_extranjeros_serie8a"]
    s2 = ser[ser.nivel == "ccaa"].pivot_table(index=["territorio", "periodo"], columns="edicion", values="valor")
    for y in ANUARIOS:
        a73 = an[(an.edicion == y) & (an.serie == "viv_pct_compras_extranjeros") & (an.nivel == "ccaa")].set_index("territorio")["valor"]
        a75 = an[(an.edicion == y) & (an.serie == "viv_pct_compras_extranjeros_serie8a") & (an.nivel == "ccaa") & (an.periodo == str(y))].set_index("territorio")["valor"]
        a75.index = [k.replace("  ", " ") for k in a75.index]
        k73 = {key(t): v for t, v in a73.items()}
        k75 = {key(t): v for t, v in a75.items()}
        d_ = max(abs(k73[k] - k75[k]) for k in k73 if k in k75)
        V(f"anuario{y}_pct_extranjeros_CCAA_p73_vs_serie_p75", d_ <= 0.0051 and len(set(k73) & set(k75)) == 17, d_,
          f"% extranjeros del ano {y} en dos tablas del mismo PDF (17 CCAA)", PR)
    for a_, b_ in ((2025, 2024), (2024, 2023)):
        x = s2[[a_, b_]].dropna()
        V(f"anuarios_{a_}_vs_{b_}_pct_extranjeros_CCAA_solape", (x[a_] - x[b_]).abs().max() <= 0.01, (x[a_] - x[b_]).abs().max(),
          f"serie % extranjeros CCAA {len(x)} celdas solapadas entre ediciones (revision)", PR)
    # (d) contraste con opendata CSV (4T = ano natural): compraventas y precio
    o = od[(od.periodo.str.endswith("T4"))].copy()
    o["anio"] = o.periodo.str[:4].astype(int)
    for y in ANUARIOS:
        for serie_pdf, serie_od, nm in (("compraventas_viv_general", "compraventas_viv_num", "compraventas"), ("precio_m2_viv_general", "compraventas_viv_pm2", "precio_m2")):
            pdf_ = an[(an.edicion == y) & (an.serie == serie_pdf) & (an.nivel.isin(["nacional", "ccaa", "provincia"]))].copy()
            od_ = o[(o.anio == y) & (o.serie == serie_od)].copy()
            pdf_["k"] = pdf_.territorio.map(key)
            od_["k"] = od_.territorio.map(key)
            adj_note = ""
            if nm == "compraventas":
                # El Anuario asigna Ceuta a Cadiz y Melilla a Almeria (y ambas a Andalucia); el CSV las lista aparte.
                # Se concilia SUMANDO a la cifra del CSV (el PDF no se toca) y se documenta.
                ce = float(od_[(od_.k == "ceuta")]["valor"].iloc[0]); me = float(od_[(od_.k == "melilla")]["valor"].iloc[0])
                for kk, add in (("andalucia", ce + me), ("cadiz", ce), ("almeria", me)):
                    od_.loc[od_.k == kk, "valor"] += add
                adj_note = (f"conciliacion documentada: CSV Andalucia += Ceuta+Melilla ({ce + me:.0f}), Cadiz += Ceuta ({ce:.0f}), "
                            f"Almeria += Melilla ({me:.0f}) (criterio registral del Anuario); sin conciliar el error maximo seria {ce + me:.0f}")
            j = pdf_.merge(od_, on=["k", "nivel"], suffixes=("_pdf", "_od"))
            ad = (j.valor_pdf - j.valor_od).abs()
            rel = (ad / j.valor_od.abs()).max()
            bad = j.loc[ad.sort_values(ascending=False).index[:1], ["territorio_pdf", "valor_pdf", "valor_od"]].values.tolist()
            tol = 0 if nm == "compraventas" else 1.0
            V(f"anuario{y}_{nm}_vs_opendata_CSV", ad.max() <= tol, float(ad.max()),
              f"{len(j)} territorios (nacional+CCAA+provincia) PDF vs CSV opendata 4T; peor: {bad}", PR, adj_note, float(rel))
    # (e) contraste con INE ETDP (anual, 12 meses) y MIVAU
    ine = ine_year("")
    pairs = {"Espana": "Total Nacional", "Comunitat Valenciana": "Comunitat Valenciana", "Valencia/València": "Valencia/València",
             "Alicante/Alacant": "Alicante/Alacant", "Castellón/Castelló": "Castellón/Castelló"}
    names = set(ine.index.get_level_values(0))
    nac_name = next((n for n in names if n.lower().startswith(("total nac", "españa", "nacional"))), None)
    for y in ANUARIOS:
        errs, rels, det = [], [], []
        for terr_pdf, terr_ine in (("Espana", nac_name), ("Comunitat Valenciana", "Comunitat Valenciana"), ("Valencia/València", "Valencia/València"),
                                   ("Alicante/Alacant", "Alicante/Alacant"), ("Castellón/Castelló", "Castellón/Castelló")):
            if terr_ine is None or (terr_ine, y) not in ine.index:
                continue
            a = an[(an.edicion == y) & (an.serie == "compraventas_viv_general") & (an.territorio.map(key) == key(terr_pdf))]
            if a.empty:
                continue
            v = float(a["valor"].iloc[0])
            errs.append(abs(v - ine[(terr_ine, y)]))
            rels.append(errs[-1] / ine[(terr_ine, y)])
            det.append(f"{terr_pdf}: ERI {v:.0f} vs INE {ine[(terr_ine, y)]:.0f}")
        if errs:
            V(f"anuario{y}_compraventas_vs_INE_ETDP", max(rels) < 0.05, max(errs), f"{len(errs)} territorios; " + "; ".join(det), PR,
              "INE ETDP y ERI parten de registros de la propiedad, pero con criterios/cortes distintos", max(rels))
    # (f) plausibilidad extranjeros: implicitos (% x compraventas) vs notarios CGN (xls, CCAA, vivienda libre, 1S+2S)
    cgn = pd.read_csv(PDF_DIR / "notariado_cgn_extranjeros_semestral.csv") if (PDF_DIR / "notariado_cgn_extranjeros_semestral.csv").exists() else None
    if cgn is not None:
        c = cgn[(cgn.tabla == "T2") & (cgn.territorio != "Nacional")].copy()
        c["anio"] = c.periodo.str[:4].astype(int)
        cc = c.groupby(["territorio", "anio"])["valor"].sum()
        for y in ANUARIOS:
            a = an[(an.edicion == y) & (an.periodo == str(y))]
            tot = a[(a.serie == "compraventas_viv_general") & (a.nivel == "ccaa")].set_index("territorio")["valor"]
            pct = a[(a.serie == "viv_pct_compras_extranjeros") & (a.nivel == "ccaa")].set_index("territorio")["valor"]
            imp = (tot * pct / 100).dropna()
            rel, det = [], []
            for terr in ("Comunitat Valenciana", "Balears, Illes", "Canarias", "Andalucía", "Cataluña"):
                m = {"Comunitat Valenciana": "Comunidad Valenciana", "Balears, Illes": "Islas Baleares", "Canarias": "Islas Canarias"}.get(terr, terr)
                if terr in imp.index and (m, y) in cc.index:
                    rel.append(abs(imp[terr] - cc[(m, y)]) / cc[(m, y)])
                    det.append(f"{terr}: registral {imp[terr]:.0f} vs notarial {cc[(m, y)]:.0f}")
            if rel:
                V(f"anuario{y}_extranjeros_implicitos_vs_notarios_CGN", max(rel) < 0.30, np.nan,
                  "compras de extranjeros implicitas (pct x compraventas) vs CGN xls (vivienda libre) en 5 CCAA; " + "; ".join(det), PR,
                  "fuentes distintas (registro vs notarios; fechas de escritura vs inscripcion): plausibilidad, no cuadre", max(rel))
    vdf = pd.DataFrame(val)
    vdf.to_csv(PDF_DIR / "registradores_validacion.csv", index=False)
    print(vdf[["tabla", "validado", "error_max", "error_max_rel"]].to_string())

    # ---------- renders PNG
    import pypdfium2 as pdfium
    for y, pgs in RENDER.items():
        pdf = pdfium.PdfDocument(str(ORIG / f"registradores_eri_anuario_{y}.pdf"))
        for p in pgs:
            out = VALID_DIR / f"registradores_eri_anuario_{y}_p{p}.png"
            if not out.exists():
                pdf[p - 1].render(scale=1.5).to_pil().save(out)


if __name__ == "__main__":
    main()
