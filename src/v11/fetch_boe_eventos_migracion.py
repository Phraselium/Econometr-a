"""V11-DATOS (bloque 1, punto 7): tabla de eventos normativos migratorios del ámbito estatal desde el BOE.

Fuente: API de datos abiertos del BOE, legislación consolidada
(https://www.boe.es/datosabiertos/api/legislacion-consolidada), búsqueda por título con términos de extranjería,
asilo, protección temporal o internacional, visados y residencia de extranjeros; se añaden por identificador las
disposiciones no consolidadas que aplican la protección temporal (Ucrania 2022), verificadas una a una contra el XML
del BOE (https://www.boe.es/diario_boe/xml.php?id=<id>).
Cada evento: identificador BOE, rango, número, fecha de disposición, publicación y vigencia, título, departamento,
vigencia agotada y «alcance» (clasificación propia por palabras del título: ley orgánica de extranjería, reglamento,
protección internacional, protección temporal, ciudadanos UE, visados y movilidad, regularización o arraigo, otros).
Segunda salida: modificaciones_normas_nucleo.csv.gz, las referencias posteriores (modifica, deroga, desarrolla) de\ncada norma núcleo según el análisis del BOE. Solo hechos de calendario (C1, descriptivo); el alcance es una etiqueta de búsqueda, no una valoración.
Licencia BOE: reutilización libre con cita (Aviso legal; Ley 37/2007).
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, RAW11, abrir_gz_texto, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "boe_eventos_migracion"
DIR = RAW11 / FUENTE
API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada"
LIC = "BOE: reutilización libre con cita de la fuente"
CONSULTAS = ["titulo:extranjeros", "titulo:extranjería", "titulo:asilo", "titulo:\"protección temporal\"",
             "titulo:\"protección internacional\"", "titulo:inmigración", "titulo:\"Ley Orgánica 4/2000\"",
             "titulo:visados", "titulo:apátrida", "titulo:refugiados", "titulo:\"Unión Europea\" AND titulo:residencia"]
# no consolidadas: verificadas contra el XML del BOE en cada ejecución
EXTRA = ["BOE-A-2022-3715", "BOE-A-2022-3716", "BOE-A-2005-342"]
ALCANCE = [("protección temporal", "proteccion_temporal"), ("asilo", "proteccion_internacional"),
           ("protección internacional", "proteccion_internacional"), ("refugiad", "proteccion_internacional"),
           ("apátrida", "proteccion_internacional"), ("Unión Europea", "ciudadanos_ue"),
           ("Reglamento de la Ley Orgánica 4/2000", "reglamento_extranjeria"), ("Reglamento de ejecución", "reglamento_extranjeria"),
           ("Ley Orgánica 4/2000", "ley_extranjeria"), ("derechos y libertades de los extranjeros", "ley_extranjeria"),
           ("visado", "visados_movilidad"), ("movilidad internacional", "visados_movilidad"), ("emprendedores", "visados_movilidad"),
           ("arraigo", "regularizacion_arraigo"), ("regulariza", "regularizacion_arraigo"), ("normalización", "regularizacion_arraigo")]
COLS = ["identificador", "rango", "numero_oficial", "fecha_disposicion", "fecha_publicacion", "fecha_vigencia",
        "vigencia_agotada", "departamento", "alcance", "titulo", "url", "origen"]


def get(url: str) -> requests.Response:
    for i in range(3):
        try:
            r = requests.get(url, headers={**CABECERAS, "Accept": "application/json"}, timeout=120)
            r.raise_for_status()
            return r
        except Exception:  # noqa: BLE001
            time.sleep(2 ** (i + 1))
    raise RuntimeError(url)


def alcance(t: str) -> str:
    for k, v in ALCANCE:
        if k.lower() in t.lower():
            return v
    return "otros"


def iso(f: str) -> str:
    return f"{f[:4]}-{f[4:6]}-{f[6:8]}" if f and re.fullmatch(r"\d{8}", f[:8]) else ""


MESES = {m: i + 1 for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                           "septiembre", "octubre", "noviembre", "diciembre"])}
COLS_MOD = ["norma_modificada", "alcance_modificada", "id_norma_modificadora", "fecha_disposicion_modificadora", "relacion", "texto"]


def lista(x) -> list:
    """El JSON del BOE convierte listas de un elemento en objeto: se normaliza a lista."""
    return [] if x in (None, "") else x if isinstance(x, list) else [x]


def modificaciones(nucleo: list[dict]) -> list[dict]:
    """Referencias posteriores (modifica, deroga, desarrolla…) de cada norma núcleo, según el análisis del BOE."""
    out = []
    for e in nucleo:
        d = get(f"{API}/id/{e['identificador']}/analisis").json().get("data") or []
        refs = (d[0].get("referencias") or {}) if d and isinstance(d[0], dict) else {}
        refs = refs if isinstance(refs, dict) else {}
        for bloque in lista(refs.get("posteriores")):
            for r in lista(bloque.get("posterior") if isinstance(bloque, dict) else None):
                if not isinstance(r, dict):
                    continue
                t = r.get("texto", "") or ""
                m = re.search(r"(?:por|:) [^,:]*?\d+/(\d{4}), de (\d{1,2}) de (\w+)", t)
                f = f"{m.group(1)}-{MESES.get(m.group(3).lower(), 0):02d}-{int(m.group(2)):02d}" if m and m.group(3).lower() in MESES else ""
                out.append({"norma_modificada": e["identificador"], "alcance_modificada": e["alcance"],
                            "id_norma_modificadora": r.get("id_norma", ""), "fecha_disposicion_modificadora": f,
                            "relacion": r.get("relacion", {}).get("texto", ""), "texto": t})
        time.sleep(0.5)
    return sorted(out, key=lambda x: (x["fecha_disposicion_modificadora"], x["norma_modificada"], x["id_norma_modificadora"]))


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    ev: dict[str, dict] = {}
    for q in CONSULTAS:
        consulta = json.dumps({"query": {"query_string": {"query": q}}}, ensure_ascii=False)
        url = f"{API}?query={urllib.parse.quote(consulta)}&limit=500"
        for d in get(url).json().get("data", []) or []:
            if d.get("ambito", {}).get("codigo") != "1":
                continue
            t = d["titulo"]
            ev[d["identificador"]] = {"identificador": d["identificador"], "rango": d["rango"]["texto"],
                                      "numero_oficial": d.get("numero_oficial", ""), "fecha_disposicion": iso(d.get("fecha_disposicion", "")),
                                      "fecha_publicacion": iso(d.get("fecha_publicacion", "")), "fecha_vigencia": iso(d.get("fecha_vigencia", "")),
                                      "vigencia_agotada": d.get("vigencia_agotada", ""), "departamento": d["departamento"]["texto"],
                                      "alcance": alcance(t), "titulo": t, "url": d.get("url_html_consolidada", ""),
                                      "origen": f"API consolidada ({q})"}
        print(q, len(ev))
    for i in EXTRA:
        if i in ev:
            continue
        x = get(f"https://www.boe.es/diario_boe/xml.php?id={i}").text
        g = lambda tag: (re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", x, re.S) or [None, ""])[1].strip()  # noqa: E731
        t = g("titulo")
        if not t:
            print("no verificado", i)
            continue
        ev[i] = {"identificador": i, "rango": g("rango"), "numero_oficial": g("numero_oficial"),
                 "fecha_disposicion": iso(g("fecha_disposicion")), "fecha_publicacion": iso(g("fecha_publicacion")),
                 "fecha_vigencia": iso(g("fecha_vigencia")), "vigencia_agotada": "", "departamento": g("departamento"),
                 "alcance": alcance(t), "titulo": t, "url": f"https://www.boe.es/diario_boe/txt.php?id={i}", "origen": "XML BOE (no consolidada)"}
    filas = sorted(ev.values(), key=lambda e: (e["fecha_publicacion"], e["identificador"]))
    ruta = DIR / "eventos_normativos_migracion.csv.gz"
    with abrir_gz_texto(ruta) as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(filas)
    registrar(FUENTE, ruta, API, edicion="BOE legislación consolidada (API) + XML del BOE",
              periodo=f"{filas[0]['fecha_publicacion']}–{filas[-1]['fecha_publicacion']}", nivel_territorial="España (ámbito estatal)",
              licencia=LIC, redistribuible=True, notas=f"{len(filas)} disposiciones; alcance = etiqueta propia por título")
    mods = modificaciones([e for e in filas if e["alcance"] != "otros" and e["origen"].startswith("API")])
    r2 = DIR / "modificaciones_normas_nucleo.csv.gz"
    with abrir_gz_texto(r2) as f:
        w = csv.DictWriter(f, fieldnames=COLS_MOD)
        w.writeheader()
        w.writerows(mods)
    fs = [m["fecha_disposicion_modificadora"] for m in mods if m["fecha_disposicion_modificadora"]]
    registrar(FUENTE, r2, API + "/id/<id>/analisis", edicion="BOE legislación consolidada: análisis (referencias posteriores)",
              periodo=f"{min(fs)}–{max(fs)}", nivel_territorial="España (ámbito estatal)", licencia=LIC, redistribuible=True,
              notas=f"{len(mods)} modificaciones, derogaciones o desarrollos de las normas núcleo (alcance distinto de «otros»); "
                    "fecha extraída del texto de la referencia")
    print(len(filas), len(mods))
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
