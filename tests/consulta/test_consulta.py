"""V8.1-B: la capa de consulta (consulta/ y llms.txt) es exactamente lo que genera `make consulta` y respeta las reglas del proyecto."""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "consulta"))
import generar as G  # noqa: E402

CAPAS = {"C1", "C2", "C3", "C3s", "C4"}
MARCA_SUPERADAS = "## Superadas y retiradas"


def _md() -> list[Path]:
    return sorted((RAIZ / "consulta").glob("*.md"))


def test_cifras_con_id_existen_y_coinciden():
    cifras, sup = G.cargar_cifras(), G.cargar_superadas()
    assert not (set(cifras) & set(sup)), "una cifra no puede estar a la vez en cifras_clave y en cifras_superadas"
    n = 0
    for p in _md():
        texto = p.read_text(encoding="utf-8").split(MARCA_SUPERADAS)[0]
        for linea in texto.splitlines():
            for tok in re.findall(r"`([^`]+)`", linea):
                if tok in sup:
                    raise AssertionError(f"{p.name}: cifra superada citada: {tok}")
                if tok in cifras:
                    n += 1
                    assert G.valor_texto(cifras[tok]) in linea, f"{p.name}: el valor de {tok} no coincide con cifras_clave en la línea: {linea[:120]}"
    assert n > 100
    # hallazgos.json: las vigentes salen de cifras_clave con el mismo valor; las superadas, de cifras_superadas
    for h in json.loads((RAIZ / "consulta/hallazgos.json").read_text(encoding="utf-8"))["hallazgos"]:
        if h["tipo"] == "cifra" and h["estado"] == "vigente":
            r = cifras[h["id"]]
            assert h["cifra"] == G._num(r["valor"]) and h["cifra_texto"] == G.valor_texto(r)
        if h["tipo"] == "cifra" and h["estado"] == "superada":
            assert h["id"] in sup and h["id"] not in cifras and h.get("sustituida_por")


def test_enlaces_relativos_resuelven():
    ficheros = _md() + [RAIZ / "llms.txt"]
    n = 0
    for p in ficheros:
        for destino in re.findall(r"\]\(([^)\s]+)\)", p.read_text(encoding="utf-8")):
            if re.match(r"^(?:[a-z]+:|#)", destino):
                continue
            n += 1
            ruta = (p.parent / destino.split("#")[0]).resolve()
            assert ruta.exists(), f"{p.relative_to(RAIZ)}: enlace roto {destino}"
    assert n > 200


def test_hallazgos_capa_fuente_ruta():
    d = json.loads((RAIZ / "consulta/hallazgos.json").read_text(encoding="utf-8"))
    H = d["hallazgos"]
    assert d["n"] == len(H)
    campos = {"id", "enunciado", "cifra", "rango", "unidad", "periodo", "ambito", "mercado", "capa", "metodo", "fuente", "ruta", "version", "estado"}
    ids = set()
    for h in H:
        assert campos <= set(h), h["id"]
        assert h["id"] not in ids
        ids.add(h["id"])
        assert h["capa"] in CAPAS, h["id"]
        assert h["fuente"].strip() and h["ruta"].strip(), h["id"]
        assert (RAIZ / h["ruta"]).exists(), f"{h['id']}: ruta inexistente {h['ruta']}"
        assert h["estado"] in ("vigente", "superada", "retirada")
    assert sum(h["version"] == "V8" and h["tipo"] == "cifra" for h in H) >= 290
    assert sum(h["version"] in ("v5", "v5.1", "v6", "v6.1", "v6.2", "v7", "v7.1", "v7.2") and h["estado"] == "vigente" for h in H) >= 100
    assert any(h["estado"] == "superada" for h in H) and any(h["estado"] == "retirada" for h in H)


def test_leeme_asistente_longitud_y_contenido():
    t = (RAIZ / "consulta/LEEME_ASISTENTE.md").read_text(encoding="utf-8")
    assert len(t.split()) <= 1500
    assert t.startswith("<!-- Generado por `make consulta`")
    assert len(re.findall(r"^- Si te preguntan por", t, re.M)) >= 20
    for clave in ("versión pública", "8.1", "v7.1", "C3s", "neutralidad", "no concluyente", "parque", "contratos nuevos", "SHAP"):
        assert clave.lower() in t.lower(), clave


def test_faq_entre_60_y_80():
    t = (RAIZ / "consulta/preguntas_frecuentes.md").read_text(encoding="utf-8")
    assert 60 <= len(re.findall(r"^### \d+\. ", t, re.M)) <= 80


def test_cabecera_en_cada_fichero():
    for p in _md():
        assert p.read_text(encoding="utf-8").startswith("<!-- Generado por `make consulta`"), p.name
    for n in ("hallazgos.json", "version.json"):
        assert "Generado por `make consulta`" in json.loads((RAIZ / "consulta" / n).read_text(encoding="utf-8"))["_generado"]
    assert "Generado por `make consulta`" in (RAIZ / "llms.txt").read_text(encoding="utf-8")
    assert (RAIZ / "llms.txt").read_text(encoding="utf-8").startswith("# ")


def _foto(base: Path) -> dict[str, bytes]:
    return {p.relative_to(base).as_posix(): p.read_bytes() for p in [*sorted((base / "consulta").rglob("*")), base / "llms.txt"] if p.is_file()}


def test_generador_idempotente(tmp_path):
    # V12-F0: se genera en un directorio temporal; `make check` no reescribe consulta/ (version.json lleva el commit)
    G.escribir(tmp_path / "a")
    G.escribir(tmp_path / "b")
    a = _foto(tmp_path / "a")
    assert a == _foto(tmp_path / "b")
    assert set(a) == {f"consulta/{n}" for n in G.FICHEROS} | {"llms.txt"}


def test_consulta_al_dia_con_sus_fuentes():
    """Lo versionado es lo que se genera ahora (salvo `commit`/`fecha` de version.json, que dependen del historial de git)."""
    esperado = G.generar()
    for rel, txt in esperado.items():
        actual = (RAIZ / rel).read_text(encoding="utf-8")
        if rel.endswith("version.json"):
            a, e = json.loads(actual), json.loads(txt)
            for k in ("commit", "fecha"):
                a.pop(k), e.pop(k)
            assert a == e, "ejecutar `make consulta`"
        else:
            assert actual == txt, f"{rel} desactualizado: ejecutar `make consulta`"


def test_version_json():
    v = json.loads((RAIZ / "consulta/version.json").read_text(encoding="utf-8"))
    notas = (RAIZ / "docs/v8/notas_release.md").read_text(encoding="utf-8")
    m = re.search(r"^doi:\s*(\S+)", notas, re.M)
    proyecto = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))   # V13: versión pública y DOI en proyecto.json
    assert v["version"] == proyecto["version_publica"] and v["doi"] == proyecto["doi"]
    assert v["doi_preregistro_v8"] == (m.group(1) if m else "pendiente")
    assert v["repositorio"] == proyecto["repositorio"]
    assert {"commit", "fecha", "fecha_verificable", "pendientes"} <= set(v) and isinstance(v["pendientes"], list) and v["pendientes"]
