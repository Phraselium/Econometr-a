"""V18 · Conductor común del Monte Carlo de Callaway-Sant'Anna y de Sun-Abraham con wild cluster bootstrap de Webb."""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import functools
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.herramientas.did import CallawaySantAnna, SunAbraham  # noqa: E402
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402
from src.v18.montecarlo._resumen import filas_por_p  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
TAU_ALT = 0.05
CLASES = {"cs": CallawaySantAnna, "sa": SunAbraham}


@functools.lru_cache(maxsize=None)
def _objetos(clase: str, nombre: str, cl: str):
    d = D.diseno(nombre)
    cluster = d.cl_fino if cl == "principal" else d.cl_grueso
    return d, CLASES[clase](d.cohorte, cluster, d.T)


def rep(rng: np.random.Generator, clase: str, nombre: str, tau: float, B: int, comarca: bool, sin_nulo: bool) -> list[float]:
    d, est = _objetos(clase, nombre, "principal")
    Y, efecto = D.simular(d, rng, tau)
    ver = est.verdad(efecto)
    p0, att, _ = est.p_valor(Y, 0.0, rng, B)
    pT = est.p_valor(Y, ver, rng, B)[0] if tau != 0 else p0
    fila = [ver, att, p0, pT]
    if comarca:
        _, est2 = _objetos(clase, nombre, "grueso")
        a0 = est2.p_valor(Y, 0.0, rng, B)[0]
        aT = est2.p_valor(Y, ver, rng, B)[0] if tau != 0 else a0
        fila += [a0, aT]
    if sin_nulo:
        s0 = est.p_valor(Y, 0.0, rng, B, nulo_impuesto=False)[0]
        sT = est.p_valor(Y, ver, rng, B, nulo_impuesto=False)[0] if tau != 0 else s0
        fila += [s0, sT]
    return fila


def correr(clase: str, herramienta_id: int, escenarios: list[str], R: int, B: int, jobs: int, comarca_en: tuple = (), sin_nulo_en: tuple = ()) -> pd.DataFrame:
    filas = []
    for i, nom in enumerate(escenarios):
        t0 = time.time()
        com = nom in comarca_en
        sn = nom in sin_nulo_en
        Mn = C.ejecutar(rep, (clase, nom, 0.0, B, com, sn), R, herramienta_id, i * 10 + 1, jobs)
        Ma = C.ejecutar(rep, (clase, nom, TAU_ALT, B, com, sn), R, herramienta_id, i * 10 + 2, jobs)
        var = {"webb_WCR_t_cluster_principal": (2, 3)}
        k = 4
        if com:
            var["webb_WCR_t_cluster_comarca"] = (k, k + 1)
            k += 2
        if sn:
            var["webb_sin_nulo_impuesto (diagnóstico)"] = (k, k + 1)
        d = D.diseno(nom)
        ex = {"n_tratadas": int((d.cohorte >= 0).sum()), "n_controles": int((d.cohorte < 0).sum()), "T": d.T,
              "clusters": int(len(np.unique(d.cl_fino))), "B": B, "seg": round(time.time() - t0, 1)}
        filas += filas_por_p(nom, var, Mn, Ma, extra=ex)
        print(nom, [(f["variante"], round(f["tamano_5pct"], 4), round(f["cobertura_alt"], 4)) for f in filas[-len(var):]], ex["seg"], flush=True)
    return pd.DataFrame(filas)


def principal(tabla: pd.DataFrame) -> str:
    return "webb_WCR_t_cluster_principal"


def dictamen(tabla: pd.DataFrame) -> tuple[str, str, dict]:
    t = tabla[(tabla.variante == principal(tabla)) & ~tabla.escenario.str.contains("diagnóstico")]
    ok = t[t.veredicto == "APTO"].escenario.tolist()
    mal = t[t.veredicto != "APTO"]
    por = {r.escenario: r.veredicto for r in t.itertuples()}
    if len(mal) == 0:
        return "APTO", "", por
    cond = "; ".join(f"{r.escenario} ({r.fallos})" for r in mal.itertuples())
    if ok:
        return "APTO CONDICIONADO (solo en: " + ", ".join(ok) + ")", cond, por
    return "NO APTO", cond, por
