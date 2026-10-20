"""V18 · E2 · salidas: resultado.json (formato de CLAUDE.md + clasificacion_v18), hechos.json (cifras V18-E2-*) e informe.md.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin lenguaje causal en cifras (check_v18) ni en el informe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e2_diseno as DS  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
FUENTES = ["Incasòl, fianzas (Socrata qww9-bvhh, descarga 2026-10-14)", "BOE-A-2020-11363 (Ley 11/2020 de Cataluña) y cataluna_contencion_rentas_v3.csv (v3)",
           "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"]
I8 = "Clasificación provisional: falta I8 (réplica ciega, B6)"
FRASE_K9 = ("Entre 2020T4 y 2022T1, la renta media de los contratos nuevos registrados en el Incasòl en los 49 municipios sujetos a la Ley 11/2020 (sin Barcelona ciudad) se situó, "
            "respecto a 2019, un 3,8 % por debajo (log −0,038; IC95 −0,051 a −0,026) de la de municipios catalanes no regulados con mercado tensionado. La diferencia no es estable: "
            "es máxima en 2021T1 (−0,058), se reduce de forma gradual hasta no distinguirse de cero en 2022T1, antes de la STC 37/2022, sin cambio posterior, y baja a −0,023 "
            "(IC95 −0,045 a −0,001) cuando se permiten trayectorias trimestrales distintas según el tamaño del municipio. Con estos datos no se separa la parte asociada a la norma "
            "de un choque transitorio de la COVID-19 en los municipios grandes ni de un cambio en la composición de los contratos registrados, y la sensibilidad a tendencias "
            "diferenciales (Honest DiD con M̄ ≥ 0,5) no es evaluable con la potencia disponible. La magnitud coincide con la de Jofre-Monseny et al. (2023), que usan el mismo "
            "registro y el mismo episodio. Clase V18: SUGESTIVO; capa del proyecto C4.")


def f(x, n=4):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{n}f}"


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in df.itertuples(index=False):
        out.append("| " + " | ".join("—" if (isinstance(v, float) and not np.isfinite(v)) or v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def escribir(OUT: Path, d: dict, est: pd.DataFrame, tab: pd.DataFrame, diag: dict, clasif: dict, segundos: float) -> None:
    r1, r1c = diag["E2-R1"], diag["E2-R1c"]
    t = tab.set_index("id")
    cls = {k: v["clase"] for k, v in clasif.items()}
    ref = DS.ESPEC["E2-R1"]["ref"]
    razon = t.loc["E2-R1", "coef"] / (-ref)
    mde_r1, mde_r1c = float(est.set_index("id").loc["E2-R1", "mde80"]), float(est.set_index("id").loc["E2-R1c", "mde80"])

    # ---------------------------------------------------------------- hechos
    H = []
    cob_r1 = (f"{int(t.loc['E2-R1', 'n_tratados'])} municipios regulados por la Ley 11/2020 y {int(t.loc['E2-R1', 'n_controles'])} controles de Cataluña, "
              "panel trimestral equilibrado 2019T1-2022T1 sin Barcelona ciudad; sin los municipios sellados en v6, V15 y V16")
    nota_r1 = (f"Coeficiente de Reg × Post con efectos fijos de municipio y de trimestre; inferencia de Webb por municipio (9.999 réplicas, p con valor crítico corregido "
               f"por el tamaño de Monte Carlo 0,071), p tras Holm {f(t.loc['E2-R1', 'p_holm'], 5)}. Razón con la referencia de Jofre-Monseny et al. (2023, −0,045): {f(razon, 2)} "
               f"(etiqueta coherente, razón en [1/3; 3]). Pretendencias p = {f(r1['evento']['p_pretend'], 3)}; reversión en 2022T2-2023T4: {f(r1['reversion']['coef_reversion'])}. "
               f"Tope SUGESTIVO por corrección de un fallo conocido de V9-D1b. Lectura: asociación estimada. {I8}. "
               f"Frase de limitación (K9, obligatoria al difundir la cifra): «{FRASE_K9}»")
    H.append(K.hecho("V18-E2-R1", "Coeficiente Reg × Post sobre el log de la renta media de contratos nuevos de alquiler (Ley 11/2020, Cataluña, Incasòl)", t.loc["E2-R1", "coef"],
                     t.loc["E2-R1", "ic95_lo"], t.loc["E2-R1", "ic95_hi"], "log (diferencia entre regulados y controles, posterior frente a previo)", "2019T1-2022T1",
                     cob_r1, FUENTES, cls["E2-R1"]["clase"], nota_r1))
    H.append(K.hecho("V18-E2-R1-REV", "Coeficiente de la reversión en 2022T2-2023T4 (tras la STC 37/2022) sobre el log de la renta media, municipios regulados frente a controles",
                     r1["reversion"]["coef_reversion"], r1["reversion"]["coef_reversion"] - 1.96 * r1["reversion"]["se_reversion"],
                     r1["reversion"]["coef_reversion"] + 1.96 * r1["reversion"]["se_reversion"], "log (nivel posterior a la norma frente a previo)", "2019T1-2023T4",
                     f"{r1['reversion']['n_tr']} regulados y {r1['reversion']['n_co']} controles, panel 2019T1-2023T4", FUENTES, cls["E2-R1"]["clase"],
                     f"Prueba de reversión de la adenda (AD-E2-R1); p = {f(r1['reversion']['p_reversion'], 3)}; no persiste una diferencia de la mitad del coeficiente de la vigencia, "
                     f"por lo que no se aplica el tope. IC95 con EE agrupado por municipio. {I8}."))
    nota_c = (f"Coeficiente de Reg × Post sobre log(contratos/población × 1.000); p con Webb {f(t.loc['E2-R1c', 'p_webb'], 3)}; p tras Holm {f(t.loc['E2-R1c', 'p_holm'], 3)}; "
              f"TOST con δ = 0,05: intervalo al 90 % ({f(clasif['E2-R1c']['info']['tost']['ic90'][0])}; {f(clasif['E2-R1c']['info']['tost']['ic90'][1])}) "
              f"{'dentro' if clasif['E2-R1c']['info']['tost']['equivalente'] else 'no dentro'} de ±0,05. Sin significación y con el placebo de fecha significativo (p = {f(r1c['placebo_fecha']['p'], 4)}) "
              "y una diferencia que persiste tras la STC: no supera I1-I5 y no existe la clase SUGESTIVO sin significación (K7): ASOCIACIÓN. "
              f"No se descarta el desvío a la temporada o a no depositar la fianza (variante con hogares inquilinos del Censo 2021 en la sección de robustez B6, a posteriori). {I8}.")
    H.append(K.hecho("V18-E2-R1c", "Coeficiente Reg × Post sobre el log de contratos nuevos por 1.000 habitantes (Ley 11/2020, Cataluña, Incasòl)", t.loc["E2-R1c", "coef"],
                     t.loc["E2-R1c", "ic95_lo"], t.loc["E2-R1c", "ic95_hi"], "log (diferencia entre regulados y controles, posterior frente a previo)", "2019T1-2022T1",
                     f"{int(t.loc['E2-R1c', 'n_tratados'])} regulados y {int(t.loc['E2-R1c', 'n_controles'])} controles, panel trimestral equilibrado", FUENTES, cls["E2-R1c"]["clase"], nota_c))
    ne = est.set_index("id")
    for ident, texto in (("E2-A1", "MDE al 80 % de potencia de la ampliación a las zonas tensionadas de 2024 de Cataluña (log de la renta media)"),
                         ("E2-A4", "MDE al 80 % de potencia del desbordamiento a municipios vecinos (log de la renta media)")):
        e = ne.loc[ident]
        H.append(K.hecho(f"V18-{ident}", texto, e.mde80, None, None, "log (MDE80)", "2019T1-2026T1" if ident == "E2-A1" else "2019T1-2022T1",
                         f"{int(e.n_tratados)} tratados y {int(e.n_controles)} controles", FUENTES, "NO ESTIMABLE",
                         f"NO ESTIMABLE por variación: MDE80 {f(e.mde80)} mayor que el umbral {f(e.umbral)} ({e.referencia}); no se estima y sale de la familia de Holm. "
                         "Sin resultado que difundir (la ampliación A1 estaba marcada provisional). Lo haría estimable: más trimestres posteriores a 2024 o más municipios nunca tratados."))
    H.append(K.hecho("V18-E2-A2", "Zonas tensionadas fuera de Cataluña (País Vasco, EMAL): recuento de municipios tratados con datos", float(ne.loc["E2-A2", "n_tratados"]), None, None,
                     "municipios", "2016T1-2025T4", ne.loc["E2-A2", "minimo_datos"], FUENTES + ["EMAL (Gobierno Vasco)"], "NO ESTIMABLE",
                     "NO ESTIMABLE: no alcanza el mínimo de 10 municipios tratados no sellados con 3 trimestres posteriores por cohorte; Bizkaia y Gipuzkoa están sellados en su mayoría. "
                     "Lo haría estimable: más trimestres de EMAL tras 2025 y los municipios sellados en la evaluación diferida."))
    H.append(K.hecho("V18-E2-A3", "Desplazamiento a la venta: compraventas municipales por 1.000 habitantes, controles disponibles en la serie municipal de MIVAU", float(ne.loc["E2-A3", "n_controles"]),
                     None, None, "municipios de control", "2016-2022", ne.loc["E2-A3", "minimo_datos"], FUENTES + ["MIVAU (compraventas por municipio >25.000 habitantes)"], "NO ESTIMABLE",
                     "NO ESTIMABLE: la serie municipal de MIVAU solo trae municipios grandes y casi todos los catalanes están regulados (2 controles). Lo haría estimable: compraventas "
                     "municipales de todos los municipios (Registradores o Notariado, tareas_autor punto 3)."))
    for ident, texto in (("E2-R2", "Monràs y García-Montalvo: PPML de contratos por tramo de renta"), ("E2-R2s", "Proporción de contratos en tramos superiores"),
                         ("E2-R2-X1", "Precio en exceso sobre el de referencia y composición"), ("E2-A5", "Desplazamiento al alquiler de temporada")):
        H.append(K.hecho(f"V18-{ident}", texto, None, None, None, "sin cifra", "—", "sin datos", ["docs/v18/tareas_autor.md, punto 4"], "NO ESTIMABLE",
                         f"NO ESTIMABLE: {tab.set_index('id').loc[ident, 'nota']}."))
    K.volcar_json(OUT / "hechos.json", H)

    # ---------------------------------------------------------------- resultado.json
    est_d = {k: float(v) for k, v in t[t.estado == "estimada"].coef.dropna().items()}
    res = {
        "rama": "v18/estimacion/e2", "pregunta": "¿Se asocian la Ley 11/2020 (topes al alquiler en Cataluña) y las zonas tensionadas de 2024 con la renta y el número de contratos nuevos de alquiler?",
        "capa": "C4", "datos": "Incasòl trimestral 2019T1-2026T1 y anual 2007-2025 por municipio; lista de la Ley 11/2020; sepe, padrón e idescat como controles; sin unidades selladas (v6, V15, V16)",
        "N": {"E2-R1": int(t.loc["E2-R1", "n_tratados"] + t.loc["E2-R1", "n_controles"]), "E2-R1c": int(t.loc["E2-R1c", "n_tratados"] + t.loc["E2-R1c", "n_controles"])},
        "metodo": "TWFE con efectos fijos de municipio y trimestre, CR1 y wild cluster bootstrap de Webb por municipio, aleatorización, Conley 10 km, estudio de eventos, Honest DiD (M̄ = 0 informativo), CS para la coprincipal V9-D1b",
        "estimacion": {"E2-R1": float(t.loc["E2-R1", "coef"]), "E2-R1c": float(t.loc["E2-R1c", "coef"]), "E2-P-D1b": float(t.loc["E2-P-D1b", "coef"]),
                       "E2-P-D1b-c": float(t.loc["E2-P-D1b-c", "coef"]), "todas": est_d},
        "ic95": {k: [float(t.loc[k, "ic95_lo"]), float(t.loc[k, "ic95_hi"])] for k in ("E2-R1", "E2-R1c", "E2-P-D1b", "E2-P-D1b-c")},
        "p_ajustado": {k: float(t.loc[k, "p_holm"]) for k in ("E2-R1", "E2-R1c", "E2-P-D1b", "E2-P-D1b-c")},
        "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": K.clase_corta(cls["E2-R1"]["clase"]),
        "clasificaciones": {k: v["clase"] for k, v in cls.items()} | {k: "NO ESTIMABLE" for k in ("E2-A1", "E2-A2", "E2-A3", "E2-A4", "E2-R2", "E2-R2s", "E2-R2-X1", "E2-A5")},
        "diagnosticos": {
            "estimabilidad": est.to_dict("records"),
            "E2-R1": {"pretendencias_p": r1["evento"]["p_pretend"], "pendiente_detectable_80": r1["evento"]["pendiente_detectable"], "sesgo_implicado_post": r1["evento"]["sesgo_post"],
                      "placebo_fecha_2017_anual": r1["placebo_fecha"], "placebo_resultado": "población de 65+ por municipio y año: sin dato; renta IRPF: sin municipios catalanes",
                      "reversion": r1["reversion"], "honest": r1["honest"], "honest_anual_v8": r1.get("honest_anual_v8"), "moran_residuos": r1["moran"], "razon_con_referencia": razon, "mde80": mde_r1,
                      "inferencia": {"p_webb": float(t.loc["E2-R1", "p_webb"]), "p_webb_conglomerado_espacial": float(t.loc["E2-R1", "p_webb_conglom"]),
                                     "p_aleatorizacion": float(t.loc["E2-R1", "p_aleat"]), "p_aleatorizacion_conglomerado": float(t.loc["E2-R1", "p_aleat_conglom"]),
                                     "se_conley_10km": float(t.loc["E2-R1", "se_conley10"]), "p_driscoll_kraay_no_fiable": float(t.loc["E2-R1", "p_dk_no_fiable"])},
                      "clasificacion_razones": cls["E2-R1"]["razones"]},
            "E2-R1c": {"pretendencias_p": r1c["evento"]["p_pretend"], "placebo_fecha_2017_anual": r1c["placebo_fecha"], "reversion": r1c["reversion"], "mde80": mde_r1c,
                       "clasificacion_razones": cls["E2-R1c"]["razones"]},
        },
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no aplica: diseño de evaluación (diferencias en diferencias), no predictivo; la evaluación sellada diferida de la adenda 1.11 no incluye a E2-R1 (episodio histórico)"},
        "notas": "Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. " + I8 + ". Ninguna estimación IDENTIFICADO: sin contradicción con lo publicado (parada G no activada).",
    }
    K.volcar_json(OUT / "resultado.json", res)

    # ---------------------------------------------------------------- informe.md
    e_tab = est[["id", "n_tratados", "n_controles", "minimo_datos", "mde80", "umbral", "estimable"]].copy()
    e_tab["mde80"] = e_tab.mde80.map(lambda x: f(x))
    e_tab["umbral"] = e_tab.umbral.map(lambda x: f(x))
    e_tab["minimo_datos"] = e_tab.minimo_datos.str.replace(r"\{[^}]*\}", "…", regex=True).str.slice(0, 110)
    base_cols = ["id", "n_tratados", "n_controles", "coef", "ic95_lo", "ic95_hi", "p_webb", "p_i7", "p_holm", "clase"]
    prin = tab[tab.id.isin(["E2-R1", "E2-R1c", "E2-P-D1b", "E2-P-D1b-c"])][base_cols].copy()
    for c in ("coef", "ic95_lo", "ic95_hi"):
        prin[c] = prin[c].map(lambda x: f(x))
    for c in ("p_webb", "p_i7", "p_holm"):
        prin[c] = prin[c].map(lambda x: f(x, 4))
    prin["n_tratados"] = prin.n_tratados.astype(int)
    prin["n_controles"] = prin.n_controles.astype(int)
    var = tab[(tab.rol.isin(["variante", "holgura"])) & (tab.estado.str.startswith(("estimada", "coincide", "NO ESTIMABLE"))) & tab.id.str.startswith(("E2-R1", "E2-R1c"))]
    var = var[["id", "nota", "estado", "n_tratados", "n_controles", "coef", "ic95_lo", "ic95_hi", "p_webb", "q_by"]].copy()
    for c in ("coef", "ic95_lo", "ic95_hi"):
        var[c] = var[c].map(lambda x: f(x))
    for c in ("p_webb", "q_by"):
        var[c] = var[c].map(lambda x: f(x, 4))
    var["nota"] = var.nota.str.slice(0, 90)
    var["n_tratados"] = var.n_tratados.map(lambda x: "—" if x != x or x is None else int(x))
    var["n_controles"] = var.n_controles.map(lambda x: "—" if x != x or x is None else int(x))
    ev = r1["evento"]["tabla"].copy()
    ev["periodo"] = ev.k.map(lambda k: DS.D.PER13[int(k)])
    ev["coef"] = ev.coef.map(lambda x: f(x))
    ev["se"] = ev.se.map(lambda x: f(x))
    hon = pd.DataFrame([{"M̄": h["Mbar"], "IC95": f"({f(h['ic95'][0])}; {f(h['ic95'][1])})", "excluye 0": h["excluye_cero"], "lectura": h["lectura"]} for h in r1["honest"]])
    vr = tab[(tab.rol == "variante") & tab.id.str.startswith("E2-R1-") & (tab.estado == "estimada")]
    ic0 = r1["r"]["ic_cr1"]
    no_sol = [i for i, lo, hi in zip(vr.id, vr.ic95_lo, vr.ic95_hi) if not (lo <= ic0[1] and hi >= ic0[0])]
    mismo = int((np.sign(vr.coef) == np.sign(t.loc["E2-R1", "coef"])).sum())
    txt_rob = (f"el signo coincide con el de la principal en {mismo} de {len(vr)} variantes estimadas; "
               + (f"el IC95 (CR1) no solapa con el de la principal en: {', '.join(no_sol)}." if no_sol else "todos los IC95 solapan con el de la principal."))
    hv8 = r1.get("honest_anual_v8") or []
    honest_v8 = "; ".join(f"M̄ = {h['Mbar']:g}: ({f(h['ic95'][0])}; {f(h['ic95'][1])})" for h in hv8) if hv8 else "no disponible"
    txt = f"""# V18 · E2 · Topes al alquiler (Ley 11/2020 de Cataluña, Incasòl)

**Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Nivel de evidencia EXPLORATORIO. La clasificación V18 va en el campo `clasificacion_v18` y no cambia la capa.
Clasificaciones provisionales: falta I8 (réplica ciega, B6). Código: `src/v18/estimacion/e2_topes.py` (+ `e2_datos.py`, `e2_diseno.py`, `e2_estim.py`, `e2_salidas.py`, `_e2e8_comun.py`); SEED 20261010; sin red; {segundos:.0f} s.

## 1. Resumen
- **E2-R1 (principal)**: coeficiente de Reg × Post sobre el log de la renta media de contratos nuevos = **{f(t.loc['E2-R1','coef'])}** (IC95 de Webb {f(t.loc['E2-R1','ic95_lo'])}; {f(t.loc['E2-R1','ic95_hi'])}; p tras Holm {f(t.loc['E2-R1','p_holm'], 5)}). Clase V18: **{cls['E2-R1']['clase']}**. Razón con la referencia (−0,045 de Jofre-Monseny et al., 2023): {f(razon, 2)}, etiqueta «coherente» (razón en [1/3; 3]; no interviene en la clase).
- **E2-R1c (contratos por 1.000 habitantes)**: {f(t.loc['E2-R1c','coef'])} (IC95 {f(t.loc['E2-R1c','ic95_lo'])}; {f(t.loc['E2-R1c','ic95_hi'])}), sin significación (p Holm {f(t.loc['E2-R1c','p_holm'], 3)}). Clase V18: **{cls['E2-R1c']['clase']}**; el TOST con δ = 0,05 {'se cumple' if clasif['E2-R1c']['info']['tost']['equivalente'] else 'no se cumple'} (IC90 {f(clasif['E2-R1c']['info']['tost']['ic90'][0])}; {f(clasif['E2-R1c']['info']['tost']['ic90'][1])}).
- **Reversión** tras la STC 37/2022 (2022T2-2023T4): coeficiente {f(r1['reversion']['coef_reversion'])} (p {f(r1['reversion']['p_reversion'], 3)}): el nivel vuelve al previo; no se aplica el tope de la adenda.
- **No estimables por variación o por datos**: E2-A1 (MDE {f(ne.loc['E2-A1','mde80'])} > 0,0298), E2-A2 (6 municipios tratados con EMAL no sellados), E2-A3 (2 controles), E2-A4 (MDE {f(ne.loc['E2-A4','mde80'])} > 0,027), E2-R2, E2-R2s, E2-R2-X1 y E2-A5 (datos). La ampliación A1 («provisional, sin difundir») no se estima: no hay cifra que difundir.
- Ninguna estimación IDENTIFICADO: no hay contradicción con una conclusión publicada (parada G no activada).

