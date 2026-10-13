"""v6.2 L5: lista de cifras publicables y de cifras que no deben citarse fuera de contexto, generada desde cifras_clave.

Sin red; lee solo output/v5/cifras_clave.csv. Escribe docs/v6_2/cifras_publicables.md (el test L5 comprueba que coincide).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
from render import texto  # noqa: E402

SALIDA = RAIZ / "docs" / "v6_2" / "cifras_publicables.md"
# Aptas para difusión: hechos C1 y cotas C2 de la página única (y su contexto mínimo obligatorio).
APTAS = [
    ("dh_2125", "Citar con periodo y las dos fuentes (ECP y EPA)."),
    ("terminadas_1924", "Rango anual del territorio común; no extrapolar a País Vasco y Navarra."),
    ("L3-DEF-2124-SINBAJAS", "Es una cota: citar siempre el rango completo, nunca un punto ni el extremo alto solo."),
    ("A23-P2", "Variación del precio de compra con tres fuentes; no confundir con el IPV del INE."),
    ("A23-A2", "Alquiler de contratos vigentes; no es el alquiler de los contratos nuevos."),
    ("A23-A10", "Contratos nuevos, solo Comunitat Valenciana; no generalizar a España."),
    ("A23-A9", "Contratos nuevos, solo Cataluña."),
    ("E-B1-F", "Proyección del INE (C2), no previsión del autor."),
    ("R1C-001", "Hogares propietarios de su vivienda principal."),
]
# No citar fuera de contexto: C4, dependientes de supuestos o de un modelo, o con signo inestable.
NO_FUERA = [
    ("T3-H5b", "Necesidad anual: contabilidad con supuestos (C4); citar el rango y la definición A+R+V+F−M−K."),
    ("T3-H5", "Necesidad con sensibilidad X (C4)."),
    ("D1-H11", "Traslado a precio en una rejilla de elasticidades supuestas: no es una estimación."),
    ("D1-H12", "Ídem."),
    ("K2-CUOTA-COMPRA-SINPOB-SIN", "Inmigración, asociación total (C4): no es un efecto."),
    ("K2-CUOTA-COMPRA-SIN", "Inmigración, asociación directa a igual población (mal control): el signo negativo no implica que abarate."),
    ("K1-N-MEJOR", "Predicción, no causalidad; solo frente a la base más exigente."),
    ("latente_convivencia", "Demanda latente: cota con supuestos sobre preferencias."),
    ("B4-v3-vut-cantidad", "Cota máxima del stock desplazado por viviendas turísticas; no es el efecto en el precio."),
    ("L3-DEF-2124-BAJAST1", "Única cifra de déficit con bajas: bajas estimadas en v5.1 (T1) sobre las 8 variantes de L3 (C4)."),
    ("L3-DEF-2124-SENS", "Sensibilidad del déficit: citarla junto al rango completo, nunca sola."),
]
HISTORICAS = [   # v7.2: retiradas de cifras_clave.csv; se leen de cifras_superadas.csv
    ("deficit_2124_c1", "Sustituida en v6.2 por L3-DEF-2124-SINBAJAS. No citar."),
    ("T3-H1", "Sustituida en v6.2 por L3-DEF-2124-SINBAJAS. No citar."),
    ("deficit_2124_c2", "Bajas supuestas sin respaldo; retirada en v7.2 (sustituta: L3-DEF-2124-BAJAST1). No citar."),
    ("L3-DEF-2124-CONBAJAS", "Bajas supuestas sin respaldo; retirada en v7.2 (sustituta: L3-DEF-2124-BAJAST1). No citar."),
    ("T3-H2", "Sustituida en v6.2 por L3-DEF-2124-BAJAST1. No citar."),
    ("B1-H1", "Necesidad de v5; sustituida por T3-H5b. No citar."),
]


def fila(c, i, nota):
    r = c.loc[i]
    v = texto(r, "rango") if r.capa == "C2" and r.notna()["min"] else texto(r, None)   # cota: solo el rango, sin punto central
    return f"| {i} | {r.indicador} | {v} | {r.capa} | {r.periodo} | {r.fecha_dato} | {r.fuentes} | {nota} |"


def generar() -> str:
    c = pd.concat([pd.read_csv(RAIZ / "output" / "v5" / f) for f in ("cifras_clave.csv", "cifras_superadas.csv")]).set_index("id", drop=False)
    cab = "| id | Indicador | Valor (rango) | Capa | Periodo | Fecha del dato | Fuentes | Cómo citarla |\n|---|---|---|---|---|---|---|---|"
    L = ["# Cifras publicables (v6.2, L5)", "",
         "Generado por src/v6_2/l5_publicables.py desde output/v5/cifras_clave.csv; no editar a mano. "
         "Toda cifra se cita con su rango, periodo, fuente, fecha del dato y capa.", "",
         "## Aptas para difusión (C1 o cota C2)", "", cab] + [fila(c, i, n) for i, n in APTAS] + [
         "", "## No citar fuera de contexto (C4 o dependientes de supuestos)", "", cab] + [fila(c, i, n) for i, n in NO_FUERA] + [
         "", "## Históricas: no citar (sustituidas; ver ERRATA.md)", "", cab] + [fila(c, i, n) for i, n in HISTORICAS] + [""]
    return "\n".join(L)


if __name__ == "__main__":
    SALIDA.write_text(generar(), encoding="utf-8")
    print(f"l5_publicables: {len(APTAS)} aptas, {len(NO_FUERA)} no fuera de contexto")
