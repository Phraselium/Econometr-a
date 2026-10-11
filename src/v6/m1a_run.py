"""M1a v6: econometría explicativa del ALQUILER (stock SERPAVI/IPC y contratos nuevos, por separado).
Solo paneles de entrenamiento de output/v6/M0/paneles. Sin red. SEED=20261010. `--smoke` = submuestra y B=99."""
import json
import os
import sys
import time
import warnings
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src/v6"))
import m1a_lib as L  # noqa: E402
from econ_utils import Registry  # noqa: E402
from holdout import CCAA_PROV  # noqa: E402  (solo el diccionario provincia->CCAA; no se abre ningún sellado)

warnings.filterwarnings("ignore")
SEED = 20261010
SMOKE = "--smoke" in sys.argv
B = 99 if SMOKE else 999
PAN = RAIZ / "output/v6/M0/paneles"
OUT = RAIZ / ("output/v6/M1A/_smoke" if SMOKE else "output/v6/M1A")
OUT.mkdir(parents=True, exist_ok=True)
FECHA = "2026-10-11"
rng = np.random.default_rng(SEED)
reg = Registry(OUT / "registro.csv")

ALQ_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres",
           "n_mun_tensionados", "n_mun_topes_cat"]
MUN_REG = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_vut", "ln_terminadas_libres", "ln_iniciadas_libres",
           "tensionada_mun", "tope_cat_mun"]
DIS_REG = ["ln_vut_plazas_dis", "ln_pib_pc"]
SC = ["ln_pob", "share_ext_pob", "ln_pib_pc"]
SC2 = ["ln_pob", "ln_pib_pc"]
DELTA = {  # variable -> (etiqueta, tipo, cantidad)
    "ln_vut": ("+1.000 viviendas turísticas", "ln", 1000), "ln_pob": ("+10.000 habitantes", "ln", 10000),
    "ln_pib_pc": ("+1.000 EUR de PIB por habitante", "ln", 1000),
    "ln_terminadas_libres": ("+1.000 viviendas libres terminadas", "ln", 1000),
    "ln_iniciadas_libres": ("+1.000 viviendas libres iniciadas", "ln", 1000),
    "ln_hip_viv_num": ("+1.000 hipotecas sobre vivienda", "ln", 1000),
    "share_ext_pob": ("+1 punto de población extranjera", "lin", 1),
    "n_mun_tensionados": ("+1 municipio tensionado", "lin", 1), "n_mun_topes_cat": ("+1 municipio con tope", "lin", 1),
    "tensionada_mun": ("municipio pasa a zona tensionada", "lin", 1), "tope_cat_mun": ("municipio pasa a tope", "lin", 1),
    "ln_vut_plazas_dis": ("+100 plazas turísticas en el distrito", "ln", 100)}


def rd(path, **kw):
    return pd.read_csv(PAN / path, dtype={"cod": str, "cod_prov": str, "cod_mun": str, "distrito": str}, **kw)


# ------------------------------------------------------------------ datos
alq = rd("prov_alquiler_anual_train.csv.gz")
cmp_ = rd("prov_compra_anual_train.csv.gz")
mun = rd("mun_alquiler_anual_train.csv.gz")
dis = rd("dis_alquiler_anual_train.csv.gz")
con = rd("prov_contratos_nuevos_anual_train.csv.gz")
cen = pd.read_csv(RAIZ / "data/raw/v5/municipio_centroides_utm30.csv", dtype={"codigo": str})
cen = cen.rename(columns={"codigo": "cod_mun"})

PROV_VARS = ["ln_pob", "share_ext_pob", "ln_pib_pc", "ln_terminadas_libres", "ln_iniciadas_libres", "ln_hip_viv_num"]
rt = cmp_[["cod", "anio"] + PROV_VARS].merge(alq[["cod", "anio", "ln_vut", "n_mun_tensionados", "n_mun_topes_cat"]],
                                              on=["cod", "anio"], how="outer")
rt["anio"] += 1  # regresores en t-1: el valor de t-1 se etiqueta con el año t
rt = rt.rename(columns={"cod": "cod_prov"})
ccaa = lambda s: s.map(lambda c: CCAA_PROV.get(str(c).zfill(2), "x"))  # noqa: E731

# panel provincial
P = alq.rename(columns={"cod": "cod_prov"}).drop(columns=["ln_vut", "n_mun_tensionados", "n_mun_topes_cat"])
P = P.merge(rt, on=["cod_prov", "anio"], how="left")
P["unit"], P["ccaa"] = P.cod_prov, ccaa(P.cod_prov)
P["ln_alq_m2"] = P.ln_alq_m2_serpavi_vc
sup = float(np.nanmean(np.exp(alq.ln_alq_mes_serpavi_vc - alq.ln_alq_m2_serpavi_vc)))  # m2 implícitos
RENTA_PROV = float(np.nanmean(np.exp(alq.ln_alq_mes_serpavi_vc)))

# panel municipal
m_own = mun[["cod_mun", "anio", "tensionada_mun", "tope_cat_mun"]].copy()
m_own["anio"] += 1
M = mun[["cod_mun", "anio", "cod_prov", "ln_alq_m2_serpavi_mun"]].merge(m_own, on=["cod_mun", "anio"], how="left")
M = M.merge(rt, on=["cod_prov", "anio"], how="left")
M = M.merge(cen[["cod_mun", "x_m", "y_m"]], on="cod_mun", how="left")
M["unit"], M["ccaa"] = M.cod_mun, ccaa(M.cod_prov)
M["ln_alq_m2"] = M.ln_alq_m2_serpavi_mun
# eventos (sin retardo) para event study
EV = mun[["cod_mun", "anio", "cod_prov", "ln_alq_m2_serpavi_mun", "tope_cat_mun", "tensionada_mun"]].copy()

# panel de distritos
d_own = dis[["distrito", "anio", "ln_vut_plazas_dis"]].copy()
d_own["anio"] += 1
D = dis[["distrito", "anio", "cod_prov", "ln_alq_m2_serpavi_dis", "ln_alq_m2_p25_dis", "ln_alq_m2_p75_dis"]].merge(
    d_own, on=["distrito", "anio"], how="left")
