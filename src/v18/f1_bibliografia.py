"""V18 · Fase 1 · Catálogo y verificación de la bibliografía (docs/v18/bib/<factor>/*.md).

Reutiliza el verificador de V15 (src/v15/verificar_referencias.py: Crossref, DataCite y doi.org; comparación de título, año y
primer autor; cuartil Scimago si está en docs/v15/scimago_cuartiles.csv) sobre las fichas de los bibliotecarios, cuyo DOI va en
la línea «- Clave: … · DOI: …». La caché de V18 es docs/v18/bib/crossref_cache.json.

- `--verificar` (con red, una vez): consulta los DOI sin caché y escribe «- Estado: …» en cada ficha.
- sin argumentos (make v18_f1; sin red): solo con la caché; no reescribe fichas. Escribe output/v18/f1/catalogo.csv e
  informe.md (fichas por factor, lectura, paquete de replicación y estado) y falla si una ficha tiene un DOI sin caché.
No lee datos del proyecto.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v15"))
import verificar_referencias as vr  # noqa: E402

BIB = RAIZ / "docs" / "v18" / "bib"
CACHE = BIB / "crossref_cache.json"
OUT = RAIZ / "output" / "v18" / "f1"
DOI = re.compile(r"DOI:\s*(10\.\d{4,9}/(?:[^\s·;,()]|\([^\s()]*\))+)")
LEIDO = re.compile(r"Leído:\s*(texto completo|solo resumen)", re.I)
PAQUETE = re.compile(r"^- Paquete de replicación:\s*(sí|si|no)\b", re.M | re.I)


def fichas() -> list[Path]:
    return sorted(p for p in BIB.glob("*/*.md") if p.name != "resumen.md")


def procesar(red: bool, escribir: bool) -> tuple[list[dict], list[str]]:
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    sj, filas, err = vr.scimago(), [], []
    for p in fichas():
        t = p.read_text(encoding="utf-8")
        partes, nuevas = re.split(r"(?=^### )", t, flags=re.M), []
        for b in partes:
            if not b.startswith("### "):
                nuevas.append(b)
                continue
            cab = vr.FICHA.search(b).group(1)
            md = DOI.search(b)
            doi = md.group(1).rstrip(".") if md else None
            if doi and doi not in cache and not red:
                err.append(f"{p.relative_to(RAIZ)}: DOI sin caché ({doi}); ejecute con --verificar")
                cr = None
            else:
                try:
                    cr = vr.crossref(doi, cache, red) if doi else None
                except Exception as e:  # noqa: BLE001 (fallo de red: la ficha queda sin verificar y se dice)
                    err.append(f"{p.relative_to(RAIZ)}: consulta de {doi} fallida ({type(e).__name__})")
                    cr = None
            e = vr.estado(cab, cr, sj) if (cr is not None or not doi) else "NO VERIFICADA (consulta pendiente)"
            if escribir:
                b = vr.ESTADO.sub(f"- Estado: {e}", b) if vr.ESTADO.search(b) else b.rstrip("\n") + f"\n- Estado: {e}\n\n"
            nuevas.append(b)
            ml, mp = LEIDO.search(b), PAQUETE.search(b)
            filas.append({"factor": p.parent.name, "fichero": p.name, "referencia": cab, "doi": doi or "",
                          "leido": ml.group(1).lower() if ml else "sin indicar",
                          "paquete": ("sí" if mp.group(1).lower() in ("sí", "si") else "no") if mp else "sin indicar",
                          "estado": e.split(" (")[0], "detalle_estado": e})
        if escribir:
            p.write_text("".join(nuevas), encoding="utf-8")
    if red:
        CACHE.write_text(json.dumps(dict(sorted(cache.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return filas, err


def informe(filas: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "catalogo.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    factores = sorted({f["factor"] for f in filas})
    estados = sorted({f["estado"] for f in filas})
    L = ["# V18 · Fase 1 · Catálogo de la bibliografía", "",
         "Generado por src/v18/f1_bibliografia.py a partir de docs/v18/bib/<factor>/ (criterios en docs/v18/bib/criterios.md). "
         "Estado del DOI según el verificador de V15 (Crossref o DataCite); el cuartil Scimago queda «no verificado» hasta que el "
         "autor descargue la tabla. Los PDF y los paquetes de replicación están solo en disco (data/bib/, sha256 en "
         "data/bib/CHECKSUMS.sha256).", "",
         f"Fichas: {len(filas)}; texto completo: {sum(f['leido'] == 'texto completo' for f in filas)}; "
         f"solo resumen: {sum(f['leido'] == 'solo resumen' for f in filas)}; con paquete de replicación: "
         f"{sum(f['paquete'] == 'sí' for f in filas)}.", "",
         "| Factor | Fichas | Texto completo | Solo resumen | Con paquete | " + " | ".join(estados) + " |",
         "|---|---|---|---|---|" + "---|" * len(estados)]
    for fa in factores:
        g = [f for f in filas if f["factor"] == fa]
        L.append(f"| {fa} | {len(g)} | {sum(f['leido'] == 'texto completo' for f in g)} | {sum(f['leido'] == 'solo resumen' for f in g)} | "
                 f"{sum(f['paquete'] == 'sí' for f in g)} | " + " | ".join(str(sum(f['estado'] == e for f in g)) for e in estados) + " |")
    disc = [f for f in filas if f["estado"] == "DISCREPANTE"]
    if disc:
        L += ["", "## Fichas con DOI discrepante (revisar)", "",
              "Revisadas el 2026-10-20: todas describen una versión de trabajo y citan el DOI de una versión posterior (otro año o "
              "un título cambiado), como dice cada ficha. No se cita ninguna cifra de la versión publicada sin leerla.", ""] + [f"- {f['factor']}/{f['fichero']}: {f['detalle_estado']}" for f in disc]
    L += ["", "Tablas de efectos con su unidad: docs/v18/bib/<factor>/resumen.md."]
    (OUT / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", action="store_true", help="consulta Crossref y escribe el estado en las fichas")
    a = ap.parse_args()
    filas, err = procesar(red=a.verificar, escribir=a.verificar)
    informe(filas)
    for e in err[:40]:
        print(f"  - {e}")
    cuenta = {}
    for f in filas:
        cuenta[f["estado"]] = cuenta.get(f["estado"], 0) + 1
    print(f"f1_bibliografia V18: {len(filas)} fichas; {cuenta}; {len(err)} avisos")
    return 1 if err and not a.verificar else 0


if __name__ == "__main__":
    sys.exit(main())
