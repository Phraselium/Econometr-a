"""BD - punto de entrada. Uso: python3 src/v2/bd_run.py [--smoke]
Salidas en output/v2/BD/ (smoke en output/v2/BD/smoke/). Determinista, 1 hilo, SEED=20261010, sin red.
Datos SOLO vía v2_common.load (entrenamiento <= 2024Q2). NO usa la muestra sellada."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bd_lib as L  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import econ_utils as eu  # noqa: E402

import bd_nacional as bn  # noqa: E402
import bd_panel as bp  # noqa: E402
import bd_report as br  # noqa: E402
import bd_texto as bt  # noqa: E402

SMOKE = "--smoke" in sys.argv
B = 49 if SMOKE else 999
OUT = L.OUT / ("smoke" if SMOKE else "")
OUT.mkdir(parents=True, exist_ok=True)


def guardar(df, nombre):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].round(7)
    df.to_csv(OUT / nombre, index=False)


def main():
    d = L.cargar_panel()
    provs = None
    if SMOKE:
        pr = sorted(d["cod_prov"].unique())
        provs = sorted(np.random.default_rng(L.SEED).choice(pr, 12, replace=False).tolist())
        print("SMOKE provincias:", provs)
    reg = eu.Registry(OUT / "registro.csv")
    res = {}
    k = 0
    for mercado in ("alquiler", "compra"):
        for modelo in ("M1", "M2"):
            k += 1
            res[(mercado, modelo)] = bp.decompone(d, mercado, modelo, B, L.SEED + 1000 * k, reg, provs=provs)
            print(mercado, modelo, "n", res[(mercado, modelo)]["n"], flush=True)
    tur = bp.decompone(d, "alquiler_turismo", "M1", B, L.SEED + 9000, reg, provs=provs, con_cf=False)
    contrib = pd.concat([r["contrib"] for r in res.values()], ignore_index=True)
    coef = pd.concat([r["coef"] for r in res.values()], ignore_index=True)
    cfdf = pd.concat([r["cf"] for r in res.values()], ignore_index=True)
    obsn = {m: bp.niveles_observados(d, m, provs) for m in ("alquiler", "compra")}
    guardar(contrib, "contribuciones_todas.csv")
    guardar(coef, "coeficientes_por_periodo.csv")
    guardar(cfdf, "contrafactuales.csv")
    guardar(tur["contrib"], "turismo_ventana_2021Q3_2024Q1.csv")
    guardar(tur["coef"], "turismo_coeficientes.csv")
    res_t = br.tabla_resumen(contrib)
    guardar(res_t, "tabla_resumen.csv")
    guardar(pd.DataFrame([dict(mercado=m, periodo=p, delta_ln_nivel_pp=v) for m, dd in obsn.items() for p, v in dd.items()]),
            "observado_niveles_referencia.csv")
    # nacional
    nac = bn.ejecutar(B, L.SEED + 5000, reg)
    guardar(nac["cp"], "nacional_corto_plazo.csv")
    guardar(nac["lp"], "nacional_largo_plazo.csv")
    guardar(nac["coef"], "nacional_coeficientes.csv")
    # figuras
    fd = OUT / "figuras"
    fd.mkdir(exist_ok=True)
    br.fig_apilada(contrib, "alquiler", fd / "descomposicion_alquiler.png", "Alquiler (IPC alquiler, nominal): descomposición por periodo")
    br.fig_apilada(contrib, "compra", fd / "descomposicion_compra.png", "Compra (valor tasado real): descomposición por periodo")
    br.fig_bosque(contrib, "alquiler", "M1", fd / "ic_alquiler_M1.png", "Alquiler: contribuciones con IC95")
    br.fig_bosque(contrib, "compra", "M1", fd / "ic_compra_M1.png", "Compra: contribuciones con IC95")
    br.fig_nacional(nac["cp"], nac["lp"], fd / "descomposicion_nacional_ecm.png")
    reg.flush()
    ctx = dict(res=res, tur=tur, contrib=contrib, cf=cfdf, coef=coef, resumen=res_t, nac=nac, obsn=obsn, B=B, smoke=SMOKE,
               OUT=OUT)
    bt.escribir(ctx)
    print("OK", OUT)


if __name__ == "__main__":
    main()
