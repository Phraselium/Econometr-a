"""V18 · Utilidades comunes del Monte Carlo (plan de replicación, sección 1.13). Sin lectura de datos: todo se simula.

Semilla SEED = 20261010. Cada réplica tiene su propio generador (SeedSequence([SEED, k1, k2]).spawn(R)): el resultado no depende
del reparto entre procesos. Bandas: criterio del encargo (tamaño en [0,03; 0,08] y cobertura en [0,92; 0,97]) y bandas de la
adenda 1.12 (apta: tamaño [0,04; 0,06] y cobertura [0,93; 0,97]; valor crítico corregido: tamaño [0,02; 0,04) o (0,06; 0,15];
no fiable: tamaño > 0,15 o < 0,02).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ALCANCE_TERRITORIAL = "sin lectura de datos"

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

SEMILLA = 20261010
SALIDA = RAIZ / "output" / "v18" / "montecarlo"

_WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def flujos(k1: int, k2: int, n: int) -> list[np.random.Generator]:
    """n generadores independientes y reproducibles a partir de [SEMILLA, k1, k2]."""
    return [np.random.default_rng(s) for s in np.random.SeedSequence([SEMILLA, k1, k2]).spawn(n)]


def webb(rng: np.random.Generator, size) -> np.ndarray:
    """Pesos de Webb (6 puntos, media 0 y varianza 1)."""
    return _WEBB[rng.integers(0, 6, size=size)]


def ar1(rng: np.random.Generator, n: int, T: int, rho: float, sd: float = 1.0, escala=None) -> np.ndarray:
    """n series AR(1) estacionarias (n, T) con desviación típica marginal sd (por serie si escala es un vector)."""
    z = rng.standard_normal((n, T))
    x = np.empty((n, T))
    x[:, 0] = z[:, 0]
    s = np.sqrt(1 - rho ** 2)
    for t in range(1, T):
        x[:, t] = rho * x[:, t - 1] + s * z[:, t]
    x = x * sd
    if escala is not None:
        x = x * np.asarray(escala)[:, None]
    return x


def mc_se(p: float, R: int) -> float:
    return float(np.sqrt(max(p * (1 - p), 1e-12) / R))


def _bloque(fn, args, rngs):
    return [fn(r, *args) for r in rngs]


def ejecutar(fn, args: tuple, R: int, k1: int, k2: int, jobs: int = 4) -> np.ndarray:
    """Ejecuta fn(rng, *args) -> vector en R réplicas, en paralelo, con orden y semillas deterministas. Devuelve (R, m)."""
    rngs = flujos(k1, k2, R)
    if jobs <= 1:
        return np.array(_bloque(fn, args, rngs), float)
    from joblib import Parallel, delayed
    nb = jobs * 6
    sal = Parallel(n_jobs=jobs)(delayed(_bloque)(fn, args, rngs[i::nb]) for i in range(nb))
    res = [None] * R
    for i, blq in enumerate(sal):
        for j, fila in enumerate(blq):
            res[i + j * nb] = fila
    return np.array(res, float)


# ------------------------------------------------------------------------------------------------ bandas
def _lista(cob) -> list[float]:
    if cob is None:
        return []
    if isinstance(cob, (list, tuple)):
        return [float(c) for c in cob if c is not None and np.isfinite(c)]
    return [float(cob)] if np.isfinite(cob) else []


def banda_encargo(tam: float, cob, R: int) -> dict:
    """APTO si tamaño en [0,03; 0,08] y toda cobertura (bajo el nulo y bajo la alternativa) en [0,92; 0,97]; R >= 1.000 (se declara si < 2.000)."""
    cobs = _lista(cob)
    ok_t = 0.03 <= tam <= 0.08
    ok_c = all(0.92 <= c <= 0.97 for c in cobs)
    fallos = []
    if not ok_t:
        fallos.append(f"tamaño {tam:.4f} fuera de [0,03; 0,08]" + (" (conservador)" if tam < 0.03 else " (liberal)"))
    for c in cobs:
        if not 0.92 <= c <= 0.97:
            fallos.append(f"cobertura {c:.4f} fuera de [0,92; 0,97]" + (" (conservadora)" if c > 0.97 else " (insuficiente)"))
    return {"apto": bool(ok_t and ok_c and R >= 1000), "R": int(R), "R_menor_2000": bool(R < 2000), "fallos": fallos}


def banda_112(tam: float, cob, R: int) -> str:
    """Bandas de la adenda 1.12."""
    cobs = _lista(cob)
    if tam > 0.15 or tam < 0.02:
        return "no fiable"
    if 0.04 <= tam <= 0.06 and all(0.93 <= c <= 0.97 for c in cobs) and R >= 2000:
        return "apta"
    return "con valor crítico corregido"


def fila_metricas(escenario: str, variante: str, tam: float, cob_nulo: float | None, cob_alt: float | None, pot: float | None, R: int,
                  sesgo: float | None = None, rmse: float | None = None, extra: dict | None = None) -> dict:
    cobs = _lista([cob_nulo, cob_alt])
    b = banda_encargo(tam, cobs, R)
    f = {"escenario": escenario, "variante": variante, "R": R, "tamano_5pct": tam, "se_mc_tamano": mc_se(tam, R),
         "cobertura_nulo": cob_nulo, "cobertura_alt": cob_alt, "potencia": pot, "sesgo": sesgo, "rmse": rmse,
         "veredicto": "APTO" if b["apto"] else "NO APTO", "fallos": " / ".join(b["fallos"]), "banda_112": banda_112(tam, cobs, R)}
    if extra:
        f.update(extra)
    return f


def escribir(herramienta: str, resultado: dict, tabla: pd.DataFrame, informe: str, carpeta: Path | None = None) -> Path:
    c = (carpeta or SALIDA) / herramienta
    c.mkdir(parents=True, exist_ok=True)
    (c / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    tabla.to_csv(c / "tabla.csv", index=False)
    (c / "informe.md").write_text(informe, encoding="utf-8")
    return c


def resultado_base(herramienta: str, pregunta: str, datos: str, N: str, metodo: str) -> dict:
    return {"rama": "v18/montecarlo", "pregunta": pregunta, "capa": "validación de herramienta (sin capa de evidencia)",
            "datos": datos, "N": N, "metodo": metodo, "estimacion": None, "ic95": None, "p_ajustado": None,
            "nivel_evidencia": "no aplica (validación Monte Carlo)", "diagnosticos": {}, "fuera_muestra": None, "notas": "",
            "herramienta": herramienta, "semilla": SEMILLA}


def veredicto_global(tabla: pd.DataFrame, col_variante: str | None = None, principal: str | None = None) -> tuple[str, str]:
    """(veredicto, condición en que falla). Si hay variante principal, decide solo ella; el resto es información."""
    t = tabla if principal is None else tabla[tabla["variante"] == principal]
    if len(t) == 0:
        return "NO EVALUADO", "sin filas"
    malos = t[t["veredicto"] != "APTO"]
    if len(malos) == 0:
        return "APTO", ""
    cond = "; ".join(f"{r.escenario}: {r.fallos}" for r in malos.itertuples())
    if len(malos) < len(t):
        return "APTO CONDICIONADO", "falla en " + cond
    return "NO APTO", cond


def md_tabla(df: pd.DataFrame, dec: int = 4) -> str:
    def f(v):
        if isinstance(v, (float, np.floating)):
            return "" if not np.isfinite(v) else f"{v:.{dec}f}"
        return str(v)
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f(r[c]) for c in cols) + " |")
    return "\n".join(out)


class Reloj:
    def __init__(self):
        self.t0 = time.time()

    def seg(self) -> float:
        return round(time.time() - self.t0, 1)
