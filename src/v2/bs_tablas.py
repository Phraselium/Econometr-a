"""BS · tablas de síntesis (output/v2/tablas/*.csv). Todo se LEE de ficheros versionados de las ramas."""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

import bs_lib as L

# Etiquetas finales fijadas por el orquestador (docs/v2/decisiones.md, «BS · Etiquetas finales»):
# ninguna confirmatoria alcanza ASOCIACIÓN ROBUSTA ni CAUSAL; todas EXPLORATORIO. Se comprueba contra Holm-7.
NIVEL_FIJADO = {f"H{i}": "EXPLORATORIO" for i in range(1, 8)}
ORDEN_NIVEL = {"CAUSAL": 3, "ASOCIACIÓN ROBUSTA": 2, "EXPLORATORIO": 1, "DESCRIPTIVO": 0}


# ------------------------------------------------------------------ (a) hipótesis confirmatorias
def t_hipotesis(holm: pd.DataFrame) -> pd.DataFrame:
    if holm["supera_holm7_5pct"].any():
        raise RuntimeError("Alguna confirmatoria supera Holm-7: las etiquetas fijadas por el orquestador deben revisarse")
    h = L.parse_hipotesis_md()
    hm = holm.set_index("hipotesis")
    ba, bp = L.j("BA/resultado.json"), L.j("BP/resultado.json")
    h1p = L.c("BA/h1_principal.csv").set_index("var")
    h2p = L.c("BV/h2_resultados.csv").query("spec=='H2_principal'").set_index("var")
    h3p = L.c("BI/h3_principal.csv").set_index("resultado")
    h4p = L.c("BO/h4_principal.csv").iloc[0]
    h1s = L.j("BA/h1_sellado.json")["resultado"]["todas"]
    h2s = L.j("BV/h2_sellado.json")["resultado"]["PRINCIPAL_todas"]
    h6s = L.j("BP/h6_sellado.json")["resultado"]
    h7s = L.j("BM/h7_sellado.json")["resultado"]
    n = L.num
    est, icc, dec, nota = {}, {}, {}, {}

    est["H1"] = (f"pob 20-34 {n(h1p.loc['d4_ln_pob_20_34','coef'])}; pob extranjera {n(h1p.loc['d4_ln_pob_extranj','coef'])}; "
                 f"ocupados {n(h1p.loc['d4_ln_ocupados','coef'])}")
    icc["H1"] = (f"20-34 {L.ic(h1p.loc['d4_ln_pob_20_34','ic95_lo'], h1p.loc['d4_ln_pob_20_34','ic95_hi'])}; "
                 f"extranjera {L.ic(h1p.loc['d4_ln_pob_extranj','ic95_lo'], h1p.loc['d4_ln_pob_extranj','ic95_hi'])}")
    dec["H1"] = (f"NO confirmada como conjunción de signos (extranjera con signo opuesto; p_IUT {n(hm.loc['H1','p_dentro_muestra'])}). "
                 f"Hecho fuera de muestra: el modelo con las variables de H1 mejora al AR(4) en la muestra sellada "
                 f"(RMSE {n(h1s['rmse'],4)} vs {n(h1s['rmse_AR4'],4)}; DM-HLN {n(h1s['dm_vs_AR4'],2)}; p {L.pv(h1s['p_vs_AR4'])}) y al ECM v1 (p {L.pv(h1s['p_vs_ECM_v1'])}); "
                 f"p conjunto (máximo) {n(hm.loc['H1','p_hipotesis'])}; no supera Holm-7")
    nota["H1"] = "El p sellado ×7 = %s no convierte la mejora predictiva en asociación robusta de cada coeficiente" % n(7 * h1s["p_vs_AR4"])

    est["H2"] = (f"crédito hipotecario {n(h2p.loc['d4_ln_hipotecas_importe','coef'],4)}; coste de uso × exposición "
                 f"{n(h2p.loc['cu_x_expo','coef'],4)}; ocupados {n(h2p.loc['d4_ln_ocupados','coef'],3)}")
    icc["H2"] = (f"crédito {L.ic(h2p.loc['d4_ln_hipotecas_importe','ic95_inf'], h2p.loc['d4_ln_hipotecas_importe','ic95_sup'],4)}; "
                 f"coste de uso {L.ic(h2p.loc['cu_x_expo','ic95_inf'], h2p.loc['cu_x_expo','ic95_sup'],4)}")
    dec["H2"] = (f"NO confirmada en la muestra sellada: C3 RMSE {n(h2s['rmse'],4)} vs AR(4) {n(h2s['rmse_AR4'],4)}; DM-HLN {n(h2s['dm_vs_AR4'],2)}; "
                 f"p {L.pv(h2s['p_vs_AR4'])} (regla: mejora significativa). Signos dentro de muestra como los esperados (p_IUT {L.pv(hm.loc['H2','p_dentro_muestra'])})")
    nota["H2"] = "Simultaneidad: con el crédito retardado 4 trimestres el coeficiente no es significativo (BV/h2_resultados.csv)"

    est["H3"] = f"β alquiler {n(h3p.loc['alq','b_2sls'],2)}; β compra {n(h3p.loc['pre','b_2sls'],2)}; alquiler − compra {n(h3p.loc['dif','b_2sls'],2)}"
    icc["H3"] = (f"alquiler {L.ic(h3p.loc['alq','ic95_lo'], h3p.loc['alq','ic95_hi'],2)}; "
                 f"contraste {L.ic(h3p.loc['dif','ic95_lo'], h3p.loc['dif','ic95_hi'],2)}")
    dec["H3"] = (f"p_IUT nominal {n(hm.loc['H3','p_hipotesis'],4)} < 0,05 pero no supera Holm-7 ({n(hm.loc['H3','p_holm7'])}); "
                 "el IC95 del contraste incluye 0; GPSS, placebos, timing y submuestras lo debilitan; magnitud no identificada")
    nota["H3"] = "Sin evaluación sellada posible (flujos hasta 2021-2022). Identificación NO superada: CAUSAL descartado"

    est["H4"] = f"β precio {n(h4p['b_precio'])}; β precio × ln suelo {n(h4p['b_inter'])}"
    icc["H4"] = f"precio {L.ic(h4p['lo_precio'], h4p['hi_precio'])}; interacción {L.ic(h4p['lo_inter'], h4p['hi_inter'])}"
    dec["H4"] = (f"p_IUT nominal {n(h4p['p_IUT'],4)} < 0,05 pero no supera Holm-7 ({n(hm.loc['H4','p_holm7'])}); "
                 "falla submuestras 2005-2013 y 2014-2023; el IV no la respalda (J rechaza); placebo de precio futuro significativo")
    nota["H4"] = "Sin evaluación sellada. Asociación exploratoria; elasticidad no estructural"

    est["H5"] = f"τ SDiD 2020Q4-2022Q1 (ln IPC alquiler) {n(bp['estimacion']['efecto_medio_ln_2020Q4_2022Q1'],4,True)}"
    lo, hi = bp["ic95"]["efecto_2020Q4_2022Q1"]
    icc["H5"] = L.ic(lo, hi, 4)
    dec["H5"] = (f"NO confirmada: signo contrario al esperado (p una cola del signo − = {n(hm.loc['H5','p_dentro_muestra'])}; bilateral {n(bp['diagnosticos']['p_permutacion_dos_colas_post1'])}); "
                 "fallan pretendencias y placebo en el tiempo")
    nota["H5"] = "Un nulo no prueba ausencia de efecto: el IPC provincial diluye el tratamiento (BP/resultado.json, notas)"

    sd = h6s["PRINCIPAL_ln_ipc_alquiler"]["sdid"]
    est["H6"] = f"τ SDiD 2024Q3-2026Q2 (ln IPC alquiler) {n(sd['tau'],4,True)}"
    icc["H6"] = L.ic(*sd["ic95"], 4)
    sc, did = h6s["PRINCIPAL_ln_ipc_alquiler"]["sc"], h6s["PRINCIPAL_ln_ipc_alquiler"]["did"]
    dec["H6"] = (f"Cumple la regla pre-registrada nominalmente (τ<0, p de permutación bilateral {n(sd['p_perm_bilateral'],3)}) pero NO supera Holm-7 "
                 f"({n(hm.loc['H6','p_holm7'])}). Discrepancias: control sintético {n(sc['tau'],4,True)} (p {n(sc['p_perm_bilateral'])}) coincide; "
                 f"DiD simple {n(did['tau'],4,True)} (signo contrario); heterogeneidad por provincia; sin 2023Q3-Q4 en el pre p {n(h6s['sec_sin_2023Q3_Q4_en_pre']['sdid']['p_perm_bilateral'])}")
    nota["H6"] = "Efecto estimado por debajo del MDE declarado (≈1,7 %); paquete regulatorio catalán coetáneo: mide «Cataluña 2024-2026», no la zona tensionada aislada"

    rm = {k: (h7s[k]["PRINCIPAL"]["rmse"], h7s[k]["PRINCIPAL"]["rmse_AR4"], h7s[k]["PRINCIPAL"]["p_vs_AR4"]) for k in "ABC"}
    est["H7"] = "; ".join(f"{k}: RMSE {n(v[0],4)} vs AR(4) {n(v[1],4)}" for k, v in rm.items())
    icc["H7"] = "n/a (contraste de predicción)"
    dec["H7"] = ("NO confirmada: ningún objetivo cumple la regla (p_IUT Holm m=3 = "
                 + "; ".join(n(h7s[k]['p_IUT_Holm'], 3) for k in "ABC") + ")")
    nota["H7"] = ("Observación NO pre-registrada, no usada como evidencia: en la ventana sellada nacional (n=8) el ECM v1 tuvo RMSE "
                  f"{n(h7s['A']['PRINCIPAL']['rmse_ECM_v1'],4)} frente a {n(h7s['A']['PRINCIPAL']['rmse_AR4'],4)} del AR(4)")

    filas = []
    for _, r in h.iterrows():
        k = r["hipotesis"]
        filas.append(dict(
            hipotesis=k, rama=r["rama"], enunciado=r["enunciado"], signo_esperado=r["signo_esperado"],
            estimacion=est[k], ic95=icc[k],
            p_dentro_muestra=hm.loc[k, "p_dentro_muestra"], p_sellado=hm.loc[k, "p_sellado"],
            p_hipotesis_preregistrada=hm.loc[k, "p_hipotesis"], p_holm7=hm.loc[k, "p_holm7"],
            decision=dec[k], nivel_evidencia=NIVEL_FIJADO[k], nota=nota[k],
            fuente=hm.loc[k, "fuente"]))
    return pd.DataFrame(filas)


