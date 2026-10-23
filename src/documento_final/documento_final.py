"""Consolidación final · `make documento_final`: documento final del proyecto (publicación 2.0; sin análisis nuevo).

Integra lo que V15-V18 permiten decir: V17 (auditoría, lectura convencional y preguntas D3), V18 (réplicas, magnitudes y tabla de
impactos) y las capas del proyecto. No estima nada: ensambla las plantillas de docs/documento_final/plantilla/[0-9][0-9]_*.md
(texto escrito a mano, con marcadores) y sustituye cada marcador contra output/v5/cifras_clave.csv con el mismo motor que el
Documento de Trabajo V18 (src/v18/f6_documento.py: {{id}}, {{id:campo}}, {{id:clasificacion}}, {{tabla.impactos}}…).

Salidas (las copia `make publicacion` a publicacion/documento_final/):
  output/documento_final/documento_final.md     documento completo (resumen ejecutivo, partes I-IX y anexos A-E)
  output/documento_final/resumen_ejecutivo.md   solo la cabecera y el resumen ejecutivo (PDF de revision_externa/, web y consulta)
  output/documento_final/resultado.json         partes, marcadores y recuento de ids por capa y por clase V18
Falla (código 1) si queda un marcador sin cifra o si el texto incumple las reglas de comprobar() (lenguaje causal fuera de los
anexos técnicos; rótulo de juicio experto en la tabla del resumen y en la contabilidad con magnitudes de la literatura).
Determinista; sin red; solo lee cifras_clave, output/v18/f5/magnitudes.csv y las plantillas.
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ALCANCE_TERRITORIAL = "sin lectura de datos"   # solo lee cifras_clave y salidas ya generadas (guarda de fuga v6 de check_v17)
PLANT = RAIZ / "docs" / "documento_final" / "plantilla"
DIR = RAIZ / "output" / "documento_final"
DOC = DIR / "documento_final.md"
RES = DIR / "resumen_ejecutivo.md"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"
MAG = RAIZ / "output" / "v18" / "f5" / "magnitudes.csv"
JUICIO = "juicio experto con magnitudes de la literatura, no estimación propia"


def _cargar(nombre: str, ruta: Path):
    """Carga un módulo por ruta: «f6_documento» o «check_v18» a secas podrían ser los de otra versión ya importados."""
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _cargar("f6_documento_v18", RAIZ / "src" / "v18" / "f6_documento.py")
C18 = _cargar("check_v18_final", RAIZ / "src" / "v18" / "check_v18.py")

CAB = """# La subida del precio de la vivienda en España: qué sabemos, con qué confianza y qué falta (documento final)

