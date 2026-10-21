"""V18 · Fase 6 · Cifras V18 difundibles para cifras_clave.

Reúne en output/v18/f6/hechos.json las cifras V18 de output/v18/estimacion/*/hechos.json y de output/v18/f5/hechos.json (570).
src/v5/cifras_clave.py lee solo este fichero de V18 (como output/v17/f5/hechos.json en V17).
Comprueba, y sale con código 1 si algo falla: ids únicos con prefijo V18-, fuente, capa C4, clasificacion_v18 válida y ninguna
palabra causal en el indicador ni en la nota (K2; mismas expresiones que check_v18). Añade:
- tipo_rango coherente con min y max: «rango» si min <= valor <= max (o falta el valor central y min <= max), «referencias» si
  min y max existen pero no encierran el valor, «sin rango» si falta alguno;
- cobertura real: el territorio de la cifra. Las coberturas que solo describen la muestra («N = 234», «4 ramas», «sin datos»,
  «—», el número de estudios de B5…) se sustituyen por el territorio del diseño, con la descripción original entre paréntesis;
- fecha_dato (último año del periodo) y ficha (el hechos.json de origen).
Además (auxiliares(), ids V18-AUX-*) copia, sin recalcular, las cifras que el Documento de Trabajo cita y que no tenían id:
valores publicados de la literatura (output/v18/f5/magnitudes_estudios.csv y fichas de docs/v18/bib), contabilidad provincial,
comparación con V8 y sensibilidad de B5 (output/v18/f5), reproducciones (output/v18/reproduccion), Monte Carlo
(output/v18/montecarlo), variantes de E1 y E2 (output/v18/estimacion), recuentos del catálogo (output/v18/f1) y cuotas por
subperiodo de V17-D3 (output/v17/d3; las del periodo completo ya son V17-D3-VARIANZA-COMUN-* y no se duplican). Las únicas
operaciones son selección de filas, recuentos, mínimo y máximo de filas ya publicadas, el cambio de unidad de proporción a %
y la transformación 100·(exp(b)−1) de E2-R1, marcada como tal.
Determinista; sin red; solo lee salidas ya generadas (output/v17, output/v18) y fichas (docs/v18/bib).
Uso: python3 src/v18/f6_hechos.py
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import check_v18  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"   # solo lee salidas V17/V18 ya generadas y fichas (guarda de fuga v6 de check_v17)
OUT = RAIZ / "output" / "v18"
BIB = RAIZ / "docs" / "v18" / "bib"
SALIDA = OUT / "f6" / "hechos.json"
FECHA = "2026-10-20"
N_BASE = 487          # cifras de los hechos.json de estimación y de f5 (570 en K12; K14: −87 filas «no explicado» de la ilustración, +4 OBS)
N_AUX = 163           # cifras V18-AUX-* de auxiliares() (135 de K11, 27 de K12 y 1 de K14: V18-AUX-F1-OOS-GW-P)
N_ESPERADO = N_BASE + N_AUX
TIPOS_RANGO = ("rango", "referencias", "sin rango")

# Territorio del diseño de cada estimación (docs/v18/plan_replicacion.md), para las coberturas que solo describen la muestra.
TERRITORIO = {
    "E1-A2": "Málaga y Sevilla (municipios)", "E1-X1": "Barcelona (barrios)", "E1": "ciudades españolas con registro de viviendas turísticas",
    "E2": "Cataluña (municipios)", "E3": "España (provincias)", "E4": "España", "E5": "España (provincias)",
    "E6-A2": "España sin la provincia de València (secciones)", "E6": "España (provincias)", "E7": "España",
    "E8": "España (comunidades autónomas)", "E9": "España", "E10": "España (municipios)", "E11": "España",
    "E12": "España (provincias)", "F1": "España", "F2": "España", "F3": "España", "F4": "España",
}
TERR = re.compile(r"nacional|españa|provincia|municipi|secci|barrio|ccaa|comunidad|país|orígen|origen|barcelona|cataluña|"
                  r"valència|andaluc|castilla|galicia|extremadura|vasco|distrit|controles|tratados|ciudad", re.I)


def tipo_rango(h: dict) -> str:
    mn, mx, v = h.get("min"), h.get("max"), h.get("valor")
    if mn is None or mx is None:
        return "sin rango"
    if mn > mx:
        return "referencias"
    if v is None or mn - 1e-12 <= v <= mx + 1e-12:
        return "rango"
    return "referencias"


def _paises_b5() -> dict[str, str]:
    """Países de los estudios que entran en la magnitud preferida de cada factor (output/v18/f5/magnitudes_estudios.csv)."""
    p = OUT / "f5" / "magnitudes_estudios.csv"
    res: dict[str, list[str]] = {}
    if p.exists():
        with p.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("entra_en_B5") == "sí" and r.get("pais"):
                    for x in re.split(r"\s*[;,/]\s*", r["pais"]):
                        if x and x not in res.setdefault(r["factor"], []):
                            res[r["factor"]].append(x)
    return {f: ", ".join(v) for f, v in res.items()}


def cobertura_real(h: dict, paises: dict[str, str]) -> str:
    c = re.sub(r"[;\s]+$", "", str(h.get("cobertura") or "").strip())
    i = str(h["id"])
    if i.startswith("V18-AUX-") and c:   # auxiliares: la cobertura ya es el territorio (o la simulación) de la fila de origen
        return c
    m = re.match(r"V18-B5-(E\d+)", i)
    if m:   # B5: magnitud de la literatura y, en su caso, estimación propia; la cobertura es la de los estudios
        # K14 (árbitro, ronda 2, N1): frase completa con mayúscula inicial y sin paréntesis anidados (el documento la cita sola)
        if m.group(1) in paises:
            return f"Estudios de {paises[m.group(1)]}: {c}" if c else f"Estudios de {paises[m.group(1)]}"
        resto = "; ".join(x for x in c.split("; ") if x and not x.startswith("ningún estudio"))
        terr = "Literatura sin estudios con error típico en la unidad"
        return f"{terr}; {resto}" if resto else terr
    if c and TERR.search(c):
        return c
    e = re.match(r"V18-((?:E|F)\d+)(?:-([A-Z]+\d+))?", i)
    terr = "España"
    if e:
        terr = TERRITORIO.get(f"{e.group(1)}-{e.group(2)}", TERRITORIO.get(e.group(1), "España"))
    if not c or c in ("—", "-", "no estimada"):
        return f"{terr} (no estimada)"
    if c.startswith(("sin ", "no ")):
        return f"{terr} (no estimada: {c})"
    return f"{terr} ({c})"


def fuentes_hechos() -> list[Path]:
    return sorted((OUT / "estimacion").glob("*/hechos.json")) + [OUT / "f5" / "hechos.json"]


# ---------------------------------------------------------------------------------------------------------------------------
# Cifras auxiliares V18-AUX-* (citadas en el Documento de Trabajo; copiadas de su salida de origen, sin recalcular)
# ---------------------------------------------------------------------------------------------------------------------------
NOTA_LIT = "magnitud de la literatura ({estado}); valor del autor en su unidad, sin conversión; no es estimación del proyecto"
_PREPLAN = "docs/v18/plan_replicacion.md + plan_replicacion_adenda.md (pre-registro interno plan-replicacion-v18)"


def _f(x) -> float | None:
    """Número o None (NaN, vacío o texto no numérico)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else float(f"{v:.10g}")   # 10 cifras significativas: quita el ruido de coma flotante


