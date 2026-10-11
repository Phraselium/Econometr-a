"""K4c · Coherencia de cifras: cada cifra significativa de entregables/fichas/posts frente a output/v5/cifras_clave.csv.

Clases: EN_CIFRAS_CLAVE · HISTORICA_MARCADA · HUERFANA · CONTRADICTORIA · SIN_FECHA (cifra en cifras_clave, sin año del dato
en su frase). Determinista y sin red. Salidas: output/v6_1/K4C/cifras_entregables.csv y resumen.md.
Cifra significativa: con decimales, con % , con separador de miles, o entero >= 10 que no sea un año (1900-2100) ni
numeración (listas, apartados «3.1», fechas, ids tipo A23-A10, notas a pie, URL/DOI, código).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "output" / "v5"
OUT = ROOT / "output" / "v6_1" / "K4C"
PUB_DOCS = ("calendario_publicacion.md", "licencias_datos.md", "literatura_instrumentos.md")

NUM = re.compile(r"(?<![\w.,/\-])(-?\d{1,3}(?:\.\d{3})+(?:,\d+)?|-?\d+(?:,\d+)?)(\s?%)?(?![\w/])")
HIST = re.compile(r"hist[óo]ric|\bv[345]\b|versi[óo]n anterior|superad[oa]|retirad[oa]", re.I)
ANIO = re.compile(r"\b(19[5-9]\d|20[0-4]\d)\b")
# Excepciones documentadas (fichero, cifra): parámetros de método, códigos HTTP y recuentos de repositorio que no son cifras de resultado.
EXCEPCIONES = {
    ("output/v5/working_paper.md", "200"),  # B=200 permutaciones (parámetro del control sintético)
    ("README_REPLICACION.md", "7.564"), ("README_REPLICACION.md", "7.776"), ("README_REPLICACION.md", "154"),  # recuentos de especificaciones/ficheros
    ("docs/v5/literatura_instrumentos.md", "403"), ("docs/v5/literatura_instrumentos.md", "429"),  # códigos HTTP de Crossref/Scimago
    ("docs/v5/literatura_instrumentos.md", "400"),
    ("output/v5/correo_coev.md", "2.000"),  # extensión pedida del artículo (palabras)
}
# Revisión manual de las CONTRADICTORIA heurísticas del verificador (misma redacción, otro indicador): no son contradicciones reales.
REVISION_MANUAL = {
    ("output/v5/verificador/verificador.md", "45,2%"): "falso positivo: cota de población extranjera, no el precio A23-P2",
    ("output/v5/verificador/verificador.md", "2,26"): "huérfana de ficha: pp de la v2 (B4), no es el máximo de VUT",
    ("output/v5/verificador/verificador.md", "470"): "redondeo de 471,8 mil millones (CA-CR-saldo-pico); diferencia 0,4 %",
    ("output/v5/verificador/verificador.md", "2.333.816"): "falso positivo: solo vivienda habitual; CB-C6-03 es habitual y otras",
}
STOP = {"de", "la", "el", "en", "los", "las", "del", "y", "a", "que", "por", "con", "un", "una", "para", "se", "al", "es", "o", "su", "como", "más", "entre"}


def ficheros() -> list[Path]:
    fs = sorted(V5.glob("*.md"))
    fs = [f for f in fs if f.name != "cifras_clave.md"]
    for sub in ("articulos", "ponencia", "linkedin", "verificador"):
        fs += sorted((V5 / sub).glob("*.md"))
    fs += sorted((ROOT / "archive").rglob("*.md"))
    fs += [ROOT / "README.md", ROOT / "README_REPLICACION.md"]
    fs += [ROOT / "docs" / "v5" / n for n in PUB_DOCS if (ROOT / "docs" / "v5" / n).exists()]
    return [f for f in fs if f.exists()]


def a_float(tok: str) -> tuple[float, int]:
    """Número en formato español -> (valor, decimales)."""
    t = tok.strip()
    if re.fullmatch(r"-?0\.\d+", t):  # decimal con punto (estadísticos): 0.762
        return float(t), len(t.split(".")[1])
    if "," in t:
        ent, dec = t.rsplit(",", 1)
        return float(ent.replace(".", "") + "." + dec), len(dec)
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", t):
        return float(t.replace(".", "")), 0
    return float(t), 0


def cargar_ck() -> pd.DataFrame:
    ck = pd.read_csv(V5 / "cifras_clave.csv")
    ck["pal"] = ck.indicador.astype(str).str.lower().map(lambda s: {w for w in re.findall(r"[a-záéíóúñ0-9]+", s) if w not in STOP and len(w) > 2})
    return ck


def valores_ck(ck: pd.DataFrame) -> list[float]:
    vs = set()
    for c in ("valor", "min", "max"):
        for v in ck[c].dropna():
            v = float(v)
            vs.update({v, abs(v)})
            if abs(v) <= 1.5:
                vs.add(v * 100)
            vs.add(v / 1000)  # «1,2 mil»
            vs.add(v / 1e6)  # «1,2 millones»
    return sorted(vs)


def en_ck(x: float, dec: int, vs: list[float]) -> bool:
    tol = 0.5 * 10 ** (-dec) + 1e-9
    xs = {x, abs(x)}
    return any(abs(v - a) <= tol for v in vs for a in xs)


def limpiar(txt: str) -> list[tuple[int, str]]:
    """Devuelve (nº de línea, texto con lo no numérico neutralizado)."""
    res, fence = [], False
    txt = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), txt, flags=re.S)
    for i, ln in enumerate(txt.split("\n"), 1):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if fence or re.match(r"\s*\[\^[^\]]+\]:", ln):
            continue
        ln = re.sub(r"\]\([^)]*\)", "]", ln)  # destinos de enlace
        ln = re.sub(r"https?://\S+|doi:\S+|10\.\d{4,}/\S+", " ", ln)
        ln = re.sub(r"`[^`]*`", " ", ln)  # código en línea
        ln = re.sub(r"\[\^\d+\]", " ", ln)
        ln = re.sub(r"=\s?\d\.\d+", " ", ln)  # estadísticos con punto decimal (p=0.762)
        ln = re.sub(r"\bpor 1\.000\b", " ", ln)  # unidad «por 1.000 hab.»
        ln = re.sub(r"\d+\(\d+\)(,\s*\d+[\-–]\d+)?|\([A-Za-z]+ \d+\)|,\s*\d+[\-–]\d+\)", " ", ln)  # volumen(número), páginas de revista
        ln = re.sub(r"\b\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}\b|\b\d{4}-\d{2}(-\d{2})?\b|\bT[1-4]\b|\b[1-4]T\b", " ", ln)  # fechas, trimestres
        ln = re.sub(r"^\s*(#+\s*)?(\d+(\.\d+)*[.)]?)\s+", lambda m: (m.group(1) or "") + " ", ln)  # numeración
        ln = re.sub(r"\b[A-Za-z]{1,4}\d*[A-Za-z]*-\d+[A-Za-z0-9\-]*\b", " ", ln)  # ids A23-A10
        ln = re.sub(r"\b(?:tabla|figura|apartado|secci[óo]n|anexo|p\.|pp\.|n\.º|nº|hip[óo]tesis|H|R)\s*\d+(?:[.,]\d+)*", " ", ln, flags=re.I)
        res.append((i, ln))
    return res


def frase(lineas: list[tuple[int, str]], k: int, pos: int, bloque: bool = False) -> str:
    ln = lineas[k][1]
    if ln.lstrip().startswith("|") and not bloque:
        return ln
    if ln.lstrip().startswith("|"):  # tabla: el año puede estar en cualquier fila del bloque
        a = k
        while a > 0 and lineas[a - 1][1].lstrip().startswith("|"):
            a -= 1
        b = k
        while b + 1 < len(lineas) and lineas[b + 1][1].lstrip().startswith("|"):
            b += 1
        return " ".join(x[1] for x in lineas[a:b + 1])
    ini = max([m.end() for m in re.finditer(r"(?<=[.!?])\s+|\n", ln[:pos])] or [0])
    m = re.search(r"(?<=[.!?])\s", ln[pos:])
    return ln[ini: pos + (m.start() if m else len(ln))]


def contradice(tok_x: float, unidad_pct: bool, fr: str, ck: pd.DataFrame) -> str | None:
    """Fila de cifras_clave de la misma unidad cuyo indicador comparte >=3 palabras con la frase y valor próximo (±35%)."""
    pal = {w for w in re.findall(r"[a-záéíóúñ0-9]+", fr.lower()) if w not in STOP and len(w) > 2}
    mejor = None
    for r in ck.itertuples():
        if pd.isna(r.valor) or (r.unidad == "%") != unidad_pct:
            continue
        com = len(pal & r.pal)
        if com >= 3 and r.valor != 0 and abs(tok_x - r.valor) / abs(r.valor) <= 0.35 and (mejor is None or com > mejor[0]):
            mejor = (com, r.id)
    return mejor[1] if mejor else None


def escanear() -> pd.DataFrame:
    ck = cargar_ck()
    vs = valores_ck(ck)
    filas = []
    for f in ficheros():
        rel = f.relative_to(ROOT).as_posix()
        es_arch = rel.startswith("archive/")
        txt = f.read_text(encoding="utf-8")
        lineas = limpiar(txt)
        for k, (n, ln) in enumerate(lineas):
            for m in NUM.finditer(ln):
                tok = m.group(1)
                x, dec = a_float(tok)
                pct = bool(m.group(2))
                if not (dec > 0 or pct or "." in tok or abs(x) >= 10):
                    continue
                if dec == 0 and not pct and "." not in tok and 1900 <= abs(x) <= 2100:
                    continue  # año
                if dec == 0 and not pct and "." not in tok and abs(x) >= 1000 and not en_ck(x, dec, vs):
                    continue  # código (tabla INE, semilla, HTTP): una cifra >= 1000 se escribe con separador de miles
                if (rel, tok) in EXCEPCIONES:
                    continue
                fr = frase(lineas, k, m.start())
                fr_anio = frase(lineas, k, m.start(), bloque=True)
                if es_arch or HIST.search(ln):
                    clase, ref = "HISTORICA_MARCADA", ""
                elif en_ck(x, dec, vs):
                    clase, ref = ("EN_CIFRAS_CLAVE" if ANIO.search(fr_anio) else "SIN_FECHA"), ""
                else:
                    ref = contradice(x, pct, fr, ck)
                    clase = "CONTRADICTORIA" if ref else "HUERFANA"
                filas.append({"fichero": rel, "linea": n, "cifra": tok + ("%" if pct else ""), "clase": clase,
                              "id_ref": ref or "", "frase": re.sub(r"\s+", " ", fr).strip()[:160],
                              "revision_manual": REVISION_MANUAL.get((rel, tok + ("%" if pct else "")), "")})
    return pd.DataFrame(filas)


def resumen(df: pd.DataFrame) -> str:
    cl = ["EN_CIFRAS_CLAVE", "HISTORICA_MARCADA", "SIN_FECHA", "HUERFANA", "CONTRADICTORIA"]
    t = df.pivot_table(index="fichero", columns="clase", values="cifra", aggfunc="count", fill_value=0).reindex(columns=cl, fill_value=0)
    t["total"] = t.sum(axis=1)
    out = ["# K4c · Coherencia de cifras (resumen)", "", f"Cifras significativas analizadas: {len(df)}. Fuente de verdad: output/v5/cifras_clave.csv.", "",
           "## Recuentos globales", "", "| clase | n |", "|---|---|"]
    out += [f"| {c} | {int((df.clase == c).sum())} |" for c in cl]
    out += ["", "## Recuentos por fichero", "", "| fichero | " + " | ".join(cl) + " | total |", "|---|" + "---|" * (len(cl) + 1)]
    out += [f"| {i} | " + " | ".join(str(int(r[c])) for c in cl) + f" | {int(r.total)} |" for i, r in t.iterrows()]
    for c, tit in (("CONTRADICTORIA", "Contradictorias (prioridad 1)"), ("HUERFANA", "Huérfanas (prioridad 2; primeras 60)")):
        d = df[df.clase == c]
        out += ["", f"## {tit}", ""]
        out += [f"- {r.fichero}:{r.linea} · {r.cifra} · {r.id_ref} · «{r.frase[:110]}»" + (f" → REVISADA: {r.revision_manual}" if isinstance(r.revision_manual, str) and r.revision_manual else "") for r in d.head(60).itertuples()] or ["(ninguna)"]
    return "\n".join(out) + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = escanear()
    df.to_csv(OUT / "cifras_entregables.csv", index=False)
    (OUT / "resumen.md").write_text(resumen(df), encoding="utf-8")
    print(df.clase.value_counts().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
