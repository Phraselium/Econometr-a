"""V11-DATOS (3.ª pasada): extracción de tablas de los PDF del padrón de València (Oficina d'Estadística).

Herramienta: pdfplumber (texto por página) y, solo en las páginas cuyas fuentes no traen mapa Unicode (texto
«(cid:..)», padrón 2026), ocrmypdf/tesseract (spa) sobre esas páginas; las filas OCR se validan con sus sumas.
Los títulos solo aparecen en la primera página de cada tabla: el analizador arrastra la tabla activa entre páginas.
Filas reconocidas: ciudad («València …»), distrito («D. Nombre …»), barrio («D.B. Nombre …» desde 2016, con o sin
«D. Distrito» delante y con o sin espacios; o «B. Nombre …» bajo la cabecera de distrito hasta 2015) y componente
(línea sin código con números, p. ej. «Altes per naixement …» en las tablas de altas y bajas).
Códigos: distrito = 46250 + DD; barrio del Ajuntament = 46250 + DD + BB (el código de data/base/geo). La asignación es por
el CÓDIGO (D, B) impreso; el nombre solo sirve de control (equivalencias_barrios.csv, versionada y revisada).
Salidas en data/raw/v11/vlc_padron/:
- tablas_crudas.csv.gz: todas las filas reconocidas (año, fichero, página, tabla, título, subtabla, componente,
  cabecera, nivel, códigos, valores) para auditoría y para tablas aún no normalizadas;
- vlc_padron_barrio.csv.gz y vlc_padron_distrito.csv.gz (largo: anio, codigo, variable, desagregacion, valor, control);
- vlc_altas_bajas_distrito.csv.gz (anio, cod_distrito, componente, valor, informe);
- equivalencias_barrios.csv; validacion.csv (ciudad frente al padrón del INE; barrios frente al censo anual).
"""
from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAIZ, RAW11, registrar  # noqa: E402

DIR = RAW11 / "vlc_padron"
ORIG = DIR / "original"
CACHE, OCR = ORIG / "_texto", ORIG / "_ocr"
LIC = "Ajuntament de València, Oficina d'Estadística: reutilización con cita de la fuente"
URL = "https://www.valencia.es/estadistica/Padron/"
NUM = re.compile(r"^(-|–|\.\.|-?\d{1,3}(\.\d{3})+(,\d+)?|-?\d+(,\d+)?)$")
TITULO = re.compile(r"^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.?\s*(\S.*)$")
CLAVE = re.compile(r"(pobla|altes|altas|baixes|bajas|nombre|n[uú]mero|evoluc|moviment|movimiento|canvis|cambios|modificac|"
                   r"nacionalit|nacionalid|edat|edad|estrang|extranj|fulls|hojas)", re.I)
