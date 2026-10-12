"""V7-R6: propuestas e impacto regional por traslado (incidencia). Capa C4: los parametros son supuestos.
Determinista, sin red, SEED=20261010. Uso: python3 src/v7/r6_propuestas.py [--smoke]
Cruces por codigo INE (CCAA 2 digitos como texto; provincia = 2 primeros digitos del codigo municipal).
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.multitest import multipletests
from statsmodels.tsa.stattools import coint

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
SMOKE = "--smoke" in sys.argv
NMC = 400 if SMOKE else 4000
OUT = ROOT / "output" / "v7" / ("R6_smoke" if SMOKE else "R6")
FECHA = "2026-10-12"
HOR = (2, 5, 10)
UMBRAL = -0.1   # materialidad: variacion del esfuerzo en % (declarada)
GRID_ES = {1: 1.75, 2: 0.0, 3: 0.45}
ED_LO, ED_HI = 0.3, 1.5
M2 = 90.0   # m2 por vivienda en el coste fiscal (supuesto)
PROV2CCAA = {}
for _c, _ps in {"01": "04 11 14 18 21 23 29 41", "02": "22 44 50", "03": "33", "04": "07", "05": "35 38", "06": "39",
                "07": "05 09 24 34 37 40 42 47 49", "08": "02 13 16 19 45", "09": "08 17 25 43", "10": "03 12 46",
                "11": "06 10", "12": "15 27 32 36", "13": "28", "14": "30", "15": "31", "16": "01 20 48", "17": "26"}.items():
    for _p in _ps.split():
        PROV2CCAA[_p] = _c
NOMBRE = {}


def leer_panel() -> pd.DataFrame:
    d = pd.read_csv(ROOT / "data/processed/v7/panel_ccaa_q_v7.csv")
    d["cc"] = d.codigo_ine_ccaa.astype(int).map("{:02d}".format)
    for c, n in d.groupby("cc").ccaa.first().items():
        NOMBRE[c] = n
    d["anio"] = d.trimestre.str[:4].astype(int)
    h = pd.read_csv(ROOT / "data/raw/eu_hicp.csv")
    h = h[h.serie.str.endswith("CP00|ES")].set_index("periodo")
    idx = {int(str(k)[:4]): v for k, v in h.valor.items()}
    idx[2026] = idx[2025]
    d["hicp"] = d.anio.map(idx)
    d["ln_ipv_real"] = np.log(d.ipv / d.hicp)
    d["ln_vis"] = np.log(d.visados.where(d.visados > 0))
    return d


def dols(g: pd.DataFrame, k: int = 2):
    """DOLS +-k: ln visados sobre ln precio real, con adelantos y retardos de d ln precio. HAC (Newey-West, 4)."""
    g = g.sort_values("trimestre").reset_index(drop=True)
    x = g.ln_ipv_real
    X = pd.DataFrame({"x": x})
    for j in range(-k, k + 1):
        X[f"dx{j}"] = x.diff().shift(-j)
    X = sm.add_constant(X)
    ok = X.notna().all(axis=1) & g.ln_vis.notna()
    m = sm.OLS(g.ln_vis[ok], X[ok]).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    b, se = float(m.params["x"]), float(m.bse["x"])
    p_c = float(coint(g.ln_vis[ok], x[ok], trend="c")[1])
    return b, se, float(m.pvalues["x"]), p_c, int(ok.sum()), m


def elasticidades_regionales(d: pd.DataFrame, reg: Registry) -> pd.DataFrame:
    f = []
    for cc, g in d[(d.anio >= 2008) & (d.anio <= 2025)].groupby("cc"):
        b, se, p, pc, n, m = dols(g)
        p_lb = float(acorr_ljungbox(m.resid, lags=[4])["lb_pvalue"].iloc[0])
        lo, hi = b - 1.96 * se, b + 1.96 * se
        f.append(dict(cc=cc, ccaa=NOMBRE[cc], n=n, es_dols=b, ee=se, ic95_lo=lo, ic95_hi=hi, p=p, p_coint_EG=pc, p_ljungbox4=p_lb,
                      ic_en_0_5=bool(lo >= 0 and hi <= 5), diag_ok=bool(pc < 0.10 and p_lb > 0.05)))
        reg.log("R6-es", f"DOLS2_{cc}", "ln(visados)~ln(ipv/HICP)+dln(ipv)[-2..2]", "2008Q1", "2025Q4", n, np.nan, np.nan, np.nan,
                coef_interes=b, p_interes=p, notas=f"IC95=[{lo:.2f};{hi:.2f}]; p_coint={pc:.3f}; C4")
    e = pd.DataFrame(f)
    e["p_BH"] = multipletests(e.p, method="fdr_bh")[1]
    e["p_Holm"] = multipletests(e.p, method="holm")[1]
    e["usable"] = e.ic_en_0_5 & e.diag_ok
    mg = e.es_dols.mean()
    mg_se = e.es_dols.std(ddof=1) / np.sqrt(len(e))
    reg.log("R6-es", "MG_DOLS2", "media de DOLS2 por CCAA", "2008Q1", "2025Q4", int(e.n.sum()), np.nan, np.nan, np.nan,
            coef_interes=mg, p_interes=float(2 * (1 - stats.t.cdf(abs(mg / mg_se), len(e) - 1))), notas=f"MG se={mg_se:.2f}; insumo")
    e.attrs["mg"] = (mg, mg_se)
    return e


def rejilla_a4() -> pd.DataFrame:
    a = pd.read_csv(ROOT / "output/v5/A4/clasificacion_provincias.csv", dtype={"cod_prov": str})
    a["cc"] = a.cod_prov.map(PROV2CCAA)
    a = a[a.cc.notna()].copy()
    cl = {}
    for k, g in a.groupby("clase_2021_2025"):   # metodo A de v5 D1 (es_por_clase)
        r = g.resp_oferta.clip(lower=0)
        cl[int(k)] = (float(r.quantile(.25)), float(r.quantile(.75)))
    lo, hi = [], []
    for k in a.clase_2021_2025:
        k = int(k)
        if k == 9:
            lo.append(0.0), hi.append(1.75)
        else:
            lo.append(min(cl[k][0], GRID_ES[k])), hi.append(max(cl[k][1], GRID_ES[k]))
    a["es_lo"], a["es_hi"] = lo, hi
    a["w"] = a.deficit_2021_2025_mediana.clip(lower=0).fillna(0) + 1e-9
    f = []
    for cc, g in a.groupby("cc"):
        w = g.w / g.w.sum()
        modal = g.groupby("clase_2021_2025").w.sum().idxmax()
        cuenta = g.clase_2021_2025.value_counts().to_dict()
        f.append(dict(cc=cc, clase_modal=int(modal), n_prov=len(g), provincias_por_clase=json.dumps({int(k): int(v) for k, v in cuenta.items()}),
                      cods_prov=" ".join(sorted(g.cod_prov)), rej_lo=float((w * g.es_lo).sum()), rej_hi=float((w * g.es_hi).sum())))
    return pd.DataFrame(f)


def base_regional(d: pd.DataFrame) -> pd.DataFrame:
    r = pd.read_csv(ROOT / "output/v5/R1C/vacias_esporadicas_municipio_censo2021.csv")
    r["cc"] = r.terr.str[:2].map(PROV2CCAA)
    parque = r.groupby("cc").totales.sum()
    t = pd.read_csv(ROOT / "output/v5_1/T3/tablas/necesidad_provincial.csv", dtype={"cod_prov": str})
    t["cc"] = t.cod_prov.map(PROV2CCAA)
    t = t[t.cc.notna()]
    tc = t.groupby("cc")[["N_anual_central", "M_min", "M_central", "M_max"]].sum()
    out = pd.DataFrame({"parque": parque}).join(tc)
    out["N_anual_central"] = out.N_anual_central.clip(lower=0)
    last = d[d.trimestre == "2025Q4"].set_index("cc")
    out["vut"] = last.vut_viviendas
    an = d[(d.anio >= 2016) & (d.anio <= 2025)].groupby(["cc", "anio"]).visados.sum().unstack()
    out["vis_2025"] = an[2025]
    out["vis_max_2016_25"] = an.max(axis=1)
    cv = d[(d.anio == 2025)].groupby("cc").compraventas.sum()
    pt = d[d.trimestre == "2025Q4"].set_index("cc").p_tasado
    out["valor_compras_meur"] = cv * M2 * pt / 1e6
    return out


def sendas(rng, n):
    sv_a, sv_b = SV
    sv = np.exp(rng.uniform(np.log(sv_a), np.log(sv_b), n))
    return {h: 1 - 0.5 ** (4 * h / sv) for h in HOR}


def simular(cc, b, rej, esreg, rng, fuente):
    """Devuelve filas (instrumento, mercado, horizonte) con mediana, p5, p95, coste y vector de esfuerzo (para robustez)."""
    n = NMC
    ed = rng.uniform(ED_LO, ED_HI, n)
    if fuente == "rejilla":
        es = rng.uniform(rej.rej_lo, max(rej.rej_hi, rej.rej_lo + 1e-9), n)
    else:
        es = np.clip(rng.normal(esreg.es_dols, esreg.ee, n), 0, 5)
    adj = sendas(rng, n)
    Q = b.parque
    alq = rng.uniform(0.15, 0.20, n) * Q   # parque en alquiler (supuesto; 15-20 %)
    ahorro = {}
    inc = ed / (es + ed)
    # --- ofertas: dQ anual (viviendas/ano), fase de llegada y destino a alquiler
    cap = max(b.vis_max_2016_25 - b.vis_2025, 0.0)
    a_anual = min(b.N_anual_central, cap) * rng.uniform(0.5, 1.0, n)
    b_anual = rng.triangular(b.M_min, b.M_central, b.M_max, n) / 10 if b.M_max > 0 else np.zeros(n)
    c_anual = 0.2 * b.N_anual_central * rng.uniform(0.5, 1.5, n) * (1 - rng.uniform(0, 0.5, n))   # 10-30 % de la necesidad anual, con desplazamiento 0-50 %
    d_unico = b.vut * rng.uniform(0.05, 0.30, n)
    ofer = {"a_construccion": (a_anual, "anual", rng.uniform(0.1, 0.3, n)), "b_vacias": (b_anual, "anual", rng.uniform(0.3, 0.7, n)),
            "c_vivienda_publica": (c_anual, "anual", rng.uniform(0.8, 1.0, n)), "d_turisticos": (d_unico, "unico", np.ones(n))}
    filas, vec = [], {}
    for inst, (dq, modo, om) in ofer.items():
        for mer in ("precio", "alquiler"):
            for h in HOR:
                acum = dq * (max(h - 1, 0) if modo == "anual" else 1.0)   # llegada tras 1 ano de obra/tramite
                base = Q if mer == "precio" else alq
                frac = acum * (1.0 if mer == "precio" else om) / base
                dp = -100 * frac / (es + ed) * adj[h]
                vec[(inst, mer, h)] = (dp, dp, np.nan)
    # --- demanda: subvencion o rebaja fiscal s (% del precio pagado); coste sobre valor de compra
    s_ay = rng.uniform(0.05, 0.15, n)
    s_itp = rng.uniform(0.01, 0.04, n)
    for inst, s, mers in (("e_ayuda_demanda", s_ay, ("precio", "alquiler")), ("f1_rebaja_ITP_IVA_vivienda_nueva", s_itp, ("precio",))):
        for mer in mers:
            for h in HOR:
                dp = 100 * s * inc * adj[h]
                esf = 100 * ((1 + dp / 100) * (1 - s * adj[h]) - 1)   # esfuerzo = precio neto pagado/renta, renta constante
                coste = s * b.valor_compras_meur if mer == "precio" else np.full(n, np.nan)
                vec[(inst, mer, h)] = (dp, esf, coste)
    # --- coste: rebaja c del coste de construccion (impuestos), cuota de coste en el precio 40-70 %
    c_red = rng.uniform(0.02, 0.06, n)
    cuota = rng.uniform(0.4, 0.7, n)
    for mer in ("precio", "alquiler"):
        for h in HOR:
            dp = -100 * c_red * cuota * es / (es + ed) * adj[h]
            vec[("f2_impuestos_construccion", mer, h)] = (dp, dp, np.full(n, np.nan))
    for (inst, mer, h), v in vec.items():
        if len(v) == 3:
            dp, esf, coste = v
        else:
            dp = esf = v[0]
            coste = np.full(n, np.nan)
        filas.append(dict(cc=cc, instrumento=inst, mercado=mer, horizonte=h, fuente_es=fuente,
                          dprecio_med=np.median(dp), dprecio_p5=np.percentile(dp, 5), dprecio_p95=np.percentile(dp, 95),
                          esfuerzo_med=np.median(esf), esfuerzo_p5=np.percentile(esf, 5), esfuerzo_p95=np.percentile(esf, 95),
                          esfuerzo_max=float(np.max(esf)),
                          coste_meur_med=float(np.nanmedian(coste)) if np.isfinite(coste).any() else np.nan,
                          coste_meur_p5=float(np.nanpercentile(coste, 5)) if np.isfinite(coste).any() else np.nan,
                          coste_meur_p95=float(np.nanpercentile(coste, 95)) if np.isfinite(coste).any() else np.nan,
                          coste_por_eur_reduccion=float(np.nanmedian(coste / (-esf / 100 * b.valor_compras_meur))) if np.isfinite(coste).any() and np.median(esf) < 0 else np.nan))
    return filas


SV = (6.6, 24.8)


def semivida_r4():
    xs = {}
    for m in ("alquiler", "compra"):
        v = pd.read_csv(ROOT / f"output/v7/R4/{m}/velocidad_ajuste_region.csv", dtype={"codigo_ine_ccaa": str})
        for (sp, rz), g in v.groupby(["spec", "rezago"]):
            xs.setdefault(sp, []).append(g.semivida_trim.dropna())
    a = float(pd.concat(xs["A"]).median())
    b = float(pd.concat(xs["B"]).median())
    return min(a, b), max(a, b)


METODO = r"""# V7-R6 · Método de traslado (incidencia) y escenarios. Capa C4 (los parámetros son supuestos)

