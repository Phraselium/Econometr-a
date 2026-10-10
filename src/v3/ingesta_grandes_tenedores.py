"""Ingesta preparada para los datos de grandes tenedores (solicitud 1, docs/v3/solicitudes_transparencia.md).

Espera data/raw/v3/catastro_titulares_tramos.csv con columnas:
    anio, cod_muni, tipo_titular, tramo (1, 2, 3-4, 5-9, 10-24, 25-99, 100-999, 1000+), n_inmuebles, superficie_m2
Mientras el fichero no exista, escribe output/v3/PB/grandes_tenedores.json con estado «en espera» y no calcula nada.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "data" / "raw" / "v3" / "catastro_titulares_tramos.csv"
SALIDA = RAIZ / "output" / "v3" / "PB" / "grandes_tenedores.json"
TRAMOS_GT = {"10-24", "25-99", "100-999", "1000+"}   # Ley 12/2023, art. 3.k: 10 o más inmuebles residenciales


def cuota_grandes_tenedores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["gran_tenedor"] = df["tramo"].astype(str).isin(TRAMOS_GT)
    g = df.groupby(["anio", "cod_muni", "gran_tenedor"])["n_inmuebles"].sum().unstack(fill_value=0)
    return (g[True] / g.sum(axis=1)).rename("cuota_gt").reset_index()


def main() -> dict:
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    if not ENTRADA.exists():
        res = {"estado": "en espera", "motivo": "datos de titularidad por tramos no disponibles (solicitud de transparencia pendiente)",
               "capa": "C2", "cota": None}
    else:
        c = cuota_grandes_tenedores(pd.read_csv(ENTRADA, dtype={"cod_muni": str}))
        res = {"estado": "datos recibidos", "capa": "C2", "n_municipios": int(c["cod_muni"].nunique()),
               "anios": [int(c["anio"].min()), int(c["anio"].max())],
               "nota": "cota pendiente de especificar con el esquema de B1 (docs/v3/especificacion_PA_PB.md)"}
    SALIDA.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    return res


if __name__ == "__main__":
    print(main())
