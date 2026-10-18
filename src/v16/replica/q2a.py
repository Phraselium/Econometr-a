"""Replica ciega Q2a: DiD de intensidad, forma reducida, estimacion puntual."""
import json
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
D = str(__import__("pathlib").Path(__file__).resolve().parents[3]) + "/data/processed/v16/entrenamiento/"
OUT = str(__import__("pathlib").Path(__file__).resolve().parents[3]) + "/output/v16/replica/q2a/resultado.json"
CIFRA = 0.0132

a = pd.read_parquet(D + "base_alquiler.parquet")
a = a[(a.nivel == "provincia") & (a.variable == "ipc_alquiler_indice") & (a.frecuencia == "T")].copy()
a["anio"] = a.periodo.str[:4].astype(int)
y = a[a.anio.isin([2017, 2018, 2019, 2022, 2023, 2024, 2025])]
y = y.groupby(["territorio_codigo", "anio"]).valor.mean().reset_index()
y["ly"] = np.log(y.valor)

t = pd.read_parquet(D + "alquiler_turismo.parquet")
t = t[(t.nivel == "provincia") & (t.periodo == "2020-08") &
      (t.variable == "ine_vte_porcentaje_de_viviendas_turisticas_sobre_el_total_de_viviendas_censadas")]
t = t[["territorio_codigo", "valor"]].rename(columns={"valor": "pct"})
n_cero = int((t.pct <= 0).sum())
t = t[t.pct > 0]
t["x"] = np.log(t.pct)
t["z"] = (t.x - t.x.mean()) / t.x.std(ddof=1)
sd_x = float(t.x.std(ddof=1))

d = y.merge(t[["territorio_codigo", "z"]], on="territorio_codigo")
d["post"] = (d.anio >= 2022).astype(float)
d["w"] = d.z * d.post
# efectos fijos de provincia y anio: demeaning bipartito (panel balanceado)
for c in ["ly", "w"]:
    d[c + "_t"] = (d[c] - d.groupby("territorio_codigo")[c].transform("mean")
                   - d.groupby("anio")[c].transform("mean") + d[c].mean())
beta = float((d.w_t * d.ly_t).sum() / (d.w_t ** 2).sum())

res = {
    "id": "q2a", "replica": "ciega", "seed": SEED,
    "N": int(len(d)), "provincias": int(d.territorio_codigo.nunique()),
    "metodo": "TWFE forma reducida: log IPC alquiler (media anual de trimestres) ~ z(log % VUT 2020-08) x post(2022-25); FE provincia y anio; 2017-19 vs 2022-25",
    "estimacion": beta, "unidad": "por DT del log de la exposicion",
    "dt_log_exposicion": sd_x, "provincias_pct_cero_excluidas": n_cero,
    "cifra_orquestador": CIFRA,
}
dif = beta - CIFRA
res["comparacion"] = {"dif_abs": dif, "dif_rel": dif / CIFRA,
                      "N_igual": res["N"] == 287 and res["provincias"] == 41}
res["veredicto"] = "COINCIDE" if abs(dif / CIFRA) <= 0.10 and res["comparacion"]["N_igual"] else "DISCREPA"
json.dump(res, open(OUT, "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
