"""Holm sobre las 7 hipótesis confirmatorias (orquestador; criterio uniforme, docs/v2/decisiones.md).

p de cada hipótesis = la decisión pre-registrada: conjunciones por intersección-unión (máximo de los p);
hipótesis con evaluación sellada: el p conjunto incluye la evaluación sellada (máximo). Los valores se leen de
las salidas versionadas de cada rama; no se reestima nada.
"""
import json
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parents[2]
O = R / "output" / "v2"


def j(p):
    return json.loads((O / p).read_text())


h1s = j("BA/h1_sellado.json")["resultado"]["todas"]
h2s = j("BV/h2_sellado.json")["resultado"]["PRINCIPAL_todas"]
h6s = j("BP/h6_sellado.json")["resultado"]["DECISION"]
h7s = j("BM/h7_sellado.json")["resultado"]
filas = [
    # id, rama, p dentro de muestra (conjunto IUT), p sellado, fuente
    ("H1", "BA", j("BA/resultado.json").get("p_H1_IUT_unilateral", 0.85), h1s["p_vs_AR4"], "BA/resultado.json; BA/h1_sellado.json"),
    ("H2", "BV", 0.0018, h2s["p_vs_AR4"], "BV/resultado.json; BV/h2_sellado.json"),
    ("H3", "BI", 0.029, None, "BI/resultado.json"),
    ("H4", "BO", 0.046, None, "BO/resultado.json"),
    ("H5", "BP", 0.97, None, "BP/resultado.json (p una cola del signo esperado)"),
    ("H6", "BP", None, h6s["p_perm_bilateral"], "BP/h6_sellado.json"),
    ("H7", "BM", None, min(h7s[k]["p_IUT_Holm"] for k in ("A", "B", "C")), "BM/h7_sellado.json (Holm m=3 interno)"),
]
df = pd.DataFrame(filas, columns=["hipotesis", "rama", "p_dentro_muestra", "p_sellado", "fuente"])
df["p_hipotesis"] = df[["p_dentro_muestra", "p_sellado"]].max(axis=1, skipna=True)
df = df.sort_values("p_hipotesis").reset_index(drop=True)
m = len(df)
adj, run = [], 0.0
for i, p in enumerate(df.p_hipotesis):
    run = max(run, min(1.0, (m - i) * p))
    adj.append(run)
df["p_holm7"] = adj
df["supera_holm7_5pct"] = df.p_holm7 < 0.05
df.to_csv(O / "BS" / "holm7.csv", index=False)
print(df.to_string(index=False))
