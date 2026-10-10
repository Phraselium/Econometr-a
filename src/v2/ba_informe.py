"""Rama BA: tablas finales (Holm/BH, signos vs literatura), resultado.json y resumen.md.
Todo se genera a partir de los resultados de ba_run.py (sin cifras escritas a mano)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ba_lib as bl  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import econ_utils as eu  # noqa: E402
import v2_common as vc  # noqa: E402


def pf(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def _pp(x):
    return "n/d" if x is None or not np.isfinite(x) else f"{100 * x:.2f} pp"


def escribir(OUT, r_h1, holm, signos, robdf, k1, per_t, per_w, cont, c2, c4, tur, tab, rb, LOG):
    nm = r_h1["names"]
    co = dict(zip(nm, r_h1["beta"]))
    ic = {n: [float(r_h1["lo"][i]), float(r_h1["hi"][i])] for i, n in enumerate(nm)}
    pbt = r_h1["p_boot"]
    # ---------------- familias de contrastes
    fam = []
    for v, p in holm.items():
        fam.append(dict(familia="F1_H1_contrastes_clave(Holm)", contraste=v, p_bruto=pbt[v], p_ajustado=p,
                        metodo="Holm (p wild cluster bootstrap Webb 9.999, bilateral)"))
    pp = per_t.set_index("var")
    for v in pp.index:
        fam.append(dict(familia="F2_coef_por_periodo(12)", contraste=v, p_bruto=pp.loc[v, "p"],
                        p_ajustado=pp.loc[v, "q_BH"], metodo="BH (q); Holm en periodos_coef.csv"))
    ps = {r["modelo"]: r["p_vs_AR4"] for _, r in tab.iterrows()}
    for k, v in eu.holm(ps).items():
        fam.append(dict(familia="F3_OOS_DM_vs_AR4(4)", contraste=k, p_bruto=ps[k], p_ajustado=v, metodo="Holm"))
    t_m = tur[(tur["spec"].isin(["T_muni_base", "T_prov_dlnVUT", "T_prov_dVUTpc"])) &
              (tur["var"].isin(["dvut", "d4_ln_vut_viviendas", "d4_vut_pc"]))]
    qv = bl.bh(dict(zip(t_m["spec"], t_m["p"])))
    for _, r in t_m.iterrows():
        fam.append(dict(familia="F4_turismo(3)", contraste=r["spec"], p_bruto=r["p"], p_ajustado=qv[r["spec"]],
                        metodo="BH"))
    famdf = pd.DataFrame(fam)
    for c in ("p_bruto", "p_ajustado"):
        famdf[c] = famdf[c].astype(float).round(10)
    famdf.to_csv(OUT / "familias_holm_bh.csv", index=False)

    # ---------------- signos vs literatura
    def g(df, spec, var, col="coef"):
        s = df[(df["spec"] == spec) & (df["var"] == var)]
        return float(s[col].iloc[0]) if len(s) else np.nan
    sf = robdf[(robdf["submuestra"] == "variante_sin_FE_tiempo")].set_index("var")
    c2i = c2.set_index("var")
    sig = [
        dict(variable="Δ4 ln pob 20-34", signo_esperado="+", fuente="Khametshin et al. (2024, BdE DO 2432); hipotesis.md",
             estimacion=co["d4_ln_pob_20_34"], p_ajustado=holm["d4_ln_pob_20_34"], modelo="H1 (FE prov+trim; Holm)"),
        dict(variable="Δ4 ln pob extranjera", signo_esperado="+",
             fuente="Khametshin et al. (2024); Helfer et al. (2023, Suiza); Torres-Téllez y Montero-Soler (2023, resumen secundario)",
             estimacion=co["d4_ln_pob_extranj"], p_ajustado=holm["d4_ln_pob_extranj"], modelo="H1 (FE prov+trim; Holm)"),
        dict(variable="Δ4 ln pob extranjera", signo_esperado="+", fuente="idem (variante sin FE de tiempo)",
             estimacion=float(sf.loc["d4_ln_pob_extranj", "coef"]), p_ajustado=float(sf.loc["d4_ln_pob_extranj", "p"]),
             modelo="H1 sin FE de tiempo (p bruto cluster)"),
        dict(variable="Δ4 ln ocupados", signo_esperado="+", fuente="hipotesis.md (signos esperados)",
             estimacion=co["d4_ln_ocupados"], p_ajustado=pbt["d4_ln_ocupados"], modelo="H1 (p bootstrap, sin ajuste: no clave)"),
        dict(variable="oferta: terminadas/1.000 hab. (Δ4 ln, retardo 4T)", signo_esperado="-",
             fuente="hipotesis.md; Khametshin et al. (demanda > oferta)",
             estimacion=float(c2i.loc["x_oferta_l4__P2", "coef"]), p_ajustado=float(c2i.loc["x_oferta_l4__P2", "p"]),
             modelo="C2 (P2; sin FE de tiempo; p bruto)"),
        dict(variable="coste de uso (Δ4 pp, nacional)", signo_esperado="ambiguo (+ si sustitución compra→alquiler)",
             fuente="Khametshin et al. (2024): prudencia crediticia desplaza demanda al alquiler; Garriga et al. (2019)",
             estimacion=float(c2i.loc["x_cu__P2", "coef"]), p_ajustado=float(c2i.loc["x_cu__P2", "p"]),
             modelo="C2 (P2; serie temporal única; p bruto)"),
        dict(variable="viviendas turísticas (Δ por 1.000 uu, municipal 2020→23)", signo_esperado="+",
             fuente="García-López et al. (2020, JUE; Barcelona)", estimacion=g(tur, "T_muni_base", "dvut"),
             p_ajustado=float(qv["T_muni_base"]), modelo="muni, FE prov (BH)"),
        dict(variable="viviendas turísticas (Δ por 1.000 hab., provincial)", signo_esperado="+", fuente="idem",
             estimacion=g(tur, "T_prov_dVUTpc", "d4_vut_pc"), p_ajustado=float(qv["T_prov_dVUTpc"]),
             modelo="prov trimestral N_t=6 (BH)"),
    ]
    sg = pd.DataFrame(sig)
    sg["signo_observado"] = np.where(sg["estimacion"] > 0, "+", "-")
    esp = sg["signo_esperado"].str[0]
    sg["coherente_con_signo"] = np.where(esp == "a", "n/a", np.where(esp == sg["signo_observado"], "sí", "no"))
    sg["significativo_5%"] = sg["p_ajustado"] < 0.05
    sg.round(8).to_csv(OUT / "signos_vs_literatura.csv", index=False)

    # ---------------- criterio de robustez fijado antes de mirar resultados
    ok_pob = bool(holm["d4_ln_pob_20_34"] < 0.05 and signos.get("d4_ln_pob_20_34", False)
                  and signos.get("d_ln_pob_20_34", False))
    ok_ext = bool(holm["d4_ln_pob_extranj"] < 0.05 and co["d4_ln_pob_extranj"] > 0 and
                  signos.get("d4_ln_pob_extranj", False) and signos.get("d_ln_pob_extranj", False))
    h1_conj = ok_pob and ok_ext
    nivel = "ASOCIACIÓN ROBUSTA" if (ok_pob or ok_ext) else "EXPLORATORIO"
    best = tab[tab["primario"]].iloc[0]
    mejora_oos = bool(best["rmse"] < best["rmse_AR4"] and best["p_vs_AR4"] < 0.05)

    # ---------------- resultado.json
    res = vc.resultado_json(
        OUT / "resultado.json", rama="BA",
        pregunta="¿Qué se asocia con el crecimiento del alquiler provincial y cómo cambia por periodo? "
                 "H1: Δ4 ln IPC alquiler ~ Δ4 ln pob 20-34, Δ4 ln pob extranjera, Δ4 ln ocupados (FE prov y trimestre).",
        datos="panel_prov_q 2008Q1-2024Q2, 49 provincias de entrenamiento (via v2_common.load); panel_prov_a; panel_muni_a. "
              "Población interpolada intra-anual en T2-T4 (marcada); robustez con T1 observado y panel anual.",
        N={"H1_prov_trim": int(r_h1["n"]), "provincias": int(r_h1["G"]), "OOS_obs_comunes": int(best["n"]),
           "municipal": int(tur[tur["spec"] == "T_muni_base"]["n"].iloc[0])},
        metodo="MCO con efectos fijos de provincia y trimestre; EE cluster por provincia (CR1, t(G-1)); wild cluster "
               "bootstrap restringido con pesos de Webb (9.999, semilla 20261010); Holm sobre los 2 contrastes clave; "
               "BH sobre coeficientes por periodo; OOS directo h=4 con bloques+embargo y DM-HLN.",
        estimacion={n: float(co[n]) for n in nm},
        ic95=ic,
        p_ajustado={"p_boot_bruto": {k: float(v) for k, v in pbt.items()},
                    "holm_H1_clave": {k: float(v) for k, v in holm.items()}},
        nivel_evidencia=nivel,
        diagnosticos={"r2_within": float(r_h1["r2_within"]), "clusters": int(r_h1["G"]),
                      "criterio_robustez_pob_20_34": ok_pob, "criterio_robustez_pob_extranj": ok_ext,
                      "H1_conjuncion_confirmada_en_entrenamiento": h1_conj,
                      "signos_positivos_en_todas_las_submuestras": {k: bool(v) for k, v in signos.items()},
                      "Wald_igualdad_coef_periodos": per_w.round(6).to_dict("records"),
                      "n_especificaciones_registradas": int(len(LOG.reg.rows))},
        fuera_muestra={"modelo": bl.PRIMARIO, "rmse": float(best["rmse"]), "rmse_AR4": float(best["rmse_AR4"]),
                       "rmse_ECM_v1": float(best["rmse_ECM_v1"]), "dm_vs_ar4": float(best["dm_vs_AR4"]),
                       "p_vs_ar4": float(best["p_vs_AR4"]), "dm_vs_ecm_v1": float(best["dm_vs_ECM_v1"]),
                       "p_vs_ecm_v1": float(best["p_vs_ECM_v1"]), "mejora_significativa_vs_AR4": mejora_oos,
                       "validacion": "bloques de 4 orígenes, primer test 2012Q1, h=4, embargo 4, misma muestra"},
        notas="Asociación, sin identificación causal. ASOCIACIÓN ROBUSTA se aplica SOLO al componente población 20-34 y es "
              "PROVISIONAL (falta la evaluación sellada de H1: RMSE vs AR(4)). La conjunción de H1 (joven Y extranjera) NO se "
              "confirma en entrenamiento: la población extranjera no es significativa y su signo es negativo con efectos de "
              "tiempo. El modelo con variables de H1 no mejora significativamente al AR(4) fuera de muestra: no se presenta "
              "como explicación predictiva. Turismo y contribuciones por periodo: EXPLORATORIO (causalidad inversa posible).")

    # ---------------- resumen.md
    c = cont[(cont["spec"] == "C1_Q_H1vars_sinFEt") & (cont["referencia"] == "media_muestra")]

    def cr(df, per, fam_):
        s = df[(df["periodo"] == per) & (df["familia"] == fam_)]
        return (float(s["contrib"].iloc[0]), float(s["lo"].iloc[0]), float(s["hi"].iloc[0])) if len(s) else (np.nan,) * 3
    lin_c = []
    for p in bl.PERIODOS:
        ymm = float(c[c["periodo"] == p]["y_medio"].iloc[0])
        d_, l_, h_ = cr(c, p, "demografia")
        e_, le_, he_ = cr(c, p, "empleo_renta")
        lin_c.append(f"| {p} {bl.PERIODOS[p][0]}-{bl.PERIODOS[p][1]} | {_pp(ymm)} | {_pp(d_)} [{_pp(l_)}; {_pp(h_)}] | "
                     f"{_pp(e_)} [{_pp(le_)}; {_pp(he_)}] |")
    ppi = per_t.set_index("var")
    lin_p = []
    for x, et in (("d4_ln_pob_20_34", "pob 20-34"), ("d4_ln_pob_extranj", "pob extranjera"), ("d4_ln_ocupados", "ocupados")):
        cel = []
        for p in bl.PERIODOS:
            r = ppi.loc[f"{x}__{p}"]
            cel.append(f"{r['coef']:.3f} ({r['se']:.3f}; q={r['q_BH']:.2f})")
        lin_p.append(f"| {et} | " + " | ".join(cel) + " |")
    lin_o = [f"| {r['modelo']} | {r['rmse']:.5f} | {r['razon_rmse_vs_AR4']:.3f} | {r['dm_vs_AR4']:.2f} ({r['p_vs_AR4']:.2f}; Holm {r['p_vs_AR4_holm']:.2f}) | "
             f"{r['dm_vs_ECM_v1']:.2f} ({r['p_vs_ECM_v1']:.2f}) |" for _, r in tab.iterrows()]
    an = robdf[(robdf["submuestra"] == "anual_ipc")].set_index("var")
    tm = tur[tur["spec"] == "T_muni_base"].iloc[0]
    tpl = tur[tur["spec"] == "T_muni_PLACEBO_pretend"].iloc[0]
    tp1 = tur[tur["spec"] == "T_prov_dVUTpc"].iloc[0]
    tp2 = tur[tur["spec"] == "T_prov_dlnVUT"].iloc[0]
    wx = per_w.set_index("x")
    nccaa = int(robdf["submuestra"].str.startswith("sin_CCAA_").pipe(lambda m: robdf.loc[m, "submuestra"].nunique()))
    cv = cont[(cont["spec"] == "C3_Q_VUT") & (cont["referencia"] == "media_muestra")]
    cvv = cr(cv, "P4", "turismo_VUT")
    md = f"""# BA - Alquiler: resumen (fase de entrenamiento; muestra sellada NO evaluada)

