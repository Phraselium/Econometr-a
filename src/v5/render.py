"""Rellena las plantillas de entregables v5 (docs/v5/plantillas/*.md) con output/v5/cifras_clave.csv.

Marcadores:
- {{id}}: el valor con su unidad y, si existe, el rango [min-max];
- {{id:campo}}: un campo concreto (valor, min, max, periodo, cobertura, fuentes, capa, fecha_dato, rango);
- {{id:cita}}: «valor (periodo; fuentes; fecha; capa)».
Un marcador sin resolver es un error. Determinista y sin red.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PLANT = ROOT / "docs" / "v5" / "plantillas"
OUT = ROOT / "output" / "v5"
MARC = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([a-z_]+))?\}\}")


CONTEOS = {"instrumentos", "referencias", "afirmaciones", "distritos", "documentos", "medidas", "especificaciones",
           "series", "entidades", "clase", "declarantes", "hechos/anio", "procedimientos/anio", "lanzamientos/anio"}


def fmt_num(x: float, unidad: str = "") -> str:
    if pd.isna(x):
        return "—"
    x = float(x)
    # recuentos (instrumentos, referencias, afirmaciones...): enteros sin decimales
    if x.is_integer() and str(unidad).split(" ")[0] in CONTEOS:
        return f"{x:,.0f}".replace(",", ".")
    if unidad in ("viviendas", "hogares", "personas", "contratos", "€", "€/m²", "€/mes", "municipios", "provincias") or abs(x) >= 1000:
        s = f"{x:,.0f}".replace(",", ".")
    elif abs(x) >= 10:
        s = f"{x:.1f}".replace(".", ",")
    else:
        s = f"{x:.2f}".replace(".", ",") if abs(x) < 1 else f"{x:.1f}".replace(".", ",")
    return s


def texto(r: pd.Series, campo: str | None) -> str:
    u = r.unidad if isinstance(r.unidad, str) else ""
    sep = " " if u and u != "%" else (" " if u == "%" else "")
    if pd.isna(r.valor) and pd.notna(r["min"]) and campo in (None, "valor", "valor_rango", "cita"):
        # sin valor central: se da el rango (revisión E, B2)
        rango = f"{fmt_num(r['min'], u)}-{fmt_num(r['max'], u)}{sep}{u}".strip()
        return rango if campo != "cita" else f"{rango} ({r.periodo}; {r.fuentes}; dato de {r.fecha_dato}; {r.capa})"
    if campo in (None, "valor_rango"):
        base = f"{fmt_num(r.valor, u)}{sep}{u}".strip()
        if campo is None and pd.notna(r["min"]) and pd.notna(r["max"]):
            base += f" ({fmt_num(r['min'], u)}-{fmt_num(r['max'], u)}{sep}{u})".rstrip()
        return base
    if campo == "valor":
        return f"{fmt_num(r.valor, u)}{sep}{u}".strip()
    if campo == "num":
        return fmt_num(r.valor, u)
    if campo in ("min", "max"):
        return f"{fmt_num(r[campo], u)}{sep}{u}".strip()
    if campo == "rango":
        return f"{fmt_num(r['min'], u)}-{fmt_num(r['max'], u)}{sep}{u}".strip()
    if campo == "cita":
        return f"{texto(r, None)} ({r.periodo}; {r.fuentes}; dato de {r.fecha_dato}; {r.capa})"
    return str(r[campo])


def render(src: Path, ck: pd.DataFrame) -> tuple[str, list[str]]:
    falta: list[str] = []

    def sub(m: re.Match) -> str:
        i, campo = m.group(1), m.group(2)
        if i not in ck.index:
            falta.append(i)
            return m.group(0)
        return texto(ck.loc[i], campo)

    return MARC.sub(sub, src.read_text()), falta


def main() -> int:
    ck = pd.read_csv(OUT / "cifras_clave.csv").set_index("id")
    errores = 0
    for p in sorted(PLANT.glob("**/*.md")):
        txt, falta = render(p, ck)
        dest = OUT / p.relative_to(PLANT)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(txt)
        if falta:
            errores += len(falta)
            print(f"{p.relative_to(ROOT)}: marcadores sin cifra: {sorted(set(falta))}")
    print(f"render: {errores} marcadores sin resolver")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
