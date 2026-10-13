"""V7-R5: predicción regional (17 CCAA), backtest de origen móvil y congelación. Capa C4 (predicción, no causalidad).

Informativo, muestra ya vista en v1. Determinista, sin red, SEED=20261010, un hilo. Todas las especificaciones van a econ_utils.Registry.
Uso: python3 src/v7/r5_prediccion.py [--smoke]
Interfaz para evaluate_v7: nuevos_periodos(destino, despues_de) y evaluar_congelado(cong, datos, simular).

Modelos (todos sobre ln del índice; predicción de NIVEL a h=1-4 trimestres, estimados SOLO con datos hasta el origen):
  persistencia; ult_crec_nac (persistencia + crecimiento nacional de los h últimos trimestres, FACTIBLE);
  ar_factor (AR(1) por CCAA en diferencias con el crecimiento nacional retardado; es la «base fuerte»);
  ar4 (AR(4) en diferencias por CCAA); ecm_v1 (ECM NACIONAL con la especificación A, aplicado a cada CCAA con ajuste por
  nivel: y_i = y_nac_pred + (y_i,T - y_nac,T)); pmg (PMG de panel_tools, spec A, sin demeaning ni ajuste de rupturas porque
  se predice en niveles; coeficientes por unidad con theta fijo); gbm (LightGBM directo por horizonte, 1 configuración fija);
  mixto (MixedLM AR(2) en diferencias con intercepto y pendiente aleatorios por CCAA).
Regresores futuros de ecm_v1/pmg: dX = 0 (los X se congelan en su último valor).
"""
from __future__ import annotations

import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v7"))
import panel_tools as pt  # noqa: E402
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = RAIZ / "output" / "v7" / "R5"
PANEL = RAIZ / "data" / "processed" / "v7" / "panel_ccaa_q_v7.csv"
H = 4
ORIGEN_INI = "2016Q1"
ROT = "informativo, muestra ya vista en v1"
FECHA = "2026-10-12"
MERC = {"alquiler": ("ln_ipc_alquiler", ["ln_ocupados", "ln_pob_total"]),
        "compra": ("ln_ipv", ["ln_ocupados", "ln_hip_importe", "ln_pob_total"])}
MODELOS = ["persistencia", "ult_crec_nac", "ar_factor", "ar4", "ecm_v1", "pmg", "gbm", "mixto"]
BASE = "ar_factor"
CAND = ["ar4", "ecm_v1", "pmg", "gbm", "mixto"]
GBM_PAR = dict(n_estimators=120, learning_rate=0.05, num_leaves=5, min_child_samples=15, subsample=0.8, subsample_freq=1,
               colsample_bytree=0.8, reg_lambda=1.0, random_state=SEED, n_jobs=1, deterministic=True, force_row_wise=True,
               verbose=-1)
PROV_A_CCAA = {  # misma tabla que src/v7/r1_panel.py (códigos INE)
    "01": "16", "02": "08", "03": "10", "04": "01", "05": "07", "06": "11", "07": "04", "08": "09", "09": "07",
    "10": "11", "11": "01", "12": "10", "13": "08", "14": "01", "15": "12", "16": "08", "17": "09", "18": "01",
    "19": "08", "20": "16", "21": "01", "22": "02", "23": "01", "24": "07", "25": "09", "26": "17", "27": "12",
    "28": "13", "29": "01", "30": "14", "31": "15", "32": "12", "33": "03", "34": "07", "35": "05", "36": "12",
    "37": "07", "38": "05", "39": "06", "40": "07", "41": "01", "42": "07", "43": "09", "44": "02", "45": "08",
    "46": "10", "47": "07", "48": "16", "49": "07", "50": "02", "51": "18", "52": "19"}


# ------------------------------------------------------------------------------------------------ datos
def carga_panel():
    d = pd.read_csv(PANEL, dtype={"codigo_ine_ccaa": str})
    qs = sorted(d["trimestre"].unique())
    cods = sorted(d["codigo_ine_ccaa"].unique())
    data = {}
    for m, (yv, xs) in MERC.items():
        piv = lambda v: d.pivot(index="codigo_ine_ccaa", columns="trimestre", values=v).loc[cods, qs].to_numpy(float)  # noqa: E731
        X = np.stack([piv(v) for v in xs], axis=2)
        for i in range(X.shape[0]):   # los regresores no publicados al final (desde 2025T2) se arrastran con su último valor
            X[i] = pd.DataFrame(X[i]).ffill().to_numpy()
        data[m] = (piv(yv), X)
    return qs, cods, data


# ------------------------------------------------------------------------------------------------ MCO auxiliares
def _ols(Z, d):
    b = np.linalg.lstsq(Z, d, rcond=None)[0]
    return b


def _bloque_ar(y):
    """Diferencias y factor nacional."""
    dy = np.diff(y, axis=1)
    f = np.diff(y.mean(0))
    return dy, f


# ------------------------------------------------------------------------------------------------ modelos
def m_persistencia(y, X, h=H):
    return np.repeat(y[:, -1:], h, axis=1), {}


def m_ult_crec_nac(y, X, h=H):
    yb = y.mean(0)
    cr = np.array([yb[-1] - yb[-1 - k] for k in range(1, h + 1)])
    return y[:, -1:] + cr[None, :], {"regla": "y_T + (ybar_T - ybar_{T-h})"}


