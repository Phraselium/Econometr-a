"""V14.2-B4 · Material de publicación (docs/v14/publicacion_1_0/): coherencia con .zenodo.json y con los límites pedidos."""
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PUB = RAIZ / "docs" / "v14" / "publicacion_1_0"


def test_metadatos_zenodo_coherentes_con_zenodo_json():
    z = json.loads((RAIZ / ".zenodo.json").read_text(encoding="utf-8"))
    md = (PUB / "zenodo_metadatos.md").read_text(encoding="utf-8")
    assert f"| Título | {z['title']} |" in md
    assert f"| Versión | {z['version']} |" in md
    assert f"| Fecha de publicación | {z['publication_date']} |" in md
    assert f"| Idioma | {z['language']} " in md
    assert "; ".join(z["keywords"]) in md
    c = z["creators"][0]
    assert f"{c['name']} · afiliación: {c['affiliation']}" in md
    assert all(r["identifier"] in md for r in z["related_identifiers"])
    assert z["notes"] in md
    assert z["description"].split(".")[0] in md


def test_correo_revisor_200_palabras_como_maximo():
    t = (PUB / "correo_revisor.md").read_text(encoding="utf-8")
    cuerpo = t[t.index("**Asunto:**"):]
    assert len(cuerpo.split()) <= 200


def test_osf_con_las_nueve_etiquetas_y_la_declaracion():
    t = (PUB / "osf_registro.md").read_text(encoding="utf-8")
    etiquetas = re.findall(r"^\| (prereg-v[\w-]+) \| ([0-9a-f]{40}) \| (\S+) \| (\S+) \| ([0-9a-f]{64}) \|$", t, re.M)
    assert len(etiquetas) == 9
    assert "**posteriores** a los commits que fijan" in t
    v13 = (RAIZ / "docs" / "v13" / "tareas_autor.md").read_text(encoding="utf-8")
    for e, sha1, fecha, doc, h in etiquetas:   # mismos commits, fechas y huellas que la tabla 3.1 de V13
        assert f"| {e} | " in v13 and sha1 in v13 and fecha in v13 and h in v13, e


def test_notas_de_version_sin_cifras_de_resultados():
    t = (PUB / "notas_version_github.md").read_text(encoding="utf-8")
    for s in ("## Qué es", "## Cómo citar", "## Qué no se puede afirmar", "## Limitación de reproducibilidad"):
        assert s in t
    sin_enlaces = re.sub(r"\([^)]*\)|https?://\S+|v\d+(\.\d+)?|V\d+|\d+\.\d+\.x|C[1-4]s?", "", t)
    assert not re.search(r"\d+[,.]?\d*\s*%", sin_enlaces)   # las cifras viven en cifras_clave, no aquí
