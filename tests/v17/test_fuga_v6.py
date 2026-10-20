"""V17 · Guarda de fuga v6 (check_v17, control 5; decisión del autor del 2026-10-20; incidente K4 de docs/v17/decisiones.md)."""
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v17"))
sys.path.insert(0, str(RAIZ / "src"))
import check_v17  # noqa: E402
import holdout  # noqa: E402


def test_detecta_el_incidente_de_d3():
    """La versión de src/v17/d3_cuantitativo.py del commit del incidente (415eb90) leía el IPV por CCAA de la base sin excluir las
    CCAA de los bloques sellados: la guarda la habría rechazado."""
    texto = subprocess.run(["git", "show", "415eb90:src/v17/d3_cuantitativo.py"], cwd=RAIZ, capture_output=True, text=True).stdout
    if not texto:   # clon superficial sin ese commit: se reconstruye el caso mínimo
        texto = 'HECHOS_BASE = "data/base/hechos.parquet"\nx = duckdb.sql(f"select * from {HECHOS_BASE} where not muestra_sellada_v6")\n'
    assert "muestra_sellada_v6" in texto   # el filtro de la base no basta: no marca las CCAA
    assert check_v17.fuga_v6_texto(texto)


def test_acepta_filtro_o_declaracion():
    lee = 'p = RAIZ / "data" / "raw" / "x.csv"\n'
    assert check_v17.fuga_v6_texto(lee)
    assert not check_v17.fuga_v6_texto(lee + "d = holdout.excluir_sellados_v6(d, 'cod', 'provincia')\n")
    assert not check_v17.fuga_v6_texto(lee + "d = sellado.filtrar(d, 'cod', 'provincia', 'periodo', 'v', 'T')\n")   # V18
    for a in ("nacional", "sin lectura de datos", "reproduce publicado"):
        assert not check_v17.fuga_v6_texto(f'ALCANCE_TERRITORIAL = "{a}"\n' + lee)
    assert check_v17.fuga_v6_texto('ALCANCE_TERRITORIAL = "provincial"\n' + lee)
    assert not check_v17.fuga_v6_texto('x = pd.read_csv(RAIZ / "output" / "v17" / "a.csv")\n')   # leer salidas no es leer datos


def test_filtro_excluye_las_ocho_ccaa_y_sus_unidades():
    assert sorted(holdout.ccaa_selladas_v6()) == ["02", "03", "04", "05", "13", "14", "15", "17"]
    cc = holdout.excluir_sellados_v6(pd.DataFrame({"c": ["13", "09", "2", "17"]}), "c", "ccaa")
    assert cc.c.tolist() == ["09"]
    prov = holdout.excluir_sellados_v6(pd.DataFrame({"c": ["28", "08", "7"]}), "c", "provincia")
    assert prov.c.tolist() == ["08"]
    sec = holdout.excluir_sellados_v6(pd.DataFrame({"c": ["2807901001", "0801901001"]}), "c", "seccion")
    assert sec.c.tolist() == ["0801901001"]
    nac = pd.DataFrame({"c": ["00"]})
    assert holdout.excluir_sellados_v6(nac, "c", "nacional").equals(nac)
