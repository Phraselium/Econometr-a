"""A1 (v5): tabla única de cifras clave. Todos los entregables v5 leen de aquí (src/v5/render.py).

Fuentes de cada fila:
- hechos.json de los módulos v5 (output/v5/*/hechos.json, lista estándar);
- adaptadores de v4 que LEEN las cifras de sus JSON y CSV (no hay cifras tecleadas).
Un periodo por indicador y la cobertura explícita. Sin red y determinista.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
V4, V5 = RAIZ / "output" / "v4", RAIZ / "output" / "v5"
COLS = ["id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha", "origen"]
# v6.3 (R0 de V7, pendiente K4a-04): sentido de min/max cuando NO es un rango del valor. Las cifras no cambian; la columna
# «sentido_min_max» lo declara y los tests exigen min <= valor <= max solo cuando es «rango».
SENTIDO_MIN_MAX = {
    "CA-EU-": "min = mediana de la UE-27; max = percentil 75 de la UE-27 (referencia, no rango del valor)",
    "R1B-G-": "min = valor crítico al 95 %; max = estadístico observado (GSADF)",
    "R1B-S-": "min = umbral de referencia; max = valor observado (Cinelli-Hazlett)",
    "m2_pip_": "valor = PIP con prior uniforme; min y max = PIP en el núcleo y con prior beta-binomial (variantes, no rango)",
    "E-E1-VLC-contratos": "min y max = contratos del distrito con menos y con más contratos (extremos por distrito; valor = total)",
    "T1-H1": "min = bajas implícitas con signo invertido (referencia); max = valor (identidad negativa)",
    "T3-H8": "min = max = aporte del componente con mayor amplitud (valor = amplitud conjunta)",
    "CC-C7b-jov-": "min = valor del año base; max = valor del último año (no rango)",
    "CA-CT-ratio-triang-": "min = ratio INE; max = ratio Registradores (dos fuentes; valor redondeado del titular)",
    "V8-M9-shap-": "min y max = banda del 68 % del bootstrap de bloques (el punto SHAP puede quedar fuera de la banda: no es rango del valor)",   # V8
}


# v7.2 (correcciones previas a release): cifras RETIRADAS de la tabla vigente. Se conservan, con el motivo y su sustituta, en
# output/v5/cifras_superadas.csv (trazabilidad, doble implementación y ERRATA); ningún entregable puede citarlas (render falla).
RETIRADAS = {
    "deficit_2124_c1": ("L3-DEF-2124-SINBAJAS", "superada en v6.2: rango C1 con una sola corrección de la EPA; pasa a cota C2 con 8 variantes"),
    "T3-H1": ("L3-DEF-2124-SINBAJAS", "superada en v6.2: mismas 4 combinaciones de fuentes que deficit_2124_c1 (C1 retirado)"),
    "deficit_2124_c2": ("L3-DEF-2124-BAJAST1", "superada: bajas SUPUESTAS del 0,1-0,2 % anual (v4) sin respaldo observado; máximo 902.808"),
    "L3-DEF-2124-CONBAJAS": ("L3-DEF-2124-BAJAST1", "superada en v7.2: mismas variantes L3 con bajas SUPUESTAS del 0,1-0,2 % anual; máximo 924.658"),
    "T3-H2": ("L3-DEF-2124-BAJAST1", "superada en v6.2: bajas estimadas T1 sobre las 4 combinaciones antiguas de M0; máximo 744.144"),
    "T3-H3": ("L3-DEF-2124-BAJAST1", "superada: compara con el supuesto antiguo de bajas (902.808), ya retirado"),
    "T3-H4": ("L3-DEF-2125", "retirada en v7.2: déficit 2021-2025 con bajas T1 sobre las combinaciones antiguas de M0 (solo ECP); se publica una sola cifra con bajas (2021-2024)"),
    "B1-H1": ("T3-H5b", "superada en v5.1: necesidad de v5 (B1); la vigente es la recalculada en T3"),
    "V7-R6-a_construccion-esfuerzo10a": ("V71-S3-R6-a_construccion-compra-precio10a", "superada en v7.2: dosis de construcción adicional nula en 14 CCAA; reestimada con dosis no nula"),
    "V7-R6-n-robustas": ("V71-S3-R6-*-robustas", "superada en v7.2: incluía la construcción adicional con dosis nula y la rebaja de impuestos a la construcción (no difundible)"),
}
# v7.2: cifras NO DIFUNDIBLES por sobrestimación de diseño (rebaja de impuestos y costes de construcción, f2: la simulación traslada
# la rebaja al precio de todo el mercado y el coste fiscal solo cubre la obra nueva). Se conservan en cifras_superadas.csv.
NO_DIFUNDIBLE_PREFIJOS = ("V7-R6-f2_", "V71-S1-f2_", "V71-S3-R6-f2_")
MOTIVO_F2 = ("—", "no difundible (v7.2): sobrestimación de diseño del escenario de rebaja de impuestos y costes de construcción")


def sentido(i: str) -> str:
    return next((v for k, v in SENTIDO_MIN_MAX.items() if str(i).startswith(k)), "rango")


def _f(i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha, ficha, origen) -> dict:
    return dict(zip(COLS, [i, ind, val, mn, mx, uni, per, cob, fue, capa, fecha, ficha, origen]))


def v4_adaptadores() -> list[dict]:
    f = []
    m0 = json.loads((V4 / "M0" / "resultado.json").read_text())
    d = m0["deficit_2021_2024"]
    f.append(_f("deficit_2124_c1", "Déficit acumulado: aumento de hogares menos viviendas terminadas, sin bajas", d["mediana"],
                d["c1_sin_bajas"][0], d["c1_sin_bajas"][1], "viviendas", "2021-2024", "España",
                "hogares: ECP y EPA corregida; terminadas: Ministerio y Catastro", "C1", "2024", "V04, V05",
                "output/v4/M0/resultado.json:deficit_2021_2024.c1_sin_bajas"))
    f[-1]["valor"] = None   # C1 es el rango; la mediana incluye combinaciones con bajas
    f.append(_f("deficit_2124_c2", "Déficit acumulado con bajas del parque supuestas del 0,1-0,2 % anual (cota)", None,
                d["c2_con_bajas"][0], d["c2_con_bajas"][1], "viviendas", "2021-2024", "España",
                "ídem, con bajas supuestas", "C2", "2024", "V04, V05", "output/v4/M0/resultado.json:deficit_2021_2024.c2_con_bajas"))
    h0 = {x["periodo"]: x for x in json.loads((V4 / "M2" / "hechos.json").read_text())[0]["magnitud"]}["2021-2025"]
    lo, hi = sorted([h0["dH_EPA_hogares_corregida"], h0["dH_ECP_o_censo"]])
    f.append(_f("dh_2125", "Aumento del número de hogares", (lo + hi) / 2, lo, hi, "hogares", "2021-2025", "España",
                "INE ECP y EPA (sin corrección: los dos extremos son posteriores a la ruptura de 2021; ventanas distintas: stock a 1 de enero en la ECP y media anual en la EPA, v7.1 K4b-dh)", "C1", "2025T1", "V03", "output/v4/M2/hechos.json:M2-H0"))
    t = pd.read_csv(V4 / "M0" / "terminadas_triangulacion.csv")
    t = t[(t.anio >= 2019) & (t.anio <= 2024)]
    f.append(_f("terminadas_1924", "Viviendas terminadas al año (territorio común: sin País Vasco ni Navarra)", None,
                t.comun_mivau_bruto_sin_PV_NA.min(), t.comun_mivau_bruto_sin_PV_NA.max(), "viviendas/año", "2019-2024",
                "territorio común", "Ministerio (fin de obra) y Catastro (altas), dentro de ±15 %", "C1", "2024", "—",
                "output/v4/M0/terminadas_triangulacion.csv:comun_mivau_bruto_sin_PV_NA"))
    m2c = json.loads((V4 / "M2" / "hechos.json").read_text())
    lat = [x for x in m2c if x["id"] == "M2-C1"][0]
    import re
    mn, mx = (int(x) * 1000 for x in re.search(r"(\d+)-(\d+) mil", lat["magnitud"]).groups())
    f.append(_f("latente_convivencia", "Demanda latente de jóvenes por convivencia con los padres (frente a 2008)", None, mn, mx,
                "hogares", "2008-2025", "España", "INE EPA y ECV (tasa de convivencia con los padres)", "C2", "2025", "—",
                "output/v4/M2/hechos.json:M2-C1 (magnitud, «convivencia con padres»)"))
    ext = json.loads((V4 / "M4" / "hechos.json").read_text())["extranjeros_nacional"]
    f.append(_f("compradores_extranjeros", "Compraventas de vivienda con comprador extranjero (residente o no)", ext["mivau_pct"],
                ext["mivau_pct"], ext["notariado_pct"], "%", str(ext["anyo_mivau"]), "España", "Ministerio; Notariado (no independientes)",
                "C4", str(ext["anyo_mivau"]), "M4-V1", "output/v4/M4/hechos.json:extranjeros_nacional"))
    f.append(_f("compradores_no_residentes", "Compraventas con comprador extranjero no residente", ext["mivau_pct_no_residentes"], None, None,
                "%", str(ext["anyo_mivau"]), "España", "Ministerio", "C4", str(ext["anyo_mivau"]), "M4-V1",
                "output/v4/M4/hechos.json:extranjeros_nacional.mivau_pct_no_residentes"))
    return f


def V7_HECHOS() -> list[Path]:   # v7.1 (W2): hechos de V7 (R4, R4b, R5, R6) y de V7.1 (S1, S3); V8 (F6, ids «V8-»); nunca los _smoke
    return [p for v in ("v7", "v7_1", "v7_2", "v8", "v9", "v10", "v12") for p in sorted((RAIZ / "output" / v).glob("*/hechos.json")) if "_smoke" not in p.parent.name]   # V10: atlas (ids «V10-ATL-»); V9: F5 (ids «V9-»); V12: hechos (ids «V12-»)


def v5_hechos() -> list[dict]:
    f = []
    for p in sorted(V5.glob("*/hechos.json")) + sorted((RAIZ / "output" / "v5_1").glob("*/hechos.json")) + sorted((RAIZ / "output" / "v6").glob("*/hechos.json")) + sorted((RAIZ / "output" / "v6_1").glob("*/hechos.json")) + sorted((RAIZ / "output" / "v6_2").glob("*/hechos.json")) + sorted((RAIZ / "output" / "v6_3").glob("*/hechos.json")) + V7_HECHOS():   # v5.1, v6, v6.1, v6.2, v6.3, v7 y v7.1
        h = json.loads(p.read_text())
        if not isinstance(h, list):
            continue
        for x in h:
            r = {c: x.get(c) for c in COLS if c not in ("ficha", "origen")}
            if isinstance(r.get("fuentes"), list):   # listas de fuentes -> texto (revisión E, B2)
                r["fuentes"] = "; ".join(map(str, r["fuentes"]))
            r["ficha"] = x.get("ficha", "—")
            r["origen"] = f"{p.relative_to(RAIZ)}:{x.get('id')}"
            f.append(r)
    return f


def main() -> None:
    ck = pd.DataFrame(v4_adaptadores() + v5_hechos(), columns=COLS)
    ck = ck[ck[["valor", "min", "max"]].notna().any(axis=1)]   # filas sin cifra (p. ej. NaN de origen) no entran
    ck["capa"] = ck.capa.astype(str)
    ck = ck.sort_values("id", kind="stable")
    # K4a-01: «%.6g» redondeaba a 6 cifras significativas los recuentos >= 1e6 (1.720.537 -> 1.720.540); «%.10g» es exacto hasta 1e10
    ck["sentido_min_max"] = ck.id.map(sentido)
    fuera = ck.id.isin(RETIRADAS) | ck.id.str.startswith(NO_DIFUNDIBLE_PREFIJOS)
    sup = ck[fuera].copy()
    sup["sustituida_por"] = [RETIRADAS.get(i, MOTIVO_F2)[0] for i in sup.id]
    sup["motivo"] = [RETIRADAS.get(i, MOTIVO_F2)[1] for i in sup.id]
    sup.to_csv(V5 / "cifras_superadas.csv", index=False, float_format="%.10g")
    ck = ck[~fuera]
    ck.to_csv(V5 / "cifras_clave.csv", index=False, float_format="%.10g")
    md = ["# Cifras clave v5", "",
          "Tabla única de la que leen todos los entregables. Una fila por indicador y periodo. Generada por src/v5/cifras_clave.py.", "",
          "| id | indicador | valor | rango | unidad | periodo | cobertura | fuentes | capa | fecha del dato |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in ck.itertuples():
        rango = "" if pd.isna(r.min) else f"{r.min:.4g}–{r.max:.4g}"
        val = "" if pd.isna(r.valor) else f"{r.valor:.4g}"
        md.append(f"| {r.id} | {r.indicador} | {val} | {rango} | {r.unidad} | {r.periodo} | {r.cobertura} | {r.fuentes} | {r.capa} | {r.fecha_dato} |")
    md += ["", "## Clases territoriales (A4)", "",
           "Se clasifica por provincia y municipio con el precio P, el suelo repercutido, el coste de construcción c (rango oficial derivado; "
           "C2 exige la misma clase también con el rango supuesto de v4), el margen m y la holgura r. «Falta» significa déficit del periodo > 0.", "",
           "| Clase | Nombre | Definición |", "|---|---|---|",
           "| 1 | Falta y es rentable | Déficit > 0; P − c(1+m) − suelo > 0; no cumple la clase 2. |",
           "| 2 | Falta con freno regulatorio o de suelo | Déficit > 0; P > r(c + suelo) (holgura) y las terminadas no responden. No se atribuye causa. |",
           "| 3 | Falta y no es rentable | Déficit > 0; P − c(1+m) − suelo ≤ 0. |",
           "| 4 | No falta | Déficit ≤ 0. No implica exceso de oferta. |",
           "| 9 | Sin dato | Falta precio, suelo, déficit u oferta; no se imputa. |", "",
           "Capa de la clase: C2 si se mantiene en todo el rango de costes, márgenes y holguras y el signo del déficit es estable; si no, C4. "
           "Los municipios son siempre C4. Véase output/v5/A4/resultado.json."]
    (V5 / "cifras_clave.md").write_text("\n".join(md) + "\n")
    print(f"cifras_clave: {len(ck)} filas (retiradas o no difundibles: {len(sup)}, en cifras_superadas.csv)")


if __name__ == "__main__":
    main()