def m_ar_factor(y, X, h=H):
    dy, f = _bloque_ar(y)
    N = y.shape[0]
    Zf = np.column_stack([np.ones(len(f) - 1), f[:-1]])
    af, bf = _ols(Zf, f[1:])
    coefs = np.zeros((N, 3))
    for i in range(N):
        Z = np.column_stack([np.ones(len(f) - 1), dy[i, :-1], f[:-1]])
        coefs[i] = _ols(Z, dy[i, 1:])
    pred = np.zeros((N, h))
    pd_, pf = dy[:, -1].copy(), f[-1]
    lvl = y[:, -1].copy()
    for k in range(h):
        nd = coefs[:, 0] + coefs[:, 1] * pd_ + coefs[:, 2] * pf
        pf = af + bf * pf
        pd_ = nd
        lvl = lvl + nd
        pred[:, k] = lvl
    return pred, {"factor_ar1": [float(af), float(bf)], "coef_ccaa[const,dy_1,f_1]": coefs.round(10).tolist()}


def m_ar4(y, X, h=H):
    dy, _ = _bloque_ar(y)
    N, T1 = dy.shape
    pred = np.zeros((N, h))
    cs = []
    for i in range(N):
        Z = np.column_stack([np.ones(T1 - 4)] + [dy[i, 4 - j - 1:T1 - j - 1] for j in range(4)])
        b = _ols(Z, dy[i, 4:])
        cs.append(b)
        hist = list(dy[i, -4:][::-1])
        lvl = y[i, -1]
        for k in range(h):
            nd = b[0] + sum(b[1 + j] * hist[j] for j in range(4))
            hist = [nd] + hist[:3]
            lvl += nd
            pred[i, k] = lvl
    return pred, {"coef_ccaa[const,l1..l4]": np.array(cs).round(10).tolist()}


def _ec_forecast(coef, y_last, dy_last, xlast, theta, h):
    """Recursión ECM [phi, const, gammaX(k), rho] con dX futuro = 0. coef: (phi, c, gam.., rho)."""
    k = len(theta)
    phi, c, rho = coef[0], coef[1], coef[2 + k]
    out, lvl, pd_ = [], y_last, dy_last
    for _ in range(h):
        nd = phi * (lvl - xlast @ theta) + c + rho * pd_
        lvl += nd
        pd_ = nd
        out.append(lvl)
    return np.array(out)


def _ecm_unit(y, X, theta=None):
    """Una unidad (T,), (T,k): ECM p=2,q=1 por MCO (theta libre) o con theta fijo."""
    d, L, W = pt._build(y, X, 2, 1, 2)
    if theta is None:
        Z = np.hstack([L, W])
        b = _ols(Z, d)
        k = X.shape[1]
        if b[0] >= -1e-3:   # sin corrección de error significativa: se reestima en diferencias (phi=0), sin deriva espuria
            return np.concatenate([[0.0], _ols(W, d)]), np.zeros(k)
        th = -b[1:1 + k] / b[0]
        return np.concatenate([[b[0]], b[1 + k:]]), th
    ec = L[:, 0] - L[:, 1:] @ theta
    b = _ols(np.column_stack([ec, W]), d)
    if b[0] >= -1e-3:   # phi_i no negativo: se reestima en diferencias (phi=0)
        b = np.concatenate([[0.0], _ols(W, d)])
    return b, theta


def _ventana(X):
    ok = np.isfinite(X).all(axis=(0, 2))
    return int(np.argmax(ok)) if ok.any() else 0


def m_ecm_v1(y, X, h=H):
    t0 = _ventana(X)
    yn, Xn = y[:, t0:].mean(0), X[:, t0:].mean(0)
    coef, th = _ecm_unit(yn, Xn)
    dyn = yn[-1] - yn[-2]
    nat = _ec_forecast(coef, yn[-1], dyn, Xn[-1], th, h)
    pred = y[:, -1:] - yn[-1] + nat[None, :]
    return pred, {"coef[phi,const,gamma_X..,rho]": coef.round(10).tolist(), "theta": th.round(10).tolist(), "inicio_muestra_idx": t0,
                  "ajuste_nivel": "y_i = y_nac_pred + (y_iT - y_nacT)"}


def m_pmg(y, X, h=H):
    t0 = _ventana(X)
    ys, Xs = y[:, t0:], X[:, t0:]
    try:
        r = pt.pmg(ys, Xs, 2, 1)
        th, conv = r["theta"], r["converged"]
    except Exception:
        th, conv = pt.mg(ys, Xs, 2, 1)["theta"], False
    N = y.shape[0]
    pred = np.zeros((N, h))
    cs = []
    for i in range(N):
        b, _ = _ecm_unit(ys[i], Xs[i], th)
        cs.append(b)
        pred[i] = _ec_forecast(b, ys[i, -1], ys[i, -1] - ys[i, -2], Xs[i, -1], th, h)
    return pred, {"theta": np.asarray(th).round(10).tolist(), "convergio": bool(conv), "inicio_muestra_idx": t0,
                  "coef_ccaa[phi,const,gamma_X..,rho]": np.array(cs).round(10).tolist()}


