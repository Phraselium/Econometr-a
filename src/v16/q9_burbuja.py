"""V16 fase 6 · Q9: fundamentales y burbuja. Q9-g (GSADF sobre el factor común; APTO con bootstrap salvaje), Q9-c (CS-ARDL/MG/PMG; NO APTO, puntual),
GSADF por provincia (descriptivo) y CIPS (descriptivo). Desviaciones y operacionalización: docs/v16/desviaciones.md, D4. Uso: python3 src/v16/q9_burbuja.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v16 import qc_comun as C  # noqa: E402
from src.v16 import qc_series as S  # noqa: E402

warnings.filterwarnings("ignore")
OUT = C.OUTD / "q9"
B = 499
INI, FIN = pd.Period("2002Q1", "Q"), pd.Period("2026Q2", "Q")


def paneles():
    vt = C.prov_q("base_precio", "valor_tasado")
    rent = C.prov_q("base_alquiler", "ipc_alquiler_indice")
    idx = pd.period_range(INI, FIN, freq="Q")
    vt, rent = vt.reindex(idx), rent.reindex(idx)
    prov = [p for p in vt.columns if p in rent.columns and vt[p].notna().all() and rent[p].notna().all() and (vt[p] > 0).all()]
    return np.log(vt[prov]), np.log(rent[prov]), prov, idx


def factor(R: pd.DataFrame) -> np.ndarray:
    Z = (R - R.mean()) / R.std(ddof=1)
    u, s, vt = np.linalg.svd(Z.to_numpy(), full_matrices=False)
    f = u[:, 0] * s[0]
    if np.corrcoef(f, Z.mean(1))[0, 1] < 0:
        f = -f
    return f, float(s[0] ** 2 / (s ** 2).sum())


def arch_lm(e, q=4):
    from statsmodels.stats.diagnostic import het_arch
    lm, p, *_ = het_arch(e, nlags=q)
    return float(lm), float(p)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lvt, lrent, prov, idx = paneles()
    R = lvt - lrent
    reg = []
    # ------------------------------------------------------------------ Q9-g
    fac, var1 = factor(R)
    g = S.gsadf_boot(fac, B=B, k=1)
    fechas = [str(idx[e]) for e in g["indices_exuberancia"]]
    lm, pa = arch_lm(np.diff(fac))
    mitad = float(np.var(np.diff(fac)[: len(fac) // 2]) / np.var(np.diff(fac)[len(fac) // 2:]))
    g_media = S.gsadf_boot(R.mean(1).to_numpy(), B=B, k=2)
    reg.append({"id": "Q9-g-P", "pregunta": "Q9", "rol": "principal", "especificacion": "GSADF del factor común (1ª CP) de ln(valor tasado/IPC alquiler), 38 provincias, 2002T1-2026T2",
                "muestra": f"{len(prov)} provincias x {len(idx)} trimestres", "n": len(idx), "estimacion": g["stat"], "unidad": "estadístico GSADF",
                "inferencia": f"bootstrap salvaje B={B}: vc95 {g['cv95']:.3f}, p {g['p_bootstrap']:.3f}", "nota": "APTO (conservador si homocedástico)"})
    reg.append({"id": "Q9-g-v1", "pregunta": "Q9", "rol": "robustez", "especificacion": "GSADF de la media de los ln-cocientes (en vez de la 1ª CP)", "muestra": f"{len(idx)} trimestres",
                "n": len(idx), "estimacion": g_media["stat"], "unidad": "estadístico GSADF", "inferencia": f"vc95 {g_media['cv95']:.3f}, p {g_media['p_bootstrap']:.3f}", "nota": "robustez; no entra en el control"})
    # alternativa SERPAVI anual
    vta = np.exp(lvt).groupby(idx.year).mean()
    serp = C.prov_a("base_alquiler", "serpavi_alquiler_m2_mediana")
    pr2 = [p for p in prov if p in serp.columns and serp[p].notna().sum() >= 10]
    ann = np.log(vta[pr2]).reindex(serp.index) - np.log(serp[pr2])
    ann = ann.loc[2011:2024].dropna(axis=1)
    fac2, _ = factor(ann)
    g2 = S.gsadf_boot(fac2, B=B, k=3)
    reg.append({"id": "Q9-g-alt-SERPAVI", "pregunta": "Q9", "rol": "alternativa declarada", "especificacion": "GSADF del factor de ln(valor tasado anual/SERPAVI €/m² provincial), 2011-2024",
                "muestra": f"{ann.shape[1]} provincias x {len(fac2)} años", "n": len(fac2), "estimacion": g2["stat"], "unidad": "estadístico GSADF",
                "inferencia": f"vc95 {g2['cv95']:.3f}, p {g2['p_bootstrap']:.3f}", "nota": "T = 14: sin potencia"})
    # ------------------------------------------------------------------ GSADF por provincia (descriptivo)
    filas = []
    for j, p in enumerate(prov):
        r = S.gsadf_boot(R[p].to_numpy(), B=B, k=100 + j)
        filas.append({"provincia": p, "ratio": "valor_tasado/IPC_alquiler (trimestral)", "T": len(idx), "gsadf": r["stat"], "vc95_bootstrap": r["cv95"],
                      "supera_vc95": bool(r["stat"] > r["cv95"]), "n_fechas_exuberantes": len(r["indices_exuberancia"])})
    for j, p in enumerate(ann.columns):
        r = S.gsadf_boot(ann[p].to_numpy(), B=B, k=300 + j)
        filas.append({"provincia": p, "ratio": "valor_tasado/SERPAVI (anual, T=14)", "T": ann.shape[0], "gsadf": r["stat"], "vc95_bootstrap": r["cv95"],
                      "supera_vc95": bool(r["stat"] > r["cv95"]), "n_fechas_exuberantes": len(r["indices_exuberancia"])})
    prov_df = pd.DataFrame(filas)
    prov_df.to_csv(OUT / "q9_gsadf_provincias.csv", index=False)
    resum_prov = {k: {"n": int(len(v)), "supera_vc95_sin_ajuste_multiple": int(v.supera_vc95.sum())} for k, v in prov_df.groupby("ratio")}
    # ------------------------------------------------------------------ Q9-c panel
    Y, X = lvt.to_numpy(), lrent.to_numpy()
    u = C.nat_q("base_macro", "tipo_hip_real_bde").reindex(idx).to_numpy()
    cs_res = {}
    for p in (1, 2, 3):
        cs_res[("CS-ARDL", p, "sin")] = S.mg_cs(Y, X, p, "CS-ARDL")
        for cu in ("sin", "con"):
            Z = u if cu == "con" else None
            cs_res[("MG", p, cu)] = S.mg_cs(Y, X, p, "MG", Z=Z)
            cs_res[("PMG", p, cu)] = S.pmg(Y, X, p, Z=Z)
    mv = []
    for (est, p, cu), r in cs_res.items():
        th = r.get("theta_media", r.get("theta"))
        principal = (est, p, cu) == ("CS-ARDL", 2, "sin")
        mv.append({"estimador": est, "p": p, "coste_uso": cu, "theta": th, "theta_mediana": r.get("theta_mediana"), "principal": principal})
        reg.append({"id": "Q9-c-P" if principal else f"Q9-c-{est}-p{p}-{cu}", "pregunta": "Q9", "rol": "principal" if principal else "multiverso",
                    "especificacion": f"{est} p={p}, {cu} coste de uso: elasticidad de largo plazo de ln valor tasado frente a ln IPC alquiler", "muestra": f"{len(prov)} provincias x {len(idx)}",
                    "n": int(len(prov) * len(idx)), "estimacion": th, "unidad": "elasticidad (media entre provincias; PMG: común)", "inferencia": "ninguna (csardl NO APTO)",
                    "nota": f"mediana entre provincias {r.get('theta_mediana')}"})
    mvd = pd.DataFrame(mv)
    pr = mvd[mvd.principal].iloc[0]
    nop = mvd[~mvd.principal]
    ci = {"ratio": S.cips(R.to_numpy()), "ln_valor_tasado": S.cips(Y), "ln_ipc_alquiler": S.cips(X)}
    # diagnósticos Q9-c: dependencia transversal (correlación media de residuos de Δ) y heterogeneidad
    dY, dX = np.diff(Y, axis=0), np.diff(X, axis=0)
    cd = np.corrcoef(dY.T)
    rho_med = float((cd.sum() - len(prov)) / (len(prov) * (len(prov) - 1)))
    th_i = np.array(cs_res[("CS-ARDL", 2, "sin")]["theta_i"])
    # ------------------------------------------------------------------ salidas
    estim = {"Q9-g": {"gsadf_factor": g["stat"], "vc95_bootstrap_salvaje": g["cv95"], "p_bootstrap": g["p_bootstrap"], "B": B,
                      "explosivo_al_5pct": bool(g["stat"] > g["cv95"]), "lectura": "explosivo" if g["stat"] > g["cv95"] else "no detectado con esta potencia (no «no hay burbuja»)",
                      "fechas_BSADF_sobre_vc_puntual": fechas, "varianza_explicada_1ªCP": var1, "robustez_media": {"gsadf": g_media["stat"], "vc95": g_media["cv95"], "p": g_media["p_bootstrap"]},
                      "alternativa_SERPAVI_anual": {"gsadf": g2["stat"], "vc95": g2["cv95"], "p": g2["p_bootstrap"], "T": len(fac2), "nota": "sin potencia con T = 14"},
                      "n": len(idx), "unidades": len(prov), "ic95": None},
             "Q9-c": {"theta_principal_CS_ARDL_p2": float(pr.theta), "theta_mediana_entre_provincias": float(pr.theta_mediana), "n_provincias": len(prov), "T": len(idx),
                      "multiverso": {"n": int(len(nop)), "mediana": float(nop.theta.median()), "min": float(nop.theta.min()), "max": float(nop.theta.max()),
                                     "proporcion_mismo_signo": float((np.sign(nop.theta) == np.sign(pr.theta)).mean()),
                                     "por_estimador": {k: float(v.theta.median()) for k, v in mvd.groupby("estimador")}},
                      "ic95": None, "p": None},
             "Q9-gsadf-provincias": resum_prov}
    homo = "heterocedástico (ARCH-LM p < 0,05)" if pa < 0.05 else "sin heterocedasticidad condicional detectada: el bootstrap salvaje es conservador (tamaño 0,017)"
    diag = {"Q9-g": [C.diag("calibración GSADF-factor", "superada", "bootstrap salvaje: tamaño 0,0455 (salto), 0,0455 (estocástica); homocedástico 0,017 (conservador)"),
                     C.diag("heterocedasticidad de Δ factor (ARCH-LM 4)", "reportado", {"LM": lm, "p": pa, "razon_var_1ª_mitad/2ª": mitad, "lectura": homo}),
                     C.diag("potencia", "límite declarado", "el GSADF agregado detecta ρ explosiva con potencia limitada; «no explosivo» = no detectado con esta potencia"),
                     C.diag("raíces unitarias / rupturas / Moran / pretendencias / placebos / Oster", "no aplicable", "prueba de explosividad sobre un factor; no hay coeficiente de tratamiento"),
                     C.diag("multiplicidad", "BY del orquestador", "explosivo exige BH/BY y réplica sellada")],
            "Q9-c": [C.diag("calibración CS-ARDL", "NO APTO", "tamaño 0,1015; cobertura 0,8985: solo estimación puntual"),
                     C.diag("CIPS (descriptivo, sin vc: bootstrap NO APTO)", "reportado", ci),
                     C.diag("dependencia transversal (correlación media de Δln valor tasado)", "reportado", {"rho_medio": rho_med}),
                     C.diag("heterogeneidad de θ_i (CS-ARDL p=2)", "reportado", {"p25": float(np.nanquantile(th_i, .25)), "mediana": float(np.nanmedian(th_i)), "p75": float(np.nanquantile(th_i, .75)),
                                                                                 "n_nan": int(np.isnan(th_i).sum())}),
                     C.diag("Westerlund / Pedroni", "no ejecutado", "no figuran en la especificación de la adenda ni en veredictos.csv")]}
    py = [{"id": "Q9-g", "p": g["p_bootstrap"], "motivo": "gsadf_factor APTO (bootstrap salvaje)"}, {"id": "Q9-c", "p": None, "motivo": "csardl NO APTO"}]
    Q = C.Q
    Q.registro(reg, OUT / "registro.csv")
    nota = ["C4 exploratorio, pendiente de evaluación sellada; sin lenguaje causal.",
            "Ratio con IPC de alquiler en vez de índice de stock de contratos (no existe en entrenamiento): declarado en D4.",
            "Lectura simétrica: «no explosivo» = no detectado con esta potencia, nunca «no hay burbuja».", "Ya visto: GSADF por CCAA de la versión 7.2."]
    r = C.resultado("q9", "Q9: ratio valor tasado / IPC de alquiler: explosividad del factor común (GSADF) y elasticidad de largo plazo provincial (CS-ARDL)",
                    "data/processed/v16/entrenamiento: base_precio (valor tasado), base_alquiler (IPC alquiler, SERPAVI), base_macro (coste de uso)", {"Q9-g": len(idx), "Q9-c": len(prov) * len(idx)},
                    "GSADF con bootstrap salvaje (APTO); CS-ARDL/MG/PMG y CIPS puntuales (NO APTOS)", estim, diag, nota, py,
                    ic95={"Q9-g": None, "Q9-c": None})
    Q.jdump(r, OUT / "resultado.json")
    Q.jdump({"estim": estim, "multiverso_q9c": mv, "cips": ci, "provincias": prov, "factor": fac.tolist()}, OUT / "q9_detalle.json")
    f = C.f
    contra = bool(g["stat"] > g["cv95"])
    if contra:
        (OUT / "contradiccion.md").write_text("# Q9-g: posible contradicción con V7.2\nEl GSADF del factor supera el valor crítico bootstrap al 5 %. La conclusión publicada de V7.2 es «sin exuberancia de los cocientes tras el ajuste múltiple». "
                                              "Es el factor agregado (no el GSADF por CCAA de V7.2) y no ha pasado BY ni réplica sellada; la tendencia del cociente puede producir rechazos del GSADF sin deriva. Se retiene aquí y no va a hechos.json hasta decisión del orquestador (parada D).\n", encoding="utf-8")
    hs = [] if contra else [C.hecho("g", "Q9", "Q9-g: estadístico GSADF del factor común de ln(valor tasado/IPC alquiler) frente a su valor crítico bootstrap del 95 %", g["stat"], g["cv95"], g["cv95"],
                                    "estadístico", "2002T1-2026T2", f"{len(prov)} provincias, factor", "MIVAU; INE", "q9g")]
    hs.append(C.hecho("c", "Q9", "Q9-c: elasticidad de largo plazo del valor tasado respecto al IPC de alquiler (CS-ARDL p=2, media entre provincias; puntual)", float(pr.theta),
                      float(nop.theta.min()), float(nop.theta.max()), "elasticidad", "2002T1-2026T2", f"{len(prov)} provincias", "MIVAU; INE", "q9c"))
    Q.jdump(hs, OUT / "hechos.json")
    md = f"""# Q9 · Fundamentales y burbuja (C4, pendiente de evaluación sellada)

