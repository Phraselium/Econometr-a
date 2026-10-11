"""M3a v6: ML del alquiler de stock (RF, gradient boosting) + líneas base + interpretación descriptiva (C4).
Solo paneles de entrenamiento. Sin red. SEED=20261010. `--smoke` reduce configuraciones.
Presupuesto declarado: 30 configuraciones por familia y nivel (búsqueda aleatoria, semilla fija); 2 familias x 3 niveles = 180.
BART: no realizado (sin pymc_bart ni librería equivalente)."""
import json
import sys
import time
import warnings

import joblib
import numpy as np
import pandas as pd

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import m3a_lib as L  # noqa: E402

warnings.filterwarnings("ignore")
SMOKE = "--smoke" in sys.argv
NCFG = 4 if SMOKE else 30
OUT = L.OUT / ("_smoke" if SMOKE else "")
(OUT / "modelos").mkdir(parents=True, exist_ok=True)
(OUT / "figuras").mkdir(exist_ok=True)
NIVELES = ["provincia", "municipio", "distrito"]
FAM = {"rf": L.RF_GRID, "gb": L.LGBM_GRID}
REG_ROWS, PRED, INTERP = [], [], {}


def sub(df, ymax, anios=None):
    d = df[df.anio <= ymax] if anios is None else df[df.anio.isin(anios)]
    return d


def preds_fold(nivel, P, o, ymax_tr, vanios, cols, best):
    tr, va = P[P.anio <= ymax_tr], P[P.anio.isin(vanios)].dropna(subset=["y", "y_lag1"])
    tr = tr.dropna(subset=["y"])
    base = va[["unit", "anio", "y", "y_lag1", "cod_prov", "ccaa"]].copy()
    base["origen"], base["nivel"] = o, nivel
    res = {"persistencia": L.pred_persistencia(tr, va), "AR_unidad": L.pred_ar(tr, va),
           "M1A_TWFE_tendencia": L.pred_twfe(tr, va, L.REGS_ECO[nivel]), "ECM_v1_aprox": L.pred_ecm(tr, va, L.REGS_ECO[nivel])}
    for f in FAM:
        res[f], _ = L.ajustar_predecir(f, best[f], tr, va, cols)
    for k, v in res.items():
        PRED.append(base.assign(modelo=k, pred=v))


def seleccion(nivel, P, cols, fam, cfgs, anio_max):
    """Puntuación = RMSE medio en bloques espacio-temporales: para cada origen y cada bloque de CCAA (k=4), se entrena con
    las demás CCAA y años <= o-2 y se valida en el bloque en los años o, o+1."""
    P = P.dropna(subset=["y", "y_lag1"]).copy()
    P["blk"] = L.bloques_espaciales(P)
    folds = L.pliegues(nivel, anio_max)
    out = []
    for i, cfg in enumerate(cfgs):
        errs = []
        for o, ymax, vanios in folds:
            for b in range(4):
                tr = P[(P.anio <= ymax) & (P.blk != b)]
                va = P[(P.anio.isin(vanios)) & (P.blk == b)]
                if len(tr) < 30 or len(va) < 3:
                    continue
                p, _ = L.ajustar_predecir(fam, cfg, tr, va, cols)
                errs.append(np.sqrt(np.mean((va.y.to_numpy() - p) ** 2)))
        out.append((float(np.mean(errs)), cfg))
        REG_ROWS.append({"nivel": nivel, "familia": fam, "config_id": i, "config": json.dumps(cfg, sort_keys=True),
                         "rmse_bloques_espaciotemporales": float(np.mean(errs)), "n_bloques": len(errs),
                         "estado": "especificacion probada (cuenta en el Registry)"})
    return sorted(out, key=lambda x: x[0])


def grupos_perm(model, fam, X, y_lvl_base, yv_dy, cols, rng, R=5):
    """Importancia por permutación agrupada por familia: aumento del MSE de dy al permutar las columnas de la familia."""
    def pr(Xm):
        return model.predict(np.nan_to_num(Xm, nan=-9.0) if fam == "rf" else Xm)
    base = np.mean((yv_dy - pr(X)) ** 2)
    res = {}
    for g in sorted(set(L.FAM_DE[c] for c in cols)):
        idx = [i for i, c in enumerate(cols) if L.FAM_DE[c] == g]
        v = []
        for _ in range(R):
            Xp = X.copy()
            perm = rng.permutation(len(X))
            Xp[:, idx] = X[perm][:, idx]
            v.append(np.mean((yv_dy - pr(Xp)) ** 2) - base)
        res[g] = float(np.mean(v))
    return res


