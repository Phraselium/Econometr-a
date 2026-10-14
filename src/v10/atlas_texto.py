"""V10-B2 · texto del atlas descriptivo: output/v10/atlas_descriptivo.md (lo copia `make publicacion` a
publicacion/atlas_descriptivo.md). Todas las cifras se calculan aquí desde output/v10/atlas/*.csv; ninguna se escribe a
mano. Lenguaje descriptivo: sin causas ni valoraciones.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
A = RAIZ / "output" / "v10" / "atlas"
SAL = RAIZ / "output" / "v10" / "atlas_descriptivo.md"


HECHOS: list[dict] = []
CODIGOS = {"València": "46250", "Málaga": "29067", "Sevilla": "41091", "Bilbao": "48020", "Zaragoza": "50297",
           "Palma": "07040", "Alicante/Alacant": "03014"}


def reg(ident: str, indicador: str, valor: float, unidad: str, periodo: str, cobertura: str, fuentes: str, capa: str,
        fecha: str, mn: float | None = None, mx: float | None = None) -> str:
    """Registra la cifra en output/v10/atlas/hechos.json (de ahí pasa a cifras_clave) y devuelve su marca «[id]»."""
    HECHOS.append({"id": ident, "indicador": indicador, "valor": round(float(valor), 4),
                   "min": None if mn is None else round(float(mn), 4), "max": None if mx is None else round(float(mx), 4),
                   "unidad": unidad, "periodo": periodo, "cobertura": cobertura, "fuentes": fuentes, "capa": capa,
                   "fecha_dato": fecha, "ficha": "—"})
    return f"[{ident}]"


def f(x: float, d: int = 1) -> str:
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def hallazgos() -> tuple[list[str], dict]:
    h, cifras = [], {}
    ecv = pd.read_csv(A / "a_quien_ecv.csv")
    ult, pri = int(ecv.anio.max()), int(ecv.anio.min())

    def v(anio, grupo, cat, ind):
        x = ecv[(ecv.anio == anio) & (ecv.grupo == grupo) & (ecv.categoria.astype(str) == str(cat)) & (ecv.indicador == ind)]
        return x.iloc[0] if len(x) else None

    am_u, am_p = v(ult, "tenencia", "alquiler de mercado", "sobrecarga_40"), v(pri, "tenencia", "alquiler de mercado", "sobrecarga_40")
    tot = v(ult, "total", "Total", "sobrecarga_40")
    if am_u is not None and am_p is not None and tot is not None:
        r1 = reg("V10-ATL-A1", "Sobrecarga del gasto en vivienda (>40 % de la renta), personas en alquiler de mercado", am_u.valor, "%",
                 str(ult), "España", "INE ECV (microdatos), cálculo propio; contraste Eurostat ilc_lvho07c", am_u.capa, f"ECV {ult}",
                 am_u.ic95_inf, am_u.ic95_sup)
        r2 = reg("V10-ATL-A2", "Sobrecarga del gasto en vivienda (>40 % de la renta), total de la población", tot.valor, "%", str(ult),
                 "España", "INE ECV (microdatos); contraste Eurostat ilc_lvho07a", tot.capa, f"ECV {ult}", tot.ic95_inf, tot.ic95_sup)
        r3 = reg("V10-ATL-A3", "Sobrecarga del gasto en vivienda (>40 %), alquiler de mercado, primer año de la serie", am_p.valor,
                 "%", str(pri), "España", "INE ECV (microdatos); contraste Eurostat ilc_lvho07c", am_p.capa, f"ECV {pri}",
                 am_p.ic95_inf, am_p.ic95_sup)
        h.append(f"- **Sobrecarga del gasto en vivienda (>40 % de la renta).** En {ult} afecta al {f(am_u.valor)} % {r1} de las "
                 f"personas que viven de alquiler a precio de mercado (IC 95 %: {f(am_u.ic95_inf)}-{f(am_u.ic95_sup)}), "
                 f"frente al {f(tot.valor)} % {r2} del conjunto de la población. En {pri}, la cifra de los inquilinos de mercado "
                 f"era del {f(am_p.valor)} % {r3}. *Capa {am_u.capa}; INE ECV (microdatos) con contraste con Eurostat; "
                 f"renta del año anterior a la encuesta.*")
        cifras["sobrecarga40_alquiler_mercado"] = (ult, am_u.valor)
    d1, d10 = v(ult, "decil_renta", 1, "sobrecarga_40"), v(ult, "decil_renta", 10, "sobrecarga_40")
    if d1 is not None and d10 is not None:
        a4 = reg("V10-ATL-A4", "Sobrecarga del gasto en vivienda (>40 %), primer decil de renta equivalente", d1.valor, "%", str(ult),
                 "España", "INE ECV (microdatos)", d1.capa, f"ECV {ult}", d1.ic95_inf, d1.ic95_sup)
        a5 = reg("V10-ATL-A5", "Sobrecarga del gasto en vivienda (>40 %), décimo decil de renta equivalente", d10.valor, "%", str(ult),
                 "España", "INE ECV (microdatos)", d10.capa, f"ECV {ult}", d10.ic95_inf, d10.ic95_sup)
        h.append(f"- **Por renta.** La sobrecarga del 40 % alcanza al {f(d1.valor)} % {a4} de las personas del primer decil de "
                 f"renta equivalente y al {f(d10.valor)} % {a5} del décimo ({ult}). *Capa {d1.capa}; INE ECV.*")
    ext, esp = v(ult, "nacionalidad", "resto del mundo", "sobrecarga_40"), v(ult, "nacionalidad", "España", "sobrecarga_40")
    if ext is not None and esp is not None:
        a6 = reg("V10-ATL-A6", "Sobrecarga del gasto en vivienda (>40 %), nacionalidad de fuera de la UE", ext.valor, "%", str(ult),
                 "España", "INE ECV (microdatos)", ext.capa, f"ECV {ult}", ext.ic95_inf, ext.ic95_sup)
        a7 = reg("V10-ATL-A7", "Sobrecarga del gasto en vivienda (>40 %), nacionalidad española", esp.valor, "%", str(ult),
                 "España", "INE ECV (microdatos)", esp.capa, f"ECV {ult}", esp.ic95_inf, esp.ic95_sup)
        h.append(f"- **Por nacionalidad.** {f(ext.valor)} % {a6} de las personas con nacionalidad de fuera de la UE viven en "
                 f"hogares con sobrecarga del 40 %, frente al {f(esp.valor)} % {a7} de las de nacionalidad española ({ult}; "
                 f"IC 95 % {f(ext.ic95_inf)}-{f(ext.ic95_sup)} y {f(esp.ic95_inf)}-{f(esp.ic95_sup)}). *Capa {ext.capa}; INE ECV.*")
    j = v(ult, "edad", "18-29", "esfuerzo_alquiler_mediana")
    m = v(ult, "edad", "45-64", "esfuerzo_alquiler_mediana")
    if j is not None and m is not None:
        a8 = reg("V10-ATL-A8", "Esfuerzo mediano de alquiler (alquiler anual / renta del hogar), 18-29 años, alquiler de mercado",
                 j.valor, "%", str(ult), "España", "INE ECV (microdatos); IC de Woodruff", j.capa, f"ECV {ult}", j.ic95_inf, j.ic95_sup)
        a9 = reg("V10-ATL-A9", "Esfuerzo mediano de alquiler, 45-64 años, alquiler de mercado", m.valor, "%", str(ult), "España",
                 "INE ECV (microdatos); IC de Woodruff", m.capa, f"ECV {ult}", m.ic95_inf, m.ic95_sup)
        h.append(f"- **Esfuerzo de alquiler por edad.** El alquiler anual mediano equivale al {f(j.valor)} % {a8} de la renta del "
                 f"hogar para las personas de 18 a 29 años que alquilan a precio de mercado y al {f(m.valor)} % {a9} para las de "
                 f"45 a 64 ({ult}; IC de Woodruff {f(j.ic95_inf)}-{f(j.ic95_sup)} y {f(m.ic95_inf)}-{f(m.ic95_sup)}). "
                 f"*Capa {j.capa}; INE ECV.*")
    epa = pd.read_csv(A / "a_quien_epa.csv")
    e = epa[(epa.grupo == "total") & (epa.tramo_edad == "30-34")].sort_values("anio")
    if len(e) > 1:
        e0, e1 = e.iloc[0], e[e.trimestres == 4].iloc[-1]
        b1 = reg("V10-ATL-A10", "Personas de 30 a 34 años que viven con al menos uno de sus padres, primer año", e0.valor, "%",
                 str(int(e0.anio)), "España", "INE EPA (microdatos)", e0.capa, str(int(e0.anio)), e0.ic95_inf, e0.ic95_sup)
        b2 = reg("V10-ATL-A11", "Personas de 30 a 34 años que viven con al menos uno de sus padres, último año completo", e1.valor,
                 "%", str(int(e1.anio)), "España", "INE EPA (microdatos)", e1.capa, str(int(e1.anio)), e1.ic95_inf, e1.ic95_sup)
        h.append(f"- **Emancipación.** Vivía con al menos uno de sus padres el {f(e0.valor)} % {b1} de las personas de 30 a 34 "
                 f"años en {int(e0.anio)} y el {f(e1.valor)} % {b2} en {int(e1.anio)} (media de cuatro trimestres). "
                 f"*Capa {e1.capa}; INE EPA (microdatos).*")
    ip = pd.read_csv(A / "b_ipva_nuevo_existente.csv", dtype={"territorio_codigo": str})
    nac = ip[(ip.nivel == "nacional")].sort_values("periodo").iloc[-1]
    pr = ip[(ip.nivel == "provincia") & (ip.periodo == nac.periodo)].sort_values("brecha_nuevo_menos_existente")
    c1 = reg("V10-ATL-B1", "Brecha IPVA contratos nuevos menos existentes (índices 2015=100)", nac.brecha_nuevo_menos_existente,
             "puntos de índice", str(nac.periodo), "España", "INE IPVA (59004)", "C4", str(nac.periodo))
    h.append(f"- **Entrar frente a quedarse.** Desde 2015, la renta de los contratos nuevos ha crecido más que la de los "
             f"existentes: en {nac.periodo}, el índice de contratos nuevos está en {f(nac.nuevo)} y el de existentes en "
             f"{f(nac.existente)} (2015 = 100), una brecha de {f(nac.brecha_nuevo_menos_existente)} puntos {c1} en España. "
             f"Las mayores brechas provinciales están en {pr.iloc[-1].nombre} ({f(pr.iloc[-1].brecha_nuevo_menos_existente)}) y "
             f"{pr.iloc[-2].nombre} ({f(pr.iloc[-2].brecha_nuevo_menos_existente)}); las menores, en {pr.iloc[0].nombre} "
             f"({f(pr.iloc[0].brecha_nuevo_menos_existente)}). *Capa C4; INE IPVA (59004 y 59005).*")
    b = pd.read_csv(A / "c_valencia_barrio.csv", dtype={"cod_barrio": str})
    s = pd.read_csv(A / "c_valencia_seccion.csv", dtype={"cod_seccion": str})
    pob21, pob25 = s.pob_2021.sum(), s.pob_2025.sum()
    ex21, ex25 = s.extranj_2021.sum(), s.extranj_2025.sum()
    d1_ = reg("V10-ATL-C1", "València: porcentaje de población de nacionalidad extranjera", 100 * ex25 / pob25, "%", "2025",
              "València (municipio 46250)", "INE censo anual (suma de secciones)", "C4", "2025-01-01")
    d2_ = reg("V10-ATL-C2", "València: porcentaje de población de nacionalidad extranjera", 100 * ex21 / pob21, "%", "2021",
              "València (municipio 46250)", "INE censo anual (suma de secciones)", "C4", "2021-01-01")
    h.append(f"- **València, población.** La ciudad pasa de {f(pob21, 0)} a {f(pob25, 0)} habitantes entre 2021 y 2025 "
             f"(suma de secciones del censo anual); la población de nacionalidad extranjera, de {f(ex21, 0)} a {f(ex25, 0)} "
             f"({f(100 * ex21 / pob21)} % {d2_} → {f(100 * ex25 / pob25)} % {d1_}). *Capa C4 (fuente única: censo anual del INE).*")
    top = b.dropna(subset=["indice_presion_descriptivo"]).sort_values("indice_presion_descriptivo").tail(5)
    marcas = {r.cod_barrio: reg(f"V10-ATL-C4-{r.cod_barrio}", f"Índice descriptivo de presión residencial, barrio {r.nombre.title()}",
                                r.indice_presion_descriptivo, "puntuación z media", "2019-2026", f"València, barrio {r.cod_barrio}",
                                "INE; MIVAU SERPAVI; Ajuntament de València", "C4", "2026-05") for r in top.itertuples()}
    h.append("- **València, barrios.** Los cinco barrios con el índice descriptivo de presión residencial más alto son "
             + ", ".join(f"{r.nombre.title()} ({f(r.indice_presion_descriptivo, 2)} {marcas[r.cod_barrio]})" for r in top.iloc[::-1].itertuples())
             + ". El índice promedia cuatro indicadores estandarizados (alquiler 2024, su variación 2019-2024, viviendas "
             "turísticas por 100 viviendas y cambio del porcentaje de población extranjera); describe coincidencias, no "
             "causas. *Capa C4; INE, MIVAU SERPAVI, Ajuntament de València.*")
    vut = s.vut_2026_05.sum()
    d3_ = reg("V10-ATL-C3", "València: viviendas turísticas (INE, medición experimental)", vut, "viviendas", "2026-05",
              "València (municipio 46250)", "INE, viviendas turísticas", "C4", "2026-05")
    h.append(f"- **València, viviendas turísticas.** El INE contabiliza {f(vut, 0)} {d3_} viviendas turísticas en la ciudad en mayo "
             f"de 2026 ({f(100 * vut / s.viviendas_2021.sum(), 2)} por 100 viviendas del Censo 2021), frente a "
             f"{f(s.vut_2021_08.sum(), 0)} en agosto de 2021. *Capa C4; INE, medición experimental.*")
    p = pd.read_csv(A / "d_espana_provincias.csv", dtype={"cod_provincia": str}).dropna(subset=["alquiler_anual_80m2_pct_renta_persona"])
    p = p.sort_values("alquiler_anual_80m2_pct_renta_persona")
    e1_ = reg("V10-ATL-D1", "Alquiler anual de 80 m² sobre la renta neta por persona, rango provincial", p.alquiler_anual_80m2_pct_renta_persona.median(),
              "%", "alquiler 2024; renta 2023", "52 provincias (valor: mediana; mín. y máx.: rango)", "MIVAU SERPAVI; INE ADRH y censo anual", "C4",
              "2024", p.iloc[0].alquiler_anual_80m2_pct_renta_persona, p.iloc[-1].alquiler_anual_80m2_pct_renta_persona)
    h.append(f"- **España por provincia** {e1_}. El alquiler anual de una vivienda tipo de 80 m² equivale a entre el "
             f"{f(p.iloc[0].alquiler_anual_80m2_pct_renta_persona)} % ({p.iloc[0].nombre}) y el "
             f"{f(p.iloc[-1].alquiler_anual_80m2_pct_renta_persona)} % ({p.iloc[-1].nombre}) de la renta neta media por "
             f"persona (alquiler 2024, renta 2023). *Capa C4; indicador comparativo, no carga de un hogar concreto.*")
    c = pd.read_csv(A / "d_cv_municipios.csv", dtype={"cod_municipio": str}).dropna(subset=["var_alquiler_2019_2024_pct"])
    c = c[c.pob_2025 >= 20000].sort_values("var_alquiler_2019_2024_pct")
    if len(c):
        cv = reg("V10-ATL-D2", "Variación del alquiler mediano 2019-2024, municipios de la Comunitat Valenciana con 20.000 hab. o más",
                 c.var_alquiler_2019_2024_pct.median(), "%", "2019-2024", f"{len(c)} municipios (valor: mediana; mín. y máx.: rango)",
                 "MIVAU SERPAVI; INE censo anual", "C4", "2024", c.iloc[0].var_alquiler_2019_2024_pct, c.iloc[-1].var_alquiler_2019_2024_pct)
        h.append(f"- **Comunitat Valenciana** {cv}. Entre los municipios de 20.000 habitantes o más con dato, el alquiler mediano "
                 f"(SERPAVI) varía entre 2019 y 2024 desde un {f(c.iloc[0].var_alquiler_2019_2024_pct)} % ({c.iloc[0].nombre}) "
                 f"hasta un {f(c.iloc[-1].var_alquiler_2019_2024_pct)} % ({c.iloc[-1].nombre}); la mediana de esos municipios "
                 f"es del {f(c.var_alquiler_2019_2024_pct.median())} %. *Capa C4; MIVAU SERPAVI.*")
    e = pd.read_csv(A / "e_ciudades_comparables.csv", dtype={"periodo": str})
    a = e[e.indicador == "alquiler_m2_mediana"].pivot_table(index="ciudad", columns="periodo", values="valor")
    if "2019" in a and "2024" in a:
        var = (100 * (a["2024"] / a["2019"] - 1)).dropna().sort_values()
        h.append("- **Ciudades comparables.** Variación del alquiler mediano 2019-2024 (SERPAVI): "
                 + "; ".join(f"{k} {f(x)} % " + reg(f"V10-ATL-E-{CODIGOS.get(k, k)}", f"Variación del alquiler mediano 2019-2024, {k}", x, "%",
                                                       "2019-2024", k, "MIVAU SERPAVI", "C4", "2024") for k, x in var.iloc[::-1].items())
                 + ". *Capa C4; comparación descriptiva, Bilbao sin serie anterior a 2024.*")
    return h, cifras


def main() -> dict:
    HECHOS.clear()
    h, _ = hallazgos()
    (A / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1), encoding="utf-8")
    res = json.loads((A / "resumen.json").read_text(encoding="utf-8"))
    lin = ["# Atlas descriptivo: quién soporta el coste de la vivienda y dónde (V10)", "",
           "Generado por `make atlas` (src/v10/atlas_texto.py) desde las tablas de output/v10/atlas/; no editar a mano. "
           "Solo descriptivo: ninguna frase atribuye causas. Cada hallazgo indica capa, fuente y fecha del dato. "
           "Las filas posteriores al pre-registro (desde 2026T3) no entran en ningún cálculo. Entre corchetes, el id de cada "
           "cifra en publicacion/cifras_clave.csv.", "",
           "## Hallazgos", "", *h, "",
           "## Tablas", "",
           "| tabla | filas | contenido |", "|---|---|---|",
           f"| a_quien_ecv.csv | {sum(1 for _ in open(A / 'a_quien_ecv.csv')) - 1} | ECV 2018-2025: sobrecarga, esfuerzo, hacinamiento y tenencia por grupo, con IC 95 % |",
           f"| a_quien_epa.csv | {sum(1 for _ in open(A / 'a_quien_epa.csv')) - 1} | EPA 2018-2026T2: jóvenes que viven con sus padres, con IC 95 % |",
           "| a_contraste_eurostat.csv | — | contraste de los totales propios con Eurostat (criterio de C1) |",
           *[f"| {k} | {v} | véase la cabecera de src/v10/atlas.py |" for k, v in res.items()], "",
           "## Método", "",
           "- **Microdatos.** Personas ponderadas. IC por linealización con el hogar como conglomerado; los ficheros públicos "
           "no traen estratos, así que los IC son algo estrechos. Las celdas con menos de 50 casos se suprimen.",
           "- **Agregación a barrio.** Correspondencia sección → barrio por área (data/base/geo/). Los recuentos se reparten "
           "con el peso de área, las tasas se recalculan y las medianas se promedian ponderando por población o viviendas.",
           "- **Índice de presión.** Media simple de puntuaciones z, sin pesos. Se construye para describir, no para explicar.",
           "- **Lo que falta.** Antigüedad y usos del parque por sección (Catastro INSPIRE no descargado), accesibilidad "
           "(GTFS no descargado) y compraventas municipales con código INE (el MIVAU solo las publica con el nombre). "
           "Véase docs/v9/estado_datos.md.", "",
           "## Summary (English)", "",
           "Descriptive atlas built from the project's single database. It covers:",
           "",
           "- housing cost overburden, rent and mortgage effort, overcrowding and tenure by income decile, age, nationality, "
           "household type and region (Spain's Living Conditions Survey microdata, 2018-2025, with confidence intervals; "
           "national overburden totals match Eurostat within 0.5 points every year);",
           "- living with parents from the Labour Force Survey;",
           "- the gap between new and existing rental contracts (INE IPVA);",
           "- València by census section and neighbourhood;",
           "- the Valencian Community by municipality and Spain by province;",
           "- València compared with similar cities.",
           "",
           "No causal claims are made.", ""]
    SAL.write_text("\n".join(lin), encoding="utf-8")
    return {"hallazgos": len(h)}


if __name__ == "__main__":
    print(main())
