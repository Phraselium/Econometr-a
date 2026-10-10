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
                "INE ECP y EPA (corregida por la ruptura de 2021)", "C1", "2025T1", "V03", "output/v4/M2/hechos.json:M2-H0"))
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


def v5_hechos() -> list[dict]:
    f = []
    for p in sorted(V5.glob("*/hechos.json")):
        h = json.loads(p.read_text())
        if not isinstance(h, list):
            continue
        for x in h:
            r = {c: x.get(c) for c in COLS if c not in ("ficha", "origen")}
            r["ficha"] = x.get("ficha", "—")
            r["origen"] = f"{p.relative_to(RAIZ)}:{x.get('id')}"
            f.append(r)
    return f


def main() -> None:
    ck = pd.DataFrame(v4_adaptadores() + v5_hechos(), columns=COLS)
    ck["capa"] = ck.capa.astype(str)
    ck = ck.sort_values("id", kind="stable")
    ck.to_csv(V5 / "cifras_clave.csv", index=False, float_format="%.6g")
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
    print(f"cifras_clave: {len(ck)} filas")


if __name__ == "__main__":
    main()
