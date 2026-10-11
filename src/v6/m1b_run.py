"""M1b v6: econometría explicativa de la COMPRAVENTA y relación entre mercados. Solo paneles *_train de M0. Sin red.
SEED=20261010. `--smoke` reduce réplicas. Escribe en output/v6/M1B."""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v6"))
import econ_utils  # noqa: E402
import m1b_lib as L  # noqa: E402
from holdout import CCAA_PROV  # noqa: E402

SEED = 20261010
SMOKE = "--smoke" in sys.argv
B = 99 if SMOKE else 999
OUT = RAIZ / "output/v6/M1B" / ("smoke" if SMOKE else "")
(OUT / "tablas").mkdir(parents=True, exist_ok=True)
PAN = RAIZ / "output/v6/M0/paneles"
REG = econ_utils.Registry(OUT / "registro.csv")
FECHA = "2026-10-11"

CP = ["ln_pob", "share_ext_pob", "ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_terminadas_libres",
      "ln_iniciadas_libres", "ln_suelo_pm2_m50k", "ln_vut", "ln_hip_viv_num"]
CORE8 = [v for v in CP if v not in ("ln_suelo_pm2_m50k", "ln_vut")]
HOLM_VOL = ["ln_pib_pc", "ln_ocupados_miles", "ln_pob", "paro_tasa", "ln_terminadas_libres", "ln_iniciadas_libres"]
ROWS: list[dict] = []        # todas las especificaciones (para ajuste por multiplicidad)
EXTRA: dict = {}


