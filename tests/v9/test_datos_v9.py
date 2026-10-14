"""V9-DATOS: validación de data/raw/v9 (existencia o descarga con `make datos_v9`, checksums, claves territoriales,
sumas de control y duplicados). Los ficheros no versionados (licencia o tamaño) se comprueban solo si están en disco."""
from __future__ import annotations

import csv
import gzip
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
RAW9 = RAIZ / "data" / "raw" / "v9"
sys.path.insert(0, str(RAIZ / "src" / "v9"))
import comun  # noqa: E402


def _manifiesto() -> list[dict]:
    filas = []
    for m in sorted(RAW9.glob("*/_manifest.csv")):
        with open(m, encoding="utf-8") as f:
            filas += list(csv.DictReader(f))
    return filas


def _leer(rel: str, **kw) -> pd.DataFrame:
    ruta = RAW9 / rel
    if not ruta.exists():
        pytest.skip(f"{rel} no está en disco (ejecutar `make datos_v9`)")
    return pd.read_csv(ruta, dtype=str, **kw)


def test_manifiesto_completo_y_scripts():
    filas = _manifiesto()
    assert len(filas) >= 30
    fuentes = {r["fuente"] for r in filas}
    for f in fuentes:
        assert (RAIZ / "src" / "v9" / f"fetch_{f}.py").exists(), f
    for r in filas:
        assert r["sha256"] and re.fullmatch(r"[0-9a-f]{64}", r["sha256"]), r["fichero"]
        assert r["licencia"] and r["redistribuible"] in ("sí", "no"), r["fichero"]


def test_checksums_de_lo_que_esta_en_disco():
    malos = [r["fichero"] for r in _manifiesto()
             if (RAIZ / r["fichero"]).exists() and comun.sha256(RAIZ / r["fichero"]) != r["sha256"]]
    assert not malos, malos


def test_versionados_existen():
    """Todo fichero versionado de data/raw/v9 figura en algún manifiesto (nada sin registrar)."""
    import subprocess
    vers = subprocess.run(["git", "ls-files", "data/raw/v9"], cwd=RAIZ, capture_output=True, text=True).stdout.split()
    registrados = {r["fichero"] for r in _manifiesto()}
    sueltos = [v for v in vers if not v.endswith(("_manifest.csv", ".md", ".geojson")) and v not in registrados
               and "/correspondencia" not in v and "/original" not in v]
    assert not sueltos, sueltos


def test_censo_claves_y_sumas():
    d = _leer("ine_censo_anual/censo_seccion_pais.csv.gz")
    assert not d.duplicated(["edicion", "cod_provincia", "cod_municipio", "cod_seccion", "nivel", "pais_nacionalidad"]).any()
    sec = d[d.nivel == "seccion"]
    assert sec.cod_seccion.str.fullmatch(r"\d{10}").all() and (sec.cod_seccion.str[:5] == sec.cod_municipio).all()
    d["poblacion"] = pd.to_numeric(d.poblacion)
    tot = d[(d.nivel == "provincia") & (d.pais_nacionalidad == "Total")].groupby("edicion").poblacion.sum()
    # Cifras publicadas por el INE (Censo anual, tabla 68065, Total Nacional)
    publicado = {"2021": 47400798, "2022": 47486727, "2023": 48085361, "2024": 48619695, "2025": 49128297}
    for e, v in publicado.items():
        assert tot[e] == v, e
    s = d[(d.nivel == "seccion") & (d.pais_nacionalidad == "Total")].groupby(["edicion", "cod_municipio"]).poblacion.sum()
    m = d[(d.nivel == "municipio") & (d.pais_nacionalidad == "Total")].set_index(["edicion", "cod_municipio"]).poblacion
    assert (s - m.reindex(s.index)).abs().max() == 0


