"""Genera _manifest.csv de alquiler_turismo. Ejecutar con: python3 -I 03_manifiesto.py (desde cualquier directorio)."""
import csv, gzip, hashlib, json, os, re, zipfile

RAIZ = "/home/user/Econometr-a"
BASE = RAIZ + "/data/raw/v16/alquiler_turismo"
HOY = "2026-10-17"
COLS = "fuente,fichero,url,fecha_descarga,edicion,periodo,nivel_territorial,n_filas,sha256,licencia,redistribuible,notas".split(",")

CC = "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)"
LIC_IAB = "CC BY 4.0 declarada en https://insideairbnb.com/get-the-data/ (enlace a https://creativecommons.org/licenses/by/4.0/); datos no oficiales"
LIC_INE = "INE: reutilizacion con cita de la fuente (aviso legal, https://www.ine.es/aviso_legal)"
LIC_MAD = "CC BY (campo license_id=cc-by en https://datos.comunidad.madrid/catalogo/dataset/declaraciones_actividad_viviendas_uso_turistico)"
LIC_CAIB = "CC BY (license_id=cc-by en https://intranet.caib.es/opendatacataleg/dataset/<id>)"
LIC_GOBCAN = "Aviso Legal del Gobierno de Canarias (https://datos.canarias.es/portal/aviso-legal-y-condiciones-de-uso)"
LIC_ISTAC = "Aviso Legal del ISTAC (http://www.gobiernodecanarias.org/istac/aviso_legal.html)"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def filas(p):
    try:
        if p.endswith(".gz") and ".json" in p:
            return len(json.load(gzip.open(p, "rt", encoding="utf-8")))  # series
        op = gzip.open if p.endswith(".gz") else open
        with op(p, "rb") as f:
            n = sum(1 for _ in f)
        return max(n - 1, 0)
    except Exception:
        return ""


def rel(p):
    return os.path.relpath(p, RAIZ)


R = []


def add(fuente, p, url, edicion, periodo, nivel, lic, red, notas, n=None):
    R.append(dict(fuente=fuente, fichero=rel(p), url=url, fecha_descarga=HOY, edicion=edicion, periodo=periodo,
                  nivel_territorial=nivel, n_filas=filas(p) if n is None else n, sha256=sha(p), licencia=lic,
                  redistribuible=red, notas=notas))


# 1. Inside Airbnb
d = BASE + "/original/insideairbnb"
ruta = {"barcelona": "catalonia", "girona": "catalonia", "euskadi": "pv", "madrid": "comunidad-de-madrid",
        "malaga": "andaluc%C3%ADa", "sevilla": "andaluc%C3%ADa", "mallorca": "islas-baleares",
        "menorca": "islas-baleares", "valencia": "vc"}
for f in sorted(os.listdir(d)):
    if not f.endswith(".csv.gz"):
        continue
    m = re.match(r"listings_(\w+)_(\d{4}-\d{2}-\d{2})\.csv\.gz", f)
    c, fe = m.groups()
    add("insideairbnb", d + "/" + f, f"https://data.insideairbnb.com/spain/{ruta[c]}/{c}/{fe}/data/listings.csv.gz", fe, fe,
        "anuncio (lat/lon)", LIC_IAB, "sí",
        "listings detallado; instantanea trimestral; contiene host_name y textos libres: excluir de la capa publica; la de 2026-09 de BCN/MAD/MLG/MLL/VLC ya esta en data/raw/v9/insideairbnb")

# 2. Registros autonomicos
d = BASE + "/original/madrid_vut"
add("madrid_vut", d + "/declaraciones_actividad_vut_2026-10-17.csv",
    "https://datos.comunidad.madrid/dataset/914c95d2-455e-4797-893f-97b1e2b2426e/resource/41072914-3b76-46b2-bfff-4afdd48ed3cc/download/declaraciones_actividad_viviendas_uso_turistico.csv",
    "corte 2026-10-14 (metadata_modified)", "corte 2026-10", "direccion + localidad (sin fecha de alta)", LIC_MAD, "sí",
    "declaraciones responsables VUT (sin inscripcion en REmpresas Turisticas); solo direccion, sin titular; separador ;")
