"""BM bloque 6: LSTM pequeño SOLO en el panel B (IPC alquiler provincial). Mismos block_splits que el resto; estandarización,
imputación por mediana y efecto fijo (media de y por unidad) ajustados con las filas de entrenamiento de cada split.
Determinista: semilla fija, torch.use_deterministic_algorithms(True), 1 hilo. Fuera de H7 (no es candidato)."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bm_lib as bl  # noqa: E402

VENTANA = 8
LR, WD, BATCH = 0.003, 1e-3, 256
GRID = [(8, 25), (8, 50), (16, 25), (16, 50)]       # (hidden, epochs): 4 configuraciones declaradas en presupuesto.json


def _torch():
    import torch
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    return torch


def lstm_bloques(long, per, splits, cols, units, hidden, epochs, etiqueta, h=bl.H):
    torch = _torch()
    nn = torch.nn
    rows = []
    long = long.sort_values(["unidad", "pos"]).reset_index(drop=True)
    npos = len(per)
    for sid, (itr, ite) in enumerate(splits):
        posL = int(itr[-1])
        tr = (long["pos"] + h <= posL) & long["yh"].notna() & long[bl.AR_COLS].notna().all(axis=1) & long["unidad"].isin(units)
        D = long.loc[tr]
        if len(D) < 50:
            continue
        fe = D.groupby("unidad")["yh"].mean().to_dict()
        sdy = float(np.std(D["yh"].values - D["unidad"].map(fe).values)) or 1.0
        X = D[cols].astype(float)
        c2 = [c for c in cols if X[c].notna().any()]
        med = X[c2].median().fillna(0.0)
        mu = X[c2].fillna(med).mean()
        sd = X[c2].fillna(med).std(ddof=0).replace(0, 1.0)
        mats = {}
        for u, g in long[long["unidad"].isin(units)].groupby("unidad"):
            M = np.full((npos, len(c2)), 0.0, dtype=np.float32)
            Z = ((g[c2].astype(float).fillna(med) - mu) / sd).values
            M[g["pos"].values] = Z
            mats[u] = M

        def seqs(sub):
            xs = [mats[u][p - VENTANA + 1:p + 1] for u, p in zip(sub["unidad"].values, sub["pos"].values)]
            return torch.tensor(np.stack(xs), dtype=torch.float32)
        D = D[D["pos"] >= VENTANA - 1]
        te = long["pos"].isin(set(ite)) & (long["pos"] >= VENTANA - 1) & long[bl.AR_COLS].notna().all(axis=1) & long["unidad"].isin(units)
        T = long.loc[te]
        if D.empty or T.empty:
            continue
        torch.manual_seed(bl.SEED)

        class Net(nn.Module):
            def __init__(s):
                super().__init__()
                s.l = nn.LSTM(len(c2), hidden, batch_first=True)
                s.o = nn.Linear(hidden, 1)

            def forward(s, x):
                return s.o(s.l(x)[0][:, -1]).squeeze(-1)
        net = Net()
        opt = torch.optim.Adam(net.parameters(), lr=LR, weight_decay=WD)
        Xt = seqs(D)
        yt = torch.tensor(((D["yh"].values - D["unidad"].map(fe).values) / sdy), dtype=torch.float32)
        g = torch.Generator().manual_seed(bl.SEED)
        for _ in range(epochs):
            perm = torch.randperm(len(Xt), generator=g)
            for i in range(0, len(Xt), BATCH):
                b = perm[i:i + BATCH]
                opt.zero_grad()
                loss = ((net(Xt[b]) - yt[b]) ** 2).mean()
                loss.backward()
                opt.step()
        net.eval()
        with torch.no_grad():
            pred = net(seqs(T)).numpy() * sdy + T["unidad"].map(fe).values
        rows.append(bl.a_frame(T, pred, per, etiqueta, sid, h))
    cols_out = ["periodo", "periodo_obj", "unidad", "y_real", "y_pred", "modelo", "split", "h"]
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=cols_out)
