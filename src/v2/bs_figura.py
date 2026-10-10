"""BS · figura resumen: contribuciones por periodo (M1, IC95 de BD), alquiler frente a compra. Datos: BD/tabla_resumen.csv."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import bs_lib as L  # noqa: E402

FAM = [("demografia", "Demografía\n(20-34 + extranjera)"), ("empleo_renta", "Empleo"), ("credito_tipos_cu", "Crédito y\ncoste de uso"),
       ("oferta", "Oferta"), ("politica", "Política\n(tope CAT)")]
PER = ["P1", "P2", "P3", "P4"]
ETQ = {"P1": "P1 2008-13", "P2": "P2 2014-19", "P3": "P3 2020-21", "P4": "P4 2022-24T1"}
COL = {"P1": "#c6dbef", "P2": "#6baed6", "P3": "#2171b5", "P4": "#08306b"}


def figura(destino: Path) -> Path:
    d = L.c("BD/tabla_resumen.csv")
    fig, axs = plt.subplots(1, 2, figsize=(11, 5.2), sharey=False)
    for ax, mer in zip(axs, ("alquiler", "compra")):
        fams = [f for f in FAM if not (mer == "compra" and f[0] == "politica")]
        for i, (fk, _) in enumerate(fams):
            for k, p in enumerate(PER):
                r = d[(d.mercado == mer) & (d.periodo == p) & (d.familia == fk)].iloc[0]
                y = i + (k - 1.5) * 0.18
                ax.plot([r.ic95_inf_M1, r.ic95_sup_M1], [y, y], color=COL[p], lw=1.8, solid_capstyle="butt")
                ax.plot(r.contrib_pp_M1, y, "o", color=COL[p], ms=5, mec="black", mew=0.4, label=ETQ[p] if i == 0 else None)
        ax.axvline(0, color="black", lw=0.8)
        ax.set_yticks(range(len(fams)))
        ax.set_yticklabels([n for _, n in fams], fontsize=9)
        ax.invert_yaxis()
        ax.set_title("Alquiler (IPC alquiler, nominal)" if mer == "alquiler" else "Compra (valor tasado, real)", fontsize=11, loc="left")
        ax.set_xlabel("Contribución acumulada (pp de ln), M1 [IC95 %]", fontsize=8.5)
        ax.grid(axis="x", color="#dddddd", lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=8, frameon=False, loc="upper right", ncol=4, bbox_to_anchor=(0.99, 0.965))
    fig.suptitle("Contribuciones por periodo y familia: asociaciones condicionales (EXPLORATORIO), no efectos causales", fontsize=10.5, x=0.01, ha="left")
    fig.text(0.01, 0.005, "Fuente: output/v2/BD/tabla_resumen.csv. IC95 % de BD (bootstrap por provincias y por bloques de tiempo). "
             "No se muestra el componente común (efectos de tiempo): domina el crecimiento observado. M2 en la tabla.", fontsize=7, ha="left")
    fig.tight_layout(rect=(0, 0.03, 1, 0.93))
    destino.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino, dpi=150, metadata={"Software": None})
    plt.close(fig)
    return destino