# ------------------------------------------------------------------ (b) modelos fuera de muestra
COLS_B = ["rama", "bloque", "objetivo", "modelo", "tipo_muestra", "muestra", "N", "n_periodos", "RMSE", "MAE", "RMSE_AR4",
          "RMSE_ECM_v1", "DM_vs_AR4", "p_vs_AR4", "DM_vs_ECM_v1", "p_vs_ECM_v1", "p_BH_AR4", "p_BH_ECM_v1", "origen_BH", "fuente", "nota"]


def _f(rama, bloque, objetivo, modelo, tipo, muestra, N, npd, rmse, mae, ra, re_, da, pa, de, pe, bha, bhe, obh, fuente, nota=""):
    return dict(zip(COLS_B, [rama, bloque, objetivo, modelo, tipo, muestra, N, npd, rmse, mae, ra, re_, da, pa, de, pe, bha, bhe, obh, fuente, nota]))


def t_oos() -> pd.DataFrame:
    V = "validacion_entrenamiento"
    F = []
    # --- BA
    d = L.c("BA/oos_h4.csv")
    d["bha"], d["bhe"] = L.bh(d.p_vs_AR4), L.bh(d.p_vs_ECM_v1)
    val_ba = L.j("BA/resultado.json")["fuera_muestra"]["validacion"]
    for _, r in d.iterrows():
        F.append(_f("BA", "H1/alquiler", "Δ4 ln IPC alquiler (panel provincial, 49 prov.)", r.modelo, V, val_ba, r.n, r.n_periodos, r.rmse, r.mae,
                    r.rmse_AR4, r.rmse_ECM_v1, r.dm_vs_AR4, r.p_vs_AR4, r.dm_vs_ECM_v1, r.p_vs_ECM_v1, r.bha, r.bhe,
                    "calculado BS: BH sobre los 4 modelos de BA", "BA/oos_h4.csv",
                    "modelo primario ex ante" if r.primario else ""))
    # --- BV
    mv = "bloques con embargo, h=4, primer test 2012Q1; entrenamiento ≤2024Q2"
    for fich, obj in (("BV/oos_panel.csv", "Δ4 ln valor tasado real (panel provincial, 49 prov.)"),
                      ("BV/oos_nacional.csv", "Δ4 ln valor tasado real (nacional)")):
        d = L.c(fich)
        for _, r in d.iterrows():
            F.append(_f("BV", "H2/compra", obj, r.modelo, V, mv, r.n, r.n_periodos, r.rmse, r.mae, r.rmse_AR4, r.rmse_ECM_v1,
                        r.dm_vs_AR4, r.p_vs_AR4, r.dm_vs_ECM_v1, r.p_vs_ECM_v1, r.p_bh_vs_AR4, r.p_bh_vs_ECM,
                        "fichero de la rama (BH sobre las configuraciones)", fich,
                        "C3 = modelo de H2 enviado al sellado" if r.modelo == "BV_C3" else ""))
    # --- BO
    d = L.c("BO/oos_h4.csv")
    for _, r in d.iterrows():
        F.append(_f("BO", "H4/oferta", f"{r.objetivo}", r.modelo, V, "bloques con embargo, h=4, test 2014Q1-2024Q2", r.n, r.n_periodos, r.rmse, r.mae,
                    r.rmse_AR4, r.rmse_ECM_v1, r.dm_vs_AR4, r.p_vs_AR4, r.dm_vs_ECM_v1, r.p_vs_ECM_v1, r.p_BH, np.nan,
                    "fichero de la rama (BH sobre 6 contrastes vs AR(4))", "BO/oos_h4.csv"))
    # --- BI
    d = L.c("BI/oos_anual.csv")
    d["bha"] = L.bh(d.p_vs_AR4)
    for _, r in d.iterrows():
        F.append(_f("BI", "H3/inmigración", "Δ ln IPC alquiler (panel provincial anual)", r.modelo, V,
                    "anual, orígenes 2013-2020 con embargo de 1 año; sin ECM v1 anual comparable", r.n, r.n_periodos, r.rmse, r.mae,
                    r.rmse_AR4, np.nan, r.dm_vs_AR4, r.p_vs_AR4, np.nan, np.nan, r.bha, np.nan,
                    "calculado BS: BH sobre 2 modelos", "BI/oos_anual.csv",
                    "pseudo-pronóstico: el flujo del año t se publica a mitad de t+1" if "NO pronóstico" in r.modelo else ""))
    # --- BM
    obj = {"A": "ln IPV real (nacional)", "B": "Δ4 ln IPC alquiler (panel provincial)", "C": "Δ4 ln valor tasado real (panel provincial)"}
    d = L.c("BM/tabla_fuera_muestra.csv")
    for _, r in d.iterrows():
        base = r.modelo in ("AR4", "ECM_v1")
        F.append(_f("BM", "H7/modelos", obj[r.objetivo], r.modelo, V, "bloques con embargo, h=4, primer test 2012Q1; entrenamiento ≤2024Q2", r.N, r.n_periodos,
                    r.RMSE, r.MAE, r.RMSE_AR4, r.RMSE_ECM_v1, r.DM_vs_AR4, r.p_vs_AR4, r.DM_vs_ECM_v1, r.p_vs_ECM_v1, r.p_BH_AR4, r.p_BH_ECM_v1,
                    "fichero de la rama (BH sobre las configuraciones del objetivo)", "BM/tabla_fuera_muestra.csv",
                    "línea base" if base else ""))
    d = L.c("BM/lstm_panelB.csv")
    d["bha"] = L.bh(d.p_vs_AR4)
    for _, r in d.iterrows():
        F.append(_f("BM", "bloque 6 (LSTM)", obj["B"], r.modelo, V, "bloques con embargo, h=4, primer test 2012Q1; entrenamiento ≤2024Q2", r.N, np.nan,
                    r.RMSE, np.nan, r.RMSE_AR4, r.RMSE_ECM_v1, r.DM_vs_AR4, r.p_vs_AR4, np.nan, np.nan, r.bha, np.nan,
                    "calculado BS: BH sobre 4 LSTM", "BM/lstm_panelB.csv",
                    f"vs LightGBM: DM {L.num(r.DM_LSTM_vs_GB,2)}, p {L.pv(r.p_LSTM_vs_GB)} (resultado negativo; fuera de H7)"))
    # --- sellada
    h1 = L.j("BA/h1_sellado.json")["resultado"]
    h2 = L.j("BV/h2_sellado.json")["resultado"]
    h7 = L.j("BM/h7_sellado.json")["resultado"]
    S = []

    def sel(rama, bloque, objetivo, modelo, clave, blk, desc, fuente, principal, nota=""):
        S.append((principal, _f(rama, bloque, objetivo, modelo, "sellada_principal" if principal else "sellada_secundaria", desc,
                                blk["n"], blk["n_periodos"], blk["rmse"], blk["mae"], blk["rmse_AR4"], blk.get("rmse_ECM_v1", np.nan),
                                blk["dm_vs_AR4"], blk["p_vs_AR4"], blk.get("dm_vs_ECM_v1", np.nan), blk.get("p_vs_ECM_v1", np.nan),
                                np.nan, np.nan, "", fuente, nota)))

    sell = h1["selladas"]
    d52 = "2024Q3-2026Q2, h=4, 52 provincias (49 de entrenamiento + selladas %s)" % "/".join(sell)
    f1 = "BA/h1_sellado.json"
    sel("BA", "H1/alquiler", obj["B"], "B_AR4_mas_H1", "todas", h1["todas"], d52, f1, True)
    sel("BA", "H1/alquiler", obj["B"], "B_AR4_mas_H1", "train", h1["train_provs"], "2024Q3-2026Q2, 49 provincias de entrenamiento", f1, False)
    sel("BA", "H1/alquiler", obj["B"], "B_AR4_mas_H1", "ventana", h1["selladas_ventana"], "2024Q3-2026Q2, solo provincias selladas", f1, False, "n=24: potencia muy baja")
    sel("BA", "H1/alquiler", obj["B"], "B_AR4_mas_H1", "hist", h1["selladas_toda_historia"], "provincias selladas, toda la historia", f1, False)
    f2 = "BV/h2_sellado.json"
    sel("BV", "H2/compra", obj["C"], "BV_C3", "todas", h2["PRINCIPAL_todas"], d52, f2, True, "no cumple la regla pre-registrada (p ≥ 0,05)")
    sel("BV", "H2/compra", obj["C"], "BV_C3", "a", h2["sec_a_entrenamiento"], "2024Q3-2026Q2, 49 provincias de entrenamiento", f2, False)
    sel("BV", "H2/compra", obj["C"], "BV_C3", "b", h2["sec_b_selladas_ventana"], "2024Q3-2026Q2, solo provincias selladas", f2, False)
    sel("BV", "H2/compra", obj["C"], "BV_C3", "b2", h2["sec_b2_selladas_historia"], "provincias selladas, toda la historia", f2, False)
    sel("BV", "H2/compra", obj["C"], "BV_C3", "c", h2["sec_c_ecm_v1_referencia_entrenamiento"], "2024Q3-2026Q2, 49 provincias de entrenamiento (referencia ECM v1)", f2, False)
    f7 = "BM/h7_sellado.json"
    dd = {"A": "2024Q3-2026Q2, nacional (n=8)", "B": d52, "C": d52}
    for k in "ABC":
        sel("BM", "H7/modelos", obj[k], h7["seleccion"][k], k, h7[k]["PRINCIPAL"], dd[k], f7, True,
            "ECM v1 mejor que el modelo (DM<0 vs ECM): observación no pre-registrada, no se usa como evidencia" if k == "A" else "")
        for sk, desc in (("sec_a_entrenamiento_49", "2024Q3-2026Q2, 49 provincias de entrenamiento"),
                         ("sec_b_selladas_ventana", "2024Q3-2026Q2, solo provincias selladas"),
                         ("sec_b2_selladas_historia", "provincias selladas, toda la historia")):
            if sk in h7[k]:
                sel("BM", "H7/modelos", obj[k], h7["seleccion"][k], k, h7[k][sk], desc, f7, False)
    sd = pd.DataFrame([x[1] for x in S])
    pri = [i for i, x in enumerate(S) if x[0]]
    sd.loc[pri, "p_BH_AR4"] = L.bh(sd.loc[pri, "p_vs_AR4"]).values
    sd.loc[pri, "p_BH_ECM_v1"] = L.bh(sd.loc[pri, "p_vs_ECM_v1"]).values
    sd.loc[pri, "origen_BH"] = "calculado BS: BH sobre los 5 contrastes sellados principales (H1, H2, H7-A/B/C)"
    out = pd.concat([pd.DataFrame(F), sd], ignore_index=True)
    return out[COLS_B]


