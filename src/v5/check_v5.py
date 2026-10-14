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

import csv
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
LIBRE = [r"\bv\d+(?:\.\d+)+\b", r"`[^`]*`", r"\]\([^)]*\)", r"https?://\S+", r"\b(?:19|20)\d{2}(?:T[1-4]|-\d{2})?\b", r"\b[CEABDR]\d{1,2}\b",
         r"\b(?:BK|S|V|H|I|N|M|P)\d{1,3}(?:-\d+)?\b", r"^\s*\d+[.)]\s", r"^#+.*$", r"\b\d{1,2}:\d{2}\b", r"\bv\d\b",
         r"\b(?:Q[1-4]|ODS ?\d+)\b", r"<!--.*?-->", r"\bLey \d+/\d{4}\b", r"\b\d{1,2} de \w+\b", r"\(\d+\)",
         r"\$[^$]+\$",   # v7.1: fórmulas LaTeX en línea (parámetros y notación, no cifras difundibles)
         r"\bI\(\d\)", r"\b17\b"]   # v7.1: orden de integración, etiquetas de versión y número de CCAA (constante)


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
    mal = ck[~ck.capa.astype(str).str.match(r"^C[1-4]s?\b")]
    err += [f"cifras_clave: {r.id} capa inválida {r.capa!r}" for r in mal.itertuples()]
    return err


SUMAS_REQUERIDAS = ("A4", "B1", "B2", "D2")   # módulos con tablas provinciales declaradas
SUMAS_REQUERIDAS_V51 = ("T1", "T2", "T3", "T4")
OUT51 = RAIZ / "output" / "v5_1"


def sumas() -> list[str]:
    err = [f"falta output/v5/{m}/control_sumas.json (suma provincial = nacional)" for m in SUMAS_REQUERIDAS
           if (OUT / m).is_dir() and not (OUT / m / "control_sumas.json").exists()]
    err += [f"falta output/v5_1/{m}/control_sumas.json (suma provincial = nacional)" for m in SUMAS_REQUERIDAS_V51
            if (OUT51 / m).is_dir() and not (OUT51 / m / "control_sumas.json").exists()]
    for p in sorted(OUT.glob("*/control_sumas.json")) + sorted(OUT51.glob("*/control_sumas.json")):
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
        nc = sub[~sub.direccion.astype(str).str.startswith("a favor") & ~sub.doc_id.isin(normas)].doc_id.nunique()
        if nf != x.n_documentos_a_favor:
            err.append(f"A5: {x.instrumento}: recuento a favor {x.n_documentos_a_favor} ≠ {nf} documentos oficiales")
        if "n_documentos_en_contra" in rec and nc < x.n_documentos_en_contra:
            err.append(f"A5: {x.instrumento}: recuento en contra {x.n_documentos_en_contra} > {nc} documentos oficiales")
    return err


# lecturas con caché versionada: el script solo abre el fichero si falta la caché
EXENTOS = {("src/v3/c1_geo.py", "Cartografia_secc.zip"): "caché versionada output/v3/C1/centroides.csv"}


def retirados_con_descarga() -> set[str]:
    """V8.1 C: nombres de ficheros retirados del índice por licencia (data/raw, en .gitignore) que están en
    data/CHECKSUMS.sha256 y tienen script de descarga en docs/v8_1/inventario_licencias.csv. Se aceptan como lectura
    legítima: `make datos_terceros` los regenera y verifica su sha256."""
    inv, ck = RAIZ / "docs/v8_1/inventario_licencias.csv", RAIZ / "data/CHECKSUMS.sha256"
    if not inv.exists() or not ck.exists():
        return set()
    en_ck = {l.split("  ", 1)[1].strip() for l in ck.read_text(encoding="utf-8").splitlines() if "  " in l}
    out = set()
    with inv.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            scr = r["script_descarga"].split(";")[0]
            if r["estado"].startswith("no claramente") and scr.startswith("src/") and r["fichero"] in en_ck:
                out.add(Path(r["fichero"]).name)
    return out


