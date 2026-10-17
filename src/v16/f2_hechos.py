"""V16-F2.1 · Hechos C1/C2 actualizados con las fuentes nuevas (docs/v16/plan.md, fase 2, punto 1). Sin estimar efectos; sin lenguaje causal.

Orquesta: precios (f2_hechos_precios), alquiler (f2_hechos_alquiler), parque, obra/hogares, lanzamientos e internacional (f2_hechos_resto).
Tolerancias y grupos de fuentes: f2_hechos_base (TOL_PP = 3,0 p.p.; TOL_REL_RECUENTO = 15 %). SEED = 20261010 (no hay aleatoriedad).
Salidas en output/v16/f2_hechos/: hechos.json, fichas.md, informe.md, discrepancias.md, resultado.json, registro.csv, control.json y tablas CSV.
Uso: python3 src/v16/f2_hechos.py [--smoke]   (--smoke escribe en output/v16/f2_hechos/smoke/ y solo calcula precios y alquiler).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src" / "v16"))
import f2_hechos_alquiler as alq  # noqa: E402
import f2_hechos_base as base  # noqa: E402
import f2_hechos_precios as pre  # noqa: E402
import f2_hechos_resto as rest  # noqa: E402
from econ_utils import Registry  # noqa: E402

MAX_CIFRAS = 60
PENDIENTE_PUBLICA = ("Vivienda pública por habitante frente a la UE: no hay dato descargado (OCDE Affordable Housing Database, PH4.2). "
                     "Se deja la cifra pendiente en tareas del autor; no se estima ni se aproxima con otra fuente.")


def build(smoke: bool = False) -> dict:
    np.random.seed(base.SEED)
    base.HECHOS.clear()
    base.CONTROL.clear()
    base.FICHAS.clear()
    avisos: list[str] = []
    r = pre.calcular()
    avisos += pre.hechos(r)
    avisos += alq.stock_nacional()
    avisos += alq.brechas()
    if not smoke:
        rest.publica_pendiente()
        for f in (rest.parque, rest.obra_hogares, rest.lanzamientos, rest.internacional):
            avisos += f()
    if len(base.HECHOS) > MAX_CIFRAS:
        raise RuntimeError(f"{len(base.HECHOS)} cifras: el máximo es {MAX_CIFRAS}")
    ids = [h["id"] for h in base.HECHOS]
    if len(set(ids)) != len(ids):
        raise RuntimeError("ids duplicados")
    return {"hechos": list(base.HECHOS), "control": list(base.CONTROL), "fichas": dict(base.FICHAS), "avisos": avisos, "precios_ccaa": r["ccaa"]}


def _informe(res: dict) -> str:
    h = {x["id"]: x for x in res["hechos"]}
    n = {c: sum(1 for x in res["hechos"] if x["capa"] == c) for c in ("C1", "C2", "C4")}
    c1 = [x for x in res["hechos"] if x["capa"] == "C1"]
    g = lambda i: h[i]  # noqa: E731
    p19 = g("V16-HEC-PRECIO-REAL-2019-2025")
    p13 = g("V16-HEC-PRECIO-REAL-2013-2025")
    p07 = g("V16-HEC-PRECIO-REAL-2007-2025")
    filas = "\n".join(f"| {x['id']} | {x['indicador']} | {x['valor'] if x['valor'] is not None else '—'} | "
                      f"{x['min'] if x['min'] is not None else '—'} a {x['max'] if x['max'] is not None else '—'} | {x['capa']} |" for x in c1)
    return f"""# V16 · Fase 2.1 · Hechos actualizados (informe)

Generado por `python3 src/v16/f2_hechos.py`. Sin estimar efectos y sin lectura causal. Cifras en `hechos.json`; una ficha por cifra en `fichas.md`.

## 1. Resumen