add("madrid_vut", d + "/declaraciones_actividad_vut_historico_2026-10-17.zip",
    "https://datos.comunidad.madrid/dataset/914c95d2-455e-4797-893f-97b1e2b2426e/resource/11fb61a4-99a8-405a-bc36-7631d8bc306b/download/declaraciones_actividad_viviendas_uso_turistico_historico.zip",
    "historico mensual (13 cortes)", "2025-04 a 2026-08 (meses 202504-202507, 202509, 202512, 202601, 202603-202608)",
    "direccion + localidad", LIC_MAD, "sí", "zip con 13 CSV mensuales (cortes irregulares: faltan 202508, 202510, 202511, 202602); permite altas/bajas por diferencia de cortes",
    n=len(zipfile.ZipFile(d + "/declaraciones_actividad_vut_historico_2026-10-17.zip").namelist()))
add("madrid_alojamientos", d + "/alojamientos_turisticos_2026-10-17.csv",
    "https://datos.comunidad.madrid/dataset/ef437c50-5b26-4843-92c3-d8eef5507fac/resource/260e80ac-2062-41f6-9f96-4902675b1078/download/alojamientos_turisticos.csv",
    "corte 2026-10-12", "corte 2026-10", "direccion + localidad + CP",
    "CC BY (license_id=cc-by en https://datos.comunidad.madrid/catalogo/dataset/alojamientos_turisticos)", "sí",
    "hoteles, hostales, apartamentos turisticos, etc. (no VUT); sin fecha de alta")
add("andalucia_rta", BASE + "/_terceros/openrta_all_2026-10-17.csv.gz",
    "https://datos.juntadeandalucia.es/api/v0/openrta/all?format=csv",
    "OpenRTA, catalogo modificado 2026-08-11", "registro completo; registration_date y activity_start_date",
    "establecimiento (municipality_id, coordenadas, referencia catastral)",
    "CC BY 4.0 (https://www.juntadeandalucia.es/datosabiertos/portal/dataset/openrta; license_url http://creativecommons.org/licenses/by/4.0/deed.es_ES)",
    "dudoso", "gzip del CSV original (69,7 MB descomprimido, separador |); incluye email, telefono, titular: datos personales; grupos 'Completa' y 'Por habitaciones' = VFT; fechas de alta con formato heterogeneo")
add("andalucia_rta", BASE + "/_terceros/openrta_openapi_2026-10-17.json",
    "https://datos.juntadeandalucia.es/api/v0/openrta/openapi.json", "2026-10-17", "-", "-", "CC BY 4.0", "sí", "especificacion OpenAPI de la API", n="")
d = BASE + "/original/baleares"
add("baleares_mallorca_alojamientos", d + "/allotjaments_turistics_mallorca_2026-10-17.csv",
    "https://intranet.caib.es/opendatacataleg/files/dataset/allotjaments_turistics_mallorca/allotjaments_turistics_mallorca.csv",
    "corte 2026-10-14", "corte 2026-10", "establecimiento (municipio)", LIC_CAIB.replace("<id>", "allotjaments-turistics-mallorca"), "sí",
    "hoteles, agroturismos, etc. (no ETV/HUT); Consell de Mallorca")
add("baleares_menorca_alojamientos", d + "/allotjaments_turistics_menorca_2026-10-17.csv",
    "https://intranet.caib.es/opendatacataleg/files/dataset/allotjaments_turistics_menorca/allotjaments_turistics_menorca.csv",
    "corte 2026-10-14", "corte 2026-10", "establecimiento", LIC_CAIB.replace("<id>", "allotjaments-turistics-de-menorca"), "sí",
    "Consell Insular de Menorca; incluye apartamentos turisticos")
add("baleares_mallorca_etv", BASE + "/_terceros/habitatges_turistics_mallorca_2026-10-17.csv",
    "https://intranet.caib.es/opendatacataleg/files/dataset/habitatges_turistics_mallorca/habitatges_turistics_mallorca.csv",
    "corte 2026-09-07", "corte 2026-09; campo 'Inici d'activitat' (fecha de alta)", "vivienda (municipio, UTM, lat/lon)",
    LIC_CAIB.replace("<id>", "habitatges-turistics-mallorca"), "dudoso",
    "registro de HUT y estades turistiques en habitatge (ETV) de Mallorca, con fecha de inicio de actividad; incluye explotador/es (nombres): datos personales")