D = D.merge(rt[["cod_prov", "anio", "ln_pib_pc"]], on=["cod_prov", "anio"], how="left")
D["cod_mun"] = D.distrito.str[:5]
D = D.merge(cen[["cod_mun", "x_m", "y_m"]], on="cod_mun", how="left")
D["unit"], D["ccaa"] = D.distrito, ccaa(D.cod_prov)
D["ln_alq_m2"] = D.ln_alq_m2_serpavi_dis

if SMOKE:
    keep = set(pd.Series(M.cod_mun.unique()).sample(frac=0.15, random_state=SEED))
    M = M[M.cod_mun.isin(keep)]
    EV = EV[EV.cod_mun.isin(keep)]
    kd = set(pd.Series(D.distrito.unique()).sample(frac=0.15, random_state=SEED))
    D = D[D.distrito.isin(kd)]

# ------------------------------------------------------------------ núcleo de ajuste
ROWS = []  # resultados por (spec, variable)
DIAG = {}


def prep(df, y, xs, minobs=2):
    d = df.dropna(subset=[y] + xs).copy()
    cnt = d.groupby("unit").anio.transform("size")
    d = d[cnt >= minobs].sort_values(["unit", "anio"]).reset_index(drop=True)
    u = pd.factorize(d.unit)[0]
    t = (d.anio - d.anio.min()).to_numpy().astype(int)
    cl = pd.factorize(d.ccaa)[0]
    return d, u, t, cl


def convert(var, b, lo, hi, d, y):
    """Magnitud en EUR/mes para el cambio unitario declarado. Devuelve (etiqueta, EUR/mes, lo, hi, % )."""
    if var not in DELTA or y not in ("ln_alq_m2", "ln_alq_mes_serpavi_vc"):
        return (None, np.nan, np.nan, np.nan, np.nan)
    lab, kind, amt = DELTA[var]
    dx = amt
    if kind == "ln":
        lv = float(np.nanmean(np.exp(d[var])))
        dx = np.log1p(amt / lv)
    renta = float(np.nanmean(np.exp(d[y]))) * (sup if y == "ln_alq_m2" else 1.0)
    f = lambda c: (np.exp(c * dx) - 1) * renta  # noqa: E731
    return (lab, f(b), f(lo), f(hi), 100 * (np.exp(b * dx) - 1))


def fit(df, y, xs, nivel, mercado, spec, familia, trend=False, conley=False, sens=True, ylab=None, nota=""):
    t0 = time.time()
    d, u, t, cl = prep(df, y, xs)
    if len(d) < len(xs) + 10 or cl.max() < 2:
        DIAG[f"{nivel}|{spec}"] = {"omitida": "N insuficiente", "n": int(len(d))}
        return None
    Z = L.absorb(np.column_stack([d[y].to_numpy(float)] + [d[x].to_numpy(float) for x in xs]), u, t, trend)
    ya, Xa = Z[:, 0], Z[:, 1:]
    const = [x for x, s_ in zip(xs, Xa.std(0)) if s_ < 1e-8]  # sin variacion tras absorber FE (p. ej. zonas tensionadas)
    if const:
        reg.log("M1a", f"{nivel}|{spec}|sin_variacion", ",".join(const), "", "", len(d), np.nan, np.nan, np.nan, np.nan, np.nan,
                np.nan, "excluidas: sin variacion intra-unidad en entrenamiento")
        xs = [x for x in xs if x not in const]
        Xa = Xa[:, Xa.std(0) >= 1e-8]
    k_abs = int(t.max())
    b, e, Minv = L.ols(ya, Xa)
    V, G = L.cr1(Xa, e, Minv, cl, k_abs)
    se = np.sqrt(np.diag(V))
    dk = np.sqrt(np.diag(L.dk_cov(Xa, e, Minv, t)))
    cf = None
    if conley:
        loc = pd.factorize(d.cod_mun)[0]
        xy = d.groupby("cod_mun")[["x_m", "y_m"]].first().reindex(pd.unique(d.cod_mun)).to_numpy(float)
        if np.isfinite(xy).all():
            cf = np.sqrt(np.diag(L.conley_cov(Xa, e, Minv, t, loc, xy)))
    r2l = 1 - (e @ e) / (ya @ ya)
    tq = stats.t.ppf(0.975, G - 1)
    nu = d.unit.nunique()
    for j, x in enumerate(xs):
        pw, t_c = L.wild_p(ya, Xa, Minv, cl, j, B, rng, "webb", k_abs)
        pr, _ = L.wild_p(ya, Xa, Minv, cl, j, B, rng, "rademacher", k_abs)
        pdk = 2 * stats.t.sf(abs(b[j] / dk[j]), max(t.max(), 1))
        pcf = 2 * stats.norm.sf(abs(b[j] / cf[j])) if cf is not None else np.nan
        lo, hi = b[j] - tq * se[j], b[j] + tq * se[j]
        out = dict(mercado=mercado, nivel=nivel, spec=spec, familia=familia, metodo="TWFE" + ("+tend" if trend else ""),
                   var=x, y=ylab or y, b=b[j], se=se[j], lo=lo, hi=hi, p=pw, p_tipo="wild Webb", p_rade=pr, p_dk=pdk,
                   se_dk=dk[j], se_conley=cf[j] if cf is not None else np.nan, p_conley=pcf, t_cluster=t_c, N=len(d),
                   unidades=nu, G=G, anio_min=int(d.anio.min()), anio_max=int(d.anio.max()), nota=nota)
        if sens:
            xj = Xa[:, [j]]
            bc, ec, _ = L.ols(ya, xj)
            r2c = 1 - (ec @ ec) / (ya @ ya)
            ds, b1 = L.oster(bc[0], b[j], r2c, r2l)
            rv, rva = L.cinelli_hazlett(b[j] / se[j], max(G - 1, 2))
            out.update(oster_delta=ds, oster_beta_d1=b1, ch_rv=rv, ch_rv_alpha=rva, b_corto=bc[0])
        lab, mm, ml, mh, pc = convert(x, b[j], lo, hi, d, "ln_alq_m2" if y == "ln_alq_m2" else y)
        out.update(unidad=lab, eur_mes=mm, eur_mes_lo=ml, eur_mes_hi=mh, pct=pc)
        ROWS.append(out)
        reg.log("M1a", f"{nivel}|{spec}|{x}", f"{y} ~ {x} | {','.join(xs)} +FE", d.anio.min(), d.anio.max(), len(d), np.nan,
                np.nan, np.nan, np.nan, b[j], pw, f"{familia}; {out['metodo']}; p wild Webb B={B}; {nota}")
    DIAG[f"{nivel}|{spec}"] = {"n": int(len(d)), "excluidas_sin_variacion": const, "unidades": int(nu), "clusters": int(G), "r2_within": float(r2l),
                               "anios": [int(d.anio.min()), int(d.anio.max())], "seg": round(time.time() - t0, 1)}
    return dict(d=d, u=u, t=t, cl=cl, ya=ya, Xa=Xa, b=b, V=V, G=G)