def _qant(p: str) -> str:
    """Trimestre anterior a «AAAATn» (nivel de partida de un periodo; el primero de la serie, 1995T1, es su propio nivel)."""
    y, q = int(p[:4]), int(p[-1])
    return p if p == "1995T1" else (f"{y - 1}T4" if q == 1 else f"{y}T{q - 1}")


def _cifra(i: str, indicador: str, valor, unidad: str, periodo: str, cobertura: str, fuentes: list[str], clase: str, nota: str,
           ficha: str, mn=None, mx=None) -> dict:
    return {"id": i, "indicador": indicador, "valor": _f(valor), "min": _f(mn), "max": _f(mx), "unidad": unidad,
            "periodo": periodo, "cobertura": cobertura, "fuentes": fuentes, "capa": "C4", "clasificacion_v18": clase,
            "nota": nota, "ficha": ficha}


def _rel(p: Path) -> str:
    return str(p.relative_to(RAIZ))


def _num_es(s: str) -> float:
    return float(s.replace(".", "").replace(",", ".")) if "," in s else float(s)


def _buscar(texto: str, patron: str, donde: str) -> re.Match:
    m = re.search(patron, texto)
    if not m:
        raise ValueError(f"{donde}: no se encuentra «{patron}» (la ficha cambió: revisar auxiliares())")
    return m


def _fichas_bib() -> dict[str, Path]:
    return {p.stem: p for p in BIB.glob("*/*.md")}


def _aux_literatura() -> list[dict]:
    """Valor publicado y error típico de cada estudio de la literatura (magnitudes_estudios.csv), con la ficha como fuente."""
    src = OUT / "f5" / "magnitudes_estudios.csv"
    fichas = _fichas_bib()
    res = []
    for r in pd.read_csv(src).itertuples():
        if str(r.estado_ficha).startswith("estimación propia") or _f(r.valor) is None:
            continue
        clave = re.sub(r"[^A-Z0-9]+", "-", str(r.estudio).upper()).strip("-")
        ficha = _rel(fichas[r.estudio]) if r.estudio in fichas else _rel(src)
        lugar = str(r.referencia).split("), ", 1)[-1]
        per = re.findall(r"\d{4}(?:T\d)?-\d{4}", lugar) or re.findall(r"\((\d{4})", str(r.referencia))
        nota = NOTA_LIT.format(estado=r.estado_ficha) + f"; entra en la magnitud preferida (B5): {r.entra_en_B5}"
        comun = dict(unidad=str(r.unidad_del_autor), periodo=per[-1] if per else str(r.referencia),
                     cobertura=f"{r.pais}: {lugar}", fuentes=[ficha, _rel(src)], clase="NO ESTIMABLE", ficha=ficha)
        res.append(_cifra(f"V18-AUX-LIT-{clave}", f"Valor publicado por {r.referencia} (factor {r.factor}, literatura)", r.valor,
                          nota=nota, **comun))
        if _f(r.error_tipico) is not None:
            res.append(_cifra(f"V18-AUX-LIT-{clave}-ET", f"Error típico del valor publicado por {r.referencia} (factor {r.factor})",
                              r.error_tipico, nota=nota + f"; origen del error: {r.origen_error}", **comun))
    return res


def _aux_fichas() -> list[dict]:
    """García-López et al. (2020) y González y Ortega (2009, 2011, 2013): cifras del texto de los autores, leídas de la ficha."""
    f = _fichas_bib()
    res = []
    gl = f["garcialopez2020"]
    t = gl.read_text(encoding="utf-8")
    m = _buscar(t, r"barrio medio \(nivel de 2016\): \+(\d+(?:,\d+)?) % en alquileres", _rel(gl))
    d = _buscar(t, r"decil superior de actividad: \+(\d+(?:,\d+)?) %", _rel(gl))
    comun = dict(unidad="% del alquiler anunciado (valor de los autores)", periodo="2016",
                 cobertura="Barcelona (áreas estadísticas básicas)", fuentes=[_rel(gl)], clase="NO ESTIMABLE", ficha=_rel(gl))
    nota = NOTA_LIT.format(estado="VERIFICADA") + "; cifra del resumen de los autores (p. 1)"
    res.append(_cifra("V18-AUX-LIT-GL2020-BARRIO-MEDIO", "Variación del alquiler asociada a Airbnb en el barrio medio según "
                      "García-López et al. (2020), Barcelona", _num_es(m.group(1)), nota=nota, **comun))
    res.append(_cifra("V18-AUX-LIT-GL2020-DECIL-ALTO", "Variación del alquiler asociada a Airbnb en el decil de mayor actividad "
                      "según García-López et al. (2020), Barcelona", _num_es(d.group(1)), nota=nota, **comun))
    iza = f["gonzalez_ortega_2009_iza"]
    t = iza.read_text(encoding="utf-8")
    b = _buscar(t, r"(\d+(?:,\d+)?) euros/m² por cada punto de población de entrada de extranjeros, error típico (\d+(?:,\d+)?)", _rel(iza))
    a = _buscar(t, r"eleva el precio en torno al (\d+)%", _rel(iza))
    comun = dict(periodo="1998-2008", cobertura="España (50 provincias)", fuentes=[_rel(iza)], clase="NO ESTIMABLE", ficha=_rel(iza))
    nota = NOTA_LIT.format(estado="NO VERIFICADA") + "; versión IZA de 2009 de González y Ortega"
    res.append(_cifra("V18-AUX-LIT-GO2009-EUR", "Coeficiente de la entrada de extranjeros sobre el precio en la versión IZA de "
                      "2009 de González y Ortega (tabla 3, panel IV, col. 5)", _num_es(b.group(1)),
                      unidad="€/m² por punto de población", nota=nota, **comun))
    res.append(_cifra("V18-AUX-LIT-GO2009-EUR-ET", "Error típico del coeficiente de la versión IZA de 2009 de González y Ortega",
                      _num_es(b.group(2)), unidad="€/m² por punto de población", nota=nota, **comun))
    res.append(_cifra("V18-AUX-LIT-GO2009-PRECIO-ACUM", "Aumento acumulado del precio asociado a la entrada media de "
                      "extranjeros en la versión IZA de 2009 de González y Ortega (extrapolación lineal de los autores)",
                      _num_es(a.group(1)), unidad="% del precio", nota=nota + "; no es una fracción de la subida observada", **comun))
    chi = f["gonzalez_ortega_2011_chicagofed"]
    t = chi.read_text(encoding="utf-8")
    c = _buscar(t, r"en torno al (\d+)% del aumento de precios", _rel(chi))
    res.append(_cifra("V18-AUX-LIT-GO2011-FRACCION", "Fracción del aumento de precios asociada a la inmigración según la versión "
                      "Chicago Fed de 2011 de González y Ortega (resumen)", _num_es(c.group(1)), unidad="% del aumento de precios",
                      periodo="2001-2010", cobertura="España (provincias)", fuentes=[_rel(chi)], clase="NO ESTIMABLE",
                      nota=NOTA_LIT.format(estado="NO VERIFICADA") + "; cifra del resumen de los autores", ficha=_rel(chi)))
    go = f["gonzalez_ortega_2013"]
    t = go.read_text(encoding="utf-8")
    _buscar(t, r"un cuarto del aumento de precios", _rel(go))
    cat = pd.read_csv(OUT / "f1" / "catalogo.csv")
    estado = str(cat.loc[cat.fichero == "gonzalez_ortega_2013.md", "estado"].iloc[0])
    res.append(_cifra("V18-AUX-LIT-GO2013-FRACCION", "Fracción del aumento de precios asociada a la inmigración según la edición "
                      "de 2013 de González y Ortega (resumen: «un cuarto»)", 25, unidad="% del aumento de precios",
                      periodo="2000-2010", cobertura="España (provincias)", fuentes=[_rel(go)], clase="NO ESTIMABLE",
                      nota=NOTA_LIT.format(estado=estado) + "; «un cuarto» del resumen escrito como 25 % (transcripción, sin cálculo)",
                      ficha=_rel(go)))
    return res


