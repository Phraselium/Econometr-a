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


def test_clases_k12_en_check_v18():
    """K12: tres valores para cifras sin clase propia, aceptados por check_v18 y por f6_hechos."""
    assert {check_v18.SIN_CLASIFICAR, check_v18.ROBUSTEZ_POSTERIORI, check_v18.DIAGNOSTICO} <= check_v18.CLASES
    assert check_v18.SIN_CLASIFICAR == "sin clasificar (coprincipal informativa)"
    assert check_v18.ROBUSTEZ_POSTERIORI == "robustez a posteriori"
    assert not [e for e in check_v18.cifras() if "clasificacion_v18" in e]


def test_clase_propia_por_especificacion():
    nc = {"V18-E1-P-H3", "V18-E10-A1-v1"}
    h = {"id": "V18-E1-P-H3", "valor": -6.5e-05, "clasificacion_v18": "SUGESTIVO"}
    assert H.clase_propia(h, nc)[0] == check_v18.SIN_CLASIFICAR
    assert H.clase_propia({"id": "V18-E10-A1-v1", "valor": 2.7, "clasificacion_v18": "ASOCIACIÓN"}, nc)[0] == check_v18.DIAGNOSTICO
    assert H.clase_propia({"id": "V18-E2-B6-C", "valor": -0.05, "clasificacion_v18": "SUGESTIVO"}, nc)[0] == check_v18.ROBUSTEZ_POSTERIORI
    assert H.clase_propia({"id": "V18-E2-R1-REV", "valor": -0.0016, "clasificacion_v18": "SUGESTIVO"}, nc)[0] == check_v18.DIAGNOSTICO
    assert H.clase_propia({"id": "V18-E2-R1", "valor": -0.038, "clasificacion_v18": "SUGESTIVO"}, nc) == ("SUGESTIVO", "")


def test_solo_e2_r1_es_sugestivo_y_e1_p_h3_sin_clasificar():
    """Árbitro, hallazgo 2: la única estimación designada SUGESTIVO es E2-R1; sus robusteces y diagnósticos no heredan la clase."""
    filas = {h["id"]: h for h in json.loads(H.SALIDA.read_text(encoding="utf-8"))}
    con_cifra = {i for i, h in filas.items() if any(h.get(k) is not None for k in ("valor", "min", "max"))}
    assert {i for i in con_cifra if filas[i]["clasificacion_v18"] == "SUGESTIVO"} == H.SUGESTIVO_PERMITIDO
    assert filas["V18-E1-P-H3"]["clasificacion_v18"] == check_v18.SIN_CLASIFICAR
    assert filas["V18-B5-E8"]["clasificacion_v18"] == "ASOCIACIÓN"            # hallazgo 3: clase de la designada (E8-R1)
    assert all(filas[i]["clasificacion_v18"] == check_v18.ROBUSTEZ_POSTERIORI for i in con_cifra if "-B6-" in i or i.endswith("-B6B2"))
    assert "1983-2024" not in filas["V18-B5-E8"]["periodo"]                     # hallazgo 18: periodo de los estudios del factor
    assert filas["V18-C5-1995T1-2007T4-00-NOEXPL-A"]["periodo"] == "2002T1-2007T4"   # hallazgo 1: periodo real del dato
    assert filas["V18-C5-1995T1-2007T4-09-NOEXPL-P"]["periodo"] == "2002T1-2007T4"
    assert "relativa a la media de las provincias no selladas" in filas["V18-C5-2014T1-2019T4-09-NOEXPL-P"]["indicador"]


def test_auxiliares_k12():
    aux = {h["id"]: h for h in H.auxiliares()}
    assert aux["V18-AUX-E2-R1-B6B2"]["max"] == pytest.approx(-0.001246, abs=1e-6)     # −0,001 a 3 decimales (errata de ronda 2)
    assert aux["V18-AUX-E2-R1-HONEST-M05"]["min"] == pytest.approx(-0.08705, abs=1e-4)
    assert aux["V18-AUX-E2-R1-ROTH-SESGO"]["valor"] == pytest.approx(0.0606, abs=1e-4)
    assert aux["V18-AUX-E2-R1-MULTIVERSO"]["min"] < aux["V18-AUX-E2-R1-MULTIVERSO"]["max"] < 0
    assert aux["V18-AUX-F1-OOS-RMSE-ECM"]["valor"] > aux["V18-AUX-F1-OOS-RMSE-AR4"]["valor"]   # F1 no predice mejor que el AR(4)
    assert aux["V18-AUX-CRIT-ADENDA-TAM"]["min"] == 0.04 and aux["V18-AUX-CRIT-HHI-E9"]["valor"] == 10
    assert aux["V18-AUX-CONT-PROV-PRECIO-1995T1-2007T4"]["periodo"] == "2002T1-2007T4"


def test_campos_propios_del_documento():
    """K12: «sig» sin notación científica; 3 y 1 decimales; valor absoluto; punto decimal en inglés."""
    assert D._sig(-6.5e-05) == "−0,000065" and D._sig(-0.038434) == "−0,0384" and D._sig(0.0874, en=True) == "0.0874"
    ck = _ck()
    ck.loc["V18-B5-E1", ["valor", "min", "max"]] = [-0.038434, -0.050944, -0.00125]
    txt, falta = D.render_texto("{{V18-B5-E1:tres_dec}} ({{V18-B5-E1:min_tres_dec}} a {{V18-B5-E1:max_tres_dec}}); "
                                "{{V18-B5-E1:tres_dec_en}}; {{V18-B5-E1:abs_un_dec}}; {{V18-B5-E1:min_sig_en}}", ck, pd.read_csv(D.MAG))
    assert falta == [] and txt == "−0,038 (−0,051 a −0,001); −0.038; 0,0; −0.0509"


def test_tabla_impactos_no_llama_ic95_al_efecto_fijo_con_dos_estudios():
    ck = _ck()
    ck.loc["V18-B5-E4", "valor"] = 0.04
    t, falta = D.tabla_impactos(ck, pd.read_csv(D.MAG))
    fila_e4 = next(x for x in t.splitlines() if "(E4)" in x)
    assert falta == [] and "no es un IC95 fiable" in fila_e4


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