def add_row_generic(mercado, nivel, spec, familia, metodo, x, b, se, p, ptipo, N, units, G, d, ylab="ln_alq_m2", nota="",
                    extra=None, dfm=None):
    tq = stats.t.ppf(0.975, max(G - 1, 1))
    lo, hi = b - tq * se, b + tq * se
    lab, mm, ml, mh, pc = convert(x, b, lo, hi, dfm if dfm is not None else d, ylab) if dfm is not None or d is not None else (None,) * 5
    r = dict(mercado=mercado, nivel=nivel, spec=spec, familia=familia, metodo=metodo, var=x, y=ylab, b=b, se=se, lo=lo, hi=hi,
             p=p, p_tipo=ptipo, N=N, unidades=units, G=G, unidad=lab, eur_mes=mm, eur_mes_lo=ml, eur_mes_hi=mh, pct=pc,
             nota=nota)
    if extra:
        r.update(extra)
    ROWS.append(r)
    reg.log("M1a", f"{nivel}|{spec}|{x}", f"{metodo}: {ylab} ~ {x}", "", "", N, np.nan, np.nan, np.nan, np.nan, b, p,
            f"{familia}; {ptipo}; {nota}")


# ------------------------------------------------------------------ 1. Alquiler de stock: especificaciones TWFE
MS = "alquiler de stock"
LONG_P = [x for x in ALQ_REG if x != "ln_vut"]
LONG_M = [x for x in MUN_REG if x != "ln_vut"]
t_start = time.time()

fits = {}
fits["P0"] = fit(P, "ln_alq_m2", ALQ_REG, "provincia", MS, "S0 pre-registrada (TWFE, caso completo)", "confirmatoria",
                 nota="incluye ln_vut: solo 2021-2023")
fits["P0t"] = fit(P, "ln_alq_m2", ALQ_REG, "provincia", MS, "S0 + tendencias por unidad", "robustez", trend=True)
fits["P1"] = fit(P, "ln_alq_m2", LONG_P, "provincia", MS, "S1 muestra larga sin ln_vut (TWFE)", "robustez",
                 nota="desviacion: sin ln_vut (cobertura 2020-2024)")
fits["P1t"] = fit(P, "ln_alq_m2", LONG_P, "provincia", MS, "S1 + tendencias por unidad", "robustez", trend=True)
fits["P1mes"] = fit(P, "ln_alq_mes_serpavi_vc", LONG_P, "provincia", MS, "S1 desenlace EUR/mes", "robustez",
                    ylab="ln_alq_mes_serpavi_vc")
fits["P1ipc"] = fit(P, "ln_ipc_alq_idx", LONG_P, "provincia", "alquiler de stock (IPC)", "S1 desenlace IPC alquiler (indice)",
                    "robustez", ylab="ln_ipc_alq_idx", sens=False, nota="IPC: indice, sin conversion a EUR/mes")
# primeras diferencias
Pd = P.sort_values(["unit", "anio"]).copy()
for c in ["ln_alq_m2"] + LONG_P:
    Pd["d_" + c] = Pd.groupby("unit")[c].diff()
    ok = Pd.groupby("unit").anio.diff() == 1
    Pd.loc[~ok, "d_" + c] = np.nan
fits["P1d"] = fit(Pd, "d_ln_alq_m2", ["d_" + c for c in LONG_P], "provincia", MS, "S1 primeras diferencias", "robustez",
                  ylab="d_ln_alq_m2", sens=False)

fits["M0"] = fit(M, "ln_alq_m2", MUN_REG, "municipio", MS, "S0 pre-registrada (TWFE, caso completo)", "confirmatoria",
                 nota="regresores provinciales + tensionada_mun/tope_cat_mun; incluye ln_vut")
fits["M0t"] = fit(M, "ln_alq_m2", MUN_REG, "municipio", MS, "S0 + tendencias por unidad", "robustez", trend=True)
fits["M1"] = fit(M, "ln_alq_m2", LONG_M, "municipio", MS, "S1 muestra larga sin ln_vut (TWFE)", "robustez")
fits["M1t"] = fit(M, "ln_alq_m2", LONG_M, "municipio", MS, "S1 + tendencias por unidad", "robustez", trend=True)

fits["D0"] = fit(D, "ln_alq_m2", DIS_REG, "distrito", MS, "S0 pre-registrada (TWFE, caso completo)", "confirmatoria",
                 conley=True, nota="desenlace = punto medio p25-p75; ln_vut_plazas_dis solo 2022-2023 tras el retardo")
fits["D0t"] = fit(D, "ln_alq_m2", DIS_REG, "distrito", MS, "S0 + tendencias por unidad", "robustez", trend=True, conley=True)
fits["D1"] = fit(D, "ln_alq_m2", ["ln_pib_pc"], "distrito", MS, "S1 muestra larga solo ln_pib_pc", "robustez", conley=True)
fits["D1p25"] = fit(D, "ln_alq_m2_p25_dis", ["ln_pib_pc"], "distrito", MS, "S1 desenlace p25", "robustez", conley=True,
                    ylab="ln_alq_m2_p25_dis", sens=False)
fits["D1p75"] = fit(D, "ln_alq_m2_p75_dis", ["ln_pib_pc"], "distrito", MS, "S1 desenlace p75", "robustez", conley=True,
                    ylab="ln_alq_m2_p75_dis", sens=False)
print("TWFE hecho", round(time.time() - t_start), "s", flush=True)


