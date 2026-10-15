"""V12-B8 · cifras clave de V12 → output/v12/hechos/hechos.json (formato estándar que lee src/v5/cifras_clave.py).

Ids «V12-<bloque>-…». Solo cifras ya calculadas en output/v12/b1-b7 (este script no calcula nada nuevo). Capa C4 en
todas (descriptivas o contables, una fuente por nivel); los rangos son el intervalo de confianza (muestras) o los dos
órdenes de la descomposición (B3).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
O = RAIZ / "output" / "v12"


def h(i, indicador, valor, unidad, periodo, cobertura, fuentes, fecha, mn=None, mx=None, capa="C4", ficha="—"):
    f = lambda x: None if x is None or pd.isna(x) else float(x)  # noqa: E731
    return {"id": i, "indicador": indicador, "valor": f(valor), "min": f(mn), "max": f(mx), "unidad": unidad, "periodo": periodo,
            "cobertura": cobertura, "fuentes": fuentes, "capa": capa, "fecha_dato": fecha, "ficha": ficha}


def main() -> int:
    H = []
    # B1
    n = pd.read_csv(O / "b1/contabilidad_periodos_nacional.csv")
    n = n[n.nac == "TOTAL"].set_index("periodo")
    F1 = "INE: padrón y censo anual, MNP, EVR (hasta 2020) y EMCR (desde 2021); cálculo V12-B1"
    for p, r in n.iterrows():
        for c, et in (("crecimiento", "Crecimiento de la población"), ("vegetativo", "Saldo vegetativo (nacimientos − defunciones)"),
                      ("saldo_exterior", "Saldo migratorio con el extranjero"), ("residuo", "Residuo de la identidad demográfica")):
            H.append(h(f"V12-B1-{p}-{c}", f"{et}, España, {p}", r[c], "personas", p, "España", F1, p[-4:]))
    v = json.loads((O / "b1/resultado.json").read_text(encoding="utf-8"))["valencia"]
    for k, et in (("var_total", "Variación de la población de València"), ("var_espanola", "Variación de la población de nacionalidad española, València"),
                  ("var_extranjera", "Variación de la población de nacionalidad extranjera, València")):
        H.append(h(f"V12-B1-VLC-{k}", et + ", 2021-2025", v[k], "personas", "2021-2025", "València", "INE, censo anual por sección", "2025-01-01"))
    # B2
    p = pd.read_csv(O / "b2/flujos_area_periodos.csv")
    t = p[p.periodo == "2022-2024"].groupby("area")[["saldo_capital_con_corona", "capital_a_corona"]].sum()
    for a, r in t.iterrows():
        H.append(h(f"V12-B2-{a}-saldo-corona", f"Saldo de la capital con su corona metropolitana ({a}), 2022-2024", r.saldo_capital_con_corona,
                   "personas", "2022-2024", a, "INE, EMCR (microdatos origen-destino); V12-B2", "2024"))
    # B3
    d = pd.read_csv(O / "b3/descomposicion_2011_2021_nacional.csv").iloc[0]
    F3 = "INE, Censos 2011 y 2021 (microdatos); ECP; V12-B3"
    H.append(h("V12-B3-hogares-crec", "Crecimiento del número de hogares, España, 2011-2021", d.crecimiento, "hogares", "2011-2021", "España", F3, "2021-01-01"))
    for c, et in (("poblacion", "población"), ("estructura", "estructura por edad"), ("jefatura", "tasa de jefatura")):
        a, b = d[f"{c}_A"], d[f"{c}_B"]
        H.append(h(f"V12-B3-hogares-{c}", f"Componente «{et}» del crecimiento de hogares 2011-2021 (media de los dos órdenes; rango = órdenes)",
                   (a + b) / 2, "hogares", "2011-2021", "España", F3, "2021-01-01", min(a, b), max(a, b)))
    rr = pd.read_csv(O / "b3/hogares_reciente_provincia.csv").sum(numeric_only=True)
    per = pd.read_csv(O / "b3/hogares_reciente_provincia.csv").periodo.iloc[0]
    for c, et in (("crecimiento_observado", "Crecimiento de hogares (ECP)"), ("efecto_poblacion", "Componente población"),
                  ("efecto_estructura_edad", "Componente estructura por edad"), ("cambio_jefatura_implicito", "Cambio implícito de jefatura")):
        H.append(h(f"V12-B3-reciente-{c}", f"{et}, España, {per}", rr[c], "hogares", per, "España (suma de provincias)", "INE, ECP y Censo 2021; V12-B3", per[-4:] + "-01-01"))
    nh = pd.read_csv(O / "b3/hogares_nacionalidad_censo2021.csv")
    x = nh[nh.nivel == "nacional"].iloc[0]
    H.append(h("V12-B3-hogares-ext", "Hogares cuya persona de referencia tiene nacionalidad extranjera, España", x.cuota_ext_pct, "%", "2021", "España",
               "INE, Censo 2021 (muestra de hogares); V12-B3", "2021-01-01", x.ic95_inf, x.ic95_sup))
    # B4
    r4 = json.loads((O / "b4/resultado.json").read_text(encoding="utf-8"))
    pv = r4["provincia_2021_2025"]
    F4 = "Catastro (URBANA); MIVAU; INE ECP; V12-B4"
    H.append(h("V12-B4-hogares-nuevos", f"Hogares nuevos (ECP), 1-1-2021 → 1-1-2025, {pv['provincias']} provincias con Catastro y MIVAU", pv["hogares_nuevos_ecp"], "hogares", "2021-2024",
               "España sin País Vasco, Navarra, Ceuta ni Melilla", F4, "2025-01-01"))
    H.append(h("V12-B4-obra-catastro", "Obra nueva neta (Catastro, unidades residenciales), 2021-2024", pv["obra_neta_catastro"], "viviendas", "2021-2024",
               "España sin País Vasco, Navarra, Ceuta ni Melilla", F4, "2024-12-31"))
    H.append(h("V12-B4-terminadas-mivau", "Viviendas terminadas (MIVAU: libres + protegidas), 2021-2024", pv["terminadas_mivau"], "viviendas", "2021-2024",
               "España sin País Vasco, Navarra, Ceuta ni Melilla", F4, "2024"))
    H.append(h("V12-B4-regularizacion", "Exceso del Catastro sobre el MIVAU en 2013-2017 (regularización catastral)", r4["regularizacion_2013_2017_catastro_menos_mivau"],
               "viviendas", "2013-2017", "España sin País Vasco ni Navarra", F4, "2017"))
    # B5
    t5 = pd.read_csv(O / "b5/titularidad_cuotas.csv", dtype={"cod_territorio": str})
    u = int(t5.anio.max())
    r = t5[(t5.nivel == "nacional") & (t5.anio == u)].iloc[0]
    F5 = "Catastro, titularidad por tramo de inmuebles y tipo de persona (uso residencial); V12-B5"
    for c, et in (("pct_mas10", "Viviendas de titulares con más de 10 viviendas"), ("pct_mas100", "Viviendas de titulares con más de 100 viviendas"),
                  ("pct_PJ", "Viviendas de personas jurídicas privadas"), ("pct_PE", "Viviendas de entidades públicas"), ("pct_PF", "Viviendas de personas físicas")):
        H.append(h(f"V12-B5-{c}", f"{et}, España sin País Vasco ni Navarra, {u}", r[c], "%", str(u), "España sin País Vasco ni Navarra", F5, str(u), ficha="V12-V02"))
    f5 = json.loads((O / "b5/fichas_verificador_v12.json").read_text(encoding="utf-8"))
    del f5
    # B6
    b6 = pd.read_csv(O / "b6/ecv_brecha_misma_edad_renta.csv").set_index("indicador")
    F6 = "INE, ECV (microdatos); V12-B6"
    nombres = {"sobrecarga_40": "Sobrecarga > 40 %", "hacinamiento": "Hacinamiento", "esfuerzo_alquiler_30": "Alquiler > 30 % de la renta (inquilinos de mercado)",
               "tenencia_3": "Alquiler a precio de mercado"}
    for i, et in nombres.items():
        r6 = b6.loc[i]
        H.append(h(f"V12-B6-brecha-{i}", f"{et}: hogares extranjeros − españoles de igual edad y renta (puntos)", r6.diferencia_estandarizada, "puntos",
                   r6.periodo, "España", F6, f"ECV {r6.periodo[-4:]}", r6.ic95_inf, r6.ic95_sup))
    # B7
    r7 = json.loads((O / "b7/resultado.json").read_text(encoding="utf-8"))
    cv = r7["cv"]
    k = [c for c in cv if c.startswith("vut_ine_2") and c != "vut_ine_2021_08"][0]
    F7 = "INE (viviendas turísticas, experimental); GVA (registro); V12-B7"
    H.append(h("V12-B7-CV-vut-ine", "Viviendas turísticas anunciadas (INE), Comunitat Valenciana", cv[k], "viviendas", k[-7:], "Comunitat Valenciana", F7, k[-7:]))
    H.append(h("V12-B7-CV-vut-registro", "Viviendas turísticas inscritas en el registro de la GVA, Comunitat Valenciana", cv["registro_gva_2026_10_14"], "viviendas",
               "2026-10-14", "Comunitat Valenciana", F7, "2026-10-14"))
    vl = r7["valencia"]
    H.append(h("V12-B7-VLC-vut-ine", "Viviendas turísticas anunciadas (INE), València", vl[k], "viviendas", k[-7:], "València", F7, k[-7:]))
    H.append(h("V12-B7-VLC-vut-registro", "Viviendas turísticas inscritas en el registro de la GVA, València", vl["registro_gva_2026_10_14"], "viviendas",
               "2026-10-14", "València", F7, "2026-10-14"))
    (O / "hechos").mkdir(parents=True, exist_ok=True)
    (O / "hechos" / "hechos.json").write_text(json.dumps(H, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(H), "cifras V12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
