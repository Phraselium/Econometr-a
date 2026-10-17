"""V16-F5 · Reúne la validación por Monte Carlo de las herramientas de V16 (docs/v16/plan.md, fase 5).

Lee output/v16/montecarlo/<herramienta>/resultado.json y docs/v16/validacion_montecarlo/<herramienta>.md, y escribe:
- docs/v16/validacion_montecarlo.md (publicado como metodologia/validacion_montecarlo_v16.md con `make publicacion`): tabla de
  veredictos y, debajo, la sección de cada herramienta;
- output/v16/montecarlo/veredictos.csv: herramienta, tamaño, cobertura, veredicto, inferencia que se puede usar en la fase 6.
Criterio (adenda del pre-registro V16, punto 11): tamaño al 5 % en [0,04; 0,06] con R ≥ 2.000 y cobertura al 95 % en [0,92; 0,97].
La fase 6 solo usa una herramienta con veredicto APTO o «alternativa APTA» (y entonces con esa inferencia). Sin red; determinista.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
MC = RAIZ / "output" / "v16" / "montecarlo"
SECC = RAIZ / "docs" / "v16" / "validacion_montecarlo"
SAL = RAIZ / "docs" / "v16" / "validacion_montecarlo.md"
TAB = MC / "veredictos.csv"


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _veredicto(d: dict) -> dict:
    g = d.get("diagnosticos") or {}
    def buscar(*claves):
        for k in claves:
            for fuente in (g, d):
                if k in fuente and fuente[k] not in (None, ""):
                    return fuente[k]
        return None
    return {"tamano": _num(buscar("tamano_5pct", "tamano", "size_5pct", "rechazo_nulo_5pct")),
            "cobertura": _num(buscar("cobertura_95", "cobertura", "coverage_95")),
            "replicas": buscar("R", "replicas", "R_nulo"),
            "veredicto": str(buscar("veredicto", "verdict") or d.get("nivel_evidencia") or "sin veredicto"),
            "inferencia_valida": str(buscar("inferencia_valida", "inferencia_apta", "inferencia") or "")}


def main() -> int:
    filas = []
    for r in sorted(MC.glob("*/resultado.json")):
        d = json.loads(r.read_text(encoding="utf-8"))
        v = _veredicto(d)
        filas.append({"herramienta": r.parent.name, **v})
    if not filas:
        print("f5_validacion: sin resultados de Monte Carlo todavía")
        return 0
    MC.mkdir(parents=True, exist_ok=True)
    with TAB.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["herramienta", "tamano", "cobertura", "replicas", "veredicto", "inferencia_valida"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    f = (lambda x: "" if x is None else f"{x:.3f}".replace(".", ","))
    L = ["# V16 · Validación de herramientas por Monte Carlo (fase 5)", "",
         "Generado por `python3 src/v16/f5_validacion.py`. Cada herramienta se valida con un proceso generador que reproduce la estructura de los "
         "datos de entrenamiento de V16 (unidades, periodos, clusters, calendario de tratamiento, distancias) con resultados SIMULADOS: ningún "
         "dato real de resultado ni ninguna muestra sellada. Criterio (adenda del pre-registro, punto 11): tamaño al 5 % en [0,04; 0,06] con "
         "R ≥ 2.000 réplicas y cobertura al 95 % en [0,92; 0,97]. Una herramienta NO APTA no se usa en la fase 6 (su diseño queda descriptivo).", "",
         "| Herramienta | Tamaño al 5 % | Cobertura al 95 % | Réplicas | Veredicto | Inferencia utilizable |", "|---|---|---|---|---|---|"]
    for x in filas:
        L.append(f"| {x['herramienta']} | {f(x['tamano'])} | {f(x['cobertura'])} | {x['replicas'] or ''} | {x['veredicto']} | {x['inferencia_valida']} |")
    L.append("")
    for x in filas:
        s = SECC / f"{x['herramienta']}.md"
        if s.exists():
            L += [s.read_text(encoding="utf-8").rstrip(), ""]
    SAL.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f5_validacion: {len(filas)} herramientas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