# ------------------------------------------------------------------ 2. CCE, MG, SDM (muestra común SC)
def hetero_block(df, nivel, xy_col=True, sdm=True):
    d, u, t, cl = prep(df, "ln_alq_m2", SC, minobs=5)
    y = d.ln_alq_m2.to_numpy(float)
    X = d[SC].to_numpy(float)
    Z = L.absorb(np.column_stack((y, X)), u, t)
    ya, Xa = Z[:, 0], Z[:, 1:]
    bt, et, Mi = L.ols(ya, Xa)
    Vt, G = L.cr1(Xa, et, Mi, cl, int(t.max()))
    dd = dict(nivel=nivel, N=len(d), unidades=int(d.unit.nunique()), G=G)
    for j, x in enumerate(SC):  # TWFE en la misma muestra
        add_row_generic(MS, nivel, "SC TWFE (muestra comun CCE/MG/SDM)", "robustez", "TWFE", x, bt[j], np.sqrt(Vt[j, j]),
                        2 * stats.t.sf(abs(bt[j] / np.sqrt(Vt[j, j])), G - 1), "t cluster CCAA", len(d), dd["unidades"], G, d,
                        dfm=d)
    # CCEP
    bc, Vc, Gc, nc, nuc = L.cce_p(y, X, u, t, cl)
    for j, x in enumerate(SC):
        add_row_generic(MS, nivel, "SC CCEP", "robustez", "CCEP Pesaran", x, bc[j], np.sqrt(Vc[j, j]),
                        2 * stats.t.sf(abs(bc[j] / np.sqrt(Vc[j, j])), Gc - 1), "t cluster CCAA", nc, nuc, Gc, d, dfm=d,
                        nota="cobertura limitada: T<=8 y parametros por unidad")
    # MG y CCEMG (2 regresores en CCEMG por grados de libertad)
    mg, se, nmg, sdb = L.mean_group(y, X, u, t, cce=False)
    for j, x in enumerate(SC):
        add_row_generic(MS, nivel, "SC MG", "robustez", "Mean Group", x, mg[j], se[j], 2 * stats.t.sf(abs(mg[j] / se[j]), nmg - 1),
                        "t entre unidades", len(d), nmg, G, d, dfm=d, extra={"sd_entre_unidades": float(sdb[j])},
                        nota="heterogeneidad: sd de los coeficientes por unidad en sd_entre_unidades")
    X2 = d[SC2].to_numpy(float)
    mc, sc_, nmc, sdc = L.mean_group(y, X2, u, t, cce=True, min_extra=1)
    for j, x in enumerate(SC2):
        add_row_generic(MS, nivel, "SC2 CCEMG", "robustez", "CCEMG Pesaran", x, mc[j], sc_[j],
                        2 * stats.t.sf(abs(mc[j] / sc_[j]), max(nmc - 1, 1)), "t entre unidades", len(d), nmc, G, d, dfm=d,
                        extra={"sd_entre_unidades": float(sdc[j])}, nota="grados de libertad por unidad: 1 con T=8")
    if sdm:
        xy_u = d.groupby("unit")[["x_m", "y_m"]].first().reindex(pd.unique(d.unit)).to_numpy(float) if "x_m" in d else None
        if nivel == "provincia":
            xy_u = prov_xy.reindex(pd.unique(d.unit)).to_numpy(float)
        uidx = pd.factorize(d.unit)[0]
        ok = np.isfinite(xy_u).all(1)
        if (~ok).any():  # unidades sin centroide: se excluyen
            msk = ok[uidx]
            d2 = d[msk]
            uidx2 = pd.factorize(d2.unit)[0]
            xy2 = xy_u[ok]
            y2, X2s, t2, cl2 = d2.ln_alq_m2.to_numpy(float), d2[SC].to_numpy(float), t[msk], pd.factorize(d2.ccaa)[0]
        else:
            d2, uidx2, xy2, y2, X2s, t2, cl2 = d, uidx, xy_u, y, X, t, cl
        Z2 = L.absorb(np.column_stack((y2, X2s)), uidx2, t2)
        for trend in (False,):
            r = L.sdm_2sls(Z2[:, 0], Z2[:, 1:], uidx2, t2, cl2, xy2, k=5, trend=trend, B=500 if not SMOKE else 100)
            DIAG[f"{nivel}|SDM"] = {"rho": float(r["rho"]), "rho_se": r["rho_se"], "n": r["n"], "G": r["G"],
                                    "W": "5 vecinos mas cercanos por anio, estandarizada por filas",
                                    "estimador": "2SLS (instrumentos W2X, W3X)"}
            if abs(r["rho"]) >= 0.98:
                DIAG[f"{nivel}|SDM"]["impactos"] = "no reportados: |rho|>=0,98 (serie de impactos no convergente)"
                reg.log("M1a", f"{nivel}|SC SDM", "SDM 2SLS", "", "", r["n"], np.nan, np.nan, np.nan, np.nan, r["rho"], np.nan,
                        "rho fuera de rango; impactos no reportados")
                continue
            for j, x in enumerate(SC):
                for k_, nm in (("dir", "directo"), ("ind", "indirecto"), ("tot", "total")):
                    bb, ss = float(r[k_][j]), float(r[k_ + "_se"][j])
                    add_row_generic(MS, nivel, f"SC SDM {nm}", "robustez", f"SDM 2SLS ({nm})", x, bb, ss,
                                    2 * stats.norm.sf(abs(bb / ss)), "z simulado", r["n"], int(np.unique(uidx2).size), r["G"], d2,
                                    dfm=d2, extra={"rho": float(r["rho"])}, nota="W kNN (k=5) sobre centroides")


# centroides de provincia: municipio con más secciones (proxy de la capital) -- ver desviaciones.md
cen2 = cen.copy()
cen2["cod_prov"] = cen2.cod_mun.str[:2]
cen2 = cen2.sort_values(["cod_prov", "n_secciones"], ascending=[True, False]).groupby("cod_prov").first()
prov_xy = cen2[["x_m", "y_m"]]
hetero_block(P, "provincia")
hetero_block(M, "municipio")
print("CCE/MG/SDM hecho", round(time.time() - t_start), "s", flush=True)

