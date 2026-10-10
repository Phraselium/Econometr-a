"""H1 - evaluación sellada (PREPARADA, NO EJECUTADA por esta rama).

Se invoca UNA vez, tras la puerta del revisor, con:
    holdout.evaluate("H1", ba_h1_sellado.evaluar_H1, "BA", ["panel_prov_q", "nacional_q_v2"])
Este módulo no llama a holdout.evaluate ni lee data/sealed; al importarlo no hace nada.

Modelo PRIMARIO fijado antes de ver resultados: ba_lib.PRIMARIO = B_AR4_mas_H1 (AR(4) + Δ4 ln pob 20-34,
Δ4 ln pob extranjera, Δ4 ln ocupados; población en escalera = último 1 de enero observado).

Procedimiento (criterio uniforme con BV)
* PENDIENTES (y DOLS del ECM v1) estimadas SOLO con las 49 provincias de entrenamiento y objetivos <= 2024Q2.
* Provincias selladas (las que están en `sellado` y no en `train`: 11, 16, 45): su efecto fijo es la media del
  residuo en su PROPIA historia con objetivos <= 2024Q2 (no influyen en las pendientes); igual para B, AR(4) y ECM v1.
* Orígenes t con t+4 en 2024Q3-2026Q2. Se exige n_periodos >= 8 en el contraste principal (si no, ValueError).

REGLA DE DECISIÓN (declarada antes de la llamada)
* Contraste PRINCIPAL ÚNICO = clave "todas" (49 + 3 provincias, objetivos 2024Q3-2026Q2): H1 se cumple en la parte
  sellada si rmse(B) < rmse(AR4) y DM-HLN > 0 y p bilateral < 0,05.
* SECUNDARIOS (informativos, no deciden): "train_provs" (49), "selladas_ventana" (3, mismo periodo) y
  "selladas_toda_historia" (b'; 3 provincias, orígenes con primer test 2012Q1 y bloques con embargo, objetivos <= 2024Q2).
* Pasar este contraste NO eleva H1 a ROBUSTA: H1 (conjunta) ya falla en entrenamiento (la población extranjera no es +).
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
def _parches(tmax: str, sell: set):
    """(1) amplía la ventana de las líneas base a tmax; (2) pendientes/DOLS solo con provincias de
    entrenamiento y efecto fijo de las selladas desde su propia historia. Se restauran al salir."""
    q0, prep0, fit0, dols0 = vc.Q_TRAIN_FIN, vc._prep, vc._fit_predict, vc._dols

    def prep(df, col_u, tmax_=None):
        return prep0(df, col_u, tmax)

    def dols(long, posL, ycol, xcols, units, k_max=2):
        tr = long[~long["unidad"].isin(sell)]
        r = dols0(tr, posL, ycol, xcols, [u for u in units if u not in sell], k_max)
        if r is None:
            return None
        ect, meta = r
        co = meta["coef"]
        bx = np.array([co[x] for x in xcols])
        bq = np.array([co["q2"], co["q3"], co["q4"]])

        def ect2(lg):
            out = ect(lg).copy()
            q = vc._qdum(lg["trimestre"].values)
            q.index = lg.index
            rest = lg[ycol] - (lg[xcols].values * bx).sum(axis=1) - (q.values * bq).sum(axis=1)
            for u in sell:
                m = lg["unidad"] == u
                alpha = rest[m & (lg["pos"] <= posL)].mean()
                out[m] = rest[m] - alpha
            return out
        return ect2, meta

    def fit(long, posL, test_pos, fcols, units, h, min_extra=4):
        tr_units = [u for u in units if u not in sell]
        lt = long[~long["unidad"].isin(sell)]
        res = fit0(lt, posL, test_pos, fcols, tr_units, h, min_extra)
        if res is None:
            return None
        pred, cf = res
        beta = pd.Series(cf)
        parts = [pred]
        for u in sorted(sell):
            lu = long["unidad"] == u
            ok = long[fcols].notna().all(axis=1)
            te = lu & long["pos"].isin(test_pos) & ok
            hist = lu & (long["pos"] + h <= posL) & long["yh"].notna() & ok
            if not te.any() or hist.sum() < 4:
                continue
            Xh = vc._design(long, hist, fcols, tr_units, h)[beta.index]
            alpha = float((long.loc[hist, "yh"].values - Xh.values @ beta.values).mean())
            Xt = vc._design(long, te, fcols, tr_units, h)[beta.index]
            parts.append(pd.Series(Xt.values @ beta.values + alpha, index=Xt.index))
        return pd.concat(parts), cf

    vc.Q_TRAIN_FIN, vc._prep, vc._fit_predict, vc._dols = tmax, prep, fit, dols
    try:
        yield
    finally:
        vc.Q_TRAIN_FIN, vc._prep, vc._fit_predict, vc._dols = q0, prep0, fit0, dols0


def _concat(a: pd.DataFrame, b: pd.DataFrame, clave) -> pd.DataFrame:
    x = pd.concat([a, b], ignore_index=True)
    return x.drop_duplicates(clave, keep="first").reset_index(drop=True)


def _resumen(fr, cfg_nombre, h=4):
    r = vc.evaluar(fr[cfg_nombre], {vc.BASE: fr[vc.BASE], vc.ECM: fr[vc.ECM]}, h)
    return {k: (float(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v))
            for k, v in r.iloc[0].to_dict().items()}


def evaluar_H1(sellado: dict, train: dict, q_fin_train: str = "2024Q2", cfg_nombre: str = bl.PRIMARIO) -> dict:
    pan = _concat(train["panel_prov_q"], sellado["panel_prov_q"], ["cod_prov", "trimestre"])
    nac = _concat(train["nacional_q_v2"], sellado["nacional_q_v2"], ["trimestre"])
    pan["cod_prov"] = pan["cod_prov"].astype(str)
    pan["trimestre"] = pan["trimestre"].astype(str)
    nac["trimestre"] = nac["trimestre"].astype(str)
    sell = set(sellado["panel_prov_q"]["cod_prov"].astype(str)) - set(train["panel_prov_q"]["cod_prov"].astype(str))
    tmax = min(str(max(pan["trimestre"].max(), nac["trimestre"].max())), "2026Q2")
    per = sorted(pan.loc[pan["trimestre"] <= tmax, "trimestre"].unique())
    h = 4
    posL = per.index(q_fin_train)
    orig = [i for i in range(len(per)) if i + h < len(per) and per[i + h] > q_fin_train]
    splits = [(np.arange(0, posL + 1), np.array(orig))]
    with _parches(tmax, sell):
        m = bl.predecir_modelo(pan, cfg_nombre, bl.CONFIGS[cfg_nombre], splits=splits)
        ar4 = vc.panel_ar4(pan, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, splits=splits)
        ecm = vc.panel_ecm_v1(pan, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, splits=splits)
    com = bl.muestra_comun({cfg_nombre: m, vc.BASE: ar4, vc.ECM: ecm})
    salida = {"n_omitidos_ecm": len(ecm.attrs.get("omitidos", [])), "tmax": tmax, "selladas": sorted(sell)}
    filtros = (("todas", None), ("train_provs", lambda u: ~u.isin(sell)), ("selladas_ventana", lambda u: u.isin(sell)))
    for etq, filtro in filtros:
        fr = {k: (v if filtro is None else v[filtro(v["unidad"])]) for k, v in com.items()}
        npd = int(fr[cfg_nombre]["periodo"].nunique())
        if etq == "todas" and npd < 8:
            raise ValueError(f"contraste principal con n_periodos={npd} < 8")
        salida[etq] = _resumen(fr, cfg_nombre) if (npd >= 8 and len(fr[cfg_nombre]) >= 8) else {"n": len(fr[cfg_nombre])}
    # (b') provincias selladas en toda su historia (objetivos <= q_fin_train), bloques con embargo
    pb = pan[pan["trimestre"] <= q_fin_train]
    kw = dict(desde="2012Q1", min_train=36)
    with _parches(q_fin_train, sell):
        mb = bl.predecir_modelo(pb, cfg_nombre, bl.CONFIGS[cfg_nombre], **kw)
        ab = vc.panel_ar4(pb, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, **kw)
        eb = vc.panel_ecm_v1(pb, "ipc_alquiler", "cod_prov", h, real=False, nac=nac, **kw)
    cb = bl.muestra_comun({cfg_nombre: mb, vc.BASE: ab, vc.ECM: eb})
    fb = {k: v[v["unidad"].isin(sell)] for k, v in cb.items()}
    salida["selladas_toda_historia"] = (_resumen(fb, cfg_nombre) if len(fb[cfg_nombre]) >= 8
                                        else {"n": len(fb[cfg_nombre])})
    t = salida["todas"]
    salida["H1_mejora_vs_AR4_principal"] = bool(t.get("rmse", np.inf) < t.get("rmse_AR4", -np.inf)
                                                and t.get("dm_vs_AR4", -1) > 0 and t.get("p_vs_AR4", 1) < 0.05)
    return salida
