"""V16 fase 2 · hechos.json, resultado.json e informe.md a partir de las tablas (ninguna cifra tecleada)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from f2_esfuerzo_nucleo import CCAA_NOMBRES, EDAD, NAC, QUIN, SEED, TEN

FUENTE = "INE, Encuesta de Condiciones de Vida, microdatos transversales (ficheros D, H, R, P)"
FECHA = "2026-06-10"
COB = "España (hogares privados; agregado de las 19 regiones NUTS2 de la ECV)"
ANCL = {"Total": "esf-espana", "Tenencia": "esf-tenencia", "Quintil": "esf-quintil", "Edad": "esf-edad",
        "Nacionalidad": "esf-nacionalidad", "CCAA": "esf-ccaa"}
NOMBRE_TEN = {"prop_sin_hipoteca": "propiedad sin hipoteca", "prop_con_hipoteca": "propiedad con hipoteca",
              "alquiler_mercado": "alquiler a precio de mercado", "alquiler_reducido_cesion": "alquiler reducido o cesión",
              "Espana": "nacionalidad española", "UE": "nacionalidad de otro país de la UE", "Resto": "nacionalidad de fuera de la UE"}
NOMBRE_IND = {"sobre40": "Población con gasto neto de vivienda > 40 % de la renta neta",
              "sobre30": "Población con gasto neto de vivienda > 30 % de la renta neta",
              "cae_bajo_umbral": "Población que cae bajo el umbral de pobreza (60 % de la mediana) tras el gasto de vivienda y no estaba bajo él antes"}


def _f(x, n=1):
    return "s. d." if x is None or not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def _celda(T, y, d, c, i):
    r = T[(T.anio == y) & (T.dimension == d) & (T.categoria == c) & (T.indicador == i)]
    return r.iloc[0] if len(r) else None


def _txt(T, y, d, c, i):
    r = _celda(T, y, d, c, i)
    if r is None or r.estado != "publicable":
        return "suprimida"
    return f"{_f(r.estimacion)} [{_f(r.ic_lo)}; {_f(r.ic_hi)}]"


def _chg(CH, per, d, c, i):
    r = CH[(CH.periodo == per) & (CH.dimension == d) & (CH.categoria == c) & (CH.indicador == i)]
    return r.iloc[0] if len(r) else None


def escribir_informe(out, T, CH, CE, DC, CM, DD, B, anios, smoke):
    uy = max(anios)
    hechos = []
    n_supr = 0

    def add(slug, ind, val, lo, hi, unidad, periodo, dim, extra=""):
        hechos.append(dict(id=f"V16-ESF-{slug}", indicador=ind, valor=round(float(val), 3), min=round(float(lo), 3),
                           max=round(float(hi), 3), unidad=unidad, periodo=periodo, cobertura=COB + extra,
                           fuentes=[FUENTE], capa="C4", fecha_dato=FECHA,
                           ficha=f"output/v16/f2_esfuerzo/informe.md#{ANCL[dim]}"))

    def nivel(slug, d, c, i, nombre):
        nonlocal n_supr
        r = _celda(T, uy, d, c, i)
        if r is None or r.estado != "publicable":
            n_supr += 1
            return
        add(f"{slug}-{uy}", f"{NOMBRE_IND[i]} · {nombre}", r.estimacion, r.ic_lo, r.ic_hi, UN(i), str(uy), d)

    def UN(i):
        return "% de la población"

    def cambio(slug, d, c, i, nombre, per):
        nonlocal n_supr
        r = _chg(CH, per, d, c, i)
        if r is None or r.estado != "publicable":
            n_supr += 1
            return
        ex = ""
        if per.startswith("2008"):
            e8 = CE[CE.anio == 2008]
            if len(e8) and not bool(e8.dentro_0_5pp.iloc[0]):
                ex = "; el nivel de 2008 difiere de Eurostat más de 0,5 pp (ver informe, validación)"
        add(f"{slug}-{per.replace('-', '_')}", f"Cambio de: {NOMBRE_IND[i]} · {nombre}", r.cambio, r.ic_lo, r.ic_hi,
            "puntos porcentuales", per, d, ex)

    for i, s in [("sobre40", "S40"), ("sobre30", "S30"), ("cae_bajo_umbral", "RES")]:
        nivel(f"ESP-{s}", "Total", "Espana", i, "España")
    for p in ("2008-" + str(uy), "2015-" + str(uy), "2019-" + str(uy)):
        cambio("ESP-S40", "Total", "Espana", "sobre40", "España", p)
    for c in TEN:
        nivel(f"TEN-{c}-S40", "Tenencia", c, "sobre40", NOMBRE_TEN[c])
    for c in ("alquiler_mercado", "prop_con_hipoteca"):
        for p in ("2008-" + str(uy), "2015-" + str(uy), "2019-" + str(uy)):
            cambio(f"TEN-{c}-S40", "Tenencia", c, "sobre40", NOMBRE_TEN[c], p)
    for c in QUIN:
        nivel(f"QUI-{c}-S40", "Quintil", c, "sobre40", f"quintil de renta {c}")
    cambio("QUI-Q1-S40", "Quintil", "Q1", "sobre40", "quintil de renta Q1", "2019-" + str(uy))
    for c in EDAD:
        nivel(f"EDA-{c}-S40", "Edad", c, "sobre40", f"sustentador de {c} años")
    for p in ("2008-" + str(uy), "2019-" + str(uy)):
        cambio("EDA-16-34-S40", "Edad", "16-34", "sobre40", "sustentador de 16-34 años", p)
    for c in NAC:
        nivel(f"NAC-{c}-S40", "Nacionalidad", c, "sobre40", f"sustentador con {NOMBRE_TEN[c]}")
        cambio(f"NAC-{c}-S40", "Nacionalidad", c, "sobre40", f"sustentador con {NOMBRE_TEN[c]}", "2019-" + str(uy))
    for t in ("alquiler_mercado", "prop_con_hipoteca"):
        per = "2019-" + str(uy)
        g = DC[(DC.tenencia == t) & (DC.periodo == per)]
        for met, est, comp, lab in [("observado", "media", "total", "cambio observado del esfuerzo medio (gasto/renta)"),
                                    ("DFL", "media", "composicion", "parte del cambio atribuida contablemente a la composición (DFL)")]:
            r = g[(g.metodo == met) & (g.estadistico == est) & (g.componente == comp)]
            if len(r):
                r = r.iloc[0]
                hechos.append(dict(id=f"V16-ESF-DES-{t}-{met}-{comp}-{per.replace('-', '_')}",
                                   indicador=f"{lab} · {NOMBRE_TEN[t]}", valor=round(float(r.valor_pp), 3),
                                   min=round(float(r.ic_lo), 3), max=round(float(r.ic_hi), 3),
                                   unidad="puntos porcentuales de la renta neta", periodo=per, cobertura=COB,
                                   fuentes=[FUENTE], capa="C4", fecha_dato=FECHA,
                                   ficha="output/v16/f2_esfuerzo/informe.md#esf-descomposicion"))
    hechos = hechos[:40]
    if not smoke:
        assert len(hechos) <= 40
    (out / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---------- validación
    v1 = CE[CE.anio >= 2013]
    v0 = CE[CE.anio < 2013]
    ok1519 = CE[(CE.anio >= 2015) & (CE.anio <= 2024)]
    # ---------- informe
    L = []
    L.append("# V16 · Fase 2 · Esfuerzo de acceso a la vivienda (ECV 2004-2025)\n")
    L.append("Capa **C4 · DESCRIPTIVO**. Contabilidad y descripción: no se contrasta ninguna política. ECV y Eurostat son la misma "
             "encuesta (K6): la coincidencia con Eurostat valida la implementación, no forma un C1. Año = año de la encuesta "
             "(la renta es del año anterior). " + (f"**Ejecución de humo (B={B}); no son resultados finales.** " if smoke else "") + "\n")
    L.append("## Definiciones y método\n")
    L.append("- **Gasto neto** G = 12·HH070 − HY070N (HH070 mensual; HY070N, ayudas a la vivienda, anual). **Renta neta** Y = HY020 − HY070N "
             "(definición Eurostat de la sobrecarga de coste de vivienda). Se cuenta como sobrecarga G > 40 % o 30 % de Y; con Y ≤ 0 y G > 0 también.")
    L.append("- **Renta residual:** renta equivalente (HY020/HX240) antes y después de 12·HH070; umbral = 60 % de la mediana ponderada "
             "por personas del mismo año de la renta antes del gasto. Indicador: antes ≥ umbral y después < umbral.")
    L.append("- **Esfuerzo** r = min(G/Y, 1) (r = 1 si Y ≤ 0 y G > 0). Tasas: ponderadas por personas (suma de RB050 del hogar); "
             "esfuerzo medio: pesos de hogar DB090.")
    L.append("- **Grupos:** quintil de renta equivalente antes del gasto (personas); edad y nacionalidad del sustentador (miembro con mayor renta personal neta; "
             "nacionalidad: PB220A hasta 2020, RB290 desde 2021; 2004-2009 el código 4 se agrupa con 3: supuesto); tenencia: HH021 desde 2011; "
             "hasta 2010 (HH020) la hipoteca se identifica por cuotahip > 0 (ruptura de definición); región NUTS2 (DB040; la ECV no tiene provincia).")
    L.append(f"- **Incertidumbre:** bootstrap de hogares con reposición, B = {B}, SEED = {SEED}, IC 95 % percentil; el umbral de pobreza se recalcula en cada réplica; "
             "los quintiles se fijan con la muestra completa. El diseño real tiene estratos y conglomerados no publicados: el IC es **aproximado** (algo estrecho). "
             "**Supresión:** celdas con menos de 50 hogares muestrales o CV > 30 % se marcan «suprimida».\n")
    L.append("## Validación frente a Eurostat ilc_lvho07a\n")
    L.append(f"- 2013-{uy}: diferencia absoluta máxima {_f(v1.diferencia_pp.abs().max(), 2)} pp; dentro de ±0,5 pp en {int(v1.dentro_0_5pp.sum())} de {len(v1)} años "
             f"(2015-2024: {int(ok1519.dentro_0_5pp.sum())} de {len(ok1519)}).")
    if len(v0):
        L.append(f"- 2004-2012: **no coincide** en {int((~v0.dentro_0_5pp).sum())} de {len(v0)} años (diferencia máxima {_f(v0.diferencia_pp.abs().max(), 1)} pp, "
                 "mi tasa por encima). Origen no resuelto (posible cambio de definición de HH070 en la serie anterior a 2013). Esos años se tratan como no validados; "
                 "el nivel de 2008 solo se usa con esta advertencia.")
    L.append("")
    L.append("(Años seleccionados; serie completa en comparacion_eurostat.csv.)\n")
    L.append("| Año | ECV (%) | Eurostat (%) | Dif. (pp) |\n|---|---|---|---|")
    for r in CE[CE.anio.isin([2008, 2012, 2013, 2015, 2019, 2022, uy])].itertuples():
        L.append(f"| {r.anio} | {_f(r.ecv_microdatos)} | {_f(r.eurostat_ilc_lvho07a)} | {_f(r.diferencia_pp)} |")
    L.append("")
    ys = [y for y in (2008, 2015, 2019, uy) if y in anios]

    def tabla(dim, cats, ind, nombres=None):
        L.append("| Grupo | " + " | ".join(str(y) for y in ys) + " |\n|---|" + "---|" * len(ys))
        for c in cats:
            nm = (nombres or {}).get(c, c)
            L.append(f"| {nm} | " + " | ".join(_txt(T, y, dim, c, ind) for y in ys) + " |")
        L.append("")

    L.append("## Esfuerzo de acceso\n")
    L.append('<a id="esf-espana"></a>\n### España (% de la población; IC 95 %)\n')
    L.append("| Indicador | " + " | ".join(str(y) for y in ys) + " |\n|---|" + "---|" * len(ys))
    for i in ("sobre40", "sobre30", "cae_bajo_umbral", "pobreza_antes", "pobreza_despues"):
        L.append(f"| {i} | " + " | ".join(_txt(T, y, "Total", "Espana", i) for y in ys) + " |")
    L.append("")
    L.append('<a id="esf-tenencia"></a>\n### Por tenencia (sobre40, %)\n')
    tabla("Tenencia", TEN, "sobre40", NOMBRE_TEN)
    L.append('<a id="esf-quintil"></a>\n### Por quintil de renta (sobre40, %)\n')
    tabla("Quintil", QUIN, "sobre40")
    L.append('<a id="esf-edad"></a>\n### Por edad del sustentador (sobre40, %)\n')
    tabla("Edad", EDAD, "sobre40")
    L.append('<a id="esf-nacionalidad"></a>\n### Por nacionalidad del sustentador (sobre40, %)\n')
    tabla("Nacionalidad", NAC, "sobre40", NOMBRE_TEN)
    L.append('<a id="esf-ccaa"></a>\n### Por región (sobre40, último año; todas las regiones y años en esfuerzo_por_anio.csv)\n')
    L.append("; ".join(f"{CCAA_NOMBRES[c]} {_txt(T, uy, 'CCAA', c, 'sobre40')}" for c in sorted(CCAA_NOMBRES, key=lambda k: CCAA_NOMBRES[k])) + ".\n")
    L.append('<a id="esf-descomposicion"></a>\n## Descomposiciones contables del esfuerzo medio (puntos porcentuales; IC 95 %)\n')
    L.append("Variable: r = min(G/Y, 1). Covariables: ln renta, edad del sustentador (y cuadrado), tamaño del hogar, nacionalidad, región. "
             "«Atribuido a características» es una suma contable: la renta entra a la vez en la ratio y como covariable, así que no se lee como mecanismo. "
             "OB2 = Oaxaca-Blinder de dos pliegues (referencia agrupada); DFL = reponderación; directa = identidad exacta de la razón de medias.\n")
    L.append("| Tenencia | Periodo | Cambio observado | OB2 características | OB2 no atribuido | OB3 dotaciones / coef. / interacción | DFL composición / estructura | Directa: gasto / renta / interacción | Métodos |")
    L.append("|---|---|---|---|---|---|---|---|---|")

    def g_(t, p, met, est, comp, dfx=DC):
        r = dfx[(dfx.tenencia == t) & (dfx.periodo == p) & (dfx.metodo == met) & (dfx.estadistico == est) & (dfx.componente == comp)]
        return r.iloc[0] if len(r) else None

    def ft(r):
        return "s. d." if r is None else f"{_f(r.valor_pp, 2)} [{_f(r.ic_lo, 2)}; {_f(r.ic_hi, 2)}]"

    for t in sorted(DC.tenencia.unique()):
        for p in DC[DC.tenencia == t].periodo.unique():
            dd = DD[(DD.tenencia == t) & (DD.periodo == p) & (DD.gasto_definicion == "HH070 neto de ayudas")]
            dg = lambda c: dd[dd.componente == c].iloc[0] if len(dd[dd.componente == c]) else None  # noqa: E731
            dire = " / ".join(_f(dg(c).valor, 1) if dg(c) is not None else "s. d." for c in ("gasto", "renta", "interaccion"))
            ob3 = " / ".join(_f(g_(t, p, "OB3", "media", c).valor_pp, 2) for c in ("dotaciones", "coeficientes", "interaccion"))
            dfl = " / ".join(_f(g_(t, p, "DFL", "media", c).valor_pp, 2) for c in ("composicion", "estructura"))
            dis = CM[(CM.tenencia == t) & (CM.periodo == p) & (CM.estadistico == "media")].discrepan.iloc[0]
            L.append(f"| {NOMBRE_TEN[t]} | {p} | {ft(g_(t, p, 'observado', 'media', 'total'))} | {ft(g_(t, p, 'OB2', 'media', 'atribuido'))} | "
                     f"{ft(g_(t, p, 'OB2', 'media', 'no_atribuido'))} | {ob3} | {dfl} | {dire} | {'discrepan' if dis else 'coinciden'} |")
    L.append("")
    L.append(f"Cuantiles, solo 2019-{uy} (resto en comparacion_metodos.csv; RIF, Firpo-Fortin-Lemieux, atribuido a características frente a composición DFL; pp):\n")
    L.append("| Tenencia | Periodo | Estadístico | Cambio | RIF características | DFL composición | Métodos |\n|---|---|---|---|---|---|---|")
    for r in CM[(CM.estadistico != "media") & (CM.periodo == "2019-" + str(uy))].itertuples():
        L.append(f"| {NOMBRE_TEN[r.tenencia]} | {r.periodo} | {r.estadistico} | {_f(r.cambio_total_pp, 2)} | {_f(r.atribuido_regresion_pp, 2)} | "
                 f"{_f(r.composicion_DFL_pp, 2)} | {'discrepan' if r.discrepan else 'coinciden'} |")
    L.append("")
    nd = int(CM.discrepan.sum())
    L.append(f"Regla de discrepancia (fijada aquí): signo distinto o diferencia > 25 % del cambio total. Discrepan {nd} de {len(CM)} comparaciones; "
             "se reportan ambos métodos siempre (comparacion_metodos.csv).\n")
    L.append("## Límites\n")
    L.append("- C4 (fuente única); sin interpretación de mecanismos. HH070 en propiedad con hipoteca recoge intereses, no amortización (la cuota completa está en la variante de descomposicion_directa.csv). "
             "El gasto no es el precio de compra ni la renta contractual nueva. Ruptura de marco y tamaño muestral en 2021 (ver auditoría V15). "
             "La edad y la nacionalidad son las del sustentador (criterio de mayor renta personal). Los IC no incluyen estratos ni conglomerados. "
             f"Celdas suprimidas entre las cifras candidatas: {n_supr}. Contrastes de la parte atribuida: BH sobre {int(DC.p_ajustado_BH.notna().sum())} (descomposiciones.csv).")
    (out / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------- resultado.json
    tot = _celda(T, uy, "Total", "Espana", "sobre40")
    pad = DC.p_ajustado_BH.dropna()
    res = {
        "rama": "v16/f2_esfuerzo",
        "pregunta": "¿Cuál es el esfuerzo de acceso a la vivienda (sobrecarga 30/40 %, renta residual) por renta, edad, tenencia, nacionalidad y región, y cómo se reparte contablemente su cambio entre características y resto?",
        "capa": "C4",
        "datos": FUENTE + " 2004-2025; sin provincia (NUTS2); no toca la muestra sellada v6",
        "N": int(T.groupby("anio").n_hogares.max().sum()),
        "metodo": f"Descriptivo ponderado con bootstrap de hogares (B={B}); Oaxaca-Blinder 2 y 3 pliegues, reponderación DFL, regresiones RIF p10/p50/p90, identidad directa gasto-renta",
        "estimacion": {"sobre40_espana_%s" % uy: round(float(tot.estimacion), 3)},
        "ic95": [round(float(tot.ic_lo), 3), round(float(tot.ic_hi), 3)],
        "p_ajustado": {"metodo": "BH sobre contrastes de la parte atribuida", "n_contrastes": int(len(pad)),
                       "minimo": float(pad.min()) if len(pad) else None},
        "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"eurostat_2013_%s_max_abs_dif_pp" % uy: round(float(v1.diferencia_pp.abs().max()), 3),
                         "eurostat_2015_2024_anios_dentro_0_5pp": f"{int(ok1519.dentro_0_5pp.sum())}/{len(ok1519)}",
                         "eurostat_2004_2012_anios_fuera_0_5pp": int((~v0.dentro_0_5pp).sum()) if len(v0) else 0,
                         "discrepancias_metodos": f"{nd}/{len(CM)}", "B": B, "semilla": SEED,
                         "n_cifras_candidatas": len(hechos)},
        "fuera_muestra": {"modelo": "no aplica (descriptivo)", "rmse": None, "dm_vs_ar4": None},
        "notas": "ECV y Eurostat son la misma encuesta: no hay C1. IC aproximados (sin estratos ni conglomerados). Descomposiciones contables, sin interpretación de mecanismoses. 2004-2012 no coincide con Eurostat.",
    }
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