def ale_1d(model, fam, X, j, nb=10):
    q = np.unique(np.nanquantile(X[:, j], np.linspace(0, 1, nb + 1)))
    if len(q) < 3:
        return None
    k = np.clip(np.searchsorted(q, X[:, j], side="right") - 1, 0, len(q) - 2)
    f = lambda Z: model.predict(np.nan_to_num(Z, nan=-9.0) if fam == "rf" else Z)  # noqa: E731
    lo, hi = X.copy(), X.copy()
    lo[:, j], hi[:, j] = q[k], q[k + 1]
    d = f(hi) - f(lo)
    eff = np.array([d[k == i].mean() if np.any(k == i) else 0.0 for i in range(len(q) - 1)])
    ale = np.concatenate([[0], np.cumsum(eff)])
    cnt = np.array([np.sum(k == i) for i in range(len(q) - 1)])
    ale = ale - np.sum((ale[:-1] + ale[1:]) / 2 * cnt) / cnt.sum()
    return q, ale


def main():
    t0 = time.time()
    rng = np.random.default_rng(L.SEED)
    finales, stab, ales, shap_tabs = [], {}, {}, {}
    for nivel in NIVELES:
        P = L.cargar(nivel)
        cols = L.columnas_x(nivel)
        anio_max = int(P.dropna(subset=["y"]).anio.max())
        best, best_sc = {}, {}
        for f, grid in FAM.items():
            cfgs = L.muestrear_configs(grid, NCFG, L.SEED + len(f))
            if nivel == "distrito" and f == "rf":
                cfgs = [dict(c, n_estimators=min(c["n_estimators"], 100), max_samples=min(c["max_samples"], 0.5)) for c in cfgs]
            r = seleccion(nivel, P, cols, f, cfgs, anio_max)
            best[f], best_sc[f] = r[0][1], r[0][0]
            print(nivel, f, "mejor RMSE bloques", round(r[0][0], 4), round(time.time() - t0), "s", flush=True)
        folds = L.pliegues(nivel, anio_max)
        for o, ymax, vanios in folds:
            preds_fold(nivel, P, o, ymax, vanios, cols, best)
        # ----- modelos finales (todo el entrenamiento) y especificación
        tr = P.dropna(subset=["y", "y_lag1"])
        for f in FAM:
            _, m = L.ajustar_predecir(f, best[f], tr, tr.head(2), cols)
            mid = f"alquiler_{nivel}_{f}"
            joblib.dump(m, OUT / "modelos" / f"{mid}.joblib", compress=3)
            ficha = {"id": mid, "mercado": "alquiler de stock (SERPAVI)", "nivel": nivel, "medida": L.YCOL[nivel],
                     "familia": f, "variables": cols, "objetivo": "dy = y - y_lag1 (prediccion = y_lag1 + modelo)",
                     "hiperparametros": best[f], "semilla": L.SEED, "ruta_modelo": f"modelos/{mid}.joblib",
                     "entrenamiento": f"anios <= {anio_max}, N={len(tr)}", "rmse_bloques_espaciotemporales": best_sc[f],
                     "funcion_prediccion": "src/v6/m3a_lib.predecir_modelo(id, {nombre: DataFrame sellado})",
                     "nombres_paneles": L.NOMBRES[nivel], "nulos": "RF: NaN->-9; LightGBM: NaN nativo"}
            (OUT / "modelos" / f"{mid}.json").write_text(json.dumps(ficha, indent=1, ensure_ascii=False))
            finales.append({k: ficha[k] for k in ("id", "nivel", "medida", "familia")} | {"mercado": "alquiler", "ruta": f"output/v6/M3A/modelos/{mid}.json"})
        # ----- interpretación descriptiva (C4) con el gradient boosting final
        gb = joblib.load(OUT / "modelos" / f"alquiler_{nivel}_gb.joblib")
        X = tr[cols].to_numpy(float)
        import shap
        Xs = tr[tr.anio >= anio_max - 1]
        sv = shap.TreeExplainer(gb).shap_values(Xs[cols].to_numpy(float))
        sh = pd.DataFrame(sv, columns=cols)
        sh["fam"] = None
        sh["cod_prov"] = Xs.cod_prov.to_numpy()
        fam_sh = pd.DataFrame({g: sh[[c for c in cols if L.FAM_DE[c] == g]].sum(axis=1) for g in sorted(set(L.FAM_DE[c] for c in cols))})
        fam_sh["cod_prov"] = sh.cod_prov
        fam_sh["dy_predicho"] = gb.predict(Xs[cols].to_numpy(float))
        tab = fam_sh.groupby("cod_prov").mean().round(5)
        tab["n_filas"] = fam_sh.groupby("cod_prov").size()
        tab.to_csv(OUT / f"shap_por_provincia_{nivel}.csv")
        shap_tabs[nivel] = tab
        # ALE de las 3 variables de mayor |SHAP| medio (no autorregresivas primero)
        imp = pd.Series(np.abs(sv).mean(axis=0), index=cols).sort_values(ascending=False)
        top = [c for c in imp.index if c in L.REGS[nivel] or c in ("x_m", "y_m")][:3]
        ales[nivel] = {}
        for c in top:
            r = ale_1d(gb, "gb", X, cols.index(c))
            if r is not None:
                ales[nivel][c] = {"x": r[0].round(5).tolist(), "ale": r[1].round(6).tolist()}
        # estabilidad: importancia agrupada por pliegue (gb), con nulo de desenlace permutado
        per, nulo = [], []
        for o, ymax, vanios in folds:
            a = tr[tr.anio <= ymax]
            v = tr[tr.anio.isin(vanios)]
            _, m = L.ajustar_predecir("gb", best["gb"], a, v.head(2), cols)
            per.append(pd.Series(grupos_perm(m, "gb", v[cols].to_numpy(float), None, v.dy.to_numpy(float), cols, rng), name=o))
            for b in range(3 if SMOKE else 10):
                ap = a.copy()
                ap["dy"] = rng.permutation(ap.dy.to_numpy())
                _, mp = L.ajustar_predecir("gb", best["gb"], ap, v.head(2), cols)
                nulo.append(pd.Series(grupos_perm(mp, "gb", v[cols].to_numpy(float), None, v.dy.to_numpy(float), cols, rng, R=2)))
        imp_f = pd.concat(per, axis=1)
        p95 = pd.concat(nulo, axis=1).quantile(0.95, axis=1)
        imp_f["p95_nulo_desenlace_permutado"] = p95
        imp_f["media"] = imp_f[[o for o, _, _ in folds]].mean(axis=1)
        imp_f["por_encima_del_ruido"] = imp_f.media > imp_f.p95_nulo_desenlace_permutado
        imp_f.round(6).to_csv(OUT / f"importancia_permutacion_{nivel}.csv")
        rk = imp_f[[o for o, _, _ in folds]].rank()
        stab[nivel] = {"spearman_entre_pliegues": float(rk.corr(method="pearson").values[np.triu_indices(len(folds), 1)].mean()) if len(folds) > 1 else None}
        # colinealidad
        Z = tr[[c for c in L.REGS[nivel] + (["x_m", "y_m"] if nivel != "provincia" else []) if tr[c].notna().sum() > 50]].dropna()
        from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
        Zc = (Z - Z.mean()) / Z.std().replace(0, 1)
        Zc = Zc.assign(const=1.0)
        vifs = {c: float(vif(Zc.to_numpy(), i)) for i, c in enumerate(Zc.columns) if c != "const"}
        Z.corr().round(3).to_csv(OUT / f"correlacion_{nivel}.csv")
        INTERP[nivel] = {"vif": vifs, "N_vif": len(Z), "aviso_colinealidad": "VIF>5 o |r|>0.8 indica rasgos que se sustituyen entre si; la importancia de un rasgo individual es poco fiable.",
                         "estabilidad": stab[nivel], "mejores_hiperparametros": best, "rmse_bloques": best_sc,
                         "shap_top_global": imp.head(6).round(5).to_dict()}
        print(nivel, "hecho", round(time.time() - t0), "s", flush=True)
    pd.concat(PRED).to_csv(OUT / "predicciones_cv_ml.csv.gz", index=False)
    pd.DataFrame(REG_ROWS).to_csv(OUT / "registro_ml.csv", index=False)
    (OUT / "modelos_finales_ml.json").write_text(json.dumps(finales, indent=1, ensure_ascii=False))
    (OUT / "interpretacion.json").write_text(json.dumps({"ale": ales, "diag": INTERP}, indent=1, ensure_ascii=False))
    figuras(shap_tabs, ales)


