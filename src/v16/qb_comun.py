"""V16 · fase 6 · utilidades comunes del grupo B (Q3, Q4, Q6). (Prefijo qb_ para no chocar con las del grupo A.)

Solo entrenamiento (data/processed/v16/entrenamiento). Nunca la muestra sellada. SEED = 20261010.
Herramientas NO APTAS (docs/v16/validacion_montecarlo.md): solo estimación puntual. No se calcula p-valor ni IC con ellas.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
ENT = RAIZ / "data" / "processed" / "v16" / "entrenamiento"
SEED = 20261010
FECHA = "2026-10-17"

PROV_CCAA = {
    "01": "16", "02": "08", "03": "10", "04": "01", "05": "07", "06": "11", "07": "04", "08": "09", "09": "07", "10": "11",
    "11": "01", "12": "10", "13": "08", "14": "01", "15": "12", "16": "08", "17": "09", "18": "01", "19": "08", "20": "16",
    "21": "01", "22": "02", "23": "01", "24": "07", "25": "09", "26": "17", "27": "12", "28": "13", "29": "01", "30": "14",
    "31": "15", "32": "12", "33": "03", "34": "07", "35": "05", "36": "12", "37": "07", "38": "05", "39": "06", "40": "07",
    "41": "01", "42": "07", "43": "09", "44": "02", "45": "08", "46": "10", "47": "07", "48": "16", "49": "07", "50": "02",
    "51": "18", "52": "19"}
GRANDES_PROV = {"08", "46", "41", "29"}
GRANDES_MUN = {"08019", "46250", "41091", "29067"}
ORIGENES = ["Alemania", "Argelia", "Argentina", "Bolivia", "Brasil", "Bulgaria", "Chile", "China", "Colombia", "Cuba", "Ecuador",
            "Francia", "Italia", "Marruecos", "Nigeria", "Pakistán", "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido",
            "República Dominicana", "Rumanía", "Rusia", "Senegal", "Ucrania", "Uruguay", "Venezuela"]


def cargar(archivo: str, variable: str | list, nivel: str | None = None, desag: str | None = None) -> pd.DataFrame:
    """Lee un panel de entrenamiento y filtra por variable (y nivel, desagregación)."""
    d = pd.read_parquet(ENT / f"{archivo}.parquet", columns=["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor"])
    vs = [variable] if isinstance(variable, str) else variable
    d = d[d.variable.isin(vs)]
    if nivel:
        d = d[d.nivel == nivel]
    if desag is not None:
        d = d[d.desagregacion == desag]
    return d


def anual(d: pd.DataFrame, nombre: str = "y") -> pd.Series:
    """Serie indexada por (territorio, año) con año entero."""
    s = d.assign(a=d.periodo.astype(str).str[:4].astype(int)).groupby(["territorio_codigo", "a"]).valor.first()
    s.index.names = ["u", "t"]
    return s.rename(nombre)


def codif(x) -> np.ndarray:
    return pd.factorize(pd.Series(x))[0]


def _desmedia(M: np.ndarray, grupos: list[np.ndarray], iters: int = 200, tol: float = 1e-10) -> np.ndarray:
    M = np.array(M, dtype=float, copy=True)
    if M.ndim == 1:
        M = M[:, None]
    if not grupos:
        return M - M.mean(0)
    for _ in range(iters):
        previo = M.copy()
        for g in grupos:
            k = int(g.max()) + 1
            cnt = np.bincount(g, minlength=k).astype(float)
            for j in range(M.shape[1]):
                M[:, j] -= (np.bincount(g, weights=M[:, j], minlength=k) / cnt)[g]
        if np.max(np.abs(M - previo)) < tol:
            break
    return M


def mco_fe(y, X, grupos: list[np.ndarray]) -> dict:
    """MCO con efectos fijos absorbidos (demedia alternada). X (n,k). Devuelve beta, residuos, R2 total y dentro."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X[:, None]
    yt = _desmedia(y, grupos)[:, 0]
    Xt = _desmedia(X, grupos)
    b, *_ = np.linalg.lstsq(Xt, yt, rcond=None)
    e = yt - Xt @ b
    sst_tot = float(((y - y.mean()) ** 2).sum())
    sst_w = float((yt ** 2).sum())
    ssr = float((e ** 2).sum())
    return {"beta": b, "resid": e, "yt": yt, "Xt": Xt, "r2_total": 1 - ssr / sst_tot, "r2_within": 1 - ssr / sst_w if sst_w > 0 else np.nan,
            "n": len(y), "sdx_t": Xt.std(0), "sdy_t": float(yt.std())}


