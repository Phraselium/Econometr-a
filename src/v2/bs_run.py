"""BS · punto de entrada. Uso: python3 src/v2/bs_run.py [--smoke]
Síntesis v2: Holm-7 (leído de ficheros), tablas, figura, informe_v2.md y resultado.json.
No estima nada: solo lee salidas versionadas de las ramas. Determinista, 1 hilo, SEED=20261010, sin red.
--smoke: submuestra (5 especificaciones por rama en el registro) y salidas en output/v2/BS/smoke/."""
from __future__ import annotations

import os
import sys
from pathlib import Path

for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(v, "1")
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import bs_figura as F  # noqa: E402
import bs_informe as I  # noqa: E402
import bs_lib as L  # noqa: E402
import bs_tablas as T  # noqa: E402
import holm7  # noqa: E402
import v2_common as vc  # noqa: E402
from econ_utils import Registry  # noqa: E402

SMOKE = "--smoke" in sys.argv
np.random.seed(L.SEED)


def main():
    bs = L.O / "BS" / ("smoke" if SMOKE else "")
    tab = bs / "tablas" if SMOKE else L.O / "tablas"
    tab.mkdir(parents=True, exist_ok=True)
    bs.mkdir(parents=True, exist_ok=True)

    holm = holm7.calcular(bs)                     # 1. Holm-7 leído de los ficheros de cada rama
    ha = T.t_hipotesis(holm)                      # 2a
    oos = T.t_oos()                               # 2b
    ctr = T.t_contrib()                           # 2c
    rank = T.t_ranking(holm)                      # 2d
    refs = T.t_refs()                             # 2e
    reg, regmeta = T.t_registro(SMOKE)            # 2f
    for nombre, df in (("hipotesis_confirmatorias", ha), ("modelos_fuera_muestra", oos), ("contribuciones_periodo", ctr),
                       ("ranking_factores", rank), ("referencias_v2", refs), ("registro_v2", reg)):
        df.to_csv(tab / f"{nombre}.csv", index=False, float_format="%.10g")

    fig = F.figura(bs / "contribuciones_periodo.png")   # 4. figura
    md = I.construir(holm, ha, oos, ctr, rank, refs, reg, regmeta, bs)   # 3. informe
    (bs / "informe_v2.md" if SMOKE else L.O / "informe_v2.md").write_text(md)

    # registro de BS: no se estima ninguna especificación (solo lectura/síntesis)
    Registry(bs / "registro.csv").flush()

    # 4. resultado.json
    h = holm.set_index("hipotesis")
    h1s = L.j("BA/h1_sellado.json")["resultado"]["todas"]
    k = I.pack(holm, ha, oos, ctr, rank, refs, reg, regmeta)
    vc.resultado_json(
        bs / "resultado.json",
        rama="BS",
        pregunta="Síntesis v2: ¿qué se asocia con el alquiler y con la compra, por periodo, y qué hipótesis confirmatorias sobreviven a Holm-7 y a la muestra sellada?",
        datos="Solo salidas versionadas de output/v2/{BA,BV,BI,BO,BP,BM,BD} y docs (sin data/sealed ni data/raw; sin estimación nueva)",
        N={"hipotesis_confirmatorias": 7, "modelos_fuera_muestra_filas": int(len(oos)), "contribuciones_filas": int(len(ctr)),
           "factores_ranking": int(len(rank)), "referencias": int(len(refs)), "especificaciones_v2": int(regmeta["total"])},
        metodo="Holm sobre las 7 confirmatorias (p = decisión pre-registrada, intersección-unión; con evaluación sellada, máximo de dentro de muestra y sellado), leyendo todos los p de los ficheros de rama; BH en tablas fuera de muestra cuando la rama no lo aporta",
        estimacion={f"p_hipotesis_{x}": float(h.loc[x, "p_hipotesis"]) for x in h.index},
        ic95=None,
        p_ajustado={f"holm7_{x}": float(h.loc[x, "p_holm7"]) for x in h.index},
        nivel_evidencia="EXPLORATORIO",
        diagnosticos={"supera_holm7": [x for x in h.index if bool(h.loc[x, "supera_holm7_5pct"])],
                      "etiquetas_finales": T.NIVEL_FIJADO,
                      "modelos_validacion_mejoran_AR4_con_BH": k["val_bh"], "modelos_validacion_mejoran_AR4_sin_corregir": k["val_raw"],
                      "sellados_principales_que_mejoran_AR4": k["sel_ok"],
                      "componentes_BD_no_robustos": int(ctr.no_robusto.sum()), "smoke": SMOKE},
        fuera_muestra={"modelo": "H1: AR(4)+variables demográficas (sellado, 52 provincias, 2024Q3-2026Q2)",
                       "rmse": float(h1s["rmse"]), "dm_vs_ar4": float(h1s["dm_vs_AR4"]),
                       "p_vs_ar4": float(h1s["p_vs_AR4"]), "rmse_ar4": float(h1s["rmse_AR4"]),
                       "dm_vs_ecm_v1": float(h1s["dm_vs_ECM_v1"]), "p_vs_ecm_v1": float(h1s["p_vs_ECM_v1"])},
        notas="Ninguna confirmatoria supera Holm-7; todas EXPLORATORIO (etiquetas del orquestador). La mejora predictiva sellada de H1 es un hecho fuera de muestra, no una asociación robusta de cada coeficiente. Se leen p de ficheros (holm7_verificacion.csv).")
    print(f"BS ok (smoke={SMOKE}): {bs}")


if __name__ == "__main__":
    main()