BARRIO = re.compile(r"^(?:(\d{1,2})\.\s*(\D+?)\s+)?(\d{1,2})\.(\d{1,2})\.?\s*(\D.*)$")
DISTRITO = re.compile(r"^(\d{1,2})\.\s*(\D.*)$")
SUB = re.compile(r"^(total|homes|dones|hombres|mujeres)$", re.I)
SUBNORM = {"total": "Total", "homes": "Hombres", "hombres": "Hombres", "dones": "Mujeres", "mujeres": "Mujeres"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


def numero(t: str) -> float:
    if t in ("-", "–", ".."):
        return 0.0
    return float(t.replace(".", "").replace(",", "."))


def texto(pdf: Path) -> list[str]:
    """Texto por página (caché en original/_texto). Páginas «(cid:..)»: se sustituyen por el texto del OCR de esas páginas
    (original/_ocr/<fichero>_ocr.pdf; se genera con ocrmypdf si falta y está instalado)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / f"{pdf.stem}.json"
    if c.exists():
        pags = json.loads(c.read_text(encoding="utf-8"))
    else:
        import pdfplumber
        with pdfplumber.open(pdf) as d:
            pags = [(p.extract_text() or "") for p in d.pages]
        c.write_text(json.dumps(pags, ensure_ascii=False), encoding="utf-8")
    malas = [i for i, t in enumerate(pags) if "(cid:" in t]
    if not malas:
        return pags
    o = OCR / f"{pdf.stem}_ocr.pdf"
    if not o.exists() and shutil.which("ocrmypdf"):
        OCR.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ocrmypdf", "-q", "--force-ocr", "-l", "spa", "--pages", ",".join(str(i + 1) for i in malas), "-j", "4",
                        str(pdf), str(o)], check=False)
    if o.exists():
        co = CACHE / f"{pdf.stem}_ocr.json"
        if not co.exists():
            import pdfplumber
            with pdfplumber.open(o) as d:
                co.write_text(json.dumps({i: (d.pages[i].extract_text() or "") for i in malas}, ensure_ascii=False), encoding="utf-8")
        ocr = {int(k): v for k, v in json.loads(co.read_text(encoding="utf-8")).items()}
        pags = [ocr.get(i, t) if i in malas else t for i, t in enumerate(pags)]
    return pags


def separar(linea: str) -> tuple[str, list[float]]:
    tk = linea.split()
    k = len(tk)
    while k > 0 and NUM.match(tk[k - 1]):
        k -= 1
    return " ".join(tk[:k]), [numero(t) for t in tk[k:]]


def es_titulo(linea: str) -> re.Match | None:
    m = TITULO.match(linea)
    if not m or re.match(r"^\d{1,2}\.\d{1,2}\.", linea) and BARRIO.match(separar(linea)[0]) and separar(linea)[1]:
        return None
    etq, nums = separar(linea)
    return m if len(nums) <= 1 and CLAVE.search(m.group(2)) else None


def subtabla_de(titulo: str) -> str:
    m = re.search(r"[.\s](total|homes|dones|hombres|mujeres)\.?\s*$", titulo, re.I)
    return SUBNORM[m.group(1).lower()] if m else ""


def analizar(pags: list[str], anio: int, fichero: str) -> list[dict]:
    filas, tabla, titulo, sub, cab, dist, comp, ocr = [], None, "", "", [], None, "", False
    for ip, t in enumerate(pags):
        ocr = "(cid:" not in t and "Valéncia" in t   # marca aproximada de texto OCR (acento cambiado)
        for linea in t.split("\n"):
            linea = re.sub(r"[|¦]", " ", linea).strip()
            linea = re.sub(r"\s{2,}", " ", linea)
            if not linea or linea.startswith(("Oficina d", "Fuente", "Font:", "Fonte")):
                continue
            m = es_titulo(linea)
            if m:
                if m.group(1) != tabla or subtabla_de(m.group(2)) not in ("", sub):
                    tabla, titulo, cab, dist, comp = m.group(1), m.group(2), [], None, ""
                    sub = subtabla_de(m.group(2))
                continue
            if tabla is None:
                continue
            if SUB.match(linea):
                sub = SUBNORM[linea.lower()]
                dist = None
                continue
            etq, nums = separar(linea)
            if not etq and nums and all(1990 <= x <= 2030 and x == int(x) for x in nums):
                cab.append(" ".join(str(int(x)) for x in nums))   # fila de años de las tablas con años en columnas
                continue
            if not nums:
                md = DISTRITO.match(etq)
                if md and int(md.group(1)) <= 19:
                    dist = (int(md.group(1)), md.group(2))
                elif len(cab) < 6:
                    cab.append(linea)
                continue
            base = {"anio": anio, "fichero": fichero, "pagina": ip + 1, "tabla": tabla, "titulo": titulo, "subtabla": sub,
                    "componente": comp, "cabecera": " | ".join(cab), "valores": json.dumps(nums), "ocr": ocr}
            if norm(etq) in ("valencia", "valenciatotal", "total", "totalvalencia", "valenciavalencia"):
                filas.append({**base, "nivel": "ciudad", "d": None, "b": None, "nombre": etq})
                continue
            mb = BARRIO.match(etq)
            if mb:
                if mb.group(1):
                    dist = (int(mb.group(1)), mb.group(2))
                filas.append({**base, "nivel": "barrio", "d": int(mb.group(3)), "b": int(mb.group(4)), "nombre": mb.group(5)})
                continue
            md = DISTRITO.match(etq)
            if md and int(md.group(1)) <= 19:
                n, nom = int(md.group(1)), md.group(2)
                if nom.upper() == nom and len(norm(nom)) > 3:   # «D. NOMBRE» en mayúsculas con números: distrito y cabecera
                    dist = (n, nom)
                    filas.append({**base, "nivel": "distrito", "d": n, "b": None, "nombre": nom})
                elif dist is not None:
                    filas.append({**base, "nivel": "barrio", "d": dist[0], "b": n, "nombre": nom})
                else:
                    filas.append({**base, "nivel": "distrito", "d": n, "b": None, "nombre": nom})
                continue
            if not re.match(r"^\d", etq) and len(norm(etq)) > 3:
                comp, dist = etq, None   # componente (p. ej. «Altes per naixement»): las filas siguientes son sus distritos
                filas.append({**base, "componente": etq, "nivel": "ciudad_componente", "d": None, "b": None, "nombre": etq})
    return filas


def crudas() -> pd.DataFrame:
    filas = []
    for pdf in sorted(ORIG.glob("*.pdf")):
        tipo, anio = pdf.stem.rsplit("_", 1)
        filas += analizar(texto(pdf), int(anio), pdf.name)
    c = pd.DataFrame(filas)
    c["n_valores"] = c.valores.map(lambda v: len(json.loads(v)))
    return c


# ------------------------------------------------------------------------------------------------ normalización
CONTINENTES = [("ue", r"\bue\b|uni[oó] europea|europea|resta ue|unió"), ("resto_europa", r"resta d.europa|resto de europa|europa no|no ue|euro.*no"),
               ("africa", r"[aà]frica"), ("america_norte", r"am[eè]rica del nord|am[eé]rica del norte|nord"),
               ("america_central", r"central"), ("america_sur", r"am[eè]rica del sud|am[eé]rica del sur|del sud|del sur"),
               ("asia", r"[aà]sia"), ("oceania_otros", r"oceania|apàtrid|apátrid|altres|otros")]


def _val(v: str) -> list[float]:
    return json.loads(v)


def reparar(pad: pd.DataFrame) -> pd.DataFrame:
    """1) Tablas repetidas en el mismo informe (2016-2017): se conserva la primera aparición de cada fila.
    2) Cabecera de distrito fusionada con la fila de su primer barrio («11. POBLATS MARÍTIMS 8.563 …», 2001): en una
    tabla por barrio, si falta el barrio D.1 y hay una fila de distrito D con números, esa fila es el barrio D.1."""
    pad = pad.drop_duplicates(["anio", "tabla", "subtabla", "componente", "nivel", "d", "b", "valores"]).copy()
    pad = pad.drop_duplicates(["anio", "tabla", "subtabla", "componente", "nivel", "d", "b"], keep="first").copy()
    es_tb = pad.titulo.str.contains("barri", case=False)
    tot_d = {(r.anio, r.d): json.loads(r.valores)[0] for r in pad[(pad.tabla == "1.2") & (pad.nivel == "distrito")].itertuples()}
    for (a, t, sb), g in pad[es_tb].groupby(["anio", "tabla", "subtabla"]):
        for i, r in g[g.nivel == "distrito"].iterrows():
            hij = g[(g.nivel == "barrio") & (g.d == r.d)].sort_values("b")
            if hij.empty:
                continue
            if (r.d, 1.0) not in set(zip(hij.d, hij.b)):
                pad.loc[i, ["nivel", "b", "nombre"]] = ["barrio", 1.0, f"{r.nombre} [cabecera fusionada con el barrio {int(r.d)}.1]"]
                continue
            # cabecera con los valores del barrio D.1 y el resto desplazado una fila (2001, Poblats Marítims): solo si la
            # suma de la cabecera y los barrios es el total del distrito (tabla 1.2) y la cabecera no es ese total
            s_tot = json.loads(r.valores)[0] + sum(json.loads(v)[0] for v in hij.valores)
            if t == "1.3" and tot_d.get((a, r.d)) == s_tot and json.loads(r.valores)[0] != tot_d.get((a, r.d)):
                pad.loc[i, ["nivel", "b", "nombre"]] = ["barrio", 1.0, f"{hij.nombre.iloc[0]} [valores desplazados una fila en el PDF; reparado]"]
                for j, rb in hij.iterrows():
                    nb = rb.b + 1
                    pad.loc[j, ["b", "nombre"]] = [nb, f"[barrio {int(r.d)}.{int(nb)}; valores desplazados en el PDF; reparado]"]
    return pad


def norm_barrio_distrito(c: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    pad = reparar(c[c.fichero.str.startswith("padron")])
    out = []

    def emit(x: pd.DataFrame, variable: str, cols: list[str], des: str = "sexo", control=None):
        for r in x.itertuples():
            v = _val(r.valores)
            if len(v) != len(cols):
                continue
            ctl = control(v) if control else True
            cod = (f"46250{int(r.d):02d}{int(r.b):02d}" if r.nivel == "barrio" else f"46250{int(r.d):02d}")
            for k, val in zip(cols, v):
                out.append({"anio": r.anio, "nivel": r.nivel, "codigo": cod, "variable": variable, "tabla": r.tabla,
                            "desagregacion": f"{des}={k}" + (f"|sexo={r.subtabla}" if des != "sexo" and r.subtabla else ""),
                            "valor": val, "control_suma": bool(ctl), "pagina": r.pagina, "ocr": r.ocr, "nombre_pdf": r.nombre})
    suma3 = lambda v: abs(v[0] - v[1] - v[2]) <= 1  # noqa: E731
    sumarest = lambda v: abs(v[0] - sum(v[1:])) <= max(1, 0.001 * v[0])  # noqa: E731
    # población por sexo (1.3 barrios, 1.2 distritos)
    emit(pad[(pad.tabla == "1.3") & (pad.nivel == "barrio")], "vlc_padron_pob", ["Total", "Hombres", "Mujeres"], control=suma3)
    emit(pad[(pad.tabla == "1.2") & (pad.nivel == "distrito")], "vlc_padron_pob", ["Total", "Hombres", "Mujeres"], control=suma3)
    # edad en tres grupos por barrio y distrito (Total / Hombres / Mujeres)
    seccion45 = pad.tabla.str.match(r"^[45]\.")   # 4.x por distrito, 5.x por barrio (6.x es por sección censal)
    t3 = pad[seccion45 & pad.titulo.str.contains(r"edat en (?:tres|3) grups|edad en (?:tres|3) grupos", case=False, regex=True)
             & ~pad.titulo.str.contains(r"estrang|extranj|col.lect|colect|secci", case=False, regex=True) & pad.nivel.isin(["barrio", "distrito"])]
    emit(t3, "vlc_padron_pob_edad", ["Total", "0-15", "16-64", "65+"], des="edad", control=sumarest)
    # extranjeros por continente de nacionalidad (barrio y distrito): columnas por la cabecera si se identifican
    tc = pad[seccion45 & pad.titulo.str.contains("continent", case=False) & pad.titulo.str.contains(r"nacionalit|nacionalid", case=False, regex=True)
             & pad.nivel.isin(["barrio", "distrito"])]
    for (anio, tabla, subt), g in tc.groupby(["anio", "tabla", "subtabla"]):
        n = int(g.n_valores.mode().iloc[0])
        nombres = COL_CONTINENTE.get(n) or continentes_de(norm_cab(g.cabecera.iloc[0]), n)
        emit(g, "vlc_padron_ext_continente", nombres, des="continente", control=sumarest)
    o = pd.DataFrame(out)
    # nivel según la sección del informe: barrios en 1.3 y 5.x; distritos en 1.2 y 4.x; y solo códigos de barrio
    # existentes en el geoportal (más el 11.6 de 2002, sin código vigente)
    validos = set(pd.read_parquet(RAIZ / "data/base/geo/barrios_valencia.parquet", columns=["cod_barrio"]).cod_barrio) | {"462501106"}
    ok_b = (o.nivel == "barrio") & o.tabla.str.match(r"^(1\.3|5\.)") & o.codigo.isin(validos)
    ok_d = (o.nivel == "distrito") & o.tabla.str.match(r"^(1\.2|4\.)")
    return o[ok_b].drop(columns="tabla"), o[ok_d].drop(columns="tabla")


# orden de columnas de las tablas «población extranjera según nacionalidad, por continentes» (comprobado en las cabeceras
# de 2001, 2011 y 2025): 10 columnas hasta la UE-15/25 (Oceanía y «altres situacions» separadas); 9 desde la UE-27
# («Oceania i altres»). «ue» = resto de la UE con la composición de cada año.
COL_CONTINENTE = {10: ["total_extranjeros", "ue", "resto_europa", "africa", "america_norte", "america_central", "america_sur", "asia", "oceania", "otros"],
                  9: ["total_extranjeros", "ue", "resto_europa", "africa", "america_norte", "america_central", "america_sur", "asia", "oceania_otros"]}


def norm_cab(c: str) -> str:
    return c.replace(" | ", " ")


def continentes_de(cab: str, n: int) -> list[str]:
    hall = []
    low = cab.lower()
    for nombre, pat in CONTINENTES:
        m = re.search(pat, low)
        if m:
            hall.append((m.start(), nombre))
    nombres = ["total_extranjeros"] + [x for _, x in sorted(hall)]
    if len(nombres) == n:
        return nombres
    return ["total_extranjeros"] + [f"col{k}" for k in range(1, n)]


def altas_bajas(c: pd.DataFrame) -> pd.DataFrame:
    """Tablas por distrito con años en columnas (informe de altas y bajas: movimiento natural, migratorio, cambios de
    domicilio). Para cada año se conserva el dato del informe más reciente."""
    ab = c[c.fichero.str.startswith("altas_bajas") & (c.nivel == "distrito") & (c.componente != "")]
    filas = []
    for r in ab.itertuples():
        anios = [int(x) for x in re.findall(r"\b(19\d{2}|20\d{2})\b", r.cabecera)]
        v = _val(r.valores)
        if not anios or len(anios) != len(v):
            continue
        for a, val in zip(anios, v):
            filas.append({"anio": a, "cod_distrito": f"46250{int(r.d):02d}", "tabla": r.tabla, "componente": r.componente, "valor": val,
                          "informe": r.anio, "pagina": r.pagina})
    f = pd.DataFrame(filas)
    if f.empty:
        return f
    f = f.sort_values("informe").drop_duplicates(["anio", "cod_distrito", "tabla", "componente"], keep="last")
    return f.sort_values(["componente", "cod_distrito", "anio"])


def paises(c: pd.DataFrame) -> pd.DataFrame:
    """Tabla «Distribució per districtes de les nacionalitats més freqüents» (2005-2018): para cada nacionalidad principal,
    total de la ciudad y los cuatro distritos con más peso (código de distrito leído del número «D.»; % de la nacionalidad).
    Las filas agregadas (Total, UE...) se marcan como agregado. Desde 2019 el PDF no trae esta tabla."""
    x = c[c.titulo.str.contains("districtes de les nacionalitats|distritos de las nacionalidades", case=False, na=False)]
    filas = []
    for r in x.itertuples():
        m = re.match(r"^(.+?)\s+(\d{1,3}(?:\.\d{3})*)\s+(\d{1,2}\..*)$", r.componente if isinstance(r.componente, str) else "")
        if not m:
            continue
        resto = m.group(3) + " " + " ".join(f"{v:.1f}".replace(".", ",") for v in _val(r.valores))
        top = re.findall(r"(\d{1,2})\.\s*\D+?\s+(\d{1,3},\d)", resto)
        nombre = m.group(1).strip()
        agregado = bool(re.match(r"^(total|ue\b|ue \(|resto|resta|rest |altres|otros|unió|unión|europa|àfrica|africa|àsia|asia|amèrica|america|oceania|oceanía|apàtrides)", nombre, re.I))
        f = {"anio": int(r.anio), "nacionalidad_pdf": nombre, "agregado": agregado, "poblacion_ciudad": numero(m.group(2)), "pagina": r.pagina}
        for k, (dd, pct) in enumerate(top[:4], 1):
            f[f"distrito_{k}"] = f"46250{int(dd):02d}"
            f[f"pct_{k}"] = numero(pct)
        filas.append(f)
    return pd.DataFrame(filas).drop_duplicates(["anio", "nacionalidad_pdf"]).sort_values(["anio", "poblacion_ciudad"], ascending=[True, False])


REVISADAS = {   # revisión manual de las equivalencias cuyo nombre no coincide (código del PDF = código del Ajuntament)
    "462501705": "mismo barrio 17.5: «Mauella» en la estadística municipal y «Rafalell-Vistabella» en el geoportal",
    "462501106": "barrio 11.6 «Les Moreres», solo en 2002 (después integrado en Natzaret): sin código vigente en el geoportal",
}


def equivalencias(b: pd.DataFrame) -> pd.DataFrame:
    nom = pd.read_parquet(RAIZ / "data/base/geo/barrios_valencia.parquet", columns=["cod_barrio", "nombre"]).set_index("cod_barrio").nombre
    e = b[b.variable == "vlc_padron_pob"].drop_duplicates(["anio", "codigo"])[["anio", "codigo", "nombre_pdf"]].rename(columns={"codigo": "cod_barrio"})
    e["nombre_ajuntament"] = e.cod_barrio.map(nom)
    e["similitud"] = [round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 3) if isinstance(b, str) else 0.0
                      for a, b in zip(e.nombre_pdf, e.nombre_ajuntament)]
    contiene = np.array([isinstance(b, str) and (norm(a) in norm(b) or norm(b) in norm(a)) for a, b in zip(e.nombre_pdf, e.nombre_ajuntament)], dtype=bool)
    e["coincide"] = (e.similitud >= 0.75).to_numpy() | contiene
    e["revision"] = e.cod_barrio.map(REVISADAS).fillna("")
    e.loc[e.nombre_pdf.str.contains("cabecera fusionada|desplazados"), "revision"] = "valores desplazados o cabecera fusionada en el PDF (reparado con el total del distrito)"
    e["aceptada"] = e.coincide | (e.revision != "")
    return e.sort_values(["anio", "cod_barrio"])


def validar(b: pd.DataFrame, d: pd.DataFrame, c: pd.DataFrame) -> pd.DataFrame:
    filas = []
    ciudad = c[c.fichero.str.startswith("padron") & (c.tabla == "1.3") & (c.nivel == "ciudad")].drop_duplicates("anio")
    ciudad = ciudad.set_index("anio").valores.map(lambda v: json.loads(v)[0])
    ine = pd.read_csv(RAIZ / "data/raw/ine_padron_valencia.csv", dtype={"periodo": str})
    ine = ine[ine.serie == "DPOP21796"].assign(anio=lambda x: x.periodo.str[:4].astype(int)).set_index("anio").valor
    pob = b[(b.variable == "vlc_padron_pob") & (b.desagregacion == "sexo=Total")]
    for a in sorted(pob.anio.unique()):
        sb = pob[pob.anio == a].valor.sum()
        f = {"anio": int(a), "barrios": int(pob[pob.anio == a].codigo.nunique()), "suma_barrios": sb, "total_ciudad_pdf": ciudad.get(a, np.nan),
             "padron_ine": ine.get(a, np.nan),
             "control_suma_barrios_ok": bool(pob[pob.anio == a].control_suma.all())}
        f["dif_ciudad_ine_pct"] = round(100 * (f["total_ciudad_pdf"] / f["padron_ine"] - 1), 3) if f["padron_ine"] == f["padron_ine"] else np.nan
        f["dif_barrios_ciudad"] = sb - f["total_ciudad_pdf"]
        filas.append(f)
    v = pd.DataFrame(filas)
    # barrios frente al censo anual por sección (2021-2025), en los barrios cuyo distrito no cambió de seccionado (V12-B1)
    p = RAIZ / "output/v12/b1/valencia_barrio_variacion_2021_2025.csv"
    q = RAIZ / "output/v12/b1/valencia_barrio_nacionalidad.csv"
    if p.exists() and q.exists():
        comp = set(pd.read_csv(p, dtype={"cod_barrio": str}).query("comparable").cod_barrio)
        ca = pd.read_csv(q, dtype={"cod_barrio": str})
        ca = ca[(ca.nacionalidad == "Total") & ca.cod_barrio.isin(comp)].set_index(["anio", "cod_barrio"]).poblacion
        for a in range(2021, 2026):
            x = pob[pob.anio == a].set_index("codigo").valor
            y = ca.xs(a, level="anio") if a in ca.index.get_level_values(0) else pd.Series(dtype=float)
            j = pd.concat([x.rename("padron"), y.rename("censo")], axis=1).dropna()
            if len(j):
                r = (j.padron / j.censo - 1).abs() * 100
                v.loc[v.anio == a, "barrios_contraste_censo"] = len(j)
                v.loc[v.anio == a, "dif_censo_mediana_pct"] = round(float(r.median()), 2)
                v.loc[v.anio == a, "dif_censo_max_pct"] = round(float(r.max()), 2)
    return v


def main() -> int:
    c = crudas()
    c.to_csv(DIR / "tablas_crudas.csv.gz", index=False, compression=GZ_PANDAS)
    b, d = norm_barrio_distrito(c)
    ab = altas_bajas(c)
    pa = paises(c)
    e = equivalencias(b)
    v = validar(b, d, c)
    for df, n in ((b, "vlc_padron_barrio.csv.gz"), (d, "vlc_padron_distrito.csv.gz"), (ab, "vlc_altas_bajas_distrito.csv.gz"),
                  (pa, "vlc_nacionalidades_principales.csv.gz")):
        df.to_csv(DIR / n, index=False, compression=GZ_PANDAS)
    e.to_csv(DIR / "equivalencias_barrios.csv", index=False)
    v.to_csv(DIR / "validacion.csv", index=False)
    for n, desc in (("tablas_crudas.csv.gz", "todas las filas reconocidas"), ("vlc_padron_barrio.csv.gz", "barrio: sexo, edad (3 grupos), continente"),
                    ("vlc_padron_distrito.csv.gz", "distrito: sexo, edad (3 grupos), continente"),
                    ("vlc_altas_bajas_distrito.csv.gz", "altas y bajas por distrito y componente"),
                    ("vlc_nacionalidades_principales.csv.gz", "nacionalidades principales: total de la ciudad y 4 distritos con más peso (2005-2018)"), ("equivalencias_barrios.csv", "código PDF → código del Ajuntament"),
                    ("validacion.csv", "contraste con INE y censo anual")):
        registrar("vlc_padron", DIR / n, URL, edicion="Ajuntament de València, padrón municipal (PDF, extracción propia)", periodo="2001-2026",
                  nivel_territorial="ciudad, distrito, barrio", licencia=LIC, redistribuible=True, notas=desc)
    print(v.to_string())
    print("equivalencias que no coinciden:", int((~e.coincide).sum()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