Borja Romero, economista (firma individual, independiente). Documento final del proyecto, preparado para la publicación 2.0: reúne
lo que permiten decir las versiones internas V15 a V18 sobre lo publicado en las anteriores, sin análisis nuevo. Toda cifra procede
de output/v5/cifras_clave.csv con su id, su capa y, en las cifras V18, su clasificación. Lo que es juicio experto va rotulado como tal.
Generado por src/documento_final/documento_final.py (`make documento_final`); no se edita a mano.
"""

# Secciones de nivel 2 en las que se aplica cada regla de lenguaje (texto_causal de check_v18, con las secciones de este documento)
TECNICAS = re.compile(r"^anexo\b", re.I)                          # métodos, réplicas, reproducciones, erratas y pre-registros
ESTRICTAS = re.compile(r"^(?:resumen|executive summary)\b", re.I)  # resumen ejecutivo y su versión inglesa: nada causal


def texto_causal(texto: str, nombre: str) -> list[str]:
    """Como check_v18.texto_causal, con las secciones de este documento: fuera de los anexos, solo líneas que niegan; en los
    resúmenes, nada. Ninguna estimación del proyecto es IDENTIFICADO, de modo que no hay lenguaje causal permitido en el cuerpo."""
    err, seccion = [], ""
    for n, ln in enumerate(texto.splitlines(), 1):
        if ln.startswith("## "):
            seccion = ln[3:].strip()
            continue
        m = C18.CAUSAL_DOC.search(ln)
        if not m or TECNICAS.match(seccion):
            continue
        if ESTRICTAS.match(seccion) or not C18.NEGACION.search(ln):
            err.append(f"{nombre}:{n}: lenguaje causal fuera de los anexos técnicos, sección «{seccion or 'cabecera'}»: {m.group(0)!r}")
    return err


def comprobar(texto: str, nombre: str) -> list[str]:
    err = texto_causal(texto, nombre)
    # el juicio experto va rotulado: la tabla del resumen ejecutivo y la contabilidad con magnitudes de la literatura
    if "Mejor estimación (juicio experto" not in texto:
        err.append(f"{nombre}: la tabla del resumen ejecutivo no rotula la mejor estimación como juicio experto")
    if texto.lower().count(JUICIO) < 2:
        err.append(f"{nombre}: la contabilidad con magnitudes de la literatura no lleva el rótulo «{JUICIO}» (resumen y cuerpo)")
    if "{{" in texto:
        err.append(f"{nombre}: quedan marcadores sin resolver")
    return err


def tabla_erratas() -> str:
    """Índice de la fe de erratas: fecha, versión y fichero de cada entrada de la primera tabla de ERRATA.md (el texto, con sus
    cifras, se queda en ERRATA.md)."""
    filas = []
    for ln in (RAIZ / "ERRATA.md").read_text(encoding="utf-8").split("\n## ", 1)[0].splitlines():
        c = [x.strip() for x in ln.strip().strip("|").split(" | ")]
        if re.match(r"^\d{4}-\d{2}-\d{2}$", c[0]) and len(c) >= 5:
            filas.append(f"| {c[0]} | {c[1]} | {c[2]} |")
    return "\n".join(["| Fecha | Versión | Fichero |", "|---|---|---|"] + filas)


def tabla_preregistros() -> str:
    """Tabla de etiquetas de docs/preregistros.md, tal cual (la genera src/v16/preregistros.py desde git)."""
    t = (RAIZ / "docs" / "preregistros.md").read_text(encoding="utf-8")
    return "\n".join(ln for ln in t.splitlines() if ln.startswith("|"))


TABLAS = {"erratas": tabla_erratas, "preregistros": tabla_preregistros}
TABLA_PROPIA = re.compile(r"\{\{tabla\.(" + "|".join(TABLAS) + r")\}\}")


def ensamblar(ck, mag) -> tuple[str, str, dict]:
    partes = sorted(PLANT.glob("[0-9][0-9]_*.md"))
    trozos, resumen, falta, ids = [CAB], [CAB], [], set()
    for p in partes:
        bruto = p.read_text(encoding="utf-8")
        sin_tablas = TABLA_PROPIA.sub(lambda m: TABLAS[m.group(1)](), D.COMENTARIO.sub("", bruto))
        txt, f = D.render_texto(sin_tablas, ck, mag)
        txt = re.sub(r"\n{3,}", "\n\n", txt).strip() + "\n"
        falta += [f"{p.name}: {i}" for i in f]
        ids |= {m.group(1) for m in D.R.MARC.finditer(bruto) if not m.group(1).startswith("proyecto.")}
        trozos.append(txt)
        if p.name.startswith(("01_", "02_")):   # resumen ejecutivo y su versión inglesa
            resumen.append(txt)
    usados = sorted(i for i in ids if i in ck.index)
    res = dict(rama="documento_final", pregunta="Documento final (publicación 2.0): qué permiten decir V15-V18",
               capa="la de cada cifra citada (sin cifras nuevas)", partes=[p.name for p in partes], marcadores=len(ids),
               ids_por_capa={str(k): int(v) for k, v in ck.loc[usados, "capa"].value_counts().items()},
               ids_v18_por_clasificacion={str(k): int(v) for k, v in ck.loc[[i for i in usados if i.startswith("V18-")],
                                                                              "clasificacion_v18"].value_counts().items()},
               marcadores_sin_cifra=falta, notas="Ensamblado determinista; las cifras vienen de cifras_clave; sin análisis nuevo.")
    return "\n\n".join(trozos), "\n\n".join(resumen), res


def main() -> int:
    ck, mag = D.leer_ck(CK), D.pd.read_csv(MAG)
    texto, resumen, res = ensamblar(ck, mag)
    err = [f"marcador sin cifra: {x}" for x in res["marcadores_sin_cifra"]]
    if not res["partes"]:
        err.append(f"sin plantillas en {PLANT.relative_to(RAIZ)}")
    err += comprobar(texto, str(DOC.relative_to(RAIZ)))
    if err:
        print(f"documento_final: {len(err)} problemas")
        for x in err[:40]:
            print("  -", x)
        return 1
    DIR.mkdir(parents=True, exist_ok=True)
    DOC.write_text(texto, encoding="utf-8")
    RES.write_text(resumen, encoding="utf-8")
    (DIR / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"documento_final: {len(res['partes'])} partes, {res['marcadores']} cifras distintas -> {DOC.relative_to(RAIZ)} y "
          f"{RES.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
