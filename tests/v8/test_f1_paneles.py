"""V8-F1: pruebas rápidas de los paneles (claves únicas, códigos INE, 17 CCAA, columnas clave, marcas *_interp, sin cruces por nombre)."""
import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "data" / "processed" / "v8"
CCAA17 = {f"{i:02d}" for i in range(1, 18)}
PROV_VALIDAS = {f"{i:02d}" for i in range(1, 53)}


@pytest.fixture(scope="module", autouse=True)
def construye():
    ficheros = ["nacional_q_v8.csv", "panel_ccaa_q_v8.csv", "cv_prov_q_v8.csv", "cv_prov_a_v8.csv", "valencia_ciudad_v8.csv"]
    if not all((OUT / f).exists() for f in ficheros):
        subprocess.run([sys.executable, str(RAIZ / "src" / "v8" / "f1_paneles.py")], check=True, cwd=RAIZ)


@pytest.fixture(scope="module")
def N():
    return pd.read_csv(OUT / "nacional_q_v8.csv")


@pytest.fixture(scope="module")
def P():
    return pd.read_csv(OUT / "panel_ccaa_q_v8.csv", dtype={"codigo_ine_ccaa": str})


def test_nacional_sin_duplicados_y_rango(N):
    assert not N.duplicated("trimestre").any()
    assert N["trimestre"].iloc[0] == "1995Q1" and N["trimestre"].iloc[-1] == "2026Q2" and len(N) == 126


COLUMNAS_CLAVE = ["p_tasado", "p_bde", "ipv", "ipc_alquiler", "ocupados", "pob_total", "pob_extranj", "hogares_epa", "pib_nom", "rdb", "salario", "tipo_hip_bde",
                  "tipo_hip_bce", "euribor_1y", "euribor_3m", "tipo_dfr", "tipo_mro", "credito_nuevo", "credito_stock_bde", "credito_promotor", "bls_criterios_neto",
                  "jk_mp", "jk_cbi", "hpi_ea19", "hpi_ea20", "bis_hpi_xm_nom", "tx_extranj", "turistas", "visados", "terminadas", "costes_constr", "tx_total",
                  "compraventas_ine", "vut_viviendas", "ipc_general", "deflactor_pib", "ln_p_tasado_real", "d4_ln_p_tasado_real", "tipo_hip_real_bde",
                  "dif_hip_euribor_bde", "covid", "epa2021", "P1", "P2", "P3", "P4", "P5"]


def test_columnas_clave_nacional(N):
    falta = [c for c in COLUMNAS_CLAVE if c not in N.columns]
    assert not falta, falta
    for c in ("p_tasado", "ipc_general", "deflactor_pib", "pob_total", "visados"):
        assert N[c].first_valid_index() == 0, f"{c} debe empezar en 1995T1"


def test_dummies_y_periodos(N):
    i = N.set_index("trimestre")
    assert i.loc["2020Q1", "covid"] == 0 and i.loc["2020Q2", "covid"] == 1 and i.loc["2020Q4", "covid"] == 1 and i.loc["2021Q1", "covid"] == 0
    assert i.loc["2020Q4", "epa2021"] == 0 and i.loc["2021Q1", "epa2021"] == 1
    assert (i[["P1", "P2", "P3", "P4", "P5"]].sum(axis=1) <= 1).all()
    assert i.loc[["2008Q1", "2008Q2", "2020Q1"], ["P1", "P2", "P3", "P4", "P5"]].to_numpy().sum() == 0
    assert i.loc["2007Q4", "P1"] == 1 and i.loc["2008Q3", "P2"] == 1 and i.loc["2022Q3", "P5"] == 1 and i.loc["2026Q2", "P5"] == 1