def _feats(y, X, t):
    N = y.shape[0]
    yb = y.mean(0)
    cols = [y[:, t - j] - y[:, t - j - 1] for j in range(4)] + [y[:, t] - y[:, t - 4], y[:, t] - yb[t],
                                                                  np.full(N, yb[t] - yb[t - 1])]
    for j in range(X.shape[2]):
        cols += [X[:, t, j] - X[:, t - 1, j], X[:, t - 1, j] - X[:, t - 2, j], X[:, t, j] - X[:, t - 4, j]]
    return np.column_stack(cols)


def m_gbm(y, X, h=H):
    import lightgbm as lgb
    T = y.shape[1]
    N = y.shape[0]
    pred = np.zeros((N, h))
    modelos = {}
    for k in range(1, h + 1):
        ts = range(4, T - k)
        A = np.vstack([_feats(y, X, t) for t in ts])
        tg = np.concatenate([y[:, t + k] - y[:, t] for t in ts])
        mdl = lgb.LGBMRegressor(**GBM_PAR).fit(A, tg)
        pred[:, k - 1] = y[:, -1] + mdl.predict(_feats(y, X, T - 1))
        modelos[f"h{k}"] = mdl.booster_.model_to_string()
    return pred, {"_modelos_txt": modelos, "hiperparametros": {k: v for k, v in GBM_PAR.items()}}


def m_mixto(y, X, h=H):
    import statsmodels.api as sm
    dy, _ = _bloque_ar(y)
    N, T1 = dy.shape
    ex = np.vstack([np.column_stack([np.ones(T1 - 2), dy[i, 1:-1], dy[i, :-2]]) for i in range(N)])
    en = np.concatenate([dy[i, 2:] for i in range(N)])
    g = np.repeat(np.arange(N), T1 - 2)
    res, var = None, "pendiente_aleatoria"
    for var, cre in (("pendiente_aleatoria", ex[:, :2]), ("intercepto_aleatorio", ex[:, :1])):
        try:
            r = sm.MixedLM(en, ex, groups=g, exog_re=cre).fit(method=["lbfgs"], maxiter=200)
            if np.all(np.isfinite(r.fe_params)):
                res = r
                break
        except Exception:
            continue
    if res is None:
        var, fe, re_ = "efectos_fijos_MCO", _ols(ex, en), {i: np.zeros(2) for i in range(N)}
    else:
        fe, re_ = res.fe_params, {i: np.asarray(res.random_effects[i]) for i in range(N)}
    pred = np.zeros((N, h))
    for i in range(N):
        u = np.zeros(3)
        u[:len(re_[i])] = re_[i]
        b = fe + u
        d1, d2, lvl = dy[i, -1], dy[i, -2], y[i, -1]
        for k in range(h):
            nd = b[0] + b[1] * d1 + b[2] * d2
            d2, d1, lvl = d1, nd, lvl + nd
            pred[i, k] = lvl
    return pred, {"variante": var, "efectos_fijos[const,dy_1,dy_2]": np.asarray(fe).round(10).tolist(),
                  "efectos_aleatorios_ccaa": {str(i): np.asarray(re_[i]).round(10).tolist() for i in range(N)}}


FUN = {"persistencia": m_persistencia, "ult_crec_nac": m_ult_crec_nac, "ar_factor": m_ar_factor, "ar4": m_ar4,
       "ecm_v1": m_ecm_v1, "pmg": m_pmg, "gbm": m_gbm, "mixto": m_mixto}


# ------------------------------------------------------------------------------------------------ estadística
def dm_hln(d):
    d = np.asarray(d, float)
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return np.nan, np.nan
    dc = d - d.mean()
    lrv = dc @ dc / n
    if lrv <= 0:
        return np.nan, np.nan
    st = d.mean() / np.sqrt(lrv / n) * np.sqrt((n - 1) / n)
    return float(st), float(stats.t.cdf(st, n - 1))   # p unilateral: el modelo es mejor (d<0)


_SG: dict = {}


def perm_signos(d):
    d = np.asarray(d, float)
    n = len(d)
    if n < 3 or np.allclose(d, 0):
        return np.nan
    if n not in _SG:
        if n <= 16:
            _SG[n] = 1.0 - 2.0 * ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1)
        else:
            _SG[n] = np.random.default_rng(SEED).choice(np.array([-1.0, 1.0]), size=(20000, n))
    pm = _SG[n] @ d / n
    obs = d.mean()
    return float(np.mean(pm <= obs + 1e-15)) if n <= 16 else float((1 + np.sum(pm <= obs + 1e-15)) / (1 + len(pm)))


def holm(p):
    p = np.asarray(p, float)
    o = np.argsort(np.where(np.isnan(p), 2, p))
    m = int(np.sum(~np.isnan(p)))
    out = np.full(len(p), np.nan)
    run = 0.0
    for r, i in enumerate(o[:m]):
        run = max(run, (m - r) * p[i])
        out[i] = min(1.0, run)
    return out