## 2. Qué se ha leído y qué queda fuera (sellado)
- Toda serie pasa por `sellado.filtrar` (tope temporal de docs/v18/sellado_v18.json y exclusión de unidades de v6, V15 y V16) y por `holdout.excluir_sellados_v6`. No se lee `data/sealed` ni se ejecuta ningún `evaluate_*`.
- Cataluña no tiene provincia sellada en v6. Los bloques de V15 y V16 dejan fuera 176 municipios catalanes (Barcelona 83, Lleida 86, Tarragona 7, Girona 0; adenda 1.5): de los 61 de la Ley 11/2020 quedan {len(d['ley'] & set(d['cT'].index))} con Incasòl trimestral.
- Barcelona ciudad (08019), que tiene distritos sellados, queda fuera de la principal (criterio de JMS) y entra en la variante v2: el total municipal de esa ciudad es una fuga declarada (adenda 1.5).
- Incasòl público: trimestral solo desde 2019T1 (anual desde 2007); la ventana de JMS (2016T1-2022T1) no existe en nuestros datos y la principal es 2019T1-2022T1 (adenda R-1).

## 3. Estimabilidad (adenda 1.3), calculada antes de mirar los coeficientes
MDE80: R = 2.000 reasignaciones placebo del tratamiento con el número y el calendario reales (σ y dependencia «ya vistas», tomadas del propio panel de entrenamiento; V15 y V16 publican la sd placebo del ATT y no la σ residual de este resultado). El MDE es optimista: no incluye los choques de comarca.

