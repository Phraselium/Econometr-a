"""V16 fase 6, grupo C · utilidades comunes de Q5, Q9, Q10 y la rejilla. Solo entrenamiento; sin efectos al importar.

Todo es C4 y «pendiente de evaluación sellada». Sin lenguaje causal. Importa q_comun (grupo A) sin modificarlo.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.v16 import q_comun as Q  # noqa: E402

SEED = Q.SEED
OUTD = ROOT / "output" / "v16"
FECHA = Q.CORTE


def nat_q(archivo: str, variable: str, nivel: str = "nacional") -> pd.Series:
    """Serie trimestral (PeriodIndex Q) de una variable nacional del entrenamiento."""
    d = Q.trimestral(Q.cargar(archivo, nivel, variable))
    return d.groupby("q").valor.last().sort_index()


def nat_m(archivo: str, variable: str) -> pd.Series:
    d = Q.cargar(archivo, "nacional", variable)
    d = d[d.periodo.astype(str).str.match(r"^\d{4}-\d{2}$")]
    d = d.assign(m=pd.PeriodIndex(d.periodo.astype(str), freq="M"))
    return d.groupby("m").valor.last().sort_index()


def prov_q(archivo: str, variable: str) -> pd.DataFrame:
    """Panel trimestral provincial: filas = trimestre, columnas = provincia."""
    d = Q.trimestral(Q.cargar(archivo, "provincia", variable))
    return d.pivot_table(index="q", columns="territorio_codigo", values="valor", aggfunc="last").sort_index()


def prov_a(archivo: str, variable: str) -> pd.DataFrame:
    """Panel anual provincial (periodos 'AAAA')."""
    d = Q.cargar(archivo, "provincia", variable)
    d = d[d.periodo.astype(str).str.fullmatch(r"\d{4}")]
    d = d.assign(t=d.periodo.astype(str).astype(int))
    return d.pivot_table(index="t", columns="territorio_codigo", values="valor", aggfunc="last").sort_index()


def dlog(s: pd.Series, k: int = 1) -> pd.Series:
    return np.log(s).diff(k)


def hecho(i, q, indicador, valor, mn, mx, unidad, periodo, cobertura, fuentes, ancla, fecha=None):
    return {"id": f"V16-{q}-{i}", "indicador": indicador, "valor": valor, "min": mn, "max": mx, "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "fecha_dato": fecha or FECHA,
            "ficha": f"output/v16/{q.lower().split('-')[0]}/informe.md#{ancla}"}


def resultado(rama, pregunta, datos, N, metodo, estimacion, diag, notas, p_by, extra=None, ic95=None, nivel="DESCRIPTIVO"):
    r = {"rama": f"v16/{rama}", "pregunta": pregunta, "capa": "C4", "datos": datos, "N": N, "metodo": metodo, "estimacion": estimacion,
         "ic95": ic95, "p_ajustado": {"metodo": "sin corrección aquí: el control Benjamini-Yekutieli lo aplica el orquestador", "valores": []},
         "p_valores_para_BY": p_by, "nivel_evidencia": nivel, "diagnosticos": diag,
         "fuera_muestra": {"modelo": "no aplica (no es predicción)", "rmse": None, "dm_vs_ar4": None}, "pendiente_sellada": True,
         "regla_hallazgo": {"a_q_menor_0_10": "pendiente (BY del orquestador; p null si NO APTO)", "b_error_S_M": "no evaluable sin errores típicos válidos",
                            "c_sellada": "pendiente", "resultado": "estimación C4 pendiente de evaluación sellada; sin lenguaje causal"},
         "notas": notas}
    if extra:
        r.update(extra)
    return r


def diag(prueba, estado, detalle):
    return {"prueba": prueba, "estado": estado, "detalle": detalle}


def f(x, d=3):
    return "n/d" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{d}f}".replace(".", ",")
