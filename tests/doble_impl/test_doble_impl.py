"""Doble implementacion L2 (a ciegas): calculos.py frente a output/v5/cifras_clave.csv."""
import math

import pytest

import calculos as c
from comparar import FUNCIONES, comparar

# Cifras que NO coinciden (ninguna en esta ejecucion). Formato: id -> motivo explicito.
XFAIL: dict[str, str] = {}

_DF = comparar().set_index("id")


@pytest.mark.parametrize("id_", list(FUNCIONES))
def test_coincide_con_cifras_clave(id_):
    if id_ in XFAIL:
        pytest.xfail(XFAIL[id_])
    fila = _DF.loc[id_]
    assert fila["clase"] == "coincide", (id_, dict(fila))


def test_determinista():
    assert c.SEED == 20261010
    assert c.dh_2125() == c.dh_2125()


def test_valor_dentro_de_rango():
    for id_, f in FUNCIONES.items():
        v, lo, hi = f()
        if not math.isnan(v):
            assert lo - 1e-6 <= v <= hi + 1e-6, id_
