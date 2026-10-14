"""V9-DATOS-COMPLETO, bloque 0: regulación de vivienda (zonas tensionadas y normas) ampliada hasta octubre de 2026.

Pasos (solo descarga, transcripción con fuente y validación; sin estimaciones):
  1. Escanea los sumarios del BOE (API de datos abiertos, un JSON por día) desde la Ley 12/2023 (2023-05-25) hasta
     FIN y guarda los títulos que contienen términos de vivienda en regulacion/boe_sumarios_vivienda.csv (cada fila
     con su identificador BOE, fecha, sección, departamento y URL).
  2. Para cada resolución de la Secretaría de Estado de Vivienda «por la que se publica la relación de zonas de mercado
     residencial tensionado» descarga el XML y extrae los municipios. El cruce nombre → código INE usa el diccionario
     de municipios del INE dentro de la provincia indicada y queda en correspondencia_zt_nombre_ine.csv (tabla de
     correspondencia documentada; una fila por nombre de la resolución).
  3. Escribe zonas_tensionadas_v9.csv: las 318 declaraciones de data/raw/v3 (sin cambios, origen = v3) más las nuevas,
     con fechas de declaración, efecto y fin, norma y alcance (topes, temporada, habitaciones; véase LEEME.md).
  4. Escribe eventos_regulacion_v9.csv: eventos de v2 y v3 más las normas nuevas identificadas en el BOE, con URL.
Los ficheros de data/raw/v2 y data/raw/v3 se leen, nunca se modifican.
"""
from __future__ import annotations

import concurrent.futures as cf
import csv
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import CABECERAS, FORCE, RAIZ, RAW9, registrar, sha256  # noqa: E402

FUENTE = "regulacion"
DIR = RAW9 / FUENTE
INICIO = dt.date(2023, 5, 25)
FIN = dt.date(2026, 10, 14)
API_SUMARIO = "https://www.boe.es/datosabiertos/api/boe/sumario/{fecha}"
LICENCIA = "BOE: reutilización libre con cita de la fuente (aviso legal del BOE; Real Decreto 181/2008)"
PATRON = re.compile(r"tensionad|vivienda|arrendamiento|alquiler|uso tur[ií]stico|turístic|habitatge|lloguer", re.I)
SUMARIOS = DIR / "boe_sumarios_vivienda.csv"
COLS_SUM = ["fecha", "identificador", "seccion", "departamento", "epigrafe", "titulo", "url_html"]


def _items(nodo):
    if nodo is None:
        return []
    return nodo if isinstance(nodo, list) else [nodo]


def _dia(fecha: dt.date) -> list[dict]:
    url = API_SUMARIO.format(fecha=fecha.strftime("%Y%m%d"))
    for i in range(3):
        try:
            r = requests.get(url, headers={**CABECERAS, "Accept": "application/json"}, timeout=60)
            if r.status_code == 404:
                return []          # sin BOE ese día (domingos y festivos)
            r.raise_for_status()
            d = r.json()["data"]["sumario"]
            break
        except Exception:  # noqa: BLE001
            if i == 2:
                raise
            time.sleep(2 ** (i + 1))
    filas = []
    for diario in _items(d.get("diario")):
        for sec in _items(diario.get("seccion")):
            for dep in _items(sec.get("departamento")):
                epis = _items(dep.get("epigrafe"))
                grupos = [(e.get("nombre", ""), _items(e.get("item"))) for e in epis] + [("", _items(dep.get("item")))]
                for epi, items in grupos:
                    for it in items:
                        t = it.get("titulo", "")
                        if PATRON.search(t):
                            filas.append({"fecha": fecha.isoformat(), "identificador": it.get("identificador", ""),
                                          "seccion": sec.get("nombre", ""), "departamento": dep.get("nombre", ""),
                                          "epigrafe": epi, "titulo": " ".join(t.split()), "url_html": it.get("url_html", "")})
    return filas


