"""E-V6: cifras v6 (alquiler y compraventa) que piden los entregables y no están en output/v6/*/hechos.json.

Todo se LEE de output/v6 (nada tecleado). Ids con prefijo E-V6-.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e_hechos import h  # noqa: E402

R = Path(__file__).resolve().parents[2]
O6 = R / "output" / "v6"
FECHA = "2026-10-11"
VAL = "validacion sellada v6 (11 provincias)"


def _j(p: Path):
    return json.loads(p.read_text())


def filas() -> list[dict]:
    out: list[dict] = []
    # Sellado: provincias de entrenamiento y selladas
    si = {d["panel"]: d for d in _j(O6 / "M0/sellado_info.json")}
    pc = si["prov_compra_anual"]
    out.append(h("E-V6-NPROV-SELL", "Provincias selladas en la validación v6 (bloques de CCAA)", pc["unidades_sealed"], None, None,
                 "provincias", f"{pc['anios_total'][0]}-{pc['anios_total'][1]}", f"{pc['unidades_total']} provincias",
                 "holdout.py (sellar_v6)", "C4", FECHA))
    out.append(h("E-V6-NPROV-TRAIN", "Provincias de entrenamiento en v6", pc["unidades_train"], None, None,
                 "provincias", f"{pc['anios_train'][0]}-{pc['anios_train'][1]}", f"{pc['unidades_total']} provincias",
                 "holdout.py (sellar_v6)", "C4", FECHA))

    # M2: PIP del BMA núcleo (sin ln_vut ni ln_suelo), discrepancia con el BMA completo
    pv = pd.read_csv(O6 / "M2/peso_variables.csv").set_index("variable")
    for var, nom in [("share_ext_pob", "población extranjera"), ("ln_iniciadas_libres", "viviendas libres iniciadas"),
                     ("ln_pib_pc", "PIB por habitante"), ("ln_pob", "población")]:
        for mk, mt, per in [("ALQ", "alquiler de stock (SERPAVI)", "2015-2023"), ("COMPRA", "precio de compra (tasado MIVAU)", "2015-2024")]:
            out.append(h(f"E-V6-M2-PIPN-{mk}-{var}", f"PIP BMA núcleo (sin VUT ni suelo) de {nom}, {mt}, provincia",
                         float(pv.loc[var, f"{mk}_pip_nucleo"]), None, None, "probabilidad", per,
                         "provincias de entrenamiento", "output/v6/M2 (paneles M0)", "C4", FECHA))

    # M3a: deep learning frente a gradient boosting (distrito, validación interna)
    dl = _j(O6 / "M3A/resultado.json")["diagnosticos"]["dl_vs_gradient_boosting"]
    for k, nom in [("mlp", "MLP con embeddings"), ("gnn", "GraphSAGE")]:
        out.append(h(f"E-V6-M3A-DL-{k}", f"RMSE de validación interna, {nom}, alquiler de stock (distrito)", dl[k]["rmse"] * 100, None, None,
                     "log-puntos x100 (aprox. %)", "2018-2023 (pliegues)", "distritos de entrenamiento", "SERPAVI (MIVAU)", "C4", "2023"))
        out.append(h(f"E-V6-M3A-DLp-{k}", f"p DM-HLN de {nom} frente a gradient boosting, alquiler de stock (distrito)", dl[k]["p"], None, None,
                     "p", "2018-2023 (pliegues)", "distritos de entrenamiento", "SERPAVI (MIVAU)", "C4", "2023"))
    out.append(h("E-V6-M3A-GB-dis", "RMSE de validación interna, gradient boosting, alquiler de stock (distrito)", dl["mlp"]["rmse_gb"] * 100, None, None,
                 "log-puntos x100 (aprox. %)", "2018-2023 (pliegues)", "distritos de entrenamiento", "SERPAVI (MIVAU)", "C4", "2023"))

    # M3b: DL municipal y persistencia en la validación interna trimestral
    e3 = _j(O6 / "M3B/resultado.json")["estimacion"]
    fu3 = "MIVAU/INE ETDP (paneles M0 train)"
    for k, nom in [("DL_MLP_tabular", "MLP tabular"), ("DL_GCN_espacial", "GCN espacial")]:
        d = e3["MUN_PRECIO_ANUAL"]["DL"][k]
        out.append(h(f"E-V6-M3B-{k}", f"RMSE % de {nom}, precio municipal anual, validación por bloques con embargo", d["rmse_pct"], None, None,
                     "% (RMSE de ln)", "orígenes 2018/2020/2022", "municipios de entrenamiento", fu3, "C4", "2024"))
        out.append(h(f"E-V6-M3Bp-{k}", f"p DM-HLN de {nom} frente a gradient boosting, precio municipal anual", d["p_dm_vs_GB"], None, None,
                     "p", "orígenes 2018/2020/2022", "municipios de entrenamiento", fu3, "C4", "2024"))
    for t, nom in [("PROV_PRECIO_TRIM", "precio provincial trimestral"), ("PROV_VOL_TRIM", "volumen provincial trimestral")]:
        out.append(h(f"E-V6-M3B-PERS-{t}", f"RMSE % de la persistencia, {nom}, validación por bloques con embargo",
                     e3[t]["rmse_pct_persistencia"], None, None, "% (RMSE de ln)", "orígenes 2018/2020/2022",
                     "provincias de entrenamiento", fu3, "C4", "2024T4"))

    # M4: parte temporal del sellado en el volumen trimestral (persistencia no batida)
    mm = pd.read_csv(O6 / "M4/mejor_modelo.csv").set_index("tarea")
    r = mm.loc["PROV_VOL_TRIM"]
    out.append(h("E-V6-M4-TEMP-PROV_VOL_TRIM", "RMSE temporal sellado del mejor modelo (bosque), volumen provincial trimestral",
                 float(r.rmse_temporal) * 100, None, None, "log-puntos x100 (aprox. %)", "último año (temporal ya visto en v2)",
                 "provincias de entrenamiento, último año", "INE ETDP", "C4", "2025"))
    out.append(h("E-V6-M4-TEMPPERS-PROV_VOL_TRIM", "RMSE temporal sellado de la persistencia, volumen provincial trimestral",
                 float(r.rmse_temporal_persistencia) * 100, None, None, "log-puntos x100 (aprox. %)",
                 "último año (temporal ya visto en v2)", "provincias de entrenamiento, último año", "INE ETDP", "C4", "2025"))

    # M1b: Holm, GSADF
    e1 = _j(O6 / "M1B/resultado.json")["estimacion"]
    out.append(h("E-V6-M1B-HOLM", "Hipótesis confirmatorias de compra que pasan Holm (p<0,05)", e1["n_confirmatorias_Holm_p<0.05"], None, None,
                 "hipótesis", "2016-2024", "41 provincias de entrenamiento", "MIVAU; INE", "C4", FECHA))
    out.append(h("E-V6-M1B-GSADF-SIG", "CCAA con exuberancia GSADF (p<0,05) en el ratio precio/alquiler", e1["gsadf_ccaa_p<0.05"], None, None,
                 "CCAA", "2015T1-2024T4", "CCAA con provincias de entrenamiento", "MIVAU valor tasado; INE IPC alquiler", "C4", FECHA))
    out.append(h("E-V6-M1B-GSADF-TOT", "CCAA contrastadas con GSADF", e1["gsadf_ccaa_total"], None, None,
                 "CCAA", "2015T1-2024T4", "CCAA con provincias de entrenamiento", "MIVAU valor tasado; INE IPC alquiler", "C4", FECHA))

    # M1a: confirmatorias que pasan Holm (S0 pre-registrada)
    tc = pd.read_csv(O6 / "M1A/tabla_coeficientes.csv")
    conf = tc[(tc.familia == "confirmatoria") & tc.ajuste.astype(str).str.startswith("Holm")]
    out.append(h("E-V6-M1A-HOLM", "Hipótesis confirmatorias de alquiler que pasan Holm (p<0,05)", int((conf.p_ajustado < 0.05).sum()), None, None,
                 "hipótesis", "2021-2023", "provincias, municipios y distritos de entrenamiento", "MIVAU-SERPAVI; INE", "C4", "2023"))
    out.append(h("E-V6-M1A-NCONF", "Hipótesis confirmatorias de alquiler contrastadas con Holm", int(len(conf)), None, None,
                 "hipótesis", "2021-2023", "provincias, municipios y distritos de entrenamiento", "MIVAU-SERPAVI; INE", "C4", "2023"))
    return out
