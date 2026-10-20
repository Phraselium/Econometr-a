"""V18 · Fase 2 · Reproducción de los estudios originales: resumen (docs/v18/reproduccion.md).

Une los resultados de los replicadores (output/v18/reproduccion/<clave>/resultado.json) y declara, para cada estudio clave de
la sección E del plan, si tiene paquete de replicación con datos, solo código o nada (según sus fichas de docs/v18/bib/ y el
catálogo output/v18/f1/catalogo.csv). Sin paquete con datos, el estudio pasa a la fase 3 solo con su especificación.
No lee datos del proyecto. Determinista; sin red.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[2]
REP = RAIZ / "output" / "v18" / "reproduccion"
SALIDA = RAIZ / "docs" / "v18" / "reproduccion.md"

# Estudios clave de la sección E y estado de su paquete (fichas de la fase 1; 2026-10-20).
CLAVE: list[tuple[str, str, str, str]] = [
    ("E1", "Garcia-López et al. (2020)", "sin paquete público", "datos de Airbnb y de alquiler de Barcelona de terceros"),
    ("E1", "Chaves-Fonseca (2026)", "chavesfonseca2026", "paquete CC BY 4.0 con datos"),
    ("E2", "Jofre-Monseny, Martínez-Mazza y Segú (2023)", "sin paquete público", "registro de fianzas del Incasòl (microdatos no públicos)"),
    ("E2", "Monràs y García-Montalvo (2023)", "sin paquete público", "contratos del Incasòl, no anuncios (ficha de la fase 1)"),
    ("E3", "González y Ortega (2013)", "sin paquete público", "padrón y valor tasado; se replica con nuestros datos"),
    ("E3", "Borusyak, Hull y Jaravel (2022)", "borusyak_hull_jaravel_2022", "método shift-share; aplicación ADH con datos (GPL-3.0)"),
    ("E4", "Fack (2006); Gibbons y Manning (2006); Grislain-Letrémy y Trevien (2022)", "sin paquete público", "microdatos administrativos"),
    ("E5", "Saiz (2010)", "sin paquete público", "solo resumen en la fase 1"),
    ("E5", "Baum-Snow y Han (2024)", "solo código", "el paquete completo (19,4 GB) no cabe en el disco; se bajaron 3 ficheros"),
    ("E6", "Mense (2025)", "mense_2025", "paquete CC0 con datos"),
    ("E6", "Asquith, Mast y Reed (2023)", "solo código", "CC0, sin datos (alquileres de terceros)"),
    ("E7", "Jarociński y Karadi (2020); Altavilla et al. (2019)", "datos de choques", "series de sorpresas del BCE: se usan como dato en la fase 4, no se reproducen"),
    ("E8", "Best y Kleven (2018); Besley, Meads y Surico (2014)", "sin paquete público", "datos fiscales administrativos"),
    ("E9", "Badarinza y Ramadorai (2018); Cvijanović y Spaenjers (2021)", "sin paquete público", "datos de transacciones de terceros"),
    ("E10", "Literatura de grandes tenedores (EE. UU. y Europa)", "sin paquete descargado", "Diamond et al. y Duso et al. existen, pero la descarga devolvió 403"),
    ("E11", "Segú (2020)", "sin paquete público", "datos fiscales franceses"),
    ("E12", "Koster y van Ommeren (2019)", "solo código", "sin datos (registros neerlandeses)"),
]


def main() -> int:
    res = {}
    for p in sorted(REP.glob("*/resultado.json")):
        r = json.loads(p.read_text(encoding="utf-8"))
        res[p.parent.name] = r
    L = ["# V18 · Fase 2 · Reproducción de los estudios originales", "",
         "Generado por src/v18/f2_reproduccion.py. Cada reproducción usa solo el paquete de su autor (data/bib/replicacion/, fuera de "
         "git) y no usa datos del proyecto; el código está en src/v18/reproduccion/ y las salidas en output/v18/reproduccion/. "
         "Veredicto: «coincide» (misma cifra al redondeo publicado o diferencia menor que el 5 % del coeficiente y dentro del error), "
         "«difiere con explicación» o «difiere sin explicación» (parada G).", "",
         "## Reproducciones", "", "| Clave | Método | N | Estimación | IC 95 % | Veredicto |", "|---|---|---|---|---|---|"]
    for k, r in res.items():
        ic = r.get("ic95") or ["", ""]
        ver = "coincide" if "coincide" in str(r.get("notas", "")).lower() else str(r.get("notas", ""))[:80]
        L.append(f"| [{k}](../../output/v18/reproduccion/{k}/informe.md) | {r.get('metodo', '')} | {r.get('N', '')} | "
                 f"{r.get('estimacion', '')} | [{ic[0]}; {ic[1]}] | {ver} |")
    L += ["", "## Estudios clave de la sección E", "",
          "Sin paquete con datos, el estudio pasa a la fase 3 solo con su especificación (plan, fase 2).", "",
          "| Factor | Estudio | Paquete | Nota | Reproducido |", "|---|---|---|---|---|"]
    for fa, est, paq, nota in CLAVE:
        hecho = "sí, coincide" if paq in res and "coincide" in str(res[paq].get("notas", "")).lower() else ("sí" if paq in res else "no")
        L.append(f"| {fa} | {est} | {paq if paq not in res else 'con datos'} | {nota} | {hecho} |")
    falta = [k for k in res if k not in {c[2] for c in CLAVE}]
    if falta:
        L += ["", "Otras reproducciones: " + ", ".join(falta) + "."]
    L += ["", "Ninguna reproducción difiere sin explicación: no hay parada G en esta fase."
          if all("coincide" in str(r.get("notas", "")).lower() for r in res.values())
          else "Hay reproducciones que no coinciden: véase su informe (parada G si no se explica)."]
    SALIDA.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f2_reproduccion V18: {len(res)} reproducciones; {len(CLAVE)} estudios clave -> {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
