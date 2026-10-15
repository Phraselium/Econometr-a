"""V12: incorporación de los resultados descriptivos de V12 a la base única (`make base`).

src/v10/base.py llama a `partes()` y une `META_V12` a `META_V11` (variable -> unidad, fuente, capa, licencia,
redistribuible). Solo códigos INE; todas las variables son C4 (descriptivo o contable de fuente única por nivel) y
llevan el prefijo `v12_`. Lee únicamente salidas versionadas de output/v12.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
O = RAIZ / "output" / "v12"
INE = "INE: reutilización con cita (Ley 37/2007)"
CAT = "Catastro: reutilización con reconocimiento"
_C = "C4"


def partes() -> list[pd.DataFrame]:
    out = []

    def add(df: pd.DataFrame, origen: str, metodo: str) -> None:
        df = df.copy()
        df["origen"], df["prioridad"], df["metodo_dato"] = origen, 4, metodo
        if "desagregacion" not in df:
            df["desagregacion"] = ""
        out.append(df)

    # B1: contabilidad demográfica anual (flujos del año t; España, CCAA y provincia por nacionalidad; municipio total)
    for nivel in ("nacional", "ccaa", "provincia", "municipio"):
        f = O / "b1" / f"contabilidad_anual_{nivel}.csv{'.gz' if nivel == 'municipio' else ''}"
        if not f.exists():
            continue
        a = pd.read_csv(f, dtype={"cod_territorio": str})
        if nivel == "municipio":
            a = a[a.nac == "TOTAL"]
        for c in ("crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo"):
            add(pd.DataFrame({"territorio_codigo": a.cod_territorio, "nivel": nivel, "periodo_raw": a.anio.astype(str),
                              "variable": f"v12_pob_{c}", "desagregacion": "nacionalidad=" + a.nac, "valor": a[c]}),
                str(f.relative_to(RAIZ)), "identidad contable (B1): ΔP = vegetativo + exterior + interior + residuo")
    # B3: descomposición del crecimiento de hogares 2011-2021 (orden A y B) por provincia y CCAA
    for nivel, col in (("provincia", "cpro"), ("ccaa", "ccaa"), ("nacional", None)):
        f = O / "b3" / f"descomposicion_2011_2021_{nivel}.csv"
        if not f.exists():
            continue
        d = pd.read_csv(f, dtype={"cpro": str, "ccaa": str})
        cod = d[col] if col else pd.Series("00", index=d.index)
        for c in ("crecimiento", "poblacion_A", "estructura_A", "jefatura_A", "poblacion_B", "estructura_B", "jefatura_B"):
            comp, orden = (c.rsplit("_", 1) + [""])[:2] if c != "crecimiento" else ("crecimiento", "")
            add(pd.DataFrame({"territorio_codigo": cod, "nivel": nivel, "periodo_raw": "2021", "variable": f"v12_hogares_2011_2021_{comp}",
                              "desagregacion": f"orden={orden}" if orden else "", "valor": d[c]}),
                str(f.relative_to(RAIZ)), "descomposición contable 2011→2021 (B3; dos órdenes)")
    # B3: cuota de hogares con persona de referencia extranjera (Censo 2021, muestra; solo celdas publicables)
    f = O / "b3" / "hogares_nacionalidad_censo2021.csv"
    if f.exists():
        h = pd.read_csv(f, dtype={"cod_territorio": str})
        h = h[h.publicable]
        add(pd.DataFrame({"territorio_codigo": h.cod_territorio, "nivel": h.nivel, "periodo_raw": "2021",
                          "variable": "v12_hogares_ext_cuota", "valor": h.cuota_ext_pct}),
            str(f.relative_to(RAIZ)), "muestra del Censo 2021 (IC95 en output/v12/b3)")
    # B4: presión hogares nuevos / obra nueva por municipio y periodo
    f = O / "b4" / "presion_hogares_obra_municipio.csv"
    if f.exists():
        p = pd.read_csv(f, dtype={"cod_municipio": str})
        p["fin"] = p.periodo.str[-4:]
        for c in ("hogares_nuevos_estimados", "obra_neta", "ratio_obra_hogares"):
            add(pd.DataFrame({"territorio_codigo": p.cod_municipio, "nivel": "municipio", "periodo_raw": p.fin,
                              "variable": f"v12_{c}", "desagregacion": "periodo=" + p.periodo, "valor": p[c]}),
                str(f.relative_to(RAIZ)), "contable (B4); hogares 2021-2025 estimados con el tamaño de hogar de 2021")
    # B5: cuotas de titularidad (cuatro ámbitos; tramos dentro del ámbito)
    f = O / "b5" / "titularidad_cuotas.csv"
    if f.exists():
        t = pd.read_csv(f, dtype={"cod_territorio": str})
        for c in ("pct_mas5", "pct_mas10", "pct_mas100", "pct_PJ", "pct_PE"):
            add(pd.DataFrame({"territorio_codigo": t.cod_territorio, "nivel": t.nivel, "periodo_raw": t.anio.astype(str),
                              "variable": f"v12_titularidad_{c.lower()}", "valor": t[c]}),
                str(f.relative_to(RAIZ)), "cuota de viviendas (B5); tramo contado dentro del ámbito (municipio = cota inferior)")
    out = [d[d.valor.notna()] for d in out]
    return out


META_V12 = {
    **{f"v12_pob_{c}": ("personas", "INE: padrón/censo anual, MNP, EVR/EMCR (contabilidad V12-B1)", _C, INE, True)
       for c in ("crecimiento", "vegetativo", "saldo_exterior", "saldo_interior", "residuo")},
    **{f"v12_hogares_2011_2021_{c}": ("hogares", "INE: Censos 2011 y 2021 (microdatos), ECP; descomposición V12-B3", _C, INE, True)
       for c in ("crecimiento", "poblacion", "estructura", "jefatura")},
    "v12_hogares_ext_cuota": ("%", "INE: Censo 2021, muestra de hogares (persona de referencia de nacionalidad extranjera; V12-B3)", _C, INE, True),
    "v12_hogares_nuevos_estimados": ("hogares", "INE: censo anual y Censo 2021 (V12-B4)", _C, INE, True),
    "v12_obra_neta": ("unidades residenciales", "Catastro, estadística URBANA (V12-B4)", _C, CAT, True),
    "v12_ratio_obra_hogares": ("ratio", "Catastro e INE (V12-B4)", _C, CAT, True),
    **{f"v12_titularidad_{c}": ("%", "Catastro, titularidad por tramo de inmuebles y tipo de persona, uso residencial (V12-B5)", _C, CAT, True)
       for c in ("pct_mas5", "pct_mas10", "pct_mas100", "pct_pj", "pct_pe")},
}
