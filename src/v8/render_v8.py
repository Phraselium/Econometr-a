#!/usr/bin/env python3
"""V8-F6: rellena docs/v8/plantillas/**/*.md -> output/v8/ con output/v5/cifras_clave.csv, reutilizando src/v5/render.py (importado, no copiado).

Marcadores: {{id}}, {{id:campo}}, {{id:cita}} (ver src/v5/render.py). Un marcador sin resolver es un error (código de salida 1).
No se renderiza docs/v8/plantillas/README.md; sí se REGENERA con la lista completa de ids V8 (indicador y valor), leída de cifras_clave.csv.
Uso: python3 src/v8/render_v8.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import render as R  # noqa: E402

PLANT = RAIZ / "docs" / "v8" / "plantillas"
OUT = RAIZ / "output" / "v8"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"

# Unidades de V8 que son recuentos (enteros sin decimales) y p-valores (3 decimales): se registran en el módulo de v5 sin modificarlo en disco.
R.CONTEOS |= {"votos", "celdas", "combinaciones", "coeficientes", "efectos", "modelos", "designado"}
_fmt_v5 = R.fmt_num
_texto_v5 = R.texto


def _fmt_p(x: float, unidad: str = "") -> str:
    if pd.isna(x):
        return "—"
    return "< 0,001" if float(x) < 0.001 else f"{float(x):.3f}".replace(".", ",")


def _fmt_2(x: float, unidad: str = "") -> str:
    return "—" if pd.isna(x) else f"{float(x):.2f}".replace(".", ",")


def _fmt_cero(x: float, unidad: str = "") -> str:
    s = _fmt_v5(x, unidad)
    return "0,00" if s == "-0,00" else s   # un valor negativo minúsculo no se escribe «-0,00»


FORMATO_SIN_UNIDAD = {"p-valor": _fmt_p, "estadístico F": _fmt_2, "estadístico t": _fmt_2}   # se escriben sin la palabra de la unidad


def _texto_v8(r: pd.Series, campo: str | None) -> str:
    """P-valores y estadísticos F y t: 3 o 2 decimales y sin unidad; el resto, como en v5."""
    if r.unidad not in FORMATO_SIN_UNIDAD:
        return _texto_v5(r, campo)
    fmt = FORMATO_SIN_UNIDAD[r.unidad]
    r = r.copy()
    r["unidad"] = "proporción"   # v5 no escribe la unidad «proporción»
    R.fmt_num = fmt
    try:
        return _texto_v5(r, campo)
    finally:
        R.fmt_num = _fmt_cero


R.fmt_num = _fmt_cero
R.texto = _texto_v8

README_CAB = """# Plantillas V8

Las plantillas de este directorio (`*.md`, salvo este README) se rellenan con `python3 src/v8/render_v8.py` (o `make render_v8`) y se escriben en `output/v8/`
con la misma ruta relativa. Cada cifra sale de `output/v5/cifras_clave.csv`; ninguna se escribe a mano. Un marcador sin resolver es un error.

## Marcadores

- `{{id}}`: valor con su unidad y, si existe, el rango entre paréntesis (banda del 68 % o intervalo al 95 % según el indicador).
- `{{id:campo}}`: un campo concreto: `valor`, `num` (sin unidad), `min`, `max`, `rango`, `periodo`, `cobertura`, `fuentes`, `capa`, `fecha_dato`, `indicador`.
- `{{id:cita}}`: «valor (periodo; fuentes; fecha del dato; capa)».

## Reglas de redacción

- Capas: `C3s` (descomposición histórica del SVAR) se escribe siempre «condicionado a las restricciones de signo y de cero»; el resto es `C4` (asociación o descriptivo).
- Sin lenguaje causal fuera de C3/C3s. Atribuciones siempre con banda. Unidades: `pp` = puntos porcentuales (log×100); `%`; `proporción` (sin unidad); `p-valor`.
- Los ids con sufijo `-media` y `-mediana` comparten la misma banda del 68 % (percentiles 16-84 de la posterior).
- `V8-REGLA-*`: 1 = designado, 0 = no designado (leer el campo `indicador` para el factor evaluado y el resultado).
- Unidades de recuento (`votos`, `celdas`, `combinaciones`, `coeficientes`, `efectos`, `modelos`, `especificaciones`, `instrumentos`) se escriben sin decimales.

## Ids V8 (generado por `src/v8/render_v8.py`; {n} ids)

"""


def escribir_readme(ck: pd.DataFrame) -> int:
    v = ck[ck.index.str.startswith("V8-")]
    L = [README_CAB.format(n=len(v)), "| id | indicador | valor | capa | periodo |", "|---|---|---|---|---|"]
    for i, r in v.iterrows():
        val = R.texto(r, None).replace("|", "/")
        L.append(f"| `{i}` | {str(r.indicador).replace('|', '/')} | {val} | {r.capa} | {r.periodo} |")
    (PLANT / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(v)


def main() -> int:
    ck = pd.read_csv(CK).set_index("id")
    PLANT.mkdir(parents=True, exist_ok=True)
    n = escribir_readme(ck)
    errores = 0
    for p in sorted(PLANT.glob("**/*.md")):
        if p.name == "README.md":
            continue
        txt, falta = R.render(p, ck)
        dest = OUT / p.relative_to(PLANT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(txt, encoding="utf-8")
        if falta:
            errores += len(falta)
            print(f"{p.relative_to(RAIZ)}: marcadores sin cifra: {sorted(set(falta))}")
    print(f"render_v8: {n} ids V8 en README; {errores} marcadores sin resolver")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
