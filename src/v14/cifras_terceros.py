"""V14.1-B3 · Cifras de cifras_clave que dependen de Notariado, Registradores o AEAT → docs/v14/cifras_terceros.{md,csv}.

Sirve para que el autor revise las licencias. No cambia ninguna cifra: solo lee output/v5/cifras_clave.csv y los textos.
Clasificación de la dependencia:
- «directa»: la fuente se nombra en `fuentes`, `indicador` o el id (Notariado/CGN; Registradores/ERI; AEAT/IRPF).
- «indirecta (estadística oficial)»: AEAT solo aparece como origen de una estadística publicada por el INE o el MIVAU (IPVA,
  SERPAVI). El dato se descarga de esos organismos y va en el depósito.
- Si `fuentes` u `origen` remiten a un panel cuyos datos de entrada incluyen series de esas fuentes (PANELES), se miran los
  scripts del módulo (src/<versión>/<módulo>*.py; en V8, también los módulos M<n> que nombra `fuentes`):
  - «indirecta (el modelo usa la serie)»: algún script lee columnas de Notariado o Registradores;
  - «técnica (panel con terceros; el modelo no usa la serie)»: ningún script las lee. La cifra no contiene datos de esas
    fuentes, pero recalcularla exige reconstruir un panel que sí los contiene.
¿Se reproduce en el árbol público?
- «sí»: indirecta vía estadística oficial;
- «solo con datos_terceros»: Notariado o Registradores;
- «no»: AEAT directa (licencia no abierta, D4).
Dónde aparece: el id en las plantillas y los textos de publicacion/ (sin cifras_clave.csv), en consulta/ y en el código y las
plantillas de la web. Determinista; sin red.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "docs" / "v14"
FUENTES = {
    "Notariado": re.compile(r"notar|\bCGN\b", re.I),
    "Registradores": re.compile(r"registrador|\bERI\b|registr_pm2|registr_num|Colegio de Registradores", re.I),
    "AEAT": re.compile(r"\bAEAT\b|IRPF|Agencia Tributaria|aeat_irpf", re.I),
}
OFICIAL = re.compile(r"(IPVA|SERPAVI)[^;]*\(?[^;]*AEAT|AEAT[^;]*\)?[^;]*(IPVA|SERPAVI)|INE IPVA \(AEAT\)|SERPAVI \(AEAT", re.I)
# paneles o módulos cuyos datos de entrada incluyen series de Notariado o Registradores (cabeceras comprobadas en V14)
PANELES = {
    "nacional_q_v8": "Notariado y Registradores", "cv_prov_q_v8": "Notariado y Registradores", "nacional_q_v2": "Notariado y Registradores",
    "panel_ccaa_a": "Notariado y Registradores", "nacional_q.csv": "Notariado y Registradores",
    "prov_compra_anual_train": "Registradores", "output/v6/M0/paneles": "Registradores (panel provincial de compra)",
    "B3 (MIVAU y Registradores)": "Registradores",
}
USA = re.compile(r"registr_pm2|registr_num|notariado_|registradores|_registr\b|pm2_registr|ln_cv_registr", re.I)


def _scripts(r) -> list[Path]:
    """Scripts del módulo de una cifra: por su origen (output/<v>/<MOD>/) y, en V8, por los M<n> o F<n> que nombra fuentes."""
    fs = set()
    m = re.match(r"output/(v[0-9_]+)/([A-Za-z0-9]+)/", str(r.origen))
    if m:
        fs |= set((RAIZ / "src" / m.group(1)).glob(f"{m.group(2).lower()}*.py"))
    if str(r.origen).startswith("output/v8/"):
        for mod in re.findall(r"\b([MF]\d)\b", str(r.fuentes)):
            fs |= set((RAIZ / "src" / "v8").glob(f"{mod.lower()}_*.py"))
        if mod_m := re.search(r"V8-(M\d)", r.id):
            fs |= set((RAIZ / "src" / "v8").glob(f"{mod_m.group(1).lower()}_*.py"))
    return sorted(fs)


CONDICIONES = [
    ("Notariado (Consejo General del Notariado)", "https://www.notariado.org/portal/aviso-legal"),
    ("Notariado: portal estadístico", "https://www.notariado.org/portal/estad%C3%ADsticas"),
    ("Registradores (Colegio de Registradores): aviso legal", "https://www.registradores.org/aviso-legal"),
    ("Registradores: portal estadístico registral", "https://www.registradores.org/actualidad/portal-estadistico-registral"),
    ("Registradores: datos abiertos", "https://opendata.registradores.org"),
    ("AEAT: aviso legal, propiedad intelectual", "https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica/aviso-legal/propiedad-intelectual.html"),
    ("AEAT: condiciones de uso de la sede", "https://sede.agenciatributaria.gob.es/Sede/condiciones-uso-sede-electronica.html"),
    ("AEAT: estadísticas", "https://sede.agenciatributaria.gob.es/Sede/estadisticas.html"),
]


def _anexo() -> dict[str, str]:
    out = {}
    for ln in (RAIZ / "metodologia" / "anexo_metodologico.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^###\s+(A\d+(?:-A\d+)?)\.\s+(.+?):", ln)
        if m:
            for i in re.findall(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*", m.group(2)):
                out.setdefault(i, m.group(1))
    return out


def _textos() -> dict[str, str]:
    def junta(rutas):
        return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in rutas if p.is_file())
    pub = [p for p in (RAIZ / "publicacion").rglob("*.md")] + list((RAIZ / "docs").glob("**/plantillas/**/*.md"))
    web = [RAIZ / "src" / "v10" / "web.py"] + list((RAIZ / "web" / "plantillas").rglob("*"))
    return {"publicacion": junta(pub), "consulta": junta(list((RAIZ / "consulta").rglob("*"))), "web": junta(web)}


def clasificar() -> pd.DataFrame:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv")
    anexo, textos = _anexo(), _textos()
    filas = []
    for r in ck.itertuples():
        texto = f"{r.id} {r.indicador} {r.fuentes}"
        for fuente, pat in FUENTES.items():
            tipo = ""
            if pat.search(texto):
                tipo = "indirecta (estadística oficial)" if fuente == "AEAT" and OFICIAL.search(str(r.fuentes)) and not re.search(
                    r"declarantes|aeat_irpf|IRPF (municip|por municipios)", texto, re.I) else "directa"
            elif fuente in ("Notariado", "Registradores"):
                for k, v in PANELES.items():
                    if k in f"{r.fuentes} {r.origen}" and fuente in v:
                        scr = _scripts(r)
                        usa = any(USA.search(p.read_text(encoding="utf-8", errors="ignore")) for p in scr)
                        tipo = ("indirecta (el modelo usa la serie)" if usa else "técnica (panel con terceros; el modelo no usa la serie)")
                        break
            if not tipo:
                continue
            reproduce = ("sí" if tipo.startswith("indirecta (estadística") else "no" if fuente == "AEAT" else "solo con datos_terceros")
            aparece = [k for k, t in textos.items() if re.search(rf"(?<![\w-]){re.escape(r.id)}(?![\w-])", t)]
            filas.append({"fuente": fuente, "id": r.id, "enunciado": r.indicador, "capa": r.capa, "fuentes": r.fuentes,
                          "ficha_anexo": anexo.get(r.id, "—"), "origen": r.origen, "dependencia": tipo, "reproduce_arbol_publico": reproduce,
                          "aparece_en": ", ".join(aparece) or "solo cifras_clave"})
    return pd.DataFrame(filas).sort_values(["fuente", "dependencia", "id"]).reset_index(drop=True)


def _md(d: pd.DataFrame) -> str:
    L = ["# V14.1 · Cifras de cifras_clave que dependen de Notariado, Registradores o AEAT", "",
         "Generado por src/v14/cifras_terceros.py (`python3 src/v14/cifras_terceros.py`) para la revisión de licencias del autor. "
         "No cambia ninguna cifra. La lista completa, en [cifras_terceros.csv](cifras_terceros.csv).", "",
         "**Cómo leerlo.**",
         "- La **dependencia** es «directa» si la fuente se nombra en la cifra.",
         "- Es «indirecta (estadística oficial)» si solo es el origen de una estadística del INE o del MIVAU (IPVA, SERPAVI).",
         "- Es «indirecta (el modelo usa la serie)» si la cifra sale de un módulo cuyos scripts leen columnas de esas fuentes.",
         "- Es «técnica» si la cifra sale de un panel que contiene esas series, pero ningún script de su módulo las lee. La cifra no lleva datos de la fuente; recalcularla exige reconstruir el panel.",
         "- **Reproduce en el árbol público** dice si la cifra se puede recalcular allí: «sí»; «solo con datos_terceros»; o «no» (AEAT, licencia no abierta).",
         "- **Aparece en** dice dónde está el id: publicacion/ (o sus plantillas), consulta/ o la web.", "",
         "## Resumen por fuente", "", "| Fuente | Dependencia | Cifras | Reproduce en el árbol público | En publicacion/ | En consulta/ | En la web |", "|---|---|---|---|---|---|---|"]
    for (f, t), g in d.groupby(["fuente", "dependencia"], sort=True):
        L.append(f"| {f} | {t} | {len(g)} | {', '.join(sorted(set(g.reproduce_arbol_publico)))} | "
                 f"{g.aparece_en.str.contains('publicacion').sum()} | {g.aparece_en.str.contains('consulta').sum()} | {g.aparece_en.str.contains('web').sum()} |")
    n_ids = d.id.nunique()
    L += ["", f"Total: {len(d)} filas, {n_ids} cifras distintas. Una cifra que depende de más de una fuente aparece una vez por fuente.", ""]
    for f, g in d.groupby("fuente", sort=True):
        L += [f"## {f} ({len(g)} cifras)", "", "| id | Enunciado publicado | Capa | Fuentes | Ficha del anexo | Dependencia | Reproduce | Aparece en |", "|---|---|---|---|---|---|---|---|"]
        for r in g.itertuples():
            enun = str(r.enunciado).replace("|", "/")
            L.append(f"| {r.id} | {enun} | {r.capa} | {str(r.fuentes).replace('|', '/')} | {r.ficha_anexo} | {r.dependencia} | {r.reproduce_arbol_publico} | {r.aparece_en} |")
        L.append("")
    L += ["## Condiciones de uso de cada fuente (para que el autor las lea)", "",
          "Solo se enlazan; aquí no se interpretan.", ""]
    L += [f"- {n}: {u}" for n, u in CONDICIONES]
    return "\n".join(L) + "\n"


def main() -> int:
    d = clasificar()
    SAL.mkdir(parents=True, exist_ok=True)
    d.to_csv(SAL / "cifras_terceros.csv", index=False)
    (SAL / "cifras_terceros.md").write_text(_md(d), encoding="utf-8")
    print("cifras_terceros:", d.groupby(["fuente", "dependencia"]).size().to_dict(), f"· {d.id.nunique()} cifras distintas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
