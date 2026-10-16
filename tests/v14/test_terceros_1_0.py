"""V14.2-B3 · Un test por valor de terceros_1_0 (agregados, excluir, redistribuir): textos (render), consulta, árbol público y
paquete. Los escenarios se prueban con la variable de entorno VIVIENDA_TERCEROS_1_0, sin tocar proyecto.json."""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
from src.v14 import terceros as T  # noqa: E402
from src.v14 import terceros_1_0 as T10  # noqa: E402

TODAS = lambda v: {f: v for f in T10.FUENTES}  # noqa: E731
ARBOL = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8")).get("arbol_publico", False)   # árbol público: tablas ya redactadas
CA = "output/v5/CA/tablas/contado_ratio_hipotecas_compraventas.csv"
F6 = "output/f6/notariado_provincia_trimestral.csv"
B5 = "output/v12/b5/aeat_cv_declarantes_inmuebles.csv"
M0 = "output/v6/M0/paneles/prov_compra_anual_train.csv.gz"
REG_DIRECTA = "A23-P2"   # precio de compra, núcleo MIVAU/Notariado/Registradores: directa para Notariado y Registradores


def _escenario(monkeypatch, valor):
    monkeypatch.setenv(T10.ENV, json.dumps(TODAS(valor)))
    assert T10.politica() == TODAS(valor)
    return T10.politica()


def _render(tmp_path, ids):
    import pandas as pd
    import render as R
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    p = tmp_path / "plantilla.md"
    p.write_text(" | ".join("{{" + i + "}}" for i in ids), encoding="utf-8")
    txt, falta = R.render(p, ck)
    assert not falta
    return txt.split(" | ")


def test_por_defecto_en_proyecto_json(monkeypatch):
    monkeypatch.delenv(T10.ENV, raising=False)
    assert T10.politica() == T10.POR_DEFECTO == {"registradores": "agregados", "notariado": "agregados", "aeat": "excluir"}
    assert set(T10.retiradas()) == {f"CB-C6-0{i}" for i in range(1, 6)}
    assert (RAIZ / T10.NO_PUBLICADAS).read_text(encoding="utf-8").count("\n") == 1 + 5


def test_agregados(monkeypatch, tmp_path):
    pol = _escenario(monkeypatch, "agregados")
    assert T10.retiradas(pol) == {} and T10.series_brutas(pol) == []
    assert T10.variables_excluidas(pol) == r"^aeat_"
    assert not any(t.startswith("[cifra no publicada") for t in _render(tmp_path, ["CB-C6-01", REG_DIRECTA]))
    if ARBOL:   # en el árbol público la redacción ya está aplicada: las columnas de la serie no están
        assert not {"reg_compraventas_viv", "reg_hipotecas_viv"} & set(T.cabecera(RAIZ / CA))
        assert not {"ln_pm2_registradores", "ln_cv_registradores"} & set(T.cabecera(RAIZ / M0))
    else:
        assert T.accion(CA, RAIZ / CA, pol) == ("redactar", ["reg_compraventas_viv", "reg_hipotecas_viv"])
        assert T.accion(M0, RAIZ / M0, pol) == ("redactar", ["ln_pm2_registradores", "ln_cv_registradores"])
    assert T.accion(F6, RAIZ / F6, pol) == ("vaciar", "notariado")
    assert T.accion(B5, RAIZ / B5, pol) == ("copiar", None)   # agregado propio: se publica citando la fuente
    d = tmp_path / "vacia.csv"
    T.aplicar(F6, RAIZ / F6, d, pol)
    assert d.read_text(encoding="utf-8").count("\n") == 1   # solo la cabecera


def test_excluir(monkeypatch, tmp_path):
    pol = _escenario(monkeypatch, "excluir")
    ret = T10.retiradas(pol)
    assert {"CB-C6-01", REG_DIRECTA} <= set(ret)
    import csv
    deps: dict[str, set] = {}
    for r in csv.DictReader((RAIZ / "docs/v14/cifras_terceros.csv").open(encoding="utf-8")):
        deps.setdefault(r["id"], set()).add(r["dependencia"])
    solo_tecnicas = {i for i, d in deps.items() if all(x.startswith("técnica") for x in d)}
    oficiales = {i for i, d in deps.items() if d == {"indirecta (estadística oficial)"}}
    assert solo_tecnicas and not solo_tecnicas & set(ret)   # una cifra solo técnica nunca se retira
    assert oficiales and not oficiales & set(ret)          # ni una que solo usa una estadística oficial (INE, MIVAU)
    assert all(t.startswith("[cifra no publicada") for t in _render(tmp_path, ["CB-C6-01", REG_DIRECTA]))
    from src.consulta import generar as G
    cifras = G.cargar_cifras()
    assert G.valor_texto(cifras["CB-C6-01"]).startswith("[cifra no publicada")
    H = {h["id"]: h for h in G.construir_hallazgos(cifras, {}) if h["tipo"] == "cifra"}
    assert H["CB-C6-01"]["estado"] == "no publicada (1.0)" and H["CB-C6-01"]["cifra"] is None
    assert T.accion(B5, RAIZ / B5, pol) == ("vaciar", "aeat")
    # cifras_clave no cambia en ningún escenario
    import pandas as pd
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    assert pd.notna(ck.at["CB-C6-01", "valor"])


def test_redistribuir(monkeypatch, tmp_path):
    pol = _escenario(monkeypatch, "redistribuir")
    if ARBOL:
        pytest.skip("árbol público: las series de terceros no están (make datos_terceros); se prueba en el repositorio de desarrollo")
    assert T10.retiradas(pol) == {} and T10.variables_excluidas(pol) is None
    assert "data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz" in T10.series_brutas(pol)
    for rel in (CA, M0, F6, B5):
        assert T.accion(rel, RAIZ / rel, pol) == ("copiar", None), rel
    # CGPJ no tiene escenario: nunca se redistribuye
    cg = "output/v5/CB/tablas/cgpj_lanzamientos_ccaa.csv"
    assert T.accion(cg, RAIZ / cg, pol) == ("vaciar", "cgpj")
    from src.v13 import paquete_zenodo as PZ
    inc, _ = PZ.seleccionar()
    assert "data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz" in inc


def test_valor_invalido(monkeypatch):
    monkeypatch.setenv(T10.ENV, json.dumps({"aeat": "publicar"}))
    with pytest.raises(SystemExit):
        T10.politica()