# ------------------------------------------------------------------ 3. DML con cross-fitting
for nivel, df, regs_all, hip in (("provincia", P, ALQ_REG, True), ("municipio", M, MUN_REG, False)):
    trs = ["ln_vut", "ln_pob", "ln_terminadas_libres"] + (["ln_hip_viv_num"] if hip else [])
    for tr_ in trs:
        ctrl = [c for c in (regs_all if tr_ == "ln_vut" else [c for c in regs_all if c != "ln_vut"]) if c != tr_]
        xs = [tr_] + ctrl
        d, u, t, cl = prep(df, "ln_alq_m2", xs)
        if len(d) < 80:
            continue
        Z = L.absorb(np.column_stack([d.ln_alq_m2.to_numpy(float)] + [d[c].to_numpy(float) for c in xs]), u, t)
        th, se, G = L.dml_plr(Z[:, 0], Z[:, 1], Z[:, 2:], cl, nfold=5, trees=100 if SMOKE else 150)
        add_row_generic(MS, nivel, f"DML PLR ({tr_})", "robustez", "DML (RF, cross-fitting por CCAA)", tr_, th, se,
                        2 * stats.t.sf(abs(th / se), G - 1), "t cluster CCAA", len(d), int(d.unit.nunique()), G, d, dfm=d,
                        nota="asociacion parcial sin supuestos de forma funcional; no es efecto causal. Credito: ln_hip_viv_num")
print("DML hecho", round(time.time() - t_start), "s", flush=True)

# ------------------------------------------------------------------ 4. Exposición (shift-share de un solo choque, tipo BHJ)
try:
    sh = cmp_.pivot(index="cod", columns="anio", values="share_ext_pob")
    base = sh[2015]
    cur = P.copy()
    tot = sh.sum(0)
    cnt = sh.notna().sum(0)
    loo = pd.DataFrame({a: (tot[a] - sh[a]) / (cnt[a] - 1) for a in sh.columns})  # media de las demás provincias, año a
    loo.index = sh.index
    cur["z"] = [base.get(c, np.nan) * loo.at[c, a - 1] if (c in loo.index and (a - 1) in loo.columns) else np.nan
                for c, a in zip(cur.cod_prov, cur.anio)]
    cur["ln_alq_prev"] = cur.groupby("unit").ln_alq_m2.shift(1)
    cur["g_prev"] = cur.ln_alq_prev - cur.groupby("unit").ln_alq_m2.shift(2)
    xs_ctrl = [c for c in LONG_P if c != "share_ext_pob"]
    d, u, t, cl = prep(cur, "ln_alq_m2", ["share_ext_pob", "z"] + xs_ctrl)
    Z = L.absorb(np.column_stack([d[c].to_numpy(float) for c in ["ln_alq_m2", "share_ext_pob", "z"] + xs_ctrl]), u, t)
    y_, en, zz, Cc = Z[:, 0], Z[:, 1], Z[:, 2], Z[:, 3:]
    Zi = np.column_stack((zz, Cc))
    fs, e_fs, Mfs = L.ols(en, Zi)
    Vfs, G = L.cr1(Zi, e_fs, Mfs, cl, int(t.max()))
    F = float((fs[0] / np.sqrt(Vfs[0, 0])) ** 2)
    enh = Zi @ fs
    Xh = np.column_stack((enh, Cc))
    b2, _, Mh = L.ols(y_, Xh)
    e2 = y_ - np.column_stack((en, Cc)) @ b2
    V2, _ = L.cr1(Xh, e2, Mh, cl, int(t.max()))
    # placebo: z (t-1) sobre el crecimiento previo del alquiler (t-1 menos t-2)
    dp, up, tp, clp = prep(cur, "g_prev", ["z"] + xs_ctrl)
    Zp = L.absorb(np.column_stack([dp[c].to_numpy(float) for c in ["g_prev", "z"] + xs_ctrl]), up, tp)
    bp, ep, Mp = L.ols(Zp[:, 0], Zp[:, 1:])
    Vp, Gp = L.cr1(Zp[:, 1:], ep, Mp, clp, int(tp.max()))
    pp_ = 2 * stats.t.sf(abs(bp[0] / np.sqrt(Vp[0, 0])), Gp - 1)
    p_iv = 2 * stats.t.sf(abs(b2[0] / np.sqrt(V2[0, 0])), G - 1)
    DIAG["provincia|exposicion_IV"] = {"F_primera_etapa_cluster": F, "n": len(d), "clusters": int(G),
                                       "placebo_crecimiento_previo_coef": float(bp[0]), "placebo_p": float(pp_),
                                       "instrumento": "share_ext_pob 2015 x media de las demas provincias en t-1 (un solo choque; "
                                                      "sin origen: padron por pais fuera de los paneles de M0)",
                                       "rotemberg": "no aplicable (un solo choque); exposicion tipo Borusyak-Hull-Jaravel",
                                       "veredicto": "no supera placebo" if pp_ < 0.10 else "placebo no rechazado; C3 requiere ademas "
                                                                                          "exclusion plausible, no demostrada"}
    add_row_generic(MS, "provincia", "IV exposicion (share_ext_pob)", "robustez", "2SLS exposicion", "share_ext_pob", b2[0],
                    np.sqrt(V2[0, 0]), p_iv, "t cluster CCAA", len(d), int(d.unit.nunique()), G, d, dfm=d,
                    extra={"F_1a_etapa": F, "placebo_p": float(pp_)}, nota="C4: exclusion no verificable")
except Exception as ex:  # el diagnóstico se documenta, no se oculta
    DIAG["provincia|exposicion_IV"] = {"error": repr(ex)}