**Capa.** C4 exploratorio. Sin lenguaje causal. Solo Q9-g tiene inferencia APTA (GSADF con bootstrap salvaje). Q9-c, CIPS y el GSADF por provincia son **descriptivos** (sin p-valor ni IC).

## Q9-g · GSADF del factor común (APTO)
<a id="q9g"></a>Ratio: ln(valor tasado provincial) − ln(IPC de alquiler provincial), {len(prov)} provincias, 2002T1-2026T2 (T = {len(idx)}); factor = 1ª componente principal ({f(100 * var1, 1)} % de la varianza).
GSADF = {f(g['stat'], 3)}; valor crítico bootstrap (95 %, B = {B}) = {f(g['cv95'], 3)}; p bootstrap = {f(g['p_bootstrap'], 3)}. Lectura: **{estim['Q9-g']['lectura']}**.
Fechas con BSADF sobre su valor crítico puntual: {', '.join(fechas) if fechas else 'ninguna'}.
Heterocedasticidad (ARCH-LM): LM {f(lm, 2)}, p {f(pa, 3)}: {homo}.
Robustez: media de los ln-cocientes, GSADF {f(g_media['stat'], 3)} (vc {f(g_media['cv95'], 3)}, p {f(g_media['p_bootstrap'], 3)}). Alternativa SERPAVI anual (T = 14, sin potencia): GSADF {f(g2['stat'], 3)} (vc {f(g2['cv95'], 3)}, p {f(g2['p_bootstrap'], 3)}).
Cautela de lectura: el factor tiene una tendencia marcada y el GSADF (con constante, sin tendencia) puede rechazar con tramos de ascenso sostenido sin que sean explosivos en sentido estricto; el bootstrap salvaje impone raíz unitaria sin deriva. Provincias con ambas series completas: {len(prov)} de las 38 de entrenamiento (D4 las daba por 38; el resto carece de valor tasado trimestral).
«No explosivo» significa «no detectado con esta potencia», nunca «no hay burbuja»; «explosivo» exigiría BH/BY y réplica sellada. Ya visto: GSADF por CCAA de V7.2.

