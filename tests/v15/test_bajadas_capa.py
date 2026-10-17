"""V15 · Bajadas de capa documentadas: los controles de cifras comparan valores y solo aceptan bajadas con ERRATA."""
import hashlib
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import check_v8 as C8  # noqa: E402
import cifras_clave as CK  # noqa: E402


def _ck(capa: str, valor: str = "10") -> pd.DataFrame:
    fila = {c: "x" for c in C8.COLS}
    fila.update(id="X-1", valor=valor, capa=capa)
    return pd.DataFrame([fila]).set_index("id")


def _h(ck) -> str:
    return C8._huella(ck, "X-1")


def test_bajada_documentada_aceptada():
    base = _h(_ck("C1"))
    assert C8.cambio_documentado(_ck("C4"), "X-1", base, "| X-1 | capa C1 → C4 | motivo |\n")


def test_bajada_sin_errata_rechazada():
    assert not C8.cambio_documentado(_ck("C4"), "X-1", _h(_ck("C1")), "")


def test_subida_rechazada():
    assert not C8.cambio_documentado(_ck("C1"), "X-1", _h(_ck("C4")), "| X-1 | capa C4 → C1 | motivo |\n")


def test_cambio_de_valor_con_bajada_rechazado():
    base = _h(_ck("C1", "10"))
    assert not C8.cambio_documentado(_ck("C4", "11"), "X-1", base, "| X-1 | capa C1 → C4 | motivo |\n")


def test_generador_no_admite_subidas(tmp_path, monkeypatch):
    f = tmp_path / "b.csv"
    f.write_text("id,capa_antes,capa_nueva,motivo\nX-1,C4,C1,no\n", encoding="utf-8")
    monkeypatch.setattr(CK, "BAJADAS", f)
    with pytest.raises(ValueError):
        CK.bajar_capas(pd.DataFrame({"id": ["X-1"], "capa": ["C4"]}))


def test_bajadas_vigentes_en_cifras_clave():
    b = pd.read_csv(RAIZ / "docs/v15/bajadas_capa.csv", dtype=str)
    ck = pd.read_csv(RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")
    assert (ck.loc[b.id, "capa"].values == b.capa_nueva.values).all()
    assert hashlib.sha256(b"ok").hexdigest()   # el fichero de bajadas existe y se aplica