def compara(err, base_de, comparadores, cods):
    """err: DataFrame largo [mercado, modelo, h, ccaa, e2]; pérdida por CCAA = media de e2. Devuelve filas DM/permutación + Holm."""
    L = err.groupby(["mercado", "modelo", "h", "ccaa"])["e2"].mean().unstack("ccaa")
    filas = []
    for (m, h), _ in err.groupby(["mercado", "h"]):
        for comp in comparadores:
            if (m, comp, h) not in L.index:
                continue
            for mod in MODELOS:
                if mod == comp or (m, mod, h) not in L.index:
                    continue
                d = (L.loc[(m, mod, h)] - L.loc[(m, comp, h)]).to_numpy(float)
                st, p_dm = dm_hln(d)
                filas.append(dict(mercado=m, h=h, modelo=mod, comparador=comp, n_ccaa=len(d), dm_hln=st, p_dm_mejor=p_dm,
                                  p_perm_mejor=perm_signos(d), n_ccaa_mejor=int((d < 0).sum())))
    R = pd.DataFrame(filas)
    if len(R):
        for c in ("p_dm_mejor", "p_perm_mejor"):
            R[c + "_holm"] = np.nan
            for _, ix in R.groupby(["mercado", "h", "comparador"]).groups.items():
                R.loc[ix, c + "_holm"] = holm(R.loc[ix, c].to_numpy())
    return R


# ------------------------------------------------------------------------------------------------ backtest
def run_modelo(nombre, y, X, h=H):
    return FUN[nombre](y, X, h)


def backtest(qs, cods, data, reg, smoke=False):
    filas = []
    i0 = qs.index(ORIGEN_INI)
    T = len(qs)
    origs = list(range(i0, T - 1))
    if smoke:
        origs = origs[::10]
    for m, (y, X) in data.items():
        for o in origs:
            for nom in MODELOS:
                pred, _ = run_modelo(nom, y[:, :o + 1], X[:, :o + 1])
                for k in range(1, H + 1):
                    if o + k >= T:
                        continue
                    e = y[:, o + k] - pred[:, k - 1]
                    for i, c in enumerate(cods):
                        filas.append((m, nom, qs[o], k, c, e[i]))
    E = pd.DataFrame(filas, columns=["mercado", "modelo", "origen", "h", "ccaa", "e"])
    E["e2"] = E["e"] ** 2
    for m in MERC:
        for nom in MODELOS:
            s = E[(E.mercado == m) & (E.modelo == nom) & (E.h == 1)]
            reg.log("R5_backtest", f"{nom}__{m}", f"{MERC[m][0]} ~ {nom} (origen movil {ORIGEN_INI}..., h=1-4)", qs[0], qs[-1], len(s),
                    np.nan, np.nan, np.nan, rmse_oos=float(100 * np.sqrt(s.e2.mean())),
                    notas=("hiperparametros fijos, 1 configuracion " if nom == "gbm" else "") + ROT)
    return E


