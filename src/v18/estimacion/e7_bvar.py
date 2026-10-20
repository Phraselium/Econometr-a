"""V18 · fase 4 · E7-R3 (réplica de San Juan, 2023) y E7-A1 (ampliación a 2026T2): BVAR recursivo con prior de Minnesota.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md 1.7, R3 y A1; adenda R-27, 1.7, 1.12 y Anexo A).
Determinista (SEED = 20261010), sin red. Los datos pasan por src/v18/sellado.filtrar (f_datos.py). Nunca data/sealed ni evaluate_*.

Antes de estimar se ejecutó el Monte Carlo de la cobertura de las bandas (src/v18/montecarlo/bvar.py, output/v18/montecarlo/bvar/): con el veredicto
NO APTO la estimación se publica solo como informativa (encargo y plan, sección 1.13). Tope ASOCIACIÓN (identificación recursiva, sin variación externa);
fuera de la familia de Holm (adenda 1.7). Las bandas son de credibilidad al 68 % y al 90 % (San Juan, 2023): no hay p-valor.

Uso: python3 src/v18/estimacion/e7_bvar.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e7_bvar_lib as B  # noqa: E402
import f_conjunto as F  # noqa: E402
import f_datos as D  # noqa: E402
import f_nucleo as N  # noqa: E402

RAIZ = N.RAIZ
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
OUT = RAIZ / "output" / "v18" / "estimacion" / "e7_bvar"
MC = RAIZ / "output" / "v18" / "montecarlo" / "bvar" / "resultado.json"
ROTULO = F.ROTULO
NOMBRES = ["compraventas", "precio", "visados", "PIB", "IPC", "euríbor", "crédito (flujo)"]
J_SHOCK = 5
VARS = {1: "precio", 0: "compraventas", 2: "visados"}
GAMMA = np.array([1, 1, 1, 1, 0.8, 0.8, 1.0])
UNIDAD = np.array([100.0, 100.0, 100.0, 100.0, 1.0, 1.0, 100.0])
PRIORS = {"principal": dict(lam=0.2, mu=0.5), "laxa": dict(lam=0.5, mu=0.0)}
P_LAGS = 2
H_MAX = 12
OMIT_1013 = ("2010Q1", "2013Q4")
REF = {"precio": -2.0, "compraventas": -3.0, "visados": -11.0}      # San Juan (2023): mediana a 8 trimestres por +100 pb del tipo hipotecario
FUENTES = ["base:compraventas (INE ETDP) hasta 2026T2", "base:p_tasado nominal (MIVAU) hasta 2026T2", "base:visados (Fomento) hasta 2026T2: faltan 2016T2 y 2017T2",
           "base:pib_vol_idx hasta 2026T2", "base:inflacion_ipc_yoy hasta 2026T2", "base:euribor_1y hasta 2026T2", "base:credito_nuevo (flujo, no saldo) hasta 2026T2"]
FILAS: list[dict] = []
HECHOS: list[dict] = []
REG: Registry | None = None
NOTA_ASOC = "Identificación recursiva sin variación externa: asociación condicionada al orden de las variables."


def num(x, d=3):
    return F.num(x, d)


def veredicto_mc() -> tuple[str, str]:
    j = json.loads(MC.read_text(encoding="utf-8"))["diagnosticos"]
    return j["veredicto"], j.get("condicion_en_que_falla", "")


def datos() -> pd.DataFrame:
    """Siete variables trimestrales 2008T1-2026T2 (compraventas desde 2007T1; visados observados desde 2008T1: las interpoladas de 2007 solo irían a robustez)."""
    s = lambda v: D.trim_idx(D.base(v, "nacional", "T"))      # noqa: E731
    X = pd.DataFrame({"cv": 100 * np.log(s("compraventas")), "p": 100 * np.log(s("p_tasado")), "vis": 100 * np.log(s("visados")), "pib": 100 * np.log(s("pib_vol_idx")),
                      "ipc": s("inflacion_ipc_yoy"), "eur": s("euribor_1y"), "cred": 100 * np.log(s("credito_nuevo"))})
    return X.reindex(pd.period_range("2008Q1", "2026Q2", freq="Q"))


def ajustar_spec(X: pd.DataFrame, ini: str, fin: str, prior: dict, omit=None, orden: list[int] | None = None, D_: int = 10000, seed: int = SEED, h_max: int = H_MAX) -> dict:
    sub = X.loc[ini:fin]
    cols = list(range(X.shape[1])) if orden is None else orden
    Y = sub.to_numpy()[:, cols]
    gam, uni = GAMMA[cols], UNIDAD[cols]
    trim = sub.index.quarter.to_numpy()
    om = None
    if omit is not None:
        om = np.asarray((sub.index >= pd.Period(omit[0], "Q")) & (sub.index <= pd.Period(omit[1], "Q")))
    post = B.ajustar(Y, trim, P_LAGS, prior["lam"], prior["mu"], gam, omitir=om, unidad=uni)
    rng = np.random.default_rng(seed)
    Bd, Sg = B.sacar(post, D_, rng)
    j = cols.index(J_SHOCK)
    R = B.irf(Bd, Sg, Y.shape[1], P_LAGS, h_max, j)
    raiz = B.raiz_maxima(Bd, Y.shape[1], P_LAGS)
    bmed = Bd.mean(0)[None]
    return {"R": R, "raiz": raiz, "post": post, "cols": cols, "muestra": f"{sub.index[0]}-{sub.index[-1]}", "T": len(sub), "filas": post["filas"],
            "raiz_media_posterior": float(B.raiz_maxima(bmed, Y.shape[1], P_LAGS)[0])}


def resumen(R: np.ndarray, cols: list[int], variable: int, h: int) -> dict:
    j = cols.index(variable)
    x = R[:, h, j]
    q = np.percentile(x, [5, 16, 50, 84, 95])
    return {"mediana": float(q[2]), "lo68": float(q[1]), "hi68": float(q[3]), "lo90": float(q[0]), "hi90": float(q[4]), "p_negativa": float(np.mean(x < 0))}


def etiqueta_i6(valor: float, ref: float) -> str:
    razon = valor / ref
    return (f"{'coherente' if 1 / 3 <= razon <= 3 else 'no coherente'} con San Juan (2023) ({ref:+.0f} % por +100 pb del tipo hipotecario), razón {razon:.2f}; "
            "unidad distinta: aquí +100 pb en el euríbor a 1 año en el impacto (el tipo hipotecario no está en el VAR) y flujo de crédito en lugar del saldo")


def hecho(id_, indicador, valor, lo, hi, unidad, periodo, nota):
    HECHOS.append({"id": id_, "indicador": indicador, "valor": num(valor), "min": num(lo), "max": num(hi), "unidad": unidad, "periodo": periodo, "cobertura": "nacional",
                   "fuentes": FUENTES, "capa": "C4", "clasificacion_v18": "ASOCIACIÓN", "nota": f"{nota} [{ROTULO}]"})


def spec(X, id_, estado, desc, ini, fin, prior_nombre, apto: str, omit=None, repite="no", D_=10000) -> dict:
    pr = PRIORS[prior_nombre]
    REG.log("E7B-prereg", id_, f"BVAR({P_LAGS}) Minnesota λ={pr['lam']} μ={pr['mu']}; orden {','.join(NOMBRES)}; choque euríbor +100 pb; omit={omit}", ini, fin, 0, np.nan, np.nan, np.nan,
            notas=f"{estado}; repite_visto={repite}; Monte Carlo de las bandas (previo): {apto}; tope ASOCIACIÓN; fuera de Holm")
    e = ajustar_spec(X, ini, fin, pr, omit, D_=D_)
    r = {k: {h: resumen(e["R"], e["cols"], j, h) for h in (4, 8, 12)} for j, k in VARS.items()}
    REG.log("E7B", id_, f"BVAR({P_LAGS}) h=8 precio", ini, fin, e["filas"], np.nan, np.nan, np.nan, coef_interes=r[VARS[1]][8]["mediana"], p_interes=np.nan,
            notas=f"banda 68 % [{r['precio'][8]['lo68']:.2f}; {r['precio'][8]['hi68']:.2f}]; MC: {apto}")
    e.update({"id": id_, "estado": estado, "desc": desc, "prior": prior_nombre, "resp": r, "repite": repite, "omit": omit})
    return e


def publicar(e: dict, apto: str, informativa: bool) -> None:
    id_ = e["id"]
    for j, nombre in VARS.items():
        k = nombre
        r8 = e["resp"][k][8]
        sufijo = "" if j == 1 else ("-cv" if j == 0 else "-vis")
        unidad = "% de " + {"precio": "el precio nominal (valor tasado)", "compraventas": "las compraventas", "visados": "los visados de obra nueva"}[k] + " por +100 pb del euríbor a 1 año en el impacto (BVAR recursivo; respuesta en nivel a 8 trimestres)"
        nota = (f"{e['desc']}. BVAR({P_LAGS}) de 7 variables, prior de Minnesota ({e['prior']}), muestra {e['muestra']} ({e['filas']} filas de regresión), identificación recursiva en el orden de San Juan (2023) "
                f"con el euríbor sexto; respuesta de {k} a 8 trimestres: mediana {r8['mediana']:.2f}, banda al 68 % [{r8['lo68']:.2f}; {r8['hi68']:.2f}], al 90 % [{r8['lo90']:.2f}; {r8['hi90']:.2f}]; "
                f"probabilidad posterior de respuesta negativa {r8['p_negativa']:.2f}. Monte Carlo de las bandas: {apto}"
                f"{': estimación solo informativa' if informativa else ''}. I6 (etiqueta, no decide): {etiqueta_i6(r8['mediana'], REF[k])}. {NOTA_ASOC} "
                f"Crédito: flujo (base:credito_nuevo), no el saldo de préstamos de vivienda de San Juan (R-27); IPC en lugar de IPCA; visados con huecos en 2016T2 y 2017T2 (filas omitidas).")
        hecho(f"V18-{id_}{sufijo}", f"Respuesta de {k} a 8 trimestres de un aumento de 100 pb del euríbor, BVAR recursivo ({id_})", r8["mediana"], r8["lo68"], r8["hi68"], unidad, e["muestra"], nota)
        FILAS.append({"id": id_ + sufijo, "familia": "E7", "estado": e["estado"], "repite_visto": e["repite"], "muestra": e["muestra"], "N": e["filas"], "variable": k, "h": 8,
                      "mediana": num(r8["mediana"]), "lo68": num(r8["lo68"]), "hi68": num(r8["hi68"]), "lo90": num(r8["lo90"]), "hi90": num(r8["hi90"]),
                      "p_respuesta_negativa": num(r8["p_negativa"], 2), "referencia_san_juan": REF[k], "prior": e["prior"], "mc_bandas": apto, "solo_informativa": informativa,
                      "clasificacion_v18": "ASOCIACIÓN", "nota": nota})


def diagnosticos(X: pd.DataFrame, e_r3: dict, e_a1: dict, D_: int) -> dict:
    """B4, series temporales: raíces unitarias, estabilidad del VAR y sensibilidad a la identificación (orden alternativo y omisión de una variable), con bandas."""
    out = {"series_adf_kpss": {c: F.adf_kpss(X[c].dropna()) for c in X.columns},
           "estabilidad": {"R3_raiz_maxima_media_posterior": num(e_r3["raiz_media_posterior"]), "R3_proporcion_extracciones_explosivas": num(float(np.mean(e_r3["raiz"] >= 1.0))),
                           "A1_raiz_maxima_media_posterior": num(e_a1["raiz_media_posterior"]), "A1_proporcion_extracciones_explosivas": num(float(np.mean(e_a1["raiz"] >= 1.0)))}}
    sens = {}
    for nombre, orden in {"euribor_primero": [5, 0, 1, 2, 3, 4, 6], "sin_credito": [0, 1, 2, 3, 4, 5], "precio_primero": [1, 0, 2, 3, 4, 5, 6]}.items():
        REG.log("E7B-diag", f"E7-R3-diag-{nombre}", f"BVAR({P_LAGS}) orden {orden}", "2008Q1", "2022Q4", 0, np.nan, np.nan, np.nan, notas="diagnóstico de sensibilidad a la identificación; no cuenta en el multiverso")
        e = ajustar_spec(X, "2008Q1", "2022Q4", PRIORS["principal"], orden=orden, D_=D_)
        sens[nombre] = {k: {kk: num(vv) for kk, vv in resumen(e["R"], e["cols"], j, 8).items()} for j, k in VARS.items()}
    out["sensibilidad_orden_R3_h8"] = sens
    return out


def informe(res: dict, t: pd.DataFrame, apto: str, cond: str, informativa: bool, salida: Path) -> None:
    L_ = [f"# E7-R3 y E7-A1 · BVAR recursivo (réplica de San Juan, 2023 y ampliación a 2026T2)\n\n*{ROTULO}.*\n"]
    L_.append("## Lectura\n")
    L_.append(f"- **Validación previa de la herramienta.** Monte Carlo de la cobertura de las bandas del BVAR (output/v18/montecarlo/bvar): **{apto}**."
              + (f" Condición en que falla: {cond[:600]}…" if cond else "") + (" Por eso la estimación se publica **solo como informativa**: las bandas no deben leerse como intervalos con cobertura conocida.\n" if informativa else "\n"))
    r3, a1 = res["e_r3"], res["e_a1"]
    for e in (r3, a1):
        r = e["resp"]
        L_.append(f"- **{e['id']}** ({e['muestra']}, {e['filas']} filas): a 8 trimestres de +100 pb en el euríbor, precio {r['precio'][8]['mediana']:.2f} % (68 % [{r['precio'][8]['lo68']:.2f}; {r['precio'][8]['hi68']:.2f}], "
                  f"90 % [{r['precio'][8]['lo90']:.2f}; {r['precio'][8]['hi90']:.2f}]), compraventas {r['compraventas'][8]['mediana']:.2f} % (68 % [{r['compraventas'][8]['lo68']:.2f}; {r['compraventas'][8]['hi68']:.2f}]), "
                  f"visados {r['visados'][8]['mediana']:.2f} % (68 % [{r['visados'][8]['lo68']:.2f}; {r['visados'][8]['hi68']:.2f}]). Referencia de San Juan: −2 %, −3 % y −11 % (intervalos al 68 %).")
    L_.append("\n- **Clase: ASOCIACIÓN** (tope fijado en el plan: identificación recursiva sin variación externa; fuera de la familia de Holm). Es una réplica de un resultado del Banco de España, y se dice. "
              "No hay p-valor: las bandas son de credibilidad.\n")
    L_.append("## Diferencias con el original (desviaciones: docs/v18/desviaciones_e4_e7b_e10_e12.md)\n")
    L_.append("- Muestra: 2008T1-2022T4 en lugar de 2004-2022 (compraventas desde 2007T1 y visados observados desde 2008T1; las interpoladas solo entran en robustez). R3-v2: 2008T1-2019T4.\n"
              "- Crédito: flujo (base:credito_nuevo), no el saldo (R-27). IPC, no IPCA. Visados: faltan 2016T2 y 2017T2 y se omiten las filas afectadas.\n"
              "- Choque: innovación recursiva del euríbor a 1 año normalizada a +100 pb en su impacto; San Juan escala un choque al tipo hipotecario: la unidad no es idéntica y I6 es solo una etiqueta.\n"
              "- BVAR(2) con prior de Minnesota (λ = 0,2, suma de coeficientes con peso 0,5; variante laxa λ = 0,5) y tres ficticias estacionales: San Juan no declara el prior ni el orden de rezagos.\n")
    L_.append("## Tabla de especificaciones (h = 8)\n")
    L_.append(F.md_tabla(t, ["id", "estado", "muestra", "N", "variable", "mediana", "lo68", "hi68", "lo90", "hi90", "p_respuesta_negativa", "prior", "solo_informativa", "clasificacion_v18"]))
    L_.append("\n## Diagnósticos del pre-registro\n")
    L_.append("```json\n" + json.dumps(res["diag"], ensure_ascii=False, indent=1, default=str) + "\n```\n")
    L_.append("## Respuesta del precio (E7-R3, % por +100 pb del euríbor; mediana y bandas)\n")
    L_.append(F.md_tabla(res["irf_r3"], ["h", "mediana", "lo68", "hi68", "lo90", "hi90"]))
    (salida / "informe.md").write_text("\n".join(L_), encoding="utf-8")


def irf_tabla(e: dict, variable: int) -> pd.DataFrame:
    return pd.DataFrame([{"h": h, **{k: num(v) for k, v in resumen(e["R"], e["cols"], variable, h).items()}} for h in range(H_MAX + 1)])


def main(rapido: bool = False, salida: Path | None = None) -> dict:
    global REG
    out = salida or OUT
    out.mkdir(parents=True, exist_ok=True)
    FILAS.clear()
    HECHOS.clear()
    REG = Registry(out / "registro.csv")
    D_ = 500 if rapido else 10000
    apto, cond = veredicto_mc()
    informativa = apto == "NO APTO"
    X = datos()
    e_r3 = spec(X, "E7-R3", "principal", "BVAR recursivo 2008T1-2022T4 (réplica de San Juan; prior principal)", "2008Q1", "2022Q4", "principal", apto, D_=D_)
    e_v1 = spec(X, "E7-R3-v1", "variante", "E7-R3 con prior más laxa (λ = 0,5, sin suma de coeficientes)", "2008Q1", "2022Q4", "laxa", apto, D_=D_)
    e_v2 = spec(X, "E7-R3-v2", "variante", "E7-R3 con muestra 2008T1-2019T4 (el plan decía 2004-2019)", "2008Q1", "2019Q4", "principal", apto, D_=D_)
    e_a1 = spec(X, "E7-A1", "principal", "BVAR recursivo ampliado a 2026T2 (prior principal)", "2008Q1", "2026Q2", "principal", apto, D_=D_)
    e_a1v = spec(X, "E7-A1-v1", "variante", "E7-A1 sin las filas de 2010T1-2013T4", "2008Q1", "2026Q2", "principal", apto, omit=OMIT_1013, D_=D_)
    for e in (e_r3, e_v1, e_v2, e_a1, e_a1v):
        publicar(e, apto, informativa)
    diag = diagnosticos(X, e_r3, e_a1, D_)
    # I5 (informativo, no clasifica): proporción de variantes con el mismo signo de la mediana del precio a 8 trimestres
    s0 = np.sign(e_r3["resp"]["precio"][8]["mediana"])
    diag["I5_mismo_signo_precio_h8"] = {"R3": {k: bool(np.sign(e["resp"]["precio"][8]["mediana"]) == s0) for k, e in (("v1", e_v1), ("v2", e_v2))},
                                        "A1": bool(np.sign(e_a1v["resp"]["precio"][8]["mediana"]) == np.sign(e_a1["resp"]["precio"][8]["mediana"]))}
    diag["mc_bandas"] = {"veredicto": apto, "condicion": cond, "ruta": "output/v18/montecarlo/bvar/informe.md"}
    diag["gate_MDE_1.3"] = ("No aplica de forma frecuentista: un BVAR con prior informativa no tiene un MDE por contraste. Se publican las bandas al 68 % y al 90 % y su anchura; la especificación no entra en la familia de Holm "
                            "(tope ASOCIACIÓN) ni en B5. Declarado en docs/v18/desviaciones_e4_e7b_e10_e12.md.")
    diag["datos"] = {"filas_R3": e_r3["filas"], "filas_A1": e_a1["filas"], "visados_ausentes": ["2016T2", "2017T2"], "credito": "flujo (credito_nuevo), no saldo"}
    t = pd.DataFrame(FILAS)
    t.to_csv(out / "tabla.csv", index=False)
    (out / "hechos.json").write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1), encoding="utf-8")
    irf3, irfa = irf_tabla(e_r3, 1), irf_tabla(e_a1, 1)
    irf3.to_csv(out / "irf_R3_precio.csv", index=False)
    irfa.to_csv(out / "irf_A1_precio.csv", index=False)
    estim = {r.id: {"mediana_h8": r.mediana, "banda68": [r.lo68, r.hi68], "banda90": [r.lo90, r.hi90], "variable": r.variable, "clasificacion_v18": r.clasificacion_v18} for r in t.itertuples()}
    resultado = {
        "rama": "v18/estimacion/e7_bvar",
        "pregunta": "¿Qué respuesta del precio, las compraventas y los visados a 8 trimestres de un aumento de 100 pb del euríbor da un BVAR recursivo de siete variables (réplica de San Juan, 2023) y cambia al ampliarlo a 2026T2? "
                    "Asociación condicionada al orden de las variables, sin identificación externa (E7-R3 y E7-A1 del plan de replicación V18)",
        "capa": "C4",
        "datos": "base (hechos.parquet) vía src/v18/sellado.filtrar, series nacionales trimestrales 2008T1-2026T2: compraventas, valor tasado nominal, visados, PIB, IPC, euríbor a 1 año y flujo de crédito nuevo",
        "N": {"R3_filas": e_r3["filas"], "A1_filas": e_a1["filas"], "T_R3": e_r3["T"], "T_A1": e_a1["T"]},
        "metodo": f"BVAR({P_LAGS}) con prior de Minnesota en observaciones ficticias (normal-Wishart inversa), tres ficticias estacionales, identificación recursiva en el orden de San Juan, "
                  f"{D_} extracciones del posterior, bandas por percentiles 16-84 y 5-95; Monte Carlo previo de la cobertura de las bandas (R = 2.000): {apto}",
        "estimacion": estim,
        "ic95": None,
        "p_ajustado": {"metodo": "no aplica: bandas de credibilidad al 68 % y al 90 %; fuera de la familia de Holm (adenda 1.7)", "valores": None},
        "nivel_evidencia": "EXPLORATORIO",
        "clasificacion_v18": "ASOCIACIÓN",
        "clasificacion_v18_por_especificacion": {r.id: r.clasificacion_v18 for r in t.itertuples()},
        "solo_informativa": informativa,
        "diagnosticos": {**diag, "irf_R3_precio": irf3.to_dict("records"), "irf_A1_precio": irfa.to_dict("records")},
        "fuera_muestra": None,
        "notas": [ROTULO, "Clase provisional hasta I8 (réplica ciega, B6); el tope es ASOCIACIÓN en cualquier caso.",
                  "fuera_muestra: no aplica a una réplica de un BVAR de identificación recursiva; la predicción frente a AR(4) y ECM v1 se hace en F1.",
                  "Referencia única: San Juan (2023), −2 % en el precio, −3 % en compraventas y −11 % en visados a 8 trimestres por +100 pb del tipo hipotecario (intervalos al 68 %; ficha VERIFICADA); la unidad no es idéntica (euríbor, crédito en flujo).",
                  "Desviaciones y motivos: docs/v18/desviaciones_e4_e7b_e10_e12.md. Monte Carlo: output/v18/montecarlo/bvar/."],
    }
    (out / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    informe({"e_r3": e_r3, "e_a1": e_a1, "diag": diag, "irf_r3": irf3}, t, apto, cond, informativa, out)
    REG.flush()
    return resultado


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    r = main(a.rapido, Path(a.salida) if a.salida else None)
    print(f"e7_bvar: {len(FILAS)} filas, {len(HECHOS)} cifras; MC: {r['diagnosticos']['mc_bandas']['veredicto']}")
