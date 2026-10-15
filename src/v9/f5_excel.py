"""V9 F5 · publicacion/tablas_v9.xlsx (vía output/v9/tablas_v9.xlsx y `make publicacion`).

Convención de colores: azul = entrada (cifra de cifras_clave, con su id y fuente), negro = cálculo (fórmula Excel),
verde = enlace a otra hoja. Sin paneles inmovilizados. Determinista (metadatos de fecha fijos).
Hojas: Léeme · Entradas (ids V9) · Cálculos (amplitud del IC, ¿excluye el 0?, descomposición D7 recalculada) ·
Resumen (enlaces verdes a Entradas y Cálculos).
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd
from openpyxl import Workbook

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "v10"))
from tablas_excel import fijar_zip  # noqa: E402
from openpyxl.styles import Font

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v9" / "tablas_v9.xlsx"
AZUL, NEGRO, VERDE = Font(color="0000FF"), Font(color="000000"), Font(color="008000")
NEGRITA = Font(bold=True)


def main() -> int:
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str)
    v9 = ck[ck.id.str.startswith("V9-")].reset_index(drop=True)
    wb = Workbook()
    le = wb.active
    le.title = "Léeme"
    textos = ["Tablas V9 · qué causa qué (Borja Romero, economista; firma individual, independiente)",
              "Generado por src/v9/f5_excel.py desde output/v5/cifras_clave.csv (ids «V9-»). No editar a mano.",
              "Colores: azul = entrada (cifra publicada con su fuente); negro = cálculo (fórmula); verde = enlace a otra hoja.",
              "Ningún resultado de V9 alcanza C3/C3s: todas las cifras son asociaciones o descripciones (C4) o recuentos.",
              "Efectos en puntos logarítmicos ×100 (≈ %). Pre-registro: docs/v9/hipotesis.md y docs/v9/hipotesis_addendum_a1.md."]
    for i, t in enumerate(textos, 1):
        le.cell(i, 1, t).font = NEGRITA if i == 1 else NEGRO
    en = wb.create_sheet("Entradas")
    cols = ["id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "origen"]
    for j, c in enumerate(cols, 1):
        en.cell(1, j, c).font = NEGRITA
    fila_de = {}
    for i, r in v9.iterrows():
        fila = i + 2
        fila_de[r.id] = fila
        for j, c in enumerate(cols, 1):
            val = r[c]
            if c in ("valor", "min", "max") and pd.notna(val):
                val = float(val)
            cel = en.cell(fila, j, None if pd.isna(val) else val)
            cel.font = AZUL
    ca = wb.create_sheet("Cálculos")
    cab = ["id", "valor (enlace)", "amplitud del IC 95 %", "¿el IC excluye el 0?"]
    for j, c in enumerate(cab, 1):
        ca.cell(1, j, c).font = NEGRITA
    k = 2
    for i, r in v9.iterrows():
        if pd.isna(r["min"]):
            continue
        f = fila_de[r.id]
        ca.cell(k, 1, r.id).font = NEGRO
        ca.cell(k, 2, f"=Entradas!C{f}").font = VERDE
        ca.cell(k, 3, f"=Entradas!E{f}-Entradas!D{f}").font = NEGRO
        ca.cell(k, 4, f'=IF(OR(Entradas!D{f}>0,Entradas!E{f}<0),"sí","no")').font = NEGRO
        k += 1
    k += 1
    ca.cell(k, 1, "Descomposición D7 recalculada (ΔH = h̄·ΔP + P̄·Δh)").font = NEGRITA
    k += 1
    for j, c in enumerate(["zona y periodo", "H0", "H1", "P0", "P1", "ΔH", "componente población", "componente jefatura",
                           "% población", "control: % población publicado"], 1):
        ca.cell(k, j, c).font = NEGRITA
    k += 1
    for zona in ("ES", "CV"):
        for per in ("1121", "2225"):
            ref = {c: fila_de[f"V9-D7-{zona}-{per}-{c}"] for c in ("H0", "H1", "P0", "P1")}
            ca.cell(k, 1, f"{zona} {per[:2]}-{per[2:]}").font = NEGRO
            for j, c in enumerate(("H0", "H1", "P0", "P1"), 2):
                ca.cell(k, j, f"=Entradas!C{ref[c]}").font = VERDE
            ca.cell(k, 6, f"=C{k}-B{k}").font = NEGRO
            ca.cell(k, 7, f"=(B{k}/D{k}+C{k}/E{k})/2*(E{k}-D{k})").font = NEGRO
            ca.cell(k, 8, f"=(D{k}+E{k})/2*(C{k}/E{k}-B{k}/D{k})").font = NEGRO
            ca.cell(k, 9, f"=100*G{k}/F{k}").font = NEGRO
            ca.cell(k, 10, f"=Entradas!C{fila_de[f'V9-D7-{zona}-{per}-cuota-pob']}").font = VERDE
            k += 1
    re_ = wb.create_sheet("Resumen")
    for j, c in enumerate(["Afirmación evaluada", "Cifra principal", "Capa", "id"], 1):
        re_.cell(1, j, c).font = NEGRITA
    resumen = [("Topes Ley 11/2020: renta de contratos nuevos (ATT, %)", "V9-D1b-renta-att"),
               ("Zonas tensionadas Cataluña: renta (ATT, %)", "V9-D1a-renta-att"),
               ("Turísticos × reapertura: renta (% por DE de dosis)", "V9-D2-renta-reap"),
               ("Inmigración: IPC alquiler (% por punto)", "V9-D4-ipc-replica"),
               ("Tipos × tipo variable: precio a 4 trimestres (%)", "V9-D5-precio-h4"),
               ("Hogares 2022-2025: componente población (%)", "V9-D7-ES-2225-cuota-pob"),
               ("Resultados en C3/C3s", "V9-NC3")]
    for i, (txt, ident) in enumerate(resumen, 2):
        f = fila_de[ident]
        re_.cell(i, 1, txt).font = NEGRO
        re_.cell(i, 2, f"=Entradas!C{f}").font = VERDE
        re_.cell(i, 3, f"=Entradas!J{f}").font = VERDE
        re_.cell(i, 4, ident).font = NEGRO
    for ws in wb.worksheets:
        ws.freeze_panes = None
    fijo = dt.datetime(2026, 10, 15)
    wb.properties.created = fijo
    wb.properties.modified = fijo
    wb.properties.creator = "Borja Romero"
    wb.save(OUT)
    fijar_zip(OUT)
    print("tablas_v9.xlsx:", len(v9), "entradas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