{md(e_tab)}

## 4. Resultados de las especificaciones estimadas
{md(prin)}

p_i7 = p de Webb con el valor crítico corregido por el tamaño de Monte Carlo (cs_webb, cat_trim_M: 0,071, banda «con valor crítico corregido»). Holm sobre la familia E2 (m = 4 tras las comprobaciones previas: E2-R1, E2-R1c, E2-P-D1b, E2-P-D1b-c). Las coprincipales P no se clasifican; la cifra publicada de V9-D1b (−0,0585 en renta y −0,0132 en contratos, con 60 y 181 unidades) va al lado y se reproduce en la muestra V18 con CS.

Inferencias alternativas de E2-R1: Webb por conglomerado espacial de 42 grupos (sustituto de las comarcas, que no están en el repositorio) p = {f(t.loc['E2-R1','p_webb_conglom'], 4)}; aleatorización entre municipios p = {f(t.loc['E2-R1','p_aleat'], 4)} y dentro del conglomerado p = {f(t.loc['E2-R1','p_aleat_conglom'], 4)}; EE de Conley a 10 km = {f(t.loc['E2-R1','se_conley10'], 5)} (CR1 {f(t.loc['E2-R1','se_cr1'], 5)}); Driscoll-Kraay p = {f(t.loc['E2-R1','p_dk_no_fiable'], 5)} (rótulo «no fiable»: NO APTO en su Monte Carlo).

