#!/usr/bin/env python3
"""V8-F4 M3: coeficientes que cambian por periodo (P1-P5 pre-registrados como fechas conocidas).

Principal (Y6): proyecciones locales (LP-OLS) dependientes del periodo, interaccion impulso x ficticia de periodo, EWC fixed-b (C4).
Contraste: VAR bayesiano por regimenes (tvp.var_regimenes), declarado NO APTO por F3 (cobertura 0,08 en el tramo de 9 trimestres);
solo descriptivo. Impulso = variable observada (no shock identificado): asociacion condicional, sin lectura causal.
Uso: python3 src/v8/m3_periodos_var.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

import argparse  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v8"))
from econ_utils import Registry  # noqa: E402
from herramientas import bvar, tvp  # noqa: E402
from herramientas.lp import _lead  # noqa: E402

SEED = 20261010
DATOS = RAIZ / "data" / "processed" / "v8" / "nacional_q_v8.csv"
PERIODOS = {"P1": ("1995Q1", "2007Q4"), "P2": ("2008Q3", "2013Q4"), "P3": ("2014Q1", "2019Q4"),
            "P4": ("2020Q2", "2022Q2"), "P5": ("2022Q3", "2026Q2")}
PERS = list(PERIODOS)
HS_AGG = (4, 8)
H_MAX = 8
REZ = 2
# especificaciones: nombre -> (mercado, [vars], medida de precio)
SPECS = {
    "compra_larga": ("compra", ["p", "i", "y", "n"], "valor tasado real (p_tasado / IPC general), PIB en volumen en lugar de EPA"),
    "compra_epa": ("compra", ["p", "i", "e", "n"], "valor tasado real (p_tasado / IPC general)"),
    "alquiler_epa": ("alquiler", ["r", "i", "e", "n"], "IPC alquiler real (ipc_alquiler / IPC general)"),
    "alquiler_pib": ("alquiler", ["r", "i", "y", "n"], "IPC alquiler real (ipc_alquiler / IPC general), PIB en volumen en lugar de EPA"),
}
NIVEL = ("i",)
AVISO = ("C4: multiplicador condicional (impulso = variable observada, no shock identificado); asociacion, sin lectura causal. LP-OLS con T~90-110: cobertura "
         "F3 0,78-0,84 incluso con EWC, bandas aproximadas. P4 (9 trimestres) impreciso. Rezagos y ficticias comunes a todos los periodos.")


def qidx(s):
    a, q = s.split("Q")
    return int(a) * 4 + int(q) - 1


def cargar():
    d = pd.read_csv(DATOS).set_index("trimestre")
    ld = np.log(d["ipc_general"])
    dl = lambda s: 100.0 * s.diff()  # noqa: E731
    S = pd.DataFrame(index=d.index)
    S["p"] = dl(np.log(d["p_tasado"]) - ld)
    S["r"] = dl(np.log(d["ipc_alquiler"]) - ld)
    S["i"] = d["tipo_hip_bce"].where(d["tipo_hip_bce"].notna(), d["tipo_hip_bde"])
    S["e"] = dl(np.log(d["ocupados"]))
    S["n"] = dl(np.log(d["pob_total"]))
    S["y"] = dl(np.log(d["pib_vol_idx"]))
    S["covid"] = d["covid"].astype(float)
    S["epa2021"] = d["epa2021"].astype(float)
    return S


def dummies_periodo(idx):
    D = pd.DataFrame(0.0, index=idx, columns=PERS)
    for k, (a, b) in PERIODOS.items():
        D[k] = [float(qidx(a) <= qidx(t) <= qidx(b)) for t in idx]
    return D


def lp_periodo(S, vars_, origen, destino, h, agg=False, ewc_frac=0.4):
    """LP con interaccion impulso x periodo. h entero, o agg=True: media de y_{t+4..t+8}. Devuelve dict con beta/V por periodo."""
    idx = S.index
    D = dummies_periodo(idx)
    acum = destino not in NIVEL
    y = S[destino]
    if agg:
        dep = pd.concat([_lead(y, k, acum) for k in range(HS_AGG[0], HS_AGG[1] + 1)], axis=1).mean(axis=1, skipna=False)
    else:
        dep = _lead(y, h, acum)
    cols = {"dep": dep}
    for k in PERS:
        cols[f"x_{k}"] = S[origen] * D[k]
    for k in PERS:
        cols[f"d_{k}"] = D[k]
    for v in vars_:
        for l in range(1, REZ + 1):
            cols[f"{v}_l{l}"] = S[v].shift(l)
    cols["covid"] = S["covid"]
    if "e" in vars_:
        cols["epa2021"] = S["epa2021"]
    M = pd.DataFrame(cols, index=idx)
    M = M[D.sum(axis=1) > 0].dropna()
    X = M.drop(columns="dep")
    keep = [c for c in X.columns if X[c].abs().sum() > 0]
    X = X[keep]
    Xv, Yv = X.values, M["dep"].values
    n, k = Xv.shape
    XtXi = np.linalg.pinv(Xv.T @ Xv)
    b = XtXi @ Xv.T @ Yv
    u = Yv - Xv @ b
    G = Xv * u[:, None]
    q = max(int(np.floor(ewc_frac * n ** (2 / 3))), 2)
    t = (np.arange(1, n + 1) - 0.5) / n
    Lam = np.array([np.sqrt(2) * np.cos(np.pi * j * t) @ G / np.sqrt(n) for j in range(1, q + 1)])
    V = n * XtXi @ (Lam.T @ Lam / q) @ XtXi
    pos = {c: i for i, c in enumerate(keep)}
    ks = [f"x_{p_}" for p_ in PERS if f"x_{p_}" in pos]
    ii = [pos[c] for c in ks]
    pers = [c[2:] for c in ks]
    ss = np.sum(u ** 2)
    sst = np.sum((Yv - Yv.mean()) ** 2)
    return {"per": pers, "beta": b[ii], "V": V[np.ix_(ii, ii)], "q": q, "n": n, "k": k,
            "n_per": {p_: int(M[f"d_{p_}"].sum()) for p_ in pers}, "ini": M.index[0], "fin": M.index[-1],
            "r2": float(1 - ss / sst), "r2_adj": float(1 - (ss / (n - k)) / (sst / (n - 1)))}


def bandas_t(beta, se, q):
    out = {}
    for nv, lvl in (("b68", 0.68), ("b90", 0.90)):
        c = stats.t.ppf(0.5 + lvl / 2, q)
        out[nv + "_lo"], out[nv + "_hi"] = beta - c * se, beta + c * se
    return out


def bh(p, q=0.10):
    p = np.asarray(p, float)
    ok = ~np.isnan(p)
    adj = np.full_like(p, np.nan)
    pv = p[ok]
    m = len(pv)
    o = np.argsort(pv)
    a = pv[o] * m / (np.arange(m) + 1)
    a = np.minimum.accumulate(a[::-1])[::-1]
    r = np.empty(m)
    r[o] = np.minimum(a, 1.0)
    adj[ok] = r
    return adj


def pares(vars_):
    return [(o, d) for o in vars_ for d in vars_ if o != d]


def var_contraste(S, vars_, ndraw, rng):
    """VAR por regimenes (p=2) con prior comun; coeficientes del retardo 1 origen->destino por periodo. NO APTO (F3): descriptivo."""
    cols = vars_ + ["covid"]
    Z = S[vars_].dropna()
    Y = Z.values
    p = 2
    fechas = list(Z.index[p:])
    tramos, nombres = [], []
    for k, (a, b) in PERIODOS.items():
        ii = [j for j, t in enumerate(fechas) if qidx(a) <= qidx(t) <= qidx(b)]
        if len(ii) >= 3:
            tramos.append((ii[0], ii[-1] + 1))
            nombres.append(k)
    delta = np.array([1.0 if v in NIVEL else 0.0 for v in vars_])
    res = tvp.var_regimenes(Y, p, tramos=tramos, delta=delta)
    n = len(vars_)
    draws = []
    for reg in res["regimenes"]:
        B, _ = bvar.muestrear(reg, ndraw, rng)
        draws.append(B)
    rows, difs = [], []
    for o, d in pares(vars_):
        io, idd = vars_.index(o), vars_.index(d)
        pos = io  # retardo 1
        for kk, nm in enumerate(nombres):
            x = draws[kk][:, pos, idd]
            qs = np.quantile(x, [0.05, 0.16, 0.5, 0.84, 0.95])
            rows.append({"variable_origen": o, "variable_destino": d, "periodo": nm, "mediana": qs[2], "b68_lo": qs[1], "b68_hi": qs[3],
                         "b90_lo": qs[0], "b90_hi": qs[4], "n_trim": tramos[kk][1] - tramos[kk][0]})
        for a_, b_ in itertools.combinations(range(len(nombres)), 2):
            x = draws[b_][:, pos, idd] - draws[a_][:, pos, idd]
            difs.append({"variable_origen": o, "variable_destino": d, "periodo_a": nombres[a_], "periodo_b": nombres[b_],
                         "dif_mediana": float(np.median(x)), "prob_pos": float(np.mean(x > 0))})
    return pd.DataFrame(rows), pd.DataFrame(difs), res["lam"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=str(RAIZ / "output" / "v8" / "M3"))
    a = ap.parse_args()
    t0 = time.time()
    out = Path(a.salida)
    out.mkdir(parents=True, exist_ok=True)
    S = cargar()
    reg = Registry(out / "registro.csv")
    specs = {k: v for k, v in SPECS.items() if not a.rapido or k == "compra_larga"}
    hs = [4, 8] if a.rapido else list(range(0, H_MAX + 1))
    ndraw = 300 if a.rapido else 3000

    cp, cph, coefs, difs, cons = [], [], [], [], []
    for sn, (mercado, vars_, medida) in specs.items():
        Ssub = S[[*vars_, "covid", "epa2021"]].copy()
        Ssub = Ssub.loc[Ssub[vars_].dropna().index[0]:]
        for o, d in pares(vars_):
            # perfiles por horizonte
            for h in hs:
                r = lp_periodo(Ssub, vars_, o, d, h)
                se = np.sqrt(np.diag(r["V"]))
                for j, pr in enumerate(r["per"]):
                    bd = bandas_t(r["beta"][j], se[j], r["q"])
                    cph.append({"especificacion": sn, "mercado": mercado, "variable_origen": o, "variable_destino": d, "periodo": pr, "h": h,
                                "mediana": r["beta"][j], **bd, "n": r["n"]})
                    pv = 2 * stats.t.sf(abs(r["beta"][j] / se[j]), r["q"])
                    reg.log("M3", f"{sn}|{o}>{d}|{pr}|h{h}", f"{d}(t+{h}) ~ {o}_t x {pr} + rezagos{REZ}", r["ini"], r["fin"], r["n"], r["r2_adj"],
                            np.nan, np.nan, coef_interes=r["beta"][j], p_interes=pv, notas="LP periodo EWC C4")
            # resumen h=4-8
            r = lp_periodo(Ssub, vars_, o, d, None, agg=True)
            se = np.sqrt(np.diag(r["V"]))
            for j, pr in enumerate(r["per"]):
                bd = bandas_t(r["beta"][j], se[j], r["q"])
                t_ = r["beta"][j] / se[j]
                p_ = 2 * stats.t.sf(abs(t_), r["q"])
                cp.append({"especificacion": sn, "mercado": mercado, "variable_origen": o, "variable_destino": d, "periodo": pr,
                           "mediana": r["beta"][j], **bd, "n_trim_periodo": r["n_per"][pr]})
                c95 = stats.t.ppf(0.975, r["q"])
                coefs.append({"modelo_id": f"M3_lp_{sn}_{o}>{d}_{pr}_h4-8", "modulo": "M3", "familia_modelo": "lp_periodo", "mercado": mercado,
                              "ambito": "nacional", "periodo": pr, "dependiente": d,
                              "transformacion": "media y_{t+4..t+8} (acumulada si tasa) sobre impulso_t", "medida_precio": medida,
                              "variable": f"{o}_t x {pr}", "beta": r["beta"][j], "ee": se[j], "tipo_ee": f"EWC fixed-b t({r['q']})", "t": t_,
                              "p": p_, "ic95_lo": r["beta"][j] - c95 * se[j], "ic95_hi": r["beta"][j] + c95 * se[j], "n": r["n"],
                              "r2": r["r2"], "r2_adj": r["r2_adj"], "capa": "C4", "script": "src/v8/m3_periodos_var.py"})
                reg.log("M3", f"{sn}|{o}>{d}|{pr}|h4-8", f"mean y(t+4..8) ~ {o}_t x {pr} + rezagos{REZ}", r["ini"], r["fin"], r["n"], r["r2_adj"],
                        np.nan, np.nan, coef_interes=r["beta"][j], p_interes=p_, notas="LP periodo EWC C4 agregado h4-8")
            for ja, jb in itertools.combinations(range(len(r["per"])), 2):
                dif = r["beta"][jb] - r["beta"][ja]
                v = r["V"][ja, ja] + r["V"][jb, jb] - 2 * r["V"][ja, jb]
                sed = float(np.sqrt(max(v, 1e-300)))
                t_ = dif / sed
                difs.append({"especificacion": sn, "mercado": mercado, "variable_origen": o, "variable_destino": d, "periodo_a": r["per"][ja],
                             "periodo_b": r["per"][jb], "dif_mediana": dif, "ee": sed, "t": t_, "p": 2 * stats.t.sf(abs(t_), r["q"]),
                             **bandas_t(dif, sed, r["q"]), "implica_P4": "P4" in (r["per"][ja], r["per"][jb])})
                reg.log("M3", f"{sn}|{o}>{d}|{r['per'][jb]}-{r['per'][ja]}|h4-8", "diferencia de coeficientes de periodo", r["ini"], r["fin"],
                        r["n"], np.nan, np.nan, np.nan, coef_interes=dif, p_interes=difs[-1]["p"], notas="diferencia entre periodos")
        # contraste VAR por regimenes
        rng = np.random.default_rng([SEED, len(cons)])
        cv, dv, lam = var_contraste(Ssub, vars_, ndraw, rng)
        cv.insert(0, "mercado", mercado)
        cv.insert(0, "especificacion", sn)
        dv.insert(0, "mercado", mercado)
        dv.insert(0, "especificacion", sn)
        cons.append((cv, dv))
        reg.log("M3", f"{sn}|var_regimenes", f"VAR(2) por regimenes {vars_}", Ssub.index[0], Ssub.index[-1], len(Ssub), np.nan, np.nan, np.nan,
                notas=f"contraste NO APTO F3; lambda={lam:.3f}")

    cp = pd.DataFrame(cp)
    cph = pd.DataFrame(cph)
    co = pd.DataFrame(coefs)
    di = pd.DataFrame(difs)
    co["p_ajustado"] = bh(co["p"].values)
    co["metodo_ajuste"] = "BH"
    di["p_ajustado"] = bh(di["p"].values)
    di["metodo_ajuste"] = "BH"
    di["sig_bh10"] = di["p_ajustado"] < 0.10
    co["sig_bh10"] = co["p_ajustado"] < 0.10
    cvs = pd.concat([c for c, _ in cons], ignore_index=True)
    dvs = pd.concat([d for _, d in cons], ignore_index=True)

    from itertools import product  # noqa: F401
    cols_contrato = ["modelo_id", "modulo", "familia_modelo", "mercado", "ambito", "periodo", "dependiente", "transformacion", "medida_precio",
                     "variable", "beta", "ee", "tipo_ee", "t", "p", "p_ajustado", "metodo_ajuste", "ic95_lo", "ic95_hi", "beta_std", "elasticidad",
                     "n", "r2", "r2_adj", "aic", "bic", "vel_ajuste", "semivida", "coint_p", "bg_p", "bp_p", "jb_p", "reset_p", "cusum_estable",
                     "vif_max", "f1_etapa", "ar_lo", "ar_hi", "capa", "n_multiverso", "pct_mismo_signo", "pct_sig_bh", "cumple_regla_m0",
                     "cumple_multiverso", "destacado", "motivo_destacado", "script"]
    # coeficientes del contraste VAR (retardo 1) en el mismo contrato
    filas_v = []
    for _, r in cvs.iterrows():
        filas_v.append({"modelo_id": f"M3_var_{r['especificacion']}_{r['variable_origen']}>{r['variable_destino']}_{r['periodo']}_lag1", "modulo": "M3",
                        "familia_modelo": "var_regimenes", "mercado": r["mercado"], "ambito": "nacional", "periodo": r["periodo"],
                        "dependiente": r["variable_destino"], "transformacion": "coef. del retardo 1 (mediana posterior)",
                        "variable": f"{r['variable_origen']}_t-1", "beta": r["mediana"], "tipo_ee": "posterior (68/90 % en coef_periodo_var.csv)",
                        "ic95_lo": np.nan, "ic95_hi": np.nan, "n": r["n_trim"], "capa": "C4", "script": "src/v8/m3_periodos_var.py"})
    allco = pd.concat([co, pd.DataFrame(filas_v)], ignore_index=True)
    for c in cols_contrato:
        if c not in allco:
            allco[c] = np.nan
    allco[cols_contrato].to_csv(out / "coeficientes.csv", index=False)
    cp.to_csv(out / "coef_periodo.csv", index=False,
              columns=["variable_origen", "variable_destino", "periodo", "mediana", "b68_lo", "b68_hi", "b90_lo", "b90_hi", "especificacion", "mercado",
                       "n_trim_periodo"])
    cph.to_csv(out / "coef_periodo_h.csv", index=False)
    di.to_csv(out / "diferencias_periodos.csv", index=False)
    cvs.to_csv(out / "coef_periodo_var.csv", index=False)
    dvs.to_csv(out / "diferencias_var.csv", index=False)
    reg.flush()

    # resumen numerico
    nt = int(len(di))
    nsig = int(di["sig_bh10"].sum())
    nsig_sinP4 = int(di.loc[~di["implica_P4"], "sig_bh10"].sum())
    top = di[di["sig_bh10"]].sort_values("p_ajustado").head(12)
    ancho = cp.assign(a=cp["b90_hi"] - cp["b90_lo"]).groupby(["especificacion", "periodo"])["a"].median().unstack()
    res = {"rama": "M3", "pregunta": "Cambian por periodo (P1-P5) las asociaciones dinamicas entre precio/alquiler, tipo hipotecario, empleo/PIB y poblacion?",
           "capa": "C4", "datos": "data/processed/v8/nacional_q_v8.csv (tasas trimestrales log x100 reales; tipo en nivel); " +
           "; ".join(f"{k}: {v[1]}" for k, v in specs.items()),
           "N": {k: int(cp.loc[cp['especificacion'] == k].shape[0]) for k in specs},
           "metodo": "LP-OLS con interaccion impulso x periodo (principal, Y6), EWC fixed-b; contraste VAR(2) bayesiano por regimenes (no apto F3)",
           "estimacion": {"n_diferencias": nt, "n_sig_bh10": nsig, "n_sig_bh10_sin_P4": nsig_sinP4,
                          "ancho_b90_mediano_por_periodo": {k: {kk: round(float(vv), 3) for kk, vv in v.items()} for k, v in ancho.to_dict("index").items()}},
           "ic95": "ver coeficientes.csv (ic95_lo, ic95_hi)", "p_ajustado": "BH q=0,10 sobre coeficientes y sobre diferencias (diferencias_periodos.csv)",
           "nivel_evidencia": "EXPLORATORIO (C4)",
           "diagnosticos": {"ewc_q": "q = floor(0,4 n^(2/3)), t(q)", "cobertura_F3": "0,78-0,84 (LP-OLS con T 90-110)",
                            "var_regimenes": "no apto (cobertura 0,08 tramo 9 trim.); sin ficticias exogenas", "P4": "impreciso (9 trimestres)",
                            "rapido": a.rapido},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None,
                             "nota": "No aplica: M3 estima coeficientes por periodo, no predice; la comparacion con AR(4) y ECM v1 corresponde a M2/M9."},
           "notas": [AVISO, "Principal = LP periodo (Y6); contraste = VAR por regimenes. Resumen por periodo = media de h=4-8; perfiles en coef_periodo_h.csv.",
                     "Huecos 2008T1-T2 y 2020T1 fuera; la dependiente puede caer en el periodo siguiente.",
                     "Compra larga usa PIB en volumen (1995T2+); compra_epa y alquiler comparten muestra desde 2002T2.",
                     f"tiempo_s={time.time() - t0:.0f}"]}
    (out / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False, default=float))

    def f(x):
        return f"{x:.2f}"
    L = ["# M3: coeficientes por periodo (C4, exploratorio)", "",
         f"**Principal (Y6):** LP-OLS dependiente del periodo (impulso x ficticia P1-P5), EWC fixed-b, resumen = media de h=4-8. **Contraste:** VAR(2) bayesiano "
         f"por regímenes, «no apto» según F3 (cobertura 0,08 en 9 trimestres): solo descriptivo (`coef_periodo_var.csv`). {AVISO}", "",
         f"- Especificaciones: {', '.join(specs)}. Pares origen→destino: 12 por especificación; 10 contrastes de periodos por par.",
         f"- Diferencias entre periodos con BH q=0,10: **{nsig} de {nt}** ({nsig_sinP4} sin implicar a P4). Un no rechazo no prueba igualdad (potencia baja).",
         "- Ancho mediano de la banda del 90 % por periodo (coeficientes h=4-8):", "",
         "| espec. | " + " | ".join(ancho.columns) + " |", "|---|" + "---|" * len(ancho.columns)]
    for k, r in ancho.iterrows():
        L.append(f"| {k} | " + " | ".join(f(v) for v in r.values) + " |")
    L += ["", "P4 (9 trimestres) se declara impreciso por diseño. Aviso: la banda de P4 NO es siempre la más ancha (p. ej. compra_larga); con 9 observaciones, "
          "regresores comunes y EWC con pocos grados de libertad, las bandas de P4 pueden ser artificialmente estrechas (sobreajuste), no más informativas. "
          "Las diferencias que implican a P4 no deben leerse como evidencia sólida. Diferencias significativas tras BH (hasta 12):", ""]
    if len(top):
        L += ["| espec. | origen→destino | periodos | dif. | p BH |", "|---|---|---|---|---|"]
        for _, r in top.iterrows():
            L.append(f"| {r['especificacion']} | {r['variable_origen']}→{r['variable_destino']} | {r['periodo_a']} vs {r['periodo_b']} | {f(r['dif_mediana'])} | {r['p_ajustado']:.3f} |")
    else:
        L.append("Ninguna.")
    L += ["", "Todas las filas (significativas o no) están en `diferencias_periodos.csv`, `coef_periodo.csv` y `coeficientes.csv`. "
          "Los coeficientes del VAR son del retardo 1 (unidades distintas del multiplicador LP). Sin lectura causal."]
    (out / "resumen.md").write_text("\n".join(L) + "\n")
    print(f"M3 listo en {time.time() - t0:.0f}s; dif sig BH: {nsig}/{nt}")


if __name__ == "__main__":
    main()
