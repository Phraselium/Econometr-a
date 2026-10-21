"""V18 · fase 6: cifras V18 consolidadas (f6_hechos), Documento de Trabajo (f6_documento) y control de lenguaje causal de check_v18."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import check_v18  # noqa: E402
import f6_documento as D  # noqa: E402
import f6_hechos as H  # noqa: E402


def test_tipo_rango():
    assert H.tipo_rango({"valor": 1.0, "min": 0.5, "max": 2.0}) == "rango"
    assert H.tipo_rango({"valor": None, "min": -1.0, "max": 2.0}) == "rango"
    assert H.tipo_rango({"valor": 3.0, "min": 0.5, "max": 2.0}) == "referencias"
    assert H.tipo_rango({"valor": 1.0, "min": None, "max": 2.0}) == "sin rango"


def test_cobertura_real():
    assert H.cobertura_real({"id": "V18-E5-R1-F-2002-2007", "cobertura": "N = 234"}, {}) == "España (provincias) (N = 234)"
    assert H.cobertura_real({"id": "V18-E1-A4", "cobertura": "sin datos"}, {}).startswith("ciudades españolas")
    assert H.cobertura_real({"id": "V18-F4-1", "cobertura": "—"}, {}) == "España (no estimada)"
    assert H.cobertura_real({"id": "V18-C5I-x", "cobertura": "Andalucía; "}, {}) == "Andalucía"
    assert H.cobertura_real({"id": "V18-B5-E4", "cobertura": "2 estudios"}, {"E4": "Francia, Finlandia"}).startswith("estudios de Francia")


def test_consolidado_al_dia_y_valido():
    filas, err = H.consolidar()
    assert err == []
    assert len(filas) == H.N_ESPERADO and len({h["id"] for h in filas}) == len(filas)
    assert json.loads(H.SALIDA.read_text(encoding="utf-8")) == filas, "output/v18/f6/hechos.json desactualizado: python3 src/v18/f6_hechos.py"
    for h in filas:
        assert h["capa"] == "C4" and h["clasificacion_v18"] in check_v18.CLASES and h["tipo_rango"] in H.TIPOS_RANGO
        assert h["cobertura"] and not h["cobertura"].endswith(";")


def test_auxiliares_copian_su_origen():
    aux = {h["id"]: h for h in H.auxiliares()}
    assert len(aux) == H.N_AUX and all(i.startswith("V18-AUX-") for i in aux)
    for h in aux.values():
        assert h["capa"] == "C4" and h["fuentes"] and h["clasificacion_v18"] in check_v18.CLASES
        assert any(h.get(k) is not None for k in ("valor", "min", "max")), f"{h['id']}: recuento o cifra sin valor"
        assert not check_v18.CAUSAL.search(f"{h['indicador']} {h['nota']}")
    e2 = pd.read_csv(H.OUT / "estimacion" / "e2" / "tabla.csv").set_index("id").loc["E2-R1", "coef"]
    assert aux["V18-AUX-E2-R1-PCT"]["valor"] == pytest.approx(100 * (2.718281828459045 ** e2 - 1), abs=1e-6)
    assert aux["V18-AUX-E2-R1-EV-2021T1"]["valor"] == pytest.approx(-0.057798)
    assert aux["V18-AUX-CAT-FICHAS"]["valor"] == len(pd.read_csv(H.OUT / "f1" / "catalogo.csv"))
    assert aux["V18-AUX-LIT-GL2020-BARRIO-MEDIO"]["valor"] == pytest.approx(1.9)
    assert not any(i.startswith("V18-AUX-D3-") and i.endswith(("2015-2025", "2015-2024")) for i in aux)   # ya son V17-D3-*


def test_min_sig_max_sig():
    ck = _ck()
    txt, falta = D.render_texto("{{V18-B5-E1:min_sig}} a {{V18-B5-E1:max_sig}}", ck, pd.read_csv(D.MAG))
    assert falta == [] and txt == "0,1 a 0,9"


def _ck() -> pd.DataFrame:
    filas = [dict(id=f"V18-B5-E{k}", indicador=f"Magnitud preferida de factor {k} (E{k}): unidad", valor=0.5 if k == 1 else None, min=0.1,
                  max=0.9, unidad="u", periodo="2024", cobertura="España", fuentes="x", capa="C4", fecha_dato="2024", ficha="—",
                  origen=f"output/v18/f6/hechos.json:V18-B5-E{k}", sentido_min_max="rango", tipo_rango="rango",
                  clasificacion_v18="NO ESTIMABLE") for k in range(1, 10)]
    return pd.DataFrame(filas).set_index("id")


def test_render_resuelve_y_falla_si_falta():
    ck, mag = _ck(), pd.read_csv(D.MAG)
    txt, falta = D.render_texto("A {{V18-B5-E1:valor}} ({{V18-B5-E1:clasificacion}})\n\n{{tabla.impactos}}", ck, mag)
    assert falta == [] and "NO ESTIMABLE" in txt and "| Factor | Magnitud preferida |" in txt and "{{" not in txt
    _, falta = D.render_texto("{{V18-NO-EXISTE}} y {{tabla.otra}}", ck, mag)
    assert "V18-NO-EXISTE" in falta and "{{tabla.otra}}" in falta


def test_confianza_regla():
    assert D.confianza("magnitud preferida", 3) == "media"
    assert D.confianza("magnitud preferida", 2) == "baja"
    assert D.confianza("rango de la literatura, sin error típico", 0) == "muy baja"


@pytest.mark.parametrize("texto,errores", [
    ("## Resumen ejecutivo\nEl diseño identifica el efecto.\n", 1),
    ("## Resumen ejecutivo\nNo es causal.\n", 1),                       # en los resúmenes, nada
    ("## 4. Resultados por factor\nCon los supuestos X, el diseño identifica el efecto.\n", 0),
    ("## Anexo D. Pruebas\nEfecto causal del tope.\n", 0),
    ("## 7. Limitaciones\nEl diseño no permite una lectura causal.\n", 0),  # negación fuera de los resúmenes
    ("## 6. Implicaciones\nLa subida se debe a la demanda.\n", 1),
    ("## Abstract\nPrices rose due to demand.\n", 1),
])
def test_lenguaje_causal_por_seccion(texto, errores):
    assert len(check_v18.texto_causal(texto, "x")) == errores
