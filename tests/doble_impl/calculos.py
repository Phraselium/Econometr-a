"""Segunda doble implementacion (L2, v6.2), a ciegas: sigue SOLO output/v6_2/anexo_metodologico.md.

Cada funcion devuelve (valor, min, max). Determinista, sin red, SEED=20261010.
Capa C4 (documentacion/verificacion). Lee solo data/raw y las tablas intermedias que el anexo cita.
"""
from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
RAIZ = Path(__file__).resolve().parents[2]
RAW = RAIZ / "data" / "raw"


@lru_cache(maxsize=None)
def _csv(rel: str, **kw) -> pd.DataFrame:
    return pd.read_csv(RAW / rel, **kw)


# ----------------------------------------------------------------- hogares
def _ecp() -> pd.Series:
    d = _csv("ine_hogares_60131.csv")
    d = d[d.nombre == "Total Nacional. Total. Hogares en viviendas familiares. Número."]
    return d.drop_duplicates("periodo").set_index("periodo")["valor"].astype(float)


def _epa() -> pd.Series:
    d = _csv("ine_epa_hogares.csv")
    d = d[d.nombre == "Hogares. Total Nacional. Ambos sexos. Total. Total."]
    return d.drop_duplicates("periodo").set_index("periodo")["valor"].astype(float) * 1000.0


def dh_2125():
    epa, ecp = _epa(), _ecp()
    m = lambda y: np.mean([epa[f"{y}T{q}"] for q in range(1, 5)])  # noqa: E731
    v_epa = m(2025) - m(2021)
    v_ecp = ecp["2025T1"] - ecp["2021T1"]
    lo, hi = min(v_epa, v_ecp), max(v_epa, v_ecp)
    return (lo + hi) / 2, lo, hi


# ------------------------------------------------------------- terminadas
def _miv_serie(fichero: str, serie: str) -> pd.Series:
    d = _csv(fichero)
    d = d[d.serie == serie].copy()
    d["a"] = d.periodo.astype(str).str[:4].astype(int)
    return d.groupby("a")["valor"].sum().astype(float)


def _term(territorio: str | None = None) -> pd.Series:
    """libres + protegidas definitivas anuales. territorio: None=nacional, o sufijo ccaa."""
    suf = "nacional" if territorio is None else f"ccaa_{territorio}"
    lib = _miv_serie("mivau_v2_iniciadas_terminadas_prov.csv", f"viv_libres_terminadas_anual_{suf}")
    pro = _miv_serie("mivau_v2_protegida.csv", f"prot_definitiva_anual_{suf}")
    return lib.add(pro, fill_value=0.0)


def _libres_nac() -> pd.Series:
    return _miv_serie("mivau_v2_iniciadas_terminadas_prov.csv", "viv_libres_terminadas_anual_nacional")


def _pv_na() -> pd.Series:
    return _term("pais_vasco").add(_term("navarra_comunidad_foral_de"), fill_value=0.0)


def terminadas_1924():
    comun = _term() - _pv_na()
    s = comun.loc[2019:2024]
    return float("nan"), float(s.min()), float(s.max())


def _parque_bajas():
    d = _csv("mivau_parque.csv")
    d = d[d.serie == "parque_total_viviendas_nacional"].copy()
    d["a"] = d.periodo.astype(int)
    suma = d.set_index("a").loc[2020:2023, "valor"].sum()
    return 0.001 * suma, 0.002 * suma


@lru_cache(maxsize=None)
def _catastro_altas() -> float:
    c = _csv("catastro_urbana_municipios.csv.gz")
    c = c[c.unidad == "unidades_urbanas_residenciales"]
    uu = c.groupby("periodo")["valor"].sum()
    return float(sum(uu[y + 1] - uu[y] for y in range(2021, 2025)))


def _hogares_variantes() -> dict[str, float]:
    epa, ecp = _epa(), _ecp()
    base = epa["2024T4"] - epa["2020T4"]
    salto = epa["2021T1"] - epa["2020T4"]
    d = epa.diff()
    b = base - salto + np.mean([d["2020T4"], d["2021T2"]])
    b4 = base - salto + np.mean([d["2020T3"], d["2020T4"], d["2021T2"], d["2021T3"]])
    d1 = ecp["2024T4"] - epa["2020T4"] * (ecp["2021T1"] / epa["2021T1"])
    m2020 = np.mean([d[f"2020T{q}"] for q in range(1, 5)])
    d2 = ecp["2024T4"] - (ecp["2021T1"] - m2020)
    return {
        "v1": base + 242400.0, "a": base, "b": b, "b4": b4, "c": base - salto,
        "d1": d1, "d2": d2, "e": ecp["2024T4"] - ecp["2021T1"],
    }


def _terminadas_fuentes() -> dict[str, float]:
    with_p = float((_term().loc[2021:2024]).sum())
    sin_p = float(_libres_nac().loc[2021:2024].sum())
    pvna = float(_pv_na().loc[2021:2024].sum())
    return {"con_prot": with_p, "sin_prot": sin_p, "catastro": _catastro_altas() + pvna}


def _def_sin_bajas() -> list[float]:
    h, t = _hogares_variantes(), _terminadas_fuentes()
    return [hv - tv for hv in h.values() for tv in t.values()]


def L3_DEF_2124_SINBAJAS():
    x = _def_sin_bajas()
    lo, hi = min(x), max(x)
    return (lo + hi) / 2, lo, hi


def L3_DEF_2124_CONBAJAS():
    x = _def_sin_bajas()
    b01, b02 = _parque_bajas()
    lo = min(x)
    hi = max(x) + b02
    return (lo + hi) / 2, lo, hi
