"""V16-F2.2 · Contabilidad, no causalidad (docs/v16/plan.md, fase 2, punto 2, primeras dos descomposiciones). Capa C4.

1. Variación del número de hogares (shift-share exacto) -> f2_contabilidad_hogares.py
2. Precio: parte común y parte local (PCA y DynamicFactor) -> f2_contabilidad_precio.py
La descomposición del esfuerzo (renta/precio) es de OTRO módulo (f2_esfuerzo).
Uso: python3 src/v16/f2_contabilidad.py [--smoke]. SEED = 20261010. Sin red. No lee data/sealed.
Salidas: output/v16/f2_contabilidad/ (tablas CSV, registro.csv, informe.md, hechos.json, resultado.json).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v16"))
from econ_utils import Registry  # noqa: E402
import f2_contabilidad_hogares as H  # noqa: E402
import f2_contabilidad_precio as P  # noqa: E402

SEED = 20261010
OUT = RAIZ / "output/v16/f2_contabilidad"
COMP = ["poblacion", "composicion_nacionalidad", "estructura_edad", "jefatura_residuo"]
V8_CSV = RAIZ / "output/v8/M1/cuota_varianza.csv"


def _cols_tabla_hogares(df: pd.DataFrame) -> pd.DataFrame:
    base = ["fuente_hogares", "nivel", "codigo", "nombre", "desde", "hasta", "H0", "H1", "cambio_observado"]
    comp = [c for n in COMP[:3] for c in (n, f"{n}_min", f"{n}_max")] + ["jefatura_residuo", "jefatura_agregada_pct",
                                                                           "suma_componentes", "error_identidad", "nac_ES", "nac_EXT",
                                                                           "pobl0", "pobl1", "pobl_ES", "pobl_EXT", "pct_ext_0", "pct_ext_1"]
    extra = [c for c in df.columns if c not in base + comp]
    return df[base + comp + extra]


def hogares(out: Path, smoke: bool) -> dict:
    t0 = time.time()
    r = {}
    ecp25 = H.bloque_ecp(2021, 2025, smoke)
    ecp26 = H.bloque_ecp(2021, 2026, smoke)
    anual = H.bloque_ecp_anual(smoke)
    for nombre, df in (("ecp_2021_2025", ecp25), ("ecp_2021_2026", ecp26)):
        _cols_tabla_hogares(df).round(4).to_csv(out / f"hogares_{nombre}.csv", index=False)
    _cols_tabla_hogares(anual).round(4).to_csv(out / "hogares_ecp_anual_nacional.csv", index=False)
    epa25 = H.bloque_epa_reciente(2021, 2025)
    epa26 = H.bloque_epa_reciente(2021, 2026)
    larga = H.bloque_epa_larga()
    _cols_tabla_hogares(pd.DataFrame([epa25, epa26])).round(4).to_csv(out / "hogares_epa_2021_2025_2026_nacional.csv", index=False)
    _cols_tabla_hogares(larga).round(4).to_csv(out / "hogares_epa_2002_2021_nacional.csv", index=False)
    # discrepancia ECP-EPA
    nac = ecp25[ecp25.nivel == "nacional"].iloc[0].to_dict()
    disc = pd.DataFrame([{"periodo": "1-1-2021 a 1-1-2025", "H0_ecp": nac["H0"], "H0_epa": epa25["H0"], "H1_ecp": nac["H1"], "H1_epa": epa25["H1"],
                          "cambio_ecp": nac["cambio_observado"], "cambio_epa": epa25["cambio_observado"],
                          "diferencia_pct_cambio": 100 * (epa25["cambio_observado"] / nac["cambio_observado"] - 1),
                          "jefatura_ecp": nac["jefatura_residuo"], "jefatura_epa": epa25["jefatura_residuo"],
                          "discrepan_mas_10pct": abs(epa25["cambio_observado"] / nac["cambio_observado"] - 1) > 0.10}])
    disc.round(4).to_csv(out / "hogares_discrepancia_ecp_epa.csv", index=False)
    # EMCR (migración exterior) frente a la variación de la población extranjera
    em = H.emcr_saldo_exterior()
    saldo = sum(v for a, v in em.items() if 2021 <= a <= 2024)
    cr = pd.DataFrame([{"periodo": "2021-2024 (años naturales)", "saldo_exterior_emcr": saldo, "variacion_pob_extranjera_ecp_1ene21_1ene25": nac["pobl_EXT"],
                        "variacion_pob_espanola_ecp": nac["pobl_ES"], "cociente": nac["pobl_EXT"] / saldo,
                        "nota": "la variación de la población extranjera incluye cambios de nacionalidad y saldo vegetativo; no se concilian"}])
    cr.round(4).to_csv(out / "hogares_emcr_contraste.csv", index=False)
    r.update(ecp25=ecp25, ecp26=ecp26, anual=anual, epa25=epa25, epa26=epa26, larga=larga, disc=disc.iloc[0].to_dict(), emcr=cr.iloc[0].to_dict(),
             segundos=time.time() - t0)
    return r


def precio(out: Path, smoke: bool, reg: Registry) -> dict:
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    B, BN = (60, 100) if smoke else (499, 999)
    lp = P.cargar_log_precio()
    defl = P.cargar_deflactor()
    ccaa_de = pd.read_parquet(RAIZ / "data/base/territorios.parquet")
    ccaa_de = ccaa_de[ccaa_de.nivel == "provincia"].set_index("territorio_codigo").cod_ccaa.to_dict()
    todas = list(lp.columns)
    assert not set(todas) & set(P.SELLADAS_V6)
    completas = [c for c in todas if c not in P.CON_HUECOS and lp.loc[P._q("2006T1"):, c].notna().all()]
    if smoke:
        completas = completas[:12]
    lp_real = lp.sub(defl.reindex(lp.index), axis=0)
    variantes = {
        "principal_d4_nominal": (lp[completas], "d4", False),
        "d4_real": (lp_real[completas], "d4", False),
        "trimestral_nominal": (lp[completas], "dq", False),
        "d4_nominal_interpolada": (lp[[c for c in todas if c in completas or c in P.CON_HUECOS]], "d4", True),
    }
    nulas: dict = {}
    filas, filas_prov, filas_niv, filas_res = [], [], [], []
    for vn, (lpv, tipo, interp) in variantes.items():
        R = P.construir(lpv, tipo, interp)
        for pn, (a, b) in PERIODOS_ITER():
            X = P.ventana(R, a, b)
            if X.shape[0] < 12:
                continue
            p = P.pca_periodo(X.values)
            T, N = X.shape
            bs = P.cuota_bootstrap(X.values, B, rng)
            if (T, N) not in nulas:
                nulas[(T, N)] = P.cuota_nula(T, N, BN, rng)
            nul = nulas[(T, N)]
            pval = (1 + (nul >= p["cuota1"]).sum()) / (1 + len(nul))
            ccaa = P.correlacion_residuos(p["e"], list(X.columns), ccaa_de)
            fila = {"variante": vn, "periodo": pn, "tasa": tipo, "N_provincias": N, "T": T, "cuota_pc1": p["cuota1"], "cuota_2_factores": p["cuota2"],
                    "b68_lo": np.quantile(bs, 0.16), "b68_hi": np.quantile(bs, 0.84), "ic95_lo": np.quantile(bs, 0.025), "ic95_hi": np.quantile(bs, 0.975),
                    "cuota_azar_media": nul.mean(), "cuota_azar_p95": np.quantile(nul, 0.95), "p_vs_azar": pval,
                    "k_bai_ng_icp2": P.bai_ng_icp2(X.values), "r2_mediano": np.median(p["r2"]), "r2_min": p["r2"].min(), "r2_max": p["r2"].max(),
                    "interpolada": bool(interp), **ccaa}
            filas.append(fila)
            if vn in ("principal_d4_nominal", "trimestral_nominal"):
                for c, r2, lam in zip(X.columns, p["r2"], p["lam"]):
                    filas_prov.append({"variante": vn, "periodo": pn, "provincia": c, "ccaa": ccaa_de.get(c), "cuota_comun_r2": r2, "cuota_local": 1 - r2,
                                       "sd_tasa_pp": 100 * X[c].std(ddof=1), "sd_local_pp": 100 * X[c].std(ddof=1) * np.sqrt(1 - r2), "carga_tipificada": lam})
            if vn == "trimestral_nominal":
                filas_niv.append(P.contabilidad_nivel(X.values, list(X.columns), pn))
            reg.log("v16-f2-contabilidad", f"precio_{vn}_{pn}", f"PCA1 de {N} provincias; {tipo} ln valor tasado", a, b, T, np.nan, np.nan, np.nan,
                    coef_interes=p["cuota1"], p_interes=pval, notas=f"cuota PC1 frente a azar (N={N},T={T}); C4 contabilidad")
    tab = pd.DataFrame(filas)
    ok = ~tab.p_vs_azar.isna()
    tab["p_ajustado_bh"] = np.nan
    tab.loc[ok, "p_ajustado_bh"] = multipletests(tab.loc[ok, "p_vs_azar"], method="fdr_bh")[1]
    tab.round(5).to_csv(out / "precio_cuota_comun_periodo.csv", index=False)
    prov = pd.DataFrame(filas_prov)
    prov.round(5).to_csv(out / "precio_cuota_comun_provincia.csv", index=False)
    niv = pd.concat(filas_niv, ignore_index=True)
    niv.round(4).to_csv(out / "precio_contabilidad_nivel_provincia.csv", index=False)

    # DynamicFactor (statsmodels): toda la muestra 2007T1-2026T2, tasa trimestral, provincias principales
    Rq = P.construir(lp[completas], "dq")
    Xq = P.ventana(Rq, "2007T1", "2026T2")
    f_dfm, conv, llf = P.dfm_statsmodels(Xq.values, maxiter=40 if smoke else 150)
    pc = P.pca_periodo(Xq.values)
    corr = float(np.corrcoef(f_dfm, pc["f"])[0, 1])
    filas_dfm = []
    for pn, (a, b) in PERIODOS_ITER():
        sel = (Xq.index >= P._q(a)) & (Xq.index <= P._q(b))
        Zs = (Xq.values[sel] - Xq.values[sel].mean(0)) / Xq.values[sel].std(0, ddof=1)
        r2d = P.r2_con_factor(Zs, f_dfm[sel])
        r2p = P.r2_con_factor(Zs, pc["f"][sel])
        pcp = P.pca_periodo(Xq.values[sel])
        filas_dfm.append({"periodo": pn, "T": int(sel.sum()), "N": Xq.shape[1], "r2_medio_dfm_global": r2d.mean(), "r2_medio_pc1_global": r2p.mean(),
                          "cuota_pc1_propia_periodo": pcp["cuota1"], "corr_factor_dfm_pc1_global": corr})
        reg.log("v16-f2-contabilidad", f"precio_dfm_global_{pn}", "DynamicFactor(k=1, AR2) 2007T1-2026T2, R2 medio por periodo", a, b, int(sel.sum()),
                np.nan, np.nan, np.nan, coef_interes=float(r2d.mean()), notas=f"convergió={conv}; llf={llf:.1f}; contraste de PCA")
    dfm_tab = pd.DataFrame(filas_dfm)
    dfm_tab["dfm_convergio"] = conv
    dfm_tab.round(5).to_csv(out / "precio_dfm_contraste.csv", index=False)

    # puente con V8 (17 CCAA, precio real, P2/P3/P5): V8 publicado, 11 CCAA libres y 33 provincias en los periodos de V8
    v8 = pd.read_csv(V8_CSV)
    v8 = v8[(v8.serie == "compra_tasado") & (v8.metodo == "pca") & (v8.k == 1) & v8.periodo.isin(["P2", "P3", "P5", "completo"])]
    pv8 = {"P2": ("2008T3", "2013T4"), "P3": ("2014T1", "2019T4"), "P5": ("2022T3", "2026T2")}
    cc = P.panel_ccaa_libres()
    cc_real = cc.sub(defl.reindex(cc.index), axis=0)
    puente = []
    for pn, (a, b) in pv8.items():
        fv = v8[v8.periodo == pn].iloc[0]
        for nom, panel in (("CCAA sin provincias selladas con serie completa (real)", cc_real), ("33 provincias (real)", lp_real[completas])):
            X = P.ventana(P.construir(panel, "d4"), a, b)
            if X.shape[0] < 8:
                continue
            p = P.pca_periodo(X.values)
            puente.append({"periodo_v8": pn, "ventana": f"{a}-{b}", "panel": nom, "N": X.shape[1], "T": X.shape[0], "cuota_pc1": p["cuota1"],
                           "v8_17_ccaa_cuota": fv.cuota, "v8_b68_lo": fv.b68_lo, "v8_b68_hi": fv.b68_hi, "v8_N": int(fv.N), "v8_T": int(fv["T"]),
                           "cuota_azar_v8": fv.cuota_azar_media})
    pt = pd.DataFrame(puente)
    pt["diferencia_pp"] = 100 * (pt.cuota_pc1 - pt.v8_17_ccaa_cuota)
    pt["fuera_banda68_v8"] = (pt.cuota_pc1 < pt.v8_b68_lo) | (pt.cuota_pc1 > pt.v8_b68_hi)
    pt.round(5).to_csv(out / "precio_puente_v8.csv", index=False)
    for q in pt.itertuples():
        reg.log("v16-f2-contabilidad", f"puente_v8_{q.periodo_v8}_{q.N}", f"PCA1 {q.panel}; d4 ln real", q.ventana.split("-")[0], q.ventana.split("-")[1], q.T,
                np.nan, np.nan, np.nan, coef_interes=q.cuota_pc1, notas="puente con V8-M1 (17 CCAA); sin contraste de hipótesis")
    return {"tab": tab, "prov": prov, "niv": niv, "dfm": dfm_tab, "puente": pt, "N_completas": len(completas), "N_disponibles": len(todas),
            "conv": conv, "corr_dfm_pc1": corr, "columnas": completas, "segundos": time.time() - t0}


def PERIODOS_ITER():
    return list(P.PERIODOS.items())


# ---------------------------------------------------------------- hechos, resultado, informe
def _h(id_, ind, val, mn, mx, unidad, per, cob, fuentes, fecha, ancla=None):
    return {"id": f"V16-CON-{id_}", "indicador": ind, "valor": None if val is None else float(round(val, 4)),
            "min": None if mn is None else float(round(mn, 4)), "max": None if mx is None else float(round(mx, 4)),
            "unidad": unidad, "periodo": per, "cobertura": cob, "fuentes": fuentes, "capa": "C4", "fecha_dato": fecha,
            "ficha": f"output/v16/f2_contabilidad/informe.md#v16-con-{id_.lower()}"}


def construir_hechos(h: dict, pr: dict) -> list[dict]:
    hs = []
    e25 = h["ecp25"][h["ecp25"].nivel == "nacional"].iloc[0]
    ep = h["epa25"]
    fu = "INE ECP (t60129, t60133); INE EPA (hogares); Censo 2021 (microdatos)"
    per = "1-1-2021 a 1-1-2025"
    rng_ = lambda k: (min(e25[f"{k}_min"], ep[f"{k}_min"]), max(e25[f"{k}_max"], ep[f"{k}_max"])) if f"{k}_min" in ep else (None, None)
    hs.append(_h("HOG-CAMBIO", "Variación observada del número de hogares, España (valor: ECP; rango: ECP y EPA)", e25.cambio_observado,
                 min(e25.cambio_observado, ep["cambio_observado"]), max(e25.cambio_observado, ep["cambio_observado"]), "hogares", per, "España", fu, "2026-01-01"))
    for k, nom in (("poblacion", "tamaño de la población"), ("composicion_nacionalidad", "composición por nacionalidad (extranjera frente a española)"),
                   ("estructura_edad", "estructura por edad")):
        mn, mx = rng_(k)
        hs.append(_h(f"HOG-{k.upper().replace('_', '-')}", f"Contabilidad del cambio de hogares 2021-2025: parte de {nom}, España (Shapley; rango: órdenes y ECP/EPA)",
                     e25[k], mn, mx, "hogares", per, "España", fu, "2026-01-01"))
    hs.append(_h("HOG-JEFATURA", "Contabilidad del cambio de hogares 2021-2025: residuo de jefatura (tasa agregada a población constante), España (rango: ECP y EPA)",
                 e25.jefatura_residuo, min(e25.jefatura_residuo, ep["jefatura_residuo"]), max(e25.jefatura_residuo, ep["jefatura_residuo"]), "hogares", per,
                 "España", fu, "2026-01-01"))
    c = h["ecp25"][h["ecp25"].nivel == "ccaa"]
    hs.append(_h("HOG-CCAA-JEFATURA-PCT", "Residuo de jefatura como % de los hogares iniciales, 11 CCAA sin provincias selladas (valor: mediana; rango: mín. y máx.)",
                 float((100 * c.jefatura_residuo / c.H0).median()), float((100 * c.jefatura_residuo / c.H0).min()), float((100 * c.jefatura_residuo / c.H0).max()),
                 "%", per, "11 CCAA (8 excluidas por K8)", fu, "2026-01-01"))
    c = c.assign(p=100 * c.poblacion / c.cambio_observado)
    hs.append(_h("HOG-CCAA-POBLACION-PCT", "Parte de población en el cambio observado de hogares, 11 CCAA (valor: mediana; rango: mín. y máx.)",
                 float(c.p.median()), float(c.p.min()), float(c.p.max()), "% del cambio", per, "11 CCAA (8 excluidas por K8)", fu, "2026-01-01"))
    d = h["disc"]
    hs.append(_h("HOG-ECP-EPA-DISCREPANCIA", "Diferencia del cambio de hogares 2021-2025 entre EPA y ECP", d["diferencia_pct_cambio"], None, None, "%", per, "España",
                 "INE ECP; INE EPA", "2026-01-01"))
    l = h["larga"]
    l21 = l[(l.referencia_censo == 2021) & (l.desde == 2002) & (l.hasta == 2021)].iloc[0]
    l11 = l[(l.referencia_censo == 2011) & (l.desde == 2002) & (l.hasta == 2021)].iloc[0]
    fu2 = "INE EPA (hogares); INE padrón (edad y nacionalidad); Censos 2011 y 2021 (microdatos)"
    hs.append(_h("HOG-EPA-2002-2021-CAMBIO", "Variación de hogares EPA 2002T1-2021T1, España", l21.cambio_observado, None, None, "hogares", "2002-2021", "España", fu2, "2021-01-01"))
    for k, nom in (("poblacion", "tamaño de la población"), ("composicion_nacionalidad", "composición por nacionalidad"), ("estructura_edad", "estructura por edad"),
                   ("jefatura_residuo", "residuo de jefatura")):
        hs.append(_h(f"HOG-EPA-2002-2021-{k.upper().replace('_', '-')}", f"Contabilidad EPA 2002-2021: {nom} (valor: tasas del Censo 2021; rango: con tasas del Censo 2011 y órdenes)",
                     l21[k], min(l21[k], l11[k], l21.get(f"{k}_min", l21[k]), l11.get(f"{k}_min", l11[k])), max(l21[k], l11[k], l21.get(f"{k}_max", l21[k]), l11.get(f"{k}_max", l11[k])),
                     "hogares", "2002-2021", "España", fu2, "2021-01-01"))
    l14 = l[(l.referencia_censo == 2021) & (l.desde == 2014)].iloc[0]
    hs.append(_h("HOG-EPA-2014-2021-JEFATURA", "Residuo de jefatura EPA 2014-2021, España (ruptura de la EPA en 2021T1 posible; no se interpreta)", l14.jefatura_residuo, None, None,
                 "hogares", "2014-2021", "España", fu2, "2021-01-01"))
    em = h["emcr"]
    hs.append(_h("MIG-EMCR-SALDO", "Saldo migratorio exterior EMCR acumulado 2021-2024 frente a variación de la población extranjera ECP 1-1-2021 a 1-1-2025 (valor: saldo)",
                 em["saldo_exterior_emcr"], min(em["saldo_exterior_emcr"], em["variacion_pob_extranjera_ecp_1ene21_1ene25"]),
                 max(em["saldo_exterior_emcr"], em["variacion_pob_extranjera_ecp_1ene21_1ene25"]), "personas", "2021-2024", "España", "INE EMCR (t69711); INE ECP", "2024-12-31"))
    t = pr["tab"]
    prin = t[t.variante == "principal_d4_nominal"].set_index("periodo")
    for pn in PERIODOS_ITER_NOMBRES():
        r = prin.loc[pn]
        hs.append(_h(f"PRECIO-CUOTA-PC1-{pn}", f"Cuota del 1.er factor común (PC1) en la varianza del crecimiento interanual del valor tasado, {int(r.N_provincias)} provincias (valor: cuota; rango: banda 95 %)",
                     100 * r.cuota_pc1, 100 * r.ic95_lo, 100 * r.ic95_hi, "%", pn, f"{int(r.N_provincias)} provincias (11 selladas v6 excluidas)",
                     "MIVAU valor tasado (data/base)", "2026-06-30" if pn == "2020-2026" else f"{pn[-4:]}-12-31"))
    pv = pr["prov"]
    pv = pv[pv.variante == "principal_d4_nominal"]
    for pn in PERIODOS_ITER_NOMBRES():
        g = pv[pv.periodo == pn].cuota_comun_r2
        hs.append(_h(f"PRECIO-R2-PROV-{pn}", f"Cuota común por provincia (R² con el factor), {len(g)} provincias (valor: mediana; rango: mín. y máx.)", 100 * g.median(), 100 * g.min(),
                     100 * g.max(), "%", pn, f"{len(g)} provincias", "MIVAU valor tasado (data/base)", "2026-06-30" if pn == "2020-2026" else f"{pn[-4:]}-12-31"))
    dfm = pr["dfm"].set_index("periodo")
    hs.append(_h("PRECIO-DFM-R2", "R² medio con el factor del DynamicFactor (tasa trimestral, 2007T1-2026T2), periodo 2020-2026 (rango: periodos 2007-2013 y 2014-2019)", 100 * dfm.loc["2020-2026", "r2_medio_dfm_global"],
                 100 * dfm.r2_medio_dfm_global.min(), 100 * dfm.r2_medio_dfm_global.max(), "%", "2007-2026", f"{pr['N_completas']} provincias", "MIVAU valor tasado (data/base); statsmodels", "2026-06-30"))
    tq = t[t.variante == "principal_d4_nominal"]
    hs.append(_h("PRECIO-LOCAL-CCAA", "Correlación media de los residuos locales entre provincias de la misma CCAA, 2014-2019 (rango: 2007-2013 a 2020-2026)",
                 float(tq.set_index("periodo").loc["2014-2019", "corr_residual_misma_ccaa"]), float(tq.corr_residual_misma_ccaa.min()), float(tq.corr_residual_misma_ccaa.max()),
                 "correlación", "2014-2019", "provincias de la misma CCAA", "MIVAU valor tasado (data/base)", "2019-12-31"))
    pt = pr["puente"]
    x = pt[pt.panel.str.startswith("33")]
    hs.append(_h("PRECIO-V8-DIF-PP", "Diferencia de la cuota del PC1 (33 provincias, precio real) con la de V8 (17 CCAA) en P2, P3 y P5 (valor: media; rango: mín. y máx.)",
                 float(x.diferencia_pp.mean()), float(x.diferencia_pp.min()), float(x.diferencia_pp.max()), "pp", "P2, P3, P5 de V8", "33 provincias frente a 17 CCAA", "V8-M1; MIVAU valor tasado", "2026-06-30"))
    assert len(hs) <= 30, len(hs)
    return hs


def PERIODOS_ITER_NOMBRES():
    return list(P.PERIODOS)


def f0(x, d=0):
    return f"{x:,.{d}f}".replace(",", " ")


def escribir_informe(out: Path, h: dict, pr: dict, hechos: list[dict]) -> str:
    e = h["ecp25"][h["ecp25"].nivel == "nacional"].iloc[0]
    ep = h["epa25"]
    e26 = h["ecp26"][h["ecp26"].nivel == "nacional"].iloc[0]
    cc = h["ecp25"][h["ecp25"].nivel == "ccaa"]
    t = pr["tab"]
    prin = t[t.variante == "principal_d4_nominal"].set_index("periodo")
    tr = t[t.variante == "trimestral_nominal"].set_index("periodo")
    rl = t[t.variante == "d4_real"].set_index("periodo")
    ip = t[t.variante == "d4_nominal_interpolada"].set_index("periodo")
    dfm = pr["dfm"].set_index("periodo")
    pt = pr["puente"]
    l = h["larga"]
    l21 = l[(l.referencia_censo == 2021) & (l.desde == 2002) & (l.hasta == 2021)].iloc[0]
    sub = l[(l.referencia_censo == 2021) & (l.hasta - l.desde < 19)]
    v = {x["id"]: x for x in hechos}
    pv = pr["prov"]
    pv = pv[(pv.variante == "principal_d4_nominal")]
    loc = pv[pv.periodo == "2020-2026"].sort_values("cuota_local", ascending=False)
    niv = pr["niv"]
    nv = niv[niv.periodo == "2020-2026"]
    L = []
    A = lambda i: f'<a id="{i.lower()}"></a>'
    L.append("# V16 · F2.2 Contabilidad, no causalidad (C4)\n")
    L.append("Capa C4, descriptiva: son identidades contables y resúmenes de comovimiento, sin interpretación causal. Generado por `src/v16/f2_contabilidad.py` "
             "(SEED 20261010). La descomposición del esfuerzo es de otro módulo (`f2_esfuerzo`).\n")
    L.append("## 1. Hogares: demografía, jefatura y nacionalidad\n")
    L.append("**Qué amplía.** V12-B3 ya descompuso 2011-2021 con los dos censos (lo ya visto: V12-B3-hogares-*; no se repite). Aquí se añade 2021-2026 con ECP y EPA, "
             "la separación extranjera/española (V12 solo separaba edad) y 2002-2021 con EPA.\n")
    L.append("**Método.** H = k·Σ N·m·s·h (tamaño N, cuota de nacionalidad m, estructura por edad s dentro de cada nacionalidad, tasa de jefatura h por nacionalidad y quinquenio de edad del Censo 2021). "
             "Los tres factores demográficos se reparten por Shapley (rango = 6 órdenes); la jefatura es el residuo exacto H1 − k·V(1,1,1). No hay tasas de jefatura por edad "
             "después de 2021, así que la jefatura es una tasa agregada a población constante, no una tasa por edad. La suma reproduce el cambio observado "
             f"(error máximo {h['ecp25'].error_identidad.abs().max():.1e} hogares; test).\n")
    L.append(f"**España, 1-1-2021 a 1-1-2025 (ECP).** {A('v16-con-hog-cambio')}Cambio observado {f0(e.cambio_observado)} hogares (EPA: {f0(ep['cambio_observado'])}; difiere {h['disc']['diferencia_pct_cambio']:.1f} %). "
             f"{A('v16-con-hog-poblacion')}Población {f0(e.poblacion)} ({f0(e.poblacion_min)} a {f0(e.poblacion_max)}); "
             f"{A('v16-con-hog-composicion-nacionalidad')}composición por nacionalidad {f0(e.composicion_nacionalidad)}; "
             f"{A('v16-con-hog-estructura-edad')}estructura por edad {f0(e.estructura_edad)}; {A('v16-con-hog-jefatura')}residuo de jefatura {f0(e.jefatura_residuo)} "
             f"({e.jefatura_agregada_pct:.2f} % de los hogares a población constante). La población extranjera cambia {f0(e.pobl_EXT)} personas y la española {f0(e.pobl_ES)}; "
             f"su cuota pasa de {e.pct_ext_0:.1f} % a {e.pct_ext_1:.1f} %. A tasas de jefatura iniciales, la variación de población extranjera suma {f0(e.nac_EXT)} hogares y la española {f0(e.nac_ES)} (vista aditiva exacta). "
             f"La composición resta porque las tasas de jefatura por edad del Censo 2021 son menores en la población extranjera; \"composición\" mezcla migración y cambios de nacionalidad.\n")
    L.append(f"**ECP frente a EPA.** {A('v16-con-hog-ecp-epa-discrepancia')}Los dos discrepan en el nivel (18,54 M frente a {ep['H0'] / 1e6:.2f} M hogares en 2021T1) y {h['disc']['diferencia_pct_cambio']:.1f} % en el cambio; se reportan por separado "
             f"(`hogares_ecp_*`, `hogares_epa_*`). Con EPA el residuo de jefatura es {f0(ep['jefatura_residuo'])} (ECP: {f0(e.jefatura_residuo)}). Hasta 1-1-2026 (ECP): cambio {f0(e26.cambio_observado)}, población {f0(e26.poblacion)}, "
             f"composición {f0(e26.composicion_nacionalidad)}, estructura {f0(e26.estructura_edad)}, jefatura {f0(e26.jefatura_residuo)}.\n")
    L.append(f"**CCAA (11 sin provincias selladas v6; las 8 restantes se excluyen por K8).** {A('v16-con-hog-ccaa-jefatura-pct')}{A('v16-con-hog-ccaa-poblacion-pct')}El residuo de jefatura va de "
             f"{v['V16-CON-HOG-CCAA-JEFATURA-PCT']['min']:.2f} % a {v['V16-CON-HOG-CCAA-JEFATURA-PCT']['max']:.2f} % de los hogares iniciales; la parte de población en el cambio, de "
             f"{v['V16-CON-HOG-CCAA-POBLACION-PCT']['min']:.0f} % a {v['V16-CON-HOG-CCAA-POBLACION-PCT']['max']:.0f} %. Provincias (41): `hogares_ecp_2021_2025.csv`. EPA no publica hogares por CCAA en la base.\n")
    L.append(f"**2002-2021 (EPA, nacional).** {A('v16-con-hog-epa-2002-2021-cambio')}Cambio {f0(l21.cambio_observado)} hogares: "
             f"{A('v16-con-hog-epa-2002-2021-poblacion')}población {f0(l21.poblacion)}, {A('v16-con-hog-epa-2002-2021-composicion-nacionalidad')}composición {f0(l21.composicion_nacionalidad)}, "
             f"{A('v16-con-hog-epa-2002-2021-estructura-edad')}estructura {f0(l21.estructura_edad)}, {A('v16-con-hog-epa-2002-2021-jefatura-residuo')}jefatura {f0(l21.jefatura_residuo)} "
             f"(padrón en 4 grupos de edad). Con las tasas del Censo 2011 la jefatura sería {f0(l[(l.referencia_censo == 2011) & (l.desde == 2002) & (l.hasta == 2021)].iloc[0].jefatura_residuo)}: "
             f"el reparto depende de la tasa de referencia. {A('v16-con-hog-epa-2014-2021-jefatura')}En 2014-2021 el residuo es {f0(sub[sub.desde == 2014].iloc[0].jefatura_residuo)}, "
             "compatible con la ruptura de la EPA en 2021T1 (recalibración al Censo 2021); no se interpreta. ")
    em = h["emcr"]
    L.append(f"{A('v16-con-mig-emcr-saldo')}**Migración (EMCR).** Saldo exterior 2021-2024: {f0(em['saldo_exterior_emcr'])} personas; la población extranjera ECP crece {f0(em['variacion_pob_extranjera_ecp_1ene21_1ene25'])} "
             "(incluye cambios de nacionalidad); no se concilian. Solo se usa EMCR desde 2021 (ruptura de nivel antes: K6).\n")
    L.append("## 2. Precio: parte común y parte local\n")
    L.append(f"**Muestra.** Valor tasado MIVAU, trimestral, {pr['N_completas']} provincias con serie completa de las {pr['N_disponibles']} no selladas (las 11 de v6 se excluyen, K8; "
             "Cantabria no figura en la serie; 5 provincias con huecos en 2012 solo entran interpoladas, MARCADO, en robustez). Nominal salvo la variante real (deflactor nacional).\n")
    L.append("**Ya visto.** V8-M1 estimó el factor común de 17 CCAA (precio real, periodos P1-P5). Aquí: provincias, tres periodos nuevos, DynamicFactor y residuo local.\n")
    L.append("| Periodo | Cuota PC1 (IC95 bootstrap) | Azar (media) | p BH | Factores Bai-Ng | R² mediano prov. (mín.-máx.) | Trimestral | Real | Interpolada (38) |\n|---|---|---|---|---|---|---|---|---|")
    for pn in P.PERIODOS:
        r = prin.loc[pn]
        L.append(f"| {pn} | {A('v16-con-precio-cuota-pc1-' + pn)}{100 * r.cuota_pc1:.1f} % ({100 * r.ic95_lo:.1f}-{100 * r.ic95_hi:.1f}) | {100 * r.cuota_azar_media:.1f} % | {r.p_ajustado_bh:.3f} | {int(r.k_bai_ng_icp2)} | "
                 f"{A('v16-con-precio-r2-prov-' + pn)}{100 * r.r2_mediano:.0f} % ({100 * r.r2_min:.0f}-{100 * r.r2_max:.0f}) | {100 * tr.loc[pn, 'cuota_pc1']:.1f} % | {100 * rl.loc[pn, 'cuota_pc1']:.1f} % | {100 * ip.loc[pn, 'cuota_pc1']:.1f} % |")
    L.append("\nCuota = parte de la varianza de la tasa interanual de ln precio que recoge el PC1 (series tipificadas). Con N = 33 y T = 24-28 la cuota está sesgada al alza incluso sin factor (columna azar). Bai-Ng alcanza el máximo permitido (4) en la tasa interanual, que es muy persistente: ese número no es fiable. La cuota depende de la tasa: con la variación trimestral baja a 19-45 % (ruido de medida trimestral).\n")
    L.append(f"**DynamicFactor (statsmodels, 1 factor AR(2), 2007T1-2026T2, tasa trimestral; convergió: {pr['conv']}).** Correlación absoluta del factor con el PC1: {abs(pr['corr_dfm_pc1']):.3f}. "
             f"{A('v16-con-precio-dfm-r2')}R² medio con el factor: " + "; ".join(f"{pn} {100 * dfm.loc[pn, 'r2_medio_dfm_global']:.0f} % (PC1 global {100 * dfm.loc[pn, 'r2_medio_pc1_global']:.0f} %)" for pn in P.PERIODOS) +
             ". Se estima una sola vez en toda la muestra (N > T por periodo); las cuotas por periodo salen de ese factor.\n")
    mc = tq_mean = prin.corr_residual_misma_ccaa
    L.append(f"**Residuo local.** Es lo que queda tras quitar el factor. {A('v16-con-precio-local-ccaa')}Sus correlaciones entre provincias de la misma CCAA son {prin.loc['2007-2013', 'corr_residual_misma_ccaa']:.2f}, "
             f"{prin.loc['2014-2019', 'corr_residual_misma_ccaa']:.2f} y {prin.loc['2020-2026', 'corr_residual_misma_ccaa']:.2f} (por periodo), frente a {prin.loc['2007-2013', 'corr_residual_distinta_ccaa']:.2f}, "
             f"{prin.loc['2014-2019', 'corr_residual_distinta_ccaa']:.2f} y {prin.loc['2020-2026', 'corr_residual_distinta_ccaa']:.2f} entre CCAA distintas: las del mismo territorio autonómico son algo mayores, "
             f"pero pequeñas: el residuo es en su mayor parte específico de cada provincia. En 2020-2026 las provincias con mayor cuota local son {', '.join(loc.provincia.head(4))} ({', '.join(f'{100 * x:.0f} %' for x in loc.cuota_local.head(4))}). "
             f"Contabilidad exacta del cambio acumulado de ln precio (tasa trimestral, factor sin centrar; `precio_contabilidad_nivel_provincia.csv`): en 2020-2026 la parte del factor es "
             f"{nv.comun.median():.0f} puntos de ln x100 en la mediana provincial (local {nv.local.median():.0f}; local mín.-máx. {nv.local.min():.0f} a {nv.local.max():.0f}).\n")
    partes = []
    for pn_ in pt.periodo_v8.unique():
        z = pt[pt.periodo_v8 == pn_]
        c9 = z[~z.panel.str.startswith("33")].iloc[0]
        c33 = z[z.panel.str.startswith("33")].iloc[0]
        partes.append(f"{pn_}: V8 {100 * c9.v8_17_ccaa_cuota:.0f} % (banda 68 % {100 * c9.v8_b68_lo:.0f}-{100 * c9.v8_b68_hi:.0f}); {int(c9.N)} CCAA sin provincias selladas {100 * c9.cuota_pc1:.0f} %; "
                      f"{int(c33.N)} provincias {100 * c33.cuota_pc1:.0f} %")
    L.append("**Contraste con V8 (17 CCAA, precio real, interanual, `precio_puente_v8.csv`).** " + "; ".join(partes) + ". ")
    x = pt[pt.panel.str.startswith("33")]
    n_f = int(x.fuera_banda68_v8.sum())
    L.append(f"{A('v16-con-precio-v8-dif-pp')}Con 33 provincias la cuota difiere de V8 entre {x.diferencia_pp.min():.0f} y {x.diferencia_pp.max():.0f} pp; {n_f} de {len(x)} caen fuera de la banda del 68 % de V8. "
             "Discrepan: se informan ambas. Con 9 CCAA agregadas la cuota es parecida a la de V8; con 33 provincias es menor. Una explicación posible, no contrastada, es que las CCAA agregan provincias y promedian parte del residuo local.\n")
    L.append("## Límites\n- Contabilidad, no causalidad: ni la composición por nacionalidad ni el factor común admiten lectura causal. "
             "- Jefatura: residuo agregado; la tasa de referencia es la del Censo 2021 (2011 como sensibilidad). - Las 8 CCAA con provincias selladas (K8) no se calculan en hogares; el panel de precios no incluye las 11 provincias v6. "
             "- Valor tasado nominal; la variante real usa el deflactor nacional. - Registro de especificaciones: `registro.csv`; p frente a azar por BH.\n")
    texto = "\n".join(L)
    (out / "informe.md").write_text(texto, encoding="utf-8")
    return texto


def resultado(h: dict, pr: dict, out: Path, smoke: bool) -> dict:
    t = pr["tab"]
    prin = t[t.variante == "principal_d4_nominal"].set_index("periodo")
    e = h["ecp25"][h["ecp25"].nivel == "nacional"].iloc[0]
    res = {
        "rama": "v16-f2-contabilidad", "pregunta": "¿Cómo se reparte contablemente la variación de hogares (demografía, jefatura, nacionalidad) y la del precio (común frente a local)?",
        "capa": "C4",
        "datos": ["data/raw/v11/ine_ecp/ecp_t60129.csv.gz", "data/raw/ine_v2_hogares_prov.csv", "data/base/hechos.parquet (hogares_epa, valor_tasado; muestra_sellada_v6 == False)",
                  "data/raw/v11/ine_censos_microdatos/jefatura_2021.csv.gz", "data/processed/v16/tension_social.parquet (EMCR, nacional)"],
        "N": {"provincias_precio": pr["N_completas"], "trimestres_precio_2007_2026": 78, "ccaa_hogares": int((h["ecp25"].nivel == "ccaa").sum()), "provincias_hogares": int((h["ecp25"].nivel == "provincia").sum())},
        "metodo": "Shift-share con reparto de Shapley (tamaño, nacionalidad, edad) y residuo de jefatura; PCA y DynamicFactor (statsmodels) sobre tasas de ln valor tasado; bootstrap por bloques; BH",
        "estimacion": {"hogares_2021_2025_ecp": {k: float(e[k]) for k in ["cambio_observado", *COMP[:3], "jefatura_residuo"]},
                       "cuota_pc1_precio": {pn: float(prin.loc[pn, "cuota_pc1"]) for pn in prin.index}},
        "ic95": {pn: [float(prin.loc[pn, "ic95_lo"]), float(prin.loc[pn, "ic95_hi"])] for pn in prin.index},
        "p_ajustado": {pn: float(prin.loc[pn, "p_ajustado_bh"]) for pn in prin.index},
        "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"error_identidad_max_hogares": float(max(h["ecp25"].error_identidad.abs().max(), h["ecp26"].error_identidad.abs().max(), h["larga"].error_identidad.abs().max())),
                         "discrepancia_ecp_epa_pct": float(h["disc"]["diferencia_pct_cambio"]), "dfm_convergio": pr["conv"], "corr_dfm_pc1": pr["corr_dfm_pc1"],
                         "smoke": smoke, "ya_visto": ["V12-B3 (hogares 2011-2021)", "V8-M1 (factor común 17 CCAA)"],
                         "excluidas_k8": H.SELLADAS_V6},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Contabilidad C4 sin lectura causal. Hogares: 8 CCAA con provincias selladas excluidas (K8). Precio: 33 provincias con serie completa; interpolación solo en robustez. "
                 "Fuera de muestra no aplica (identidad contable)."}
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return res


def main(smoke: bool = False) -> None:
    out = OUT / "smoke" if smoke else OUT
    out.mkdir(parents=True, exist_ok=True)
    reg = Registry(out / "registro.csv")
    t0 = time.time()
    h = hogares(out, smoke)
    pr = precio(out, smoke, reg)
    if smoke:
        print("smoke OK", round(time.time() - t0, 1), "s", pr["segundos"], h["segundos"])
        reg.flush()
        return
    hechos = construir_hechos(h, pr)
    (out / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    escribir_informe(out, h, pr, hechos)
    resultado(h, pr, out, smoke)
    reg.flush()
    print("OK", round(time.time() - t0, 1), "s;", len(hechos), "hechos")


if __name__ == "__main__":
    main("--smoke" in sys.argv)