- **{len(res['hechos'])} cifras:** {n['C1']} en C1, {n['C2']} en C2 y {n['C4']} en C4. No hay C2: ningún hecho de esta fase es una cota con supuestos explícitos (Manski).
- **Regla de capa.** C1 solo con al menos dos fuentes de grupos distintos (misma fuente primaria = un grupo) cuyas cifras coinciden dentro de una tolerancia fijada antes de mirar las parejas nuevas: ±{base.TOL_PP} p.p. en cambios acumulados y ±{base.TOL_REL_RECUENTO:.0%} en recuentos. Es la vara de las 11 bajadas de `docs/v15/bajadas_capa.csv`.
- **Grupos.** IPV del INE y Notariado: notarial. MIVAU valor tasado: tasación. Registradores: registral. IPC alquiler: encuesta INE. IPVA y SERPAVI: AEAT-IRPF (un grupo). Fianzas Incasòl y GVA: un grupo cada una. OCDE, Eurostat y BIS para el precio de España: derivados del IPV del INE (K6).
- **Controles con la 1.0.** El cambio 2015-2025 reproduce A23-P1 (79,9) y los extremos de A23-P2 (44,2; 47,2; 56,1); el IPVA nuevo y las fianzas 2021-2024 caen dentro de los rangos de A23-A9 y A23-A10; el aumento de hogares ECP reproduce el extremo inferior de dh_2125. Discrepancias: ver `discrepancias.md`.

## 2. Cifras C1

| id | indicador | valor | rango entre fuentes | capa |
|---|---|---|---|---|
{filas}

## 3. Lectura por tema

- **Precios de compra.** En términos reales (IPC general) 2019-2025 el cambio es {p19['min']} a {p19['max']} % según la medida ({p19['capa']}); 2013-2025, {p13['min']} a {p13['max']} % ({p13['capa']}); 2007-2025, {p07['min']} a {p07['max']} % ({p07['capa']}). Las medidas notarial (IPV), de tasación y registral difieren en la cuantía en varias ventanas: se publican todas y, si no coinciden, no se elige una. Por CCAA, `precios_ccaa.csv` (el deflactor es nacional: no hay IPC autonómico en el repositorio).
- **Alquiler.** El IPC de alquiler (stock) llega a 2025; IPVA y SERPAVI acaban en 2024, así que en 2025 no hay segunda fuente (C4). Las brechas nuevo/vigente 2021-2024 se calculan con dos estimaciones independientes (IPVA frente a fianzas menos IPC) en Cataluña y la Comunitat Valenciana; solo Cataluña supera la vara. IPVA y SERPAVI comparten fuente primaria. Inside Airbnb queda fuera (turístico).
- **Parque y vacías.** La tabla 59531 (vacías y uso esporádico por consumo eléctrico) es una tabla del propio Censo 2021 con el mismo universo de viviendas: las «vacías del Censo» y las «vacías por consumo» son la misma cifra, no dos fuentes (C4). El Catastro y el Censo difieren en {g('V16-HEC-PARQUE-CATASTRO-CENSO-2021')['valor']} % en el territorio común, pero se mantiene C4 por no estar demostrada la independencia. Nivel nacional y CCAA (`parque_ccaa.csv`); lo municipal queda para el atlas (fase 3) con el filtro de la muestra sellada v6.
- **Obra nueva frente a hogares.** Libres terminadas MIVAU 2021-2025 y hogares ECP: ampliación a 2025 con ids nuevos; no sustituye a terminadas_1924 ni a dh_2125. Las terminadas de la 1.0 incluyen protegidas en V12; aquí solo libres.
- **Vivienda pública por habitante frente a la UE.** {PENDIENTE_PUBLICA}
- **Lanzamientos (CGPJ).** Una sola fuente: C4. Serie nacional y por TSJ (`lanzamientos_ccaa.csv`); agregado propio, la serie no se redistribuye (terceros_1_0: agregados). El total nacional es el de los TSJ, no la suma de provincias, para no depender de la muestra sellada.
- **Comparación internacional.** España frente a la mediana UE y OCDE en precio real, precio/alquiler y precio/renta (OCDE) y sobrecarga (Eurostat ECV): C4, porque no hay segunda fuente independiente para España.

## 4. Límites