def escanear_boe() -> list[dict]:
    dias = [INICIO + dt.timedelta(d) for d in range((FIN - INICIO).days + 1)]
    filas: list[dict] = []
    fallos = []
    with cf.ThreadPoolExecutor(8) as ex:
        fut = {ex.submit(_dia, d): d for d in dias}
        for f in cf.as_completed(fut):
            try:
                filas += f.result()
            except Exception as e:  # noqa: BLE001
                fallos.append(f"{fut[f]}: {e}")
    if fallos:
        raise RuntimeError(f"{len(fallos)} días sin sumario: {fallos[:5]}")
    filas.sort(key=lambda r: (r["fecha"], r["identificador"]))
    with open(SUMARIOS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS_SUM)
        w.writeheader()
        w.writerows(filas)
    return filas


# ---------------------------------------------------------------- normas: XML del BOE (metadatos, análisis y texto)
XML_BOE = "https://www.boe.es/diario_boe/xml.php?id={id}"
DIR_XML = DIR / "boe_xml"
EVENTOS = DIR / "eventos_regulacion_v9.csv"
BANDERAS = {   # búsqueda literal en el texto de la norma (indicador automático; no sustituye a la lectura del articulado)
    "menciona_zona_tensionada": r"tensionad|mercado residencial tensado",
    "menciona_indice_referencia": r"[íi]ndices? de (?:precios de )?referencia",
    "menciona_temporada": r"arrendamientos? de temporada|alquiler(?:es)? de temporada|car[aá]cter temporal",
    "menciona_habitaciones": r"arrendamientos? de habitaci|alquiler(?:es)? de habitaci",
    "menciona_uso_turistico": r"uso tur[ií]stico",
    "menciona_gran_tenedor": r"gran(?:des)? tenedor",
}
COLS_EV = ["identificador", "origen", "fecha_publicacion", "fecha_disposicion", "rango", "numero_oficial", "departamento",
           "titulo", "fecha_vigencia", "estatus_derogacion", "fecha_derogacion", "judicialmente_anulada", "vigencia_agotada",
           "nota_diario_autonomico", "convalidacion", "referencias_posteriores", "materias", *BANDERAS,
           "en_proyecto_v2_v3", "url_eli", "url_html", "verificacion"]
# Normas autonómicas que no están en el BOE a la fecha de corte: se registran con la ficha del DOGC (Portal Jurídic)
DOGC_SIN_BOE = [
    {"identificador": "DOGC-9339-DL-1/2025", "origen": "DOGC (Portal Jurídic de Catalunya, conjunto abierto n6hn-rmy7)",
     "fecha_publicacion": "2025-01-29", "fecha_disposicion": "2025-01-28", "rango": "Decreto-ley", "numero_oficial": "1/2025",
     "departamento": "Comunidad Autónoma de Cataluña",
     "titulo": "Decreto ley 1/2025, de 28 de enero, de medidas urgentes en materia de contención de rentas",
     "nota_diario_autonomico": "DOGC núm. 9339, de 29 de enero de 2025",
     "url_eli": "https://portaljuridic.gencat.cat/eli/es-ct/dl/2025/01/28/1",
     "verificacion": "VERIFICADA la publicación (DOGC). Convalidación o derogación NO VERIFICADA: no figura en el BOE a "
                     "2026-10-14 y el conjunto de normativa del DOGC no incluye las resoluciones del Parlament "
                     "(docs/v9/fuentes_fallidas.md)."},
]


def _txt(raw: str, etiqueta: str) -> str:
    m = re.search(rf"<{etiqueta}[^>]*>(.*?)</{etiqueta}>", raw, re.S)
    return " ".join(m.group(1).split()) if m else ""


def _fecha(s: str) -> str:
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if re.fullmatch(r"\d{8}", s or "") else ""


