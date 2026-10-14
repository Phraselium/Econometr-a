"""V10-B2/B3: atlas y figuras. Cada tabla lleva capa, fuente y fecha; C1 solo con contraste; nada posterior al
pre-registro; texto sin lenguaje causal; cada figura con ficha."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
A = RAIZ / "output" / "v10" / "atlas"
TABLAS = sorted(A.glob("*.csv"))


@pytest.mark.parametrize("ruta", TABLAS, ids=lambda p: p.name)
def test_tablas_con_capa_fuente_fecha(ruta):
    d = pd.read_csv(ruta, dtype=str)
    if ruta.name == "a_contraste_eurostat.csv":
        return
    for c in ("capa", "fecha_dato"):
        assert c in d and d[c].notna().all(), (ruta.name, c)
    assert "fuente" in d and d.fuente.notna().all()
    assert d.capa.isin(["C1", "C2", "C4"]).all()


def test_c1_solo_con_contraste_eurostat():
    t = pd.read_csv(A / "a_quien_ecv.csv")
    c = pd.read_csv(A / "a_contraste_eurostat.csv")
    ok = set(map(tuple, c[c.coincide][["grupo", "categoria", "indicador"]].drop_duplicates().values))
    c1 = t[t.capa == "C1"]
    assert len(c1) > 0 and all((r.grupo, r.categoria, r.indicador) in ok for r in c1.itertuples())
    assert (t.n_muestral >= 50).all()


def test_sin_periodos_posteriores_al_preregistro():
    epa = pd.read_csv(A / "a_quien_epa.csv")
    assert not (epa.fecha_dato >= "2026-07-01").any()
    f = pd.read_csv(A / "b_fianzas_gva_cp.csv", dtype=str)
    assert f.anyo_datos.astype(int).max() <= 2025


def test_texto_sin_lenguaje_causal():
    txt = (RAIZ / "output/v10/atlas_descriptivo.md").read_text(encoding="utf-8").lower()
    for permitido in ("no causas", "atribuye causas", "no causal claims"):
        txt = txt.replace(permitido, "")
    for p in (r"\bprovoca", r"\bcaus", r"\bdebido a\b", r"\bimpulsad", r"\bpor culpa\b", r"\befecto de\b", r"\bexplica\b"):
        assert not re.search(p, txt), p


def test_fichas_de_figuras():
    fichas = json.loads((RAIZ / "figuras/fichas.json").read_text(encoding="utf-8"))
    assert len(fichas) >= 12
    for f in fichas:
        for k in ("titulo", "fuente", "fecha_dato", "capa", "texto_alternativo"):
            assert f[k], (f["id"], k)
        for r in f["ficheros"]:
            assert (RAIZ / "figuras" / r).exists(), r
