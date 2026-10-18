"""Replica ciega Q6-p: Wald-DID dosis continua (dCDH), log valor tasado provincial, 2011-2024."""
import json
import numpy as np
import pandas as pd

SEED = 20261010
np.random.seed(SEED)
R = str(__import__("pathlib").Path(__file__).resolve().parents[3]) + "/"
PROV2CCAA = {"04": "01", "11": "01", "14": "01", "18": "01", "21": "01", "23": "01", "29": "01", "41": "01",
             "22": "02", "44": "02", "50": "02", "33": "03", "07": "04", "35": "05", "38": "05", "39": "06",
             "05": "07", "09": "07", "24": "07", "34": "07", "37": "07", "40": "07", "42": "07", "47": "07",
             "49": "07", "02": "08", "13": "08", "16": "08", "19": "08", "45": "08", "08": "09", "17": "09",
             "25": "09", "43": "09", "03": "10", "12": "10", "46": "10", "06": "11", "10": "11", "15": "12",
             "27": "12", "32": "12", "36": "12", "28": "13", "30": "14", "31": "15", "01": "16", "20": "16",
             "48": "16", "26": "17", "51": "18", "52": "19"}
EXCL = {"16", "15", "18", "19"}  # Pais Vasco foral, Navarra (v6), Ceuta, Melilla

iv = pd.read_csv(R + "output/v16/f1/intervenciones.csv", dtype={"cod_ine": str})
iv = iv[iv.parametro.isin(["tipo general ITP", "tipo general ITP (tipo mínimo de la escala)"])].copy()
iv["fe"] = pd.to_datetime(iv.fecha_efecto)
iv = iv.sort_values(["cod_ine", "fe"])
years = range(2009, 2025)
tipo = {}
for c, g in iv.groupby("cod_ine"):
    for y in years:
        s = g[g.fe.dt.year <= y]
        if len(s):
            tipo[(c, y)] = float(s.valor.iloc[-1])  # ultimo en vigor a 31-dic (ultimo cambio del anyo)

d = pd.read_parquet(R + "data/processed/v16/entrenamiento/base_precio.parquet")
d = d[(d.variable == "valor_tasado") & (d.nivel == "provincia") & (d.frecuencia == "A")].copy()
d["y"] = d.periodo.str[:4].astype(int)
d["prov"] = d.territorio_codigo
d["ccaa"] = d.prov.map(PROV2CCAA)
d = d[~d.ccaa.isin(EXCL) & d.ccaa.notna() & (d.y.between(2010, 2024)) & (d.valor > 0)]
d["ly"] = np.log(d.valor)
Y = d.pivot(index="prov", columns="y", values="ly")
cc = {p: PROV2CCAA[p] for p in Y.index}

def dose(c, t):
    a, b = tipo.get((c, t)), tipo.get((c, t - 1))
    return np.nan if a is None or b is None else a - b

def wald(lag=0):
    num = den = 0.0; ns = 0; rows = 0
    for t in range(2011 + 1, 2025):
        tt = t - lag
        # panel 2011-2024: DeltaY_t requiere Y_t, Y_{t-1} dentro de 2011-2024
        dY = (Y[tt] - Y[tt - 1]) if (tt - 1 >= 2011) else None
        if dY is None: continue
        D = pd.Series({p: dose(cc[p], t) for p in Y.index})
        # anticipacion: ccaa que cambia en tt+1 queda fuera del contraste del anyo tt
        ant = pd.Series({p: (dose(cc[p], tt + 1) not in (0, np.nan) and not np.isnan(dose(cc[p], tt + 1))) if tt + 1 <= 2024 else False for p in Y.index})
        ok = dY.notna() & D.notna() & ~ant.astype(bool)
        stab = ok & (D == 0)
        sw = ok & (D != 0)
        if stab.sum() == 0 or sw.sum() == 0: continue
        m = dY[stab].mean()
        num += (dY[sw] - m).sum(); den += D[sw].sum(); ns += sw.sum(); rows += ok.sum()
    return (num / den if den else np.nan), ns

beta, ns = wald(0)
plac, nsp = wald(1) if False else (np.nan, 0)
# N = provincia-anyos con valor tasado en el panel 2011-2024
N = int(d[d.y.between(2011, 2024)].shape[0])
ref = -0.0157; Nref = 485
# bootstrap por CCAA (clusters) para IC
rng = np.random.default_rng(SEED)
cl = sorted(set(cc.values()))
def est_sub(sel):
    global Y, cc
    Y0, cc0 = Y, cc
    Y = Y0.loc[[p for p in Y0.index if cc0[p] in sel]]
    try: return wald(0)[0]
    finally: Y = Y0
bs = []
for _ in range(500):
    s = set(rng.choice(cl, len(cl), replace=True))
    bs.append(est_sub(s))
bs = np.array(bs, float); bs = bs[~np.isnan(bs)]
ic = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
rel = (beta - ref) / abs(ref)
ver = "COINCIDE" if abs(rel) <= 0.10 and abs(N - Nref) / Nref <= 0.01 else "DISCREPA"
res = {"id": "q6p", "N": N, "n_switchers_provincia_anyo": int(ns), "n_provincias": int(Y.shape[0]),
       "estimacion": float(beta), "ic95_bootstrap_ccaa_percentil": ic, "cifra_original": ref, "N_original": Nref,
       "dif_abs": float(beta - ref), "dif_rel": float(rel), "ref_en_ic_replica": bool(ic[0] <= ref <= ic[1]),
       "veredicto": ver, "seed": SEED}
json.dump(res, open(R + "output/v16/replica/q6p/resultado.json", "w"), indent=1, ensure_ascii=False)
print(res)
