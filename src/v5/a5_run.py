"""A5 run (sin red, determinista): extrae texto de los PDF oficiales de data/raw/v5/programas/, busca por diccionario y escribe salidas.

Entradas: docs/v5/programas/inventario.csv, data/raw/v5/programas/*.pdf, data/raw/v4/medidas_programas.csv.
Salidas: output/v5/A5/*.csv|json, docs/v5/programas/diccionario.md, docs/v5/programas/conciliacion_v4.csv
"""
import csv
import json
import random
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from a5_dict import ALIAS_N, AMBIG_I14, CONTEXT_REQ, D, NEG, NEG_I14, V, WIN  # noqa: E402

SEED = 20261010
random.seed(SEED)
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/v5/programas"
OUT = ROOT / "output/v5/A5"
DOCS = ROOT / "docs/v5/programas"
CTX = re.compile(V + r"|alquiler|lloguer|aluguer|hipotec|arrend|suelo|sol\b|habitac")
SENT_END = re.compile(r"[.;!?•]\s")


def norm(t):
    out = []
    for ch in t:
        d = unicodedata.normalize("NFD", ch)
        out.append(d[0].lower() if d else ch)
    return "".join(out)


def pages_text(pdf):
    """Texto por pagina con pdftotext; si no hay texto (escaneado) usa ocrmypdf (OCR) si esta instalado."""
    def run(p):
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True)
        return r.stdout.split("\f")[:-1] or [""]
    pg = run(pdf)
    metodo = "texto"
    if sum(len(x.split()) for x in pg) < 50 * len(pg):
        tmp = OUT / ("_ocr_" + pdf.name)
        r = subprocess.run(["ocrmypdf", "-l", "spa", "--force-ocr", str(pdf), str(tmp)], capture_output=True)
        if r.returncode == 0:
            pg, metodo = run(tmp), "OCR"
            tmp.unlink()
    out = []
    for x in pg:
        x = re.sub(r"-\n\s*(?=[a-z])", "", x)
        out.append(re.sub(r"\s+", " ", x).strip())
    return out, metodo


