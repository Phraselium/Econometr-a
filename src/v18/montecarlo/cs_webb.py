"""V18 · Monte Carlo de Callaway-Sant'Anna con wild cluster bootstrap de Webb (plan de replicación 1.13; E2-A1, E6-R1, E8).

Uso: python3 src/v18/montecarlo/cs_webb.py [--R 2000] [--jobs 4]
Estimador: src/v18/herramientas/did.py (CallawaySantAnna). Proceso generador: src/v18/montecarlo/_dgp_did.py.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # BLAS de un hilo: antes de importar numpy
    os.environ.setdefault(_v, "1")

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v18.montecarlo import _comun as C  # noqa: E402
from src.v18.montecarlo import _did_driver as DD  # noqa: E402
from src.v18.montecarlo import _dgp_did as D  # noqa: E402
from src.v18.montecarlo import _informe as I  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
HERR = "cs_webb"
K1 = 27
B = 999

DGP = D.__doc__ + """
Estimador: Callaway-Sant'Anna con nunca tratadas y periodo base g − 1; agregado «simple» (peso por tamaño de cohorte sobre las celdas t >= g). Verdad: el mismo agregado de los efectos verdaderos.
Inferencia (principal): wild cluster bootstrap-t de Webb (6 puntos, B = 999) con el NULO IMPUESTO sobre el agregado y EE de agrupación recalculado en cada réplica bootstrap (WCR-t); cluster = nivel del
tratamiento (municipio en los diseños municipales; CCAA en itp_8ccaa), como pide B2. Variantes: cluster = comarca (diseños municipales) y bootstrap sin nulo impuesto (diagnóstico de V16).
Diagnóstico (no decide el veredicto): el diseño de 8 CCAA con 4 y 5 CCAA de control y 3 y 2 tratadas. Medidas: tamaño = rechazo de θ = 0 con τ = 0; cobertura = 1 − rechazo de θ = verdad (inversión del contraste) con τ = 0,05 y bajo el nulo; potencia = rechazo de θ = 0 con τ = 0,05 (log).
"""

V16 = """
V16 (cs_webb, NO APTO): tamaño 0,0655 y cobertura 0,9015 en la variante principal (41 provincias x 30 trimestres, cohortes de 1 provincia y 11 tratadas) y tamaño 0,3145 y cobertura 0,6905 en la variante
de multiplicador sobre la función de influencia SIN nulo impuesto. Causa de la variante «a»: con cohortes de una sola provincia la función de influencia centrada por cohorte es cero para la tratada, de modo
que el EE no incluía la variabilidad de las tratadas. Causa de la principal: la dependencia espacial y los factores comunes con cargas heterogéneas (los clusters provinciales no son independientes) y el
estadístico bootstrap estudentizado con el EE de la influencia no recalculado. Aquí: nulo impuesto sobre el agregado (sin imponer igualdad entre celdas), EE recalculado en cada réplica bootstrap, cobertura
por inversión del mismo contraste, y diseños con la estructura de V18 (unidad = municipio, 50-150 tratados, 100-300 controles, y el caso de 8 clusters de E8, donde se espera que falle por tener solo 2 clusters de control).
"""


def main(R: int = 2000, jobs: int = 4, escenarios: list[str] | None = None, salida: Path | None = None):
    t0 = time.time()
    esc = escenarios or (D.ESCENARIOS + D.DIAGNOSTICO)
    tabla = DD.correr("cs", K1, esc, R, B, jobs, comarca_en=tuple(e for e in esc if e in ("cat_trim_M", "cat_trim_S", "cat_trim_L", "cat_anual", "zt2024_2cohortes")),
                      sin_nulo_en=("cat_trim_M", "pocos_tratados", "itp_8ccaa"))
    veredicto, cond, por = DD.dictamen(tabla)
    res = C.resultado_base(HERR, "¿Es válida la inferencia de Callaway-Sant'Anna con wild cluster bootstrap de Webb en los diseños escalonados de V18?",
                           "simulados (sin datos reales ni muestra sellada)", f"50-150 tratados y 100-300 controles (T = 8, 13, 17); 36 provincias en 8 CCAA (T = 24); R = {R}",
                           "Callaway-Sant'Anna (nunca tratadas, ATT simple) + wild cluster bootstrap-t de Webb con nulo impuesto (B = 999)")
    sel = tabla[tabla.variante == DD.principal(tabla)]
    p = (sel[sel.escenario == "cat_trim_M"] if (sel.escenario == "cat_trim_M").any() else sel).iloc[0]
    res["estimacion"] = {"tamano_cat_trim_M": float(p.tamano_5pct), "cobertura_nulo": float(p.cobertura_nulo), "cobertura_alt": float(p.cobertura_alt), "potencia": float(p.potencia),
                         "sesgo": float(p.sesgo), "rmse": float(p.rmse)}
    res["diagnosticos"] = {"veredicto": veredicto, "condicion_en_que_falla": cond, "variante_principal": DD.principal(tabla), "por_escenario": por, "R": R, "B": B,
                           "segundos": round(time.time() - t0, 1)}
    informe = I.construir("Callaway-Sant'Anna con wild cluster bootstrap de Webb", DGP, tabla, veredicto, cond,
                          ["Principal: cluster = nivel del tratamiento. Las variantes (comarca, sin nulo impuesto) y las filas «(diagnóstico)» no deciden el veredicto.",
                           "B = 999 en el Monte Carlo (el plan fija 9.999 para el análisis real: el tamaño del p-valor bootstrap con 999 es el mismo salvo el error de discretización de 0,001).",
                           "Diagnóstico puntual (R = 800, fuera de la tabla): una sola cohorte, 3 CCAA tratadas (15 provincias) y 2 de control (10), mismo proceso generador. Callaway-Sant'Anna y Sun-Abraham dan estimaciones y EE de agrupación idénticos (diferencia 1e-15), el EE medio es 0,016 frente a una desviación típica real de 0,033 (el t normal rechaza el 40,6 %), y el bootstrap de Webb con nulo impuesto rechaza el 0,5 % con la construcción de CS y el 7,9 % con la de SA: con 5 clusters el tamaño depende de cómo se construyan los residuos del bootstrap, no solo del estimador. La forma cerrada de CS está verificada contra un remuestreo ingenuo (tests/v18/test_herramientas_did_bootstrap_ingenuo.py). Con 8 clusters no hay veredicto fiable en ninguna de las dos: SA da 0,0685 con 2 CCAA de control pero 0,0805 y 0,0920 con 4 y 5; CS da 0,178, 0,015 y 0,0005."], V16,
                          ["escenario", "variante", "R", "n_tratadas", "n_controles", "clusters", "tamano_5pct", "cobertura_nulo", "cobertura_alt", "potencia", "veredicto", "banda_112"])
    C.escribir(HERR, res, tabla, informe, salida)
    return tabla


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=2000)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    print(main(a.R, a.jobs).to_string())
