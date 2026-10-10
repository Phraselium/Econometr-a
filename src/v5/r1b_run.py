"""R1b · punto de entrada: BK-041 (donut), BK-040 (sensibilidad/multiverso v2), BK-023 (GSADF corregido).

Uso: python3 src/v5/r1b_run.py [--solo-ensamblar]   (sin la opción ejecuta los tres módulos, ~9 min, un hilo).
Ensambla output/v5/R1B/{resultado,hechos,fichas_verificador}.json. Sin red; SEED=20261010.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output/v5/R1B"
T = OUT / "tablas"
FECHA = "2026-10-10 (MIVAU valor tasado hasta 2026T2; SERPAVI hasta 2024; IPV/IPC alquiler hasta 2026T2)"


def h(i, ind, v, lo, hi, u, per, cob, fu, capa, fd=FECHA):
    return dict(id=i, indicador=ind, valor=v, min=lo, max=hi, unidad=u, periodo=per, cobertura=cob, fuentes=fu, capa=capa, fecha_dato=fd)


def main():
    if "--solo-ensamblar" not in sys.argv:
        for m in ("r1b_donut", "r1b_sens", "r1b_gsadf"):
            subprocess.run([sys.executable, str(RAIZ / f"src/v5/{m}.py")], check=True)
    dn = json.load(open(T / "donut_resumen.json"))
    sm = json.load(open(T / "sens_multiverso.json"))
    gs = pd.read_csv(T / "gsadf_corregido.csv")
    tam = json.load(open(T / "gsadf_tamano.json"))
    mv = pd.read_csv(T / "donut_multiverso.csv")
    P = dn["principal"]
    H = []
    # ---- donut
    for fu, nom in (("tasado", "valor tasado (>25.000 hab.)"), ("serpavi_VC", "alquiler SERPAVI VC")):
        r = P[fu]
        H.append(h(f"R1B-D-{fu}", f"Cambio de pendiente del gradiente de crecimiento anual con la distancia al centro (2019-2024 menos 2015-2019), {nom}, capital + 25 km",
                   round(r["dif"], 3), round(r["dif"] - 1.96 * r["ee"], 3), round(r["dif"] + 1.96 * r["ee"], 3), "pp de crecimiento anual por cada 10 km",
                   "2015-2019 frente a 2019-2024", f"{r['areas']} áreas, {r['n']} municipios", [nom], "C4"))
        x = mv[mv.fuente == fu]
        H.append(h(f"R1B-D-{fu}-mv", f"Proporción de especificaciones con cambio de pendiente positivo (periferia gana frente al centro), {nom}",
                   round(float((x.dif > 0).mean()), 3), round(float((x.dif > 0).mean()), 3), round(float((x.dif > 0).mean()), 3), "proporción", "2015-2024",
                   f"{len(x)} especificaciones", [nom], "C4"))
        H.append(h(f"R1B-D-{fu}-holm", f"Proporción de especificaciones significativas tras Holm, {nom}", round(float((x.p_holm < .05).mean()), 3), 0, 1,
                   "proporción", "2015-2024", f"{len(x)} especificaciones", [nom], "C4"))
    # ---- sensibilidad
    s = sm["BI"]["sensibilidad"]
    H.append(h("R1B-S-BI-delta", "Oster δ (β*=0, Rmax=1,3·R²) de la forma reducida alquiler~instrumento Bartik, BI", round(s["RF_alq_z"]["delta_oster"], 2),
               round(s["OLS_alq_x"]["delta_oster"], 2), round(s["RF_alq_z"]["delta_oster"], 2), "razón δ", "2009-2021", "49 provincias, N=621", ["INE/MIVAU vía data/processed"], "C4"))
    H.append(h("R1B-S-BI-RV", "Valor de robustez Cinelli-Hazlett RV (q=1) de la forma reducida BI, gl=G-1", round(s["RF_alq_z"]["RV"], 3), round(s["RF_alq_z"]["RV_alpha"], 3),
               round(s["RF_alq_z"]["RV"], 3), "R² parcial", "2009-2021", "49 provincias", ["INE/MIVAU vía data/processed"], "C4"))
    mb = sm["BI"]["multiverso"]
    H.append(h("R1B-S-BI-mv", "BI: proporción de especificaciones con el mismo signo que la base (alquiler)", round(mb["prop_mismo_signo"], 3), round(mb["prop_mismo_signo_sig_holm"], 3),
               round(mb["prop_mismo_signo_sig_nominal"], 3), "proporción (min = significativas tras Holm; max = significativas nominales)", "2009-2021", f"{mb['n_spec']} especificaciones", ["INE/MIVAU vía data/processed"], "C4"))
    b5 = sm["BP"]["multiverso_H5"]["sdid"]
    H.append(h("R1B-S-BP-mv", "BP H5 SDiD: proporción de especificaciones con el mismo signo que la base (positivo)", round(b5["prop_mismo_signo"], 3), round(b5["prop_mismo_signo_sig_holm"], 3),
               round(b5["prop_mismo_signo_sig_nominal"], 3), "proporción (min = Holm; B=200 permutaciones, resolución limitada)", "2012Q1-2022Q1", f"{b5['n_spec']} especificaciones", ["INE IPC alquiler vía data/processed"], "C4"))
    h6 = sm["BP"]["sens_H6_publicado"]
    H.append(h("R1B-S-BP-H6-RV", "BP H6 (resultado publicado, muestra sellada): RV aproximado desde τ y EE de placebo", round(h6["RV"], 3), round(h6["RV_alpha"], 3), round(h6["RV"], 3),
               "R² parcial (aprox.)", "2024Q3-2026Q2", "4 tratadas, 40 donantes", ["output/v2/BP/h6_sellado.json"], "C4"))
    # ---- GSADF
    nf = gs[gs.familia == "fundamentales"]
    H.append(h("R1B-G-tam", "Tamaño empírico del GSADF con vc iid cuando Δy es AR(1) con phi=0,5 (nominal 5 %)", tam["phi0.5"]["rechazo_vc_iid"], tam["phi0.0"]["rechazo_vc_iid"],
               tam["phi0.5"]["rechazo_vc_iid"], "% (fracción)", "simulación T=78, R=200", "Monte Carlo", ["simulación propia"], "C4", "2026-10-10"))
    H.append(h("R1B-G-tam-corr", "Tamaño empírico con vc por bootstrap de AR(p) estimado, phi=0,5", tam["phi0.5"]["rechazo_bootstrap_AR"], tam["phi0.0"]["rechazo_bootstrap_AR"],
               tam["phi0.5"]["rechazo_bootstrap_AR"], "% (fracción)", "simulación T=78, R=200", "Monte Carlo", ["simulación propia"], "C4", "2026-10-10"))
    for r in nf.itertuples():
        if r.territorio == "Nacional":
            H.append(h(f"R1B-G-{r.Index}", f"GSADF (vc bootstrap AR): {r.medida}", round(r.gsadf, 3), round(r.cv95_corr, 3), round(r.gsadf, 3),
                       f"estadístico (min = vc 95 %; p={r.p_corr:.3f}; BH familia={r.p_bh:.3f})", f"{r.ini}-{r.fin}", "Nacional", ["INE IPV", "MIVAU tasado", "INE renta", "BdE tipo hipotecario"], "C4"))
    cc = gs[gs.familia == "ccaa"]
    H.append(h("R1B-G-ccaa", "CCAA-medida con exuberancia tras BH (vc corregidos) de 34", int(cc.exuberancia_bh05.sum()), int(cc.exuberancia_bh05.sum()), int((cc.p_corr < .05).sum()),
               "series (max = significativas sin ajuste)", "2007Q1-2026Q2", "17 CCAA x 2 medidas", ["INE IPV", "MIVAU tasado", "INE IPC alquiler"], "C4"))
    (OUT / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1))
    # ---- ficha
    pa = nf[nf.territorio == "Nacional"]
    sup = pa[pa.medida.str.startswith("precio/alquiler")]
    ficha = {
        "id": "R1B-V1", "tema": "Burbuja de precios (revisión con tamaño corregido y fundamentales)",
        "enunciado": "Hay una burbuja en el precio de la vivienda en España.", "capa": "C4",
        "magnitud": (f"Con valores críticos por bootstrap de AR(p) estimado (tamaño comprobado: {100 * tam['phi0.5']['rechazo_bootstrap_AR']:.1f} % con phi=0,5 frente a "
                     f"{100 * tam['phi0.5']['rechazo_vc_iid']:.1f} % con vc iid), el cociente precio/alquiler muestra exuberancia sin ajustar (p<0,05) en "
                     f"{int((sup.p_corr < .05).sum())} de 2 medidas nacionales, pero ninguna sobrevive a BH en la familia de 8 cocientes (BH {sup.p_bh.min():.3f}-{sup.p_bh.max():.3f}); "
                     f"episodios fechados sin ajuste múltiple (ninguno sobrevive a BH): {'; '.join(sup.episodios_corregidos.dropna())}. Precio frente a valor de descuento del alquiler con tipos (prima de 3 pp; sensibilidad 2 y 4 pp) y frente a la cuota hipotecaria constante sobre renta: "
                     f"sin exuberancia (p {nf[nf.medida.str.contains('frente a valor')].p_corr.min():.2f}-{nf[nf.medida.str.contains('frente a valor')].p_corr.max():.2f}). "
                     f"CCAA con exuberancia tras BH: {int(cc.exuberancia_bh05.sum())} de 34 series (M7 con vc iid: {int((cc.p_M7 < .05).sum())} de 34 con p<0,05 sin ajuste; con vc corregidos: {int((cc.p_corr < .05).sum())})."),
        "intervalo": "—", "cota": "—", "literatura": "Phillips, Shi y Yu (2015), GSADF: NO VERIFICADA (DOI y cuartil no comprobados sin red).",
        "veredicto": "ANALIZADA, NO CONCLUYENTE",
        "regla": ("Una exuberancia estadística no es una burbuja: el test detecta crecimiento explosivo de una serie o de un cociente, no la causa (renta, tipos, oferta, expectativas) ni la sobrevaloración. "
                  "Con capa C4 el veredicto no puede ser RESPALDADA ni CONTRADICHA. Los cocientes frente a fundamentales con tipos no muestran exuberancia, lo que no equivale a ausencia de sobrevaloración: el valor fundamental usado es una referencia simple con supuestos propios."),
        "limites": ("Muestra 2007Q1-2026Q2 (T=78) corta para el ciclo; ADF con un rezago; el valor de descuento fija g=2 % y una prima de 3 pp (sensibilidad 2 y 4 pp) y usa el tipo medio de nuevas hipotecas "
                    f"{'(con tramos interpolados: solo robustez)' if bool(nf.tipo_hip_interpolada.any()) else ''}; renta del hogar nacional; sin renta por CCAA; el tamaño con bootstrap queda en 2-4 % (por debajo del nominal) con R=200."),
        "evidencia": ["output/v5/R1B/tablas/gsadf_corregido.csv", "output/v5/R1B/tablas/gsadf_tamano.json", "output/v4/M7/tablas/gsadf_resultados.csv"]}
    (OUT / "fichas_verificador.json").write_text(json.dumps([ficha], ensure_ascii=False, indent=1))
    # ---- resultado
    res = {
        "rama": "R1b",
        "pregunta": "BK-041 efecto donut post-COVID; BK-040 sensibilidad/multiverso de diseños v2 (BI, BP); BK-023 GSADF con tamaño corregido y fundamentales.",
        "capa": "C4",
        "datos": "MIVAU valor tasado municipal (>25k hab., 306 municipios, hasta 2026T2); SERPAVI municipal VC (2011-2024); centroides de secciones INE 2021; Censo 2021; panel_prov_a/q (v2, entrenamiento); nacional_q_v2 (holdout.load_full, registrado); panel_ccaa_q",
        "N": {"donut_tasado_principal": P["tasado"]["n"], "donut_serpavi_principal": P["serpavi_VC"]["n"], "BI": 621, "BP_tratadas": 4, "BP_donantes": 45, "gsadf_T": 78, "gsadf_series": int(len(gs))},
        "metodo": ("Donut: diferencia de pendientes de Δ(crecimiento anual) sobre distancia con FE de área, EE agrupados por área; multiverso 320 especificaciones (fuente, centro, radio, periodo, forma, centro incluido); Holm. "
                   "Sensibilidad: Oster (Rmax=1,3·R²) y Cinelli-Hazlett (RV, RV_alfa; fórmula propia en src/v5/r1b_sens.py); multiverso BI (160) y BP H5 (216); Holm. "
                   "GSADF: vc por bootstrap recursivo de residuos con AR(p) por BIC bajo raíz unitaria, 499 réplicas; BH y Holm por familia; tamaño por Monte Carlo."),
        "estimacion": {"donut": dn["resumen"], "donut_principal": {k: {"dif": v["dif"], "ee": v["ee"], "p": v["p"], "p_holm_320": v["p_holm"], "areas": v["areas"]} for k, v in P.items()},
                       "donut_placebo_tasado": dn["placebo"], "sensibilidad_BI": sm["BI"]["sensibilidad"], "multiverso_BI": sm["BI"]["multiverso"], "multiverso_BI_dif": sm["BI"]["multiverso_dif"],
                       "sens_BP_H5_colapsada": sm["BP"]["sens_H5_colapsada"], "sens_BP_H6_publicado": sm["BP"]["sens_H6_publicado"], "multiverso_BP_H5": sm["BP"]["multiverso_H5"],
                       "gsadf_tamano": tam},
        "ic95": None,
        "p_ajustado": {"donut": "Holm sobre 320 especificaciones: ninguna significativa; ver tablas/donut_multiverso.csv", "gsadf": "BH/Holm por familia en tablas/gsadf_corregido.csv"},
        "nivel_evidencia": "EXPLORATORIO (C4)",
        "diagnosticos": {"donut_cobertura": dn["cobertura"], "BP_multiverso_nota": "B=200 permutaciones por especificación: el p mínimo es ~0,005, así que Holm sobre 72 pruebas no puede rechazar por resolución; la proporción Holm es un límite inferior",
                         "BI_nota": "Oster y RV sobre la forma reducida y el MCO (la 2SLS no tiene R² propio); RV con gl=G-1",
                         "BO_H4": sm["BO_H4"]},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": ("Sin lenguaje causal. Donut: el Atlas de Áreas Urbanas no está en el repositorio y mivau.gob.es respondió 403 desde el proxy (2026-10-10); áreas = capital provincial (o mayor parque de viviendas del Censo 2021) y radio declarado; "
                  "centroides como media de cajas de secciones. El tasado cubre solo municipios >25k, así que la periferia lejana no se observa. Una exuberancia estadística no es una burbuja. "
                  "H6 se evalúa solo con su resultado publicado (muestra sellada, sin re-acceso). nacional_q_v2 leído vía holdout.load_full (registrado).")}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    # registro único
    regs = [pd.read_csv(p) for p in (OUT / "registro_donut.csv", OUT / "registro_sens.csv", OUT / "registro_gsadf.csv")]
    pd.concat(regs, ignore_index=True).to_csv(OUT / "registro.csv", index=False)
    print("ok", len(H), "hechos")


if __name__ == "__main__":
    main()