## 5. Pruebas B4 de E2-R1
**Estudio de eventos** (coeficientes Reg × 1[t = k], base 2019T4; k = 0..12 es 2019T1..2022T1; k = 6 es 2020T3, la anticipación):

{md(ev[['periodo', 'coef', 'se']])}

- Pretendencias (cinco adelantos, contraste conjunto con covarianza agrupada): p = {f(r1['evento']['p_pretend'], 3)}.
- Potencia de Roth: pendiente lineal previa detectable al 80 % = {f(r1['evento']['pendiente_detectable'], 4)} por trimestre; el sesgo que implicaría en la ventana posterior ({f(r1['evento']['sesgo_post'], 4)}) supera la mitad de |referencia| (0,0225): prueba débil (tope SUGESTIVO).
- Placebo de fecha (anual 2014-2019, adopción falsa en 2017): coeficiente {f(r1['placebo_fecha']['coef'])}, p = {f(r1['placebo_fecha']['p'], 3)}, de signo contrario al principal.
- Placebo de resultado (población de 65 años o más por municipio y año; contratos de locales): sin dato en el repositorio. El sustituto de la renta IRPF solo cubre la C. Valenciana: no realizable. Prueba débil.
- Honest DiD (muestra comprimida sin 2020T1-2020T3; previos 2019T1-T3; referencia 2019T4). Según el Monte Carlo de V18 solo M̄ = 0 es apto; con M̄ = 0,5 y 1 es válido pero conservador (tamaño ≈ 0): se publica y no decide (adenda 1.12; desviación D2):

