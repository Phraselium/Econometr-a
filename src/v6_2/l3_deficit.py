"""L3 · Déficit 2021-2024 y 2021-2025 bajo correcciones alternativas del salto EPA 2021T1 (respuesta a A-01).

Determinista, sin red. SEED=20261010. Solo ficheros versionados (data/raw, output/v4, output/v5_1).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
from econ_utils import Registry  # noqa: E402

import pa_data  # noqa: E402

SEED = 20261010
np.random.seed(SEED)
OUT = RAIZ / "output" / "v6_2" / "L3"
OUT.mkdir(parents=True, exist_ok=True)
REG = Registry(OUT / "registro.csv")
TOL = 0.15
CORR_V1 = 242_400.0

REGLA = """## Regla de decisión (declarada ANTES de mirar los resultados finales)

1. Universo: todas las variantes de hogares (v1 constante, a, b, b4, c, d1, d2, e) cruzadas con todas las terminadas
   (MIVAU con y sin protegida; Catastro completado), SIN bajas.
2. Amplitud relativa = (máx - mín) / (máx + mín), es decir, semiamplitud sobre el punto medio. Estrecho: amplitud <= 15 % (tolerancia C1 del proyecto).
3. Independencia: hay >= 2 fuentes independientes si (i) hogares: EPA y ECP coinciden dentro de +-15 % en el cambio de hogares
   con la corrección que se elija, y (ii) terminadas: MIVAU y Catastro (territorio común) coinciden dentro de +-15 % en 2021-2024.
   Se declara que la EPA corregida con una constante o con un supuesto no es una medida independiente de la ECP en el salto.
4. Si 1-3 se cumplen: se mantiene C1 con el rango completo (nuevo mín-máx de todas las variantes sin bajas).
   Si no: C2 (cota con supuestos explícitos: la corrección del salto y la fuente de terminadas).
