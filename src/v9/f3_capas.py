"""V9 F3 · consolidación: p ajustados (Holm en la familia confirmatoria {H1a-renta, H1b-renta}; BH q = 0,10 en una
única familia exploratoria con la especificación principal de cada hipótesis exploratoria) y capa de cada resultado
según las reglas pre-registradas (docs/v9/hipotesis.md y addendum A1). Nada sube de capa por robustez.
Salidas: output/v9/f3/{tabla_capas.csv, tabla_revista.md, comparacion_literatura.csv, resultado.json},
output/v9/registry.csv (consolidado de los registros de cada diseño).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import herramientas as H  # noqa: E402
import paneles as P  # noqa: E402

V9 = P.RAIZ / "output" / "v9"
OUT = V9 / "f3"


def fmt(x, d=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{d}f}".replace(".", ",")


def fmt_p(p):
    if p is None or not np.isfinite(p):
        return "—"
    return "< 0,001" if p < 0.001 else fmt(p, 3)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    d1 = pd.read_csv(V9 / "d1/tabla_d1.csv")
    pr1 = pd.read_csv(V9 / "d1/pruebas.csv").set_index("prueba_diseno")
    d2 = pd.read_csv(V9 / "d2/tabla_d2.csv")
    pr2 = pd.read_csv(V9 / "d2/pruebas.csv").set_index("prueba_diseno")
    d3 = pd.read_csv(V9 / "d3/tabla_d3.csv")
    d4 = pd.read_csv(V9 / "d4/tabla_d4.csv")
    d5 = pd.read_csv(V9 / "d5/tabla_d5.csv")
    filas = []
    # principales por hipótesis
    for _, r in d1[d1.especificacion.str.contains("principal") | (d1.diseno == "D1c")].iterrows():
        prueba = pr1.loc[f"{r.diseno} {r.resultado}"] if f"{r.diseno} {r.resultado}" in pr1.index else None
        if prueba is None and isinstance(r.diagnosticos, str) and "pretend p = " in r.diagnosticos:
            prueba = pd.Series({"pretend_p": float(r.diagnosticos.split("pretend p = ")[1].split(";")[0]), "placebo_fecha_p": np.nan,
                                "honest_M1_lo": np.nan, "honest_M1_hi": np.nan, "honest_Mbar_ruptura": np.nan,
                                "permutacion_etiquetas_p": np.nan})
        filas.append({"diseno": r.diseno, "hipotesis": r.hipotesis, "resultado": r.resultado, "beta": r.beta, "se": r.se,
                      "ic95_lo": r.ic95_lo, "ic95_hi": r.ic95_hi, "p": r.p, "N": r.N_unidades, "tratadas": r.tratadas,
                      "confirmatoria": bool(r.confirmatoria and r.diseno in ("D1a", "D1b") and "renta" in r.resultado),
                      "pretend_p": prueba.pretend_p if prueba is not None else np.nan,
                      "placebo_fecha_p": prueba.placebo_fecha_p if prueba is not None else np.nan,
                      "honest_M1": (prueba.honest_M1_lo, prueba.honest_M1_hi) if prueba is not None else (np.nan, np.nan),
                      "honest_ruptura": prueba.honest_Mbar_ruptura if prueba is not None else np.nan,
                      "perm_p": prueba.permutacion_etiquetas_p if prueba is not None else np.nan,
                      "metodo": "CS (nunca tratados)" if r.diseno != "D1c" else "CS (aún no tratados)"})
    for _, r in d2[d2.especificacion == "principal"].iterrows():
        nom = "renta" if "renta" in r.hipotesis else "contratos"
        prueba = pr2.loc[f"D2 {r.resultado}"]
        per = "covid" if "covid" in r.hipotesis else "reapertura"
        tend = d2[(d2.hipotesis == r.hipotesis) & d2.especificacion.str.startswith("con tendencia")]
        filas.append({"diseno": "D2", "hipotesis": r.hipotesis, "resultado": r.resultado + f" ({per}; por 1 DE de dosis)",
                      "beta": r.beta, "se": r.se, "ic95_lo": r.ic95_lo, "ic95_hi": r.ic95_hi, "p": r.p, "N": r.N_unidades,
                      "tratadas": np.nan, "confirmatoria": False, "pretend_p": prueba.pretend_p,
                      "placebo_fecha_p": prueba.placebo_fecha_p, "perm_p": prueba[f"permutacion_p_{per}"],
                      "tendencia_p": float(tend.p.iloc[0]) if len(tend) else np.nan,
                      "metodo": f"TWFE dosis continua ({nom})"})
    d3p = d3[d3.especificacion.str.startswith("placebo") & d3.especificacion.str.contains("10 km")].set_index("resultado").p
    for _, r in d3[d3.especificacion.str.startswith("principal") & d3.especificacion.str.contains("10 km")].iterrows():
        filas.append({"diseno": "D3", "hipotesis": "descriptiva", "resultado": f"{r.resultado} ~ ΔVUT por 100 viviendas",
                      "beta": r.beta, "se": r.se, "ic95_lo": r.ic95_lo, "ic95_hi": r.ic95_hi, "p": r.p, "N": r.N_unidades,
                      "confirmatoria": False, "placebo_fecha_p": float(d3p.get(r.resultado, np.nan)),
                      "metodo": "MCO diferencias largas, Conley 10 km"})
    rot = pd.read_csv(V9 / "d4/rotemberg.csv")
    rot_fallan = sorted(set(rot[(rot.get("p_holm", pd.Series(dtype=float)) < 0.10)].pais)) if "p_holm" in rot else []
    for _, r in d4[d4.especificacion.str.startswith("principal") | (d4.especificacion == "ampliación 2015-2022")].iterrows():
        filas.append({"diseno": "D4", "hipotesis": r.hipotesis, "resultado": f"{r.resultado} ({r.especificacion})",
                      "beta": r.beta, "se": r.se, "ic95_lo": r.ic95_lo, "ic95_hi": r.ic95_hi,
                      # con instrumento débil (F < 23,1) la inferencia válida es la de Anderson-Rubin: con un instrumento,
                      # su p para β = 0 es el de la forma reducida (revisión F3, hallazgo 2)
                      "p": r.p_rf if r.F_eff < 23.1 else r.p, "p_wald": r.p, "N": r.N_unidades,
                      "confirmatoria": False, "F_eff": r.F_eff, "AR": (r.AR_lo, r.AR_hi), "AR_acotado": r.get("AR_acotado", np.nan),
                      "rotemberg_fallan": ", ".join(rot_fallan) if r.especificacion.startswith("principal") else "",
                      "se_akm": r.se_akm_iv, "metodo": "2SLS shift-share"})
    for _, r in d5[d5.especificacion == "principal"].iterrows():
        filas.append({"diseno": "D5", "hipotesis": "exploratoria", "resultado": r.resultado + " por shock × 1 DE de exposición",
                      "beta": r.beta, "se": r.se, "ic95_lo": r.ic95_lo, "ic95_hi": r.ic95_hi, "p": r.p, "N": r.N_unidades,
                      "confirmatoria": False, "metodo": "proyección local, Driscoll-Kraay"})
    T = pd.DataFrame(filas)
    conf = T.confirmatoria
    T["p_holm"] = np.nan
    T.loc[conf, "p_holm"] = H.holm(T.loc[conf, "p"].tolist())
    expl = ~conf & (T.diseno != "D3")
    T["p_bh"] = np.nan
    T.loc[expl, "p_bh"] = H.bh(T.loc[expl, "p"].fillna(1).tolist())

    def capa(r):
        if r.confirmatoria:
            pruebas = {"Holm < 0,05": r.p_holm < 0.05, "pretendencias p > 0,10": r.pretend_p > 0.10,
                       "placebo de fecha p > 0,10": r.placebo_fecha_p > 0.10,
                       "Honest DiD M̄ = 1 excluye 0": not (r.honest_M1[0] <= 0 <= r.honest_M1[1]),
                       "permutación de etiquetas p < 0,05": r.perm_p < 0.05}
            fallan = [k for k, v in pruebas.items() if not v]
            if not fallan:
                return "C3", "supera todas las pruebas pre-registradas"
            return "C4", "confirmatoria; no cumple: " + "; ".join(fallan)
        if r.diseno == "D3":
            nota = "; placebo 2021→2023 con asociación (p < 0,10)" if np.isfinite(r.get("placebo_fecha_p", np.nan)) and r.placebo_fecha_p < 0.10 else ""
            return "C4", "descriptivo (sin potencia)" + nota
        etiqueta = "asociación (BH < 0,10)" if r.p_bh < 0.10 else "no detectada (BH ≥ 0,10)"
        extra = []   # pruebas que la exploratoria no supera (revisión F3, hallazgo 4)
        if r.diseno == "D4" and np.isfinite(r.get("F_eff", np.nan)) and r.F_eff < 23.1:
            extra.append(f"instrumento débil (F efectiva {r.F_eff:.1f} < 23,1): p e IC de Anderson-Rubin"
                         + ("" if r.get("AR_acotado") in (True, "True") else "; conjunto de AR no acotado"))
        if isinstance(r.get("rotemberg_fallan"), str) and r.rotemberg_fallan:
            extra.append(f"pretendencias de cuotas con mayor peso de Rotemberg (Holm < 0,10): {r.rotemberg_fallan}")
        if np.isfinite(r.get("pretend_p", np.nan)) and r.pretend_p <= 0.10:
            extra.append(f"pretendencias rechazadas (p {r.pretend_p:.3f})")
        if r.diseno != "D3" and np.isfinite(r.get("placebo_fecha_p", np.nan)) and r.placebo_fecha_p <= 0.10:
            extra.append(f"placebo de fecha rechazado (p {r.placebo_fecha_p:.3f})")
        if r.diseno == "D2" and np.isfinite(r.get("perm_p", np.nan)) and r.perm_p >= 0.05:
            extra.append(f"permutación de la dosis p {r.perm_p:.3f}")
        if r.diseno == "D2" and np.isfinite(r.get("tendencia_p", np.nan)) and r.tendencia_p >= 0.05:
            extra.append("no se mantiene con tendencia lineal por dosis")
        return "C4", "exploratoria: " + etiqueta + ("; " + "; ".join(extra) if extra else "")
    cc = T.apply(capa, axis=1, result_type="expand")
    T["capa"], T["motivo_capa"] = cc[0], cc[1]
    T.to_csv(OUT / "tabla_capas.csv", index=False, float_format="%.5f")

    # tabla de estilo revista
    lin = ["# Tabla V9 · resultados de los diseños D1-D5 (estilo revista)", "",
           "β: diferencia o asociación en log (≈ proporción); no es un efecto causal salvo en C3/C3s. IC 95 %. p: bootstrap salvaje por conglomerados (D1, D2), normal (D3-D5).",
           "p ajustado: Holm en la familia confirmatoria {H1a-renta, H1b-renta}; BH (q = 0,10) en las exploratorias.",
           "Capa según las reglas pre-registradas (docs/v9/hipotesis.md y addendum A1). Sin lenguaje causal por debajo de C3/C3s.", "",
           "| Diseño | Hipótesis | Resultado | β | EE | IC 95 % | p | p ajustado | N | Diagnósticos | Capa |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in T.iterrows():
        padj = r.p_holm if r.confirmatoria else r.p_bh
        diag = []
        if np.isfinite(r.get("pretend_p", np.nan)):
            diag.append(f"pretend. p = {fmt_p(r.pretend_p)}")
        if np.isfinite(r.get("placebo_fecha_p", np.nan)):
            diag.append(f"placebo fecha p = {fmt_p(r.placebo_fecha_p)}")
        if isinstance(r.get("honest_M1"), tuple) and np.isfinite(r.honest_M1[0]):
            diag.append(f"Honest DiD (RR) M̄=1 [{fmt(r.honest_M1[0])}; {fmt(r.honest_M1[1])}], M̄ ruptura {fmt(r.honest_ruptura, 2)}")
        if np.isfinite(r.get("perm_p", np.nan)):
            diag.append(f"permutación p = {fmt_p(r.perm_p)}")
        if np.isfinite(r.get("F_eff", np.nan)):
            diag.append(f"F ef. = {fmt(r.F_eff, 1)}; AR [{fmt(r.AR[0])}; {fmt(r.AR[1])}]; EE AKM {fmt(r.se_akm)}")
        lin.append(f"| {r.diseno} | {r.hipotesis} | {r.resultado} | {fmt(r.beta)} | {fmt(r.se)} | [{fmt(r.ic95_lo)}; {fmt(r.ic95_hi)}] | "
                   f"{fmt_p(r.p)} | {fmt_p(padj)} | {int(r.N)} | {'; '.join(diag) or '—'} | {r.capa}: {r.motivo_capa} |")
    lin += ["", "Fuentes: Incasòl (no redistribuible; solo agregados), EMAL, IDESCAT, GVA, INE, MIVAU, BIS, Eurostat, BCE, "
            "Jarociński-Karadi. Elaboración propia. D6 no se estima (sin edad exacta); D7 es contable (output/v9/d7)."]
    (OUT / "tabla_revista.md").write_text("\n".join(lin) + "\n", encoding="utf-8")

    # comparación con la literatura (docs/v9_prep/literatura.csv)
    lit = pd.read_csv(P.RAIZ / "docs/v9_prep/literatura.csv").set_index("id")
    comp = []
    def b(dis, txt):
        s = T[(T.diseno == dis) & T.resultado.str.contains(txt, regex=False)]
        return s.iloc[0] if len(s) else None
    for dis, txt, ids, nota in (
        ("D1b", "log renta media", ["LB01"], "mismo episodio (Ley 11/2020), mismos datos de fianzas"),
        ("D1a", "log renta media", ["LB03", "LB01"], "Fedea es descriptivo; LB01 es otro régimen"),
        ("D1b", "log contratos", ["LB01"], "LB01: sin caída de la oferta"),
        ("D2", "renta media de contratos nuevos (reapertura", ["LA01"], "unidades no comparables (dosis municipal vs. anuncios por barrio)"),
        ("D4", "IPC de alquiler (principal", ["LA07", "LA09", "LA08"], "réplica con IPC de alquiler provincial (stock), no precios de oferta"),
        ("D5", "alquiler (h = 4)", ["LA25"], "LA25 cualitativo"),
    ):
        r = b(dis, txt)
        if r is None:
            continue
        for i in ids:
            if i in lit.index:
                comp.append({"diseno": dis, "resultado": r.resultado, "beta_v9": r.beta, "ic95": f"[{r.ic95_lo:.3f}; {r.ic95_hi:.3f}]",
                             "capa_v9": r.capa, "literatura_id": i, "cita": lit.loc[i, "cita_completa"][:160],
                             "hallazgo_literatura": str(lit.loc[i, "hallazgo_magnitud"])[:240], "nota": nota})
    pd.DataFrame(comp).to_csv(OUT / "comparacion_literatura.csv", index=False, float_format="%.4f")

    # registro consolidado
    regs = [pd.read_csv(f) for f in sorted(V9.glob("d*/registry.csv")) if f.stat().st_size > 0]
    if regs:
        pd.concat(regs, ignore_index=True).to_csv(V9 / "registry.csv", index=False)
    res = {"rama": "v9/f3", "pregunta": "Capa y p ajustados de los diseños D1-D5", "capa": "por fila",
           "datos": "output/v9/d1..d5", "N": int(len(T)), "metodo": "Holm (confirmatorias) y BH (exploratorias)",
           "estimacion": T[["diseno", "hipotesis", "resultado", "beta", "capa"]].to_dict("records"), "ic95": None,
           "p_ajustado": T[["hipotesis", "p_holm", "p_bh"]].to_dict("records"), "nivel_evidencia": "ver capa",
           "diagnosticos": {"n_C3": int((T.capa == "C3").sum()), "n_C4": int((T.capa == "C4").sum())},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Nada sube de capa por robustez."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    with pd.option_context("display.width", 250, "display.max_colwidth", 80):
        print(T[["diseno", "hipotesis", "resultado", "beta", "p", "p_holm", "p_bh", "capa", "motivo_capa"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