def _conv(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def jd(o):
    return json.dumps(o, default=_conv)


def ccaa_of(c):
    return CCAA_PROV[str(int(c)).zfill(2)]


def reg(fase, mid, formula, n, coef, p, notas, r2=np.nan, fam="BH", var=None, mercado=None, nivel=None, medida=None):
    REG.log(fase, mid, formula, "", "", int(n), r2, np.nan, np.nan, coef_interes=coef, p_interes=p, notas=notas)
    ROWS.append(dict(idx=len(REG.rows) - 1, id=mid, fam=fam, p=p, var=var, mercado=mercado, nivel=nivel, medida=medida,
                     coef=coef))


def lag_panel(df, unit, per, cols, k=1):
    l_ = df[[unit, per] + cols].copy()
    l_[per] = l_[per] + k
    return l_


# ====================================================================== datos
def cargar():
    ca = pd.read_csv(PAN / "prov_compra_anual_train.csv.gz")
    ca["ccaa"] = ca.cod.map(ccaa_of)
    regs = sorted(set(CP + ["share_compra_ext_res_pct", "share_contado_proxy"]))
    lg = lag_panel(ca, "cod", "anio", regs)
    cal = ca[["cod", "anio", "provincia", "ccaa", "ln_pm2_tasado", "ln_pm2_registradores", "ln_cv_etdp",
              "ln_cv_registradores"]].merge(lg, on=["cod", "anio"], how="left")
    tr = pd.read_csv(PAN / "prov_trim_compra_train.csv.gz")
    tr["ccaa"] = tr.cod.map(ccaa_of)
    tr["q"] = tr.anio * 4 + tr.t.str[-1].astype(int) - 1
    nac = pd.read_csv(PAN / "nacional_trim_desc.csv")
    nac["q"] = nac.t.str[:4].astype(int) * 4 + nac.t.str[-1].astype(int) - 1
    nac["ln_cred_nuevas"] = np.log(nac.credito_viv_nuevas_mill_eur)
    mu = pd.read_csv(PAN / "mun_compra_anual_train.csv.gz")
    mu["cod_prov"] = mu.cod_prov.astype(int)
    mu["ccaa"] = mu.cod_prov.map(ccaa_of)
    al = pd.read_csv(PAN / "prov_alquiler_anual_train.csv.gz")
    al["ccaa"] = al.cod.map(ccaa_of)
    return ca, cal, tr, nac, mu, al


def efecto(var, b, y, mean_level):
    """Magnitud por unidad interpretable. Regresor en logs: +10 % en x; en pp: +1 pp. Devuelve (% y, abs)."""
    delta = math.log(1.1) if var.startswith("ln_") else 1.0
    pct = 100 * (math.exp(b * delta) - 1)
    return pct, mean_level * pct / 100


# ====================================================================== A1 efectos fijos
def a_fe(cal, ca):
    rows = []
    pm2 = float(np.exp(ca.ln_pm2_tasado).mean())
    cv = float(np.exp(ca.ln_cv_etdp).mean())
    specs = [
        ("S1_prereg_10", CP, "ute"), ("S2_nucleo8", CORE8, "ute"), ("S3_nucleo8+vut", CORE8 + ["ln_vut"], "ute"),
        ("S4_nucleo8+suelo", CORE8 + ["ln_suelo_pm2_m50k"], "ute"), ("S5_nucleo8_tendencias", CORE8, "utrend"),
    ]
    outs = [("ln_pm2_tasado", "valor tasado MIVAU", pm2, "€/m²"), ("ln_cv_etdp", "compraventas INE ETDP (volumen)", cv, "compraventas/año"),
            ("ln_pm2_registradores", "Registradores", pm2, "€/m²"), ("ln_cv_registradores", "Registradores (volumen)", cv, "compraventas/año")]
    for y, medida, lvl, uni in outs:
        for sid, xs, mode in specs:
            if y in ("ln_pm2_registradores", "ln_cv_registradores") and sid not in ("S2_nucleo8", "S5_nucleo8_tendencias"):
                continue
            d = cal.dropna(subset=[y] + xs)
            if d.cod.nunique() < 15 or len(d) < 60:
                continue
            f = L.fit_fe(d, y, xs, "cod", "anio", "ccaa", mode, B=B)
            dk = L.driscoll_kraay(d, y, xs, "cod", "anio") if mode == "ute" else None
            mercado = "precio" if "pm2" in y else "volumen"
            for j, v in enumerate(xs):
                pct, ab = efecto(v, f["coef"][j], y, lvl)
                os_ = L.oster_delta(f["yt"], f["X"], j, f["r2_within"]) if sid in ("S2_nucleo8", "S1_prereg_10") else {}
                ch = L.cinelli_hazlett(f["t"][j], f["df_res"]) if sid in ("S2_nucleo8", "S1_prereg_10") else {}
                fam = "BH"
                if sid == "S1_prereg_10" and y in ("ln_pm2_tasado", "ln_cv_etdp") and (y == "ln_pm2_tasado" or v in HOLM_VOL):
                    fam = "Holm"
                mid = f"A_fe_prov_anual|{sid}|{y}|{v}"
                nota = jd(dict(medida_precio=medida if mercado == "precio" else None, G=f["G"], p_cr1=round(f["p_cr1"][j], 4),
                                       p_dk=None if dk is None else round(float(dk.p.get(v, np.nan)), 4), efecto_pct=round(pct, 3),
                                       efecto_abs=round(ab, 2), unidad_abs=uni, oster=os_, ch=ch, modo=mode))
                reg("A_fe", mid, f"{y} ~ {v}(t-1)+... | FE {mode}", f["n"], f["coef"][j], f["p_wcb"][j], nota, f["r2_within"], fam,
                    v, mercado, "provincia anual", medida)
                rows.append(dict(spec=sid, y=y, medida=medida, var=v, coef=f["coef"][j], se_cr1=f["se"][j], p_wcb=f["p_wcb"][j],
                                 p_dk=None if dk is None else float(dk.p.get(v, np.nan)), efecto_pct_unidad=pct, efecto_abs=ab,
                                 unidad_abs=uni, n=f["n"], clusters=f["G"], r2_within=f["r2_within"],
                                 oster_delta=os_.get("delta"), RV_q1=ch.get("RV_q1"), RV_q1_a05=ch.get("RV_q1_alpha05")))
    t = pd.DataFrame(rows)
    EXTRA["fe_prov"] = t
    return t


def a_trimestral(tr, cal, nac):
    d = tr.merge(nac[["q", "tipo_hip_ecb_pct", "ln_cred_nuevas"]], on="q", how="left")
    lg = lag_panel(d, "cod", "q", ["ln_hip_viv_num", "ln_ipc_alq_idx"])
    d = d[["cod", "q", "anio", "ccaa", "ln_pm2_tasado", "ln_cv_etdp"]].merge(lg, on=["cod", "q"], how="left")
    an = cal[["cod", "anio", "ln_pib_pc", "paro_tasa", "ln_pob", "share_ext_pob"]]
    d = d.merge(an, on=["cod", "anio"], how="left")
    pm2 = float(np.exp(tr.ln_pm2_tasado).mean())
    cv = float(np.exp(tr.ln_cv_etdp).mean())
    rows = []
    for y, lvl, uni, med in (("ln_pm2_tasado", pm2, "€/m²", "valor tasado MIVAU"), ("ln_cv_etdp", cv, "compraventas/trimestre", "compraventas ETDP")):
        for sid, xs in (("T1_trim", ["ln_hip_viv_num", "ln_ipc_alq_idx"]),
                        ("T2_trim+anuales", ["ln_hip_viv_num", "ln_ipc_alq_idx", "ln_pib_pc", "paro_tasa", "ln_pob", "share_ext_pob"])):
            dd = d.dropna(subset=[y] + xs)
            f = L.fit_fe(dd, y, xs, "cod", "q", "ccaa", "ute", B=B)
            for j, v in enumerate(xs):
                pct, ab = efecto(v, f["coef"][j], y, lvl)
                reg("A_fe_trim", f"A_fe_prov_trim|{sid}|{y}|{v}", f"{y} ~ {v}(t-1) | FE unidad+trimestre", f["n"], f["coef"][j], f["p_wcb"][j],
                    jd(dict(medida_precio=med if "pm2" in y else None, efecto_pct=round(pct, 3), efecto_abs=round(ab, 2), unidad_abs=uni, G=f["G"])),
                    f["r2_within"], "BH", v, "precio" if "pm2" in y else "volumen", "provincia trimestral", med)
                rows.append(dict(spec=sid, y=y, var=v, coef=f["coef"][j], se_cr1=f["se"][j], p_wcb=f["p_wcb"][j], efecto_pct_unidad=pct,
                                 efecto_abs=ab, unidad_abs=uni, n=f["n"], clusters=f["G"]))
    EXTRA["fe_trim"] = pd.DataFrame(rows)
    return d


def a_municipal(mu, cal):
    lg = cal[["cod", "anio"] + CORE8].rename(columns={"cod": "cod_prov"})
    d = mu.merge(lg, on=["cod_prov", "anio"], how="left").dropna(subset=["ln_pm2_tasado_mun"] + CORE8)
    f = L.fit_fe(d, "ln_pm2_tasado_mun", CORE8, "cod_mun", "anio", "ccaa", "ute", B=B)
    pm2 = float(np.exp(mu.ln_pm2_tasado_mun).mean())
    rows = []
    for j, v in enumerate(CORE8):
        pct, ab = efecto(v, f["coef"][j], "", pm2)
        reg("A_fe_mun", f"A_fe_mun_anual|nucleo8|ln_pm2_tasado_mun|{v}", f"ln_pm2_tasado_mun ~ {v}(t-1) [regresor provincial] | FE municipio+año", f["n"],
            f["coef"][j], f["p_wcb"][j], jd(dict(medida_precio="valor tasado MIVAU municipal", efecto_pct=round(pct, 3), efecto_abs=round(ab, 2), G=f["G"],
                                                         municipios=int(d.cod_mun.nunique()))), f["r2_within"], "BH", v, "precio", "municipio", "valor tasado MIVAU municipal")
        rows.append(dict(var=v, coef=f["coef"][j], se_cr1=f["se"][j], p_wcb=f["p_wcb"][j], efecto_pct_unidad=pct, efecto_abs_eur_m2=ab, n=f["n"],
                         municipios=int(d.cod_mun.nunique()), clusters=f["G"]))
    EXTRA["fe_mun"] = pd.DataFrame(rows)


# ====================================================================== A2 CCE, MG
def a_cce_mg(cal, trd):
    rows = []
    a = cal.dropna(subset=["ln_pm2_tasado", "ln_cv_etdp", "ln_pib_pc", "paro_tasa", "ln_pob"]).copy()
    a["tt"] = a.anio
    q = trd.dropna(subset=["ln_pm2_tasado", "ln_cv_etdp", "ln_hip_viv_num", "ln_ipc_alq_idx"]).copy()
    q["tt"] = q.q
    for nivel, d, xs_mg, xs_cce in (("anual", a, ["ln_pib_pc", "paro_tasa", "ln_pob"], ["ln_pib_pc", "paro_tasa"]),
                                    ("trimestral", q, ["ln_hip_viv_num", "ln_ipc_alq_idx"], ["ln_hip_viv_num", "ln_ipc_alq_idx"])):
        for y in ("ln_pm2_tasado", "ln_cv_etdp"):
            med = "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP"
            for nm, r in (("MG", L.mg(d, y, xs_mg, "cod")), ("CCEMG", L.mg(d, y, xs_cce, "cod", extra_cs=(1,))), ("CCEP", L.ccep(d, y, xs_cce, "cod"))):
                xs = xs_mg if nm == "MG" else xs_cce
                for j, v in enumerate(xs):
                    reg("A_cce_mg", f"A_{nm}_prov_{nivel}|{y}|{v}", f"{y} ~ {v}(t-1) | {nm}", r.get("n", len(d)), r["coef"][j], r["p"][j],
                        jd(dict(medida_precio=med if "pm2" in y else None, N_unidades=r["N_unidades"], se=round(float(r["se"][j]), 5))),
                        np.nan, "BH", v, "precio" if "pm2" in y else "volumen", f"provincia {nivel}", med)
                    rows.append(dict(metodo=nm, nivel=nivel, y=y, var=v, coef=r["coef"][j], se=r["se"][j], p=r["p"][j], N_unidades=r["N_unidades"]))
    EXTRA["cce_mg"] = pd.DataFrame(rows)


# ====================================================================== A3 Durbin espacial
def a_sdm(cal, ca):
    cen = pd.read_csv(RAIZ / "data/raw/v5/municipio_centroides_utm30.csv", dtype={"codigo": str})
    cen["cod"] = cen.codigo.str[:2].astype(int)
    pc = cen.groupby("cod")[["x_m", "y_m"]].mean()
    xs = ["ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_pob", "ln_hip_viv_num"]
    rows = []
    for y in ("ln_pm2_tasado", "ln_cv_etdp"):
        d = cal.dropna(subset=[y] + xs)
        cnt = d.groupby("cod").anio.count()
        full = cnt[cnt == cnt.max()].index
        d = d[d.cod.isin(full) & d.cod.isin(pc.index)]
        provs = sorted(d.cod.unique())
        Wm = L.matriz_w(pc.loc[provs].to_numpy(), k=4)
        Yw = d.pivot(index="cod", columns="anio", values=y).loc[provs].to_numpy()
        Xw = [d.pivot(index="cod", columns="anio", values=v).loc[provs].to_numpy() for v in xs]
        r = L.sdm_fe(Yw, Xw, Wm, nsim=300 if SMOKE else 2000)
        lvl = float(np.exp(ca[y]).mean())
        for j, v in enumerate(xs):
            for tipo, key in (("directo", "direct"), ("indirecto", "indirect")):
                b = r[key][j]
                ci = r["dir_ci" if key == "direct" else "ind_ci"][:, j]
                p = r["dir_p" if key == "direct" else "ind_p"][j]
                pct, ab = efecto(v, b, y, lvl)
                reg("A_sdm", f"A_SDM_prov_anual|{y}|{v}|{tipo}", f"SDM W=4 vecinos (centroides) {y} ~ {v}(t-1)", r["N"] * r["T"], b, p,
                    jd(dict(rho=round(r["rho"], 4), ic95=[round(float(ci[0]), 4), round(float(ci[1]), 4)], efecto_pct=round(pct, 3), efecto_abs=round(ab, 2),
                                    medida_precio="valor tasado MIVAU" if "pm2" in y else None)), np.nan, "BH", v,
                    "precio" if "pm2" in y else "volumen", "provincia anual", "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP")
                rows.append(dict(y=y, var=v, tipo=tipo, coef=b, ic_lo=ci[0], ic_hi=ci[1], p_sim=p, efecto_pct_unidad=pct, efecto_abs=ab, rho=r["rho"],
                                 rho_se=r["rho_se"], N=r["N"], T=r["T"]))
    EXTRA["sdm"] = pd.DataFrame(rows)


# ====================================================================== A4 identificación
def a_ident(cal, ca, nac):
    rows = []
    # exposición base: apalancamiento hipotecario 2015-16 (hipotecas / compraventas)
    base = ca[ca.anio <= 2016].assign(lev=lambda x: np.exp(x.ln_hip_viv_num) / np.exp(x.ln_cv_etdp)).groupby("cod").lev.mean()
    E = (base - base.mean()) / base.std()
    nac["anio"] = nac.t.str[:4].astype(int)
    cred = nac.groupby("anio").credito_viv_nuevas_mill_eur.sum()
    dcred = np.log(cred).diff()
    tipo = nac.groupby("anio").tipo_hip_ecb_pct.mean().diff()
    d = cal.copy()
    d["E"] = d.cod.map(E)
    # balance: exposición frente a nivel y crecimiento pre-periodo del precio
    pre = ca[ca.anio <= 2019].pivot(index="cod", columns="anio", values="ln_pm2_tasado")
    gpre = (pre[2019] - pre[2016])
    bal = dict(corr_E_nivel2015=float(np.corrcoef(E.loc[pre.index], pre[2015].loc[E.index].reindex(pre.index))[0, 1]) if True else None,
               corr_E_crecimiento_2016_2019=float(np.corrcoef(E.loc[gpre.index], gpre)[0, 1]), n_prov=int(len(E)))
    EXTRA["ss_balance"] = bal
    for sname, S in (("credito_nuevo_dln", dcred), ("tipo_hipotecario_dpp", tipo)):
        for y in ("ln_pm2_tasado", "ln_cv_etdp"):
            for lab, shift in (("t-1", 1), ("placebo_lead_t+1", -1)):
                d["Z"] = d.E * d.anio.map(lambda a: S.get(a - shift, np.nan))
                dd = d.dropna(subset=[y, "Z"])
                dd = dd[dd.anio.between(2016, 2023)]
                f = L.fit_fe(dd, y, ["Z"], "cod", "anio", "ccaa", "ute", B=B)
                med = "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP"
                reg("A_ident", f"A_exposicion|{sname}|{y}|{lab}", f"{y} ~ E_apalancamiento_2015-16 x {sname}[{lab}] | FE unidad+año", f["n"], f["coef"][0],
                    f["p_wcb"][0], jd(dict(medida_precio=med if "pm2" in y else None, G=f["G"], nota="efecto DIFERENCIAL por exposición; el nivel común lo absorbe el FE de año")),
                    f["r2_within"], "BH", "Z_exposicion", "precio" if "pm2" in y else "volumen", "provincia anual", med)
                rows.append(dict(diseno="exposicion", shift=sname, y=y, tiempo=lab, coef=f["coef"][0], se=f["se"][0], p_wcb=f["p_wcb"][0], n=f["n"],
                                 clusters=f["G"], contraste="placebo" if "placebo" in lab else "principal"))
    # shift-share población extranjera con 2SLS
    base_sh = ca[ca.anio == 2015].set_index("cod").share_ext_pob
    x = ca.pivot(index="cod", columns="anio", values="share_ext_pob")
    dx = x.diff(axis=1)
    sumx = dx.sum()
    loo = (sumx - dx) / (len(dx) - 1)         # media de las demás provincias
    d2 = cal.copy()
    d2["Z"] = [base_sh[c] * loo.loc[c, a - 1] if (a - 1) in loo.columns else np.nan for c, a in zip(d2.cod, d2.anio)]
    ctrl = [v for v in CORE8 if v != "share_ext_pob"]
    for y in ("ln_pm2_tasado", "ln_cv_etdp"):
        dd = d2.dropna(subset=[y, "Z", "share_ext_pob"] + ctrl).reset_index(drop=True)
        u, t = L.codif(dd, "cod", "anio")
        M = L._dm2(dd[[y, "share_ext_pob", "Z"] + ctrl].to_numpy(float), u, t)
        yv, xv, zv, C = M[:, 0], M[:, 1], M[:, 2], M[:, 3:]
        b, se = L.iv2sls(yv, np.column_stack([xv, C]), np.column_stack([zv, C]), dd.ccaa)
        # primera etapa
        Zf = np.column_stack([zv, C])
        g1 = np.linalg.lstsq(Zf, xv, rcond=None)[0]
        e1 = xv - Zf @ g1
        n_, k_ = Zf.shape
        tz = g1[0] / math.sqrt((e1 @ e1) / (n_ - k_) * np.linalg.inv(Zf.T @ Zf)[0, 0])
        F = tz ** 2
        # pesos de Rotemberg por año: alpha_t proporcional a g_t * suma(share_p0 * x~_pt)
        w = {}
        for a in sorted(dd.anio.unique()):
            i = dd.anio.to_numpy() == a
            gt = float(loo[a - 1].mean()) if (a - 1) in loo.columns else 0
            w[int(a)] = gt * float((dd.cod[i].map(base_sh).to_numpy() * xv[i]).sum())
        tot = sum(w.values()) or 1
        rot = {k_: round(v_ / tot, 3) for k_, v_ in w.items()}
        p = 2 * stats.t.sf(abs(b[0] / se[0]), dd.ccaa.nunique() - 1)
        reg("A_ident", f"A_shiftshare_poblext|{y}", f"2SLS {y} ~ share_ext_pob(t-1) [Z = share_2015 x crec. resto de provincias] | FE", len(dd), b[0], p,
            jd(dict(F_primera_etapa=round(F, 2), rotemberg_por_anio=rot,
                            medida_precio="valor tasado MIVAU" if "pm2" in y else None,
                            lectura="instrumento débil" if F < 10 else "F>10; no demuestra exclusión")), np.nan, "BH", "share_ext_pob_IV",
            "precio" if "pm2" in y else "volumen", "provincia anual", "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP")
        rows.append(dict(diseno="shiftshare_poblacion_ext_2SLS", y=y, coef=b[0], se=se[0], p=p, F_1a_etapa=F, n=len(dd), rotemberg=jd(rot)))
    EXTRA["ident"] = pd.DataFrame(rows)


def a_dml(cal, ca):
    trat = ["ln_vut", "ln_pob", "ln_terminadas_libres", "ln_hip_viv_num", "share_compra_ext_res_pct", "share_contado_proxy"]
    ctrl_base = ["ln_pib_pc", "paro_tasa", "ln_ocupados_miles", "ln_iniciadas_libres", "share_ext_pob", "ln_pob", "ln_terminadas_libres", "ln_hip_viv_num"]
    rows = []
    for y in ("ln_pm2_tasado", "ln_cv_etdp"):
        for dname in trat:
            ctrl = [c for c in ctrl_base if c != dname]
            r = L.dml_plr(cal, y, dname, ctrl, "cod", "anio", "ccaa")
            lvl = float(np.exp(ca[y]).mean())
            pct, ab = efecto(dname, r["theta"], y, lvl)
            med = "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP"
            reg("A_dml", f"A_DML|{y}|{dname}", f"DML-PLR RF(200) FE-demeaned, pliegues por provincia: {y} ~ {dname}(t-1)", r["n"], r["theta"], r["p"],
                jd(dict(medida_precio=med if "pm2" in y else None, se=round(r["se"], 5), efecto_pct=round(pct, 3), efecto_abs=round(ab, 2), r2_y=round(r["r2_y"], 3),
                                r2_d=round(r["r2_d"], 3), G=r["G"])), np.nan, "BH", dname, "precio" if "pm2" in y else "volumen", "provincia anual", med)
            rows.append(dict(y=y, tratamiento=dname, theta=r["theta"], se=r["se"], p=r["p"], efecto_pct_unidad=pct, efecto_abs=ab, n=r["n"], r2_y=r["r2_y"], r2_d=r["r2_d"]))
    EXTRA["dml"] = pd.DataFrame(rows)


# ====================================================================== B1 ratio y coste de uso
def b_ratio(ca, al, nac):
    nac["anio"] = nac.t.str[:4].astype(int)
    tipo = nac.groupby("anio").tipo_hip_ecb_pct.mean()
    d = ca[["cod", "anio", "provincia", "ln_pm2_tasado", "ln_pm2_registradores"]].merge(
        al[["cod", "anio", "ln_alq_m2_serpavi_vc", "ccaa"]], on=["cod", "anio"]).dropna()
    d["ratio_anios"] = np.exp(d.ln_pm2_tasado - d.ln_alq_m2_serpavi_vc) / 12
    d["ratio_anios_registradores"] = np.exp(d.ln_pm2_registradores - d.ln_alq_m2_serpavi_vc) / 12
    d["rent_yield_bruta_pct"] = 100 / d.ratio_anios
    d["tipo_hip_pct"] = d.anio.map(tipo)
    # SUPUESTOS declarados: depreciación y mantenimiento 2,0 %; IBI y otros impuestos 0,5 %; ganancia esperada g (2 % principal, 0 y 4 % sensibilidad).
    for g in (0.0, 2.0, 4.0):
        d[f"coste_uso_pct_g{int(g)}"] = d.tipo_hip_pct + 2.0 + 0.5 - g
        d[f"brecha_pp_g{int(g)}"] = d.rent_yield_bruta_pct - d[f"coste_uso_pct_g{int(g)}"]
    d.to_csv(OUT / "tablas/b1_ratio_coste_uso_provincia_anio.csv", index=False)
    evo = d.groupby("anio").agg(ratio_mediana=("ratio_anios", "median"), ratio_p25=("ratio_anios", lambda x: x.quantile(.25)),
                                ratio_p75=("ratio_anios", lambda x: x.quantile(.75)), yield_mediana=("rent_yield_bruta_pct", "median"),
                                tipo_hip=("tipo_hip_pct", "first"), coste_uso_g2=("coste_uso_pct_g2", "first"),
                                brecha_mediana_g2=("brecha_pp_g2", "median"), n_prov=("cod", "nunique")).reset_index()
    evo.to_csv(OUT / "tablas/b1_evolucion_nacional_mediana.csv", index=False)
    ult = d[d.anio == d.anio.max()].sort_values("ratio_anios", ascending=False)
    ult[["cod", "provincia", "anio", "ratio_anios", "ratio_anios_registradores", "rent_yield_bruta_pct", "coste_uso_pct_g2", "brecha_pp_g2"]].to_csv(
        OUT / "tablas/b1_provincias_ultimo_anio.csv", index=False)
    EXTRA["ratio_evo"] = evo
    EXTRA["ratio_ult"] = ult
    EXTRA["ratio_d"] = d


# ====================================================================== B2 SUR / VAR de panel
def _ah(Y, Xl, Z):
    """2SLS equación a equación (Anderson-Hsiao). Devuelve matriz de coef (k×2) y residuos."""
    coefs, res = [], []
    for j in range(Y.shape[1]):
        PZ = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
        Xh = PZ @ Xl
        b = np.linalg.solve(Xh.T @ Xl, Xh.T @ Y[:, j])
        coefs.append(b)
        res.append(Y[:, j] - Xl @ b)
    return np.array(coefs).T, np.array(res).T


def _pvar(d, provs):
    """d con columnas cod, anio, p, r. Construye Δy_t, Δy_{t-1}, instrumentos y_{t-2}; demedia por año (FE de tiempo)."""
    d = d[d.cod.isin(provs)].sort_values(["cod", "anio"])
    g = d.groupby("cod")
    d = d.assign(dp=g.p.diff(), dr=g.r.diff())
    g = d.groupby("cod")
    d = d.assign(dp1=g.dp.shift(1), dr1=g.dr.shift(1), p2=g.p.shift(2), r2=g.r.shift(2)).dropna()
    for c in ("dp", "dr", "dp1", "dr1", "p2", "r2"):
        d[c] = d[c] - d.groupby("anio")[c].transform("mean")
    return d


def b_var(cal, ca, al):
    d = ca[["cod", "anio", "ln_pm2_tasado"]].merge(al[["cod", "anio", "ln_alq_m2_serpavi_vc", "ccaa"]], on=["cod", "anio"]).dropna()
    d = d.rename(columns={"ln_pm2_tasado": "p", "ln_alq_m2_serpavi_vc": "r"})
    provs = sorted(d.cod.unique())
    dd = _pvar(d, provs)
    Y = dd[["dp", "dr"]].to_numpy()
    Xl = dd[["dp1", "dr1"]].to_numpy()
    Z = dd[["p2", "r2", "dp1", "dr1"]].to_numpy()
    # instrumentos: niveles t-2 para las diferencias retardadas (Anderson-Hsiao); Z incluye lo exógeno (ninguno aquí) => usar solo p2,r2
    Z = dd[["p2", "r2"]].to_numpy()
    A, E = _ah(Y, Xl, Z)
    cov = E.T @ E / len(E)
    # SUR por FE (niveles within) con regresores distintos por ecuación
    from linearmodels.system import SUR
    m = cal[["cod", "anio", "ln_hip_viv_num", "ln_terminadas_libres", "ln_pib_pc", "ln_pob"]].merge(
        d[["cod", "anio", "p", "r"]], on=["cod", "anio"]).dropna()
    lg = lag_panel(d, "cod", "anio", ["p", "r"]).rename(columns={"p": "p1", "r": "r1"})
    m = m.merge(lg, on=["cod", "anio"]).dropna().reset_index(drop=True)
    cols = ["p", "r", "p1", "r1", "ln_hip_viv_num", "ln_terminadas_libres", "ln_pib_pc", "ln_pob"]
    u, t = L.codif(m, "cod", "anio")
    Mt = pd.DataFrame(L._dm2(m[cols].to_numpy(float), u, t), columns=cols)
    eqs = {"precio": dict(dependent=Mt.p, exog=Mt[["p1", "r1", "ln_hip_viv_num", "ln_terminadas_libres"]]),
           "alquiler": dict(dependent=Mt.r, exog=Mt[["p1", "r1", "ln_pib_pc", "ln_pob"]])}
    sur = SUR(eqs).fit(cov_type="robust")
    srows = []
    for nm in sur.params.index:
        srows.append(dict(parametro=nm, coef=sur.params[nm], se=sur.std_errors[nm], p=sur.pvalues[nm]))
        eq = nm.split("_")[0]
        reg("B_sur", f"B_SUR|{nm}", f"SUR within unidad+año (T={t.max() + 1}): {eq}", len(m), sur.params[nm], sur.pvalues[nm],
            jd(dict(medida_precio="valor tasado MIVAU", alquiler="SERPAVI stock (€/m²/mes VC)", correlacion_residuos=round(float(sur.resids.corr().iloc[0, 1]), 3))),
            np.nan, "BH", nm, "sistema", "provincia anual", "valor tasado MIVAU")
    EXTRA["sur"] = pd.DataFrame(srows)
    # PVAR-AH: coeficientes con IC por remuestreo de provincias (B réplicas), IRF Cholesky (precio->alquiler y alquiler->precio)
    H = 6
    rng = np.random.default_rng(SEED)

    def irf(A_, cov_, order):
        P = np.linalg.cholesky(cov_[np.ix_(order, order)])
        A_t = A_.T                           # filas ecuación: Δy_t = A_t Δy_{t-1}
        out = np.zeros((H + 1, 2, 2))
        Phi = np.eye(2)
        for h in range(H + 1):
            Pm = Phi[np.ix_(order, order)] @ P
            out[h] = Pm
            Phi = A_t @ Phi
        # acumulado: Δ -> niveles
        return np.cumsum(out, axis=0)
    base = {o: irf(A, cov, o) for o in ([0, 1], [1, 0])}
    boots = {o: [] for o in base}
    Bn = min(B, 499) if not SMOKE else 49
    byprov = {c: dd[dd.cod == c] for c in provs}
    for _ in range(Bn):
        pick = rng.choice(provs, size=len(provs), replace=True)
        bb = pd.concat([byprov[c] for c in pick])
        Ab, Eb = _ah(bb[["dp", "dr"]].to_numpy(), bb[["dp1", "dr1"]].to_numpy(), bb[["p2", "r2"]].to_numpy())
        cb = Eb.T @ Eb / len(Eb)
        try:
            for o in base:
                boots[o].append(irf(Ab, cb, o))
        except np.linalg.LinAlgError:
            continue
    pv = []
    for o in ([0, 1], [1, 0]):
        key = tuple(o)
        bs = np.array(boots[key]) if len(boots[key]) else None
        for h in range(H + 1):
            for resp, rn in ((0, "precio"), (1, "alquiler")):
                for shock, sn in ((0, "choque_precio"), (1, "choque_alquiler")):
                    # posición del choque en la ordenación: Pm[i, j] filas=variable en orden, columnas=choque en orden
                    ir = o.index(resp)
                    jc = o.index(shock)
                    v = base[key][h, ir, jc]
                    # el choque 'precio' o 'alquiler' tiene sentido para ambas ordenaciones; se guarda con IC
                    lo_, hi_ = (np.percentile(bs[:, h, ir, jc], [2.5, 97.5]) if bs is not None else (np.nan, np.nan))
                    pv.append(dict(orden="precio->alquiler" if o == [0, 1] else "alquiler->precio", h=h, respuesta=rn, choque=sn, irf=v, lo=lo_, hi=hi_))
    pvdf = pd.DataFrame(pv)
    pvdf.to_csv(OUT / "tablas/b2_pvar_irf_precio_alquiler.csv", index=False)
    coef = pd.DataFrame(A, index=["d_p(t-1)", "d_r(t-1)"], columns=["ec_precio", "ec_alquiler"])
    coef.to_csv(OUT / "tablas/b2_pvar_ah_coeficientes.csv")
    reg("B_pvar", "B_PVAR_AH|coef", "PVAR(1) en diferencias, Anderson-Hsiao, FE año", len(dd), float(A[1, 0]), np.nan,
        jd(dict(coef=A.tolist(), cov_resid=cov.tolist(), T_efectivo=int(dd.anio.nunique()), bootstrap=Bn,
                        nota="IRF recursivo (Cholesky) en ambos órdenes; no causal")), np.nan, "BH", "dr1->dp", "sistema", "provincia anual", "valor tasado MIVAU")
    EXTRA["pvar_irf"] = pvdf
    EXTRA["var_n"] = len(dd)


# ====================================================================== B3 capitalización y cointegración
def b_cap(ca, al, tr):
    from statsmodels.tsa.stattools import adfuller, coint
    d = ca[["cod", "anio", "ln_pm2_tasado", "ln_pm2_registradores"]].merge(al[["cod", "anio", "ln_alq_m2_serpavi_vc", "ccaa"]], on=["cod", "anio"]).dropna()
    rows = []
    for y, med in (("ln_pm2_tasado", "valor tasado MIVAU"), ("ln_pm2_registradores", "Registradores")):
        f = L.fit_fe(d, y, ["ln_alq_m2_serpavi_vc"], "cod", "anio", "ccaa", "ute", B=B)
        fu = L.fit_fe(d, y, ["ln_alq_m2_serpavi_vc"], "cod", "anio", "ccaa", "utrend", B=B)
        for nm, ff in (("FE_unidad+año", f), ("FE_unidad+tendencia", fu)):
            reg("B_cap", f"B_cap_anual|{nm}|{y}", f"{y} ~ ln alquiler SERPAVI (mismo año) | {nm}", ff["n"], ff["coef"][0], ff["p_wcb"][0],
                jd(dict(medida_precio=med, se=round(float(ff["se"][0]), 4), G=ff["G"], lectura="elasticidad precio-alquiler (log-log), asociación")),
                ff["r2_within"], "BH", "elasticidad_precio_alquiler", "relación", "provincia anual", med)
            rows.append(dict(nivel="anual", y=y, esp=nm, elasticidad=ff["coef"][0], se=ff["se"][0], p_wcb=ff["p_wcb"][0], n=ff["n"]))
    # trimestral: IPC alquiler (stock) y valor tasado; raíces unitarias, EG por provincia, DOLS agrupado
    q = tr.dropna(subset=["ln_pm2_tasado", "ln_ipc_alq_idx"]).sort_values(["cod", "q"])
    pu_p, pu_r, eg_p, ok = [], [], [], []
    for c, h in q.groupby("cod"):
        if len(h) < 36:
            continue
        pu_p.append(adfuller(h.ln_pm2_tasado, maxlag=4, regression="ct")[1])
        pu_r.append(adfuller(h.ln_ipc_alq_idx, maxlag=4, regression="ct")[1])
        eg_p.append(coint(h.ln_pm2_tasado, h.ln_ipc_alq_idx, trend="c", maxlag=4, autolag="aic")[1])
        ok.append(c)

    def fisher(ps):
        ps = np.clip(np.array(ps), 1e-12, 1)
        s = -2 * np.log(ps).sum()
        return float(s), float(stats.chi2.sf(s, 2 * len(ps)))
    uf = dict(precio=fisher(pu_p), alquiler=fisher(pu_r), engle_granger=fisher(eg_p))
    n_rej = int((np.array(eg_p) < 0.05).sum())
    # DOLS agrupado con 2 adelantos y 2 retardos de Δx
    g = q.copy()
    g["dx"] = g.groupby("cod").ln_ipc_alq_idx.diff()
    dl = []
    for k in range(-2, 3):
        g[f"dx{k}"] = g.groupby("cod").dx.shift(k)
        dl.append(f"dx{k}")
    gg = g.dropna(subset=["ln_pm2_tasado", "ln_ipc_alq_idx"] + dl)
    fd = L.fit_fe(gg, "ln_pm2_tasado", ["ln_ipc_alq_idx"] + dl, "cod", "q", "ccaa", "utrend", B=B)
    fd2 = L.fit_fe(gg, "ln_pm2_tasado", ["ln_ipc_alq_idx"] + dl, "cod", "q", "ccaa", "ute", B=B)
    # nota: con FE de tiempo el nivel común queda absorbido; la elasticidad sale de la variación entre provincias
    for nm, ff in (("DOLS_FE_unidad+tendencia", fd), ("DOLS_FE_unidad+trimestre(entre provincias)", fd2)):
        reg("B_cap", f"B_cap_trim|{nm}", f"ln tasado ~ ln IPC alquiler (stock) + Δ adelantos/retardos | {nm}", ff["n"], ff["coef"][0], ff["p_wcb"][0],
            jd(dict(medida_precio="valor tasado MIVAU", alquiler="IPC alquiler provincial (stock, índice)", se=round(float(ff["se"][0]), 4), G=ff["G"],
                            Fisher_precio_I1=uf["precio"], Fisher_alquiler_I1=uf["alquiler"], Fisher_EG=uf["engle_granger"], prov_rechazan_EG_5pct=n_rej, N_prov=len(ok),
                            nota="Fisher asume independencia entre provincias (hay dependencia): contraste indicativo; no es Pedroni/Westerlund")),
            ff["r2_within"], "BH", "elasticidad_largo_plazo", "relación", "provincia trimestral", "valor tasado MIVAU")
        rows.append(dict(nivel="trimestral", y="ln_pm2_tasado", esp=nm, elasticidad=ff["coef"][0], se=ff["se"][0], p_wcb=ff["p_wcb"][0], n=ff["n"]))
    t = pd.DataFrame(rows)
    EXTRA["cap"] = t
    EXTRA["coint"] = dict(fisher=uf, n_prov=len(ok), n_rej_5pct=n_rej)
    t.to_csv(OUT / "tablas/b3_capitalizacion_elasticidades.csv", index=False)


def b_lp(ca, tr, nac):
    """Proyecciones locales: respuesta diferencial por exposición (apalancamiento 2015-16) a Δ tipo hipotecario y Δ ln crédito nuevo."""
    base = ca[ca.anio <= 2016].assign(lev=lambda x: np.exp(x.ln_hip_viv_num) / np.exp(x.ln_cv_etdp)).groupby("cod").lev.mean()
    E = (base - base.mean()) / base.std()
    nac = nac.sort_values("q").assign(dtipo=lambda x: x.tipo_hip_ecb_pct.diff(), dcred=lambda x: x.ln_cred_nuevas.diff())
    d = tr.sort_values(["cod", "q"]).copy()
    d["E"] = d.cod.map(E)
    d = d.dropna(subset=["E"])
    Hm = 8 if not SMOKE else 4
    rows = []
    for sname in ("dtipo", "dcred"):
        sh = nac.set_index("q")[sname]
        d["Z"] = d.E * d.q.map(sh)
        for y, med, mer in (("ln_pm2_tasado", "valor tasado MIVAU", "precio"), ("ln_ipc_alq_idx", "IPC alquiler (stock)", "alquiler"), ("ln_cv_etdp", "compraventas ETDP", "volumen")):
            g = d.groupby("cod")[y]
            for h in range(Hm + 1):
                d["Yh"] = g.shift(-h) - g.shift(1)
                d["c1"] = g.diff(1).groupby(d.cod).shift(1)
                d["c2"] = g.diff(1).groupby(d.cod).shift(2)
                dd = d.dropna(subset=["Yh", "Z", "c1", "c2"])
                dd = dd[dd.anio >= 2016]
                f = L.fit_fe(dd, "Yh", ["Z", "c1", "c2"], "cod", "q", "ccaa", "ute", B=B)
                rows.append(dict(choque=sname, y=y, mercado=mer, medida=med, h=h, coef=f["coef"][0], se=f["se"][0], p_wcb=f["p_wcb"][0], n=f["n"]))
                reg("B_lp", f"B_LP|{sname}|{y}|h{h}", f"Δ_{h + 1} {y} ~ E x {sname} | FE unidad+trimestre", f["n"], f["coef"][0], f["p_wcb"][0],
                    jd(dict(medida_precio=med if mer == "precio" else None, alquiler=med if mer == "alquiler" else None, h=h, G=f["G"],
                                    identificacion="respuesta DIFERENCIAL por exposición; choque nacional común absorbido por FE de trimestre; el tipo hipotecario no es exógeno al mercado")),
                    f["r2_within"], "BH", f"{sname}xE", mer, "provincia trimestral", med)
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "tablas/b3_proyecciones_locales_exposicion.csv", index=False)
    EXTRA["lp"] = t
    # LP nacional (media de provincias), HAC; descriptivo
    import statsmodels.api as sm
    nrows = []
    mq = tr.groupby("q")[["ln_pm2_tasado", "ln_ipc_alq_idx", "ln_cv_etdp"]].mean()
    mq = mq.join(nac.set_index("q")[["dtipo", "dcred"]])
    for sname in ("dtipo", "dcred"):
        for y in ("ln_pm2_tasado", "ln_ipc_alq_idx", "ln_cv_etdp"):
            for h in range(Hm + 1):
                z = pd.DataFrame({"Yh": mq[y].shift(-h) - mq[y].shift(1), "s": mq[sname], "c1": mq[y].diff().shift(1), "c2": mq[y].diff().shift(2)}).dropna()
                if len(z) < 15:
                    continue
                r = sm.OLS(z.Yh, sm.add_constant(z[["s", "c1", "c2"]])).fit(cov_type="HAC", cov_kwds={"maxlags": h + 1})
                nrows.append(dict(choque=sname, y=y, h=h, coef=r.params["s"], se=r.bse["s"], p=r.pvalues["s"], n=len(z)))
                reg("B_lp_nac", f"B_LPnac|{sname}|{y}|h{h}", f"Δ_{h + 1} {y} (media provincias) ~ {sname} | HAC", len(z), r.params["s"], r.pvalues["s"],
                    jd(dict(nota="serie nacional 2015-2024, N<=40; descriptivo C4")), r.rsquared_adj, "BH", sname, "relación", "nacional trimestral", "valor tasado MIVAU")
    pd.DataFrame(nrows).to_csv(OUT / "tablas/b3_proyecciones_locales_nacional.csv", index=False)
    EXTRA["lp_nac"] = pd.DataFrame(nrows)