Todo el texto es condicional: «si se hiciera X, con estos supuestos…». No se afirma causalidad (C4). Se evalúan instrumentos, no actores.

## Ecuaciones (equilibrio parcial, mercado local)

Demanda con elasticidad $\varepsilon_d<0$ y oferta con elasticidad $\varepsilon_s\ge 0$ (respecto del precio).

1. Incidencia de una ayuda a la demanda sobre el precio (parte que capta el vendedor):
$$\iota=\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}\in(0,1]$$
2. Variación del precio ante una ayuda de demanda de intensidad $s$ (fracción del precio pagado), con ajuste completo:
$$\frac{\Delta p}{p}=s\,\iota=s\,\frac{|\varepsilon_d|}{\varepsilon_s+|\varepsilon_d|}$$
   Precio neto pagado por el comprador: $\frac{\Delta p^{n}}{p}\approx -s\,(1-\iota)=-s\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$. Con $\varepsilon_s=0$ el precio absorbe toda la ayuda y el esfuerzo no varía.
3. Variación del precio ante un aumento de oferta $\Delta Q/Q$:
$$\frac{\Delta p}{p}=-\frac{\Delta Q/Q}{\varepsilon_s+|\varepsilon_d|}$$
4. Rebaja de un impuesto al coste de construcción $c$ (cuota $\kappa$ del coste en el precio), desplazamiento de la oferta:
$$\frac{\Delta p}{p}=-c\,\kappa\,\frac{\varepsilon_s}{\varepsilon_s+|\varepsilon_d|}$$
5. Senda de ajuste a horizonte $h$ años, con semivida $\tau$ (trimestres): $A(h)=1-2^{-4h/\tau}$, de modo que el efecto es el de las ecuaciones 2-4 multiplicado por $A(h)$.
6. Esfuerzo (compra) = precio neto pagado / renta, con la renta constante: su variación porcentual es la del precio neto. Para el alquiler, la variación de la renta.
7. Coste por euro: $\text{coste}/(\text{reducción del precio neto}\times\text{valor anual de compras})$, que en demanda es $1/(1-\iota)$ en el límite.

