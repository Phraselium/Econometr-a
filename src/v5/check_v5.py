"""Comprobaciones de puerta v5 (entran en `make check`). Sin red.

1. Plantillas de entregables (docs/v5/plantillas): toda cifra procede de un marcador {{id}} de
   output/v5/cifras_clave.csv; no quedan marcadores sin resolver en output/v5.
2. cifras_clave.csv: cada fila tiene capa válida, periodo, cobertura, fuentes y fecha del dato.
3. Suma provincial = nacional: output/v5/*/control_sumas.json [{tabla, suma_provincial, nacional, tolerancia_rel}].
4. Recuentos de programas (A5): solo documentos oficiales.
5. Ningún script de `make all` lee ficheros de data/raw no versionados (nombres literales; se excluyen fetch_*).
6. Ningún texto v5 asocia los topes al alquiler a C3 (A6).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v5"
PLANT = RAIZ / "docs" / "v5" / "plantillas"
MARC = re.compile(r"\{\{[^}]+\}\}")
# cifras permitidas fuera de marcadores: años, capas, numeración, rutas, identificadores y horas de guion
LIBRE = [r"`[^`]*`", r"\]\([^)]*\)", r"https?://\S+", r"\b(?:19|20)\d{2}(?:T[1-4]|-\d{2})?\b", r"\b[CEABDR]\d{1,2}\b",
         r"\b(?:BK|S|V|H|I|N|M|P)\d{1,3}(?:-\d+)?\b", r"^\s*\d+[.)]\s", r"^#+.*$", r"\b\d{1,2}:\d{2}\b", r"\bv\d\b",
         r"\b(?:Q[1-4]|ODS ?\d+)\b", r"<!--.*?-->", r"\bLey \d+/\d{4}\b", r"\b\d{1,2} de \w+\b", r"\(\d+\)"]


def _sin_libres(linea: str) -> str:
    for p in LIBRE:
        linea = re.sub(p, " ", linea)
    return linea


def plantillas() -> list[str]:
    err = []
    for p in sorted(PLANT.rglob("*.md")):
        for i, l in enumerate(p.read_text().splitlines(), 1):
            if "check:cifra-libre" in l:
                continue
            resto = _sin_libres(MARC.sub(" ", l))
            if re.search(r"\d", resto):
                err.append(f"{p.relative_to(RAIZ)}:{i}: cifra fuera de cifras_clave: «{l.strip()[:90]}»")
    for p in sorted(OUT.rglob("*.md")):
        if MARC.search(p.read_text()):
            err.append(f"{p.relative_to(RAIZ)}: marcador sin resolver")
    return err


def cifras() -> list[str]:
    f = OUT / "cifras_clave.csv"
    if not f.exists():
        return [] if not any(PLANT.rglob("*.md")) else ["falta output/v5/cifras_clave.csv"]
    ck = pd.read_csv(f)
    err = []
    if ck.id.duplicated().any():
        err.append(f"cifras_clave: ids duplicados {ck.id[ck.id.duplicated()].tolist()}")
    for c in ("capa", "periodo", "cobertura", "fuentes", "fecha_dato"):
        mal = ck[ck[c].isna() | (ck[c].astype(str).str.strip() == "")]
        err += [f"cifras_clave: {r.id} sin «{c}»" for r in mal.itertuples()]
    mal = ck[~ck.capa.astype(str).str.match(r"^C[1-4]\b")]
    err += [f"cifras_clave: {r.id} capa inválida {r.capa!r}" for r in mal.itertuples()]
    return err


def sumas() -> list[str]:
    err = []
    for p in sorted(OUT.glob("*/control_sumas.json")):
        for c in json.loads(p.read_text()):
            tol = c.get("tolerancia_rel", 1e-6)
            if abs(c["suma_provincial"] - c["nacional"]) > tol * max(1.0, abs(c["nacional"])):
                err.append(f"{p.relative_to(RAIZ)}: {c['tabla']}: suma provincial {c['suma_provincial']} ≠ nacional {c['nacional']}")
    return err


def recuentos() -> list[str]:
    m, r = OUT / "A5" / "medidas_programas_v5.csv", OUT / "A5" / "recuentos.csv"
    if not (m.exists() and r.exists()):
        return []
    med, rec = pd.read_csv(m), pd.read_csv(r)
    of = med[med.oficial.astype(str).str.lower().isin(["sí", "si", "true", "1"])]
    err = []
    for x in rec.itertuples():
        sub = of[of.instrumento == x.instrumento]
        normas = set(str(x.normas_con_coincidencia).split(";")) if "normas_con_coincidencia" in rec else set()
        nf = sub[sub.direccion.astype(str).str.startswith("a favor") & ~sub.doc_id.isin(normas)].doc_id.nunique()
        if nf != x.n_documentos_a_favor:
            err.append(f"A5: {x.instrumento}: recuento a favor {x.n_documentos_a_favor} ≠ {nf} documentos oficiales")
    return err


# lecturas con caché versionada: el script solo abre el fichero si falta la caché
EXENTOS = {("src/v3/c1_geo.py", "Cartografia_secc.zip"): "caché versionada output/v3/C1/centroides.csv"}


def lecturas_no_versionadas() -> list[str]:
    vers = set(subprocess.run(["git", "ls-files", "data/raw"], cwd=RAIZ, capture_output=True, text=True).stdout.split())
    nombres = {Path(v).name for v in vers}
    err = []
    scripts = [p for p in RAIZ.joinpath("src").rglob("*.py") if not re.match(r"(fetch_|.*_fetch\.py$|extract_|check_v5)", p.name)]
    for p in scripts:
        for m in re.finditer(r"[\"']([A-Za-z0-9_./-]+\.(?:csv|csv\.gz|json|parquet|xlsx|xls|zip))[\"']", p.read_text()):
            n = Path(m.group(1)).name
            enraw = any(RAIZ.joinpath("data/raw").rglob(n)) if n not in nombres else True
            if enraw and n not in nombres and not n.startswith("_") and (str(p.relative_to(RAIZ)), n) not in EXENTOS:
                err.append(f"{p.relative_to(RAIZ)}: lee data/raw/…/{n}, no versionado")
    return sorted(set(err))


def topes_c3() -> list[str]:
    err = []
    for p in list(OUT.rglob("*.md")) + list(PLANT.rglob("*.md")):
        for i, l in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"\btopes?\b", l, re.I) and "[C3]" in l:
                err.append(f"{p.relative_to(RAIZ)}:{i}: topes etiquetados como C3")
    return err


def main() -> int:
    err = plantillas() + cifras() + sumas() + recuentos() + lecturas_no_versionadas() + topes_c3()
    for e in err:
        print(e)
    print(f"check_v5: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
