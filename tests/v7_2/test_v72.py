"""V7.2: construcción adicional con dosis no nula, f2 no difundible, comparadores de R5 rotulados y GSADF nacional reverificado."""
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parents[2]


def test_construccion_dosis_no_nula():
    a = pd.read_csv(RAIZ / "output/v7_2/construccion/impactos_construccion.csv", dtype={"cc": str})
    assert a.cc.nunique() == 17
    assert (a.dosis_anual_max > 0).all() and (a[a.horizonte == 10].dosis_med > 0).all()
    assert (a.dosis_anual_max <= a.necesidad_anual_T3 + 1e-6).all() and (a.dosis_anual_max <= a.capacidad_observada + 1e-6).all()
    t = pd.read_csv(RAIZ / "output/v7_1/S1/dosis_coste.csv", dtype={"cc": str})
    assert (t[(t.instrumento == "a_construccion") & (t.horizonte == 10)].dosis_med > 0).all()


def test_f2_no_difundible():
    ck = pd.read_csv(RAIZ / "publicacion/cifras_clave.csv")
    assert not ck.id.str.contains("f2_impuestos").any()
    for f in (RAIZ / "publicacion").glob("*.md"):
        assert "f2_impuestos" not in f.read_text(encoding="utf-8"), f.name


def test_r5_comparador_rotulado():
    for f in ("dm_permutacion.csv", "h7_p1_mejor_regional.csv"):
        d = pd.read_csv(RAIZ / "output/v7/R5" / f)
        assert "comparador_tipo" in d.columns and d.comparador_tipo.notna().all(), f
    r = (RAIZ / "output/v7/R5/resumen.md").read_text(encoding="utf-8")
    assert "Base más exigente" in r or "base más exigente" in r
    assert "comparador_tipo" in r


def test_gsadf_reverificado_y_ficha():
    rv = pd.read_csv(RAIZ / "output/v7_2/gsadf/reverificacion.csv")
    assert len(rv) == 14 and rv.coincide.all()
    v = (RAIZ / "publicacion/verificador/verificador_v7_1.md").read_text(encoding="utf-8")
    assert "V72-BURBUJA" in v and "Tampoco se puede afirmar que NO la haya" in v


def test_excel_construccion():
    wb = load_workbook(RAIZ / "output/v7_1/atlas/tablas_regionales.xlsx")
    k = wb["CONSTR_v72"]
    assert all(ws.freeze_panes is None for ws in wb.worksheets)
    assert k["C3"].font.color.rgb == "FF0000FF" and k["F3"].font.color.rgb == "FF000000"
    assert str(k["F3"].value).startswith("=MAX(")