# ------------------------------------------------------------------ 5. Event study de topes en Cataluña + Rambachan-Roth
try:
    E = EV.copy()
    E["unit"], E["ccaa"] = E.cod_mun, ccaa(E.cod_prov)
    g = E[E.tope_cat_mun == 1].groupby("cod_mun").anio.min()
    E["g"] = E.cod_mun.map(g)
    E["trat"] = E.g.notna()
    E = E.dropna(subset=["ln_alq_m2_serpavi_mun"])
    ks = [k for k in range(-5, 4) if k != -1]
    for k in ks:
        E[f"k{k}"] = ((E.anio - E.g) == k).astype(float)
    E["cl_prov"] = pd.factorize(E.cod_prov)[0]
    u = pd.factorize(E.unit)[0]
    t = (E.anio - E.anio.min()).to_numpy().astype(int)
    cols = [f"k{k}" for k in ks]
    Z = L.absorb(np.column_stack([E.ln_alq_m2_serpavi_mun.to_numpy(float)] + [E[c].to_numpy(float) for c in cols]), u, t)
    b, e, Mi = L.ols(Z[:, 0], Z[:, 1:])
    V, G = L.cr1(Z[:, 1:], e, Mi, E.cl_prov.to_numpy(), int(t.max()))
    se = np.sqrt(np.diag(V))
    coefs = dict(zip(ks, b))
    pre = [k for k in ks if k < 0]
    Wd = float(b[[ks.index(k) for k in pre]] @ np.linalg.pinv(V[np.ix_([ks.index(k) for k in pre], [ks.index(k) for k in pre])])
               @ b[[ks.index(k) for k in pre]])
    p_pre = float(stats.chi2.sf(Wd, len(pre)))
    seq = [coefs[k] for k in sorted(pre)] + [0.0]
    m_pre = max(abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1))
    b0 = coefs[0]
    rr = {str(Mb): [float(b0 - Mb * m_pre), float(b0 + Mb * m_pre)] for Mb in (0.5, 1.0, 1.5, 2.0)}
    breakdown = float(abs(b0) / m_pre) if m_pre > 0 else None
    # placebo temporal: tratamiento ficticio dos años antes, solo años anteriores al real
    Eb = E[(E.anio < E.g.fillna(9999)) | (~E.trat)]
    Eb = Eb[Eb.anio <= (g.min() - 1 if len(g) else 9999)]
    Eb["post_f"] = (Eb.trat & (Eb.anio >= Eb.g - 2)).astype(float)
    ub, tb = pd.factorize(Eb.unit)[0], (Eb.anio - Eb.anio.min()).to_numpy().astype(int)
    Zb = L.absorb(np.column_stack((Eb.ln_alq_m2_serpavi_mun.to_numpy(float), Eb.post_f.to_numpy(float))), ub, tb)
    bb, eb, Mb_ = L.ols(Zb[:, 0], Zb[:, 1:])
    Vb, Gb = L.cr1(Zb[:, 1:], eb, Mb_, pd.factorize(Eb.cod_prov)[0], int(tb.max()))
    p_plac = float(2 * stats.t.sf(abs(bb[0] / np.sqrt(Vb[0, 0])), Gb - 1))
    DIAG["municipio|event_study_tope_cat"] = {
        "tratados": int(E[E.trat].cod_mun.nunique()), "controles": int(E[~E.trat].cod_mun.nunique()), "cohortes": sorted(set(map(int, g.unique()))),
        "coef_evento": {str(k): [float(coefs[k]), float(se[ks.index(k)])] for k in ks}, "p_conjunta_pretendencias": p_pre,
        "RR_relative_magnitudes_conjunto_k0": rr, "RR_M_breakdown_plugin": breakdown, "max_salto_pre": float(m_pre),
        "placebo_fecha_ficticia_p": p_plac, "clusters_provincia": int(G),
        "nota": "RR simplificado: conjunto identificado plug-in con las estimaciones puntuales (sin IC de longitud fija); "
                "tratados en 4 provincias de una CCAA; tope vigente 2020-2021 (anulado)"}
    ok_c3 = (p_pre > 0.10) and (p_plac > 0.10) and (breakdown is not None and breakdown >= 1.0) and G >= 30
    DIAG["municipio|event_study_tope_cat"]["criterios_C3_cumplidos"] = bool(ok_c3)
    for k in [0, 1, 2, 3]:
        add_row_generic(MS, "municipio", f"Event study tope CAT k={k}", "robustez", "TWFE event study", "tope_cat_mun", coefs[k],
                        se[ks.index(k)], float(2 * stats.t.sf(abs(coefs[k] / se[ks.index(k)]), G - 1)), "t cluster provincia",
                        len(E), int(E.unit.nunique()), int(G), E, ylab="ln_alq_m2", dfm=E.assign(ln_alq_m2=E.ln_alq_m2_serpavi_mun),
                        extra={"p_pretend": p_pre, "RR_breakdown": breakdown},
                        nota=f"k={k} anios desde el tope; capa {'C3' if ok_c3 else 'C4 (no pasa criterios C3)'}")
except Exception as ex:
    DIAG["municipio|event_study_tope_cat"] = {"error": repr(ex)}