# ====================================================================== B4 GSADF
def b_gsadf(tr):
    q = tr.dropna(subset=["ln_pm2_tasado", "ln_ipc_alq_idx"]).copy()
    q["ln_ratio"] = q.ln_pm2_tasado - q.ln_ipc_alq_idx
    # ratio de índices (precio €/m² / IPC alquiler stock): el nivel no tiene unidad económica; solo importa su dinámica
    rows = []
    nb = 49 if SMOKE else 499
    for i, (cc, h) in enumerate(q.groupby("ccaa")):
        s = h.groupby("q").ln_ratio.mean()
        n_prov = h.cod.nunique()
        if len(s) < 36:
            continue
        r = L.gsadf_corr(s.to_numpy(), nb, SEED + i)
        eps = [f"{(s.index[a] // 4)}T{s.index[a] % 4 + 1}-{(s.index[b] // 4)}T{s.index[b] % 4 + 1}" for a, b in r["eps"]]
        rows.append(dict(ccaa=cc, n_prov_train=n_prov, T=r["T"], gsadf=r["gsadf"], cv95=r["cv95"], p_boot=r["p"], ar_p=r["ar_p"], episodios=";".join(eps)))
    t = pd.DataFrame(rows)
    t["p_BH"] = L.bh(t.p_boot.to_numpy())
    t.to_csv(OUT / "tablas/b4_gsadf_ratio_precio_alquiler_ccaa.csv", index=False)
    for _, r in t.iterrows():
        reg("B_gsadf", f"B_GSADF|CCAA{r.ccaa}", "GSADF bootstrap AR(p) sobre ln(precio tasado / IPC alquiler) trimestral 2015-2024", r["T"], r.gsadf, r.p_boot,
            jd(dict(cv95=round(r.cv95, 3), episodios=r.episodios, medida_precio="valor tasado MIVAU", capa="C4", nota="señal de desalineación, no burbuja")),
            np.nan, "BH", "GSADF", "relación", "CCAA trimestral", "valor tasado MIVAU")
    # tamaño Monte Carlo T=40
    R = 30 if SMOKE else 200
    rng = np.random.default_rng(SEED + 9)
    out = {}
    for phi in (0.0, 0.5):
        rej = 0
        for r_ in range(R):
            e = rng.standard_normal(40)
            dy = np.zeros(40)
            for k in range(1, 40):
                dy[k] = phi * dy[k - 1] + e[k]
            rej += L.gsadf_corr(np.cumsum(dy), 49 if SMOKE else 99, SEED + 1000 + r_)["p"] <= 0.05
        out[f"phi{phi}"] = rej / R
    EXTRA["gsadf_tamano"] = dict(T=40, R=R, nboot_interno=49 if SMOKE else 99, **out)
    EXTRA["gsadf"] = t


