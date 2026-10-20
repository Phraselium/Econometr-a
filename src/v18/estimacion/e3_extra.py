"""V18 · E3 · especificaciones municipales (A3, P-H4), coprincipales provinciales (P-D4, P-Q3c1) y balance a nivel de choque.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010. Las P (adenda 1.6) reproducen la especificación ya estimada en V9, V15 o V16 en la
muestra V18 (sin unidades de v6, V15 ni V16; sellado.filtrar); no se clasifican y entran en la familia de Holm de E3.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

import _e359_comun as K
import _e359_datos as D
import e3_municipal as EM
from herramientas import webb_twfe as WT

GRUPOS = D.GRUPOS


# ------------------------------------------------------------------------------------------------ balance a nivel de choque (BHJ; plan 1.3 d)
def balance_choques(dat, pan, extra_X: dict[str, pd.Series] | None = None) -> dict:
    """Por origen c: g_c = entradas medias anuales de la ventana / stock nacional del origen en el Censo de 2001; X̄_c = media de la característica de 2001 de las provincias,
    ponderada por la exposición (peso · e_pc). Regresión de X̄_c sobre g_c (8 puntos) con t de Student (6 g. l.); Holm entre características; criterio p ajustado > 0,10."""
    E = pan.expo
    w = np.ones(len(E)) if pan.w is None else pan.w
    prov = pan.prov
    FL = dat.flujos(pan.cfg.get("interpolar_2003", False))
    años = sorted(set(pan.año))
    stock_nac = dat.stock[GRUPOS].sum(axis=0)
    g = {}
    for o in pan.origenes:
        g[o] = float(FL.loc[años, o].mean() / stock_nac[o])
    carac = {"cuota empleo construcción 2001": dat.cuota_constr, "cuota empleo industria 2001": dat.cuota_indus,
             "log población 2001": np.log(dat.stock["pob_total"].reindex(dat.P)), "cuota de extranjeros 2001": dat.cuota_ext01}
    if extra_X:
        carac.update(extra_X)
    filas = {}
    pesos = w[:, None] * E
    for nombre, X in carac.items():
        xv = X.reindex(prov).to_numpy(float)
        xbar = (pesos * xv[:, None]).sum(axis=0) / pesos.sum(axis=0)
        gv = np.array([g[o] for o in pan.origenes])
        A = np.column_stack([np.ones(len(gv)), gv])
        b = np.linalg.lstsq(A, xbar, rcond=None)[0]
        e = xbar - A @ b
        h = np.einsum("ij,jk,ik->i", A, np.linalg.pinv(A.T @ A), A)
        meat = (A * (e / (1 - h))[:, None]).T @ (A * (e / (1 - h))[:, None])      # HC3
        V = np.linalg.pinv(A.T @ A) @ meat @ np.linalg.pinv(A.T @ A)
        tt = float(b[1] / np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
        filas[nombre] = {"pendiente": float(b[1]), "t": tt, "p": float(2 * stats.t.sf(abs(tt), len(gv) - 2))}
    ph = K.holm({k: v["p"] for k, v in filas.items()})
    for k in filas:
        filas[k]["p_holm"] = ph[k]
    return {"por_caracteristica": filas, "p_holm_min": min(ph.values()), "choques": g, "n_choques": len(g),
            "nota": "con 8 choques la potencia es mínima; renta, paro y cuota urbana de 2001 no están a escala provincial en el repositorio"}


# ------------------------------------------------------------------------------------------------ municipal
def sigma_pre_municipal(mun: EM.DatosMunicipal, cfgm: dict) -> tuple[float, float]:
    pre = mun.panel(ventana=(2012, 2013), origenes=cfgm.get("origenes"), peso_pob0=False, solo_resultado=True, min_años=1,
                    sin_distritos_sellados=cfgm.get("sin_distritos_sellados", False), mun_min_pob=cfgm.get("mun_min_pob"))
    d = pre["D"]
    d = d[~d["cod"].isin(EM.GRANDES)]
    dis = K.DisenoIV(d["y"].to_numpy(), d["y"].to_numpy(), d["y"].to_numpy(), d["prov"].to_numpy(), grupos=(d["prov"] + "_" + d["año"].astype(str)).to_numpy(), B=1)
    r = dis._m(dis.sw * d["y"].to_numpy()[dis.orden]) / dis.sw
    return K.sigma_rho_equicorr(r, d["cod"].to_numpy()[dis.orden])


def precomprobar_municipal(mun: EM.DatosMunicipal, cfgm: dict, ref_v: float, R: int) -> dict:
    pa = mun.panel(**{k: v for k, v in cfgm.items() if k in ("ventana", "origenes", "peso_pob0", "mun_min_pob", "sin_distritos_sellados", "resultado", "min_años")})
    d = pa["D"]
    dis = K.DisenoIV(d["y"].to_numpy(), d["x"].to_numpy(), d["z"].to_numpy(), d["prov"].to_numpy(), w=pa["w"], grupos=d["pv"].to_numpy(), B=1)
    sig, rho = sigma_pre_municipal(mun, cfgm)
    m = K.mde_iv(dis, None, sig, rho, R=R, unidad=d["cod"].to_numpy()[dis.orden])
    m.update({"ref": ref_v, "estimable": bool(m["mde80"] <= ref_v), "n": dis.n, "G": dis.G, "k": dis.k, "n_pre": None, "F_eff": dis.f_efectivo()})
    s_c = (pa["w"] if pa["w"] is not None else np.ones(len(d)))[:, None] * np.abs(pa["ZC"])
    sc = s_c.sum(axis=0)
    m["inv_hhi_origen"] = {"por_origen": K.inv_hhi(sc), "pesos_origen": {o: float(v) for o, v in zip(pa["origenes"], sc / sc.sum())}}
    return m


def estimar_municipal(mun: EM.DatosMunicipal, cfgm: dict, B: int, completo: bool) -> dict:
    pa = mun.panel(**{k: v for k, v in cfgm.items() if k in ("ventana", "origenes", "peso_pob0", "mun_min_pob", "sin_distritos_sellados", "resultado", "min_años")})
    d = pa["D"]
    dis = K.DisenoIV(d["y"].to_numpy(), d["x"].to_numpy(), d["z"].to_numpy(), d["prov"].to_numpy(), w=pa["w"], grupos=d["pv"].to_numpy(), B=B)
    r = dis.resumen(con_ic=True, con_ic90=completo)
    r["panel"], r["dis"], r["pa"] = pa, dis, pa
    r["n_municipios"] = int(d["cod"].nunique())
    return r


def diag_municipal(mun: EM.DatosMunicipal, cfgm: dict, r: dict, ref_v: float, B: int) -> dict:
    out = {}
    pa, dis, d = r["pa"], r["dis"], r["pa"]["D"]
    ic = (r["ic_webb_ar"]["lo"], r["ic_webb_ar"]["hi"])
    kw = {k: v for k, v in cfgm.items() if k in ("origenes", "peso_pob0", "mun_min_pob", "sin_distritos_sellados", "resultado")}
    # pretendencia: Δ alquiler 2012-2013 medio sobre el instrumento medio, con efectos de provincia
    pre = mun.panel(ventana=(2012, 2013), solo_resultado=True, min_años=1, **{k: v for k, v in kw.items() if k != "peso_pob0"})["D"]
    ypre = pre.groupby("cod")["y"].mean()
    zb = d.groupby("cod")[["z", "x"]].mean()
    com = [c for c in ypre.index if c in zb.index]
    prov = np.array([c[:2] for c in com])
    w = None if not cfgm.get("peso_pob0") else mun.N["Total"][cfgm["ventana"][0] - 1].reindex(com).to_numpy(float)
    dp = K.DisenoIV(ypre.loc[com].to_numpy(), zb.loc[com, "z"].to_numpy(), zb.loc[com, "z"].to_numpy(), prov, w=w, grupos=prov, B=B)
    rp = dp.iv()
    d1 = K.DisenoIV(zb.loc[com, "x"].to_numpy(), zb.loc[com, "z"].to_numpy(), zb.loc[com, "z"].to_numpy(), prov, w=w, grupos=prov, B=1)
    pics = d1.iv()["beta"]
    det = (1.96 + 0.8416) * rp["se"]
    out["pretendencia"] = {"pendiente": rp["beta"], "se": rp["se"], "p_t": rp["p_t"], "p_webb": dp.webb_ar_p(0.0), "pendiente_detectable80": det, "primera_etapa_cs": pics,
                           "sesgo_detectable_beta": det / abs(pics), "n": len(com)}
    out["pretendencia"]["roth_ok"] = bool(out["pretendencia"]["sesgo_detectable_beta"] < 0.5 * ref_v)
    # placebo de fecha: instrumento de t + 6 en 2012-2013 (años 2018-2019 de la ventana)
    zmap = d.set_index(["cod", "año"])["z"]
    pf = pre.copy()
    pf["zf"] = [zmap.get((c, t + 6), np.nan) for c, t in zip(pf["cod"], pf["año"])]
    pf = pf.dropna(subset=["zf"])
    pf["prov"] = pf["cod"].str[:2]
    dpf = K.DisenoIV(pf["y"].to_numpy(), pf["zf"].to_numpy(), pf["zf"].to_numpy(), pf["prov"].to_numpy(), grupos=(pf["prov"] + "_" + pf["año"].astype(str)).to_numpy(), B=B)
    rpf = dpf.iv()
    out["placebo_fecha"] = {"coef": rpf["beta"], "se": rpf["se"], "p_webb": dpf.webb_ar_p(0.0), "n": rpf["n"],
                            "mismo_signo_mitad": bool(np.sign(rpf["beta"]) == np.sign(r["rf"]) and abs(rpf["beta"]) >= 0.5 * abs(r["rf"]))}
    out["placebo_resultado"] = None   # población de 65 años o más por municipio: no está en el repositorio
    # Rotemberg: excluir los 5 orígenes de más peso (plan 1.3 d)
    ZC = np.column_stack([dis._m(dis.sw * pa["ZC"][dis.orden, j]) for j in range(pa["ZC"].shape[1])])
    rot = K.rotemberg(ZC, dis.xt, dis.yt)
    alpha = rot["alpha"]
    top = list(np.argsort(-np.abs(alpha))[:5])
    keep = [j for j in range(len(alpha)) if j not in top]
    z2 = pa["ZC"][:, keep].sum(axis=1)
    d2 = K.DisenoIV(d["y"].to_numpy(), d["x"].to_numpy(), z2, d["prov"].to_numpy(), w=pa["w"], grupos=d["pv"].to_numpy(), B=B)
    r2 = d2.iv()
    ic2 = d2.ic_webb_ar(0.05, centro=r2["beta"], escala=r2["se"])
    out["rotemberg"] = {"alpha_top": {pa["origenes"][j]: float(alpha[j]) for j in np.argsort(-np.abs(alpha))[:8]}, "excluidos": [pa["origenes"][j] for j in top],
                        "beta_sin_top": r2["beta"], "se": r2["se"], "F_eff": d2.f_efectivo(), "ic_webb_ar": ic2, "mismo_signo": bool(np.sign(r2["beta"]) == np.sign(r["beta"])),
                        "dentro_ic": bool(ic[0] <= r2["beta"] <= ic[1])}
    # JRS: instrumento de t-4 como control (FWL con efectos de provincia-año)
    try:
        pl = mun.panel(**{k: v for k, v in cfgm.items() if k in ("ventana", "origenes", "peso_pob0", "mun_min_pob", "sin_distritos_sellados", "resultado", "min_años")}, con_lag=True)
        dl = pl["D"].dropna(subset=["zlag"])
        wl = None if pl["w"] is None else pl["w"][pl["D"]["zlag"].notna().to_numpy()]
        base = K.DisenoIV(dl["y"].to_numpy(), dl["x"].to_numpy(), dl["z"].to_numpy(), dl["prov"].to_numpy(), w=wl, grupos=dl["pv"].to_numpy(), B=1)
        zl = base._m(base.sw * dl["zlag"].to_numpy()[base.orden])
        coef = {}
        for nm in ("y", "x", "z"):
            v = base._m(base.sw * dl[nm].to_numpy()[base.orden])
            coef[nm] = float(zl @ v / (zl @ zl))
        yj = dl["y"].to_numpy() - coef["y"] * dl["zlag"].to_numpy()
        xj = dl["x"].to_numpy() - coef["x"] * dl["zlag"].to_numpy()
        zj = dl["z"].to_numpy() - coef["z"] * dl["zlag"].to_numpy()
        dj = K.DisenoIV(yj, xj, zj, dl["prov"].to_numpy(), w=wl, grupos=dl["pv"].to_numpy(), B=1)
        rj = dj.iv()
        out["jrs"] = {"beta": rj["beta"], "se": rj["se"], "F_eff": dj.f_efectivo(), "n": rj["n"], "dentro_ic": bool(ic[0] <= rj["beta"] <= ic[1]),
                      "nota": "instrumento de t-4 como control, por Frisch-Waugh sobre los efectos provincia-año"}
    except Exception as e:   # pragma: no cover
        out["jrs"] = {"error": str(e)}
    # sin atípicos (1 % superior de exposición y 1 % extremo del resultado)
    zbar = d.groupby("cod")["z"].mean()
    ybar = d.groupby("cod")["y"].mean()
    k = max(1, int(round(0.01 * len(zbar))))
    at = set(zbar.nlargest(k).index) | set((ybar - ybar.median()).abs().nlargest(k).index)
    da = d[~d["cod"].isin(at)]
    wa = None if pa["w"] is None else pa["w"][~d["cod"].isin(at).to_numpy()]
    dis_a = K.DisenoIV(da["y"].to_numpy(), da["x"].to_numpy(), da["z"].to_numpy(), da["prov"].to_numpy(), w=wa, grupos=da["pv"].to_numpy(), B=1)
    ra = dis_a.iv()
    out["sin_atipicos"] = {"n_excluidos": len(at), "beta": ra["beta"], "se": ra["se"], "mismo_signo": bool(np.sign(ra["beta"]) == np.sign(r["beta"])), "n": ra["n"]}
    # balance a nivel de choque con las características municipales de 2003 (población y cuota de extranjeros)
    g = {}
    años = sorted(set(d["año"]))
    G = pd.concat([mun._gcrec(pa["origenes"], t).mean() for t in años], axis=1).mean(axis=1)
    tot03 = mun.N["Total"][2003]
    car = {"log población 2003": np.log(tot03), "cuota de extranjeros 2003": mun.N["Extranjera"][2003] / tot03}
    S = pa["S"]
    wpob = d.groupby("cod").size().index
    filas = {}
    for nm, Xs in car.items():
        xbar = []
        for o in pa["origenes"]:
            sw_ = S.loc[S.index.isin(wpob), o].fillna(0) * tot03.reindex(S.index[S.index.isin(wpob)])
            xv = Xs.reindex(sw_.index)
            xbar.append(float((sw_ * xv).sum() / sw_.sum()) if sw_.sum() > 0 else np.nan)
        xbar = np.array(xbar)
        gv = np.array([G[o] for o in pa["origenes"]])
        ok = np.isfinite(xbar) & np.isfinite(gv)
        A = np.column_stack([np.ones(ok.sum()), gv[ok]])
        b = np.linalg.lstsq(A, xbar[ok], rcond=None)[0]
        e = xbar[ok] - A @ b
        h = np.einsum("ij,jk,ik->i", A, np.linalg.pinv(A.T @ A), A)
        meat = (A * (e / (1 - h))[:, None]).T @ (A * (e / (1 - h))[:, None])
        V = np.linalg.pinv(A.T @ A) @ meat @ np.linalg.pinv(A.T @ A)
        tt = float(b[1] / np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
        filas[nm] = {"pendiente": float(b[1]), "t": tt, "p": float(2 * stats.t.sf(abs(tt), ok.sum() - 2))}
    ph = K.holm({k_: v["p"] for k_, v in filas.items()})
    for k_ in filas:
        filas[k_]["p_holm"] = ph[k_]
    out["balance"] = {"por_caracteristica": filas, "p_holm_min": min(ph.values()), "n_choques": int(len(pa["origenes"]))}
    return out


# ------------------------------------------------------------------------------------------------ coprincipales provinciales
def _padron_prov(dat) -> pd.DataFrame:
    p = K.leer_hechos("padron_pob_nacionalidad", "provincia", "A")
    p["nac"] = p["desagregacion"].str.replace("nacionalidad=", "", regex=False)
    p["cod"] = p["territorio_codigo"]
    p = p[p["cod"].isin(dat.P)]
    p["año"] = p["periodo"].astype(int)
    return p[["cod", "año", "nac", "valor"]]


def p_d4(dat, B: int) -> dict:
    """E3-P-D4: V9-D4, réplica 2003-2012 (src/v9/d4_inmigracion.py, paneles.construir, herramientas.iv_just). Δ ln valor tasado 2003-2012 sobre la variación de extranjeros 2003-2012 en
    puntos de la población de 2003; instrumento de Card (cuotas de 2003 por país × crecimiento nacional sin la propia provincia); controles log población inicial y suma de cuotas.
    Muestra V18: provincias de entrenamiento. Inferencia: Webb-AR (cada provincia es un cluster) y AR exacto."""
    p = _padron_prov(dat)
    EXC = ("Total", "Española", "Extranjera")
    AGR = ("De ", "Europa", "País", "Oceanía")
    pais = p[~p["nac"].isin(EXC) & ~p["nac"].str.startswith(AGR)]
    tot = p[p["nac"] == "Total"].pivot_table(index="cod", columns="año", values="valor")
    ext = p[p["nac"] == "Extranjera"].pivot_table(index="cod", columns="año", values="valor")
    t0, t1 = 2003, 2012
    F0 = pais[pais["año"] == t0].pivot_table(index="cod", columns="nac", values="valor").fillna(0)
    F1 = pais[pais["año"] == t1].pivot_table(index="cod", columns="nac", values="valor").reindex_like(F0).fillna(0)
    N0, N1 = F0.sum(0), F1.sum(0)
    g = ((N1 - F1) - (N0 - F0)) / (N0 - F0).replace(0, np.nan)
    w = F0.div(tot.loc[F0.index, t0], axis=0)
    Z = (w * g.fillna(0)).sum(1) * 100
    x = (ext.loc[F0.index, t1] - ext.loc[F0.index, t0]) / tot.loc[F0.index, t0] * 100
    out = {}
    for nombre, ser in (("valor tasado", dat.vt), ("IPC de alquiler", dat.ipc)):
        y = np.log(ser[t1] / ser[t0]).reindex(F0.index)
        m = y.notna() & x.notna() & Z.notna()
        C = np.column_stack([np.ones(m.sum()), np.log(tot.loc[F0.index, t0])[m], w.sum(1)[m]])
        d = K.DisenoIV(y[m].to_numpy(), x[m].to_numpy(), Z[m].to_numpy(), np.arange(m.sum()), C=C, B=B)
        r = d.resumen(con_ic=True, con_ic90=False)
        out[nombre] = {"beta": r["beta"], "se": r["se"], "F_eff": r["F_eff"], "p_webb_ar": r["p_webb_ar"], "p_ar": r["ar"]["p_beta0"], "ic_webb_ar": r["ic_webb_ar"], "n": r["n"],
                       "G": r["G"], "pi": r["pi"], "ar": r["ar"], "ic95_t": r["ic95_t"], "rf": r["rf"], "p_t": r["p_t"]}
    out["publicado_v9"] = {"IPC de alquiler 2003-2012": 0.0072, "valor tasado 2003-2012": -0.0029, "F efectivo V9": "3,4 a 4,6"}
    return out


def p_q3c1(dat, B: int) -> dict:
    """E3-P-Q3c1: V16 (src/v16/q3_shiftshare.py): ln valor tasado = β·x + α_p + γ_t, 2011-2022 (padrón por nacionalidad hasta 2022), x = 100·Σ_o F_{p,o,2003}·(N_{o,t,-p}/N_{o,2003,-p})/Pob_{p,2003}
    (puntos de la población de 2003; 28 orígenes del padrón). Forma reducida de MCO con efectos de provincia y de año (herramienta de V16); inferencia aquí con el bootstrap de Webb para TWFE (APTO)."""
    p = _padron_prov(dat)
    ORIGENES = ["Alemania", "Argelia", "Argentina", "Bolivia", "Brasil", "Bulgaria", "Chile", "China", "Colombia", "Cuba", "Ecuador", "Francia", "Italia", "Marruecos", "Nigeria", "Pakistán",
                "Paraguay", "Perú", "Polonia", "Portugal", "Reino Unido", "República Dominicana", "Rumanía", "Rusia", "Senegal", "Ucrania", "Uruguay", "Venezuela"]
    años = list(range(2011, 2023))
    tot = p[p["nac"] == "Total"].pivot_table(index="cod", columns="año", values="valor")
    F = p[p["nac"].isin(ORIGENES)].pivot_table(index=["cod"], columns=["año", "nac"], values="valor").fillna(0)
    provs = [c for c in tot.index if c in dat.P]
    Nn = {t: F[t].sum(0) for t in sorted(set(a for a, _ in F.columns))}
    x = {}
    for u in provs:
        fila = {}
        for t in años:
            comp = 0.0
            for o in ORIGENES:
                n_t = Nn[t][o] - F.loc[u, (t, o)]
                n_b = Nn[2003][o] - F.loc[u, (2003, o)]
                if n_b > 0:
                    comp += F.loc[u, (2003, o)] * n_t / n_b
            fila[t] = 100.0 * comp / tot.loc[u, 2003]
        x[u] = fila
    X = pd.DataFrame(x).T
    y = np.log(dat.vt.reindex(provs)[años])
    ok = y.notna().all(axis=1)
    prov_ok = list(ok[ok].index)
    Y = y.loc[prov_ok].to_numpy()
    Xm = X.loc[prov_ok, años].to_numpy()
    rng = np.random.default_rng(K.SEMILLA)
    beta, se, _, _ = WT.twfe_crve(Y, Xm)
    pw, tstat, _, _ = WT.wcr_webb(Y, Xm, 0.0, B, rng)
    # IC por inversión del Webb (misma semilla)
    def pf(b0):
        return WT.wcr_webb(Y, Xm, b0, B, np.random.default_rng(K.SEMILLA))[0]
    centro, esc = beta, se
    out_ic = []
    for s in (-1.0, 1.0):
        dentro, fuera, k = centro, centro + s * 4 * esc, 0
        while pf(fuera) >= 0.05 and k < 6:
            dentro, fuera, k = fuera, fuera + s * 6 * esc, k + 1
        for _ in range(14):
            m = (dentro + fuera) / 2
            dentro, fuera = (m, fuera) if pf(m) >= 0.05 else (dentro, m)
        out_ic.append((dentro + fuera) / 2)
    return {"beta": float(beta), "se": float(se), "p_webb": float(pw), "ic_webb": (float(out_ic[0]), float(out_ic[1])), "n": int(Y.size), "G": int(Y.shape[0]), "T": int(Y.shape[1]),
            "publicado_v16": 0.0119, "unidad": "log del valor tasado por punto de población de 2003"}