def figuras(shap_tabs, ales):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    for nivel, tab in shap_tabs.items():
        fam_cols = [c for c in tab.columns if c not in ("dy_predicho", "n_filas")]
        t = tab.assign(tot=tab[fam_cols].abs().sum(axis=1)).sort_values("tot", ascending=False).head(15)
        ax = t[fam_cols].plot.barh(stacked=True, figsize=(8, 6))
        ax.set_title(f"SHAP medio por provincia y familia (descriptivo, C4) - {nivel}")
        ax.set_xlabel("contribucion media a la variacion anual de ln(EUR/m2/mes), 2022-2023")
        plt.tight_layout()
        plt.savefig(OUT / "figuras" / f"shap_provincia_{nivel}.png", dpi=110, metadata={"Software": None})
        plt.close()
        a = ales.get(nivel, {})
        if a:
            fig, axs = plt.subplots(1, len(a), figsize=(4 * len(a), 3.2))
            for ax, (c, d) in zip(np.atleast_1d(axs), a.items()):
                ax.plot(d["x"], d["ale"], marker="o", ms=3)
                ax.set_title(f"ALE: {c}")
                ax.set_ylabel("efecto sobre dy")
            plt.tight_layout()
            plt.savefig(OUT / "figuras" / f"ale_{nivel}.png", dpi=110, metadata={"Software": None})
            plt.close()


if __name__ == "__main__":
    main()