# ------------------------------------------------------------------ (c) contribuciones por periodo
NO_CAUSA = {"observado", "explicado_familias", "comun_efectos_tiempo", "residuo"}


def _excl(lo, hi):
    return (lo > 0) or (hi < 0)


def t_contrib() -> pd.DataFrame:
    d = L.c("BD/tabla_resumen.csv")
    filas = []
    for _, r in d.iterrows():
        e1, e2 = _excl(r.ic95_inf_M1, r.ic95_sup_M1), _excl(r.ic95_inf_M2, r.ic95_sup_M2)
        s1, s2 = np.sign(r.contrib_pp_M1), np.sign(r.contrib_pp_M2)
        if r.familia in NO_CAUSA:
            clase, nr = "contable (identidad observado = familias + común + residuo)", False
        elif e1 and e2 and s1 == s2:
            clase, nr = "replica en M1 y M2 (IC95 excluye 0, mismo signo)", False
        elif e1 and e2:
            clase, nr = "NO ROBUSTO: signos opuestos entre M1 y M2", True
        elif e1 or e2:
            clase, nr = "NO ROBUSTO: IC95 excluye 0 solo en %s" % ("M1" if e1 else "M2"), True
        else:
            clase, nr = "sin señal: IC95 incluye 0 en M1 y M2", False
        filas.append(dict(
            periodo=r.periodo, familia=r.familia, mercado=r.mercado,
            contrib_pp_M1=r.contrib_pp_M1, ic95_inf_M1=r.ic95_inf_M1, ic95_sup_M1=r.ic95_sup_M1,
            contrib_pp_M2=r.contrib_pp_M2, ic95_inf_M2=r.ic95_inf_M2, ic95_sup_M2=r.ic95_sup_M2,
            observado_pp=r.observado_pp, pct_observado_M1=r.pct_observado_M1, pct_observado_M2=r.pct_observado_M2,
            nivel_evidencia=str(r.nivel_evidencia).split(" (")[0], robustez_M1_M2=clase, no_robusto=nr,
            fuente="BD/tabla_resumen.csv"))
    o = pd.DataFrame(filas)
    assert set(o.nivel_evidencia) <= {"DESCRIPTIVO", "EXPLORATORIO"}
    return o


