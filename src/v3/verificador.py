"""Verificador v3: una ficha por afirmación del debate (`make verificador`).

Lee solo salidas ya generadas (output/v3/PA, PB, GL, C1, C3, PD) y los paneles vía holdout.load_full, sin red.
Cada ficha: enunciado neutro, capa de la evidencia más fuerte usada (C1-C4), magnitud e intervalo, cota si
procede, literatura (replicada o de calibración), veredicto con su REGLA explícita, límites y rutas de evidencia.
Veredictos: RESPALDADA / PARCIALMENTE / NO RESPALDADA / CONTRADICHA / SIN EVIDENCIA SUFICIENTE.
Reglas generales:
- CONTRADICHA: un hecho C1, una cota C2 o un efecto C3 robusto incompatible con la afirmación.
- NO RESPALDADA: la evidencia C2/C3 acota el factor muy por debajo de lo que la afirmación necesita, o el diseño
  C3 no encuentra el efecto con potencia suficiente.
- RESPALDADA: C1, C2 o C3 robusto compatibles con la afirmación en todo su rango.
- PARCIALMENTE: respaldada en parte (zonas, periodos o magnitud menor) o según supuestos.
- SIN EVIDENCIA SUFICIENTE: solo C4, o sin datos.
Una ficha nunca usa una capa superior a la de su evidencia (check_texto lo comprueba).

REGLA COMÚN para afirmaciones de atribución («X explica / es la causa principal de la subida») — V01, V03, V04, V12:
(i) el enunciado fija la fracción que necesita: «causa principal» = ≥50 % de la subida; «explica» = ≥50 %;
(ii) una cota superior C2 de CANTIDAD (viviendas u hogares) no es respaldo ni parcial: no atribuye precio;
(iii) la evidencia C4 no entra en el veredicto (se informa en «magnitud»);
(iv) CONTRADICHA en un periodo si una cota C2 o un hecho C1 tiene signo contrario en ese periodo; PARCIALMENTE si
     está contradicha en unos periodos y es compatible (cota C2 que alcanza el 50 %) en otros; RESPALDADA si una cota
     inferior C2/C3 supera el 50 %; NO RESPALDADA si una cota superior C2/C3 de PRECIO queda por debajo del 50 %;
     en otro caso, SIN EVIDENCIA SUFICIENTE.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
OUT = RAIZ / "output" / "v3"
DEST = OUT / "verificador"

LIT = {
    "GL": "García-López et al. (2020), JUE, VERIFICADA, Q1",
    "MESVAL": "MESVAL-UV (2022), NO VERIFICADA (sin DOI)",
    "JMS": "Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE, VERIFICADA, Q1",
    "DIAMOND": "Diamond, McQuade y Qian (2019), AER, VERIFICADA, Q1",
    "SAIZ07": "Saiz (2007), JUE, VERIFICADA, Q1 (año no comprobado)",
    "SA": "Sá (2015), EJ, VERIFICADA, Q1",
    "GO": "González y Ortega (2013), JRS, VERIFICADA, cuartil no verificado",
    "POTERBA": "Poterba (1984), QJE, VERIFICADA, Q1",
    "BDE": "Banco de España, Informe Anual 2025 (DOI no comprobado)",
    "SAIZ10": "Saiz (2010), QJE, VERIFICADA",
}


def _json(ruta: Path):
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def _por_id(lista, clave="id"):
    return {x[clave]: x for x in (lista or [])}


def _f(x, nd=1):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return "n/d"
    s = f"{x:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s


def _iv(iv, nd=1):
    return f"[{_f(iv[0], nd)}; {_f(iv[1], nd)}]" if iv else "n/d"


def cargar() -> dict:
    ev = {
        "PA": _por_id(_json(OUT / "PA" / "hechos.json")),
        "PB": _por_id(_json(OUT / "PB" / "cotas.json")),
        "GL": _json(OUT / "GL" / "resultado.json"),
        "C1": _json(OUT / "C1" / "resultado.json"),
        "C3": _json(OUT / "C3" / "resultado.json"),
        "PD": _json(OUT / "PD" / "resultados.json"),
        "holm": _json(OUT / "holm_v3.json"),
    }
    ev["extranjeros"] = compradores_extranjeros()
    return ev


def compradores_extranjeros() -> dict | None:
    """Hecho C1 auxiliar: cuota de compraventas de vivienda por personas de nacionalidad extranjera (2 fuentes)."""
    try:
        import holdout
        d = holdout.load_full("nacional_q_v2", "verificador")
    except Exception:  # noqa: BLE001
        return None
    d = d[d["trimestre"].astype(str).str[:4].isin(["2023", "2024", "2025"])]
    mivau = (d["trans_extranjeros"] / d["trans_total"] * 100).dropna()
    regis = d["registradores_extranj_pct"].dropna()
    if mivau.empty or regis.empty:
        return None
    return {"mivau_min": float(mivau.min()), "mivau_max": float(mivau.max()),
            "registradores_min": float(regis.min()), "registradores_max": float(regis.max()),
            "intervalo": [float(min(mivau.min(), regis.min())), float(max(mivau.max(), regis.max()))]}


def _c3(ev, clave):
    """Resumen de un diseño de la oleada 2: (capa, texto) o (None, motivo)."""
    r = ev.get(clave)
    if not r:
        return None, "diseño no disponible"
    return r.get("capa"), r


def fichas(ev) -> list[dict]:
    PA, PB = ev["PA"], ev["PB"]
    out = []

    # ---------------------------------------------------------------- V01 turísticos
    b1c, b1p = PB.get("B1-nac-cantidad", {}), PB.get("B1-nac-precio-eps_min", {})
    b1cen = PB.get("B1-nac-precio-central", {})
    c1capa, c1 = _c3(ev, "C1")
    gl = ev["GL"] or {}
    if c1capa is None:
        c1txt = "H3-1 no disponible"
    else:
        sel = _json(OUT / "C1" / "sellado_H3-1.json") or {}
        sn = sel.get("nacional", {})
        c1txt = (f"H3-1 (sección, efectos fijos, nacional): capa {c1capa}; entrenamiento β = {_f(c1.get('estimacion'), 5)} "
                 f"log-p por pp de VUT, IC95 {_iv(c1.get('ic95'), 4)}; distritos sellados β = {_f(sn.get('b'), 4)} "
                 f"[{_f(sn.get('lo'), 4)}; {_f(sn.get('hi'), 4)}] (p {_f(sn.get('p'), 2)}). Con un aumento típico de "
                 "1,37 pp de VUT equivale a menos de +0,5 % de alquiler (C4)")
    out.append(dict(
        id="V01", tema="Viviendas turísticas",
        enunciado="Las viviendas turísticas son la causa principal de la subida del alquiler en España.",
        capa="C2",
        magnitud=(f"El aumento de VUT 2020M08-2024M08 equivale como máximo al {_f(b1c.get('cota_superior'))} % del stock "
                  f"de alquiler (sustitución 1:1). El {_f(b1c.get('no_explica'))} % de la subida municipal del alquiler "
                  f"ocurre en municipios donde las VUT apenas crecieron. {c1txt}."),
        intervalo=f"desplazamiento de oferta {_iv([b1c.get('sensibilidad_min'), b1c.get('sensibilidad_max')])} % del stock",
        cota=(f"C2 (cantidad): ≤{_f(b1c.get('cota_superior'))} % del stock de alquiler. C4 (precio, condicionado a ε): "
              f"≤{_f(b1p.get('cota_superior'))} % con |ε_d|=0,33 y ≤{_f(b1cen.get('cota_superior'))} % con |ε_d|=1"),
        literatura=(f"{LIT['GL']}, Barcelona 2012-2016: réplica conceptual 2021-2024 NO REPLICADO "
                    f"(T = {_f(gl.get('objetivo_T_pp'), 4)} log-p por pp; propia {_f(gl.get('estimacion'), 4)}). "
                    f"{LIT['MESVAL']}: NO REPLICABLE (datos propietarios)."),
        veredicto=("NO RESPALDADA" if (c1capa == "C3" and c1 and c1.get("contribucion_nacional_pct_max", 100) < 50)
                   else "SIN EVIDENCIA SUFICIENTE"),
        regla=("Regla común (i)-(iv): «causa principal» exige ≥50 % de la subida. Solo hay cota C2 de cantidad "
               "(desplazamiento ≤2,7 % del stock de alquiler; el 25 % de la subida municipal ocurre donde las VUT "
               "apenas crecieron), que no atribuye precio; sin cota C2/C3 de precio, SIN EVIDENCIA SUFICIENTE. "
               "H3-1 y H3-2 quedaron en C4 (fallan adelanto, sensibilidad y sellado; el placebo de tratamiento pasa): sus estimaciones, "
               "con IC95 que incluye 0, no se promueven de capa."),
        limites=("Las VUT del INE no son todos los alquileres de temporada; el efecto local en barrios concretos puede "
                 "ser mayor que el nacional (ver cotas por ciudad en output/v3/PB); SERPAVI es un stock que amortigua."),
        evidencia=["output/v3/PB/cotas.json#B1", "output/v3/C1/resultado.json", "output/v3/GL/replicacion.md"],
    ))

    # ---------------------------------------------------------------- V02 grandes tenedores
    out.append(dict(
        id="V02", tema="Grandes tenedores",
        enunciado="Los fondos de inversión y los grandes tenedores son los responsables de la subida de precios y alquileres.",
        capa="C4", magnitud="Sin datos de titularidad por tamaño de tenedor (solicitud de transparencia al Catastro pendiente).",
        intervalo="n/d", cota="B3 en espera de datos (src/v3/ingesta_grandes_tenedores.py)",
        literatura="Sin trabajo replicado para España con estos datos.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla="Sin datos de la cuota de grandes tenedores no se puede acotar su contribución.",
        limites="La ingesta está preparada; la cota se calculará con el esquema de B1 cuando lleguen los datos.",
        evidencia=["docs/v3/solicitudes_transparencia.md", "output/v3/PB/grandes_tenedores.json"],
    ))

    # ---------------------------------------------------------------- V03 inmigración
    b2c = PB.get("B2-nac-cuota-2014-2019", {})
    b2_0813 = PB.get("B2-nac-cuota-2008-2013", {})
    ne = None
    f_ne = OUT / "PB" / "tablas" / "b2_no_explica_provincias.csv"
    if f_ne.exists():
        t = pd.read_csv(f_ne)
        ne = t[(t["periodo"] == "2014-2019") & (t["mercado"] == "alquiler")]["no_explica_saldo_no_pos_pct"]
        ne = float(ne.iloc[0]) if len(ne) else None
    out.append(dict(
        id="V03", tema="Inmigración",
        enunciado="La inmigración es la causa principal de la subida de los precios y de los alquileres (≥50 % de la subida).",
        capa="C2",
        magnitud=(f"Fracción máxima de la creación neta de hogares atribuible a hogares extranjeros: "
                  f"{_f(b2c.get('cota_superior'))} % en 2014-2019 (rango {_iv([b2c.get('sensibilidad_min'), b2c.get('sensibilidad_max')])}); "
                  "en 2014-2025 y 2020-2025 la cota con el extremo lógico (1 persona por hogar) llega al 100 % y no es informativa; "
                  f"en 2008-2013 el saldo extranjero neto fue negativo (cota {_f(b2_0813.get('cota_superior'))} %). "
                  + (f"Dato análogo al de V01: en 2014-2019 el {_f(ne)} % de la subida del alquiler provincial ocurrió en "
                     "provincias con saldo extranjero no positivo; en 2020-2025 no hay provincias así (sin dato análogo). "
                     if ne is not None else "Sin dato análogo de subida sin inmigración neta. ")
                  + "Las traducciones a precio son C4 condicionadas a ε."),
        intervalo=_iv([b2c.get("sensibilidad_min"), b2c.get("sensibilidad_max")]) + " % de Δhogares (2014-2019)",
        cota="C2 de cantidad (hogares); las traducciones a precio son C4 condicionadas a ε.",
        literatura=f"{LIT['SAIZ07']}; {LIT['SA']}; {LIT['GO']}: magnitudes de calibración (no replicadas).",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla=("Regla común (i)-(iv), la misma que V01: solo hay cota C2 de cantidad (hogares), que no atribuye precio; "
               "sin cota C2/C3 de precio ni diseño C3 propio, SIN EVIDENCIA SUFICIENTE. v2 (BI) asocia la inmigración al "
               "alquiler con evidencia EXPLORATORIA, que no entra en el veredicto."),
        limites="Medida por nacionalidad (las nacionalizaciones la sesgan a la baja); tamaño del hogar extranjero supuesto.",
        evidencia=["output/v3/PB/cotas.json#B2", "output/v3/PB/tablas/b2_no_explica_provincias.csv", "output/v2/informe_v2.md"],
    ))

    # ---------------------------------------------------------------- V04 falta de oferta y suelo
    a1 = PA.get("A1_nacional_2021-2025", {})
    a1b = PA.get("A1_nacional_2012-2021", {})
    out.append(dict(
        id="V04", tema="Oferta y suelo",
        enunciado="La falta de oferta nueva y de suelo es la causa principal del problema de la vivienda (≥50 % de la subida).",
        capa="C1",
        magnitud=(f"Balance contable hogares − viviendas nuevas 2021-2025: {_f(a1.get('magnitud'), 0)} viviendas "
                  f"(rango entre fuentes {_iv(a1.get('intervalo'), 0)}); en 2012-2021 el signo no está determinado "
                  f"({_iv(a1b.get('intervalo'), 0)}). El papel del suelo como moderador no es detectable con los datos (P-C4)."),
        intervalo=_iv(a1.get("intervalo"), 0) + " viviendas (2021-2025)",
        cota="—",
        literatura=f"{LIT['SAIZ10']}; Glaeser y Gyourko (2018), JEP, VERIFICADA: calibración. {LIT['BDE']}: ≈750 mil.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla=("Regla común (i)-(iv), la misma que V01 y V03: el desfase hogares − viviendas nuevas desde 2021 es un hecho "
               "C1 (ver V05), pero no atribuye la subida; no hay cota C2/C3 de precio para la oferta y el moderador «suelo» "
               "no es detectable (P-C4)."),
        limites="Un balance contable no mide demanda insatisfecha a cualquier precio; bajas del parque supuestas.",
        evidencia=["output/v3/PA/tablas/A1_tabla_unica_periodos.csv", "output/v3/POT/potencia.md#P-C4"],
    ))

    # ---------------------------------------------------------------- V05 déficit de cientos de miles
    out.append(dict(
        id="V05", tema="Déficit",
        enunciado="Faltan cientos de miles de viviendas en España.",
        capa="C1",
        magnitud=(f"2021-2025: {_f(a1.get('magnitud'), 0)} viviendas; rango entre fuentes {_iv(a1.get('intervalo'), 0)}. "
                  f"2012-2021: signo no determinado ({_iv(a1b.get('intervalo'), 0)})."),
        intervalo=_iv(a1.get("intervalo"), 0) + " viviendas",
        cota="—", literatura=f"{LIT['BDE']}: ≈750 mil, dentro del rango.",
        veredicto="PARCIALMENTE",
        regla=("Criterio de periodo común a todas las fichas: una afirmación sin periodo se juzga en todas las ventanas C1 "
               "disponibles. Respaldada en 2021-2025 (todas las combinaciones dan cientos de miles, C1) y no determinada "
               "con 2012 como base: PARCIALMENTE. Las ventanas C1 se eligieron tras ver la disponibilidad de fuentes "
               "(docs/v3/limitaciones.md, 7)."),
        limites=("Depende del periodo de partida: con 2012 como base el signo no está determinado. «Faltan» se refiere "
                 "al balance contable, no a una necesidad normativa."),
        evidencia=["output/v3/PA/hechos.json#A1_nacional_2021-2025"],
    ))

    # ---------------------------------------------------------------- V06 / V07 topes
    c3 = ev.get("C3")
    holm = {}
    f_h = OUT / "holm_v3.csv"
    if f_h.exists():
        holm = pd.read_csv(f_h).set_index("hipotesis")["p_holm"].to_dict()
    jt = None
    f_j = OUT / "C3" / "tabla_replicacion_jms.csv"
    if f_j.exists():
        jt = pd.read_csv(f_j)

    def ficha_tope(h, fid, enunciado, objetivo, que):
        if not c3:
            return dict(id=fid, tema="Topes de alquiler", enunciado=enunciado, capa="C4",
                        magnitud="Diseño H3-3 no disponible.", intervalo="n/d", cota="—", literatura=LIT["JMS"],
                        veredicto="SIN EVIDENCIA SUFICIENTE", regla="Sin diseño.", limites="—", evidencia=[])
        e, capa = c3["estimacion"][h], c3["capa"][h]
        mv = c3.get("diagnosticos", {}).get("multiverso", {}).get(h, {})
        alt = ""
        if jt is not None:
            sub = jt[jt["hipotesis"] == h].head(2)
            alt = "; ".join(f"{r.especificacion.split(':')[0]} {_f(100 * r.coef)} % [{_f(100 * r.ic95_lo)}; "
                            f"{_f(100 * r.ic95_hi)}] ({r.clasificacion if isinstance(r.clasificacion, str) else 's/c'})"
                            for r in sub.itertuples())
        mag = (f"Principal (Callaway-Sant'Anna, fianzas Incasòl, {que}): {_f(e['CS']['pct'])} % {_iv(e['CS']['pct_ic95'])} "
               f"(p {_f(e['CS']['p'], 3)}). Validación sellada por fuente (SERPAVI, stock): {_f(e['sellado']['pct'], 2)} % "
               f"{_iv(e['sellado']['pct_ic95'], 2)}, p_Holm {_f(holm.get(h), 3)}. Estimadores alternativos y réplica de "
               f"JMS (objetivo {objetivo}): {alt or 'n/d'}. Multiverso: {_f(100 * mv.get('prop_mismo_signo', float('nan')), 0)} % "
               f"mismo signo, {_f(100 * mv.get('prop_signif_5pct', float('nan')), 0)} % significativas. Capa {capa['capa']} "
               f"({capa.get('fallo', '')}).")
        return dict(id=fid, tema="Topes de alquiler", enunciado=enunciado, capa=capa["capa"], magnitud=mag,
                    intervalo=_iv(e["CS"]["pct_ic95"]) + " % (principal)", cota="—",
                    literatura=f"{LIT['JMS']}; {LIT['DIAMOND']} (calibración, San Francisco).",
                    veredicto="RESPALDADA" if capa["capa"] == "C3" and e["CS"]["ic95"][1] < 0 else "SIN EVIDENCIA SUFICIENTE",
                    regla=("RESPALDADA solo con C3 robusto; con capa C4 el veredicto es SIN EVIDENCIA SUFICIENTE aunque "
                           "las estimaciones C4 apunten en una dirección (no se promueve de capa)."),
                    limites=("Un solo episodio (Cataluña, 2020Q4-2022Q1). La validación por fuente mide un stock (SERPAVI) "
                             "en los mismos municipios: no es independiente y su magnitud es menor que la principal."),
                    evidencia=["output/v3/C3/resultado.json", "output/v3/C3/tabla_replicacion_jms.csv", "output/v3/holm_v3.csv"])

    out.append(ficha_tope("H3-3a", "V06", "Los topes al precio del alquiler bajan los alquileres.", "−4,5 %",
                          "renta de los contratos nuevos"))
    out.append(ficha_tope("H3-3b", "V07", "Los topes al precio del alquiler reducen la oferta de vivienda en alquiler.",
                          "−0,3 % en contratos", "número de contratos nuevos"))

    # ---------------------------------------------------------------- V08 vacías
    a3 = PA.get("A3_vacias_tercil_alto_vs_bajo", {})
    out.append(dict(
        id="V08", tema="Viviendas vacías",
        enunciado="Hay millones de viviendas vacías que se podrían movilizar para resolver el problema.",
        capa="C1",
        magnitud=("Censo 2021: 3,83 millones de viviendas vacías (estimación por consumo eléctrico, fuente única, C4). "
                  "Sobre los 277 municipios con dato, el 27,5-40,3 % de las vacías está en el tercil alto de presión de "
                  "precios y el 20,7-28,3 % en el tercil bajo (C1, dos medidas)."),
        intervalo="27,5-40,3 % en el tercil alto de presión (277 municipios)",
        cota="—", literatura="—",
        veredicto="PARCIALMENTE",
        regla=("La cifra de millones es de fuente única (C4); el reparto por presión (C1) sitúa en el tercil alto entre "
               "el 27,5 % y el 40,3 %; la fracción movilizable es un supuesto (P-D). PARCIALMENTE: hay muchas vacías, "
               "pero su movilización para «resolver» no está evaluada."),
        limites="Vacía por consumo eléctrico incluye viviendas en venta, en obras o en herencias; independencia parcial de las dos medidas.",
        evidencia=["output/v3/PA/hechos.json#A3", "output/v3/PD/resultados.json"],
    ))

    # ---------------------------------------------------------------- V09 ocupación ilegal
    out.append(dict(
        id="V09", tema="Seguridad jurídica",
        enunciado="La ocupación ilegal de viviendas y la inseguridad jurídica retraen la oferta de alquiler.",
        capa="C4", magnitud="Sin datos de ocupaciones por municipio y periodo en las fuentes reunidas.",
        intervalo="n/d", cota="—", literatura="Sin trabajo verificado incorporado.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla="Sin medida del fenómeno ni diseño, no se puede evaluar.",
        limites="Requeriría datos judiciales o policiales a escala municipal.",
        evidencia=["docs/v3/fuentes_fallidas.md"],
    ))

    # ---------------------------------------------------------------- V10 ITP / IVA
    out.append(dict(
        id="V10", tema="Fiscalidad",
        enunciado="Bajar el ITP o el IVA de la vivienda la abarataría para los compradores.",
        capa="C4", magnitud="Sin diseño propio; la incidencia depende de la elasticidad de la oferta (no estimada aquí).",
        intervalo="n/d", cota="—", literatura="Sin trabajo de incidencia verificado incorporado.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla=("La incidencia depende de la elasticidad de la oferta: si fuera baja, parte de la rebaja podría trasladarse al "
               "precio; sin estimación no se puede cuantificar ni fijar su signo neto para el comprador."),
        limites="Los cambios autonómicos del ITP permitirían un diseño de diferencias (no realizado).",
        evidencia=[],
    ))

    # ---------------------------------------------------------------- V11 vivienda pública
    pd_ = ev["PD"] or []
    pub = [x for x in pd_ if "públic" in str(x.get("politica", "")).lower()]
    out.append(dict(
        id="V11", tema="Vivienda pública",
        enunciado="Construir vivienda pública resolvería el problema de la vivienda.",
        capa="C4" if not pub else min(x.get("capa", "C4") for x in pub),
        magnitud=("; ".join(f"{x['metrica']}: {_iv([x['rango_min'], x['rango_max']])} {x['unidad']}" for x in pub[:3])
                  or "Simulación P-D no disponible."),
        intervalo="ver magnitud", cota="—", literatura="Calibración con la literatura de P-D.",
        veredicto="PARCIALMENTE" if pub else "SIN EVIDENCIA SUFICIENTE",
        regla=("Según supuestos: en P-D la vivienda pública reduce el esfuerzo de acceso o lo deja igual (≤ 0; nulo si "
               "desplaza por completo a la construcción privada, ρ = 1); con 10.000-25.000 viviendas/año queda lejos de "
               "la brecha de 104.000-413.000 viviendas/año, de modo que «resolver» depende del volumen y del desplazamiento."),
        limites="Simulación con rangos de elasticidades; coste fiscal no cuantificado sin dato de coste.",
        evidencia=["output/v3/PD/resultados.json"],
    ))

    # ---------------------------------------------------------------- V12 tipos de interés
    b4a, b4b = PB.get("B4-nac-2014-2021", {}), PB.get("B4-nac-2021-2025", {})
    out.append(dict(
        id="V12", tema="Tipos de interés",
        enunciado="Los tipos de interés son la causa principal de la subida de los precios de la vivienda (≥50 % de la subida).",
        capa="C4",
        magnitud=(f"Con el supuesto estructural P/R = 1/coste de uso (C4): 2014-2021, Δln(1/uc) = +{_f(b4a.get('cota_superior'))} % "
                  f"(rango {_iv([b4a.get('sensibilidad_min'), b4a.get('sensibilidad_max')])} %), por encima de la subida del precio "
                  f"de compra; 2021-2025, Δln(1/uc) = {_f(b4b.get('cota_superior'))} %, de signo contrario a la subida de precios. "
                  "Sobre el alquiler no se calcula cota."),
        intervalo=f"2014-2021 {_iv([b4a.get('sensibilidad_min'), b4a.get('sensibilidad_max')])} %; 2021-2025 {_iv([b4b.get('sensibilidad_min'), b4b.get('sensibilidad_max')])} %",
        cota="C4: traducción a precio con un supuesto estructural (mismo estándar que la vía ε de V01 y V03).",
        literatura=f"{LIT['POTERBA']} para el coste de uso.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla=("Regla común (i)-(iv), con el mismo estándar que V01 y V03: toda traducción de una cota a precio que descansa en "
               "un supuesto estructural no estimado (ε en V01/V03; P/R = 1/uc aquí) es C4 y no decide. Con ese supuesto, la "
               "afirmación sería incompatible con 2021-2025 y no descartada en 2014-2021."),
        limites="Estado estacionario; depende del suelo del coste de uso y de la ganancia esperada.",
        evidencia=["output/v3/PB/cotas.json#B4"],
    ))

    # ---------------------------------------------------------------- V13 burbuja
    a4 = PA.get("A4_precio_renta_nacional_2023", {})
    a6 = PA.get("A6_ratio_precio_alquiler_2015_2024", {})
    out.append(dict(
        id="V13", tema="Burbuja",
        enunciado="Hay una burbuja en el precio de la vivienda en España.",
        capa="C4",
        magnitud=(f"Precio/renta 2023: {_iv(a4.get('intervalo'))} veces la renta anual; la dirección de la razón "
                  f"precio/alquiler 2015-2024 no está establecida (medidas de signo contrario: {_iv(a6.get('intervalo'))} %)."),
        intervalo="n/d", cota="—", literatura="Sin test de exuberancia (GSADF) realizado en v3.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla="Sin test de exuberancia y con indicadores de valoración contradictorios, no se puede afirmar ni descartar.",
        limites="El test GSADF por CCAA estaba previsto en P-E (exploratorio) y no se ejecutó.",
        evidencia=["output/v3/PA/hechos.json#A4", "output/v3/PA/hechos.json#A6"],
    ))

    # ---------------------------------------------------------------- V14 compradores extranjeros
    ex = ev["extranjeros"]
    out.append(dict(
        id="V14", tema="Compradores extranjeros",
        enunciado="Los compradores extranjeros encarecen la vivienda en España.",
        capa="C1" if ex else "C4",
        magnitud=(f"Cuota de compraventas por personas de nacionalidad extranjera 2023-2025: {_iv(ex['intervalo'])} % "
                  f"(MIVAU {_f(ex['mivau_min'])}-{_f(ex['mivau_max'])} %; Registradores {_f(ex['registradores_min'])}-"
                  f"{_f(ex['registradores_max'])} %). Su efecto sobre el precio no se ha estimado."
                  if ex else "Sin datos."),
        intervalo=_iv(ex["intervalo"]) + " % de las compraventas" if ex else "n/d",
        cota="—", literatura="v2 (BV): sin efecto identificado.",
        veredicto="SIN EVIDENCIA SUFICIENTE",
        regla="Hay un hecho C1 sobre su peso, pero ningún diseño sobre su efecto en el precio.",
        limites="La cuota incluye residentes extranjeros; la de no residentes es menor y se concentra en zonas costeras.",
        evidencia=["data/processed (nacional_q_v2 vía holdout.load_full)"],
    ))
    return out


def ficha_md(f: dict) -> str:
    return (f"## {f['id']} · {f['tema']}\n\n**Afirmación:** {f['enunciado']}\n\n"
            f"| Campo | Contenido |\n|---|---|\n| Veredicto | **{f['veredicto']}** |\n| Capa de la evidencia | {f['capa']} |\n"
            f"| Magnitud | {f['magnitud']} |\n| Intervalo | {f['intervalo']} |\n| Cota | {f['cota']} |\n"
            f"| Literatura | {f['literatura']} |\n| Regla del veredicto | {f['regla']} |\n| Límites | {f['limites']} |\n"
            f"| Evidencia | {', '.join(f['evidencia']) or '—'} |\n")


def main() -> list[dict]:
    ev = cargar()
    fs = fichas(ev)
    (DEST / "fichas").mkdir(parents=True, exist_ok=True)
    for f in fs:
        (DEST / "fichas" / f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1))
    cab = ("# Verificador de afirmaciones sobre la vivienda en España (v3)\n\n"
           "Generado por `make verificador` a partir de output/v3. Cada ficha evalúa la afirmación, no a quien la "
           "formula. Capas: C1 hechos (≥2 fuentes), C2 cotas, C3 efectos con identificación, C4 exploratorio.\n\n"
           "| Id | Afirmación | Veredicto | Capa |\n|---|---|---|---|\n"
           + "".join(f"| {f['id']} | {f['enunciado']} | {f['veredicto']} | {f['capa']} |\n" for f in fs) + "\n")
    (DEST / "verificador.md").write_text(cab + "\n".join(ficha_md(f) for f in fs), encoding="utf-8")
    pd.DataFrame([{k: f[k] for k in ("id", "tema", "enunciado", "veredicto", "capa")} for f in fs]).to_csv(
        DEST / "resumen.csv", index=False)
    return fs


if __name__ == "__main__":
    for f in main():
        print(f["id"], f["veredicto"], f["capa"])