def test_emal_claves_y_cuadre():
    d = _leer("emal/emal_largo.csv")
    assert not d.duplicated(["libro", "hoja", "grupo", "codigo_ine", "nombre", "periodo"]).any()
    cod = d.codigo_ine.dropna()
    assert cod.str.fullmatch(r"\d{5}").all()
    t = d[(d.hoja == "T2.1") & d.libro.str.startswith("EMAL-2016") & ~d.periodo.str.startswith("vig")].copy()
    t["v"] = pd.to_numeric(t.valor)
    eus = t[t.nombre == "Euskadi"].set_index("periodo").v
    th = t[t.nombre.isin(["Álava", "Gipuzkoa", "Bizkaia"])].groupby("periodo").v.sum()
    assert len(eus) >= 10 and (eus - th.reindex(eus.index)).abs().max() == 0


def test_gva_vut_panel():
    d = _leer("gva_vut/gva_vut_panel_municipio.csv")
    assert d.ine5.str.fullmatch(r"\d{5}").all() and not d.duplicated(["ine5", "tipo", "fecha"]).any()
    m = pd.read_excel(RAIZ / "data/raw/ine_diccionario_municipios_2026.xlsx", dtype=str, header=1)
    validos = set(m.CPRO + m.CMUN) | {"03000"}   # 03000: registros sin municipio asignado (docs/v9/decisiones_datos.md, D2)
    assert d.ine5.isin(validos).all()
    d["stock"] = pd.to_numeric(d.stock)
    ult = d[(d.tipo == "corte") & (d.fecha == d[d.tipo == "corte"].fecha.max())]
    assert ult.stock.sum() > 50000 and ult[ult.ine5 == "03000"].stock.sum() == 0


def test_insideairbnb_seccion():
    d = _leer("insideairbnb/insideairbnb_seccion.csv.gz")
    col = next(c for c in d.columns if "secc" in c.lower() or c.upper() == "CUSEC")
    assert d[col].str.fullmatch(r"\d{10}").all()
    claves = [c for c in d.columns if c in ("ciudad", "edicion", col)]
    assert not d.duplicated(claves).any()


def test_ipva_y_fianzas():
    for rel in ("ine_ipva/ipva_ccaa_antiguedad.csv", "ine_ipva/ipva_provincia_antiguedad.csv"):
        d = _leer(rel)
        assert not d.duplicated().any()
    c = _leer("gva_fianzas/comparacion_v5.csv")
    assert (c.igual == "sí").all(), "las fianzas GVA difieren de la copia v5: revisar antes de usar"


def test_series_de_precios_marcan_posterior_prereg():
    for rel in ("incasol/incasol_qww9-bvhh_actual.csv.gz",):
        ruta = RAW9 / rel
        if not ruta.exists():
            continue
        with gzip.open(ruta, "rt", encoding="utf-8") as f:
            cab = f.readline()
        assert "posterior_prereg" in cab, rel


def test_insideairbnb_cuadre_con_publicado():
    """Filas de listings frente al recuento de visualisations/listings.csv publicado por Inside Airbnb (diferencia ≤1 %)."""
    v = _leer("insideairbnb/validacion_insideairbnb.csv")
    num = [c for c in v.columns if v[c].str.fullmatch(r"\d+").all()]
    assert len(num) >= 2
    a, b = pd.to_numeric(v[num[0]]), pd.to_numeric(v[num[1]])
    assert ((a - b).abs() / b).max() <= 0.01


def test_eurostat_y_bce_sin_duplicados():
    e = _leer("eurostat_plataformas/tour_ce_oan3.csv.gz")
    assert not e.duplicated(["dataset", "geo", "periodo", "indicador"]).any() and e.geo.str.startswith("ES").any()
    b = _leer("bce_hipotecas/bce_mir_vivienda_zona_euro.csv.gz")
    assert not b.duplicated(["pais", "fijacion_codigo", "periodo"]).any()
    assert {"F", "I", "O", "P", "A_volumen"} <= set(b.fijacion_codigo) and "ES" in set(b.pais)
