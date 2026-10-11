"""M1b v6: resultado.json, hechos.json y desviaciones.md a partir de los resultados en memoria de m1b_run.py."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

FECHA = "2026-10-11"


def _f(x, n=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def escribir(OUT, EXTRA, df, smoke, B):
    fe = EXTRA["fe_prov"]
    adj = df.copy()
    holm = adj[adj.fam == "Holm"]
    # Holm: variables de S1 (pre-registro)
    s1 = []
    for _, r in holm.iterrows():
        s1.append(dict(id=r["id"], coef=_f(r.coef), p_wcb=_f(r.p), p_holm=_f(r.p_adj)))
    n_holm_sig = int((holm.p_adj < 0.05).sum())
    bh = adj[adj.fam == "BH"]
    n_bh_sig = int((bh.p_adj < 0.10).sum())
    oos = EXTRA["oos"]
    fm = {}
    for _, r in oos.iterrows():
        fm.setdefault(r.y, {})[r.modelo] = dict(rmse_ln=_f(r.rmse_ln), rmse_pct=_f(r.rmse_pct, 2), rmse_abs=_f(r.rmse_abs, 1),
                                                 dm_vs_ar4=_f(r.get("dm_vs_AR4")), p_dm_vs_ar4=_f(r.get("p_dm_vs_AR4")),
                                                 dm_vs_ecm_v1=_f(r.get("dm_vs_ECMv1")), p_dm_vs_ecm_v1=_f(r.get("p_dm_vs_ECMv1")))
    cap = EXTRA["cap"]
    ev = EXTRA["ratio_evo"]
    ult, pri = ev.iloc[-1], ev.iloc[0]
    gs = EXTRA["gsadf"]
    sdm = EXTRA["sdm"]
    res = {
        "rama": "v6/M1b", "modulo": "M1b", "smoke": bool(smoke),
        "pregunta": "¿Qué variables se asocian con el precio y el volumen de la compraventa por provincia y municipio, y cómo se relacionan los mercados de compra y alquiler?",
        "mercado": ["compra (precio)", "compra (volumen)", "relación compra-alquiler"],
        "medida_precio": {"principal": "valor tasado MIVAU (provincia, municipio)", "robustez": ["Registradores (provincia anual)"],
                          "no_usadas": "Notariado (solo Comunitat Valenciana, sin panel M0); índice triangulado A23 y IPV INE: sin desagregación provincial (solo nacional/CCAA)"},
        "capa": "C4",
        "datos": "output/v6/M0/paneles/*_train (prov_compra_anual, prov_trim_compra, mun_compra_anual, prov_alquiler_anual) y nacional_trim_desc; sin parte sellada",
        "N": {"prov_anual_S1_prereg": int(fe[(fe.spec == "S1_prereg_10") & (fe.y == "ln_pm2_tasado")].n.iloc[0]),
              "prov_anual_S2_nucleo8": int(fe[(fe.spec == "S2_nucleo8") & (fe.y == "ln_pm2_tasado")].n.iloc[0]),
              "prov_trim": int(EXTRA["fe_trim"].n.max()), "municipal": int(EXTRA["fe_mun"].n.iloc[0]),
              "var_panel": int(EXTRA["var_n"]), "provincias_train": 41, "clusters_CCAA": int(fe.clusters.iloc[0])},
        "metodo": f"FE unidad+año (pre-registrada) y unidad+tendencia; wild cluster bootstrap Webb restringido por CCAA (B={B}); Driscoll-Kraay; CCEP/CCEMG/MG; Durbin espacial (W 4 vecinos por centroides); exposición tipo shift-share y 2SLS; DML-PLR (RF, pliegues por provincia); Oster; Cinelli-Hazlett; SUR y PVAR Anderson-Hsiao; proyecciones locales por exposición; DOLS; GSADF bootstrap AR(p); validación por bloques con embargo y DM-HLN.",
        "estimacion": {
            "confirmatorias_S1_Holm": s1, "n_confirmatorias_Holm_p<0.05": n_holm_sig,
            "n_BH_q10_exploratorias": n_bh_sig, "n_especificaciones_registradas": int(len(adj)),
            "elasticidad_precio_alquiler": cap[["nivel", "esp", "elasticidad", "se", "p_wcb"]].round(4).to_dict("records"),
            "ratio_precio_alquiler_mediana_anios": {"2015": _f(pri.ratio_mediana, 2), str(int(ult.anio)): _f(ult.ratio_mediana, 2)},
            "gsadf_ccaa_p<0.05": int((gs.p_boot < 0.05).sum()), "gsadf_ccaa_total": int(len(gs)),
            "sdm_rho": {y: _f(g.rho.iloc[0]) for y, g in sdm.groupby("y")},
        },
        "ic95": "por coeficiente en tablas/fe_prov.csv (se CR1), tablas/sdm.csv (simulación) y IRF en tablas/b2_pvar_irf_precio_alquiler.csv; no hay IC único",
        "p_ajustado": {"Holm_min": _f(holm.p_adj.min()) if len(holm) else None, "BH_min": _f(bh.p_adj.min()) if len(bh) else None},
        "nivel_evidencia": "EXPLORATORIO (C4). Ningún contraste cumple los criterios de C3 en M1b; asociaciones, sin lenguaje causal. Veredicto máximo: ANALIZADA, NO CONCLUYENTE.",
        "diagnosticos": {
            "clusters": "8 CCAA en entrenamiento provincial (7 en municipal, 11 en trimestral): inferencia por wild cluster bootstrap Webb",
            "S1_pre_registrada": "los 10 regresores juntos dejan N=64: ln_vut (2020-2024) y ln_suelo (25 provincias) recortan la muestra; se añade el núcleo de 8 (N=342)",
            "potencia": "docs/v6/potencia.md: efectos mínimos detectables 2,5 % (precio) y 5 % (volumen) por 1 DE within con clúster",
            "balance_exposicion": EXTRA.get("ss_balance"),
            "shiftshare_poblacion_F1a": [_f(x, 2) for x in EXTRA["ident"].F_1a_etapa.dropna().unique()],
            "cointegracion_trimestral": EXTRA["coint"],
            "gsadf_tamano_MC": EXTRA["gsadf_tamano"],
            "no_ejecutados": "Rambachan-Roth (sin evento de compra identificable en train); Bartik de empleo (sin composición sectorial provincial); Pedroni/Westerlund (T anual=9)",
        },
        "fuera_muestra": {"modelo": "M1b_ADL (AR(4)+regresores t-1) frente a AR(4) y ECM v1; trimestral provincial, orígenes 2018/2020/2022, embargo 4 trimestres, h=1, misma muestra",
                          "rmse": {k: {m: v["rmse_pct"] for m, v in d.items()} for k, d in fm.items()}, "dm_vs_ar4": {k: d["M1b_ADL"]["dm_vs_ar4"] for k, d in fm.items()},
                          "p_dm_vs_ar4": {k: d["M1b_ADL"]["p_dm_vs_ar4"] for k, d in fm.items()}, "detalle": fm,
                          "nota": "RMSE en % (exp(rmse_ln)-1). Validación temporal dentro de entrenamiento; la muestra sellada la abre solo M4"},
        "notas": "Validación espacial nueva; temporal ya vista en v2 (otras provincias) y de forma descriptiva en v4-v5. Magnitudes: regresores en logs, por +10 %; en niveles, por +1 pp; € /m² al precio medio del entrenamiento. La tasa hipotecaria es nacional (no provincial); el crédito provincial no existe en M0: se usa hipotecas sobre vivienda (ETDP/HPT) como proxy.",
        "ficheros": {"registro": "registro.csv", "p_ajustados": "tablas/multiplicidad_p_ajustados.csv", "tablas": "tablas/", "desviaciones": "desviaciones.md"},
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    # ---------- hechos
    H = []
    d = EXTRA["ratio_d"]
    ylast = int(ult.anio)

    def hecho(i, ind, val, mn, mx, uni, per, cob, fu):
        H.append(dict(id=i, indicador=ind, valor=_f(val, 3), min=_f(mn, 3), max=_f(mx, 3), unidad=uni, periodo=per, cobertura=cob, fuentes=fu, capa="C4", fecha_dato=FECHA))
    cob = f"{int(ult.n_prov)} provincias de entrenamiento"
    fu = "MIVAU valor tasado; MIVAU-SERPAVI (alquiler de stock)"
    hecho("m1b_ratio_precio_alquiler_mediana", "Ratio precio/alquiler anual, mediana provincial (valor tasado / alquiler de stock anualizado)", ult.ratio_mediana, ult.ratio_p25, ult.ratio_p75, "años de alquiler (p25-p75)", str(ylast), cob, fu)
    hecho("m1b_ratio_precio_alquiler_mediana_2015", "Ratio precio/alquiler anual, mediana provincial", pri.ratio_mediana, pri.ratio_p25, pri.ratio_p75, "años de alquiler (p25-p75)", "2015", f"{int(pri.n_prov)} provincias de entrenamiento", fu)
    hecho("m1b_rentabilidad_bruta_mediana", "Rentabilidad bruta por alquiler, mediana provincial", ult.yield_mediana, None, None, "% del valor tasado", str(ylast), cob, fu)
    hecho("m1b_coste_uso_g2", "Coste de uso anual (tipo hipotecario ECB + 2,0 % depreciación y mantenimiento + 0,5 % impuestos - 2 % ganancia esperada; SUPUESTOS)", ult.coste_uso_g2, None, None, "% del valor", str(ylast), "nacional", "ECB tipo hipotecario España; supuestos del autor")
    hecho("m1b_brecha_rentabilidad_coste_uso", "Rentabilidad bruta menos coste de uso (g=2 %), mediana provincial", ult.brecha_mediana_g2, None, None, "pp", str(ylast), cob, fu + "; ECB")
    for _, r in cap.iterrows():
        hecho(f"m1b_elasticidad_{r.nivel}_{r.esp}".replace("+", "_").replace("(", "").replace(")", "").replace(" ", ""), f"Elasticidad precio tasado - alquiler ({r.esp}, asociación)", r.elasticidad, r.elasticidad - 1.96 * r.se, r.elasticidad + 1.96 * r.se, "elasticidad (IC95 por se CR1)", "2015-2023" if r.nivel == "anual" else "2015T1-2024T4", "41 provincias de entrenamiento", fu if r.nivel == "anual" else "MIVAU valor tasado; INE IPC alquiler (stock)")
    for y, g in sdm.groupby("y"):
        hecho(f"m1b_sdm_rho_{y}", f"Autocorrelación espacial (Durbin espacial, W 4 vecinos) de {y}", g.rho.iloc[0], g.rho.iloc[0] - 1.96 * g.rho_se.iloc[0], g.rho.iloc[0] + 1.96 * g.rho_se.iloc[0], "rho", "2016-2024", "41 provincias", "MIVAU; INE ETDP; centroides v5")
    for _, r in gs.iterrows():
        hecho(f"m1b_gsadf_ccaa_{r.ccaa}", f"GSADF ratio precio/IPC alquiler, CCAA {r.ccaa}: p bootstrap (episodios: {r.episodios if isinstance(r.episodios, str) else 'ninguno'})", r.gsadf, None, r.cv95, "estadístico (max = vc 95 %)", "2015T1-2024T4", f"{int(r.n_prov_train)} provincias de entrenamiento", "MIVAU valor tasado; INE IPC alquiler")
    for _, r in fe[(fe.spec == "S2_nucleo8") & (fe.y == "ln_pm2_tasado")].iterrows():
        hecho(f"m1b_fe_precio_{r['var']}", f"Efecto asociado en el valor tasado de {r['var']} (t-1): % por +10 % (logs) o +1 pp", r.efecto_pct_unidad, None, None, "% ; p_wcb=" + str(_f(r.p_wcb, 3)), "2016-2024", "41 provincias de entrenamiento", "MIVAU; INE")
    (OUT / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1))
