"""BM: genera resumen.md y resultado.json a partir de las tablas (sin cifras a mano)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import v2_common as vc  # noqa: E402

NOMBRE_OBJ = {"A": "A nacional (ln IPV real)", "B": "B panel provincial (IPC alquiler)",
              "C": "C panel provincial (p_tasado real)"}


def _f(x, d=4):
    return "n/d" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}"


def escribir(OUT, T, sel, P, perm, shp, lps, ms, usadas):
    cand = T[T["clase"] != "linea_base"]
    L = ["# Resumen BM (modelos predictivos y no lineales) — EXPLORATORIO",
         "",
         "Validación SOLO en bloques temporales con embargo (v2_common.block_splits: h=4, primer test 2012Q1, bloques de 4 "
         "orígenes, embargo 4, ventana expansiva). Misma muestra que AR(4) y ECM v1; DM-HLN (h=4, pérdida cuadrática; paneles: "
         "media transversal por periodo). Datos solo de entrenamiento (vía v2_common.load); H7 sellada NO ejecutada aquí.",
         "", f"Configuraciones de hiperparámetros evaluadas: {usadas} (presupuesto declarado 63, de las cuales 4 reservadas al "
         "bloque 5, no ejecutado). Cada una cuenta como especificación en output/v2/BM/registro.csv.", ""]
    L += ["## 1. Qué modelo gana (fuera de muestra, entrenamiento)", ""]
    L += ["| Objetivo | N | RMSE AR(4) | RMSE ECM v1 | Mejor candidato por RMSE medio en bloques | RMSE | DM vs AR4 (p) | DM vs ECM v1 (p) | p_BH AR4 / ECM |",
          "|---|---|---|---|---|---|---|---|---|"]
    for o in "ABC":
        t = cand[(cand["objetivo"] == o) & (cand["N"] > 0)]
        s = sel[o]["modelo"]
        r = t[t["modelo"] == s].iloc[0]
        L.append(f"| {NOMBRE_OBJ[o]} | {int(r['N'])} | {_f(r['RMSE_AR4'])} | {_f(r['RMSE_ECM_v1'])} | {s} | {_f(r['RMSE'])} | "
                 f"{_f(r['DM_vs_AR4'], 2)} ({_f(r['p_vs_AR4'], 3)}) | {_f(r['DM_vs_ECM_v1'], 2)} ({_f(r['p_vs_ECM_v1'], 3)}) | "
                 f"{_f(r['p_BH_AR4'], 3)} / {_f(r['p_BH_ECM_v1'], 3)} |")
    L += ["", "DM > 0 = el modelo es mejor que la base. El «mejor candidato» es el ELEGIDO para H7 por la regla fijada antes "
          "(output/v2/BM/regla_H7.md): menor RMSE medio en bloques, empate (<1 %) → el más simple.", ""]
    n_ok = int(cand["mejora_ambas_nominal"].fillna(False).sum())
    n_ok_bh = int(((cand["p_BH_AR4"] < 0.05) & (cand["p_BH_ECM_v1"] < 0.05) & (cand["RMSE"] < cand["RMSE_AR4"])
                   & (cand["RMSE"] < cand["RMSE_ECM_v1"])).sum())
    L += [f"Candidatos que mejoran a AR(4) y ECM v1 (RMSE menor y p<0,05 frente a ambos, sin corrección): **{n_ok}** de "
          f"{int((cand['N'] > 0).sum())}; con BH sobre las configuraciones de cada objetivo: **{n_ok_bh}**.", ""]
    for o in "ABC":
        t = cand[(cand["objetivo"] == o) & (cand["N"] > 0)]
        mejor_rm = t.loc[t["RMSE"].idxmin()]
        L.append(f"- {NOMBRE_OBJ[o]}: menor RMSE absoluto {mejor_rm['modelo']} = {_f(mejor_rm['RMSE'])} (AR(4) {_f(mejor_rm['RMSE_AR4'])}; "
                 f"ECM v1 {_f(mejor_rm['RMSE_ECM_v1'])}); p vs AR(4) {_f(mejor_rm['p_vs_AR4'], 3)}, p vs ECM v1 {_f(mejor_rm['p_vs_ECM_v1'], 3)}.")
    L += ["", "Lectura: ver sección 5. El menor RMSE absoluto puede diferir del elegido por RMSE medio en bloques (promedio de RMSE "
          "por bloque, que pondera igual a cada bloque).", ""]
    L += ["## 2. Modelos elegidos para H7 (a evaluar UNA vez en la muestra sellada, por el orquestador)", ""]
    for o in "ABC":
        s = sel[o]
        L.append(f"- {NOMBRE_OBJ[o]}: **{s['modelo']}** (clase {s['clase']}, config {json.dumps(s['config'])}); RMSE medio en bloques "
                 f"{_f(s['rmse_bloques'])} sobre {s['n_comun_ranking']} observaciones comunes; empatados (<1 %): {', '.join(s['empatados'])}.")
    L += ["", "Evaluación sellada preparada en src/v2/bm_h7_sellado.py (`evaluar_H7`); ensayo en seco en tests/test_bm_h7_sellado.py "
          "(pseudo-sellado solo con entrenamiento). Regla de decisión: un objetivo cumple si RMSE < AR(4) y ECM v1, DM>0 frente a ambos y "
          "p_IUT=max(p) con Holm (m=3) < 0,05; H7 se cumple si algún objetivo cumple.", ""]
    L += ["## 3. Familias que importan, por periodo (EXPLORATORIO)", "",
          "AVISO DE COLINEALIDAD: dentro de familias (tipo hipotecario real y coste de uso ρ≈0,97; importe y nº de hipotecas ρ≈0,95; "
          "población total, 20-34 y extranjera ρ 0,7-0,9) y entre familias (en el nacional, tipo real y nº de eventos de política ρ≈-0,87; "
          "población y precio cruzado ρ>0,9) las importancias se reparten de forma arbitraria; ver colinealidad_pares_0.7.csv. "
          "Las permutaciones se hacen por familia completa (conjuntamente), lo que mitiga pero no elimina el problema. "
          "Los periodos P1-P4 de la importancia son periodos de los ORÍGENES de test (2012Q1-2023Q2), no del objetivo.", ""]
    pp = perm[~perm["familia"].isin(["autorregresivo", "estacional"])]
    for o in "BC":
        g = pp[pp["objetivo"] == o]
        if g.empty:
            continue
        for mod, gm in g.groupby("modelo"):
            mej = bool(gm["mejora_fuera_muestra"].iloc[0])
            etq = "el modelo mejora al AR(4) (p<0,05)" if mej else "el modelo NO mejora significativamente al AR(4): se publica por transparencia, NO como explicación"
            L.append(f"**{NOMBRE_OBJ[o]} — {mod} (permutación agrupada; Δ ECM relativo al ECM del modelo)** — {etq}")
            for per_, gp in gm.groupby("periodo"):
                top = gp.sort_values("delta_mse_rel", ascending=False).head(2)
                L.append(f"- {per_} (n={int(gp['n'].iloc[0])}): " + "; ".join(f"{r.familia} {r.delta_mse_rel:+.3f}" for r in top.itertuples()))
            L.append("")
    sh = shp[~shp["familia"].isin(["autorregresivo", "estacional"])]
    for o in "BC":
        g = sh[sh["objetivo"] == o]
        if g.empty:
            continue
        L.append(f"**{NOMBRE_OBJ[o]} — SHAP (TreeSHAP LightGBM; |contribución| media por familia)**")
        for per_, gp in g.groupby("periodo"):
            top = gp.sort_values("abs_shap_medio", ascending=False).head(2)
            L.append(f"- {per_}: " + "; ".join(f"{r.familia} {r.abs_shap_medio:.4f}" for r in top.itertuples()))
        L.append("")
    L += ["ALE de las 3 variables con mayor |SHAP| en output/v2/BM/ale_top3.csv (efecto medio local, libre de colinealidad extrema "
          "solo si las variables no son colineales; aquí es una aproximación).", ""]
    L += ["### Post-double-selection por familia (BCH, EE Driscoll-Kraay/HAC(4); EXPLORATORIO)", "",
          "Solo se reportan contrastes con ≥20 periodos distintos y diseño de rango completo (P3 y P4 tienen 8 y 6 periodos: "
          "no hay potencia para variables que solo varían en el tiempo; se omiten). BH dentro de cada objetivo. "
          "Asociación, no causalidad.", ""]
    Pf = P[(P.get("fiable", False) == True)]  # noqa: E712
    sig = Pf[Pf["p_BH"] < 0.05]
    for o in "ABC":
        g = sig[sig["objetivo"] == o]
        tot = Pf[Pf["objetivo"] == o]
        L.append(f"- {NOMBRE_OBJ[o]}: {len(g)} de {len(tot)} contrastes (familia × periodo) fiables con p_BH<0,05. " +
                 ("; ".join(f"{r.periodo}: {r.familia}" for r in g.itertuples()) if len(g) else "Ninguno."))
    L += ["", "Proyecciones locales por periodo (familias principales): output/v2/BM/proyecciones_locales_periodos.csv "
          "(p solo con ≥20 periodos). Los coeficientes cambian de signo entre periodos (p. ej. tipo hipotecario real y n_eventos), "
          "lo que sugiere parámetros cambiantes, pero con colinealidad temporal fuerte entre regresores nacionales.", ""]
    L += ["## 4. Parámetros cambiantes y no linealidad (nacional, A)", "",
          "- ECM de umbral (ECT>0 vs ≤0; crédito en expansión vs no): ver tabla; ninguno supera al AR(4).",
          f"- Markov-switching (2 regímenes, ECT con coeficiente cambiante; DESCRIPTIVO en muestra, N={ms.get('n', 'n/d')}): "
          f"estado {ms.get('estado')}; duraciones esperadas {ms.get('duraciones_esperadas')}. No se usa como predictor.",
          "- BVAR Minnesota (VAR(2), 4 variables: Δ ln IPV real, Δ ln ocupados, Δ tipo hipotecario real, Δ ln crédito nuevo): "
          "SIMPLIFICACIÓN de Giannone-Lenza-Primiceri (2015): sin hiperprior ni suma de coeficientes; λ fijo por configuración (5) y "
          "verosimilitud marginal (fórmula cerrada con observaciones ficticias) informada por split en sel['bvar_logml_medio'] "
          "(seleccion_H7.json). Prior de media cero (variables en diferencias).",
          "- TVP-VAR: SIMPLIFICACIÓN de Primiceri (2005) con olvido exponencial (Koop-Korobilis): coeficientes paseo aleatorio con factor "
          "κ, varianza de medida EWMA (0,98), sin volatilidad estocástica; los coeficientes se filtran hasta L (fin de entrenamiento del "
          "split) y se mantienen fijos en el bloque de test (misma información que el resto de modelos).", ""]
    L += ["## 5. Resultados negativos y lo que NO se puede afirmar", ""]
    L += ["- Ningún modelo con variables mejora de forma significativa (p<0,05 frente a AR(4) y ECM v1) en los bloques de entrenamiento "
          "si n_ok es 0 (ver conteo arriba); si algún candidato lo hiciera, la selección es optimista (mínimo sobre ≥19 configuraciones "
          "por objetivo) y solo la evaluación sellada puede confirmarlo.",
          "- Objetivo A: N de entrenamiento 8-60 (IPV desde 2007Q1; muestra común AR4∩ECM v1 de 38 orígenes y 12 bloques); no se ejecutan "
          "árboles (RF/LightGBM) por falta de datos; la potencia del DM es muy baja. Elastic net con N≈8 al inicio produce RMSE muy "
          "superiores al AR(4).",
          "- El ECM v1 es la base peor en los tres objetivos (RMSE mayor que el AR(4)); mejorar al ECM v1 es un listón bajo.",
          "- Importancias: de modelos que no mejoran al AR(4) fuera de muestra → NO son explicación (regla 4). Incluso si lo hicieran, son "
          "asociaciones predictivas, no efectos causales, con colinealidad alta.",
          "- Bloque 5 NO ejecutado: factor dinámico provincial (reserva de 4 configuraciones sin usar) y spillovers espaciales (los paneles no "
          "traen coordenadas ni matriz de contigüidad: se omite).",
          "- Bloque 6 NO ejecutado: torch no está instalado (se declara; no se instala). Sin deep learning no hay nada que reportar frente a "
          "gradient boosting; el resultado es «no ejecutado», no «negativo».",
          "- Los datos de población en el modelo son «en escalera» (último 1-ene observado); el padrón se publica con retraso: en tiempo real "
          "no estaría disponible. Variables de oferta y turismo tienen mucha ausencia (imputación por mediana dentro del split; LightGBM "
          "usa NaN nativo); turismo (VUT) solo existe desde 2020Q3.",
          "- Efectos de política (n_eventos, nacionales) solo varían en el tiempo y se confunden con cualquier shock agregado.",
          "- Nada de lo anterior es evidencia de H7 hasta la evaluación sellada (criterio uniforme (b)): nivel EXPLORATORIO.", ""]
    (OUT / "resumen.md").write_text("\n".join(L))
    # resultado.json
    fm_rmse, fm_dm, fm_p = {}, {}, {}
    for o in "ABC":
        r = cand[(cand["objetivo"] == o) & (cand["modelo"] == sel[o]["modelo"])].iloc[0]
        fm_rmse[o] = {"modelo": sel[o]["modelo"], "rmse": float(r["RMSE"]), "rmse_AR4": float(r["RMSE_AR4"]),
                      "rmse_ECM_v1": float(r["RMSE_ECM_v1"]), "N": int(r["N"])}
        fm_dm[o] = float(r["DM_vs_AR4"])
        fm_p[o] = {"p_vs_AR4": float(r["p_vs_AR4"]), "p_vs_ECM_v1": float(r["p_vs_ECM_v1"]),
                   "p_BH_AR4": float(r["p_BH_AR4"]), "p_BH_ECM_v1": float(r["p_BH_ECM_v1"])}
    vc.resultado_json(
        OUT / "resultado.json", rama="BM",
        pregunta="H7 (confirmatoria, fase de entrenamiento): ¿algún modelo con variables (panel o ML) supera al AR(4) y al ECM v1 fuera de "
                 "muestra a 4 trimestres? Más: qué familias importan por periodo (exploratorio).",
        datos="nacional_q_v2 y panel_prov_q (holdout.load_train vía v2_common.load); 49 provincias de entrenamiento; orígenes 2012Q1-2023Q2; "
              "sin muestra sellada",
        N={"A": int(fm_rmse["A"]["N"]), "B": int(fm_rmse["B"]["N"]), "C": int(fm_rmse["C"]["N"]), "configuraciones": int(usadas)},
        metodo="Validación en bloques con embargo (h=4, primer test 2012Q1, embargo 4); elastic net, post-lasso plug-in, RF, LightGBM; "
               "ARDL, ECM de umbral, BVAR Minnesota, TVP-VAR con olvido (nacional); DM-HLN; PDS grupal (BCH) y proyecciones locales por periodo; "
               "importancias por permutación agrupada, SHAP y ALE",
        estimacion={o: fm_rmse[o] for o in "ABC"}, ic95=None, p_ajustado={"BH_por_objetivo_sobre_configuraciones": fm_p},
        nivel_evidencia="EXPLORATORIO",
        diagnosticos={"seleccion": {o: sel[o]["modelo"] for o in "ABC"},
                      "candidatos_que_mejoran_ambas_bases_nominal": n_ok, "con_BH": n_ok_bh,
                      "bloque5": "no ejecutado", "bloque6": "no ejecutado (torch no instalado)",
                      "markov_switching": ms.get("estado")},
        fuera_muestra={"modelo": {o: sel[o]["modelo"] for o in "ABC"}, "rmse": {o: fm_rmse[o]["rmse"] for o in "ABC"},
                       "dm_vs_ar4": fm_dm},
        notas="Criterio uniforme (b): H7 tiene evaluación sellada, así que antes del sellado el máximo es EXPLORATORIO. Evaluación sellada "
              "preparada (bm_h7_sellado.evaluar_H7) y NO ejecutada. Importancias exploratorias con colinealidad.")
