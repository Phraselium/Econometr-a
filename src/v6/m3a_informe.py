"""M3a v6: informe de validación interna (RMSE, MAE, DM-HLN vs líneas base en la MISMA muestra), registro y entregables.
Lee las predicciones por pliegue de m3a_run, m3a_bayes y m3a_dl. No abre data/sealed."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m3a_lib as L  # noqa: E402

OUT = L.OUT
FECHA = L.FECHA
BASES = ["AR_unidad", "ECM_v1_aprox", "M1A_TWFE_tendencia", "persistencia"]
MODELOS = ["rf", "gb", "mixto_jerarquico", "mlp", "gnn"]


def cargar_preds():
    fs = [OUT / f for f in ("predicciones_cv_ml.csv.gz", "predicciones_cv_mixto.csv.gz", "predicciones_cv_dl.csv.gz") if (OUT / f).exists()]
    return pd.concat([pd.read_csv(f, dtype={"unit": str}) for f in fs], ignore_index=True)


def main():
    P = cargar_preds()
    P["e"] = P.y - P.pred
    filas, dms, fm = [], [], {}
    for nivel, g in P.groupby("nivel"):
        W = g.pivot_table(index=["origen", "unit", "anio"], columns="modelo", values="e", aggfunc="first")
        mods = [m for m in BASES + MODELOS if m in W.columns]
        if "mlp" in W.columns or "gnn" in W.columns:
            pass
        comun_ml = W[[m for m in mods if m not in ("mlp", "gnn")]].dropna()
        for etiqueta, ms in (("sin_DL", [m for m in mods if m not in ("mlp", "gnn")]), ("con_DL", mods)):
            if etiqueta == "con_DL" and nivel != "distrito":
                continue
            C = W[ms].dropna()
            fm[(nivel, etiqueta)] = len(C)
            for m in ms:
                filas.append({"nivel": nivel, "muestra": etiqueta, "modelo": m, "N": len(C), "rmse": L.rmse(C[m]), "mae": L.mae(C[m])})
            anual = (C ** 2).groupby(level="anio").mean()
            pares = [(m, b) for m in ms for b in BASES if m != b and m not in BASES] + ([("rf", "gb"), ("mixto_jerarquico", "gb")] if etiqueta == "sin_DL" else [])
            if etiqueta == "con_DL":
                pares = [(m, b) for m in ("mlp", "gnn") for b in BASES + ["gb", "rf"]]
            for m, b in pares:
                dm, p, n = L.dm_hln(C[m], C[b])
                dma, pa, na = L.dm_hln(np.sqrt(anual[m]), np.sqrt(anual[b]))
                dms.append({"nivel": nivel, "muestra": etiqueta, "modelo": m, "contra": b, "N": n, "DM_HLN": dm, "p": p,
                            "DM_HLN_medias_anuales": dma, "p_medias_anuales": pa, "n_anios": na,
                            "rmse_modelo": L.rmse(C[m]), "rmse_contra": L.rmse(C[b])})
    M = pd.DataFrame(filas)
    D = pd.DataFrame(dms)
    D["p_holm"] = np.nan
    D["p_bh"] = np.nan
    for (nv, mu), ix in D.groupby(["nivel", "muestra"]).groups.items():
        D.loc[ix, "p_holm"] = L.holm(D.loc[ix, "p"].to_numpy())
        D.loc[ix, "p_bh"] = L.bh(D.loc[ix, "p"].to_numpy())
    M.round(6).to_csv(OUT / "metricas_validacion_interna.csv", index=False)
    D.round(6).to_csv(OUT / "dm_hln_validacion_interna.csv", index=False)
    # registro de especificaciones
    reg = pd.concat([pd.read_csv(OUT / f) for f in ("registro_ml.csv", "registro_mixto.csv", "registro_dl.csv") if (OUT / f).exists()])
    base_rows = [{"nivel": n, "familia": b, "config_id": 0, "config": "sin hiperparametros", "estado": "linea base (1 especificacion)"}
                 for n in ("provincia", "municipio", "distrito") for b in BASES]
    reg = pd.concat([reg, pd.DataFrame(base_rows)], ignore_index=True)
    reg.to_csv(OUT / "registro.csv", index=False)
    # mejor por nivel en la muestra sin DL
    mejores = {}
    for nivel in ("provincia", "municipio", "distrito"):
        m = M[(M.nivel == nivel) & (M.muestra == "sin_DL") & (M.modelo.isin(MODELOS))].sort_values("rmse")
        mb = m.iloc[0]
        d = D[(D.nivel == nivel) & (D.muestra == "sin_DL") & (D.modelo == mb.modelo)].set_index("contra")
        rb = M[(M.nivel == nivel) & (M.muestra == "sin_DL")].set_index("modelo").rmse
        mejores[nivel] = {"modelo": mb.modelo, "rmse": float(mb.rmse), "mae": float(mb.mae), "N": int(mb.N),
                          "rmse_AR": float(rb["AR_unidad"]), "rmse_ECM_v1_aprox": float(rb["ECM_v1_aprox"]),
                          "rmse_M1A_TWFE": float(rb["M1A_TWFE_tendencia"]), "rmse_persistencia": float(rb["persistencia"]),
                          "dm_vs_ar4": {"DM_HLN": float(d.loc["AR_unidad", "DM_HLN"]), "p": float(d.loc["AR_unidad", "p"]),
                                        "p_holm": float(d.loc["AR_unidad", "p_holm"]),
                                        "p_medias_anuales": float(d.loc["AR_unidad", "p_medias_anuales"])},
                          "dm_vs_ecm_v1": {"DM_HLN": float(d.loc["ECM_v1_aprox", "DM_HLN"]), "p": float(d.loc["ECM_v1_aprox", "p"]),
                                           "p_holm": float(d.loc["ECM_v1_aprox", "p_holm"])},
                          "dm_vs_m1a_twfe": {"DM_HLN": float(d.loc["M1A_TWFE_tendencia", "DM_HLN"]), "p": float(d.loc["M1A_TWFE_tendencia", "p"])}}
    # DL frente a gb
    dl = {}
    for m in ("mlp", "gnn"):
        s = D[(D.nivel == "distrito") & (D.muestra == "con_DL") & (D.modelo == m) & (D.contra == "gb")]
        if len(s):
            r = s.iloc[0]
            dl[m] = {"rmse": float(r.rmse_modelo), "rmse_gb": float(r.rmse_contra), "DM_HLN_vs_gb": float(r.DM_HLN), "p": float(r.p),
                     "p_medias_anuales": float(r.p_medias_anuales),
                     "veredicto": "supera a gradient boosting (DM-HLN p<0,05, N obs)" if (r.DM_HLN < 0 and r.p < 0.05) else "NO supera a gradient boosting: resultado negativo"}
    # modelos finales
    fin = []
    for f in ("modelos_finales_ml.json", "modelos_finales_mixto.json", "modelos_finales_dl.json"):
        if (OUT / f).exists():
            fin += json.loads((OUT / f).read_text())
    (OUT / "modelos_finales.json").write_text(json.dumps(fin, indent=1, ensure_ascii=False))
    interp = json.loads((OUT / "interpretacion.json").read_text())
    res = {
        "rama": "v6/M3a", "mercado": "alquiler",
        "pregunta": "Predice mejor el alquiler de stock (SERPAVI) un modelo de ML que AR por unidad, ECM v1 y el mejor econometrico de M1A, en validacion interna con embargo de 1 anio?",
        "capa": "C4", "nivel_evidencia": "EXPLORATORIO (prediccion; las interpretaciones SHAP, ALE e importancias son descriptivas, no causales)",
        "medida_precio": "SERPAVI mediana VC EUR/m2/mes (provincia, municipio); distrito: punto medio p25-p75. Contratos nuevos (fianzas): no modelizable (N~15)",
        "datos": "output/v6/M0/paneles/{prov,mun,dis}_alquiler_anual_train.csv.gz y prov_compra_anual_train (regresores provinciales); solo entrenamiento; datos hasta 2023",
        "N": {"muestra_comun_sin_DL": {k[0]: v for k, v in fm.items() if k[1] == "sin_DL"}, "muestra_comun_con_DL_distrito": fm.get(("distrito", "con_DL"))},
        "metodo": "Random forest y LightGBM (30 configuraciones por familia y nivel, busqueda aleatoria, bloques espacio-temporales de 4 grupos de CCAA con embargo de 1 anio); mixto jerarquico (MixedLM, sustituto declarado de PyMC/NumPyro); MLP con embeddings y GraphSAGE propio solo en distrito. BART: no realizado (sin libreria). Objetivo: variacion anual de ln(EUR/m2/mes); regresores en t-1.",
        "estimacion": mejores, "ic95": None, "p_ajustado": "Holm y BH dentro de cada nivel y muestra: ver dm_hln_validacion_interna.csv",
        "diagnosticos": {"interpretacion": "interpretacion.json", "metricas": "metricas_validacion_interna.csv",
                         "dl_vs_gradient_boosting": dl, "colinealidad": {n: interp["diag"][n]["vif"] for n in interp["diag"]}},
        "fuera_muestra": {"modelo": {n: mejores[n]["modelo"] for n in mejores}, "rmse": {n: mejores[n]["rmse"] for n in mejores},
                          "dm_vs_ar4": {n: mejores[n]["dm_vs_ar4"] for n in mejores}, "validacion": "interna (origenes 2018/2020/2022; embargo 1 anio); la evaluacion sellada la hace M4"},
        "notas": "Prediccion no es causalidad. Contratos nuevos (fianzas): no modelizable (3 provincias GVA y 4 Incasol, N~15). AR por unidad con T corto: p elegido por AIC entre 1 y 4, persistencia si T insuficiente. Optimismo declarado: la eleccion de hiperparametros y la validacion comparten anios de entrenamiento. Horizonte h=2 no evaluado. El DM de observaciones agrupadas (N grande) ignora la correlacion transversal dentro de cada anio y es anticonservador; el conservador es DM_HLN_medias_anuales (pocos anios, baja potencia). Las lineas base AR y M1A-TWFE se re-estiman en cada pliegue (entrenamiento hasta o-2), por lo que su RMSE difiere del de M1A, que valida 2022-2023 con entrenamiento hasta 2020. El GNN y el MLP se seleccionan con un solo origen (2020) y 6 configuraciones. Las figuras SHAP y ALE y las importancias son descriptivas (C4), no causales. Cifras con fecha del dato 2023.",
    }
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))
    hechos = []
    for n, d in mejores.items():
        hechos.append({"id": f"m3a_rmse_{n}", "indicador": f"RMSE de validacion interna del mejor modelo de ML ({d['modelo']}), alquiler de stock, {n} (variacion anual de ln EUR/m2)",
                       "valor": round(d["rmse"], 5), "min": None, "max": None, "unidad": "log-puntos", "periodo": "2018-2023 (pliegues)",
                       "cobertura": f"N={d['N']} observaciones", "fuentes": "SERPAVI (MIVAU)", "capa": "C4", "fecha_dato": "2023"})
        hechos.append({"id": f"m3a_rmse_ar_{n}", "indicador": f"RMSE de AR por unidad, misma muestra, {n}", "valor": round(d["rmse_AR"], 5),
                       "min": None, "max": None, "unidad": "log-puntos", "periodo": "2018-2023 (pliegues)", "cobertura": f"N={d['N']}",
                       "fuentes": "SERPAVI (MIVAU)", "capa": "C4", "fecha_dato": "2023"})
    (OUT / "hechos.json").write_text(json.dumps(hechos, indent=1, ensure_ascii=False))
    print(M.round(4).to_string())
    print(json.dumps(mejores, indent=1, default=float)[:3000])
    print(json.dumps(dl, indent=1))


if __name__ == "__main__":
    main()