## Supuestos y capa

| Supuesto | Valor | Capa |
|---|---|---|
| Equilibrio parcial, un solo mercado local por CCAA, sin cambios de composición | — | C4 |
| $\lvert\varepsilon_d\rvert$ | rejilla uniforme 0,3-1,5 (P-D v3 / v5). Literatura sin valor verificado en docs/literatura.md: NO VERIFICADA | C4 |
| $\varepsilon_s$ rejilla | por clase A4 (método A de v5: percentiles 25-75 de la respuesta de oferta; método B: 1,75 / 0 / 0,45), media ponderada por déficit de las provincias de cada CCAA, cruce por código INE. Referencias: Saiz (2010, DOI verificado, cuartil no verificado); BdE IA 2025 (≈0,45) | C4 |
| $\varepsilon_s$ regional | DOLS ±2 de ln(visados) sobre ln(IPV/IPCA), 2008-2025, por CCAA; MG solo como insumo. Se usa si IC95 en [0; 5] y diagnósticos (cointegración Engle-Granger p<0,10; Ljung-Box(4) p>0,05) | C4 |
| Senda de ajuste | semivida entre las medianas regionales de R4 (spec A y B). Supuesto de senda: la inferencia de R4 no es válida (sin largo plazo identificado) | C4 |
| Ofertas: llegada | 1 año de trámite y obra antes de completarse; el acumulado es lineal | C4 |
| (a) construcción adicional | min(necesidad anual central T3, máximo anual de visados 2016-2025 menos visados 2025) × U(0,5; 1) | C4 |
| (b) vacías | triangular(M_min, M_central, M_max) de T3 / 10 años (v5 B1/T3) | C4 |
| (c) vivienda pública | 20 % de la necesidad anual central × U(0,5; 1,5), con desplazamiento de la promoción privada U(0; 0,5) | C4 |
| (d) turísticos | 5-30 % del stock de VUT regional vuelve al uso residencial; la cota nacional B4-v3-vut-cantidad (2,746 % del stock de alquiler, C2) no se reparte por CCAA | C4 |
| (e) ayuda a la demanda | 5-15 % del precio o la renta | C4 |
| (f1) rebaja ITP / IVA vivienda nueva | 1-4 puntos del precio; sin tipos vigentes por CCAA en data/raw: escenario genérico | C4 |
| (f2) impuestos a la construcción | rebaja del coste 2-6 %, cuota del coste en el precio 40-70 % | C4 |
| Reparto a alquiler | parque en alquiler 15-20 %; fracción de ΔQ al alquiler: (a) 10-30 %, (b) 30-70 %, (c) 80-100 %, (d) 100 % | C4 |
| Coste fiscal | s × compraventas 2025 × 90 m² × precio tasado (€/m²), sin efectos inducidos. Alquiler y oferta: sin base | C4 |

