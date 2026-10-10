"""Verificador v4 (`make verificador`, después del v3).

Parte de las 14 fichas v3 (output/v3/verificador/fichas/*.json) y aplica los cambios de M0:
1. «SIN EVIDENCIA SUFICIENTE» se separa en dos veredictos:
   - «ANALIZADA, NO CONCLUYENTE»: hay análisis propio (cotas, diseños o hechos) y no decide la afirmación;
   - «NO ANALIZADA: FALTAN DATOS»: no hay datos para el análisis (el motivo concreto va en «regla»).
2. Cada ficha con cota de precio muestra su veredicto bajo las DOS convenciones de traducción a precio:
   - A (estricta, la de v3): traducciones con supuestos estructurales no estimados (ε, P/R = 1/uc) en C4;
   - B (estructural): esas traducciones cuentan como cotas C2.
3. Añade las fichas nuevas de v4 (output/v4/*/fichas_verificador.json, si existen: M1-M5).
Salida: output/v4/verificador/ (fichas/*.json, verificador.md, resumen.csv).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v3"))
import verificador as v3  # noqa: E402

DEST = RAIZ / "output" / "v4" / "verificador"

# Clasificación de las fichas v3 con «SIN EVIDENCIA SUFICIENTE» (motivo en «regla_v4»)
SPLIT = {
    "V01": ("ANALIZADA, NO CONCLUYENTE", "Hay cotas C2 de cantidad, cotas de precio C4 y un diseño (H3-1, C4); ninguno decide."),
    "V02": ("NO ANALIZADA: FALTAN DATOS", "Faltan datos de titularidad por tamaño de tenedor (solicitud al Catastro pendiente)."),
    "V03": ("ANALIZADA, NO CONCLUYENTE", "Hay cotas C2 de hogares (M2 la amplía) y traducciones a precio C4; ninguna decide."),
    "V04": ("ANALIZADA, NO CONCLUYENTE", "Hay hechos C1 de balance hogares-viviendas (M1) sin atribución de precio; el suelo no es detectable (P-C4)."),
    "V06": ("ANALIZADA, NO CONCLUYENTE", "H3-3a analizada: C4. No puede ser C3: la validación por fuente no es independiente y el cálculo de potencia vio municipios sellados (decisiones v3, O1)."),
    "V07": ("ANALIZADA, NO CONCLUYENTE", "H3-3b analizada: C4 (fallan pretendencias, placebo de fecha y sensibilidad); mismas salvedades de contaminación que V06."),
    "V09": ("NO ANALIZADA: FALTAN DATOS", "Faltan datos de ocupaciones ilegales por municipio y periodo (judiciales o policiales)."),
    "V10": ("NO ANALIZADA: FALTAN DATOS", "Falta una serie armonizada de tipos de ITP/IVA por CCAA y fecha con precios a escala fina; el diseño de diferencias no se realizó."),
    "V12": ("ANALIZADA, NO CONCLUYENTE", "Cota B4 analizada; con la convención A la traducción a precio es C4."),
    "V13": ("ANALIZADA, NO CONCLUYENTE", "Se analizaron indicadores de valoración (precio/renta, precio/alquiler), que discrepan en dirección; no se realizó test de exuberancia (GSADF), que los datos permitirían."),
    "V14": ("ANALIZADA, NO CONCLUYENTE", "Hay un hecho C1 sobre su peso en las compraventas (M4 lo amplía) y ningún diseño sobre el precio."),
}

# Veredicto bajo la convención B (traducciones a precio estructurales como C2), con su motivo
CONV_B = {
    # Regla B: la cota de precio se compara con la subida OBSERVADA del mismo periodo; «causa principal» queda
    # NO RESPALDADA solo si la cota es < 50 % de esa subida. B nunca cambia la capa de la ficha.
    "V01": ("ANALIZADA, NO CONCLUYENTE", "Con |ε_d| = 0,33 la cota de precio es ≤8,3 % de alquiler frente a una subida observada del 6,3 % "
            "(IPC de alquiler 2020-2024): la cota supera el 100 % de la subida (133 %) y no excluye la afirmación; "
            "con |ε_d| = 1 la cota es 2,7 % (44 % de la subida), y quedaría NO RESPALDADA."),
    "V03": ("ANALIZADA, NO CONCLUYENTE", "Compra 2014-2025: cota de precio ≤26,3 % frente a una subida observada de ≈33-34 % según la ponderación (≈78-79 % de la "
            "subida): no excluye la afirmación; alquiler: cota no informativa (227 %)."),
    "V11": ("PARCIALMENTE", "Igual en ambas convenciones: el signo de P-D (≤ 0, nulo con desplazamiento total) no depende de la traducción a precio."),
    "V12": ("PARCIALMENTE", "Con P/R = 1/uc: incompatible con 2021-2025 (signo contrario) y no descartada en 2014-2021 (la cota supera la subida observada)."),
}


def _cargar_v3() -> list[dict]:
    v3.main()   # regenera las fichas v3 a partir de output/v3 (sin red)
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((RAIZ / "output" / "v3" / "verificador" / "fichas").glob("V*.json"))]


def _nuevas() -> list[dict]:
    out = []
    for f in sorted((RAIZ / "output" / "v4").glob("M*/fichas_verificador.json")):
        out += json.loads(f.read_text(encoding="utf-8"))
    return out


RETIRADAS = {"V14": "sustituida por M4-V1 (una sola definición de comprador extranjero; revisión B, B1)"}
CAPA_V4 = {"V08": ("C4", "La cifra de vacías y su reparto proceden del Censo 2021 (consumo eléctrico); Catastro − hogares no es "
                   "independiente del Censo, que se construye sobre el Catastro (revisión B, B10/B8).")}
VEREDICTOS_C4 = {"ANALIZADA, NO CONCLUYENTE", "NO ANALIZADA: FALTAN DATOS", "SIN EVIDENCIA SUFICIENTE"}


def transformar(f: dict) -> dict:
    f = dict(f)
    if f["id"] in CAPA_V4:
        f["capa"], motivo = CAPA_V4[f["id"]]
        f["regla"] = f["regla"] + " v4: " + motivo
    if f["capa"] == "C4" and f["veredicto"] not in VEREDICTOS_C4:   # regla B4: con C4, como máximo «no concluyente»
        f["veredicto_previo"] = f["veredicto"]
        f["veredicto"] = "ANALIZADA, NO CONCLUYENTE"
    if f["veredicto"] == "SIN EVIDENCIA SUFICIENTE" and f["id"] in SPLIT:
        f["veredicto_v3"] = f["veredicto"]
        f["veredicto"], motivo = SPLIT[f["id"]]
        f["regla"] = f["regla"] + " v4: " + motivo
    f["literatura"] = f.get("literatura", "").replace("Banco de España, Informe Anual 2025 (DOI no comprobado)",
                                                       "Banco de España, Informe Anual 2025 (NO VERIFICADA: DOI no comprobado)")
    if f["id"] in CONV_B:
        vb, motivo = CONV_B[f["id"]]
        f["convenciones"] = {"A (estricta: traducción a precio en C4)": f["veredicto"],
                             "B (estructural: traducción a precio como C2)": f"{vb}. {motivo}"}
    return f


def ficha_md(f: dict) -> str:
    md = v3.ficha_md(f)
    if "convenciones" in f:
        md += "".join(f"| Convención {k} | {v} |\n" for k, v in f["convenciones"].items())
    return md


def main() -> list[dict]:
    fs = [transformar(f) for f in _cargar_v3() if f["id"] not in RETIRADAS] + [transformar(f) for f in _nuevas()]
    (DEST / "fichas").mkdir(parents=True, exist_ok=True)
    for f in fs:
        (DEST / "fichas" / f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1))
    cab = ("# Verificador de afirmaciones sobre la vivienda en España (v4)\n\n"
           "Generado por `make verificador`. Cada ficha evalúa la afirmación, no a quien la formula. Capas: C1 hechos "
           "(≥2 fuentes), C2 cotas, C3 efectos con identificación, C4 exploratorio. Veredictos: RESPALDADA, "
           "PARCIALMENTE, NO RESPALDADA, CONTRADICHA, ANALIZADA, NO CONCLUYENTE y NO ANALIZADA: FALTAN DATOS. "
           "Las fichas con cota de precio muestran su veredicto bajo las dos convenciones de traducción a precio.\n\n"
           "| Id | Afirmación | Veredicto (convención A) | Capa |\n|---|---|---|---|\n"
           + "".join(f"| {f['id']} | {f['enunciado']} | {f['veredicto']} | {f['capa']} |\n" for f in fs) + "\n")
    (DEST / "verificador.md").write_text(cab + "\n".join(ficha_md(f) for f in fs), encoding="utf-8")
    pd.DataFrame([{k: f.get(k) for k in ("id", "tema", "enunciado", "veredicto", "capa")} for f in fs]).to_csv(
        DEST / "resumen.csv", index=False)
    return fs


if __name__ == "__main__":
    for f in main():
        print(f["id"], f["veredicto"], f["capa"])