def test_interp_marcadas_y_sin_extrapolar(N):
    for v in ("pob_total", "pob_extranj", "pob_extranj_ine", "inmig_anual", "visados", "terminadas", "vut_viviendas", "vut_plazas", "ipc_general"):
        assert v + "_interp" in N.columns, v
        f = N[v + "_interp"].astype(bool)
        assert f.any()
        assert N.loc[f, v].notna().all(), f"{v}: valor marcado sin dato"
    for v in ("pob_total", "pob_extranj", "pob_extranj_ine", "vut_viviendas", "vut_plazas"):    # interpolación estricta entre observaciones
        f = N[v + "_interp"].astype(bool)
        obs = N[v].notna() & ~f
        for i in np.flatnonzero(f):
            assert obs[:i].any() and obs[i:].any(), f"{v}: extrapolación en la fila {i}"
    assert N["pob_extranj"].last_valid_index() < len(N) - 1          # el final queda NaN
    # toda columna *_interp tiene su variable base
    for c in N.columns:
        if c.endswith("_interp"):
            assert c[:-7] in N.columns


def test_ccaa_17_codigos_ine_sin_duplicados(P):
    assert set(P["codigo_ine_ccaa"]) == CCAA17
    assert not P.duplicated(["codigo_ine_ccaa", "trimestre"]).any()
    assert (P.groupby("codigo_ine_ccaa").size() == 126).all()
    for c in ("valor_tasado_ccaa", "turistas_ccaa", "salario_ccaa", "tx_extranj_ccaa", "hpi_ea20", "ln_valor_tasado_ccaa"):
        assert c in P.columns
    assert P["valor_tasado_ccaa"].notna().all()                       # 1995T1+ en las 17
    assert P["turistas_ccaa"].notna().groupby(P["codigo_ine_ccaa"]).any().sum() == 6   # FRONTUR publica 6 CCAA
    h = P.groupby("trimestre")["hpi_ea20"].nunique()
    assert (h <= 1).all()                                             # columna común


def test_cv_provincias_codigos_ine():
    q = pd.read_csv(OUT / "cv_prov_q_v8.csv", dtype={"cod_prov": str})
    a = pd.read_csv(OUT / "cv_prov_a_v8.csv", dtype={"cod_prov": str})
    for d, k in ((q, "trimestre"), (a, "anio")):
        assert set(d["cod_prov"]) == {"03", "12", "46"} <= PROV_VALIDAS
        assert not d.duplicated(["cod_prov", k]).any()
    assert "vut_viviendas_interp" in q.columns and "fianzas_parcial" in a.columns
    assert q["valor_tasado"].notna().all()


def test_valencia_codigos_y_unicidad():
    v = pd.read_csv(OUT / "valencia_ciudad_v8.csv", dtype={"codigo_ine": str})
    assert not v.duplicated(["codigo_ine", "variable", "periodo"]).any()
    assert set(v["codigo_ine"]) <= {"46250"} | {f"46250{i:02d}" for i in range(1, 20)}
    assert "fianzas_n" in set(v["variable"]) and "p_tasado" in set(v["variable"])


def test_sin_cruces_por_nombre_en_src_v8():
    spec = importlib.util.spec_from_file_location("cruces", RAIZ / "tests" / "test_v7_cruces.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    malos = [str(p.relative_to(RAIZ)) for p in (RAIZ / "src" / "v8").rglob("*.py") if m.cruces_por_nombre(p, nuevo=True)]
    assert not malos, malos


def test_tasa_paro_epa(N):
    """J8: tasa de paro = parados/(parados+ocupados)x100 desde data/raw, 2002T1-2026T2, coherente con el panel de CCAA."""
    i = N.set_index("trimestre")["tasa_paro_epa"]
    v = i.dropna()
    assert v.index[0] == "2002Q1" and v.index[-1] == "2026Q2" and len(v) == 98
    assert v.between(5, 30).all()
    raw = pd.read_csv(RAIZ / "data" / "raw" / "ine_v2_epa_prov.csv", dtype={"codigo": str})
    r = raw[raw["codigo"] == "00"].pivot_table(index="periodo", columns="medida", values="valor")
    esp = (r["EPA_parados"] / (r["EPA_parados"] + r["EPA_ocupados"]) * 100)
    assert np.allclose(v.to_numpy(), esp.reindex([x.replace("Q", "T") for x in v.index]).to_numpy())