def _aux_f5() -> list[dict]:
    res = []
    # Contabilidad provincial: rango entre provincias de la variación observada relativa (la no explicada es idéntica)
    src = OUT / "f5" / "contabilidad.csv"
    c = pd.read_csv(src)
    p = c[c.territorio_tipo == "provincia"]
    obs = p[p.tipo_fila == "observado"].set_index(["resultado", "periodo", "territorio"]).obs_pp
    noe = p[p.tipo_fila == "no_explicado"].set_index(["resultado", "periodo", "territorio"]).contrib_med
    if not ((obs - noe.reindex(obs.index)).abs().fillna(0) < 1e-9).all():
        raise ValueError("contabilidad.csv: la variación no explicada provincial ya no es igual a la observada (revisar el texto)")
    fu = [_rel(src), "output/v18/f5/informe.md"]
    ven = p[p.tipo_fila == "observado"].set_index(["resultado", "periodo", "territorio"]).ventana_factor
    nprov = int(p.territorio.nunique())
    res.append(_cifra("V18-AUX-CONT-PROV-N", "Provincias no selladas con detalle de contabilidad (variación observada y sin explicar)",
                      nprov, unidad="provincias", periodo="1995-2026", cobertura="España (provincias no selladas)", fuentes=fu,
                      clase="NO ESTIMABLE", nota="recuento de provincias de contabilidad.csv", ficha=_rel(src)))
    for (res_, per), g in obs.dropna().groupby(level=[0, 1]):
        k = f"V18-AUX-CONT-PROV-{res_.upper()}-{per}"
        # periodo real del dato (K12, árbitro, hallazgo 1): las provincias pueden empezar después del inicio del periodo del plan
        ini = ven.loc[g.index].str.slice(0, 6).value_counts()
        base = f"{_qant(per.split('-')[0])}"
        per_real, aviso = per, ""
        if ini.index[0] not in (per.split("-")[0], base):
            per_real = f"{ini.index[0]}-{per.split('-')[1]}"
        if len(ini) > 1:
            aviso = ("; la media provincial mezcla ventanas (" + "; ".join(f"{n} provincias desde {i}" for i, n in ini.items())
                     + "): las provincias de ventana distinta no son comparables con el resto")
        res.append(_cifra(k, f"Variación observada del {res_} real relativa a la media de las provincias no selladas, {per_real}: mínimo "
                          "y máximo entre provincias (igual a la variación sin explicar)", None, unidad="puntos (100·Δln)",
                          periodo=per_real, cobertura=f"España ({len(g)} provincias no selladas)", fuentes=fu, clase="NO ESTIMABLE",
                          nota="mínimo y máximo de obs_pp entre provincias; ningún factor tiene magnitud preferida con estimación "
                          "propia, por lo que la variación sin explicar coincide con la observada; relativa a la media simple de las "
                          f"provincias no selladas con dato, sin el componente común{aviso}", ficha=_rel(src),
                          mn=g.min(), mx=g.max()))
    # Comparación con V8
    src = OUT / "f5" / "comparacion_v8.csv"
    v = pd.read_csv(src)
    ambos = v[v.v18_mediana.notna() & v.v8_mediana.notna()]
    sig = ambos.mismo_signo.astype(str).str.lower().eq("true")
    sol = ambos.intervalos_solapan.astype(str).str.lower().eq("true")
    fact = ", ".join(sorted(ambos.factor_v18.unique()))
    comun = dict(unidad="comparaciones", periodo="1995-2026", cobertura="España", fuentes=[_rel(src)], clase="NO ESTIMABLE",
                 ficha=_rel(src))
    nota = f"recuento de filas de comparacion_v8.csv con cifra en V8 y en V18 (factores {fact})"
    res.append(_cifra("V18-AUX-V8-N", "Comparaciones con V8 con cifra en ambos lados", len(ambos), nota=nota, **comun))
    res.append(_cifra("V18-AUX-V8-SIGNO", "Comparaciones con V8 en las que el signo coincide", int(sig.sum()), nota=nota, **comun))
    res.append(_cifra("V18-AUX-V8-SOLAPE", "Comparaciones con V8 en las que las bandas se solapan", int(sol.sum()), nota=nota, **comun))
    # Sensibilidad de B5: estrategia B de Hahn et al. en E2
    src = OUT / "f5" / "sensibilidad_b5.csv"
    s = pd.read_csv(src)
    r = s[(s.factor == "E2") & (s.variante == "hahn_estrategia_B")].iloc[0]
    res.append(_cifra("V18-AUX-B5-E2-HAHN-B", "Magnitud preferida de topes al alquiler (E2) con la estrategia B de Hahn et al. "
                      "(sensibilidad de B5)", r.mu, unidad="log de la renta de los contratos regulados", periodo="2016-2024",
                      cobertura=f"estudios de España, Francia y Alemania ({r.unidades})", fuentes=[_rel(src)], clase="NO ESTIMABLE",
                      nota=f"sensibilidad: {r.estado}; I² {r.I2}; no cambia la tabla de magnitudes preferidas (regla fijada antes "
                      "de combinar)", ficha=_rel(src), mn=r.lo, mx=r.hi))
    return res