def ficha_boe(ident: str) -> dict:
    import gzip
    import html as html_mod
    ruta = DIR_XML / f"{ident}.xml.gz"
    if not ruta.exists():
        r = requests.get(XML_BOE.format(id=ident), headers=CABECERAS, timeout=120)
        r.raise_for_status()
        DIR_XML.mkdir(parents=True, exist_ok=True)
        with open(ruta, "wb") as f, gzip.GzipFile(filename="", mode="wb", fileobj=f, mtime=0) as g:
            g.write(r.content)
    raw = gzip.decompress(ruta.read_bytes()).decode("utf-8")
    # el cuerpo es el bloque <texto> más largo (las referencias del análisis también usan <texto>)
    cuerpo = max(re.findall(r"<texto[^>]*>(.*?)</texto>", raw, re.S), key=len, default=raw)
    texto = " ".join(html_mod.unescape(re.sub(r"<[^>]+>", " ", cuerpo)).split())
    post = re.search(r"<posteriores>(.*?)</posteriores>", raw, re.S)
    refs = []
    if post:
        for m in re.finditer(r'referencia="(.*?)".*?<palabra[^>]*>(.*?)</palabra>\s*<texto>(.*?)</texto>', post.group(1), re.S):
            refs.append(f"{m.group(1)}: {' '.join(m.group(2).split())} {' '.join(m.group(3).split())}")
    fila = {"identificador": ident, "origen": "BOE (XML de la disposición)",
            "fecha_publicacion": _fecha(_txt(raw, "fecha_publicacion")),
            "fecha_disposicion": _fecha(_txt(raw, "fecha_disposicion")), "rango": _txt(raw, "rango"),
            "numero_oficial": _txt(raw, "numero_oficial"), "departamento": _txt(raw, "departamento"),
            "titulo": _txt(raw, "titulo"), "fecha_vigencia": _fecha(_txt(raw, "fecha_vigencia")),
            "estatus_derogacion": _txt(raw, "estatus_derogacion"), "fecha_derogacion": _fecha(_txt(raw, "fecha_derogacion")),
            "judicialmente_anulada": _txt(raw, "judicialmente_anulada"), "vigencia_agotada": _txt(raw, "vigencia_agotada"),
            "nota_diario_autonomico": "; ".join(" ".join(n.split()) for n in re.findall(r"<nota[^>]*>(.*?)</nota>", raw, re.S)),
            "convalidacion": "; ".join(r for r in refs if re.search(r"convalid|DEROGA", r, re.I)),
            "referencias_posteriores": " | ".join(refs),
            "materias": "; ".join(re.findall(r"<materia[^>]*>(.*?)</materia>", raw)),
            "url_eli": _txt(raw, "url_eli"), "url_html": f"https://www.boe.es/buscar/act.php?id={ident}",
            "verificacion": "VERIFICADA BOE"}
    for k, pat in BANDERAS.items():
        fila[k] = "sí" if re.search(pat, texto, re.I) else "no"
    return fila


def ids_proyecto() -> set[str]:
    ids = set()
    for rel in ("data/raw/v2_eventos_politica.csv", "data/raw/v3/eventos_v3.csv", "data/raw/v3/zonas_tensionadas_v3.csv"):
        ids |= set(re.findall(r"BOE-A-\d{4}-\d+", (RAIZ / rel).read_text(encoding="utf-8")))
    return ids


def construir_eventos(sumarios: list[dict]) -> list[dict]:
    """Disposiciones generales (sección I) con términos de vivienda y resoluciones de zonas tensionadas (sección III)."""
    sel = [r for r in sumarios if r["seccion"].startswith("I.") or re.search(r"tensionad", r["titulo"], re.I)]
    ids = sorted({r["identificador"] for r in sel if r["identificador"].startswith("BOE-A")})
    previos = ids_proyecto()
    filas = []
    for ident in ids:
        f = ficha_boe(ident)
        f["en_proyecto_v2_v3"] = "sí" if ident in previos else "no"
        filas.append(f)
    for d in DOGC_SIN_BOE:
        filas.append({**{k: "" for k in COLS_EV}, **d, "en_proyecto_v2_v3": "no"})
    filas.sort(key=lambda r: (r["fecha_publicacion"], r["identificador"]))
    with open(EVENTOS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS_EV)
        w.writeheader()
        w.writerows(filas)
    return filas


