"""Interpretabilidad de modelos de arboles por FAMILIAS de variables: SHAP agrupado (suma de SHAP de TreeExplainer por grupo),
importancia por permutacion agrupada, ALE de primer orden (implementacion propia), dependencia parcial, interacciones SHAP,
modelo sustituto (arbol poco profundo) y estabilidad del ranking de familias (bootstrap y pliegues temporales).

PREDICCION != CAUSALIDAD: nada de lo que sale de aqui es un efecto causal; solo describe como el modelo ajustado usa las
familias de variables (con correlaciones entre familias el reparto de SHAP no identifica efectos).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20261010


def modelo_lgbm(seed=SEED, n_estimators=150, **kw):
    import lightgbm as lgb
    par = dict(n_estimators=n_estimators, learning_rate=0.05, num_leaves=8, min_child_samples=10, subsample=0.8, subsample_freq=1,
               colsample_bytree=0.8, n_jobs=1, random_state=seed, deterministic=True, force_row_wise=True, verbose=-1)
    par.update(kw)
    return lgb.LGBMRegressor(**par)


def _idx(grupos, cols):
    cols = list(cols)
    return {g: [cols.index(c) for c in v] for g, v in grupos.items()}


def shap_valores(modelo, X):
    import shap
    return np.asarray(shap.TreeExplainer(modelo).shap_values(np.asarray(X, float) if not isinstance(X, pd.DataFrame) else X))


def shap_grupos(modelo, X, grupos, sv=None):
    """Importancia por familia = media de |suma de SHAP de sus variables|. Devuelve Series ordenada y dict con SHAP por variable."""
    cols = list(X.columns)
    sv = shap_valores(modelo, X) if sv is None else sv
    ix = _idx(grupos, cols)
    g = pd.DataFrame({k: sv[:, v].sum(1) for k, v in ix.items()})
    imp = g.abs().mean().sort_values(ascending=False)
    return imp, pd.Series(np.abs(sv).mean(0), index=cols), g


def perm_agrupada(modelo, X, y, grupos, n_rep=10, seed=SEED):
    """Aumento del RMSE al permutar CONJUNTAMENTE las columnas de cada familia (misma permutacion de filas)."""
    rng = np.random.default_rng(seed)
    Xv = X.values.astype(float)
    cols = list(X.columns)
    ix = _idx(grupos, cols)
    base = np.sqrt(np.mean((np.asarray(y) - modelo.predict(Xv)) ** 2))
    out = {}
    for g, v in ix.items():
        d = []
        for _ in range(n_rep):
            Xp = Xv.copy()
            Xp[:, v] = Xv[rng.permutation(len(Xv))][:, v]
            d.append(np.sqrt(np.mean((np.asarray(y) - modelo.predict(Xp)) ** 2)) - base)
        out[g] = np.mean(d)
    return pd.Series(out).sort_values(ascending=False)


def ale_1d(predict, X, col, K=20):
    """ALE de primer orden (Apley-Zhu 2020) para la columna `col` con K intervalos de cuantiles. Devuelve DataFrame x, ale
    (centrado: media ponderada por la muestra = 0)."""
    x = X[col].values.astype(float)
    z = np.unique(np.quantile(x, np.linspace(0, 1, K + 1)))
    if len(z) < 3:
        return pd.DataFrame({"x": z, "ale": np.zeros(len(z))})
    k = np.clip(np.searchsorted(z, x, side="left") - 1, 0, len(z) - 2)
    Xlo, Xhi = X.copy(), X.copy()
    Xlo[col] = z[k]
    Xhi[col] = z[k + 1]
    d = predict(Xhi.values.astype(float)) - predict(Xlo.values.astype(float))
    efecto = np.array([d[k == j].mean() if np.any(k == j) else 0.0 for j in range(len(z) - 1)])
    cnt = np.array([np.sum(k == j) for j in range(len(z) - 1)])
    ale = np.r_[0.0, np.cumsum(efecto)]
    centro = np.sum((ale[:-1] + ale[1:]) / 2 * cnt) / cnt.sum()
    return pd.DataFrame({"x": z, "ale": ale - centro})


def pdp_1d(predict, X, col, n_grid=20):
    """Dependencia parcial (media de predicciones fijando la columna en cada valor de la rejilla de cuantiles)."""
    grid = np.unique(np.quantile(X[col].values, np.linspace(0.02, 0.98, n_grid)))
    v = []
    for g in grid:
        Xg = X.copy()
        Xg[col] = g
        v.append(predict(Xg.values.astype(float)).mean())
    return pd.DataFrame({"x": grid, "pdp": v})


def interacciones_shap(modelo, X, grupos, max_n=300, seed=SEED):
    """Matriz de interacciones SHAP (media |.|) entre FAMILIAS (suma de las interacciones cruzadas); diagonal = efecto principal."""
    import shap
    rng = np.random.default_rng(seed)
    Xs = X.iloc[np.sort(rng.choice(len(X), min(max_n, len(X)), replace=False))]
    iv = np.asarray(shap.TreeExplainer(modelo).shap_interaction_values(Xs))
    ix = _idx(grupos, list(X.columns))
    names = list(grupos)
    M = pd.DataFrame(0.0, index=names, columns=names)
    for a in names:
        for b in names:
            M.loc[a, b] = np.abs(iv[:, ix[a]][:, :, ix[b]].sum((1, 2))).mean()
    return M


def sustituto(modelo, X, profundidad=3, seed=SEED):
    """Arbol sustituto de profundidad baja ajustado a las PREDICCIONES del modelo; devuelve fidelidad (R2 sobre predicciones) y reglas."""
    from sklearn.tree import DecisionTreeRegressor, export_text
    yh = modelo.predict(X.values.astype(float))
    t = DecisionTreeRegressor(max_depth=profundidad, min_samples_leaf=10, random_state=seed).fit(X.values.astype(float), yh)
    r2 = 1 - np.sum((yh - t.predict(X.values.astype(float))) ** 2) / np.sum((yh - yh.mean()) ** 2)
    return {"fidelidad_r2": float(r2), "reglas": export_text(t, feature_names=list(X.columns))}


def _ranking(modelo, X, grupos):
    imp = shap_grupos(modelo, X, grupos)[0]
    return list(imp.index)


def estabilidad_ranking(X, y, grupos, fit_fn=modelo_lgbm, B=30, n_pliegues=4, bloque=1, seed=SEED):
    """Estabilidad del ranking de familias (SHAP agrupado).

    - Bootstrap: B remuestreos de filas (bloques moviles si bloque>1), reajuste; % de replicas en que cada familia ocupa la
      MISMA posicion que en la muestra completa.
    - Pliegues temporales: ventanas expansivas (n_pliegues cortes de entrenamiento 50%..100%); % de pliegues con la misma posicion.
    Devuelve dict con ranking completo, tablas y el % de replicas donde el ranking COMPLETO coincide.
    """
    rng = np.random.default_rng(seed)
    n = len(X)
    ref = _ranking(fit_fn(seed=seed).fit(X.values, y), X, grupos)
    fams = list(grupos)
    pos_ref = {f: ref.index(f) for f in fams}
    mismo = {f: 0 for f in fams}
    completo = 0
    for b in range(B):
        if bloque <= 1:
            idx = rng.integers(0, n, n)
        else:
            nb = int(np.ceil(n / bloque))
            st = rng.integers(0, n - bloque + 1, nb)
            idx = (st[:, None] + np.arange(bloque)[None]).ravel()[:n]
        Xb = X.iloc[idx]
        r = _ranking(fit_fn(seed=seed + b + 1).fit(Xb.values, np.asarray(y)[idx]), Xb, grupos)
        for f in fams:
            mismo[f] += r.index(f) == pos_ref[f]
        completo += r == ref
    boot = pd.Series({f: mismo[f] / B for f in fams})
    cortes = np.linspace(0.5, 1.0, n_pliegues).tolist()
    mp = {f: 0 for f in fams}
    comp_p = 0
    for c in cortes:
        m = int(c * n)
        Xt = X.iloc[:m]
        r = _ranking(fit_fn(seed=seed).fit(Xt.values, np.asarray(y)[:m]), Xt, grupos)
        for f in fams:
            mp[f] += r.index(f) == pos_ref[f]
        comp_p += r == ref
    tem = pd.Series({f: mp[f] / len(cortes) for f in fams})
    return {"ranking": ref, "pct_misma_pos_bootstrap": boot, "pct_ranking_completo_bootstrap": completo / B,
            "pct_misma_pos_pliegues": tem, "pct_ranking_completo_pliegues": comp_p / len(cortes)}
