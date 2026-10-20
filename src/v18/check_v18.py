"""V18 · Controles de `make check` (plan V18, secciones A, B y fase 6). Solo lectura; sin red; no escribe nada.

1. cifras V18: toda cifra de output/v18/**/hechos.json tiene id V18-*, fuente, capa del proyecto (C1-C4, al lado) y
   clasificación V18 (IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE); la capa es C4 (K2).
2. lenguaje causal (K2, decisión del autor): ninguna cifra V18 usa lenguaje causal en su indicador o su nota, tampoco en
   IDENTIFICADO (toda cifra V18 es C4); la fórmula condicional solo va en las secciones técnicas del Documento de Trabajo.
3. plan antes de estimar (B1): todo fichero de src/v18/estimacion/ y output/v18/estimacion/ entró en git después del commit de
   la etiqueta plan-replicacion-v18; sin etiqueta, esas carpetas no pueden tener ficheros.
4. derechos (sección A): ningún PDF versionado en data/bib/ ni en docs/v18/; las citas literales «…» de docs/v18/bib/ tienen 15
   palabras como máximo; cada PDF de data/bib/pdf/ en disco figura en data/bib/CHECKSUMS.sha256 con su sha256.
5. nada anterior cambia y fuga v6: lo comprueban check_v8, check_v9, check_v13, check_v16 y check_v17 (que ya cubre src/v18/).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import etiqueta  # noqa: E402

OUT = RAIZ / "output" / "v18"
CLASES = {"IDENTIFICADO", "SUGESTIVO", "ASOCIACIÓN", "NO CONCLUYENTE", "NO ESTIMABLE"}
CAUSAL = re.compile(r"\b(causa(?:n|do|da|l|les)?|provoc\w*|efecto causal|debido a|gracias a|se debe a|impacto causal)\b", re.I)
CITA = re.compile(r"«([^»]*)»")
MAX_PALABRAS = 15


def _hechos() -> list[tuple[Path, dict]]:
    filas = []
    for p in sorted(OUT.rglob("hechos.json")):
        try:
            filas += [(p, h) for h in json.loads(p.read_text(encoding="utf-8"))]
        except json.JSONDecodeError as e:
            filas.append((p, {"id": f"<JSON inválido: {e}>"}))
    return filas


def cifras() -> list[str]:
    err = []
    for p, h in _hechos():
        rel, i = p.relative_to(RAIZ), str(h.get("id", ""))
        if not i.startswith("V18-"):
            err.append(f"{rel}: id sin prefijo V18-: {i!r}")
        if not h.get("fuentes") and not h.get("fuente"):
            err.append(f"{rel}: {i} sin fuente")
        if h.get("capa") != "C4":
            err.append(f"{rel}: {i} con capa {h.get('capa')!r}: toda cifra V18 es C4 (K2)")
        if h.get("clasificacion_v18") not in CLASES:
            err.append(f"{rel}: {i} sin clasificacion_v18 válida ({sorted(CLASES)})")
    return err


def causal() -> list[str]:
    return [f"{p.relative_to(RAIZ)}: {h.get('id')} ({h.get('clasificacion_v18')}) con lenguaje causal"
            for p, h in _hechos() if CAUSAL.search(f"{h.get('indicador', '')} {h.get('nota', '')}")]


def _primer_commit(p: Path) -> str | None:
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--", str(p.relative_to(RAIZ))],
                       cwd=RAIZ, capture_output=True, text=True)
    lineas = r.stdout.split()
    return lineas[-1] if lineas else None


def plan_antes() -> list[str]:
    fich = [p for d in (RAIZ / "src" / "v18" / "estimacion", OUT / "estimacion") if d.exists()
            for p in sorted(d.rglob("*")) if p.is_file() and "__pycache__" not in p.parts]
    if not fich:
        return []
    if not etiqueta.commit_etiqueta():
        return [f"{p.relative_to(RAIZ)}: estimación sin la etiqueta {etiqueta.ETIQUETA} (plan V18, B1)" for p in fich]
    err = []
    for p in fich:
        c = _primer_commit(p)
        if c and not etiqueta.es_posterior(c):
            err.append(f"{p.relative_to(RAIZ)}: entró en git ({c[:7]}) antes de {etiqueta.ETIQUETA}")
    return err


def derechos() -> list[str]:
    err = []
    r = subprocess.run(["git", "ls-files", "data/bib", "docs/v18"], cwd=RAIZ, capture_output=True, text=True)
    err += [f"{f}: PDF versionado (solo ficha, enlace, DOI y licencia)" for f in r.stdout.split() if f.lower().endswith(".pdf")]
    for p in sorted((RAIZ / "docs" / "v18" / "bib").rglob("*.md")):
        for c in CITA.findall(p.read_text(encoding="utf-8")):
            if len(c.split()) > MAX_PALABRAS:
                err.append(f"{p.relative_to(RAIZ)}: cita de {len(c.split())} palabras (máximo {MAX_PALABRAS}): «{c[:40]}…»")
    ck = RAIZ / "data" / "bib" / "CHECKSUMS.sha256"
    sumas = {}
    if ck.exists():
        for linea in ck.read_text(encoding="utf-8").splitlines():
            if linea.strip():
                h, _, f = linea.partition("  ")
                sumas[f.strip()] = h.strip()
    for p in sorted((RAIZ / "data" / "bib" / "pdf").glob("*.pdf")) if (RAIZ / "data" / "bib" / "pdf").exists() else []:
        rel = str(p.relative_to(RAIZ))
        if rel not in sumas:
            err.append(f"{rel}: sin sha256 en data/bib/CHECKSUMS.sha256")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != sumas[rel]:
            err.append(f"{rel}: sha256 distinto del registrado")
    return err


def main() -> int:
    total = 0
    for nombre, f in (("cifras V18", cifras), ("lenguaje causal", causal), ("plan antes de estimar", plan_antes),
                      ("derechos", derechos)):
        e = f()
        total += len(e)
        print(f"check_v18 · {nombre}: {len(e)} errores")
        for x in e[:30]:
            print(f"  - {x}")
    ok, motivo = etiqueta.puerta()
    print(f"check_v18 · puerta del plan de replicación: {'abierta' if ok else 'cerrada'} ({motivo})")
    print(f"check_v18: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
