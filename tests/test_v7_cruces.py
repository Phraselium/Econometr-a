"""V7 (R0): los cruces territoriales se hacen por código INE, nunca por nombre.

- Código nuevo (src/v7, src/v6_3): prohibido cualquier merge/join cuya clave sea una columna de nombre territorial.
- Código heredado (v1-v6.2): se congela el recuento actual de cruces por nombre (todos revisados en la auditoría K4a y
  en L1/L2 de v6.2); un cruce nuevo por nombre en esos ficheros hace fallar el test.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
NOMBRES = r"(nombre|territorio|provincia|ccaa|municipio|comunidad|nombre_prov|nombre_ccaa|nom_prov|nom_mun)"
PAT = re.compile(r"\.(merge|join)\([^)]*\bon\s*=\s*[\[\(]?[^)]*['\"]" + NOMBRES + r"['\"]", re.I)
PAT_LR = re.compile(r"(left_on|right_on)\s*=\s*[\[\(]?\s*['\"]" + NOMBRES + r"['\"]", re.I)
NUEVO = ("src/v7", "src/v6_3", "src/v8", "src/v12")


PAT_MAP = re.compile(r"\[\s*['\"]" + NOMBRES + r"['\"]\s*\]\s*\.(map|replace)\(|\." + NOMBRES + r"\.(map|replace)\(", re.I)


def cruces_por_nombre(p: Path, nuevo: bool = False) -> int:
    txt = p.read_text(encoding="utf-8", errors="ignore")
    n = len(PAT.findall(txt)) + len(PAT_LR.findall(txt))
    if nuevo:   # en código nuevo también se prohíbe traducir nombres territoriales con diccionarios (.map/.replace)
        n += len(PAT_MAP.findall(txt))
    return n


def test_codigo_nuevo_sin_cruces_por_nombre():
    malos = []
    for d in NUEVO:
        for p in (RAIZ / d).rglob("*.py"):
            if cruces_por_nombre(p, nuevo=True):
                malos.append(str(p.relative_to(RAIZ)))
    assert not malos, f"cruce territorial por nombre en código nuevo (usar código INE): {malos}"


# Recuento congelado del código heredado (2026-10-12). Solo puede bajar.
HEREDADO_MAX = {"src/v5/r1c_run.py": 1}   # R1C (C4 descriptivo): ocupados/iniciadas por CCAA; declara las no cruzadas (sin_map)


def test_heredado_no_aumenta():
    actuales = {}
    for p in (RAIZ / "src").rglob("*.py"):
        rel = str(p.relative_to(RAIZ))
        if rel.startswith(NUEVO):
            continue
        n = cruces_por_nombre(p)
        if n:
            actuales[rel] = n
    nuevos = {k: v for k, v in actuales.items() if v > HEREDADO_MAX.get(k, 0)}
    assert not nuevos, f"nuevos cruces por nombre en código heredado: {nuevos}"
