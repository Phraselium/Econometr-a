"""BI · heterogeneidad EXPLORATORIA: DML (PLR / PLIV; lasso y RF) y causal forest, cross-fitting por bloques
de provincias. Presupuesto declarado: 14 configuraciones (usadas 10: 4 DML + 1 CausalForestDML + 5 interacciones IV)."""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bi_core as bc  # noqa: E402
import v2_common as vc  # noqa: E402

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parents[2] / "output" / "v2" / "BI"
HET = ["ln_pob02", "extr02", "ln_p02", "costa", "paro02"]
K_FOLDS, N_REP = 5, 3


def folds_por_provincia(cod, seed):
    """Bloques de provincias (no aleatorio por observación): K_FOLDS grupos de provincias."""
    rng = np.random.default_rng(seed)
    provs = np.array(sorted(set(cod)))
    asign = dict(zip(rng.permutation(provs), np.arange(len(provs)) % K_FOLDS))
    f = np.array([asign[c] for c in cod])
    return [(np.where(f != k)[0], np.where(f == k)[0]) for k in range(K_FOLDS)]


def se_cluster(psi_a, psi_b, theta, cl):
    psi = psi_a * theta + psi_b
    G = cl.max() + 1
    sc = np.bincount(cl, weights=psi, minlength=G)
    J = psi_a.mean()
    return float(np.sqrt(G / (G - 1) * (sc ** 2).sum() / (len(psi) * J) ** 2)), int(G)


