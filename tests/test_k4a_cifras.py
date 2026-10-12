"""K4a: integridad de output/v5/cifras_clave.csv y de su cadena (hechos.json -> cifras_clave -> entregables). Sin red."""
from __future__ import annotations

import glob
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"

# Filas cuyo «min»/«max» NO son el rango del valor (valor crítico, mediana UE, extremo de distritos, etc.). Documentado en
# docs/v6_1/auditoria_K4a.md (K4a-06). Cualquier otra fila con valor fuera de [min, max] es un error.
RANGO_OTRO_SENTIDO = ("CA-EU-", "R1B-G-", "R1B-S-", "m2_pip_", "E-E1-VLC-contratos", "T1-H1", "T3-H8", "CC-C7b-jov-",
                      "CA-CT-ratio-triang-")
# Filas con unidad «%» que son variaciones o log-puntos (pueden ser negativas)
PCT_CAMBIO = ("CA-CR-", "E-v3-H3-", "V7-R6-", "V71-S3-R6-")   # v7.1: variaciones % de escenarios R6 (pueden ser negativas)


@pytest.fixture(scope="module")
def ck() -> pd.DataFrame:
    return pd.read_csv(CK)


def test_ids_unicos(ck):
    assert not ck.id.duplicated().any(), ck.id[ck.id.duplicated()].tolist()
    assert ck.origen.is_unique


def test_campos_obligatorios(ck):
    for c in ("indicador", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato"):
        assert ck[c].notna().all(), c
    assert set(ck.capa.astype(str)) <= {"C1", "C2", "C3", "C4"}
    assert ck[["valor", "min", "max"]].notna().any(axis=1).all()


def test_valores_finitos(ck):
    for c in ("valor", "min", "max"):
        x = ck[c].dropna()
        assert x.map(math.isfinite).all(), c


def test_min_valor_max(ck):
    assert set(ck[ck.id.str.startswith(RANGO_OTRO_SENTIDO)].sentido_min_max) - {"rango"}, "las filas de otro sentido deben declararlo"
    assert (ck[~ck.id.str.startswith(RANGO_OTRO_SENTIDO)].sentido_min_max == "rango").all()
    ok = ck[ck.sentido_min_max == "rango"]
    ok = ok[ok.valor.notna() & ok["min"].notna() & ok["max"].notna()]
    mal = ok[(ok.valor < ok["min"] - 1e-9 * ok.valor.abs().clip(lower=1)) | (ok.valor > ok["max"] + 1e-9 * ok.valor.abs().clip(lower=1))]
    assert mal.empty, mal[["id", "valor", "min", "max"]].to_string()
    # min <= max siempre, salvo las filas documentadas
    r = ck[(ck.sentido_min_max == "rango") & ck["min"].notna() & ck["max"].notna()]
    assert (r["min"] <= r["max"]).all(), r[r["min"] > r["max"]].id.tolist()


def test_porcentajes_en_rango(ck):
    p = ck[(ck.unidad == "%") & ck.valor.notna()]
    assert (p.valor <= 100).all(), p[p.valor > 100].id.tolist()
    neg = p[(p.valor < 0) & ~p.id.str.startswith(PCT_CAMBIO)]
    assert neg.empty, neg.id.tolist()


def test_precios_positivos(ck):
    # niveles de precio/renta; se excluyen los efectos estimados de v6 (pueden ser negativos)
    pr = ck[ck.unidad.isin(["EUR/m2", "€/m²", "€/m²/mes"]) & ~ck.id.str.match(r"^(m[0-9][a-z]?_|E-V6)")]
    for c in ("valor", "min", "max"):
        assert (pr[c].dropna() > 0).all(), (c, pr[pr[c] <= 0].id.tolist())


def test_recuentos_sin_perdida_de_cifras(ck):
    """K4a-01: float_format %.6g redondeaba los recuentos >= 1e6 (1.720.537 -> 1.720.540)."""
    fila = ck.set_index("id")
    assert fila.loc["B1-H4", "valor"] == 1720537
    assert fila.loc["B2-H3", "valor"] == 1024156


def test_hechos_json_igual_a_cifras_clave(ck):
    idx = ck.set_index("origen")
    n = 0
    for p in sorted(glob.glob(str(RAIZ / "output" / "v5" / "*" / "hechos.json")) + glob.glob(str(RAIZ / "output" / "v5_1" / "*" / "hechos.json"))
                    + glob.glob(str(RAIZ / "output" / "v6" / "*" / "hechos.json"))):
        h = json.loads(Path(p).read_text())
        if not isinstance(h, list):
            continue
        rel = str(Path(p).relative_to(RAIZ))
        for x in h:
            o = f"{rel}:{x.get('id')}"
            vals = {k: x.get(k) for k in ("valor", "min", "max")}
            hay = any(isinstance(v, (int, float)) and math.isfinite(v) for v in vals.values())
            if not hay:
                continue
            assert o in idx.index, f"falta en cifras_clave: {o}"
            for k, v in vals.items():
                b = idx.loc[o, k]
                if isinstance(v, (int, float)) and math.isfinite(v):
                    assert abs(float(v) - b) <= 1e-8 * max(1.0, abs(v)), (o, k, v, b)
                else:
                    assert pd.isna(b), (o, k, v, b)
            n += 1
    assert n > 400


def test_entregables_renderizados_igual_a_cifras_clave(ck):
    import render
    ckx = ck.set_index("id")
    for p in sorted(render.PLANT.glob("**/*.md")):
        txt, falta = render.render(p, ckx)
        assert not falta, (p.name, falta)
        dest = render.OUT / p.relative_to(render.PLANT)
        assert dest.read_text() == txt, f"{dest.relative_to(RAIZ)} desactualizado respecto de cifras_clave.csv"


def test_control_sumas_suma_provincial_igual_nacional():
    n = 0
    for f in glob.glob(str(RAIZ / "output" / "v5*" / "*" / "control_sumas.json")):
        d = json.loads(Path(f).read_text())
        for x in (d if isinstance(d, list) else [d]):
            s, nac, tol = x["suma_provincial"], x["nacional"], x.get("tolerancia_rel", 1e-6)
            assert abs(s - nac) <= tol * max(abs(nac), 1e-9) + 1e-9, (f, x["tabla"], s, nac)
            n += 1
    assert n > 50
