"""H2 en la muestra sellada. NO SE EJECUTA desde la rama BV. El orquestador la llama UNA vez:
    holdout.evaluate("H2", bv_h2_sellado.evaluar_H2, "BV", ["panel_prov_q", "nacional_q_v2"])

DISEÑO FIJADO ANTES DE LA LLAMADA
* Modelo: C3 = AR(4) de panel (4 retardos de Δln precio real) + Δ4 ln hipotecas_importe + Δ4 ln ocupados +
  coste_uso_aprox + coste_uso×exposición 2005-07, directo a h=4, FE de provincia y dummies de trimestre.
  Es el modelo con las variables de H2 del pre-registro; NO se elige por RMSE (C1 era el de menor RMSE
  en entrenamiento, pero no contiene las variables de H2; elegir entre configuraciones es tarea de H7).
* Ajuste con información hasta L=2024Q2 (orígenes s con s+4 <= L). Pendientes: 49 provincias de
  entrenamiento. Orígenes de test: 2023Q3-2025Q2 (8), objetivos 2024Q3-2026Q2; en cada origen solo
  se usan regresores fechados <= origen. Se aborta (sin devolver nada) si n_periodos < 8.
* Provincias selladas (11, 16, 45): mismas pendientes; efecto fijo propio = media del residuo
  (y - x'b sin FE) en su historia con objetivos <= L. Se aplica por igual al modelo y al AR(4).
* Exposición 2005-07: estandarizada con media y DE de las 49 provincias de entrenamiento.
* CONTRASTE PRINCIPAL: 52 provincias, ventana 2024Q3-2026Q2, DM-HLN (h=4) sobre la diferencia de pérdidas
  cuadráticas promediada por periodo (v2_common.evaluar), bilateral, t(n-1). H2 fuera de muestra se
  cumple si RMSE_C3 < RMSE_AR4 y p < 0,05; entra luego en el Holm de las 7 confirmatorias.
* SECUNDARIOS (informativos, no deciden): (a) 49 provincias de entrenamiento; (b) solo 11, 16, 45 en la
  ventana; (b') solo 11, 16, 45 con orígenes 2012Q1-2023Q2 (coeficientes por split de la validación en
  bloques, FE con objetivos <= L del split); (c) ECM v1 de panel como referencia en las 49.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bv_lib as bl  # noqa: E402
import v2_common as vc  # noqa: E402

CFG = "C3"
H = 4
L_REAL, FIN_REAL = "2024Q2", "2026Q2"
ORIGEN_INI_REAL, ORIGEN_FIN_REAL = "2023Q3", "2025Q2"
N_MIN_PERIODOS = 8
_NOMB = {"C3": "BV_C3"}


def _preparar_long(pan_all, nac, tmax, expo_ref):
    d = bl.preparar_panel(pan_all, nac, tmax=tmax, expo_ref=expo_ref).replace([np.inf, -np.inf], np.nan)
    d["unidad"] = d["cod_prov"].astype(str)
    long, per, units = vc._grid(d, lambda x: x["ln_p_real"])
    lvl = long["lvl"]
    long["dY"] = lvl - vc._g(long, lvl, 1)
    long["yh"] = vc._g(long, lvl, -H) - lvl
    return long, per, units


def _predecir(long, per, units_train, units_sealed, cfg, posL, origen_pos):
    """Predicciones directas a h=4 del modelo `cfg` y del AR(4) para todas las unidades en `origen_pos`.
    Pendientes y FE de entrenamiento: unidades `units_train` con pos+H <= posL. FE de las selladas: media del
    residuo en su historia con pos+H <= posL."""
    out = []
    for nombre, feat in ((_NOMB[cfg], bl.feat_panel(cfg)), (vc.BASE, vc._feat_ar4)):
        lg = long.copy()
        fcols = list(feat(lg))
        ok = lg[fcols].notna().all(axis=1)
        tr = (lg["pos"] + H <= posL) & lg["yh"].notna() & ok & lg["unidad"].isin(units_train)
        Xtr = vc._design(lg, tr, fcols, units_train, H)
        beta = pd.Series(np.linalg.lstsq(Xtr.values, lg.loc[tr, "yh"].values, rcond=None)[0], index=Xtr.columns)
        slope_cols = [c for c in Xtr.columns if not c.startswith("u_")]
        te = lg["pos"].isin(origen_pos) & ok & lg["yh"].notna()
        sub = lg.loc[te]
        Xte = vc._design(lg, te, fcols, units_train, H)
        base_pred = Xte[slope_cols].values @ beta[slope_cols].values
        alpha = sub["unidad"].map(lambda u: beta.get(f"u_{u}", np.nan)).values.astype(float)
        for u in units_sealed:
            rows = (lg["pos"] + H <= posL) & lg["yh"].notna() & ok & (lg["unidad"] == u)
            if rows.sum() == 0:
                continue
            Xu = vc._design(lg, rows, fcols, units_train, H)
            res = lg.loc[rows, "yh"].values - Xu[slope_cols].values @ beta[slope_cols].values
            alpha[(sub["unidad"] == u).values] = res.mean()
        pred = base_pred + alpha
        out.append(pd.DataFrame({"periodo": sub["trimestre"].values,
                                 "periodo_obj": [per[p + H] if p + H < len(per) else None for p in sub["pos"]],
                                 "unidad": sub["unidad"].values, "y_real": sub["yh"].values, "y_pred": pred,
                                 "modelo": nombre, "split": 0, "h": H}).dropna(subset=["y_pred"]))
    return out[0], out[1]


def _resumen(mod, ar4, unidades=None, extra_base=None):
    if unidades is not None:
        mod, ar4 = mod[mod["unidad"].isin(unidades)], ar4[ar4["unidad"].isin(unidades)]
        if extra_base is not None:
            extra_base = extra_base[extra_base["unidad"].isin(unidades)]
    bases = {vc.BASE: ar4} if extra_base is None else {vc.BASE: ar4, vc.ECM: extra_base}
    r = vc.evaluar(mod, bases, H).iloc[0].to_dict()
    r["cumple_regla"] = bool(r["rmse"] < r["rmse_AR4"] and r["p_vs_AR4"] < 0.05)
    return {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in r.items()}


def _ecm_ref(pan49, nac, tmax, train_fin, o_ini, o_fin):
    """ECM v1 de panel (referencia) en las provincias de entrenamiento; parchea en memoria Q_TRAIN_FIN."""
    old_q, old_def = vc.Q_TRAIN_FIN, vc._prep.__defaults__
    vc.Q_TRAIN_FIN, vc._prep.__defaults__ = tmax, (tmax,)
    try:
        per = sorted(pan49.loc[pan49["trimestre"] <= tmax, "trimestre"].unique())
        posL = per.index(train_fin)
        ite = np.array([i for i, p in enumerate(per) if o_ini <= p <= o_fin])
        return vc.panel_ecm_v1(pan49, "p_tasado", "cod_prov", H, real=True, nac=nac,
                               splits=[(np.arange(0, posL + 1), ite)], min_train=8)
    finally:
        vc.Q_TRAIN_FIN, vc._prep.__defaults__ = old_q, old_def


def _evaluar(sellado, train, L, fin, o_ini, o_fin, cfg=CFG, primer_test_hist="2012Q1"):
    ps, pt = sellado["panel_prov_q"], train["panel_prov_q"]
    ns, nt = sellado["nacional_q_v2"], train["nacional_q_v2"]
    nac = pd.concat([nt, ns]).drop_duplicates("trimestre").sort_values("trimestre").reset_index(drop=True)
    units_train = sorted(pt["cod_prov"].astype(str).unique())
    units_sealed = sorted(set(ps["cod_prov"].astype(str)) - set(units_train))
    pan_all = pd.concat([pt, ps]).drop_duplicates(["cod_prov", "trimestre"]).sort_values(["cod_prov", "trimestre"])
    # la exposición usa solo 2005-07 (anterior a cualquier origen); parámetros de las provincias de entrenamiento
    ref = bl.exposicion_ref(pt)
    long, per, _ = _preparar_long(pan_all, nac, fin, ref)
    posL = per.index(L)
    origen_pos = [i for i, p in enumerate(per) if o_ini <= p <= o_fin]
    mod, ar4 = _predecir(long, per, units_train, units_sealed, cfg, posL, origen_pos)
    n_per = mod.dropna(subset=["y_real"])["periodo"].nunique()
    if n_per < N_MIN_PERIODOS:
        raise RuntimeError(f"abortado: n_periodos={n_per} < {N_MIN_PERIODOS}; el DM-HLN no sería calculable")
    todas = units_train + units_sealed
    res = {"cfg": cfg, "regla": "RMSE_modelo < RMSE_AR4 y p < 0,05 (principal: todas las provincias)",
           "provincias_entrenamiento": len(units_train), "provincias_selladas": units_sealed,
           "PRINCIPAL_todas": _resumen(mod, ar4, todas),
           "sec_a_entrenamiento": _resumen(mod, ar4, units_train)}
    if units_sealed:
        res["sec_b_selladas_ventana"] = _resumen(mod, ar4, units_sealed)
    # (b') selladas, historia 2012Q1-L con coeficientes por split de la validación en bloques
    if units_sealed:
        pers_tr = per[:posL + 1]
        sp = vc.block_splits(pers_tr, H, 4, 4, 8, first_test=primer_test_hist)
        ms, as_ = [], []
        for itr, ite in sp:
            m_, a_ = _predecir(long, per, units_train, units_sealed, cfg, int(itr[-1]), ite.tolist())
            ms.append(m_[m_["unidad"].isin(units_sealed)])
            as_.append(a_[a_["unidad"].isin(units_sealed)])
        mh, ah = pd.concat(ms, ignore_index=True), pd.concat(as_, ignore_index=True)
        res["sec_b2_selladas_historia"] = _resumen(mh, ah)
    # (c) ECM v1 de panel en entrenamiento (referencia)
    try:
        pan49 = pan_all[pan_all["cod_prov"].isin(units_train)]
        ecm = _ecm_ref(pan49, nac, fin, L, o_ini, o_fin)
        m49, a49 = mod[mod["unidad"].isin(units_train)], ar4[ar4["unidad"].isin(units_train)]
        res["sec_c_ecm_v1_referencia_entrenamiento"] = _resumen(m49, a49, None, ecm)
    except Exception as e:  # noqa: BLE001  (secundario: no debe impedir devolver el contraste principal)
        res["sec_c_ecm_v1_referencia_entrenamiento"] = f"no disponible: {type(e).__name__}: {e}"
    return res


def evaluar_H2(sellado: dict, train: dict) -> dict:
    """Función para holdout.evaluate("H2", ...). Parámetros fijos del diseño (ver docstring del módulo)."""
    return _evaluar(sellado, train, L_REAL, FIN_REAL, ORIGEN_INI_REAL, ORIGEN_FIN_REAL)


if __name__ == "__main__":
    raise SystemExit("solo vía holdout.evaluate('H2', evaluar_H2, 'BV', [...])")
