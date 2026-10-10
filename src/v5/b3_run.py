"""B3 · diferencias entre provincias (pre-registro docs/v5/prereg_B3.md). Determinista, sin red, un hilo, SEED=20261010.
Salidas en output/v5/B3. SMOKE=1: 5 permutaciones y sin mapas (escribe en output/v5/B3/_smoke).
Lenguaje: asociación, nunca efecto. Capa máxima C4."""
from __future__ import annotations

import ast
import itertools
import json
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import warnings
from math import factorial
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src/v5"))
import b3_data as bd  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
SMOKE = os.environ.get("SMOKE") == "1"
NPERM = 5 if SMOKE else 5000
OUT = RAIZ / "output/v5/B3" / ("_smoke" if SMOKE else "")
(OUT / "tablas").mkdir(parents=True, exist_ok=True)
(OUT / "figuras").mkdir(parents=True, exist_ok=True)
FAMS = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]
LEAD = {"H-B3-1": ("F1", "F1_bartik", +1), "H-B3-2": ("F2", "F2_dlnpob", +1), "H-B3-6": ("F6", "F6_lnp0", -1)}


# ------------------------------------------------------------ fórmulas de r1b_sens (se extraen por AST: importarlo escribiría su registro)
def _carga_r1b():
    src = (RAIZ / "src/v5/r1b_sens.py").read_text()
    tree = ast.parse(src)
    ns = {"np": np, "stats": stats}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name in ("rv", "cr1", "oster"):
            exec(compile(ast.Module([n], []), "r1b_sens", "exec"), ns)
    return ns["oster"], ns["rv"]


OSTER, RV = _carga_r1b()


# ------------------------------------------------------------ MCO y errores
def ajusta(y, Z):
    """Z ya incluye constante. Devuelve dict con b, e, XtXi, h."""
    XtXi = np.linalg.inv(Z.T @ Z)
    b = XtXi @ Z.T @ y
    e = y - Z @ b
    h = np.einsum("ij,jk,ik->i", Z, XtXi, Z)
    return dict(b=b, e=e, XtXi=XtXi, h=h, n=len(y), k=Z.shape[1])


def cov_hc3(f, Z):
    u = f["e"] / (1 - f["h"])
    M = (Z * u[:, None]).T @ (Z * u[:, None])
    return f["XtXi"] @ M @ f["XtXi"]


def cov_conley(f, Z, D, corte):
    W = np.clip(1 - D / corte, 0, None)
    S = Z * f["e"][:, None]
    M = S.T @ W @ S
    return f["XtXi"] @ M @ f["XtXi"] * f["n"] / (f["n"] - f["k"])


def dist_km(xy):
    d = xy[:, None, :] - xy[None, :, :]
    return np.sqrt((d ** 2).sum(-1))


def covs(f, Z, Dm):
    return {"hc3": cov_hc3(f, Z), "c100": cov_conley(f, Z, Dm, 100.0), "c200": cov_conley(f, Z, Dm, 200.0)}


def wald_p(f, V, idx):
    q = len(idx)
    b = f["b"][idx]
    try:
        W = float(b @ np.linalg.solve(V[np.ix_(idx, idx)], b)) / q
    except np.linalg.LinAlgError:
        return np.nan
    return float(stats.f.sf(W, q, f["n"] - f["k"]))


def std(M):
    M = np.asarray(M, float)
    return (M - M.mean(0)) / M.std(0, ddof=1)


def perm_p(y, Zfull, idx, perms):
    """Freedman-Lane: contraste (t si len(idx)=1; F si >1) de las columnas idx, perms (n x B) de residuos del modelo reducido."""
    n, k = Zfull.shape
    keep = [j for j in range(k) if j not in idx]
    Zr = Zfull[:, keep]
    br = np.linalg.lstsq(Zr, y, rcond=None)[0]
    fit, er = Zr @ br, y - Zr @ br
    P = np.linalg.pinv(Zfull)                        # k x n
    Ystar = np.column_stack([y] + [fit + er[perms[:, b]] for b in range(perms.shape[1])])
    Bt = P @ Ystar
    R = Ystar - Zfull @ Bt
    s2 = (R ** 2).sum(0) / (n - k)
    XtXi = np.linalg.inv(Zfull.T @ Zfull)
    if len(idx) == 1:
        j = idx[0]
        T = np.abs(Bt[j] / np.sqrt(s2 * XtXi[j, j]))
    else:
        Vi = np.linalg.inv(XtXi[np.ix_(idx, idx)])
        T = np.einsum("ib,ij,jb->b", Bt[idx], Vi, Bt[idx]) / len(idx) / s2
    return float((1 + (T[1:] >= T[0] - 1e-12).sum()) / (1 + perms.shape[1]))


