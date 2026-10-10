"""H2 en la muestra sellada. NO SE EJECUTA desde la rama BV: la define y la dejan lista para que el
orquestador la llame UNA vez:  holdout.evaluate("H2", bv_h2_sellado.evaluar_H2, "BV", ["panel_prov_q", "nacional_q_v2"])

Modelo fijado ex ante (configuración elegida en validación en bloques sobre entrenamiento; ver
output/v2/BV/oos_panel.csv y resultado.json -> fuera_muestra): se lee de CONFIG_H2.
Contraste: RMSE del modelo vs AR(4) de panel (DM-HLN, h=4) en 2024Q3-2026Q2 (orígenes 2024Q3-2025Q2,
objetivos hasta 2026Q2), provincias de entrenamiento con filas selladas. Ajuste con información hasta 2024Q2.
La parte de provincias selladas (11, 16, 45) usa el mismo modelo con efecto fijo medio (provincia no vista).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bv_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402

CONFIG_H2 = json.loads((bl.OUT / "config_h2_sellado.json").read_text())["cfg"] \
    if (bl.OUT / "config_h2_sellado.json").exists() else "C3"
H = 4


def _core(pan_all, nac_all, cfg, tmax, train_fin, origen_ini, unidades_test=None):
    """Parchea temporalmente Q_TRAIN_FIN de v2_common (solo en memoria) para admitir periodos > 2024Q2.
    Entrenamiento con orígenes s tal que s+H <= train_fin; test = orígenes >= origen_ini con objetivo <= tmax."""
    old_q, old_def = vc.Q_TRAIN_FIN, vc._prep.__defaults__
    vc.Q_TRAIN_FIN = tmax
    vc._prep.__defaults__ = (tmax,)
    try:
        pan = bl.preparar_panel(pan_all, nac_all)   # recorta a <= Q_TRAIN_FIN (parcheado)
        pan = pan[pan["trimestre"] <= tmax]
        per = sorted(pan["trimestre"].unique())
        posL = per.index(train_fin)
        ite = np.array([i for i, p in enumerate(per) if p >= origen_ini and i + H < len(per)])
        splits = [(np.arange(0, posL + 1), ite)]
        kw = dict(splits=splits, desde=None, min_train=8)
        mod = bl.run_panel_model(pan, nac_all, cfg, **{"splits": splits, "min_train": 8})
        ar4 = vc.panel_ar4(pan, "p_tasado", "cod_prov", H, real=True, nac=nac_all, **kw)
        ecm = vc.panel_ecm_v1(pan, "p_tasado", "cod_prov", H, real=True, nac=nac_all, **kw)
    finally:
        vc.Q_TRAIN_FIN, vc._prep.__defaults__ = old_q, old_def
    if unidades_test is not None:
        mod, ar4, ecm = (x[x["unidad"].isin(unidades_test)] for x in (mod, ar4, ecm))
    return vc.evaluar(mod, {vc.BASE: ar4, vc.ECM: ecm}, H)


def evaluar_H2(sellado: dict, train: dict) -> dict:
    ps, pt = sellado["panel_prov_q"], train["panel_prov_q"]
    ns, nt = sellado["nacional_q_v2"], train["nacional_q_v2"]
    nac = pd.concat([nt, ns]).drop_duplicates("trimestre").sort_values("trimestre").reset_index(drop=True)
    sel_prov = sorted(set(ps["cod_prov"]) - set(pt["cod_prov"]))
    # (a) provincias de entrenamiento, trimestres sellados
    pa = pd.concat([pt, ps[~ps["cod_prov"].isin(sel_prov)]]).drop_duplicates(["cod_prov", "trimestre"])
    ra = _core(pa, nac, CONFIG_H2, "2026Q2", "2024Q2", "2024Q3")
    return {"cfg": CONFIG_H2, "provincias_selladas": sel_prov, "a_prov_train_trim_sellados": ra.to_dict("records"),
            "nota_b": "provincias selladas (11,16,45): requieren FE medio; no implementado aquí para no "
                      "introducir unidades sin entrenamiento en v2_common (ver limitaciones)"}