# ------------------------------------------------------------------ 6. Fuera de muestra (provincial, un origen) frente a AR(4) y ECM v1 aprox.
try:
    Q = P.sort_values(["unit", "anio"])
    xs = LONG_P
    Q = Q.dropna(subset=["ln_alq_m2"] + xs)
    wide = P.pivot(index="unit", columns="anio", values="ln_alq_m2")
    units = [i for i in wide.index if wide.loc[i, 2015:2023].notna().all()]
    Q = Q[Q.unit.isin(units)]
    ORIG = 2020  # último año de entrenamiento; embargo 2021; validación 2022-2023
    tr = Q[Q.anio <= ORIG]
    te = Q[Q.anio >= ORIG + 2]
    # AR(4) agrupado con constante (iterado desde ORIG)
    rows = []
    for i in units:
        for a in range(2019, ORIG + 1):
            rows.append([wide.at[i, a]] + [wide.at[i, a - k] for k in range(1, 5)])
    A = np.array(rows)
    ph = np.linalg.lstsq(np.column_stack((np.ones(len(A)), A[:, 1:])), A[:, 0], rcond=None)[0]
    # M1-fc: EF de unidad + tendencia común + X(t-1); ECM: Delta y_t sobre y_{t-1}, X_{t-1}
    ut = pd.factorize(tr.unit)[0]
    Z = np.column_stack([tr.ln_alq_m2, tr.anio - 2015] + [tr[x] for x in xs]).astype(float)
    Zd = Z - pd.DataFrame(Z).groupby(ut).transform("mean").to_numpy()
    bm = np.linalg.lstsq(Zd[:, 1:], Zd[:, 0], rcond=None)[0]
    fe = pd.Series(Z[:, 0] - Z[:, 1:] @ bm).groupby(ut).mean()
    fe.index = pd.unique(tr.unit)
    ecm_d = tr.assign(yl=tr.groupby("unit").ln_alq_m2.shift(1)).dropna(subset=["yl"])
    Xe = np.column_stack([np.ones(len(ecm_d)), ecm_d.yl] + [ecm_d[x] for x in xs]).astype(float)
    be = np.linalg.lstsq(Xe, (ecm_d.ln_alq_m2 - ecm_d.yl).to_numpy(float), rcond=None)[0]
    errs = {"AR4": [], "M1": [], "ECM": []}
    hist = {i: {a: wide.at[i, a] for a in range(2015, ORIG + 1)} for i in units}
    hist_e = {i: dict(hist[i]) for i in units}
    for a in range(ORIG + 1, 2024):
        for i in units:
            h = hist[i]
            h[a] = ph[0] + sum(ph[k] * h[a - k] for k in range(1, 5))
            r = P[(P.unit == i) & (P.anio == a)]
            x = r[xs].to_numpy(float).ravel()
            if a >= ORIG + 2 and np.isfinite(x).all():
                m1 = fe[i] + bm[0] * (a - 2015) + x @ bm[1:]
                he = hist_e[i]
                he[a] = he[a - 1] + be[0] + be[1] * he[a - 1] + x @ be[2:]
                yt = wide.at[i, a]
                errs["AR4"].append(yt - h[a])
                errs["M1"].append(yt - m1)
                errs["ECM"].append(yt - he[a])
            elif a == ORIG + 1:
                he = hist_e[i]
                x = r[xs].to_numpy(float).ravel()
                he[a] = he[a - 1] + be[0] + be[1] * he[a - 1] + (x @ be[2:] if np.isfinite(x).all() else 0.0)
    rm = {k: float(np.sqrt(np.mean(np.square(v)))) for k, v in errs.items()}
    dm_ar = L.dm_hln(errs["M1"], errs["AR4"])
    dm_ecm = L.dm_hln(errs["M1"], errs["ECM"])
    FUERA = {"modelo": "M1 (EF de unidad + tendencia comun + regresores t-1, S1)", "rmse": rm["M1"],
             "rmse_ar4": rm["AR4"], "rmse_ecm_v1_aprox": rm["ECM"],
             "dm_vs_ar4": {"DM_HLN": dm_ar[0], "p": dm_ar[1], "n": dm_ar[2]},
             "dm_vs_ecm_v1": {"DM_HLN": dm_ecm[0], "p": dm_ecm[1], "n": dm_ecm[2]},
             "origen": ORIG, "embargo": "2021", "validacion": "2022-2023", "unidades": len(units),
             "nota": "un solo origen (T corto: AR(4) exige 4 retardos); errores agrupados por provincia-anio; regresores t-1 observados "
                     "(prediccion condicional); ECM v1 aproximado (Delta y sobre y(t-1) y X(t-1), MCO agrupado); no usa la parte sellada"}
    reg.log("M1a", "fuera_muestra|M1", "ver resultado.json", 2015, 2023, len(errs["M1"]), np.nan, np.nan, np.nan, rm["M1"], np.nan,
            dm_ar[1], f"rmse AR4={rm['AR4']:.4f}; ECM={rm['ECM']:.4f}")
