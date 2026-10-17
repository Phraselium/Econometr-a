"""V16 fase 6 · Q10: predicción más allá de H5. Q10-1 (Δlog IPV, MIDAS), Q10-2 (Δlog IPC de alquiler, nowcasting), Q10-3 (Δlog compraventas, MIDAS) frente a AR(4).
Ventana expansiva, h = 1 (principal) y 4 (robustez), misma muestra de objetivos para todos los modelos; ECM v1 solo para el IPV. DM-HLN y Clark-West NO APTOS:
solo la reducción puntual del ECM, sin p-valor. Los objetivos se construyen de forma directa (el modelo de origen T solo usa objetivos ya conocidos en T: embargo de h trimestres).
Desviaciones y operacionalización: docs/v16/desviaciones.md, D4. Uso: python3 src/v16/q10_prediccion.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v16 import qc_comun as C  # noqa: E402

warnings.filterwarnings("ignore")
OUT = C.OUTD / "q10"
W0 = 30
TH1, TH2 = np.linspace(-1, 1, 21), np.linspace(-0.3, 0.0, 21)
NL = 6
CFG = {"Q10-1": {"var": ("base_precio", "ipv"), "ini": "2007Q1", "modelo": "MIDAS", "nombre": "Δlog IPV nacional"},
       "Q10-2": {"var": ("base_alquiler", "ipc_alquiler"), "ini": "2002Q1", "modelo": "nowcasting", "nombre": "Δlog IPC de alquiler nacional"},
       "Q10-3": {"var": ("base_precio", "compraventas"), "ini": "2007Q1", "modelo": "MIDAS", "nombre": "Δlog compraventas nacional"}}


def mensual_a_matriz(m: pd.Series, idx: pd.PeriodIndex, nl: int = NL) -> np.ndarray:
    """Para cada trimestre t: nl meses hacia atrás desde el último mes del trimestre (j = 0 es el mes 3)."""
    out = np.full((len(idx), nl), np.nan)
    for i, q in enumerate(idx):
        fin = q.asfreq("M", "end")
        for j in range(nl):
            out[i, j] = m.get(fin - j, np.nan)
    return out


def datos(q: str):
    arch, var = CFG[q]["var"]
    y = C.nat_q(arch, var)
    y = y[y.index >= pd.Period(CFG[q]["ini"], "Q")]
    idx = pd.period_range(y.index[0], pd.Period("2026Q2", "Q"), freq="Q")
    ly = np.log(y.reindex(idx))
    imp = np.log(C.nat_m("demanda_internacional", "bde_importe_vivienda_total_be1911")).diff()
    tedr = C.nat_m("demanda_internacional", "bde_tedr_vivienda_total_be1903").diff()
    vis = np.log(C.nat_q("base_precio", "visados")).reindex(idx)
    X = {"qtr": np.array(idx.quarter), "ly": ly, "imp_m": mensual_a_matriz(imp, idx), "tedr_m": mensual_a_matriz(tedr, idx), "dvis": vis.diff()}
    if q == "Q10-1":
        X["ocup"] = np.log(C.nat_q("base_macro", "ocupados")).reindex(idx)
        X["tipo"] = C.nat_q("base_macro", "tipo_hip_bde").reindex(idx)
        X["vis4"] = vis.shift(4)
        X["pobx"] = np.log(C.nat_q("base_poblacion", "pob_extranj_ine")).reindex(idx)
    return idx, X


def ols(A, y):
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    return b


def ar_lags(dy: np.ndarray, t: int, p: int = 4):
    return [dy[t - l] for l in range(p)]


def prever(modelo: str, X: dict, T: int, h: int):
    """Previsión de log y(T+h) − log y(T) con información hasta el trimestre de índice T. Solo usa objetivos ya observados (t + h <= T)."""
    ly = X["ly"].to_numpy()
    dy = np.diff(ly, prepend=np.nan)
    ts = [t for t in range(5, T - h + 1) if np.isfinite(ly[t + h]) and np.isfinite(ly[t]) and all(np.isfinite(dy[t - l]) for l in range(4))]
    z = np.array([ly[t + h] - ly[t] for t in ts])
    if modelo == "RW_deriva":
        return float(z.mean())
    base = lambda t: [1.0] + ar_lags(dy, t)
    if modelo == "AR4":
        A = np.array([base(t) for t in ts])
        return float(np.array(base(T)) @ ols(A, z))
    if modelo == "AR4_S":   # diagnóstico: AR(4) + dummies del trimestre del objetivo (línea base más exigente con estacionalidad)
        qt = X["qtr"]
        dm = lambda t: [float((qt[t] - 1 + h) % 4 + 1 == k) for k in (2, 3, 4)]
        A = np.array([base(t) + dm(t) for t in ts])
        return float(np.array(base(T) + dm(T)) @ ols(A, z))
    if modelo == "ECM_v1":
        o, tp, v4, px = (X[k].to_numpy() for k in ("ocup", "tipo", "vis4", "pobx"))
        okl = [t for t in range(T + 1) if np.isfinite([ly[t], o[t], tp[t], v4[t]]).all()]
        LR = np.column_stack([np.ones(len(okl)), o[okl], tp[okl], v4[okl]])
        bl = ols(LR, ly[okl])
        ect = np.full(len(ly), np.nan)
        for t in okl:
            ect[t] = ly[t] - np.array([1, o[t], tp[t], v4[t]]) @ bl
        def row(t):
            return [1.0, o[t] - o[t - 1], tp[t] - tp[t - 1], (v4[t] - v4[t - 1]), px[t] - px[t - 1], dy[t], ect[t]]
        tt = [t for t in ts if np.isfinite(row(t)).all()]
        A = np.array([row(t) for t in tt])
        zz = np.array([ly[t + h] - ly[t] for t in tt])
        return float(np.array(row(T)) @ ols(A, zz))
    if modelo == "MIDAS":
        m = X["imp_m"]
        tt = [t for t in ts if np.isfinite(m[t]).all()]
        A0 = np.array([base(t) for t in tt])
        zz = np.array([ly[t + h] - ly[t] for t in tt])
        best, bw = np.inf, None
        j = np.arange(NL)
        for a in TH1:
            for b in TH2:
                w = np.exp(a * j + b * j ** 2)
                w /= w.sum()
                A = np.column_stack([A0, m[tt] @ w])
                bb = ols(A, zz)
                s = ((zz - A @ bb) ** 2).sum()
                if s < best:
                    best, bw, bbest = s, w, bb
        return float(np.append(base(T), m[T] @ bw) @ bbest)
    if modelo == "NOWCAST":
        im = np.nanmean(X["imp_m"][:, :3], axis=1)
        td = np.nanmean(X["tedr_m"][:, :3], axis=1)
        dv = X["dvis"].to_numpy()
        row = lambda t: base(t) + [im[t], td[t], dv[t]]
        tt = [t for t in ts if np.isfinite(row(t)).all()]
        A = np.array([row(t) for t in tt])
        zz = np.array([ly[t + h] - ly[t] for t in tt])
        return float(np.array(row(T)) @ ols(A, zz))
    raise ValueError(modelo)


def evaluar(q: str, h: int):
    idx, X = datos(q)
    ly = X["ly"].to_numpy()
    modelos = ["AR4", "RW_deriva", "AR4_S", CFG[q]["modelo"] if CFG[q]["modelo"] != "nowcasting" else "NOWCAST"] + (["ECM_v1"] if q == "Q10-1" else [])
    filas = []
    for T in range(W0 + 5, len(idx) - h):
        if not np.isfinite(ly[T + h]) or not np.isfinite(ly[T]):
            continue
        real = ly[T + h] - ly[T]
        row = {"origen": str(idx[T]), "objetivo": str(idx[T + h]), "real": real}
        try:
            for m in modelos:
                row[m] = prever(m, X, T, h)
        except Exception as e:  # modelo no estimable en este origen
            continue
        if all(np.isfinite([row[m] for m in modelos])):
            filas.append(row)
    return pd.DataFrame(filas), modelos


def metricas(d: pd.DataFrame, modelos, excluir_2020: bool):
    x = d.copy()
    if excluir_2020:
        o = pd.PeriodIndex(x.objetivo, freq="Q")
        x = x[~((o >= pd.Period("2020Q1", "Q")) & (o <= pd.Period("2021Q2", "Q")))]
    mse = {m: float(((x.real - x[m]) ** 2).mean()) for m in modelos}
    return {"n": int(len(x)), "rmse": {m: float(np.sqrt(v)) for m, v in mse.items()},
            "reduccion_ecm_vs_AR4": {m: float(1 - mse[m] / mse["AR4"]) for m in modelos if m != "AR4"},
            "reduccion_ecm_vs_ECM_v1": ({m: float(1 - mse[m] / mse["ECM_v1"]) for m in modelos if m != "ECM_v1"} if "ECM_v1" in modelos else None),
            "muestra": f"{x.objetivo.iloc[0]}-{x.objetivo.iloc[-1]}"}


def conforme(d: pd.DataFrame, m: str, nivel: float = 0.9, minimo: int = 12):
    e = (d.real - d[m]).abs().to_numpy()
    cub, anch = [], []
    for i in range(minimo, len(e)):
        r = np.quantile(e[:i], nivel)
        cub.append(e[i] <= r)
        anch.append(2 * r)
    return {"cobertura_empirica_90": float(np.mean(cub)) if cub else None, "n": len(cub), "ancho_medio": float(np.mean(anch)) if anch else None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reg, est, py, detalle = [], {}, [], {}
    for q in CFG:
        est[q] = {}
        for h in (1, 4):
            d, modelos = evaluar(q, h)
            d.to_csv(OUT / f"previsiones_{q.lower()}_h{h}.csv", index=False)
            for ex in (False, True):
                mt = metricas(d, modelos, ex)
                tag = f"h{h}{'_sin2020' if ex else ''}"
                est[q][tag] = mt
                for m, red in mt["reduccion_ecm_vs_AR4"].items():
                    principal = (h == 1 and not ex and m in ("MIDAS", "NOWCAST"))
                    reg.append({"id": f"{q}-P" if principal else f"{q}-mv-{m}-{tag}", "pregunta": q, "rol": "principal" if principal else "multiverso",
                                "especificacion": f"{m} frente a AR(4), {CFG[q]['nombre']}, h={h}{', sin 2020T1-2021T2' if ex else ''}, ventana expansiva inicial {W0}",
                                "muestra": mt["muestra"], "n": mt["n"], "estimacion": red, "unidad": "reducción del ECM respecto al AR(4)",
                                "inferencia": "ninguna (dm_hln NO APTO)", "nota": f"RMSE {mt['rmse'][m]:.5f} vs AR(4) {mt['rmse']['AR4']:.5f}"})
        pm = est[q]["h1"]
        m_pr = "MIDAS" if "MIDAS" in pm["reduccion_ecm_vs_AR4"] else "NOWCAST"
        d1, mods = evaluar(q, 1)
        est[q]["conforme_h1"] = {m: conforme(d1, m) for m in (m_pr, "AR4")}
        est[q]["modelo_principal"] = m_pr
        est[q]["reduccion_principal"] = pm["reduccion_ecm_vs_AR4"][m_pr]
        est[q]["relevancia_minima_10pct"] = bool(est[q]["reduccion_principal"] >= 0.10)
        est[q]["ic95"] = None
        est[q]["p"] = None
        py.append({"id": q, "p": None, "motivo": "dm_hln y Clark-West NO APTOS: solo reducción puntual del ECM"})
    Q = C.Q
    Q.registro(reg, OUT / "registro.csv")
    diag = {q: [C.diag("calibración DM-HLN / Clark-West", "NO APTO", "tamaño HLN 0,002; Clark-West 0,033: sin p-valor"),
                C.diag("MCS / GW", "no ejecutado", "no validados en veredictos.csv"),
                C.diag("misma muestra de objetivos", "superada", f"todos los modelos sobre los mismos {est[q]['h1']['n']} objetivos ({est[q]['h1']['muestra']})"),
                C.diag("ECM v1", "reportado" if q == "Q10-1" else "no existe", "reproducción en entrenamiento sin ln_costes (D4)" if q == "Q10-1" else "no hay ECM v1 para esta variable"),
                C.diag("cobertura conforme h=1 (90 %)", "reportada", est[q]["conforme_h1"]),
                C.diag("embargo/bloques", "no interviene", "modelos fijados de antemano, objetivos directos con información ≤ origen"),
                C.diag("límite de información", "declarado", "indicadores mensuales en su última edición, no en tiempo real (adenda, punto 8)")] for q in CFG}
    f = C.f
    for q in CFG:
        mt = est[q]["h1"]
        r = C.resultado(q.lower(), f"{q}: {CFG[q]['nombre']}, h = 1, {est[q]['modelo_principal']} frente a AR(4)", "data/processed/v16/entrenamiento: base_precio, base_alquiler, base_macro, base_poblacion, demanda_internacional",
                        mt["n"], "ventana expansiva; reducción puntual del ECM; sin DM/CW (NO APTOS)", est[q], diag[q],
                        ["C4; predicción ≠ causalidad.", "El nowcasting puede parecer mejor de lo que sería en directo (última edición de los indicadores).", "Solo «predice mejor» si supera a la línea base más exigente: ver razones frente a RW con deriva y ECM v1."],
                        [p for p in py if p["id"] == q])
        r["fuera_muestra"] = {"modelo": est[q]["modelo_principal"], "rmse": mt["rmse"], "dm_vs_ar4": None}
        Q.jdump(r, OUT / f"resultado_{q.lower()}.json")
    r = C.resultado("q10", "Q10: predicción nacional (IPV, IPC de alquiler, compraventas) h = 1 frente a AR(4) y ECM v1; reducción puntual del ECM",
                    "data/processed/v16/entrenamiento: base_precio, base_alquiler, base_macro, base_poblacion, demanda_internacional", {q: est[q]["h1"]["n"] for q in CFG},
                    "ventana expansiva (30 trimestres iniciales); MIDAS exp-Almon / puente; DM-HLN y Clark-West NO APTOS: solo razones de ECM", est, diag,
                    ["C4; predicción, sin lenguaje causal.", "Límite declarado: indicadores mensuales en su última edición.", "ECM v1 solo existe para el IPV."], py)
    r["fuera_muestra"] = {"modelo": {q: est[q]["modelo_principal"] for q in CFG}, "rmse": {q: est[q]["h1"]["rmse"] for q in CFG}, "dm_vs_ar4": None}
    Q.jdump(r, OUT / "resultado.json")
    Q.jdump({"estimacion": est, "diagnosticos": diag}, OUT / "q10_detalle.json")
    hs = []
    for i, q in enumerate(CFG, 1):
        mt, pr = est[q]["h1"], est[q]["modelo_principal"]
        vs = [v for k, v in est[q].items() if k.startswith("h") and isinstance(v, dict) and "reduccion_ecm_vs_AR4" in v and pr in v["reduccion_ecm_vs_AR4"]]
        reds = [v["reduccion_ecm_vs_AR4"][pr] for v in vs]
        hs.append(C.hecho("red", q.split("-")[0] + f"-{i}", f"{q}: reducción puntual del ECM de {pr} respecto al AR(4) en {CFG[q]['nombre']}, h = 1", est[q]["reduccion_principal"], min(reds), max(reds),
                          "reducción relativa del ECM", mt["muestra"], f"nacional, {mt['n']} objetivos", "INE; BdE; MIVAU", q.lower()))
    Q.jdump(hs, OUT / "hechos.json")
    md = "# Q10 · Predicción nacional frente a AR(4) y ECM v1 (C4, pendiente de evaluación sellada)\n\n"
    md += ("**Capa.** C4. Predicción, no causalidad. DM-HLN y Clark-West son NO APTOS (tamaño 0,002 y 0,033): se publica **solo la reducción puntual del ECM**, sin p-valor ni IC; GW y MCS no están validados y no se usan. "
           "Ventana expansiva (30 trimestres iniciales), misma muestra de objetivos para todos los modelos; objetivos directos con información hasta el origen. Indicadores mensuales en su última edición (límite declarado): "
           "el nowcasting puede parecer mejor de lo que sería en directo.\n\n")
    for q in CFG:
        e = est[q]
        mt = e["h1"]
        md += f"## {q} · {CFG[q]['nombre']} (h = 1)\n<a id=\"{q.lower()}\"></a>Modelo {e['modelo_principal']} frente a AR(4): reducción puntual del ECM **{f(100 * e['reduccion_principal'], 1)} %** ({mt['muestra']}, n = {mt['n']}); relevancia mínima del 10 %: {'alcanzada' if e['relevancia_minima_10pct'] else 'no alcanzada'} (descriptivo).\n"
        md += "RMSE: " + "; ".join(f"{m} {f(v, 5)}" for m, v in mt["rmse"].items()) + ".\n"
        md += "Reducción frente al AR(4): " + "; ".join(f"{m} {f(100 * v, 1)} %" for m, v in mt["reduccion_ecm_vs_AR4"].items()) + ".\n"
        if mt["reduccion_ecm_vs_ECM_v1"]:
            md += "Misma muestra frente al ECM v1: " + "; ".join(f"{m} {f(100 * v, 1)} %" for m, v in mt["reduccion_ecm_vs_ECM_v1"].items()) + ".\n"
        else:
            md += "No existe ECM v1 para esta variable.\n"
        for tag in ("h1_sin2020", "h4", "h4_sin2020"):
            x = e[tag]
            md += f"- {tag}: n = {x['n']}; " + "; ".join(f"{m} {f(100 * v, 1)} %" for m, v in x["reduccion_ecm_vs_AR4"].items()) + "\n"
        c = e["conforme_h1"][e["modelo_principal"]]
        md += f"Intervalos conformes 90 % (h = 1): cobertura empírica {f(c['cobertura_empirica_90'], 2)} (n = {c['n']}).\n\n"
    md += "## Regla de hallazgo\n(a) sin p-valor (NO APTO): no evaluable; (b) sin magnitud inferencial: la reducción puntual se compara con la relevancia mínima del 10 %, solo descriptiva; (c) sellada: pendiente (H5 de V15 sigue siendo la confirmatoria). Resultado: C4 descriptivo.\n"
    (OUT / "informe.md").write_text(md, encoding="utf-8")
    return est


if __name__ == "__main__":
    e = main()
    for q in e:
        print(q, e[q]["h1"]["n"], e[q]["h1"]["reduccion_ecm_vs_AR4"], e[q]["h4"]["reduccion_ecm_vs_AR4"])