# ------------------------------------------------------------------ (d) ranking de factores
def _bd(d, periodo, fam, mer):
    r = d[(d.periodo == periodo) & (d.familia == fam) & (d.mercado == mer)].iloc[0]
    return r


def _bd_repl(d, periodo, fam, mer):
    r = _bd(d, periodo, fam, mer)
    return bool(_excl(r.ic95_inf_M1, r.ic95_sup_M1) and _excl(r.ic95_inf_M2, r.ic95_sup_M2) and np.sign(r.contrib_pp_M1) == np.sign(r.contrib_pp_M2))


def t_ranking(holm: pd.DataFrame) -> pd.DataFrame:
    """Criterios (True/False/None=no evaluable): A p ajustado <0,05; B signo estable en submuestras/periodos;
    C mejora predictiva significativa en validación de entrenamiento (p<0,05 vs AR(4)); D mejora en la muestra sellada
    (p<0,05 vs AR(4)); E contribución de BD replicada en M1 y M2 (desde 2020). Puntuación = nº de criterios cumplidos.
    El nivel NUNCA supera el fijado por el orquestador (EXPLORATORIO)."""
    ba = L.j("BA/resultado.json")
    hm = holm.set_index("hipotesis")
    h1p = L.c("BA/h1_principal.csv").set_index("var")
    pco = L.c("BA/periodos_coef.csv")
    oosA = L.c("BA/oos_h4.csv").set_index("modelo")
    h1s = L.j("BA/h1_sellado.json")["resultado"]["todas"]
    bd = L.c("BD/tabla_resumen.csv")
    tur = L.c("BA/turismo.csv").set_index("spec")
    fam = L.c("BA/familias_holm_bh.csv")
    bi_id = L.c("BI/h3_identificacion.csv")
    bi = L.j("BI/resultado.json")
    oosI = L.c("BI/oos_anual.csv").iloc[0]
    h2 = L.c("BV/h2_resultados.csv")
    arb = L.c("BV/arbitraje_lp.csv")
    oosV = L.c("BV/oos_panel.csv").set_index("cfg")
    oosO = L.c("BO/oos_h4.csv").set_index("modelo")
    suelo = L.c("BO/suelo_proyecciones_locales.csv")
    ta = L.c("BD/tabla_resumen.csv")
    h6 = L.j("BP/h6_sellado.json")["resultado"]
    bp = L.j("BP/resultado.json")["diagnosticos"]
    N = L.num

    def sg(x):
        return np.sign(x)

    def bdsg(per, f, m):
        r = _bd(bd, per, f, m)
        return sg(r.contrib_pp_M1) == sg(r.contrib_pp_M2)

    filas = []

    def add(mercado, fam_, nivel, crit, por_que, fuentes):
        keys = ["A_p_ajustado", "B_signo_estable", "C_oos_entrenamiento", "D_sellado", "E_bd_M1_M2"]
        ev = [crit.get(k) for k in keys]
        filas.append(dict(familia=fam_, mercado=mercado, evidencia_mas_alta=nivel,
                          **{k: ("n/a" if v is None else bool(v)) for k, v in zip(keys, ev)},
                          criterios_cumplidos=sum(v is True for v in ev), criterios_evaluables=sum(v is not None for v in ev),
                          tope_orquestador="EXPLORATORIO", por_que=por_que, fuentes=fuentes))

    # ---------------- alquiler
    p2034 = h1p.loc["d4_ln_pob_20_34"]
    add("alquiler", "Demografía: población 20-34 (BA)", "EXPLORATORIO", dict(
        A_p_ajustado=fam.query("contraste=='d4_ln_pob_20_34'").p_ajustado.iloc[0] < .05,
        B_signo_estable=ba["diagnosticos"]["signos_positivos_en_todas_las_submuestras"]["d4_ln_pob_20_34"],
        C_oos_entrenamiento=oosA.loc["B_AR4_mas_H1", "p_vs_AR4"] < .05, D_sellado=None,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "demografia_20_34", "alquiler")),
        f"Coef. {N(p2034.coef)} (Holm intra-H1 {N(p2034.p_holm_H1,4)}), + en todas las submuestras; el modelo no mejora al AR(4) en entrenamiento "
        f"(p {L.pv(oosA.loc['B_AR4_mas_H1','p_vs_AR4'])}); en BD desde 2020 no replica entre M1 y M2; H1 (conjunta) no supera Holm-7 ({N(hm.loc['H1','p_holm7'])}): tope EXPLORATORIO",
        "BA/h1_principal.csv; BA/familias_holm_bh.csv; BA/resultado.json; BA/oos_h4.csv; BD/tabla_resumen.csv; BS/holm7.csv")
    add("alquiler", "Demografía: modelo conjunto de H1 (valor predictivo)", "EXPLORATORIO", dict(
        C_oos_entrenamiento=oosA.loc["B_AR4_mas_H1", "p_vs_AR4"] < .05, D_sellado=h1s["p_vs_AR4"] < .05),
        f"Hecho fuera de muestra: en la muestra sellada mejora al AR(4) (RMSE {N(h1s['rmse'],4)} vs {N(h1s['rmse_AR4'],4)}; p {L.pv(h1s['p_vs_AR4'])}); "
        f"×7 = {N(7*h1s['p_vs_AR4'])}; en entrenamiento no mejoraba (p {L.pv(oosA.loc['B_AR4_mas_H1','p_vs_AR4'])}). No se atribuye a un coeficiente concreto; H1 conjunta EXPLORATORIO",
        "BA/h1_sellado.json; BA/oos_h4.csv; BS/holm7.csv")
    pe = h1p.loc["d4_ln_pob_extranj"]
    add("alquiler", "Población extranjera (BA, MCO con FE)", "EXPLORATORIO", dict(
        A_p_ajustado=fam.query("contraste=='d4_ln_pob_extranj'").p_ajustado.iloc[0] < .05,
        B_signo_estable=ba["diagnosticos"]["signos_positivos_en_todas_las_submuestras"]["d4_ln_pob_extranj"],
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "demografia_extranj", "alquiler")),
        f"Coef. {N(pe.coef)} (p Holm {N(pe.p_holm_H1)}): signo opuesto al esperado; IC95 incluye 0; no replica en BD", "BA/h1_principal.csv; BA/resultado.json; BD/tabla_resumen.csv")
    bia = bi_id.query("spec=='principal' and res=='alq'").iloc[0]
    g_extr = bi_id[(bi_id.spec == "gpss_extr02") & (bi_id.res == "alq")].p_wcb_1c.iloc[0]
    s_1521 = bi_id[(bi_id.spec == "sub_2015-2021") & (bi_id.res == "alq")].p_wcb_1c.iloc[0]
    add("alquiler", "Inmigración instrumentada, shift-share 2002 (BI)", "EXPLORATORIO", dict(
        A_p_ajustado=bia.p_wcb_1c < .05, B_signo_estable=bool(g_extr < .05 and s_1521 < .05),
        C_oos_entrenamiento=oosI.p_vs_AR4 < .05),
        f"β alquiler {N(bia.b,2)} (p WCB 1 cola {N(bia.p_wcb_1c)}) pero con GPSS de extranjeros 2002 (p {N(g_extr)}) y 2015-2021 "
        f"(p {N(s_1521)}) pierde significación; placebos de alquiler pasado rechazan; magnitud no identificada; H3 no supera Holm-7 ({N(hm.loc['H3','p_holm7'])})",
        "BI/h3_identificacion.csv; BI/oos_anual.csv; BS/holm7.csv")
    sp = pco[pco.x == "d4_ln_ocupados"].coef
    add("alquiler", "Empleo (ocupados)", "EXPLORATORIO", dict(
        A_p_ajustado=ba["p_ajustado"]["p_boot_bruto"]["d4_ln_ocupados"] < .05, B_signo_estable=bool((sg(sp) == sg(sp.iloc[0])).all()),
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "empleo_renta", "alquiler")),
        f"Coef. {N(h1p.loc['d4_ln_ocupados','coef'],4)} (p bootstrap {N(ba['p_ajustado']['p_boot_bruto']['d4_ln_ocupados'])}); el signo cambia entre periodos", "BA/h1_principal.csv; BA/periodos_coef.csv; BA/resultado.json")
    pmD = oosA.loc["D_AR4_H1_oferta_cu"]
    add("alquiler", "Crédito, tipos y coste de uso", "EXPLORATORIO", dict(
        C_oos_entrenamiento=pmD.p_vs_AR4 < .05, E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "credito_tipos_cu", "alquiler")),
        f"Coste de uso = una serie nacional única (IC subestimados, sin ajuste); el modelo D no mejora al AR(4) (p {L.pv(pmD.p_vs_AR4)}); BD sin señal", "BA/oos_h4.csv; BD/tabla_resumen.csv; BA/signos_vs_literatura.csv")
    add("alquiler", "Oferta (terminadas)", "EXPLORATORIO", dict(
        C_oos_entrenamiento=oosA.loc["C_AR4_H1_oferta", "p_vs_AR4"] < .05,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "oferta", "alquiler")),
        f"Contribuciones del orden de décimas de pp; signo + en P1 (contrario al esperado); el modelo C no mejora al AR(4) (p {L.pv(oosA.loc['C_AR4_H1_oferta','p_vs_AR4'])})", "BA/oos_h4.csv; BA/signos_vs_literatura.csv; BD/tabla_resumen.csv")
    add("alquiler", "Política: tope de rentas de Cataluña (H5)", "EXPLORATORIO", dict(
        A_p_ajustado=hm.loc["H5", "p_holm7"] < .05, B_signo_estable=bp["pretendencias_ok"] and bp["placebo_tiempo_ok"],
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "politica", "alquiler")),
        f"Signo contrario al esperado (p una cola − = {N(hm.loc['H5','p_dentro_muestra'])}); fallan pretendencias y placebo en el tiempo (p {N(bp['placebo_tiempo_2018Q4_p'])})", "BP/resultado.json; BS/holm7.csv; BD/tabla_resumen.csv")
    dc = h6["DECISION"]
    add("alquiler", "Política: zonas tensionadas de Cataluña (H6)", "EXPLORATORIO", dict(
        A_p_ajustado=hm.loc["H6", "p_holm7"] < .05, B_signo_estable=bool(h6["PRINCIPAL_ln_ipc_alquiler"]["did"]["tau"] < 0 and all(v["tau"] < 0 for v in h6["sec_tratadas_solas"].values())),
        D_sellado=dc["cumple_regla"]),
        f"τ SDiD {N(dc['tau'],4,True)}, p nominal {N(dc['p_perm_bilateral'])} (cumple la regla), Holm-7 {N(hm.loc['H6','p_holm7'])}; DiD simple de signo contrario y Tarragona positiva",
        "BP/h6_sellado.json; BS/holm7.csv")
    pm, pp_, pl = tur.loc["T_muni_base"], tur.loc["T_prov_dVUTpc"], tur.loc["T_prov_dlnVUT"]
    bht = fam[fam.familia.str.startswith("F4_turismo")].p_ajustado
    add("alquiler", "Viviendas turísticas (VUT)", "EXPLORATORIO", dict(
        A_p_ajustado=bool((bht < .05).all()), B_signo_estable=None,
        E_bd_M1_M2=None),
        f"Depende de la métrica: municipal p {N(pm.p)}, provincial Δ ln VUT p {N(pl.p)}, provincial Δ por 1.000 hab. p {N(pp_.p,4)} (N temporal 6); causalidad inversa no descartada", "BA/turismo.csv; BA/familias_holm_bh.csv")
    a_al = arb[(arb.h == 4) & (arb.outcome == "y_alq")].set_index("desv")
    add("alquiler", "Precio/alquiler (arbitraje, ratio vs media)", "EXPLORATORIO", dict(
        A_p_ajustado=a_al.loc["media_total", "p_holm_m16"] < .05, B_signo_estable=bool(sg(a_al.loc["media_total", "coef"]) == sg(a_al.loc["media_expansiva", "coef"]))),
        f"Ratio por encima de la media predice más alquiler (h=4: {N(a_al.loc['media_total','coef'])}, Holm {N(a_al.loc['media_total','p_holm_m16'])}); con media expansiva Holm {N(a_al.loc['media_expansiva','p_holm_m16'])}; reversión mecánica posible", "BV/arbitraje_lp.csv")
    cm = _bd(bd, "P3-P4 (desde 2020)", "comun_efectos_tiempo", "alquiler")
    add("alquiler", "No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…)", "DESCRIPTIVO", dict(),
        f"Desde 2020 el componente común es {N(cm.contrib_pp_M1,2)} pp de {N(cm.observado_pp,2)} pp observados en M1 ({N(cm.pct_observado_M1,0)} %): las familias medidas no explican la subida", "BD/tabla_resumen.csv")
    # ---------------- compra
    c_cr = h2[(h2.spec == "H2_principal")].set_index("var")
    sub = h2[h2.spec.isin(["H2_sub_hasta2013", "H2_sub_desde2014"])]
    cu_sub = sub[sub["var"] == "cu_x_expo"]
    cr_sub = sub[sub["var"] == "d4_ln_hipotecas_importe"]
    h2s = L.j("BV/h2_sellado.json")["resultado"]["PRINCIPAL_todas"]
    holm2 = L.j("BV/resultado.json")["p_ajustado"]["holm_m2_wcb"]
    add("compra", "Crédito hipotecario nuevo", "EXPLORATORIO", dict(
        A_p_ajustado=holm2["d4_ln_hipotecas_importe"] < .05, B_signo_estable=bool((cr_sub.p < .05).all()),
        C_oos_entrenamiento=oosV.loc["C1", "p_vs_AR4"] < .05, D_sellado=h2s["p_vs_AR4"] < .05,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "credito_tipos_cu", "compra")),
        f"Coef. {N(c_cr.loc['d4_ln_hipotecas_importe','coef'],4)} (Holm m=2 {N(holm2['d4_ln_hipotecas_importe'],4)}); no significativo en 2014-2024 (p {N(cr_sub.p.iloc[-1])}) ni con crédito retardado; "
        f"H2 no se confirma en el sellado (p {L.pv(h2s['p_vs_AR4'])}); simultaneidad", "BV/h2_resultados.csv; BV/resultado.json; BV/h2_sellado.json; BV/oos_panel.csv; BD/tabla_resumen.csv")
    add("compra", "Coste de uso × exposición hipotecaria", "EXPLORATORIO", dict(
        A_p_ajustado=holm2["cu_x_expo"] < .05, B_signo_estable=bool((cu_sub.p < .05).all()),
        C_oos_entrenamiento=oosV.loc["C3", "p_vs_AR4"] < .05, D_sellado=h2s["p_vs_AR4"] < .05,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "credito_tipos_cu", "compra")),
        f"Coef. {N(c_cr.loc['cu_x_expo','coef'],4)} (Holm m=2 {L.pv(holm2['cu_x_expo'])}), significativo en ambas submuestras; el modelo C3 es peor que el AR(4) en entrenamiento (p {L.pv(oosV.loc['C3','p_vs_AR4'])}) y no mejora en el sellado; "
        "solo se identifica el diferencial por exposición (no aleatoria); en BD M2 el coste de uso nacional sale con signo contrario", "BV/h2_resultados.csv; BV/resultado.json; BV/oos_panel.csv; BV/h2_sellado.json; BD/tabla_resumen.csv")
    add("compra", "Empleo (ocupados)", "EXPLORATORIO", dict(
        A_p_ajustado=False, C_oos_entrenamiento=oosV.loc["C4", "p_vs_AR4"] < .05,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "empleo_renta", "compra")),
        f"Coef. {N(c_cr.loc['d4_ln_ocupados','coef'])}; p bootstrap {N(c_cr.loc['d4_ln_ocupados','p_wcb'])} sin ajuste (no forma parte de Holm de H2); el modelo con ocupados no mejora al AR(4)",
        "BV/h2_resultados.csv; BV/oos_panel.csv; BD/tabla_resumen.csv")
    dm_ = _bd(bd, "P3-P4 (desde 2020)", "demografia", "compra")
    add("compra", "Demografía (20-34 y extranjera)", "EXPLORATORIO", dict(
        B_signo_estable=bool(bdsg("P3-P4 (desde 2020)", "demografia", "compra")), E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "demografia", "compra")),
        f"En BD desde 2020 la contribución cambia de signo entre M1 ({N(dm_.contrib_pp_M1,2)} pp) y M2 ({N(dm_.contrib_pp_M2,2)} pp): sin atribución estable", "BD/tabla_resumen.csv")
    bic = bi_id.query("spec=='principal' and res=='pre'").iloc[0]
    add("compra", "Inmigración instrumentada (BI)", "EXPLORATORIO", dict(
        A_p_ajustado=bic.p_wcb_1c < .05, B_signo_estable=False),
        f"β compra {N(bic.b,2)} (p WCB 1 cola {N(bic.p_wcb_1c)}), IC95 muy ancho; el signo cambia entre variantes", "BI/h3_identificacion.csv; BI/resultado.json")
    add("compra", "Oferta (terminadas / iniciadas)", "EXPLORATORIO", dict(
        C_oos_entrenamiento=oosO.loc["P4_ini_suelo_term", "p_vs_AR4"] < .05,
        E_bd_M1_M2=_bd_repl(bd, "P3-P4 (desde 2020)", "oferta", "compra")),
        f"Contribución ≈ 0 en BD; ningún modelo de precio con oferta mejora al AR(4) (P4 p {L.pv(oosO.loc['P4_ini_suelo_term','p_vs_AR4'])})", "BO/oos_h4.csv; BD/tabla_resumen.csv")
    mh = suelo[suelo.variante == "media4T"]
    add("compra", "Suelo (precio del suelo)", "EXPLORATORIO", dict(
        A_p_ajustado=bool(suelo[suelo.variante == "crudo"].p_Holm.min() < .05), C_oos_entrenamiento=oosO.loc["P2_suelo", "p_vs_AR4"] < .05),
        f"Serie cruda sin señal (mín. Holm {N(suelo[suelo.variante=='crudo'].p_Holm.min(),2)}); solo la variante «media4T», añadida a posteriori, da Holm {N(mh.p_Holm.min())} en P4 (h=6); P2 no mejora al AR(4) (p {L.pv(oosO.loc['P2_suelo','p_vs_AR4'])})", "BO/suelo_proyecciones_locales.csv; BO/oos_h4.csv")
    a_pr = arb[(arb.h == 4) & (arb.outcome == "y_precio")].set_index("desv")
    add("compra", "Precio/alquiler (arbitraje, ratio vs media)", "EXPLORATORIO", dict(
        A_p_ajustado=a_pr.loc["media_total", "p_holm_m16"] < .05, B_signo_estable=bool(sg(a_pr.loc["media_total", "coef"]) == sg(a_pr.loc["media_expansiva", "coef"]))),
        f"Ratio por encima de la media predice menos crecimiento del precio (h=4: {N(a_pr.loc['media_total','coef'])}, Holm {L.pv(a_pr.loc['media_total','p_holm_m16'])}); con media expansiva {N(a_pr.loc['media_expansiva','coef'])} (Holm {N(a_pr.loc['media_expansiva','p_holm_m16'])}); reversión mecánica posible", "BV/arbitraje_lp.csv")
    cm = _bd(bd, "P3-P4 (desde 2020)", "comun_efectos_tiempo", "compra")
    add("compra", "No explicado: efectos comunes de tiempo (tipos, expectativas, inflación…)", "DESCRIPTIVO", dict(),
        f"Desde 2020 el real cae {N(cm.observado_pp,2)} pp; el común es {N(cm.contrib_pp_M1,2)} pp en M1 y {N(cm.contrib_pp_M2,2)} pp en M2: sin atribución estable", "BD/tabla_resumen.csv")
    dn = L.c("BO/deficit_nacional.csv")
    r0 = dn.iloc[0]
    add("ambos", "Déficit acumulado de vivienda (oferta − hogares)", "DESCRIPTIVO", dict(),
        f"EPA corregida 2021Q1-2024Q2: {L.entero(r0.deficit)} sin protegida; no comparable con el periodo 2021-2025 del BdE; la protegida incluye supuestos en la ilustración", "BO/deficit_nacional.csv")
    o = pd.DataFrame(filas)
    assert (o.evidencia_mas_alta.map(ORDEN_NIVEL) <= ORDEN_NIVEL["EXPLORATORIO"]).all()
    o["_n"] = o.evidencia_mas_alta.map(ORDEN_NIVEL)
    o = o.sort_values(["_n", "criterios_cumplidos", "criterios_evaluables"], ascending=[False, False, True], kind="stable").drop(columns="_n")
    o.insert(0, "rango", range(1, len(o) + 1))
    return o.reset_index(drop=True)


