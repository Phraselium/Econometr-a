"""V15-B · E2 (P7): presión demográfica frente a obra nueva y crecimiento del alquiler. Descriptiva (24 especificaciones, correlaciones puntuales, sin p ni IC).
Solo entrenamiento. Uso: python3 src/v15/p7_demografia.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v15.pb_comun import OUT, Registry, cargar, escribe_json, hecho, resultado_base  # noqa: E402

CARPETA = OUT / "p7"
HOGAR = 2.5          # tamaño medio de hogar nacional (INE ECP 2021, ≈ 2,5; DV15-B-8)


def anual(d, var, nivel, y, col="valor", filt=None):
    x = d[(d.variable == var) & (d.nivel == nivel) & (d.periodo.astype(str) == str(y))]
    if filt is not None:
        x = x[filt(x)]
    return x.drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor.astype(float)


def corr(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 10:
        return {"n": int(m.sum()), "pearson": None, "spearman": None}
    return {"n": int(m.sum()), "pearson": float(stats.pearsonr(x[m], y[m])[0]), "spearman": float(stats.spearmanr(x[m], y[m])[0])}


def provincial():
    d7, d9, d4 = cargar("p7_demografia_obra"), cargar("p9_prediccion"), cargar("p4_inmigracion")
    pob0 = anual(d9, "pob_total", "provincia", 2018)
    cr = d7[(d7.variable == "v12_pob_crecimiento") & (d7.nivel == "provincia") & (d7.desagregacion == "nacionalidad=TOTAL") & d7.periodo.isin([str(a) for a in range(2019, 2025)])]
    dpob = cr.groupby("territorio_codigo").valor.sum()
    neta = d7[(d7.variable == "obra_nueva_neta_catastro") & (d7.nivel == "municipio") & d7.periodo.isin([str(a) for a in range(2019, 2026)])]
    neta = neta.assign(prov=neta.territorio_codigo.str[:2]).groupby("prov").valor.sum()          # desfase de 1 año: Δ(t+1) = obra de t
    term = d7[(d7.variable == "terminadas") & (d7.nivel == "provincia") & d7.periodo.isin([str(a) for a in range(2018, 2025)])].groupby("territorio_codigo").valor.sum()
    ini = d9[(d9.variable == "iniciadas") & (d9.nivel == "provincia") & d9.periodo.isin([str(a) for a in range(2018, 2025)])].groupby("territorio_codigo").valor.sum()
    s0 = {t: anual(d4, "serpavi_alquiler_m2_mediana", "provincia", a, filt=lambda x: x.desagregacion == "tipologia=VC") for t, a in (("0", 2018), ("1", 2024))}
    out_s = np.log(s0["1"]) - np.log(s0["0"])
    ia0 = d4[(d4.variable == "ipc_alquiler_indice") & (d4.nivel == "provincia") & (d4.periodo.astype(str) == "2018")].set_index("territorio_codigo").valor
    ia1 = d4[(d4.variable == "ipc_alquiler_indice") & (d4.nivel == "provincia") & (d4.periodo.astype(str) == "2024")].set_index("territorio_codigo").valor
    out_i = np.log(ia1) - np.log(ia0)
    return pob0, dpob, {"obra_neta_catastro": neta, "terminadas_MIVAU": term, "iniciadas_MIVAU": ini}, {"SERPAVI": out_s, "IPC_alquiler": out_i}


def municipal():
    d7, d4 = cargar("p7_demografia_obra"), cargar("p4_inmigracion")
    tot = d7[(d7.variable == "pob_censo_anual") & (d7.nivel == "municipio") & (d7.desagregacion == "nacionalidad=Total")]
    p21 = tot[tot.periodo.astype(str) == "2021"].set_index("territorio_codigo").valor
    p25 = tot[tot.periodo.astype(str) == "2025"].set_index("territorio_codigo").valor
    hog = d7[(d7.variable == "v12_hogares_nuevos_estimados") & (d7.nivel == "municipio") & (d7.desagregacion == "periodo=2021-2025")].set_index("territorio_codigo").valor
    obra = d7[(d7.variable == "v12_obra_neta") & (d7.nivel == "municipio") & (d7.desagregacion == "periodo=2021-2025")].set_index("territorio_codigo").valor
    s = d7[(d7.variable == "serpavi_alquiler_m2_mediana") & (d7.nivel == "municipio") & (d7.desagregacion == "tipologia=VC")]
    s21, s24 = (s[s.periodo.astype(str) == a].drop_duplicates("territorio_codigo").set_index("territorio_codigo").valor for a in ("2021", "2024"))
    ia = d4[(d4.variable == "ipc_alquiler_indice") & (d4.nivel == "provincia")]
    ipc = (np.log(ia[ia.periodo.astype(str) == "2024"].set_index("territorio_codigo").valor) - np.log(ia[ia.periodo.astype(str) == "2021"].set_index("territorio_codigo").valor))
    ipc_m = pd.Series({m: ipc.get(m[:2], np.nan) for m in p21.index})
    return p21, p25 - p21, hog, obra, {"SERPAVI": np.log(s24) - np.log(s21), "IPC_alquiler": ipc_m}


def main():
    CARPETA.mkdir(parents=True, exist_ok=True)
    reg = Registry(CARPETA / "registro.csv")
    filas = []
    pob0, dpob, ofertas, outs = provincial()
    for dem in ("hogares", "poblacion"):
        dh = dpob / HOGAR if dem == "hogares" else dpob
        for on, oferta in ofertas.items():
            ofe = oferta if dem == "hogares" else oferta * HOGAR
            exc = ((dh - ofe) / pob0).replace([np.inf, -np.inf], np.nan)
            for rn, ro in outs.items():
                df = pd.concat([exc.rename("x"), ro.rename("y")], axis=1).dropna()
                c = corr(df.x.values, df.y.values)
                filas.append({"id": f"E2-prov-{on}-{dem}-{rn}", "nivel": "provincia", "ventana": "2018-2024", "oferta": on, "demanda": dem, "resultado": rn, **c})
    p21, dp, hog, obra, mout = municipal()
    for dem in ("hogares", "poblacion"):
        dd = hog if dem == "hogares" else dp / HOGAR * 1.0
        ob = obra
        for on in ("obra_neta_catastro", "terminadas_MIVAU", "iniciadas_MIVAU"):
            for rn, ro in mout.items():
                if on != "obra_neta_catastro":
                    filas.append({"id": f"E2-mun-{on}-{dem}-{rn}", "nivel": "municipio", "ventana": "2021-2025", "oferta": on, "demanda": dem, "resultado": rn, "n": 0,
                                  "pearson": None, "spearman": None, "nota": "no disponible a nivel municipal (MIVAU solo provincial)"})
                    continue
                exc = ((dd - ob) / p21).replace([np.inf, -np.inf], np.nan)
                df = pd.concat([exc.rename("x"), ro.rename("y")], axis=1).dropna()
                df = df[(df.x.abs() < df.x.abs().quantile(0.99))]
                filas.append({"id": f"E2-mun-{on}-{dem}-{rn}", "nivel": "municipio", "ventana": "2021-2025", "oferta": on, "demanda": dem, "resultado": rn, **corr(df.x.values, df.y.values)})
    F = pd.DataFrame(filas)
    for r in filas:
        reg.log("E2", r["id"], f"{r['nivel']} {r['demanda']} vs {r['oferta']} -> {r['resultado']}", r["ventana"][:4], r["ventana"][-4:], r["n"], np.nan, np.nan, np.nan,
                coef_interes=r["pearson"] if r["pearson"] is not None else np.nan, notas="descriptiva; sin p")
    F.to_csv(CARPETA / "multiverso.csv", index=False)
    v = F.dropna(subset=["pearson"])
    prin = F[F.id == "E2-prov-terminadas_MIVAU-hogares-SERPAVI"].iloc[0]
    diag = {"especificaciones": int(len(F)), "con_dato": int(len(v)), "pearson_min_max": [float(v.pearson.min()), float(v.pearson.max())],
            "frac_pearson_positivo": float((v.pearson > 0).mean()), "frac_spearman_positivo": float((v.spearman > 0).mean()),
            "limitaciones": ["N provincial ≈ 38 (correlación con ruido grande, sin IC)", "provincial: demanda hogares y población coinciden salvo escala (DV15-B-8)",
                             "Catastro municipal solo de municipios de entrenamiento: la suma provincial es parcial", "contaminación por regularización catastral 2011-2021 (por eso solo 2018+)"],
            "inferencia": "ninguna herramienta de inferencia de E2 figura en las tablas de K13: puntual"}
    res = resultado_base("r15/p7", "E2: ¿se asocia la presión demográfica no cubierta por la obra con el crecimiento del alquiler? (descriptiva)", "data/processed/v15/p7_demografia_obra.parquet (+ p9, p4); entrenamiento",
                         int(prin.n), "Correlaciones de Pearson/Spearman del exceso de presión (demanda − obra)/población inicial con el Δlog del alquiler; 24 especificaciones",
                         {"pearson_provincial_terminadas_hogares_SERPAVI": prin.pearson, "spearman": prin.spearman}, None, "DESCRIPTIVO (C4)", diag, {"modelo": None, "rmse": None, "dm_vs_ar4": None},
                         ["Sin p ni IC. Capa C4; pendiente de evaluación sellada. Asociación, no efecto."], [{"id": i, "p": None} for i in F.id])
    escribe_json(CARPETA / "resultado.json", res)
    escribe_json(CARPETA / "hechos.json", [hecho("V15-E2-pearson", "Correlación (Pearson) entre exceso de presión (hogares − terminadas) y Δlog SERPAVI, provincias 2018-2024", round(float(prin.pearson), 3),
                                                round(float(v.pearson.min()), 3), round(float(v.pearson.max()), 3), "r", "2018-2024", f"{int(prin.n)} provincias", "INE; MIVAU; Catastro", "pearson", "p7")])
    print(F[["id", "n", "pearson", "spearman"]].to_string())


if __name__ == "__main__":
    main()
