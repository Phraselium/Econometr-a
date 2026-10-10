"""A5 (v5): hechos.json generado desde el inventario, la conciliación con v4 y la validación de precisión (revisión A, B3).

Sin cifras tecleadas. Sin red y determinista. Corre después de a5_run.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PROG, OUT = RAIZ / "docs" / "v5" / "programas", RAIZ / "output" / "v5" / "A5"


def main() -> None:
    inv = pd.read_csv(PROG / "inventario.csv")
    con = pd.read_csv(PROG / "conciliacion_v4.csv")
    val = json.loads((OUT / "validacion_precision.json").read_text())
    ofi = inv[inv.oficial.astype(str).str.lower().isin(["si", "sí"])]
    tipos = ofi.tipo.astype(str).str.split(" ").str[0].value_counts().to_dict()
    fecha = str(pd.to_datetime(ofi.fecha_descarga, errors="coerce").max().date())
    excl = con.estado.astype(str).str.startswith("no verificable")
    conf = con.estado.astype(str).eq("confirmada")
    con_cita = con.cita_v4_en_texto_oficial.notna() & ~excl
    h = [
        dict(id="A5-H01", indicador="Documentos oficiales con texto buscado por palabras clave", valor=len(ofi), min=None, max=None,
             unidad="documentos", periodo="2023-2026", cobertura="; ".join(f"{k}: {v}" for k, v in sorted(tipos.items())),
             fuentes="docs/v5/programas/inventario.csv", capa="C4", fecha_dato=fecha),
        dict(id="A5-H02", indicador="Medidas de v4 sin documento oficial (excluidas de los recuentos)", valor=int(excl.sum()), min=None, max=None,
             unidad="medidas", periodo="2023", cobertura=f"{con[excl].doc_id.nunique()} documentos de v4", fuentes="docs/v5/programas/conciliacion_v4.csv",
             capa="C4", fecha_dato=fecha),
        dict(id="A5-H03", indicador="Medidas de v4 detectadas por el diccionario en el texto oficial", valor=int(conf.sum()), min=None, max=None,
             unidad="medidas", periodo="2023", cobertura=f"{int(con_cita.sum())} medidas de v4 con documento oficial (calibración en la misma muestra)",
             fuentes="docs/v5/programas/conciliacion_v4.csv", capa="C4", fecha_dato=fecha),
        dict(id="A5-H04", indicador="Precisión del diccionario: coincidencias que son una medida (estricta)", valor=round(100 * val["precision_estricta_M"], 1),
             min=round(100 * val["precision_estricta_M"], 1), max=round(100 * val["precision_M_o_X"], 1), unidad="%", periodo="2023-2026",
             cobertura=f"muestra aleatoria de {val['n']} coincidencias (máximo: medida o mención)", fuentes="output/v5/A5/validacion_precision.json",
             capa="C4", fecha_dato=fecha),
    ]
    (OUT / "hechos.json").write_text(json.dumps(h, ensure_ascii=False, indent=1))
    r = json.loads((OUT / "resultado.json").read_text())
    nota = (f"Los recuentos son COTAS de coincidencias del diccionario, no de medidas validadas: precisión {100 * val['precision_estricta_M']:.0f} % "
            f"(medida) y {100 * val['precision_M_o_X']:.0f} % (medida o mención), n = {val['n']}.")
    notas = r.get("notas", [])
    notas = [notas] if isinstance(notas, str) else notas
    r["notas"] = [x for x in notas if not str(x).startswith("Los recuentos son COTAS")] + [nota]
    (OUT / "resultado.json").write_text(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