add("baleares_menorca_etv", BASE + "/_terceros/estades_habitatges_turistics_menorca_2026-10-17.csv",
    "https://intranet.caib.es/opendatacataleg/files/dataset/estades_habitatges_turistics_menorca/estades_habitatges_turistics_menorca.csv",
    "corte 2026-09-07", "corte 2026-09 (sin fecha de alta)", "vivienda (poblacio, lat/lon)",
    LIC_CAIB.replace("<id>", "estades-i-habitatges-turistics-vacacionals-de-menorca"), "dudoso",
    "HTV y estades de Menorca; incluye telefono y nombre comercial: datos personales")
d = BASE + "/original/canarias"
add("canarias_vv", d + "/vivienda_vacacional_registro_2026-10-17.csv",
    "https://datos.canarias.es/catalogos/general/dataset/9f4355a2-d086-4384-ba72-d8c99aa2d544/resource/8ff8cc43-c00b-4513-8f42-a5b961c579e1/download/establecimientos-extrahoteleros-de-tipologia-vivienda-vacacional-inscritos-en-el-registro-genera.csv",
    "Registro General Turistico de Canarias, corte 2026-10-17", "corte 2026-10", "vivienda (municipio, isla, lat/lon)", LIC_GOBCAN, "sí",
    "sin fecha de alta; separador ;; incluye nombre comercial")
add("canarias_vv", d + "/diccionario_vivienda_vacacional_2026-10-17.csv",
    "https://datos.canarias.es/catalogos/general/dataset/9f4355a2-d086-4384-ba72-d8c99aa2d544/resource/07e101fc-ee77-4a0f-b1ae-b466dbb9e427/download/diccionario_datos_establecimientos-extrahoteleros-vivienda-vacacional.csv",
    "2026-10-17", "-", "-", LIC_GOBCAN, "sí", "diccionario de datos")
add("canarias_istac_vv", d + "/istac_C00065A_000061_v1.29_2026-10-17.csv",
    "https://datos.canarias.es/api/estadisticas/statistical-resources/v1.0/datasets/ISTAC/C00065A_000061/1.29.csv",
    "ISTAC C00065A_000061 v1.29", "2019-01 a ultimo mes publicado (mensual)", "isla y municipio", LIC_ISTAC, "sí",
    "viviendas vacacionales, plazas, ocupacion, estancia media e ingresos (estadistica oficial ISTAC, base en datos de plataformas)")