def holm_adj(p):
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * p[o]))
    out = np.empty(m)
    out[o] = adj
    return out


def bh_adj(p):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p)
    a = np.minimum.accumulate((p[o] * m / (np.arange(m) + 1))[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(1, a)
    return out


# ------------------------------------------------------------ especificación
def spec(D, lab, ysel, src="t", w=2015, excl_grandes=False, fam_use=None, sample_mask=None, f6src=None):
    X, fam = bd.regresores(D, lab, w=w, src=src)
    if f6src:
        a0 = 2015 if lab == "P1" else 2021
        X["F6_lnp0"] = np.log(D[f"p{f6src}{a0}"])
    Y = bd.dependientes(D, lab, src=src)
    y = Y[ysel]
    ok = y.notna() & X.notna().all(axis=1)
    if excl_grandes:
        ok &= D["grande"] == 0
    if sample_mask is not None:
        ok &= sample_mask
    cols = [c for f in (fam_use or FAMS) for c in fam[f]]
    Xs = X.loc[ok, cols]
    cols = [c for c in cols if Xs[c].std(ddof=1) > 0]      # p. ej. «isla» sin Baleares ni Canarias
    Xs = Xs[cols]
    Zs = np.column_stack([np.ones(ok.sum()), std(Xs.values)])
    yy = y[ok].values.astype(float)
    xy = D.loc[ok, ["x_km", "y_km"]].values
    return dict(y=yy, Z=Zs, cols=cols, fam=fam, idx=list(D.index[ok]), Dm=dist_km(xy), sdy=float(yy.std(ddof=1)),
                sdx=Xs.std(ddof=1).values, ysel=ysel, lab=lab, src=src)


def estima(S, perms=None, perm_idx=None):
    """Estima el modelo y devuelve filas por coeficiente y por familia."""
    y, Z, cols = S["y"], S["Z"], S["cols"]
    f = ajusta(y, Z)
    V = covs(f, Z, S["Dm"])
    dfr = f["n"] - f["k"]
    tss = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (f["e"] ** 2).sum() / tss
    r2a = 1 - (1 - r2) * (f["n"] - 1) / dfr
    ncoef, nfam = [], []
    for j, c in enumerate(cols, start=1):
        se = {k: float(np.sqrt(v[j, j])) for k, v in V.items()}
        p = {k: float(2 * stats.t.sf(abs(f["b"][j] / s), dfr)) for k, s in se.items()}
        row = dict(coef=c, familia=c.split("_")[0], b=float(f["b"][j]), beta_std=float(f["b"][j] / S["sdy"]),
                   **{f"se_{k}": s for k, s in se.items()}, **{f"p_{k}": q for k, q in p.items()})
        row["p_mayor"] = max(p.values())
        row["se_mayor"] = max(se.values())
        row["p_perm"] = perm_p(y, Z, [j], perms) if perms is not None else np.nan
        ncoef.append(row)
    for fm, cs in S["fam"].items():
        cs = [c for c in cs if c in cols]
        if not cs:
            continue
        idx = [cols.index(c) + 1 for c in cs]
        p = {k: wald_p(f, v, idx) for k, v in V.items()}
        nfam.append(dict(familia=fm, q=len(cs), p_hc3=p["hc3"], p_c100=p["c100"], p_c200=p["c200"], p_mayor=max(p.values()),
                         p_perm=perm_p(y, Z, idx, perms) if perms is not None else np.nan))
    return dict(f=f, V=V, r2=float(r2), r2a=float(r2a), n=f["n"], K=len(cols), coefs=pd.DataFrame(ncoef), fams=pd.DataFrame(nfam))


def shapley(y, Xs, fam_cols):
    """Shapley de R² por familia (todas las 2^8 submuestras de familias)."""
    fams = list(fam_cols)
    m = len(fams)
    tss = ((y - y.mean()) ** 2).sum()
    cache = {}

    def r2(sub):
        if sub in cache:
            return cache[sub]
        if not sub:
            cache[sub] = 0.0
            return 0.0
        c = [x for f in sub for x in fam_cols[f]]
        A = np.column_stack([np.ones(len(y)), Xs[c].values])
        b = np.linalg.lstsq(A, y, rcond=None)[0]
        cache[sub] = float(1 - ((y - A @ b) ** 2).sum() / tss)
        return cache[sub]

    out = {}
    for f in fams:
        otros = [g for g in fams if g != f]
        s = 0.0
        for r in range(m):
            for sub in itertools.combinations(otros, r):
                sub = tuple(sorted(sub))
                w = factorial(r) * factorial(m - r - 1) / factorial(m)
                s += w * (r2(tuple(sorted(sub + (f,)))) - r2(sub))
        out[f] = s
    return out, r2(tuple(sorted(fams)))


def loo_rmse(y, Z):
    n = len(y)
    f = ajusta(y, Z)
    e = f["e"] / (1 - f["h"])
    base = y - (y.sum() - y) / (n - 1)       # LOO del modelo solo con media
    return e, base


def dm_hln(e1, e2):
    """Diebold-Mariano con pérdida cuadrática, h=1, corrección Harvey-Leybourne-Newbold (t con n-1 gl).
    d = e1^2 - e2^2; DM<0 => e1 mejor."""
    d = e1 ** 2 - e2 ** 2
    n = len(d)
    dm = d.mean() / np.sqrt(d.var(ddof=1) / n)
    hln = dm * np.sqrt((n - 1) / n)
    return float(hln), float(2 * stats.t.sf(abs(hln), n - 1))


def main():
    D, meta = bd.construir()
    reg = []
    rng = np.random.default_rng(SEED)
    PERMS = {}

    def perms_for(n):
        if n not in PERMS:
            PERMS[n] = np.column_stack([rng.permutation(n) for _ in range(NPERM)])
        return PERMS[n]

    def log(fase, mid, tipo, S, E, fam=None, coef=None, row=None, notas=""):
        r = dict(fase=fase, modelo_id=mid, formula=f"{S['ysel']}[{S['lab']},{S['src']}] ~ " + "+".join(S["cols"]) if fam is None else "", tipo=tipo,
                 muestra_ini=min(S["idx"]), muestra_fin=max(S["idx"]), n=E["n"], r2_adj=E["r2a"], aic=np.nan, bic=np.nan,
                 rmse_oos=np.nan, familia=fam, coef=coef, notas=notas, Y=S["ysel"], periodo=S["lab"], fuente_Y=S["src"])
        r.update(row)
        reg.append(r)

    todas_f = {}
    # ======================================================= especificación principal y rejilla familia x Y x periodo
    cuadro = {}
    for lab in ("P1", "P2"):
        for ysel in ("Y1", "Y2", "Y3"):
            S = spec(D, lab, ysel)
            E = estima(S, perms=perms_for(len(S["y"])))
            cuadro[(lab, ysel)] = (S, E)
            for _, r in E["coefs"].iterrows():
                log("B3-coef", f"{ysel}_{lab}_{r['coef']}", "COEFICIENTE", S, E, fam=r["familia"], coef=r["coef"],
                    row={k: r[k] for k in r.index if k not in ("coef", "familia")},
                    notas="coeficiente de la especificación principal (sin ajuste propio: el ajuste está en las filas de familia)")
            for _, r in E["fams"].iterrows():
                tipo = "CONFIRMATORIA" if (lab, ysel) == ("P1", "Y1") else "EXPLORATORIA"
                log("B3-fam", f"{ysel}_{lab}_{r['familia']}", tipo, S, E, fam=r["familia"],
                    row={k: r[k] for k in r.index if k != "familia"}, notas="p de familia = Wald conjunto; p_mayor = máximo de HC3, Conley 100 y 200 km")
    # confirmatorias: p de H-B3-2 por el coeficiente líder; Holm sobre las 8 familias x Y1 x P1
    S, E = cuadro[("P1", "Y1")]
    fam_p = E["fams"].set_index("familia").p_mayor.copy()
    cf = E["coefs"].set_index("coef")
    for h, (fm, c, sg) in LEAD.items():
        fam_p[fm] = cf.loc[c, "p_mayor"]
    holm8 = pd.Series(holm_adj(fam_p.loc[FAMS].values), index=FAMS)
    holm3 = pd.Series(holm_adj(fam_p.loc[["F1", "F2", "F6"]].values), index=["F1", "F2", "F6"])
    for r in reg:
        if r["fase"] == "B3-fam" and r["tipo"] == "CONFIRMATORIA":
            r["p_ajustado"] = holm8[r["familia"]]
            r["metodo_ajuste"] = "Holm(8 familias x Y1 x P1)"
            r["p_mayor_usado"] = fam_p[r["familia"]]
    # exploratorias: BH sobre las 40 familias x Y x periodo no confirmatorias
    ex = [r for r in reg if r["fase"] == "B3-fam" and r["tipo"] == "EXPLORATORIA"]
    adj = bh_adj([r["p_mayor"] for r in ex])
    for r, a in zip(ex, adj):
        r["p_ajustado"] = float(a)
        r["metodo_ajuste"] = "BH(40 exploratorias)"
    # ======================================================= hipótesis
    hip = {}
    for h, (fm, c, sg) in LEAD.items():
        r = cf.loc[c]
        hip[h] = dict(familia=fm, regresor=c, signo_esperado=sg, b_por_DT=float(r.b), beta_std=float(r.beta_std),
                      ic95=[float(r.b - stats.t.ppf(0.975, E["n"] - E["f"]["k"]) * r.se_mayor), float(r.b + stats.t.ppf(0.975, E["n"] - E["f"]["k"]) * r.se_mayor)],
                      p_hc3=float(r.p_hc3), p_c100=float(r.p_c100), p_c200=float(r.p_c200), p_mayor=float(r.p_mayor), p_perm=float(r.p_perm),
                      p_holm8=float(holm8[fm]), p_holm3=float(holm3[fm]), signo_observado=int(np.sign(r.b)),
                      signo_coincide=bool(np.sign(r.b) == sg), rechaza_holm8=bool(holm8[fm] < 0.05), rechaza_holm3=bool(holm3[fm] < 0.05),
                      concuerda_perm=bool((r.p_perm < 0.05) == (r.p_mayor < 0.05)))
    # ======================================================= LOO frente a modelo de media (sustituto del AR(4)/ECM v1: no aplican a corte transversal)
    e_m, e_b = loo_rmse(S["y"], S["Z"])
    hln, p_dm = dm_hln(e_m, e_b)
    fuera = dict(modelo="MCO 8 familias, LOO-CV (validación en bloques con embargo no aplica a corte transversal)",
                 rmse=float(np.sqrt((e_m ** 2).mean())), rmse_media=float(np.sqrt((e_b ** 2).mean())), dm_vs_ar4=None,
                 dm_hln_vs_media=hln, p_dm_hln_vs_media=p_dm)
    # ======================================================= Y1 en la muestra de Y2 (misma muestra)
    mask46 = D["y2_P1"].notna()
    S46 = spec(D, "P1", "Y1", sample_mask=mask46)
    E46 = estima(S46, perms=perms_for(len(S46["y"])))
    for _, r in E46["fams"].iterrows():
        log("B3-rob", f"Y1_P1_muestraY2_{r['familia']}", "ROBUSTEZ", S46, E46, fam=r["familia"],
            row={k: r[k] for k in r.index if k != "familia"}, notas="Y1 en las 46 provincias con Y2 (misma muestra)")
    # control de error de medida en F6: Y1 (tasado) con el precio inicial de Registradores
    Sx6 = spec(D, "P1", "Y1", f6src="r")
    Ex6 = estima(Sx6, perms=perms_for(len(Sx6["y"])))
    c6 = Ex6["coefs"].set_index("coef").loc["F6_lnp0"]
    hip["H-B3-6"]["control_error_medida_F6_precio_registradores"] = dict(b_por_DT=float(c6.b), p_mayor=float(c6.p_mayor), p_perm=float(c6.p_perm))
    log("B3-rob", "Y1_P1_F6_precio_registradores", "ROBUSTEZ", Sx6, Ex6, fam="F6", coef="F6_lnp0",
        row={k: c6[k] for k in c6.index if k not in ("coef", "familia")}, notas="F6 medido con otra fuente (Registradores 2015) para acotar el sesgo por error de medida/reversión")
    # robustez Y1 con Registradores, Y2 con IPVA
    rob_p = {}
    for lab in ("P1", "P2"):
        Sr = spec(D, lab, "Y1", src="r")
        Er = estima(Sr, perms=perms_for(len(Sr["y"])))
        rob_p[("Y1r", lab)] = (Sr, Er)
        for _, r in Er["fams"].iterrows():
            log("B3-rob", f"Y1reg_{lab}_{r['familia']}", "ROBUSTEZ", Sr, Er, fam=r["familia"],
                row={k: r[k] for k in r.index if k != "familia"}, notas="Y1 = precio Registradores provincial (F6 con su propia fuente)")
        Si = spec(D, lab, "Y2_ipva")
        Ei = estima(Si, perms=perms_for(len(Si["y"])))
        for _, r in Ei["fams"].iterrows():
            log("B3-rob", f"Y2ipva_{lab}_{r['familia']}", "ROBUSTEZ", Si, Ei, fam=r["familia"],
                row={k: r[k] for k in r.index if k != "familia"}, notas="Y2 = IPVA provincial (INE), 2015/2021 a 2024")
    # ======================================================= Shapley (dos fuentes de Y1)
    shp = {}
    for src, nom in (("t", "valor_tasado"), ("r", "registradores")):
        Sx = spec(D, "P1", "Y1", src=src)
        Xd = pd.DataFrame(Sx["Z"][:, 1:], columns=Sx["cols"])
        fc = {f: [c for c in Sx["cols"] if c.startswith(f + "_")] for f in FAMS}
        sv, rt = shapley(Sx["y"], Xd, fc)
        shp[nom] = dict(sv=sv, r2=rt, n=len(Sx["y"]))
    st = pd.DataFrame({k: v["sv"] for k, v in shp.items()})
    st["cuota_tasado_pct"] = st.valor_tasado / shp["valor_tasado"]["r2"] * 100
    st["cuota_reg_pct"] = st.registradores / shp["registradores"]["r2"] * 100
    st["rango_tasado"] = st.valor_tasado.rank(ascending=False).astype(int)
    st["rango_reg"] = st.registradores.rank(ascending=False).astype(int)
    st.index.name = "familia"
    st.to_csv(OUT / "tablas/shapley_R2.csv")
    orden_igual = bool((st.rango_tasado == st.rango_reg).all())
    rho = float(stats.spearmanr(st.valor_tasado, st.registradores).statistic)
    tau = float(stats.kendalltau(st.valor_tasado, st.registradores).statistic)
    # ======================================================= multiverso
    mv = []
    for lab, src, w, ex_g, se in itertools.product(("P1", "P2"), ("t", "r"), (2015, 2011), (False, True), ("hc3", "c200")):
        Sx = spec(D, lab, "Y1", src=src, w=w, excl_grandes=ex_g)
        Ex = estima(Sx)
        for h, (fm, c, sg) in LEAD.items():
            r = Ex["coefs"].set_index("coef").loc[c]
            p = float(r[f"p_{se}"])
            mv.append(dict(hipotesis=h, periodo=lab, fuente=src, pesos_bartik=w, sin_grandes=ex_g, ee=se, n=Ex["n"], b=float(r.b),
                           p=p, signo=int(np.sign(r.b)), signo_esperado=sg))
            reg.append(dict(fase="B3-multiverso", modelo_id=f"MV_{h}_{lab}_{src}_{w}_{'sg' if ex_g else 'cg'}_{se}", formula=f"Y1[{lab},{src}] lider {c}",
                            tipo="MULTIVERSO", muestra_ini="", muestra_fin="", n=Ex["n"], r2_adj=Ex["r2a"], aic=np.nan, bic=np.nan, rmse_oos=np.nan,
                            familia=fm, coef=c, b=float(r.b), p_mayor=p, p_ajustado=np.nan, metodo_ajuste="sin ajuste (conjunto de sensibilidad)",
                            notas="multiverso", Y="Y1", periodo=lab, fuente_Y=src))
    mv = pd.DataFrame(mv)
    mv.to_csv(OUT / "tablas/multiverso.csv", index=False)
    mvr = []
    for h, g in mv.groupby("hipotesis"):
        ref = hip[h]["signo_observado"]
        mvr.append(dict(hipotesis=h, n_especificaciones=len(g), pct_mismo_signo_que_principal=float((g.signo == ref).mean() * 100),
                        pct_signo_esperado=float((g.signo == g.signo_esperado).mean() * 100), pct_p_menor_005=float((g.p < 0.05).mean() * 100),
                        b_min=float(g.b.min()), b_max=float(g.b.max())))
    mvr = pd.DataFrame(mvr)
    mvr.to_csv(OUT / "tablas/multiverso_resumen.csv", index=False)
    # ======================================================= Oster y Cinelli-Hazlett
    sens = {}
    S, E = cuadro[("P1", "Y1")]
    n = S["Z"].shape[0]
    for h in ("H-B3-1", "H-B3-2"):
        fm, c, sg = LEAD[h]
        j = S["cols"].index(c) + 1
        x = S["Z"][:, j]
        otros = [i for i in range(S["Z"].shape[1]) if i != j]
        C = S["Z"][:, otros]
        y = S["y"]

        def res(v, C=C):
            return v - C @ np.linalg.lstsq(C, v, rcond=None)[0]
        yc, xc = y - y.mean(), x - x.mean()
        r = OSTER(yc, xc, res(y), res(x), np.arange(n), 1, S["Z"].shape[1] - 1)
        sens[h] = {k: (None if isinstance(v, float) and not np.isfinite(v) else v) for k, v in r.items()}
        sens[h]["regresor"] = c
        sens[h]["nota"] = "Corto = solo el regresor; largo = las 8 familias. gl de RV: G-1 con G=N (cada provincia su clúster) y N-K-1 (RV_gl_n)."
        reg.append(dict(fase="B3-sens", modelo_id=f"SENS_{h}", formula=f"Oster/CH {c}", tipo="SENSIBILIDAD", n=n, r2_adj=np.nan, familia=fm, coef=c,
                        b=r["b_largo"], p_mayor=np.nan, p_ajustado=np.nan, metodo_ajuste="no aplica",
                        notas=f"delta*={r['delta_oster']:.3g}; RV={r['RV_gl_n']:.3g}; RV_alpha={r['RV_alpha_gl_n']:.3g}", Y="Y1", periodo="P1", fuente_Y="t"))
    json.dump(sens, open(OUT / "tablas/sensibilidad.json", "w"), indent=1, ensure_ascii=False)
    # ======================================================= tablas
    cuadro_filas = []
    for (lab, ysel), (Sx, Ex) in cuadro.items():
        c = Ex["coefs"].copy()
        c.insert(0, "Y", ysel)
        c.insert(1, "periodo", lab)
        c["n"] = Ex["n"]
        c["r2"] = Ex["r2"]
        cuadro_filas.append(c)
    pd.concat(cuadro_filas).to_csv(OUT / "tablas/coeficientes_principal.csv", index=False)
    rg = pd.DataFrame(reg)
    rg.to_csv(OUT / "registro.csv", index=False)
    # ======================================================= salidas JSON (se completan abajo con el mapa)
    resumen = dict(hip=hip, fuera=fuera, shap=dict(orden_igual=orden_igual, spearman=rho, kendall=tau, r2_tasado=shp["valor_tasado"]["r2"],
                                                   r2_reg=shp["registradores"]["r2"]),
                   n={f"{k[1]}_{k[0]}": v[1]["n"] for k, v in cuadro.items()}, sens=sens, mvr=mvr.to_dict("records"),
                   holm8=holm8.to_dict(), holm3=holm3.to_dict(), ycre=meta["ycre"], r2_principal=E["r2"], r2a_principal=E["r2a"])
    json.dump(resumen, open(OUT / "tablas/resumen_interno.json", "w"), indent=1, ensure_ascii=False, default=float)
    D.drop(columns=[]).to_csv(OUT / "tablas/panel_b3.csv")
    if not SMOKE:
        import b3_salidas as bs
        bs.escribe(D, cuadro, resumen, rg, st, mv)
    print(json.dumps({"hip": hip, "fuera": fuera, "shap": resumen["shap"], "mvr": resumen["mvr"], "sens": sens}, indent=1, default=float, ensure_ascii=False))


if __name__ == "__main__":
    main()
