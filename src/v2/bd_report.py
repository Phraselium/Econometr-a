"""BD - tablas resumen, figuras y textos. Sin lenguaje causal: todo es EXPLORATORIO salvo lo heredado."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bd_lib as L  # noqa: E402

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

TOP = ["demografia", "empleo_renta", "credito_tipos_cu", "oferta", "politica", "comun_efectos_tiempo", "residuo"]
SUBS = ["demografia_20_34", "demografia_extranj"]
ETQ = {"demografia": "demografía (20-34 + extranjera)", "demografia_20_34": "  · pob 20-34", "demografia_extranj": "  · pob extranjera",
       "empleo_renta": "empleo (ocupados)", "credito_tipos_cu": "crédito / coste de uso", "oferta": "oferta (terminadas)",
       "politica": "política (tope de rentas CAT)", "comun_efectos_tiempo": "común: efectos de tiempo + FE (no explicado)",
       "residuo": "residuo", "turismo": "turismo (VUT)", "observado": "OBSERVADO"}
COL = {"demografia": "#1b6ca8", "empleo_renta": "#6aa84f", "credito_tipos_cu": "#e69f00", "oferta": "#8e6bb0",
       "politica": "#c0504d", "comun_efectos_tiempo": "#b8b8b8", "residuo": "#7f7f7f"}
CAUSAL_AVISO = "Asociaciones condicionales; descomposición contable; sin interpretación causal."


def evidencia(mercado, comp):
    if comp in ("comun_efectos_tiempo", "residuo", "observado", "explicado_familias"):
        return "DESCRIPTIVO"
    if mercado == "alquiler":
        if comp == "demografia_20_34":
            return "ASOCIACIÓN ROBUSTA (candidato: coef. 20-34 de H1; mejora predictiva confirmada en sellado; Holm-7 pendiente en BS)"
        if comp == "demografia":
            return "mixto: 20-34 candidato a ASOCIACIÓN ROBUSTA; extranjera EXPLORATORIO"
        if comp == "politica":
            return "EXPLORATORIO (H5/tope: falló placebos y pretendencias en BP)"
        return "EXPLORATORIO"
    return "EXPLORATORIO (H2 no confirmada en el sellado)"


def tabla_resumen(contrib):
    c = contrib.copy()
    m1 = c[c.modelo == "M1"]
    m2 = c[c.modelo == "M2"].set_index(["mercado", "periodo", "componente"])
    rows = []
    for _, r in m1.iterrows():
        k = (r["mercado"], r["periodo"], r["componente"])
        o = m2.loc[k] if k in m2.index else None
        rows.append(dict(periodo=r["periodo"], familia=r["componente"], mercado=r["mercado"],
                         contrib_pp_M1=r["contrib_pp"], ic95_inf_M1=r["ic95_inf"], ic95_sup_M1=r["ic95_sup"],
                         pct_observado_M1=r["pct_observado"], observado_pp=r["observado_pp"],
                         contrib_pp_M2=o["contrib_pp"] if o is not None else np.nan,
                         ic95_inf_M2=o["ic95_inf"] if o is not None else np.nan,
                         ic95_sup_M2=o["ic95_sup"] if o is not None else np.nan,
                         pct_observado_M2=o["pct_observado"] if o is not None else np.nan,
                         nivel_evidencia=evidencia(r["mercado"], r["componente"])))
    t = pd.DataFrame(rows)
    orden = {p: i for i, p in enumerate(L.PNAMES + ["P2-P4 (desde 2014)", "P3-P4 (desde 2020)"])}
    forden = {f: i for i, f in enumerate(["observado", "explicado_familias"] + TOP[:5] + SUBS + TOP[5:])}
    t["_o"], t["_f"] = t["periodo"].map(orden), t["familia"].map(forden)
    t = t.sort_values(["mercado", "_o", "_f"]).drop(columns=["_o", "_f"]).reset_index(drop=True)
    return t


def fig_apilada(contrib, mercado, ruta, titulo):
    fig, axs = plt.subplots(1, 2, figsize=(13, 5.2), sharey=False)
    for ax, mo, sub in zip(axs, ("M1", "M2"), ("M1: FE de provincia y de trimestre", "M2: sin FE de trimestre (con Δ4 coste de uso nacional)")):
        c = contrib[(contrib.mercado == mercado) & (contrib.modelo == mo)]
        x = np.arange(4)
        pos, neg = np.zeros(4), np.zeros(4)
        for f in [f for f in TOP if f in set(c.componente)]:
            v = np.array([c[(c.periodo == p) & (c.componente == f)]["contrib_pp"].iloc[0] for p in L.PNAMES])
            b = np.where(v >= 0, pos, neg)
            ax.bar(x, v, 0.6, bottom=b, color=COL[f], label=ETQ[f], edgecolor="white", linewidth=0.5)
            pos += np.where(v >= 0, v, 0)
            neg += np.where(v < 0, v, 0)
        obs = np.array([c[(c.periodo == p) & (c.componente == "observado")]["contrib_pp"].iloc[0] for p in L.PNAMES])
        ex = c[c.componente == "explicado_familias"].set_index("periodo")
        xe = x + 0.36
        ax.errorbar(xe, ex.loc[L.PNAMES, "contrib_pp"], yerr=[ex.loc[L.PNAMES, "contrib_pp"] - ex.loc[L.PNAMES, "ic95_inf"],
                    ex.loc[L.PNAMES, "ic95_sup"] - ex.loc[L.PNAMES, "contrib_pp"]], fmt="s", color="black", ms=4, capsize=3,
                    label="suma de familias explicadas (IC95)")
        ax.scatter(x, obs, marker="D", color="black", zorder=5, s=36, label="observado")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([f"{p}\n{L.PERIODOS[p][0]}-{min(L.PERIODOS[p][1], L.Q_FIN_MUESTRA)}" for p in L.PNAMES], fontsize=8)
        ax.set_ylabel("contribución acumulada (pp de ln)")
        ax.set_title(sub, fontsize=10)
        ax.grid(axis="y", alpha=0.25)
    axs[0].legend(fontsize=7, loc="best")
    fig.suptitle(titulo + " - EXPLORATORIO", fontsize=11)
    fig.text(0.01, 0.005, "Fuente: v2_common.load (panel_prov_q, nacional_q_v2); elaboración propia. IC95: envolvente de bootstrap por provincias y por bloques de tiempo (B=999). " + CAUSAL_AVISO,
             fontsize=6.5, ha="left")
    fig.tight_layout(rect=(0, 0.03, 1, 0.96))
    fig.savefig(ruta, dpi=130, metadata={"Software": None})
    plt.close(fig)


def fig_bosque(contrib, mercado, modelo, ruta, titulo):
    c = contrib[(contrib.mercado == mercado) & (contrib.modelo == modelo)]
    comps = [f for f in TOP if f in set(c.componente)]
    fig, axs = plt.subplots(1, 4, figsize=(15, 4.2), sharey=True)
    for ax, p in zip(axs, L.PNAMES):
        cp = c[c.periodo == p].set_index("componente")
        y = np.arange(len(comps))[::-1]
        v = cp.loc[comps, "contrib_pp"].values
        ax.errorbar(v, y, xerr=[v - cp.loc[comps, "ic95_inf"].values, cp.loc[comps, "ic95_sup"].values - v], fmt="o", color="#1b6ca8", capsize=3, ms=4)
        ax.axvline(0, color="black", lw=0.8)
        ax.axvline(cp.loc["observado", "contrib_pp"], color="#c0504d", ls="--", lw=1)
        ax.set_title(f"{p} (observado {cp.loc['observado', 'contrib_pp']:.1f} pp)", fontsize=9)
        ax.set_xlabel("pp de ln acumulados (IC95)")
        ax.grid(axis="x", alpha=0.25)
    axs[0].set_yticks(np.arange(len(comps))[::-1])
    axs[0].set_yticklabels([ETQ[f] for f in comps], fontsize=8)
    fig.suptitle(f"{titulo} ({modelo}) - EXPLORATORIO", fontsize=11)
    fig.text(0.01, 0.005, "Fuente: v2_common.load; elaboración propia. Línea discontinua roja: crecimiento observado. " + CAUSAL_AVISO, fontsize=6.5)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    fig.savefig(ruta, dpi=130, metadata={"Software": None})
    plt.close(fig)


def fig_nacional(cp, lp, ruta):
    fig, axs = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, df, tt in ((axs[0], lp, "Largo plazo (identidad ECM v1 real)"), (axs[1], cp, "Corto plazo (ecuación ECM v1 real)")):
        comps = [c for c in df.componente.unique() if c != "observado"]
        cmap = plt.get_cmap("tab10")
        x = np.arange(4)
        pos, neg = np.zeros(4), np.zeros(4)
        for i, f in enumerate(comps):
            v = np.array([df[(df.periodo == p) & (df.componente == f)]["contrib_pp"].iloc[0] for p in L.PNAMES])
            b = np.where(v >= 0, pos, neg)
            ax.bar(x, v, 0.6, bottom=b, color=cmap(i), label=f, edgecolor="white", linewidth=0.4)
            pos += np.where(v >= 0, v, 0)
            neg += np.where(v < 0, v, 0)
        obs = [df[(df.periodo == p) & (df.componente == "observado")]["contrib_pp"].iloc[0] for p in L.PNAMES]
        ax.scatter(x, obs, marker="D", color="black", zorder=5, s=34, label="observado")
        ax.axhline(0, color="black", lw=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(L.PNAMES)
        ax.set_ylabel("pp de ln precio real acumulados")
        ax.set_title(tt, fontsize=10)
        ax.legend(fontsize=6.5)
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("Nacional: precio real de la vivienda (IPV/deflactor), descomposición con el ECM v1 real - EXPLORATORIO", fontsize=10)
    fig.text(0.01, 0.005, "Fuente: nacional_q_v2 (v2_common.load); elaboración propia. Los IC95 (bootstrap de residuos por bloques) están en nacional_*.csv. " + CAUSAL_AVISO, fontsize=6.5)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    fig.savefig(ruta, dpi=130, metadata={"Software": None})
    plt.close(fig)


def md_tabla(df, cols, fmt):
    h = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    for _, r in df.iterrows():
        h += "| " + " | ".join(fmt[c](r) if c in fmt else str(r[c]) for c in cols) + " |\n"
    return h