# 5. INE
d = BASE + "/original/ine_turismo"
INE = {
    "2072": ("EOAP", "provincias: plazas, apartamentos, grados de ocupacion, personal", "provincia"),
    "2083": ("EOAP", "puntos turisticos: plazas, apartamentos, ocupacion, personal", "punto turistico"),
    "75193": ("EOAP", "puntos turisticos (serie nueva)", "punto turistico"),
    "2021": ("EOAP", "CCAA: apartamentos, plazas, ocupacion", "CCAA"),
    "2022": ("EOAP", "zonas turisticas", "zona turistica"),
    "2082": ("EOAP", "viajeros y pernoctaciones por puntos turisticos", "punto turistico"),
    "75191": ("EOAP", "viajeros y pernoctaciones por puntos turisticos (serie nueva)", "punto turistico"),
    "2063": ("EOAP", "viajeros y pernoctaciones por provincias", "provincia"),
    "61766": ("EOT/EOAP/EOH", "viajeros y pernoctaciones por CCAA", "CCAA"),
    "75192": ("EOAP", "viajeros y pernoctaciones por CCAA (serie nueva)", "CCAA"),
    "1993": ("EOAP", "viajeros y pernoctaciones por CCAA (identica a 67191)", "CCAA"),
    "2025": ("EOT", "establecimientos, plazas y personal por tipo de alojamiento (identica a 3151)", "CCAA"),
    "61768": ("EOT", "establecimientos, plazas y personal por tipo de alojamiento", "CCAA"),
    "2074": ("EOH", "viajeros y pernoctaciones hoteleros por CCAA y provincias (identica a 67190)", "provincia"),
    "2066": ("EOH", "establecimientos, plazas, ocupacion y personal por provincias", "provincia"),
    "49371": ("EOH", "viajeros y pernoctaciones por CCAA y provincias (serie nueva)", "provincia"),
    "2078": ("EOH", "viajeros y pernoctaciones hoteleros por puntos turisticos", "punto turistico"),
    "2076": ("EOH", "establecimientos, plazas, ocupacion y personal por puntos turisticos", "punto turistico"),
    "75197": ("EOH", "viajeros y pernoctaciones por puntos turisticos (serie nueva)", "punto turistico"),
    "75198": ("EOH", "establecimientos, plazas, ocupacion por puntos turisticos (serie nueva)", "punto turistico"),
    "2039": ("EOH", "viajeros y pernoctaciones por zonas turisticas", "zona turistica"),
    "2013": ("EOH", "establecimientos, plazas, ocupacion por zonas turisticas", "zona turistica"),
    "48441": ("OAT", "ocupacion en alojamientos turisticos y otros de corta estancia (mensual)", "nacional/CCAA"),
    "48440": ("OAT", "ocupacion en alojamientos turisticos y otros de corta estancia (anual)", "nacional/CCAA"),
    "48424": ("OAT", "alojamientos y noches ocupados por residencia, puntos turisticos", "punto turistico"),
    "48429": ("OAT", "alojamientos y noches ocupados por residencia, puntos turisticos", "punto turistico"),
    "48427": ("OAT", "pernoctaciones por residencia, provincias", "provincia"),
    "48426": ("OAT", "pernoctaciones por residencia, puntos turisticos", "punto turistico"),
    "48431": ("OAT", "pernoctaciones por residencia, puntos turisticos", "punto turistico"),
    "48432": ("OAT", "pernoctaciones por residencia, zonas turisticas", "zona turistica"),
    "48423": ("OAT", "alojamientos y noches ocupados por residencia, nacional y CCAA", "CCAA"),
    "48428": ("OAT", "alojamientos y noches ocupados por residencia, nacional y CCAA", "CCAA"),
    "1989": ("IPAP", "indice de precios de apartamentos, general y modalidades", "nacional"),
    "2050": ("IPAP", "indice de precios de apartamentos, tarifas", "nacional"),
    "39364": ("VTE", "viviendas turisticas, plazas: nacional, CCAA, provincias", "provincia"),
    "39363": ("VTE", "viviendas turisticas, plazas: municipios", "municipio"),
    "46141": ("VTE", "viviendas turisticas, plazas y % sobre viviendas censadas", "nacional/CCAA/provincia"),
    "39365": ("VTE", "% viviendas turisticas sobre censadas: nacional, CCAA, provincias", "provincia"),
    "39366": ("VTE", "% viviendas turisticas sobre censadas: municipios", "municipio"),
}
for f in sorted(os.listdir(d)):
    m = re.match(r"ine_tabla_(\d+)_", f)
    t = m.group(1)
    if f.endswith(".dup"):
        continue
    op, desc, nivel = INE.get(t, ("INE", "", ""))
    exp = ""
    if t in ("1993", "2025", "2074"):
        exp = " Duplicada con otra tabla (mismo sha256): " + {"1993": "67191", "2025": "3151", "2074": "67190"}[t] + " (ver .dup)."
    add("ine_" + op.lower().replace("/", "_"), d + "/" + f, f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{t}?nult=1000",
        f"INE tabla {t} (Tempus, consulta {HOY})", "serie completa disponible (nult=1000)", nivel, LIC_INE, "sí",
        f"{op}: {desc}. JSON de Tempus (lista de series con Data) comprimido con gzip, sin transformar.{exp}" +
        (" VTE = medicion experimental de viviendas turisticas; ya hay version previa en data/raw/ine_v2_vut.csv (hasta 2026-05)." if op == "VTE" else ""))

with open(BASE + "/_manifest.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    w.writerows(R)
print(len(R), "filas")