def _aux_reproduccion() -> list[dict]:
    res = []
    base = OUT / "reproduccion"
    # Borusyak, Hull y Jaravel (2022): conjunto de controles 5 (el de resultado.json); IC con el nulo impuesto, publicado y propio
    d = base / "borusyak_hull_jaravel_2022"
    t = pd.read_csv(d / "tabla.csv")
    r = t[t.conjunto_controles == 5].iloc[0]
    rj = json.loads((d / "resultado.json").read_text(encoding="utf-8"))
    comun = dict(unidad="coeficiente IV (ADH 2013, nivel de choque)", periodo="1990-2007",
                 cobertura=f"Estados Unidos ({int(r.n_py)} zonas de desplazamiento por periodo)",
                 fuentes=[_rel(d / "tabla.csv"), _rel(d / "resultado.json"), _rel(d / "informe.md")], clase="NO ESTIMABLE",
                 ficha=_rel(d / "resultado.json"))
    nota = "reproducción del estudio original con los datos de sus autores (no usa datos del proyecto); conjunto de controles 5; " \
           f"IC95 por inversión con el nulo impuesto; veredicto: {r.veredicto_beta}"
    res.append(_cifra("V18-AUX-REP-BHJ-PUB", "Coeficiente publicado por Borusyak, Hull y Jaravel (2022), con su IC95", r.beta_pub,
                      nota=nota, mn=r.ic_nulo_pub_izq, mx=r.ic_nulo_pub_der, **comun))
    res.append(_cifra("V18-AUX-REP-BHJ-REP", "Coeficiente reproducido de Borusyak, Hull y Jaravel (2022), con su IC95", r.beta_py,
                      nota=nota, mn=r.ic_nulo_py_izq, mx=r.ic_nulo_py_der, **comun))
    assert rj["N"] == int(r.n_py)
    # Chaves-Fonseca (2026), columna 6 (IV); Mense (2025), columna 3 (IV)
    for clave, carpeta, fila, col_pub, col_se, col_rep, unidad, periodo, cob in (
            ("CHAVES", "chavesfonseca2026", lambda t: t[t.columna == 6].iloc[0], "coef_publicado", "se_publicado", "coef_repro",
             "ln del precio por 100 anuncios en el barrio (IV)", "2010-2018", "Madrid (barrios), 1.029 observaciones barrio-año"),
            ("MENSE", "mense_2025", lambda t: t[(t.columna == 3) & t.parametro.str.startswith("oferta_nueva")].iloc[0],
             "publicado", "se_publicado", "reproducido", "elasticidad del alquiler respecto a la oferta nueva (IV)", "2011-2018",
             "Alemania (94 regiones de planificación)")):
        d = base / carpeta
        r = fila(pd.read_csv(d / "tabla.csv"))
        rj = json.loads((d / "resultado.json").read_text(encoding="utf-8"))
        comun = dict(unidad=unidad, periodo=periodo, cobertura=cob,
                     fuentes=[_rel(d / "tabla.csv"), _rel(d / "resultado.json"), _rel(d / "informe.md")], clase="NO ESTIMABLE",
                     ficha=_rel(d / "resultado.json"))
        nota = "reproducción del estudio original con los datos de su autor (no usa datos del proyecto); " \
               f"veredicto: {r.veredicto}"
        ref = "Chaves-Fonseca (2026)" if clave == "CHAVES" else "Mense (2025)"
        res.append(_cifra(f"V18-AUX-REP-{clave}-PUB", f"Coeficiente publicado por {ref}", r[col_pub], nota=nota, **comun))
        res.append(_cifra(f"V18-AUX-REP-{clave}-PUB-ET", f"Error típico publicado por {ref}", r[col_se], nota=nota, **comun))
        res.append(_cifra(f"V18-AUX-REP-{clave}-REP", f"Coeficiente reproducido de {ref}, con su IC95", r[col_rep], nota=nota,
                          mn=rj["ic95"][0], mx=rj["ic95"][1], **comun))
    return res


# Filas que deciden el veredicto de cada herramienta (columna «principal», «entra_en_veredicto» o «decisivo» cuando existe;
# si no, la variante principal que nombra su resultado.json, en el horizonte decisivo h = 8 cuando lo hay).
MC_FILAS = {
    "aleatorizacion": lambda t: t.variante.str.contains("(plan)", regex=False),
    "cs_webb": lambda t: t.variante == "webb_WCR_t_cluster_principal",
    "sa_webb": lambda t: t.variante == "webb_WCR_t_cluster_principal",
    "dcdh_aleatorizacion": lambda t: t.variante == "aleatorizacion_estudentizada",
    "sdid_conley_taber": lambda t: t.variante == "conley_taber_sdid",
    "lp_iv": lambda t: t.variante.isin(["AR_aumentado_EHW", "2SLS_NeweyWest_h+1", "2SLS_aumentado_EHW"]) & (t.h == 8),
    "svar_proxy": lambda t: t.variante.isin(["AR_delta_NeweyWest4", "Wald_delta"]) & (t.h == 8),
    # K14 (árbitro, ronda 2, N2): la herramienta es Webb; las filas CR1 de la misma tabla son otra inferencia
    "webb_twfe": lambda t: _verdadero(t.principal) & t.inferencia.astype(str).str.startswith("wild cluster bootstrap (Webb)"),
}
DIAG_MC = "(diagnóstico)"   # K14 (N2): los escenarios de diagnóstico no deciden el veredicto y no entran en el mínimo y el máximo


def _verdadero(s: pd.Series) -> pd.Series:
    return s.astype(str).str.lower().isin(["true", "1", "sí"])


def _aux_montecarlo() -> list[dict]:
    res = []
    for d in sorted(p for p in (OUT / "montecarlo").iterdir() if (p / "tabla.csv").exists()):
        t = pd.read_csv(d / "tabla.csv")
        rj = json.loads((d / "resultado.json").read_text(encoding="utf-8"))
        if d.name in MC_FILAS:
            sel, criterio = MC_FILAS[d.name](t), "variante principal del resultado.json"
            if d.name == "webb_twfe":
                criterio = "filas «principal» del bootstrap de Webb; las de CR1 son otra inferencia y no entran"
        else:
            col = next(c for c in ("principal", "entra_en_veredicto", "decisivo") if c in t.columns)
            sel, criterio = _verdadero(t[col]), f"columna «{col}»"
        if "escenario" in t.columns and t.escenario.astype(str).str.contains(DIAG_MC, regex=False).any():
            sel = sel & ~t.escenario.astype(str).str.contains(DIAG_MC, regex=False)
            criterio += ", sin los escenarios de diagnóstico"
        f = t[sel]
        if f.empty:
            raise ValueError(f"{_rel(d)}: sin filas decisivas")
        diag = rj.get("diagnosticos", {})
        ver = diag.get("veredicto") or "; ".join(f"{k}: {v['veredicto']}" for k, v in diag.get("veredicto_por_inferencia", {}).items())
        clave = d.name.upper().replace("_", "-")
        comun = dict(periodo="simulación (semilla 20261010)", cobertura=f"simulación sin datos reales ({rj.get('N')})",
                     fuentes=[_rel(d / "tabla.csv"), _rel(d / "resultado.json")], clase="NO ESTIMABLE", ficha=_rel(d / "resultado.json"))
        nota = f"validación Monte Carlo; mínimo y máximo de {len(f)} filas decisivas ({criterio}); veredicto: {ver}"
        cols = [("TAM", "tamano_5pct", "Tamaño empírico al 5 %"),
                ("COB", next((c for c in ("cobertura_95", "cobertura_nulo", "cobertura_mu") if c in t.columns), None),
                 "Cobertura empírica al 95 %"),
                ("COB68", "cobertura_68", "Cobertura empírica al 68 %"), ("COB90", "cobertura_90", "Cobertura empírica al 90 %")]
        for suf, col, nombre in cols:
            if col is None or col not in t.columns or f[col].dropna().empty:
                continue
            res.append(_cifra(f"V18-AUX-MC-{clave}-{suf}", f"{nombre} de {d.name} (filas decisivas)", None, unidad="proporción",
                              nota=nota, mn=f[col].min(), mx=f[col].max(), **comun))
    return res