def congela(qs, cods, data, E, mejor):
    (OUT / "congelacion").mkdir(parents=True, exist_ok=True)
    pr, ficheros, specs = [], {}, {}
    T = len(qs)
    y0, q0 = qs[-1], qs[-1]
    fut = [f"{int(q0[:4]) + (int(q0[-1]) + k - 1) // 4}Q{(int(q0[-1]) + k - 1) % 4 + 1}" for k in range(1, H + 1)]
    for m, (y, X) in data.items():
        for nom in MODELOS:
            pred, art = run_modelo(nom, y, X)
            txt = art.pop("_modelos_txt", {})
            for hk, s in txt.items():
                p = OUT / "congelacion" / f"{nom}_{m}_{hk}.txt"
                p.write_text(s, encoding="utf-8")
                ficheros[str(p.relative_to(RAIZ))] = hashlib.sha256(p.read_bytes()).hexdigest()
            art["cods_ccaa"] = cods
            art["inicio_estimacion"] = qs[0]
            art["fin_estimacion"] = q0
            p = OUT / "congelacion" / f"{nom}_{m}.json"
            p.write_text(json.dumps(art, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
            ficheros[str(p.relative_to(RAIZ))] = hashlib.sha256(p.read_bytes()).hexdigest()
            for i, c in enumerate(cods):
                for k in range(H):
                    pr.append((m, nom, c, k + 1, fut[k], float(pred[i, k]), float(y[i, -1])))
        for i, c in enumerate(cods):  # modelo «mejor regional» (selección en el backtest, optimista por construcción)
            nom = mejor.get((m, c), BASE)
            for k in range(H):
                v = [r for r in pr if r[0] == m and r[1] == nom and r[2] == c and r[3] == k + 1][0]
                pr.append((m, "mejor_regional", c, k + 1, fut[k], v[5], v[6]))
    P = pd.DataFrame(pr, columns=["mercado", "modelo", "codigo_ine_ccaa", "h", "trimestre_objetivo", "pred_ln", "y_origen_ln"])
    P.to_csv(OUT / "predicciones_congeladas.csv", index=False)
    pc = OUT / "predicciones_congeladas.csv"
    specs = {
        "persistencia": "y_{T+h}=y_T", "ult_crec_nac": "y_{T+h}=y_T+(ybar_T-ybar_{T-h}), ybar=media de 17 CCAA (factible)",
        "ar_factor": "base fuerte K1 factible: dy_i,t=a_i+b_i dy_i,t-1+c_i f_t-1; f=AR(1) del crecimiento medio; recursivo",
        "ar4": "dy_i,t=a_i+sum_{j=1..4} b_ij dy_i,t-j por CCAA; recursivo",
        "ecm_v1": "ECM nacional (p=2,q=1, spec A; ver r5_prediccion.m_ecm_v1) + ajuste por nivel; no hay ECM v1 por CCAA",
        "pmg": "PMG (panel_tools.pmg, p=2,q=1, spec A, sin demeaning) + coeficientes por unidad con theta fijo; dX futuro=0",
        "gbm": "LightGBM directo por h; rasgos: 4 dy, d4y, brecha a la media, factor, dX_t, dX_t-1, d4X",
        "mixto": "MixedLM dy_t~1+dy_t-1+dy_t-2, aleatorios (1, dy_t-1) por CCAA (o intercepto / MCO si no converge)",
        "mejor_regional": "para cada (mercado, CCAA) el modelo candidato de menor RMSE en el backtest (selección en muestra)"}
    mj = {"rama": "R5", "rotulo": ROT, "semilla": SEED, "hilos": 1, "origen_estimacion": q0, "periodos_prediccion": fut,
          "regla_reestimacion": f"expansiva, trimestral: en cada origen se reestima con todos los datos hasta ese trimestre; la "
                                f"congelación reestima con datos hasta {q0}; en la evaluación diferida NO se reestima",
          "mercados": {m: {"y": MERC[m][0], "x_especificacion_A": MERC[m][1]} for m in MERC},
          "modelos": {n: {"especificacion": specs[n], "hiperparametros": (GBM_PAR if n == "gbm" else None)} for n in specs},
          "base_fuerte": BASE, "comparadores": [BASE, "ar4", "ecm_v1"], "mejor_regional": {f"{m}|{c}": v for (m, c), v in mejor.items()},
          "ficheros_versionados_sha256": ficheros,
          "predicciones": {"fichero": str(pc.relative_to(RAIZ)), "sha256": hashlib.sha256(pc.read_bytes()).hexdigest()},
          "presupuesto_hiperparametros": "1 configuración fija de LightGBM; sin búsqueda; 8 modelos x 2 mercados = 16 especificaciones"}
    (OUT / "modelos_congelados.json").write_text(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    return P


# ------------------------------------------------------------------------------------------------ evaluación diferida
def _clave(s):
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", s)


def _nombre_a_cod():
    d = pd.read_csv(PANEL, dtype={"codigo_ine_ccaa": str})[["ccaa", "codigo_ine_ccaa"]].drop_duplicates()
    mp = {_clave(a): c for a, c in zip(d.ccaa, d.codigo_ine_ccaa)}
    mp["principadodeasturias"] = mp["asturias"]
    return mp


def _cod_de_territorio(t, mp):
    base = t.split(". ")[0].strip()
    ks = [_clave(base)]
    if "," in base:
        a, b = [x.strip() for x in base.split(",", 1)]
        ks.append(_clave(b + " " + a))
    for k in ks:
        if k in mp:
            return mp[k]
    return None


def _trim(p):
    p = str(p)
    if "M" in p:   # 2026M08
        return f"{p[:4]}Q{(int(p[-2:]) - 1) // 3 + 1}", True
    return p.replace("T", "Q"), False


def observados(dirx: Path) -> pd.DataFrame:
    """ln IPV y ln IPC alquiler por CCAA y trimestre (código INE) desde ficheros con el formato de data/raw."""
    mp = _nombre_a_cod()
    filas = []
    a = pd.read_csv(Path(dirx) / "ine_ipv_80270.csv", dtype=str)
    a = a[a["nombre"].str.endswith(". General. Índice.")]
    a = a.assign(cod=[_cod_de_territorio(t, mp) for t in a["nombre"]]).dropna(subset=["cod"])
    for (c, p), v in a.groupby(["cod", "periodo"])["valor"]:
        filas.append(("compra", c, _trim(p)[0], np.log(float(v.iloc[0]))))
    f_ccaa = Path(dirx) / "ine_ipc_alquiler.csv"
    if f_ccaa.exists():
        b = pd.read_csv(f_ccaa, dtype=str)
        b = b[b["nombre"].str.endswith(". Alquiler de vivienda. Índice.")]
        b = b.assign(cod=[_cod_de_territorio(t, mp) for t in b["nombre"]]).dropna(subset=["cod"])
        b["q"] = [_trim(p)[0] for p in b["periodo"]]
        b["valor"] = b["valor"].astype(float)
    else:
        b = pd.read_csv(Path(dirx) / "ine_v2_ipc_alquiler_prov.csv", dtype={"codigo": str})
        b = b[(b["medida"] == "IPC_alquiler_vivienda_indice") & (b["nivel"] == "provincia")]
        b = b.assign(cod=b["codigo"].map(PROV_A_CCAA), q=[_trim(p)[0] for p in b["periodo"]])
        b = b.groupby(["cod", "q", "periodo"], as_index=False)["valor"].mean()
    g = b.groupby(["cod", "q"])["valor"].agg(["mean", "count"]).reset_index()
    for r in g[g["count"] >= 3].itertuples():
        filas.append(("alquiler", r.cod, r.q, float(np.log(r.mean))))
    return pd.DataFrame(filas, columns=["mercado", "codigo_ine_ccaa", "trimestre", "ln"])


def nuevos_periodos(destino: Path, despues_de: str) -> list[str]:
    o = observados(destino)
    des = _trim(despues_de)[0] if "Q" not in despues_de else despues_de
    n = o.groupby(["mercado", "trimestre"])["codigo_ine_ccaa"].nunique().unstack("mercado")
    ok = n[(n >= 17).all(axis=1)] if n.shape[1] == 2 else n.iloc[0:0]
    return sorted(q for q in ok.index if q > des)


def _evalua(P, obs, etiqueta):
    O = obs.rename(columns={"trimestre": "trimestre_objetivo"})
    M = P.merge(O, on=["mercado", "codigo_ine_ccaa", "trimestre_objetivo"], how="inner")
    M["e"] = M["ln"] - M["pred_ln"]
    M["e2"] = M["e"] ** 2
    M = M.rename(columns={"codigo_ine_ccaa": "ccaa"})
    if M.empty:
        return dict(resumen=dict(estado="sin observaciones", etiqueta=etiqueta), por_ccaa=[], dm=[], permutacion=[], holm=[])
    mods = sorted(M["modelo"].unique())
    res = M.groupby(["mercado", "modelo", "h"])["e2"].agg(lambda s: float(100 * np.sqrt(s.mean()))).reset_index(name="rmse_x100")
    pc = M.groupby(["mercado", "modelo", "h", "ccaa"])["e2"].mean().reset_index()
    pc["rmse_x100"] = 100 * np.sqrt(pc["e2"])
    comps = [c for c in (BASE, "ar4", "ecm_v1") if c in mods]
    globals_modelos = MODELOS
    try:
        globals()["MODELOS"] = [m for m in mods]
        R = compara(M, BASE, comps, None)
    finally:
        globals()["MODELOS"] = globals_modelos
    cols = ["p_dm_mejor_holm", "p_perm_mejor_holm"]
    bate = R[(R.comparador == BASE) & (R.modelo == "mejor_regional")] if len(R) else R
    resumen = dict(etiqueta=etiqueta, periodos_objetivo=sorted(M["trimestre_objetivo"].unique()), base_fuerte=BASE,
                   n_ccaa=int(M["ccaa"].nunique()), rmse_x100=res.to_dict("records"),
                   h7_p1_mejor_regional_vs_base=bate.to_dict("records"), nota=ROT if etiqueta != "diferida" else "validación diferida")
    return dict(resumen=resumen, por_ccaa=pc.drop(columns="e2").to_dict("records"), dm=R.drop(columns=[c for c in cols if c in R], errors="ignore").to_dict("records") if len(R) else [],
                permutacion=R[["mercado", "h", "modelo", "comparador", "p_perm_mejor", "n_ccaa_mejor"]].to_dict("records") if len(R) else [],
                holm=R[["mercado", "h", "modelo", "comparador", *cols]].to_dict("records") if len(R) else [])


def evaluar_congelado(cong: Path, datos: Path | None, simular: bool) -> dict:
    cong = Path(cong)
    mj = json.loads(cong.read_text(encoding="utf-8"))
    for f, s in mj["ficheros_versionados_sha256"].items():
        assert hashlib.sha256((RAIZ / f).read_bytes()).hexdigest() == s, f"sha256 distinto: {f}"
    pf = RAIZ / mj["predicciones"]["fichero"]
    assert hashlib.sha256(pf.read_bytes()).hexdigest() == mj["predicciones"]["sha256"], "predicciones alteradas"
    if simular:
        # ensayo con corte falso: se reestima con datos hasta 2023Q4 (dentro de la muestra) y se predice 2024Q1-2024Q4
        qs, cods, data = carga_panel()
        o = qs.index("2023Q4")
        rows = []
        for m, (y, X) in data.items():
            for nom in MODELOS:
                pred, _ = run_modelo(nom, y[:, :o + 1], X[:, :o + 1])
                for i, c in enumerate(cods):
                    for k in range(H):
                        rows.append((m, nom, c, k + 1, qs[o + 1 + k], float(pred[i, k]), float(y[i, o])))
        P = pd.DataFrame(rows, columns=["mercado", "modelo", "codigo_ine_ccaa", "h", "trimestre_objetivo", "pred_ln", "y_origen_ln"])
        obs = pd.DataFrame([(m, c, qs[t], data[m][0][i, t]) for m in data for i, c in enumerate(cods) for t in range(o + 1, o + 1 + H)],
                           columns=["mercado", "codigo_ine_ccaa", "trimestre", "ln"])
        return _evalua(P, obs, "simulacion: corte falso 2023Q4, sin descargas")
    P = pd.read_csv(pf, dtype={"codigo_ine_ccaa": str})
    return _evalua(P, observados(Path(datos)), "diferida")


# ------------------------------------------------------------------------------------------------ main
def main(smoke=False):
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registro.csv")
    qs, cods, data = carga_panel()
    E = backtest(qs, cods, data, reg, smoke)
    # RMSE por CCAA, mercado, modelo y horizonte (x100 = puntos log, aprox. %)
    B = E.groupby(["mercado", "modelo", "h", "ccaa"]).agg(rmse_x100=("e2", lambda s: 100 * np.sqrt(s.mean())), n=("e2", "size")).reset_index()
    B["rotulo"] = ROT
    B.to_csv(OUT / "backtest.csv", index=False)
    # mejor modelo por región (candidatos) y si bate a la base fuerte
    Pm = E.groupby(["mercado", "modelo", "ccaa"])["e2"].mean().unstack("modelo")
    mejor, filas = {}, []
    for (m, c), r in Pm.iterrows():
        cand = r[CAND]
        b = cand.idxmin()
        mejor[(m, c)] = b
        filas.append(dict(mercado=m, codigo_ine_ccaa=c, mejor_modelo=b, rmse_mejor_x100=100 * np.sqrt(cand.min()),
                          rmse_base_fuerte_x100=100 * np.sqrt(r[BASE]), rmse_ar4_x100=100 * np.sqrt(r["ar4"]),
                          bate_base_fuerte=bool(cand.min() < r[BASE]),
                          rmse_base_exigente_x100=100 * np.sqrt(r[["persistencia", "ult_crec_nac", BASE]].min()),
                          bate_base_exigente=bool(cand.min() < r[["persistencia", "ult_crec_nac", BASE]].min()), rotulo=ROT + "; h=1-4 agrupados; selección en muestra"))
    MB = pd.DataFrame(filas)
    MB.to_csv(OUT / "mejor_por_region.csv", index=False)
    # DM + permutación + Holm por mercado y horizonte (comparadores: base fuerte, AR(4), ECM v1)
    R = compara(E, BASE, [BASE, "ar4", "ecm_v1"], cods)
    R.insert(R.columns.get_loc("comparador") + 1, "comparador_tipo", R.comparador.map(COMPARADOR))   # v7.2: rótulo del comparador
    R.to_csv(OUT / "dm_permutacion.csv", index=False)
    # mejor regional agregado (selección en muestra): pérdida de cada CCAA con su mejor modelo
    mj_rows = []
    for (m, c), b in mejor.items():
        for h in range(1, H + 1):
            s = E[(E.mercado == m) & (E.ccaa == c) & (E.h == h)]
            mj_rows.append((m, "mejor_regional", h, c, s[s.modelo == b]["e2"].mean(), s[s.modelo == BASE]["e2"].mean(),
                            s[s.modelo == "ar4"]["e2"].mean()))
    MR = pd.DataFrame(mj_rows, columns=["mercado", "modelo", "h", "ccaa", "l", "lb", "l4"])
    h7 = []
    for (m, h), s in MR.groupby(["mercado", "h"]):
        for nm, col in ((BASE, "lb"), ("ar4", "l4")):
            d = (s["l"] - s[col]).to_numpy()
            st, p = dm_hln(d)
            h7.append(dict(mercado=m, h=h, comparador=nm, dm_hln=st, p_dm_mejor=p, p_perm_mejor=perm_signos(d), n_ccaa_mejor=int((d < 0).sum()),
                           rmse_mejor_regional_x100=100 * np.sqrt(s["l"].mean()), rmse_comparador_x100=100 * np.sqrt(s[col].mean())))
    H7 = pd.DataFrame(h7)
    for c in ("p_dm_mejor", "p_perm_mejor"):
        H7[c + "_holm"] = holm(H7[c].to_numpy())
    H7["nota"] = "selección en muestra (optimista); la validación honesta es la diferida (H7-P1)"
    H7.insert(H7.columns.get_loc("comparador") + 1, "comparador_tipo", H7.comparador.map(COMPARADOR))   # v7.2: rótulo del comparador
    H7.to_csv(OUT / "h7_p1_mejor_regional.csv", index=False)
    P = congela(qs, cods, data, E, mejor)
    reg.flush()
    escribe_salidas(E, B, MB, R, H7, qs, P)
    return 0


COMPARADOR = {"ar_factor": "base fuerte (AR con factor común; no es la más exigente)", "ar4": "AR(4)", "ecm_v1": "ECM v1 (nacional)",
              "persistencia": "persistencia", "ult_crec_nac": "último crecimiento nacional"}


def escribe_salidas(E, B, MB, R, H7, qs, P):
    sha = hashlib.sha256((OUT / "modelos_congelados.json").read_bytes()).hexdigest()
    pr = {}
    for m in MERC:
        s = MB[MB.mercado == m]
        pr[m] = dict(bate=int(s.bate_base_fuerte.sum()), n=len(s), exig=int(s.bate_base_exigente.sum()))
    rm1 = E[E.h == 1].groupby(["mercado", "modelo"])["e2"].mean().pipe(lambda s: 100 * np.sqrt(s)).unstack("modelo")
    lines = [f"# R5 · Predicción regional y congelación ({ROT})", "",
             f"Capa C4 (predicción, no causalidad). Backtest de origen móvil {ORIGEN_INI}..{qs[-2]}, h=1-4, estimación solo con datos "
             f"hasta cada origen. Datos hasta {qs[-1]} (panel_ccaa_q_v7). RMSE en puntos log x100 (aprox. %).", "",
             "## Mejor candidato por región frente a la base fuerte (AR con factor común), h=1-4 agrupados", ""]
    for m, v in pr.items():
        lines.append(f"- {m}: el mejor candidato bate a la base fuerte en {v['bate']} de {v['n']} CCAA; frente a la más exigente "
                     f"(mín. de persistencia, ult_crec_nac y ar_factor): {v['exig']} de {v['n']} (selección en muestra: optimista).")
    lines += ["", "**Comparadores (v7.2).** «Base fuerte» = ar_factor (AR con factor común). «Base más exigente» = el mínimo, por CCAA, de "
              "persistencia, ult_crec_nac y ar_factor. Solo «predice mejor» quien bate a la más exigente.", "",
              "## RMSE x100 a h=1 (17 CCAA, todos los orígenes; sin comparador: errores de cada modelo)", "", rm1.round(3).to_markdown(), "",
              "## H7-P1 (mejor regional frente a cada comparador de la columna «comparador_tipo»: base fuerte o AR(4); agregado de 17 CCAA; en muestra, con Holm)", "",
              H7.round(4).to_markdown(index=False), "",
              "## Notas", "- ECM v1 no es replicable por CCAA: se usa un ECM nacional (spec A) con ajuste por nivel.",
              "- PMG sin demeaning ni ajuste de rupturas (se predice en niveles); dX futuro = 0.",
              "- GBM: 1 configuración fija (sin búsqueda). Mixto: pendiente aleatoria en el retardo 1, con alternativas si no converge.",
              "- Un modelo solo «predice mejor» si supera a la base más exigente; los p son por CCAA (n=17), DM-HLN y permutación de signo, Holm por mercado, horizonte y comparador.",
              f"- Congelación: output/v7/R5/modelos_congelados.json (sha256 {sha}).", ""]
    (OUT / "resumen.md").write_text("\n".join(lines), encoding="utf-8")
    fm = {}
    for m in MERC:
        s = H7[(H7.mercado == m) & (H7.comparador == "ar4") & (H7.h == 1)].iloc[0]
        fm[m] = dict(rmse=float(s.rmse_mejor_regional_x100), p_dm=float(s.p_dm_mejor))
    res = dict(rama="R5", pregunta="¿Algún modelo regional bate fuera de muestra (origen móvil, h=1-4) a la base fuerte K1, a AR(4) y a ECM v1 en 17 CCAA?",
               capa="C4", datos=f"data/processed/v7/panel_ccaa_q_v7.csv (17 CCAA, 2007Q1-{qs[-1]}); medida_precio: IPV del INE (CCAA) y IPC alquiler (stock)",
               N=int(len(E)), metodo="backtest de origen móvil con reestimación; DM-HLN y permutación de signo sobre 17 CCAA; Holm; " + ROT,
               estimacion=MB.groupby("mercado")["bate_base_fuerte"].sum().astype(int).to_dict(), ic95=None,
               p_ajustado=H7.set_index(["mercado", "h", "comparador"])["p_dm_mejor_holm"].round(4).rename(lambda x: str(x)).to_dict() if False else
               {f"{a}|h{b}|{c}": float(v) for (a, b, c), v in H7.set_index(["mercado", "h", "comparador"])["p_dm_mejor_holm"].items()},
               nivel_evidencia="EXPLORATORIO", diagnosticos=dict(n_regiones=17, congelacion_sha256=sha),
               fuera_muestra=dict(modelo="mejor_regional (selección en muestra)", rmse={k: v["rmse"] for k, v in fm.items()},
                                  dm_vs_ar4={k: v["p_dm"] for k, v in fm.items()}),
               notas="Informativo, muestra ya vista en v1; la prueba honesta es la validación diferida (H7-P1). Sin lenguaje causal.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    hechos = []
    for j, m in enumerate(MERC, 1):
        s = MB[MB.mercado == m]
        hechos.append(dict(id=f"V7-R5-{j:03d}", indicador=f"CCAA donde el mejor candidato bate a la base fuerte ({m}), h=1-4 [comparador: base fuerte = AR con factor común; frente a la base más exigente, ver V71-S3-R5-exigente-{m}]",
                           valor=int(s.bate_base_fuerte.sum()), min=0, max=17, unidad="CCAA de 17",
                           periodo=f"origenes {ORIGEN_INI}-{qs[-2]}", cobertura="17 CCAA", fuentes=["INE IPV 80270", "INE IPC alquiler", "R1 panel"],
                           capa="C4", fecha_dato=FECHA))
        hechos.append(dict(id=f"V7-R5-{j + 2:03d}", indicador=f"RMSE x100 de la base fuerte a h=1 ({m})", valor=float(rm1.loc[m, BASE]),
                           min=float(B[(B.mercado == m) & (B.modelo == BASE) & (B.h == 1)].rmse_x100.min()),
                           max=float(B[(B.mercado == m) & (B.modelo == BASE) & (B.h == 1)].rmse_x100.max()), unidad="puntos log x100",
                           periodo=f"origenes {ORIGEN_INI}-{qs[-2]}", cobertura="17 CCAA", fuentes=["INE IPV 80270", "INE IPC alquiler"],
                           capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main("--smoke" in sys.argv))
