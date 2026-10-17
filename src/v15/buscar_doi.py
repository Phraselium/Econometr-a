"""V15-F2 · Busca en Crossref el DOI de las fichas «sin DOI» de docs/v15/literatura/*.md (necesita red; se ejecuta una vez).

Para cada ficha sin DOI consulta Crossref por bibliografía (autores + título) y acepta el primer resultado solo si:
título con similitud de palabras ≥ 0,8, apellido del primer autor presente en la cabecera y año a ±1. Si se acepta, la línea
«- DOI:» pasa a «- DOI: <doi> (localizado en Crossref por el orquestador; …)» y verificar_referencias.py hace después la
comprobación completa. Nunca inventa: si no hay coincidencia, la ficha sigue «sin DOI».
Uso: python3 src/v15/buscar_doi.py [--solo P9_*.md]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verificar_referencias import FICHA, LIT, _norm, _palabras  # noqa: E402

LINEA_DOI = re.compile(r"^- DOI:[ \t]*+(?!10\.)(.*)$", re.M)   # posesivo: sin retroceso que deje pasar «- DOI: 10.…»


def candidato(cab: str) -> dict | None:
    q = urllib.parse.quote(re.sub(r"[()]", " ", cab))
    req = urllib.request.Request(f"https://api.crossref.org/works?query.bibliographic={q}&rows=3",
                                 headers={"User-Agent": "vivienda-espana-evidencia (verificador de referencias)"})
    for espera in (2, 8, 30, 60):   # Crossref limita la frecuencia (429): reintentos con espera creciente
        time.sleep(1)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:   # noqa: S310 (URL fija de Crossref)
                items = json.load(r)["message"]["items"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(espera)
    else:
        return None
    tit = cab.split(". ", 1)[1] if ". " in cab else cab
    anio = re.search(r"\((\d{4})", cab)
    for it in items:
        ct = _palabras((it.get("title") or [""])[0])
        ft = _palabras(tit)
        if not ct or len(ft & ct) / max(1, min(len(ft), len(ct))) < 0.8:
            continue
        a = (it.get("author") or [{}])[0].get("family", "")
        if not a or re.sub(r"[^a-z]", "", _norm(a).split()[-1]) not in re.sub(r"[^a-z]", "", _norm(cab.split("(")[0])):
            continue
        y = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        if anio and y and abs(int(anio.group(1)) - int(y)) > 1:
            continue
        return {"doi": it["DOI"], "revista": (it.get("container-title") or [""])[0]}
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", default="*.md")
    a = ap.parse_args()
    n = 0
    for p in sorted(LIT.glob(a.solo)):
        partes = re.split(r"(?=^### )", p.read_text(encoding="utf-8"), flags=re.M)
        for i, b in enumerate(partes):
            m = LINEA_DOI.search(b)
            if not b.startswith("### ") or not m:
                continue
            c = candidato(FICHA.search(b).group(1))
            if c:
                partes[i] = b.replace(m.group(0), f"- DOI: {c['doi']} (localizado en Crossref por el orquestador; {c['revista']}) · antes: {m.group(1)}")
                n += 1
        p.write_text("".join(partes), encoding="utf-8")
    print(f"buscar_doi: {n} DOI localizados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
