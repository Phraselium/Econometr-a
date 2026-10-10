"""v3 / A5: tenencia por edad. EFF (cuadro 3 de los articulos del BdE, PDF con texto: pdfplumber)
y INE ECV (tabla 9994, API JSON de Tempus, persona de referencia).
Salidas: data/raw/v3/eff_tenencia_edad_v3.csv, ine_ecv_tenencia_edad_v3.csv, eff_validacion_v3.csv.
Idempotente: si las salidas existen y no hay FORCE=1, termina sin red.
"""
from __future__ import annotations
import datetime as dt, json, re, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from utils_fetch import download, FORCE  # noqa: E402

OUT = ROOT / "data" / "raw" / "v3"
ORIG = OUT / "originales"
VAL = OUT / "validacion"
F_EFF, F_ECV, F_VAL = (OUT / n for n in ("eff_tenencia_edad_v3.csv", "ine_ecv_tenencia_edad_v3.csv", "eff_validacion_v3.csv"))
COLS = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "territorio", "nivel", "codigo", "origen", "validado", "error_max"]

B = "https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/InformesBoletinesRevistas/"
# (fichero, url, paginas del cuadro 3, referencia)
DOCS = [
    ("bde_separata_eff2007.pdf", "https://www.bde.es/f/webbde/SES/estadis/eff/Separata_EFF_2007.pdf", [14, 15], "BE dic-2007 (EFF2005)"),
    ("bde_be1012_art2_eff2008.pdf", B + "BoletinEconomico/10/Dic/Fich/art2.pdf", [11, 12], "BE dic-2010 (EFF2008)"),
    ("bde_be1401_art2_eff2011.pdf", B + "BoletinEconomico/14/Ene/Fich/be1401-art2.pdf", [10, 11], "BE ene-2014 (EFF2011)"),
    ("bde_beaa1701_art2e_eff2014_en.pdf", "https://repositorio.bde.es/bitstream/123456789/8860/1/beaa1701-art2e.pdf", [12, 13], "AA 2017 (EFF2014, ingles)"),
    ("bde_be2203_art21_eff2020.pdf", B + "ArticulosAnaliticos/22/T3/Fich/be2203-art21.pdf", [16, 17], "BE 3/2022 (EFF2020)"),
    ("bde_do2413_eff2022.pdf", "https://repositorio.bde.es/bitstream/123456789/36572/1/do2413.pdf", [23, 24], "DO 2413 (EFF2022)"),
]
AGES = {"menorde35": "<35", "entre35y44": "35-44", "entre45y54": "45-54", "entre55y64": "55-64", "entre65y74": "65-74", "mayorde74": "75+",
        "under35": "<35", "between35and44": "35-44", "between45and54": "45-54", "between55and64": "55-64", "between65and74": "65-74", "over74": "75+"}
NUM = re.compile(r"-?\d+(?:[.,]\d+)?")
# Revision visual (PNG leidos por el autor); se rellena tras la inspeccion
VISUAL = {("bde_separata_eff2007.pdf", 14): "si: PNG leido, 7 filas x 4 variables coinciden",
          ("bde_beaa1701_art2e_eff2014_en.pdf", 13): "si: PNG leido, 7 filas x 4 variables coinciden",
          ("bde_do2413_eff2022.pdf", 24): "si: PNG leido, 7 filas x 4 variables coinciden"}


def fnum(s):
    return float(s.replace(",", "."))


def parse_page(pdf, pag):
    """-> (ola, base_precios, filas[(bloque, edad, v_principal, v_otras)])"""
    t = pdf.pages[pag - 1].extract_text()
    head = t[:500]
    ola = int(re.search(r"EFF\s*(\d{4})", head).group(1))
    ln_e = next((x for x in head.split("\n") if "euro" in x.lower()), "")
    m = re.search(r"(?:del a[nñ]o|del|de|of)\s+((?:I\s*TR\s*)?\d{4})", ln_e)
    base = m.group(1) if m else None
    bloque, filas = None, []
    for ln in t.split("\n"):
        l = ln.strip()
        if re.match(r"(?i)^(porcentaje|percentage)", l):
            bloque = "pct"
        elif re.match(r"(?i)^(mediana|median)", l):
            bloque = "mediana"
        if bloque is None:
            continue
        nums = NUM.findall(l)
        lab = re.sub(r"\s+", "", NUM.sub("", l.split(" ")[0] if False else re.split(r"\s\d", l + " ")[0])).lower()
        lab_full = re.sub(r"[^a-zñ0-9]", "", re.split(r"\s-?\d+[.,]\d", l)[0].lower())
        edad = None
        for k, v in AGES.items():
            if lab_full.startswith(k):
                edad = v
        if lab_full.startswith(("todosloshogares", "allhouseholds")):
            edad = "total"
        if edad and len(nums) >= 6:
            vals = [fnum(x) for x in nums[-6:]]
            filas.append((bloque, edad, vals[0], vals[1]))
    return ola, base, filas


