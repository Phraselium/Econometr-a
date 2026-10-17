"""Utilidades comunes del grupo «panel» del Monte Carlo V16 (fase 5).

Solo se lee la ESTRUCTURA (códigos de unidad, periodos disponibles, calendario de intervenciones); nunca los valores de los resultados
reales ni la muestra sellada. El resultado se SIMULA en cada herramienta.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

SEMILLA = 20261010
ENTR = RAIZ / "data" / "processed" / "v16" / "entrenamiento"
INTERV = RAIZ / "output" / "v16" / "f1" / "intervenciones.csv"

# Centroides aproximados de provincia (lat, lon); sirven solo para distancias en la dependencia espacial simulada.
CENTROIDES = {
    "01": (42.85, -2.67), "02": (39.0, -1.86), "03": (38.35, -0.5), "04": (37.0, -2.4), "05": (40.65, -4.7),
    "06": (38.9, -6.3), "07": (39.6, 2.9), "08": (41.6, 2.0), "09": (42.35, -3.7), "10": (39.5, -6.2),
    "11": (36.5, -5.9), "12": (40.2, -0.1), "13": (38.95, -3.9), "14": (37.9, -4.8), "15": (43.1, -8.4),
    "16": (40.1, -2.1), "17": (42.0, 2.8), "18": (37.3, -3.4), "19": (40.8, -2.6), "20": (43.2, -2.2),
    "21": (37.5, -6.9), "22": (42.1, -0.1), "23": (37.8, -3.5), "24": (42.6, -5.7), "25": (41.8, 1.0),
    "26": (42.3, -2.5), "27": (43.0, -7.5), "28": (40.5, -3.7), "29": (36.8, -4.6), "30": (38.0, -1.4),
    "31": (42.7, -1.7), "32": (42.25, -7.5), "33": (43.3, -5.9), "34": (42.4, -4.5), "35": (28.2, -15.4),
    "36": (42.4, -8.5), "37": (40.9, -5.9), "38": (28.3, -16.5), "39": (43.2, -4.0), "40": (41.1, -4.1),
    "41": (37.4, -5.9), "42": (41.7, -2.5), "43": (41.1, 0.9), "44": (40.6, -1.1), "45": (39.8, -4.0),
    "46": (39.4, -0.9), "47": (41.6, -4.7), "48": (43.3, -2.9), "49": (41.6, -6.0), "50": (41.6, -1.0),
    "51": (35.89, -5.32), "52": (35.29, -2.94),
}
# Provincia -> CCAA (códigos INE de CCAA)
PROV_CCAA = {
    "01": "16", "02": "08", "03": "10", "04": "01", "05": "07", "06": "11", "07": "04", "08": "09", "09": "07", "10": "11",
    "11": "01", "12": "10", "13": "08", "14": "01", "15": "12", "16": "08", "17": "09", "18": "01", "19": "08", "20": "16",
    "21": "01", "22": "02", "23": "01", "24": "07", "25": "09", "26": "17", "27": "12", "28": "13", "29": "01", "30": "14",
    "31": "15", "32": "12", "33": "03", "34": "07", "35": "05", "36": "12", "37": "07", "38": "05", "39": "06", "40": "07",
    "41": "01", "42": "07", "43": "09", "44": "02", "45": "08", "46": "10", "47": "07", "48": "16", "49": "07", "50": "02",
    "51": "18", "52": "19",
}


# ---------------------------------------------------------------- aleatoriedad
def flujos(k: int, n: int) -> list[np.random.Generator]:
    """n generadores independientes y reproducibles a partir de [SEMILLA, k] (independientes del reparto entre procesos)."""
    return [np.random.default_rng(s) for s in np.random.SeedSequence([SEMILLA, k]).spawn(n)]


def rng_estructura(k: int) -> np.random.Generator:
    return np.random.default_rng([SEMILLA, k])


_WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def webb(rng: np.random.Generator, size) -> np.ndarray:
    return _WEBB[rng.integers(0, 6, size=size)]


def ar1(rng: np.random.Generator, shape_unidades, T: int, rho: float, sd: float = 1.0, escala=None) -> np.ndarray:
    """AR(1) estacionario, desviación típica marginal sd (por unidad si escala es un vector). Devuelve (n, T)."""
    n = shape_unidades
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


# ---------------------------------------------------------------- geografía simulada
def dist_km(c1: np.ndarray, c2: np.ndarray | None = None) -> np.ndarray:
    """Distancia (km) por aproximación equirrectangular; c = (n,2) lat, lon."""
    c2 = c1 if c2 is None else c2
    lat0 = np.deg2rad((c1[:, None, 0] + c2[None, :, 0]) / 2)
    dx = np.deg2rad(c1[:, None, 1] - c2[None, :, 1]) * np.cos(lat0)
    dy = np.deg2rad(c1[:, None, 0] - c2[None, :, 0])
    return 6371.0 * np.sqrt(dx ** 2 + dy ** 2)


def cholesky_exp(coords: np.ndarray, alcance_km: float) -> np.ndarray:
    """Factor de Cholesky de una covarianza exponencial exp(-d/alcance) (campo espacial de varianza 1)."""
    K = np.exp(-dist_km(coords) / alcance_km) + 1e-6 * np.eye(len(coords))
    return np.linalg.cholesky(K)


def coords_municipios(codigos, rng: np.random.Generator, radio_km: float = 35.0) -> np.ndarray:
    """Coordenadas simuladas: centroide de provincia + dispersión gaussiana (≈ radio_km); estructura, no datos reales."""
    out = np.empty((len(codigos), 2))
    for i, c in enumerate(codigos):
        la, lo = CENTROIDES[str(c).zfill(5)[:2]]
        out[i, 0] = la + rng.normal(0, radio_km / 111.0)
        out[i, 1] = lo + rng.normal(0, radio_km / (111.0 * np.cos(np.deg2rad(la))))
    return out


# ---------------------------------------------------------------- estructura leída (solo códigos y calendario)
def _sellada_v16(cod: pd.Series, nivel: str) -> np.ndarray:
    from src import holdout
    return holdout.unidad_sellada_v16(cod.astype(str), nivel).to_numpy()


def estructura_serpavi_municipal(completo: bool = True) -> pd.DataFrame:
    """Municipios de entrenamiento con SERPAVI en todos los años 2019-2022 y 2024 (solo códigos y presencia; sin valores).
    completo=False: todos los municipios de entrenamiento con SERPAVI en algún año (≈2.000 unidades)."""
    a = pd.read_parquet(ENTR / "base_alquiler.parquet", columns=["territorio_codigo", "nivel", "periodo", "variable"])
    s = a[(a.nivel == "municipio") & (a.variable == "serpavi_alquiler_m2_mediana")].copy()
    s["territorio_codigo"] = s.territorio_codigo.astype(str).str.zfill(5)
    s = s[~_sellada_v16(s.territorio_codigo, "municipio")]
    años = ["2019", "2020", "2021", "2022", "2024"]
    if completo:
        n = s[s.periodo.isin(años)].groupby("territorio_codigo").periodo.nunique()
        cods = sorted(n[n == len(años)].index)
    else:
        cods = sorted(s.territorio_codigo.unique())
    return pd.DataFrame({"cod": cods, "prov": [c[:2] for c in cods], "ccaa": [PROV_CCAA[c[:2]] for c in cods]})


def intervenciones() -> pd.DataFrame:
    return pd.read_csv(INTERV, dtype=str)


def zonas_tensionadas() -> pd.DataFrame:
    d = intervenciones()
    z = d[d.instrumento == "zona_tensionada"].copy()
    z["cod"] = z.cod_ine.str.zfill(5)
    z["prov"] = z.cod.str[:2]
    z["ccaa"] = z.prov.map(PROV_CCAA)
    z["efecto"] = pd.to_datetime(z.fecha_efecto)
    return z


def provincias_entrenamiento() -> list[str]:
    """Provincias de entrenamiento (nivel provincia, frecuencia trimestral, IPC de alquiler: solo códigos)."""
    a = pd.read_parquet(ENTR / "base_alquiler.parquet", columns=["territorio_codigo", "nivel", "frecuencia", "variable"])
    p = a[(a.nivel == "provincia") & (a.frecuencia == "T") & (a.variable == "ipc_alquiler_indice")].territorio_codigo.astype(str).str.zfill(2)
    p = sorted(set(p))
    return [c for c in p if not _sellada_v16(pd.Series([c]), "provincia")[0]]


# ---------------------------------------------------------------- veredicto (adenda, punto 11)
def veredicto(tamano: float, cobertura: float, R_nulo: int) -> dict:
    """APTO si tamaño en [0,04; 0,06] con R_nulo >= 2.000 y cobertura del IC 95 % en [0,92; 0,97]. Tamaño 0,0 es NO APTO."""
    ok_t = (R_nulo >= 2000) and (0.04 <= tamano <= 0.06) and tamano > 0.0
    ok_c = 0.92 <= cobertura <= 0.97
    fallos = []
    if R_nulo < 2000:
        fallos.append(f"R bajo el nulo = {R_nulo} < 2000")
    if not (0.04 <= tamano <= 0.06) or tamano == 0.0:
        fallos.append(f"tamaño {tamano:.4f} fuera de [0,04; 0,06]" + (" (0,0: conservador extremo)" if tamano == 0.0 else ""))
    if not ok_c:
        fallos.append(f"cobertura {cobertura:.4f} fuera de [0,92; 0,97]")
    return {"apto": bool(ok_t and ok_c), "tamano_ok": bool(ok_t), "cobertura_ok": bool(ok_c), "fallos": fallos}


def resumen_escenario(est: np.ndarray, ic_lo: np.ndarray, ic_hi: np.ndarray, rechaza: np.ndarray, verdad: np.ndarray | float) -> dict:
    est = np.asarray(est, float)
    verdad = np.broadcast_to(np.asarray(verdad, float), est.shape)
    ok = np.isfinite(est) & np.isfinite(ic_lo) & np.isfinite(ic_hi)
    e = est[ok] - verdad[ok]
    cov = float(np.mean((ic_lo[ok] <= verdad[ok]) & (verdad[ok] <= ic_hi[ok])))
    return {"R": int(len(est)), "R_validas": int(ok.sum()), "sesgo": float(e.mean()), "rmse": float(np.sqrt((e ** 2).mean())),
            "cobertura": cov, "rechazo": float(np.mean(rechaza[ok])), "ancho_medio_ic": float(np.mean(ic_hi[ok] - ic_lo[ok]))}


def mc_se(p: float, R: int) -> float:
    return float(np.sqrt(max(p * (1 - p), 1e-12) / R))


def guardar(carpeta: Path, resultado: dict, tabla: pd.DataFrame) -> None:
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=float), encoding="utf-8")
    tabla.to_csv(carpeta / "tabla.csv", index=False)
