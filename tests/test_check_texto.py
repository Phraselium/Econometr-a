import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "v3"))
import check_texto as ct  # noqa: E402

FICHA = {"id": "x", "enunciado": "e", "capa": "C2", "magnitud": "como máximo 10 %", "intervalo": "[0, 10]",
         "cota": "10 %", "literatura": "-", "veredicto": "PARCIALMENTE", "limites": "-"}


def test_valorativo_y_partidista():
    assert ct.revisar_texto("Una medida escandalosa", "t")
    assert ct.revisar_texto("Según el PSOE", "t")
    assert not ct.revisar_texto("Según el PSOE <!-- check:ok cita literal -->", "t")
    assert not ct.revisar_texto("El alquiler subió un 4 % [C1]", "t")


def test_promocion_de_capa():
    assert ct.revisar_texto("[C4] Los turísticos provocan la subida", "t")
    assert not ct.revisar_texto("[C3] Los turísticos provocan +1 % (robusto)", "t")
    assert not ct.revisar_texto("[C2] Como máximo el 10 % puede deberse a turísticos", "t")
    txt = "# Afirmable con seguridad\n- [C4] algo\n- [C3] efecto de 2 %\n- [C3] efecto robusto de 2 %"
    assert len(ct.revisar_texto(txt, "t")) == 2


def test_fichas():
    assert not ct.revisar_ficha(FICHA, "f")
    assert ct.revisar_ficha({**FICHA, "capa": "C4", "veredicto": "RESPALDADA"}, "f")
    assert ct.revisar_ficha({k: v for k, v in FICHA.items() if k != "cota"}, "f")
    assert ct.revisar_ficha({**FICHA, "magnitud": "los turísticos causan la subida"}, "f")