def _aux_estimacion() -> list[dict]:
    res = []
    # E1-R4-v3: estudio de eventos con los adelantos como regresores; IC90 de la nota de tabla.csv (inversión de Webb)
    src = OUT / "estimacion" / "e1" / "tabla.csv"
    r = pd.read_csv(src).set_index("id").loc["E1-R4-v3"]
    m = _buscar(str(r.nota), r"IC90 \((-?[\d.]+); (-?[\d.]+)\)", _rel(src))
    e1 = {h["id"]: h for h in json.loads((OUT / "estimacion" / "e1" / "hechos.json").read_text(encoding="utf-8"))}
    res.append(_cifra("V18-AUX-E1-R4-V3", "Coeficiente de E1-R4 con los adelantos de 2011-2012 como regresores (variante), con "
                      "IC90 de Webb", r.coef, unidad=e1["V18-E1-R4"]["unidad"], periodo=str(r.ventana),
                      cobertura=f"Barcelona (barrios; {r.nota.split(';')[0]})", fuentes=e1["V18-E1-R4"]["fuentes"],
                      clase=check_v18.DIAGNOSTICO, nota=f"variante [E] de E1-R4; tabla.csv y resultado.json la rotulan «{r.clase}», pero por "
                      "K8 bis la clase de E1-R4 es la de la principal (NO CONCLUYENTE) y la variante no tiene réplica ciega coincidente: "
                      "sin clase propia (K12); IC90 por inversión de Webb; IC95 en tabla.csv", ficha=_rel(src), mn=float(m.group(1)),
                      mx=float(m.group(2))))
    # E2-R1: estudio de eventos (2021T1 = k 8, base 2019T4), trayectorias por tamaño (B6b-2) y transformación porcentual
    d = OUT / "estimacion" / "e2"
    e2 = {h["id"]: h for h in json.loads((d / "hechos.json").read_text(encoding="utf-8"))}
    h = e2["V18-E2-R1"]
    tab = pd.read_csv(d / "tabla.csv").set_index("id").loc["E2-R1"]
    ev = pd.read_csv(d / "estudio_eventos.csv")
    k8 = ev[(ev.spec == "E2-R1") & (ev.k == 8)].iloc[0]
    _buscar((d / "informe.md").read_text(encoding="utf-8"), r"k = 0\.\.12 es 2019T1\.\.2022T1", _rel(d / "informe.md"))
    comun = dict(periodo="2019T1-2022T1", cobertura=h["cobertura"], fuentes=h["fuentes"])
    res.append(_cifra("V18-AUX-E2-R1-EV-2021T1", "Coeficiente de 2021T1 del estudio de eventos de E2-R1 (base 2019T4)", k8.coef,
                      unidad="log de la renta media de los contratos nuevos", nota=f"estudio de eventos de E2-R1, k = 8 (2021T1); "
                      f"error típico {k8.se}; diagnóstico de E2-R1, sin clase propia (K12)", ficha=_rel(d / "estudio_eventos.csv"),
                      clase=check_v18.DIAGNOSTICO, **comun))
    rb = pd.read_csv(d / "robustez_b6.csv").set_index("id").loc["E2-R1-B6b-2"]
    res.append(_cifra("V18-AUX-E2-R1-B6B2", "Coeficiente de E2-R1 con trayectorias trimestrales por tamaño del municipio "
                      "(ln de la población de 2019 × trimestre), con IC95", rb.coef, unidad="log de la renta media de los contratos "
                      "nuevos", nota=f"robustez a posteriori (B6b-2): {rb.descripcion}; {rb.nota}", ficha=_rel(d / "robustez_b6.csv"),
                      mn=rb.ic95_lo, mx=rb.ic95_hi, clase=check_v18.ROBUSTEZ_POSTERIORI, **comun))
    res.append(_cifra("V18-AUX-E2-R1-PCT", "Diferencia porcentual equivalente al coeficiente logarítmico de E2-R1", 100 * math.expm1(
                      float(tab.coef)), unidad="%", nota=f"transformación 100·(exp(b)−1) del coeficiente log {tab.coef} de "
                      "E2-R1 (tabla.csv); no es una estimación nueva", ficha=_rel(d / "tabla.csv"), clase=h["clasificacion_v18"], **comun))
    # K12 (árbitro, hallazgos 4 y 5): variantes enumeradas del multiverso, SERPAVI, sesgo indetectable de Roth, Honest DiD con M̄ = 0,5
    t = pd.read_csv(d / "tabla.csv").set_index("id")
    mv = t.loc[[i for i in t.index if re.fullmatch(r"E2-R1(-v\d+)?", i) and pd.notna(t.loc[i, "coef"])]]
    rj = json.loads((d / "resultado.json").read_text(encoding="utf-8"))["diagnosticos"]["E2-R1"]
    hon = next(x for x in rj["honest"] if x["Mbar"] == 0.5)
    v9 = t.loc["E2-R1-v9"]
    diag = dict(clase=check_v18.DIAGNOSTICO, **comun)
    res.append(_cifra("V18-AUX-E2-R1-N-REGULADOS", "Municipios sujetos a la Ley 11/2020 en la muestra de E2-R1 (sin Barcelona ciudad)",
                      tab.n_tratados, unidad="municipios", nota=f"n_tratados de tabla.csv (controles: {int(tab.n_controles)}); recuento de "
                      "la muestra de E2-R1", ficha=_rel(d / "tabla.csv"), **diag))
    res.append(_cifra("V18-AUX-E2-R1-MULTIVERSO", f"Coeficiente de E2-R1 en su multiverso enumerado (principal y {len(mv) - 1} "
                      "variantes del anexo A de la adenda): mínimo y máximo", None, unidad="log de la renta media de los contratos nuevos",
                      nota="mínimo y máximo de coef de E2-R1 y E2-R1-v1 a v11 en tabla.csv (variantes pre-registradas; no es un intervalo "
                      f"de confianza); mínimo en {mv.coef.idxmin()}, máximo en {mv.coef.idxmax()}", ficha=_rel(d / "tabla.csv"),
                      mn=mv.coef.min(), mx=mv.coef.max(), **diag))
    res.append(_cifra("V18-AUX-E2-R1-SERPAVI", "Coeficiente de la variante de E2-R1 con el alquiler mediano de SERPAVI por municipio "
                      "(anual 2016-2021), con IC95", v9.coef, unidad="log del alquiler mediano de SERPAVI (stock de contratos)",
                      nota=f"variante E2-R1-v9 de tabla.csv ({v9.nota}); SERPAVI mide la renta del stock de contratos, no la de los "
                      "contratos nuevos", ficha=_rel(d / "tabla.csv"), mn=v9.ic95_lo, mx=v9.ic95_hi,
                      **{**diag, "periodo": "2016-2021"}))
    res.append(_cifra("V18-AUX-E2-R1-ROTH-SESGO", "Sesgo en la ventana posterior que implicaría la pendiente previa detectable al 80 % "
                      "(potencia de Roth) en E2-R1", rj["sesgo_implicado_post"], unidad="log de la renta media de los contratos nuevos",
                      nota=f"diagnosticos.E2-R1.sesgo_implicado_post de resultado.json (pendiente detectable "
                      f"{rj['pendiente_detectable_80']:.4f} por trimestre); un sesgo de este tamaño no se detectaría con la prueba de "
                      "pretendencias", ficha=_rel(d / "resultado.json"), **diag))
    res.append(_cifra("V18-AUX-E2-R1-HONEST-M05", "Intervalo de Honest DiD de E2-R1 con M̄ = 0,5 (IC95)", None,
                      unidad="log de la renta media de los contratos nuevos", nota="diagnosticos.E2-R1.honest (M̄ = 0,5) de resultado.json; "
                      "con M̄ > 0 la herramienta es válida pero conservadora y sin potencia en el Monte Carlo (adenda 1.12): informativo, "
                      "no decide la clase", ficha=_rel(d / "resultado.json"), mn=hon["ic95"][0], mx=hon["ic95"][1], **diag))
    return res


