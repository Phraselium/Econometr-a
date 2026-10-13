"""v6.2 L5: coherencia final de cifras.

Ningún entregable, post, ficha del verificador ni el anexo cita una cifra sustituida (ERRATA), y la lista de
cifras publicables coincide con cifras_clave.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
# Valores superados (ERRATA.md): déficit C1 de v4-v6.1, A23-A10 de v5 y v6.1, recuentos redondeados de K4a-01
SUPERADOS = ["562.692-688.692", "562.692-902.808", "26,6 % (22,4-30,8", "27,7 % (24,6-30,8", "22,4-30,8 %", "24,6-30,8 %",
             "1.720.540", "1.024.160", "562.692-744.144", "344.803", "2.148.680", "1.447.950", "1.296.670", "1.415.260", "3.262.030", "1.349.020",
             "924.658"]   # v7.2: máximo con bajas supuestas del 0,1-0,2 % (L3-DEF-2124-CONBAJAS, retirada)
PERMITIDO = re.compile(r"hist[oó]ric|v6\.1|ERRATA|antes|publicado en|sustituid|retirad|^\| (deficit_2124_c[12]|T3-H2) \|", re.I)


def ficheros():
    fs = [p for p in (RAIZ / "output" / "v5").rglob("*.md") if not p.name.startswith("cifras_clave")]
    fs += list((RAIZ / "output" / "v5" / "verificador" / "fichas").glob("*.json"))
    fs += [RAIZ / "output" / "v6_2" / "anexo_metodologico.md", RAIZ / "README.md"]
    # documentos para el lector externo (los registros internos de proceso -estado, revisión, decisiones- citan valores anteriores a propósito)
    fs += [RAIZ / "docs" / "v6_2" / n for n in ("guia_revisor.md", "cifras_publicables.md", "tareas_autor.md")]
    return [f for f in fs if f.exists()]


def test_sin_cifras_superadas():
    malas = []
    for f in ficheros():
        for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for v in SUPERADOS:
                if v in ln and not PERMITIDO.search(ln):
                    malas.append(f"{f.relative_to(RAIZ)}:{n}: {v}")
    assert not malas, "cifras superadas citadas: " + "; ".join(malas[:15])


def test_plantillas_sin_ids_historicos():
    malas = []
    for f in (RAIZ / "docs" / "v5" / "plantillas").rglob("*.md"):
        for n, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"\{\{deficit_2124_c[12]", ln) and not PERMITIDO.search(ln):
                malas.append(f"{f.relative_to(RAIZ)}:{n}")
    assert not malas, f"ids históricos en plantillas: {malas}"


def test_cifras_publicables_al_dia():
    sys.path.insert(0, str(RAIZ / "src" / "v6_2"))
    import l5_publicables
    assert (RAIZ / "docs" / "v6_2" / "cifras_publicables.md").read_text(encoding="utf-8") == l5_publicables.generar(), \
        "docs/v6_2/cifras_publicables.md desactualizado: ejecutar python3 src/v6_2/l5_publicables.py"


# v7.2: el control de cifras superadas cubre también la tabla única (output/v5/cifras_clave.csv y su copia en publicacion/)
RETIRADAS_NUM = [(562692, 688692), (562692, 902808), (562692, 744144.3), (389361, 924658), (700934, 826702.8)]


def test_cifras_clave_sin_superadas():
    sys.path.insert(0, str(RAIZ / "src" / "v5"))
    import cifras_clave as CK
    import pandas as pd
    for f in (RAIZ / "output" / "v5" / "cifras_clave.csv", RAIZ / "publicacion" / "cifras_clave.csv"):
        ck = pd.read_csv(f)
        assert not set(CK.RETIRADAS) & set(ck.id), (f.name, sorted(set(CK.RETIRADAS) & set(ck.id)))
        assert not ck.id.str.startswith(CK.NO_DIFUNDIBLE_PREFIJOS).any(), f
        for lo, hi in RETIRADAS_NUM:
            assert not ((ck["min"].round(1) == lo) & (ck["max"].round(1) == hi)).any(), (f.name, lo, hi)
        assert not ck.astype(str).apply(lambda c: c.str.contains("0,1-0,2 %")).any().any(), "supuesto de bajas 0,1-0,2 % en cifras_clave"
    sup = pd.read_csv(RAIZ / "output" / "v5" / "cifras_superadas.csv")
    assert set(CK.RETIRADAS) <= set(sup.id), sorted(set(CK.RETIRADAS) - set(sup.id))
    assert sup.motivo.notna().all() and sup.sustituida_por.notna().all()
