"""V15-B3 · Verificador determinista de referencias de docs/v15/literatura/*.md.

Para cada ficha («### Autores (año). Título» con una línea «- DOI: …» y una línea «- Estado: …»):
1. Si el DOI está en la caché versionada docs/v15/literatura/crossref_cache.json, la usa (sin red). Si no, y no se pasa
   --sin-red, consulta https://api.crossref.org/works/<DOI> y guarda la respuesta reducida (título, autores, año, revista,
   ISSN, fecha de consulta) en la caché.
2. Compara con la ficha: título (similitud de palabras ≥ 0,6), año (±1 por la diferencia entre versión en línea e impresa) y
   apellido del primer autor.
3. Cuartil: busca la revista (por ISSN o por nombre normalizado) en docs/v15/scimago_cuartiles.csv (versionado; columnas
   revista, issn, cuartil, categoria, anio_scimago, fecha_consulta).
4. Escribe en la ficha «Estado: VERIFICADA (Crossref; cuartil Qx Scimago <año>)», «Estado: VERIFICADA (Crossref; cuartil no
   verificado)», «Estado: DISCREPANTE (<qué no cuadra>)» o «Estado: NO VERIFICADA (sin DOI)».
Un DOI que Crossref no tiene (404) se busca en DataCite (arXiv, Zenodo): si existe, «VERIFICADA (DataCite; … cuartil no aplicable)».
Falla (código 1) si una ficha cita un DOI que no está ni en Crossref ni en DataCite o un DOI sin caché con --sin-red.
Uso: python3 src/v15/verificar_referencias.py [--sin-red] [--solo-comprobar]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
LIT = RAIZ / "docs" / "v15" / "literatura"
CACHE = LIT / "crossref_cache.json"
SCIMAGO = RAIZ / "docs" / "v15" / "scimago_cuartiles.csv"
FICHA = re.compile(r"^### (.+)$", re.M)
DOI = re.compile(r"^- DOI:\s*(10\.\d{4,9}/[^\s·]+)", re.M)
ESTADO = re.compile(r"^- Estado:.*$", re.M)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def _palabras(s: str) -> set[str]:
    return {w for w in _norm(s).split() if len(w) > 3}


def crossref(doi: str, cache: dict, red: bool) -> dict | None:
    if doi in cache:
        return cache[doi]
    if not red:
        raise SystemExit(f"verificar_referencias: DOI sin caché y --sin-red: {doi}")
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "vivienda-espana-evidencia (verificador de referencias)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:   # noqa: S310 (URL fija de Crossref)
            m = json.load(r)["message"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            cache[doi] = datacite(doi) or handle(doi) or {"existe": False, "consulta": dt.date.today().isoformat()}
            return cache[doi]
        raise
    a = m.get("author") or [{}]
    cache[doi] = {"existe": True, "titulo": (m.get("title") or [""])[0], "primer_autor": a[0].get("family", ""),
                  "anio": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                  "revista": (m.get("container-title") or [""])[0], "issn": m.get("ISSN") or [], "consulta": dt.date.today().isoformat()}
    return cache[doi]


def datacite(doi: str) -> dict | None:
    """DOI que no es de Crossref (p. ej. arXiv, Zenodo: 10.48550, 10.5281): se busca en DataCite. Sin cuartil (preprint o datos)."""
    req = urllib.request.Request("https://api.datacite.org/dois/" + urllib.parse.quote(doi),
                                 headers={"User-Agent": "vivienda-espana-evidencia (verificador de referencias)"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:   # noqa: S310 (URL fija de DataCite)
            m = json.load(r)["data"]["attributes"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    cr = (m.get("creators") or [{}])[0]
    return {"existe": True, "registro": "DataCite", "titulo": (m.get("titles") or [{}])[0].get("title", ""),
            "primer_autor": cr.get("familyName") or cr.get("name", "").split(",")[0], "anio": m.get("publicationYear"),
            "revista": m.get("publisher", ""), "issn": [], "consulta": dt.date.today().isoformat()}


def handle(doi: str) -> dict | None:
    """Último recurso: el DOI existe en doi.org (otra agencia, p. ej. mEDRA) pero sin metadatos en Crossref ni DataCite."""
    ag = "https://doi.org/ra/" + urllib.parse.quote(doi.split("/")[0])
    with urllib.request.urlopen(urllib.request.Request("https://doi.org/api/handles/" + urllib.parse.quote(doi)), timeout=60) as r:  # noqa: S310
        if json.load(r).get("responseCode") != 1:
            return None
    with urllib.request.urlopen(urllib.request.Request(ag), timeout=60) as r:   # noqa: S310
        ra = (json.load(r) or [{}])[0].get("RA", "otra agencia")
    return {"existe": True, "registro": ra, "consulta": dt.date.today().isoformat()}


def scimago() -> list[dict]:
    if not SCIMAGO.exists():
        return []
    with SCIMAGO.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def cuartil(cr: dict, sj: list[dict]) -> str | None:
    issn = {i.replace("-", "") for i in cr.get("issn", [])}
    for r in sj:
        if issn & {x.replace("-", "").strip() for x in r["issn"].split(";")} or _norm(r["revista"]) == _norm(cr.get("revista", "")):
            return f"cuartil {r['cuartil']} Scimago {r['anio_scimago']}"
    return None


def estado(cab: str, cr: dict | None, sj: list[dict]) -> str:
    if cr is None:
        return "NO VERIFICADA (sin DOI)"
    if not cr.get("existe"):
        return "DISCREPANTE (el DOI no existe en Crossref)"
    if cr.get("registro") not in (None, "DataCite"):
        return f"NO VERIFICADA (el DOI existe en doi.org, agencia {cr['registro']}, sin metadatos comparables)"
    problemas = []
    tit = cab.split(". ", 1)[1] if ". " in cab else cab
    ft, ct = _palabras(tit), _palabras(cr["titulo"])
    if ct and len(ft & ct) / max(1, min(len(ft), len(ct))) < 0.6:
        problemas.append("título")
    m = re.search(r"\((\d{4})", cab)
    if m and cr.get("anio") and abs(int(m.group(1)) - int(cr["anio"])) > 1:
        problemas.append(f"año ({m.group(1)} frente a {cr['anio']})")
    if cr.get("primer_autor") and _norm(cr["primer_autor"]).split()[-1] not in _norm(cab.split("(")[0]):
        problemas.append(f"primer autor ({cr['primer_autor']})")
    if problemas:
        return "DISCREPANTE (" + ", ".join(problemas) + ")"
    if cr.get("registro") == "DataCite":
        return "VERIFICADA (DataCite; preprint o documento sin revista: cuartil no aplicable)"
    return f"VERIFICADA (Crossref; {cuartil(cr, sj) or 'cuartil no verificado'})"


def procesar(red: bool, escribir: bool, solo: str = "*.md") -> tuple[dict, list[str]]:
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    sj, errores, cuenta = scimago(), [], {}
    for p in sorted(LIT.glob(solo)):
        t = p.read_text(encoding="utf-8")
        partes = re.split(r"(?=^### )", t, flags=re.M)
        nuevas = []
        for b in partes:
            if not b.startswith("### "):
                nuevas.append(b)
                continue
            cab = FICHA.search(b).group(1)
            md = DOI.search(b)
            cr = crossref(md.group(1).rstrip(".,;"), cache, red) if md else None
            if cr is not None and not cr.get("existe"):
                errores.append(f"{p.name}: DOI inexistente en Crossref: {md.group(1)} ({cab[:60]})")
            e = estado(cab, cr, sj)
            cuenta[e.split(" (")[0]] = cuenta.get(e.split(" (")[0], 0) + 1
            b = ESTADO.sub(f"- Estado: {e}", b) if ESTADO.search(b) else b.rstrip("\n") + f"\n- Estado: {e}\n\n"
            nuevas.append(b)
        if escribir:
            p.write_text("".join(nuevas), encoding="utf-8")
    if escribir and red:
        CACHE.write_text(json.dumps(dict(sorted(cache.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return cuenta, errores


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-red", action="store_true")
    ap.add_argument("--solo-comprobar", action="store_true", help="no reescribe las fichas")
    ap.add_argument("--solo", default="*.md", help="patrón de ficheros de docs/v15/literatura (por defecto, todos)")
    a = ap.parse_args()
    cuenta, errores = procesar(red=not a.sin_red, escribir=not a.solo_comprobar, solo=a.solo)
    print("verificar_referencias:", cuenta)
    for e in errores:
        print("  ERROR", e)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
