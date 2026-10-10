"""v3: municipios catalanes con régimen de contención de rentas (Ley 11/2020) y zonas de mercado
residencial tensionado (Ley 12/2023) declaradas por la Generalitat y publicadas en el BOE.

Fuentes (todas oficiales, sin scraping de portales no autorizados):
  1. Ley 11/2020, de 18 de septiembre (DOGC núm. 8229, 21/09/2020). Disposición transitoria segunda y anexo
     («Municipios incluidos en la declaración transitoria de áreas con mercado de vivienda tenso»).
     Texto consolidado BOE (versión 2020-10-01, tras Decreto-ley 33/2020, que modificó el anexo): 61 municipios.
     Versión 2020-09-21 (texto original): 60 municipios. Se usa la versión consolidada (61).
     La STC 37/2022, de 10 de marzo (BOE-A-2022-5807, publicada en el BOE el 08/04/2022) anuló los arts. 1, 6 a 13,
     15, 16.2 y DA 1 a 4 y las DT 1 y 4.b; la DT segunda (declaración transitoria) no se anuló y caducó a
     su año de duración (entrada en vigor 22/09/2020).
  2. Ley 12/2023 (art. 18): relaciones trimestrales de zonas tensionadas publicadas en el BOE mediante
     Resolución de la Secretaría de Estado de Vivienda y Agenda Urbana. Se parsean las filas «Cataluña» de cada
     resolución de data/raw/v3/zonas_tensionadas_v3.csv (solo lectura) y se cruzan con el texto BOE.

Salida: data/raw/v3/cataluna_contencion_rentas_v3.csv
Columnas: cod_ine, municipio, norma, fecha_publicacion, fecha_vigencia_inicio, fecha_vigencia_fin,
          regimen, url_oficial, verificado.
Validaciones: nº de municipios frente al que cita la norma; códigos INE presentes en
              data/raw/v3/incasol_fianzas_municipio_v3.csv.gz (columna codigo, nivel MUN).
Caché: si el CSV de salida existe no se rehace (FORCE=1 para rehacer). Los HTML del BOE se cachean en
       data/raw/v3/originales/cataluna_contencion/.
"""
from __future__ import annotations

import datetime as dt
import fcntl
import html as htmllib
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from utils_fetch import FORCE, MANIFEST, RAW, download  # noqa: E402

OUT = RAW / "v3" / "cataluna_contencion_rentas_v3.csv"
ORIG = RAW / "v3" / "originales" / "cataluna_contencion"
ZONAS = RAW / "v3" / "zonas_tensionadas_v3.csv"
INCASOL = RAW / "v3" / "incasol_fianzas_municipio_v3.csv.gz"
FAILS = ROOT / "docs" / "v3" / "fuentes_fallidas.md"
COLS = ["cod_ine", "municipio", "norma", "fecha_publicacion", "fecha_vigencia_inicio",
        "fecha_vigencia_fin", "regimen", "url_oficial", "verificado"]
