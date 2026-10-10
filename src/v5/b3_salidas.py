"""B3 · salidas: mapas deterministas, figuras, resultado.json, hechos.json, desviaciones.md. Lo llama b3_run.main()."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output/v5/B3"
GEOM = RAIZ / "data/raw/v5/prov_geom_simplificada.json"
import b3_data as bd  # noqa: E402


def mapas(D):
    g = json.load(open(GEOM))
    nom = {"Y1": "Y1 precio de compra (valor tasado)", "Y2": "Y2 alquiler (SERPAVI)", "Y3": "Y3 esfuerzo (precio/renta)"}
    ventana = {"P1": {"Y1": "2015-2025", "Y2": "2015-2024", "Y3": f"2015-{D.attrs['ycre']}"},
               "P2": {"Y1": "2021-2025", "Y2": "2021-2024", "Y3": f"2021-{D.attrs['ycre']}"}}
    for lab in ("P1", "P2"):
        Y = bd.dependientes(D, lab)
        fig, axs = plt.subplots(1, 3, figsize=(18, 6.2))
        for ax, k in zip(axs, ("Y1", "Y2", "Y3")):
            v = (np.exp(Y[k]) - 1) * 100
            lo, hi = np.nanpercentile(v, 2), np.nanpercentile(v, 98)
            norm = plt.Normalize(lo, hi)
            cmap = plt.get_cmap("viridis")
            for c, rings in g.items():
                val = v.get(c, np.nan)
                col = "#cccccc" if pd.isna(val) else cmap(norm(val))
                ax.add_collection(PolyCollection([np.array(r) for r in rings], facecolors=col, edgecolors="white", linewidths=0.3))
            ax.set_xlim(-1000, 1300)
            ax.set_ylim(3700, 4900)
            ax.set_aspect("equal")
            ax.axis("off")
            sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
            fig.colorbar(sm, ax=ax, shrink=0.55, label="variación %")
            ax.set_title(f"{nom[k]}\n{ventana[lab][k]} (gris: sin dato)", fontsize=10)
        fig.suptitle(f"B3 · {lab}: variación por provincia (Canarias trasladada). Descriptivo, sin inferencia.", fontsize=11)
        fig.savefig(OUT / f"figuras/mapa_{lab}.png", dpi=110, bbox_inches="tight")
        plt.close(fig)


def fig_shapley(st):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    i = np.arange(len(st))
    ax.bar(i - 0.2, st.valor_tasado, 0.4, label="Y1 valor tasado")
    ax.bar(i + 0.2, st.registradores, 0.4, label="Y1 Registradores")
    ax.set_xticks(i)
    ax.set_xticklabels(st.index)
    ax.set_ylabel("Contribución Shapley al R²")
    ax.legend()
    ax.set_title("B3 · Shapley de R² por familia (P1, N=50). C4: magnitudes exploratorias")
    fig.savefig(OUT / "figuras/shapley.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def escribe(D, cuadro, R, rg, st, mv):
    mapas(D)
    fig_shapley(st)
    hip, ycre = R["hip"], R["ycre"]
    sens = R["sens"]
    mvr = {m["hipotesis"]: m for m in R["mvr"]}
    sh = R["shap"]
    fam_n = R["n"]
    emd = json.load(open(OUT / "tablas/resumen_potencia.json")) if (OUT / "tablas/resumen_potencia.json").exists() else {}
    resultado = {
        "rama": "B3",
        "pregunta": "¿Con qué características provinciales se asocian las diferencias de variación del precio, el alquiler y el esfuerzo de acceso entre las 50 provincias, 2015-2025?",
        "capa": "C4",
        "datos": ("MIVAU valor tasado libre trimestral (2015T1-2025T4) y Registradores provincial anual (2015, 2025); SERPAVI municipal agregado a provincia (2015/2021-2024); "
                  "IPVA INE (robustez); EPA INE ocupados por sector y provincia (2011/2015-2025); Padrón INE 1-ene (2015-2025); CRE INE PIB provincial (hasta "
                  f"{ycre}); INE VUT 2021; Censo 2021 viviendas; INE hipotecas sobre viviendas (2015); A4 (clase, brecha, respuesta de oferta 2021-2025); centroides municipales UTM30"),
        "N": {"principal_Y1_P1": fam_n["Y1_P1"], "Y2_P1": fam_n["Y2_P1"], "Y2_P2": fam_n["Y2_P2"], "Y3_P1": fam_n["Y3_P1"],
              "excluidas": "Ceuta y Melilla (sin A4, sin SERPAVI 2015, sin sectores EPA comparables)"},
        "metodo": ("MCO con las 8 familias a la vez (13 regresores estandarizados); EE HC3 y Conley (Bartlett, 100 y 200 km); se usa el mayor p; inferencia por "
                   "aleatorización Freedman-Lane (5.000 permutaciones, SEED=20261010); Holm sobre 8 familias x Y1 x P1 (y sobre las 3 confirmatorias); BH sobre las 40 "
                   "exploratorias; Shapley de R² con dos fuentes de Y1; multiverso 32 especificaciones; Oster y Cinelli-Hazlett."),
        "estimacion": {h: {"regresor": v["regresor"], "b_por_DT_logpuntos": v["b_por_DT"], "beta_std_en_DT_de_Y": v["beta_std"], "signo_esperado": v["signo_esperado"]} for h, v in hip.items()},
        "ic95": {h: v["ic95"] for h, v in hip.items()},
        "p_ajustado": {h: {"holm_8_familias": v["p_holm8"], "holm_3_confirmatorias": v["p_holm3"], "p_mayor_sin_ajuste": v["p_mayor"], "p_aleatorizacion": v["p_perm"]} for h, v in hip.items()},
        "nivel_evidencia": "DESCRIPTIVO (descriptivo honesto: el efecto mínimo detectable con Holm supera 0,5 DT; ver potencia.md)",
        "diagnosticos": {
            "R2_principal": R["r2_principal"], "R2_ajustado_principal": R["r2a_principal"],
            "shapley": {"orden_igual_en_dos_fuentes": sh["orden_igual"], "spearman": sh["spearman"], "kendall": sh["kendall"],
                        "R2_tasado": sh["r2_tasado"], "R2_registradores": sh["r2_reg"]},
            "multiverso": R["mvr"], "sensibilidad": sens,
            "advertencia_F6": ("Y1 es la variación del log del precio y F6 es el log del precio inicial de la misma serie: el error de medida del precio inicial "
                               "empuja el coeficiente hacia valores negativos. Control con el precio inicial de otra fuente en hip['H-B3-6']."),
        },
        "fuera_muestra": R["fuera"],
        "notas": ("Capa C4. Lenguaje de asociación, no de efecto. Validación AR(4)/ECM v1 y bloques con embargo no aplican a un corte transversal de 50 provincias: se "
                  "sustituyen por validación cruzada dejando una fuera (LOO) frente al modelo de solo media, con Diebold-Mariano corregido por HLN (declarado como "
                  "desviación). Ventanas distintas por límite de datos: Y2 hasta 2024 (SERPAVI), Y3 y crecimiento de renta hasta "
                  f"{ycre} (CRE). Renta: PIB per cápita CRE en lugar de ADRH (ver desviaciones.md)."),
    }
    json.dump(resultado, open(OUT / "resultado.json", "w"), indent=1, ensure_ascii=False, default=float)
    H = []

    def h(id_, ind, val, mn, mx, uni, per, cob, fu, fecha):
        H.append(dict(id=id_, indicador=ind, valor=val, min=mn, max=mx, unidad=uni, periodo=per, cobertura=cob, fuentes=fu, capa="C4", fecha_dato=fecha))
    for k, v in hip.items():
        h(f"B3-{k}-b", f"Asociación de {v['regresor']} con la variación log del precio (por DT del regresor)", round(v["b_por_DT"] * 100, 2),
          round(v["ic95"][0] * 100, 2), round(v["ic95"][1] * 100, 2), "puntos logarítmicos (≈ %) por DT", "2015-2025", "50 provincias",
          "MIVAU valor tasado; INE (EPA, Padrón); A4", "2026-10-10 (tasado hasta 2025T4)")
        h(f"B3-{k}-p", f"p ajustado Holm (8 familias) de {k}", round(v["p_holm8"], 4), None, None, "probabilidad", "2015-2025", "50 provincias", "MIVAU valor tasado; INE", "2026-10-10")
    h("B3-R2", "R² del modelo de 8 familias (Y1 tasado, P1)", round(R["r2_principal"], 3), None, None, "proporción", "2015-2025", "50 provincias", "MIVAU valor tasado; INE; A4", "2026-10-10")
    h("B3-shap-orden", "Shapley: mismo orden de familias con Y1 tasado y Registradores (1 = sí)", int(sh["orden_igual"]), None, None, "indicador", "2015-2025", "50 provincias", "MIVAU valor tasado; Registradores", "2026-10-10")
    h("B3-shap-spearman", "Correlación de Spearman de los Shapley entre fuentes", round(sh["spearman"], 3), None, None, "coeficiente", "2015-2025", "50 provincias", "MIVAU valor tasado; Registradores", "2026-10-10")
    for k, m in mvr.items():
        h(f"B3-mv-{k}", f"Multiverso {k}: % de especificaciones con el signo de la principal", round(m["pct_mismo_signo_que_principal"], 1), None, None, "%", "2015-2025 / 2021-2025", "32 especificaciones", "MIVAU; Registradores; INE", "2026-10-10")
    json.dump(H, open(OUT / "hechos.json", "w"), indent=1, ensure_ascii=False, default=float)
