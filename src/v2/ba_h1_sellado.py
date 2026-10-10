"""H1 - evaluación sellada (PREPARADA, NO EJECUTADA por esta rama).

Se invoca UNA vez, tras la puerta del revisor, con:
    holdout.evaluate("H1", ba_h1_sellado.evaluar_H1, "BA", ["panel_prov_q", "nacional_q_v2"])
Este módulo no llama a holdout.evaluate ni lee data/sealed; al importarlo no hace nada.

Criterio pre-registrado (docs/v2/hipotesis.md): el modelo con las variables de H1 reduce el RMSE frente
al AR(4) de panel en 2024Q3-2026Q2 (DM-HLN). Modelo PRIMARIO fijado antes de ver resultados:
ba_lib.PRIMARIO = B_AR4_mas_H1 (AR(4) + Δ4 ln pob 20-34, Δ4 ln pob extranjera, Δ4 ln ocupados,
población en escalera = último 1 de enero observado: sin la fuga de la interpolación intra-anual).

Procedimiento: ventana expansiva estimada SOLO con objetivos <= 2024Q2 (embargo >= h=4 por construcción);
orígenes de test t con t+4 en 2024Q3-2026Q2. Las 3 provincias selladas (11, 16, 45) no están en
entrenamiento: su efecto fijo se estima con su propia historia hasta 2024Q2 (información disponible en t).
Se reportan: todas las unidades, provincias de entrenamiento y provincias selladas por separado.
"""
from __future__ import annotations

import contextlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ba_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402

PROVS_SELLADAS = ("11", "16", "45")


@contextlib.contextmanager
def _extender_ventana(tmax: str):
    """Las líneas base recortan a Q_TRAIN_FIN; durante la evaluación sellada se amplía (y se restaura)."""
    q0, prep0 = vc.Q_TRAIN_FIN, vc._prep

    def prep(df, col_u, tmax_=None):
        return prep0(df, col_u, tmax)
    vc.Q_TRAIN_FIN, vc._prep = tmax, prep
    try:
        yield
    finally:
        vc.Q_TRAIN_FIN, vc._prep = q0, prep0


def _concat(a: pd.DataFrame, b: pd.DataFrame, clave) -> pd.DataFrame:
    x = pd.concat([a, b], ignore_index=True)
    return x.drop_duplicates(clave, keep="first").reset_index(drop=True)


def evaluar_H1(sellado: dict, train: dict, q_fin_train: str = "2024Q2", cfg_nombre: str = bl.PRIMARIO) -> dict:
    pan = _concat(train["panel_prov_q"], sellado["panel_prov_q"], ["cod_prov", "trimestre"])
    nac = _concat(train["nacional_q_v2"], sellado["nacional_q_v2"], ["trimestre"])
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    pan["trimestre"] = pan["trimestre"].astype(str)
    nac["trimestre"] = nac["trimestre"].astype(str)
    tmax = str(max(pan["trimestre"].max(), nac["trimestre"].max()))
    tmax = min(tmax, "2026Q2")
    per = sorted(pan.loc[pan["trimestre"] <= tmax, "trimestre"].unique())
    h = 4
    posL = per.index(q_fin_train)
    orig = [i for i, q in enumerate(per) if q_fin_train < (per[i + h] if i + h < len(per) else "0")]
    # orígenes t cuyo objetivo t+h cae después de q_fin_train
    splits = [(np.arange(0, posL + 1), np.array(orig))]
    with _extender_ventana(tmax):
        # el entrenamiento usa orígenes s con s+h <= posL (lo fuerza _fit_predict): nada posterior entra
        m = bl.predecir_modelo(pan, cfg_nombre, bl.CONFIGS[cfg_nombre], splits=splits)
        ar4 = vc.panel_ar4(pan, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, splits=splits)
        ecm = vc.panel_ecm_v1(pan, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, splits=splits)
    com = bl.muestra_comun({cfg_nombre: m, vc.BASE: ar4, vc.ECM: ecm})
    salida = {"n_splits_omitidos_ecm": len(ecm.attrs.get("omitidos", [])), "tmax": tmax}
    for etq, filtro in (("todas", None), ("train_provs", lambda u: ~u.isin(PROVS_SELLADAS)),
                        ("provs_selladas", lambda u: u.isin(PROVS_SELLADAS))):
        fr = {k: (v if filtro is None else v[filtro(v["unidad"])]) for k, v in com.items()}
        if len(fr[cfg_nombre]) < 8:
            salida[etq] = {"n": int(len(fr[cfg_nombre]))}
            continue
        r = vc.evaluar(fr[cfg_nombre], {vc.BASE: fr[vc.BASE], vc.ECM: fr[vc.ECM]}, h)
        salida[etq] = {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v))
                       for k, v in r.iloc[0].to_dict().items()}
    t = salida["todas"]
    salida["H1_mejora_vs_AR4"] = bool(t.get("rmse", np.inf) < t.get("rmse_AR4", -np.inf)
                                      and t.get("dm_vs_AR4", -1) > 0 and t.get("p_vs_AR4", 1) < 0.05)
    return salida