{md(hon)}

- I de Moran de los residuos medios por municipio (5 vecinos más próximos): I = {f(r1['moran']['I'], 3)} (E[I] = {f(r1['moran']['E_I'], 3)}), p unilateral = {f(r1['moran']['p_unilateral'], 3)}: {'hay' if r1['moran']['p_unilateral'] < 0.05 else 'no hay'} autocorrelación espacial positiva significativa de los residuos medios. Se publican igualmente Webb por conglomerado espacial, aleatorización dentro del conglomerado y Conley, porque el Monte Carlo de V18 mide un sobrerrechazo de la agrupación por municipio con choques de comarca (tamaño 0,071).
- Honest DiD en la variante anual (E2-R1-v8; previos 2014-2018, referencia 2019, posterior 2021): {honest_v8}.
- Reversión tras la STC 37/2022: coeficiente en 2022T2-2023T4 = {f(r1['reversion']['coef_reversion'])} (p {f(r1['reversion']['p_reversion'], 3)}); coeficiente de la vigencia en ese panel {f(r1['reversion']['coef_post'])}.
- Robustez: {txt_rob}

## 6. Variantes enumeradas (anexo A) y holgura
Ajuste de Benjamini-Yekutieli al 10 % dentro de cada identificador (q_by). Webb con 1.999 réplicas.

