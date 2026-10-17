"""V15-A · auxiliares comunes de H1, H2, H3 y E4 (solo entrenamiento: data/processed/v15).

SEED = 20261010. No toca src/econ_utils.py (solo lo importa) ni src/v16/q_comun.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
SEED = 20261010
PROC = RAIZ / "data" / "processed" / "v15"
OUT = RAIZ / "output" / "v15"
FECHA = "2026-10-17"


def periodo_idx(p: str) -> int:
    """'2024T3' -> 2024*4+2 (indice trimestral)."""
    return int(p[:4]) * 4 + int(p[5]) - 1


def idx_periodo(i: int) -> str:
    return f"{i // 4}T{i % 4 + 1}"


def centroides_municipio() -> pd.DataFrame:
    """Centroides municipales (lon, lat) de data/base/geo/municipios.parquet (solo geometria; sin variables de resultado)."""
    import shapely
    g = pd.read_parquet(RAIZ / "data/base/geo/municipios.parquet", columns=["cod_municipio", "geometry"])
    c = shapely.centroid(shapely.from_wkb(g.geometry.values))
    return pd.DataFrame({"cod": g.cod_municipio.values, "lon": shapely.get_x(c), "lat": shapely.get_y(c)})


def xyz_km(lon, lat):
    lo, la = np.radians(np.asarray(lon)), np.radians(np.asarray(lat))
    return 6371.0 * np.column_stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def volcar(ruta: Path, obj) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.ndarray,)):
            return o.tolist()
        if isinstance(o, (np.bool_,)):
            return bool(o)
        return str(o)
    ruta.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=conv), encoding="utf-8")


def registrar(reg, fase, mid, formula, ini, fin, n, coef=np.nan, p=np.nan, notas=""):
    """Atajo al Registry de econ_utils: toda especificacion probada queda registrada."""
    reg.log(fase, mid, formula, ini, fin, int(n), np.nan, np.nan, np.nan, coef_interes=coef, p_interes=p, notas=notas)
