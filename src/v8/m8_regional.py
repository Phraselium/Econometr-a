#!/usr/bin/env python3
"""V8-F4 M8: descomposicion regional. 17 CCAA (factor comun + variables regionales por periodo, panel FE con Driscoll-Kraay,
LP en panel), Comunitat Valenciana por provincia (03, 12, 46) y Valencia ciudad (descriptivo + contabilidad). Todo C4
(asociacion, sin lectura causal); C1 solo en las cifras descriptivas con >= 2 fuentes concordantes.
Uso: python3 src/v8/m8_regional.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402
from statsmodels.stats.multitest import multipletests  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry  # noqa: E402
from herramientas.lp import lp_panel  # noqa: E402
from m1_factor_comun import (COLS_ATR, COLS_COEF, PERS, bandas, cargar, fila_coef, idx_bloques, matriz,  # noqa: E402
                             pc1, periodo_de)

SEED = 20261010
D = RAIZ / "data" / "processed" / "v8"
SCRIPT = "src/v8/m8_regional.py"
AVISO = ("C4: asociacion estadistica condicional; sin lectura causal. Ecuaciones por CCAA y periodo con pocos trimestres "
         "(P4 = 9): bandas aproximadas. El factor comun y las covariables regionales son colineales por construccion (VIF en coeficientes.csv).")
FACTOR_DE = {"ocupados": "empleo_renta", "paro": "empleo_renta", "pob_total": "demografia", "pob_extranj": "demografia",
             "visados": "oferta", "tx_extranj": "demanda_externa", "turismo": "turismo"}
NOMBRES_CCAA = {}


def qi(s):
    a, q = str(s).split("Q")
    return int(a) * 4 + int(q) - 1


def tidy_p(b, se, df):
    t = b / se if se > 0 else np.nan
    return t, 2 * (1 - stats.t.cdf(abs(t), df)) if np.isfinite(t) else np.nan


def ols_hac(y, X, L):
    """MCO con varianza Newey-West (Bartlett, L retardos). Devuelve beta, ee, r2, r2a, n."""
    n, k = X.shape
    be, *_ = np.linalg.lstsq(X, y, rcond=None)
    u = y - X @ be
    XtXi = np.linalg.inv(X.T @ X)
    G = X * u[:, None]
    S = G.T @ G
    for l in range(1, L + 1):
        w = 1 - l / (L + 1)
        Gl = G[l:].T @ G[:-l]
        S += w * (Gl + Gl.T)
    V = XtXi @ S @ XtXi * n / max(1, n - k)
    r2 = 1 - (u @ u) / ((y - y.mean()) @ (y - y.mean()))
    return be, np.sqrt(np.diag(V)), float(r2), float(1 - (1 - r2) * (n - 1) / max(1, n - k)), n


# ------------------------------------------------------------------ panel FE (numpy) para bootstrap de contribuciones
def within_ols(Y, Xs, ix=None):
    """Y: E x T; Xs: lista de E x T. Estimador intragrupo con T remuestreado (ix). Devuelve gamma (K,)."""
    if ix is not None:
        Y = Y[:, ix]
        Xs = [x[:, ix] for x in Xs]
    Yd = Y - Y.mean(1, keepdims=True)
    A = np.column_stack([(x - x.mean(1, keepdims=True)).ravel() for x in Xs])
    g, *_ = np.linalg.lstsq(A, Yd.ravel(), rcond=None)
    return g


def contribs_panel(Y, Xs, ix=None):
    """Contribuciones por entidad: gamma_k * media_t(x_ik) * T/4 y total media(y)*T/4. Devuelve (E x K, E)."""
    g = within_ols(Y, Xs, ix)
    if ix is not None:
        Y = Y[:, ix]
        Xs = [x[:, ix] for x in Xs]
    T = Y.shape[1]
    C = np.column_stack([g[k] * Xs[k].mean(1) * T / 4 for k in range(len(Xs))])
    return C, Y.mean(1) * T / 4


def vif_max(A):
    if A.shape[1] < 2:
        return np.nan
    R = np.corrcoef(A, rowvar=False)
    try:
        return float(np.max(np.diag(np.linalg.inv(R))))
    except np.linalg.LinAlgError:
        return np.inf


def main(rapido=False, salida=None):
    t0 = time.time()
    out = Path(salida) if salida else RAIZ / "output" / "v8" / "M8"
    out.mkdir(parents=True, exist_ok=True)
    B = 99 if rapido else 399
    reg = Registry(out / "registro.csv")
    rng = np.random.default_rng(SEED + 8)
    avisos = []
    p = cargar()
    nombres = p[["codigo_ine_ccaa", "ccaa"]].drop_duplicates().set_index("codigo_ine_ccaa")["ccaa"].to_dict()
    per = periodo_de(p)
    ipc = p.groupby("trimestre")["ipc_general"].first()
    medida = {"compra": "valor tasado real por CCAA (valor_tasado_ccaa / IPC general)", "alquiler": "IPC alquiler real por CCAA (ipc_alquiler / IPC general)"}
    Y = {"compra": matriz(p, "valor_tasado_ccaa").dropna(), "alquiler": matriz(p, "ipc_alquiler").dropna()}
    Fm = {}
    for m in Y:
        f0 = pd.Series(pc1(Y[m].values), index=Y[m].index)
        # factor en puntos de crecimiento interanual: pendiente media = 1 y nivel = media transversal de la muestra completa
        lam = float(np.mean([np.cov(Y[m][c].values, f0.values)[0, 1] / f0.var() for c in Y[m].columns]))
        Fm[m] = f0 * lam + float(Y[m].values.mean())

    # covariables (100 x d4 log; paro: diferencia interanual en pp)
    def wide(col, fn):
        w = p.pivot(index="trimestre", columns="codigo_ine_ccaa", values=col)
        return fn(w)
    d4l = lambda w: 100 * (np.log(w) - np.log(w.shift(4)))  # noqa: E731
    COV = {"ocupados": wide("ocupados", d4l), "paro": wide("tasa_paro_epa", lambda w: w - w.shift(4)),
           "pob_total": wide("pob_total", d4l), "pob_extranj": wide("pob_extranj", d4l),
           "visados": wide("visados", lambda w: d4l(w.where(w > 0))), "tx_extranj": wide("tx_extranj_ccaa", lambda w: d4l(w.where(w > 0)))}
    TUR = wide("turistas_ccaa", lambda w: d4l(w.where(w > 0)))

    coefs, atr, filas_cuota = [], [], []

    # ------------------------------------------------------------ 1. por CCAA y periodo: y = a + b F
    for m in ("compra", "alquiler"):
        for pe in PERS:
            ix = [t for t in Y[m].index if per.get(t) == pe]
            if len(ix) < 8:
                avisos.append(f"{m} {pe}: {len(ix)} trimestres (<8), sin ecuacion por CCAA")
                continue
            f = Fm[m].loc[ix].values
            L = max(1, min(4, len(ix) // 4))
            for c in Y[m].columns:
                y = Y[m].loc[ix, c].values
                X = np.column_stack([np.ones(len(ix)), f])
                be, ee, r2, r2a, n = ols_hac(y, X, L)
                bs = np.empty(B)
                bshare = np.empty(B)
                for b in range(B):
                    j = idx_bloques(n, max(2, min(4, n // 3)), rng)
                    bb, *_ = np.linalg.lstsq(X[j], y[j], rcond=None)
                    u = y[j] - X[j] @ bb
                    bs[b] = bb[1] * f[j].mean() * n / 4
                    bshare[b] = 1 - (u @ u) / max(1e-12, ((y[j] - y[j].mean()) ** 2).sum())
                t, pv = tidy_p(be[1], ee[1], n - 2)
                tc = stats.t.ppf(0.975, n - 2)
                mid = f"M8_ccaa{c}_{m}_{pe}"
                coefs.append(fila_coef(modelo_id=mid, familia_modelo="ols_ccaa_factor", mercado=m, ambito=f"ccaa:{c}", periodo=pe,
                                       dependiente="d4 ln precio real x100", transformacion="interanual", medida_precio=medida[m],
                                       variable="factor_comun", beta=be[1], ee=ee[1], tipo_ee=f"Newey-West L={L}", t=t, p=pv,
                                       ic95_lo=be[1] - tc * ee[1], ic95_hi=be[1] + tc * ee[1], n=n, r2=r2, r2_adj=r2a, capa="C4",
                                       beta_std=be[1] / max(1e-12, y.std())))
                bd = bandas(bshare)
                filas_cuota.append(dict(mercado=m, ambito=f"ccaa:{c}", ccaa=nombres[c], periodo=pe, n=n, cuota_comun=r2,
                                        cuota_idiosincratica=1 - r2, b90_lo_comun=bd["b90_lo"], b90_hi_comun=bd["b90_hi"],
                                        carga=be[1], media_crec=float(y.mean())))
                # atribucion regional (factor comun vs resto) por CCAA con bandas
                tot = float(y.mean() * n / 4)
                cf = float(be[1] * f.mean() * n / 4)
                bt = bandas(bs)
                atr.append(dict(metodo="regional_ccaa_ols", mercado=m, ambito=f"ccaa:{c}", periodo=pe, factor="factor_comun", contribucion_pp=cf,
                                pct_total=cf / tot if abs(tot) > 1e-9 else np.nan, b68_lo=bt["b68_lo"], b68_hi=bt["b68_hi"], b90_lo=bt["b90_lo"],
                                b90_hi=bt["b90_hi"], capa="C4", notas=f"ecuacion por CCAA y = a + b F (n={n}); variacion acumulada aprox. = media interanual x trimestres/4"))
                atr.append(dict(metodo="regional_ccaa_ols", mercado=m, ambito=f"ccaa:{c}", periodo=pe, factor="residuo", contribucion_pp=tot - cf,
                                pct_total=(tot - cf) / tot if abs(tot) > 1e-9 else np.nan, b68_lo=np.nan, b68_hi=np.nan, b90_lo=np.nan, b90_hi=np.nan,
                                capa="C4", notas=f"idiosincratico (constante + residuo); total periodo {tot:.1f} pp; banda no calculada (resto)"))
                reg.log("M8_ccaa", mid, "y ~ 1 + F", ix[0], ix[-1], n, r2a, np.nan, np.nan, coef_interes=be[1], p_interes=pv,
                        notas=f"{m} {pe} ccaa {c}; NW L={L}")
    cuota = pd.DataFrame(filas_cuota)
    cuota.to_csv(out / "cuota_ccaa.csv", index=False)

    # ------------------------------------------------------------ 2. panel FE con covariables regionales por periodo
    def panel_modelo(m, pe, covs_cand, tag, ccaas=None):
        Ym = Y[m]
        ixp = [t for t in Ym.index if per.get(t) == pe]
        if len(ixp) < 8:
            return None
        cols = [c for c in Ym.columns if ccaas is None or c in ccaas]
        covs = {k: v for k, v in covs_cand.items()}
        usa = list(covs)

        def balanceados(us):
            ok = pd.Series(True, index=ixp)
            for k in us:
                ok &= covs[k].loc[ixp, cols].notna().all(axis=1)
            return [t for t in ixp if ok[t]]
        qs = balanceados(usa)
        while len(qs) < max(8, 0.65 * len(ixp)) and usa:
            cobertura = {k: covs[k].loc[ixp, cols].notna().all(axis=1).mean() for k in usa}
            usa.remove(min(cobertura, key=cobertura.get))
            qs = balanceados(usa)
        if len(qs) < 6:
            return None
        Yp = Ym.loc[qs, cols].T.values
        Xs = [np.tile(Fm[m].loc[qs].values, (len(cols), 1))] + [covs[k].loc[qs, cols].T.values for k in usa]
        nombres_x = ["factor_comun"] + usa
        E, T = Yp.shape
        # linearmodels: DK
        from linearmodels.panel import PanelOLS
        idx = pd.MultiIndex.from_product([cols, [qi(t) for t in qs]], names=["ccaa", "t"])
        dfX = pd.DataFrame({n: x.ravel() for n, x in zip(nombres_x, Xs)}, index=idx)
        dy = pd.Series(Yp.ravel(), index=idx)
        bw = max(1, min(4, T // 3))
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = PanelOLS(dy, dfX, entity_effects=True).fit(cov_type="kernel", kernel="bartlett", bandwidth=bw)
        vm = vif_max(np.column_stack([x.ravel() for x in Xs]))
        mid = f"M8_panel_{tag}_{m}_{pe}"
        tc = stats.t.ppf(0.975, max(1, T - 1))
        for n_ in nombres_x:
            b_, se_ = float(r.params[n_]), float(r.std_errors[n_])
            t_, pv_ = tidy_p(b_, se_, max(1, T - 1))
            coefs.append(fila_coef(modelo_id=mid, familia_modelo="panel_fe_dk", mercado=m, ambito="ccaa_panel", periodo=pe,
                                   dependiente="d4 ln precio real x100", transformacion="interanual", medida_precio=medida[m], variable=n_,
                                   beta=b_, ee=se_, tipo_ee=f"Driscoll-Kraay bw={bw}", t=t_, p=pv_, ic95_lo=b_ - tc * se_, ic95_hi=b_ + tc * se_,
                                   n=int(r.nobs), r2=float(r.rsquared), r2_adj=np.nan, vif_max=vm, capa="C4"))
        reg.log("M8_panel", mid, "y ~ F + " + " + ".join(usa) + " + FE", qs[0], qs[-1], int(r.nobs), np.nan, np.nan, np.nan,
                coef_interes=float(r.params["factor_comun"]), p_interes=float(r.pvalues["factor_comun"]),
                notas=f"covariables usadas {usa}; E={E}, T={T}; DK bw={bw}")
        # contribuciones por CCAA con bandas (bootstrap por bloques de trimestres, mismo para todas las CCAA)
        C0, tot0 = contribs_panel(Yp, Xs)
        Cb = np.empty((B, E, len(Xs)))
        Tb = np.empty((B, E))
        for b in range(B):
            jj = idx_bloques(T, max(2, min(4, T // 3)), rng)
            Cb[b], Tb[b] = contribs_panel(Yp, Xs, jj)
        grupos = {}
        for k, n_ in enumerate(nombres_x):
            grupos.setdefault("factor_comun" if n_ == "factor_comun" else FACTOR_DE[n_], []).append(k)
        for e, c in enumerate(cols):
            suma0 = 0.0
            for fac, ks in grupos.items():
                v0 = float(C0[e, ks].sum())
                vb = Cb[:, e, ks].sum(axis=1)
                bd = bandas(vb)
                suma0 += v0
                atr.append(dict(metodo="regional_panel", mercado=m, ambito=f"ccaa:{c}", periodo=pe, factor=fac, contribucion_pp=v0,
                                pct_total=v0 / tot0[e] if abs(tot0[e]) > 1e-9 else np.nan, b68_lo=bd["b68_lo"], b68_hi=bd["b68_hi"],
                                b90_lo=bd["b90_lo"], b90_hi=bd["b90_hi"], capa="C4",
                                notas=f"panel FE {tag} (covariables {usa}); gamma comun a las CCAA; contribucion = gamma x media regional x T/4"))
            rb = Tb[:, e] - Cb[:, e, :].sum(axis=1)
            bd = bandas(rb)
            atr.append(dict(metodo="regional_panel", mercado=m, ambito=f"ccaa:{c}", periodo=pe, factor="residuo", contribucion_pp=float(tot0[e] - suma0),
                            pct_total=(tot0[e] - suma0) / tot0[e] if abs(tot0[e]) > 1e-9 else np.nan, b68_lo=bd["b68_lo"], b68_hi=bd["b68_hi"],
                            b90_lo=bd["b90_lo"], b90_hi=bd["b90_hi"], capa="C4", notas=f"efecto fijo + residuo; panel FE {tag}; total {tot0[e]:.1f} pp"))
        return dict(modelo=mid, covs=usa, T=T, E=E)

    resumen_paneles = []
    # los paneles reemplazan, para la atribucion 'regional_panel', las contribuciones de la ecuacion solo-factor (se conservan ambas: nota)
    atr_solo_factor = list(atr)
    atr.clear()
    for m in ("compra", "alquiler"):
        for pe in PERS:
            r_ = panel_modelo(m, pe, COV, "cov")
            if r_:
                resumen_paneles.append(dict(mercado=m, periodo=pe, **r_))
            else:
                avisos.append(f"panel {m} {pe}: sin trimestres suficientes")
    # sensibilidad turismo (6 CCAA)
    cols_t = [c for c in TUR.columns if TUR[c].notna().sum() >= 20]
    for m in ("compra",):
        for pe in ("P3", "P4", "P5"):
            cov_t = dict(COV)
            cov_t["turismo"] = TUR
            # solo sub-panel con turismo
            r_ = panel_modelo(m, pe, {k: cov_t[k] for k in ("ocupados", "pob_total", "tx_extranj", "turismo")}, "turismo_sens", ccaas=cols_t)
            if r_:
                resumen_paneles.append(dict(mercado=m, periodo=pe, **r_))
    atr_panel = atr
    atr_all = atr_solo_factor + atr_panel

    # ------------------------------------------------------------ 3. LP panel (DK) por periodo
    plog = p.copy()
    plog["t"] = plog["trimestre"].map(qi)
    plog["periodo"] = plog["trimestre"].map(per)
    plog["y_compra"] = 100 * (np.log(plog["valor_tasado_ccaa"]) - np.log(plog["ipc_general"]))
    plog["y_alquiler"] = 100 * (np.log(plog["ipc_alquiler"]) - np.log(plog["ipc_general"]))
    for m in ("compra", "alquiler"):
        dq = plog.pivot(index="trimestre", columns="codigo_ine_ccaa", values="valor_tasado_ccaa" if m == "compra" else "ipc_alquiler")
        dq = 100 * (np.log(dq.div(ipc, axis=0)).diff())
        fq = pd.Series(pc1(dq.dropna().values), index=dq.dropna().index)
        plog[f"fq_{m}"] = plog["trimestre"].map(fq)
    plog["s_ocupados"] = 100 * plog["d_ln_ocupados"]
    plog["s_pob_total"] = 100 * plog["d_ln_pob_total"]
    plog["s_tx_extranj"] = 100 * plog["d_ln_trans_extranjeros"]
    lp_rows = []
    for m in ("compra", "alquiler"):
        shocks = {"factor_comun": f"fq_{m}", "ocupados": "s_ocupados", "pob_total": "s_pob_total", "tx_extranj": "s_tx_extranj"}
        for pe in PERS + ["completo"]:
            sub = plog if pe == "completo" else plog[plog["periodo"] == pe]
            for sn, sc in shocks.items():
                dd = sub[["codigo_ine_ccaa", "t", f"y_{m}", sc]].dropna()
                nmin = dd.groupby("codigo_ine_ccaa").size().min() if len(dd) else 0
                H = min(8 if pe != "P4" else 3, (nmin - 4) // 2)
                if H < 3:
                    continue
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        r = lp_panel(dd.rename(columns={sc: "shock"}), f"y_{m}", "shock", "codigo_ine_ccaa", "t", H=H, rezagos=1, cov="dk")
                except Exception as ex:  # noqa: BLE001
                    avisos.append(f"lp_panel {m} {pe} {sn}: {type(ex).__name__}")
                    continue
                for _, rr in r.iterrows():
                    lp_rows.append(dict(mercado=m, periodo=pe, impulso=sn, h=int(rr["h"]), beta=rr["beta"], ee=rr["se"], ic95_lo=rr["lo"], ic95_hi=rr["hi"],
                                        n=int(rr["n"]), p=2 * (1 - stats.norm.cdf(abs(rr["beta"] / rr["se"]))) if rr["se"] > 0 else np.nan))
                reg.log("M8_lp_panel", f"M8_lp_{m}_{pe}_{sn}", "y_{t+h} ~ shock + y_{t-1} + shock_{t-1} + FE", dd["t"].min(), dd["t"].max(), len(dd), np.nan,
                        np.nan, np.nan, coef_interes=float(r.loc[r.h == min(4, H), "beta"].iloc[0]), p_interes=np.nan,
                        notas=f"LP panel Driscoll-Kraay h<= {H}; C4")
    lp = pd.DataFrame(lp_rows)
    if len(lp):
        lp["p_bh"] = multipletests(lp["p"].fillna(1), method="fdr_bh")[1]
        lp["sig_bh_q10"] = lp["p_bh"] < 0.10
    lp.to_csv(out / "lp_panel.csv", index=False)

    # ------------------------------------------------------------ 4. Comunitat Valenciana: provincias y Valencia ciudad
    q = pd.read_csv(D / "cv_prov_q_v8.csv", dtype={"cod_prov": str})
    nac = pd.read_csv(D / "nacional_q_v8.csv").set_index("trimestre")
    ipcq = nac["ipc_general"]
    fcomp = Fm["compra"]
    desc, cadena = [], []
    series_prov = {}
    for cp in ("03", "12", "46"):
        s = q[q.cod_prov == cp].set_index("trimestre")
        v_ts = 100 * (np.log(s["valor_tasado"] / s["ipc_general"]))
        series_prov[cp] = {"tasado_real": v_ts, "reg_real": 100 * np.log(s["registr_pm2_4tm"] / s["ipc_general"]),
                           "alq_real": 100 * (np.log(s["ipc_alquiler_indice"]) - np.log(s["ipc_general"]))}
    # CV como CCAA (codigo 10) y Espana
    yc_cv = Y["compra"][10] if 10 in Y["compra"].columns else None
    nac_real = 100 * np.log(nac["p_tasado"] / ipcq)
    ccaa_cv_level = 100 * (np.log(p[p.codigo_ine_ccaa == 10].set_index("trimestre")["valor_tasado_ccaa"]) - np.log(ipcq))

    def d4s(s):
        return s - s.shift(4)

    def cob(ix, ms=None):
        return None
    cv_unidades = {f"cv_prov:{cp}": (series_prov[cp]["tasado_real"], series_prov[cp]["reg_real"]) for cp in series_prov}
    # Valencia ciudad
    v = pd.read_csv(D / "valencia_ciudad_v8.csv", dtype={"codigo_ine": str})
    vc = v[v.codigo_ine == "46250"]
    pv_ = vc[vc.variable == "p_tasado"].set_index("periodo")["valor"].astype(float)
    vc_real = 100 * (np.log(pv_) - np.log(ipcq.reindex(pv_.index)))
    ipva_vc = vc[vc.variable == "ipva"].set_index("periodo")["valor"].astype(float)
    ipva_vc.index = ipva_vc.index.astype(str)
    cv_unidades["valencia_ciudad"] = (vc_real, None)
    pvl = {"valencia_ciudad": ipva_vc}
    for cp in series_prov:
        a = pd.read_csv(D / "cv_prov_a_v8.csv", dtype={"cod_prov": str})
        a = a[a.cod_prov == cp].set_index("anio")
        pvl[f"cv_prov:{cp}"] = a["ipva_indice"].dropna()
        pvl[f"cv_prov:{cp}_ann"] = a
    PER_ANIO = {"P1": (1996, 2007), "P2": (2008, 2013), "P3": (2014, 2019), "P4": (2020, 2022), "P5": (2023, 2025)}
    for amb, (s1, s2) in cv_unidades.items():
        yy = d4s(s1).dropna()
        for pe in PERS:
            ix = [t for t in yy.index if per.get(t) == pe and t in fcomp.index]
            n = len(ix)
            fila = dict(ambito=amb, periodo=pe, n_trim=n)
            if n < 6:
                continue
            ysub = yy.loc[ix].values
            f = fcomp.loc[ix].values
            fcv = (Y["compra"][10].loc[ix].values if yc_cv is not None else None)
            if n < 8:
                fila["aviso"] = "muestra < 8 trimestres: C4 con aviso"
            L = max(1, min(4, n // 4))
            X = np.column_stack([np.ones(n), f])
            be, ee, r2, r2a, _ = ols_hac(ysub, X, L)
            X2 = np.column_stack([np.ones(n), f, fcv])
            be2, r2b = (None, np.nan) if fcv is None else ols_hac(ysub, X2, L)[0::2][:2]
            t, pv = tidy_p(be[1], ee[1], n - 2)
            tc = stats.t.ppf(0.975, n - 2)
            tot = float(ysub.mean() * n / 4)
            cf = float(be[1] * f.mean() * n / 4)
            bs = np.empty(B)
            for b in range(B):
                j = idx_bloques(n, max(2, min(4, n // 3)), rng)
                bb, *_ = np.linalg.lstsq(X[j], ysub[j], rcond=None)
                bs[b] = bb[1] * f[j].mean() * n / 4
            bt = bandas(bs)
            mid = f"M8_{amb.replace(':', '')}_compra_{pe}"
            coefs.append(fila_coef(modelo_id=mid, familia_modelo="ols_cv_factor", mercado="compra", ambito=amb, periodo=pe, dependiente="d4 ln valor tasado real x100",
                                   transformacion="interanual", medida_precio="valor tasado real (MIVAU / IPC general)", variable="factor_comun",
                                   beta=be[1], ee=ee[1], tipo_ee=f"Newey-West L={L}", t=t, p=pv, ic95_lo=be[1] - tc * ee[1], ic95_hi=be[1] + tc * ee[1],
                                   n=n, r2=r2, r2_adj=r2a, capa="C4"))
            reg.log("M8_cv", mid, "d4 p_real ~ 1 + F_nacional", ix[0], ix[-1], n, r2a, np.nan, np.nan, coef_interes=be[1], p_interes=pv,
                    notas="C4 con aviso" if n < 8 else "C4")
            aviso_n = " Muestra corta (<12 trimestres): bandas aproximadas." if n < 12 else ""
            atr_all.append(dict(metodo="contabilidad", mercado="compra", ambito=amb, periodo=pe, factor="factor_comun", contribucion_pp=cf,
                                pct_total=cf / tot if abs(tot) > 1e-9 else np.nan, b68_lo=bt["b68_lo"], b68_hi=bt["b68_hi"], b90_lo=bt["b90_lo"],
                                b90_hi=bt["b90_hi"], capa="C4", notas=f"parte asociada al factor comun nacional (regresion, n={n}); total = media interanual x T/4.{aviso_n}"))
            atr_all.append(dict(metodo="contabilidad", mercado="compra", ambito=amb, periodo=pe, factor="residuo", contribucion_pp=tot - cf,
                                pct_total=(tot - cf) / tot if abs(tot) > 1e-9 else np.nan, b68_lo=np.nan, b68_hi=np.nan, b90_lo=np.nan, b90_hi=np.nan,
                                capa="C4", notas=f"idiosincratico respecto al factor nacional; total {tot:.1f} pp; banda no calculada (resto)"))
            fila.update(total_pp=tot, cuota_factor_nacional=r2, cuota_adicional_ccaa_cv=(r2b - r2) if be2 is not None else np.nan,
                        nota_ccaa="la serie de la CCAA incluye a la propia provincia/ciudad: cota superior del aporte autonomico")
            desc.append(fila)
    cuota_cv = pd.DataFrame(desc)
    cuota_cv.to_csv(out / "cuota_cv.csv", index=False)

    # cadena territorial contable (identidad aritmetica sobre series publicadas, sin estimacion): Espana -> CV -> provincia -> ciudad
    for pe in PERS:
        ixq = [t for t in nac_real.index if per.get(t) == pe]
        if len(ixq) < 6:
            continue
        a0, a1 = qi(ixq[0]), qi(ixq[-1])
        inicio = ixq[0]
        prev = f"{(a0 - 1) // 4}Q{(a0 - 1) % 4 + 1}"

        def delta(s):
            if inicio not in s.index or ixq[-1] not in s.index or prev not in s.index:
                return np.nan
            return float(s.loc[ixq[-1]] - s.loc[prev])
        dn, dcv = delta(nac_real), delta(ccaa_cv_level)
        row = dict(periodo=pe, nacional=dn, cv_menos_nacional=dcv - dn if np.isfinite(dcv) else np.nan)
        prev_lvl = dcv
        for cp in ("46",):
            dp_ = delta(series_prov[cp]["tasado_real"])
            row["prov46_menos_cv"] = dp_ - dcv
            prev_lvl = dp_
        dv = delta(vc_real)
        row["valencia_menos_prov46"] = dv - prev_lvl if np.isfinite(dv) else np.nan
        row["valencia_ciudad_total"] = dv
        for cp in ("03", "12"):
            dp_ = delta(series_prov[cp]["tasado_real"])
            row[f"prov{cp}_total"] = dp_
        cadena.append(row)
    pd.DataFrame(cadena).to_csv(out / "cadena_territorial.csv", index=False)

    # descriptivo (cambio acumulado por periodo, fuentes y concordancia -> C1 si >= 2 fuentes concordantes)
    dd_rows = []

    def cambio(s, pe):
        ixq = [t for t in s.index if per.get(t) == pe]
        if len(ixq) < 6:
            return np.nan
        a0 = qi(ixq[0])
        prev = f"{(a0 - 1) // 4}Q{(a0 - 1) % 4 + 1}"
        if prev not in s.index or ixq[-1] not in s.index or np.isnan(s.loc[prev]) or np.isnan(s.loc[ixq[-1]]):
            return np.nan
        return float(s.loc[ixq[-1]] - s.loc[prev])
    for amb in [f"cv_prov:{c}" for c in ("03", "12", "46")] + ["valencia_ciudad"]:
        s1, s2 = cv_unidades[amb]
        for pe in PERS:
            c1 = cambio(s1, pe)
            if amb == "valencia_ciudad":
                c2 = np.nan
                # segunda fuente: IPVA (anual): variacion entre el ultimo ano del periodo y el anterior al primero
                y0, y1 = PER_ANIO[pe]
                ip = pvl[amb]
                if (y0 - 1) in ip.index.astype(int) if len(ip) else False:
                    pass
                ipi = ip.copy()
                ipi.index = ipi.index.astype(int)
                if (y0 - 1) in ipi.index and y1 in ipi.index:
                    c2 = 100 * np.log(ipi.loc[y1] / ipi.loc[y0 - 1])
                    c2 -= 100 * (np.log(ipcq.reindex([f"{y1}Q4"]).values[0]) - np.log(ipcq.reindex([f"{y0 - 1}Q4"]).values[0]))
                f2 = "IPVA (anual, deflactado por IPC)"
            else:
                c2 = cambio(s2, pe) if s2 is not None else np.nan
                f2 = "Registradores precio/m2 (4 trimestres, deflactado)"
            conc = bool(np.isfinite(c1) and np.isfinite(c2) and np.sign(c1) == np.sign(c2) and abs(c1 - c2) <= 10)
            dd_rows.append(dict(ambito=amb, periodo=pe, variable="precio real de compra (cambio acumulado, pp log)", fuente1="valor tasado MIVAU (p_tasado) real",
                                valor1=c1, fuente2=f2, valor2=c2, concordantes=conc, capa="C1" if conc else "C4",
                                nota="C1 si 2 fuentes con mismo signo y diferencia <= 10 pp; si no, fuente unica o discrepantes: C4"))
    pd.DataFrame(dd_rows).to_csv(out / "descriptivo_cv.csv", index=False)

    # ------------------------------------------------------------ ajuste BH y salidas
    cf = pd.DataFrame(coefs, columns=COLS_COEF)
    mask = cf["variable"].ne("const") & cf["p"].notna()
    cf["p_ajustado"] = np.nan
    cf["metodo_ajuste"] = ""
    cf.loc[mask, "p_ajustado"] = multipletests(cf.loc[mask, "p"], method="fdr_bh")[1]
    cf.loc[mask, "metodo_ajuste"] = "BH"
    cf.to_csv(out / "coeficientes.csv", index=False)
    atribucion = pd.DataFrame(atr_all, columns=COLS_ATR)
    atribucion.to_csv(out / "atribucion.csv", index=False)
    pd.DataFrame(resumen_paneles).assign(covs=lambda d: d["covs"].astype(str)).to_csv(out / "paneles_resumen.csv", index=False)

    # resumen cuantitativo
    sig = int((cf.loc[mask & cf["modelo_id"].str.startswith("M8_ccaa"), "p_ajustado"] < 0.10).sum())
    ntest = int((mask & cf["modelo_id"].str.startswith("M8_ccaa")).sum())
    cq = cuota.groupby(["mercado", "periodo"])["cuota_comun"].median().round(3).unstack()
    pan = cf[(cf.familia_modelo == "panel_fe_dk") & (cf.variable == "factor_comun") & cf.modelo_id.str.contains("_cov_")]
    est = {"cuota_comun_mediana_ccaa": {m: cq.loc[m].to_dict() for m in cq.index},
           "n_coef_ccaa_sig_bh10": f"{sig} de {ntest}",
           "beta_factor_panel": {f"{r.mercado}_{r.periodo}": round(float(r.beta), 3) for r in pan.itertuples()}}
    res = dict(
        rama="M8", pregunta="Cuanto del crecimiento del precio real por CCAA, y en la Comunitat Valenciana por provincia y ciudad, es comun frente a idiosincratico, y que variables regionales se asocian?",
        capa="C4", datos="panel_ccaa_q_v8.csv, cv_prov_q_v8.csv, cv_prov_a_v8.csv, valencia_ciudad_v8.csv, nacional_q_v8.csv (cruces por codigo INE)",
        N={"ccaa": 17, "trimestres_compra": int(len(Y['compra'])), "trimestres_alquiler": int(len(Y['alquiler'])), "paneles": len(resumen_paneles)},
        metodo="ecuacion por CCAA y periodo sobre el factor comun (PCA, NW), panel FE con covariables regionales (Driscoll-Kraay), LP panel (DK), contabilidad CV con bandas bootstrap por bloques; BH q=0,10",
        estimacion=est, ic95="ver coeficientes.csv (ic95_lo, ic95_hi)", p_ajustado="BH q=0,10 sobre todos los coeficientes (excluida la constante) y sobre lp_panel.csv",
        nivel_evidencia="EXPLORATORIO (C4); C1 solo en descriptivo_cv.csv donde 2 fuentes concuerdan",
        diagnosticos={"B": B, "rapido": rapido, "avisos": avisos[:30], "vif_max_paneles": float(np.nanmax(cf["vif_max"].astype(float))) if cf["vif_max"].notna().any() else None,
                      "heterogeneidad_por_periodo": "ajustes separados por periodo (no se contrasta igualdad de coeficientes)"},
        fuera_muestra={"modelo": "no aplica", "rmse": None, "dm_vs_ar4": None},
        notas=AVISO + " Fuera de muestra: M8 es descriptivo/asociativo, sin comparacion con AR(4)/ECM v1. Alquiler por CCAA solo desde 2008 (sin P1). Turismo solo en 6 CCAA (sensibilidad).",
    )
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    reg.flush()
    lpt = ""
    if len(lp):
        lpt = f" LP panel: {int(lp['sig_bh_q10'].sum())} de {len(lp)} coeficientes (impulso x periodo x h) con p BH < 0,10."
    md = ["# M8: descomposicion regional (C4, exploratorio)", "",
          f"**17 CCAA, cuota comun** (R2 de y sobre el factor comun; mediana entre CCAA): {json.dumps(est['cuota_comun_mediana_ccaa'], ensure_ascii=False)}. "
          f"Coeficientes del factor por CCAA con p BH<0,10: {est['n_coef_ccaa_sig_bh10']}. Detalle por CCAA/periodo en `cuota_ccaa.csv` (con bandas).", "",
          f"**Panel FE (Driscoll-Kraay)** por periodo con covariables regionales disponibles (`paneles_resumen.csv`, `coeficientes.csv`); beta del factor comun: {est['beta_factor_panel']}. "
          "Contribuciones por CCAA con bandas bootstrap en `atribucion.csv` (metodo regional_panel; factores demografia, empleo_renta, oferta, demanda_externa, factor_comun, residuo)." + lpt, "",
          "**Comunitat Valenciana** (03, 12, 46) y **Valencia ciudad**: `cuota_cv.csv` (parte asociada al factor nacional y aporte adicional de la serie CV, cota superior porque incluye a la propia provincia), "
          "`cadena_territorial.csv` (identidad aritmetica Espana -> CV -> provincia -> ciudad), `descriptivo_cv.csv` (C1 solo con 2 fuentes concordantes). Muestras cortas (P4, P1 de Valencia ciudad desde 2006): C4 con aviso.", "",
          "**Limites.** " + AVISO, "Turismo: 6 CCAA desde 2015T4 (sensibilidad). Alquiler por CCAA desde 2008 (sin P1)."]
    (out / "resumen.md").write_text("\n".join(md) + "\n")
    json.dump({"segundos": round(time.time() - t0, 1)}, open(out / "tiempos.json", "w"))
    print(f"M8 ok en {time.time() - t0:.0f} s; filas atribucion {len(atribucion)}; coef {len(cf)}; lp {len(lp)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    main(a.rapido, a.salida)