- Medias anuales de 4 trimestres; el último año es 2025. Los cambios 2007, 2013 y 2019 usan la misma metodología que la 1.0.
- Registradores: agregado propio de datos abiertos (ODbL); Notariado: agregado propio. No se publican las series.
- Sin pruebas de hipótesis: el control de falsos descubrimientos (Holm o BH) no se aplica; cada cifra va al Registry (`registro.csv`).
"""


def escribir(res: dict, sal: Path) -> None:
    sal.mkdir(parents=True, exist_ok=True)
    (sal / "hechos.json").write_text(json.dumps(res["hechos"], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (sal / "control.json").write_text(json.dumps({"tol_pp": base.TOL_PP, "tol_rel_recuento": base.TOL_REL_RECUENTO, "grupos": base.GRUPO,
                                                  "cifras": res["control"]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    cab = ("# V16 · Fase 2.1 · Fichas de las cifras\n\nUna ficha por cifra: definición, fuentes, por qué es o no C1, tolerancia y cálculo reproducible "
           "(`python3 src/v16/f2_hechos.py`).\n\n")
    (sal / "fichas.md").write_text(cab + "\n".join(res["fichas"][k] for k in sorted(res["fichas"])), encoding="utf-8")
    res["precios_ccaa"].to_csv(sal / "precios_ccaa.csv", index=False)
    reg = Registry(sal / "registro.csv")
    for x in res["hechos"]:
        reg.log("f2_hechos", x["id"], f"{x['indicador']} [{x['fuentes']}]", x["periodo"], x["periodo"], len(x["fuentes"].split(";")), np.nan, np.nan, np.nan,
                coef_interes=x["valor"] if x["valor"] is not None else np.nan, p_interes=np.nan, notas=f"capa {x['capa']}; sin contraste de hipótesis")
    reg.flush()
    av = res["avisos"]
    disc = ("# Discrepancias con la 1.0 (fase 2.1)\n\n" + ("Ninguna: todos los controles reproducen las cifras publicadas (precios 2015-2025, rangos de A23-A9 y A23-A10, "
            "SERPAVI de A23-A2b y el extremo inferior de dh_2125). No se ha publicado ninguna cifra V16 para un concepto y periodo ya publicados con otro valor.\n"
            if not av else "**PARADA DEL PLAN.** Se anotan y NO se publican:\n\n" + "\n".join(f"- {a}" for a in av) + "\n"))
    (sal / "discrepancias.md").write_text(disc, encoding="utf-8")
    n = {c: sum(1 for x in res["hechos"] if x["capa"] == c) for c in ("C1", "C2", "C4")}
    rj = {"rama": "f2_hechos", "pregunta": "¿Qué hechos de precios, alquiler, parque, obra, lanzamientos y comparación internacional se sostienen con dos fuentes independientes?",
          "capa": "C1/C4 (mixta; cada cifra lleva la suya)", "datos": "INE IPV, IPC alquiler, IPVA, Censo 2021; MIVAU tasado, fin de obra, SERPAVI; Registradores; Notariado; Incasòl; GVA; Catastro; CGPJ; OCDE; Eurostat",
          "N": len(res["hechos"]), "metodo": f"Cambios acumulados con media anual; coincidencia ±{base.TOL_PP} p.p. (cambios) o ±{base.TOL_REL_RECUENTO:.0%} (recuentos); grupos por fuente primaria",
          "estimacion": n, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
          "diagnosticos": {"controles_1_0": "reproducidos" if not av else av, "tolerancia_pp": base.TOL_PP, "pendiente": PENDIENTE_PUBLICA},
          "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "Hechos descriptivos, sin estimar efectos ni predecir; sin contraste de hipótesis (no aplica FDR)."}
    (sal / "resultado.json").write_text(json.dumps(rj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if "smoke" not in str(sal):
        (sal / "informe.md").write_text(_informe(res), encoding="utf-8")


def main() -> int:
    smoke = "--smoke" in sys.argv
    sal = base.SAL / "smoke" if smoke else base.SAL
    res = build(smoke)
    escribir(res, sal)
    print(f"{len(res['hechos'])} cifras; avisos: {res['avisos']}")
    return 1 if res["avisos"] else 0


if __name__ == "__main__":
    sys.exit(main())