Nivel de evidencia global: **{nivel}** (provisional), solo para el componente población 20-34; asociación, no causalidad.
Contribuciones por periodo y turismo: **EXPLORATORIO**. Muestra: 49 provincias, 2008Q1-2024Q2 (N={r_h1['n']}).
Cifras generadas por src/v2/ba_run.py (output/v2/BA/*.csv); {len(LOG.reg.rows)} filas en registro.csv.

## H1 (pre-registrada)
Δ4 ln IPC alquiler sobre Δ4 ln pob 20-34, Δ4 ln pob extranjera, Δ4 ln ocupados; FE de provincia y trimestre; EE cluster provincia.

| variable | coef | IC95 % (t, 48 gl) | p cluster | p wild bootstrap (Webb, 9.999) | p Holm (2 contrastes clave) |
|---|---|---|---|---|---|
| pob 20-34 | {co['d4_ln_pob_20_34']:.3f} | [{ic['d4_ln_pob_20_34'][0]:.3f}; {ic['d4_ln_pob_20_34'][1]:.3f}] | {r_h1['p'][0]:.4f} | {pbt['d4_ln_pob_20_34']:.4f} | {holm['d4_ln_pob_20_34']:.4f} |
| pob extranjera | {co['d4_ln_pob_extranj']:.3f} | [{ic['d4_ln_pob_extranj'][0]:.3f}; {ic['d4_ln_pob_extranj'][1]:.3f}] | {r_h1['p'][1]:.4f} | {pbt['d4_ln_pob_extranj']:.4f} | {holm['d4_ln_pob_extranj']:.4f} |
| ocupados | {co['d4_ln_ocupados']:.4f} | [{ic['d4_ln_ocupados'][0]:.3f}; {ic['d4_ln_ocupados'][1]:.3f}] | {r_h1['p'][2]:.4f} | {pbt['d4_ln_ocupados']:.4f} | - |

Lectura: 1 pp más de crecimiento interanual de la población de 20-34 años se asocia con ~{co['d4_ln_pob_20_34']:.2f} pp más de crecimiento del
alquiler (diferencial entre provincias, condicionado a efectos de tiempo). **La parte "extranjera" de H1 no se confirma**: coeficiente
{co['d4_ln_pob_extranj']:.3f}, indistinguible de 0 y de signo opuesto al esperado. Con ocupados tampoco hay asociación. La conjunción
pre-registrada (joven Y extranjera, ambos +) **no queda confirmada** en entrenamiento.

Robustez (h1_robustez.csv): el coeficiente de 20-34 es positivo en todas las submuestras (sin COVID, 2008-2019, desde 2014, sin Madrid/Barcelona,
sin las 5 mayores, solo T1 con población observada, {nccaa} salidas de una CCAA) y en el panel anual (coef {an.loc['d_ln_pob_20_34','coef']:.3f}, p bootstrap {an.loc['d_ln_pob_20_34','p_boot']:.4f});
el de extranjera es negativo o nulo en todas (anual: {an.loc['d_ln_pob_extranj','coef']:.3f}). Sin efectos de tiempo (la variante usa también
la serie temporal común) la extranjera pasa a {sf.loc['d4_ln_pob_extranj','coef']:.3f} (p {pf(sf.loc['d4_ln_pob_extranj','p'])}): la
asociación temporal agregada con la población extranjera no se traslada a diferencias entre provincias.
**Aviso de datos**: la población (1 de enero) está interpolada log-linealmente en T2-T4 (marcada); la robustez T1 y anual evita la interpolación y coincide.

## Por periodos (EXPLORATORIO; P1-P4 pre-registrados)
Coeficientes H1 por periodo (EE cluster; q = BH sobre 12 contrastes):

| variable | P1 2008-13 | P2 2014-19 | P3 2020-21 | P4 2022-24Q2 |
|---|---|---|---|---|
{chr(10).join(lin_p)}

Igualdad entre periodos (Wald, F): pob 20-34 p={wx.loc['d4_ln_pob_20_34','p_F']:.3f}; extranjera p={wx.loc['d4_ln_pob_extranj','p_F']:.3f}; ocupados p={wx.loc['d4_ln_ocupados','p_F']:.3f}.
La asociación con 20-34 es positiva en P1-P3 y se debilita en P4 (q alto), cuando el alquiler crece más en la muestra.

Contribuciones (C1: sin efectos de tiempo, FE provincia + trimestre del año, coeficientes por periodo; contribución = β_P × (media_P(x) − media muestral de x);
IC95 con EE cluster, que NO recogen shocks comunes; tipos, regulación y expectativas quedan en "no explicado"):

| periodo | Δ4 ln alquiler (media periodo − media muestra) | demografía | empleo |
|---|---|---|---|
{chr(10).join(lin_c)}

Oferta (terminadas/1.000 hab.), coste de uso y PIB pc (anual): contribuciones_por_periodo.csv (C2 trimestral desde 2010Q4; C4 anual). Contribuciones pequeñas
(del orden de décimas de pp) y, para oferta, con signo + en P1 (contrario a la literatura; posible respuesta de la construcción al alquiler). El coste de
uso es una única serie nacional: sus IC están subestimados. Viviendas turísticas (INE, 2021Q3-2024Q1), contribución en P4: {_pp(cvv[0])} [{_pp(cvv[1])}; {_pp(cvv[2])}] (N temporal 6).

## Turismo (EXPLORATORIO; causalidad inversa y selección no descartadas)
- Municipal (SERPAVI vc 2020→2023 ~ ΔVUT por 1.000 uu residenciales, FE provincia, N={int(tm['n'])}, {int(tm['G'])} provincias): coef {tm['coef']:.5f} (EE {tm['se']:.5f}, p {tm['p']:.2f}). Sin asociación detectable; placebo (Δ SERPAVI 2017→2020 sobre ΔVUT futura) p={tpl['p']:.2f}.
- Provincial trimestral: ΔVUT por 1.000 hab. coef {tp1['coef']:.4f} (p {tp1['p']:.4f}); Δ ln VUT {tp2['coef']:.4f} (p {tp2['p']:.2f}). N temporal = 6 (2021Q3-2024Q1): inferencia frágil; el resultado depende de la métrica.

## Fuera de muestra (h=4, bloques con embargo, primer test 2012Q1; misma muestra)
| modelo | RMSE | RMSE / AR(4) | DM-HLN vs AR(4) (p) | DM-HLN vs ECM v1 (p) |
|---|---|---|---|---|
{chr(10).join(lin_o)}

RMSE de las bases en la muestra común: AR(4) {best['rmse_AR4']:.5f}, ECM v1 {best['rmse_ECM_v1']:.5f}. Modelo primario fijado ex ante: {bl.PRIMARIO}.
**No hay mejora significativa frente al AR(4)** (p {best['p_vs_AR4']:.2f}); el modelo de H1 no se presenta como explicación predictiva del alquiler.

## Qué NO se puede afirmar
- Nada causal: sin identificación (población y alquiler se determinan conjuntamente; la población joven se mueve hacia donde hay empleo o sube el alquiler).
- Que la inmigración extranjera eleve el alquiler provincial: H1 no lo encuentra con efectos de tiempo (la identificación causal es de BI).
- Que las viviendas turísticas expliquen el alquiler: sin asociación robusta y con N temporal corto.
- Que el modelo prediga mejor que un AR(4), ni que H1 se confirme en la muestra sellada (no evaluada).
- Efectos de tipos, regulación y expectativas: no medidos aquí (el coste de uso es una sola serie nacional).
"""
    (OUT / "resumen.md").write_text(md)
    return res