def run_eff():
    ORIG.mkdir(parents=True, exist_ok=True)
    import pdfplumber
    rows, val = [], []
    for fn, url, pags, ref in DOCS:
        path = download(url, ORIG / fn)
        pdf = pdfplumber.open(path)
        fulltext = {i + 1: (p.extract_text() or "") for i, p in enumerate(pdf.pages)}
        for pag in pags:
            ola, base, filas = parse_page(pdf, pag)
            # cuadre: 6 edades + total en cada bloque
            for bl in ("pct", "mediana"):
                eds = [f[1] for f in filas if f[0] == bl]
                assert sorted(eds) == sorted(["<35", "35-44", "45-54", "55-64", "65-74", "75+", "total"]), (fn, pag, bl, eds)
            tot = [f for f in filas if f[0] == "pct" and f[1] == "total"][0][2]
            pcts = [f[2] for f in filas if f[0] == "pct" and f[1] != "total"]
            # (a) total vs cifra publicada en el texto del articulo
            tstr = {f"{tot:.1f}".replace(".", ","), f"{tot:.1f}"}
            hallado = []
            for p, tx in fulltext.items():
                if p in pags:
                    continue
                for m in re.finditer(r"|".join(re.escape(x) for x in tstr) + r"\s?%?", tx):
                    ctx = tx[max(0, m.start() - 250): m.end() + 250].lower()
                    if re.search(r"propietari|own their|ownership", ctx):
                        hallado.append(p)
                        break
            cuadra_rango = min(pcts) <= tot <= max(pcts)
            ok = bool(hallado) and cuadra_rango
            val.append(dict(tabla=f"Cuadro 3 {ref} ola {ola}", ola=ola, fichero=fn, pagina=pag, total_pct_vivienda_principal=tot,
                            total_en_texto=("si, pp. " + ",".join(map(str, hallado[:3]))) if hallado else "no localizado",
                            total_entre_min_max_edades=cuadra_rango, validado="si" if ok else "no",
                            error_max=0.0 if hallado else "", metodo="cifra total del cuadro vs cifra en el texto del articulo (|dif|); total dentro del rango de los grupos de edad; render PNG",
                            paginas_revisadas=pag, revision_visual=VISUAL.get((fn, pag), "")))
            for bl, edad, v1, v2 in filas:
                for var, v in (("vivienda_principal", v1), ("otras_propiedades", v2)):
                    if bl == "mediana" and var == "otras_propiedades":
                        sn = "eff_mediana_valor_otras_propiedades"
                    else:
                        sn = {"pct": "eff_pct_hogares_", "mediana": "eff_mediana_valor_"}[bl] + var
                    unidad = "% de hogares" if bl == "pct" else f"miles EUR de {base}"
                    rows.append(dict(fecha=f"{ola}-12-31", periodo=str(ola), serie=f"{sn}|edad={edad}|ed={ref}", valor=v, unidad=unidad,
                                     fuente="Banco de España, EFF " + ref, url=url, territorio="España", nivel="nacional",
                                     codigo=f"{fn}#p{pag}", origen="pdf", validado="si" if ok else "no", error_max=0.0 if hallado else None))
            png = VAL / f"{Path(fn).stem}_p{pag}.png"
            if not png.exists():
                import pypdfium2 as pdfium
                VAL.mkdir(parents=True, exist_ok=True)
                pdfium.PdfDocument(str(path))[pag - 1].render(scale=1.6).to_pil().save(png)
    df = pd.DataFrame(rows)[COLS]
    # (b) solape entre ediciones de la misma ola
    v = pd.DataFrame(val)
    d = df.copy()
    d["k"] = d.serie.str.replace(r"\|ed=.*", "", regex=True)
    sol = []
    for (ola, k), g in d.groupby(["periodo", "k"]):
        if len(g) > 1 and not k.startswith("eff_mediana"):
            sol.append(dict(ola=int(ola), k=k, dif=g.valor.max() - g.valor.min()))
    sol = pd.DataFrame(sol)
    if len(sol):
        s = sol.groupby("ola").dif.max()
        v["error_max_entre_ediciones_pp"] = v.ola.map(s)
    df.to_csv(F_EFF, index=False)
    v.to_csv(F_VAL, index=False)
    return df, v


