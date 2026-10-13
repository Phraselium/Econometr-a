"""V8-F6: hechos V8 (output/v8/F6/hechos.json), su paso a cifras_clave y la plantilla de ensayo."""
import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
H = RAIZ / "output" / "v8" / "F6" / "hechos.json"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"
sys.path.insert(0, str(RAIZ / "src" / "v8"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))


def _h() -> list[dict]:
    return json.loads(H.read_text(encoding="utf-8"))


def test_formato_estandar():
    h = _h()
    assert len(h) >= 40
    ids = [x["id"] for x in h]
    assert len(ids) == len(set(ids)) and all(i.startswith("V8-") for i in ids)
    for x in h:
        for c in ("indicador", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato"):
            assert x[c], (x["id"], c)
        assert re.fullmatch(r"C(1|2|3|3s|4)", x["capa"]), x["id"]
        assert re.fullmatch(r"20\d\dT[1-4]", x["fecha_dato"]), x["id"]
        assert any(x[k] is not None for k in ("valor", "min", "max"))


def test_causal_solo_en_c3s():
    """Las cifras del SVAR son C3s y dicen «condicionado a las restricciones»; las demás no llevan lenguaje causal."""
    for x in _h():
        if x["capa"] == "C3s":
            assert "condicionad" in x["indicador"] or x["id"].startswith(("V8-REGLA", "V8-PFSTAR")) or "Holm" in x["indicador"], x["id"]
        else:
            assert not re.search(r"\b(causa|provoca|efecto causal)\b", x["indicador"], re.I), x["id"]


def test_valores_leidos_de_f5():
    r = pd.read_csv(RAIZ / "output" / "v8" / "F5" / "regla_s9.csv")
    h = {x["id"]: x for x in _h()}
    for t in r.itertuples():
        assert abs(h[f"V8-OBS-{t.mercado[0]}-{t.periodo}"]["valor"] - t.delta_y_pp) < 1e-9
        assert h[f"V8-REGLA-{t.mercado[0]}-{t.periodo}"]["valor"] == (1.0 if t.resultado == "designado" else 0.0)
    assert sum(h[i]["valor"] for i in h if i.startswith("V8-REGLA-")) == 0


def test_cifras_clave_recoge_v8():
    ck = pd.read_csv(CK).set_index("id")
    h = _h()
    assert {x["id"] for x in h} <= set(ck.index)
    assert ck.loc[h[0]["id"], "origen"].startswith("output/v8/F6/hechos.json:")
    assert not ck.origen.astype(str).str.contains("_smoke").any()


def test_generacion_determinista(tmp_path):
    antes = H.read_bytes()
    subprocess.run([sys.executable, str(RAIZ / "src" / "v8" / "f6_hechos.py")], check=True, capture_output=True)
    assert H.read_bytes() == antes


def test_render_ensayo_y_marcador_sin_resolver(tmp_path):
    import render_v8 as RV
    ck = pd.read_csv(CK).set_index("id")
    ok, falta = RV.render(RAIZ / "docs" / "v8" / "plantillas" / "ensayo.md", ck)
    assert not falta and "{{" not in ok
    p = tmp_path / "x.md"
    p.write_text("cifra {{V8-NO-EXISTE}}", encoding="utf-8")
    _, falta = RV.render(p, ck)
    assert falta == ["V8-NO-EXISTE"]
    assert ck.loc["V8-H8-1-pholm"].unidad == "p-valor" and RV.texto(ck.loc["V8-H8-1-pholm"], None) == "0,987"


def test_readme_lista_todos_los_ids():
    t = (RAIZ / "docs" / "v8" / "plantillas" / "README.md").read_text(encoding="utf-8")
    assert all(f"`{x['id']}`" in t for x in _h())


def test_formato_v8_no_contamina_v5():
    """Los formatos de V8 solo rigen dentro de formato_v8(): render.py de v5 queda intacto fuera."""
    import render as R5
    import render_v8 as RV
    antes = (R5.fmt_num, R5.texto, set(R5.CONTEOS))
    with RV.formato_v8():
        assert R5.fmt_num is not antes[0]
    assert (R5.fmt_num, R5.texto, R5.CONTEOS) == antes
