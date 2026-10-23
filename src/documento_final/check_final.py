"""Consolidación final · Controles de `make check` del documento final. Solo lectura; sin red; no escribe nada.

1. Al día: el documento y su resumen ejecutivo, regenerados en memoria desde docs/documento_final/plantilla y cifras_clave, coinciden
   con output/documento_final/ y con su copia en publicacion/documento_final/ (sin la cabecera que añade `make publicacion`).
2. Lenguaje y rótulos (documento_final.comprobar): nada causal fuera de los anexos técnicos; la mejor estimación y la contabilidad
   con magnitudes de la literatura van rotuladas como juicio experto.
3. Coherencia entre puertas: consulta/resumen_final.md lleva el mismo resumen ejecutivo; si la web está construida (web/_site, no
   versionada), su portada lleva todas las cifras de la tabla de factores del resumen.
4. Cifras de juicio experto: las V18-AUX-JE-* de cifras_clave son C4 y su nota dice que son juicio experto.
"""
from __future__ import annotations

import html
import importlib.util
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("documento_final", RAIZ / "src" / "documento_final" / "documento_final.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)

PUB = RAIZ / "publicacion" / "documento_final"
CONSULTA = RAIZ / "consulta" / "resumen_final.md"
WEB = RAIZ / "web" / "_site" / "index.html"
CIFRA = re.compile(r"(?<![\w,.\-])−?\d{1,3}(?:\.\d{3})*,\d+|(?<![\w,.\-])\d{1,3}(?:\.\d{3})+(?![\d,])")   # decimales y miles: no años ni periodos


def _sin_cabecera(t: str) -> str:
    return t.split("\n", 2)[-1] if t.startswith("<!--") else t


def al_dia() -> tuple[list[str], str, str]:
    ck, mag = F.D.leer_ck(F.CK), F.D.pd.read_csv(F.MAG)
    texto, resumen, res = F.ensamblar(ck, mag)
    err = [f"marcador sin cifra: {x}" for x in res["marcadores_sin_cifra"]]
    for ruta, esperado in ((F.DOC, texto), (F.RES, resumen)):
        if not ruta.exists():
            err.append(f"{ruta.relative_to(RAIZ)}: no existe (make documento_final)")
        elif ruta.read_text(encoding="utf-8") != esperado:
            err.append(f"{ruta.relative_to(RAIZ)}: desactualizado (make documento_final)")
        pub = PUB / ruta.name
        if not pub.exists():
            err.append(f"{pub.relative_to(RAIZ)}: no existe (make publicacion)")
        elif _sin_cabecera(pub.read_text(encoding="utf-8")) != esperado:
            err.append(f"{pub.relative_to(RAIZ)}: distinto de {ruta.relative_to(RAIZ)} (make publicacion)")
    return err, texto, resumen


def coherencia(resumen: str) -> list[str]:
    err = []
    if not CONSULTA.exists() or resumen.split("## Resumen ejecutivo", 1)[-1] not in CONSULTA.read_text(encoding="utf-8"):
        err.append(f"{CONSULTA.relative_to(RAIZ)}: no lleva el resumen ejecutivo del documento final (make consulta)")
    if WEB.exists():
        portada = html.unescape(re.sub(r"<[^>]+>", " ", WEB.read_text(encoding="utf-8")))
        tabla = resumen.split("## Resumen ejecutivo", 1)[-1].split("\nNota sobre los topes", 1)[0]
        faltan = sorted({c for c in CIFRA.findall(tabla) if c not in portada})
        if faltan:
            err.append(f"{WEB.relative_to(RAIZ)}: faltan cifras del resumen ejecutivo ({', '.join(faltan[:8])}; make web)")
    return err


def juicio_experto() -> list[str]:
    """Las cifras V18-AUX-JE-* son C4 en cifras_clave y su nota (output/v18/f6/hechos.json) las rotula como juicio experto."""
    import json
    ck = F.D.leer_ck(F.CK)
    je = ck[ck.index.str.startswith("V18-AUX-JE-")]
    err = [] if len(je) else ["cifras_clave: faltan las cifras V18-AUX-JE-* de la contabilidad con magnitudes de la literatura"]
    err += [f"{i}: capa {r.capa} (debe ser C4)" for i, r in je.iterrows() if r.capa != "C4"]
    notas = {h["id"]: h.get("nota", "") for h in json.loads((RAIZ / "output/v18/f6/hechos.json").read_text(encoding="utf-8"))}
    err += [f"{i}: la nota de output/v18/f6/hechos.json no la rotula como juicio experto" for i in je.index
            if F.JUICIO not in notas.get(i, "")]
    return err


def main() -> int:
    err, texto, resumen = al_dia()
    err += F.comprobar(texto, str(F.DOC.relative_to(RAIZ)))
    err += coherencia(resumen)
    err += juicio_experto()
    print(f"check_final (documento final): {len(err)} errores")
    for x in err[:30]:
        print(f"  - {x}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
