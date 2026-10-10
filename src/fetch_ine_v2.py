"""Descarga v2 de series del INE por PROVINCIA (52) a data/raw, formato largo.

Tablas usadas (API JSON wstempus, https://servicios.ine.es/wstempus/js/ES):
  1. Hipotecas sobre viviendas, mensual, provincia (op. HPT): 76317 (base nueva, desde 2003).
  2. Compraventas de viviendas, mensual, provincia (op. ETDP): 6150 (general/nueva/usada/libre/protegida).
  3. IPC subclase "Alquiler de vivienda", mensual, provincia (op. IPC): 76142 (ECOICOP v2).
  4. IPVA, anual, provincia/municipio/distrito (op. IPVA): 59058, 59005, 59059 (provincia),
     59060 (municipio >10.000 hab.), 59061 (distrito). Solo índices y variación anual (no hay €).
  5. Inmigración desde el extranjero, semestral, provincia (op. EM/EMCR): 24420 (sexo Ambos, edad
     Total, nacionalidad Total/Española/Extranjero) y 24421 (provincia x país/nacionalidad).
  6. Población residente por provincia, sexo, edad y nacionalidad (ECP, op. ECP): 77023.
     Edad: 5 años -> agregados 0-19, 20-34, 35-64, 65+ (suma de grupos publicados, se valida
     contra "Todas las edades"). Anual = trimestre T1 (fecha 1 de enero).
     Pais: misma tabla, edad "Todas", agrupaciones de países de nacimiento/nacionalidad disponibles.
  7. Contabilidad Regional (op. CRE): 80109 PIB a precios corrientes por provincia, anual.
  8. EPA por provincia (op. EPA): 65345 ocupados y parados, trimestral, valor absoluto.
  9. Viviendas turísticas (op. VTE): 39364 (provincia, nacional) y 39363 (municipio), mensual.
 10. Hogares por provincia (ECP, op. ECP): 60133 (tamaño del hogar, trimestral, desde 2021).

Verificación previa: cada tabla se consulta con nult=1 (listado de series + última fecha)
antes de descargar. Para tablas grandes (77023, 39363, 76142, 24420) se piden series
individuales con DATOS_SERIE/{COD} seleccionadas por nombre (sin volcar la tabla completa).

Periodos: FK_Periodo 1-12 = mes; 19-22 = T1-T4; 26/27 = S1/S2 (verificado: Fecha = 1 ene / 1 jul);
28 = anual. Fecha = primer día del periodo. Se comprueba contra el epoch de Fecha (Europe/Madrid).

Serie: COD del INE (p. ej. HPT34618) salvo agregados ECP, que llevan
"ECP77023_<codigo>_<nacionalidad>_<grupo>". Territorio = nombre INE normalizado;
codigo = código INE de provincia 01-52 ('00' nacional; vacío para municipio/distrito porque la
API no expone el código de municipio en el nombre de la serie).

Caché: si el CSV de destino existe en data/raw no se vuelve a descargar salvo FORCE=1.
Manifiesto: utils_fetch.save() (por archivo) y data/raw/_manifest_series_ine_v2.csv (por serie).
Fallos y limitaciones: docs/v2/fallidas/ine.md (se regenera en cada ejecución).
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import RAW, ROOT, cached, get, save  # noqa: E402

BASE = "https://servicios.ine.es/wstempus/js/ES"
FUENTE = "INE"
MAD = ZoneInfo("Europe/Madrid")
NULT = 400  # periodos máximos pedidos (cubre desde 2002 en mensual)
THREADS = 8
MANIFEST_SER = RAW / "_manifest_series_ine_v2.csv"
FALLIDAS_MD = ROOT / "docs" / "v2" / "fallidas" / "ine.md"

# Código INE de provincia -> nombre INE (tal como aparece en las tablas del INE)
PROV = {
    "01": "Araba/Álava", "02": "Albacete", "03": "Alicante/Alacant", "04": "Almería",
    "05": "Ávila", "06": "Badajoz", "07": "Balears, Illes", "08": "Barcelona",
    "09": "Burgos", "10": "Cáceres", "11": "Cádiz", "12": "Castellón/Castelló",
    "13": "Ciudad Real", "14": "Córdoba", "15": "Coruña, A", "16": "Cuenca",
    "17": "Girona", "18": "Granada", "19": "Guadalajara", "20": "Gipuzkoa",
    "21": "Huelva", "22": "Huesca", "23": "Jaén", "24": "León", "25": "Lleida",
    "26": "Rioja, La", "27": "Lugo", "28": "Madrid", "29": "Málaga", "30": "Murcia",
    "31": "Navarra", "32": "Ourense", "33": "Asturias", "34": "Palencia",
    "35": "Palmas, Las", "36": "Pontevedra", "37": "Salamanca",
    "38": "Santa Cruz de Tenerife", "39": "Cantabria", "40": "Segovia", "41": "Sevilla",
    "42": "Soria", "43": "Tarragona", "44": "Teruel", "45": "Toledo",
    "46": "Valencia/València", "47": "Valladolid", "48": "Bizkaia", "49": "Zamora",
    "50": "Zaragoza", "51": "Ceuta", "52": "Melilla",
}
ALIAS = {
    "A Coruña": "15", "Asturias, Principado de": "33", "Valencia": "46",
    "Castellón": "12", "Castelló": "12", "Alicante": "03", "Alacant": "03",
    "Illes Balears": "07", "Baleares": "07", "Palmas, Las": "35", "Las Palmas": "35",
    "Rioja, La": "26", "La Rioja": "26", "Araba": "01", "Álava": "01", "Vizcaya": "48",
    "Guipúzcoa": "20", "Lérida": "25", "Gerona": "17", "Orense": "32", "Coruña": "15",
}
CCAA = {
    "Andalucía", "Aragón", "Asturias, Principado de", "Balears, Illes", "Canarias",
    "Cantabria", "Castilla y León", "Castilla - La Mancha", "Cataluña",
    "Comunitat Valenciana", "Extremadura", "Galicia", "Madrid, Comunidad de",
    "Murcia, Región de", "Navarra, Comunidad Foral de", "País Vasco", "Rioja, La",
}
NAC = {"Total Nacional", "Nacional"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.strip()).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).lower()


_PROV_KEYS = {norm(v): k for k, v in PROV.items()}
_PROV_KEYS.update({norm(k): v for k, v in ALIAS.items()})


def geo(nombre: str):
    """(nivel, codigo, territorio) si el nombre es nacional o provincia; si no, None."""
    if nombre in NAC:
        return ("nacional", "00", "España")
    c = _PROV_KEYS.get(norm(nombre))
    if c:
        return ("provincia", c, PROV[c])
    return None


def partes(nombre: str) -> list[str]:
    out = []
    for x in nombre.split(". "):
        x = x.strip().rstrip(".").strip()
        if x:
            out.append(x)
    return out


# ----------------------------------------------------------------- periodos
def periodo(fk: int, anyo: int):
    if 1 <= fk <= 12:
        return dt.date(anyo, fk, 1), f"{anyo}M{fk:02d}"
    if 19 <= fk <= 22:
        q = fk - 18
        return dt.date(anyo, 3 * (q - 1) + 1, 1), f"{anyo}T{q}"
    if fk in (26, 27):
        s = fk - 25
        return dt.date(anyo, 1 if s == 1 else 7, 1), f"{anyo}S{s}"
    if fk == 28:
        return dt.date(anyo, 1, 1), f"{anyo}"
    raise ValueError(f"FK_Periodo no reconocido: {fk}")


# ----------------------------------------------------------------- API
def listado(tid: str) -> list[dict]:
    """Petición pequeña (nult=1): lista de series de la tabla. Sirve de verificación."""
    d = get(f"{BASE}/DATOS_TABLA/{tid}", params={"nult": 1}, timeout=900)
    if isinstance(d, dict):
        raise RuntimeError(f"tabla {tid}: respuesta no válida: {str(d)[:150]}")
    ult = None
    for s in d:
        for x in s.get("Data") or []:
            f = (int(x["Anyo"]), int(x["FK_Periodo"]))
            ult = f if ult is None or f > ult else ult
    print(f"  [verif] tabla {tid}: {len(d)} series; último periodo (Anyo, FK)={ult}")
    return d


def serie_individual(cod: str, nult: int = NULT) -> dict:
    d = get(f"{BASE}/DATOS_SERIE/{cod}", params={"nult": nult}, timeout=300)
    if isinstance(d, list):
        d = d[0]
    if not isinstance(d, dict) or "Data" not in d:
        raise RuntimeError(f"DATOS_SERIE/{cod}: {str(d)[:150]}")
    return d


def tabla_completa(tid: str, nult: int = NULT) -> dict[str, dict]:
    d = get(f"{BASE}/DATOS_TABLA/{tid}", params={"nult": nult}, timeout=900)
    if isinstance(d, dict):
        raise RuntimeError(f"tabla {tid}: {str(d)[:150]}")
    return {s["COD"]: s for s in d}


def descargar(tid: str, cods: list[str], modo: str) -> dict[str, dict]:
    if modo == "tabla":
        full = tabla_completa(tid)
        return {c: full[c] for c in cods}
    with ThreadPoolExecutor(THREADS) as ex:
        res = list(ex.map(serie_individual, cods))
    return dict(zip(cods, res))


# ----------------------------------------------------------------- filas
def filas(serie: dict, meta: dict, url: str, tabla: str, fk_keep=None):
    out, mism = [], 0
    for x in serie.get("Data") or []:
        fk = int(x["FK_Periodo"])
        if fk_keep and fk not in fk_keep:
            continue
        d, lab = periodo(fk, int(x["Anyo"]))
        loc = dt.datetime.fromtimestamp(x["Fecha"] / 1000, tz=MAD)
        if (loc.year, loc.month) != (d.year, d.month):
            mism += 1
        out.append({
            "fecha": d.isoformat(), "periodo": lab, "serie": meta["serie"],
            "valor": None if x.get("Secreto") else x.get("Valor"),
            "unidad": meta["unidad"], "fuente": FUENTE, "url": url,
            "territorio": meta["territorio"], "nivel": meta["nivel"], "codigo": meta["codigo"],
            "medida": meta["medida"], "desglose": meta["desglose"],
            "cod_serie": serie["COD"], "tabla": tabla, "nombre_ine": serie["Nombre"].strip(),
        })
    return out, mism


# ----------------------------------------------------------------- selectores
HIP_MED = {
    "Número de hipotecas": ("hipotecas_viviendas_numero", "número"),
    "Importe de hipotecas": ("hipotecas_viviendas_importe", "miles de euros (inferido de magnitud; FK_Unidad=7)"),
}
ETDP_TIPO = {"General": "total", "Vivienda nueva": "nueva", "Vivienda segunda mano": "usada",
             "Vivienda libre": "libre", "Vivienda protegida": "protegida"}
IPVA_MED = {"Índice": ("IPVA_indice", "índice"), "Variación anual": ("IPVA_variacion_anual", "% variación anual")}
VUT_MED = {"Viviendas turísticas": "viviendas_turisticas", "Plazas": "plazas",
           "Plazas por vivienda turística": "plazas_por_vivienda"}
ECP_GRUPO4 = [("0-19", 0, 19), ("20-34", 20, 34), ("35-64", 35, 64), ("65+", 65, 200)]


def edad_inicio(txt: str):
    if txt == "Todas las edades":
        return "todas", None
    m = re.match(r"De (\d+) a (\d+) años", txt)
    if m:
        return "quinq", int(m.group(1))
    m = re.match(r"(\d+) y más años", txt)
    if m:
        return "quinq", int(m.group(1))
    return None, None


def grupo4(edad_ini: int) -> str:
    for lab, a, b in ECP_GRUPO4:
        if a <= edad_ini <= b:
            return lab
    raise ValueError(edad_ini)


def sel_hip(n, _t):
    p = partes(n)
    if len(p) < 4 or p[0] != "Viviendas" or p[1] not in HIP_MED:
        return None
    g = geo(p[2])
    if not g:
        return None
    med, uni = HIP_MED[p[1]]
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida=med, desglose=f"base {p[3]}", unidad=uni)


def sel_etdp(n, _t):
    p = partes(n)
    if len(p) < 4 or p[2] != "Compraventa" or p[3] != "Número" or p[1] not in ETDP_TIPO:
        return None
    g = geo(p[0])
    if not g:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="compraventas_viviendas",
                desglose=ETDP_TIPO[p[1]], unidad="número de compraventas")


def sel_ipc(n, _t):
    p = partes(n)
    if len(p) < 3 or p[1] != "Alquiler de vivienda" or p[2] not in ("Índice", "Variación anual"):
        return None
    g = geo(p[0])
    if not g:
        return None
    med, uni = IPVA_MED[p[2]]
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="IPC_alquiler_vivienda_" + med.split("_", 1)[1],
                desglose="subclase Alquiler de vivienda (ECOICOP v2)", unidad=uni)


def sel_ipva_factory(tid):
    def sel(n, _t):
        p = partes(n)
        idx = [i for i, x in enumerate(p) if x in IPVA_MED]
        if len(idx) != 1:
            return None
        i = idx[0]
        med, uni = IPVA_MED[p[i]]
        desg = " | ".join(p[j] for j in range(1, len(p)) if j != i)
        if tid == "59060":
            g = ("nacional", "00", "España") if p[0] in NAC else ("municipio", "", p[0])
        elif tid == "59061":
            g = ("nacional", "00", "España") if p[0] in NAC else ("distrito", "", p[0])
        else:
            g = geo(p[0])
            if not g:
                return None
        return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida=med, desglose=desg, unidad=uni)
    return sel


def sel_mig420(n, _t):
    p = partes(n)
    if len(p) != 5 or p[1] != "Ambos sexos" or p[4] != "Total" or p[3] not in ("Total", "Española", "Extranjero"):
        return None
    g = geo(p[0])
    if not g:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="inmigracion_desde_extranjero",
                desglose=f"nacionalidad={p[3]}; sexo=Ambos; edad=Total", unidad="personas (flujo semestral)")


def sel_mig421(n, _t):
    p = partes(n)
    if len(p) != 3 or not p[1].startswith("Flujo de inmigraciones"):
        return None
    g = geo(p[0])
    if not g:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="inmigracion_desde_extranjero",
                desglose=f"nacionalidad={p[2]}", unidad="personas (flujo semestral)")


def sel_ecp(n, _t):
    """ECP 77023: [geo, nacionalidad, edad, sexo, Población, Número]."""
    p = partes(n)
    if len(p) != 6 or p[3] != "Total" or p[4] != "Población":
        return None
    g = geo(p[0])
    if not g:
        return None
    tipo, ini = edad_inicio(p[2])
    if tipo is None:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], nacionalidad=p[1], edad=p[2],
                edad_ini=ini, edad_tipo=tipo, medida="poblacion_residente_1_enero",
                desglose=f"nacionalidad={p[1]}; edad={p[2]}", unidad="personas")


def sel_epa(n, _t):
    p = partes(n)
    if len(p) < 5 or p[-1] != "Valor absoluto" or p[-2] not in ("Ocupados", "Parados") or p[-3] != "Total":
        return None
    if "Ambos sexos" not in p:
        return None
    g = None
    for x in p:
        g = geo(x)
        if g:
            break
    if not g:
        return None
    cat = p[-2].lower()
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida=f"EPA_{cat}",
                desglose="ambos sexos; total", unidad="miles de personas (valor absoluto EPA)")


def sel_cre(n, _t):
    p = partes(n)
    if len(p) < 4 or p[1] != "Dato base" or p[2] != "Producto interior bruto a precios de mercado" \
            or p[3] != "Precios corrientes":
        return None
    g = geo(p[0])
    if not g:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="PIB_precios_corrientes",
                desglose="precios corrientes", unidad="miles de euros (inferido; FK_Unidad=7)")


def sel_vut(n, _t):
    p = partes(n)
    if len(p) < 3 or p[2] != "Dato base" or p[1] not in VUT_MED:
        return None
    return dict(medida=VUT_MED[p[1]], nombre=p[0], desglose="dato base", unidad="número" if p[1] != "Plazas por vivienda turística" else "plazas por vivienda")


def sel_hogares(n, _t):
    p = partes(n)
    if len(p) != 4 or not p[2].startswith("Hogares en viviendas familiares") or p[3] != "Número":
        return None
    g = geo(p[0])
    if not g:
        return None
    return dict(nivel=g[0], codigo=g[1], territorio=g[2], medida="hogares_viviendas_familiares",
                desglose=f"tamaño={p[1]}", unidad="número de hogares")


# ----------------------------------------------------------------- utilidades de job
def seleccionar(listing, selector):
    out = []
    for s in listing:
        m = selector(s["Nombre"], None)
        if m:
            out.append((s["COD"], m))
    return out


def construir(tid, seleccion, modo, fk_keep=None, extra=None):
    """Descarga las series seleccionadas y devuelve (df, resumen)."""
    cods = [c for c, _ in seleccion]
    datos = descargar(tid, cods, modo)
    url_base = f"{BASE}/DATOS_TABLA/{tid}?nult={NULT}" if modo == "tabla" else f"{BASE}/DATOS_SERIE/{{cod}}?nult={NULT}"
    rows, mism = [], 0
    for cod, m in seleccion:
        url = url_base.replace("{cod}", cod)
        r, mm = filas(datos[cod], dict(m, serie=cod), url, tid, fk_keep)
        rows.extend(r)
        mism += mm
    if mism:
        print(f"  [aviso] {mism} obs. con Fecha epoch distinta al periodo (tabla {tid})")
    return pd.DataFrame(rows)


def dedup_identicas(df: pd.DataFrame, claves: list[str]) -> pd.DataFrame:
    """Para un mismo (territorio, desglose) con varias series INE: conserva una si son idénticas.

    Si dos series del mismo grupo difieren en algún periodo, se aborta (no se elige a ciegas).
    """
    out = []
    for k, grp in df.groupby(claves, sort=False):
        ids = sorted(grp["serie"].unique())
        primera = grp[grp["serie"] == ids[0]]
        for otra_id in ids[1:]:
            a = primera.set_index("fecha")["valor"].sort_index()
            b = grp[grp["serie"] == otra_id].set_index("fecha")["valor"].sort_index()
            igual = a.index.equals(b.index) and bool(((a == b) | (a.isna() & b.isna())).all())
            if not igual:
                raise RuntimeError(f"series duplicadas con valores distintos en {k}: {ids}")
            print(f"  [dedup] {k}: {otra_id} idéntica a {ids[0]}; descartada")
        out.append(primera)
    return pd.concat(out, ignore_index=True)


def actualizar_manifiesto_series(df: pd.DataFrame, fuente: str):
    RAW.mkdir(parents=True, exist_ok=True)
    rows = []
    for serie, g in df.groupby("serie"):
        f = g["fecha"].sort_values()
        rows.append({
            "serie": serie, "fuente": fuente, "url": g["url"].iloc[0],
            "primera_fecha": f.iloc[0], "ultima_fecha": f.iloc[-1], "n_obs": len(g),
            "n_nan": int(g["valor"].isna().sum()),
            "descargado_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
    nuevo = pd.DataFrame(rows)
    if MANIFEST_SER.exists():
        old = pd.read_csv(MANIFEST_SER)
        old = old[~old["serie"].isin(nuevo["serie"])]
        nuevo = pd.concat([old, nuevo], ignore_index=True)
    nuevo.sort_values("serie").to_csv(MANIFEST_SER, index=False)


def guardar(df: pd.DataFrame, archivo: str, fuente_txt: str):
    df = df.dropna(subset=["fecha"])
    save(df, archivo, fuente_txt)
    actualizar_manifiesto_series(df, fuente_txt)
    print(f"  [serie] {df['serie'].nunique()} series; "
          f"{df['fecha'].min()} -> {df['fecha'].max()}; NaN={int(df['valor'].isna().sum())}")


RESULTADOS: list[dict] = []
FALLOS: list[dict] = []


def registrar(archivo, tabla, url, error, alternativa):
    FALLOS.append(dict(archivo=archivo, tabla=tabla, url=url, error=str(error)[:300], alternativa=alternativa))


# ----------------------------------------------------------------- jobs
def job_hipotecas():
    arch = "ine_v2_hipotecas_prov.csv"
    if cached(arch):
        return
    print("[get] hipotecas (76317)")
    L = listado("76317")
    sel = seleccionar(L, sel_hip)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("76317", sel, "serie")
    guardar(df, arch, "INE HPT - Hipotecas constituidas sobre el total de fincas, viviendas (tabla 76317, base nueva)")


def job_etdp():
    arch = "ine_v2_etdp_prov.csv"
    if cached(arch):
        return
    print("[get] compraventas ETDP (6150)")
    L = listado("6150")
    sel = seleccionar(L, sel_etdp)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("6150", sel, "tabla")
    df = dedup_identicas(df, ["territorio", "desglose"])
    guardar(df, arch, "INE ETDP - Compraventa de viviendas según régimen y estado (tabla 6150, mensual)")


def job_ipc():
    arch = "ine_v2_ipc_alquiler_prov.csv"
    if cached(arch):
        return
    print("[get] IPC alquiler de vivienda provincial (76142)")
    L = listado("76142")
    sel = seleccionar(L, sel_ipc)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("76142", sel, "serie")
    guardar(df, arch, "INE IPC - Índices provinciales de subgrupos ECOICOP v2, Alquiler de vivienda (tabla 76142)")


def job_ipva():
    arch = "ine_v2_ipva.csv"
    if cached(arch):
        return
    partes_df = []
    for tid in ["59058", "59005", "59059", "59060", "59061"]:
        print(f"[get] IPVA {tid}")
        L = listado(tid)
        sel = seleccionar(L, sel_ipva_factory(tid))
        print(f"  seleccionadas {len(sel)} series")
        d = construir(tid, sel, "tabla")
        partes_df.append(d)
    df = pd.concat(partes_df, ignore_index=True)
    guardar(df, arch, "INE IPVA - Índice de Precios de Vivienda en Alquiler (tablas 59058, 59005, 59059, 59060, 59061)")


def job_migraciones():
    arch = "ine_v2_migraciones_prov.csv"
    if cached(arch):
        return
    print("[get] inmigración desde extranjero semestral (24420, 24421)")
    L1 = listado("24420")
    s1 = seleccionar(L1, sel_mig420)
    print(f"  24420 seleccionadas {len(s1)} series")
    d1 = construir("24420", s1, "serie")
    L2 = listado("24421")
    s2 = seleccionar(L2, sel_mig421)
    print(f"  24421 seleccionadas {len(s2)} series")
    d2 = construir("24421", s2, "tabla")
    df = pd.concat([d1, d2], ignore_index=True)
    guardar(df, arch, "INE EM/EMCR - Flujo de inmigración procedente del extranjero por provincia, semestre (tablas 24420, 24421)")


def _ecp_listado():
    print("  listado ECP 77023 (nult=1)")
    return listado("77023")


def job_padron_edad_nac(L=None):
    arch = "ine_v2_padron_prov_edad_nac.csv"
    if cached(arch):
        return
    print("[get] ECP 77023 provincia x edad x nacionalidad")
    L = L or _ecp_listado()
    sel = []
    for cod, m in seleccionar(L, sel_ecp):
        if m["nacionalidad"] in ("Total", "Española", "Extranjera") and m["edad_tipo"] in ("todas", "quinq"):
            sel.append((cod, m))
    print(f"  seleccionadas {len(sel)} series")
    df = construir("77023", sel, "serie", fk_keep={19})  # T1 = 1 de enero
    # Mapear metadatos de edad desde el nombre INE (edad y nacionalidad en el 2º y 3er campo)
    meta = {cod: m for cod, m in sel}
    df["edad_txt"] = df["cod_serie"].map(lambda c: meta[c]["edad"])
    df["edad_ini"] = df["cod_serie"].map(lambda c: meta[c]["edad_ini"])
    df["nac"] = df["cod_serie"].map(lambda c: meta[c]["nacionalidad"])
    df["edad_tipo"] = df["cod_serie"].map(lambda c: meta[c]["edad_tipo"])
    q = df[df["edad_tipo"] == "quinq"].copy()
    q["grupo"] = q["edad_ini"].map(grupo4)
    agg = q.groupby(["fecha", "periodo", "territorio", "nivel", "codigo", "nac", "grupo"], as_index=False).agg(
        valor=("valor", lambda s: s.sum(min_count=len(s))), n_grupos=("valor", "size"))
    agg["n_grupos_esperados"] = agg["grupo"].map({"0-19": 4, "20-34": 3, "35-64": 6, "65+": 6})
    incompletos = int((agg["n_grupos"] != agg["n_grupos_esperados"]).sum())
    # Validación: suma de grupos quinquenales vs "Todas las edades" publicado
    tot = df[df["edad_tipo"] == "todas"].set_index(["fecha", "territorio", "nac"])["valor"]
    suma = q.groupby(["fecha", "territorio", "nac"])["valor"].sum(min_count=1)
    cmp_ = pd.concat([tot.rename("pub"), suma.rename("suma")], axis=1).dropna()
    dif = (cmp_["suma"] - cmp_["pub"]).abs()
    print(f"  [valid] suma quinquenales vs 'Todas': máx |dif|={dif.max():.0f} personas; "
          f"filas con dif>10: {int((dif > 10).sum())} de {len(dif)}; grupos incompletos: {incompletos}")
    publicado = df[df["edad_tipo"] == "todas"].copy()
    publicado["grupo"] = "Todas"
    cols = ["fecha", "periodo", "territorio", "nivel", "codigo", "nac", "grupo", "valor"]
    base = pd.concat([agg[cols], publicado[cols]], ignore_index=True)
    slug = {"Total": "total", "Española": "espanola", "Extranjera": "extranjera"}
    base["serie"] = base.apply(lambda r: f"ECP77023_{r['codigo'] or r['territorio']}_{slug[r['nac']]}_{r['grupo']}", axis=1)
    base["unidad"] = "personas"
    base["fuente"] = FUENTE
    base["url"] = f"{BASE}/DATOS_SERIE/<COD>?nult={NULT}"
    base["cod_serie"] = ""
    base["tabla"] = "77023"
    base["nombre_ine"] = ""
    base["medida"] = "poblacion_residente_1_enero"
    base["desglose"] = base.apply(lambda r: f"nacionalidad={r['nac']}; edad={r['grupo']}", axis=1)
    base.loc[base["grupo"] == "Todas", "nombre_ine"] = "Todas las edades (publicado)"
    base.loc[base["grupo"] != "Todas", "nombre_ine"] = "Suma de grupos quinquenales INE (agregado)"
    base = base.drop(columns=["nac", "grupo"])
    guardar(base, arch, "INE ECP - Población residente por fecha, sexo, grupo de edad y nacionalidad (tabla 77023; 1 de enero)")


def job_padron_pais(L=None):
    arch = "ine_v2_padron_prov_pais.csv"
    if cached(arch):
        return
    print("[get] ECP 77023 provincia x agrupación de países (edad Todas)")
    L = L or _ecp_listado()
    sel = []
    for cod, m in seleccionar(L, sel_ecp):
        if m["edad_tipo"] == "todas":
            sel.append((cod, m))
    print(f"  seleccionadas {len(sel)} series")
    df = construir("77023", sel, "serie", fk_keep={19})
    meta = {cod: m for cod, m in sel}
    df["desglose"] = "nacionalidad=" + df["cod_serie"].map(lambda c: meta[c]["nacionalidad"])
    guardar(df, arch, "INE ECP - Población residente por provincia y agrupación de países de nacionalidad, 1 de enero (tabla 77023)")


def job_cre():
    arch = "ine_v2_cre.csv"
    if cached(arch):
        return
    print("[get] Contabilidad Regional PIB provincial (80109)")
    L = listado("80109")
    sel = seleccionar(L, sel_cre)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("80109", sel, "tabla")
    guardar(df, arch, "INE CRE - PIB a precios de mercado, precios corrientes, por CCAA y provincias (tabla 80109)")


def job_epa():
    arch = "ine_v2_epa_prov.csv"
    if cached(arch):
        return
    print("[get] EPA provincial ocupados/parados (65345)")
    L = listado("65345")
    sel = seleccionar(L, sel_epa)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("65345", sel, "tabla")
    guardar(df, arch, "INE EPA - Ocupados y parados por provincia, trimestral (tabla 65345)")


def job_vut():
    arch = "ine_v2_vut.csv"
    if cached(arch):
        return
    print("[get] viviendas turísticas provincia (39364)")
    L1 = listado("39364")
    s1 = []
    for cod, m in seleccionar(L1, sel_vut):
        g = geo(m["nombre"])
        if g:
            s1.append((cod, dict(m, nivel=g[0], codigo=g[1], territorio=g[2])))
    print(f"  39364 seleccionadas {len(s1)} series")
    d1 = construir("39364", s1, "tabla")
    # Referencia de provincia para distinguir provincia/municipio homónimos en 39363
    ref = d1.copy()
    print("[get] viviendas turísticas municipio (39363; serie a serie)")
    L2 = listado("39363")
    s2 = []
    for cod, m in seleccionar(L2, sel_vut):
        nom = m["nombre"]
        if nom in NAC or nom in CCAA:
            continue
        g = geo(nom)
        if g and g[0] == "provincia":
            # Homónimo de provincia: se considera municipio solo si su serie difiere de la provincial
            s2.append((cod, dict(m, nivel="municipio?", codigo="", territorio=nom)))
        else:
            s2.append((cod, dict(m, nivel="municipio", codigo="", territorio=nom)))
    print(f"  39363 seleccionadas {len(s2)} series (incl. homónimos de provincia a verificar)")
    d2 = construir("39363", s2, "serie")
    if not d2.empty:
        # Quitar provincias duplicadas: si el valor más reciente coincide con la provincia de 39364, se descarta
        ult = ref.sort_values("fecha").groupby(["territorio", "medida", "desglose"]).tail(1)
        ult_map = {(r.territorio, r.medida): r.valor for r in ult.itertuples()}
        mun_ult = d2.sort_values("fecha").groupby("serie").tail(1)
        descartar = set()
        for r in mun_ult.itertuples():
            if r.nivel == "municipio?":
                ref_val = ult_map.get((r.territorio, r.medida))
                if ref_val is not None and r.valor == ref_val:
                    descartar.add(r.serie)
        d2 = d2[~d2["serie"].isin(descartar)].copy()
        d2["nivel"] = "municipio"
        print(f"  [homónimos] {len(descartar)} series de provincia descartadas (duplican 39364)")
    df = pd.concat([d1, d2], ignore_index=True)
    guardar(df, arch, "INE VTE - Viviendas turísticas, plazas: provincias (39364) y municipios (39363), mensual")


def job_hogares():
    arch = "ine_v2_hogares_prov.csv"
    if cached(arch):
        return
    print("[get] hogares por provincia y tamaño (60133)")
    L = listado("60133")
    sel = seleccionar(L, sel_hogares)
    print(f"  seleccionadas {len(sel)} series")
    df = construir("60133", sel, "tabla")
    guardar(df, arch, "INE ECP - Hogares de personas residentes en viviendas familiares por tamaño, trimestral (tabla 60133)")


JOBS = [
    ("hipotecas", job_hipotecas),
    ("etdp", job_etdp),
    ("ipc_alquiler", job_ipc),
    ("ipva", job_ipva),
    ("migraciones", job_migraciones),
    ("padron_edad_nac", job_padron_edad_nac),
    ("padron_pais", job_padron_pais),
    ("cre", job_cre),
    ("epa", job_epa),
    ("vut", job_vut),
    ("hogares", job_hogares),
]


def escribir_fallidas():
    FALLIDAS_MD.parent.mkdir(parents=True, exist_ok=True)
    ahora = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    L = ["# INE v2 por provincia: fallos y limitaciones", "",
         f"Generado por `src/fetch_ine_v2.py` ({ahora}). Los datos no disponibles no se han inventado.", "",
         "## Fallos de descarga en la última ejecución", ""]
    if FALLOS:
        L += ["| archivo | tabla | URL probada | error | alternativa |", "|---|---|---|---|---|"]
        for f in FALLOS:
            L.append(f"| {f['archivo']} | {f['tabla']} | {f['url']} | {f['error']} | {f['alternativa']} |")
    else:
        L.append("Ninguno.")
    L += ["", "## Limitaciones verificadas (sin dato a nivel provincial)", "",
          "| dato pedido | estado | tablas/endpoints probados | alternativa propuesta |",
          "|---|---|---|---|",
          "| Renta disponible de los hogares por provincia | No existe en la CRE. Solo PIB, PIB per cápita y empleo por CCAA/provincia. | op. CRE (257): 17 tablas, ninguna de renta disponible | INE Atlas de Distribución de Renta de los Hogares (ADRH), a nivel municipal/distrito, no verificado en esta sesión; `ine_cnt_renta_disponible.csv` (nacional/CCAA) |",
          "| Hogares por provincia antes de 2021 | No encontrado | op. ECP tablas 60131–60136 (desde 2021); op. CENSOPV (8) solo viviendas 2011 (3457, 3456) | Censo 2011 de hogares por provincia (no localizado en la API); ECP 2021+ |",
          "| Proyección de hogares | Descartada: es proyección, no dato observado | op. PROH (70), tabla 54562 | No usada |",
          "| Hipotecas (base antigua) | Series 1994–2003; solo nacional y provincia con 'Total fincas' | tablas 3232, 3233, 3241 | No usadas: la base nueva (76317) cubre 2003–2026 solo para viviendas |",
          "| Hipotecas: unidad del importe | Confirmar en metadatos INE | tabla 76317 | Unidad inferida por magnitud (miles de euros); FK_Unidad=7 |",
          "| Código INE de municipio | La API no lo incluye en el nombre de serie | tablas 59060, 59061, 39363 | Unir por nombre con el catálogo de municipios (no descargado) |",
          "| IPVA en euros | No existe: solo índices y variación anual | tablas de ponderaciones 50015, 50016, 50083, 59062–59067 (solo pesos) | Ninguna |",
          "| Población por país de nacionalidad concreto y provincia (stock) | Solo agrupaciones de países en 77023 | 77023; 77099 (lugar de nacimiento) | Flujos por 3 países principales desde 2023 (59020); país de nacimiento (79278) |",
          "| ECP por provincia en tabla completa (56947) | 'No puede mostrarse por restricciones de volumen' | 56947 con nult=4 y 40 | Descarga serie a serie con DATOS_SERIE (77023) |",
          "| PIB provincial, unidad | Etiqueta de FK_Unidad=7 no verificada | 80109 | Unidad inferida (miles de euros) |",
          "| Duplicados INE | Balears, Illes aparece dos veces con valores idénticos (ETDP3633/ETDP4170; 6150) | 6150 | Se conserva una serie |",
          "| Municipios homónimos de provincia (VUT) | En 39363 un nombre puede ser provincia o municipio | 39363 vs 39364 | Se descarta la serie si su último valor coincide con la provincia de 39364 |",
          "| Serie IPC alquiler con ECOICOP v1 | Cambio de clasificación | 76137 (v1) vs 76142 (ECOICOP v2) | Empalme no hecho; usar con cuidado |",
          ""]
    FALLIDAS_MD.write_text("\n".join(L), encoding="utf-8")


def main() -> int:
    errores = 0
    for nombre, fn in JOBS:
        try:
            fn()
        except Exception as e:  # noqa: BLE001
            errores += 1
            print(f"[fallo] {nombre}: {e}")
            registrar(nombre, "", "", e, "pendiente de revisión")
    escribir_fallidas()
    print(f"terminado: {len(JOBS) - errores} OK, {errores} fallidos")
    return 0 if errores == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
