"""Verificador v5 (`make verificador`, después de v3 y v4).

Parte de las fichas v4 (que ya incluyen las v3 transformadas) y:
1. añade las fichas nuevas de v5 (output/v5/*/fichas_verificador.json);
2. retira las fichas v3/v4 sustituidas por una ficha v5 sobre la misma afirmación (con el motivo en `sustituciones`);
3. aplica la regla B4: con capa C4, el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE»;
4. mantiene separados «ANALIZADA, NO CONCLUYENTE» y «NO ANALIZADA: FALTAN DATOS».
Salida: output/v5/verificador/ (fichas/*.json, verificador.md, resumen.csv). Sin red y determinista.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v3"))   # src/v4/verificador.py importa el de v3 como «verificador»
_spec = importlib.util.spec_from_file_location("verificador_v4", RAIZ / "src" / "v4" / "verificador.py")
v4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v4)

DEST = RAIZ / "output" / "v5" / "verificador"
SUSTITUCIONES = {
    "M7-V1": ("R1B-V1", "GSADF con tamaño corregido y frente a fundamentales"),
    "M4-V1": ("R1A-V1", "residentes y no residentes por provincia"),
    "M4-V2": ("CB-V3", "stock y flujos, con dos métodos"),
    "M5-V1": ("D1-V1", "traslado a precios por clase territorial"),
    "V09": ("CB-V1", "datos del CGPJ y de Interior: la afirmación ya está analizada"),
    "V01": ("B4-V2", "triangulación de B3, v2 y las cotas de v3 (la cota C2 de v3 se conserva)"),
    "V03": ("B4-V1", "triangulación de B3, v2 y las cotas de v3"),
    "V04": ("B4-V3", "triangulación de B3, v2 y A4"),
    "V12": ("B4-V4", "triangulación de B3, v2 y la cota de v3"),
}
VEREDICTOS_C4 = {"ANALIZADA, NO CONCLUYENTE", "NO ANALIZADA: FALTAN DATOS"}


def _v5() -> list[dict]:
    out = []
    for p in sorted((RAIZ / "output" / "v5").glob("*/fichas_verificador.json")):
        if p.parent.name == "verificador":
            continue
        out += json.loads(p.read_text(encoding="utf-8"))
    return out


def transformar(f: dict) -> dict:
    f = dict(f)
    if f.get("capa") == "C4" and f.get("veredicto") not in VEREDICTOS_C4:
        f["veredicto_previo"] = f["veredicto"]
        f["veredicto"] = "ANALIZADA, NO CONCLUYENTE"
    conv = f.get("convenciones")
    if not conv:
        f.pop("convenciones", None)
    elif not isinstance(conv, dict):
        f["convenciones"] = {"(nota)": str(conv)}
    for c in ("magnitud", "intervalo", "cota", "literatura", "regla", "limites"):
        f.setdefault(c, "—")
    return f


def main() -> list[dict]:
    viejas = [f for f in v4.main() if f["id"] not in SUSTITUCIONES]
    nuevas = [transformar(f) for f in _v5()]
    ids = {f["id"] for f in nuevas}
    assert all(n in ids for n, _ in SUSTITUCIONES.values()), "sustitución hacia una ficha v5 inexistente"
    fs = viejas + nuevas
    (DEST / "fichas").mkdir(parents=True, exist_ok=True)
    for viejo in (DEST / "fichas").glob("*.json"):
        viejo.unlink()
    for f in fs:
        (DEST / "fichas" / f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1))
    n = pd.Series([f["veredicto"] for f in fs]).value_counts()
    cab = ("# Verificador de afirmaciones sobre la vivienda en España (v5)\n\n"
           "Generado por `make verificador`. Cada ficha evalúa la afirmación, nunca a quien la formula, y se aplican las mismas reglas a todas. "
           "Capas: C1 hechos (≥2 fuentes independientes), C2 cotas con supuestos explícitos, C3 efectos identificados (ninguno) y "
           "C4 exploratorio. Con C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE». «NO ANALIZADA: FALTAN DATOS» quiere decir que "
           "no hay datos para analizar la afirmación, no que sea falsa.\n\n"
           "Recuento de veredictos: " + "; ".join(f"{k}: {v}" for k, v in n.items()) + ".\n\n"
           "| Id | Afirmación | Veredicto | Capa |\n|---|---|---|---|\n"
           + "".join(f"| {f['id']} | {f['enunciado']} | {f['veredicto']} | {f['capa']} |\n" for f in fs)
           + "\n## Fichas sustituidas en v5\n\n| Ficha anterior | Sustituida por | Motivo |\n|---|---|---|\n"
           + "".join(f"| {k} | {v[0]} | {v[1]} |\n" for k, v in SUSTITUCIONES.items()) + "\n")
    (DEST / "verificador.md").write_text(cab + "\n".join(v4.ficha_md(f) for f in fs), encoding="utf-8")
    pd.DataFrame([{k: f.get(k) for k in ("id", "tema", "enunciado", "veredicto", "capa")} for f in fs]).to_csv(DEST / "resumen.csv", index=False)
    return fs


if __name__ == "__main__":
    for f in main():
        print(f["id"], f["veredicto"], f["capa"])
