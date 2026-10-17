"""V15 · Validación sellada (src/holdout.py, sellar_v15/evaluate_v15). No abre ni escribe la muestra sellada real."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import holdout as h  # noqa: E402


def test_bloques_deterministas_y_anidados():
    a, b = h.celdas_selladas_v15(), h.celdas_selladas_v15()
    assert a == b and len(a) > 0
    mun = h.municipios_sellados_v15()
    assert not (mun & h._municipios_grandes())          # las grandes ciudades se sellan por distritos
    assert not any(m[:2] in h.provincias_selladas_v6() for m in mun)
    dis = h.distritos_sellados_v15()
    assert {d[:5] for d in dis} >= set(mun) & {d[:5] for d in dis}


def test_sellar_sin_manifiesto_se_niega(tmp_path, monkeypatch):
    monkeypatch.setattr(h, "MANIFIESTO_V15", tmp_path / "no_existe.json")
    monkeypatch.setattr(h, "SEALED", tmp_path / "sealed")
    with pytest.raises(RuntimeError):
        h.sellar_v15(pd.DataFrame({"territorio_codigo": ["46250"], "nivel": ["municipio"]}), "x")
    assert not (tmp_path / "sealed").exists()


def test_sellar_separa_temporal_y_espacial(tmp_path, monkeypatch):
    man = tmp_path / "m.json"
    man.write_text(json.dumps({"fecha_corte": "2026-10-17", "ultimo_periodo_visto": {"y|municipio|A": "2024"}}))
    monkeypatch.setattr(h, "MANIFIESTO_V15", man)
    monkeypatch.setattr(h, "SEALED", tmp_path / "sealed")
    monkeypatch.setattr(h, "LOG", tmp_path / "log")
    sell = sorted(h.municipios_sellados_v15())[0]
    libre = next(c for c in ("46250", "08019", "41091") if c not in h.municipios_sellados_v15())
    d = pd.DataFrame({"territorio_codigo": [libre, libre, sell, libre], "nivel": "municipio", "frecuencia": "A",
                      "variable": ["y", "y", "y", "z"], "periodo": ["2024", "2025", "2020", "2020"], "edicion": "2026-10-15", "valor": 1.0})
    tr = h.sellar_v15(d, "prueba")
    assert tr.index.tolist() == [0]                     # 2025 posterior, unidad sellada y variable no vista: selladas
    assert len(pd.read_parquet(tmp_path / "sealed" / "v15_prueba.parquet")) == 3


def test_evaluate_v15_con_puerta_cerrada(tmp_path, monkeypatch):
    p = tmp_path / "proyecto.json"
    p.write_text(json.dumps({"osf_prereg_v15": "PENDIENTE"}))
    monkeypatch.setattr(h, "PROYECTO", p)
    monkeypatch.setattr(h, "LOG", tmp_path / "log")
    with pytest.raises(PermissionError):
        h.evaluate_v15("P0", lambda s: {}, "prueba", ["x"])
    assert not (tmp_path / "log").exists()
