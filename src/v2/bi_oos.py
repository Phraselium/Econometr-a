"""BI · fuera de muestra (anual hasta 2021): panel AR(4) vs AR(4)+flujo observado de inmigración.
ECM v1 solo existe en frecuencia trimestral: se reporta aparte (panel_ecm_v1 vs panel_ar4, orígenes T4)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bi_core as bc  # noqa: E402
import v2_common as vc  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "output" / "v2" / "BI"


def _anual(d):
    d = d.sort_values(["cod_prov", "anio"]).copy()
    d["lnr"] = np.log(d["ipc_alquiler"])
    g = d.groupby("cod_prov")
    d["dY"] = g["lnr"].diff()
    for k in range(1, 4):
        d[f"dY_l{k}"] = g["dY"].shift(k)
    d["yh"] = g["lnr"].shift(-1) - d["lnr"]
    d["x_f1"] = g["x"].shift(-1)            # flujo del año t+1 (contemporáneo al objetivo): NO es pronóstico
    return d


def _pred(d, feats, modelo, splits, years, units, h=1):
    rows = []
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        pos = d["anio"].map({y: i for i, y in enumerate(years)})
        trm = (pos + h <= posL) & d["yh"].notna() & d[feats].notna().all(axis=1)
        tem = pos.isin(set(ite.tolist())) & d[feats].notna().all(axis=1) & d["yh"].notna()

        def X(msk):
            U = pd.DataFrame({f"u{u}": (d.loc[msk, "cod_prov"] == u).astype(float) for u in units}, index=d.index[msk])
            return pd.concat([d.loc[msk, feats].astype(float), U], axis=1)
        Xtr, Xte = X(trm), X(tem)
        b = np.linalg.lstsq(Xtr.values, d.loc[trm, "yh"].values, rcond=None)[0]
        rows.append(pd.DataFrame({"periodo": d.loc[tem, "anio"].astype(str).values, "unidad": d.loc[tem, "cod_prov"].values,
                                  "y_real": d.loc[tem, "yh"].values, "y_pred": Xte.values @ b, "modelo": modelo, "split": sid, "h": h}))
    return pd.concat(rows, ignore_index=True)


def run(reg, smoke=False):
    d0, _ = bc.construir_panel()
    d = _anual(d0)
    a_fin = 2015 if smoke else 2021
    d = d[d["anio"] <= a_fin]
    ar = ["dY", "dY_l1", "dY_l2", "dY_l3"]
    # MISMA muestra: orígenes con flujo observado en t y t+1 disponibles
    base = d.dropna(subset=ar + ["yh", "x", "x_f1"]).copy()
    years = sorted(base["anio"].unique())
    units = sorted(base["cod_prov"].unique())
    splits = vc.block_splits(years, h=1, block_len=1, embargo=1, min_train=3 if smoke else 4)
    out = {"smoke": smoke, "origenes": [int(y) for y in years], "n_splits": len(splits)}
    P = {"AR4": _pred(base, ar, "AR4", splits, years, units),
         "AR4+flujo_t (observado)": _pred(base, ar + ["x"], "AR4+flujo_t", splits, years, units),
         "AR4+flujo_t+1 (contemporáneo, NO pronóstico)": _pred(base, ar + ["x_f1"], "AR4+flujo_t+1", splits, years, units)}
    ev = []
    for k, v in P.items():
        if k == "AR4":
            continue
        r = vc.evaluar(v, {"AR4": P["AR4"]}, h=1).iloc[0].to_dict()
        r["modelo"] = k
        ev.append(r)
        reg.log("BI", f"OOS_{k}", "yh=ln rent_{t+1}-ln rent_t ~ AR4 [+ flujo]; FE prov", years[0], years[-1], int(r["n"]), np.nan, np.nan, np.nan,
                rmse_oos=r["rmse"], notas=f"anual; vs AR4 DM-HLN={r['dm_vs_AR4']:.3f} p={r['p_vs_AR4']:.3f}; bloques con embargo")
    reg.log("BI", "OOS_AR4", "AR4 panel anual", years[0], years[-1], int(ev[0]["n"]), np.nan, np.nan, np.nan, rmse_oos=ev[0]["rmse_AR4"], notas="base")
    E = pd.DataFrame(ev)
    E.to_csv(OUT / f"{'smoke_' if smoke else ''}oos_anual.csv", index=False)
    out["anual"] = E.round(5).to_dict("records")
    # --- ECM v1 trimestral (referencia aparte, orígenes T4 ≤ 2020)
    try:
        nac, pan = vc.load("nacional_q_v2"), vc.load("panel_prov_q")
        pan = pan[pan["trimestre"].astype(str) <= ("2015Q4" if smoke else "2021Q4")]
        a = vc.panel_ar4(pan, "ipc_alquiler", "cod_prov", 4, real=False, nac=nac)
        e = vc.panel_ecm_v1(pan, "ipc_alquiler", "cod_prov", 4, real=False, nac=nac)
        for df in (a, e):
            df.drop(df[~df["periodo"].astype(str).str.endswith("Q4")].index, inplace=True)
        r = vc.evaluar(e, {"AR4": a}, 4).iloc[0].to_dict()
        out["ecm_v1_trimestral_Q4"] = {k: (float(v) if not isinstance(v, str) else v) for k, v in r.items()}
        reg.log("BI", "OOS_ECMv1_trim_Q4", "panel_ecm_v1 ipc_alquiler h=4 orígenes T4", "", "", int(r["n"]), np.nan, np.nan, np.nan,
                rmse_oos=r["rmse"], notas=f"referencia; AR4 rmse={r['rmse_AR4']:.5f}; DM vs AR4={r['dm_vs_AR4']:.3f} p={r['p_vs_AR4']:.3f}; muestra distinta de la anual")
    except Exception as ex:  # documentar, no ocultar
        out["ecm_v1_trimestral_Q4"] = {"error": repr(ex)}
    out["nota"] = ("No es posible extender a la tasa de inmigración instrumentada/observada en panel_ar4 del alquiler: los flujos terminan en 2021-22 "
                   "(antes de la muestra de test completa) y el ECM v1 requiere datos trimestrales; se compara AR(4) panel anual con AR(4)+flujo "
                   "observado, bloques expansivos con embargo, orígenes hasta 2020.")
    (OUT / f"{'smoke_' if smoke else ''}oos_resultados.json").write_text(json.dumps(out, indent=2, ensure_ascii=False, default=float))
    return out
