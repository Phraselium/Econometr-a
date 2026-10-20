"""V17 · tipo_rango solo cambia la escritura de las cifras V17; las anteriores se escriben como en su versión publicada."""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v5.render import muestra_rango  # noqa: E402


def test_v17_solo_si_es_rango():
    assert muestra_rango(pd.Series({"id": "V17-X", "tipo_rango": "rango"}))
    assert not muestra_rango(pd.Series({"id": "V17-X", "tipo_rango": "referencias"}))
    assert not muestra_rango(pd.Series({"id": "V17-X", "tipo_rango": "sin rango"}))


def test_anteriores_sin_cambio():
    """Las bandas SHAP de V8 (tipo «referencias» por su sentido) se siguen escribiendo, como en la versión publicada."""
    assert muestra_rango(pd.Series({"id": "V8-M9-shap-a-P2-factor_europeo", "tipo_rango": "referencias"}))
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv", usecols=["id", "min", "max"])
    md = (RAIZ / "output" / "v5" / "cifras_clave.md").read_text(encoding="utf-8")
    assert "| V8-M9-shap-a-P2-factor_europeo |" in md and "ref.:" not in md.split("| V8-M9-shap-a-P2-factor_europeo |")[1].split("\n")[0]
    assert ck.id.str.startswith("V8-M9-shap-").any()
