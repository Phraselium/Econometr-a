#!/usr/bin/env python3
"""V8-F4 M2: SVAR bayesiano con restricciones de signo y de cero (capa C3s).

Principal pre-registrada (docs/v8/hipotesis.md §5), variantes V1-V3, robustez, version larga (4 variables, 1995T2-2026T2),
hipotesis H8-1..H8-4 (descomposicion historica, probabilidad posterior unilateral + Holm) y congelacion de predicciones (§10).
Usa SOLO src/v8/herramientas/{bvar,signos}.py (validadas en F3, output/v8/F3/var/validacion.md). Todo determinista (SEED=20261010, un hilo).
Uso: python3 src/v8/m2_svar.py [--rapido] [--salida DIR]
Referencias de metodo NO VERIFICADAS (sin acceso a Crossref): Giannone-Lenza-Primiceri (2015); Rubio-Ramirez-Waggoner-Zha (2010);
Arias-Rubio-Ramirez-Waggoner (2018).
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry, holm  # noqa: E402
from herramientas import bvar, signos  # noqa: E402

SEED = 20261010
OP = "V3"      # identificacion operativa: la principal (h=0-1) es inviable con datos reales (ver sondear)
DATOS = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
HS_FEVD = (4, 8, 12, 20)
H_IRF = 20
PERIODOS = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"),
            "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", "2026Q2")}
FACTOR = {"actividad": "empleo_renta", "demografico": "demografia", "demanda": "demanda_vivienda", "oferta": "oferta",
          "credito": "credito_tipos", "monetario": "credito_tipos", "credito_tipos": "credito_tipos"}
NIVEL = ("i", "eur", "dif")   # variables en nivel (no se acumulan)
AVISO_Y6 = ("Aviso (Y6): el BVAR en tasas atenua sistematicamente las IRF hacia cero (sesgo absoluto hasta 0,46; cobertura del 90 % de 0,86-0,90 en F3); "
            "las magnitudes de las IRF y de la descomposicion historica se leen como cota inferior aproximada. "
            "Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas.")


# ------------------------------------------------------------------ utilidades
def qidx(s: str) -> int:
    a, q = s.split("Q")
    return int(a) * 4 + int(q) - 1


def qstr(i: int) -> str:
    return f"{i // 4}Q{i % 4 + 1}"


def md_tabla(df: pd.DataFrame, fmt: str = "{:.2f}") -> str:
    def f(x):
        if isinstance(x, (float, np.floating)):
            return "" if (x != x) else fmt.format(x)
        return str(x)
    cols = list(df.columns)
    df = df.rename(columns=str)
    cols = [str(c) for c in cols]
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(f(r[c]) for c in cols) + " |")
    return "\n".join(out)


def rng_para(*claves) -> np.random.Generator:
    return np.random.default_rng([SEED, *[int(c) for c in claves]])


# ------------------------------------------------------------------ datos
def cargar() -> pd.DataFrame:
    return pd.read_csv(DATOS).set_index("trimestre")


def dl(s: pd.Series) -> pd.Series:
    return 100.0 * s.diff()


def series_base(d: pd.DataFrame, defl: str = "ipc_general") -> pd.DataFrame:
    """Tasas trimestrales log x100 (tipo en nivel). defl: columna del deflactor (IPC general o deflactor del PIB)."""
    ld = np.log(d[defl])
    S = pd.DataFrame(index=d.index)
    S["p"] = dl(np.log(d["p_tasado"]) - ld)
    S["r"] = dl(np.log(d["ipc_alquiler"]) - ld)
    S["q"] = dl(np.log(d["tx_total"]))
    S["c"] = dl(np.log(d["credito_nuevo"]) - ld)
    S["i"] = d["tipo_hip_bce"].where(d["tipo_hip_bce"].notna(), d["tipo_hip_bde"])
    S["e"] = dl(np.log(d["ocupados"]))
    S["n"] = dl(np.log(d["pob_total"]))
    S["y"] = dl(np.log(d["pib_vol_idx"]))
    S["ib"] = d["tipo_hip_bde"]
    S["eur"] = d["euribor_1y"]
    S["dif"] = d["dif_hip_euribor_bce"]
    S["dhpi"] = dl(np.log(d["hpi_ea20"]))
    S["covid"] = d["covid"].astype(float)
    S["epa2021"] = d["epa2021"].astype(float)
    return S


# ------------------------------------------------------------------ restricciones
SHOCKS7 = ["actividad", "demografico", "demanda", "oferta", "credito", "nid1", "nid2"]
VARS7 = ["p", "r", "q", "c", "i", "e", "n"]


def restr_principal(solo_impacto: bool = False) -> signos.Restricciones:
    """Tabla §5 (h=0-1) y 4 ceros en la fila de poblacion (desviaciones.md). solo_impacto = V3 (h=0, sin q en demanda ni oferta)."""
    r = signos.Restricciones(VARS7, SHOCKS7)
    hs = [0] if solo_impacto else [0, 1]
    r.signo("p", "actividad", 1, hs).signo("r", "actividad", 1, hs).signo("c", "actividad", 1, hs).signo("e", "actividad", 1, hs)
    r.signo("r", "demografico", 1, hs).signo("n", "demografico", 1, hs)
    r.signo("p", "demanda", 1, hs).signo("c", "demanda", 1, hs)
    r.signo("p", "oferta", -1, hs)
    r.signo("p", "credito", 1, hs).signo("c", "credito", 1, hs).signo("i", "credito", -1, hs)
    if not solo_impacto:
        r.signo("q", "demanda", 1, hs).signo("q", "oferta", 1, hs)
    for sh in ("actividad", "demanda", "oferta", "credito"):
        r.cero("n", sh, 0)
    return r


VARS_V1 = ["p", "r", "q", "c", "eur", "dif", "e", "n"]
SHOCKS_V1 = ["actividad", "demografico", "demanda", "oferta", "monetario", "credito", "nid1", "nid2"]


def restr_v1(hs=(0,)) -> signos.Restricciones:
    """V1: politica monetaria frente a credito (§5). Monetario: Euribor +, c -. Credito: diferencial -, c +, Euribor = 0 en el impacto.
    Con datos reales h=0-1 es inviable (0 aceptadas en 450.000 rotaciones): se estima solo en el impacto (h=0)."""
    r = signos.Restricciones(VARS_V1, SHOCKS_V1)
    hs = list(hs)
    r.signo("p", "actividad", 1, hs).signo("r", "actividad", 1, hs).signo("c", "actividad", 1, hs).signo("e", "actividad", 1, hs)
    r.signo("r", "demografico", 1, hs).signo("n", "demografico", 1, hs)
    r.signo("p", "demanda", 1, hs).signo("c", "demanda", 1, hs).signo("q", "demanda", 1, hs)
    r.signo("p", "oferta", -1, hs).signo("q", "oferta", 1, hs)
    r.signo("eur", "monetario", 1, hs).signo("c", "monetario", -1, hs)
    r.signo("dif", "credito", -1, hs).signo("c", "credito", 1, hs)
    r.cero("eur", "credito", 0)
    for sh in ("actividad", "demanda", "oferta", "monetario", "credito"):
        r.cero("n", sh, 0)
    return r


VARS_L = ["p", "ib", "y", "n"]
SHOCKS_L = ["actividad", "demografico", "credito_tipos", "residual"]


def restr_larga() -> signos.Restricciones:
    """Version larga (§5): actividad (y+, p+), demografico (n+; n=0 en los demas identificados), credito/tipos (i-, p+)."""
    r = signos.Restricciones(VARS_L, SHOCKS_L)
    hs = [0, 1]
    r.signo("y", "actividad", 1, hs).signo("p", "actividad", 1, hs)
    r.signo("n", "demografico", 1, hs)
    r.signo("ib", "credito_tipos", -1, hs).signo("p", "credito_tipos", 1, hs)
    r.cero("n", "actividad", 0).cero("n", "credito_tipos", 0)
    return r


def construir(nombre: str, d: pd.DataFrame) -> dict:
    """Devuelve la especificacion: Y (DataFrame), X (DataFrame exogenas), restr, delta, p, lam, nombres, rotulos."""
    base = dict(nombre=nombre, p=2, lam=None, defl="ipc_general", solo_impacto=False, euro=False)
    S = series_base(d)
    ex = ["covid", "epa2021"]
    if nombre in ("principal", "V3", "V2", "robust_p1", "robust_p4", "robust_prior_fijo", "robust_sin_covid", "robust_deflactor_pib"):
        vars_, shocks = VARS7, SHOCKS7
        # la principal (h=0-1) es inviable con datos reales; V2 y la robustez se estiman con la identificacion operativa (V3)
        base["solo_impacto"] = nombre != "principal"
        base["restr"] = restr_principal(base["solo_impacto"])
    if nombre == "robust_p1":
        base["p"] = 1
    if nombre == "robust_p4":
        base["p"] = 4
    if nombre == "robust_prior_fijo":
        base["lam"] = 0.2
    if nombre == "robust_deflactor_pib":
        S = series_base(d, "deflactor_pib")
        base["defl"] = "deflactor_pib"
    if nombre == "robust_sin_covid":
        for k, t in enumerate(["2020Q1", "2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2", "2021Q3", "2021Q4"]):
            S[f"d{t}"] = (S.index == t).astype(float)
        ex = ["epa2021"] + [c for c in S.columns if c.startswith("d20")]
    if nombre == "V2":
        S["dhpi_l1"] = S["dhpi"].shift(1)
        ex = ["covid", "epa2021", "dhpi", "dhpi_l1"]
        base["euro"] = True
    if nombre == "V1":
        vars_, shocks = VARS_V1, SHOCKS_V1
        base["restr"] = restr_v1((0,))
        base["solo_impacto"] = True
    if nombre == "larga":
        vars_, shocks = VARS_L, SHOCKS_L
        base["restr"] = restr_larga()
        ex = ["covid"]
    cols = vars_ + ex
    Z = S[cols].dropna()
    Y, X = Z[vars_], Z[ex]
    delta = np.array([1.0 if v in NIVEL or v == "ib" else 0.0 for v in vars_])
    base.update(Y=Y, X=X, vars=vars_, shocks=shocks, delta=delta)
    return base


# ------------------------------------------------------------------ estimacion
def identificar_ess(spec, post, objetivo, M, D0, Dmax, clave, rapido=False):
    """Piloto con D0 sorteos para dimensionar D; luego una unica llamada a identificar (pesos coherentes). Devuelve (res, D, intentos)."""
    n, p, restr = post["n"], post["p"], spec["restr"]
    rg = rng_para(clave, 1)
    B, S = bvar.muestrear(post, D0, rg)
    pil = signos.identificar(B, S, n, p, restr, H=H_IRF, rotaciones=M, rng=rg)
    ess0 = pil["ess"]
    del pil
    D = min(Dmax, 4 * D0) if ess0 < 1.0 else min(Dmax, max(D0, int(math.ceil(D0 * objetivo * 1.3 / ess0))))
    if rapido:
        D = D0
    intentos = 0
    while True:
        intentos += 1
        rg = rng_para(clave, 2, intentos)
        B, S = bvar.muestrear(post, D, rg)
        res = signos.identificar(B, S, n, p, restr, H=H_IRF, rotaciones=M, rng=rg)
        if rapido or res["ess"] >= objetivo or D >= Dmax or intentos >= 3:
            return res, D, intentos, ess0
        D = min(Dmax, int(math.ceil(D * objetivo * 1.2 / max(res["ess"], 1.0))))


def hd_por_tramos(res, Y, X, tramos, fechas, chunk=250, aislar_cols=None):
    """Descomposicion historica sumada por tramos para TODOS los sorteos aceptados (por bloques, memoria acotada).
    Devuelve contrib (N, tramo, var, shock), det (N, tramo, var), eur (N, tramo, var) (efecto de las columnas aislar_cols), error."""
    n, p = res["n"], res["p"]
    N = len(res["Q"])
    Yv, Xv = Y.values, (X.values if X is not None else None)
    X0 = None
    if aislar_cols:
        X0 = X.copy()
        for c in aislar_cols:
            X0[c] = 0.0
        X0 = X0.values
    C, Dd, Ee, err = [], [], [], 0.0
    for a in range(0, N, chunk):
        sub = dict(B=res["B"][a:a + chunk], A0inv=res["A0inv"][a:a + chunk], n=n, p=p)
        hd = signos.descomposicion_historica(sub, Yv, exog=Xv)
        err = max(err, hd["error"])
        C.append(signos.sumar_tramos(hd["contrib"], fechas, tramos))
        Dd.append(signos.sumar_tramos(hd["det"][..., None], fechas, tramos)[..., 0])
        if aislar_cols:
            hd0 = signos.descomposicion_historica(sub, Yv, exog=X0)
            Ee.append(signos.sumar_tramos((hd["det_exog"] - hd0["det_exog"])[..., None], fechas, tramos)[..., 0])
    eur = np.concatenate(Ee) if Ee else np.zeros_like(np.concatenate(Dd))
    return np.concatenate(C), np.concatenate(Dd), eur, err


def periodos_cubiertos(idx_hd):
    """Periodos P1-P5 cubiertos al menos en el 80 % de sus trimestres por la muestra de la DH: [(codigo, ini_i, fin_i, cobertura)]."""
    a, b = qidx(idx_hd[0]), qidx(idx_hd[-1])
    out = []
    for cod, (i0, i1) in PERIODOS.items():
        s, e = qidx(i0), qidx(i1)
        ov = min(b, e) - max(a, s) + 1
        if ov >= 0.8 * (e - s + 1):
            cob = "completa" if (a <= s and b >= e) else ("parcial_ini" if a > s and b >= e else "parcial_fin")
            out.append((cod, s, e, cob))
    return out


def banda_fila(x, w):
    b = bvar.bandas(x, 0, w)
    return dict(mediana=float(b["med"]), b68_lo=float(b["lo68"]), b68_hi=float(b["hi68"]), b90_lo=float(b["lo90"]), b90_hi=float(b["hi90"]))


def procesar(spec, objetivo, M, D0, Dmax, clave, rapido, reg, hs=HS_FEVD, tiempos=None):
    """Estima, identifica y resume una especificacion. Devuelve dict con DataFrames y objetos internos."""
    t0 = time.time()
    nombre, Y, X, p = spec["nombre"], spec["Y"], spec["X"], spec["p"]
    post = bvar.estimar(Y.values, p, lam=spec["lam"], delta=spec["delta"], exog=X.values)
    res, D, intentos, ess0 = identificar_ess(spec, post, objetivo, M, D0, Dmax, clave, rapido)
    N = len(res["Q"])
    tid = time.time() - t0
    vars_, shocks, w = spec["vars"], spec["shocks"], res["peso"]
    diag = dict(variante=nombre, N_obs=int(Y.shape[0]), muestra_ini=Y.index[0], muestra_fin=Y.index[-1], p=p, lam=float(post["lam"]),
                logml=float(post["logml"]), D_sorteos_theta=int(D), intentos=intentos, ess_piloto=float(ess0), M_rotaciones=M,
                n_aceptadas=N, ess=float(res["ess"]), acept_por_rotacion=float(res["acept"]), frac_theta_acept=float(res["frac_theta_acept"]),
                objetivo_ess=objetivo, cumple_ess=bool(res["ess"] >= objetivo))
    out = dict(spec=spec, post=post, res=res, diag=diag)
    if N < 5:
        diag["nota"] = "menos de 5 aceptadas: identificacion inviable con estos sorteos; sin resultados"
        out.update(irf=pd.DataFrame(), irf_acum=pd.DataFrame(), fevd=pd.DataFrame(), hd=pd.DataFrame(), hdraw=None)
        if tiempos is not None:
            tiempos[nombre] = dict(identificacion=tid, total=time.time() - t0)
        return out
    mz, fs = signos.comprobar(res, spec["restr"])
    diag.update(max_abs_cero=float(mz), frac_signos_cumplidos=float(fs))
    # --- IRF y FEVD
    rs = signos.resumen(res, hs)
    irf_rows, ac_rows = [], []
    bi = rs["irf"]
    for sj, sh in enumerate(shocks):
        for vi, v in enumerate(vars_):
            for h in range(H_IRF + 1):
                irf_rows.append((nombre, sh, v, h, bi["med"][h, vi, sj], bi["lo68"][h, vi, sj], bi["hi68"][h, vi, sj], bi["lo90"][h, vi, sj], bi["hi90"][h, vi, sj]))
    irf = pd.DataFrame(irf_rows, columns=["variante", "shock", "variable", "h", "mediana", "b68_lo", "b68_hi", "b90_lo", "b90_hi"])
    acum_idx = [k for k, v in enumerate(vars_) if v not in NIVEL and v != "ib"]
    ba = bvar.bandas(np.cumsum(res["irf"][:, :, acum_idx, :], axis=1), 0, w)
    for sj, sh in enumerate(shocks):
        for kk, vi in enumerate(acum_idx):
            for h in range(H_IRF + 1):
                ac_rows.append((nombre, sh, vars_[vi], h, ba["med"][h, kk, sj], ba["lo68"][h, kk, sj], ba["hi68"][h, kk, sj], ba["lo90"][h, kk, sj], ba["hi90"][h, kk, sj]))
    irf_ac = pd.DataFrame(ac_rows, columns=irf.columns)
    bf = rs["fevd"]
    fr = []
    for vi, v in enumerate(vars_):
        for hi_, h in enumerate(hs):
            for sj, sh in enumerate(shocks):
                fr.append((nombre, v, h, sh, bf["med"][hi_, vi, sj], bf["lo68"][hi_, vi, sj], bf["hi68"][hi_, vi, sj]))
    fev = pd.DataFrame(fr, columns=["variante", "variable", "h", "shock", "mediana", "b68_lo", "b68_hi"])
    # --- descomposicion historica por periodos
    idx_hd = list(Y.index[p:])
    fechas = np.array([qidx(s) for s in idx_hd])
    pers = periodos_cubiertos(idx_hd)
    hd_rows, hdraw = [], {}
    if pers:
        tramos = [(s, e) for (_, s, e, _) in pers]
        aislar = ["dhpi", "dhpi_l1"] if spec["euro"] else None
        C, Dd, Ee, err = hd_por_tramos(res, Y, X, tramos, fechas, aislar_cols=aislar)
        diag["hd_error_max"] = float(err)
        yv = Y.values[p:]
        mercados = [("compra", vars_.index("p"))] + ([("alquiler", vars_.index("r"))] if "r" in vars_ else [])
        ids = [sh for sh in shocks if not sh.startswith("nid") and sh != "residual"]
        nidn = [sh for sh in shocks if sh.startswith("nid") or sh == "residual"]
        for mk, vi in mercados:
            for ti, (cod, s, e, cob) in enumerate(pers):
                m = (fechas >= s) & (fechas <= e)
                tot = float(yv[m, vi].sum())
                comp = {sh: C[:, ti, vi, shocks.index(sh)] for sh in ids}
                comp["no_identificados"] = sum(C[:, ti, vi, shocks.index(sh)] for sh in nidn)
                if spec["euro"]:
                    comp["factor_europeo"] = Ee[:, ti, vi]
                comp["determinista"] = Dd[:, ti, vi] - (Ee[:, ti, vi] if spec["euro"] else 0.0)
                hdraw[(mk, cod)] = dict(comp=comp, total=tot)
                for fk, x in comp.items():
                    b = banda_fila(x, w)
                    bp = banda_fila(x / tot * 100.0, w) if abs(tot) > 1e-9 else {}
                    hd_rows.append(dict(variante=nombre, mercado=mk, periodo=cod, factor=fk, contribucion_pp=b["mediana"],
                                        pct_total=bp.get("mediana", np.nan), b68_lo=b["b68_lo"], b68_hi=b["b68_hi"], b90_lo=b["b90_lo"],
                                        b90_hi=b["b90_hi"], prob_pos=float(w[x > 0].sum()), n_trim=int(m.sum()), cobertura=cob, total_obs_pp=tot,
                                        pct_b68_lo=bp.get("b68_lo", np.nan), pct_b68_hi=bp.get("b68_hi", np.nan)))
                cerrado = sum(comp.values())
                diag.setdefault("cierre_hd_max", 0.0)
                diag["cierre_hd_max"] = max(diag["cierre_hd_max"], float(np.max(np.abs(cerrado - tot))))
    hd = pd.DataFrame(hd_rows)
    out.update(irf=irf, irf_acum=irf_ac, fevd=fev, hd=hd, hdraw=hdraw)
    if reg is not None:
        reg.log("V8-M2", f"M2_{nombre}", f"BVAR-GLP({','.join(vars_)}; p={p}; exog={','.join(X.columns)}) + signos/ceros h={'0' if spec['solo_impacto'] else '0-1'}",
                Y.index[0], Y.index[-1], int(Y.shape[0]), np.nan, np.nan, np.nan, notas=f"lam={diag['lam']:.4f}; logml={diag['logml']:.2f}; D={D}; N={N}; ESS={diag['ess']:.1f}; "
                f"acept_theta={diag['frac_theta_acept']:.3f}; lam_fijo={spec['lam']}; defl={spec['defl']}")
    if tiempos is not None:
        tiempos[nombre] = dict(identificacion=tid, total=time.time() - t0)
    return out


def sondear(spec, D, M, clave, reg):
    """Sondeo de viabilidad de la identificacion pre-registrada (h=0-1, 4 ceros) con datos reales: D sorteos de theta x M rotaciones."""
    Y, X, p = spec["Y"], spec["X"], spec["p"]
    post = bvar.estimar(Y.values, p, lam=spec["lam"], delta=spec["delta"], exog=X.values)
    rg = rng_para(clave, 1)
    B, S = bvar.muestrear(post, D, rg)
    res = signos.identificar(B, S, post["n"], p, spec["restr"], H=2, rotaciones=M, rng=rg)
    N = len(res["Q"])
    diag = dict(variante=spec["nombre"], N_obs=int(Y.shape[0]), muestra_ini=Y.index[0], muestra_fin=Y.index[-1], p=p, lam=float(post["lam"]),
                logml=float(post["logml"]), D_sorteos_theta=int(D), M_rotaciones=M, rotaciones_probadas=int(res["rot_total"]), n_aceptadas=N,
                ess=float(res["ess"]), acept_por_rotacion=float(res["acept"]), frac_theta_acept=float(res["frac_theta_acept"]),
                estado="INVIABLE" if N < 5 else "viable", nota="identificacion pre-registrada inviable con datos reales: ninguna rotacion cumple las 28 restricciones de signo (14 celdas x h=0-1) y los 4 ceros" if N < 5 else "")
    if reg is not None:
        reg.log("V8-M2", "M2_principal_sondeo", "BVAR-GLP(p,r,q,c,i,e,n; p=2) + signos h=0-1 + 4 ceros (sondeo de viabilidad)", Y.index[0], Y.index[-1], int(Y.shape[0]),
                np.nan, np.nan, np.nan, notas=f"rotaciones={res['rot_total']}; aceptadas={N}; estado={diag['estado']}")
    return diag


# ------------------------------------------------------------------ hipotesis
HIPOTESIS = [
    ("H8-1", "En P5, la contribucion del shock demografico a la subida del alquiler real es positiva", "alquiler", "P5", ["demografico"], +1),
    ("H8-2", "En P5, la contribucion de credito y tipos al precio real de compra es negativa", "compra", "P5", ["credito"], -1),
    ("H8-3", "En P3, la contribucion de actividad y renta al precio real de compra es positiva", "compra", "P3", ["actividad"], +1),
    ("H8-4", "En P2, la contribucion conjunta de credito y tipos y de actividad y renta al precio real de compra es negativa", "compra", "P2",
     ["credito", "actividad"], -1),
]


def hipotesis(out, reg):
    hd = out["hdraw"]
    w = out["res"]["peso"]
    ess = out["diag"]["ess"]
    filas = []
    for hid, txt, mk, per, fac, sg in HIPOTESIS:
        if hd is None or (mk, per) not in hd:
            filas.append(dict(id=hid, hipotesis=txt, mercado=mk, periodo=per, signo_esperado=sg, nota="periodo no cubierto"))
            continue
        x = sum(hd[(mk, per)]["comp"][f] for f in fac)
        pr = float(w[x > 0].sum()) if sg > 0 else float(w[x < 0].sum())
        b = banda_fila(x, w)
        q95 = bvar.cuantiles(x, [0.025, 0.975], 0, w)
        filas.append(dict(id=hid, hipotesis=txt, mercado=mk, periodo=per, factor="+".join(fac), signo_esperado=sg, contribucion_pp=b["mediana"],
                          b68_lo=b["b68_lo"], b68_hi=b["b68_hi"], b90_lo=b["b90_lo"], b90_hi=b["b90_hi"], ic95_lo=float(q95[0]), ic95_hi=float(q95[1]),
                          prob_posterior=pr, p_unilateral=1.0 - pr, resolucion_p=1.0 / ess))
    df = pd.DataFrame(filas)
    ok = df["p_unilateral"].notna()
    hp = holm({r["id"]: r["p_unilateral"] for _, r in df[ok].iterrows()})
    df["p_holm"] = df["id"].map(hp)
    df["metodo_ajuste"] = "Holm"
    df["rechaza_H0_alfa05"] = df["p_holm"] < 0.05
    df["capa"] = "C3s"
    df["estado"] = np.where(df["rechaza_H0_alfa05"], "respaldada (P posterior alta tras Holm), condicionada a los supuestos",
                            np.where(df["p_unilateral"] < 0.5, "no respaldada tras Holm (inclina al signo esperado, p_unilateral < 0,5)",
                                     "no respaldada (la mediana apunta al signo contrario o no distingue)"))
    df["nota"] = "Prob. posterior unilateral sobre la contribucion acumulada del periodo (DH, sorteos ponderados); capa C3s; magnitudes posiblemente atenuadas (Y6)"
    if reg is not None:
        for _, r in df.iterrows():
            reg.log("V8-M2", f"M2_{r['id']}", f"P({r['factor'] if 'factor' in r else ''} {'>' if r['signo_esperado'] > 0 else '<'} 0 | datos), {r['mercado']} {r['periodo']}",
                    "", "", out["diag"]["N_obs"], np.nan, np.nan, np.nan, coef_interes=r.get("contribucion_pp", np.nan),
                    p_interes=r.get("p_unilateral", np.nan), notas=f"p_holm={r.get('p_holm', np.nan):.4f}; Holm en la familia {{H8-1..H8-4}}")
    return df


# ------------------------------------------------------------------ atribucion
def atribucion(out, tag):
    """atribucion.csv (metodo=svar_hd) mapeando shocks a factores del contrato."""
    hd, w, spec = out["hdraw"], out["res"]["peso"], out["spec"]
    rows = []
    if not hd:
        return rows
    for (mk, per), dd in hd.items():
        comp, tot = dd["comp"], dd["total"]
        cob = [cb for (c, _, _, cb) in periodos_cubiertos(list(spec["Y"].index[spec["p"]:])) if c == per][0]
        grupos = {}
        for sh, x in comp.items():
            if sh in FACTOR:
                f = FACTOR[sh]
            elif sh == "factor_europeo":
                f = "factor_europeo"
            else:
                f = "residuo"       # no_identificados + determinista (+ residual en la larga)
            grupos[f] = grupos.get(f, 0.0) + x
        for f, x in grupos.items():
            b = banda_fila(x, w)
            pct = x / tot * 100.0 if abs(tot) > 1e-9 else None
            rows.append(dict(metodo="svar_hd", mercado=mk, ambito="nacional", periodo=per, factor=f if f != "demanda_vivienda" else "demanda_vivienda",
                             contribucion_pp=b["mediana"], pct_total=float(np.median(pct)) if pct is not None else np.nan,
                             b68_lo=b["b68_lo"], b68_hi=b["b68_hi"], b90_lo=b["b90_lo"], b90_hi=b["b90_hi"],
                             capa="C4" if f == "residuo" else "C3s",
                             notas=f"variante={tag}; total_observado_pp={tot:.3f}; cobertura_periodo={cob}; factor 'demanda_vivienda' = demanda especifica de vivienda "
                                   "(no esta en la lista del contrato); residuo = no identificados + determinista; C3s condicionada a los supuestos; magnitudes posiblemente atenuadas (Y6)"))
    return rows


# ------------------------------------------------------------------ congelacion
def congelar(out, d, salida: Path, rapido):
    """Predicciones de forma reducida del BVAR principal (p y r), sin identificacion. Origen: ultimo trimestre de la muestra comun (2026T1)."""
    post, spec = out["post"], out["spec"]
    H = 5
    rg = rng_para(77)
    nd = 400 if rapido else 5000
    Xf = np.array([[0.0, 1.0]] * H)       # covid = 0, epa2021 = 1 (nivel desde 2021T1)
    pr = bvar.prediccion(post, h=H, ndraw=nd, rng=rg, exog_futuro=Xf)
    vars_ = spec["vars"]
    fin = qidx(spec["Y"].index[-1])
    filas = []
    for v, mk in (("p", "compra"), ("r", "alquiler")):
        vi = vars_.index(v)
        x = pr[:, :, vi]
        for h in range(1, H + 1):
            bb = bvar.bandas(x[:, h - 1], 0)
            fila = dict(variable=v, mercado=mk, medida="tasa_trim_pp(log x100, real)", h_desde_origen=h, origen=qstr(fin), h_desde_2026T2=h - 1,
                        fecha_objetivo=qstr(fin + h), evaluable=bool(h >= 2), mediana=float(bb["med"]), b68_lo=float(bb["lo68"]), b68_hi=float(bb["hi68"]),
                        b90_lo=float(bb["lo90"]), b90_hi=float(bb["hi90"]))
            filas.append(fila)
            if h >= 2:   # acumulado desde 2026T2 (base = nivel de 2026T2) hasta el trimestre objetivo
                ac = x[:, 1:h].sum(1)
                ba = bvar.bandas(ac, 0)
                filas.append(dict(variable=v, mercado=mk, medida="acumulado_desde_2026T2_pp", h_desde_origen=h, origen=qstr(fin), h_desde_2026T2=h - 1,
                                  fecha_objetivo=qstr(fin + h), evaluable=True, mediana=float(ba["med"]), b68_lo=float(ba["lo68"]), b68_hi=float(ba["hi68"]),
                                  b90_lo=float(ba["lo90"]), b90_hi=float(ba["hi90"])))
    df = pd.DataFrame(filas).round({"mediana": 10, "b68_lo": 10, "b68_hi": 10, "b90_lo": 10, "b90_hi": 10})
    fcsv = salida / "predicciones_congeladas.csv"
    df.to_csv(fcsv, index=False, float_format="%.10g")
    sha = hashlib.sha256(fcsv.read_bytes()).hexdigest()
    meta = dict(fichero="predicciones_congeladas.csv", sha256=sha, modelo="BVAR-GLP principal (forma reducida, 7 variables, p=2, delta 0 en tasas y 1 en i)",
                origen=qstr(fin), objetivo_evaluate_v8="2026T3-2027T2 (h_desde_2026T2 = 1..4, filas evaluable=True)",
                lam=out["diag"]["lam"], muestra=f"{spec['Y'].index[0]}-{spec['Y'].index[-1]}", ndraw=nd, seed=SEED,
                nota=("tx_total (compraventas MIVAU) acaba en 2026T1, por lo que la muestra comun del BVAR principal acaba en 2026T1 y el origen es 2026T1 (no 2026T2): "
                      "h=1 (2026T2) ya es un dato y NO se evalua; las filas evaluables son h=2..5 desde 2026T1 = h=1..4 desde 2026T2 (docs/v8/desviaciones.md)."),
                congelado_en="ver commit/etiqueta de la release (docs/v8/notas_release.md)")
    (salida / "congelacion.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    return df, meta


# ------------------------------------------------------------------ resumen
def tabla_irf(irf_ac: pd.DataFrame, var: str, nombre: str):
    t = irf_ac[(irf_ac.variante == nombre) & (irf_ac.variable == var) & (irf_ac.h.isin(HS_FEVD))]
    f = t.assign(txt=lambda z: z.apply(lambda r: f"{r.mediana:.2f} [{r.b68_lo:.2f}; {r.b68_hi:.2f}]", axis=1))
    return f.pivot(index="shock", columns="h", values="txt").reindex(columns=list(HS_FEVD)).reset_index()


def escribir_resumen(salida, outs, hip, fev_all, hd_all, ess_tab, desv, meta, rapido):
    L = []
    pr = outs[OP]
    L.append("# M2: SVAR bayesiano con restricciones de signo y de cero (V8-F4)\n")
    L.append("Capa C3s: la identificacion vale solo bajo las restricciones de signo y de cero declaradas en docs/v8/hipotesis.md §5; "
             "el lenguaje causal queda condicionado a ellas. Referencias de metodo NO VERIFICADAS.\n")
    if rapido:
        L.append("**MODO RAPIDO (--rapido): resultados de prueba, no validos para su publicacion.**\n")
    L.append("## Avisos\n")
    L.append(f"- {AVISO_Y6}")
    L.append("- Las bandas de la descomposicion historica casi nunca excluyen el cero con T de unos 88 (Y6): una contribucion cuya banda incluye el cero se lee como «no distinguible de cero».")
    L.append("- Los dos shocks sin identificar quedan sin restricciones; sus resultados no se interpretan. Los elementos no restringidos solo se leen si su banda excluye el cero (Y4).")
    L.append("- Los pesos de importancia (ceros) son una derivacion propia NO VERIFICADA frente al articulo (Y4).")
    L.append(f"- Muestra efectiva ({OP}): {pr['diag']['muestra_ini']}-{pr['diag']['muestra_fin']} (N={pr['diag']['N_obs']}); "
             "la compraventas MIVAU (tx_total) acaba en 2026T1, por lo que P5 cubre 2022T3-2026T1 (15 trimestres) en las variantes de 7 variables y 2022T3-2026T2 en la larga.")
    L.append("- `pob_total` es una interpolacion lineal entre fechas semestrales hasta 2020 (marcada en el panel): la dinamica de n es suave por construccion; "
             "las conclusiones sobre el shock demografico dependen de ello.")
    L.append("- Contribuciones en puntos log x100 de la variacion acumulada del periodo (precio y alquiler reales, deflactor IPC); %: contribucion / variacion observada del periodo "
             "(inestable si la variacion observada es cercana a cero). `determinista` = condiciones iniciales + constante + ficticias (COVID, EPA 2021T1).\n")
    sd = meta["sondeo"]
    L.append("## Estado de la identificacion pre-registrada (principal, h = 0-1)\n")
    L.append(f"- Sondeo con datos reales: {sd['D_sorteos_theta']} sorteos de theta x {sd['M_rotaciones']} rotaciones = {sd['rotaciones_probadas']:,} rotaciones; "
             f"aceptadas = {sd['n_aceptadas']}. Estado: **{sd['estado']}**.".replace(",", "."))
    L.append(f"- Operativa: **{OP}** (solo impacto h = 0, sin la restriccion de q en demanda y oferta; pre-registrada como variante V3, Y6). "
             "Las hipotesis H8-1..H8-4, la atribucion y la congelacion usan esta identificacion; la forma reducida congelada es la misma del principal. "
             "La V1, V2 y la robustez se estiman tambien con restricciones solo de impacto (V1 h = 0-1 es inviable con datos reales).\n")
    d = pr["diag"]
    L.append("## Muestreo y ESS\n")
    L.append(md_tabla(ess_tab, "{:.3g}") + "\n")
    L.append(f"{OP}: ESS = {d['ess']:.0f} (objetivo >= {d['objetivo_ess']}); {d['n_aceptadas']} rotaciones aceptadas de {d['D_sorteos_theta']} sorteos de theta "
             f"({d['frac_theta_acept']*100:.1f} % de los theta aportan); lambda GLP = {d['lam']:.4f}; error maximo de la identidad de la DH = {d.get('hd_error_max', float('nan')):.1e}.\n")
    if "irf" in pr and len(pr["irf_acum"]):
        L.append("## IRF acumuladas (operativa V3) (nivel de p y r, h = 4, 8, 12, 20; mediana [banda 68 %], por shock de 1 d.t.)\n")
        for v, nom in (("p", "Precio real de compra"), ("r", "Alquiler real")):
            L.append(f"**{nom}**\n")
            L.append(md_tabla(tabla_irf(pr["irf_acum"], v, OP)) + "\n")
    L.append("## FEVD (V3 operativa) (mediana; h = 4, 8, 12, 20)\n")
    for v, nom in (("p", "Precio real de compra"), ("r", "Alquiler real")):
        f = fev_all[(fev_all.variante == OP) & (fev_all.variable == v)]
        t = f.pivot(index="shock", columns="h", values="mediana").reindex(columns=list(HS_FEVD)).reset_index()
        L.append(f"**{nom}**\n")
        L.append(md_tabla(t, "{:.3f}") + "\n")
    L.append("## Descomposicion historica (V3 operativa) por periodo y mercado\n")
    for mk in ("compra", "alquiler"):
        h = hd_all[(hd_all.variante == OP) & (hd_all.mercado == mk)]
        if h.empty:
            continue
        L.append(f"**{mk}** (pp log x100; mediana [68 %]; [90 %]; P(>0))\n")
        h = h.assign(txt=lambda z: z.apply(lambda r: f"{r.contribucion_pp:.1f} [{r.b68_lo:.1f}; {r.b68_hi:.1f}] ({r.b90_lo:.1f}; {r.b90_hi:.1f}) p+={r.prob_pos:.2f}", axis=1))
        t = h.pivot(index="factor", columns="periodo", values="txt").reset_index()
        tot = h.groupby("periodo")["total_obs_pp"].first()
        L.append(md_tabla(t) + "\n")
        L.append("Variacion observada (pp): " + "; ".join(f"{k} = {v:.1f}" for k, v in tot.items()) + "\n")
    L.append("## Hipotesis confirmatorias H8-1 a H8-4 (Holm en la familia)\n")
    t = hip[["id", "mercado", "periodo", "factor", "signo_esperado", "contribucion_pp", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "prob_posterior", "p_unilateral", "p_holm", "estado"]]
    L.append(md_tabla(t, "{:.3f}") + "\n")
    L.append("Lectura: cada p es 1 - P(posterior del signo esperado); resolucion minima de p = 1/ESS. Resultados bajo los supuestos de identificacion (C3s); magnitudes atenuadas (Y6).\n")
    L.append("## Variantes y robustez: contribucion mediana de cada hipotesis (pp) y P(signo esperado)\n")
    filas = []
    for nom, o in outs.items():
        if nom == "larga" or not len(o["hd"]):
            continue
        row = {"variante": nom, "ESS": o["diag"]["ess"]}
        for hid, txt, mk, per, fac, sg in HIPOTESIS:
            dd = o["hdraw"].get((mk, per))
            if dd is None:
                row[hid] = "n.c."
                continue
            x = sum(dd["comp"][f] for f in fac if f in dd["comp"]) if all(f in dd["comp"] for f in fac) else None
            if x is None:
                row[hid] = "n.c."
                continue
            w = o["res"]["peso"]
            pp = float(w[x > 0].sum() if sg > 0 else w[x < 0].sum())
            row[hid] = f"{float(bvar.cuantiles(x, [0.5], 0, w)[0]):.1f} (P={pp:.2f})"
        filas.append(row)
    L.append(md_tabla(pd.DataFrame(filas), "{:.0f}") + "\n")
    L.append("Celdas: mediana de la contribucion conjunta en pp (P = probabilidad posterior del signo esperado). En V1 el shock «credito» no incluye el monetario "
             "(H8-2/H8-4 con V1 usan solo `credito`; `monetario` esta en hd_periodos.csv). V1, V2 y la robustez usan la identificacion operativa solo de impacto. "
             "n.c. = periodo no cubierto o factor no definido en esa variante.\n")
    if "larga" in outs and len(outs["larga"]["hd"]):
        L.append("## Version larga (4 variables, 1995T2-2026T2): contribucion a la variacion del precio real de compra (pp)\n")
        h = hd_all[(hd_all.variante == "larga") & (hd_all.mercado == "compra")]
        h = h.assign(txt=lambda z: z.apply(lambda r: f"{r.contribucion_pp:.1f} [{r.b68_lo:.1f}; {r.b68_hi:.1f}]", axis=1))
        L.append(md_tabla(h.pivot(index="factor", columns="periodo", values="txt").reset_index()) + "\n")
        L.append(f"ESS larga = {outs['larga']['diag']['ess']:.0f}. Es un contraste (C3s) con 4 variables; el shock `residual` no esta identificado.\n")
    L.append("## Congelacion para evaluate_v8 (§10)\n")
    L.append(f"- Fichero: output/v8/M2/predicciones_congeladas.csv; sha256 = `{meta['sha256']}` (congelacion.json).")
    L.append(f"- {meta['nota']}\n")
    L.append("## Desviaciones y decisiones de ejecucion\n")
    for s in desv:
        L.append(f"- {s}")
    (salida / "resumen.md").write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args(argv)
    rapido = a.rapido
    salida = Path(a.salida) if a.salida else (RAIZ / "output" / "v8" / ("M2_rapido" if rapido else "M2"))
    salida.mkdir(parents=True, exist_ok=True)
    reg = Registry(salida / "registro.csv")
    d = cargar()
    tiempos = {}
    if rapido:
        cfg = dict(objetivo=0, M=1500, D0=60, Dmax=60)
        cfgL = dict(objetivo=0, M=300, D0=150, Dmax=150)
        orden = ["V3", "larga"]
    else:
        cfg = dict(objetivo=500, M=3000, D0=300, Dmax=40000)
        cfgL = dict(objetivo=500, M=3000, D0=300, Dmax=40000)
        orden = ["V3", "V1", "V2", "robust_p1", "robust_p4", "robust_prior_fijo", "robust_sin_covid", "robust_deflactor_pib", "larga"]
    outs = {}
    for k, nom in enumerate(orden):
        t0 = time.time()
        spec = construir(nom, d)
        c = cfgL if nom == "larga" else cfg
        o = procesar(spec, c["objetivo"], c["M"], c["D0"], c["Dmax"], 10 + k, rapido, reg, tiempos=tiempos)
        outs[nom] = o
        print(f"[{nom}] N={o['diag']['n_aceptadas']} ESS={o['diag']['ess']:.1f} D={o['diag']['D_sorteos_theta']} ({time.time() - t0:.0f}s)", flush=True)
    # ---- salidas
    irf = pd.concat([o["irf"] for o in outs.values()], ignore_index=True)
    irfa = pd.concat([o["irf_acum"] for o in outs.values()], ignore_index=True)
    fev = pd.concat([o["fevd"] for o in outs.values()], ignore_index=True)
    hd = pd.concat([o["hd"] for o in outs.values()], ignore_index=True)
    fm = "%.8g"
    irf.to_csv(salida / "irf.csv", index=False, float_format=fm)
    irfa.to_csv(salida / "irf_acumulada.csv", index=False, float_format=fm)
    fev.to_csv(salida / "fevd.csv", index=False, float_format=fm)
    cols_hd = ["variante", "mercado", "periodo", "factor", "contribucion_pp", "pct_total", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "prob_pos",
               "n_trim", "cobertura", "total_obs_pp", "pct_b68_lo", "pct_b68_hi"]
    hd[cols_hd].to_csv(salida / "hd_periodos.csv", index=False, float_format=fm)
    at = atribucion(outs[OP], OP) + atribucion(outs["larga"], "larga")
    pd.DataFrame(at).to_csv(salida / "atribucion.csv", index=False, float_format=fm)
    hip = hipotesis(outs[OP], reg)
    hip.to_csv(salida / "hipotesis_m2.csv", index=False, float_format=fm)
    _, meta_c = congelar(outs[OP], d, salida, rapido)
    sondeo = sondear(construir("principal", d), 30 if rapido else 300, 300 if rapido else 30000, 99, reg)
    meta_c["sondeo"] = sondeo
    reg.flush()
    ess_tab = pd.DataFrame([dict(variante=n, N_obs=o["diag"]["N_obs"], muestra=f"{o['diag']['muestra_ini']}-{o['diag']['muestra_fin']}", p=o["diag"]["p"],
                                 D_theta=o["diag"]["D_sorteos_theta"], aceptadas=o["diag"]["n_aceptadas"], ESS=o["diag"]["ess"],
                                 frac_theta=o["diag"]["frac_theta_acept"], lam=o["diag"]["lam"]) for n, o in outs.items()])
    desv = [
        "La identificacion principal pre-registrada (7 variables, signos en h=0-1, 4 ceros) es INVIABLE con datos reales (sondeo: 0 aceptadas en 9.000.000 rotaciones); se usa V3 (solo impacto, sin q en demanda ni oferta; Y6) como identificacion operativa para H8-1..H8-4, atribucion y robustez. V1 se estima solo en el impacto (con h=0-1: 0 aceptadas).",
        "Muestra efectiva (7 variables) 2004T2-2026T1 (N=88, HD desde 2004T4): tx_total acaba en 2026T1 y las tasas empiezan en 2004T2; la muestra «2004T1-2026T2» del pre-registro se reduce por disponibilidad conjunta.",
        "Origen de la congelacion: 2026T1 (ultimo trimestre de la muestra comun); h=2..5 desde 2026T1 equivale a h=1..4 desde 2026T2 (2026T2 de p y r ya esta publicado y no se evalua).",
        "Factor 'demanda_vivienda' en atribucion.csv: demanda especifica de vivienda, no incluida en la lista de factores del contrato (declarado en notas).",
        "V2: el HPI de la zona euro (EA20) incluye a Espana (peso no verificado); entra como exogena contemporanea y con un retardo; 'factor_europeo' = su efecto estimado (directo y propagado).",
        "Robustez 'prior fijo': lambda = 0,2 sin optimizar; 'sin 2020-2021': ficticias de impulso 2020T1-2021T4 en lugar de la ficticia COVID; 'deflactor PIB' en p, r y c.",
        "Version larga: ficticia COVID como unica exogena (la EPA no entra); el shock 'residual' queda sin identificar y sin ceros.",
        "IRF para un shock de 1 desviacion tipica (columnas de A0inv = chol(Sigma) Q); irf_acumulada.csv acumula las IRF de las variables en tasa (nivel de p, r, q, c, e, n).",
    ]
    escribir_resumen(salida, outs, hip, fev, hd, ess_tab, desv, meta_c, rapido)
    # ---- resultado.json
    pr = outs[OP]
    est = {r["id"]: dict(contribucion_pp=r.get("contribucion_pp"), prob_posterior=r.get("prob_posterior"), p_unilateral=r.get("p_unilateral"), estado=r.get("estado"))
           for _, r in hip.iterrows()}
    ic95 = {r["id"]: [r.get("ic95_lo"), r.get("ic95_hi")] for _, r in hip.iterrows()}
    ph = {r["id"]: r.get("p_holm") for _, r in hip.iterrows()}
    res_json = dict(
        rama="M2", pregunta="Peso de cada shock (actividad, demografico, demanda de vivienda, oferta, credito y tipos) en la variacion del precio real de compra y del alquiler real por periodo (SVAR con signos y ceros)",
        capa="C3s", datos=f"data/processed/v8/nacional_q_v8.csv; {pr['diag']['muestra_ini']}-{pr['diag']['muestra_fin']}", N=pr["diag"]["N_obs"],
        metodo="BVAR-GLP (p=2, delta 0 en tasas y 1 en i) + restricciones de signo (h=0-1) y 4 ceros (ARW, pesos propios); DH por periodos; Holm en {H8-1..H8-4}",
        estimacion=est, ic95=ic95, p_ajustado=ph, nivel_evidencia="C3s: identificacion por supuestos; sin lenguaje causal incondicional (magnitudes posiblemente atenuadas, Y6)",
        diagnosticos=dict(operativa=OP, sondeo_principal=sondeo, estimaciones={n: o["diag"] for n, o in outs.items()}),
        fuera_muestra=dict(modelo="BVAR-GLP principal (forma reducida), predicciones congeladas", rmse=None, dm_vs_ar4=None,
                           nota="Diferido a make evaluate_v8 (hipotesis.md §10); sha256 en congelacion.json"),
        notas=[AVISO_Y6] + desv, rapido=rapido)
    (salida / "resultado.json").write_text(json.dumps(res_json, indent=1, ensure_ascii=False, default=lambda x: None if x != x else float(x)))
    (salida / "tiempos.json").write_text(json.dumps(tiempos, indent=1))
    return outs


if __name__ == "__main__":
    main()