# ---------------------------------------------------------------- zonas tensionadas y alcance del régimen
ZT_V3 = RAIZ / "data/raw/v3/zonas_tensionadas_v3.csv"
ZT_V9 = DIR / "zonas_tensionadas_v9.csv"
ALCANCE = DIR / "regimen_alcance_v9.csv"
CORRECCIONES = {"BOE-A-2025-15728": "BOE-A-2025-20246 (corrección de erratas: solo enlaces a las memorias; no cambia municipios)"}
# Alcance del régimen por ámbito, transcrito de las normas (identificador BOE y artículo). `hasta` vacío = vigente a FIN.
# Las filas con fecha de inicio desde 2026-07-01 son posteriores al pre-registro de V7/V8 (posterior_prereg).
ALCANCE_FILAS = [
    ("estatal", "", "tope_renta_nuevos_contratos", "Ley 12/2023, disp. final 1.ª (art. 17.6 LAU): en zona declarada, la renta "
     "del nuevo contrato no puede superar la del contrato anterior actualizada", "BOE-A-2023-12203", "2023-05-26", ""),
    ("estatal", "", "tope_renta_indice_referencia", "Art. 17.7 LAU (Ley 12/2023): grandes tenedores y viviendas sin alquiler en "
     "los cinco años previos, límite del índice de referencia; sistema estatal publicado por resolución", "BOE-A-2024-7593",
     "2024-04-17", ""),
    ("estatal", "", "prorroga_extraordinaria_zona", "Art. 10.3 LAU (Ley 12/2023): prórroga extraordinaria anual hasta tres "
     "años en zona declarada", "BOE-A-2023-12203", "2023-05-26", ""),
    ("estatal", "", "prorroga_extraordinaria_general", "RDL 8/2026, art. 1: prórroga extraordinaria hasta dos años de "
     "contratos que vencen antes de 2028; derogado por no convalidación (BOE-A-2026-9359)", "BOE-A-2026-6545", "2026-03-22",
     "2026-04-30"),
    ("estatal", "", "temporada_y_habitaciones", "RDL 26/2026: régimen de temporada y habitaciones; derogado (BOE-A-2026-20526)",
     "BOE-A-2026-20266", "2026-10-01", "2026-10-02"),
    ("estatal", "", "temporada_y_habitaciones", "RDL 29/2026, art. 3 (LAU): la suma de rentas por habitaciones no puede "
     "superar la del contrato unitario y, en zona declarada, respeta el art. 17.6-17.8 LAU; régimen de temporada. "
     "Pendiente de convalidación a 2026-10-14", "BOE-A-2026-20823", "2026-10-08", ""),
    ("estatal", "", "duracion_contratos", "RDL 28/2026: nuevo régimen de renovación tras el plazo mínimo (vigencia "
     "2026-11-15); pendiente de convalidación a 2026-10-14. RDL 27/2026, mismo objeto, derogado (BOE-A-2026-20527)",
     "BOE-A-2026-20822", "2026-11-15", ""),
    ("09", "Cataluña", "temporada_y_habitaciones", "DL 6/2024 (temporada y habitaciones sujetos a contención); derogado por "
     "no convalidación, Resolución de 23-05-2024", "BOE-A-2024-12642", "2024-04-26", "2024-05-27"),
    ("09", "Cataluña", "contencion_rentas_otros", "DL 1/2025 (contención de rentas; DOGC 9339). Convalidación o derogación "
     "NO VERIFICADA; fechas de efecto no verificadas", "DOGC-9339-DL-1/2025", "2025-01-29", ""),
    ("09", "Cataluña", "contencion_rentas_otros", "DL 2/2025 (vivienda y urbanismo; convalidado por Resolución 169/XV, "
     "9-04-2025)", "BOE-A-2025-8490", "2025-02-27", ""),
    ("09", "Cataluña", "temporada_y_habitaciones", "Ley 11/2025, art. 5 (arts. 66 bis y 66 ter de la Ley 18/2007): "
     "arrendamiento temporal y de habitaciones; recurso de inconstitucionalidad 2415-2026 admitido el 9-06-2026 sin "
     "suspensión publicada en el BOE", "BOE-A-2026-5547", "2026-01-01", ""),
    ("15", "Navarra", "temporada_y_habitaciones", "Ley Foral 11/2026, reguladora del arrendamiento de habitaciones "
     "(habitual, de temporada y hospedaje; registro obligatorio)", "BOE-A-2026-16356", "2026-07-14", ""),
    ("15", "Navarra", "contencion_rentas_otros", "Ley Foral 9/2025, derecho a la vivienda asequible", "BOE-A-2025-15656",
     "2025-07-12", ""),
    ("15", "Navarra", "contencion_rentas_otros", "Ley Foral 14/2026, modifica la LF 10/2010", "BOE-A-2026-16359",
     "2026-07-14", ""),
]
COLS_ALC = ["cod_ccaa", "ccaa", "medida", "descripcion", "identificador", "desde", "hasta", "posterior_prereg", "url"]


