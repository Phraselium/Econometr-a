"""V18 · fase 5: magnitudes preferidas (B5) y contabilidad de la subida. Determinismo, reglas de la adenda 1.9 y 1.10 y guardas de check_v17 y check_v18."""
import hashlib
import importlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
for p in (RAIZ / "src", RAIZ / "src" / "v18", RAIZ / "src" / "v18" / "estimacion", RAIZ / "src" / "v17"):
    sys.path.insert(0, str(p))
import check_v17  # noqa: E402
import f5_contabilidad as C  # noqa: E402
import f5_magnitudes as M  # noqa: E402


def _sha(d: Path) -> dict:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.glob("*")) if p.is_file()}


def test_combinar_episodio_pesos_no_negativos_y_rho_uno():
    y, se = np.array([-0.0384, -0.044, -0.058]), np.array([0.0064, 0.006, 0.014])
    for rho in (0.5, 0.8):
        m, s, w = M.combinar_episodio(y, se, rho)
        assert abs(w.sum() - 1) < 1e-9 and (w >= 0).all()
        assert 0 < s <= se.min() + 1e-12
    m1, s1, w1 = M.combinar_episodio(y, se, 1.0)
    assert w1[int(np.argmin(se))] == 1.0 and abs(m1 - y[int(np.argmin(se))]) < 1e-12


def test_solo_e2_entra_con_estimacion_propia_y_reglas_de_b5():
    est = M.estudios_todos()
    propias = [e for e in est if e.propia]
    assert [e.clave for e in propias] == ["E2-R1"]
    # los NO ESTIMABLE o ASOCIACIÓN designados no entran como estimación propia
    assert all(M.PROPIA[f][1] in ("NO ESTIMABLE", "ASOCIACIÓN") for f in M.PROPIA if f != "E2")
    r = M.construir("E2", est)
    assert any(u["propia"] for u in r["unidades"]) and r["k"] == 3        # episodio catalán contado una vez
    n_cat = [u for u in r["unidades"] if u["nombre"].startswith("episodio")]
    assert len(n_cat) == 1 and set(n_cat[0]["miembros"]) == {"jofremonseny2023", "monras2023", "E2-R1"}
    # K < 3: efecto fijo; sin error típico: rango, nunca metaanálisis
    assert M.construir("E6", est)["metodo"] == "un solo estudio en la unidad"
    assert M.construir("E4", est)["k"] == 2 and "efecto fijo" in M.construir("E4", est)["metodo"]
    for f in ("E7", "E8", "E9"):
        assert M.construir(f, est)["k"] == 0
        lo, hi, _ = M.rango_estudios(f, est)
        assert np.isfinite(lo)


def test_clase_designada_y_periodo_real():
    """K12 (árbitro, hallazgos 1 y 3): la fila B5 lleva la clase de la designada aunque no entre; periodo real del dato."""
    assert C._clase("no entra (ASOCIACIÓN)") == "ASOCIACIÓN" and C._clase("SUGESTIVO") == "SUGESTIVO"
    assert C._clase("no entra (NO ESTIMABLE)") == "NO ESTIMABLE"
    assert C._periodo_real("1995T1-2007T4", "2002T1 a 2007T4 (media de provincias no selladas)") == "2002T1-2007T4"
    assert C._periodo_real("1995T1-2007T4", "1995T1 a 2007T4") == "1995T1-2007T4"
    assert C._periodo_real("2014T1-2019T4", "2013T4 a 2019T4") == "2014T1-2019T4"   # nivel de partida: el trimestre anterior
    assert "ATT" not in M.UNIDAD["E2"]


def test_magnitudes_deterministas():
    est = M.estudios_todos()
    a = [M.fila_factor(f, est, {})[0] for f in sorted(M.S_F)]
    b = [M.fila_factor(f, est, {})[0] for f in sorted(M.S_F)]
    for x, y in zip(a, b):
        x.pop("_resultado"), y.pop("_resultado")
        assert x == y
    d1, d2 = M.distribucion("E3", 500), M.distribucion("E3", 500)
    assert np.array_equal(d1["x"], d2["x"])


def test_guardas_de_fuga_v6():
    for f in ("f5_magnitudes.py", "f5_contabilidad.py"):
        assert not check_v17.fuga_v6_texto((RAIZ / "src" / "v18" / f).read_text(encoding="utf-8"))
    assert "sellado.filtrar(" in (RAIZ / "src" / "v18" / "f5_contabilidad.py").read_text(encoding="utf-8")


def test_fase_f5_registrada():
    fase = importlib.import_module("fase")
    assert fase.FASES["f5"] == ["src/v18/f5_magnitudes.py", "src/v18/f5_contabilidad.py"]


def test_contabilidad_determinista_y_sin_cifras_en_la_principal(tmp_path, monkeypatch):
    check_v18 = importlib.import_module("check_v18")
    salidas = []
    for i in range(2):
        d = tmp_path / f"r{i}"
        monkeypatch.setattr(M, "OUT", d)
        monkeypatch.setattr(C, "OUT", d)
        assert M.main() == 0
        assert C.main() == 0
        salidas.append(d)
    assert _sha(salidas[0]) == _sha(salidas[1])
    cp = pd.read_csv(salidas[0] / "contabilidad.csv")
    fac = cp[cp.tipo_fila == "factor"]
    assert len(fac) and fac.contrib_med.isna().all() and fac.nota.str.startswith("sin magnitud").all()
    ne = cp[cp.tipo_fila == "no_explicado"]
    assert np.allclose(ne.contrib_med, ne.obs_pp)                     # todo queda sin explicar
    # no hay filas provinciales de la principal que sumen el total nacional
    assert set(cp.alineacion) == {"plan", "v8"}
    ci = pd.read_csv(salidas[0] / "contabilidad_ilustracion.csv")
    f = ci[ci.tipo_fila == "factor"]
    assert (f[f.soporte == "fuera del soporte"].contrib_med.isna()).all()   # fuera del soporte: sin cifra
    assert not ((ci.factor == "E5") | (ci.factor == "E6") | (ci.factor == "E4")).any()
    # E3 y E9 no se suman: E9 no está en la suma de la fila NOEXPL
    assert not ci[(ci.factor == "E9") & ci.en_suma].any().any()
    import json
    h = json.loads((salidas[0] / "hechos.json").read_text(encoding="utf-8"))
    assert all(x["capa"] == "C4" and x["clasificacion_v18"] in check_v18.CLASES and x["id"].startswith("V18-") for x in h)
    assert not [x["id"] for x in h if check_v18.CAUSAL.search(f"{x['indicador']} {x['nota']}")]
    assert len({x["id"] for x in h}) == len(h)
