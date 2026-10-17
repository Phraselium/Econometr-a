"""V16 · fase 6 · constructor del shift-share de inmigración (Q3-c y Q4b): cuotas del padrón de 2003 × crecimiento nacional sin la provincia.

x_ut = 100 · Σ_o F_{u,o,b} · (N_{o,t,-g(u)} / N_{o,b,-g(u)}) / Pob_{u,b}   (puntos de la población del año base)
con N_{o,t,-g} = stock nacional (provincias de entrenamiento) del origen o sin la provincia g de la unidad u. Solo datos de entrenamiento.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import qb_comun as C


def cubo(nivel: str) -> tuple[np.ndarray, list, list, np.ndarray]:
    """F[u,t,o] (personas), unidades, años, población total Pob[u,t]. nivel = 'provincia' o 'municipio' (padrón por nacionalidad)."""
    if nivel == "provincia":
        d = C.cargar("base_poblacion", "padron_pob_nacionalidad", "provincia")
    else:
        d = C.cargar("padron_nacionalidad", "padron_municipal_nacionalidad", "municipio")
    d = d.assign(nac=d.desagregacion.str.replace("nacionalidad=", "", regex=False), t=d.periodo.astype(int))
    tot = d[d.nac == "Total"].pivot_table(index="territorio_codigo", columns="t", values="valor", aggfunc="first")
    o = d[d.nac.isin(C.ORIGENES)]
    unidades = list(tot.index)
    años = sorted(tot.columns)
    F = np.zeros((len(unidades), len(años), len(C.ORIGENES)))
    ui = {u: i for i, u in enumerate(unidades)}
    ti = {t: i for i, t in enumerate(años)}
    oi = {n: i for i, n in enumerate(C.ORIGENES)}
    o = o[o.territorio_codigo.isin(ui)]
    F[o.territorio_codigo.map(ui).values, o.t.map(ti).values, o.nac.map(oi).values] = o.valor.fillna(0).values
    return F, unidades, años, tot.reindex(unidades)[años].values


def shiftshare(nivel: str, base: int = 2003, orig_excl: list[str] | None = None) -> dict:
    F, unidades, años, pob = cubo(nivel)
    keep = [i for i, n in enumerate(C.ORIGENES) if not (orig_excl and n in orig_excl)]
    F = F[:, :, keep]
    ib = años.index(base)
    prov = np.array([u[:2] for u in unidades])
    codes = pd.factorize(prov)[0]
    G = codes.max() + 1
    # stock nacional y por provincia por origen y año
    N = F.sum(0)  # (T, O)
    Np = np.zeros((G, F.shape[1], F.shape[2]))
    np.add.at(Np, codes, F)
    Nlo = N[None, :, :] - Np  # (G,T,O)
    ratio = np.where(Nlo[:, ib:ib + 1, :] > 0, Nlo / np.where(Nlo[:, ib:ib + 1, :] > 0, Nlo[:, ib:ib + 1, :], 1), 0.0)
    comp = 100.0 * F[:, ib:ib + 1, :] * ratio[codes] / np.where(pob[:, ib] > 0, pob[:, ib], np.nan)[:, None, None]
    x = np.nansum(comp, axis=2)
    return {"x": x, "comp": comp, "unidades": unidades, "años": años, "pob": pob, "prov": prov, "origenes": [C.ORIGENES[i] for i in keep],
            "F": F, "ib": ib}
