"""V9 F3 · D2 pisos turísticos × shock COVID en Cataluña (pre-registro: docs/v9/hipotesis.md, D2). SEED = 20261010.

y_it = a_i + g_t + Σ_{k∈2014..2018} δ_k (dosis_i·1[t=k]) + β_covid (dosis_i·1[t∈2020-21]) + β_reap (dosis_i·1[t≥2022])
       + controles de política (Ley 11/2020 × 2021; zona tensionada × 2024-2025) + ε,  base 2019.
Dosis = plazas en HUT por 100 habitantes en 2019 (IDESCAT; padrón 2019), estandarizada. Incasòl anual 2014-2025.
Salidas: output/v9/d2/{tabla_d2.csv, estudio_eventos.csv, dosis_respuesta.csv, pruebas.csv, resultado.json, registry.csv, fig_*.png}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import herramientas as H  # noqa: E402
import paneles as P  # noqa: E402
from econ_utils import Registry  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d2"
REG = Registry(OUT / "registry.csv")
B = 999
NPERM = 500
RES = {"renta_media": "log renta media de contratos nuevos", "contratos": "log contratos nuevos"}


def panel(a: pd.DataFrame, var: str, a0: int, a1: int, dosis: pd.Series) -> pd.DataFrame:
    w = a[(a.anio >= a0) & (a.anio <= a1)].pivot_table(index="cod", columns="anio", values=var)
    w = w[(w > 0).all(1)].dropna()
    w = w[w.index.isin(dosis.dropna().index)]
    return np.log(w)


def disenar(W: pd.DataFrame, x: np.ndarray, ley: set, zt: pd.Series, base: int = 2019, pre=(2014, 2018),
            covid=(2020, 2021), reap=(2022, 2025), politicas: bool = True, tendencia: bool = False):
    anios = np.array(W.columns)
    Xs, nombres = [], []
    if tendencia:   # addendum A1.3: tendencia lineal específica por dosis
        Xs.append(np.outer(x, (anios - base).astype(float)))
        nombres.append("tend_dosis")
    for k in range(pre[0], pre[1] + 1):
        if k in anios and k != base:
            Xs.append(np.outer(x, (anios == k).astype(float)))
            nombres.append(f"lead_{k}")
    Xs.append(np.outer(x, ((anios >= covid[0]) & (anios <= covid[1])).astype(float)))
    nombres.append("covid")
    if reap is not None:
        Xs.append(np.outer(x, ((anios >= reap[0]) & (anios <= reap[1])).astype(float)))
        nombres.append("reapertura")
    if politicas:
        l11 = np.array([c in ley for c in W.index], float)
        if (anios == 2021).any():
            Xs.append(np.outer(l11, (anios == 2021).astype(float)))
            nombres.append("ctrl_ley11_2021")
        ztm = np.array([c in zt.index for c in W.index], float)
        if (anios >= 2024).any():
            Xs.append(np.outer(ztm, (anios >= 2024).astype(float)))
            nombres.append("ctrl_zt_2024_25")
    return Xs, nombres


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    a = P.incasol("A")
    h = P.hut_cat()
    h19 = h[h.anio == 2019].set_index("cod")
    dosis = 100 * h19.hut_plazas / h19.poblacion
    viv = pd.read_csv(P.RAW / "v3/ine_v3_censo2021_municipio_viviendas.csv", dtype={"codigo": str})
    viv = viv[(viv.serie == "V_TOTAL") & (viv.nivel == "municipio")].set_index("codigo").valor
    dosis_viv = 100 * h19.hut / viv.reindex(h19.index)
    tr = P.tratamientos_cat()
    ley = set(tr[tr.ley11].cod)
    zt = tr.dropna(subset=["zt_t0"]).set_index("cod").zt_t0
    tabla, pruebas, es_rows, dr_rows = [], [], [], []

    def estima(W, xraw, etiqueta, var, conf, hip_prefijo, **kw):
        x = (xraw - xraw.mean()) / xraw.std()
        Xs, nombres = disenar(W, x, ley, zt, **kw)
        r = H.twfe_cluster(W.values, Xs, B=B)
        out = {}
        for nom in ("covid", "reapertura"):
            if nom not in nombres:
                continue
            j = nombres.index(nom)
            hip = f"{hip_prefijo}-{nom}" + ("" if conf else " (exploratoria)")
            b, se = r["beta"][j], r["se"][j]
            tabla.append({"diseno": "D2", "hipotesis": hip, "resultado": RES[var], "especificacion": etiqueta, "beta": b, "se": se,
                          "ic95_lo": b - 1.96 * se, "ic95_hi": b + 1.96 * se, "p": r["p_boot"][j], "p_normal": r["p_normal"][j],
                          "N_unidades": W.shape[0], "periodos": W.shape[1], "confirmatoria": conf and etiqueta == "principal",
                          "diagnosticos": ""})
            REG.log("v9-D2", hip + "|" + etiqueta, f"{var}~dosis×{nom}+leads+FE", W.columns[0], W.columns[-1], W.shape[0],
                    np.nan, np.nan, np.nan, coef_interes=b, p_interes=r["p_boot"][j], notas=etiqueta)
            out[nom] = b
        leads = [i for i, n in enumerate(nombres) if n.startswith("lead_")]
        wald = H.wald(r["beta"], r["V"], leads) if leads else (np.nan, np.nan)
        return r, nombres, x, out, wald

    for var in RES:
        conf = False                                  # addendum A1.1: D2 es exploratorio
        hp = "H2-renta" if var == "renta_media" else "H2-contratos"
        W = panel(a, var, 2014, 2025, dosis)
        xraw = dosis.reindex(W.index).values
        r, nombres, x, out, wald = estima(W, xraw, "principal", var, conf, hp)
        # pruebas
        Wp = panel(a, var, 2012, 2019, dosis)
        xp = dosis.reindex(Wp.index).values
        xp = (xp - xp.mean()) / xp.std()
        anios_p = np.array(Wp.columns)
        rp = H.twfe_cluster(Wp.values, [np.outer(xp, (anios_p >= 2017).astype(float))], B=B)
        rng = np.random.default_rng(P.SEED)
        jc, jr = nombres.index("covid"), nombres.index("reapertura")
        prov = np.array([c[:2] for c in W.index])
        perm = []
        for _ in range(NPERM):
            xs = x.copy()
            for pr_ in np.unique(prov):                 # permutación dentro de provincia (addendum A1.3)
                mm = prov == pr_
                xs[mm] = rng.permutation(x[mm])
            Xs, _ = disenar(W, xs, ley, zt)
            yv = H.dm2(W.values).ravel()
            Xm = np.column_stack([H.dm2(m).ravel() for m in Xs])
            perm.append(np.linalg.lstsq(Xm, yv, rcond=None)[0][[jc, jr]])
        perm = np.array(perm)
        pruebas.append({"prueba_diseno": f"D2 {RES[var]}", "pretend_wald": wald[0], "pretend_p": wald[1], "pretend_gl": 4,
                        "placebo_fecha_beta": rp["beta"][0], "placebo_fecha_p": rp["p_boot"][0],
                        "permutacion_p_covid": float(np.mean(np.abs(perm[:, 0]) >= abs(r["beta"][jc]))),
                        "permutacion_p_reapertura": float(np.mean(np.abs(perm[:, 1]) >= abs(r["beta"][jr])))})
        # robustez
        m = ~W.index.isin(ley)
        estima(W[m], dosis.reindex(W.index[m]).values, "sin municipios de la Ley 11/2020", var, conf, hp)
        m = W.index != "08019"
        estima(W[m], dosis.reindex(W.index[m]).values, "sin Barcelona", var, conf, hp)
        Wv = W[W.index.isin(dosis_viv.dropna().index)]
        estima(Wv, dosis_viv.reindex(Wv.index).values, "dosis: HUT por 100 viviendas (censo 2021)", var, conf, hp)
        estima(W, xraw, "sin controles de política", var, conf, hp, politicas=False)
        estima(W, xraw, "con tendencia lineal por dosis (sensibilidad A1.3)", var, conf, hp, tendencia=True)
        # trimestral 2019T1-2023T4, base 2019 (4 trimestres previos)
        q = P.incasol("T")
        wq = q[(q.t >= 2019 * 4) & (q.t <= 2023 * 4 + 3)].pivot_table(index="cod", columns="t", values=var)
        wq = np.log(wq[(wq > 0).all(1)].dropna())
        wq = wq[wq.index.isin(dosis.dropna().index)]
        tq = np.array(wq.columns)
        xq = dosis.reindex(wq.index).values
        xq = (xq - xq.mean()) / xq.std()
        Xq = [np.outer(xq, ((tq >= 2020 * 4 + 1) & (tq <= 2021 * 4 + 3)).astype(float)),
              np.outer(xq, (tq >= 2022 * 4).astype(float))]
        rq = H.twfe_cluster(wq.values, Xq, B=B)
        for j, nom in enumerate(("covid", "reapertura")):
            b, se = rq["beta"][j], rq["se"][j]
            tabla.append({"diseno": "D2", "hipotesis": f"{hp}-{nom}" + ("" if conf else " (exploratoria)"), "resultado": RES[var],
                          "especificacion": "trimestral 2019T1-2023T4 (base 2019)", "beta": b, "se": se,
                          "ic95_lo": b - 1.96 * se, "ic95_hi": b + 1.96 * se, "p": rq["p_boot"][j], "p_normal": rq["p_normal"][j],
                          "N_unidades": wq.shape[0], "periodos": wq.shape[1], "confirmatoria": False, "diagnosticos": "COVID = 2020T2-2021T4"})
            REG.log("v9-D2", f"{hp}-{nom}|trimestral", var, "2019T1", "2023T4", wq.shape[0], np.nan, np.nan, np.nan,
                    coef_interes=b, p_interes=rq["p_boot"][j], notas="robustez trimestral")
        # estudio de eventos completo (cada año, base 2019)
        anios = np.array(W.columns)
        ks = [k for k in anios if k != 2019]
        Xs = [np.outer(x, (anios == k).astype(float)) for k in ks]
        l11 = np.array([c in ley for c in W.index], float)
        ztm = np.array([c in zt.index for c in W.index], float)
        Xs += [np.outer(l11, (anios == 2021).astype(float)), np.outer(ztm, (anios >= 2024).astype(float))]
        re = H.twfe_cluster(W.values, Xs, B=99)
        es_rows += [{"resultado": RES[var], "anio": k, "beta": re["beta"][i], "se": re["se"][i]} for i, k in enumerate(ks)]
        es_rows.append({"resultado": RES[var], "anio": 2019, "beta": 0.0, "se": 0.0})
        # dosis-respuesta: quintiles de dosis (Q1 = referencia)
        qd = pd.qcut(pd.Series(xraw).rank(method="first"), 5, labels=False).values
        Xs = []
        for qq in range(1, 5):
            dq = (qd == qq).astype(float)
            Xs += [np.outer(dq, ((anios >= 2020) & (anios <= 2021)).astype(float)), np.outer(dq, (anios >= 2022).astype(float))]
        rdr = H.twfe_cluster(W.values, Xs, B=99)
        for i, qq in enumerate(range(1, 5)):
            for j, nom in enumerate(("covid", "reapertura")):
                dr_rows.append({"resultado": RES[var], "quintil_dosis": qq + 1, "periodo": nom,
                                "beta": rdr["beta"][2 * i + j], "se": rdr["se"][2 * i + j],
                                "dosis_media": float(np.mean(xraw[qd == qq]))})

    T = pd.DataFrame(tabla)
    PR = pd.DataFrame(pruebas)
    ES = pd.DataFrame(es_rows).sort_values(["resultado", "anio"])
    DR = pd.DataFrame(dr_rows)
    T.to_csv(OUT / "tabla_d2.csv", index=False, float_format="%.5f")
    PR.to_csv(OUT / "pruebas.csv", index=False, float_format="%.5f")
    ES.to_csv(OUT / "estudio_eventos.csv", index=False, float_format="%.5f")
    DR.to_csv(OUT / "dosis_respuesta.csv", index=False, float_format="%.5f")
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for j, nombre in enumerate(RES.values()):
        s = ES[ES.resultado == nombre]
        ax[j].errorbar(s.anio, s.beta, yerr=1.96 * s.se, fmt="o", ms=3, capsize=2)
        ax[j].axhline(0, color="grey", lw=0.8)
        ax[j].axvspan(2019.5, 2021.5, color="0.9")
        ax[j].set_title(nombre + " por 1 DE de dosis", fontsize=9)
    fig.suptitle("D2: estudio de eventos por dosis de HUT en 2019 (base 2019; IC 95 %). Fuente: Incasòl, IDESCAT; elaboración propia", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d2_eventos.png", dpi=130)
    plt.close(fig)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
    for j, nombre in enumerate(RES.values()):
        for nom, mk in (("covid", "o"), ("reapertura", "s")):
            s = DR[(DR.resultado == nombre) & (DR.periodo == nom)]
            ax[j].errorbar(s.quintil_dosis, s.beta, yerr=1.96 * s.se, fmt=mk, ms=4, capsize=2, label=nom)
        ax[j].axhline(0, color="grey", lw=0.8)
        ax[j].set_xlabel("quintil de dosis (referencia: Q1)")
        ax[j].set_title(nombre, fontsize=9)
        ax[j].legend(fontsize=7)
    fig.suptitle("D2: dosis-respuesta por quintiles (IC 95 %). Fuente: Incasòl, IDESCAT; elaboración propia", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d2_dosis_respuesta.png", dpi=130)
    plt.close(fig)
    pr = T[T.especificacion == "principal"]
    res = {"rama": "v9/d2", "pregunta": "¿Se movieron la renta y los contratos nuevos más donde había más HUT en 2019, con el COVID y la reapertura?",
           "capa": "pendiente (src/v9/f3_capas.py)", "datos": "Incasòl anual 2014-2025; IDESCAT HUT 2019; padrón 2019",
           "N": int(pr.N_unidades.max()), "metodo": "TWFE con dosis continua, leads 2014-2018, base 2019; bootstrap salvaje por municipio",
           "estimacion": pr[["hipotesis", "beta"]].to_dict("records"), "ic95": pr[["ic95_lo", "ic95_hi"]].values.tolist(),
           "p_ajustado": "ver output/v9/f3/tabla_capas.csv", "nivel_evidencia": "pendiente", "diagnosticos": PR.to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Incasòl no redistribuible: solo agregados."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    with pd.option_context("display.width", 250, "display.max_columns", 12):
        print(T[["hipotesis", "especificacion", "beta", "se", "p", "N_unidades"]].to_string())
        print(PR.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
