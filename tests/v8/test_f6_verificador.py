"""V8-F6: fichas V8 del verificador (formato, neutralidad, trazabilidad a cifras_clave) y adenda V8 del historial."""
import json
import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
F = json.loads((RAIZ / "output" / "v8" / "fichas_verificador_v8.json").read_text(encoding="utf-8"))
CAMPOS = {"id", "tema", "enunciado", "magnitud", "intervalo", "literatura", "limites", "evidencia", "capa", "cota", "veredicto", "regla"}
VEREDICTOS = {"ANALIZADA, NO CONCLUYENTE", "NO ANALIZADA: FALTAN DATOS", "PARCIALMENTE", "CONTRADICHA", "NO RESPALDADA"}


def test_formato_y_reglas():
    assert len(F) >= 6 and len({x["id"] for x in F}) == len(F)
    for x in F:
        assert CAMPOS <= set(x) and x["id"].startswith("V8-V") and x["veredicto"] in VEREDICTOS
        assert x["capa"] in {"C3s", "C4"}
        assert x["veredicto"] == "ANALIZADA, NO CONCLUYENTE"   # C3s sin designación y C4: como máximo no concluyente
        assert x["ids_cifras"], x["id"]
        if x["capa"] == "C3s":
            assert "condicionad" in x["magnitud"] and "condicionad" in x["regla"] or "solo" in x["regla"]


def test_cifras_con_id_existente():
    ids = set(pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").id)
    for x in F:
        assert set(x["ids_cifras"]) <= ids, x["id"]
        assert all(i.startswith("V8-") for i in x["ids_cifras"])


def test_neutralidad_y_sin_marcadores():
    t = (RAIZ / "output" / "v8" / "verificador_v8.md").read_text(encoding="utf-8") + json.dumps(F, ensure_ascii=False)
    assert not re.search(r"\b(PSOE|PP|Vox|Sumar|Podemos)\b", t)   # siglas de partidos (el «pp» en minúscula es la unidad)
    assert not re.search(r"\b(gobierno|partido|programa electoral)\b", t, re.I)
    assert "{{" not in t and not re.search(r"\bnan\b", t, re.I)


def test_historial_adenda_v8():
    t = (RAIZ / "docs" / "v6_1" / "historial_conclusiones.md").read_text(encoding="utf-8")
    assert "Estado en V8 y porqué" in t and "incluye V8" in t and t.count("<!-- V8:inicio") == 1
    assert "Estado en v6.1 y porqué" in t   # las filas anteriores no se tocan
