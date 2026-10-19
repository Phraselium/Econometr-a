"""V17 · Fase 5 · Cifras V17 para cifras_clave (análisis a posteriori).

Reúne en output/v17/f5/hechos.json todas las cifras V17 de las fases 2 y 3 (output/v17/**/hechos.json y
output/v17/auditoria/*_hechos.json). Añade las cifras de documento que la corrección de las paradas P1 y P2 necesita citar
(docs/v17/bloqueos.md; decisión del autor del 2026-10-19), cada una con su documento y su página. Comprueba que los ids son únicos y
que todas son C4 con lectura V17. src/v5/cifras_clave.py lee solo este fichero de V17.
Determinista; sin red.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
V17 = RAIZ / "output" / "v17"
SALIDA = V17 / "f5" / "hechos.json"
FECHA = "2026-10-19"

# Cifras de documento (lectura «OF» o «juicio experto»), transcritas de las fichas de la fase 0, la fase 1 y la auditoría.
DOCUMENTO = [
    {"id": "V17-DOC-BDE-GT-ALQUILER-2024",
     "indicador": "Viviendas alquiladas como residencia habitual en manos de personas físicas con 11 o más viviendas, sobre el total "
                  "del alquiler de residencia habitual (no incluye personas jurídicas)",
     "valor": 2.4, "min": None, "max": None, "unidad": "% del alquiler de residencia habitual", "periodo": "2024",
     "cobertura": "España", "fuentes": ["Banco de España, Informe Anual 2025, cap. 2, cuadro 2.11, p. 169"],
     "capa": "C4", "lectura_v17": "OF", "fecha_dato": "2024", "ficha": "docs/v17/fuentes/titularidad.md",
     "nota": "a posteriori; cifra de documento"},
    {"id": "V17-DOC-OHB-GT-ALQUILER-BCN-2021",
     "indicador": "Viviendas de alquiler habitual de Barcelona ciudad en manos de grandes tenedores (104.958 de 290.416)",
     "valor": 36.1, "min": None, "max": None, "unidad": "% del alquiler habitual de la ciudad", "periodo": "1-1-2021",
     "cobertura": "Barcelona (municipio)", "fuentes": ["Observatori Metropolità de l'Habitatge de Barcelona (O-HB)"],
     "capa": "C4", "lectura_v17": "OF", "fecha_dato": "2021", "ficha": "docs/v17/fuentes/titularidad.md",
     "nota": "a posteriori; cifra de documento; solo la ciudad de Barcelona, no la media nacional"},
]


def traslacion(retiene: dict) -> dict:
    """La traslación θ es 1 menos lo que retiene el beneficiario: se deriva de la cifra de la auditoría, sin dato nuevo."""
    return {"id": "V17-AUD-RA-AYU-TRASLACION-MEDIANA",
            "indicador": "Traslación de las ayudas al alquiler a la renta (θ), mediana de 7 estudios con diseño, ninguno español; "
                         "min y max = extremos entre estudios (Eerola et al. 2026 y Fack 2006)",
            "valor": round(100 - retiene["valor"], 1), "min": round(100 - retiene["max"], 1), "max": round(100 - retiene["min"], 1),
            "unidad": "% de la ayuda", "periodo": "estudios publicados 2002-2026", "cobertura": "Francia, Reino Unido, EE. UU., "
            "Finlandia y Nueva Zelanda", "fuentes": retiene["fuentes"], "capa": "C4", "lectura_v17": "juicio experto",
            "fecha_dato": retiene.get("fecha_dato", FECHA), "ficha": "output/v17/auditoria/filas/ayudas_demanda.md",
            "nota": "a posteriori; derivada de V17-AUD-RA-AYU-RETIENE-MEDIANA (θ = 100 − retiene)"}


def main() -> int:
    filas: list[dict] = []
    fuentes = sorted(p for p in V17.rglob("hechos.json") if p != SALIDA) + sorted((V17 / "auditoria").glob("*_hechos.json"))
    for p in fuentes:
        for h in json.loads(p.read_text(encoding="utf-8")):
            h = dict(h)
            h.setdefault("ficha", str(p.relative_to(RAIZ)))
            filas.append(h)
    ids = {h["id"]: h for h in filas}
    if "V17-AUD-RA-AYU-RETIENE-MEDIANA" in ids and "V17-AUD-RA-AYU-TRASLACION-MEDIANA" not in ids:   # si la auditoría ya la da, no se deriva
        filas.append(traslacion(ids["V17-AUD-RA-AYU-RETIENE-MEDIANA"]))
    filas += DOCUMENTO
    vistos, dup = set(), []
    for h in filas:
        if h["id"] in vistos:
            dup.append(h["id"])
        vistos.add(h["id"])
    malos = [h["id"] for h in filas if h.get("capa") != "C4" or not str(h["id"]).startswith("V17-")]
    if dup or malos:
        print(f"f5_hechos V17: ids duplicados {dup}; capa o prefijo incorrectos {malos}")
        return 1
    for h in filas:
        if isinstance(h.get("fuentes"), str):
            h["fuentes"] = [h["fuentes"]]
        if not h.get("fecha_dato"):   # fecha del dato: el último año del periodo; si no hay, la de la lectura
            anios = re.findall(r"(?:19|20)\d\d", str(h.get("periodo", "")))
            h["fecha_dato"] = anios[-1] if anios else FECHA
        if not h.get("cobertura"):
            h["cobertura"] = "véase la ficha"
        h.setdefault("nota", "a posteriori")
        if "a posteriori" not in str(h["nota"]):
            h["nota"] = f"a posteriori; {h['nota']}"
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    (SALIDA.parent / "informe.md").write_text(
        "# V17 · Fase 5 · Cifras V17\n\nAnálisis a posteriori (V17). Generado por src/v17/f5_hechos.py: "
        f"{len(filas)} cifras V17 (todas C4, con su lectura V17 en columna propia) reunidas para output/v5/cifras_clave.csv.\n",
        encoding="utf-8")
    print(f"f5_hechos V17: {len(filas)} cifras de {len(fuentes)} ficheros -> {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
