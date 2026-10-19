"""V17 · Registro de subagentes por fase: anota fase, rol, tarea, tokens aproximados y ficheros en docs/v17/subagentes.csv y
reescribe la sección «## Subagentes y tokens» de docs/v17/estado.md con el total por fase. Avisa (código 3) si una fase supera
4 millones de tokens de subagentes, que es una parada del plan (sección E). Determinista; sin red.

Uso: python3 src/v17/registro_subagentes.py --fase F1 --rol adquisidor-datos --tarea "renta y hogares" --tokens 150000 \
         --ficheros data/raw/v17/credito/ [--fecha AAAA-MM-DD]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CSV = RAIZ / "docs" / "v17" / "subagentes.csv"
ESTADO = RAIZ / "docs" / "v17" / "estado.md"
CAMPOS = ["fecha", "fase", "rol", "tarea", "tokens", "ficheros"]
INI, FIN = "## Subagentes y tokens", "<!-- fin subagentes -->"
TOPE_FASE = 4_000_000


def leer() -> list[dict]:
    if not CSV.exists():
        return []
    with CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _n(x: int) -> str:
    return f"{x:,}".replace(",", ".")


def por_fase(filas: list[dict]) -> dict[str, int]:
    t: dict[str, int] = {}
    for r in filas:
        t[r["fase"]] = t.get(r["fase"], 0) + int(r["tokens"])
    return t


def seccion(filas: list[dict]) -> str:
    L = [INI, "", "Generada por src/v17/registro_subagentes.py (fuente: docs/v17/subagentes.csv). Tokens aproximados según el informe "
         "de cada subagente. Tope por fase: 4.000.000 (parada E).", "",
         "| Fecha | Fase | Rol | Tarea | Tokens | Ficheros |", "|---|---|---|---|---|---|"]
    L += [f"| {r['fecha']} | {r['fase']} | {r['rol']} | {r['tarea']} | {_n(int(r['tokens']))} | {r['ficheros']} |" for r in filas]
    tf = por_fase(filas)
    L += ["", "| Fase | Tokens de subagentes |", "|---|---|"] + [f"| {f} | {_n(v)} |" for f, v in sorted(tf.items())]
    L += ["", f"Total V17: {_n(sum(tf.values()))} tokens", "", FIN]
    return "\n".join(L) + "\n"


def escribir_estado(filas: list[dict]) -> None:
    t = ESTADO.read_text(encoding="utf-8") if ESTADO.exists() else "# V17 · Estado\n"
    if INI in t and FIN in t:
        t = t[:t.index(INI)] + t[t.index(FIN) + len(FIN) + 1:]
    ESTADO.write_text(t.rstrip("\n") + "\n\n" + seccion(filas), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fase", required=True)
    ap.add_argument("--rol", required=True)
    ap.add_argument("--tarea", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--ficheros", default="")
    ap.add_argument("--fecha", default=dt.date.today().isoformat())
    a = ap.parse_args()
    filas = leer() + [{"fecha": a.fecha, "fase": a.fase, "rol": a.rol, "tarea": a.tarea, "tokens": a.tokens, "ficheros": a.ficheros}]
    CSV.parent.mkdir(parents=True, exist_ok=True)
    with CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, CAMPOS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    escribir_estado(filas)
    tf = por_fase(filas)
    print(f"registro_subagentes V17: {len(filas)} filas; fase {a.fase}: {tf[a.fase]} tokens; total {sum(tf.values())}")
    if tf[a.fase] > TOPE_FASE:
        print(f"PARADA: la fase {a.fase} supera 4.000.000 tokens de subagentes (plan, sección E)")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
