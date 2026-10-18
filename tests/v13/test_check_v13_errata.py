"""V16 (B-4, orden del autor): check_v13 admite una cifra nueva solo con «id | nueva» en ERRATA.md y un cambio de valor solo con
«id | sha256_nuevo». Se comprueba sobre un repositorio mínimo en tmp_path (no toca el real)."""
import hashlib
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v13 import check_v13 as C  # noqa: E402

COLS = C.C8.COLS


def _fila(i, valor):
    return dict(id=i, indicador=f"indicador {i}", valor=valor, min="", max="", unidad="u", periodo="2025", cobertura="España",
                fuentes="INE", capa="C4", fecha_dato="2026-10-16")


def _huella(f):
    return hashlib.sha256("|".join(str(f[c]) for c in COLS).encode()).hexdigest()


def _repo(tmp_path, monkeypatch, base, actual, errata):
    (tmp_path / "docs/v13").mkdir(parents=True)
    (tmp_path / "output/v5").mkdir(parents=True)
    pd.DataFrame([{"id": f["id"], "sha256": _huella(f)} for f in base]).to_csv(tmp_path / "docs/v13/cifras_base_v12.csv", index=False)
    pd.DataFrame(actual, columns=COLS).to_csv(tmp_path / "output/v5/cifras_clave.csv", index=False)
    (tmp_path / "ERRATA.md").write_text(errata, encoding="utf-8")
    monkeypatch.setattr(C, "RAIZ", tmp_path)


def test_sin_cambios_pasa(tmp_path, monkeypatch):
    a = _fila("X-1", "1")
    _repo(tmp_path, monkeypatch, [a], [a], "# Fe de erratas\n")
    assert C.cifras_sin_cambios() == []


def test_rechaza_cifra_nueva_no_declarada(tmp_path, monkeypatch):
    a, b = _fila("X-1", "1"), _fila("X-NUEVA", "2")
    _repo(tmp_path, monkeypatch, [a], [a, b], "# Fe de erratas\n")
    assert C.cifras_sin_cambios() == ["cifra nueva en V13 (sin análisis nuevo): X-NUEVA"]


def test_admite_cifra_nueva_declarada(tmp_path, monkeypatch):
    a, b = _fila("X-1", "1"), _fila("X-NUEVA", "2")
    _repo(tmp_path, monkeypatch, [a], [a, b], "| id | huella |\n|---|---|\n| X-NUEVA | nueva |\n")
    assert C.cifras_sin_cambios() == []


def test_rechaza_cambio_de_valor_no_declarado(tmp_path, monkeypatch):
    a, a2 = _fila("X-1", "1"), _fila("X-1", "1.5")
    _repo(tmp_path, monkeypatch, [a], [a2], "# Fe de erratas\n")
    assert C.cifras_sin_cambios() == ["cifra cambiada sin ERRATA: X-1"]


def test_nueva_no_vale_para_un_cambio_de_valor(tmp_path, monkeypatch):
    a, a2 = _fila("X-1", "1"), _fila("X-1", "1.5")
    _repo(tmp_path, monkeypatch, [a], [a2], "| X-1 | nueva |\n")
    assert C.cifras_sin_cambios() == ["cifra cambiada sin ERRATA: X-1"]


def test_admite_cambio_de_valor_con_huella(tmp_path, monkeypatch):
    a, a2 = _fila("X-1", "1"), _fila("X-1", "1.5")
    _repo(tmp_path, monkeypatch, [a], [a2], f"| X-1 | {_huella(a2)} |\n")
    assert C.cifras_sin_cambios() == []


def test_cifras_de_la_20_solo_desde_output_v15_v16(tmp_path, monkeypatch):
    """K22 (fase 7 de V16): una cifra V15-/V16- nueva se admite solo si su origen es output/v15 u output/v16."""
    a = _fila("X-1", "1")
    b = dict(_fila("V16-Q9-g", "5.9"), origen="output/v16/q9/hechos.json:V16-Q9-g")
    c = dict(_fila("V16-FALSA", "1"), origen="output/v5/X/hechos.json:V16-FALSA")
    _repo(tmp_path, monkeypatch, [a], [dict(a, origen="output/v5/X/hechos.json:X-1"), b, c], "# Fe de erratas\n")
    pd.DataFrame([dict(a, origen="o"), b, c]).to_csv(tmp_path / "output/v5/cifras_clave.csv", index=False)
    assert C.cifras_sin_cambios() == ["cifra nueva en V13 (sin análisis nuevo): V16-FALSA"]
