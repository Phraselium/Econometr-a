"""Utilidades comunes de la auditoría de datos V16 (fase 1). Solo lectura de datos; escribe en output/v16/auditoria/."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[3]
SAL = RAIZ / "output" / "v16" / "auditoria"


def zrob(x):
    x = pd.Series(x, dtype=float)
    med = x.median()
    mad = (x - med).abs().median()
    if not mad or np.isnan(mad):
        return pd.Series(np.nan, index=x.index)
    return 0.6745 * (x - med) / mad


def escribe(familia: str, res: dict, informe: str):
    d = SAL / familia
    d.mkdir(parents=True, exist_ok=True)
    (d / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    (d / "informe.md").write_text(informe, encoding="utf-8")


def base_resultado(rama, pregunta, datos, N, metodo, diagnosticos, notas):
    return {"rama": rama, "pregunta": pregunta, "capa": "C4", "datos": datos, "N": N, "metodo": metodo,
            "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
            "diagnosticos": diagnosticos,
            "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": notas}
