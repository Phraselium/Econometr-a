"""V9 F3 · D4 inmigración: réplica de Sanchis-Guarner (2023) y ampliación (pre-registro: docs/v9/hipotesis.md, D4).

Provincias (sin Ceuta ni Melilla). Endógena: Δ población extranjera / población inicial × 100 (padrón).
Instrumento de Card: Z_p = Σ_c (F_pc,t0 / Pop_p,t0) × (ΔF_c,-p / F_c,-p,t0) × 100, con 26 países individuales del
padrón y crecimiento nacional sin la propia provincia. Controles: log población inicial y suma de cuotas (BHJ).
Diagnósticos: F efectiva, IC de Anderson-Rubin, errores AKM, pesos de Rotemberg con pretendencia (Δ log P 2002→2003)
y número efectivo de shocks. SEED = 20261010.
Salidas: output/v9/d4/{tabla_d4.csv, diagnosticos.csv, rotemberg.csv, resultado.json, registry.csv, fig_d4.png}.
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
from paneles import construir  # noqa: E402

OUT = P.RAIZ / "output" / "v9" / "d4"
REG = Registry(OUT / "registry.csv")
REJILLA = np.linspace(-0.3, 0.3, 1201)


def fila(tab, hip, resultado, espec, r, akm_rf, akm_iv, ar, conf, n, extra=""):
    tab.append({"diseno": "D4", "hipotesis": hip, "resultado": resultado, "especificacion": espec,
                "beta": r["beta"], "se": r["se"], "ic95_lo": r["beta"] - 1.96 * r["se"], "ic95_hi": r["beta"] + 1.96 * r["se"],
                "p": r["p"], "rf": r["rf"], "se_rf": r["se_rf"], "p_rf": r["p_rf"], "se_akm_rf": akm_rf, "se_akm_iv": akm_iv,
                "primera_etapa": r["pi"], "F_eff": r["F_eff"], "AR_lo": ar[0], "AR_hi": ar[1],
                "AR_acotado": bool(ar[2] and REJILLA[0] < ar[0] and ar[1] < REJILLA[-1]), "N_unidades": n,
                "confirmatoria": conf, "diagnosticos": extra})


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pp = P.padron_nac("provincia")
    pv = P.panel_prov()
    vt = pv.pivot_table(index="cod_prov", columns="anio", values="valor_tasado")
    ipc = pv.pivot_table(index="cod_prov", columns="anio", values="ipc_alquiler_indice")
    sellada = set(pv[pv.prov_sellada_v6.astype(str).str.lower() == "true"].cod_prov)
    em = pd.read_csv(P.RAW9 / "ine_migraciones/ine_em_24385.csv.gz", dtype=str)
    em = em[em.Provincias.str.match(r"^\d{2} ") & (em.Nacionalidad == "Española")]
    em["v"] = pd.to_numeric(em.Total.str.replace(".", "", regex=False), errors="coerce")
    tab, diag, rot_rows = [], [], []

    def correr(t0, t1, etiqueta, outcomes, conf_map, solo=None, mascara=None, peso=False, interp=False):
        s = construir(pp, t0, t1, solo)
        d = s["d"]
        for nombre_y, serie in outcomes.items():
            sy = serie.copy()
            if interp and t1 in sy.columns:
                sy[t1] = sy[t1].fillna((sy.get(t1 - 1) + sy.get(t1 + 1)) / 2)
            y = np.log(sy[t1] / sy[t0]).reindex(d.index)
            m = y.notna() & d.notna().all(1)
            if mascara is not None:
                m &= mascara(d.index)
            yy, dd = y[m].values, d[m]
            W = dd[["lpop0", "suma_cuotas"]].values
            wts = dd.pop0.values if peso else None
            r = H.iv_just(yy, dd.x.values, dd.Z.values, W, w=wts)
            sh, gg = s["w"].loc[dd.index].values, s["g"].values
            akm_rf = H.akm_se(r, sh, gg, W, coef="rf")
            akm_iv = H.akm_se(r, sh, gg, W, coef="iv")
            ar = H.anderson_rubin(r, REJILLA)
            hip, conf = conf_map.get(nombre_y, ("exploratoria", False))
            fila(tab, hip, nombre_y, etiqueta, r, akm_rf, akm_iv, ar, conf and etiqueta.startswith("principal"), int(m.sum()))
            REG.log("v9-D4", f"{hip}|{etiqueta}|{nombre_y}", "Δlog P ~ Δext/pop | Z (Card LOO) + lpop0 + suma_cuotas",
                    t0, t1, int(m.sum()), np.nan, np.nan, np.nan, coef_interes=r["beta"], p_interes=r["p"], notas=etiqueta)
            # efecto total (por habitante)
            rt = H.iv_just(yy, dd.x_tot.values, dd.Z.values, W, w=wts)
            fila(tab, hip + " (efecto total)", nombre_y, etiqueta + " · endógena = Δ población total", rt,
                 H.akm_se(rt, sh, gg, W, coef="rf"), H.akm_se(rt, sh, gg, W, coef="iv"), H.anderson_rubin(rt, REJILLA), False, int(m.sum()))
        return s

    principales = {"Δ log IPC de alquiler": ipc, "Δ log valor tasado": vt}
    # addendum A1.1: todo D4 es exploratorio (H4-réplica-alquiler sin potencia con AKM y referencia en forma reducida)
    conf = {"Δ log IPC de alquiler": ("H4-réplica-alquiler (exploratoria)", False), "Δ log valor tasado": ("exploratoria", False)}
    s = correr(2003, 2012, "principal (réplica 2003-2012)", principales, conf)
    correr(2003, 2012, "sin provincias de la muestra sellada de v6", principales, conf, mascara=lambda ix: ~ix.isin(sellada))
    correr(2003, 2012, "sin Madrid ni Barcelona", principales, conf, mascara=lambda ix: ~ix.isin(["28", "08"]))
    correr(2003, 2012, "ponderado por población de 2003", principales, conf, peso=True)
    uni = ["33", "07", "39", "28", "30", "31", "26"]
    correr(2003, 2012, "sin las 7 CCAA uniprovinciales (valor tasado de otra fuente)", principales, conf,
           mascara=lambda ix: ~ix.isin(uni))
    correr(2003, 2012, "valor tasado 2012 interpolado (media 2011-2013; marcado)", {"Δ log valor tasado": vt}, conf, interp=True)
    correr(2015, 2022, "ampliación 2015-2022", principales, conf)
    for p in ("Venezuela", "Colombia", "Ucrania"):
        correr(2015, 2022, f"ampliación 2015-2022, solo {p}", principales, conf, solo=p)

    # desplazamiento de nativos: saldo interprovincial de españoles 2008-2012 / población 2008 sobre Z (réplica)
    d = s["d"]
    sal = em[em.Periodo.astype(int).between(2008, 2012)].groupby(em.Provincias.str[:2]).v.sum()
    tot = pp[pp.nacionalidad == "Total"].pivot_table(index="cod_provincia", columns="anio", values="poblacion")
    ynat = (sal / tot[2008] * 100).reindex(d.index)
    m = ynat.notna()
    Wn = d.loc[m, ["lpop0", "suma_cuotas"]].values
    rn = H.iv_just(ynat[m].values, d.Z[m].values, d.Z[m].values, Wn)
    diag.append({"prueba": "desplazamiento de nativos (forma reducida: saldo interprovincial de españoles 2008-2012, % pob. 2008, sobre Z)",
                 "valor": rn["rf"], "se": rn["se_rf"], "p": rn["p_rf"], "N": int(m.sum())})
    # primera etapa de la población total frente a la extranjera
    W = d[["lpop0", "suma_cuotas"]].values
    r_ext = H.iv_just(d.x.values, d.Z.values, d.Z.values, W)
    r_tot = H.iv_just(d.x_tot.values, d.Z.values, d.Z.values, W)
    diag.append({"prueba": "primera etapa Δ extranjeros/pob sobre Z", "valor": r_ext["rf"], "se": r_ext["se_rf"], "p": r_ext["p_rf"], "N": len(d)})
    diag.append({"prueba": "primera etapa Δ población total/pob sobre Z", "valor": r_tot["rf"], "se": r_tot["se_rf"], "p": r_tot["p_rf"], "N": len(d)})
    # Rotemberg (réplica, IPC de alquiler) y pretendencia de las cuotas de los 5 países de mayor peso
    y = np.log(ipc[2012] / ipc[2003]).reindex(d.index)
    m = y.notna()
    alpha = H.rotemberg(y[m].values, d.x[m].values, s["w"].loc[m[m].index].values, s["g"].values, W[m.values])
    rot = pd.DataFrame({"pais": s["w"].columns, "alpha": alpha, "g_nacional": s["g"].values}).sort_values("alpha", key=np.abs, ascending=False)
    pre_vt = np.log(vt[2003] / vt[2002]).reindex(d.index)
    pre_ipc = np.log(ipc[2003] / ipc[2002]).reindex(d.index)
    for _, rr in rot.head(5).iterrows():
        for nom, pre in (("Δ log valor tasado 2002→2003", pre_vt), ("Δ log IPC alquiler 2002→2003", pre_ipc)):
            mm = pre.notna()
            X = np.column_stack([np.ones(mm.sum()), s["w"].loc[mm[mm].index, rr.pais].values, d.loc[mm, "lpop0"].values])
            c = H.conley(pre[mm].values, X, np.zeros((mm.sum(), 2)), -1.0)   # corte < 0 → HC0
            rot_rows.append({"pais": rr.pais, "alpha": rr.alpha, "pretendencia": nom, "coef_cuota": c["beta"][1],
                             "se_hc1": c["se_hc1"][1], "p": float(2 * __import__("scipy").stats.norm.sf(abs(c["beta"][1] / c["se_hc1"][1])))})
    sc = s["w"].sum(0)
    sc = sc / sc.sum()
    n_ef = float(1 / np.sum(sc ** 2))
    diag.append({"prueba": "BHJ: número efectivo de shocks (1/HHI de pesos de exposición)", "valor": n_ef, "se": np.nan, "p": np.nan, "N": len(sc)})
    if rot_rows:
        pr_df = pd.DataFrame(rot_rows)
        for nom in pr_df.pretendencia.unique():
            m_ = pr_df.pretendencia == nom
            pr_df.loc[m_, "p_holm"] = H.holm(pr_df.loc[m_, "p"].tolist())
        rot_rows = pr_df.to_dict("records")
    rot = pd.concat([rot.head(10).assign(pretendencia="", coef_cuota=np.nan, se_hc1=np.nan, p=np.nan), pd.DataFrame(rot_rows)])

    T = pd.DataFrame(tab)
    D = pd.DataFrame(diag)
    T.to_csv(OUT / "tabla_d4.csv", index=False, float_format="%.5f")
    D.to_csv(OUT / "diagnosticos.csv", index=False, float_format="%.5f")
    rot.to_csv(OUT / "rotemberg.csv", index=False, float_format="%.5f")
    s2 = s["d"]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].scatter(s2.Z, s2.x, s=12)
    ax[0].set_xlabel("Z (entrada predicha, puntos de población)")
    ax[0].set_ylabel("Δ extranjeros 2003-2012 (% pob. 2003)")
    yy = np.log(ipc[2012] / ipc[2003]).reindex(s2.index)
    ax[1].scatter(s2.Z, yy, s=12)
    ax[1].set_xlabel("Z")
    ax[1].set_ylabel("Δ log IPC alquiler 2003-2012")
    fig.suptitle("D4: primera etapa y forma reducida por provincia. Fuente: INE (padrón, IPC); elaboración propia", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig_d4.png", dpi=130)
    plt.close(fig)
    pr = T[T.especificacion.str.startswith("principal") & ~T.hipotesis.str.contains("total")]
    res = {"rama": "v9/d4", "pregunta": "¿Cuánto suben precios y alquileres provinciales cuando la población crece por inmigración predicha por redes de origen?",
           "capa": "pendiente (src/v9/f3_capas.py)", "datos": "Padrón por nacionalidad 2003-2022; IPC alquiler; valor tasado; EM",
           "N": int(pr.N_unidades.max()), "metodo": "2SLS shift-share (Card, LOO); AKM; AR; F efectiva; Rotemberg",
           "estimacion": pr[["resultado", "beta"]].to_dict("records"), "ic95": pr[["ic95_lo", "ic95_hi"]].values.tolist(),
           "p_ajustado": "ver output/v9/f3/tabla_capas.csv", "nivel_evidencia": "pendiente", "diagnosticos": D.to_dict("records"),
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Rotemberg con crecimientos nacionales (aproximación sin leave-one-out)."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    with pd.option_context("display.width", 250, "display.max_columns", 14):
        print(T[["hipotesis", "resultado", "especificacion", "beta", "se", "p", "se_akm_iv", "F_eff", "AR_lo", "AR_hi", "N_unidades"]].to_string())
        print(D.to_string())
        print(rot.to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