def e_value_puntual(beta: float, sdx: float, sdy: float) -> float:
    """E-value (VanderWeele-Ding) del punto, con d = beta·sdx/sdy y RR ≈ exp(0,91·d). Sin IC."""
    d = abs(beta) * sdx / sdy
    rr = float(np.exp(0.91 * d))
    return float(rr + np.sqrt(rr * (rr - 1))) if rr > 1 else 1.0


def oster_delta(b0: float, r0: float, bt: float, rt: float, factor: float = 1.3) -> float:
    """δ para β = 0 con R2max = min(factor·R2, 1) (Oster 2019). NaN si el denominador es 0."""
    rmax = min(factor * rt, 1.0)
    den = (b0 - bt) * (rmax - rt)
    return float(bt * (rt - r0) / den) if abs(den) > 1e-15 else float("nan")


def rv_q1(t: float, dof: int) -> float:
    """Valor de robustez de Cinelli-Hazlett RV_{q=1} a partir del estadístico t (solo si la inferencia es APTA)."""
    f = abs(t) / np.sqrt(dof)
    return float(0.5 * (np.sqrt(f ** 4 + 4 * f ** 2) - f ** 2))


def moran(resid: np.ndarray, xy: np.ndarray, k: int = 4) -> dict:
    """I de Moran de los residuos con k vecinos más próximos (binaria normalizada por filas); p por 999 permutaciones (SEED)."""
    from scipy.spatial import cKDTree
    n = len(resid)
    if n < 8:
        return {"I": float("nan"), "p_perm": float("nan"), "n": n}
    idx = cKDTree(xy).query(xy, k=k + 1)[1][:, 1:]
    z = resid - resid.mean()

    def I(v):
        return float(np.sum(v * v[idx].mean(1)) / np.sum(v * v))

    obs = I(z)
    rng = np.random.default_rng([SEED, 7])
    perm = np.array([I(rng.permutation(z)) for _ in range(999)])
    return {"I": obs, "p_perm_bilateral": float((1 + np.sum(np.abs(perm) >= abs(obs))) / 1000), "n": n,
            "nota": "diagnóstico de dependencia espacial de residuos; no es inferencia sobre el efecto"}


def centroides(df_geo: pd.DataFrame) -> np.ndarray:
    import shapely
    c = shapely.centroid(shapely.from_wkb(df_geo.geometry.values))
    lon, lat = np.radians(shapely.get_x(c)), np.radians(shapely.get_y(c))
    return 6371.0 * np.column_stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])


def centroides_prov() -> pd.DataFrame:
    g = pd.read_parquet(RAIZ / "data" / "base" / "geo" / "provincias.parquet", columns=["cod_provincia", "geometry"])
    g["cod_provincia"] = g.cod_provincia.astype(str).str.zfill(2)
    xyz = centroides(g)
    return pd.DataFrame(xyz, index=g.cod_provincia.values, columns=["x", "y", "z"])


def heterocedasticidad_autocorr(e: np.ndarray, xt: np.ndarray, u: np.ndarray, t: np.ndarray) -> dict:
    """Diagnósticos descriptivos: Breusch-Pagan (LM = n·R2 de e² sobre x) y Wooldridge (pendiente de Δe sobre Δe_{-1}; -0,5 = sin autocorrelación)."""
    e2 = e ** 2
    Z = np.column_stack([np.ones(len(e)), xt])
    g, *_ = np.linalg.lstsq(Z, e2, rcond=None)
    r2 = 1 - ((e2 - Z @ g) ** 2).sum() / ((e2 - e2.mean()) ** 2).sum()
    df = pd.DataFrame({"u": u, "t": t, "e": e}).sort_values(["u", "t"])
    df["de"] = df.groupby("u").e.diff()
    df["de1"] = df.groupby("u").de.shift(1)
    d = df.dropna()
    pend = float((d.de * d.de1).sum() / (d.de1 ** 2).sum()) if len(d) > 5 else float("nan")
    return {"breusch_pagan_LM": float(len(e) * r2), "wooldridge_pendiente": pend, "wooldridge_referencia_sin_autocorr": -0.5}


def _j(o):
    if isinstance(o, (np.floating, np.integer)):
        return None if (isinstance(o, np.floating) and not np.isfinite(o)) else o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return str(o)


def volcar(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=_j) + "\n", encoding="utf-8")


def hecho(id_, indicador, valor, minv, maxv, unidad, periodo, cobertura, fuentes, ancla, carpeta, fecha_dato) -> dict:
    return {"id": id_, "indicador": indicador, "valor": valor, "min": minv, "max": maxv, "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "fecha_dato": fecha_dato,
            "ficha": f"output/v16/{carpeta}/informe.md#{ancla}"}
