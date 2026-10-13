"""check_v8: la puerta V8 pasa y sus reglas detectan las infracciones que deben detectar."""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
sys.path.insert(0, str(RAIZ / "src"))
import pandas as pd  # noqa: E402
import check_v8 as C  # noqa: E402


def test_puerta_v8_sin_errores():
    r = subprocess.run([sys.executable, str(RAIZ / "src" / "v8" / "check_v8.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout[-2000:]


def test_detecta_cifra_libre_y_admite_umbrales():
    assert re.search(r"\d", C._libres("El precio subió un 12,3 % en P5."))
    assert not re.search(r"\d", C._libres("Banda del 68 % y umbral del 80 % en P5 (C3s); AR(4); log ×100."))


def test_detecta_causal_desde_shap():
    linea = "SHAP muestra que el turismo provoca la subida."
    assert C.CAUSAL.search(linea) and C.INTERP.search(linea) and not C.NEG.search(linea)
    assert C.NEG.search("SHAP no permite una lectura causal.")


def test_cifras_previas_intactas():
    assert C.cifras_previas() == []


LINEAS_MALAS = [
    "Según SHAP, el turismo impulsa la subida del precio de la vivienda [C4].",
    "La subida reciente se explica casi entera por lo común a toda España [C4].",
    "El DML muestra que el encarecimiento del crédito desvía demanda de la compra al alquiler, aunque sin identificación [C4].",
    "SHAP muestra que el turismo causa la subida, sin identificación externa [C4].",
    "La dominancia indica que el crédito es el motor de la subida de la compra [C4].",
    "El turismo explica la subida (SHAP) [C4].",
]


def test_detecta_las_lineas_fabricadas_de_la_revision():
    for linea in LINEAS_MALAS:
        assert C.lineas_causales(linea, "x.md"), linea


def test_no_marca_texto_legitimo():
    ok = [
        "El crédito empuja al alza la compra, condicionado a las restricciones de signo y de cero de M2 [C3s].",
        "Los tipos empujan el precio (C3s), condicionado a las restricciones de signo.",
        "SHAP no es el motor de la subida y no permite una lectura causal [C4].",
        "Ningún factor frena la subida según este análisis: no es causal [C4].",
        "Sus fluctuaciones se mueven despacio y se mueven juntas [C4].",
        "El panel de compra, 1,2 frente a 1,1 [C4].",
        "| H8-7 | Empuje migratorio aumenta el alquiler real (LP-IV) | F 0,05 | C4 |",
    ]
    for linea in ok:
        assert not C.lineas_causales(linea, "x.md"), linea


def test_c4_se_hereda_de_la_seccion_y_de_la_tabla():
    assert C.lineas_causales("## Resultados [C4]\n\nEl turismo impulsa la subida.\n", "x.md")
    assert not C.lineas_causales("## Resultados [C3s]\n\nEl turismo impulsa la subida.\n", "x.md")
    assert C.lineas_causales("| factor | efecto [C4] |\n|---|---|\n| turismo | impulsa la subida |\n", "x.md")


def test_negacion_por_proposicion():
    assert not C.causal_sin_negar("No es el motor de la subida.")
    assert C.causal_sin_negar("No hay efecto causal en el crédito. El turismo es el motor de la subida.")


def test_cruces_por_nombre_ast():
    malos = ["a.merge(b, left_on='nombre_ccaa', right_on='ccaa')", "a.merge(b, right_on=['x', 'name'])", "a['nombre'].map(d)",
             "a.pivot(index='nombre_prov', columns='c', values='v')", "a.set_index('provincia_nombre')", "a.join(b, on='nombre')"]
    for src in malos:
        assert C.cruces_en(src, "t.py"), src
    assert not C.cruces_en("a.merge(b, on='ccaa_cod'); ', '.join(x); a['cod'].map(d)", "t.py")


def test_bandas_exigidas_salvo_sin_banda():
    a = pd.DataFrame([dict(compite="si", metodo="lpiv", b68_lo=None, b68_hi=None, notas="", mercado="compra", periodo="P5", factor="x"),
                      dict(compite="si", metodo="lpiv", b68_lo=None, b68_hi=None, notas="sin banda (AR no acotado)", mercado="compra", periodo="P4", factor="x"),
                      dict(compite="no", metodo="lpiv", b68_lo=None, b68_hi=None, notas="", mercado="compra", periodo="P3", factor="x"),
                      dict(compite="si", metodo="shap", b68_lo=None, b68_hi=None, notas="", mercado="compra", periodo="P2", factor="x")])
    assert len(C.bandas_df(a)) == 1


def test_p_ajustado_metodo_y_columna_ausente():
    assert C._p_ajustados_df(pd.DataFrame({"p": [0.01]}), "f.csv")[0].startswith("f.csv: falta la columna p_ajustado")
    assert C._p_ajustados_df(pd.DataFrame({"p": [0.01], "p_ajustado": [0.02]}), "f.csv")[0].startswith("f.csv: falta la columna metodo_ajuste")
    assert C._p_ajustados_df(pd.DataFrame({"p": [0.01], "p_ajustado": [0.02], "metodo_ajuste": ["Bonferroni"]}), "f.csv")
    assert not C._p_ajustados_df(pd.DataFrame({"p": [0.01], "p_ajustado": [0.02], "metodo_ajuste": ["BH"]}), "f.csv")
    assert C._p_ajustados_df(pd.DataFrame({"p_holm": [0.5], "metodo_ajuste": ["x"]}), "h.csv")


def test_errata_exige_linea_id_sha():
    er = "| 2026 | v4 | A23-A10 cambia | fix |\n| A23-A10 | abc123 | motivo |\n"
    assert not C._en_errata(er, "A23-A10", "def456")
    assert C._en_errata(er, "A23-A10", "abc123")
    assert not C._en_errata(er, "A23-A10", None)
    assert C._en_errata("| X-1 | desaparecida | retirada |\n", "X-1", None)


def test_destacado_es_el_de_menor_rmse():
    oos = pd.DataFrame([dict(modulo="M4", mercado="compra", modelo="C1_sin_rupturas_SR", rmse=1.7),
                        dict(modulo="M4", mercado="compra", modelo="C1_sin_rupturas_ECM", rmse=1.4),
                        dict(modulo="M4", mercado="compra", modelo="C1_sin_rupturas_AR4", rmse=1.28)])
    base = dict(modulo="M4", familia_modelo="dols", mercado="compra", periodo="completo", destacado="si", modelo_id="m")
    assert not C.destacados_vs_oos(pd.DataFrame([dict(base, rmse_oos=1.4)]), oos)
    assert C.destacados_vs_oos(pd.DataFrame([dict(base, rmse_oos=1.7)]), oos)


def test_trazabilidad_abre_el_hechos_json():
    ck = pd.DataFrame([dict(id="V8-NO-EXISTE", valor="1", origen="output/v8/F6/hechos.json:V8-NO-EXISTE"),
                       dict(id="V8-REGLA-c-P5", valor="999", origen="output/v8/F6/hechos.json:V8-REGLA-c-P5")])
    e = C.origen_hechos(ck)
    assert len(e) == 2 and "no está en" in e[0] and "distinto" in e[1]
