"""V16-F0.4 · docs/v16/lo_ya_visto.md: conclusiones de V5-V15 con su estimación y sus pruebas, que todo pre-registro de V16
declara. Las cifras salen de output/v5/cifras_clave.csv (nada tecleado); los hallazgos de las auditorías de V15, de sus
resultado.json. Determinista; sin red.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "docs" / "v16" / "lo_ya_visto.md"

BLOQUES = [
    ("V5-V7 · Hechos de partida (hogares, déficit, necesidad, precios y alquiler)", r"^(dh_2125|L3-DEF-2124-SINBAJAS|T3-H5b|A23-P2|A23-A2|A23-A9|A23-A10|terminadas_1924)$",
     "Hechos C1 o cotas C2 de la 1.0. V16 los actualiza con fuentes nuevas, pero no los reemplaza: un valor distinto en V16 es una cifra V16-* nueva y, si contradice uno publicado, es una parada."),
    ("V7.2 · Exuberancia (GSADF)", r"^V72-GSADF-",
     "Hay niveles explosivos, pero no exuberancia de los cocientes tras el ajuste múltiple. La pregunta Q9 de V16 repite el contraste por territorio y debe declarar estas cifras."),
    ("V6.1 (K1) · Predicción en la muestra sellada v6", r"^K1-N-",
     "Ningún modelo predice mejor que la línea base más exigente en la validación sellada v6. H5 de V15 y Q10 de V16 parten de aquí."),
    ("V8 · Por qué ha subido (factores, periodos, factor común)", r"^V8-(VOTOS-c-P5|OBS-c-P5|OBS-a-P5|QNA-pp-c-P5|M1-cuota-c-P5|H8-9-est)$",
     "Ningún factor destaca como principal. La parte no atribuida es C3s, válida solo bajo las restricciones del SVAR. El factor común domina en P5."),
    ("V9-D1 · Topes y zonas tensionadas (Incasòl)", r"^V9-D1",
     "D1a (zonas tensionadas, 2022T2-2026T1) no supera pretendencias, placebo de fecha ni Honest DiD. D1b (Ley 11/2020) supera pretendencias y placebo, pero no Honest DiD (M̄ de ruptura < 1). Todo es C4. H1 y H2 de V15 y Q1 de V16 usan otro diseño sobre una ventana ya vista: lo ya visto es informativo."),
    ("V9-D2/D3 · Vivienda turística", r"^V9-D[23]",
     "Pretendencias rechazadas en D2; D3 sin potencia y con un placebo del mismo signo. C4. H3 de V15 y Q2 de V16 cambian de datos y de diseño."),
    ("V9-D4 · Inmigración (2SLS shift-share provincial)", r"^V9-D4",
     "Instrumento débil en todas las variantes (F efectiva < 5). C4, no concluyente. H4 de V15 es municipal; Q3 de V16 separa alquiler de compra y la escala de barrio."),
    ("V9-D5 a D7 · Otros diseños", r"^V9-D[567]",
     "Ver cada fila: capa y periodo. D6 (Bono Alquiler Joven) no es estimable sin microdatos de perceptores."),
    ("V12 · Población, hogares, oferta, titularidad, condiciones y turismo (descriptivo)",
     r"^V12-(B1-2022-2024-|B2-|B3-hogares-|B4-|B5-pct_mas10|B5-pct_PJ|B6-brecha-sobrecarga_40|B7-CV-)",
     "Contabilidades y descriptivos C4. V16 los amplía (fase 2), sin lenguaje causal."),
]
AUDITORIAS = ["precios_compra", "alquiler", "oferta_parque", "demografia_hogares", "turismo", "financiacion_macro", "renta_microdatos"]


def _f(x: str) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return x or ""
    return f"{v:.4g}".replace(".", ",")


def main() -> int:
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).fillna("")
    L = ["# V16 · Lo ya visto (V5-V15)", "",
         "Generado por `python3 src/v16/f0_lo_ya_visto.py` desde output/v5/cifras_clave.csv y output/v15/auditoria/*/resultado.json. "
         "Ningún número está tecleado: cada fila lleva su id de cifras_clave.",
         "",
         "**Uso.** Todo pre-registro de V16 declara qué de esto ya se ha visto para su pregunta. Lo ya visto es informativo: una pregunta de V16 "
         "solo es confirmatoria en datos o diseños que no se hayan usado antes (docs/v16/plan.md, regla A; adenda 2 de V15). Las conclusiones "
         "publicadas en la 1.0 no se reescriben: si V16 las contradice, es una parada (sección D).", ""]
    for titulo, patron, lectura in BLOQUES:
        sub = ck[ck.id.str.match(patron)]
        L += [f"## {titulo}", "", f"**Lectura.** {lectura}", "", "| id | Indicador | Valor | Rango | Periodo | Capa |", "|---|---|---|---|---|---|"]
        for r in sub.itertuples():
            rango = f"{_f(r.min)} a {_f(r.max)}" if r.min and r.max else ""
            L.append(f"| {r.id} | {r.indicador.replace('|', '/')} | {_f(r.valor)} | {rango} | {r.periodo} | {r.capa} |")
        L.append("")
    L += ["## V15 · Auditorías de calidad de los datos (fase 1; descriptivas)", "",
          "No son cifras publicadas: son diagnósticos de los datos que V16 usa y que todo diseño debe tener en cuenta. Detalle en output/v15/auditoria/<grupo>/informe.md.", ""]
    for a in AUDITORIAS:
        f = RAIZ / "output/v15/auditoria" / a / "resultado.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        notas = d.get("notas") or d.get("pregunta") or ""
        if isinstance(notas, list):
            notas = "; ".join(map(str, notas))
        notas = re.sub(r"\s+", " ", str(notas))[:400]
        L.append(f"- **{a}** (output/v15/auditoria/{a}/): {notas}")
    L += ["", "## V15 · Pre-registro interno (sin sello de tiempo externo)", "",
          "- H1-H5 están fijados en docs/v15/preregistro_v15.md y sus adendas 1 y 2 (etiqueta prereg-v15, commit 542b4fd). V16 no los modifica.",
          "- Solo es confirmatorio lo publicado después del corte del 17-10-2026. Calendario: H1 y H2 hacia marzo de 2027; H5 hacia octubre de 2027; H4 en el último trimestre de 2027.",
          "- Potencia (output/v15/potencia/informe.md) y sellado (docs/v15/sellado_v15.json): V16 los reutiliza y no toca su muestra sellada.", ""]
    SAL.write_text("\n".join(L), encoding="utf-8")
    print(f"f0_lo_ya_visto: {sum(1 for x in L if x.startswith('| ') and not x.startswith('| id'))} filas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