## GSADF por provincia (descriptivo)
<a id="q9p"></a>Sin p-valor (herramienta no validada por provincia; potencia casi nula con corrección múltiple). Por encima del valor crítico bootstrap individual, **sin ajuste múltiple**:
{'; '.join(f"{k}: {v['supera_vc95_sin_ajuste_multiple']} de {v['n']}" for k, v in resum_prov.items())}. Detalle en q9_gsadf_provincias.csv.

## Q9-c · elasticidad de largo plazo (NO APTO: puntual)
<a id="q9c"></a>CS-ARDL (p = 2, medias transversales de y y x): θ = {f(float(pr.theta), 3)} (media entre {len(prov)} provincias); mediana entre provincias {f(float(pr.theta_mediana), 3)}.
Multiverso (14 restantes de las 15 ejecutadas): mediana {f(float(nop.theta.median()), 3)}, rango [{f(float(nop.theta.min()), 3)}; {f(float(nop.theta.max()), 3)}], mismo signo {f(float((np.sign(nop.theta) == np.sign(pr.theta)).mean()), 2)}.
Por estimador (mediana): {'; '.join(f'{k} {f(v, 3)}' for k, v in estim['Q9-c']['multiverso']['por_estimador'].items())}. Se ejecutan 15 de las 36 pre-registradas (D4).
CIPS descriptivo (sin vc): ratio {f(ci['ratio']['CIPS'], 2)}; ln valor tasado {f(ci['ln_valor_tasado']['CIPS'], 2)}; ln IPC alquiler {f(ci['ln_ipc_alquiler']['CIPS'], 2)}.
Correlación transversal media de Δln valor tasado: {f(rho_med, 2)} (dependencia fuerte: motivo del uso de medias transversales).

## Regla de hallazgo
Q9-g: (a) p bootstrap sin ajuste = {f(g['p_bootstrap'], 3)}, q pendiente del BY del orquestador; (b) no aplica (prueba de explosividad: sin magnitud); (c) sellada: pendiente. Q9-c: sin p-valor ni IC; (b) no aplica. Resultado: C4 descriptivo.
"""
    (OUT / "informe.md").write_text(md, encoding="utf-8")
    return estim


if __name__ == "__main__":
    e = main()
    print(e["Q9-g"]["gsadf_factor"], e["Q9-g"]["vc95_bootstrap_salvaje"], e["Q9-g"]["p_bootstrap"], e["Q9-c"]["theta_principal_CS_ARDL_p2"], e["Q9-c"]["multiverso"], e["Q9-gsadf-provincias"])