except Exception as ex:
    FUERA = {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": f"error: {ex!r}"}

# ------------------------------------------------------------------ 7. Contratos nuevos (descriptivo + IPVA exploratorio)
cd = con.copy()
filas = []
for c, g in cd.groupby("cod"):
    for v in ["ln_fianza_media_gva_eur", "ln_n_fianzas_gva", "pct_fianzas_600_incasol", "ln_n_fianzas_incasol", "ln_ipva_nuevo_idx"]:
        s = g.dropna(subset=[v]).sort_values("anio")
        if len(s) == 0:
            continue
        lv = s[v].to_numpy()
        val = (lambda z: float(np.exp(z))) if v.startswith("ln_") else (lambda z: float(z))
        filas.append(dict(provincia=c, variable=v, n_obs=len(s), anio_ini=int(s.anio.iloc[0]), anio_fin=int(s.anio.iloc[-1]),
                          valor_ini=val(lv[0]), valor_fin=val(lv[-1]),
                          cambio_pct=float(100 * (np.exp(lv[-1] - lv[0]) - 1)) if v.startswith("ln_") and len(s) > 1 else np.nan))
cdesc = pd.DataFrame(filas)
cdesc.to_csv(OUT / "contratos_descriptivo.csv", index=False)
Pc = con.rename(columns={"cod": "cod_prov"}).merge(rt, on=["cod_prov", "anio"], how="left")
Pc["unit"], Pc["ccaa"] = Pc.cod_prov, ccaa(Pc.cod_prov)
CN = "contratos nuevos (IPVA nuevo contrato, 38 provincias)"
fi = fit(Pc, "ln_ipva_nuevo_idx", SC, "provincia", CN, "IPVA nuevo contrato TWFE (exploratorio)", "robustez",
         ylab="ln_ipva_nuevo_idx", sens=False, nota="N~100, anios 2021-2023; indice, sin conversion a EUR/mes")
n_gva = int(con.ln_fianza_media_gva_eur.notna().sum())
n_inc = int(con.pct_fianzas_600_incasol.notna().sum())

# ------------------------------------------------------------------ ajuste de p, capa y nivel de evidencia
R = pd.DataFrame(ROWS)
R["p_ajustado"], R["ajuste"] = np.nan, ""
conf = (R.familia == "confirmatoria") & (R.metodo == "TWFE")
R["grupo"] = np.where(R.mercado.str.startswith("contratos"), "contratos", "stock")
for nivel in (R.grupo + "|" + R.nivel).unique():
    gsel = (R.grupo + "|" + R.nivel) == nivel
    m = conf & gsel & (R.spec.str.startswith("S0 pre-registrada"))
    if m.sum():
        R.loc[m, "p_ajustado"] = L.holm_adj(R.loc[m, "p"].to_numpy())
        R.loc[m, "ajuste"] = "Holm (familia: variables de hipotesis.md §2, mercado principal, este nivel)"
    m2 = (~m) & gsel & R.p.notna()
    if m2.sum():
        R.loc[m2, "p_ajustado"] = L.bh_adj(R.loc[m2, "p"].to_numpy())
        R.loc[m2, "ajuste"] = "BH q=0,10 (robustez/exploratorio, este nivel)"

R["capa"] = "C4"
R["nivel_evidencia"] = "EXPLORATORIO"
mset = ["TWFE", "TWFE+tend", "CCEP Pesaran", "Mean Group", "DML (RF, cross-fitting por CCAA)"]
for i, r in R[R.spec.str.startswith(("S0 pre-reg", "S1 muestra larga", "S1 desenlace EUR"))].iterrows():
    sg = np.sign(r.b)
    oth = R[(R.nivel == r.nivel) & (R["var"] == r["var"]) & (R.y.isin(["ln_alq_m2", "ln_alq_mes_serpavi_vc"])) &
            (R.index != i) & (R.mercado == MS) & (R.metodo.isin(mset + ["SDM 2SLS (directo)"]))]
    ok_sig = bool(r.p_ajustado < 0.10)  # Driscoll-Kraay no se usa para decidir: T=2-8 es insuficiente
    if ok_sig and len(oth) >= 2 and (np.sign(oth.b) == sg).all():
        R.loc[i, "nivel_evidencia"] = "ASOCIACION ROBUSTA"
    elif not ok_sig:
        R.loc[i, "nivel_evidencia"] = "DESCRIPTIVO (no significativa tras ajuste)"
R.loc[R.metodo.str.contains("event study"), "capa"] = "C4"
R.to_csv(OUT / "tabla_coeficientes.csv", index=False, float_format="%.6g")
cols = ["mercado", "nivel", "spec", "var", "unidad", "b", "eur_mes", "eur_mes_lo", "eur_mes_hi", "pct", "p", "p_ajustado", "capa",
        "nivel_evidencia"]
R[R.spec.str.startswith(("S0 pre-reg", "S1 muestra larga", "S1 desenlace EUR"))][cols].to_csv(
    OUT / "tabla_magnitudes_eur_mes.csv", index=False, float_format="%.5g")
reg.flush()
json.dump(DIAG, open(OUT / "diagnosticos.json", "w"), indent=1, default=float, ensure_ascii=False)

# ------------------------------------------------------------------ resultado.json, hechos.json
mainP = R[(R.nivel == "provincia") & R.spec.str.startswith("S1 muestra larga") & (R.metodo == "TWFE")]
hechos = []
for _, r in R[R.spec.str.startswith(("S0 pre-reg", "S1 muestra larga")) & (R.metodo == "TWFE")].iterrows():
    if pd.isna(r.eur_mes):
        continue
    hechos.append(dict(id=f"m1a_{r.nivel}_{r.spec[:2]}_{r['var']}", indicador=f"Alquiler de stock ({r.nivel}): {r.unidad}; "
                       f"asociacion con el alquiler SERPAVI, regresor en t-1",
                       valor=round(float(r.eur_mes), 2), min=round(float(r.eur_mes_lo), 2), max=round(float(r.eur_mes_hi), 2),
                       unidad="EUR/mes", periodo=f"{r.anio_min}-{r.anio_max}", cobertura=f"{r.unidades} unidades, N={r.N}",
                       fuentes=["MIVAU-SERPAVI", "INE", "MIVAU"], capa="C4", fecha_dato="2023 (SERPAVI)"))
json.dump(hechos, open(OUT / "hechos.json", "w"), indent=1, ensure_ascii=False)


def resumen(nivel):
    s = R[(R.nivel == nivel) & R.spec.str.startswith("S0 pre-reg")]
    return {"N": int(s.N.iloc[0]) if len(s) else None, "unidades": int(s.unidades.iloc[0]) if len(s) else None}


res = {"rama": "v6/M1a", "mercado": "alquiler de stock (SERPAVI; IPC como robustez)",
       "pregunta": "Que variables se asocian con el alquiler de stock en provincia, municipio y distrito (regresores en t-1)?",
       "capa": "C4", "medida_precio": "SERPAVI mediana VC (EUR/m2/mes); distritos: punto medio p25-p75; IPC alquiler (robustez)",
       "datos": "output/v6/M0/paneles/{prov,mun,dis}_alquiler_anual_train.csv.gz + regresores de prov_compra_anual_train; "
                "solo entrenamiento (provincias <= 2023); centroides data/raw/v5",
       "N": {"provincia_S0": resumen("provincia"), "municipio_S0": resumen("municipio"), "distrito_S0": resumen("distrito")},
       "metodo": "TWFE (EF unidad y anio) con y sin tendencias; wild cluster bootstrap Webb y Rademacher B=%d por CCAA; Driscoll-Kraay; "
                 "Conley (distritos); CCEP/CCEMG, MG, SDM 2SLS, DML RF; exposicion tipo BHJ; event study + RR; Oster y Cinelli-Hazlett" % B,
       "estimacion": "ver tabla_coeficientes.csv y tabla_magnitudes_eur_mes.csv",
       "ic95": "IC t(G-1) con EE por clúster CCAA en tabla_coeficientes.csv (p = wild bootstrap)",
       "p_ajustado": "Holm en S0 de cada nivel; BH en el resto (tabla_coeficientes.csv)",
       "nivel_evidencia": "EXPLORATORIO / ASOCIACION ROBUSTA segun variable (columna nivel_evidencia); ninguna es CAUSAL",
       "diagnosticos": "diagnosticos.json", "fuera_muestra": FUERA,
       "contratos_nuevos": {"mercado": "contratos nuevos (fianzas)", "capa": "C4", "nivel_evidencia": "DESCRIPTIVO",
                            "nota": f"GVA {n_gva} obs y Incasol {n_inc} obs en provincia: sin potencia, descriptivo "
                                    "(contratos_descriptivo.csv); IPVA nuevo contrato TWFE exploratorio (N~100)"},
       "notas": "Predictores y asociaciones; sin lenguaje causal. Desviaciones: desviaciones.md. Cifras con fecha del dato 2023."}
json.dump(res, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False, default=float)
json.dump({"rama": "v6/M1a", "mercado": "contratos nuevos (fianzas)", "pregunta": "Evolucion de fianzas de contratos nuevos (descriptivo)",
           "capa": "C4", "datos": "prov_contratos_nuevos_anual_train", "N": {"gva": n_gva, "incasol": n_inc}, "metodo": "descriptivo",
           "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": None,
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Sin modelo: N sin potencia"},
          open(OUT / "resultado_contratos_nuevos.json", "w"), indent=1, ensure_ascii=False)
print("OK", len(R), "filas;", round(time.time() - t_start), "s")
