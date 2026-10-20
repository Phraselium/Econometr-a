"""V18 · fase 4 · E1 · vivienda turística: orquestación (estimabilidad → estimación → pruebas → clasificación → Holm → salidas).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (plan_replicacion.md §1.1 + adenda 1.1-1.12, anexos A-C). Orden fijado por la adenda 1.3: la estimabilidad
(mínimos de datos y MDE por Monte Carlo) se calcula y se registra ANTES de estimar ningún coeficiente; lo que no la supera queda «NO ESTIMABLE» y no se estima. Determinista
(SEED 20261010). Sin red: las fuentes `posterior_prereg` se descargaron antes con e1_adquisicion.py.

Uso: python3 src/v18/estimacion/e1_turismo.py
Salidas: output/v18/estimacion/e1/{mde.csv, registro.csv, tabla.csv, resultado.json, hechos.json, informe.md}
Lecturas de datos: solo con sellado.filtrar + holdout.excluir_sellados_v6 (e1_datos); nunca data/sealed.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _e2e8_comun as K  # noqa: E402
import e1_datos as D  # noqa: E402
import e1_diseno as G  # noqa: E402
import e1_estim as E  # noqa: E402
import e1_mde as M  # noqa: E402
import e1_nucleo as N  # noqa: E402

ALCANCE_TERRITORIAL = "lectura con sellado.filtrar y holdout.excluir_sellados_v6"
OUT = K.RAIZ / "output" / "v18" / "estimacion" / "e1"
SEMILLA = K.SEMILLA
B_PRINCIPAL = 9999
B_VAR = 1999

ANEXO_A = {
    "E1-R1": [("v1", "E", "sin tendencias por barrio"), ("v2", "E", "tendencias cuadráticas"), ("v3", "V", "sin 2020-2021"), ("v4", "M", "fianzas de Open Data BCN por barrio"),
              ("v5", "M", "HUT reconstruida por año de expediente"), ("v6", "U", "sin el 1 % superior de exposición"), ("v7", "P", "ponderada por viviendas"), ("v8", "C", "distancia al centro × año"),
              ("v9", "U", "barrio como unidad"), ("v10", "C", "ADRH en 2019-2023")],
    "E1-R2": [("v1", "M", "noches de Eurostat en lugar de Trends"), ("v2", "V", "sin 2020-2021"), ("v3", "U", "sin la Sagrada Família y el Park Güell (Casa Batlló no figura en OSM)"), ("v4", "E", "5 atractivos"),
              ("v5", "M", "endógena INE-VUT, 2022-2024"), ("v6", "C", "sin distancia × año"), ("v7", "M", "fianzas como resultado"), ("v8", "P", "ponderada")],
    "E1-R3": [("v1", "V", "base 2012"), ("v2", "E", "dosis binaria del decil superior"), ("v3", "C", "distancia × año"), ("v4", "U", "barrio como unidad"), ("v5", "U", "sin el 1 % superior")],
    "E1-R4": [("v1", "C", "resto de Barcelona como control"), ("v2", "E", "radios de 300 m y 300-800 m"), ("v3", "E", "estudio de eventos con adelantos de 2011-2012 como regresores")],
    "E1-A1": [("v1", "V", "2022-2024"), ("v2", "U", "con Barcelona"), ("v3", "M", "IPVA por distrito"), ("v4", "P", "ponderada por viviendas"), ("v5", "M", "% de plazas VUT"), ("v6", "U", "solo València"),
              ("v7", "U", "solo Sevilla"), ("v8", "U", "solo Málaga"), ("v9", "U", "solo Alicante"), ("v10", "U", "sin el 1 % superior"), ("v11", "C", "sin distancia × año")],
    "E1-A2": [("v1", "E", "Callaway, Goodman-Bacon y Sant'Anna"), ("v2", "U", "solo Málaga"), ("v3", "U", "solo Sevilla"), ("v4", "E", "Callaway-Sant'Anna con dosis binaria")],
}
FORMULAS = {
    "E1-R1": "ln SERPAVI_st = β·HUT_st + α_s + γ_t + δ_b·t + ε (HUT por 100 viviendas; 2018-2024; cluster barrio)",
    "E1-R2": "IV: ln SERPAVI_st = β·HUT_st + α_s + γ_t + dist_s×año + ε; Z = proximidad(3 atractivos) × Trends (2018-2024; cluster barrio; AR)",
    "E1-R3": "ln SERPAVI_st = Σ_k β_k·D_s·1[t=k] + α_s + γ_t (D = HUT por 100 viviendas de 2018T2; 2011-2019; base 2013; resumen media β_k de 2014-2019; cluster barrio)",
    "E1-R4": "ln SERPAVI_st = β·Tr_s·1[t ≥ 2014] + α_s + γ_t (diferencias en diferencias; Tr = < 500 m de la Sagrada Família; anillo 500-1.000 m; 2011-2019; base 2013; sin adelantos como regresores, K8 bis)",
    "E1-A1": "IV: ln SERPAVI_st = β·%VUT_st + α_s + γ_mt + dist_s×año; Z = proximidad × noches NUTS3 (València, Sevilla, Málaga, Alicante; 2021-2024; cluster distrito; AR)",
    "E1-A2": "dCDH con dosis continua (altas acumuladas del registro de Andalucía; Málaga y Sevilla; 2015-2024)",
    "E1-P-H3": "ln SERPAVI(VC)_st = β·%VUT_st/DT_intra + α_s + γ_mt + ε (V15 H3; 2021-2024; cluster municipio; muestra V18)",
}


def comprobar_sin_selladas(P: pd.DataFrame) -> None:
    """Postcondición: ninguna sección del panel pertenece a un bloque sellado (v6, V15, V16)."""
    cods = pd.Series(P.cod_seccion.astype(str).unique())
    assert not D.sellado.mascara_v15_v16(cods, "seccion").any(), "secciones de bloques de V15/V16 en el panel"
    df = pd.DataFrame({"c": cods})
    assert len(D.holdout.excluir_sellados_v6(df, "c", "seccion")) == len(df), "secciones de v6 en el panel"


def estimable(e: dict) -> tuple[bool, str]:
    if not e.get("cumple_minimo", True):
        return False, f"NO ESTIMABLE por datos: {e['minimo_datos']}"
    m = e.get("mde80", np.nan)
    if not np.isfinite(m):
        return False, f"NO ESTIMABLE por variación: el contraste no alcanza el 80 % de potencia con ningún efecto (MDE no definido; umbral {e['umbral']:.4f})"
    if m > e["umbral"]:
        return False, f"NO ESTIMABLE por variación: MDE80 {m:.4f} > umbral {e['umbral']:.4f}"
    return True, f"estimable: MDE80 {m:.4f} <= umbral {e['umbral']:.4f}"


def primera_etapa_sin_resultado(Bp: pd.DataFrame, Cp: pd.DataFrame) -> pd.DataFrame:
    """Primera etapa (F efectivo y coeficiente) de R2 y A1 y de cada variante, y de R2 por subperiodo, SIN el resultado (ln SERPAVI sustituido por 0 donde se observa): diagnóstico de
    diseño de lo que no supera la estimabilidad. Ninguna estimación del resultado."""
    cero = lambda X: X.assign(y=np.where(X.y.notna(), 0.0, np.nan))  # noqa: E731
    B0, C0 = cero(Bp), cero(Cp)
    filas = []
    for v in [None] + [x[0] for x in ANEXO_A["E1-R2"]]:
        if v in ("v7",):
            continue
        try:
            r = E.r2(B0, v)
            filas.append({"id": "E1-R2" + (f"-{v}" if v else ""), "n": r["n"], "G": r["G"], "F_efectivo": r["F"], "pi": r["pi"]})
        except Exception as e:  # noqa: BLE001
            filas.append({"id": "E1-R2" + (f"-{v}" if v else ""), "n": 0, "G": 0, "F_efectivo": np.nan, "pi": np.nan, "error": str(e)[:80]})
    r0 = E.r2(B0, None)
    r0["_x"], r0["_cluster"] = "hut", "barrio"
    sub = E.primera_etapa_subperiodos(B0, r0, lambda s: N.interaccion_anio(s.dist_c.values, s.anio.values))
    for k in ("2018-2019", "2020-2021", "2022-2024"):
        filas.append({"id": f"E1-R2 [subperiodo {k}]", "n": sub[k]["n"], "G": r0["G"], "F_efectivo": sub[k]["F"], "pi": sub[k]["pi"]})
    for v in [None] + [x[0] for x in ANEXO_A["E1-A1"]]:
        if v in ("v3",):
            continue
        try:
            Cc = pd.concat([C0, B0.assign(cod_mun="08019", barrio=B0.cod_distrito)], ignore_index=True) if v == "v2" else C0
            r = E.a1(Cc, v)
            filas.append({"id": "E1-A1" + (f"-{v}" if v else ""), "n": r["n"], "G": r["G"], "F_efectivo": r["F"], "pi": r["pi"]})
        except Exception as e:  # noqa: BLE001
            filas.append({"id": "E1-A1" + (f"-{v}" if v else ""), "n": 0, "G": 0, "F_efectivo": np.nan, "pi": np.nan, "error": str(e)[:80]})
    for nombre, col in (("hospitales", "prox_hosp"), ("universidades", "prox_univ")):          # placebos del instrumento: primera etapa con proximidad a equipamientos que no atraen turismo
        r = E.r2(B0.assign(prox3=B0[col]), None)
        filas.append({"id": f"E1-R2 [placebo {nombre}]", "n": r["n"], "G": r["G"], "F_efectivo": r["F"], "pi": r["pi"]})
        r = E.a1(C0.assign(prox3=C0[col]), None)
        filas.append({"id": f"E1-A1 [placebo {nombre}]", "n": r["n"], "G": r["G"], "F_efectivo": r["F"], "pi": r["pi"]})
    return pd.DataFrame(filas)


def main() -> int:
    t0 = time.time()
    ensayo = os.environ.get("V18_E1_ENSAYO")           # ensayo de código con resultado SINTÉTICO (ruido): escribe fuera del repositorio y no se lee
    out_dir = Path(ensayo) if ensayo else OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)
    osm, tr = D.osm(), D.trends()
    P = G.construir(osm, tr)
    B, C = P["B"], P["C"]
    if ensayo:
        for X in (B, C):
            for c in ("y", "y_vu", "y_mes"):
                m = X[c].notna()
                X.loc[m, c] = rng.normal(size=int(m.sum()))
    comprobar_sin_selladas(B)
    comprobar_sin_selladas(C)
    gsf = E.sf_geometria()
    print(f"[{time.time() - t0:5.0f}s] paneles: Barcelona {B.cod_seccion.nunique()} secciones, otras ciudades {C.cod_seccion.nunique()}", flush=True)

    # ------------------------------------------------------------------ Registry: toda especificación, antes de leer ningún coeficiente
    reg = K.Registry(out_dir / "registro.csv")
    for ident in ("E1-R1", "E1-R2", "E1-R3", "E1-R4", "E1-A1", "E1-A2", "E1-P-H3"):
        reg.log("v18-E1-prereg", ident, FORMULAS[ident], "", "", 0, np.nan, np.nan, np.nan, notas="principal o coprincipal; registrada antes de estimar (estimabilidad calculada sin coeficientes)")
        for suf, dim, desc in ANEXO_A.get(ident, []):
            reg.log("v18-E1-prereg", f"{ident}-{suf}", f"variante [{dim}] {desc}", "", "", 0, np.nan, np.nan, np.nan, notas="variante enumerada (adenda, anexo A)")
    reg.flush()

    # ------------------------------------------------------------------ estimabilidad (adenda 1.3)
    est = {"E1-R1": M.estimabilidad_r1(B), "E1-R2": M.estimabilidad_iv(B, "E1-R2"), "E1-A1": M.estimabilidad_iv(C, "E1-A1"), "E1-R3": M.estimabilidad_r3(B), "E1-R4": M.estimabilidad_r4(B, gsf)}
    est["E1-R2-v5"] = {**M.estimabilidad_iv(B, "E1-R2-v5"), "suplementaria": True}      # solo MDE de la variante con INE-VUT (2022-2024): no se estima
    print(f"[{time.time() - t0:5.0f}s] estimabilidad calculada", flush=True)
    ok = {}
    for k, e in est.items():
        ok[k], e["decision"] = estimable(e)
        reg.log("v18-E1-estimabilidad", k, FORMULAS.get(k, "variante E1-R2-v5: IV con INE-VUT como endógena, 2022-2024 (solo MDE)"), "", "", int(e.get("n_obs", 0)), np.nan, np.nan, np.nan, coef_interes=np.nan, p_interes=np.nan,
                notas=f"MDE80 {e.get('mde80')}; umbral {e['umbral']}; {e['decision']}; registrada antes de estimar")
    reg.flush()
    mde = pd.DataFrame([{k: v for k, v in e.items() if not isinstance(v, (dict, list))} | {"estimable": ok[k]} for k, e in est.items()])
    mde.to_csv(out_dir / "mde.csv", index=False)
    pe = primera_etapa_sin_resultado(B, C)
    pe.to_csv(out_dir / "primera_etapa.csv", index=False)
    print(f"[{time.time() - t0:5.0f}s] primera etapa sin resultado: F R2 {pe.F_efectivo.iloc[0]:.2f}", flush=True)

    # ------------------------------------------------------------------ estimación
    import e1_resultados as RS
    out = RS.estimar_todo(B, C, gsf, est, ok, rng, reg, pe, forzar=bool(ensayo))
    import e1_salidas as S
    S.escribir(out_dir, B, C, gsf, est, ok, pe, out, time.time() - t0, P)
    reg.flush()
    print(f"[{time.time() - t0:5.0f}s] salidas escritas en {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
