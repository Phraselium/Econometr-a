"""V8.1 (bloque A, coherencia de V8): ningún entregable V8 ni de publicacion/ usa un id de cifras_superadas.csv ni cita cifras superadas;
las cifras previas a V8 no cambian; las cifras nuevas de V8.1 salen de hechos.json y entran en los entregables por marcador."""
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "tests"))
MARC = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([a-z_]+))?\}\}")
PERMITIDO = re.compile(r"hist[oó]ric|ERRATA|antes|publicado en|sustituid|retirad|superad", re.I)


def _superadas() -> pd.DataFrame:
    return pd.read_csv(RAIZ / "output" / "v5" / "cifras_superadas.csv")


def _entregables_v8() -> list[Path]:
    fs = [p for p in (RAIZ / "output" / "v8").glob("*.md")]
    fs += [RAIZ / "output" / "v8" / "fichas_verificador_v8.json"]
    fs += [p for p in (RAIZ / "docs" / "v8" / "plantillas").rglob("*.md") if p.name != "README.md"]
    fs += [p for p in (RAIZ / "publicacion").rglob("*.md") if p.name != "MANIFIESTO.md"]
    fs += [RAIZ / "output" / "v5" / n for n in ("una_pagina.md", "lo_que_sabemos.md", "que_cambio.md")]
    fs += [RAIZ / "docs" / "v5" / "plantillas" / n for n in ("una_pagina.md", "lo_que_sabemos.md", "que_cambio.md")]
    fs += [RAIZ / "README.md", RAIZ / "LEEME_PRIMERO.md"]
    return [f for f in fs if f.exists()]


def test_ningun_id_superado_en_marcadores_ni_fichas():
    sup = set(_superadas().id)
    malas = []
    for f in _entregables_v8():
        t = f.read_text(encoding="utf-8")
        for n, ln in enumerate(t.splitlines(), 1):
            if PERMITIDO.search(ln):
                continue
            for m in MARC.finditer(ln):
                if m.group(1) in sup:
                    malas.append(f"{f.relative_to(RAIZ)}:{n}: {{{{{m.group(1)}}}}}")
    fv = (RAIZ / "output" / "v8" / "fichas_verificador_v8.json").read_text(encoding="utf-8")
    malas += [f"fichas_verificador_v8.json: id superado {i}" for i in sup if re.search(r'"' + re.escape(i) + r'"', fv)]
    assert not malas, "ids superados en entregables V8 o de publicacion/: " + "; ".join(malas[:15])


def test_ninguna_cifra_superada_citada():
    """Textos literales de ERRATA (test_l5_cifras) y valores formateados de cada cifra de cifras_superadas.csv (rango o valor de 7 o más caracteres)."""
    import test_l5_cifras as L5
    import render_v8 as RV
    formas = {}
    for r in _superadas().itertuples():
        s = pd.Series({k: getattr(r, k) for k in ("id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato")})
        for campo in ("rango", "valor"):
            x = RV.texto(s, campo)
            if len(x) >= 7 and any(ch.isdigit() for ch in x):
                formas[x] = r.id
    malas = []
    for f in _entregables_v8():
        if f.name == "cifras_clave.md":
            continue
        for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if PERMITIDO.search(ln):
                continue
            for v in L5.SUPERADOS:
                if v in ln:
                    malas.append(f"{f.relative_to(RAIZ)}:{n}: {v}")
            for x, i in formas.items():
                if x in ln:
                    malas.append(f"{f.relative_to(RAIZ)}:{n}: {x} ({i})")
    assert not malas, "cifras superadas citadas: " + "; ".join(malas[:15])


def test_publicacion_sin_ids_superados_en_tabla():
    sup = set(_superadas().id)
    for f in (RAIZ / "output" / "v5" / "cifras_clave.csv", RAIZ / "publicacion" / "cifras_clave.csv"):
        assert not set(pd.read_csv(f).id) & sup, f.name


def test_contratos_nuevos_c1_vigentes_y_citados():
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    sup = set(_superadas().id)
    for i in ("A23-A9", "A23-A10"):
        assert i in ck.index and i not in sup and ck.at[i, "capa"] == "C1", i
        for f in ("por_que_ha_subido.md", "informe_econometrico.md"):
            t = (RAIZ / "docs" / "v8" / "plantillas" / f).read_text(encoding="utf-8")
            assert "{{" + i + ":cita}}" in t, (i, f)


def test_cifras_previas_a_v8_identicas():
    import check_v8
    assert check_v8.cifras_previas() == []


def test_ids_nuevos_v81_en_cifras_clave_y_en_publicacion():
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv")
    pub = pd.read_csv(RAIZ / "publicacion" / "cifras_clave.csv")
    nuevos = ck[ck.id.str.match(r"V8-(M7-var-|M6-(vif|colpob)|M0-(no-evaluable|evaluables))")]
    assert nuevos.id.str.startswith("V8-M7-var-").sum() >= 39
    assert set(nuevos.id) <= set(pub.id)
    assert (nuevos.capa == "C4").all()
    assert nuevos.origen.str.startswith("output/v8/F6/hechos.json").all()


def test_lectura_por_variable_distinta_de_la_de_familias():
    t = (RAIZ / "output" / "v8" / "por_que_ha_subido.md").read_text(encoding="utf-8")
    assert "Lectura por variables del multiverso" in t and "no evaluable" in t and "colinealidad" in t
    d = pd.read_csv(RAIZ / "output" / "v8" / "M7" / "resumen_multiverso.csv")
    v = d[(d.variable != "TODAS") & (d.cumple_multiverso == True)]  # noqa: E712
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    assert ck.at["V8-M7-var-cumplen", "valor"] == len(v)
    for r in v.itertuples():
        k = f"V8-M7-var-{r.mercado[0]}-{r.periodo}-{r.variable}"
        assert abs(ck.at[k + "-signo", "valor"] - 100 * r.pct_mismo_signo) < 1e-6
        assert abs(ck.at[k + "-bh", "valor"] - 100 * r.pct_sig_bh) < 1e-6
