"""V15-B3 · Registro de subagentes: anota rol, tarea, tokens aproximados y ficheros tocados en docs/v15/subagentes.csv y
reescribe la sección «## Subagentes y tokens» de docs/v15/estado.md (tabla y total). Determinista; sin red.

Uso: python3 src/v15/registro_subagentes.py --rol auditor-datos --tarea "F1 precios de compra" --tokens 85000 \
         --ficheros output/v15/auditoria/precios_compra/ [--fecha AAAA-MM-DD]
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CSV = RAIZ / "docs" / "v15" / "subagentes.csv"
ESTADO = RAIZ / "docs" / "v15" / "estado.md"
CAMPOS = ["fecha", "rol", "tarea", "tokens", "ficheros"]
INI, FIN = "## Subagentes y tokens", "<!-- fin subagentes -->"


def leer() -> list[dict]:
    if not CSV.exists():
        return []
    with CSV.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def seccion(filas: list[dict]) -> str:
    L = [INI, "", "Generada por src/v15/registro_subagentes.py (fuente: docs/v15/subagentes.csv). Tokens aproximados según el informe de cada subagente.", "",
         "| Fecha | Rol | Tarea | Tokens | Ficheros |", "|---|---|---|---|---|"]
    L += [f"| {r['fecha']} | {r['rol']} | {r['tarea']} | {int(r['tokens']):,} | {r['ficheros']} |".replace(",", ".") for r in filas]
    tot = sum(int(r["tokens"]) for r in filas)
    por_rol = {}
    for r in filas:
        por_rol[r["rol"]] = por_rol.get(r["rol"], 0) + int(r["tokens"])
    L += ["", f"Total: {tot:,} tokens".replace(",", ".") + (" · " + "; ".join(f"{k}: {v:,}".replace(",", ".") for k, v in sorted(por_rol.items())) if por_rol else ""), "", FIN]
    return "\n".join(L) + "\n"


def escribir_estado(filas: list[dict]) -> None:
    t = ESTADO.read_text(encoding="utf-8") if ESTADO.exists() else "# V15 · Estado\n"
    if INI in t and FIN in t:
        t = t[:t.index(INI)] + t[t.index(FIN) + len(FIN) + 1:]
    ESTADO.write_text(t.rstrip("\n") + "\n\n" + seccion(filas), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rol", required=True)
    ap.add_argument("--tarea", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--ficheros", default="")
    ap.add_argument("--fecha", default=dt.date.today().isoformat())
    a = ap.parse_args()
    filas = leer() + [{"fecha": a.fecha, "rol": a.rol, "tarea": a.tarea, "tokens": a.tokens, "ficheros": a.ficheros}]
    CSV.parent.mkdir(parents=True, exist_ok=True)
    with CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, CAMPOS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    escribir_estado(filas)
    print(f"registro_subagentes: {len(filas)} filas; total {sum(int(r['tokens']) for r in filas)} tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
