"""V18 · E5 · escritura de salidas (resultado.json, tabla.csv, informe.md, hechos.json, mde.csv, registro.csv).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. I8 (réplica ciega, B6) queda pendiente.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import _e359_comun as K

DATOS_QUE_FALTAN = (
    "(i) afiliación a la Seguridad Social por provincia y sección o división de la CNAE-93 de 2001 (o la primera disponible) y su serie de los años siguientes, para un Bartik con más ramas "
    "que las cuatro de Eurostat y con variación suficiente entre provincias (el F efectivo del Bartik de cuatro ramas es ≈ 0); (ii) restricciones físicas (pendiente del MDT05, agua, costa) y de "
    "planeamiento (SIU) por provincia o área urbana para E5-R2; (iii) el Atlas de áreas urbanas del MIVAU con valor tasado y obra nueva por área para E5-A2; (iv) afiliación municipal por sección "
    "de la CNAE de 2011-12 en adelante (ficheros STAT/MUNCNAE de la Seguridad Social) para E5-A3; (v) la Red Natura municipal bajo el sellado de V18 para la coprincipal Q4a; (vi) las 11 provincias selladas, que no se leen")


def g4(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (float, np.floating)) and np.isinf(x):
        return "no acotado"
    return f"{x:.4g}"


def escribir(E5, dat, specs, mde_tab, res, ne, a1, fven, reg, B, t0):
    SAL = E5.SALIDA
    SAL.mkdir(parents=True, exist_ok=True)
    REF = E5.REF
    filas = []
    for s in specs:
        base = {"id": s["id"], "rol": s["rol"], "padre": s.get("padre") or "", "nota": s["nota"], "ventana": str(s["cfg"]["ventana"])}
        if s["id"] in ne:
            m = mde_tab.get(s["id"], {})
            base.update({"estado": "NO ESTIMABLE", "motivo": ne[s["id"]], "mde80": m.get("mde80"), "F_eff": m.get("F_eff"), "n": m.get("n"), "G": m.get("G"), "clase": "NO ESTIMABLE"})
        elif s["id"] in res:
            r = res[s["id"]]
            ic = r["ic_webb_ar"]
            base.update({"estado": "estimada", "beta": r["beta"], "se": r["se"], "ic95_webb_ar_lo": ic["lo"], "ic95_webb_ar_hi": ic["hi"], "F_eff": r["F_eff"], "p_webb_ar": r["p_webb_ar"],
                         "p_ar": r["ar"]["p_beta0"], "n": r["n"], "G": r["G"], "clase": "pendiente"})
        filas.append(base)
    for sid in ("E5-R2", "E5-A2", "E5-A3", "E5-P-Q4a"):
        filas.append({"id": sid, "rol": "coprincipal" if "P" in sid else "principal", "estado": "NO ESTIMABLE", "motivo": ne[sid], "clase": "NO ESTIMABLE"})
    if a1:
        filas.append({"id": "E5-A1", "rol": "principal", "estado": "estimada", "beta": a1["psi"], "se": a1["se"], "ic95_webb_ar_lo": a1["ic_webb"][0], "ic95_webb_ar_hi": a1["ic_webb"][1],
                      "p_webb_ar": a1["p_webb"], "n": a1["n"], "G": a1["G"], "mde80": mde_tab["E5-A1"]["mde80"], "clase": "ASOCIACIÓN", "nota": a1["nota"] if "nota" in a1 else ""})
    else:
        filas.append({"id": "E5-A1", "rol": "principal", "estado": "NO ESTIMABLE", "motivo": ne["E5-A1"], "mde80": mde_tab["E5-A1"]["mde80"], "n": mde_tab["E5-A1"]["n"], "clase": "NO ESTIMABLE"})
    tabla = pd.DataFrame(filas)
    tabla.to_csv(SAL / "tabla.csv", index=False)
    pd.DataFrame([{"id": k, **{kk: vv for kk, vv in v.items() if kk not in ("curva", "pesos_sector")}} for k, v in mde_tab.items()]).to_csv(SAL / "mde.csv", index=False)
    reg.flush()
    m1 = mde_tab["E5-R1"]
    clase_r1 = "NO ESTIMABLE" if "E5-R1" in ne else "pendiente"
    esp = {}
    for f in filas:
        d = {k: (None if (isinstance(v, float) and not np.isfinite(v)) else v) for k, v in f.items()}
        d.update({"capa": "C4", "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": f["clase"]})
        if f["estado"] == "NO ESTIMABLE":
            d["datos_que_lo_harian_estimable"] = DATOS_QUE_FALTAN
        esp[f["id"]] = d
    out = {
        "rama": "v18/estimacion/e5", "pregunta": "¿Cuánto responde la oferta de vivienda nueva (iniciadas) al precio, instrumentando el precio con un Bartik de empleo que no lleva construcción, finanzas ni inmobiliarias?",
        "capa": "C4", "datos": "Panel de 39 provincias de entrenamiento (sin las 11 de v6), 2002-2023: viviendas libres iniciadas y valor tasado (MIVAU), deflactor, empleo por rama (Eurostat/INE, 2001 y años siguientes)",
        "N": m1["n"], "metodo": "IV con Bartik de empleo de cuatro ramas en primeras diferencias con efectos de provincia y año; inferencia por provincia (Webb-AR 9.999 + AR exacto); MDE al 80 %; F efectivo de Montiel Olea-Pflueger",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": clase_r1,
        "diagnosticos": {"mde_E5-R1": {k: v for k, v in m1.items() if k != "curva"}, "F_por_ventana": fven, "inv_hhi_sector": m1["inv_hhi_sector"], "pesos_sector": m1["pesos_sector"],
                         "familia_holm": {"m": 0, "nota": "las NO ESTIMABLES salen de la familia antes de ajustar (adenda 1.7); E5-A1 queda fuera por su tope ASOCIACIÓN"},
                         "estado_I8": "pendiente (replicador-ciego, B6)", "b5": "E5-R1 es la estimación propia de E5 para B5 y es NO ESTIMABLE por variación; no hay respaldo (adenda 1.9): entra solo la literatura (Taltavull 0,46-0,87; cota de 0,45 del Banco de España)"},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "diseño de efectos con muestra de entrenamiento; la evaluación sellada es posterior"},
        "notas": ["análisis V18; capa C4; pre-registro interno plan-replicacion-v18", "sin coeficiente publicado: la comprobación previa por MDE (adenda 1.3) deja NO ESTIMABLE por variación", "desviaciones: docs/v18/desviaciones_e3_e5_e9.md (D-E359-2, D-E5-1 a D-E5-4)"],
        "especificaciones": esp,
    }
    K.volcar_json(SAL / "resultado.json", out)
    fuentes = ["MIVAU valor tasado e iniciadas", "Eurostat nama_10r_3empers (INE)", "deflactor del proyecto"]
    H = [K.hecho("V18-E5-R1-MDE80", "E5-R1: efecto mínimo detectable al 80 % de potencia con la variación real del Bartik y del precio", m1["mde80"], None, None, "elasticidad", "2002-2023",
                 f"39 provincias de entrenamiento; N = {m1['n']}; R = {m1['R']}", fuentes, clase_r1,
                 f"Referencia única 0,87 (Taltavull). El MDE supera {g4(m1['curva'][-1][0])} (seis errores típicos de referencia): con el Bartik de cuatro ramas el diseño no alcanza el 80 % de potencia. σ del preperiodo declarada."),
         K.hecho("V18-E5-R1-F", "E5-R1: F efectivo de Montiel Olea-Pflueger de la primera etapa del Bartik de cuatro ramas", m1["F_eff"], None, None, "estadístico F", "2002-2023", "39 provincias", fuentes,
                 clase_r1, "Primera etapa sin fuerza: el Bartik de cuatro ramas no predice el precio real."),
         K.hecho("V18-E5-1HHI", "E5: número efectivo de choques del Bartik (1/HHI de los pesos por rama)", m1["inv_hhi_sector"], None, None, "choques efectivos", "2002-2023", "4 ramas", fuentes, clase_r1,
                 "Menos de 20 por construcción: inferencia principal por provincia con Webb más AR (adenda 1.13).")]
    for ven, v in fven.items():
        H.append(K.hecho(f"V18-E5-R1-F-{ven}", f"E5-R1: F efectivo de la primera etapa en la ventana {ven}", v["F_eff"], None, None, "estadístico F", ven, f"N = {v['n']}", fuentes, clase_r1,
                         "Información de la comprobación previa; no usa el resultado."))
    mA = mde_tab["E5-A1"]
    H.append(K.hecho("V18-E5-A1-MDE80", "E5-A1: efecto mínimo detectable al 80 % de la interacción del instrumento de inmigración con los solares por vivienda", mA["mde80"], None, None,
                     "Δ ln P por punto de Z y por desviación típica de S", "2014-2022", f"N = {mA['n']}", fuentes, "ASOCIACIÓN" if a1 else "NO ESTIMABLE",
                     "Umbral 2δ = 0,10 sin referencia (Anexo B); S es endógena al mercado: tope ASOCIACIÓN."))
    if a1:
        H.append(K.hecho("V18-E5-A1-psi", "E5-A1: coeficiente de la interacción (forma reducida, asociación)", a1["psi"], a1["ic_webb"][0], a1["ic_webb"][1], "Δ ln P por punto de Z y por desviación típica de S",
                         "2014-2022", f"N = {a1['n']}", fuentes, "ASOCIACIÓN", "S_p (solares por vivienda de 2012) es endógena al mercado; IC95 Webb-AR."))
    K.volcar_json(SAL / "hechos.json", H)
    L = []
    L.append("# V18 · E5 Oferta y suelo: elasticidad de la oferta con un Bartik de empleo")
    L.append(f"\n*{K.ROTULO}.* Generado por `python3 src/v18/estimacion/e5_oferta.py` (SEED 20261010, sin red; B = {B}). Clasificaciones provisionales: pendientes de I8. Toda cifra es C4 (EXPLORATORIO). Sin lenguaje causal.\n")
    L.append("## 1. Resumen")
    L.append(f"- **E5-R1: {clase_r1}.** La comprobación previa de variación (adenda 1.3) da un MDE al 80 % {('de ' + g4(m1['mde80'])) if np.isfinite(m1['mde80']) else 'superior a ' + g4(m1['curva'][-1][0]) + ' (seis errores típicos de referencia)'} frente a la referencia única de {REF['v']} (Taltavull, {REF['estado']}); "
             f"el F efectivo de la primera etapa es {g4(m1['F_eff'])} y el número efectivo de choques es {g4(m1['inv_hhi_sector'])} (4 ramas). **No se publica ningún coeficiente de E5-R1** ni de sus variantes (auge, caída, terminadas, pesos, exclusiones).")
    L.append("- F efectivo por ventana (solo primera etapa, sin usar el resultado): " + ", ".join(f"{k}: {g4(v['F_eff'])}" for k, v in fven.items()) + ".")
    if a1:
        L.append(f"- **E5-A1** (ASOCIACIÓN como máximo; fuera de Holm): ψ = {g4(a1['psi'])} (EE {g4(a1['se'])}); IC95 Webb [{g4(a1['ic_webb'][0])}; {g4(a1['ic_webb'][1])}]; p Webb {g4(a1['p_webb'])}; N = {a1['n']}.")
    else:
        L.append(f"- **E5-A1: NO ESTIMABLE por variación** (MDE {g4(mA['mde80'])} frente al umbral 0,10).")
    L.append("- **E5-R2, E5-A2, E5-A3 y la coprincipal P-Q4a: NO ESTIMABLES por datos.**")
    L.append("- B5: E5-R1 es la estimación propia de E5 y no tiene respaldo; E5 no aporta magnitud propia (entra solo la literatura).\n")
    L.append("## 2. Diseño y traslado")
    L.append("- **Original.** Saiz (2010, QJE): elasticidades de oferta por área metropolitana con restricciones geográficas (solo resumen en la ficha). Baum-Snow y Han (2024): choques de demanda laboral (Bartik). Taltavull (2006): "
             "CCAA 1990-2004, elasticidad de los inicios de 0,46 a 0,87.")
    L.append("- **Aquí.** Δ ln iniciadas libres = ε·Δ ln valor tasado real + efectos de provincia y año, con el Bartik B = Σ_k s_pk(2001)·g_kt(sin la provincia) de cuatro ramas (A, B-E, G-J, O-U) de Eurostat/INE, sin construcción, finanzas, "
             "inmobiliarias ni servicios profesionales. 39 provincias de entrenamiento, 2002-2023, sin pesos. Inferencia: Webb-AR y AR exacto por provincia (D-E359-7).")
    L.append("- **Desviaciones:** la afiliación provincial por CNAE de 2001 no está publicada; Eurostat solo da seis ramas a escala NUTS 3 (D-E359-2, D-E5-1). Con cuatro ramas se excluye 1 sector en Rotemberg (D-E5-2).\n")
    L.append("## 3. Comprobación previa de variación (adenda 1.3)\n")
    L.append("| id | n | G | F efectivo | σ preperiodo | ρ | MDE80 | referencia | estimable | 1/HHI |\n|---|---|---|---|---|---|---|---|---|---|")
    for sid, m in mde_tab.items():
        L.append(f"| {sid} | {m['n']} | {m['G']} | {g4(m['F_eff'])} | {g4(m['sigma'])} | {g4(m['rho'])} | {g4(m['mde80'])} | {g4(m['ref'])} | {'sí' if m['estimable'] else 'NO'} | {g4(m.get('inv_hhi_sector'))} |")
    L.append(f"\nMDE por Monte Carlo (R = {m1['R']}, SEED 20261010) con el contraste de Anderson-Rubin agrupado por provincia y la variación real de x y z; σ y ρ del preperiodo 1996-2001 (E5-R1) o 2009-2013 (E5-A1) tras los efectos de provincia y año; "
             "«no vistas» en V15/V16 para esta unidad. Se calculó antes de estimar.\n")
    L.append("## 4. NO ESTIMABLES\n")
    for sid, mot in ne.items():
        L.append(f"- **{sid}**: {mot}.")
    L.append(f"\nQué datos las harían estimables: {DATOS_QUE_FALTAN}.\n")
    L.append("## 5. Lectura y limitaciones\n")
    L.append("- Con un Bartik de cuatro ramas y efectos de provincia y año, la variación del instrumento entre provincias es la de la composición sectorial de 2001 frente a los crecimientos sectoriales nacionales; no predice el precio real (F efectivo ≈ 0). "
             "La respuesta de la oferta no se identifica con estos datos; no se debe leer ninguna elasticidad de este módulo.\n- La referencia de Taltavull (CCAA, 1990-2004) y la cota de 0,45 del Banco de España siguen siendo la única información sobre la elasticidad de la oferta española en V18.\n"
             "- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.\n")
    (SAL / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("informe escrito", flush=True)