# ====================================================================== OOS
def oos(tr, nac):
    d = tr.merge(nac[["q", "tipo_hip_ecb_pct", "ln_cred_nuevas"]], on="q", how="left").sort_values(["cod", "q"]).reset_index(drop=True)
    rows, preds = [], []
    for y in ("ln_pm2_tasado", "ln_cv_etdp"):
        g = d.groupby("cod")
        D = pd.DataFrame({"cod": d.cod, "q": d.q, "y": d[y]})
        for k in range(1, 5):
            D[f"y{k}"] = g[y].shift(k)
        D["dy"] = D.y - D.y1
        D["dy1"] = D.y1 - D.y2
        xcols = {}
        for v in ("ln_hip_viv_num", "ln_ipc_alq_idx", "tipo_hip_ecb_pct", "ln_cred_nuevas"):
            D[v] = d[v]
        for v in ("ln_hip_viv_num", "ln_ipc_alq_idx", "tipo_hip_ecb_pct", "ln_cred_nuevas"):
            gg = D.groupby("cod")[v]
            D[v + "_l1"] = gg.shift(1)
            D["d_" + v + "_l1"] = gg.shift(1) - gg.shift(2)
        X1 = ["ln_hip_viv_num_l1", "ln_ipc_alq_idx_l1", "tipo_hip_ecb_pct_l1", "ln_cred_nuevas_l1"]
        dX = ["d_" + v for v in X1]
        D = D.dropna().reset_index(drop=True)
        mods = {
            "AR4": (["y1", "y2", "y3", "y4"], "y"),
            "ECMv1": (["y1"] + X1 + ["dy1"] + dX, "dy"),
            "M1b_ADL": (["y1", "y2", "y3", "y4"] + X1, "y"),
        }
        errs = {m: [] for m in mods}
        qs = []
        for orig in (2018 * 4, 2020 * 4, 2022 * 4):
            trn = D[D.q < orig - 4]
            val = D[(D.q >= orig) & (D.q < orig + 8)]
            for m, (xs, tgt) in mods.items():
                A = trn[xs + [tgt]].to_numpy(float)
                u = pd.factorize(trn.cod)[0]
                Mt = L._dm2(A, u, np.zeros(len(u), int))   # solo media de unidad
                Mt = A - pd.DataFrame(A).groupby(u).transform("mean").to_numpy()
                b = np.linalg.lstsq(Mt[:, :-1], Mt[:, -1], rcond=None)[0]
                mu = trn.groupby("cod")[xs + [tgt]].mean()
                a_i = mu[tgt] - mu[xs].to_numpy() @ b
                a_v = val.cod.map(a_i).to_numpy()
                pr = a_v + val[xs].to_numpy() @ b
                yh = pr + val.y1.to_numpy() if tgt == "dy" else pr
                errs[m].append(val.y.to_numpy() - yh)
            qs.append(val[["cod", "q"]].assign(fold=orig // 4))
        qq = pd.concat(qs).reset_index(drop=True)
        E = {m: np.concatenate(v) for m, v in errs.items()}
        # pérdida agregada por trimestre (media entre provincias) -> series de DM
        agg = {m: pd.Series(E[m] ** 2).groupby([qq.fold.to_numpy(), qq.q.to_numpy()]).mean() for m in E}
        lvl = float(np.exp(D.y).mean())
        for m in E:
            rm = float(np.sqrt((E[m] ** 2).mean()))
            row = dict(y=y, modelo=m, rmse_ln=rm, rmse_pct=100 * (math.exp(rm) - 1), rmse_abs=lvl * rm, n_val=len(E[m]), n_train_min=int((D.q < 2018 * 4 - 4).sum()))
            for ref in ("AR4", "ECMv1"):
                if m == ref:
                    continue
                dm = econ_utils.dm_test(np.sqrt(agg[m].to_numpy()), np.sqrt(agg[ref].to_numpy()), h=1)
                row[f"dm_vs_{ref}"] = dm["DM"]
                row[f"p_dm_vs_{ref}"] = dm["p"]
            rows.append(row)
            reg("OOS", f"OOS|{y}|{m}", f"{m} bloques con embargo 4 trimestres, origen 2018/2020/2022, h=1", row["n_val"], rm,
                row.get("p_dm_vs_AR4", np.nan), jd({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}), np.nan, "BH", m,
                "precio" if "pm2" in y else "volumen", "provincia trimestral", "valor tasado MIVAU" if "pm2" in y else "compraventas ETDP")
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "tablas/oos_trimestral_dm_hln.csv", index=False)
    EXTRA["oos"] = t


# ====================================================================== multiplicidad y volcado
def multiplicidad():
    df = pd.DataFrame(ROWS)
    df["p_adj"] = np.nan
    df["metodo_adj"] = ""
    h = df[(df.fam == "Holm") & df.p.notna()]
    if len(h):
        adj = econ_utils.holm({i: p for i, p in zip(h.index, h.p)})
        for i, v in adj.items():
            df.loc[i, "p_adj"], df.loc[i, "metodo_adj"] = v, "Holm (familia confirmatoria M1b: 10 precio + 6 volumen)"
    r = df[(df.fam == "BH") & df.p.notna()]
    if len(r):
        a = L.bh(r.p.to_numpy())
        df.loc[r.index, "p_adj"] = a
        df.loc[r.index, "metodo_adj"] = "BH (q=0,10) sobre todo lo no confirmatorio"
    for _, rw in df.iterrows():
        REG.rows[int(rw.idx)][-1] += f" | p_ajustado={rw.p_adj:.4g} [{rw.metodo_adj}]" if pd.notna(rw.p_adj) else " | p_ajustado=NA"
    df.to_csv(OUT / "tablas/multiplicidad_p_ajustados.csv", index=False)
    return df


def main():
    ca, cal, tr, nac, mu, al = cargar()
    a_fe(cal, ca)
    trd = a_trimestral(tr, cal, nac)
    a_municipal(mu, cal)
    a_cce_mg(cal, trd)
    a_sdm(cal, ca)
    a_ident(cal, ca, nac)
    a_dml(cal, ca)
    b_ratio(ca, al, nac)
    b_var(cal, ca, al)
    b_cap(ca, al, tr)
    b_lp(ca, tr, nac)
    b_gsadf(tr)
    oos(tr, nac)
    df = multiplicidad()
    for k, v in EXTRA.items():
        if isinstance(v, pd.DataFrame):
            v.to_csv(OUT / f"tablas/{k}.csv", index=False)
    REG.flush()
    import m1b_salidas
    m1b_salidas.escribir(OUT, EXTRA, df, SMOKE, B)


if __name__ == "__main__":
    main()
