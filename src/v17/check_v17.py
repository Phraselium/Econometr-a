"""V17 · Controles de `make check` (plan V17, fase 5). Solo lectura; sin red; no escribe nada.

1. a posteriori: todo fichero de texto de output/v17/ y de docs/v17/{referencias_bde,correcciones}.md declara «a posteriori»
   (un CSV queda rotulado por el informe .md de su carpeta).
2. cifras V17: toda cifra de output/v17/**/hechos.json tiene id V17-*, fuente, capa C4 y lectura V17 (columna propia:
   «OF», «juicio experto», etc.). La lectura V17 nunca va en la capa.
3. sin promoción: ninguna fila de output/v5/cifras_clave.csv con id V17-* tiene capa distinta de C4.
4. lo anterior no cambia: lo comprueban check_v8, check_v9, check_v13 y check_v16, que siguen en make check.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v17"
TEXTO = (".md", ".csv", ".json")
MARCA = "a posteriori"
LECTURAS = {"OF", "hecho", "cota", "asociación", "juicio experto", "juicio experto (calibración)", "no fiable", "no se puede saber", "sin cambio"}


def a_posteriori() -> list[str]:
    err = []
    fich = [p for p in OUT.rglob("*") if p.is_file() and p.suffix in TEXTO]
    fich += [RAIZ / "docs" / "v17" / n for n in ("referencias_bde.md", "correcciones.md") if (RAIZ / "docs" / "v17" / n).exists()]
    for p in fich:
        t = p.read_text(encoding="utf-8", errors="ignore").lower()
        if p.suffix == ".csv" and any(MARCA in m.read_text(encoding="utf-8", errors="ignore").lower()
                                      for m in p.parent.glob("*.md")):
            continue   # una tabla CSV va rotulada por el informe .md de su carpeta
        if MARCA not in t:
            err.append(f"{p.relative_to(RAIZ)}: falta el rótulo «a posteriori»")
    return err


def cifras() -> list[str]:
    err = []
    for p in sorted(OUT.rglob("hechos.json")):
        rel = p.relative_to(RAIZ)
        try:
            filas = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err.append(f"{rel}: JSON inválido ({e})")
            continue
        for h in filas:
            i = str(h.get("id", ""))
            if not i.startswith("V17-"):
                err.append(f"{rel}: id sin prefijo V17-: {i!r}")
            if not h.get("fuentes") and not h.get("fuente"):
                err.append(f"{rel}: {i} sin fuente")
            if h.get("capa") != "C4":
                err.append(f"{rel}: {i} con capa {h.get('capa')!r}: las cifras V17 son C4 (la lectura va en «lectura_v17»)")
            if h.get("lectura_v17") not in LECTURAS:
                err.append(f"{rel}: {i} sin lectura_v17 válida ({sorted(LECTURAS)})")
    return err


def sin_promocion() -> list[str]:
    ck = RAIZ / "output" / "v5" / "cifras_clave.csv"
    if not ck.exists():
        return []
    with ck.open(encoding="utf-8", newline="") as fh:
        return [f"cifras_clave: {r['id']} con capa {r['capa']} (V17 no promueve de capa)"
                for r in csv.DictReader(fh) if r["id"].startswith("V17-") and r["capa"] != "C4"]


def main() -> int:
    total = 0
    for nombre, f in (("a posteriori", a_posteriori), ("cifras V17", cifras), ("sin promoción", sin_promocion)):
        e = f()
        total += len(e)
        print(f"check_v17 · {nombre}: {len(e)} errores")
        for x in e[:30]:
            print(f"  - {x}")
    print(f"check_v17: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
