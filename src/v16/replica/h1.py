"""Replica ciega de H1 (V15, P6a): ATT de Callaway-Sant'Anna, renta de contratos nuevos.
Solo estimacion puntual. SEED=20261010 (determinista, sin azar)."""
import json
import os
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
RAIZ = "/home/user/Econometr-a"
SAL = os.path.join(RAIZ, "output/v16/replica/h1")
os.makedirs(SAL, exist_ok=True)

d = pd.read_parquet(os.path.join(RAIZ, "data/processed/v15/p6_zonas_tensionadas.parquet"))
d = d[(d.frecuencia == "T") & d.territorio_codigo.str[:2].isin(["08", "17", "25", "43"])]


def qi(p):
    return int(p[:4]) * 4 + int(p[5]) - 1


d = d.assign(q=d.periodo.map(qi))
Q0, Q1 = qi("2022T2"), qi("2026T1")

# contratos y renta por municipio-trimestre (rejilla vigente desde 2021T2)
c = d[d.variable == "incasol_contratos"]
c = c[(c.q >= Q0) & (c.q <= Q1)]
cont = c.groupby(["territorio_codigo", "q"]).valor.sum().unstack()
r = d[d.variable == "incasol_renta_media"][["territorio_codigo", "q", "desagregacion", "valor"]]
r = r.rename(columns={"valor": "renta"})
cc = c[["territorio_codigo", "q", "desagregacion", "valor"]].rename(columns={"valor": "n"})
m = r.merge(cc, on=["territorio_codigo", "q", "desagregacion"])
m = m[(m.q >= Q0) & (m.q <= Q1) & (m.n > 0)]
m["w"] = m.renta * m.n
g = m.groupby(["territorio_codigo", "q"]).agg(w=("w", "sum"), n=("n", "sum"))
renta = np.log(g.w / g.n).unstack()

# filtro de preperiodo limpio 2022T2-2023T4
pre = [qi("2022T2") + k for k in range(7)]
pc = cont.reindex(columns=pre)
ok = pc.notna().all(axis=1) & (pc.mean(axis=1) >= 5) & (pc > 0).all(axis=1)
muni = pc.index[ok]

# cohortes
z = d[(d.variable == "zt_vigente") & (d.valor == 1)]
prim = z.groupby("territorio_codigo").q.min()
coh = pd.Series(0, index=muni)
for k in muni:
    if k in prim.index:
        coh[k] = prim[k]
n_t = int((coh > 0).sum())
n_nt = int((coh == 0).sum())
print("tratados", n_t, "nunca tratados", n_nt, "N", len(muni))
print(coh[coh > 0].value_counts())

# Callaway-Sant'Anna 2x2, base g-1, control no tratado aun + nunca tratado
R = renta.reindex(muni)
cells = []
for gq in sorted(coh[coh > 0].unique()):
    first = gq + 1 if gq == qi("2024T1") else gq  # 2024T1: efecto desde 2024T2
    for t in range(first, Q1 + 1):
        base = gq - 1
        tr = coh.index[coh == gq]
        ctrl = coh.index[(coh == 0) | (coh > t)]
        if gq == qi("2024T1") and t < qi("2024T4"):
            pass  # controles: nunca tratados + cohorte 2024T4 (aun no tratada)
        trv = tr[R.loc[tr, base].notna() & R.loc[tr, t].notna()]
        ctv = ctrl[R.loc[ctrl, base].notna() & R.loc[ctrl, t].notna()]
        if len(trv) == 0 or len(ctv) == 0:
            continue
        att = (R.loc[trv, t] - R.loc[trv, base]).mean() - (R.loc[ctv, t] - R.loc[ctv, base]).mean()
        cells.append((gq, t, att, len(trv), len(ctv)))
cl = pd.DataFrame(cells, columns=["g", "t", "att", "ntr", "nct"])
att_log = float((cl.att * cl.ntr).sum() / cl.ntr.sum())
att_pct = 100 * (np.exp(att_log) - 1)

ref_N, ref_att = 308, -7.2
dif = att_pct - ref_att
veredicto = "COINCIDE" if (len(muni) == ref_N and abs(dif) <= 0.5) else "DISCREPA"
res = {
    "id": "h1", "pregunta": "H1 P6a zonas tensionadas y renta contratos nuevos (CS, ATT agregado)",
    "seed": SEED, "N": int(len(muni)), "tratados": n_t, "nunca_tratados": n_nt,
    "N_celdas": int(len(cl)),
    "ATT_log_x100": 100 * att_log, "ATT_pct": att_pct,
    "ATT_pct_alt_log_lineal": 100 * att_log,
    "referencia": {"N": ref_N, "ATT_pct": ref_att},
    "diferencia_pp": dif, "veredicto": veredicto,
    "notas": "Sin inferencia (herramientas NO APTAS). ATT en % = 100*(exp(ATT_log)-1). Cohorte 2024T1 efecto desde 2024T2; 2024T4 desde 2024T4; peso = tratados por celda.",
}
json.dump(res, open(os.path.join(SAL, "resultado.json"), "w"), indent=2, ensure_ascii=False)
print(json.dumps(res, indent=2, ensure_ascii=False))