# V8.1 Z5: retirado por decisión del autor sin script de descarga (transcripción manual, aplazada a la fase de propuestas);
# lo leen v4 M5 y v5 A5, cuyas salidas siguen versionadas; `make datos_terceros` solo verifica su sha256 si existe.
RETIRADOS_MANUALES = {"medidas_programas.csv": "docs/v8_1/datos_retirados.md (copia local del autor)"}


def lecturas_no_versionadas() -> list[str]:
    vers = set(subprocess.run(["git", "ls-files", "data/raw"], cwd=RAIZ, capture_output=True, text=True).stdout.split())
    nombres = {Path(v).name for v in vers} | retirados_con_descarga() | set(RETIRADOS_MANUALES)
    err = []
    scripts = [p for p in RAIZ.joinpath("src").rglob("*.py") if not re.match(r"(fetch_|.*_fetch\.py$|extract_|check_v5)", p.name)]
    for p in scripts:
        for m in re.finditer(r"[\"']([A-Za-z0-9_./-]+\.(?:csv|csv\.gz|json|parquet|xlsx|xls|zip))[\"']", p.read_text()):
            n = Path(m.group(1)).name
            enraw = any(RAIZ.joinpath("data/raw").rglob(n)) if n not in nombres else True
            if enraw and n not in nombres and not n.startswith("_") and (str(p.relative_to(RAIZ)), n) not in EXENTOS:
                err.append(f"{p.relative_to(RAIZ)}: lee data/raw/…/{n}, no versionado")
    return sorted(set(err))


def liberadas_no_restadas() -> list[str]:
    """v5.1: la necesidad nunca resta las viviendas liberadas por envejecimiento (ya descontadas en la proyección del INE)."""
    err = []
    for p in sorted(OUT51.glob("*/control_liberadas.json")):
        for c in json.loads(p.read_text()):
            if abs(c["necesidad"] - c["suma_componentes_sin_L"]) > 1e-6 * max(1.0, abs(c["necesidad"])):
                err.append(f"{p.relative_to(RAIZ)}: {c.get('tabla', '')}: la necesidad ({c['necesidad']}) no es la suma sin L ({c['suma_componentes_sin_L']})")
    for p in list(OUT.rglob("*.md")) + list(PLANT.rglob("*.md")):
        for i, l in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"(menos|restar|restando|descontar|descontando)\s+(las\s+)?(viviendas\s+)?liberadas", l, re.I) and not re.search(r"\bno\b|nunca|ya (las )?descuenta|contaría dos veces|doble", l, re.I):
                err.append(f"{p.relative_to(RAIZ)}:{i}: parece restar las liberadas de la necesidad")
    return err


def topes_c3() -> list[str]:
    err = []
    for p in sorted(OUT.rglob("*.json")):
        try:
            d = json.loads(p.read_text())
        except ValueError:
            continue
        for f in d if isinstance(d, list) else [d]:
            if isinstance(f, dict) and re.search(r"\btopes?\b", json.dumps(f, ensure_ascii=False), re.I) and str(f.get("capa", "")).startswith("C3"):
                err.append(f"{p.relative_to(RAIZ)}: topes con capa C3")
    for p in list(OUT.rglob("*.md")) + list(PLANT.rglob("*.md")):
        for i, l in enumerate(p.read_text().splitlines(), 1):
            if re.search(r"\btopes?\b", l, re.I) and re.search(r"\bC3\b", l) and not re.search(r"(fuera de|no es|sin|ning[uú]n[ao]?|nunca)\b.*C3|(fuera de|no es|sin) C3", l, re.I):
                err.append(f"{p.relative_to(RAIZ)}:{i}: topes etiquetados como C3")
    return err


def main() -> int:
    err = plantillas() + cifras() + sumas() + recuentos() + lecturas_no_versionadas() + topes_c3() + liberadas_no_restadas()
    for e in err:
        print(e)
    print(f"check_v5: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
