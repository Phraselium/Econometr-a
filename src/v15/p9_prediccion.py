"""V15-B · H5 (P9): predicción del crecimiento trimestral del valor tasado nacional. Combinación (DFM, BVAR Minnesota, LASSO, ARDL) frente al AR(4)
y al ECM v1 (reconstruido, DV15-B-2) en la MISMA muestra, ventana expansiva, solo entrenamiento. DM-HLN APTO (unilateral); CW/GW sin p; MCS descriptivo.
Evaluación sellada de H5: octubre de 2027 (no se hace aquí). Uso: python3 src/v15/p9_prediccion.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v15.pb_comun import (OUT, Registry, SEED, cargar, dm_hln, escribe_json, hecho, mcs_pertenencia, resultado_base, serie_q)  # noqa: E402
from src.build_dataset import stl_sa  # noqa: E402  (la misma STL que construyó las series *_sa; aquí se reestima en cada origen)

CARPETA = OUT / "p9"
MIN_FILAS = 24
INI = pd.Period("2003Q1", "Q")
LAMS = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
COVID = [pd.Period("2020Q2", "Q"), pd.Period("2020Q3", "Q")]


def datos() -> pd.DataFrame:
    d9, d2 = cargar("p9_prediccion"), cargar("p2_fundamentales")
    S = {}
    S["ptas"] = serie_q(d9, "p_tasado")
    S["ipv"] = serie_q(d9, "ipv")
    S["cv"] = serie_q(d9, "compraventas_sa")
    S["cv_bruta"] = serie_q(d9, "compraventas")
    for v in ("hip_n", "hip_importe"):
        x = d9[(d9.variable == v) & (d9.nivel == "provincia")]
        x = x[x.periodo.astype(str).str.contains("T")].copy()
        x["q"] = pd.PeriodIndex([f"{a[:4]}Q{a[-1]}" for a in x.periodo.astype(str)], freq="Q")
        g = x.groupby("q").valor.agg(["sum", "count"])
        S[v] = g["sum"].where(g["count"] >= g["count"].max() - 1)
    S["vis"] = serie_q(d9, "visados")
    S["ocu"] = serie_q(d9, "ocupados_sa")
    S["ocu_bruta"] = serie_q(d9, "ocupados")
    S["cred"] = serie_q(d9, "credito_nuevo")
    S["tipo"] = serie_q(d9, "tipo_hip")
    S["eur"] = serie_q(d9, "euribor")
    S["renta"] = serie_q(d9, "renta_hog_real")
    S["alq"] = serie_q(d9, "ipc_alquiler")
    S["inf"] = serie_q(d2, "inflacion_ipc_yoy")
    S["tipo_real"] = serie_q(d2, "tipo_hip_real_bde")
    D = pd.DataFrame(S).sort_index()
    D = D[D.index <= pd.Period("2026Q2", "Q")]
    D["vis"] = np.exp(np.log(D.vis).interpolate(limit_area="inside"))   # 2016T2 y 2017T2 ausentes: interpolación loglineal (DV15-B-1)
    dl = lambda c: np.log(D[c]).diff()
    X = pd.DataFrame({"cv": dl("cv"), "hn": dl("hip_n"), "hi": dl("hip_importe"), "vis": dl("vis"), "ocu": dl("ocu"), "cred": dl("cred"),
                      "dtipo": D.tipo.diff(), "deur": D.eur.diff(), "renta": dl("renta"), "alq": dl("alq"), "inf": D.inf})
    D["dy_ptas"], D["dy_ipv"] = dl("ptas"), dl("ipv")
    return D, X


def cov_dummy(idx):
    return np.array([float(p in COVID) for p in idx])


def reg_dir(Z, y):
    b, *_ = np.linalg.lstsq(Z, y, rcond=None)
    return b


def f_ar(dy, t, Yh, h, dum, ini=4):
    # solo filas cuyo objetivo se observa en el origen (i + h <= t) y con datos desde 2003T1 (corrección K16 tras la réplica de H5)
    rows = [i for i in range(max(4, ini + 3), t + 1) if i + h <= t and not np.isnan(Yh[i])]
    Z = np.array([[1, dy[i], dy[i - 1], dy[i - 2], dy[i - 3]] + dum_row(dum, i, h) for i in rows])
    b = reg_dir(Z, Yh[rows])
    z = np.array([1, dy[t], dy[t - 1], dy[t - 2], dy[t - 3]] + dum_row(dum, t, h))
    return z @ b


def dum_row(dum, i, h):
    return [] if dum is None else [dum[i + 1:i + h + 1].sum() if i + h < len(dum) else dum[i + 1:].sum()]


def target(lnp, h):
    Y = np.full(len(lnp), np.nan)
    Y[:len(lnp) - h] = lnp[h:] - lnp[:-h]
    return Y


def pred_directo(F, Yh, t, h, dum, extra_pen=None, metodo="ols", lam=None):
    """Regresión directa de Yh[i] (i+h <= t) sobre F[i] en filas con información hasta t."""
    rows = [i for i in range(len(F)) if i + h <= t and not np.isnan(Yh[i]) and np.all(np.isfinite(F[i]))]
    Z = np.column_stack([np.ones(len(rows)), F[rows]] + ([np.array([dum_row(dum, i, h)[0] for i in rows])] if dum is not None else []))
    z = np.r_[1.0, F[t], dum_row(dum, t, h) if dum is not None else []]
    return Z, Yh[rows], z, rows


def f_dfm(X, dy, Yh, t, h, dum):
    Xs = X[:t + 1]
    ok = np.all(np.isfinite(Xs), axis=1)
    mu, sd = np.nanmean(Xs[ok], 0), np.nanstd(Xs[ok], 0) + 1e-9
    U, S, Vt = np.linalg.svd((Xs[ok] - mu) / sd, full_matrices=False)
    Fa = np.full((len(X), 2), np.nan)
    Fa[:t + 1][ok] = ((Xs[ok] - mu) / sd) @ Vt[:2].T
    F = np.column_stack([dy, Fa])
    Z, y, z, _ = pred_directo(F, Yh, t, h, dum)
    return z @ reg_dir(Z, y)


def f_bvar(V, Yh, t, h, dum):
    """Ecuación del objetivo de un BVAR Minnesota (2 rezagos; variables z-scores); λ por verosimilitud marginal (empirical Bayes, DV15-B-3)."""
    n_v = V.shape[1]
    ok = np.all(np.isfinite(V[:t + 1]), axis=1)
    mu, sd = V[:t + 1][ok].mean(0), V[:t + 1][ok].std(0) + 1e-9
    Vs = (V - mu) / sd
    F = np.column_stack([Vs, np.vstack([np.full((1, n_v), np.nan), Vs[:-1]])])
    Z, y, z, rows = pred_directo(F, Yh, t, h, dum)
    ym = y.mean()
    yc = y - ym
    vy = np.var(yc, ddof=1)
    a1 = Z[:, 1] if Z.shape[1] > 1 else np.zeros(len(yc))
    s2 = max(np.var(yc - (a1 @ yc) / (a1 @ a1 + 1e-12) * a1, ddof=1), 1e-12)   # varianza residual de un AR(1) del objetivo
    lag = np.r_[[1.0] * n_v, [2.0] * n_v]
    best, bl = -np.inf, None
    for lam in LAMS:
        pen = np.r_[1e4 * vy, vy * (lam ** 2) / lag ** 2, [vy * 1e2] * (Z.shape[1] - 1 - 2 * n_v)]
        Cm = s2 * np.eye(len(y)) + (Z * pen) @ Z.T
        sign, ld = np.linalg.slogdet(Cm)
        ll = -0.5 * (ld + yc @ np.linalg.solve(Cm, yc))
        if ll > best:
            best, bl = ll, pen
    A = Z.T @ Z + s2 * np.diag(1 / bl)
    b = np.linalg.solve(A, Z.T @ yc)
    return float(z @ b + ym)


def f_lasso(X, dy, Yh, t, h, dum):
    from sklearn.linear_model import Lasso
    F = np.column_stack([dy, X])
    Z, y, z, rows = pred_directo(F, Yh, t, h, dum)
    k = Z.shape[1] - 1
    mu, sd = Z[:, 1:].mean(0), Z[:, 1:].std(0) + 1e-9
    Zs = (Z[:, 1:] - mu) / sd
    ym = y.mean()
    rows = np.array(rows)
    best, bl = np.inf, 0.1
    for lam in np.exp(np.linspace(np.log(0.003), np.log(0.5), 10)) * y.std():
        sse, nn = 0.0, 0
        for blk in range(4):
            va = rows[len(rows) - 4 * (blk + 1):len(rows) - 4 * blk]
            tr = np.where(rows <= va[0] - 4 - h)[0]       # embargo de 4 trimestres + solapamiento del objetivo
            if len(tr) < 12:
                continue
            m = Lasso(alpha=lam, max_iter=5000).fit(Zs[tr], y[tr] - ym)
            vi = np.isin(rows, va)
            sse += ((y[vi] - ym - m.predict(Zs[vi])) ** 2).sum()
            nn += vi.sum()
        if nn and sse / nn < best:
            best, bl = sse / nn, lam
    m = Lasso(alpha=bl, max_iter=5000).fit(Zs, y - ym)
    return ym + m.predict(((z[1:] - mu) / sd)[None, :])[0]


def f_ardl(dy, cv, hn, Yh, t, h, dum):
    best, fc = np.inf, None
    for py in (1, 2, 3, 4):
        for px in (1, 2, 3, 4):
            m = max(py, px)
            cols = lambda a, p, i: [a[i - l] for l in range(p)]
            rows = [i for i in range(m, t + 1) if i + h <= t and not np.isnan(Yh[i]) and np.all(np.isfinite(cols(cv, px, i) + cols(hn, px, i) + cols(dy, py, i)))]
            if len(rows) < py + 2 * px + 8:
                continue
            Zf = lambda i: [1] + cols(dy, py, i) + cols(cv, px, i) + cols(hn, px, i) + (dum_row(dum, i, h) if dum is not None else [])
            Z = np.array([Zf(i) for i in rows])
            b = reg_dir(Z, Yh[rows])
            r = Yh[rows] - Z @ b
            bic = len(r) * np.log(r @ r / len(r)) + Z.shape[1] * np.log(len(r))
            zz = np.array(Zf(t))
            if bic < best and np.all(np.isfinite(zz)):
                best, fc = bic, zz @ b
    return fc


def f_rwd(dy, t, h, ini):
    return h * np.nanmean(dy[ini:t + 1])


def f_ecm(D, X, lnp, dy, Yh, t, h, dum, ini):
    """ECM v1 reconstruido (DV15-B-2): ECT por DOLS ±2 de ln p real sobre ln ocupados, tipo real y ln visados(-4); corto plazo directo a h."""
    n = t + 1
    lnpr = lnp - np.r_[0, np.cumsum(np.log1p(np.nan_to_num(D.inf.values[1:]) / 100) / 4)]
    ocu, tr, vis = np.log(D.ocu.values), D.tipo_real.values, np.r_[np.full(4, np.nan), np.log(D.vis.values)[:-4]]
    L = np.column_stack([ocu, tr, vis])
    dL = np.vstack([np.full((1, 3), np.nan), np.diff(L, axis=0)])
    rows = [i for i in range(ini + 5, n - 2)]
    def row(i):
        return np.r_[1.0, L[i], [dL[i + j] for j in (-2, -1, 0, 1, 2) for _ in [0]][0:0] if False else np.concatenate([dL[i + j] for j in (-2, -1, 0, 1, 2)])]
    Zd = np.array([row(i) for i in rows])
    ok = np.all(np.isfinite(Zd), axis=1) & np.isfinite(lnpr[rows])
    if ok.sum() < 20:
        return np.nan
    bd = reg_dir(Zd[ok], lnpr[rows][ok])
    theta = bd[:4]
    ect = lnpr - (np.column_stack([np.ones(len(L)), L]) @ theta)
    cr = np.log(D.cred.values)
    F = np.column_stack([ect, np.r_[np.nan, np.diff(np.log(D.ocu.values))], np.r_[np.nan, np.diff(D.tipo.values)], np.r_[np.nan, np.diff(np.log(D.renta.values))],
                         np.r_[np.full(3, np.nan), dy[:-3]], np.r_[np.nan, np.diff(cr)]])
    Z, y, z, _ = pred_directo(F, Yh, t, h, dum)
    if len(y) < 14 or not np.all(np.isfinite(z)):
        return np.nan
    return z @ reg_dir(Z, y)


def origen(D, X, t):
    """D y X con compraventas y ocupados desestacionalizados por STL solo con los datos hasta el origen t (filas > t: NaN)."""
    Dt, Xt = D.copy(), X.copy()
    for col, bruta in (("cv", "cv_bruta"), ("ocu", "ocu_bruta")):
        sa = stl_sa(D[bruta].iloc[:t + 1]).reindex(D.index)
        Dt[col] = sa
        Xt[col] = np.log(sa).diff()
    return Dt, Xt


def correr(D, X, medida, h, con_dummy, con_ecm=False):
    col = "dy_ptas" if medida == "ptas" else "dy_ipv"
    base = D["ptas"] if medida == "ptas" else D["ipv"]
    lnp = np.log(base.values)
    dy = np.r_[np.nan, np.diff(lnp)]
    dum = cov_dummy(D.index) if con_dummy else None
    Yh = target(lnp, h)
    Xm = X.values
    ini = list(D.index).index(INI)
    cols_b = ["cv", "hn", "ocu", "dtipo", "inf"]
    Vb = np.column_stack([dy, X[cols_b].values])
    # primer origen: MIN_FILAS filas completas de indicadores y objetivo
    ok = np.where(np.all(np.isfinite(Xm), axis=1) & np.isfinite(dy))[0]
    t0 = ok[0] + MIN_FILAS - 1  # primer origen con MIN_FILAS trimestres completos (DV15-B-1; corrección K16)
    modelos = ["AR4", "DFM", "BVAR", "LASSO", "ARDL", "Combinacion", "RWD"] + (["ECMv1"] if con_ecm else [])
    out = {m: [] for m in modelos}
    real, orig = [], []
    for t in range(t0, len(lnp) - h):
        if np.isnan(Yh[t]):
            continue
        Dt, Xt = origen(D, X, t)  # desestacionalización con datos hasta el origen (sin datos posteriores; corrección K16)
        Xm, Vb = Xt.values, np.column_stack([dy, Xt[cols_b].values])
        fc = {"AR4": f_ar(np.where(np.isnan(dy), 0.0, dy), t, Yh, h, dum, ini), "DFM": f_dfm(Xm, dy, Yh, t, h, dum), "BVAR": f_bvar(Vb, Yh, t, h, dum),
              "LASSO": f_lasso(Xm, dy, Yh, t, h, dum), "ARDL": f_ardl(dy, Xt.cv.values, Xt.hn.values, Yh, t, h, dum), "RWD": f_rwd(dy, t, h, max(ini, 1))}
        fc["Combinacion"] = np.mean([fc["DFM"], fc["BVAR"], fc["LASSO"], fc["ARDL"]])
        if con_ecm:
            fc["ECMv1"] = f_ecm(Dt, Xt, lnp, dy, Yh, t, h, dum, ini)
        for m in modelos:
            out[m].append(Yh[t] - fc[m])
        real.append(Yh[t])
        orig.append(D.index[t])
    E = {m: np.array(v, float) for m, v in out.items()}
    ok = np.all([np.isfinite(v) for v in E.values()], axis=0)
    return {m: v[ok] for m, v in E.items()}, [str(o) for o, k in zip(orig, ok) if k]


def rmse(e):
    return float(np.sqrt(np.mean(np.square(e))))


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    reg = Registry(CARPETA / "registro.csv")
    D, X = datos()
    E, orig = correr(D, X, "ptas", 1, False, con_ecm=True)
    P = len(E["AR4"])
    tabla = {m: {"rmse": rmse(e), "ecm": float(np.mean(e ** 2)), "razon_ecm_vs_AR4": float(np.mean(e ** 2) / np.mean(E["AR4"] ** 2))} for m, e in E.items()}
    base_k1 = min(["AR4", "ECMv1", "RWD"], key=lambda m: tabla[m]["ecm"])
    dm = {m: dm_hln(E["AR4"], E[m], 1) for m in E if m != "AR4"}
    dm_ecm = {m: dm_hln(E["ECMv1"], E[m], 1) for m in E if m not in ("ECMv1",)}
    dm_k1 = dm_hln(E[base_k1], E["Combinacion"], 1)
    noms = ["AR4", "DFM", "BVAR", "LASSO", "ARDL", "Combinacion"]
    L = np.column_stack([E[m] ** 2 for m in noms])
    mcs10 = mcs_pertenencia(L, noms, 0.10)
    mcs5 = mcs_pertenencia(L, noms, 0.05)
    reg.log("H5", "H5-principal", "Δlog valor tasado h=1; Combinacion vs AR(4); sin dummy", orig[0], orig[-1], P, np.nan, np.nan, np.nan, rmse_oos=tabla["Combinacion"]["rmse"],
            coef_interes=tabla["Combinacion"]["razon_ecm_vs_AR4"], p_interes=dm["Combinacion"]["p_unilateral"], notas="DM-HLN unilateral")
    # multiverso 60
    mv, pby = [], [{"id": "H5-principal", "p": dm["Combinacion"]["p_unilateral"], "contraste": "DM-HLN unilateral, Combinación frente a AR(4), h=1"}]
    for medida in ("ptas", "ipv"):
        for h in (1, 2, 4):
            for dd in (False, True):
                Em, om = (E, orig) if (medida == "ptas" and h == 1 and not dd) else correr(D, X, medida, h, dd)
                for m in ("DFM", "BVAR", "LASSO", "ARDL", "Combinacion"):
                    r = dm_hln(Em["AR4"], Em[m], h)
                    idm = f"H5-mv-{medida}-h{h}-{'dummy' if dd else 'sin'}-{m}"
                    mv.append({"id": idm, "medida": medida, "h": h, "dummy2020": dd, "modelo": m, "P": r["P"], "razon_ecm_vs_AR4": float(np.mean(Em[m] ** 2) / np.mean(Em["AR4"] ** 2)),
                               "dm": r["dm"], "p_unilateral": r["p_unilateral"]})
                    reg.log("H5", idm, f"{medida} h={h} dummy={dd} {m}", om[0], om[-1], r["P"], np.nan, np.nan, np.nan, coef_interes=mv[-1]["razon_ecm_vs_AR4"], p_interes=r["p_unilateral"])
                    if not (medida == "ptas" and h == 1 and not dd and m == "Combinacion"):
                        pby.append({"id": idm, "p": r["p_unilateral"]})
    mvd = pd.DataFrame(mv)
    mvd.to_csv(CARPETA / "multiverso.csv", index=False)
    # exclusión de 2020 como diagnóstico: error sin 2020T2-T3
    keep = np.array([o not in ("2020Q2", "2020Q3") for o in orig])
    dm_sin2020 = dm_hln(E["AR4"][keep], E["Combinacion"][keep], 1)
    # estabilidad: mitades
    mit = P // 2
    dm_m1, dm_m2 = dm_hln(E["AR4"][:mit], E["Combinacion"][:mit], 1), dm_hln(E["AR4"][mit:], E["Combinacion"][mit:], 1)
    diag = {"muestra_errores": {"P": P, "primer_origen_objetivo": orig[0], "ultimo": orig[-1], "desviacion": "DV15-B-1 (24 trimestres de indicadores; sin los 73 del preregistro)"},
            "ECM_por_modelo": tabla, "linea_base_K1": {"base": base_k1, "ecm_base": tabla[base_k1]["ecm"], "dm_combinacion_vs_base": dm_k1,
                                                        "regla_K1": "la combinación debe batir a la base (DM tras Holm en la evaluación sellada) y estar en el MCS al 10 % (descriptivo)"},
            "DM_HLN_vs_AR4_unilateral": dm, "DM_HLN_vs_ECMv1_unilateral": dm_ecm,
            "MCS": {"al_10pct_descriptivo": mcs10, "al_5pct_descriptivo": mcs5, "nota": "MCS al 10 % NO APTO (K13): solo descriptivo; combinación en MCS 10 %: " + str("Combinacion" in mcs10)},
            "Clark_West": "NO APTO (tamaño 0,19): no se calcula p", "Giacomini_White": "NO APTO (tamaño 0,031): no se calcula p",
            "robustez_sin_2020T2_T3": dm_sin2020, "mitades": {"primera": dm_m1, "segunda": dm_m2},
            "potencia": "P ≈ %d errores (< 73 del preregistro): potencia menor que 0,58 (MC) para una reducción del 20 %%" % P,
            "multiverso_60": {"n": int(len(mvd)), "frac_ecm_menor_que_AR4": float((mvd.razon_ecm_vs_AR4 < 1).mean()), "frac_p_unilat_lt_005": float((mvd.p_unilateral < 0.05).mean()),
                              "razon_min": float(mvd.razon_ecm_vs_AR4.min()), "razon_max": float(mvd.razon_ecm_vs_AR4.max())},
            "pruebas_C3": "no aplica: H5 es predictivo (sin capa causal); la evaluación sellada es en octubre de 2027"}
    r = tabla["Combinacion"]["razon_ecm_vs_AR4"]
    res = resultado_base(
        "r15/p9", "H5: ¿predice la combinación el Δlog trimestral del valor tasado nacional mejor que el AR(4) y el ECM v1 en la misma muestra?",
        "data/processed/v15/p9_prediccion.parquet (+ inflación y tipo real de p2_fundamentales); entrenamiento", P,
        "Ventana expansiva, h = 1; combinación = media de DFM (2 factores), BVAR Minnesota (6 var.), LASSO (λ con embargo de 4 trimestres) y ARDL (BIC ≤ 4); DM-HLN unilateral",
        {"razon_ECM_combinacion_AR4": r, "rmse_combinacion": tabla["Combinacion"]["rmse"], "rmse_AR4": tabla["AR4"]["rmse"], "rmse_ECMv1": tabla["ECMv1"]["rmse"], "rmse_RWD": tabla["RWD"]["rmse"]},
        None, "PREDICTIVO (sin capa causal; C4 de entrenamiento)", diag,
        {"modelo": "Combinacion", "rmse": tabla["Combinacion"]["rmse"], "dm_vs_ar4": {"dm": dm["Combinacion"]["dm"], "p_unilateral": dm["Combinacion"]["p_unilateral"], "P": P}},
        ["Errores recursivos de entrenamiento (visto desde v1); la evaluación sellada (≥ 4 trimestres nuevos) es en octubre de 2027.", "DM-HLN unilateral APTO; CW/GW sin p; MCS descriptivo.",
         "Resultado esperado según el preregistro: no distinguible del AR(4)."], pby)
    escribe_json(CARPETA / "resultado.json", res)
    h = [hecho("V15-H5-razon-ecm", "Razón ECM de la combinación frente al AR(4) (h=1, valor tasado)", round(r, 3), round(float(mvd.razon_ecm_vs_AR4.min()), 3), round(float(mvd.razon_ecm_vs_AR4.max()), 3),
               "razón", f"{orig[0]}-{orig[-1]}", f"{P} errores de entrenamiento", "MIVAU valor tasado; INE; BdE", "razon", "p9"),
         hecho("V15-H5-p-dm", "p unilateral DM-HLN de la combinación frente al AR(4)", round(dm["Combinacion"]["p_unilateral"], 3), None, None, "p", f"{orig[0]}-{orig[-1]}", f"{P} errores",
               "MIVAU valor tasado", "dm", "p9")]
    escribe_json(CARPETA / "hechos.json", h)
    print(P, tabla, base_k1, dm["Combinacion"], mcs10, mcs5, diag["multiverso_60"])


if __name__ == "__main__":
    main()
