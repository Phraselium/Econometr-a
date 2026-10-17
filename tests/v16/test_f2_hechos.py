"""Tests de V16-F2.1 (hechos C1/C2 actualizados): determinismo, vara de C1 (dos fuentes independientes), tolerancias escritas en el código,
máximo de cifras, anclas de fichas, lecturas de la base con filtro de muestra sellada y ausencia de vocabulario causal."""
import json
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16"))
sys.path.insert(0, str(RAIZ / "src"))
import f2_hechos  # noqa: E402
import f2_hechos_base as base  # noqa: E402

SAL = RAIZ / "output" / "v16" / "f2_hechos"
CAUSAL = re.compile(r"\b(causa(?:n|do|da)?|provoc\w*|efecto causal|debido a|gracias a|impulsad[oa]s? por|explica(?:n)? (?:la|el) subida)\b", re.I)
CLAVES = {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"}


@pytest.fixture(scope="module")
def res():
    return f2_hechos.build()


def test_determinismo(res):
    otra = f2_hechos.build()
    assert json.dumps(res["hechos"], sort_keys=True) == json.dumps(otra["hechos"], sort_keys=True)
    if (SAL / "hechos.json").exists():
        assert json.loads((SAL / "hechos.json").read_text(encoding="utf-8")) == json.loads(json.dumps(res["hechos"]))


def test_forma_y_limite(res):
    h = res["hechos"]
    assert 0 < len(h) <= 60
    ids = [x["id"] for x in h]
    assert len(set(ids)) == len(ids) and all(i.startswith("V16-HEC-") for i in ids)
    for x in h:
        assert set(x) == CLAVES and x["capa"] in {"C1", "C2", "C4"}
        assert x["ficha"].startswith("output/v16/f2_hechos/fichas.md#")
        assert x["ficha"].split("#")[1] in res["fichas"]
    assert not res["avisos"], "discrepancias con la 1.0: es una parada del plan"


def test_c1_exige_dos_fuentes_independientes(res):
    c = {x["id"]: x for x in res["control"]}
    for x in res["hechos"]:
        k = c[x["id"]]
        assert all(s in base.GRUPO for s in k["fuentes"])
        if x["capa"] == "C1":
            assert len(k["grupos"]) >= 2, f"{x['id']}: C1 con un solo grupo de fuentes"
            for a, b in base.NO_INDEPENDIENTES:
                assert not (a in k["fuentes"] and b in k["fuentes"]), f"{x['id']}: pareja no independiente {a}/{b}"
            assert x["min"] is not None and x["max"] is not None
            if "ALQ-BRECHA" in x["id"] or "PRECIO" in x["id"]:
                assert x["max"] - x["min"] <= base.TOL_PP + 1e-6, f"{x['id']}: amplitud mayor que la tolerancia"
        if len(k["grupos"]) < 2:
            assert x["capa"] != "C1"


def test_vacias_censo_y_consumo_no_son_independientes(res):
    c = {x["id"]: x for x in res["control"]}
    k = c["V16-HEC-VACIAS-CONSUMO-2021"]
    assert k["capa"] == "C4" and k["grupos"] == ["censo"]


def test_tolerancias_escritas_en_el_codigo():
    assert base.TOL_PP == 3.0 and base.TOL_REL_RECUENTO == 0.15
    t = (RAIZ / "src" / "v16" / "f2_hechos_base.py").read_text(encoding="utf-8")
    assert "TOL_PP = 3.0" in t and "TOL_REL_RECUENTO = 0.15" in t and "ANTES de calcular" in t
    assert base.coinciden({"a": 10.0, "b": 12.9}) == ["a", "b"]
    assert base.coinciden({"a": 10.0, "b": 13.1}) == []
    assert base.capa_por_vara({"INE IPV": 10.0, "Notariado": 10.5})[0] == "C4"          # mismo grupo (notarial)
    assert base.capa_por_vara({"INE IPV": 10.0, "MIVAU valor tasado": 11.0})[0] == "C1"


def test_lecturas_de_la_base_filtran_muestra_sellada():
    for p in (RAIZ / "src" / "v16").glob("f2_hechos*.py"):
        t = p.read_text(encoding="utf-8")
        assert "data/sealed" not in t and "holdout" not in t.replace("src/holdout.py", "")
        if re.search(r"hechos\.parquet|vivienda\.duckdb|demanda_internacional\.parquet", t):
            assert "muestra_sellada_v6" in t, f"{p.name}: lee la base sin filtrar muestra_sellada_v6"


def test_sin_lenguaje_causal(res):
    textos = [json.dumps(res["hechos"], ensure_ascii=False)] + list(res["fichas"].values())
    for f in ("informe.md", "fichas.md"):
        if (SAL / f).exists():
            textos.append((SAL / f).read_text(encoding="utf-8"))
    for t in textos:
        m = CAUSAL.search(t)
        assert m is None, f"vocabulario causal: {m.group(0)!r}"


def test_vivienda_publica_pendiente_declarada():
    assert "Affordable Housing" in f2_hechos.PENDIENTE_PUBLICA
    if (SAL / "informe.md").exists():
        assert "PH4.2" in (SAL / "informe.md").read_text(encoding="utf-8")
