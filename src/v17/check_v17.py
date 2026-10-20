"""V17 · Controles de `make check` (plan V17, fase 5). Solo lectura; sin red; no escribe nada.

1. a posteriori: todo fichero de texto de output/v17/ y de docs/v17/{referencias_bde,correcciones}.md declara «a posteriori»
   (un CSV queda rotulado por el informe .md de su carpeta).
2. cifras V17: toda cifra de output/v17/**/hechos.json tiene id V17-*, fuente, capa C4 y lectura V17 (columna propia:
   «OF», «juicio experto», etc.), tipo_rango (rango, referencias o sin rango) y cobertura real. La lectura V17 nunca va en la capa.
3. sin promoción: ninguna fila de output/v5/cifras_clave.csv con id V17-* tiene capa distinta de C4.
4. lo anterior no cambia: lo comprueban check_v8, check_v9, check_v13 y check_v16, que siguen en make check.
5. fuga v6 (decisión del autor del 2026-10-20; incidente K4): todo script de src/v17/ o posterior que lea datos (data/raw,
   data/processed o la base) debe excluir las unidades de los bloques sellados de v6 con holdout.excluir_sellados_v6(), que
   cubre las ocho CCAA de K8 y sus provincias, municipios, distritos y secciones, o declarar
   ALCANCE_TERRITORIAL = "nacional" (solo series nacionales), "sin lectura de datos" o "reproduce publicado" (solo lee a
   través de los cargadores de la versión publicada que reproduce, sin muestra nueva). El filtro muestra_sellada_v6 de la
   base no basta: no marca las filas de CCAA. Los cargadores importados de versiones anteriores quedan cubiertos por
   check_v15 («lecturas v6»).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v17"
TEXTO = (".md", ".csv", ".json")
MARCA = "a posteriori"
TIPOS_RANGO = {"rango", "referencias", "sin rango"}
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
            if h.get("tipo_rango") not in TIPOS_RANGO:   # decisión del autor del 2026-10-20
                err.append(f"{rel}: {i} sin tipo_rango válido ({sorted(TIPOS_RANGO)})")
            if not h.get("cobertura") or "véase" in str(h.get("cobertura")):
                err.append(f"{rel}: {i} sin cobertura real")
    return err


def sin_promocion() -> list[str]:
    ck = RAIZ / "output" / "v5" / "cifras_clave.csv"
    if not ck.exists():
        return []
    with ck.open(encoding="utf-8", newline="") as fh:
        return [f"cifras_clave: {r['id']} con capa {r['capa']} (V17 no promueve de capa)"
                for r in csv.DictReader(fh) if r["id"].startswith("V17-") and r["capa"] != "C4"]


LEE_DATOS = re.compile(r'data/(raw|processed|base)|"data"\s*/\s*"(raw|processed|base)"|HECHOS_BASE|territorios\.parquet')
EXENTOS_FUGA = {"check_v17.py", "fase.py", "registro_subagentes.py"}
DECLARACION = re.compile(r'^ALCANCE_TERRITORIAL\s*=\s*"(nacional|sin lectura de datos|reproduce publicado)"', re.M)


def fuga_v6_texto(texto: str) -> bool:
    """True si el texto de un script incumple la guarda de fuga v6."""
    if not LEE_DATOS.search(texto):
        return False
    # V18: sellado.filtrar (src/v18/sellado.py) aplica holdout.excluir_sellados_v6 más las exclusiones de V15/V16 y el tope temporal
    return "excluir_sellados_v6(" not in texto and "sellado.filtrar(" not in texto and not DECLARACION.search(texto)


def fuga_v6() -> list[str]:
    err = []
    for v in sorted(p for p in (RAIZ / "src").glob("v*") if p.is_dir() and p.name[1:].isdigit() and int(p.name[1:]) >= 17):
        for p in sorted(v.rglob("*.py")):
            if p.name in EXENTOS_FUGA:
                continue
            if fuga_v6_texto(p.read_text(encoding="utf-8")):
                err.append(f"{p.relative_to(RAIZ)}: lee datos sin holdout.excluir_sellados_v6() ni ALCANCE_TERRITORIAL declarado")
    return err


def main() -> int:
    total = 0
    for nombre, f in (("a posteriori", a_posteriori), ("cifras V17", cifras), ("sin promoción", sin_promocion),
                      ("fuga v6", fuga_v6)):
        e = f()
        total += len(e)
        print(f"check_v17 · {nombre}: {len(e)} errores")
        for x in e[:30]:
            print(f"  - {x}")
    print(f"check_v17: {total} errores")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
