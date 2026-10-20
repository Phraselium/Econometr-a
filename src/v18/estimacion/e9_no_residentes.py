"""V18 · E9 (compradores no residentes: Badarinza y Ramadorai 2018; Sá 2016; Cvijanović y Spaenjers 2021) · cuenta de choques efectivos y estimabilidad.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md, 1.9, + adenda 1.3, 1.13 y AD-E9). SEED = 20261010; sin red.
Orden fijado por la adenda: ANTES de estimar nada se cuenta 1/HHI de los pesos de los choques (origen × exposición histórica) con la exposición del padrón de 2003 y solo los orígenes
con serie de riesgo en origen (Eurostat/OCDE); con 1/HHI < 10, E9-R1 y E9-R2 (y las ampliaciones que usan el mismo índice, A1 y A2) son NO ESTIMABLES (adenda 1.3 y 1.13).
X1 (fin de la golden visa) y X2 (introducción de 2013) son NO ESTIMABLES por datos (plan 1.9 g). No se estima ningún coeficiente en este módulo.
Salidas: output/v18/estimacion/e9/{resultado.json, tabla.csv, informe.md, hechos.json, registro.csv, choques.csv}.
Uso: python3 src/v18/estimacion/e9_no_residentes.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e359_comun as K  # noqa: E402
import _e359_datos as D  # noqa: E402

SALIDA = K.OUT / "e9"
UMBRAL = 10          # 1/HHI mínimo (adenda 1.3 y 1.13)
# Nacionalidades individuales del padrón provincial con código de país de las series de riesgo (eu_hpi, oecd_house_prices, eu_income_emp)
PAIS_RIESGO = {"Alemania": "DE", "Francia": "FR", "Italia": "IT", "Portugal": "PT", "Reino Unido": "UK", "Rumanía": "RO", "Bulgaria": "BG", "Polonia": "PL"}
EXCL = ("Total", "Española", "Extranjera")
AGR = ("De ", "Europa", "País", "Oceanía")
SPEC = [("E9-R1", "principal", "Badarinza-Ramadorai, forma reducida: Δ ln precio sobre exposición a nacionalidades × riesgo en origen (caída del PIB en el quintil superior de su historia, a 4 trimestres)", "SUGESTIVO"),
        ("E9-R2", "principal", "Sá, IV: Δ ln precio sobre Δ cuota de no residentes en las compras, instrumentada por el índice de R1", "IDENTIFICADO"),
        ("E9-A1", "principal", "R1 con el tipo de cambio como choque (libra en 2016 y otras monedas fuera del euro)", "SUGESTIVO"),
        ("E9-A2", "principal", "R2 con compras de extranjeros residentes (CCAA, 9 no selladas) como primera etapa alternativa", "IDENTIFICADO"),
        ("E9-X1", "principal", "fin de la golden visa (LO 1/2025) como diferencias en diferencias, UE frente a fuera de la UE", "NO ESTIMABLE"),
        ("E9-X2", "principal", "introducción de 2013 (Martínez-Toledano et al.)", "NO ESTIMABLE")]
DATOS = ("(i) compras de no residentes por nacionalidad del comprador y provincia (Notariado, Registradores o la estadística del Ministerio con detalle de nacionalidad), para una exposición por compradores y no por "
         "residentes, con al menos 10 choques efectivos; (ii) series de riesgo en origen para los países latinoamericanos, africanos y asiáticos (PIB, tipo de cambio) y no solo para 31 países europeos; "
         "(iii) autorizaciones de residencia por inversión de la OPI y compras por nacionalidad UE/fuera de la UE y provincia para X1 (tareas_autor, puntos 7 y 14); (iv) el universo de transacciones para X2; "
         "(v) las 4 provincias selladas de más cuota de no residentes (Baleares, Las Palmas, Santa Cruz de Tenerife y Murcia), que no se leen")


def padron2003(provincias: list[str]) -> pd.DataFrame:
    p = K.leer_hechos("padron_pob_nacionalidad", "provincia", "A")
    p = p[p["periodo"] == "2003"].copy()
    p["nac"] = p["desagregacion"].str.replace("nacionalidad=", "", regex=False)
    w = p.pivot_table(index="territorio_codigo", columns="nac", values="valor", aggfunc="first")
    return w.loc[[q for q in w.index if q in provincias]]


def series_de_riesgo() -> dict[str, list[str]]:
    """Países con serie de riesgo trimestral en origen (Eurostat eu_hpi y OCDE oecd_house_prices; sellado de V18: eu_hpi|pais|T y oecd_hpi|pais|T)."""
    out = {}
    h = pd.read_csv(K.RAW / "eu_hpi.csv", keep_default_na=False)
    h = h[h["unit"] == "I15_Q"].copy()
    h["periodo"] = h["periodo"].astype(str).str.replace("-Q", "T", regex=False)
    h["cod"] = h["territorio"]
    h["valor"] = pd.to_numeric(h["valor"], errors="coerce")
    h = K.filtrar(h[["cod", "periodo", "valor"]].dropna(), "cod", "pais", "periodo", "eu_hpi", "T")
    n = h.groupby("cod")["valor"].count()
    out["eu_hpi"] = sorted(n[n >= 40].index)
    o = pd.read_csv(K.RAW / "oecd_house_prices.csv", keep_default_na=False)
    o = o[o["frecuencia"] == "Q"].copy()
    o["periodo"] = o["periodo"].astype(str).str.replace("-Q", "T", regex=False)
    o["cod"] = o["territorio"]
    o["valor"] = pd.to_numeric(o["valor"], errors="coerce")
    o = K.filtrar(o[["cod", "periodo", "valor"]].dropna(), "cod", "pais", "periodo", "oecd_hpi", "T")
    n = o.groupby("cod")["valor"].count()
    out["oecd_hpi"] = sorted(n[n >= 40].index)
    return out


def main() -> int:
    t0 = time.time()
    SALIDA.mkdir(parents=True, exist_ok=True)
    reg = K.Registry(SALIDA / "registro.csv")
    P = list(K.PROVINCIAS_ENTRENAMIENTO)
    w = padron2003(P)
    tot = w["Total"]
    paises = [c for c in w.columns if c not in EXCL and not c.startswith(AGR)]
    S = w[paises].div(tot, axis=0)                      # exposición s_pc = residentes de la nacionalidad c / población, 2003
    pesos_pob = tot / tot.sum()
    riesgo = series_de_riesgo()
    cod_ok = set(riesgo["eu_hpi"]) | {"GBR" if "GBR" in riesgo["oecd_hpi"] else "XX"}
    origenes_riesgo = [n for n, c in PAIS_RIESGO.items() if n in paises and (c in riesgo["eu_hpi"] or c in cod_ok)]

    def inv(cols: list[str], pesos: pd.Series | None) -> tuple[float, dict]:
        ww = np.ones(len(S)) if pesos is None else pesos.reindex(S.index).to_numpy(float)
        s_c = (ww[:, None] * S[cols].to_numpy(float)).sum(axis=0)
        return K.inv_hhi(s_c), {c: float(v) for c, v in zip(cols, s_c / s_c.sum())}
    filas = {}
    for nombre, cols in (("origenes_con_serie_de_riesgo", origenes_riesgo), ("todos_los_paises_del_padron_(informacion)", paises)):
        for etiqueta, pesos in (("sin pesos", None), ("pesos de población 2003", pesos_pob)):
            v, d = inv(cols, pesos)
            filas[(nombre, etiqueta)] = {"n_origenes": len(cols), "inv_hhi": v, "pesos": d}
    # por origen × año: cada origen con riesgo trimestral de 2007T1 a 2025T4 (76 trimestres): los choques de un mismo origen están muy correlacionados en el tiempo
    n_trim = 76
    v_o, d_o = inv(origenes_riesgo, None)
    ninfo = {"n_trimestres": n_trim, "inv_hhi_origen_trimestre_si_fueran_independientes": v_o * n_trim, "nota": "cota superior irreal: los choques de un origen son persistentes (PIB y empleo en origen)"}
    principal = filas[("origenes_con_serie_de_riesgo", "sin pesos")]
    estimable = bool(principal["inv_hhi"] >= UMBRAL)
    print(f"[{time.time() - t0:3.0f}s] orígenes con serie de riesgo: {origenes_riesgo}; 1/HHI sin pesos {principal['inv_hhi']:.2f}; con pesos de población "
          f"{filas[('origenes_con_serie_de_riesgo', 'pesos de población 2003')]['inv_hhi']:.2f}; todos los países del padrón {filas[('todos_los_paises_del_padron_(informacion)', 'sin pesos')]['inv_hhi']:.2f}", flush=True)
    peor = max(filas[("origenes_con_serie_de_riesgo", e)]["inv_hhi"] for e in ("sin pesos", "pesos de población 2003"))
    motivo = (f"NO ESTIMABLE por choques efectivos: 1/HHI = {principal['inv_hhi']:.2f} sin pesos y {filas[('origenes_con_serie_de_riesgo', 'pesos de población 2003')]['inv_hhi']:.2f} con pesos de población "
              f"(< {UMBRAL}; adenda 1.3 y 1.13) con {len(origenes_riesgo)} orígenes que tienen serie de riesgo")
    filas_t = []
    for sid, rol, desc, tope in SPEC:
        if sid in ("E9-X1", "E9-X2"):
            mot = {"E9-X1": "no hay compras separadas entre la UE y fuera de la UE por provincia ni autorizaciones de la OPI (tareas_autor, puntos 7 y 14)",
                   "E9-X2": "requiere el universo de transacciones (Registradores o Notariado)"}[sid]
        elif estimable:
            mot = "estimable por choques efectivos (no se estima aquí)"
        else:
            mot = motivo
        reg.log("v18-E9", f"{sid}|registrada", desc, 2007, 2025, 0, np.nan, np.nan, np.nan, notas=mot)
        filas_t.append({"id": sid, "rol": rol, "descripcion": desc, "tope_tabla": tope, "estado": "NO ESTIMABLE" if sid.startswith("E9-X") or not estimable else "estimable", "motivo": mot,
                        "inv_hhi": principal["inv_hhi"], "umbral": UMBRAL, "clase": "NO ESTIMABLE" if (sid.startswith("E9-X") or not estimable) else "pendiente"})
    tabla = pd.DataFrame(filas_t)
    tabla.to_csv(SALIDA / "tabla.csv", index=False)
    pd.DataFrame([{"conjunto": k[0], "pesos": k[1], "n_origenes": v["n_origenes"], "inv_hhi": v["inv_hhi"], **{f"peso_{c}": p for c, p in v["pesos"].items()}} for k, v in filas.items()]).to_csv(
        SALIDA / "choques.csv", index=False)
    reg.flush()
    esp = {r["id"]: {"rol": r["rol"], "descripcion": r["descripcion"], "clasificacion_v18": r["clase"], "motivo": r["motivo"], "inv_hhi": r["inv_hhi"], "umbral": UMBRAL, "capa": "C4",
                    "nivel_evidencia": "EXPLORATORIO", "datos_que_lo_harian_estimable": DATOS} for r in filas_t}
    out = {"rama": "v18/estimacion/e9", "pregunta": "¿Se asocia el riesgo en el país de origen, ponderado por la exposición histórica de cada provincia a cada nacionalidad, con el precio de la vivienda?",
           "capa": "C4", "datos": "Padrón de 2003 por nacionalidad y provincia (39 provincias de entrenamiento; exposición por residentes, aproximación a la de compradores); series de riesgo de Eurostat y OCDE",
           "N": int(len(S)), "metodo": "recuento de choques efectivos (1/HHI de BHJ) antes de estimar, regla de la adenda: 1/HHI < 10 implica NO ESTIMABLE", "estimacion": None, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "NO ESTIMABLE" if not estimable else "pendiente",
           "diagnosticos": {"origenes_con_serie_de_riesgo": origenes_riesgo, "paises_con_serie_eu_hpi": riesgo["eu_hpi"], "paises_con_serie_oecd": riesgo["oecd_hpi"],
                            "inv_hhi": {f"{k[0]}|{k[1]}": {"n_origenes": v["n_origenes"], "inv_hhi": v["inv_hhi"]} for k, v in filas.items()}, "pesos_por_origen_sin_pesos": principal["pesos"],
                            "origen_trimestre": ninfo, "umbral": UMBRAL, "familia_holm": {"m": 0, "nota": "las NO ESTIMABLES salen antes de ajustar (adenda 1.7)"},
                            "doble_computo_E3_E9": "E9 no tiene instrumento estimable: la fila alternativa de E9 en la contabilidad queda vacía y no hay correlación entre instrumentos que publicar (adenda 1.10)",
                            "b5": "E9-R2 es la estimación propia de E9 para B5 y es NO ESTIMABLE por choques efectivos: no hay respaldo; entra solo la literatura (Sá, +2 % por pp de cuota)"},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None, "nota": "no se estima"},
           "notas": ["análisis V18; capa C4; pre-registro interno plan-replicacion-v18", "sin coeficiente: la regla de choques efectivos de la adenda 1.3 y 1.13 deja NO ESTIMABLES E9-R1, R2, A1 y A2",
                     "signo esperado fijado en la adenda: positivo; no hay resultado que lo contraste", "desviaciones: docs/v18/desviaciones_e3_e5_e9.md (D-E9-1, D-E9-2)"],
           "especificaciones": esp}
    K.volcar_json(SALIDA / "resultado.json", out)
    fu = ["Padrón por nacionalidad 2003 (INE)", "Eurostat eu_hpi", "OCDE house prices"]
    cl = "NO ESTIMABLE" if not estimable else "SUGESTIVO"
    H = [K.hecho("V18-E9-1HHI-origenes", "E9: número efectivo de choques (1/HHI de los pesos por origen) con exposición del padrón de 2003 y serie de riesgo en origen, sin pesos",
                 principal["inv_hhi"], None, None, "choques efectivos", "2003 (exposición); 2007-2025 (riesgo)", f"{len(origenes_riesgo)} orígenes con serie de riesgo; 39 provincias de entrenamiento", fu, cl,
                 f"Umbral de la adenda: 10. Orígenes: {', '.join(origenes_riesgo)}."),
         K.hecho("V18-E9-1HHI-pesos-poblacion", "E9: número efectivo de choques con pesos de población de 2003", filas[("origenes_con_serie_de_riesgo", "pesos de población 2003")]["inv_hhi"], None, None,
                 "choques efectivos", "2003", f"{len(origenes_riesgo)} orígenes", fu, cl, "Umbral de la adenda: 10."),
         K.hecho("V18-E9-1HHI-todos-paises", "E9: número efectivo de choques si los 28 países del padrón tuvieran serie de riesgo (información)", filas[("todos_los_paises_del_padron_(informacion)", "sin pesos")]["inv_hhi"],
                 None, None, "choques efectivos", "2003", "28 países del padrón", fu, cl, "Solo información: los países no europeos no tienen serie de riesgo en el repositorio.")]
    K.volcar_json(SALIDA / "hechos.json", H)
    L = ["# V18 · E9 Compradores no residentes: recuento de choques efectivos", f"\n*{K.ROTULO}.* Generado por `python3 src/v18/estimacion/e9_no_residentes.py` (SEED 20261010, sin red). Clasificaciones provisionales: pendientes de I8. Toda cifra es C4 (EXPLORATORIO). Sin lenguaje causal.\n",
         "## 1. Resumen",
         f"- **E9-R1, E9-R2, E9-A1 y E9-A2: {'NO ESTIMABLES' if not estimable else 'estimables'} por choques efectivos.** Con la exposición del padrón de 2003 (residentes por nacionalidad, aproximación a la exposición por compradores) y los "
         f"{len(origenes_riesgo)} orígenes con serie de riesgo ({', '.join(origenes_riesgo)}), 1/HHI = {principal['inv_hhi']:.2f} sin pesos y "
         f"{filas[('origenes_con_serie_de_riesgo', 'pesos de población 2003')]['inv_hhi']:.2f} con pesos de población, por debajo del umbral de 10 de la adenda (1.3 y 1.13). Si los 28 países individuales del padrón tuvieran serie de riesgo, "
         f"1/HHI sería {filas[('todos_los_paises_del_padron_(informacion)', 'sin pesos')]['inv_hhi']:.2f}: el límite son las series de riesgo de los países latinoamericanos, africanos y asiáticos, que no están en el repositorio.",
         "- **E9-X1 y E9-X2: NO ESTIMABLES por datos.**", "- No se estima ningún coeficiente. B5: E9-R2 (la estimación propia) no tiene respaldo; E9 no aporta magnitud propia (entra solo la literatura). Doble cómputo E3/E9: sin instrumento de E9 no hay correlación que publicar (adenda 1.10).\n",
         "## 2. Diseño que se habría estimado", "- Original: Badarinza y Ramadorai (2018; Londres 1995-2013; +1,62 pp de precio en barrios de más cuota del país en riesgo, transitorio), Sá (2016; +2 % de precio por +1 pp de cuota de compras de no residentes, IV), "
         "Cvijanović y Spaenjers (2021; París, efecto pequeño y no significativo), Álvarez, Blanco y García-Posada (2020; MCO transversal, no significativo).",
         "- Traslado: 39 provincias de entrenamiento, exposición s_pc = residentes de la nacionalidad c entre la población de 2003 (padrón provincial), riesgo en origen = caída del PIB en el quintil superior de la historia del país (a 4 trimestres); "
         "R2 instrumenta la cuota de no residentes (MIVAU) con el índice de R1. Signo esperado fijado en la adenda: positivo.\n",
         "## 3. Recuento de choques efectivos\n", "| conjunto de orígenes | pesos | nº de orígenes | 1/HHI |\n|---|---|---|---|"]
    for k, v in filas.items():
        L.append(f"| {k[0]} | {k[1]} | {v['n_origenes']} | {v['inv_hhi']:.2f} |")
    L.append("\nPesos de los orígenes con serie de riesgo (sin pesos): " + ", ".join(f"{c} {p:.1%}" for c, p in principal["pesos"].items()) + ".")
    L.append(f"\nPor origen × trimestre (76 trimestres de riesgo) el recuento sería {ninfo['inv_hhi_origen_trimestre_si_fueran_independientes']:.0f} solo si los choques de un origen fueran independientes entre trimestres; no lo son (el PIB y el empleo en origen son persistentes), "
             "de modo que la regla de la adenda cuenta orígenes («unos 10 a 15 orígenes»).\n")
    L.append("## 4. Tabla de especificaciones\n")
    L.append("| id | descripción | tope de la tabla consolidada | estado | motivo |\n|---|---|---|---|---|")
    for r in filas_t:
        L.append(f"| {r['id']} | {r['descripcion']} | {r['tope_tabla']} | {r['estado']} | {r['motivo']} |")
    L.append(f"\nQué datos las harían estimables: {DATOS}.\n")
    L.append("## 5. Limitaciones\n- La exposición es por residentes, no por compradores (aproximación declarada en el plan).\n- Los países no europeos (Ecuador, Colombia, Marruecos, China, etc.) no tienen serie de riesgo en el repositorio.\n"
             "- Las cuatro provincias selladas de más cuota de no residentes (Baleares, Las Palmas, Santa Cruz de Tenerife y Murcia) no entran; quedan Alicante, Málaga y Girona.\n- I8 (réplica ciega) y la ronda del abogado del diablo (B6) están pendientes.\n")
    (SALIDA / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("informe escrito", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
