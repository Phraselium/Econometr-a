"""Comprobaciones de puerta V9 (entran en `make check`). Sin red. Reutiliza las funciones de src/v8/check_v8.py.

1. Ninguna cifra publicada antes de V9 cambia sin ERRATA (huellas en docs/v9/cifras_base_v81.csv).
2. p ajustados: Holm en la familia confirmatoria y BH en las exploratorias (salvo D3, descriptivo) en output/v9/f3/tabla_capas.csv;
   ninguna capa C3/C3s sin p de Holm < 0,05.
3. Lenguaje causal solo en C3/C3s: los textos de V9 (informe, verificador, cotas, tabla) no contienen lenguaje causal sin negar
   (ningún resultado de V9 es C3/C3s); sin léxico valorativo (check_texto).
4. Nada no redistribuible en la capa pública: data/base/publica/variables.parquet sin Incasòl, Registre, IEET ni shocks JK, y
   ningún fichero de output/v9 con microdatos de esas fuentes (solo estimaciones agregadas).
5. Cruces solo por código: ningún merge/join de src/v9 por columnas de nombre.
6. Trazabilidad de la web: cada id V9 de src/v10/web.py existe en cifras_clave y su script existe; cada id de las fichas del
   verificador V9 existe en cifras_clave.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v8"))
import check_v8 as C8  # noqa: E402

OUT = RAIZ / "output" / "v9"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"
NO_REDIS = re.compile(r"^(incasol_|registre|ieet|jk_|registr)", re.I)


def cifras_previas() -> list[str]:
    base = pd.read_csv(RAIZ / "docs/v9/cifras_base_v81.csv", comment="#", dtype=str).set_index("id")["sha256"]
    ck = pd.read_csv(CK, dtype=str).fillna("").set_index("id")
    errata = (RAIZ / "ERRATA.md").read_text(encoding="utf-8")
    err = []
    for i, h in base.items():
        if i not in ck.index:
            if not C8._en_errata(errata, i, None):
                err.append(f"cifra publicada desaparecida sin ERRATA: {i}")
            continue
        h2 = C8._huella(ck, i)
        if h2 != h and not C8._en_errata(errata, i, h2):
            err.append(f"cifra publicada cambiada sin ERRATA: {i}")
    return err


def p_ajustados() -> list[str]:
    t = pd.read_csv(OUT / "f3/tabla_capas.csv")
    err = []
    conf = t[t.confirmatoria]
    if conf.p_holm.isna().any():
        err.append("confirmatoria sin p de Holm")
    expl = t[~t.confirmatoria & (t.diseno != "D3")]
    if expl.p_bh.isna().any():
        err.append("exploratoria sin p de BH")
    for r in t[t.capa.isin(["C3", "C3s"])].itertuples():
        if not (r.confirmatoria and r.p_holm < 0.05):
            err.append(f"C3/C3s sin Holm < 0,05: {r.diseno} {r.resultado}")
    return err


NOMBRE_PAGINA = re.compile(r"qu[ée] causa qu[ée]", re.I)


def causales(s: str, nombre: str) -> list[str]:
    """Sin C3/C3s en V9, cualquier proposición con léxico causal sin negar es un error (salvo el nombre de la página)."""
    err = []
    for i, linea in enumerate(s.splitlines(), 1):
        lin = NOMBRE_PAGINA.sub(" ", linea)
        if lin.startswith("**Afirmación.**") or "check:ok" in lin or not C8.CAUSAL.search(lin) or not C8.causal_sin_negar(lin):   # la afirmación evaluada se cita
            continue
        err.append(f"{nombre}:{i}: lenguaje causal sin C3/C3s: «{linea.strip()[:90]}»")
    return err


def texto() -> list[str]:
    err = []
    t = pd.read_csv(OUT / "f3/tabla_capas.csv")
    hay_c3 = t.capa.isin(["C3", "C3s"]).any()
    textos = [OUT / "informe_v9.md", OUT / "verificador_v9.md", OUT / "f4/cotas.md", RAIZ / "docs/v9/plantillas/informe_v9.md"]
    for p in textos:
        if not p.exists():
            err.append(f"falta {p.relative_to(RAIZ)}")
            continue
        s = p.read_text(encoding="utf-8")
        if not hay_c3:
            err += causales(s, str(p.relative_to(RAIZ)))
        err += C8.revisar_texto(s, str(p.relative_to(RAIZ)))
    for f in json.loads((OUT / "fichas_verificador_v9.json").read_text(encoding="utf-8")):
        s = "\n".join(str(f.get(k, "")) for k in ("magnitud", "limites", "veredicto"))   # el enunciado es la afirmación evaluada
        if not hay_c3:
            err += causales(s, f"ficha {f['id']}")
    return err


def capa_publica() -> list[str]:
    err = []
    v = pd.read_parquet(RAIZ / "data/base/publica/variables.parquet")
    malas = sorted(x for x in v.variable if NO_REDIS.search(x))
    if malas:
        err.append(f"variables no redistribuibles en la capa pública: {malas}")
    for p in OUT.rglob("*.csv"):
        cab = p.read_text(encoding="utf-8", errors="replace").splitlines()[0].lower() if p.stat().st_size else ""
        if any(c in cab for c in ("codi_territorial", "habitatges", "tram_preus", "signatura", "mp_median")):
            err.append(f"{p.relative_to(RAIZ)}: posibles microdatos no redistribuibles")
    return err


def cruces() -> list[str]:
    err = []
    for p in sorted((RAIZ / "src/v9").glob("*.py")):
        err += C8.cruces_en(p.read_text(encoding="utf-8"), str(p.relative_to(RAIZ)))
    return err


def trazabilidad() -> list[str]:
    ck = pd.read_csv(CK, dtype=str).set_index("id")
    err = []
    web = (RAIZ / "src/v10/web.py").read_text(encoding="utf-8")
    for i in sorted(set(re.findall(r'"(V9-[A-Za-z0-9\-]+)"', web))):
        if i not in ck.index:
            err.append(f"web: {i} no está en cifras_clave")
    arbol = ast.parse(web)
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and nodo.value.startswith("src/v9/") and nodo.value.endswith(".py"):
            if not (RAIZ / nodo.value).exists():
                err.append(f"web: script inexistente {nodo.value}")
    for f in json.loads((OUT / "fichas_verificador_v9.json").read_text(encoding="utf-8")):
        for i in f["ids_cifras"]:
            if i not in ck.index:
                err.append(f"ficha {f['id']}: {i} no está en cifras_clave")
    return err


def main() -> int:
    err = []
    for nombre, fn in (("cifras previas", cifras_previas), ("p ajustados", p_ajustados), ("texto", texto),
                       ("capa pública", capa_publica), ("cruces", cruces), ("trazabilidad", trazabilidad)):
        e = fn()
        print(f"check_v9 · {nombre}: {len(e)} errores")
        err += e
    for e in err:
        print("  -", e)
    print(f"check_v9: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
