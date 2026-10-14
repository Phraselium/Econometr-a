"""V9-DATOS: Incasòl (Generalitat de Catalunya), renta media de fianzas por municipio (Socrata qww9-bvhh).
Solo descarga, comparación con la versión v3 y registro. Periodos convertidos a trimestre para marcar_posterior_prereg.
Licencia: los metadatos del dataset dicen «See Terms of Use» (no CC BY): redistribuible = False.
"""
from __future__ import annotations

import csv
import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v9.comun import RAW9, descargar, registrar, sha256, marcar_posterior_prereg  # noqa: E402

FUENTE = "incasol"
DIR = RAW9 / FUENTE
ID = "qww9-bvhh"
CSV_URL = f"https://analisi.transparenciacatalunya.cat/resource/{ID}.csv?$limit=10000000"
META_URL = f"https://analisi.transparenciacatalunya.cat/api/views/{ID}.json"
V3 = RAW9.parent.parent / "raw" / "v3" / "incasol_fianzas_municipio_v3.csv.gz"
TRIM = {"gener-març": "T1", "abril-juny": "T2", "juliol-setembre": "T3", "octubre-desembre": "T4"}
SALIDA = DIR / f"incasol_{ID}_actual.csv.gz"


def periodo_iso(any_: str, periode: str) -> str:
    t = TRIM.get(periode.strip().lower())
    return f"{any_}{t}" if t else f"{any_}_{periode.strip()}"


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        man = DIR / "_manifest.csv"
        if not man.exists():
            print("falta _manifest.csv"); return 1
        with open(man, encoding="utf-8") as f:
            for fila in csv.DictReader(f):
                ruta = RAW9.parent.parent / fila["fichero"]
                if not ruta.exists() or sha256(ruta) != fila["sha256"]:
                    print("FALLO", fila["fichero"]); return 1
        print("OK incasol"); return 0
    meta = json.loads(Path(descargar(META_URL, DIR / "original" / "metadatos.json")).read_text(encoding="utf-8"))
    licencia = (meta.get("license") or {}).get("name") or "no consta"
    with open(descargar(CSV_URL, DIR / "original" / f"{ID}.csv", timeout=600), encoding="utf-8") as f:
        actual = list(csv.DictReader(f))
    previos = set()
    if V3.exists():
        with gzip.open(V3, "rt", encoding="utf-8") as g:
            previos = {(r["any"], r["periode"]) for r in csv.DictReader(g)}
    nuevos = sorted({(r["any"], r["periode"]) for r in actual} - previos)
    cols = ["ambit_territorial", "codi_territorial", "nom_territori", "any", "periode", "periodo_iso",
            "habitatges", "renda", "tram_preus"]
    with gzip.open(SALIDA, "wt", encoding="utf-8", newline="") as g:
        w = csv.DictWriter(g, fieldnames=cols)
        w.writeheader()
        for r in actual:
            w.writerow({**{c: r.get(c, "") for c in cols if c != "periodo_iso"},
                        "periodo_iso": periodo_iso(r["any"], r["periode"])})
    import pandas as pd
    df = marcar_posterior_prereg(pd.read_csv(SALIDA, dtype=str, encoding="utf-8"), "periodo_iso")
    df.to_csv(SALIDA, index=False, compression="gzip", encoding="utf-8")
    periodos = sorted({(r["any"], r["periode"]) for r in actual})
    registrar(FUENTE, SALIDA, CSV_URL, edicion=f"Socrata {ID} (rowsUpdatedAt {meta.get('rowsUpdatedAt')})",
              periodo=f"{periodos[0]}–{periodos[-1]}", nivel_territorial="municipio (código INE 5 dígitos)",
              licencia=f"{licencia} (metadatos Socrata; no CC BY)", redistribuible=False,
              notas=f"filas={len(actual)}; periodos_nuevos_vs_v3={nuevos}; columna posterior_prereg")
    print("filas", len(actual), "nuevos", nuevos, "licencia", licencia)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