{md(var)}

## 7. Clasificación (I1-I8 revisados)
- **E2-R1: {cls['E2-R1']['clase']}.** Razones: {'; '.join(cls['E2-R1']['razones'])}.
- **E2-R1c: {cls['E2-R1c']['clase']}.** Razones: {'; '.join(cls['E2-R1c']['razones'])}. Lectura: coeficiente no significativo; no hay clase SUGESTIVO sin significación (K7): al no superar I1-I5 (placebo de fecha, persistencia tras la STC) la clase es ASOCIACIÓN, no NO CONCLUYENTE.
- I6 se publica como etiqueta (razón con la referencia); no interviene en la clase ni en B5.
- I8 pendiente para ambas (replicador-ciego). El lenguaje de ambas cifras es el de una asociación estimada.

## 8. Desviaciones y lecturas de las reglas (se recogen en docs/v18/desviaciones.md)
- **D1 (corregida en K9). Paro registrado.** La versión anterior de esta desviación («el paro de 2020 no está en la base») era falsa: el fichero mensual del SEPE por municipio (fichero paro_registrado_municipio_mensual.csv.gz de sepe_municipios, v9) cubre 2006-2026. La principal lleva ln(1 + paro) como media trimestral de los meses del fichero (adenda R-1); falta diciembre de 2020 en el fichero, así que 2020T4 es la media de octubre y noviembre. E2-R1-v5 («sin paro») es ahora una variante estimada y desaparece la holgura E2-R1-h1. Los ERTE por municipio no están en el repositorio.
- **D2. Honest DiD.** Se aplica la lectura de la adenda 1.12 y del Monte Carlo de V18: solo M̄ = 0 es apto; el criterio de I3 «IC con M̄ = 1 excluye el cero» no es evaluable (tamaño 0 con M̄ ≥ 0,5). I3 se juzga con las pretendencias y la potencia de Roth.
- **D3. Comarcas.** No están en el repositorio: 42 conglomerados de k-medias sobre los centroides de los 947 municipios (SEED 20261010) sustituyen a las comarcas en la inferencia alternativa.
- **D4. Entradas y salidas del régimen.** La lista de la Ley 11/2020 del repositorio no identifica municipios que entraron o salieron; no se pudo reconstruir con el DOGC (sin red). Se dice.
- **D5. Hogares en alquiler del Censo 2021** (E2-R1c-v1): la variable no tenía entrada en docs/v18/sellado_v18.json cuando se estimó la principal; se añadió DESPUÉS de la etiqueta (desviación B6-1) y la variante se estima a posteriori en `e2_robustez.py` (sección «Robustez B6» de este informe).
- **D6. Población** para contratos por 1.000 habitantes: padrón municipal (tope 2022 de la regla de sellado); en la reversión de 2023 se mantiene la de 2022.
- **D7. Códigos INE de MIVAU.** Los ficheros municipales de MIVAU solo traen nombres; el código se asigna por nombre dentro de su comunidad con el diccionario oficial del INE (3 de 205 sin resolver). Solo afecta a E2-A3 (no estimable).
- **D8. Lectura de la regla de clasificación (revisada en B6, K7).** Antes se aplicaba SUGESTIVO a un coeficiente sin significación con alguna prueba débil; tras la ronda 1 el autor decidió (K7) que no existe «SUGESTIVO sin significación»: un no significativo es NO CONCLUYENTE si supera I1-I5 y ASOCIACIÓN si no (opción `nulo_sin_sugestivo` de `clasificar`). Cambia E2-R1c: SUGESTIVO → ASOCIACIÓN.
- **D9. Coprincipales sin estimar.** E2-P-H1, E2-P-H2, E2-P-D1c y E2-P-Q1c heredan la no estimabilidad de la principal que acompañan (misma variación).

## 9. Limitaciones
- **Frase de limitación (K9; obligatoria al difundir la cifra principal, tal cual):** «{FRASE_K9}»
- Incasòl público solo da la renta media por municipio y trimestre, sin renta anterior, superficie ni tipo de contrato: no se separa composición de precio y no se contrasta el desvío a la temporada.
- La COVID coincide con el posterior; el control de JMS se define por el crecimiento de la renta de 2014-2019 (criterio legal de mercado tensionado), lo que condiciona la comparación (la coprincipal V9-D1b, sin ese criterio, da un coeficiente mayor).
- Las 4 provincias catalanas no bastan como clusters; la unidad de agrupación es el municipio.

## 10. Datos que los desbloquearían
Microdatos de contratos del registro de fianzas con renta, renta anterior, superficie y tipo de contrato (tareas_autor, punto 4); compraventas municipales de todos los municipios; EMAL y zonas tensionadas con más trimestres posteriores; evaluación diferida de H1 y H2 de V15 para A1.
"""
    (OUT / "informe.md").write_text(txt, encoding="utf-8")
