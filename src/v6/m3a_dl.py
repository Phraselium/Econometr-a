"""M3a v6: deep learning SOLO en el nivel distrito (N grande). (a) MLP tabular con embedding de provincia;
(b) GraphSAGE propio en torch (sin torch_geometric): auto + media de distritos del mismo municipio + media de distritos
de los 4 municipios vecinos (kNN sobre centroides). Presupuesto: 6 configuraciones por red, semilla fija, un hilo.
Selección en bloques espacio-temporales (origen 2020, 4 bloques de CCAA). Se declara «mejor» solo si bate a gradient
boosting con DM-HLN en la validación (M4 lo repite en la sellada)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import m3a_lib as L  # noqa: E402

torch.set_num_threads(1)
torch.use_deterministic_algorithms(True)
GRID = dict(hidden=[16, 32, 64], lr=[1e-3, 3e-3], wd=[1e-4, 1e-3], drop=[0.0, 0.1, 0.2], epochs=[30, 60])
NCFG = 6


class Red(torch.nn.Module):
    def __init__(self, f, nprov, hidden, drop, grafo):
        super().__init__()
        self.grafo = grafo
        self.emb = torch.nn.Embedding(nprov + 1, 4)
        d = f + 4
        self.l1s = torch.nn.Linear(d, hidden)
        if grafo:
            self.l1m = torch.nn.Linear(d, hidden, bias=False)
            self.l1v = torch.nn.Linear(d, hidden, bias=False)
            self.l2s = torch.nn.Linear(hidden, hidden)
            self.l2m = torch.nn.Linear(hidden, hidden, bias=False)
            self.l2v = torch.nn.Linear(hidden, hidden, bias=False)
        else:
            self.l2s = torch.nn.Linear(hidden, hidden)
        self.out = torch.nn.Linear(hidden, 1)
        self.dr = torch.nn.Dropout(drop)

    def forward(self, X, pidx, Am, Av):  # X: [T,n,f]
        Z = torch.cat([X, self.emb(pidx).unsqueeze(0).expand(X.shape[0], -1, -1)], dim=2)
        if self.grafo:
            agg = lambda A, H: torch.stack([torch.sparse.mm(A, H[t]) for t in range(H.shape[0])])  # noqa: E731
            H = torch.relu(self.l1s(Z) + self.l1m(agg(Am, Z)) + self.l1v(agg(Av, Z)))
            H = self.dr(H)
            H = torch.relu(self.l2s(H) + self.l2m(agg(Am, H)) + self.l2v(agg(Av, H)))
        else:
            H = self.dr(torch.relu(self.l1s(Z)))
            H = torch.relu(self.l2s(H))
        return self.out(self.dr(H)).squeeze(-1)  # [T,n]


def _adj(units, cod_mun, xy, k=4):
    n = len(units)
    mun = pd.Series(cod_mun, index=range(n))
    grp = mun.groupby(mun).groups
    r1, c1, v1, r2, c2, v2 = [], [], [], [], [], []
    munxy = pd.DataFrame(xy, columns=["x", "y"]).assign(m=cod_mun).groupby("m").mean().dropna()
    tree = cKDTree(munxy.to_numpy())
    mlist = munxy.index.to_numpy()
    for m, idx in grp.items():
        idx = list(idx)
        for i in idx:
            o = [j for j in idx if j != i]
            if not o:
                continue
            r1 += [i] * len(o)
            c1 += o
            v1 += [1 / len(o)] * len(o)
        if m in munxy.index:
            _, nn = tree.query(munxy.loc[m].to_numpy(), k=min(k + 1, len(mlist)))
            vec = [j for q in np.atleast_1d(nn) if mlist[q] != m for j in grp.get(mlist[q], [])]
            for i in idx:
                r2 += [i] * len(vec)
                c2 += vec
                v2 += [1 / max(len(vec), 1)] * len(vec)
    mk = lambda r, c, v: torch.sparse_coo_tensor(torch.tensor([r, c]), torch.tensor(v, dtype=torch.float32), (n, n)).coalesce()  # noqa: E731
    return mk(r1 or [0], c1 or [0], v1 or [0.0]), mk(r2 or [0], c2 or [0], v2 or [0.0])


def tensores(P, cols, norm=None):
    P = P[P.unit.isin(set(P.dropna(subset=['y']).unit))]  # solo nodos con desenlace observado en algun anio
    units = sorted(P.unit.unique())
    uid = {u: i for i, u in enumerate(units)}
    anios = sorted(P.anio.unique())
    aid = {a: i for i, a in enumerate(anios)}
    f = len(cols)
    X = np.full((len(anios), len(units), f), np.nan, dtype=np.float32)
    ia, iu = P.anio.map(aid).to_numpy(), P.unit.map(uid).to_numpy()
    X[ia, iu] = P[cols].to_numpy(np.float32)
    if norm is None:
        mu, sd = np.nanmean(X, axis=(0, 1)), np.nanstd(X, axis=(0, 1))
        norm = {"mu": np.nan_to_num(mu), "sd": np.where(np.nan_to_num(sd) < 1e-6, 1.0, sd), "cols": cols,
                "conf": np.isnan(X).any(axis=(0, 1)) | True}
    Xn = (X - norm["mu"]) / norm["sd"]
    miss = np.isnan(Xn[..., :]).astype(np.float32)
    Xn = np.concatenate([np.nan_to_num(Xn), miss[..., [i for i, c in enumerate(cols) if c in ("ln_vut_plazas_dis", "dy_lag1", "dy_lag2", "dy_lag1_mun", "ln_pib_pc")]]], axis=2)
    info = P.drop_duplicates("unit").set_index("unit").loc[units]
    pmap = {p: i + 1 for i, p in enumerate(sorted(P.cod_prov.unique()))}
    pidx = torch.tensor(info.cod_prov.map(pmap).to_numpy(), dtype=torch.long)
    Am, Av = _adj(units, info.cod_mun.to_numpy(), info[["x_m", "y_m"]].to_numpy(float))
    return dict(X=torch.tensor(Xn), pidx=pidx, Am=Am, Av=Av, uid=uid, aid=aid, norm=norm, nprov=len(pmap), pmap=pmap)


def ajustar(T, P, cfg, grafo, filas, dy_sd):
    """filas: DataFrame de entrenamiento (con unit, anio, dy)."""
    torch.manual_seed(L.SEED)
    red = Red(T["X"].shape[2], T["nprov"], cfg["hidden"], cfg["drop"], grafo)
    opt = torch.optim.AdamW(red.parameters(), lr=cfg["lr"], weight_decay=cfg["wd"])
    ia = torch.tensor(filas.anio.map(T["aid"]).to_numpy())
    iu = torch.tensor(filas.unit.map(T["uid"]).to_numpy())
    yt = torch.tensor((filas.dy.to_numpy() / dy_sd).astype(np.float32))
    for _ in range(cfg["epochs"]):
        red.train()
        opt.zero_grad()
        out = red(T["X"], T["pidx"], T["Am"], T["Av"])
        loss = torch.mean((out[ia, iu] - yt) ** 2)
        loss.backward()
        opt.step()
    return red


def predecir_filas(red, T, filas, dy_sd):
    red.eval()
    with torch.no_grad():
        out = red(T["X"], T["pidx"], T["Am"], T["Av"]).numpy()
    return out[filas.anio.map(T["aid"]).to_numpy(), filas.unit.map(T["uid"]).to_numpy()] * dy_sd


def predecir_dl(ruta, ficha, P, obj):
    ck = torch.load(ruta, weights_only=False)
    T = tensores(P, ficha["variables"], ck["norm"])
    T["pmap"] = ck["pmap"]
    red = Red(T["X"].shape[2], ck["nprov"], ck["cfg"]["hidden"], 0.0, ck["grafo"])
    red.load_state_dict(ck["state"])
    return obj.y_lag1.to_numpy(float) + predecir_filas(red, T, obj, ck["dy_sd"])


def main():
    out = L.OUT
    P = L.cargar("distrito")
    cols = L.columnas_x("distrito")
    anio_max = int(P.dropna(subset=["y"]).anio.max())
    T = tensores(P, cols)
    P = P.assign(blk=L.bloques_espaciales(P))
    tr_all = P.dropna(subset=["y", "y_lag1", "dy"])
    cfgs = L.muestrear_configs(GRID, NCFG, L.SEED + 7)
    preds, reg, fin = [], [], []
    for nombre, grafo in (("mlp", False), ("gnn", True)):
        sc = []
        for i, cfg in enumerate(cfgs):
            e = []
            o, ymax, vanios = 2020, 2018, [2020, 2021]
            for b in range(4):
                a = tr_all[(tr_all.anio <= ymax) & (tr_all.blk != b)]
                v = tr_all[tr_all.anio.isin(vanios) & (tr_all.blk == b)]
                sd = float(a.dy.std())
                red = ajustar(T, P, cfg, grafo, a, sd)
                e.append(np.sqrt(np.mean((v.dy.to_numpy() - predecir_filas(red, T, v, sd)) ** 2)))
            sc.append(float(np.mean(e)))
            reg.append({"nivel": "distrito", "familia": nombre, "config_id": i, "config": json.dumps(cfg, sort_keys=True),
                        "rmse_bloques_espaciotemporales": sc[-1], "n_bloques": 4,
                        "estado": "especificacion probada (cuenta en el Registry); origen 2020 solo"})
            print(nombre, i, round(sc[-1], 4), flush=True)
        best = cfgs[int(np.argmin(sc))]
        for o, ymax, vanios in L.pliegues("distrito", anio_max):
            a = tr_all[tr_all.anio <= ymax]
            v = tr_all[tr_all.anio.isin(vanios)]
            sd = float(a.dy.std())
            red = ajustar(T, P, best, grafo, a, sd)
            p = v.y_lag1.to_numpy(float) + predecir_filas(red, T, v, sd)
            preds.append(v[["unit", "anio", "y", "y_lag1", "cod_prov", "ccaa"]].assign(origen=o, nivel="distrito", modelo=nombre, pred=p))
        sd = float(tr_all.dy.std())
        red = ajustar(T, P, best, grafo, tr_all, sd)
        mid = f"alquiler_distrito_{nombre}"
        torch.save({"state": red.state_dict(), "norm": T["norm"], "pmap": T["pmap"], "nprov": T["nprov"], "cfg": best,
                    "grafo": grafo, "dy_sd": sd}, out / "modelos" / f"{mid}.pt")
        ficha = {"id": mid, "mercado": "alquiler de stock (SERPAVI)", "nivel": "distrito", "medida": L.YCOL["distrito"],
                 "familia": "dl_gnn" if grafo else "dl_mlp", "variables": cols, "hiperparametros": best, "semilla": L.SEED,
                 "objetivo": "dy = y - y_lag1 (escalado por sd)", "ruta_modelo": f"modelos/{mid}.pt",
                 "funcion_prediccion": "src/v6/m3a_lib.predecir_modelo(id, {nombre: DataFrame sellado})",
                 "nombres_paneles": L.NOMBRES["distrito"], "rmse_bloques_espaciotemporales": min(sc)}
        (out / "modelos" / f"{mid}.json").write_text(json.dumps(ficha, indent=1, ensure_ascii=False))
        fin.append({k: ficha[k] for k in ("id", "nivel", "medida", "familia")} | {"mercado": "alquiler", "ruta": f"output/v6/M3A/modelos/{mid}.json"})
    pd.concat(preds).to_csv(out / "predicciones_cv_dl.csv.gz", index=False)
    pd.DataFrame(reg).to_csv(out / "registro_dl.csv", index=False)
    (out / "modelos_finales_dl.json").write_text(json.dumps(fin, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