UA = {"User-Agent": "econometria-vivienda-tfm/1.0 (investigacion academica)"}
BOE_TXT = "https://www.boe.es/diario_boe/txt.php?id={}"
LEY11_CON = "https://www.boe.es/eli/es-ct/l/2020/09/18/11/con/{}"
# Anexo de la Ley 11/2020: versión consolidada tras DL 33/2020 (61) y versión original (60)
LEY11_ANEXO_NUEVO = ("20201001", 61)
LEY11_ANEXO_ORIG = ("20200921", 60)
BOE_LEY11 = "BOE-A-2020-11363"
BOE_STC = "BOE-A-2022-5807"
# cod_ine erróneos en zonas_tensionadas_v3.csv (Rubí = 08184 en Incasòl; Mont-roig del Camp = 43092)
ZONAS_ERRATA = {("BOE-A-2024-5214", "08085"): "08184", ("BOE-A-2024-20576", "17110"): "43092"}
STC_PUB_BOE = "2022-04-08"
ALIAS = {  # variantes ortográficas BOE/anexo -> nombre INE/Incasòl
    "santa perpetua de la mogoda": "santa perpetua de mogoda",
    "sant adria de besos": "sant adria de besos",
    "pineda": "pineda de mar",  # anexo Ley 11/2020: «Pineda» = Pineda de Mar (08163)
    "castell d aro platja d aro i s agaro": "castell platja d aro",  # 17048
}
# Erratas del texto BOE en la lista de municipios (coma ausente / conjunción «i» suelta)
BOE_LIST_FIX = {
    "Castell d'Aro, Platja d'Aro i S'Agaró": "@@CASTELL@@",
    "Manresa el Masnou": "Manresa, el Masnou",
    "i Vilassar de Mar": "Vilassar de Mar",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("’", "'"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^a-z0-9' ]", " ", s).replace("'", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return ALIAS.get(s, s)


def boe_text(id_or_eli: str, url: str, name: str) -> str:
    """Descarga (con caché) y convierte HTML a texto plano por líneas."""
    p = download(url, ORIG / name)
    t = p.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<br\s*/?>|</p>|</div>|</tr>|</h\d>|</li>", "\n", t)
    t = htmllib.unescape(re.sub(r"<[^>]+>", "", t))
    return re.sub(r"[ \t\xa0]+", " ", t)


def anexo_ley11(t: str) -> list[str]:
    i = t.find("Municipios incluidos")
    j = t.find("Por tanto", i)
    seg = t[i:j]
    return [m.strip() for m in re.findall(r"(?:\d+\.|–)\s*([^\n.]+)\.", seg)]


def catalan_list(t: str) -> list[str]:
    """Lista de municipios de la fila «Cataluña.» de una resolución SEVAU (Ley 12/2023, art. 18)."""
    lines = [l.strip() for l in t.split("\n")]
    for k, l in enumerate(lines):
        if l == "Cataluña.":
            nxt = next(x for x in lines[k + 1:] if x)
            for bad, good in BOE_LIST_FIX.items():
                nxt = nxt.replace(bad, good)
            nxt = nxt.replace("@@CASTELL@@", "Castell-Platja d'Aro")
            return [s.strip().rstrip(".") for s in nxt.split(", ") if s.strip()]
    return []


def main() -> None:
    if OUT.exists() and not FORCE:
        print(f"[cache] {OUT.relative_to(ROOT)}")
        return

    # Municipios INE/Incasòl (nivel MUN) para validar códigos y mapear nombres
    inc = pd.read_csv(INCASOL, dtype=str, usecols=["territorio", "nivel", "codigo"])
    inc = inc[inc["nivel"] == "MUN"].drop_duplicates(["codigo"])
    codes_ok = set(inc["codigo"])
    name2code = {norm(t): c for t, c in zip(inc["territorio"], inc["codigo"])}

    zon = pd.read_csv(ZONAS, dtype=str)
    zc = zon[zon["ccaa"] == "Cataluña"].copy()
    for t, c in zip(zc["municipio_resolucion"], zc["cod_ine_municipio"]):
        name2code.setdefault(norm(t), c)
    fallidos: list[str] = []

    def to_code(name: str) -> str | None:
        return name2code.get(norm(name))

    rows: list[dict] = []
    checks: list[str] = []

    # 1) Ley 11/2020, anexo (disposición transitoria segunda)
    t_new = boe_text(LEY11_CON, LEY11_CON.format(LEY11_ANEXO_NUEVO[0]), f"boe_ley11_con{LEY11_ANEXO_NUEVO[0]}.html")
    t_orig = boe_text(LEY11_CON, LEY11_CON.format(LEY11_ANEXO_ORIG[0]), f"boe_ley11_con{LEY11_ANEXO_ORIG[0]}.html")
    t_pub = boe_text(BOE_LEY11, BOE_TXT.format(BOE_LEY11), f"{BOE_LEY11}.html")
    annex_new, annex_orig = anexo_ley11(t_new), anexo_ley11(t_orig)
    checks.append(f"Ley11 anexo consolidado 2020-10-01: {len(annex_new)} (esperado {LEY11_ANEXO_NUEVO[1]})")
    checks.append(f"Ley11 anexo original 2020-09-21: {len(annex_orig)} (esperado {LEY11_ANEXO_ORIG[1]})")
    checks.append("Ley11 publicada en DOGC 8229 el 21/09/2020: " + str("DOGC núm. 8229, de 21 de septiembre de 2020" in t_pub))
    checks.append("STC 37/2022 BOE núm. 84 (08/04/2022) en texto BOE: " + str("8 de abril de 2022" in boe_text(BOE_STC, BOE_TXT.format(BOE_STC), f"{BOE_STC}.html") or "BOE núm. 84" in boe_text(BOE_STC, BOE_TXT.format(BOE_STC), f"{BOE_STC}.html")))
    if len(annex_new) != LEY11_ANEXO_NUEVO[1]:
        raise SystemExit("ERROR: nº de municipios del anexo Ley 11/2020 no coincide")
    norma11 = ("Ley 11/2020, de 18 de septiembre (DOGC núm. 8229; BOE-A-2020-11363), disposición transitoria "
               "segunda y anexo, versión consolidada tras Decreto-ley 33/2020; anulada en parte por STC 37/2022 "
               f"(BOE-A-2022-5807, publicada {STC_PUB_BOE})")
    for n in annex_new:
        c = to_code(n)
        if c is None:
            fallidos.append(f"Ley11 sin código INE: {n}")
            continue
        rows.append(dict(cod_ine=c, municipio=n, norma=norma11, fecha_publicacion="2020-09-21",
                         fecha_vigencia_inicio="2020-09-22", fecha_vigencia_fin="2021-09-21",
                         regimen="ley11_2020", url_oficial=LEY11_CON.format(LEY11_ANEXO_NUEVO[0]),
                         verificado="sí"))

    # 2) Ley 12/2023: resoluciones SEVAU del BOE que contienen filas «Cataluña»
    boe_ids = sorted(zon["resolucion_boe"].dropna().unique())
    for bid in boe_ids:
        t = boe_text(bid, BOE_TXT.format(bid), f"{bid}.html")
        names = catalan_list(t)
        sub = zc[zc["resolucion_boe"] == bid]
        if not names:
            checks.append(f"{bid}: sin filas Cataluña en el BOE (CSV Cataluña: {len(sub)})")
            continue
        checks.append(f"{bid}: BOE Cataluña {len(names)} municipios; CSV Cataluña {len(sub)}")
        if len(sub):
            csv_set = set(sub["cod_ine_municipio"])
            boe_set = {to_code(n) for n in names}
            # Erratas conocidas en zonas_tensionadas_v3.csv (solo lectura): se usa el código validado en Incasòl/BOE
            csv_set = {ZONAS_ERRATA.get((bid, c), c) for c in csv_set}
            if csv_set != boe_set:
                fallidos.append(f"{bid}: códigos del CSV distintos de los del BOE: {sorted(csv_set ^ boe_set)}")
            elif any((bid, c) in ZONAS_ERRATA for c in sub["cod_ine_municipio"]):
                checks.append(f"{bid}: erratas corregidas del CSV de zonas " + str(
                    {c: ZONAS_ERRATA[(bid, c)] for c in sub["cod_ine_municipio"] if (bid, c) in ZONAS_ERRATA}))
        if len(names) == 131 and "131 municipios" not in t:
            fallidos.append(f"{bid}: 131 no aparece en el texto")
        r = sub.iloc[0]
        resol = (r["declaracion_autonomica"] or "").split(",")[0]
        for n in names:
            c = to_code(n)
            if c is None:
                fallidos.append(f"{bid} sin código INE: {n}")
                continue
            rows.append(dict(
                cod_ine=c, municipio=n,
                norma=f"{resol.strip()} (Cataluña, Ley 12/2023); relación SEVAU en {bid}",
                fecha_publicacion=r["fecha_publicacion_boe"], fecha_vigencia_inicio=r["fecha_efecto"],
                fecha_vigencia_fin=r["fecha_fin_prevista"], regimen="ley12_2023_zona_tensionada",
                url_oficial=BOE_TXT.format(bid), verificado="sí"))

    out = pd.DataFrame(rows, columns=COLS)
    bad = sorted(set(out["cod_ine"]) - codes_ok)
    if bad:
        fallidos.append(f"códigos fuera de Incasòl: {bad}")
    out["cod_ine"] = out["cod_ine"].str.zfill(5)
    out.to_csv(OUT, index=False)

    # Registro en manifiesto (mismo bloqueo que utils_fetch.save)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = pd.DataFrame([{
        "archivo": OUT.relative_to(RAW).as_posix(),
        "fuente": "BOE (Ley 11/2020 consolidada; Resoluciones SEVAU art. 18 Ley 12/2023) + zonas_tensionadas_v3",
        "n_series": out["norma"].nunique(), "primera_fecha": out["fecha_publicacion"].min(),
        "ultima_fecha": out["fecha_publicacion"].max(), "n_obs": len(out), "n_nan": int(out.isna().sum().sum()),
        "descargado_utc": now}])
    with open(RAW / ".manifest.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        man = pd.read_csv(MANIFEST)
        man = pd.concat([man[man["archivo"] != row["archivo"][0]], row], ignore_index=True)
        man.sort_values("archivo").to_csv(MANIFEST, index=False)

    # Registro de fuentes no verificadas (idempotente)
    fallidas_txt = [
        ("DOGC portal ELI de la Ley 11/2020 (texto DOGC)", "https://portaldogc.gencat.cat/eli/es-ct/l/2020/09/18/11",
         "HTTP 404 (2026-10-10); no se pudo confirmar el texto DOGC", "texto BOE consolidado (BOE-A-2020-11363; versiones 2020-09-21 y 2020-10-01)"),
        ("«Resolució TES/1374/2020» (referencia citada como fuente de las 61 áreas)", "no localizada",
         "búsqueda sin resultado que confirme esa resolución; las 61 áreas figuran en el anexo de la Ley 11/2020", "anexo de la Ley 11/2020 (DT segunda), verificado en BOE"),
        ("Declaración catalana de zonas tensionadas de julio de 2026 (prórroga y nueva declaración; 302 municipios)",
         "https://www.ultimahora.es/noticias/comunidades/2026/07/28/2678719/catalunya-prorroga-ano-declaracion-zona-vivienda-tensionada-llega-302-municipios.html",
         "solo prensa; BOE-A-2026-16532 (SEVAU, 2T 2026) no incluye filas de Cataluña; DOGC no accesible",
         "pendiente de DOGC y de la relación SEVAU posterior; no incluida en el CSV"),
        ("Zonas tensionadas catalanas 2025 (Ley 12/2023)", "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-1721 (y 8636, 15728, 21901)",
         "las resoluciones SEVAU de 2025 no contienen filas «Cataluña»", "no existen declaraciones catalanas 2025 en el BOE consultado"),
    ]
    existing = FAILS.read_text(encoding="utf-8") if FAILS.exists() else ""
    add = [f"| {a} | {b} | {c} | {d} | {now[:10]} |" for a, b, c, d in fallidas_txt if a[:30] not in existing]
    if add:
        with open(FAILS, "a", encoding="utf-8") as fh:
            fh.write("\n" + "\n".join(add) + "\n")

    print("\n".join(checks))
    print(f"[ok] {OUT.relative_to(ROOT)}: {len(out)} filas")
    print(out.groupby(["regimen", "norma"]).size().to_string())
    print("fallos:", fallidos or "ninguno")


if __name__ == "__main__":
    main()
