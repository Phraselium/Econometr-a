"""V15-B · utilidades comunes (H4, H5, E1, E2, E3). Solo entrenamiento (data/processed/v15). Sin efectos al importar. Todo es C4 y 'pendiente_sellada'.

Las desviaciones están en docs/v15/desviaciones.md (sección DV15-B). Sin lenguaje causal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
P15 = ROOT / "data" / "processed" / "v15"
OUT = ROOT / "output" / "v15"
SEED = 20261010
FECHA = "2026-10-17"
COSTERAS = ["03", "04", "07", "08", "11", "12", "15", "17", "18", "20", "21", "27", "29", "30", "33", "35", "36", "38", "39", "43", "46", "48"]
GRANDES_MUN = ["08019", "46250"]

from src.econ_utils import Registry  # noqa: E402


def cargar(nombre: str, variables=None, nivel=None) -> pd.DataFrame:
    d = pd.read_parquet(P15 / f"{nombre}.parquet")
    if nivel is not None:
        d = d[d.nivel == nivel]
    if variables is not None:
        v = [variables] if isinstance(variables, str) else list(variables)
        d = d[d.variable.isin(v)]
    d = d.copy()
    d["territorio_codigo"] = d.territorio_codigo.astype(str)
    return d


def trim(d: pd.DataFrame) -> pd.DataFrame:
    x = d[d.periodo.astype(str).str.contains("T")].copy()
    x["q"] = pd.PeriodIndex([f"{v[:4]}Q{v[-1]}" for v in x.periodo.astype(str)], freq="Q")
    return x


def serie_q(d: pd.DataFrame, variable: str, nivel="nacional", cod=None) -> pd.Series:
    x = trim(d[(d.variable == variable) & (d.nivel == nivel)])
    if cod is not None:
        x = x[x.territorio_codigo == cod]
    return x.drop_duplicates("q").set_index("q").valor.astype(float).sort_index()


# ------------------------------------------------------------------ mínimos cuadrados con efectos fijos (FWL)
def demean(M, grupos_list, it=100):
    """Quita efectos fijos aditivos (una o varias dimensiones) por alternancia de medias."""
    M = np.asarray(M, float).copy()
    if M.ndim == 1:
        M = M[:, None]
    codes = [pd.factorize(g)[0] for g in grupos_list]
    for _ in range(it):
        prev = M.copy()
        for c in codes:
            n = np.bincount(c)
            for j in range(M.shape[1]):
                M[:, j] -= (np.bincount(c, M[:, j]) / n)[c]
        if np.max(np.abs(M - prev)) < 1e-10:
            break
    return M


def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b, y - X @ b


def mcs_pertenencia(L: np.ndarray, nombres, alpha=0.10, B=999, bl=4, seed=SEED):
    """MCS de Hansen-Lunde-Nason (T_max, bootstrap de bloques). Solo descriptivo (K13). Devuelve los nombres del conjunto."""
    P, m = L.shape
    g = np.random.default_rng([seed, 15])
    nb = int(np.ceil(P / bl))
    st = g.integers(0, P - bl + 1, (B, nb))
    idx = (st[:, :, None] + np.arange(bl)[None, None, :]).reshape(B, -1)[:, :P]
    Lb = L[idx].mean(1)
    Lbar = L.mean(0)
    conj = list(range(m))
    while len(conj) > 1:
        S = np.array(conj)
        d = Lbar[S][:, None] - Lbar[S][None, :]
        db = Lb[:, S][:, :, None] - Lb[:, S][:, None, :]
        v = ((db - d[None]) ** 2).mean(0) + np.eye(len(S))
        t = d / np.sqrt(v)
        tb = ((db - d[None]) / np.sqrt(v)[None]).reshape(B, -1).max(1)
        if float(np.mean(tb >= np.max(t))) >= alpha:
            break
        conj = [c for k, c in enumerate(conj) if k != int(np.argmax(t.max(1)))]
    return [nombres[c] for c in conj]


def dm_hln(e_base, e_mod, h=1):
    """DM-HLN unilateral (H1: el modelo tiene menor ECM que la base); p con t(P-1). d = e_base^2 - e_mod^2."""
    d = np.asarray(e_base) ** 2 - np.asarray(e_mod) ** 2
    P = len(d)
    if P < 8:
        return {"dm": np.nan, "p_unilateral": np.nan, "p_bilateral": np.nan, "P": P}
    dc = d - d.mean()
    lrv = dc @ dc / P + 2 * sum((1 - k / h) * (dc[k:] @ dc[:-k] / P) for k in range(1, h))
    if lrv <= 0:
        return {"dm": np.nan, "p_unilateral": np.nan, "p_bilateral": np.nan, "P": P}
    dm = d.mean() / np.sqrt(lrv / P) * np.sqrt((P + 1 - 2 * h + h * (h - 1) / P) / P)
    return {"dm": float(dm), "p_unilateral": float(stats.t.sf(dm, P - 1)), "p_bilateral": float(2 * stats.t.sf(abs(dm), P - 1)), "P": P}


# ------------------------------------------------------------------ salidas
def _j(o):
    if isinstance(o, (np.floating, np.integer)):
        return None if (isinstance(o, np.floating) and not np.isfinite(o)) else o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, float) and not np.isfinite(o):
        return None
    raise TypeError(type(o))


def limpia(o):
    if isinstance(o, dict):
        return {str(k): limpia(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpia(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return limpia(o.tolist())
    return o


def escribe_json(ruta: Path, obj):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(limpia(obj), ensure_ascii=False, indent=2), encoding="utf-8")


def hecho(id_, indicador, valor, minimo, maximo, unidad, periodo, cobertura, fuentes, ancla, carpeta, capa="C4"):
    return {"id": id_, "indicador": indicador, "valor": valor, "min": minimo, "max": maximo, "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": capa, "fecha_dato": FECHA, "ficha": f"output/v15/{carpeta}/informe.md#{ancla}"}


def resultado_base(rama, pregunta, datos, N, metodo, estimacion, ic95, nivel, diag, fuera, notas, p_by, extra=None):
    r = {"rama": rama, "pregunta": pregunta, "capa": "C4", "datos": datos, "N": N, "metodo": metodo, "estimacion": estimacion,
         "ic95": ic95, "p_ajustado": None, "nivel_evidencia": nivel, "diagnosticos": diag, "fuera_muestra": fuera, "notas": notas,
         "pendiente_sellada": True, "p_valores_para_BY": p_by, "semilla": SEED}
    if extra:
        r.update(extra)
    return r


def knn_moran(resid, xy, k=4, B=999):
    from scipy.spatial import cKDTree
    n = len(resid)
    idx = cKDTree(xy).query(xy, k=k + 1)[1][:, 1:]
    z = resid - resid.mean()
    I = lambda v: float(np.sum(v * v[idx].mean(1)) / np.sum(v * v))
    obs = I(z)
    rng = np.random.default_rng([SEED, 7])
    perm = np.array([I(rng.permutation(z)) for _ in range(B)])
    return {"I": obs, "p_perm_bilateral": float((1 + np.sum(np.abs(perm) >= abs(obs))) / (B + 1)), "n": n, "k": k}


def centroides_mun(cods):
    """Centroides (km, esfera) de los municipios pedidos (solo geometría de data/base/geo)."""
    import shapely
    g = pd.read_parquet(ROOT / "data" / "base" / "geo" / "municipios.parquet", columns=["cod_municipio", "geometry"])
    g["cod"] = g.cod_municipio.astype(str).str.zfill(5)
    g = g[g.cod.isin(set(cods))].drop_duplicates("cod").set_index("cod")
    c = shapely.centroid(shapely.from_wkb(g.geometry.values))
    lon, lat = np.radians(shapely.get_x(c)), np.radians(shapely.get_y(c))
    xyz = 6371.0 * np.column_stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)])
    return pd.DataFrame(xyz, index=g.index, columns=["x", "y", "z"])
