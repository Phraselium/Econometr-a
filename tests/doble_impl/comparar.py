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


DIAG = {
    "dh_2125": "Reproduce. Sin huecos relevantes.",
    "terminadas_1924": "Reproduce. Hueco menor: protegidas ausentes se tratan como 0 (no declarado).",
    "L3-DEF-2124-SINBAJAS": "Reproduce (8 variantes x 3 fuentes). Hueco menor: el Catastro se suma sin filtrar por regimen (solo se dice 'valor por periodo').",
    "L3-DEF-2124-CONBAJAS": "Reproduce. Bajas = 0,2 % x suma parque 2020-2023 = 214.115,8 (el anexo redondea a 214.116).",
    "A23-A2": "Reproduce. Hueco menor: base del IPVA 'Contrato existente' (2021=100) solo implicita en '/100'; criterio de empate del nucleo no definido.",
    "A23-P2": "Reproduce. Hueco: el conjunto de candidatos del nucleo no se define; se asume que el IPV queda fuera por la frase del anexo.",
    "A23-A10": "Reproduce (28,46 -> 28,5). Pesos por clave normalizada (sin acentos, antes de '/'): sin ella 'Valencia/Valencia' no cruza.",
    "R1C-001": "Reproduce. Sin huecos relevantes.",
    "B4-v3-vut-cantidad": "Reproduce. Hueco: los nombres de serie ECV para 'alquiler a precio de mercado' e 'inferior' no se dan.",
    "latente_convivencia": "Reproduce. Hueco: no se dice que la serie JSON tiene un dato por anyo (FK_Periodo 28) ni que el redondeo a miles es round() sobre extremos.",
    "B1-H4": "Reproduce. Las colisiones de clave (Navarra, Madrid, Asturias, Murcia, Rioja) se resuelven con 'primera fila por clave y anyo'.",
    "E-B1-F": "Reproduce (mismo calculo que B1-H4).",
    "D1-H11": "Reproduce. Hueco: metodo de percentil (lineal, numpy por defecto) no declarado; la clase se toma de clase_2021_2025.",
    "D1-H12": "Reproduce. Mismo hueco de percentil; con recorte a >=0.",
    "B1-H1": "Reproduce desde B1_nacional.csv. Hueco menor: nombres de columnas de la tabla (componente,min,central,max) no se indican.",
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


# v6.2 (revisión H6): tolerancia = medio paso del redondeo publicado; el 0,5 % relativo solo donde hay percentiles interpolados
CON_PERCENTILES = {"D1-H11", "D1-H12", "latente_convivencia"}
# Cifras cuya doble implementación lee una tabla intermedia del código original (no es plenamente independiente)
DEPENDIENTES = {"B1-H1": "lee B1_nacional.csv (componentes de B1)", "B1-H4": "lee clasificacion_provincias.csv (lista de claves)",
                "E-B1-F": "lee clasificacion_provincias.csv (lista de claves)", "D1-H11": "lee clasificacion_provincias.csv (clase A4)",
                "D1-H12": "lee clasificacion_provincias.csv (clase A4)"}


def coincide(l2, pub, txt, id_=None) -> bool:
    """True si ambos NaN, o |dif| <= medio paso del redondeo publicado (o 0,5 % si la cifra usa percentiles interpolados)."""
    if math.isnan(pub) or math.isnan(l2):
        return math.isnan(pub) and math.isnan(l2)
    paso = 0.5 * 10 ** (-_dec(txt))
    rel = 0.005 * abs(pub) if id_ in CON_PERCENTILES else 0.0
    return abs(l2 - pub) <= max(paso, rel) + 1e-9


def comparar() -> pd.DataFrame:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv", dtype=str, keep_default_na=False).set_index("id")
    filas = []
    for id_, f in FUNCIONES.items():
        v, lo, hi = (float(x) for x in f())
        r = ck.loc[id_]
        pv, pl, ph = (_num(r[k]) for k in ("valor", "min", "max"))
        ok = [coincide(a, b, r[k], id_) for a, b, k in ((v, pv, "valor"), (lo, pl, "min"), (hi, ph, "max"))]
        if all(ok):
            clase = "coincide"
        elif (not math.isnan(v) and not math.isnan(pl) and pl - 1e-9 <= v <= ph + 1e-9) or (math.isnan(v) and math.isnan(pv)):
            clase = "coincide dentro del rango"
        else:
            clase = "no coincide"
        filas.append({
            "id": id_, "pub_valor": pv, "pub_min": pl, "pub_max": ph,
            "l2_valor": v, "l2_min": lo, "l2_max": hi, "clase": clase, "diagnostico": DIAG[id_], "independencia": DEPENDIENTES.get(id_, "plena (solo anexo y data/raw)"),
        })
    return pd.DataFrame(filas)


if __name__ == "__main__":
    df = comparar()
    SALIDA.mkdir(parents=True, exist_ok=True)
    df.to_csv(SALIDA / "comparacion.csv", index=False)
    print(df.to_string())
