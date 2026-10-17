"""V16-F1 intervenciones: construye intervenciones.csv a partir de (a) los XML del BOE guardados en ../boe/ y (b) los
valores transcritos a mano de las ediciones de «Tributación Autonómica. Medidas» (Ministerio de Hacienda) que figuran abajo.
No accede a la red. Ejecutar: python3 -I data/raw/v16/intervenciones/_scripts/build_intervenciones.py
"""
import csv
import re
from pathlib import Path

ENT = Path(__file__).resolve().parents[1]
BOE = ENT / "boe"
COLS = ["id", "instrumento", "medida", "ambito", "cod_ine", "territorio", "fecha_publicacion", "fecha_efecto", "fecha_fin",
        "parametro", "valor", "unidad", "fuente_normativa", "url", "verificacion", "notas"]
FILAS = []


def meta(i):
    x = (BOE / (i + ".xml")).read_text(encoding="utf-8", errors="replace")
    g = lambda t: (re.search(r"<%s>([^<]*)</%s>" % (t, t), x) or [None, ""])[1]
    f = lambda s: "%s-%s-%s" % (s[:4], s[4:6], s[6:8]) if len(s) == 8 else ""
    return f(g("fecha_publicacion")), f(g("fecha_vigencia")), f(g("fecha_derogacion"))


def boe_url(i):
    return "https://www.boe.es/buscar/act.php?id=" + i


def R(id, ins, medida, amb, cod, terr, pub, ef, fin, par, val, uni, fuente, url, ver, notas=""):
    FILAS.append(dict(zip(COLS, [id, ins, medida, amb, cod, terr, pub, ef, fin, par, val, uni, fuente, url, ver, notas])))


VER_BOE = "VERIFICADA (texto de la disposición)"

# ---------------------------------------------------------------- 1. ITP y AJD (Ministerio de Hacienda, Tributación Autonómica. Medidas AAAA)
def hurl(y):
    if y <= 2020:
        return "https://www.hacienda.gob.es/SGFAL/FinanciacionTerritorial/Autonomica/Cap%C3%ADtulo%20I%20Tributaci%C3%B3n%20Auton%C3%B3mica%20" + str(y) + ".pdf"
    return "https://www.hacienda.gob.es/SGFAL/FinanciacionTerritorial/Autonomica/Capitulo-I-Tributacion-Autonomica-%d.pdf" % y


CCAA = {"01": "Andalucía", "02": "Aragón", "03": "Principado de Asturias", "04": "Illes Balears", "05": "Canarias", "06": "Cantabria",
        "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña", "10": "Comunitat Valenciana", "11": "Extremadura",
        "12": "Galicia", "13": "Comunidad de Madrid", "14": "Región de Murcia", "17": "La Rioja"}