def run_ecv():
    TAB = 9994
    url = f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{TAB}?nult=40"
    p = download(url, ORIG / f"ine_ecv_tabla{TAB}.json")
    d = json.loads(Path(p).read_text())
    rows = []
    for s in d:
        partes = [x.strip() for x in s["Nombre"].split(". ")]
        sexo, edad, terr, ten = partes[0], partes[1], partes[2], partes[3]
        for pt in s["Data"]:
            if pt["Valor"] is None:
                continue
            rows.append(dict(fecha=f"{pt['Anyo']}-01-01", periodo=str(pt["Anyo"]), serie=f"ecv_pct_hogares_tenencia|{ten}|edad_persona_referencia={edad}|sexo={sexo}",
                             valor=pt["Valor"], unidad="% de hogares del grupo", fuente="INE, ECV, tabla 9994 (hogares por régimen de tenencia, edad y sexo de la persona de referencia)",
                             url=url, territorio="España", nivel="nacional", codigo=s["COD"], origen="api", _sexo=sexo, _edad=edad, _ten=ten))
    df = pd.DataFrame(rows)
    # validacion: 4 regimenes suman 100; propiedad = con + sin hipoteca
    g = df.pivot_table(index=["periodo", "_sexo", "_edad"], columns="_ten", values="valor")
    suma = g[["Propiedad", "Alquiler a precio de mercado", "Alquiler inferior al precio de mercado", "Cesión"]].sum(axis=1)
    e1 = (suma - 100).abs()
    e2 = (g["Propiedad"] - g["Propiedad con hipoteca"] - g["Propiedad sin hipoteca"]).abs()
    err = pd.concat([e1, e2], axis=1).max(axis=1).rename("error_max").reset_index()
    df = df.merge(err, left_on=["periodo", "_sexo", "_edad"], right_on=["periodo", "_sexo", "_edad"], how="left")
    df["validado"] = df.error_max.le(0.35).map({True: "si", False: "no"})  # redondeo de 4 cifras a 0,1: tolerancia 0,35
    out = df[COLS]
    out.to_csv(F_ECV, index=False)
    print("ECV max error cuadre:", err.error_max.max(), "años", out.periodo.min(), out.periodo.max())
    return out


def update_manifest():
    mf = ROOT / "data" / "raw" / "_manifest.csv"
    m = pd.read_csv(mf)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for f, fu in ((F_EFF, "BdE EFF"), (F_ECV, "INE ECV")):
        d = pd.read_csv(f)
        new = dict(archivo=f"v3/{f.name}", fuente=fu, n_series=d.serie.nunique(), primera_fecha=d.fecha.min(), ultima_fecha=d.fecha.max(),
                   n_obs=len(d), n_nan=int(d.valor.isna().sum()), descargado_utc=now)
        m = m[m.archivo != new["archivo"]]
        m = pd.concat([m, pd.DataFrame([new])], ignore_index=True)
    m.to_csv(mf, index=False)


if __name__ == "__main__":
    if F_EFF.exists() and F_ECV.exists() and F_VAL.exists() and not FORCE:
        print("[cache] salidas v3 EFF/ECV existen; FORCE=1 para regenerar")
        sys.exit(0)
    e, v = run_eff()
    c = run_ecv()
    update_manifest()
    print(v[["ola", "pagina", "total_pct_vivienda_principal", "total_en_texto", "validado", "error_max_entre_ediciones_pp"]].to_string())
