"""BM bloque 4 (nacional, objetivo A): ARDL, ECM de umbral, BVAR Minnesota (verosimilitud marginal) y TVP-VAR con
olvido exponencial. Predicción DIRECTA/iterada a h=4 del objetivo y_{t+4} = ln IPV real_{t+4} - ln IPV real_t.
Parámetros estimados con datos <= L (último periodo de entrenamiento del split); a los orígenes de test solo se
usan retardos (información en t). Sin red; deterministas."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import v2_common as vc  # noqa: E402

H = 4
ECM_X = ["ln_ocupados", "tipo_hip_real", "ln_permisos_l4", "ln_costes_real"]
LAMBDAS = (0.05, 0.1, 0.2, 0.4, 1.0)
KAPPAS = (0.95, 0.99)
P_VAR = 2


def _long_ecm(nac: pd.DataFrame, tmax: str = vc.Q_TRAIN_FIN):
    """Rejilla nacional con las variables del ECM v1 (misma construcción que v2_common.ecm_v1_nacional)."""
    q0 = vc.Q_TRAIN_FIN
    d = vc._prep(nac, None, tmax)
    d = vc._nac_x(d)
    long, per, units = vc._grid(d, vc._lvl_fn("ln_ipv", True))
    lvl = long["lvl"]
    long["dY"] = lvl - vc._g(long, lvl, 1)
    long["yh"] = vc._g(long, lvl, -H) - lvl
    for k in range(4):
        long[f"dY_l{k}"] = vc._g(long, long["dY"], k) if k else long["dY"]
    long["dOcup"] = long["ln_ocupados"] - vc._g(long, long["ln_ocupados"], 1)
    long["dTipo"] = long["tipo_hip"] - vc._g(long, long["tipo_hip"], 1)
    long["dRenta"] = long["ln_renta_hog_real"] - vc._g(long, long["ln_renta_hog_real"], 1)
    long["dCred"] = long["ln_credito_nuevo"] - vc._g(long, long["ln_credito_nuevo"], 1)
    long["dTipoR"] = long["tipo_hip_real"] - vc._g(long, long["tipo_hip_real"], 1)
    long["dY_l3"] = vc._g(long, long["dY"], 3)
    for v in ("dOcup", "dTipo", "dRenta", "dCred"):
        long[f"{v}_l1"] = vc._g(long, long[v], 1)
    del q0
    return long, per, units


def _salida(lg, pred: pd.Series, per, etiqueta, sid, h=H):
    sub = lg.loc[pred.index]
    obj = [per[p + h] if p + h < len(per) else None for p in sub["pos"]]
    return pd.DataFrame({"periodo": sub["trimestre"].values, "periodo_obj": obj, "unidad": sub["unidad"].values,
                         "y_real": sub["yh"].values, "y_pred": pred.values, "modelo": etiqueta, "split": sid, "h": h})


def _vacio():
    return pd.DataFrame(columns=["periodo", "periodo_obj", "unidad", "y_real", "y_pred", "modelo", "split", "h"])


def ardl(long, per, splits, etiqueta="ARDL"):
    """ARDL(4; Δx con 0 y 1 retardos): AR(4) de Δy + Δocup, Δtipo, Δrenta, Δcrédito (t, t-1) + dummies del trimestre
    objetivo; MCO por split."""
    fcols = [f"dY_l{k}" for k in range(4)] + [f"{v}{s}" for v in ("dOcup", "dTipo", "dRenta", "dCred") for s in ("", "_l1")]
    rows = []
    for sid, (itr, ite) in enumerate(splits):
        res = vc._fit_predict(long, int(itr[-1]), set(ite.tolist()), fcols, ["ES"], H)
        if res is not None:
            rows.append(_salida(long, res[0], per, etiqueta, sid))
    return pd.concat(rows, ignore_index=True) if rows else _vacio()


def tar_ecm(long, per, splits, variante: str, etiqueta=None):
    """ECM v1 directo con dos regímenes en el ajuste: 'asim' = ECT>0 vs ECT<=0 (sobrevaloración/infravaloración);
    'credito' = ECT interactuado con 1[Δ4 ln crédito nuevo > 0]. DOLS del ECT estimado solo con datos <= L."""
    base = ["dOcup", "dTipo", "dRenta", "dY_l3", "dCred"]
    rows = []
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        r = vc._dols(long, posL, "lvl", ECM_X, ["ES"])
        if r is None:
            continue
        ect, meta = r
        lg = long.copy()
        e = ect(lg)
        if variante == "asim":
            lg["ect_a"], lg["ect_b"] = e * (e > 0), e * (e <= 0)
        else:
            f = (lg["d4_ln_credito_nuevo"] > 0).astype(float).where(lg["d4_ln_credito_nuevo"].notna())
            lg["ect_a"], lg["ect_b"] = e * f, e * (1 - f)
        res = vc._fit_predict(lg, posL, set(ite.tolist()), ["ect_a", "ect_b"] + base, ["ES"], H)
        if res is not None:
            rows.append(_salida(lg, res[0], per, etiqueta or f"TAR_ECM_{variante}", sid))
    return pd.concat(rows, ignore_index=True) if rows else _vacio()


# ------------------------------------------------------------------ VAR bayesiano
def _var_data(long, cols):
    Y = long[cols].values.astype(float)
    ok = ~np.isnan(Y).any(axis=1)
    return Y, ok


def _xy(Y, p):
    T, n = Y.shape
    X = np.column_stack([Y[p - l:T - l] for l in range(1, p + 1)] + [np.ones(T - p)])
    return X, Y[p:]


def _sigmas(Y):
    s = []
    for i in range(Y.shape[1]):
        y, x = Y[1:, i], np.column_stack([Y[:-1, i], np.ones(len(Y) - 1)])
        b = np.linalg.lstsq(x, y, rcond=None)[0]
        s.append(max(np.std(y - x @ b, ddof=2), 1e-6))
    return np.array(s)


def _dummies(sig, lam, p, eps=1e-4):
    n = len(sig)
    k = n * p + 1
    J = np.diag(np.arange(1, p + 1, dtype=float))
    Xd1 = np.hstack([np.kron(J, np.diag(sig)) / lam, np.zeros((n * p, 1))])
    Yd1 = np.zeros((n * p, n))                  # media a priori 0 (variables en diferencias)
    Yd2, Xd2 = np.diag(sig), np.zeros((n, k))
    Yd3, Xd3 = np.zeros((1, n)), np.hstack([np.zeros((1, n * p)), [[eps]]])
    return np.vstack([Yd1, Yd2, Yd3]), np.vstack([Xd1, Xd2, Xd3])


def _logml(Y, X, sig, lam, p):
    n = Y.shape[1]
    k = X.shape[1]
    Yd, Xd = _dummies(sig, lam, p)
    Ys, Xs = np.vstack([Yd, Y]), np.vstack([Xd, X])
    ld = lambda M: np.linalg.slogdet(M)[1]   # noqa: E731
    Bd = np.linalg.solve(Xd.T @ Xd, Xd.T @ Yd)
    Sd = (Yd - Xd @ Bd).T @ (Yd - Xd @ Bd)
    Bs = np.linalg.solve(Xs.T @ Xs, Xs.T @ Ys)
    Ss = (Ys - Xs @ Bs).T @ (Ys - Xs @ Bs)
    Td, T = Yd.shape[0], Y.shape[0]
    return (n / 2) * (ld(Xd.T @ Xd) - ld(Xs.T @ Xs)) - ((Td + T - k) / 2) * ld(Ss) + ((Td - k) / 2) * ld(Sd), Bs


def _iterar(B, hist, p, h):
    """Pronóstico puntual iterado h pasos; hist: últimas p filas (orden cronológico). Devuelve filas pronosticadas."""
    n = B.shape[1]
    buf = [r.copy() for r in hist[-p:]]
    out = []
    for _ in range(h):
        x = np.concatenate([buf[-l] for l in range(1, p + 1)] + [[1.0]])
        f = x @ B
        out.append(f)
        buf.append(f)
    return np.array(out)


def var_modelos(long, per, splits, cols, modo: str, parametro: float, etiqueta: str):
    """modo 'bvar' (parametro = λ de Minnesota, fijo; la elección entre λ se hace por verosimilitud marginal y se
    informa en `elegido`) o 'tvp' (parametro = κ, factor de olvido). y = primera columna de `cols`."""
    Y, ok = _var_data(long, cols)
    p = P_VAR
    rows, lam_ml = [], {}
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        idx = np.where(ok & (long["pos"].values <= posL))[0]
        if len(idx) < 14:
            continue
        # tramo contiguo final de datos completos
        brk = np.where(np.diff(idx) != 1)[0]
        idx = idx[(brk[-1] + 1 if len(brk) else 0):]
        Ytr = Y[idx]
        if len(Ytr) < 14:
            continue
        sig = _sigmas(Ytr)
        X, Yt = _xy(Ytr, p)
        if modo == "bvar":
            lml, B = _logml(Yt, X, sig, parametro, p)
            lam_ml[sid] = {l: _logml(Yt, X, sig, l, p)[0] for l in LAMBDAS}
            Bs = [B] * 1
        else:
            Bs = [_tvp(Ytr, sig, p, parametro)]
        B = Bs[0]
        for t in ite:
            pos = long.index[long["pos"] == t]
            if len(pos) == 0:
                continue
            i = pos[0]
            if i - p + 1 < 0 or np.isnan(Y[i - p + 1:i + 1]).any():
                continue
            fc = _iterar(B, Y[i - p + 1:i + 1], p, H)
            rows.append(pd.DataFrame({"periodo": [long.at[i, "trimestre"]],
                                      "periodo_obj": [per[t + H] if t + H < len(per) else None],
                                      "unidad": ["ES"], "y_real": [long.at[i, "yh"]], "y_pred": [fc[:, 0].sum()],
                                      "modelo": etiqueta, "split": sid, "h": H}))
    out = pd.concat(rows, ignore_index=True) if rows else _vacio()
    out.attrs["logml"] = lam_ml
    return out


def _tvp(Y, sig, p, kappa, lam0=0.2, decay=0.98):
    """TVP-VAR ecuación por ecuación con olvido exponencial (Koop y Korobilis 2013), SIMPLIFICACIÓN de Primiceri
    (2005): sin volatilidad estocástica ni jerarquía; coeficientes paseo aleatorio con P_{t|t-1} = P_{t-1}/κ.
    Devuelve los coeficientes filtrados al final de la muestra de entrenamiento (k x n), que se mantienen fijos."""
    n = Y.shape[1]
    X, Yt = _xy(Y, p)
    k = X.shape[1]
    B = np.zeros((k, n))
    for i in range(n):
        v = np.empty(k)
        for l in range(1, p + 1):
            for j in range(n):
                v[(l - 1) * n + j] = (lam0 * sig[i] / (l * sig[j])) ** 2
        v[-1] = (10 * sig[i]) ** 2
        P, b, h = np.diag(v), np.zeros(k), sig[i] ** 2
        for t in range(len(Yt)):
            z = X[t]
            Pp = P / kappa
            e = Yt[t, i] - z @ b
            S = z @ Pp @ z + h
            K = Pp @ z / S
            b = b + K * e
            P = Pp - np.outer(K, z @ Pp)
            h = max(decay * h + (1 - decay) * e * e, 1e-10)
        B[:, i] = b
    return B
