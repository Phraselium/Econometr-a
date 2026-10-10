"""Control de texto v3 (parte de `make check`).

Comprueba en output/v3/**/*.md, output/v3/verificador/fichas/*.json y docs/v3/hipotesis.md:
1. Léxico valorativo o partidista (partidos, cargos, adjetivos de juicio). Una línea puede eximirse con
   el marcador `<!-- check:ok motivo -->` (p. ej. al citar literalmente una afirmación del debate).
2. Promoción de capa: lenguaje causal en líneas etiquetadas [C1], [C2] o [C4]; ítems [C4] (o [C3] sin
   «robusto») bajo el epígrafe «Afirmable con seguridad»; fichas con capa C4 y veredicto RESPALDADA.
3. Fichas del verificador incompletas (campos obligatorios).
Sale con código 1 si hay errores.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

VALORATIVO = [
    r"escandal\w*", r"vergonz\w*", r"lamentabl\w*", r"desastros\w*", r"catastr[oó]fic\w*", r"bochorn\w*",
    r"demag[oó]g\w*", r"populis\w*", r"bulo\w*", r"mentira\w*", r"menti(?:r|ra|roso)\w*", r"especulador\w*",
    r"fondos? buitre\w*", r"rentistas?", r"acertad\w*", r"fracas\w*", r"obviamente",
    r"indudablemente", r"sin duda", r"evidentemente", r"irresponsab\w*", r"injust\w*",
]
PARTIDISTA = [
    r"PSOE", r"\bPP\b", r"\bVox\b", r"\bSumar\b", r"Podemos", r"\bERC\b", r"\bJunts\b", r"\bBildu\b", r"\bPNV\b",
    r"Ciudadanos\b", r"Compromís", r"S[áa]nchez", r"Feij[óo]o", r"Abascal", r"Ayuso", r"Puigdemont",
    r"\bBNG\b", r"\bUPN\b", r"Coalici[óo]n Canaria", r"\bCUP\b", r"M[áa]s Madrid", r"\bla izquierda\b", r"\bla derecha\b", r"progresistas?", r"conservador(?:es|a)?\b", r"el Gobierno de \w+",
]
CAUSAL = r"\b(caus[aó]\w*|provoc\w*|efecto causal|impacto causal|gracias a|debido a|se debe a|ha hecho (?:subir|bajar))\b"
NEGACION = re.compile(r"(sin evidencia|no se puede afirmar|no identifica|no causal|no implica|no permite|"
                      r"no demuestra|no hay evidencia|como m[áa]ximo|como m[íi]nimo|cota)", re.I)
CAMPOS_FICHA = ["id", "enunciado", "capa", "magnitud", "intervalo", "cota", "literatura", "veredicto", "limites"]
VEREDICTOS = {"RESPALDADA", "PARCIALMENTE", "NO RESPALDADA", "CONTRADICHA", "SIN EVIDENCIA SUFICIENTE",
              "ANALIZADA, NO CONCLUYENTE", "NO ANALIZADA: FALTAN DATOS"}   # las dos últimas, v4
CAPAS = {"C1", "C2", "C3", "C4"}


def _ficheros() -> list[Path]:
    out = [p for v in ("v3", "v4", "v5") for p in sorted((RAIZ / "output" / v).rglob("*.md"))]
    out += sorted((RAIZ / "docs" / "v5" / "plantillas").rglob("*.md"))   # v5: plantillas de entregables
    h = RAIZ / "docs" / "v3" / "hipotesis.md"
    return out + ([h] if h.exists() else [])


def revisar_texto(texto: str, nombre: str) -> list[str]:
    err = []
    seccion = ""
    pat_v = re.compile("|".join(VALORATIVO), re.I)
    pat_p = re.compile("|".join(PARTIDISTA))
    pat_c = re.compile(CAUSAL, re.I)
    for i, linea in enumerate(texto.splitlines(), 1):
        if linea.lstrip().startswith("#"):
            seccion = linea.strip("# ").lower()
        if "check:ok" in linea:
            continue
        if (m := pat_v.search(linea)):
            err.append(f"{nombre}:{i}: léxico valorativo «{m.group(0)}»")
        if (m := pat_p.search(linea)):
            err.append(f"{nombre}:{i}: referencia partidista «{m.group(0)}»")
        capas = set(re.findall(r"\[(C[1-4])\]", linea))
        if capas and "C3" not in capas and pat_c.search(linea) and not NEGACION.search(linea):
            err.append(f"{nombre}:{i}: lenguaje causal en línea {sorted(capas)} (promoción de capa)")
        if seccion.startswith("afirmable con seguridad") and capas:
            if "C4" in capas:
                err.append(f"{nombre}:{i}: ítem C4 en «Afirmable con seguridad»")
            if "C3" in capas and "robust" not in linea.lower():
                err.append(f"{nombre}:{i}: ítem C3 sin «robusto» en «Afirmable con seguridad»")
    return err


def revisar_ficha(f: dict, nombre: str) -> list[str]:
    err = [f"{nombre}: falta el campo «{c}»" for c in CAMPOS_FICHA if c not in f]
    capa, ver = f.get("capa"), f.get("veredicto")
    if capa not in CAPAS:
        err.append(f"{nombre}: capa inválida {capa!r}")
    if ver not in VEREDICTOS:
        err.append(f"{nombre}: veredicto inválido {ver!r}")
    if capa == "C4" and ver in {"RESPALDADA", "CONTRADICHA", "PARCIALMENTE", "NO RESPALDADA"}:   # regla B4 (v4)
        err.append(f"{nombre}: capa C4 no puede sostener el veredicto {ver} (promoción de capa)")
    texto = " ".join(str(f.get(k, "")) for k in ("magnitud", "limites", "resumen"))
    if capa != "C3" and re.search(CAUSAL, texto, re.I) and not NEGACION.search(texto):
        err.append(f"{nombre}: lenguaje causal con capa {capa}")
    # v5 (revisión B): atribución en fichas C4 de módulos v5 («puede explicar», «contribuye», «el efecto»)
    if capa == "C4" and nombre.startswith("output/v5/") and (m := re.search(r"\b(puede explicar|explica[nr]?|contribuy\w*|el efecto de)\b", texto, re.I)):
        err.append(f"{nombre}: verbo de atribución «{m.group(0)}» con capa C4")
    err += [e.replace("<texto>", nombre) for e in revisar_texto(json.dumps(f, ensure_ascii=False), nombre)
            if "valorativo" in e or "partidista" in e]
    return err


def main() -> int:
    errores = []
    for p in _ficheros():
        errores += revisar_texto(p.read_text(encoding="utf-8"), str(p.relative_to(RAIZ)))
    fichas = [p for v in ("v3", "v4", "v5") for p in sorted((RAIZ / "output" / v / "verificador" / "fichas").glob("*.json"))]
    for p in fichas:
        errores += revisar_ficha(json.loads(p.read_text(encoding="utf-8")), str(p.relative_to(RAIZ)))
    # v5: fichas de módulo (listas) antes de pasar al verificador
    for p in sorted((RAIZ / "output" / "v5").glob("*/fichas_verificador.json")):
        for f in json.loads(p.read_text(encoding="utf-8")):
            errores += revisar_ficha(f, f"{p.relative_to(RAIZ)}#{f.get('id')}")
    for e in errores:
        print(e)
    print(f"check_texto: {len(errores)} errores")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
