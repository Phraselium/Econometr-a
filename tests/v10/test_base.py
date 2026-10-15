"""V10-B1: tests de la base única (data/base). La capa pública está versionada; la tabla completa (con filas no
redistribuibles) solo existe tras `make base` y sus tests se saltan si no está en disco."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
BASE = RAIZ / "data" / "base"
CLAVE = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion"]


def _pq(rel: str) -> pd.DataFrame:
    ruta = BASE / rel
    if not ruta.exists():
        pytest.skip(f"{rel} no está en disco (ejecutar `make base`)")
    return pd.read_parquet(ruta)


@pytest.fixture(scope="module")
def pub() -> pd.DataFrame:
    return _pq("publica/hechos.parquet")


@pytest.fixture(scope="module")
def terr() -> pd.DataFrame:
    return _pq("publica/territorios.parquet")


def test_claves_unicas(pub):
    assert not pub.duplicated(CLAVE).any()


def test_codigos_ine_validos(pub, terr):
    assert not terr.duplicated(["territorio_codigo", "nivel"]).any()
    largo = {"nacional": 2, "ccaa": 2, "provincia": 2, "municipio": 5, "distrito": 7, "barrio": 9, "seccion": 10}
    for nivel, n in largo.items():
        x = pub[pub.nivel == nivel].territorio_codigo
        assert x.str.fullmatch(rf"\d{{{n}}}").all(), nivel
        if nivel in ("ccaa", "provincia", "municipio", "seccion"):
            validos = set(terr.loc[terr.nivel == nivel, "territorio_codigo"])
            fuera = set(x) - validos
            # municipios suprimidos o fusionados antes de 2026 aparecen en series largas: se toleran solo si existen
            # en el seccionado o en la relación de municipios (no deben ser más del 0,5 %)
            assert len(fuera) <= max(1, 0.005 * len(set(x))), (nivel, sorted(fuera)[:10])
    # jerarquía: todo padre existe
    pares = set(zip(terr.territorio_codigo, terr.nivel))
    hijos = terr[terr.padre_codigo != ""]
    assert all((p, n) in pares for p, n in zip(hijos.padre_codigo, hijos.padre_nivel))


def test_sumas_territoriales_censo(pub):
    c = pub[(pub.variable == "pob_censo_anual") & (pub.desagregacion == "nacionalidad=Total")]
    sec = c[c.nivel == "seccion"].assign(mun=lambda d: d.territorio_codigo.str[:5]).groupby(["periodo", "mun"]).valor.sum()
    mun = c[c.nivel == "municipio"].set_index(["periodo", "territorio_codigo"]).valor
    assert (sec - mun.reindex(sec.index)).abs().max() == 0
    prov = c[c.nivel == "provincia"].groupby("periodo").valor.sum()
    assert prov["2025"] == 49128297 and prov["2021"] == 47400798   # total nacional publicado (INE 68065)


def test_posterior_prereg_marcado(pub):
    f = pd.to_datetime(pub.fecha_dato)
    # toda fila cuyo periodo termina después del 2026-09-30 empieza en 2026T3 o después y está marcada
    assert pub.loc[f > "2026-09-30", "posterior_prereg"].all()
    assert not pub.loc[f < "2026-07-01", "posterior_prereg"].any()
    # las series que evalúan evaluate_v7/v8 (precios y alquileres de los paneles) no tienen filas sin marca desde 2026T3
    evaluadas = pub[pub.variable.isin(["ipv", "p_tasado", "ipc_alquiler", "valor_tasado", "ipc_alquiler_indice"])]
    ini = evaluadas.periodo.str.replace("T", "Q")
    assert not ((ini >= "2026Q3") & ~evaluadas.posterior_prereg & (evaluadas.frecuencia == "T")).any()


def test_publica_solo_redistribuible(pub):
    assert pub.redistribuible.all()
    assert not pub.variable.str.match(r"^(registr|notariado|jk_|incasol_)").any()
    assert not pub.fuente.str.contains("Registradores|Notariado|Jaroci|Incasòl", case=False).any()
    v = _pq("publica/variables.parquet")
    assert v.redistribuible.all()


def test_capa_fuente_fecha_en_cada_fila(pub):
    assert pub.capa.isin(["C1", "C2", "C3", "C3s", "C4"]).all()
    assert pub.fuente.fillna("").str.len().gt(0).all() and pub.fecha_dato.notna().all()


def test_cifras_clave_identicas_desde_la_base():
    csv = pd.read_csv(RAIZ / "publicacion/cifras_clave.csv", dtype=str, keep_default_na=False)
    for rel in ("cifras_clave.parquet", "publica/cifras_clave.parquet"):
        b = _pq(rel)
        pd.testing.assert_frame_equal(csv.reset_index(drop=True), b.reset_index(drop=True), check_dtype=False)


def test_duckdb_coincide_con_parquet():
    db = BASE / "vivienda.duckdb"
    if not db.exists():
        pytest.skip("vivienda.duckdb no está en disco (ejecutar `make base`)")
    import duckdb
    con = duckdb.connect(str(db), read_only=True)
    n_pub = con.execute("select count(*) from hechos_publica").fetchone()[0]
    cif = con.execute("select * from cifras_clave").df()
    con.close()
    import pyarrow.parquet as papq   # nº de filas desde los metadatos: no carga una segunda copia en memoria (V11: 14 M filas)
    assert n_pub == papq.ParquetFile(BASE / "publica/hechos.parquet").metadata.num_rows
    csv = pd.read_csv(RAIZ / "publicacion/cifras_clave.csv", dtype=str, keep_default_na=False)
    assert cif.astype(str).equals(csv.astype(str))


def test_correspondencia_seccion_barrio_suma_uno():
    c = pd.read_csv(BASE / "geo/correspondencia_seccion_barrio_valencia.csv", dtype={"cod_seccion": str, "cod_barrio": str})
    s = c.groupby("cod_seccion").peso_area.sum()
    assert ((s - 1).abs() < 1e-4).all() and c.cod_seccion.str.startswith("46250").all()
