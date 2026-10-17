"""Pruebas de src/v16/f4_potencia.py: determinismo con la semilla y ausencia de unidades selladas (v6, V15 y V16) en las muestras."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))


def _modulo():
    if "v16_f4_potencia" in sys.modules:
        return sys.modules["v16_f4_potencia"]
    spec = importlib.util.spec_from_file_location("v16_f4_potencia", RAIZ / "src/v16/f4_potencia.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules["v16_f4_potencia"] = m
    spec.loader.exec_module(m)
    m.V15.REPS = 8
    return m


def test_semilla_fija():
    m = _modulo()
    assert m.SEED == 20261010
    d = m.logp(m.leer("ipc_alquiler_indice", "provincia", "T", "test_det"), min_t=60)
    d = d[d.u.isin(sorted(d.u.unique())[:12])].reset_index(drop=True)
    r1 = m.V15.placebo_continuo(d, m.ccaa_de(d.u), np.random.default_rng(m.SEED))
    r2 = m.V15.placebo_continuo(d, m.ccaa_de(d.u), np.random.default_rng(m.SEED))
    assert r1 == r2
    x = np.random.default_rng(1).normal(size=400)
    y = np.random.default_rng(2).normal(size=400)
    a = m.rd_placebo(x, y, np.ones(400), np.arange(400), [-0.5, 0.5], h=1.0)
    b = m.rd_placebo(x, y, np.ones(400), np.arange(400), [-0.5, 0.5], h=1.0)
    assert a == b
    c1, c2 = m.mc_cips(6, 40, np.random.default_rng(m.SEED)), m.mc_cips(6, 40, np.random.default_rng(m.SEED))
    assert json.dumps(c1, sort_keys=True) == json.dumps(c2, sort_keys=True)


def test_sin_unidades_selladas_en_las_muestras():
    m = _modulo()
    import holdout as HO
    for var, nivel, freq, desag in (("serpavi_alquiler_m2_mediana", "municipio", "A", "tipologia=VC"), ("serpavi_alquiler_m2_mediana", "seccion", "A", "tipologia=VC"),
                                    ("compraventas", "provincia", "T", None), ("compraventas", "ccaa", "T", None), ("ipva_tam_indice", "distrito", "A", "tamano=Total")):
        d = m.leer(var, nivel, freq, f"test_{var}_{nivel}", desag=desag)
        assert len(d) > 0
        assert not d.s6.fillna(False).astype(bool).any()
        u = pd.Series(d.u.unique())
        if nivel == "ccaa":
            assert not u.str.zfill(2).isin(m.CCAA_V6).any()
        else:
            assert not HO.unidad_sellada_v16(u, nivel).any()
        if nivel == "provincia":
            assert not u.isin(m.V6_PROV).any()
    # temporal: nada posterior al último periodo visto de V15
    d = m.leer("serpavi_alquiler_m2_mediana", "municipio", "A", "test_t", desag="tipologia=VC")
    assert d.t.max() <= m.ULTIMO_VISTO["serpavi_alquiler_m2_mediana|municipio|A"]


def test_salidas_si_existen():
    sal = RAIZ / "output/v16/potencia"
    if not (sal / "resultado.json").exists():
        return
    r = json.loads((sal / "resultado.json").read_text(encoding="utf-8"))
    assert r["capa"] == "C4" and r["estimacion"] is None and r["ic95"] is None
    ex = pd.read_csv(sal / "exclusiones.csv")
    assert (ex.unidades_despues <= ex.unidades_antes).all()
    t = pd.read_csv(sal / "potencia.csv")
    assert set(t.pregunta) == {f"Q{i}" for i in range(1, 11)}
