"""V7.1-S1: dosis y coste reproducen R6; «no estimable» lleva motivo; Excel con colores y sin paneles inmovilizados."""
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parents[2]
S1 = RAIZ / "output" / "v7_1" / "S1"


def test_reproduce_r6():
    t = pd.read_csv(S1 / "dosis_coste.csv", dtype={"cc": str})
    im = pd.read_csv(RAIZ / "output/v7/R6/impactos.csv", dtype={"cc": str})
    im = im[(im.fuente_es == "rejilla") & (im.instrumento != "a_construccion")]   # v7.2: construcción reestimada con dosis no nula
    t = t[t.instrumento != "a_construccion"]
    m = t.merge(im, on=["cc", "instrumento", "mercado", "horizonte"], suffixes=("", "_r6"))
    assert len(m) == len(t) == len(im)
    assert (m.dprecio_med - m.dprecio_med_r6).abs().max() < 1e-3


def test_sin_coste_con_motivo():
    t = pd.read_csv(S1 / "dosis_coste.csv")
    sin = t[t.coste_anual_meur_med.isna()]
    assert sin.estado_coste.str.contains("no estimable|el efecto en alquiler es indirecto").all()
    assert sin[sin.estado_coste.str.startswith("coste no estimable")].estado_coste.str.contains(":").all()


def test_excel_colores_sin_inmovilizar():
    wb = load_workbook(RAIZ / "output/v7_1/atlas/tablas_regionales.xlsx")
    for ws in wb.worksheets:
        assert ws.freeze_panes is None, ws.title
    d, c = wb["DC_datos"], wb["DC_calculos"]
    assert d["E3"].font.color.rgb == "FF0000FF"   # dato de entrada: azul
    assert c["A3"].font.color.rgb == "FF008000"   # enlace a otra hoja: verde
    assert c["E3"].font.color.rgb == "FF000000"   # cálculo de la hoja: negro