5. Con bajas supuestas (0,1 y 0,2 %) o estimadas (v5.1 T1): C2 como mucho (el supuesto de bajas no es un hecho). Capa final = la menor de sus componentes.
6. 2021-2025: misma regla, y capa = la menor de sus componentes (la terminadas 2025 es C4 frágil en M0).
"""


def f(x: float) -> str:
    return f"{x:,.0f}".replace(",", ".")


def hogares(q: pd.DataFrame, fin: str) -> dict[str, dict]:
    epa = q.hogares_epa * 1000.0
    ecp = q.hogares_ecp
    base = float(epa[fin] - epa["2020Q4"])
    salto = float(epa["2021Q1"] - epa["2020Q4"])
    var = epa.diff()
    t2 = float(np.mean([var["2020Q4"], var["2021Q2"]]))
    t4 = float(np.mean([var["2020Q3"], var["2020Q4"], var["2021Q2"], var["2021Q3"]]))
    r = float(ecp["2021Q1"] / epa["2021Q1"])
    pre = float(np.mean([var[k] for k in ("2020Q1", "2020Q2", "2020Q3", "2020Q4")]))
    ecp_fin = float(ecp[fin])
    return {
        "v1_constante": dict(dh=base + CORR_V1, fuente="EPA", desc="EPA + constante 242.400 (criterio v1)"),
        "a_sin_correccion": dict(dh=base, fuente="EPA", desc="EPA 2020T4-fin sin retirar el salto"),
        "b_vecinos2": dict(dh=base - salto + t2, fuente="EPA", desc="variación 2021T1 = media de 2020T4 y 2021T2"),
        "b4_vecinos4": dict(dh=base - salto + t4, fuente="EPA", desc="variación 2021T1 = media de 2020T3, T4, 2021T2, T3"),
        "c_variacion_cero": dict(dh=base - salto, fuente="EPA", desc="variación 2021T1 = 0"),
        "d1_enlace_cociente": dict(dh=ecp_fin - float(epa["2020Q4"]) * r, fuente="EPA+ECP",
                                   desc="EPA 2020T4 x (ECP/EPA en 2021T1); conserva el salto en escala ECP"),
        "d2_enlace_ecp_retropolada": dh_d2(ecp, ecp_fin, pre),
        "e_ecp": dict(dh=ecp_fin - float(ecp["2021Q1"]), fuente="ECP",
                      desc="ECP 2021T1-fin (ventana un trimestre más corta; publicado en v4)"),
    }


def dh_d2(ecp, ecp_fin, pre):
    return dict(dh=ecp_fin - (float(ecp["2021Q1"]) - pre), fuente="ECP",
                desc="ECP con nivel 2020T4 retropolado con la variación media de 2020 (ventana completa)")


def terminadas(anios: list[int], m: pd.DataFrame) -> dict[str, float]:
    tri = pd.read_csv(RAIZ / "output" / "v4" / "M0" / "terminadas_triangulacion.csv").set_index("anio").loc[anios]
    lib = m.libres.reindex(anios)
    prot = m.protegida.reindex(anios).fillna(0)
    cat_c = float(tri.catastro_dUU_res.sum())
    comp = float((tri.mivau_bruto_libres_mas_prot - tri.comun_mivau_bruto_sin_PV_NA).sum())
    return {
        "MIVAU_con_protegida": float((lib + prot).sum()),
        "MIVAU_sin_protegida": float(lib.sum()),
        "Catastro_completado": cat_c + comp,
        "_catastro_comun": cat_c,
        "_mivau_comun": float(tri.comun_mivau_bruto_sin_PV_NA.sum()),
    }


def bajas_v51(per: str) -> dict[str, float]:
    t = pd.read_csv(RAIZ / "output" / "v5_1" / "T1" / "tablas" / "deficit_con_bajas_estimadas.csv")
    t = t[t.periodo == per].set_index("escenario").bajas
    return {"v5.1_min": float(t["estimada_tasa_min"]), "v5.1_central": float(t["estimada_tasa_central"]),
            "v5.1_max": float(t["estimada_tasa_max"])}


def ventana(fin_anio: int, m: pd.DataFrame, q: pd.DataFrame) -> pd.DataFrame:
    anios = list(range(2021, fin_anio + 1))
    H = hogares(q, f"{fin_anio}Q4")
    T = terminadas(anios, m)
    park0 = m.parque.reindex([y - 1 for y in anios]).values
    per = f"2021-{fin_anio}"
    esc = {"0": 0.0, "0,1 % anual": float(np.nansum(0.001 * park0)), "0,2 % anual": float(np.nansum(0.002 * park0))}
    esc.update({k: v for k, v in bajas_v51(per).items()})
    filas = []
    for hn, h in H.items():
        for tn in ("MIVAU_con_protegida", "MIVAU_sin_protegida", "Catastro_completado"):
            for bn, bv in esc.items():
                filas.append({"periodo": per, "hogares": hn, "fuente_hogares": h["fuente"], "delta_hogares": round(h["dh"]),
                              "terminadas_fuente": tn, "terminadas": round(T[tn]), "bajas_escenario": bn,
                              "bajas": round(bv), "deficit": round(h["dh"] - (T[tn] - bv)),
                              "tipo_bajas": "ninguna" if bn == "0" else ("supuesto" if "%" in bn else "estimada v5.1 (C4)")})
    t = pd.DataFrame(filas)
    t.attrs["T"] = T
    t.attrs["H"] = H
    return t


def amplitud(lo: float, hi: float) -> float:
    return (hi - lo) / (hi + lo)


def main() -> None:
    q = pa_data.nacional_q()
    m = pa_data.mivau_nacional_anual()
    res = {}
    tablas = []
    for fin in (2024, 2025):
        t = ventana(fin, m, q)
        sb = t[t.bajas_escenario == "0"]
        lo, hi = float(sb.deficit.min()), float(sb.deficit.max())
        T, H = t.attrs["T"], t.attrs["H"]
        dif_term = abs(T["_catastro_comun"] - T["_mivau_comun"]) / np.mean([T["_catastro_comun"], T["_mivau_comun"]])
        epa_c = [H[k]["dh"] for k in ("b_vecinos2", "b4_vecinos4", "c_variacion_cero")]
        ecp = H["e_ecp"]["dh"]
        dif_h = max(abs(x - ecp) / np.mean([x, ecp]) for x in epa_c)
        amp = amplitud(lo, hi)
        indep = bool(dif_h <= TOL and dif_term <= TOL)
        c1 = bool(amp <= TOL and indep)
        cb = t[t.tipo_bajas != "ninguna"]
        res[fin] = dict(min_sb=lo, max_sb=hi, punto_medio=(lo + hi) / 2, amplitud=amp, dif_hogares_epa_ecp=float(dif_h),
                        dif_terminadas_catastro_mivau_comun=float(dif_term), indep=indep, c1=c1,
                        min_cb=float(t.deficit.min()), max_cb=float(t.deficit.max()),
                        max_cb_supuesto=float(t[t.tipo_bajas == "supuesto"].deficit.max()),
                        por_hogares={k: [float(sb[sb.hogares == k].deficit.min()), float(sb[sb.hogares == k].deficit.max())] for k in H},
                        por_terminadas={k: [float(sb[sb.terminadas_fuente == k].deficit.min()), float(sb[sb.terminadas_fuente == k].deficit.max())]
                                        for k in ("MIVAU_con_protegida", "MIVAU_sin_protegida", "Catastro_completado")},
                        dh={k: v["dh"] for k, v in H.items()}, term={k: v for k, v in T.items()},
                        bajas_estimadas=bajas_v51(f"2021-{fin}"), n_cb=int(len(cb)))
        tablas.append(t)
        for r in t.itertuples():
            REG.log("L3", f"{r.periodo}|{r.hogares}|{r.terminadas_fuente}|{r.bajas_escenario}", "dH - (terminadas - bajas)",
                    2021, fin, 4 if fin == 2024 else 5, np.nan, np.nan, np.nan, coef_interes=r.deficit)
    full = pd.concat(tablas, ignore_index=True)
    full.to_csv(OUT / "deficit_alternativas.csv", index=False)

    r4, r5 = res[2024], res[2025]
    capa4 = "C1" if r4["c1"] else "C2"
    capa5 = "C4"  # la menor de sus componentes: terminadas 2025 = C4 frágil en M0 (no se promueve)
    capa4_cb = "C2"
    capa5_cb = "C4"
    hechos = [
        dict(id="L3-DEF-2124-SINBAJAS", indicador="Déficit acumulado 2021-2024 sin bajas (todas las variantes de corrección EPA y de terminadas)",
             valor=round(r4["punto_medio"]), min=round(r4["min_sb"]), max=round(r4["max_sb"]), unidad="viviendas", periodo="2021-2024",
             cobertura="España", fuentes="hogares: EPA (varias correcciones) y ECP; terminadas: MIVAU y Catastro", capa=capa4,
             fecha_dato="2024T4", amplitud_rel=round(r4["amplitud"], 4)),
        dict(id="L3-DEF-2124-CONBAJAS", indicador="Déficit acumulado 2021-2024 con bajas supuestas 0,1-0,2 % anual (cota)",
             valor=round((r4["min_sb"] + r4["max_cb_supuesto"]) / 2), min=round(r4["min_sb"]), max=round(r4["max_cb_supuesto"]),
             unidad="viviendas", periodo="2021-2024", cobertura="España", fuentes="ídem, con bajas supuestas", capa=capa4_cb,
             fecha_dato="2024T4"),
        dict(id="L3-DEF-2125", indicador="Déficit acumulado 2021-2025 sin bajas (todas las variantes)", valor=round(r5["punto_medio"]),
             min=round(r5["min_sb"]), max=round(r5["max_sb"]), unidad="viviendas", periodo="2021-2025", cobertura="España",
             fuentes="hogares: EPA y ECP; terminadas: MIVAU y Catastro (2025 frágil)", capa=capa5, fecha_dato="2025T4",
             amplitud_rel=round(r5["amplitud"], 4)),
    ]
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    resultado = {
        "rama": "L3",
        "pregunta": "¿Depende la capa C1 del déficit 2021-2024 de la constante de corrección del salto EPA 2021T1 y de una sola fuente de terminadas? (A-01)",
        "capa": capa4,
        "datos": "INE EPA hogares y ECP (trimestral, hasta 2025T4), MIVAU terminadas libres y protegida, Catastro unidades urbanas residenciales, bajas v5.1 T1",
        "N": int(len(full)),
        "metodo": "Recálculo determinista de dH - (terminadas - bajas) bajo 8 correcciones de hogares x 3 fuentes de terminadas x 6 escenarios de bajas; regla de decisión pre-declarada",
        "estimacion": {"2021-2024_sin_bajas": [r4["min_sb"], r4["max_sb"]], "2021-2025_sin_bajas": [r5["min_sb"], r5["max_sb"]]},
        "ic95": None,
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO (contabilidad del déficit; rango por supuestos, no intervalo de confianza)",
        "diagnosticos": {"2024": {k: v for k, v in r4.items() if k not in ("term",)}, "2025": {k: v for k, v in r5.items() if k not in ("term",)}},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Capa 2021-2024 sin bajas: %s. Capa 2021-2025: %s. Censo 2021 como ancla: no disponible como cifra de hogares nacional versionada; la ECP ya está anclada a él." % (capa4, capa5),
    }
    (OUT / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    REG.flush()
    escribir_md(res, full, capa4)
    print(json.dumps({k: {x: v[x] for x in ("min_sb", "max_sb", "amplitud", "dif_hogares_epa_ecp", "dif_terminadas_catastro_mivau_comun",
                                           "indep", "c1", "max_cb_supuesto", "max_cb")} for k, v in res.items()}, indent=1, default=float))


def sensibilidad(full: pd.DataFrame) -> str:
    """Sensibilidad POSTERIOR a la regla (no la sustituye): sin las dos variantes que conservan el quiebre de la EPA (a y d1)."""
    x = full[(full.periodo == "2021-2024") & (full.bajas_escenario == "0") & ~full.hogares.isin(["a_sin_correccion", "d1_enlace_cociente"])]
    lo, hi = float(x.deficit.min()), float(x.deficit.max())
    return (f"Sensibilidad (posterior a la regla, no la sustituye): sin las variantes a y d1, que conservan el quiebre metodológico de la EPA, "
            f"el rango 2021-2024 sin bajas es {f(lo)}-{f(hi)} (amplitud {100 * amplitud(lo, hi):.1f} %). La regla pre-declarada incluía todas las variantes; "
            f"la capa C2 se mantiene. Lo que decide es qué variantes se aceptan, es decir, un supuesto sobre el salto.")


def escribir_md(res: dict, full: pd.DataFrame, capa4: str) -> None:
    L = ["# L3 · Déficit 2021-2024 y 2021-2025 bajo correcciones alternativas del salto EPA 2021T1", "",
         "Respuesta a la objeción A-01 del informe del árbitro. Datos: INE EPA (2020T4-2025T4) y ECP (2021T1-2025T4); MIVAU terminadas; Catastro (1-ene de cada ejercicio); bajas v5.1 T1.", "",
         REGLA, "## Variantes de hogares", ""]
    for fin in (2024, 2025):
        r = res[fin]
        L += [f"### Cambio de hogares hasta {fin}T4 (viviendas)", "", "| variante | fuente | cambio de hogares | descripción |", "|---|---|---|---|"]
        H = hogares(pa_data.nacional_q(), f"{fin}Q4")
        for k, v in H.items():
            L.append(f"| {k} | {v['fuente']} | {f(v['dh'])} | {v['desc']} |")
        L.append("")
    L += ["Censo 2021 como ancla: no hay una cifra nacional de hogares del Censo versionada en data/raw; la ECP ya está rebasada sobre el Censo 2021, de modo que no añade una medida independiente del cambio de hogares.", ""]
    L += ["## Resultados sin bajas", "", "| periodo | mín | máx | punto medio | amplitud rel. | EPA vs ECP (máx. dif.) | Catastro vs MIVAU común | >=2 fuentes | capa |", "|---|---|---|---|---|---|---|---|---|"]
    for fin in (2024, 2025):
        r = res[fin]
        capa = capa4 if fin == 2024 else "C4"
        L.append(f"| 2021-{fin} | {f(r['min_sb'])} | {f(r['max_sb'])} | {f(r['punto_medio'])} | {100 * r['amplitud']:.1f} % | {100 * r['dif_hogares_epa_ecp']:.1f} % | {100 * r['dif_terminadas_catastro_mivau_comun']:.1f} % | {'sí' if r['indep'] else 'no'} | {capa} |")
    L += ["", "Rango sin bajas por variante de hogares (mín-máx entre las 3 fuentes de terminadas):", "", "| variante | 2021-2024 | 2021-2025 |", "|---|---|---|"]
    for k in res[2024]["por_hogares"]:
        a, b = res[2024]["por_hogares"][k], res[2025]["por_hogares"][k]
        L.append(f"| {k} | {f(a[0])} - {f(a[1])} | {f(b[0])} - {f(b[1])} |")
    L += ["", "Rango sin bajas por fuente de terminadas (mín-máx entre variantes de hogares):", "", "| terminadas | 2021-2024 | 2021-2025 |", "|---|---|---|"]
    for k in res[2024]["por_terminadas"]:
        a, b = res[2024]["por_terminadas"][k], res[2025]["por_terminadas"][k]
        L.append(f"| {k} | {f(a[0])} - {f(a[1])} | {f(b[0])} - {f(b[1])} |")
    L += ["", "Terminadas acumuladas (viviendas): " + "; ".join(f"2021-{y}: " + ", ".join(f"{k} {f(v)}" for k, v in res[y]["term"].items() if not k.startswith("_")) for y in (2024, 2025)) + ".", "",
          "Catastro completado = unidades urbanas residenciales de territorio común + (MIVAU nacional - MIVAU común) para País Vasco y Navarra; no es una fuente totalmente independiente. Las unidades urbanas no son viviendas (ratio 0,944 respecto al Censo 2021).", "",
          "## Con bajas", "",
          "Bajas supuestas 0,1 y 0,2 % anual del parque del año anterior; bajas estimadas de v5.1 T1 (C4, fuente única de licencias y catastro): "
          + "; ".join(f"2021-{y}: " + ", ".join(f"{k} {f(v)}" for k, v in res[y]["bajas_estimadas"].items()) for y in (2024, 2025)) + ".", "",
          "| periodo | mín con bajas (cualquier escenario) | máx con supuestos 0,1-0,2 % | máx con cualquier escenario |", "|---|---|---|---|"]
    for fin in (2024, 2025):
        r = res[fin]
        L.append(f"| 2021-{fin} | {f(r['min_cb'])} | {f(r['max_cb_supuesto'])} | {f(r['max_cb'])} |")
    r4 = res[2024]
    L += ["", "## Aplicación de la regla", "",
          f"- Amplitud relativa 2021-2024 sin bajas: {100 * r4['amplitud']:.1f} % (umbral 15 %): {'cumple' if r4['amplitud'] <= TOL else 'NO cumple'}.",
          f"- EPA corregida vs ECP: máxima diferencia {100 * r4['dif_hogares_epa_ecp']:.1f} %; Catastro vs MIVAU (común, 2021-2024): {100 * r4['dif_terminadas_catastro_mivau_comun']:.1f} %.",
          f"- Capa final 2021-2024 sin bajas: **{capa4}**, rango {f(r4['min_sb'])}-{f(r4['max_sb'])} viviendas. Con bajas supuestas: **C2**, {f(r4['min_sb'])}-{f(r4['max_cb_supuesto'])}.",
          f"- 2021-2025: {f(res[2025]['min_sb'])}-{f(res[2025]['max_sb'])} sin bajas, capa C4 (la terminadas 2025 es C4 frágil en M0; no se promueve).", "",
          sensibilidad(full), "",
          "Tabla completa: deficit_alternativas.csv (%d filas)." % len(full), "",
          "Nota: d1 conserva el salto (la razón ECP/EPA alinea el nivel posterior, no el anterior) y es el extremo bajo; se reporta junto con d2, que usa la ECP con ventana completa."]
    (OUT / "deficit_alternativas.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
