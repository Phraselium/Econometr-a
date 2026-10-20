"""V18 · Fase 6 · Cifras V18 difundibles para cifras_clave.

Reúne en output/v18/f6/hechos.json las cifras V18 de output/v18/estimacion/*/hechos.json y de output/v18/f5/hechos.json (570).
src/v5/cifras_clave.py lee solo este fichero de V18 (como output/v17/f5/hechos.json en V17).
Comprueba, y sale con código 1 si algo falla: ids únicos con prefijo V18-, fuente, capa C4, clasificacion_v18 válida y ninguna
palabra causal en el indicador ni en la nota (K2; mismas expresiones que check_v18). Añade:
- tipo_rango coherente con min y max: «rango» si min <= valor <= max (o falta el valor central y min <= max), «referencias» si
  min y max existen pero no encierran el valor, «sin rango» si falta alguno;
- cobertura real: el territorio de la cifra. Las coberturas que solo describen la muestra («N = 234», «4 ramas», «sin datos»,
  «—», el número de estudios de B5…) se sustituyen por el territorio del diseño, con la descripción original entre paréntesis;
- fecha_dato (último año del periodo) y ficha (el hechos.json de origen).
Determinista; sin red; solo lee output/v18. Uso: python3 src/v18/f6_hechos.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import check_v18  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"   # solo lee salidas V18 ya generadas (guarda de fuga v6 de check_v17)
OUT = RAIZ / "output" / "v18"
SALIDA = OUT / "f6" / "hechos.json"
FECHA = "2026-10-20"
N_ESPERADO = 570
TIPOS_RANGO = ("rango", "referencias", "sin rango")

# Territorio del diseño de cada estimación (docs/v18/plan_replicacion.md), para las coberturas que solo describen la muestra.
TERRITORIO = {
    "E1-A2": "Málaga y Sevilla (municipios)", "E1-X1": "Barcelona (barrios)", "E1": "ciudades españolas con registro de viviendas turísticas",
    "E2": "Cataluña (municipios)", "E3": "España (provincias)", "E4": "España", "E5": "España (provincias)",
    "E6-A2": "España sin la provincia de València (secciones)", "E6": "España (provincias)", "E7": "España",
    "E8": "España (comunidades autónomas)", "E9": "España", "E10": "España (municipios)", "E11": "España",
    "E12": "España (provincias)", "F1": "España", "F2": "España", "F3": "España", "F4": "España",
}
TERR = re.compile(r"nacional|españa|provincia|municipi|secci|barrio|ccaa|comunidad|país|orígen|origen|barcelona|cataluña|"
                  r"valència|andaluc|castilla|galicia|extremadura|vasco|distrit|controles|tratados|ciudad", re.I)


def tipo_rango(h: dict) -> str:
    mn, mx, v = h.get("min"), h.get("max"), h.get("valor")
    if mn is None or mx is None:
        return "sin rango"
    if mn > mx:
        return "referencias"
    if v is None or mn - 1e-12 <= v <= mx + 1e-12:
        return "rango"
    return "referencias"


def _paises_b5() -> dict[str, str]:
    """Países de los estudios que entran en la magnitud preferida de cada factor (output/v18/f5/magnitudes_estudios.csv)."""
    p = OUT / "f5" / "magnitudes_estudios.csv"
    res: dict[str, list[str]] = {}
    if p.exists():
        with p.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("entra_en_B5") == "sí" and r.get("pais"):
                    for x in re.split(r"\s*[;,/]\s*", r["pais"]):
                        if x and x not in res.setdefault(r["factor"], []):
                            res[r["factor"]].append(x)
    return {f: ", ".join(v) for f, v in res.items()}


def cobertura_real(h: dict, paises: dict[str, str]) -> str:
    c = re.sub(r"[;\s]+$", "", str(h.get("cobertura") or "").strip())
    i = str(h["id"])
    m = re.match(r"V18-B5-(E\d+)", i)
    if m:   # B5: magnitud de la literatura y, en su caso, estimación propia; la cobertura es la de los estudios
        terr = f"estudios de {paises[m.group(1)]}" if m.group(1) in paises else "literatura sin estudios con error típico en la unidad"
        return f"{terr} ({c})" if c else terr
    if c and TERR.search(c):
        return c
    e = re.match(r"V18-((?:E|F)\d+)(?:-([A-Z]+\d+))?", i)
    terr = "España"
    if e:
        terr = TERRITORIO.get(f"{e.group(1)}-{e.group(2)}", TERRITORIO.get(e.group(1), "España"))
    if not c or c in ("—", "-", "no estimada"):
        return f"{terr} (no estimada)"
    if c.startswith(("sin ", "no ")):
        return f"{terr} (no estimada: {c})"
    return f"{terr} ({c})"


def fuentes_hechos() -> list[Path]:
    return sorted((OUT / "estimacion").glob("*/hechos.json")) + [OUT / "f5" / "hechos.json"]


def consolidar() -> tuple[list[dict], list[str]]:
    filas, err = [], []
    paises = _paises_b5()
    for p in fuentes_hechos():
        rel = str(p.relative_to(RAIZ))
        for h in json.loads(p.read_text(encoding="utf-8")):
            h = dict(h)
            h.setdefault("ficha", rel)
            filas.append(h)
    vistos: set[str] = set()
    for h in filas:
        i = str(h.get("id", ""))
        if i in vistos:
            err.append(f"id repetido: {i}")
        vistos.add(i)
        if not i.startswith("V18-"):
            err.append(f"{i}: sin prefijo V18-")
        if not h.get("fuentes"):
            err.append(f"{i}: sin fuentes")
        if h.get("capa") != "C4":
            err.append(f"{i}: capa {h.get('capa')!r} (toda cifra V18 es C4, K2)")
        if h.get("clasificacion_v18") not in check_v18.CLASES:
            err.append(f"{i}: clasificacion_v18 no válida ({h.get('clasificacion_v18')!r})")
        if check_v18.CAUSAL.search(f"{h.get('indicador', '')} {h.get('nota', '')}"):
            err.append(f"{i}: lenguaje causal en el indicador o la nota (K2)")
    if len(filas) != N_ESPERADO:
        err.append(f"se esperaban {N_ESPERADO} cifras V18 y hay {len(filas)}")
    for h in filas:
        if isinstance(h.get("fuentes"), str):
            h["fuentes"] = [h["fuentes"]]
        h["tipo_rango"] = tipo_rango(h)
        h["cobertura"] = cobertura_real(h, paises)
        if not h.get("fecha_dato"):
            anios = re.findall(r"(?:19|20)\d\d", str(h.get("periodo", "")))
            h["fecha_dato"] = anios[-1] if anios else FECHA
        assert h["tipo_rango"] in TIPOS_RANGO and h["cobertura"] and "véase" not in h["cobertura"]
    return filas, err


def main() -> int:
    filas, err = consolidar()
    if err:
        print(f"f6_hechos V18: {len(err)} errores")
        for x in err[:40]:
            print("  -", x)
        return 1
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(filas, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_cifra = sum(any(h.get(k) is not None for k in ("valor", "min", "max")) for h in filas)
    tipos = {t: sum(h["tipo_rango"] == t for h in filas) for t in TIPOS_RANGO}
    (SALIDA.parent / "informe.md").write_text(
        "# V18 · Fase 6 · Cifras V18 para cifras_clave\n\n"
        "**análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Generado por src/v18/f6_hechos.py: "
        f"{len(filas)} cifras V18 (todas C4, con su clasificacion_v18 al lado) de {len(fuentes_hechos())} ficheros. "
        f"{n_cifra} tienen valor, mínimo o máximo y entran en output/v5/cifras_clave.csv; el resto (sin ninguna cifra) no entra. "
        f"Tipo de rango: {tipos['rango']} rango, {tipos['referencias']} referencias, {tipos['sin rango']} sin rango.\n",
        encoding="utf-8")
    print(f"f6_hechos V18: {len(filas)} cifras ({n_cifra} con cifra) -> {SALIDA.relative_to(RAIZ)}; tipos {tipos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
