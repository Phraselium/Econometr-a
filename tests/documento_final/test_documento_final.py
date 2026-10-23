"""Consolidación final: el documento final se genera sin marcadores sueltos, sin lenguaje causal fuera de los anexos y con el juicio
experto rotulado; las cifras V18-AUX-JE-* están en cifras_clave; la muestra de la revisión externa 2.0 es determinista."""
import importlib.util
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def _cargar(nombre: str, ruta: str):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = _cargar("documento_final_t", "src/documento_final/documento_final.py")


def test_ensambla_sin_marcadores_sueltos_y_con_rotulos():
    ck, mag = F.D.leer_ck(F.CK), F.D.pd.read_csv(F.MAG)
    texto, resumen, res = F.ensamblar(ck, mag)
    assert res["marcadores_sin_cifra"] == []
    assert F.comprobar(texto, "documento_final.md") == []
    assert resumen.split("## Resumen ejecutivo", 1)[-1] in texto


def test_lenguaje_causal_detectado_fuera_de_anexos():
    t = "## Parte V. Determinantes\n\nLa subida se debe a los tipos.\n\n## Anexo A. Métodos\n\nEl diseño identifica el efecto.\n"
    err = F.texto_causal(t, "x")
    assert len(err) == 1 and "Parte V" in err[0]


def test_cifras_de_juicio_experto_en_cifras_clave():
    ck = F.D.leer_ck(F.CK)
    je = ck[ck.index.str.startswith("V18-AUX-JE-")]
    assert len(je) == 9 and set(je.capa) == {"C4"}


def test_muestra_revision_2_0_determinista():
    R = _cargar("revision_externa_t", "src/documento_final/revision_externa.py")
    a, b = R.muestra(), R.muestra()
    assert len(a) == 40 and list(a.id) == list(b.id)
    assert a.grupo.nunique() >= 35   # una cifra por ficha dentro de cada estrato
    assert {"C1", "C2", "V18 SUGESTIVO"} <= set(a.estrato)
