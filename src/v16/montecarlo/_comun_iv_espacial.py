"""Utilidades comunes del grupo «iv_espacial» de la fase 5 de V16 (validación Monte Carlo).

Criterio (adenda de V16, puntos 3 y 11): tamaño al 5 % en [0,04; 0,06] con R >= 2.000 réplicas bajo el nulo y
cobertura del IC 95 % en [0,92; 0,97] bajo una alternativa. Un tamaño de 0,0 es NO APTO.
Nunca se leen valores reales de resultados ni la muestra sellada: solo estructura (unidades, periodos, clusters, geometría).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
SEED = 20261010
MARCA = "<!-- RESULTADOS -->"
TAM_MIN, TAM_MAX = 0.04, 0.06
COB_MIN, COB_MAX = 0.92, 0.97
R_MIN = 2000
ENT = RAIZ / "data" / "processed" / "v16" / "entrenamiento"


def rng(k: int, sub: int = 0) -> np.random.Generator:
    return np.random.default_rng([SEED, k, sub])


def ic_binomial(p: float, n: int) -> list[float]:
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(float(max(p - e, 0.0)), 4), round(float(min(p + e, 1.0)), 4)]


def veredicto(tamano: float, n_rep: int, cobertura: float | None = None) -> dict:
    """Umbrales de la adenda. Devuelve veredicto y condiciones que fallan."""
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


def trozos(R: int, n: int = 40) -> list[int]:
    """Reparto fijo de R réplicas en n trozos (independiente del número de procesos: determinismo)."""
    base, extra = divmod(R, n)
    return [base + (1 if i < extra else 0) for i in range(n) if base + (1 if i < extra else 0) > 0]


def paralelo(f, k: int, R: int, n_jobs: int = 4, n_trozos: int = 40, **kw) -> np.ndarray:
    """Ejecuta f(rng, n_rep, **kw) -> ndarray (n_rep, m) en trozos con semillas [SEED, k, trozo]; concatena en orden."""
    from joblib import Parallel, delayed
    tr = trozos(R, n_trozos)
    res = Parallel(n_jobs=n_jobs)(delayed(f)(rng(k, i), n, **kw) for i, n in enumerate(tr))
    return np.vstack(res)


def declarar_dgp(herramienta: str, texto: str) -> Path:
    """Escribe el proceso generador ANTES de simular (cabecera del .md; los resultados se añaden después de MARCA)."""
    md = RAIZ / "docs" / "v16" / "validacion_montecarlo" / f"{herramienta}.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(texto.strip() + "\n\n" + MARCA + "\n(pendiente de simular)\n", encoding="utf-8")
    return md


def escribir_salidas(herramienta: str, resultado: dict, tabla: pd.DataFrame, md_resultados: str) -> Path:
    out = RAIZ / "output" / "v16" / "montecarlo" / herramienta
    out.mkdir(parents=True, exist_ok=True)
    (out / "resultado.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8")
    tabla.to_csv(out / "tabla.csv", index=False)
    md = RAIZ / "docs" / "v16" / "validacion_montecarlo" / f"{herramienta}.md"
    previo = md.read_text(encoding="utf-8") if md.exists() else f"# {herramienta}\n\n"
    md.write_text(previo.split(MARCA)[0] + MARCA + "\n" + md_resultados.strip() + "\n", encoding="utf-8")
    return out


def resultado_base(pregunta: str, N, metodo: str, datos: str) -> dict:
    return {
        "rama": "r16/montecarlo", "pregunta": pregunta, "capa": "validación de herramienta (sin capa de evidencia)",
        "datos": datos, "N": N, "metodo": metodo, "estimacion": {}, "ic95": None, "p_ajustado": None,
        "nivel_evidencia": "no aplica (validación Monte Carlo)", "diagnosticos": {},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": [],
    }


def md_tabla(df: pd.DataFrame, dec: int = 4) -> str:
    cols = list(df.columns)
    f = lambda v: (f"{v:.{dec}f}" if isinstance(v, (float, np.floating)) else str(v))
    s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for _, r in df.iterrows():
        s += "| " + " | ".join(f(r[c]) for c in cols) + " |\n"
    return s


def ar1(rng_: np.random.Generator, shape_t_last: tuple, rho: float) -> np.ndarray:
    """AR(1) estacionario de varianza 1 a lo largo del último eje."""
    *lead, T = shape_t_last
    e = rng_.standard_normal(shape_t_last)
    out = np.empty(shape_t_last)
    out[..., 0] = e[..., 0]
    s = math.sqrt(1 - rho ** 2)
    for t in range(1, T):
        out[..., t] = rho * out[..., t - 1] + s * e[..., t]
    return out
