"""Utilidades comunes del Monte Carlo V15 (fase 4.1).

Criterio (docs/v15/preregistro_v15.md sección 6 y adenda, punto 13): tamaño empírico al 5 % en [0,04; 0,06] con R >= 2.000
réplicas bajo el nulo y cobertura del IC 95 % en [0,92; 0,97] bajo una alternativa; tamaño 0,0 es NO APTO.
Solo se lee ESTRUCTURA (códigos, calendario, dimensiones, geometría): nunca valores de resultados ni la muestra sellada.
SEED = 20261010.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

SEED = 20261010
MARCA = "<!-- RESULTADOS -->"
TAM_MIN, TAM_MAX = 0.04, 0.06
COB_MIN, COB_MAX = 0.92, 0.97
R_MIN = 2000
P15 = RAIZ / "data" / "processed" / "v15"
OUT = RAIZ / "output" / "v15" / "montecarlo"
DOCS = RAIZ / "docs" / "v15" / "validacion_montecarlo"


# ------------------------------------------------------------------ aleatoriedad
def flujos(k: int, n: int, sub: int = 0) -> list[np.random.Generator]:
    """n generadores independientes y reproducibles a partir de [SEED, k, sub] (independientes del reparto entre procesos)."""
    return [np.random.default_rng(s) for s in np.random.SeedSequence([SEED, k, sub]).spawn(n)]


def rng(k: int, sub: int = 0) -> np.random.Generator:
    return np.random.default_rng([SEED, k, sub])


_WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def webb(g: np.random.Generator, size) -> np.ndarray:
    return _WEBB[g.integers(0, 6, size=size)]


def ar1(g: np.random.Generator, n, T: int, rho: float, sd: float = 1.0, escala=None) -> np.ndarray:
    """AR(1) estacionario con desviación marginal sd. Devuelve (n, T) (n entero)."""
    z = g.standard_normal((n, T))
    x = np.empty((n, T))
    x[:, 0] = z[:, 0]
    s = np.sqrt(1 - rho ** 2)
    for t in range(1, T):
        x[:, t] = rho * x[:, t - 1] + s * z[:, t]
    x = x * sd
    if escala is not None:
        x = x * np.asarray(escala)[:, None]
    return x


def dist_km(c1: np.ndarray, c2: np.ndarray | None = None) -> np.ndarray:
    """Distancia (km), aproximación equirrectangular; c = (n, 2) lat, lon."""
    c2 = c1 if c2 is None else c2
    lat0 = np.deg2rad((c1[:, None, 0] + c2[None, :, 0]) / 2)
    dx = np.deg2rad(c1[:, None, 1] - c2[None, :, 1]) * np.cos(lat0)
    dy = np.deg2rad(c1[:, None, 0] - c2[None, :, 0])
    return 6371.0 * np.sqrt(dx ** 2 + dy ** 2)


def cholesky_exp(coords: np.ndarray, alcance_km: float) -> np.ndarray:
    K = np.exp(-dist_km(coords) / alcance_km) + 1e-6 * np.eye(len(coords))
    return np.linalg.cholesky(K)


def paralelo(f, tareas, n_jobs: int = 4):
    from joblib import Parallel, delayed
    return Parallel(n_jobs=n_jobs)(delayed(f)(*t) for t in tareas)


def trozos(R: int, n: int = 40) -> list[int]:
    base, extra = divmod(R, n)
    return [base + (1 if i < extra else 0) for i in range(n) if base + (1 if i < extra else 0) > 0]


# ------------------------------------------------------------------ estructura (códigos y geometría)
_CENT = None


def centroides() -> pd.DataFrame:
    """Centroide (lat, lon) de cada municipio (geometría de data/base/geo): es estructura, no un resultado."""
    global _CENT
    if _CENT is None:
        from shapely import wkb
        g = pd.read_parquet(RAIZ / "data" / "base" / "geo" / "municipios.parquet", columns=["cod_municipio", "cod_provincia", "geometry"])
        pts = [wkb.loads(b).centroid for b in g.geometry]
        _CENT = pd.DataFrame({"cod": g.cod_municipio.astype(str).str.zfill(5), "prov": g.cod_provincia.astype(str).str.zfill(2),
                              "lat": [p.y for p in pts], "lon": [p.x for p in pts]}).set_index("cod")
    return _CENT


def estructura_cataluna() -> dict:
    """Municipios catalanes de entrenamiento (p6), cohortes de tratamiento (regulacion_zonas) y centroides. Sin valores de resultado."""
    d = pd.read_parquet(P15 / "p6_zonas_tensionadas.parquet", columns=["territorio_codigo", "variable"])
    d = d[d.variable == "incasol_renta_media"]
    cods = sorted(set(d.territorio_codigo.astype(str).str.zfill(5)))
    r = pd.read_parquet(RAIZ / "data" / "base" / "regulacion_zonas.parquet", columns=["cod_ccaa", "cod_ine_municipio", "fecha_efecto"])
    r = r[r.cod_ccaa == "09"]
    r["cod"] = r.cod_ine_municipio.astype(str).str.zfill(5)
    c1 = set(r[r.fecha_efecto.astype(str) == "2024-03-16"].cod)
    c2 = set(r[r.fecha_efecto.astype(str) == "2024-10-10"].cod)
    ce = centroides()
    cods = [c for c in cods if c in ce.index]
    return {"cods": cods, "coh1": sorted(c1 & set(cods)), "coh2": sorted(c2 & set(cods)),
            "nunca": sorted(set(cods) - c1 - c2), "coords": ce.loc[cods, ["lat", "lon"]], "todos_trat": sorted(c1 | c2)}


# ------------------------------------------------------------------ veredicto
def veredicto(tamano: float, cobertura: float | None, R_nulo: int, banda_tam=(TAM_MIN, TAM_MAX)) -> dict:
    """APTO si tamaño en [0,04; 0,06] con R_nulo >= 2.000 y, si hay IC, cobertura en [0,92; 0,97]. Tamaño 0,0 es NO APTO."""
    fallos = []
    if R_nulo < R_MIN:
        fallos.append(f"R bajo el nulo = {R_nulo} < {R_MIN}")
    if tamano == 0.0:
        fallos.append("tamaño 0,0 (conservador extremo)")
    elif not (banda_tam[0] <= tamano <= banda_tam[1]):
        fallos.append(f"tamaño {tamano:.4f} fuera de [{banda_tam[0]}; {banda_tam[1]}]")
    if cobertura is not None and not (COB_MIN <= cobertura <= COB_MAX):
        fallos.append(f"cobertura {cobertura:.4f} fuera de [{COB_MIN}; {COB_MAX}]")
    return {"veredicto": "APTO" if not fallos else "NO APTO", "apto": not fallos, "fallos": fallos}


def ic_binomial(p: float, n: int) -> list[float]:
    e = 1.96 * math.sqrt(max(p * (1 - p), 1e-12) / n)
    return [round(float(max(p - e, 0.0)), 4), round(float(min(p + e, 1.0)), 4)]


def resumen(est, lo, hi, rechaza, verdad) -> dict:
    est = np.asarray(est, float)
    verdad = np.broadcast_to(np.asarray(verdad, float), est.shape)
    ok = np.isfinite(est) & np.isfinite(lo) & np.isfinite(hi)
    e = est[ok] - verdad[ok]
    return {"R": int(len(est)), "R_validas": int(ok.sum()), "sesgo": float(e.mean()), "rmse": float(np.sqrt((e ** 2).mean())),
            "cobertura": float(np.mean((lo[ok] <= verdad[ok]) & (verdad[ok] <= hi[ok]))),
            "rechazo": float(np.mean(np.asarray(rechaza, float)[ok])), "ancho_medio_ic": float(np.mean(hi[ok] - lo[ok]))}


# ------------------------------------------------------------------ salidas
def declarar(herr: str, texto: str) -> None:
    """Escribe la sección del proceso generador ANTES de simular (el script añade los resultados después de la marca)."""
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / f"{herr}.md").write_text(texto.rstrip() + "\n\n" + MARCA + "\n", encoding="utf-8")


def cerrar(herr: str, resultado: dict, tabla: pd.DataFrame, md_resultados: str) -> None:
    out = OUT / herr
    out.mkdir(parents=True, exist_ok=True)
    (out / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8")
    tabla.to_csv(out / "tabla.csv", index=False, float_format="%.5g")
    md = DOCS / f"{herr}.md"
    previo = md.read_text(encoding="utf-8") if md.exists() else f"# {herr}\n\n"
    md.write_text(previo.split(MARCA)[0] + MARCA + "\n" + md_resultados.strip() + "\n", encoding="utf-8")


def base_resultado(pregunta: str, N, metodo: str) -> dict:
    return {"rama": "v15/montecarlo", "pregunta": pregunta, "capa": "validación de herramienta (sin capa de evidencia)",
            "datos": "simulados; solo estructura (códigos, calendario, dimensiones, geometría) de data/processed/v15; ningún valor de resultado real",
            "N": N, "metodo": metodo, "estimacion": {}, "ic95": None, "p_ajustado": None,
            "nivel_evidencia": "no aplica (validación Monte Carlo)", "diagnosticos": {},
            "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": []}


def md_tabla(df: pd.DataFrame, nd: int = 4) -> str:
    cols = list(df.columns)
    f = lambda v: (f"{v:.{nd}f}" if isinstance(v, (float, np.floating)) else str(v))
    s = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    for _, r in df.iterrows():
        s += "| " + " | ".join(f(r[c]) for c in cols) + " |\n"
    return s