def run(reg, smoke=False):
    from doubleml import DoubleMLData, DoubleMLPLIV, DoubleMLPLR
    from econml.dml import CausalForestDML
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Lasso
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    a0, a1 = (2009, 2015) if smoke else (2009, 2021)
    d, meta = bc.construir_panel()
    m = bc.muestra(d, ["x", "z", "y_alq", "y_alq_l1"] + HET, a0, a1)
    pres = vc.Presupuesto(reg, "BI", 14, "heterogeneidad EXPLORATORIA: lasso alpha=0.02 fijo (X estandarizado); RF 300 arboles, "
                          "min_samples_leaf=10, max_features=0.5; CausalForestDML 500 arboles, min_samples_leaf=10; "
                          f"cross-fitting {K_FOLDS} bloques de provincias x {N_REP} repeticiones; sin busqueda de hiperparametros")
    Wm = np.column_stack([m[HET].values, pd.get_dummies(m["anio"], dtype=float).values, m["y_alq_l1"].values])
    y, x, z = m["y_alq"].values, m["x"].values, m["z"].values
    cl = pd.factorize(m["cod_prov"])[0]
    cod = m["cod_prov"].values
    smpls = [folds_por_provincia(cod, bc.SEED + r) for r in range(N_REP)]
    learners = {"lasso": lambda: make_pipeline(StandardScaler(), Lasso(alpha=0.02, max_iter=20000)),
                "rf": lambda: RandomForestRegressor(n_estimators=100 if smoke else 300, min_samples_leaf=10,
                                                    max_features=0.5, random_state=bc.SEED, n_jobs=1)}
    res = {"smoke": smoke, "N": len(m), "dml": [], "presupuesto": "14 (10 usadas)"}
    for ml in ("lasso", "rf"):
        for mod in ("PLR", "PLIV"):
            data = DoubleMLData.from_arrays(Wm, y, x, z=z if mod == "PLIV" else None)
            if mod == "PLR":
                dm = DoubleMLPLR(data, learners[ml](), learners[ml](), n_folds=K_FOLDS, n_rep=N_REP)
            else:
                dm = DoubleMLPLIV(data, learners[ml](), learners[ml](), learners[ml](), n_folds=K_FOLDS, n_rep=N_REP)
            dm.set_sample_splitting(smpls)
            dm.fit()
            th = float(np.median(dm.all_coef[0]))
            ses = [se_cluster(dm.psi_elements["psi_a"][:, r, 0], dm.psi_elements["psi_b"][:, r, 0], dm.all_coef[0][r], cl)[0]
                   for r in range(N_REP)]
            se = float(np.sqrt(np.median(np.array(ses) ** 2 + (dm.all_coef[0] - th) ** 2)))   # mediana + dispersión entre reps
            p = float(bc.tp(th / se, cl.max() + 1))
            res["dml"].append(dict(modelo=mod, learner=ml, theta=th, se_cluster=se, p=p, theta_por_rep=[float(v) for v in dm.all_coef[0]]))
            pres.usar(f"DML_{mod}_{ml}", dict(mod=mod, learner=ml, folds=K_FOLDS, reps=N_REP), f"y_alq ~ x + g(W) [{mod}]",
                      a0, a1, len(m), notas=f"EXPLORATORIO; theta={th:.3f} se_cl={se:.3f} p={p:.4f}")
    # --- causal forest (exploratorio; tratamiento observado; sin instrumento)
    Wcf = np.column_stack([pd.get_dummies(m["anio"], dtype=float).values, m["y_alq_l1"].values])
    cvs = smpls[0]
    cf = CausalForestDML(model_y=RandomForestRegressor(n_estimators=100, min_samples_leaf=10, max_features=0.5, random_state=bc.SEED),
                         model_t=RandomForestRegressor(n_estimators=100, min_samples_leaf=10, max_features=0.5, random_state=bc.SEED),
                         discrete_treatment=False, n_estimators=200 if smoke else 500, min_samples_leaf=10, cv=cvs,
                         random_state=bc.SEED, n_jobs=1)
    X = m[HET].values
    cf.fit(y, x, X=X, W=Wcf)
    tau = cf.effect(X).ravel()
    lo, hi = cf.effect_interval(X, alpha=0.05)
    ate = cf.ate_inference(X)
    ate_s = float(np.asarray(ate.mean_point).ravel()[0])
    ate_ci = [float(np.asarray(v).ravel()[0]) for v in ate.conf_int_mean()]
    m["tau"] = tau
    het = []
    for c in HET + ["vut20_pm"]:
        v = m[c]
        ter = pd.qcut(v.rank(method="first"), 3, labels=["bajo", "medio", "alto"]) if c != "costa" else v.map({0.0: "interior", 1.0: "costa"})
        g = m.groupby(ter, observed=True)["tau"].mean()
        # correlación a nivel de provincia (EE cluster no disponible en el bosque): descriptiva
        pm = m.groupby("cod_prov").agg(t=("tau", "mean"), v=(c, "first")).dropna()
        r_, _ = stats.spearmanr(pm["v"], pm["t"])   # descriptiva: el CATE es función de X, sin p-valor válido
        het.append(dict(caracteristica=c, cate_por_grupo={str(k): float(v_) for k, v_ in g.items()}, spearman_prov=float(r_),
                        nota="vut20_pm medida en 2020, no previa: solo descriptiva" if c == "vut20_pm" else ""))
    imp = dict(zip(HET, [float(v) for v in cf.feature_importances_]))
    res["causal_forest"] = dict(ate=ate_s, ate_ic95=ate_ci, tau_p10_p90=[float(np.percentile(tau, 10)), float(np.percentile(tau, 90))],
                                frac_ic_excluye_0=float(np.mean((lo.ravel() > 0) | (hi.ravel() < 0))), importancias=imp, heterogeneidad=het,
                                aviso="bosque honesto sin remuestreo por cluster: la IC por observación subestima la incertidumbre (49 provincias); exploratorio")
    pres.usar("CausalForestDML", dict(n_estimators=200 if smoke else 500, min_samples_leaf=10, cv="bloques provincias"),
              "y_alq ~ x | X=" + ",".join(HET), a0, a1, len(m), notas=f"EXPLORATORIO; ATE={ate_s:.3f}")
    # --- heterogeneidad paramétrica IV: x y x*c instrumentados con z y z*c (c estandarizada)
    fe = bc.FE(m)
    inter = []
    for c in HET:
        cs = (m[c] - m[c].mean()) / m[c].std()
        Xm = np.column_stack([fe.r(x), fe.r(x * cs)])
        Zm = np.column_stack([fe.r(z), fe.r(z * cs)])
        r = bc.iv(fe.r(y), Xm, Zm, fe)
        pe = bc.primera_etapa(Xm[:, 0], Zm, fe)
        p_i = float(bc.tp(r["b"][1] / r["se"][1], fe.G))
        inter.append(dict(caracteristica=c, b_x=float(r["b"][0]), b_inter=float(r["b"][1]), se_inter=float(r["se"][1]), p_inter=p_i, F=pe["F"]))
        pres.usar(f"IV_inter_{c}", dict(c=c), f"y_alq ~ x + x*{c} | z, z*{c}", a0, a1, len(m), notas=f"EXPLORATORIO; p_inter={p_i:.4f}")
    from bi_h3 import holm
    h = holm([i["p_inter"] for i in inter])
    for i, a in zip(inter, h):
        i["p_holm"] = float(a)
    res["interacciones_iv"] = inter
    pd.DataFrame(res["dml"]).drop(columns="theta_por_rep").to_csv(OUT / f"{'smoke_' if smoke else ''}het_dml.csv", index=False)
    pd.DataFrame(inter).to_csv(OUT / f"{'smoke_' if smoke else ''}het_interacciones_iv.csv", index=False)
    (OUT / f"{'smoke_' if smoke else ''}het_resultados.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=float))
    return res