MESES = {m: i + 1 for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                          "septiembre", "octubre", "noviembre", "diciembre"])}


def _norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def construir_zonas() -> tuple[int, int]:
    """Copia literal de las 318 declaraciones de v3 con columnas de control frente al texto del BOE."""
    import gzip
    import html as html_mod
    with open(ZT_V3, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    textos = {}
    for ident in {r["resolucion_boe"] for r in filas}:
        raw = gzip.decompress((DIR_XML / f"{ident}.xml.gz").read_bytes()).decode("utf-8")
        cuerpo = max(re.findall(r"<texto[^>]*>(.*?)</texto>", raw, re.S), key=len)
        textos[ident] = _norm(html_mod.unescape(re.sub(r"<[^>]+>", " ", cuerpo)))
    no_hallados = 0
    for r in filas:
        nombre = re.split(r"[/(]", r["municipio_resolucion"])[0]
        hallado = _norm(nombre) in textos[r["resolucion_boe"]]
        no_hallados += not hallado
        r["nombre_en_texto_boe"] = "sí" if hallado else "no"
        r["correccion_errores"] = CORRECCIONES.get(r["resolucion_boe"], "")
        r["vigente_a_fecha_corte"] = "sí" if r["fecha_efecto"] <= FIN.isoformat() < r["fecha_fin_prevista"] else "no"
        r["posterior_prereg"] = "sí" if r["fecha_efecto"] >= "2026-07-01" else "no"
        r["origen"] = "data/raw/v3/zonas_tensionadas_v3.csv (sin cambios)"
        r["fecha_declaracion_v9"], r["fuente_fecha_declaracion_v9"] = r["fecha_declaracion_autonomica"], "v3"
        if not r["fecha_declaracion_v9"]:   # p. ej., Navarra: «Orden Foral 157E/2025, de 19 de mayo»
            m = re.search(r"(\d{4}), de (\d{1,2}) de (\w+)", r["declaracion_autonomica"])
            if m and m.group(3).lower() in MESES:
                r["fecha_declaracion_v9"] = f"{m.group(1)}-{MESES[m.group(3).lower()]:02d}-{int(m.group(2)):02d}"
                r["fuente_fecha_declaracion_v9"] = "título de la norma autonómica (año del número oficial)"
    cols = list(filas[0].keys())
    with open(ZT_V9, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)
    with open(ALCANCE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS_ALC)
        w.writeheader()
        for c, n, m, d, i, a, h in ALCANCE_FILAS:
            url = f"https://www.boe.es/buscar/act.php?id={i}" if i.startswith("BOE") else \
                "https://portaljuridic.gencat.cat/eli/es-ct/dl/2025/01/28/1"
            w.writerow({"cod_ccaa": c, "ccaa": n, "medida": m, "descripcion": d, "identificador": i, "desde": a, "hasta": h,
                        "posterior_prereg": "sí" if a >= "2026-07-01" else "no", "url": url})
    return len(filas), no_hallados


def verificar_manifiesto() -> int:
    man = DIR / "_manifest.csv"
    if not man.exists():
        print("falta _manifest.csv"); return 1
    with open(man, encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            ruta = RAIZ / fila["fichero"]
            if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                print("FALLO", fila["fichero"]); return 1
    print("OK regulacion"); return 0


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto()
    if SUMARIOS.exists() and not FORCE:   # caché: el escaneo completo tarda unos 4 minutos
        with open(SUMARIOS, encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
    else:
        filas = escanear_boe()
    registrar(FUENTE, SUMARIOS, API_SUMARIO, edicion=f"sumarios diarios del BOE {INICIO}–{FIN}",
              periodo=f"{INICIO}–{FIN}", nivel_territorial="norma (estatal y autonómica publicada en el BOE)",
              licencia=LICENCIA, redistribuible=True,
              notas=f"títulos con términos de vivienda: {len(filas)}; patrón: {PATRON.pattern}")
    print("sumarios", len(filas))
    ev = construir_eventos(filas)
    registrar(FUENTE, EVENTOS, XML_BOE, edicion=f"XML del BOE (metadatos, análisis y texto) a {FIN}",
              periodo=f"{min(r['fecha_publicacion'] for r in ev)}–{max(r['fecha_publicacion'] for r in ev)}",
              nivel_territorial="norma (estatal y autonómica)", licencia=LICENCIA, redistribuible=True,
              notas=f"normas: {len(ev)}; nuevas frente a v2/v3: {sum(r['en_proyecto_v2_v3'] == 'no' for r in ev)}; "
                    "banderas por búsqueda literal en el texto")
    print("eventos", len(ev))
    resol_boe = {r["identificador"] for r in filas if re.search(r"relación de zonas de mercado residencial tensionado",
                                                                  r["titulo"]) and not r["titulo"].startswith("Corrección")}
    with open(ZT_V3, encoding="utf-8") as f:
        resol_v3 = {r["resolucion_boe"] for r in csv.DictReader(f)}
    if resol_boe != resol_v3:
        raise RuntimeError(f"resoluciones del BOE distintas de v3: {sorted(resol_boe ^ resol_v3)}")
    n, no = construir_zonas()
    registrar(FUENTE, ZT_V9, "https://www.boe.es/buscar/act.php?id={resolucion_boe}",
              edicion=f"v3 + control frente al BOE a {FIN}", periodo="2024-03-16–2029-07-30 (efecto–fin previsto)",
              nivel_territorial="municipio (código INE) y ámbito inframunicipal", licencia=LICENCIA, redistribuible=True,
              notas=f"declaraciones={n}; resoluciones BOE={len(resol_boe)} (todas en v3; ninguna nueva hasta {FIN}); "
                    f"nombres no hallados en el texto={no}")
    registrar(FUENTE, ALCANCE, "https://www.boe.es/buscar/act.php?id={identificador}", edicion=f"transcripción a {FIN}",
              periodo="2023-05-26–", nivel_territorial="estatal y CCAA", licencia=LICENCIA, redistribuible=True,
              notas=f"filas={len(ALCANCE_FILAS)}")
    print("zonas", n, "no halladas", no)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
