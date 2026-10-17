"""Utilidades comunes del grupo «series» de la fase 5 de V16 (validación Monte Carlo).

Criterio de la adenda (puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000
réplicas bajo el nulo y, cuando hay IC, cobertura en [0,92; 0,97]. Un tamaño de 0,0 es NO APTO.
Nunca se leen datos reales de resultados ni la muestra sellada.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
SEED = 20261010
MARCA = "<!-- RESULTADOS -->"
TAM_MIN, TAM_MAX = 0.04, 0.06
COB_MIN, COB_MAX = 0.92, 0.97
R_MIN = 2000


def rng(k: int, sub: int = 0) -> np.random.Generator:
    return np.random.default_rng([SEED, k, sub])


def ic_binomial(p: float, n: int) -> list[float]:
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(max(p - e, 0.0), 4), round(min(p + e, 1.0), 4)]


def veredicto(tamano: float, n_rep: int, cobertura: float | None = None) -> dict:
    """Aplica los umbrales de la adenda. Devuelve veredicto y condiciones que fallan."""
    fallos = []
    if n_rep < R_MIN:
        fallos.append(f"R={n_rep} < {R_MIN}")
    if tamano == 0.0:
        fallos.append("tamaño 0,0 (conservador extremo)")
    elif not (TAM_MIN <= tamano <= TAM_MAX):
        fallos.append(f"tamaño {tamano:.4f} fuera de [{TAM_MIN}; {TAM_MAX}]")
    if cobertura is not None and not (COB_MIN <= cobertura <= COB_MAX):
        fallos.append(f"cobertura {cobertura:.4f} fuera de [{COB_MIN}; {COB_MAX}]")
    return {"veredicto": "APTO" if not fallos else "NO APTO", "fallos": fallos}


def paralelo(f, tareas, n_jobs: int = 4):
    from joblib import Parallel, delayed
    return Parallel(n_jobs=n_jobs)(delayed(f)(*t) for t in tareas)


def escribir_salidas(herramienta: str, resultado: dict, tabla, md_resultados: str) -> Path:
    out = RAIZ / "output" / "v16" / "montecarlo" / herramienta
    out.mkdir(parents=True, exist_ok=True)
    (out / "resultado.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8")
    tabla.to_csv(out / "tabla.csv", index=False)
    md = RAIZ / "docs" / "v16" / "validacion_montecarlo" / f"{herramienta}.md"
    previo = md.read_text(encoding="utf-8") if md.exists() else f"# {herramienta}\n\n"
    cabeza = previo.split(MARCA)[0]
    md.write_text(cabeza + MARCA + "\n" + md_resultados.strip() + "\n", encoding="utf-8")
    return out


def resultado_base(herramienta: str, pregunta: str, N, metodo: str) -> dict:
    return {
        "rama": "r16/montecarlo", "pregunta": pregunta, "capa": "validación de herramienta (sin capa de evidencia)",
        "datos": "simulados; estructura (N, T) de la pregunta; ningún valor real de resultados",
        "N": N, "metodo": metodo, "estimacion": {}, "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "no aplica (validación Monte Carlo)", "diagnosticos": {},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": [],
    }
