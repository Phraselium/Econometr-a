"""Compara calculos.py (L2) con output/v5/cifras_clave.csv y escribe output/v6_2/L2/*."""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd

import calculos as c

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "output" / "v6_2" / "L2"

FUNCIONES = {
    "dh_2125": c.dh_2125,
    "terminadas_1924": c.terminadas_1924,
    "L3-DEF-2124-SINBAJAS": c.L3_DEF_2124_SINBAJAS,
    "L3-DEF-2124-CONBAJAS": c.L3_DEF_2124_CONBAJAS,
    "A23-A2": c.A23_A2,
    "A23-P2": c.A23_P2,
    "A23-A10": c.A23_A10,
    "R1C-001": c.R1C_001,
    "B4-v3-vut-cantidad": c.B4_v3_vut_cantidad,
    "latente_convivencia": c.latente_convivencia,
    "B1-H4": c.B1_H4,
    "E-B1-F": c.E_B1_F,
    "D1-H11": c.D1_H11,
    "D1-H12": c.D1_H12,
    "B1-H1": c.B1_H1,
}


def _num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return math.nan
    return v


def _dec(txt) -> int:
    s = str(txt)
    return len(s.split(".")[1]) if "." in s else 0


def coincide(l2, pub, txt) -> bool:
    """True si ambos NaN, o |dif| <= 0,5 % o <= medio paso del redondeo publicado."""
    if math.isnan(pub) or math.isnan(l2):
        return math.isnan(pub) and math.isnan(l2)
    paso = 0.5 * 10 ** (-_dec(txt))
    return abs(l2 - pub) <= max(paso, 0.005 * abs(pub)) + 1e-9


def comparar() -> pd.DataFrame:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv", dtype=str, keep_default_na=False).set_index("id")
    filas = []
    for id_, f in FUNCIONES.items():
        v, lo, hi = (float(x) for x in f())
        r = ck.loc[id_]
        pv, pl, ph = (_num(r[k]) for k in ("valor", "min", "max"))
        ok = [coincide(a, b, r[k]) for a, b, k in ((v, pv, "valor"), (lo, pl, "min"), (hi, ph, "max"))]
        if all(ok):
            clase = "coincide"
        elif (not math.isnan(v) and not math.isnan(pl) and pl - 1e-9 <= v <= ph + 1e-9) or (math.isnan(v) and math.isnan(pv)):
            clase = "coincide dentro del rango"
        else:
            clase = "no coincide"
        filas.append({
            "id": id_, "pub_valor": pv, "pub_min": pl, "pub_max": ph,
            "l2_valor": v, "l2_min": lo, "l2_max": hi, "clase": clase, "diagnostico": "",
        })
    return pd.DataFrame(filas)


if __name__ == "__main__":
    df = comparar()
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA / "comparacion.csv", index=False)
    print(df.to_string())
