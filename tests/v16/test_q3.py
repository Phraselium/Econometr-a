"""Pruebas rápidas de Q3 (grupo B): utilidades, constructor del shift-share y forma de los resultados."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16"))
sys.path.insert(0, str(RAIZ / "src"))
import qb_comun as C  # noqa: E402

OUT = RAIZ / "output" / "v16" / "q3"
FUENTES = ["qb_comun.py", "qb_shiftshare.py", "q3_shiftshare.py", "q3_seccion.py", "q4_oferta.py", "q6_itp.py", "qb_informe.py"]
PROHIBIDO = ["data/" + "sealed", "evaluate_" + "v16", "sellar_" + "v16("]


def test_mco_fe_coincide_con_dummies():
    rng = np.random.default_rng(1)
    u = np.repeat(np.arange(6), 5)
    t = np.tile(np.arange(5), 6)
    x = rng.normal(size=30)
    y = 0.7 * x + u * 0.3 + t * 0.1 + rng.normal(scale=0.01, size=30)
    r = C.mco_fe(y, x, [u, t])
    D = np.column_stack([x, np.eye(6)[u], np.eye(5)[t][:, 1:]])
    b = np.linalg.lstsq(D, y, rcond=None)[0][0]
    assert abs(r["beta"][0] - b) < 1e-8


def test_oster_y_evalue():
    assert C.e_value_puntual(0.0, 1.0, 1.0) == 1.0
    assert C.e_value_puntual(0.5, 1.0, 1.0) > 1.0
    assert np.isfinite(C.oster_delta(0.5, 0.1, 0.4, 0.5))
    assert 0 < C.rv_q1(5.0, 100) < 1


def test_shiftshare_año_base_y_pesos_rotemberg():
    import qb_shiftshare as S
    s = S.shiftshare("provincia", 2003)
    assert s["x"].shape[0] == len(s["unidades"]) and np.isfinite(s["x"]).all()
    base = s["x"][:, s["ib"]]
    ext = 100 * s["F"][:, s["ib"], :].sum(1) / s["pob"][:, s["ib"]]
    assert np.allclose(base, ext, atol=1e-6)  # en el año base la razón de crecimiento es 1
    rot = np.loadtxt(OUT / "q3c_rotemberg.csv", delimiter=",", skiprows=1, usecols=1)
    assert abs(rot.sum() - 1.0) < 1e-9


def test_resultado_q3_forma_y_honestidad():
    r = json.loads((OUT / "resultado.json").read_text(encoding="utf-8"))
    for k in ["rama", "pregunta", "capa", "datos", "N", "metodo", "estimacion", "ic95", "p_ajustado", "nivel_evidencia", "diagnosticos", "fuera_muestra", "notas"]:
        assert k in r
    assert r["capa"] == "C4" and r["pendiente_sellada"] is True and r["p_ajustado"] is None
    assert r["ic95"]["Q3-c1"] is None and r["ic95"]["Q3-c2"] is None and r["ic95"]["Q3-b"] is not None
    con_p = [x["id"] for x in r["p_valores_para_BY"] if x["p"] is not None]
    assert con_p == ["Q3-b|principal"]
    assert r["estimacion"]["BLP_GATES_Q3"]["estado"].startswith("NO APTO")
    h = json.loads((OUT / "hechos.json").read_text(encoding="utf-8"))
    assert 0 < len(h) <= 10
    for x in h:
        assert x["id"].startswith("V16-Q3-") and x["capa"] == "C4" and x["ficha"].startswith("output/v16/q3/informe.md#")
        assert {"id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato", "ficha"} <= set(x)
    txt = (OUT / "informe.md").read_text(encoding="utf-8").lower().replace("sin lenguaje causal", "")
    assert "causal" not in txt
    assert (OUT / "registro.csv").exists()


@pytest.mark.parametrize("f", FUENTES)
def test_no_toca_muestra_sellada(f):
    src = (RAIZ / "src" / "v16" / f).read_text(encoding="utf-8")
    assert not any(p in src for p in PROHIBIDO)