# (cod, fecha_efecto, edicion_fuente, exacta, tipo_minimo, tipo_maximo_escala_o_None, nota)
ITP = [
    ("01", "2010-01-01", 2010, False, 7, 8, "7 % hasta 400.000 euros de valor real y 8 % el resto (garajes: 7 % hasta 30.000 euros)"),
    ("01", "2012-01-01", 2012, False, 8, 10, "escala 8-10 % (inmuebles) y otra para plazas de garaje"),
    ("01", "2021-04-28", 2021, True, 7, None, "tipo único 7 % desde el 28-04-2021 (hasta esa fecha, escala 8-10 %)"),
    ("02", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("02", "2016-01-01", 2016, False, 8, 10, "escala 8-10 % (la edición 2015 aún recoge el 7 %; primera edición que recoge la escala: 2016)"),
    ("03", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("03", "2010-07-15", 2010, True, 8, 10, "escala 8-10 % por tramos de base liquidable desde el 15-07-2010"),
    ("04", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("04", "2012-05-01", 2012, True, 7, 10, "escala 7-10 % (garajes 7-8 %) desde el 01-05-2012"),
    ("04", "2013-01-01", 2013, True, 8, 10, "escala 8-10 % (garajes 8-9 %) desde el 01-01-2013"),
    ("04", "2016-01-01", 2016, False, 8, 11, "escala 8-11 % (primera edición que lo recoge: 2016)"),
    ("04", "2022-01-01", 2022, False, 8, 11.5, "escala 8-11,5 % (primera edición que lo recoge: 2022)"),
    ("04", "2023-01-01", 2023, False, 8, 13, "escala 8-13 % (garajes 8-9 %; primera edición que lo recoge: 2023)"),
    ("05", "2010-01-01", 2010, False, 6.5, None, "tipo único 6,5 % en todo el periodo"),
    ("06", "2010-01-01", 2010, False, 7, 8, "7 % hasta 300.000 euros y 8 % el resto (garajes: 7 % hasta 30.000 euros)"),
    ("06", "2013-01-01", 2013, False, 8, 10, "8 % hasta 300.000 euros y 10 % el resto (cambio de 2013 según la edición 2013)"),
    ("06", "2018-01-01", 2018, False, 8, 10, "10 % con carácter general y 8 % si la base imponible del IRPF del ejercicio anterior es inferior a 30.000 euros (edición 2018)"),
    ("06", "2019-01-01", 2019, False, 10, None, "tipo único 10 % (edición 2019)"),
    ("06", "2024-01-01", 2024, False, 9, None, "tipo único 9 % (edición 2024)"),
    ("07", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("07", "2013-01-01", 2013, False, 8, 10, "8 % sobre el tramo de valor real hasta 250.000 euros y 10 % el resto, desde 2013 según la edición 2013"),
    ("08", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("08", "2012-01-01", 2012, False, 8, None, "tipo único 8 % (primera edición que lo recoge: 2012)"),
    ("08", "2016-06-01", 2016, True, 9, None, "tipo único 9 % desde el 01-06-2016"),
    ("09", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("09", "2010-07-01", 2010, True, 8, None, "tipo único 8 % desde el 01-07-2010"),
    ("09", "2013-08-01", 2013, True, 10, None, "tipo único 10 % desde el 01-08-2013"),
    ("09", "2017-01-01", 2017, False, 10, 11, "escala 10-11 % (primera edición que lo recoge: 2017)"),
    ("09", "2025-01-01", 2025, False, 10, 13, "escala 10-13 % (primera edición que lo recoge: 2025)"),
    ("10", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("10", "2013-01-01", 2013, False, 8, None, "tipo temporal 8 % para 2013 y 2014 según la edición 2013; sustituido el 06-08-2013"),
    ("10", "2013-08-06", 2013, True, 10, None, "tipo único 10 % con carácter indefinido desde el 06-08-2013"),
    ("10", "2023-01-01", 2023, False, 10, None, "10 % y tipo incrementado del 11 % si el valor supera 1.000.000 de euros (primera edición que lo recoge: 2023)"),
    ("10", "2026-06-01", 2026, True, 9, None, "9 % desde el 01-06-2026 (11 % si el valor supera 1.000.000 de euros)"),
    ("11", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("11", "2011-01-01", 2011, False, 7, 10, "escala 7-10 % (edición 2011)"),
    ("11", "2012-01-01", 2012, False, 8, 11, "escala 8-11 % (edición 2012)"),
    ("12", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("12", "2013-03-01", 2013, True, 10, None, "tipo único 10 % desde el 01-03-2013"),
    ("12", "2022-01-01", 2022, False, 9, None, "tipo único 9 % (primera edición que lo recoge: 2022)"),
    ("12", "2024-01-01", 2024, False, 8, None, "tipo único 8 % (primera edición que lo recoge: 2024)"),
    ("13", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("13", "2014-01-01", 2014, False, 6, None, "tipo único 6 % (la edición 2014 recoge la reducción del 7 % al 6 % en 2014; día exacto no recogido)"),
    ("14", "2010-01-01", 2010, False, 7, None, "tipo único 7 %"),
    ("14", "2013-07-11", 2013, True, 8, None, "tipo único 8 % desde el 11-07-2013"),
    ("14", "2025-01-01", 2025, False, 7.75, None, "tipo único 7,75 % (primera edición que lo recoge: 2025)"),
    ("17", "2010-01-01", 2010, False, 7, None, "tipo único 7 % en todo el periodo"),
]
# AJD: (cod, efecto, edicion, exacta, tipo, nota)
AJD = [
    ("01", "2010-01-01", 2010, False, 1.0, ""), ("01", "2012-01-01", 2012, False, 1.5, "primera edición que lo recoge: 2012"),
    ("01", "2021-04-28", 2021, True, 1.2, "desde el 28-04-2021 (hasta entonces 1,5 %)"),
    ("02", "2010-01-01", 2010, False, 1.0, ""), ("02", "2016-01-01", 2016, False, 1.5, "primera edición que lo recoge: 2016"),
    ("03", "2010-01-01", 2010, False, 1.0, ""), ("03", "2010-07-15", 2010, True, 1.2, "desde el 15-07-2010"),
    ("04", "2010-01-01", 2010, False, 1.0, ""), ("04", "2013-01-01", 2013, False, 1.2, "primera edición que lo recoge: 2013"),
    ("04", "2020-01-01", 2020, False, 1.5, "primera edición que lo recoge: 2020"),
    ("05", "2010-01-01", 2010, False, 0.75, "tipo 0,75 % en todo el periodo"),
    ("06", "2010-01-01", 2010, False, 1.0, ""), ("06", "2013-01-01", 2013, False, 1.5, "primera edición que lo recoge: 2013"),
    ("07", "2010-01-01", 2010, False, 1.0, ""), ("07", "2013-01-01", 2013, False, 1.5, "primera edición que lo recoge: 2013"),
    ("08", "2010-01-01", 2010, False, 1.0, ""), ("08", "2012-01-01", 2012, False, 1.25, "primera edición que lo recoge: 2012"),
    ("08", "2016-06-01", 2016, True, 1.5, "desde el 01-06-2016"),
    ("09", "2010-01-01", 2010, False, 1.0, ""), ("09", "2010-07-01", 2010, True, 1.2, "desde el 01-07-2010"),
    ("09", "2012-01-01", 2012, False, 1.5, "primera edición que lo recoge: 2012"),
    ("10", "2010-01-01", 2010, False, 1.0, ""), ("10", "2012-01-01", 2012, False, 1.2, "temporal para 2012-2013 según la edición 2013"),
    ("10", "2013-08-06", 2013, True, 1.5, "desde el 06-08-2013"), ("10", "2026-06-01", 2026, True, 1.4, "desde el 01-06-2026"),
    ("11", "2010-01-01", 2010, False, 1.0, ""), ("11", "2011-01-01", 2011, True, 1.15, "desde el 01-01-2011"),
    ("11", "2012-01-01", 2012, False, 1.2, "primera edición que lo recoge: 2012"), ("11", "2016-12-15", 2016, True, 1.5, "desde el 15-12-2016"),
    ("12", "2010-01-01", 2010, False, 1.0, ""), ("12", "2013-01-01", 2013, False, 1.5, "primera edición que lo recoge: 2013"),
    ("13", "2010-01-01", 2010, False, 1.0, ""), ("13", "2014-01-01", 2014, False, 0.75, "reducción de 1 % a 0,75 % en 2014; día exacto no recogido"),
    ("14", "2010-01-01", 2010, False, 1.0, ""), ("14", "2012-01-01", 2012, False, 1.2, "primera edición que lo recoge: 2012"),
    ("14", "2013-07-11", 2013, True, 1.5, "desde el 11-07-2013"),
    ("17", "2010-01-01", 2010, False, 1.0, "tipo 1 % en todo el periodo"),
]
NOTA_H = ("Fuente: Ministerio de Hacienda, «Tributación Autonómica. Medidas %d», cap. I, apartado 4 (resumen del ejercicio de competencias normativas). "
          "La ley autonómica que introduce el cambio NO está identificada en la fuente y NO se ha contrastado. ")


def tramos(lista, ins, nom_ins, nom_par, nom_par_max):
    por = {}
    for t in lista:
        por.setdefault(t[0], []).append(t)
    for cod, ts in por.items():
        ts.sort(key=lambda t: t[1])
        for k, t in enumerate(ts):
            fin = ""
            if k + 1 < len(ts):
                d = ts[k + 1][1]
                y, m, dd = map(int, d.split("-"))
                import datetime
                fin = (datetime.date(y, m, dd) - datetime.timedelta(days=1)).isoformat()
            ed = t[2]
            esc = (len(t) == 7 and t[5] is not None)
            tipo, mx, nota = (t[4], t[5], t[6]) if len(t) == 7 else (t[4], None, t[5])
            par = nom_par + (" (tipo mínimo de la escala)" if mx is not None and ins == "itp" else "")
            base = "%s-%s-%s" % (ins.upper(), cod, t[1])
            ex = "" if t[3] else "Fecha de efecto aproximada: 1 de enero del año de la primera edición que recoge el valor (la fecha exacta consta en la ley autonómica, no contrastada). "
            R(base, ins, "%s, tipo general, %s" % (nom_ins, CCAA[cod]), "ccaa", cod, CCAA[cod], "", t[1], fin, par, tipo, "%", "Hacienda-TA-%d-I-4" % ed, hurl(ed),
              "SECUNDARIA (Ministerio de Hacienda, Tributación Autonómica. Medidas %d)" % ed, NOTA_H % ed + ex + nota)
            if mx is not None and ins == "itp":
                R(base + "-max", ins, "%s, tipo máximo de la escala, %s" % (nom_ins, CCAA[cod]), "ccaa", cod, CCAA[cod], "", t[1], fin, nom_par_max, mx, "%",
                  "Hacienda-TA-%d-I-4" % ed, hurl(ed), "SECUNDARIA (Ministerio de Hacienda, Tributación Autonómica. Medidas %d)" % ed, NOTA_H % ed + ex + nota)


tramos(ITP, "itp", "ITP (TPO), transmisión de inmuebles, régimen común", "tipo general ITP", "tipo máximo ITP")
tramos(AJD, "ajd", "AJD (cuota gradual, documentos notariales), régimen común", "tipo general AJD", "")
for cod, nom, ter in (("15", "Navarra", "Comunidad Foral de Navarra"), ("16", "País Vasco", "País Vasco")):
    for ins in ("itp", "ajd"):
        R("%s-%s-foral" % (ins.upper(), cod), ins, "%s: régimen foral, fuera del régimen común de tributos cedidos" % ins.upper(), "ccaa", cod, nom, "", "2010-01-01", "",
          "régimen", "foral", "", "Hacienda-TA-2026-I-4", hurl(2026), "SECUNDARIA (Ministerio de Hacienda, Tributación Autonómica. Medidas 2026)",
          "Los tipos forales no se han recogido: la fuente cubre solo las CCAA de régimen común. Tipos forales: NO VERIFICADOS (requieren las normas forales de cada territorio histórico y la Ley Foral de Navarra).")

# ---------------------------------------------------------------- 2. Topes de actualización de rentas
def topes():
    t = "tope_actualizacion_rentas"
    pub, vig, _ = meta("BOE-A-2022-4972")
    R("TOPE-RDL6-2022", t, "RDL 6/2022, art. 46: limitación extraordinaria de la actualización anual de la renta (IGC)", "estatal", "00", "España", pub, vig, "2022-06-30",
      "límite de actualización anual de la renta", "", "variación anual del Índice de Garantía de Competitividad (IGC)", "BOE-A-2022-4972", boe_url("BOE-A-2022-4972"), VER_BOE,
      "Artículo 46: para actualizaciones cuya anualidad se cumple entre la entrada en vigor y el 30-06-2022; el texto remite al IGC (Ley 2/2015) y no fija una cifra; el 2 % que se cita habitualmente no figura en el artículo.")
    pub, vig, _ = meta("BOE-A-2022-10557")
    R("TOPE-RDL11-2022", t, "RDL 11/2022: prórroga del límite (IGC) hasta el 31-12-2022", "estatal", "00", "España", pub, "2022-07-01", "2022-12-31",
      "límite de actualización anual de la renta", "", "variación anual del IGC", "BOE-A-2022-10557", boe_url("BOE-A-2022-10557"), VER_BOE,
      "Modifica el art. 46 del RDL 6/2022; entra en vigor el " + vig + "; el primer día de actualizaciones cubiertas es 2022-07-01.")
    pub, vig, _ = meta("BOE-A-2022-22685")
    R("TOPE-RDL20-2022", t, "RDL 20/2022: prórroga del límite (IGC) hasta el 31-12-2023", "estatal", "00", "España", pub, "2023-01-01", "2023-12-31",
      "límite de actualización anual de la renta", "", "variación anual del IGC", "BOE-A-2022-22685", boe_url("BOE-A-2022-22685"), VER_BOE,
      "Nueva redacción del art. 46 del RDL 6/2022; en vigor desde " + vig + "; cubre actualizaciones de 2023.")
    pub, vig, _ = meta("BOE-A-2023-12203")
    R("TOPE-L12-2023-2024", t, "Ley 12/2023, disp. final 6.ª: límite del 3 % en 2024", "estatal", "00", "España", pub, "2024-01-01", "2024-12-31",
      "límite de actualización anual de la renta", 3, "%", "BOE-A-2023-12203", boe_url("BOE-A-2023-12203"), VER_BOE,
      "DF 6.ª, apartado 2: actualizaciones entre 2024-01-01 y 2024-12-31, sin exceder el 3 % (gran tenedor: pacto sin exceder el 3 %; resto: en defecto de pacto, no más del 3 %). La misma DF mantiene el IGC hasta 2023-12-31.")
    pub, vig, _ = meta("BOE-A-2024-26685")
    R("TOPE-IRAV-2025", t, "Índice de referencia para la actualización anual de los contratos de arrendamiento de vivienda (IRAV)", "estatal", "00", "España", pub, "2025-01-01", "",
      "límite de actualización anual de la renta", "", "IRAV (índice INE)", "BOE-A-2024-26685", boe_url("BOE-A-2024-26685"), VER_BOE,
      "Resolución de 18-12-2024 del INE (efectos desde 2025-01-01) en aplicación de la disp. adicional 11.ª de la LAU añadida por la Ley 12/2023, DF 1.ª; el valor mensual lo publica el INE y no se recoge aquí. Cifra mensual: NO incluida.")


topes()


# ---------------------------------------------------------------- 3. Bono Alquiler Joven y planes estatales
def bono_planes():
    pub, vig, _ = meta("BOE-A-2022-802")
    b = "BONO-RD42-2022"
    for par, val, uni, nota in (("edad máxima", 35, "años", "art. 6.1.a: hasta 35 años incluida, en el momento de solicitar la ayuda"),
                                ("importe mensual", 250, "euros", "preámbulo V: ayuda de 250 euros mensuales"),
                                ("ingresos máximos de la unidad de convivencia", 3, "veces el IPREM", "preámbulo V: no superiores a 3 veces el IPREM"),
                                ("renta máxima del alquiler", 600, "euros/mes", "art. 8: renta o precio de cesión igual o inferior a 600 euros mensuales (300 si es habitación); las CCAA pueden elevarlo hasta 900"),
                                ("duración de la ayuda", 24, "meses", "art. 12: dos años")):
        R("%s-%s" % (b, par.split()[0]), "bono_alquiler_joven", "Bono Alquiler Joven (RD 42/2022, título I)", "estatal", "00", "España", pub, vig, "", par, val, uni,
          "BOE-A-2022-802", boe_url("BOE-A-2022-802"), VER_BOE, nota + ". Convocatorias autonómicas (fechas de resolución, requisitos propios) NO incorporadas. Vigencia posterior a 2025 NO verificada.")
    planes = [("BOE-A-2008-20751", "Plan Estatal de Vivienda y Rehabilitación 2009-2012", "2009-2012", "2012-12-31"),
              ("BOE-A-2013-3780", "Plan Estatal de fomento del alquiler de viviendas, la rehabilitación edificatoria y la regeneración y renovación urbanas 2013-2016", "2013-2016", "2016-12-31"),
              ("BOE-A-2018-3358", "Plan Estatal de Vivienda 2018-2021", "2018-2021", "2021-12-31"),
              ("BOE-A-2022-802", "Plan Estatal para el acceso a la vivienda 2022-2025", "2022-2025", "2025-12-31"),
              ("BOE-A-2026-8872", "Plan Estatal de Vivienda 2026-2030", "2026-2030", "2030-12-31")]
    for i, nom, per, fin in planes:
        p, v, _ = meta(i)
        R("PLAN-" + per, "plan_estatal", nom, "estatal", "00", "España", p, v, fin, "periodo del plan", per, "años", i, boe_url(i), VER_BOE,
          "fecha_efecto = entrada en vigor del real decreto; fecha_fin = 31 de diciembre del último año del periodo que da nombre al plan (según el título); prórrogas y ampliaciones de plazo (p. ej. 2017, 2022) NO incorporadas.")


bono_planes()


# ---------------------------------------------------------------- 4. Avales ICO
def avales():
    i = "BOE-A-2024-9128"
    p, v, _ = meta(i)
    for par, val, uni, nota in (("edad máxima (programa jóvenes)", 35, "años", "ningún adquirente puede haber cumplido 36 años en la fecha del préstamo"),
                                ("ingresos máximos del adquirente", 4.5, "veces el IPREM", "familias con menores: +0,3 veces el IPREM por menor; familia monoparental +70 %"),
                                ("cobertura del aval", 20, "% del principal", "25 % si la vivienda tiene calificación energética D o superior"),
                                ("importe global máximo de avales", 2500, "millones de euros", "límite del art. 191 del RDL 5/2023")):
        R("AVAL-ICO-2024-" + par.split()[0], "avales_ico", "Línea de avales para la adquisición de primera vivienda de jóvenes y familias con menores a cargo (convenio MIVAU-ICO)", "estatal", "00",
          "España", p, p, "", par, val, uni, i, boe_url(i), VER_BOE,
          nota + ". Fuente: Resolución de 5-05-2024 que publica el convenio (BOE 2024-05-07); fecha_efecto = fecha de publicación (el convenio rige desde su firma, fecha no recogida; vigencia 15 años). Modificaciones posteriores NO comprobadas.")


avales()


# ---------------------------------------------------------------- 6. Suspensiones de desahucios y lanzamientos
def desahucios():
    s = "suspension_desahucios"
    cadena = [("RDL 11/2020", "BOE-A-2020-4208", "", "art. 1: suspensión del desahucio y de los lanzamientos en arrendamiento para hogares vulnerables por COVID-19; sin fecha propia de fin (ligada a la finalización del estado de alarma); sustituida por prórrogas posteriores"),
              ("RDL 37/2020", "BOE-A-2020-16824", "", "art. 1: suspensión durante el estado de alarma declarado por RD 926/2020 (prorrogado por RD 956/2020); sin fecha propia en el artículo"),
              ("RDL 8/2021", "BOE-A-2021-7351", "2021-08-09", ""), ("RDL 16/2021", "BOE-A-2021-13259", "2021-10-31", ""),
              ("RDL 21/2021", "BOE-A-2021-17456", "2022-02-28", ""), ("RDL 2/2022", "BOE-A-2022-2849", "2022-09-30", ""),
              ("RDL 11/2022", "BOE-A-2022-10557", "2022-12-31", ""), ("RDL 20/2022", "BOE-A-2022-22685", "2023-06-30", ""),
              ("RDL 5/2023", "BOE-A-2023-15135", "2023-12-31", ""), ("RDL 8/2023", "BOE-A-2023-26452", "2024-12-31", ""),
              ("RDL 9/2024", "BOE-A-2024-26915", "2025-12-31", "derogado: Resolución de 22-01-2025 (BOE-A-2025-1136)"),
              ("RDL 1/2025", "BOE-A-2025-1560", "2025-12-31", "modifica los arts. 1 y 1 bis con los efectos de su disposición transitoria única.2 (continuidad respecto del RDL 9/2024)"),
              ("RDL 16/2025", "BOE-A-2025-26458", "2026-12-31", "derogado por no convalidación: Resolución de 27-01-2026 (BOE-A-2026-2024)"),
              ("RDL 2/2026", "BOE-A-2026-2547", "2026-12-31", "derogado por no convalidación: Resolución de 26-02-2026 (BOE-A-2026-4667)")]
    for nom, i, fin_prev, nota in cadena:
        p, v, der = meta(i)
        fin = fin_prev
        n2 = nota
        if der and nom in ("RDL 9/2024", "RDL 16/2025", "RDL 2/2026"):
            n2 = "fecha_fin = fecha de derogación (%s); fin previsto en el texto: %s; %s" % (der, fin_prev, nota)
            fin = der
        elif fin_prev:
            n2 = "RD-ley modifica los arts. 1 y 1 bis del RDL 11/2020; fin del plazo según el texto: %s. %s" % (fin_prev, nota)
        R("DESAHUCIO-" + nom.replace(" ", "").replace("/", "-"), s, "%s: suspensión extraordinaria de desahucios y lanzamientos de hogares vulnerables (RDL 11/2020, arts. 1 y 1 bis)" % nom,
          "estatal", "00", "España", p, v, fin, "plazo de la suspensión", fin_prev, "fecha", i, boe_url(i), VER_BOE, n2)
    p, v, _ = meta("BOE-A-2024-9699")
    R("LANZAMIENTO-HIP-RDL1-2024", s, "RDL 1/2024: suspensión de lanzamientos de vivienda habitual en ejecuciones hipotecarias de colectivos vulnerables (Ley 1/2013, art. 1.1)", "estatal", "00", "España",
      p, v, "2028-05-15", "plazo de la suspensión", "2028-05-15", "fecha", "BOE-A-2024-9699", boe_url("BOE-A-2024-9699"), VER_BOE,
      "El texto fija «quince años desde la entrada en vigor» de la Ley 1/2013 (15-05-2013); la fecha 2028-05-15 es un cálculo a partir de ese plazo. Plazo anterior: 2024-05-15 (RDL 6/2020, según el preámbulo).")


desahucios()


# ---------------------------------------------------------------- 7. Golden visa
def golden():
    i = "BOE-A-2025-76"
    p, v, _ = meta(i)
    R("GOLDEN-LO1-2025", "golden_visa", "Supresión de la autorización de residencia por inversión (arts. 63-67 Ley 14/2013), LO 1/2025, disp. final 21.ª", "estatal", "00", "España", p, "2025-04-03", "",
      "régimen de residencia por inversión inmobiliaria", "suprimido", "", i, boe_url(i), VER_BOE,
      "DF 21.ª, apartado uno: se dejan sin contenido los arts. 63 a 67 de la Ley 14/2013. DF 38.ª: la ley entra en vigor a los tres meses de su publicación (BOE 2025-01-03); 2025-04-03 es la fecha de vigencia que da la API del BOE.")
    R("GOLDEN-LO1-2025-DT1", "golden_visa", "Régimen transitorio: solicitudes presentadas antes de la entrada en vigor (LO 1/2025, disp. final 21.ª, que añade DT 1.ª a la Ley 14/2013)", "estatal", "00", "España", p,
      "2025-04-03", "", "régimen transitorio", "solicitudes previas conservan la normativa de la fecha de presentación", "", i, boe_url(i), VER_BOE,
      "Texto de la DT 1.ª leído. La DT 2.ª (renovaciones) se añade en la misma disposición; su contenido NO se ha transcrito.")


golden()


# ---------------------------------------------------------------- 8. IBI vacías y 10. incentivo IRPF
def ibi_irpf():
    i = "BOE-A-2023-12203"
    p, v, _ = meta(i)
    for k, (par, val, uni, nota) in enumerate((("recargo máximo IBI, vivienda desocupada más de 2 años (titular de 4 o más inmuebles residenciales)", 50, "% de la cuota líquida", ""),
                                ("recargo máximo IBI, desocupación superior a 3 años", 100, "% de la cuota líquida", "modulable según el tiempo de desocupación"),
                                ("incremento adicional del recargo (titular de 2 o más inmuebles desocupados en el mismo municipio)", 50, "puntos porcentuales", ""))):
        R("IBI-L12-2023-%d" % (k + 1), "ibi_recargo_vacias", "Ley 12/2023, disp. final 3.ª: nueva redacción del art. 72.4 TRLRHL (recargo del IBI a inmuebles residenciales desocupados)",
          "estatal", "00", "España", p, v, "", par, val, uni, i, boe_url(i), VER_BOE,
          "Habilita a los ayuntamientos; la aplicación efectiva exige ordenanza fiscal municipal. Ordenanzas municipales concretas: NO verificadas (ver ficha). " + nota)
    for letra, val, desc in (("a", 90, "nuevo contrato en zona tensionada con rebaja de la renta inicial superior al 5 %"),
                             ("b", 70, "primer alquiler a arrendatario de 18-35 años en zona tensionada, o arrendatario Administración/entidad sin fines lucrativos con alquiler social"),
                             ("c", 60, "vivienda rehabilitada en los dos años anteriores a la fecha del contrato"), ("d", 50, "cualquier otro caso")):
        R("IRPF-L12-2023-" + letra, "incentivo_fiscal_alquiler", "Reducción del rendimiento neto del alquiler de vivienda en el IRPF (art. 23.2 Ley 35/2006, redacción de la Ley 12/2023, DF 2.ª), letra " + letra, "estatal", "00",
          "España", p, v, "", "reducción del rendimiento neto positivo", val, "%", i, boe_url(i), VER_BOE,
          desc + ". Aplicable a contratos celebrados desde la entrada en vigor de la ley. Régimen anterior (reducción general del 60 %): NO verificado.")


ibi_irpf()


# ---------------------------------------------------------------- 9. Vivienda turística
def vut():
    t, m = "vut_regulacion", "vut_moratoria"
    i = "BOE-A-2024-26931"
    p, v, _ = meta(i)
    R("VUT-RD1312-2024", t, "Registro Único de Arrendamientos (RD 1312/2024): obligación para arrendamientos de corta duración y de temporada", "estatal", "00", "España", p, "2025-07-01", "",
      "efectos de las disposiciones", "2025-07-01", "fecha", i, boe_url(i), VER_BOE, "DF 4.ª: el real decreto entra en vigor el 2025-01-02 y despliega efectos el 2025-07-01.")
    i = "BOE-A-2024-281"
    p, v, _ = meta(i)
    R("VUT-CAT-DL3-2023", t, "Cataluña, Decreto-ley 3/2023: licencia urbanística previa para el uso turístico de viviendas en municipios con problemas de acceso a la vivienda", "ccaa", "09", "Cataluña", p, v, "",
      "régimen", "licencia urbanística previa (5 años, prorrogable)", "", i, boe_url(i), VER_BOE, "Art. 1 leído. fecha_publicacion = BOE; el DOGC publicó la norma antes (fecha no recogida).")
    i = "BOE-A-2025-14462"
    p, v, _ = meta(i)
    R("VUT-BAL-DL4-2025", m, "Illes Balears, Decreto-ley 4/2025: prohibición de nuevas declaraciones responsables de inicio de actividad turística en viviendas en propiedad horizontal", "ccaa", "04", "Illes Balears",
      p, v, "", "régimen", "prohibición de nuevas declaraciones (propiedad horizontal, salvo adosadas y pareados)", "", i, boe_url(i), VER_BOE,
      "Contenido de la DA 2.ª tomado del preámbulo; el articulado de la DA 2.ª no se ha transcrito.")
    i = "BOE-A-2025-26358"
    p, v, _ = meta(i)
    R("VUT-CAN-L6-2025", t, "Canarias, Ley 6/2025: ordenación sostenible del uso turístico de viviendas", "ccaa", "05", "Canarias", p, v, "", "régimen", "regulación general del uso turístico de viviendas", "", i, boe_url(i), VER_BOE,
      "Art. 1 leído (objeto y ámbito); los requisitos concretos no se han transcrito.")
    R("VUT-BCN-PEUAT-2017", m, "Barcelona, Pla especial urbanístic d'allotjaments turístics (PEUAT): zonas de decrecimiento, mantenimiento y crecimiento contenido", "municipio", "08019", "Barcelona", "2017-03-06", "2017-03-06", "",
      "régimen", "zonificación y límite de plazas", "", "BOPB 2017-03-06 (aprobación definitiva por el Plenari 2017-01-27)", "https://ajuntament.barcelona.cat/ecologiaurbana/sites/default/files/ManualOperatiu_PEUAT.pdf",
      "SECUNDARIA (Manual operatiu del PEUAT, Ajuntament de Barcelona; solo la referencia de aprobación y publicación, no el texto)", "Modificación posterior del plan (2021-2023) NO incorporada. Fecha de efecto = publicación en el BOPB (no comprobada en el boletín).")
    R("VUT-MAD-RESIDE-2025", t, "Madrid, Plan Reside (modificación del Plan General): protección del uso residencial; sustituye al Plan Especial de Hospedaje de 2019", "municipio", "28079", "Madrid", "2025-09-22", "2025-09-22", "",
      "régimen", "restricción del alojamiento turístico disperso en edificios residenciales", "", "BOCM 2025-09-22 (según nota jurídica de Cuatrecasas)", "https://www.cuatrecasas.com/es/spain/publico/art/plan-reside-plan-general-ordenacion-urbana-madrid",
      "NO VERIFICADA (fuente secundaria: nota de un despacho; BOCM no consultado)", "Suspensión de licencias y declaraciones responsables vigente desde 2024-04-25 según la misma nota. Plan Especial de Hospedaje 2019: NO incorporado (fecha no hallada).")
    R("VUT-VAL-MORATORIA-2024", m, "València: suspensión de licencias de apartamentos turísticos (Pleno 2024-05-28; prórroga de un año acordada en abril de 2025) y normas urbanísticas posteriores", "municipio", "46250", "València",
      "", "2024-05-28", "", "régimen", "suspensión de tramitación de nuevas licencias", "", "Pleno del Ayuntamiento de València, 2024-05-28 (BOP no consultado)", "https://www.valencia.es/cas/actualidad/-/content/pleno.-moratoria-apartamentos-tur%C3%ADsticos",
      "NO VERIFICADA (resultado de búsqueda; página del Ayuntamiento no leída)", "La aprobación definitiva de la normativa (marzo-abril de 2026) y su entrada en vigor no están confirmadas; fecha_fin vacía por esa razón.")


vut()


# ---------------------------------------------------------------- 11. Vivienda pública anunciada y entregada
def vp():
    R("VP-ANUNCIO-PEV2026", "vivienda_publica_anuncio", "Consejo de Ministros aprueba el Plan Estatal de Vivienda 2026-2030, dotado con 7.000 millones de euros", "estatal", "00", "España", "2026-04-21", "2026-04-21", "",
      "dotación anunciada", 7000, "millones de euros", "Consejo de Ministros 2026-04-21 (resumen)", "https://www.lamoncloa.gob.es/consejodeministros/resumenes/paginas/2026/210426-rueda-de-prensa-ministros.aspx",
      "VERIFICADA (documento oficial: La Moncloa, resumen del Consejo de Ministros)", "Cifra de dotación del plan; no es un recuento de viviendas.")
    R("VP-ANUNCIO-CASA47-A4", "vivienda_publica_anuncio", "Consejo de Ministros autoriza la cuarta adenda al convenio con CASA 47 (antes SEPES): 22 nuevos proyectos que suman 1.629 viviendas", "estatal", "00", "España", "2026-06-02",
      "2026-06-02", "", "viviendas en proyectos nuevos", 1629, "viviendas", "Consejo de Ministros 2026-06-02 (referencia)", "https://www.lamoncloa.gob.es/consejodeministros/referencias/Paginas/2026/20260602-referencia-rueda-de-prensa-ministros.aspx",
      "VERIFICADA (documento oficial: La Moncloa, referencia del Consejo de Ministros)", "El texto añade: 260 millones de euros en la adenda, 2.080 millones transferidos en total, 68 proyectos activos (44 de edificación con 3.266 viviendas y 24 de urbanización con potencial para 22.000 viviendas). El anuncio de 183.000 viviendas NO se ha incorporado: solo se localizó en prensa.")
    R("VP-ENTREGA-CD-2024", "vivienda_publica_entrega", "Calificaciones definitivas de viviendas protegidas concedidas en 2024 (Observatorio de Vivienda y Suelo, boletín estadístico 2024)", "estatal", "00", "España", "2025-07-04",
      "2024-01-01", "2024-12-31", "calificaciones definitivas de viviendas protegidas", 14371, "viviendas", "MIVAU, nota de prensa del Boletín estadístico 2024 del OVS (2025-07-04)",
      "https://www.mivau.gob.es/recursos_mfom/sala_prensa/250704_np_boletin_ovs.pdf", "VERIFICADA (documento oficial: nota de prensa del MIVAU)",
      "Calificación definitiva = vivienda protegida terminada y calificada, no entrega a hogares. +62,4 % sobre 2023. Calificaciones provisionales 2024: 23.967. Serie anual completa (boletines OVS y anuario, cap. 5): NO descargada.")


vp()

if __name__ == "__main__":
    # ids únicos (los de IBI se construyen de forma determinista)
    vistos = set()
    for f in FILAS:
        assert f["id"] not in vistos, f["id"]
        vistos.add(f["id"])
    with open(ENT / "intervenciones.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(FILAS)
    print(len(FILAS), "filas")