def _aux_k12() -> list[dict]:
    """Cifras que el Documento de Trabajo cita tras la revisión de la ronda 1 (K12): F1 fuera de muestra, E1-R3, E8-R1, BVAR, umbrales."""
    res = []
    est = OUT / "estimacion"
    # F1 fuera de muestra (K1 de v6.1: «predice mejor» solo si supera a la línea base más exigente)
    src = est / "f_conjunto" / "resultado.json"
    fm = json.loads(src.read_text(encoding="utf-8"))["fuera_muestra"]
    fh = json.loads((est / "f_conjunto" / "hechos.json").read_text(encoding="utf-8"))
    fu = next(h["fuentes"] for h in fh if h["id"] == "V18-F1-R1")
    comun = dict(periodo="1999T1-2026T2", cobertura="España (nacional trimestral; bloques con embargo)", fuentes=fu + [_rel(src)],
                 clase=check_v18.DIAGNOSTICO, ficha=_rel(src))
    nota = f"fuera_muestra de resultado.json: {fm['diseno']}; {fm['n_prueba']} observaciones de prueba; misma muestra para todos los modelos"
    for k, nom in (("F1-ECM", "ECM"), ("AR(4)", "AR4"), ("ECM v1 (aprox.)", "ECMV1")):
        res.append(_cifra(f"V18-AUX-F1-OOS-RMSE-{nom}", f"RMSE fuera de muestra a un paso del modelo {k} (precio real, trimestral)",
                          fm["rmse"][k], unidad="% (variación trimestral del precio real)", nota=nota, **comun))
    res.append(_cifra("V18-AUX-F1-OOS-N", "Observaciones de prueba de la evaluación fuera de muestra de F1", fm["n_prueba"],
                      unidad="trimestres", nota=nota, **comun))
    res.append(_cifra("V18-AUX-F1-OOS-DM-P", "p del contraste de Diebold-Mariano (HLN) de F1-ECM frente a AR(4)", fm["dm_vs_ar4"]["p"],
                      unidad="p-valor", nota=nota, **comun))
    res.append(_cifra("V18-AUX-F1-OOS-CW-P", "p unilateral del contraste de Clark-West (AR(4) anidado en F1-ECM)", fm["cw"]["p_una_cola"],
                      unidad="p-valor", nota=nota, **comun))
    # K14 (árbitro, ronda 2, N7): el Giacomini-White frente al AR(4), que el documento no daba
    res.append(_cifra("V18-AUX-F1-OOS-GW-P", "p del contraste de Giacomini-White de F1-ECM frente a AR(4)", fm["gw_vs_ar4"]["p"],
                      unidad="p-valor", nota=nota + f"; {int(fm['gw_vs_ar4']['n'])} observaciones en el contraste", **comun))
    res.append(_cifra("V18-AUX-F1-OOS-MCS-P", "p del conjunto de confianza de modelos (MCS) para F1-ECM", fm["mcs"]["p"]["F1-ECM"],
                      unidad="p-valor", nota=nota + f"; dentro del MCS al 90 %: {', '.join(fm['mcs']['dentro_90'])}", **comun))
    # E1-R3: pretendencias, unidades de la estimación y razón con la referencia
    t = pd.read_csv(est / "e1" / "tabla.csv").set_index("id").loc["E1-R3"]
    rj = json.loads((est / "e1" / "resultado.json").read_text(encoding="utf-8"))["diagnosticos"]["E1-R3"]
    e1 = {h["id"]: h for h in json.loads((est / "e1" / "hechos.json").read_text(encoding="utf-8"))}["V18-E1-R3"]
    comun = dict(periodo=str(t.ventana), cobertura="Barcelona (secciones censales no selladas)", fuentes=e1["fuentes"],
                 clase=check_v18.DIAGNOSTICO, ficha=_rel(est / "e1" / "tabla.csv"))
    res.append(_cifra("V18-AUX-E1-R3-PRETEND-P", "p del contraste conjunto de los adelantos de 2011 y 2012 en E1-R3 (pretendencias)",
                      rj["pretendencias_p"], unidad="p-valor", nota="diagnosticos.E1-R3.pretendencias_p de resultado.json; con p < 0,01 "
                      "la regla del plan lo trata como fallo decisivo", **comun))
    res.append(_cifra("V18-AUX-E1-R3-N", "Secciones censales con dato en la estimación de E1-R3", t.n_unidades, unidad="secciones",
                      nota="n_unidades de tabla.csv (la cobertura de V18-E1-R3 cuenta las secciones de la muestra antes de exigir "
                      "SERPAVI en todo el periodo)", **comun))
    res.append(_cifra("V18-AUX-E1-R3-RAZON", "Razón entre el coeficiente de E1-R3 y la referencia de Segú (2018)", t.razon_ref,
                      unidad="razón", nota="razon_ref de tabla.csv (etiqueta I6, no interviene en la clase)", **comun))
    # E8-R1: p tras Holm y número de comunidades
    t = pd.read_csv(est / "e8" / "tabla.csv").set_index("id").loc["E8-R1"]
    e8 = {h["id"]: h for h in json.loads((est / "e8" / "hechos.json").read_text(encoding="utf-8"))}["V18-E8-R1"]
    comun = dict(periodo=e8["periodo"], cobertura="España (provincias de las comunidades de régimen común no selladas)",
                 fuentes=e8["fuentes"], clase=check_v18.DIAGNOSTICO, ficha=_rel(est / "e8" / "tabla.csv"))
    res.append(_cifra("V18-AUX-E8-R1-P-HOLM", "p de E8-R1 tras la corrección de Holm con la coprincipal V16-Q6-p", t.p_holm,
                      unidad="p-valor", nota="p_holm de tabla.csv (p de aleatorización de calendarios corregido por Holm)", **comun))
    res.append(_cifra("V18-AUX-E8-R1-NCCAA", "Comunidades autónomas en la muestra de E8-R1", t.n_comunidades, unidad="comunidades",
                      nota="n_comunidades de tabla.csv", **comun))
    # BVAR: proporción de extracciones explosivas del posterior
    src = est / "e7_bvar" / "resultado.json"
    eb = json.loads(src.read_text(encoding="utf-8"))["diagnosticos"]["estabilidad"]
    for k, per in (("R3", "2008T1-2022T4"), ("A1", "2008T1-2026T2")):
        res.append(_cifra(f"V18-AUX-E7-{k}-EXPLOSIVAS", f"Extracciones del posterior con raíz máxima mayor que 1 en E7-{k} (BVAR)",
                          100 * eb[f"{k}_proporcion_extracciones_explosivas"], unidad="% de las extracciones", periodo=per,
                          cobertura="España (nacional)", fuentes=[_rel(src)], clase=check_v18.DIAGNOSTICO, ficha=_rel(src),
                          nota=f"diagnosticos.estabilidad.{k}_proporcion_extracciones_explosivas de resultado.json, en %; raíz máxima "
                          f"media del posterior {eb[f'{k}_raiz_maxima_media_posterior']}"))
    # Umbrales y bandas fijados antes de estimar (copiados del texto del plan, de la adenda y del Monte Carlo)
    ad = RAIZ / "docs" / "v18" / "plan_replicacion_adenda.md"
    ta = ad.read_text(encoding="utf-8")
    bv = OUT / "montecarlo" / "bvar" / "informe.md"
    tb = bv.read_text(encoding="utf-8")
    num = r"(\d+,\d+)"
    m_ad = _buscar(ta, rf"\*\*Apta\.\*\* Tamaño al 5 % en \[{num}; {num}\] y cobertura al 95 % en \[{num}; {num}\]", _rel(ad))
    m_en = _buscar(tb, rf"Criterio del encargo: APTO si el tamaño al 5 % está en \[{num}; {num}\] y la cobertura al 95 % .*? en "
                       rf"\[{num}; {num}\]", _rel(bv))
    m_bv = _buscar(tb, r"cobertura 68 % [\d.]+ fuera de \[([\d.]+); ([\d.]+)\].*?cobertura 90 % [\d.]+ fuera de \[([\d.]+); ([\d.]+)\]", _rel(bv))
    m_h20 = _buscar(ta, r"Si 1/HHI < (\d+), la inferencia principal es el cluster por provincia", _rel(ad))
    m_h10 = _buscar(ta, r"En E9, 1/HHI < (\d+) implica NO ESTIMABLE", _rel(ad))
    comun = dict(periodo="2026", cobertura="regla del pre-registro interno (sin datos)", clase="NO ESTIMABLE")
    for k, ind, mn, mx, fuente in (
            ("CRIT-ADENDA-TAM", "Banda de tamaño al 5 % de una herramienta apta (adenda 1.12)", m_ad.group(1), m_ad.group(2), ad),
            ("CRIT-ADENDA-COB", "Banda de cobertura al 95 % de una herramienta apta (adenda 1.12)", m_ad.group(3), m_ad.group(4), ad),
            ("CRIT-ENCARGO-TAM", "Banda de tamaño al 5 % del criterio del encargo del Monte Carlo", m_en.group(1), m_en.group(2), bv),
            ("CRIT-ENCARGO-COB", "Banda de cobertura al 95 % del criterio del encargo del Monte Carlo", m_en.group(3), m_en.group(4), bv),
            ("CRIT-BVAR-COB68", "Banda de cobertura de las bandas del 68 % del BVAR (Monte Carlo)", m_bv.group(1), m_bv.group(2), bv),
            ("CRIT-BVAR-COB90", "Banda de cobertura de las bandas del 90 % del BVAR (Monte Carlo)", m_bv.group(3), m_bv.group(4), bv)):
        res.append(_cifra(f"V18-AUX-{k}", ind, None, unidad="proporción", fuentes=[_rel(fuente)], ficha=_rel(fuente),
                          nota="constante fijada antes de estimar, copiada del texto de origen", mn=_num_es(mn), mx=_num_es(mx), **comun))
    for k, ind, m in (("CRIT-HHI-INFERENCIA", "Choques efectivos (1/HHI) por debajo de los cuales la inferencia principal de un "
                       "shift-share pasa a Webb por provincia con AR (adenda 1.13)", m_h20),
                      ("CRIT-HHI-E9", "Choques efectivos (1/HHI) por debajo de los cuales E9 es NO ESTIMABLE (adenda 1.13)", m_h10)):
        res.append(_cifra(f"V18-AUX-{k}", ind, int(m.group(1)), unidad="choques efectivos", fuentes=[_rel(ad)], ficha=_rel(ad),
                          nota="constante fijada antes de estimar, copiada de la adenda; el umbral de NO ESTIMABLE solo existe en E9",
                          **comun))
    return res


