#!/usr/bin/env python3
"""V8-F4 M1: factor comun de las 17 CCAA (H8-8, H8-9; familia Holm) y parte europea del crecimiento nacional.

H8-8: cuota de varianza del 1.er componente (PCA, 1 factor fijo; sensibilidad con 2; DFM-ML al lado) del crecimiento
interanual del precio real de compra (valor tasado real por CCAA) en cada periodo P1-P5; bootstrap por bloques; p unilateral.
H8-9: correlacion del factor comun espanol con el crecimiento del HPI de la zona euro; bootstrap por bloques; p unilateral.
Todo C4 (asociacion): los factores son resumenes estadisticos, sin lectura causal ni estructural.
Uso: python3 src/v8/m1_factor_comun.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from statsmodels.stats.multitest import multipletests  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry  # noqa: E402
from herramientas import dfm  # noqa: E402

SEED = 20261010
PANEL = RAIZ / "data" / "processed" / "v8" / "panel_ccaa_q_v8.csv"
NACIONAL = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
EURO = RAIZ / "data" / "raw" / "v8" / "eurostat_prc_hpi_q_multi.csv"
PERS = ["P1", "P2", "P3", "P4", "P5"]
SCRIPT = "src/v8/m1_factor_comun.py"
COLS_COEF = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio",
             "variable", "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad",
             "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable",
             "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0",
             "cumple_multiverso", "destacado", "motivo_destacado", "script"]
COLS_ATR = ["metodo", "mercado", "ambito", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi",
            "capa", "notas"]
AVISO = ("C4: asociacion estadistica; el factor es un resumen de comovimiento, sin interpretacion causal ni estructural. Muestras por "
         "periodo cortas (P4 = 9 trimestres): con N = 17 y T pequeno la cuota del 1.er componente esta sesgada al alza incluso sin factor comun real.")


# ------------------------------------------------------------------ datos
def matriz(p, var, deflactar=True):
    """Crecimiento interanual (log x100) por CCAA (columnas = codigo INE), indice trimestre; real = deflactado por IPC general."""
    w = p.pivot(index="trimestre", columns="codigo_ine_ccaa", values=var)
    if deflactar:
        ipc = p.groupby("trimestre")["ipc_general"].first()
        w = w.div(ipc, axis=0)
    lw = np.log(w)
    return 100.0 * (lw - lw.shift(4))


def periodo_de(p):
    per = p.groupby("trimestre")["periodo_h8"].first()
    return per


def cargar():
    p = pd.read_csv(PANEL)
    p["codigo_ine_ccaa"] = p["codigo_ine_ccaa"].astype(int)
    return p


def cargar_euro():
    e = pd.read_csv(EURO)
    w = e.pivot(index="periodo", columns="territorio", values="valor")
    w.index = [s.replace("-", "") for s in w.index]
    return w


def crec4(s):
    return 100.0 * (np.log(s) - np.log(s.shift(4)))


# ------------------------------------------------------------------ estadisticos
def idx_bloques(T, L, rng):
    n = int(np.ceil(T / L))
    st = rng.integers(0, T, n)
    return ((st[:, None] + np.arange(L)[None, :]) % T).ravel()[:T]


def cuota_pca(X, k=1):
    return float(dfm.pca_factores(X, k)["var_explicada_total"])


def pc1(X):
    """Primer componente (serie T) con signo tal que la carga media sea positiva."""
    r = dfm.pca_factores(X, 1)
    f = r["factores"][:, 0]
    if r["cargas"][:, 0].mean() < 0:
        f = -f
    return f


def azar_cuota(X, rng, B):
    """Cuota del 1.er componente cuando cada serie se desplaza circularmente de forma independiente (sin comovimiento)."""
    T, N = X.shape
    out = np.empty(B)
    for b in range(B):
        Y = np.column_stack([np.roll(X[:, j], int(rng.integers(0, T))) for j in range(N)])
        out[b] = cuota_pca(Y, 1)
    return out


def corr_boot(X, g, L, B, rng, d_obs=None):
    """Correlacion entre PC1(X) y g con bootstrap por bloques circulares (se re-estima el factor en cada replica)."""
    T = len(g)
    r0 = float(np.corrcoef(pc1(X), g)[0, 1])
    bs = np.empty(B)
    for b in range(B):
        ix = idx_bloques(T, L, rng)
        gb = g[ix]
        if gb.std() < 1e-12:
            bs[b] = np.nan
            continue
        bs[b] = np.corrcoef(pc1(X[ix]), gb)[0, 1]
    bs = bs[np.isfinite(bs)]
    return r0, bs


def corr_boot_serie(f, g, L, B, rng):
    T = len(g)
    r0 = float(np.corrcoef(f, g)[0, 1])
    bs = np.empty(B)
    for b in range(B):
        ix = idx_bloques(T, L, rng)
        bs[b] = np.corrcoef(f[ix], g[ix])[0, 1] if g[ix].std() > 1e-12 and f[ix].std() > 1e-12 else np.nan
    return r0, bs[np.isfinite(bs)]


def p_unilat_mayor(bs, h0):
    """p de H1: parametro > h0, percentil: P(boot <= h0)."""
    return float((1 + np.sum(bs <= h0)) / (len(bs) + 1))


def bandas(x):
    q = np.percentile(x, [5, 16, 84, 95, 2.5, 97.5])
    return dict(b90_lo=q[0], b68_lo=q[1], b68_hi=q[2], b90_hi=q[3], lo95=q[4], hi95=q[5])


def fila_coef(**kw):
    d = {c: np.nan for c in COLS_COEF}
    d.update(modulo="M1", script=SCRIPT, **kw)
    return d


# ------------------------------------------------------------------ main
def main(rapido=False, salida=None):
    t0 = time.time()
    out = Path(salida) if salida else RAIZ / "output" / "v8" / "M1"
    out.mkdir(parents=True, exist_ok=True)
    B = 199 if rapido else 999
    B_att = 99 if rapido else 499
    reg = Registry(out / "registro.csv")
    p = cargar()
    per = periodo_de(p)
    aviso_datos = []

    # --- matrices de crecimiento interanual real
    Xc = matriz(p, "valor_tasado_ccaa").dropna()          # compra: valor tasado real, 1996T1+
    Xi = matriz(p, "ipv").dropna()                        # compra, IPV real (sensibilidad, 2008T1+)
    Xa = matriz(p, "ipc_alquiler").dropna()               # alquiler: IPC alquiler real por CCAA (2008T1+)
    series = {"compra_tasado": ("compra", Xc, "valor tasado real por CCAA (valor_tasado_ccaa / IPC general), interanual"),
              "compra_ipv": ("compra", Xi, "IPV real por CCAA (ipv / IPC general), interanual; sensibilidad (desde 2008T1)"),
              "alquiler_ipc": ("alquiler", Xa, "IPC alquiler real por CCAA (ipc_alquiler / IPC general), interanual (desde 2008T1)")}
    aviso_datos.append("Alquiler por CCAA: IPC alquiler (2007T1+); P1 sin datos de alquiler. Un solo indicador de alquiler por CCAA (C4).")

    # --- 1. cuota de varianza por periodo
    filas_cuota, hip_p = [], {}
    rng = np.random.default_rng(SEED + 1)
    dfm_cache = {}
    for sid, (mercado, X, medida) in series.items():
        # DFM-ML sobre la muestra completa de la serie (k = 1, 2)
        for k in (1, 2):
            try:
                idx = pd.PeriodIndex([pd.Period(t, freq="Q") for t in X.index], freq="Q")
                r = dfm.dfm_ml(pd.DataFrame(X.values, index=idx, columns=[f"c{c}" for c in X.columns]), k=k, maxiter=100 if rapido else 200)
                dfm_cache[(sid, k)] = r
            except Exception as ex:  # noqa: BLE001
                dfm_cache[(sid, k)] = None
                aviso_datos.append(f"DFM-ML {sid} k={k} fallo: {type(ex).__name__}: {str(ex)[:80]}")
        for pe in PERS + ["completo"]:
            ix = X.index[per.reindex(X.index).values == pe] if pe != "completo" else X.index
            if len(ix) < 8:
                continue
            Z = X.loc[ix].values
            T = len(ix)
            L = max(2, min(4, T // 3))
            for k in (1, 2):
                s0 = cuota_pca(Z, k)
                row = dict(serie=sid, mercado=mercado, periodo=pe, k=k, T=T, N=Z.shape[1], metodo="pca", cuota=s0)
                if k == 1:
                    bs = np.empty(B)
                    for b in range(B):
                        bs[b] = cuota_pca(Z[idx_bloques(T, L, rng)], 1)
                    bd = bandas(bs)
                    row.update(ic95_lo=bd["lo95"], ic95_hi=bd["hi95"], b68_lo=bd["b68_lo"], b68_hi=bd["b68_hi"], b90_lo=bd["b90_lo"],
                               b90_hi=bd["b90_hi"], p_unilateral_gt50=p_unilat_mayor(bs, 0.5), bloque=L, B=B)
                    az = azar_cuota(Z, rng, max(99, B // 2))
                    row.update(cuota_azar_media=float(az.mean()), cuota_azar_p95=float(np.percentile(az, 95)),
                               p_vs_azar=float((1 + np.sum(az >= s0)) / (len(az) + 1)))
                    reg.log("M1_cuota", f"M1_pca_{sid}_{pe}_k{k}", f"PC{k} cuota varianza d4 {sid}", ix[0], ix[-1], T, np.nan, np.nan, np.nan,
                            coef_interes=s0, p_interes=row["p_unilateral_gt50"], notas=f"H0 cuota<=0,5; bloque {L}; B={B}")
                else:
                    reg.log("M1_cuota", f"M1_pca_{sid}_{pe}_k{k}", f"PC1-2 cuota varianza d4 {sid}", ix[0], ix[-1], T, np.nan, np.nan, np.nan,
                            coef_interes=s0, notas="sensibilidad 2 factores, sin bootstrap")
                filas_cuota.append(row)
            # DFM: cuota = R2 medio de las series sobre el factor dentro del periodo
            for k in (1, 2):
                r = dfm_cache.get((sid, k))
                if r is None:
                    continue
                F = pd.DataFrame(r["factores"][:, :k], index=X.index)
                Fp = F.loc[ix].values
                Zs = (Z - Z.mean(0)) / Z.std(0)
                A = np.column_stack([np.ones(T), Fp])
                coef, *_ = np.linalg.lstsq(A, Zs, rcond=None)
                res = Zs - A @ coef
                cu = float(1 - (res ** 2).sum() / (Zs ** 2).sum())
                filas_cuota.append(dict(serie=sid, mercado=mercado, periodo=pe, k=k, T=T, N=Z.shape[1], metodo="dfm_ml", cuota=cu,
                                        converge=r["converge"]))
                reg.log("M1_cuota", f"M1_dfm_{sid}_{pe}_k{k}", f"DFM-ML k={k} cuota {sid}", ix[0], ix[-1], T, np.nan, np.nan, np.nan,
                        coef_interes=cu, notas="punto, sin bootstrap; factor ajustado a la muestra completa")
    cuota = pd.DataFrame(filas_cuota)
    cuota.to_csv(out / "cuota_varianza.csv", index=False)

    # H8-8: IUT sobre P1-P5, compra_tasado, PCA k=1
    c88 = cuota[(cuota.serie == "compra_tasado") & (cuota.metodo == "pca") & (cuota.k == 1) & (cuota.periodo.isin(PERS))].set_index("periodo")
    faltan = [x for x in PERS if x not in c88.index]
    p88 = float(c88["p_unilateral_gt50"].max()) if not faltan else np.nan
    est88 = {x: round(float(c88.loc[x, "cuota"]), 4) for x in c88.index}

    # --- 2. H8-9: correlacion factor comun - HPI zona euro
    eu = cargar_euro()
    ipc = p.groupby("trimestre")["ipc_general"].first()
    g_ea = crec4(eu["EA19"])
    g_ea_real = crec4(eu["EA19"] / ipc)
    g_exes = pd.concat([crec4(eu[c]) for c in ["DE", "FR", "IT", "NL", "PT"]], axis=1).mean(axis=1)
    g_es = crec4(eu["ES"])
    comun = Xc.index.intersection(g_ea.dropna().index)
    Z = Xc.loc[comun].values
    L8 = 8
    rng = np.random.default_rng(SEED + 2)
    f_pca = pd.Series(pc1(Xc.values), index=Xc.index)            # factor sobre la muestra completa de la serie
    f_pca_c = f_pca.loc[comun]
    variantes = {}
    r0, bs = corr_boot(Z, g_ea.loc[comun].values, L8, B, rng)
    variantes["principal_ea19_nominal"] = (r0, bs, len(comun), "HPI EA19 nominal interanual (Eurostat), incluye ES")
    for nom, gg, desc in [("ea19_real", g_ea_real, "HPI EA19 deflactado por IPC espanol (aprox.)"),
                          ("ex_es_proxy", g_exes, "media simple DE, FR, IT, NL, PT (aprox. EA sin ES; NO es el agregado oficial)")]:
        ok = comun.intersection(gg.dropna().index)
        r1, b1 = corr_boot(Xc.loc[ok].values, gg.loc[ok].values, L8, B, rng)
        variantes[nom] = (r1, b1, len(ok), desc)
    # factor DFM
    rd = dfm_cache.get(("compra_tasado", 1))
    if rd is not None:
        fd = pd.Series(rd["factores"][:, 0], index=Xc.index).loc[comun]
        if np.corrcoef(fd, f_pca_c)[0, 1] < 0:
            fd = -fd
        r2_, b2 = corr_boot_serie(fd.values, g_ea.loc[comun].values, L8, B, rng)
        variantes["factor_dfm_ea19"] = (r2_, b2, len(comun), "factor DFM-ML (no re-estimado en bootstrap) con EA19 nominal")
    # IPV (2008T1+)
    ok = Xi.index.intersection(g_ea.dropna().index)
    r3, b3 = corr_boot(Xi.loc[ok].values, g_ea.loc[ok].values, L8, B, rng)
    variantes["ipv_ea19"] = (r3, b3, len(ok), "factor del IPV real (2008T1+) con EA19 nominal")
    # alquiler
    ok = Xa.index.intersection(g_ea.dropna().index)
    r4, b4 = corr_boot(Xa.loc[ok].values, g_ea.loc[ok].values, L8, B, rng)
    variantes["alquiler_ea19"] = (r4, b4, len(ok), "factor del alquiler real (2008T1+) con HPI EA19 (exploratorio: otro mercado)")
    filas_h9 = []
    for nm, (r_, b_, n_, desc) in variantes.items():
        bd = bandas(b_)
        pv = p_unilat_mayor(b_, 0.0)
        filas_h9.append(dict(variante=nm, correlacion=r_, ic95_lo=bd["lo95"], ic95_hi=bd["hi95"], b68_lo=bd["b68_lo"], b68_hi=bd["b68_hi"],
                             p_unilateral=pv, n=n_, bloque=L8, B=len(b_), descripcion=desc))
        reg.log("M1_corr", f"M1_h89_{nm}", f"corr(PC1, g_EA) {nm}", comun[0], comun[-1], n_, np.nan, np.nan, np.nan, coef_interes=r_,
                p_interes=pv, notas=desc)
    h9 = pd.DataFrame(filas_h9)
    p89 = float(h9.loc[h9.variante == "principal_ea19_nominal", "p_unilateral"].iloc[0])
    r89 = float(h9.loc[h9.variante == "principal_ea19_nominal", "correlacion"].iloc[0])

    # Holm {H8-8, H8-9}
    ph = [p88 if np.isfinite(p88) else 1.0, p89]
    holm = multipletests(ph, method="holm")[1]

    # correlaciones por periodo (exploratorio, BH)
    rng = np.random.default_rng(SEED + 3)
    filas_pp = []
    for nm, gg in [("ea19_nominal", g_ea), ("ex_es_proxy", g_exes)]:
        for pe in PERS:
            ix = comun[per.reindex(comun).values == pe]
            if len(ix) < 8:
                continue
            f = f_pca.loc[ix].values
            g = gg.loc[ix].values
            T = len(ix)
            r_, b_ = corr_boot_serie(f, g, max(2, min(4, T // 3)), B, rng)
            bd = bandas(b_)
            pv = p_unilat_mayor(b_, 0.0)
            filas_pp.append(dict(variante=nm, periodo=pe, correlacion=r_, ic95_lo=bd["lo95"], ic95_hi=bd["hi95"], p_unilateral=pv, n=T))
            reg.log("M1_corr_periodo", f"M1_corrper_{nm}_{pe}", f"corr(PC1 completo, g_EA) {pe}", ix[0], ix[-1], T, np.nan, np.nan, np.nan,
                    coef_interes=r_, p_interes=pv, notas="exploratorio, BH; factor estimado en muestra completa")
    pp = pd.DataFrame(filas_pp)
    if len(pp):
        pp["p_bh"] = multipletests(pp["p_unilateral"], method="fdr_bh")[1]
        pp["sig_bh_q10"] = pp["p_bh"] < 0.10
    pp.to_csv(out / "correlaciones_periodo.csv", index=False)
    h9.to_csv(out / "correlaciones_h89.csv", index=False)

    # evolucion en ventanas (cuota PCA y correlacion)
    ev = dfm.evolucion_ventanas(Xc, k=1, ventana=40, paso=4, metodo="pca")
    ev["trim_ini"] = [Xc.index[i] for i in ev["inicio"]]
    ev["trim_fin"] = [Xc.index[i] for i in ev["fin"]]
    rows = []
    fz = f_pca.loc[comun].values
    gz = g_ea.loc[comun].values
    for a in range(0, len(comun) - 40 + 1, 4):
        rows.append(dict(trim_ini=comun[a], trim_fin=comun[a + 39], correlacion=float(np.corrcoef(fz[a:a + 40], gz[a:a + 40])[0, 1])))
    ev2 = pd.DataFrame(rows)
    ev.to_csv(out / "evolucion_ventanas.csv", index=False)
    ev2.to_csv(out / "evolucion_correlacion.csv", index=False)
    f_out = pd.DataFrame({"trimestre": Xc.index, "factor_pca": f_pca.values})
    f_out["g_ea19"] = g_ea.reindex(Xc.index).values
    f_out.to_csv(out / "factor_comun.csv", index=False)
    cargas = dfm.pca_factores(Xc.values, 1)["cargas"][:, 0]
    if cargas.mean() < 0:
        cargas = -cargas
    pd.DataFrame({"codigo_ine_ccaa": Xc.columns, "carga_pca": cargas}).to_csv(out / "cargas_pca.csv", index=False)

    # --- 3. atribucion: parte del crecimiento nacional asociada al crecimiento del HPI EA19 (regresion con retardos, C4)
    nac = pd.read_csv(NACIONAL).set_index("trimestre")
    dp = 100.0 * (np.log(nac["p_tasado"] / nac["ipc_general"])).diff()
    dea = 100.0 * (np.log(eu["EA19"] / ipc)).diff()
    rng = np.random.default_rng(SEED + 4)
    atr, coefs = [], []
    NLAG = 1
    for pe in PERS:
        ix = [t for t in dp.index if per.get(t) == pe]
        D = pd.DataFrame({"y": dp.loc[ix]})
        for k in range(NLAG + 1):
            D[f"e{k}"] = dea.shift(k).reindex(ix).values
        D = D.dropna()
        n = len(D)
        if n < 8:
            continue
        y = D["y"].values
        Xr = np.column_stack([np.ones(n)] + [D[f"e{k}"].values for k in range(NLAG + 1)])

        def contrib(yy, XX):
            be, *_ = np.linalg.lstsq(XX, yy, rcond=None)
            return float((XX[:, 1:] @ be[1:]).sum()), float(yy.sum()), be

        c0, tot, be = contrib(y, Xr)
        res = y - Xr @ be
        s2 = res @ res / max(1, n - Xr.shape[1])
        cov = s2 * np.linalg.inv(Xr.T @ Xr)
        ee = np.sqrt(np.diag(cov))
        r2 = 1 - (res @ res) / ((y - y.mean()) @ (y - y.mean()))
        r2a = 1 - (1 - r2) * (n - 1) / max(1, n - Xr.shape[1])
        bc = np.empty(B_att)
        bp = np.empty(B_att)
        bres = np.empty(B_att)
        for b in range(B_att):
            ix_b = idx_bloques(n, max(2, min(4, n // 3)), rng)
            cb, tb, _ = contrib(y[ix_b], Xr[ix_b])
            bc[b], bres[b] = cb, tb - cb
            bp[b] = cb / tb if abs(tb) > 1e-9 else np.nan
        pct = c0 / tot if abs(tot) > 1e-9 else np.nan
        bd, bdr = bandas(bc), bandas(bres)
        atr.append(dict(metodo="factor_comun", mercado="compra", ambito="nacional", periodo=pe, factor="factor_europeo", contribucion_pp=c0,
                        pct_total=pct, b68_lo=bd["b68_lo"], b68_hi=bd["b68_hi"], b90_lo=bd["b90_lo"], b90_hi=bd["b90_hi"], capa="C4",
                        notas=f"regresion crec. trimestral del valor tasado real nacional sobre crec. HPI EA19 real (retardos 0-{NLAG}); "
                              f"n={n}; bootstrap por bloques B={B_att}; suma de variaciones trimestrales del periodo; asociacion, no causal; "
                              "EA19 incluye ES; pct_total inestable si la variacion total es ~0"))
        atr.append(dict(metodo="factor_comun", mercado="compra", ambito="nacional", periodo=pe, factor="residuo", contribucion_pp=tot - c0,
                        pct_total=(tot - c0) / tot if abs(tot) > 1e-9 else np.nan, b68_lo=bdr["b68_lo"], b68_hi=bdr["b68_hi"],
                        b90_lo=bdr["b90_lo"], b90_hi=bdr["b90_hi"], capa="C4", notas=f"resto (constante + residuos); total periodo {tot:.2f} pp"))
        for j, nm in enumerate(["const"] + [f"dEA_l{k}" for k in range(NLAG + 1)]):
            tt = be[j] / ee[j]
            from scipy import stats as st
            pv = 2 * (1 - st.t.cdf(abs(tt), n - Xr.shape[1]))
            tc = st.t.ppf(0.975, n - Xr.shape[1])
            coefs.append(fila_coef(modelo_id=f"M1_att_compra_{pe}", familia_modelo="ols_retardos_ea", mercado="compra", ambito="nacional", periodo=pe,
                                   dependiente="d ln valor tasado real nacional x100", transformacion="trimestral",
                                   medida_precio="valor tasado real (p_tasado / IPC general)", variable=nm, beta=be[j], ee=ee[j],
                                   tipo_ee="MCO homocedastico", t=tt, p=pv, ic95_lo=be[j] - tc * ee[j], ic95_hi=be[j] + tc * ee[j], n=n, r2=r2,
                                   r2_adj=r2a, capa="C4"))
        reg.log("M1_atrib", f"M1_att_compra_{pe}", f"dp ~ dEA_l0..l{NLAG}", ix[0], ix[-1], n, r2a, np.nan, np.nan, coef_interes=c0,
                notas="contribucion acumulada (pp) de EA19; C4")
    atribucion = pd.DataFrame(atr, columns=COLS_ATR)
    atribucion.to_csv(out / "atribucion.csv", index=False)
    pd.DataFrame(coefs, columns=COLS_COEF).to_csv(out / "coeficientes.csv", index=False)

    # --- hipotesis
    # robustez: sensibilidades coinciden?
    sens_ok = bool((h9[h9.variante.isin(["ea19_real", "ex_es_proxy"])]["p_unilateral"] < 0.05).all())
    cuota_sens_ok = bool(((cuota[(cuota.metodo == "dfm_ml") & (cuota.k == 1) & (cuota.serie == "compra_tasado") & cuota.periodo.isin(PERS)]["cuota"]) > 0.5).all())
    hip = pd.DataFrame([
        dict(id="H8-8", hipotesis="El componente comun de las 17 CCAA explica mas del 50 % de la varianza del crecimiento interanual del precio real de compra en cada periodo",
             estimacion=json.dumps(est88), p=p88, p_holm=holm[0], metodo_ajuste="Holm", rechaza_H0_alfa05=bool(holm[0] < 0.05), capa="C4",
             nota=f"IUT: p = max de p(P1..P5), PCA 1 factor, bootstrap bloques; DFM-ML coincide (>50 % en todos): {cuota_sens_ok}. {AVISO}"),
        dict(id="H8-9", hipotesis="El factor comun espanol covaria positivamente con el crecimiento del HPI de la zona euro",
             estimacion=round(r89, 4), p=p89, p_holm=holm[1], metodo_ajuste="Holm", rechaza_H0_alfa05=bool(holm[1] < 0.05), capa="C4",
             nota=f"principal EA19 nominal (incluye ES); sensibilidades EA19 real y proxy sin ES significativas: {sens_ok}. EA sin ES oficial no construible (sin pesos). {AVISO}"),
    ])
    hip.to_csv(out / "hipotesis_m1.csv", index=False)
    for _, r in hip.iterrows():
        reg.log("M1_hipotesis", f"M1_{r['id']}", r["hipotesis"][:60], "", "", 0, np.nan, np.nan, np.nan, p_interes=r["p"], notas=f"p_holm={r['p_holm']:.4f}")

    # --- resultado.json y resumen
    robusta = bool(holm[0] < 0.05 and holm[1] < 0.05 and sens_ok and cuota_sens_ok)
    nivel = "ASOCIACION ROBUSTA (C4)" if robusta else "EXPLORATORIO (C4)"
    res = dict(
        rama="M1",
        pregunta="Explica un componente comun de las 17 CCAA mas del 50 % de la varianza del crecimiento del precio real en cada periodo, y covaria con el HPI de la zona euro?",
        capa="C4", datos=f"{PANEL.name} (valor_tasado_ccaa real, ipv, ipc_alquiler por CCAA, cruce por codigo INE); {NACIONAL.name}; eurostat_prc_hpi_q_multi.csv",
        N={"compra_tasado": int(len(Xc)), "ipv": int(len(Xi)), "alquiler": int(len(Xa)), "h89": int(len(comun))},
        metodo="PCA 1 factor (sens. 2) y DFM-ML; bootstrap por bloques circulares; Holm {H8-8, H8-9}; BH en lo exploratorio; regresion con retardos para la parte europea",
        estimacion={"H8-8_cuota_por_periodo": est88, "H8-9_correlacion": round(r89, 4),
                    "atribucion_europea_pp": {r["periodo"]: round(r["contribucion_pp"], 2) for r in atr if r["factor"] == "factor_europeo"}},
        ic95={"H8-9": [round(float(h9.iloc[0]["ic95_lo"]), 4), round(float(h9.iloc[0]["ic95_hi"]), 4)],
              "H8-8": {x: [round(float(c88.loc[x, "ic95_lo"]), 4), round(float(c88.loc[x, "ic95_hi"]), 4)] for x in c88.index}},
        p_ajustado={"H8-8": float(holm[0]), "H8-9": float(holm[1]), "metodo": "Holm", "p_crudo": {"H8-8": p88, "H8-9": p89}},
        nivel_evidencia=nivel,
        diagnosticos={"cuota_azar": "ver cuota_varianza.csv (cuota_azar_media): con N=17 y T=9-48 la cuota sin factor real es alta", "bloque": "L=8 (H8-9), 2-4 (cuotas)",
                      "B": B, "rapido": rapido, "avisos": aviso_datos, "dfm_converge": {f"{k[0]}_k{k[1]}": (None if v is None else v["converge"]) for k, v in dfm_cache.items()}},
        fuera_muestra={"modelo": "no aplica", "rmse": None, "dm_vs_ar4": None},
        notas=AVISO + " Zona euro sin Espana oficial no construible; proxy DE/FR/IT/NL/PT. Fuera de muestra: M1 no es un modelo predictivo (sin comparacion con AR(4)/ECM v1).",
    )
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    reg.flush()
    ev_txt = f"{ev['var_explicada'].min():.2f}-{ev['var_explicada'].max():.2f}"
    md = [f"# M1: factor comun de las 17 CCAA (C4, {nivel})", "",
          f"**H8-8** (cuota del 1.er componente > 50 % en cada periodo; PCA, bootstrap por bloques; IUT): cuotas {est88}; p max = {p88:.4f}; "
          f"**p Holm = {holm[0]:.4f}**. DFM-ML coincide en >50 %: {cuota_sens_ok}. Con N=17 y T pequeno la cuota esta sesgada al alza; "
          "ver `cuota_azar_media` y `p_vs_azar` en `cuota_varianza.csv`.", "",
          f"**H8-9** (corr. factor comun - HPI EA19 interanual, 2006T1+): r = {r89:.3f} (IC95 {h9.iloc[0]['ic95_lo']:.2f} a {h9.iloc[0]['ic95_hi']:.2f}); "
          f"p = {p89:.4f}; **p Holm = {holm[1]:.4f}**. EA19 incluye Espana (sesgo al alza); proxy sin ES (DE, FR, IT, NL, PT) y EA19 real en `correlaciones_h89.csv`.", "",
          f"Cuota en ventanas de 40 trimestres: {ev_txt} (`evolucion_ventanas.csv`). Correlaciones por periodo (exploratorio, BH q=0,10): `correlaciones_periodo.csv`.", "",
          "**Parte europea del crecimiento nacional** (`atribucion.csv`, metodo factor_comun, C4, con bandas): " +
          "; ".join(f"{r['periodo']} {r['contribucion_pp']:.1f} pp [{r['b90_lo']:.1f}, {r['b90_hi']:.1f}]" for r in atr if r["factor"] == "factor_europeo") + ".", "",
          "**Limites.** " + AVISO, "Alquiler por CCAA: IPC alquiler desde 2007 (sin P1). Fuera de muestra no aplica."]
    (out / "resumen.md").write_text("\n".join(md) + "\n")
    json.dump({"segundos": round(time.time() - t0, 1)}, open(out / "tiempos.json", "w"))
    print(f"M1 ok en {time.time() - t0:.0f} s; H8-8 p_holm={holm[0]:.4f}; H8-9 r={r89:.3f} p_holm={holm[1]:.4f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    main(a.rapido, a.salida)
