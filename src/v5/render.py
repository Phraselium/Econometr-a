"""Rellena las plantillas de entregables v5 (docs/v5/plantillas/*.md) con output/v5/cifras_clave.csv.

Marcadores:
- {{id}}: el valor con su unidad y, si existe, el rango [min-max];
- {{id:campo}}: un campo concreto (valor, min, max, periodo, cobertura, fuentes, capa, fecha_dato, rango);
- {{id:cita}}: «valor (periodo; fuentes; fecha; capa)»;
- {{id:breve}}: V13, para lectores no técnicos: el valor redondeado (3 cifras significativas; los % sin decimales desde 10) con el
  rango al lado, «998.000 hogares (982.000-1.010.000)»; {{id:rango_breve}}: solo el rango redondeado. No cambian la cifra;
- {{proyecto.<campo>}}: un campo de proyecto.json (V13: versión pública, repositorio, web, DOI; única fuente).
V14.2: si terceros_1_0 = «excluir» para una fuente, los marcadores de las cifras que usan su serie se sustituyen por la marca
«cifra no publicada en la versión 1.0» (src/v14/terceros_1_0.py). La cifra sigue en cifras_clave sin cambios.
V14.3: si el texto cita alguna cifra que usa los datos abiertos de Registradores (terceros_1_0.odbl), se añade al final el
aviso de atribución que exige la Open Database License 1.0 (4.3).
Un marcador sin resolver es un error. Determinista y sin red.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.v14 import terceros_1_0 as T10  # noqa: E402
PLANT = ROOT / "docs" / "v5" / "plantillas"
OUT = ROOT / "output" / "v5"
PROYECTO = json.loads((ROOT / "proyecto.json").read_text(encoding="utf-8"))
MARC = re.compile(r"\{\{([A-Za-z0-9_.+\-]+)(?::([a-z_]+))?\}\}")


CONTEOS = {"instrumentos", "variables", "hipótesis", "CCAA", "referencias", "afirmaciones", "distritos", "documentos", "medidas", "especificaciones",
           "series", "entidades", "tareas", "clase", "declarantes", "hechos/anio", "procedimientos/anio", "lanzamientos/anio"}


def fmt_num(x: float, unidad: str = "") -> str:
    if pd.isna(x):
        return "—"
    x = float(x)
    # recuentos (instrumentos, referencias, afirmaciones...): enteros sin decimales
    if x.is_integer() and str(unidad).split(" ")[0] in CONTEOS:
        return f"{x:,.0f}".replace(",", ".")
    if unidad in ("cociente", "estadístico t"):  # v6.1: cocientes con dos decimales (1,05 no debe leerse 1,0); v7.1: t simulados
        return f"{x:.2f}".replace(".", ",")
    if unidad in ("viviendas", "hogares", "personas", "contratos", "€", "€/m²", "€/mes", "municipios", "provincias") or abs(x) >= 1000:
        s = f"{x:,.0f}".replace(",", ".")
    elif abs(x) >= 10:
        s = f"{x:.1f}".replace(".", ",")
    else:
        s = f"{x:.2f}".replace(".", ",") if abs(x) < 1 else f"{x:.1f}".replace(".", ",")
    return s


def _guion(a) -> str:
    """Separador de rango: « a » si el mínimo es negativo (v6.2: «-4,3-1,7» se leía mal)."""
    return " a " if pd.notna(a) and float(a) < 0 else "-"


def _q(x: float, nd: int) -> str:
    from decimal import ROUND_HALF_UP, Decimal
    v = float(Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))
    return f"{v:,.{nd}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def escala(x: float) -> tuple[float, str]:
    """V13 (una página): escala de lectura según el valor central: millones, mil o ninguna."""
    a = abs(float(x)) if pd.notna(x) else 0.0
    return (1e6, "millones") if a >= 1e6 else ((1e3, "mil") if a >= 1e3 else (1.0, ""))


def redondeo(x: float, unidad: str = "", div: float = 1.0) -> str:
    """V13 (una página): cifra redondeada para lectores no técnicos. En millones, dos decimales; en miles, enteros (un decimal
    por debajo de 100 mil); sin escala, % sin decimales desde 10, un decimal desde 1 y dos por debajo. Solo presentación: el
    redondeo queda dentro de la precisión con que se escribe (tests/test_k4c_cifras.py lo comprueba contra cifras_clave)."""
    if pd.isna(x):
        return "—"
    y = float(x) / div
    if div == 1e6:
        return _q(y, 2)
    if div == 1e3:
        return _q(y, 0 if abs(y) >= 100 else 1)
    return _q(y, 0 if abs(y) >= 10 else (1 if abs(y) >= 1 else 2))


def texto(r: pd.Series, campo: str | None) -> str:
    u = r.unidad if isinstance(r.unidad, str) else ""
    if u == "proporción":   # v7.1: coberturas, correlaciones y tasas de rechazo (0-1) se escriben sin unidad
        u = ""
    sep = " " if u and u != "%" else (" " if u == "%" else "")
    if pd.isna(r.valor) and pd.notna(r["min"]) and campo in (None, "valor", "valor_rango", "cita"):
        # sin valor central: se da el rango (revisión E, B2)
        rango = f"{fmt_num(r['min'], u)}{_guion(r['min'])}{fmt_num(r['max'], u)}{sep}{u}".strip()
        return rango if campo != "cita" else f"{rango} ({r.periodo}; {r.fuentes}; dato de {r.fecha_dato}; {r.capa})"
    if campo in (None, "valor_rango"):
        base = f"{fmt_num(r.valor, u)}{sep}{u}".strip()
        if campo is None and pd.notna(r["min"]) and pd.notna(r["max"]) and r.get("tipo_rango", "rango") == "rango":   # V17: no si son referencias
            base += f" ({fmt_num(r['min'], u)}{_guion(r['min'])}{fmt_num(r['max'], u)}{sep}{u})".rstrip()
        return base
    if campo in ("breve", "rango_breve"):
        div, esc = escala(r.valor if pd.notna(r.valor) else r["max"])
        red = lambda v, uu: redondeo(v, uu, div)  # noqa: E731
        hay_rango = pd.notna(r["min"]) and pd.notna(r["max"]) and r.get("tipo_rango", "rango") == "rango"
        if hay_rango and red(r["min"], u) == red(r["max"], u):
            div, esc = 1.0, ""
            red = fmt_num   # rango estrecho: el redondeo lo colapsaría («17-17»); se dan las cifras completas
        esc_u = (f"{esc} de {u}" if esc == "millones" and u[:1].isalpha() else f"{esc} {u}").strip() if esc else u
        rango = f"{red(r['min'], u)}{_guion(r['min'])}{red(r['max'], u)}" if hay_rango else ""
        if campo == "rango_breve" or pd.isna(r.valor):
            return f"{rango}{sep if not esc else ' '}{esc_u}".strip() if rango else f"{red(r.valor, u)} {esc_u}".strip()
        cola = f" ({rango}{(' ' + esc) if esc else ''})" if rango else ""
        return f"{red(r.valor, u)}{sep if not esc else ' '}{esc_u}".strip() + cola
    if campo == "valor":
        return f"{fmt_num(r.valor, u)}{sep}{u}".strip()
    if campo == "num":
        return fmt_num(r.valor, u)
    if campo in ("min_num", "max_num"):   # V16: extremo del rango sin unidad
        return fmt_num(r[campo[:3]], u)
    if campo == "sig":   # V16 (arbitraje del informe integral): 3 cifras significativas, para coeficientes y p pequeños
        return f"{float(r.valor):.3g}".replace("-", "−").replace(".", ",")
    if campo in ("min", "max"):
        return f"{fmt_num(r[campo], u)}{sep}{u}".strip()
    if campo == "rango":
        return f"{fmt_num(r['min'], u)}{_guion(r['min'])}{fmt_num(r['max'], u)}{sep}{u}".strip()
    if campo == "cita":
        return f"{texto(r, None)} ({r.periodo}; {r.fuentes}; dato de {r.fecha_dato}; {r.capa})"
    return str(r[campo])


def render(src: Path, ck: pd.DataFrame) -> tuple[str, list[str]]:
    falta: list[str] = []
    retiradas = T10.retiradas()
    odbl, usa_odbl = T10.odbl(), []

    def sub(m: re.Match) -> str:
        i, campo = m.group(1), m.group(2)
        if i.startswith("proyecto.") and campo is None:
            v = PROYECTO.get(i.split(".", 1)[1])
            if isinstance(v, str):
                return v
            falta.append(i)
            return m.group(0)
        if i not in ck.index:
            falta.append(i)
            return m.group(0)
        if i in retiradas:
            return T10.marca(retiradas[i])
        if i in odbl:
            usa_odbl.append(i)
        return texto(ck.loc[i], campo)

    txt = MARC.sub(sub, src.read_text())
    if usa_odbl:
        txt = txt.rstrip("\n") + "\n\n---\n\n" + T10.nota_odbl() + "\n"
    return txt, falta


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