def cita(raw, s, e, n=40):
    """Frase que contiene el termino; si supera n palabras, ventana literal de n palabras."""
    a = max([m.end() for m in SENT_END.finditer(raw, 0, s)] or [0])
    m = SENT_END.search(raw, e)
    b = m.start() + 1 if m else len(raw)
    frase = raw[a:b].strip()
    w = frase.split()
    if len(w) <= n:
        return frase, a, b
    pre = raw[a:s].split()
    k = max(0, min(len(pre), n // 2))
    ini = len(pre) - k
    return " ".join(w[ini:ini + n]), a, b


def direccion(ins, win):
    if re.search(NEG_I14 if ins == "I14" else NEG, win):
        return "derogar/reducir"
    if ins == "I14" and re.search(AMBIG_I14, win):
        return "revisar"
    return "a favor/ampliar"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    inv = list(csv.DictReader((DOCS / "inventario.csv").open(encoding="utf-8")))
    comp = {k: [re.compile(t) for t in v[1]] for k, v in D.items()}
    medidas, cnt, textos, estado = [], defaultdict(lambda: defaultdict(set)), {}, {}
    for d in inv:
        if not d["oficial"].startswith("si") or not d["fichero"]:
            continue
        pg, metodo = pages_text(RAW / d["fichero"])
        textos[d["doc_id"]] = pg
        nw = sum(len(x.split()) for x in pg)
        estado[d["doc_id"]] = (metodo, len(pg), nw)
        for pno, raw in enumerate(pg, 1):
            n = norm(raw)
            for ins, rxs in comp.items():
                seen = set()
                for rx in rxs:
                    for m in rx.finditer(n):
                        if ins in CONTEXT_REQ and not CTX.search(n[max(0, m.start() - 250):m.end() + 250]):
                            continue
                        c, a, b = cita(raw, m.start(), m.end())
                        if a in seen:
                            continue
                        seen.add(a)
                        win = n[max(a, m.start() - WIN):m.end()]
                        dr = direccion(ins, win)
                        cnt[(d["doc_id"], ins)][dr].add((pno, a))
                        medidas.append((d["doc_id"], ins, dr, c, pno, "si", metodo, a))
    # una fila por doc x instrumento x direccion x pagina (primera frase), orden determinista
    uniq = {}
    for r in sorted(medidas, key=lambda r: (r[0], r[1], r[4], r[7])):
        uniq.setdefault((r[0], r[1], r[2], r[4]), r)
    rows = list(uniq.values())
    with (OUT / "medidas_programas_v5.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "instrumento", "direccion", "cita", "pagina", "oficial", "metodo"])
        for r in rows:
            w.writerow(r[:7])
    ids = [d["doc_id"] for d in inv if d["doc_id"] in textos]
    with (OUT / "recuentos_doc_instrumento.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "instrumento", "n_frases_a_favor", "n_frases_derogar", "n_paginas"])
        for (did, ins), v in sorted(cnt.items()):
            pgs = {p for s in v.values() for p, _ in s}
            w.writerow([did, ins, len(v["a favor/ampliar"]), len(v["derogar/reducir"]), len(pgs)])
    clase = {d["doc_id"]: ("norma" if d["formacion"] == "Gobierno" else "propuesta") for d in inv}
    docs_cota = {d["doc_id"] for d in inv if "resumen" in d["tipo"]}
    rec = []
    for ins in D:
        def docs(dr, cl):  # noqa: E306
            return {k[0] for k, v in cnt.items() if k[1] == ins and v[dr] and clase[k[0]] == cl}
        fav, con = docs("a favor/ampliar", "propuesta"), docs("derogar/reducir", "propuesta")
        nor = docs("a favor/ampliar", "norma") | docs("derogar/reducir", "norma")
        rec.append([ins, len(fav), len(con), "cota", ";".join(sorted(fav)), ";".join(sorted(con)), ";".join(sorted(nor))])
    with (OUT / "recuentos.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["instrumento", "n_documentos_a_favor", "n_documentos_en_contra", "exhaustivo", "docs_a_favor", "docs_en_contra", "normas_con_coincidencia"])
        w.writerows(rec)
    conciliar(inv, textos, cnt, uniq)
    diccionario(inv, estado)
    n_hits = sum(len(s) for v in cnt.values() for s in v.values())
    res = {
        "rama": "v5/A5", "pregunta": "Que instrumentos de vivienda aparecen en los documentos oficiales programaticos y normativos, y con que direccion",
        "capa": "C4", "datos": "docs/v5/programas/inventario.csv", "N": len(ids),
        "metodo": "pdftotext por pagina + diccionario de terminos (castellano, catalan, gallego) + direccion por regla de verbos de supresion en ventana",
        "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"documentos_oficiales_con_texto": len(ids), "frases_coincidentes": n_hits, "filas_medidas_csv": len(rows),
                         "documentos_cota": sorted(docs_cota), "estado_texto": {k: list(v) for k, v in estado.items()}},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Recuentos de coincidencias de palabras clave, no de medidas validadas una a una; ver validacion_precision.csv. No se evaluan medidas.",
    }
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


def conciliar(inv, textos, cnt, uniq):
    mp = {"PSOE": "A5-D01", "PP": "A5-D02", "Vox": "A5-D04", "Sumar": "A5-D05", "ERC": "A5-D06",
          "EH Bildu": "A5-D07", "PNV": "A5-D08", "BNG": "A5-D09", "UPN": "A5-D10"}
    v4 = list(csv.DictReader((ROOT / "data/raw/v4/medidas_programas.csv").open(encoding="utf-8")))
    rows = []
    hit_pages = defaultdict(set)
    for r in uniq.values():
        hit_pages[(r[0], r[1])].add(r[4])
    for x in v4:
        did = mp[x["partido_o_grupo"]]
        ins = x["instrumento"].split()[0]
        dr = "derogar/reducir" if x["direccion"].startswith("derogar") else "a favor/ampliar"
        if did not in textos:
            rows.append([did, ins, dr, "", "", "", "no verificable: sin documento oficial (excluido)"])
            continue
        full = norm(" ".join(textos[did]))
        pos = [i for i, p in enumerate(textos[did], 1) if " ".join(norm(x["cita_literal"]).split()[:7]) in norm(p)]
        en_txt = "si" if pos else "no"
        ok = bool(pos and pos[0] in hit_pages[(did, ins)])
        dir_v5 = [k for k, v in cnt[(did, ins)].items() if v]
        if ok and dr in dir_v5:
            est = "confirmada"
        elif pos:
            est = "baja del diccionario: cita presente, sin coincidencia de palabra clave en esa pagina"
        else:
            est = "no localizada la cita literal en el texto oficial (puede ser version distinta o salto de linea)"
        _ = full
        rows.append([did, ins, dr, en_txt, pos[0] if pos else "", "si" if ok else "no", est])
    with (DOCS / "conciliacion_v4.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "instrumento_v4", "direccion_v4", "cita_v4_en_texto_oficial", "pagina", "coincide_v5_misma_pagina", "estado"])
        w.writerows(rows)
    # altas: doc x instrumento con v5 y sin v4
    v4set = {(r[0], r[1]) for r in rows}
    altas = []
    for (did, ins), v in sorted(cnt.items()):
        if did in {"A5-D05", "A5-D06", "A5-D07", "A5-D08", "A5-D09", "A5-D10"} and (did, ins) not in v4set:
            altas.append([did, ins, len(v["a favor/ampliar"]), len(v["derogar/reducir"])])
    with (DOCS / "altas_v5_vs_v4.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doc_id", "instrumento", "n_frases_a_favor", "n_frases_derogar"])
        w.writerows(altas)


def diccionario(inv, estado):
    L = ["# Diccionario de palabras clave A5", "",
         "Texto normalizado (minusculas, sin tildes); los terminos son expresiones regulares sobre el texto de cada pagina (pdftotext -layout, lineas unidas, guiones de corte eliminados). Variantes en castellano, catalan (ca) y gallego (gl). Fuente de verdad: `src/v5/a5_dict.py`.", "",
         "## Reglas", "",
         "- Unidad: frase (delimitada por . ; ! ? o vineta) que contiene el termino; una fila por documento x instrumento x direccion x pagina (primera frase). Las paginas son indices del PDF (no la numeracion impresa).",
         "- Instrumentos con contexto obligatorio (hay palabra de vivienda/alquiler/hipoteca/suelo a +-250 caracteres): " + ", ".join(sorted(CONTEXT_REQ)) + ".",
         "- Direccion, regla de v4: `a favor/ampliar` por defecto; `derogar/reducir` si en la frase (hasta " + str(WIN) + " caracteres antes del termino, incluido este) aparece un verbo de supresion: `" + NEG + "`. En I14 (desalojos) los verbos de paralizacion/suspension (`" + AMBIG_I14 + "`) dan `revisar`: pueden describir una medida existente o una propuesta y no se decide automaticamente.",
         "- Alias N de la matriz v4: " + "; ".join(f"{k}={v}" for k, v in ALIAS_N.items()) + ". No se duplican busquedas.",
         "- I17 e I23 no tienen definicion en `docs/v4/instrumentos.md`: no se buscan (registrado como hueco).",
         "- Limites: es una busqueda de candidatos. Una coincidencia no es una medida validada (ver `output/v5/A5/validacion_precision.csv`); una medida redactada sin ninguno de los terminos no se detecta (recall medido contra v4 en `docs/v5/programas/conciliacion_v4.csv`).", "",
         "## Terminos por instrumento", ""]
    for k, (nom, rxs) in D.items():
        L.append(f"### {k} {nom}")
        L.append("")
        L += [f"- `{r}`" for r in rxs] or ["- (sin terminos)"]
        L.append("")
    L += ["## Extraccion de texto por documento", "", "| doc_id | metodo | paginas | palabras |", "|---|---|---|---|"]
    L += [f"| {k} | {v[0]} | {v[1]} | {v[2]} |" for k, v in sorted(estado.items())]
    (DOCS / "diccionario.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