def _aux_catalogo() -> list[dict]:
    src = OUT / "f1" / "catalogo.csv"
    c = pd.read_csv(src)
    comun = dict(unidad="fichas", periodo="2026", cobertura="literatura (todos los países del catálogo)",
                 fuentes=[_rel(src), "output/v18/f1/informe.md"], clase="NO ESTIMABLE", ficha=_rel(src))
    nota = "recuento de filas de catalogo.csv (fase 1)"
    cuentas = [("FICHAS", "Fichas del catálogo de la literatura", len(c)),
               ("TEXTO-COMPLETO", "Fichas leídas en texto completo", int((c.leido == "texto completo").sum())),
               ("SOLO-RESUMEN", "Fichas leídas solo por el resumen", int((c.leido == "solo resumen").sum())),
               ("SIN-INDICAR", "Fichas sin indicar el grado de lectura", int((c.leido == "sin indicar").sum())),
               ("PAQUETE", "Fichas con paquete de replicación", int((c.paquete == "sí").sum())),
               ("VERIFICADA", "Fichas con referencia VERIFICADA", int((c.estado == "VERIFICADA").sum())),
               ("NO-VERIFICADA", "Fichas con referencia NO VERIFICADA", int((c.estado == "NO VERIFICADA").sum())),
               ("DISCREPANTE", "Fichas con referencia DISCREPANTE", int((c.estado == "DISCREPANTE").sum()))]
    return [_cifra(f"V18-AUX-CAT-{k}", ind, n, nota=nota, **comun) for k, ind, n in cuentas]


D3_SERIES = {"Valor tasado": "VALOR-TASADO", "IPV INE por CCAA": "IPV-CCAA", "IPC alquiler": "IPC-ALQUILER", "IPVA": "IPVA",
             "SERPAVI": "SERPAVI"}


def _aux_d3() -> list[dict]:
    """Cuotas del componente común por subperiodo (V17-D3); las del periodo completo ya están como V17-D3-VARIANZA-COMUN-*."""
    src = RAIZ / "output" / "v17" / "d3" / "varianza_comun_local.csv"
    v = pd.read_csv(src)
    res = []
    for serie, g in v.groupby("serie", sort=False):
        clave = next(k for p, k in D3_SERIES.items() if str(serie).startswith(p))
        completo = g.periodo.map(lambda s: int(s[-4:]) - int(s[:4])).idxmax()
        for r in g.drop(index=completo).itertuples():
            res.append(_cifra(f"V18-AUX-D3-{clave}-{r.periodo}", f"Cuota de la varianza de la variación anual de {serie} debida al "
                              f"componente común (año), {r.periodo}", 100 * r.cuota_comun_anio,
                              unidad="% (IC95 bootstrap por provincias)", periodo=r.periodo,
                              cobertura=f"España ({r.N} unidades sin bloques sellados v6)",
                              fuentes=[_rel(src), "output/v17/d3/informe.md"], clase="NO ESTIMABLE",
                              nota="subperiodo de V17-D3 (cuota_comun_anio e IC95 del fichero de origen, en %); el periodo completo "
                              "es V17-D3-VARIANZA-COMUN-*", ficha=_rel(src), mn=100 * r.ic95_lo, mx=100 * r.ic95_hi))
    return res


LIT_AUX = re.compile(r"V18-AUX-(LIT|REP)-")   # valores de la literatura (publicados o reproducidos con los datos de sus autores)


