"""Comprobaciones de puerta V8 (entran en `make check`). Sin red.

1. Ninguna cifra previa a V8 (v1-v7.2) cambia sin figurar en ERRATA.md (huellas en docs/v8/cifras_base_v72.csv).
2. Todo p de los coeficientes de V8 lleva p ajustado y método (Holm o BH).
3. Ningún modelo destacado se elige por su p (motivo_destacado: regla del §8 + multiverso o error fuera de muestra).
4. Las atribuciones que votan en la regla del §9 llevan banda del 68 %.
5. Sin lenguaje causal en líneas C4 ni a partir de SHAP, importancias, dominancia, Granger o DML; sin léxico valorativo ni
   partidista (entregables V8, plantillas y fichas del verificador V8).
6. Cruces territoriales solo por código: ningún merge/join de src/v8 por columnas de nombre.
7. Toda cifra es trazable: plantillas V8 sin cifras fuera de marcadores, entregables sin marcadores sin resolver, cifras V8
   con origen en un hechos.json de output/v8 y coeficientes con su script.
Sale con código 1 si hay errores.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
from check_texto import revisar_texto  # noqa: E402
from check_v5 import _sin_libres  # noqa: E402

OUT = RAIZ / "output" / "v8"
PLANT = RAIZ / "docs" / "v8" / "plantillas"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"
BASE = RAIZ / "docs" / "v8" / "cifras_base_v72.csv"
ERRATA = RAIZ / "ERRATA.md"
MARC = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([a-z_]+))?\}\}")
COLS = ["id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato"]

CAUSAL = re.compile(r"\b(caus[aó]\w*|provoc\w*|efecto causal|impacto causal|se debe a|debido a|gracias a|hace que|"
                    r"ha hecho (?:subir|bajar)|explica[nr]? (?:la|el|que))\b", re.I)
NEG = re.compile(r"\b(no|nunca|ni|sin|nada)\b[^.]{0,60}\b(causal\w*|caus\w*|atribuci[óo]n|identifica\w*)", re.I)
INTERP = re.compile(r"\b(SHAP|importancias?|dominancia|Granger|DML)\b", re.I)
# cifras permitidas en plantillas V8 además de las de v5: umbrales pre-registrados, capas, fases, decisiones y hallazgos
LIBRE_V8 = [r"\b(?:50|68|80|90|95) ?%", r"×100", r"\bC3s\b", r"\b[FJMRYH]\d{1,2}(?:-\d+)?\b", r"\bsha256\b", r"\bq = 0,10\b",
            r"\bSEED = \d+\b", r"\bAR\(\d\)"]


def _libres(linea: str) -> str:
    for p in LIBRE_V8:
        linea = re.sub(p, " ", linea)
    return _sin_libres(linea)


def cifras_previas() -> list[str]:
    if not BASE.exists() or not CK.exists():
        return [f"falta {BASE.relative_to(RAIZ) if not BASE.exists() else CK.relative_to(RAIZ)}"]
    base = pd.read_csv(BASE, comment="#", dtype=str).set_index("id")["sha256"]
    ck = pd.read_csv(CK, dtype=str).fillna("").set_index("id")
    errata = ERRATA.read_text(encoding="utf-8") if ERRATA.exists() else ""
    err = []
    for i, h in base.items():
        if i not in ck.index:
            if i not in errata:
                err.append(f"cifra previa a V8 desaparecida sin ERRATA: {i}")
            continue
        fila = [i] + [ck.at[i, c] for c in COLS[1:]]
        if hashlib.sha256("|".join(fila).encode()).hexdigest() != h and i not in errata:
            err.append(f"cifra previa a V8 cambiada sin ERRATA: {i}")
    return err


def p_ajustados() -> list[str]:
    err = []
    for p in sorted(OUT.glob("M*/coeficientes.csv")):
        c = pd.read_csv(p, low_memory=False)
        if "p" not in c.columns:
            continue
        sin = c[c["p"].notna() & (c.get("p_ajustado").isna() | c.get("metodo_ajuste").isna())]
        if len(sin):
            err.append(f"{p.relative_to(RAIZ)}: {len(sin)} p sin p_ajustado o sin metodo_ajuste")
        if "script" in c.columns and c["script"].isna().any():
            err.append(f"{p.relative_to(RAIZ)}: coeficientes sin script")
    return err


def destacados() -> list[str]:
    p = OUT / "tablas_modelos_destacados.csv"
    if not p.exists():
        return ["falta output/v8/tablas_modelos_destacados.csv"]
    t = pd.read_csv(p, low_memory=False)
    d = t[t["destacado"].astype(str).str.lower().isin(["si", "sí", "true"])]
    err = []
    for r in d.itertuples():
        m = str(r.motivo_destacado)
        if not re.search(r"fuera de muestra|regla", m, re.I) or re.search(r"\bp\b|p-valor|p ajustado|significa", m, re.I):
            err.append(f"tablas_modelos_destacados: {r.modelo_id} con motivo no admitido «{m[:60]}»")
    return err


def bandas() -> list[str]:
    p = OUT / "F5" / "atribucion_combinada.csv"
    if not p.exists():
        return ["falta output/v8/F5/atribucion_combinada.csv"]
    a = pd.read_csv(p)
    v = a[a["vota"].astype(str) == "si"]
    sin = v[v["b68_lo"].isna() | v["b68_hi"].isna()]
    return [f"F5: voto sin banda del 68 %: {r.metodo} {r.mercado} {r.periodo} {r.factor}" for r in sin.itertuples()]


def _textos() -> list[Path]:
    return sorted(p for p in PLANT.rglob("*.md") if p.name != "README.md") + sorted(OUT.glob("*.md"))


def texto() -> list[str]:
    err = []
    for p in _textos() + [OUT / "fichas_verificador_v8.json"]:
        if not p.exists():
            continue
        nombre = str(p.relative_to(RAIZ))
        t = p.read_text(encoding="utf-8")
        err += revisar_texto(t, nombre)
        for i, linea in enumerate(t.splitlines(), 1):
            if "check:ok" in linea or not CAUSAL.search(linea) or NEG.search(linea):
                continue
            if "[C4]" in linea or "C4" in re.findall(r"\bC[1-4]s?\b", linea) and "C3s" not in linea:
                err.append(f"{nombre}:{i}: lenguaje causal en línea C4")
            if INTERP.search(linea):
                err.append(f"{nombre}:{i}: lectura causal desde SHAP, importancias, dominancia, Granger o DML")
    return err


def cruces() -> list[str]:
    err = []
    pat = re.compile(r"\.(?:merge|join)\([^)]*\bon\s*=\s*\[?[^)\]]*['\"](\w*(?:nombre|name)\w*)['\"]", re.S)
    for p in sorted((RAIZ / "src" / "v8").rglob("*.py")):
        for m in pat.finditer(p.read_text(encoding="utf-8")):
            err.append(f"{p.relative_to(RAIZ)}: cruce por nombre «{m.group(1)}» (V8: solo por código INE)")
    return err


def trazabilidad() -> list[str]:
    err = []
    for p in sorted(PLANT.rglob("*.md")):
        if p.name == "README.md":
            continue
        for i, linea in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if "check:cifra-libre" in linea:
                continue
            if re.search(r"\d", _libres(MARC.sub(" ", linea))):
                err.append(f"{p.relative_to(RAIZ)}:{i}: cifra fuera de cifras_clave: «{linea.strip()[:90]}»")
        dest = OUT / p.relative_to(PLANT)
        if not dest.exists():
            err.append(f"falta el entregable renderizado {dest.relative_to(RAIZ)}")
    for p in sorted(OUT.glob("*.md")):
        if MARC.search(p.read_text(encoding="utf-8")):
            err.append(f"{p.relative_to(RAIZ)}: marcador sin resolver")
    if CK.exists():
        ck = pd.read_csv(CK, dtype=str)
        v8 = ck[ck["id"].str.startswith("V8-")]
        mal = v8[~v8["origen"].fillna("").str.startswith("output/v8/")]
        err += [f"cifras_clave: {r.id} sin origen en output/v8" for r in mal.itertuples()]
    return err


def main() -> int:
    err = cifras_previas() + p_ajustados() + destacados() + bandas() + texto() + cruces() + trazabilidad()
    for e in err:
        print(e)
    print(f"check_v8: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
