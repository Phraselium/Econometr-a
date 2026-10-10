"""H7 en la muestra sellada (PREPARADA, NO EJECUTADA por la rama BM). El orquestador la llama UNA vez tras la puerta:
    holdout.evaluate("H7", bm_h7_sellado.evaluar_H7, "BM", ["panel_prov_q", "nacional_q_v2"])
Este módulo NO llama a holdout.evaluate ni lee data/sealed; al importarlo no hace nada.

MODELOS FIJADOS ANTES DE LA LLAMADA: output/v2/BM/seleccion_H7.json (UN modelo por objetivo, elegido con la regla de
output/v2/BM/regla_H7.md sobre la validación en bloques de entrenamiento). Objetivos: A nacional ln IPV real, B panel
IPC alquiler, C panel p_tasado real; h=4, y = ln X_{t+4} - ln X_t.

PROCEDIMIENTO (criterio uniforme con BA/BV)
* Parámetros SOLO con unidades de entrenamiento (49 provincias) y objetivos <= 2024Q2. Las provincias selladas
  (11, 16, 45) reciben un efecto fijo propio: media del residuo y - f(x) en su historia con objetivos <= 2024Q2
  (igual en el modelo, AR(4) y ECM v1: se reutilizan los parches de ba_h1_sellado._parches).
* Orígenes 2023Q3-2025Q2 (8; objetivos 2024Q3-2026Q2); se aborta si n_periodos < 8 (DM-HLN no calculable).
* Contraste por objetivo: DM-HLN (h=4, pérdida cuadrática; panel: media transversal por periodo) del modelo frente a
  AR(4) y frente a ECM v1 en la MISMA muestra.

REGLA DE DECISIÓN (declarada antes)
* Principal: A = serie nacional; B y C = 52 provincias. Un objetivo CUMPLE si RMSE(modelo) < RMSE(AR4) y < RMSE(ECM v1),
  DM > 0 frente a ambos y p_IUT = max(p_AR4, p_ECM) significativa tras Holm (m=3 objetivos, alfa 0,05).
* H7 se cumple si algún objetivo cumple. Secundarios informativos (no deciden): 49 provincias de entrenamiento; solo
  selladas en la ventana; (b') solo selladas en toda su historia (bloques con embargo, objetivos <= 2024Q2).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ba_h1_sellado as bas  # noqa: E402  (solo _parches: ampliación de ventana y FE de selladas en las líneas base)
import bm_lib as bl  # noqa: E402
import bm_modelos as bm  # noqa: E402
import v2_common as vc  # noqa: E402

H = 4
L_REAL, FIN_REAL = "2024Q2", "2026Q2"
ORIGEN_INI_REAL, ORIGEN_FIN_REAL = "2023Q3", "2025Q2"
N_MIN_PERIODOS = 8
SEL_FILE = bl.OUT / "seleccion_H7.json"
OBJ = {"B": ("ipc_alquiler", False), "C": ("p_tasado", True)}


def _spec(nombre):
    for s in bl.specs_enet() + [bl.SPEC_PL] + bl.specs_rf() + bl.specs_lgbm():
        if s.nombre == nombre:
            return s
    raise KeyError(nombre)


def _concat(a, b, clave):
    x = pd.concat([a, b], ignore_index=True)
    return x.drop_duplicates(clave, keep="first").reset_index(drop=True)


def _modelo(o, sel, long, per, cols, splits, units_train, sell, nac, tmax):
    """Predicciones del modelo seleccionado en `splits` (formato v2_common)."""
    clase, nombre, cfg = sel["clase"], sel["modelo"], sel["config"]
    if clase in ("enet", "postlasso", "rf", "lgbm"):
        spec = _spec(nombre)
        rows = []
        for sid, (itr, ite) in enumerate(splits):
            posL = int(itr[-1])
            f = bl.ajustar(long, posL, cols, spec, units_train)
            if f is None:
                continue
            r = bl.predecir_filas(f, long, posL, ite, units_train, sorted(sell))
            if r is None:
                continue
            sub, raw, fe = r
            rows.append(bl.a_frame(sub, raw + fe, per, "MODELO_H7", sid))
        return pd.concat(rows, ignore_index=True) if rows else bm._vacio()
    lg, pr, _ = bm._long_ecm(nac, tmax)
    assert pr == per
    if clase == "ardl":
        m = bm.ardl(lg, pr, splits, "MODELO_H7")
    elif clase == "tar_ecm":
        m = bm.tar_ecm(lg, pr, splits, cfg["umbral"], "MODELO_H7")
    elif clase == "bvar":
        m = bm.var_modelos(lg, pr, splits, ["dY", "dOcup", "dTipoR", "dCred"], "bvar", cfg["lambda"], "MODELO_H7")
    elif clase == "tvpvar":
        m = bm.var_modelos(lg, pr, splits, ["dY", "dOcup", "dTipoR", "dCred"], "tvp", cfg["kappa"], "MODELO_H7")
    else:
        raise ValueError(clase)
    return m


def _frames(o, sel, pan, nac, units_train, sell, tmax, split_fn):
    """(modelo, AR4, ECM v1, per) con los parches de ventana/FE de selladas activos."""
    with bas._parches(tmax, sell):
        if o == "A":
            d = bl.preparar_nacional(nac, tmax)
            long, per, _, cols = bl.construir_long(d, "A", bl.familias_con_ar(bl.FAM_NAC))
            splits = split_fn(per)
            a = vc.ar4_nacional(nac, "ln_ipv", H, real=True, splits=splits)
            e = vc.ecm_v1_nacional(nac, H, splits=splits)
            m = _modelo(o, sel, long, per, cols, splits, ["ES"], set(), nac, tmax)
        else:
            var, real = OBJ[o]
            d = bl.preparar_panel(pan, nac, o, tmax)
            long, per, _, cols = bl.construir_long(d, o, bl.familias_con_ar(bl.FAM_PANEL), nac)
            splits = split_fn(per)
            a = vc.panel_ar4(pan, var, "cod_prov", H, real=real, nac=nac, splits=splits)
            e = vc.panel_ecm_v1(pan, var, "cod_prov", H, real=real, nac=nac, splits=splits)
            m = _modelo(o, sel, long, per, cols, splits, units_train, sell, nac, tmax)
    return m, a, e, per


def _resumen(m, a, e, unidades=None):
    if unidades is not None:
        m, a, e = (x[x["unidad"].isin(unidades)] for x in (m, a, e))
    r = vc.evaluar(m, {vc.BASE: a, vc.ECM: e}, H).iloc[0].to_dict()
    r = {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v)) for k, v in r.items()}
    both = r["rmse"] < r["rmse_AR4"] and r["rmse"] < r["rmse_ECM_v1"] and r["dm_vs_AR4"] > 0 and r["dm_vs_ECM_v1"] > 0
    r["p_IUT"] = max(r["p_vs_AR4"], r["p_vs_ECM_v1"]) if both else 1.0
    return r


def _holm(ps: dict, alfa=0.05):
    items = sorted(ps.items(), key=lambda kv: (np.nan_to_num(kv[1], nan=1.0), kv[0]))
    m, rechaza, parar = len(items), {}, False
    adj, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        p = 1.0 if np.isnan(p) else p
        run = max(run, min(1.0, p * (m - i)))
        adj[k] = run
        if parar or p > alfa / (m - i):
            parar = True
        rechaza[k] = not parar
    return adj, rechaza


def _evaluar(sellado, train, L, fin, o_ini, o_fin, seleccion=None, hist_ini="2012Q1"):
    seleccion = seleccion or json.loads(SEL_FILE.read_text())
    pan = _concat(train["panel_prov_q"], sellado["panel_prov_q"], ["cod_prov", "trimestre"])
    nac = _concat(train["nacional_q_v2"], sellado["nacional_q_v2"], ["trimestre"])
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    pan["trimestre"] = pan["trimestre"].astype(str)
    nac["trimestre"] = nac["trimestre"].astype(str)
    pan = pan.sort_values(["cod_prov", "trimestre"]).reset_index(drop=True)
    units_train = sorted(train["panel_prov_q"]["cod_prov"].astype(str).unique())
    sell = set(sellado["panel_prov_q"]["cod_prov"].astype(str)) - set(units_train)

    def split_main(per):
        posL = per.index(L)
        orig = [i for i, p in enumerate(per) if o_ini <= p <= o_fin and i + H < len(per)]
        return [(np.arange(0, posL + 1), np.array(orig))]

    res = {"L": L, "fin": fin, "selladas": sorted(sell), "seleccion": {o: seleccion[o]["modelo"] for o in "ABC"},
           "regla": "objetivo cumple: RMSE<AR4 y <ECM v1, DM>0 ambos, p_IUT=max(p) con Holm m=3 < 0,05; H7 si alguno"}
    pint = {}
    for o in "ABC":
        sel = seleccion[o]
        m, a, e, per = _frames(o, sel, pan, nac, units_train, sell, fin, split_main)
        npd = int(m.dropna(subset=["y_real", "y_pred"])["periodo"].nunique())
        if npd < N_MIN_PERIODOS:
            raise RuntimeError(f"abortado: objetivo {o} con n_periodos={npd} < {N_MIN_PERIODOS}; DM-HLN no calculable")
        r = {"modelo": sel["modelo"], "clase": sel["clase"],
             "PRINCIPAL": _resumen(m, a, e, None if o != "A" else None)}
        if o != "A":
            r["sec_a_entrenamiento_49"] = _resumen(m, a, e, units_train)
            if sell:
                r["sec_b_selladas_ventana"] = _resumen(m, a, e, sorted(sell)) if \
                    m[m["unidad"].isin(sell)]["periodo"].nunique() >= 8 else "n < 8 periodos"
                # (b') selladas en toda su historia (bloques con embargo; objetivos <= L; datos recortados a L)
                pb = pan[pan["trimestre"] <= L]
                nb = nac[nac["trimestre"] <= L]

                def split_hist(per):
                    return vc.block_splits(per, H, 4, 4, 8, first_test=hist_ini)
                mb, ab, eb, perb = _frames(o, sel, pb, nb, units_train, sell, L, split_hist)
                keep = [x[x["periodo_obj"].astype(str) <= L] for x in (mb, ab, eb)]
                r["sec_b2_selladas_historia"] = _resumen(*keep, sorted(sell))
        r["p_IUT"] = r["PRINCIPAL"]["p_IUT"]
        pint[o] = r["p_IUT"]
        res[o] = r
    adj, rech = _holm(pint)
    for o in "ABC":
        res[o]["p_IUT_Holm_m3"] = adj[o]
        res[o]["cumple"] = bool(rech[o])
    res["H7_cumple"] = bool(any(rech.values()))
    return res


def evaluar_H7(sellado: dict, train: dict) -> dict:
    """Función para holdout.evaluate("H7", ...). Parámetros fijos del diseño (ver docstring del módulo)."""
    return _evaluar(sellado, train, L_REAL, FIN_REAL, ORIGEN_INI_REAL, ORIGEN_FIN_REAL)


if __name__ == "__main__":
    raise SystemExit("solo vía holdout.evaluate('H7', evaluar_H7, 'BM', ['panel_prov_q', 'nacional_q_v2'])")
