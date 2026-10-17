"""V16 · Validación sellada (src/holdout.py, bloque v16): sin solapes con v6 ni V15, determinista, y evaluate_v16 cerrado sin la
etiqueta prereg-v16 en el remoto."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout as H  # noqa: E402


def test_bloque_v16_no_solapa_ni_toca_v6():
    m16, m15 = H.municipios_sellados_v16(), H.municipios_sellados_v15()
    v6 = set(H.provincias_selladas_v6())
    assert m16 and not (m16 & m15)
    assert not {m for m in m16 if m[:2] in v6}
    assert not (set(H.celdas_selladas_v16()) & set(H.celdas_selladas_v15()))
    d16 = H.distritos_sellados_v16()
    propios = {d for d in d16 if d[:5] in m16}
    assert not ((d16 - propios) & H.distritos_sellados_v15())
    assert not {d for d in d16 if d[:2] in v6}


def test_bloque_v16_determinista():
    assert H.celdas_selladas_v16() == H.celdas_selladas_v16()
    assert H.municipios_sellados_v16() == H.municipios_sellados_v16()


def test_unidad_sellada_v16_incluye_v15_y_v6():
    m15 = sorted(H.municipios_sellados_v15())[0]
    m16 = sorted(H.municipios_sellados_v16())[0]
    v6 = H.provincias_selladas_v6()[0] + "001"
    s = H.unidad_sellada_v16(pd.Series([m15, m16, v6]), "municipio")
    assert s.tolist() == [True, True, True]


def test_sellar_v16_sin_manifiesto_se_niega(monkeypatch, tmp_path):
    monkeypatch.setattr(H, "MANIFIESTO_V16", tmp_path / "no.json")
    with pytest.raises(RuntimeError):
        H.sellar_v16(pd.DataFrame({"territorio_codigo": ["00"], "nivel": ["nacional"], "variable": ["x"], "frecuencia": ["A"],
                                   "periodo": ["2020"], "valor": [1.0]}), "prueba")


def test_evaluate_v16_cerrado_sin_etiqueta(monkeypatch, tmp_path):
    f = tmp_path / "e.json"
    f.write_text(json.dumps({}), encoding="utf-8")
    monkeypatch.setenv("ECONOMETRA_ETIQUETAS_REMOTAS", str(f))
    with pytest.raises(PermissionError):
        H.evaluate_v16("Q1", lambda d: {}, "prueba", ["q1"])