## Regla de «recomendación robusta» (adaptación declarada)

El encargo de V7 pedía robustez por PMG y jerárquico. R4 no identificó un largo plazo estable, así que se adapta: una combinación CCAA × instrumento es robusta solo si (i) la variación del esfuerzo es negativa en TODAS las extracciones de Monte Carlo y en los tres horizontes, y menor que -0,1 % a 10 años (materialidad), con la rejilla de $\varepsilon_s$, y (ii) lo mismo con la elasticidad regional cuando es utilizable. Si la regional no es utilizable, la robustez es «solo con rejilla» y se declara.
"""


def main():
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    reg = Registry(OUT / "registro.csv")
    global SV
    SV = semivida_r4()
    d = leer_panel()
    es = elasticidades_regionales(d, reg)
    rej = rejilla_a4().set_index("cc")
    bs = base_regional(d)
    es_i = es.set_index("cc")
    rng0 = np.random.default_rng(SEED)
    filas = []
    for i, cc in enumerate(sorted(rej.index)):
        seed = int(rng0.integers(1, 2**31))
        r, b, er = rej.loc[cc], bs.loc[cc], es_i.loc[cc]
        filas += simular(cc, b, r, er, np.random.default_rng(seed), "rejilla")
        filas += simular(cc, b, r, er, np.random.default_rng(seed), "regional")
    im = pd.DataFrame(filas)
    # robustez
    rob = []
    for (cc, inst, mer), g in im.groupby(["cc", "instrumento", "mercado"]):
        def ok_esf(fu):
            x = g[g.fuente_es == fu]
            return bool((x.esfuerzo_max < 0).all() and x[x.horizonte == 10].esfuerzo_p95.iloc[0] < UMBRAL and x[x.horizonte == 10].esfuerzo_max.iloc[0] < UMBRAL)

        def precio_no_sube(fu):   # V7 (orquestador): una propuesta no es robusta si sube el precio o alquiler de MERCADO
            x = g[g.fuente_es == fu]   # (p. ej. ayudas a la demanda: baja el esfuerzo neto del beneficiario pero encarece al resto)
            return bool((x.dprecio_p95 <= 1e-9).all())

        def ok(fu):
            return ok_esf(fu) and precio_no_sube(fu)
        us = bool(es_i.loc[cc, "usable"])
        r_rej, r_reg = ok("rejilla"), ok("regional")
        rob.append(dict(cc=cc, ccaa=NOMBRE[cc], instrumento=inst, mercado=mer, robusto_rejilla=r_rej, regional_utilizable=us,
                        robusto_regional=r_reg if us else np.nan,
                        robusto=bool(r_rej and (r_reg if us else True)),
                        tipo=("robusto con rejilla y regional" if r_rej and us and r_reg else "robusto solo con rejilla (regional no utilizable)" if r_rej and not us
                              else "no robusto: reduce el esfuerzo neto del beneficiario pero sube el precio de mercado" if ok_esf("rejilla") and not precio_no_sube("rejilla")
                              else "no robusto")))
    rb = pd.DataFrame(rob)
    im = im.merge(rb[["cc", "instrumento", "mercado", "robusto", "tipo"]], on=["cc", "instrumento", "mercado"])
    im.insert(1, "ccaa", im.cc.map(NOMBRE))
    im.round(4).to_csv(OUT / "impactos.csv", index=False)
    rb.to_csv(OUT / "robustas_por_ccaa.csv", index=False)
    e = es.merge(rej[["clase_modal", "provincias_por_clase", "cods_prov", "rej_lo", "rej_hi"]], left_on="cc", right_index=True)
    e["fuente_usada"] = np.where(e.usable, "regional (DOLS)", "rejilla v5 por clase A4")
    e.drop(columns=["n"]).assign(n=es.n).round(4).to_csv(OUT / "elasticidades_oferta.csv", index=False)
    for r in im[im.fuente_es == "rejilla"].itertuples():
        reg.log("R6-mc", f"{r.cc}_{r.instrumento}_{r.mercado}_{r.horizonte}", "traslado MC rejilla", "2026", f"{2026 + r.horizonte}", NMC,
                np.nan, np.nan, np.nan, coef_interes=r.esfuerzo_med, p_interes=np.nan, notas="C4, escenario; sin contraste de hipotesis")
    reg.flush()
    MG = es.attrs["mg"]
    (OUT / "metodo.md").write_text(METODO, encoding="utf-8")
    escribir_resumen(im, rb, e, MG)
    resultado(im, rb, e, MG)


def escribir_resumen(im, rb, e, MG):
    r10 = rb[rb.robusto]
    L = ["# V7-R6 · Resumen (C4; condicional; instrumentos, no actores)", "",
         f"Datos: panel_ccaa_q_v7 (visados 2008Q1-2025Q4, IPV, HICP), A4 v5 (2021-2025), T3 v5.1, Censo 2021 (parque), R4 v7. Fecha {FECHA}. "
         f"Monte Carlo: {NMC} extracciones por CCAA y fuente. Horizontes 2, 5 y 10 años. Intervalos al 90 % (p5-p95).", "",
         "## Elasticidad de oferta regional (insumo)",
         f"- DOLS ±2 por CCAA: IC95 en [0; 5] y diagnósticos pasados en {int(e.usable.sum())} de {len(e)} CCAA. "
         f"MG = {MG[0]:.2f} (ee {MG[1]:.2f}). Con tan pocas CCAA utilizables se mantiene la rejilla v5 por clase A4 como alternativa y se reportan ambas.",
         f"- Con IC95 dentro de [0; 5] sin diagnósticos: {int(e.ic_en_0_5.sum())}; con p BH < 0,05: {int((e.p_BH < .05).sum())}.", "",
         "## Qué combinaciones son robustas (esfuerzo negativo en todo el rango de MC)",
         f"- {len(r10)} de {len(rb)} combinaciones CCAA × instrumento × mercado.", ""]
    for inst, g in rb.groupby("instrumento"):
        x = g[g.robusto]
        L.append(f"- {inst}: robusto en {x.cc.nunique()} CCAA ({', '.join(sorted(x.ccaa.unique())) or 'ninguna'}); tipo: " + "; ".join(sorted(x.tipo.unique())))
    ning = [c for c in sorted(rb.cc.unique()) if not rb[(rb.cc == c) & rb.robusto].shape[0]]
    L += ["", "CCAA sin ninguna propuesta robusta: " + (", ".join(NOMBRE[c] for c in ning) or "ninguna"), "",
          "## Orden de magnitud a 10 años (rejilla, variación del esfuerzo en %, mediana [p5; p95], mercado precio)", ""]
    x = im[(im.fuente_es == "rejilla") & (im.horizonte == 10) & (im.mercado == "precio")]
    L += ["| CCAA | instrumento | mediana | p5 | p95 | coste M€ | robusto |", "|---|---|---|---|---|---|---|"]
    for r in x.itertuples():
        L.append(f"| {r.ccaa} | {r.instrumento} | {r.esfuerzo_med:.2f} | {r.esfuerzo_p5:.2f} | {r.esfuerzo_p95:.2f} | "
                 f"{'sin base' if np.isnan(r.coste_meur_med) else f'{r.coste_meur_med:.0f}'} | {'sí' if r.robusto else 'no'} |")
    L += ["", "## Efecto distributivo (cualitativo, tablas v5 CC, ECV 2025, % con sobrecarga de coste)",
          "- Si los instrumentos redujeran el esfuerzo del alquiler de mercado, el grupo con mayor sobrecarga es RENT_MKT (26,8 %; 43,3 % en 2015) y el primer quintil (27,7 %).",
          "- Con ayudas a la demanda, parte de la ayuda se traslada al precio (incidencia ι): la captan los vendedores o arrendadores y, si son propietarios, se reparte según la tenencia. Los hogares jóvenes con vivienda en propiedad son el 31,8 % de los titulares menores de 35 (EFF 2022, C4).",
          "- El efecto distributivo no se cuantifica por CCAA: sin base de renta por hogar y tenencia a ese nivel.", "",
          "## Coste fiscal", "- Solo para ayudas a la compra y rebaja ITP/IVA (base: compraventas 2025 × 90 m² × precio tasado); oferta, vivienda pública, "
          "alquiler e impuestos a la construcción: sin base (no hay coste unitario verificado).", "",
          "## Límites", "- R4 no identificó un largo plazo estable: la senda de ajuste es un supuesto. Todo es C4: «si se hiciera X, con estos supuestos…».",
          "- Ceuta y Melilla quedan fuera (sin CCAA en el panel). Panel sin sellar: informativo, muestra ya vista en v1."]
    (OUT / "resumen.md").write_text("\n".join(L), encoding="utf-8")


def resultado(im, rb, e, MG):
    r10 = rb[rb.robusto]
    por_inst = {i: sorted(g[g.robusto].cc.unique().tolist()) for i, g in rb.groupby("instrumento")}
    x = im[(im.fuente_es == "rejilla") & (im.horizonte == 10) & (im.mercado == "precio")]
    res = dict(rama="R6", pregunta="Si se aplicasen distintos instrumentos por CCAA, que variacion de precio, alquiler y esfuerzo cabria esperar (traslado), y cuales son robustos?",
               capa="C4", datos=["data/processed/v7/panel_ccaa_q_v7.csv", "output/v5/A4/clasificacion_provincias.csv", "output/v5_1/T3/tablas/necesidad_provincial.csv",
                                 "output/v5/R1C/vacias_esporadicas_municipio_censo2021.csv", "output/v7/R4 (velocidad_ajuste_region)", "data/raw/eu_hicp.csv"],
               N={"ccaa": 17, "extracciones_MC": NMC, "combinaciones": int(len(rb))},
               metodo="incidencia |ed|/(es+|ed|); MC sobre es (regional DOLS o rejilla A4), ed U(0,3;1,5) y tamano del instrumento; senda por semivida R4 (supuesto)",
               estimacion={"robustas_por_instrumento_ccaa": por_inst, "n_robustas": int(len(r10)), "n_combinaciones": int(len(rb)),
                           "esfuerzo_10a_precio_mediana_min_max": [float(x.esfuerzo_med.min()), float(x.esfuerzo_med.max())],
                           "MG_es": [float(MG[0]), float(MG[1])], "ccaa_es_regional_utilizable": int(e.usable.sum())},
               ic95=None, p_ajustado=None, nivel_evidencia="EXPLORATORIO (C4); escenarios condicionales, sin lenguaje causal",
               diagnosticos={"es_regional": "IC95 en [0;5] y Engle-Granger p<0,10 y Ljung-Box(4) p>0,05; BH y Holm sobre los 17 p de DOLS",
                             "semivida_trim_R4": list(SV), "umbral_materialidad_pct": UMBRAL, "rotulo": "informativo, muestra ya vista en v1"},
               fuera_muestra={"modelo": None, "rmse": None, "dm_vs_ar4": None},
               notas="Parametros son supuestos; sin tipos ITP/IVA por CCAA en data/raw; coste solo en compra; R4 sin largo plazo identificado.")
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    h = []
    for inst, g in x.groupby("instrumento"):
        h.append(dict(id=f"V7-R6-{inst}-esfuerzo10a", indicador=f"Variacion del esfuerzo de compra a 10 anos si se aplicase {inst} (mediana entre CCAA, rejilla)",
                      valor=float(g.esfuerzo_med.median()), min=float(g.esfuerzo_p5.min()), max=float(g.esfuerzo_p95.max()), unidad="%",
                      periodo="2026-2036 (escenario)", cobertura="17 CCAA", fuentes="A4 v5; T3 v5.1; R4 v7; panel_ccaa_q_v7", capa="C4", fecha_dato=FECHA))
    h.append(dict(id="V7-R6-n-robustas", indicador="Combinaciones CCAA x instrumento x mercado robustas", valor=int(len(r10)), min=None, max=None,
                  unidad="combinaciones", periodo="escenario", cobertura=f"{len(rb)} combinaciones", fuentes="R6", capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