# ------------------------------------------------------------------ (e) referencias
CITAS = [  # (clave en el informe, regex sobre la primera columna / entrada de docs/literatura.md)
    r"^Harvey, Leybourne y Newbold \(1997\)", r"^Diebold y Mariano \(1995\)", r"^Arkhangelsky et al\. \(2021\)",
    r"^Abadie, Diamond y Hainmueller \(2010\)", r"^Goldsmith-Pinkham et al\. \(2020\)", r"^Borusyak, Hull y Jaravel \(2022\)",
    r"^Adão, Kolesár y Morales \(2019\)", "JAEGER", "ROODMAN", r"^Webb \(2023\)", r"^Montiel Olea y Pflueger \(2013\)",
    r"^Chernozhukov et al\. \(2018\)", r"^Athey, Tibshirani y Wager \(2019\)", r"^Giannone, Lenza y Primiceri \(2015\)",
    r"^Primiceri \(2005\)", r"^Del Negro y Primiceri \(2015\)", r"^Jordà \(2005\)", r"^Belloni, Chernozhukov y Hansen \(2014\)",
    r"^Zou y Hastie \(2005\)", r"^Apley y Zhu \(2020\)", r"^Hochreiter y Schmidhuber \(1997\)", r"^Lundberg y Lee \(2017\)",
    r"^Ke et al\. \(2017\)", r"^Poterba \(1984\)", r"^Khametshin, López Rodríguez y Pérez García \(2024\)", r"^Saiz \(2007\)",
    r"^Caldera y Johansson \(2013\)", r"^Cavalleri, Cournède y Özsöğüt \(2019\)", r"^Garcia-López et al\. \(2020\)", "JOFRE", "BDE",
]