def auxiliares() -> list[dict]:
    res = (_aux_literatura() + _aux_fichas() + _aux_f5() + _aux_reproduccion() + _aux_montecarlo() + _aux_estimacion()
           + _aux_catalogo() + _aux_d3() + _aux_k12())
    # K14 (árbitro, ronda 2, N8): la clase V18 es de un factor o de una estimación propia, no de un valor publicado; los valores de la
    # literatura llevan «literatura (sin clase propia)» en lugar de NO ESTIMABLE
    for h in res:
        if LIT_AUX.match(h["id"]):
            h["clasificacion_v18"] = check_v18.LITERATURA
    return res


# ---------------------------------------------------------------------------------------------------------------------------
# Clase propia por especificación (K12; árbitro, hallazgo 2): cada cifra lleva la clase de su propia especificación, no la del
# estudio. Las robusteces B6 son «robustez a posteriori»; las especificaciones que su resultado.json declara «no se clasifica» son
# «sin clasificar (coprincipal informativa)» (coprincipales, -P-) o «diagnóstico o variante (sin clase propia)»; la prueba de
# reversión de E2-R1 es un diagnóstico. La única estimación designada de clase SUGESTIVO es E2-R1.
# ---------------------------------------------------------------------------------------------------------------------------
CLASE_FIJA = {"V18-E2-R1-REV": (check_v18.DIAGNOSTICO, "prueba de reversión de E2-R1 (adenda, AD-E2-R1): diagnóstico, sin clase propia")}
SUGESTIVO_PERMITIDO = {"V18-E2-R1", "V18-AUX-E2-R1-PCT", "V18-B5-E2"}   # E2-R1, su transformación en % y la fila B5 (clase de la designada)


def _no_se_clasifica() -> set[str]:
    ids = set()
    for p in sorted((OUT / "estimacion").glob("*/resultado.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        c = r.get("clasificaciones") or r.get("clasificacion_v18_por_especificacion") or {}
        ids |= {f"V18-{k}" for k, v in c.items() if str(v).startswith("no se clasifica")}
    return ids


def clase_propia(h: dict, no_clasif: set[str]) -> tuple[str, str]:
    """(clase, motivo) de la cifra según su propia especificación; motivo vacío si la clase no cambia."""
    i, c = str(h["id"]), h.get("clasificacion_v18")
    if i in CLASE_FIJA:
        return CLASE_FIJA[i]
    if re.match(r"V18-E\d+-B6-", i):
        return check_v18.ROBUSTEZ_POSTERIORI, "robustez añadida tras ver el resultado (B6): no decide la clase"
    if i in no_clasif and any(h.get(k) is not None for k in ("valor", "min", "max")):
        if "-P-" in i:
            return check_v18.SIN_CLASIFICAR, "coprincipal que el plan no clasifica (resultado.json: «no se clasifica»)"
        return check_v18.DIAGNOSTICO, "variante que su resultado.json no clasifica"
    return c, ""


def consolidar() -> tuple[list[dict], list[str]]:
    filas, err = [], []
    paises = _paises_b5()
    no_clasif = _no_se_clasifica()
    for p in fuentes_hechos():
        rel = str(p.relative_to(RAIZ))
        for h in json.loads(p.read_text(encoding="utf-8")):
            h = dict(h)
            h.setdefault("ficha", rel)
            clase, motivo = clase_propia(h, no_clasif)
            if motivo and clase != h.get("clasificacion_v18"):
                h["nota"] = f"{h.get('nota', '')} Clase propia de la especificación (K12): {clase}; {motivo}.".strip()
                h["clasificacion_v18"] = clase
            filas.append(h)
    filas += auxiliares()
    con_cifra = [h for h in filas if any(h.get(k) is not None for k in ("valor", "min", "max"))]
    sobran = sorted(h["id"] for h in con_cifra if h.get("clasificacion_v18") == "SUGESTIVO" and h["id"] not in SUGESTIVO_PERMITIDO)
    if sobran:
        err.append(f"cifras SUGESTIVO fuera de E2-R1 (K12): {sobran}")
    vistos: set[str] = set()
    for h in filas:
        i = str(h.get("id", ""))
        if i in vistos:
            err.append(f"id repetido: {i}")
        vistos.add(i)
        if not i.startswith("V18-"):
            err.append(f"{i}: sin prefijo V18-")
        if not h.get("fuentes"):
            err.append(f"{i}: sin fuentes")
        if h.get("capa") != "C4":
            err.append(f"{i}: capa {h.get('capa')!r} (toda cifra V18 es C4, K2)")
        if h.get("clasificacion_v18") not in check_v18.CLASES:
            err.append(f"{i}: clasificacion_v18 no válida ({h.get('clasificacion_v18')!r})")
        if check_v18.CAUSAL.search(f"{h.get('indicador', '')} {h.get('nota', '')}"):
            err.append(f"{i}: lenguaje causal en el indicador o la nota (K2)")
    if len(filas) != N_ESPERADO:
        err.append(f"se esperaban {N_ESPERADO} cifras V18 y hay {len(filas)}")
    for h in filas:
        if isinstance(h.get("fuentes"), str):
            h["fuentes"] = [h["fuentes"]]
        h["tipo_rango"] = tipo_rango(h)
        h["cobertura"] = cobertura_real(h, paises)
        if not h.get("fecha_dato"):
            anios = re.findall(r"(?:19|20)\d\d", str(h.get("periodo", "")))
            h["fecha_dato"] = anios[-1] if anios else FECHA
        assert h["tipo_rango"] in TIPOS_RANGO and h["cobertura"] and "véase" not in h["cobertura"]
    return filas, err


def main() -> int:
    filas, err = consolidar()
    if err:
        print(f"f6_hechos V18: {len(err)} errores")
        for x in err[:40]:
            print("  -", x)
        return 1
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(filas, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n_cifra = sum(any(h.get(k) is not None for k in ("valor", "min", "max")) for h in filas)
    tipos = {t: sum(h["tipo_rango"] == t for h in filas) for t in TIPOS_RANGO}
    (SALIDA.parent / "informe.md").write_text(
        "# V18 · Fase 6 · Cifras V18 para cifras_clave\n\n"
        "**análisis V18; capa C4; pre-registro interno plan-replicacion-v18.** Generado por src/v18/f6_hechos.py: "
        f"{len(filas)} cifras V18 (todas C4, con su clasificacion_v18 al lado): {len(filas) - N_AUX} de {len(fuentes_hechos())} "
        "ficheros hechos.json y "
        f"{N_AUX} cifras auxiliares V18-AUX-* copiadas de sus salidas de origen (literatura, contabilidad, reproducciones, "
        "Monte Carlo, variantes de E1 y E2, catálogo y subperiodos de V17-D3) para el Documento de Trabajo. "
        f"{n_cifra} tienen valor, mínimo o máximo y entran en output/v5/cifras_clave.csv; el resto (sin ninguna cifra) no entra. "
        f"Tipo de rango: {tipos['rango']} rango, {tipos['referencias']} referencias, {tipos['sin rango']} sin rango.\n",
        encoding="utf-8")
    print(f"f6_hechos V18: {len(filas)} cifras ({n_cifra} con cifra) -> {SALIDA.relative_to(RAIZ)}; tipos {tipos}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