def _tabla_lit(lineas):
    out = []
    for ln in lineas:
        if ln.startswith("| ") and ln.count("|") >= 6 and not ln.startswith("| Referencia") and not ln.startswith("|---"):
            p = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(p) == 5:
                out.append(p)
    return out


def t_refs() -> pd.DataFrame:
    txt = (L.R / "docs" / "literatura.md").read_text().splitlines()
    i0 = next(i for i, ln in enumerate(txt) if ln.startswith("# PARTE v2"))
    filas = _tabla_lit(txt[i0:])
    anexoC = "\n".join(txt[next(i for i, ln in enumerate(txt) if ln.startswith("## Anexo v2-C")):])
    esp = []
    for clave in CITAS:
        if clave == "JAEGER":
            bloque = anexoC.split("### C-1.")[1].split("### C-2.")[0]
            esp.append(["Jaeger, Ruist y Stuhler (2018), NBER WP 24285", re.search(r"DOI (10\.\S+?)[ \)]", bloque).group(1),
                        "NBER Working Paper", "sin cuartil (WP)", "VERIFICADA como documento de trabajo (DOI comprobado); publicación en revista NO VERIFICADA"])
        elif clave == "ROODMAN":
            bloque = anexoC.split("### C-2.")[1]
            esp.append(["Roodman, Nielsen, MacKinnon y Webb (2019), 19(1), 4-60", re.search(r"DOI (10\.\S+?) \(", bloque).group(1),
                        "The Stata Journal", "cuartil no verificado", "VERIFICADA (DOI en Crossref); cuartil no verificado"])
        elif clave == "JOFRE":
            doi_j = "10.1016/j.regsciurbeco.2023.103916"
            en_lit = any(doi_j in x and "**VERIFICADA**" in x for x in txt)   # anexo v2-D de docs/literatura.md
            esp.append(["Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916",
                        doi_j if en_lit else "no consta en docs/literatura.md",
                        "Regional Science and Urban Economics", "cuartil no verificado",
                        "VERIFICADA (DOI en Crossref); cuartil no verificado" if en_lit else
                        "NO VERIFICADA (no figura en docs/literatura.md; cifra solo según el resumen publicado, citada por la rama BP)"])
        elif clave == "BDE":
            ln = next(x for x in txt if x.startswith("- Banco de España (2026). *Informe Anual 2025*"))
            esp.append(["Banco de España (2026), Informe Anual 2025", re.search(r"DOI (10\.\S+?)\.", ln).group(1), "Banco de España (informe institucional)",
                        "n/a (informe)", "VERIFICADA (PDF oficial, cap. 2)"])
        else:
            m = [f for f in filas if re.search(clave, f[0])]
            if not m:
                raise KeyError(f"referencia no encontrada en docs/literatura.md: {clave}")
            esp.append(m[0])
    o = pd.DataFrame(esp, columns=["referencia", "doi", "revista", "cuartil", "estado_literatura_md"])
    def est(s):
        if "NO VERIFICADA" in s and not s.startswith("VERIFICADA"):
            return "NO VERIFICADA"
        if s.startswith("VERIFICADA como documento de trabajo"):
            return "VERIFICADA (WP; revista NO VERIFICADA)"
        if s.startswith("DOI VERIFICADO"):
            return "VERIFICADA (parcial: DOI sí; autores y nº no confirmados)"
        return "VERIFICADA"
    o["estado"] = o.estado_literatura_md.map(est)
    o["cuartil_no_verificado"] = o.cuartil.str.contains("no verificado") | o.estado_literatura_md.str.contains("cuartil no verificado")
    o["cuartil_anyo_publ_no_comprobado"] = o.cuartil.str.contains("no comprobado")
    o["fuente"] = "docs/literatura.md (parte v2, anexos v2-B y v2-C; v1 para Banco de España)"
    return o


# ------------------------------------------------------------------ (f) registro v2
def t_registro(smoke: bool = False) -> tuple[pd.DataFrame, dict]:
    partes = []
    for rama in L.RAMAS:
        d = L.c(f"{rama}/registro.csv")
        if smoke:
            d = d.head(5)
        d.insert(0, "rama", rama)
        partes.append(d)
    r = pd.concat(partes, ignore_index=True)
    es_pres = r.modelo_id.astype(str).str.endswith("_PRESUPUESTO")
    total = int((~es_pres).sum())
    r["es_especificacion"] = ~es_pres
    r["n_total_especificaciones_v2"] = total
    por_rama = r[~es_pres].groupby("rama").size().reindex(L.RAMAS).to_dict()
    return r, {"total": total, "por_rama": {k: int(v) for k, v in por_rama.items()}, "filas_presupuesto_excluidas": int(es_pres.sum())}
