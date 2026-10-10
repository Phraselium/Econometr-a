"""Base de eventos de política de vivienda (v2) con fechas tomadas de fuente oficial (BOE y boletines).

Genera:
  data/raw/v2_eventos_politica.csv      (un evento por fila; ver COLS_EV)
  data/raw/v2_zonas_tensionadas.csv     (un municipio/ámbito por fila, con fecha de efecto de cada declaración)
  docs/v2/fallidas/eventos.md           (lo no verificable o discrepante)

Reproducibilidad: la tabla EVENTOS contiene las fechas esperadas; el script descarga el XML oficial
de cada norma (https://www.boe.es/diario_boe/xml.php?id=...) y comprueba título, fecha de publicación,
vigencia y derogación; además abre la página pública y comprueba que su <title> contiene el título de la norma.
Si algo no coincide, el estado pasa a DISCREPANCIA (no se corrige a mano). Los eventos sin fuente oficial
accesible se escriben con estado=NO VERIFICADO y sin fechas.
Caché: si el CSV existe no se rehace salvo FORCE=1 (src/utils_fetch.py).
"""
from __future__ import annotations

import datetime as dt
import html
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import utils_fetch as uf  # noqa: E402

ROOT = uf.ROOT
OUT_EV = "v2_eventos_politica.csv"
OUT_ZT = "v2_zonas_tensionadas.csv"
FALLIDAS = ROOT / "docs" / "v2" / "fallidas" / "eventos.md"
UA = {"User-Agent": "Mozilla/5.0 (econometria-vivienda-tfm; investigacion academica)"}
DICC_URL = "https://www.ine.es/daco/daco42/codmun/diccionario26.xlsx"

MESES = {m: i + 1 for i, m in enumerate(
    "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}
CCAA_COD = {"Cataluña": "09", "País Vasco": "16", "Navarra": "15", "Galicia": "12", "Principado de Asturias": "03",
            "Comunitat Valenciana": "10", "Illes Balears": "04", "Canarias": "05"}
CCAA_PROV = {"09": ["08", "17", "25", "43"], "16": ["01", "20", "48"], "15": ["31"], "12": ["15"], "03": ["33"]}

COLS_EV = ["id", "nombre", "norma", "fecha_publicacion", "fecha_entrada_vigor", "fecha_fin", "ambito",
           "codigos_ine_ccaa", "codigos_ine_provincia", "territorios_afectados", "mercado", "descripcion_breve",
           "url_oficial", "url_secundaria", "estado", "nota_verificacion", "verificado_utc"]


def D(s):  # fecha ISO o vacío
    return s or ""


# --------------------------------------------------------------------------------------------------
# Tabla de eventos. pub/vigor/fin = valores esperados que se contrastan con el XML oficial.
# bid = identificador BOE (BOE-A-..., DOGV-r-...). Las fechas de normas autonómicas se contrastan con la
# frase "Publicada en el <boletín> núm. N, de <fecha>" del propio BOE o con fecha_publicacion de DOGV-r.
# --------------------------------------------------------------------------------------------------
EV = [
    dict(id="E01", nombre="Ley 4/2013 de flexibilización y fomento del alquiler (LAU 2013)",
         norma="Ley 4/2013, de 4 de junio", bid="BOE-A-2013-5941", tit="Ley 4/2013, de 4 de junio",
         pub="2013-06-05", vigor="2013-06-06", ambito="nacional", ccaa="", prov="", terr="España",
         mercado="alquiler", rx_vigor=r"entrará en vigor el día siguiente al de su publicación",
         desc="Reforma de la LAU: prórroga obligatoria de 3 años, libre desistimiento a 6 meses, actualización de renta pactada y recuperación de la vivienda por necesidad."),
    dict(id="E02", nombre="RDL 7/2019 medidas urgentes en vivienda y alquiler",
         norma="Real Decreto-ley 7/2019, de 1 de marzo", bid="BOE-A-2019-3108", tit="Real Decreto-ley 7/2019, de 1 de marzo",
         pub="2019-03-05", vigor="2019-03-06", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"entrará en vigor el día siguiente al de su publicación",
         desc="Modifica la LAU: prórroga obligatoria de 5 años (7 si el arrendador es persona jurídica), fianza máxima de dos mensualidades y límites a garantías adicionales."),
    dict(id="E03", nombre="Ley 5/2019 reguladora de los contratos de crédito inmobiliario",
         norma="Ley 5/2019, de 15 de marzo", bid="BOE-A-2019-3814", tit="Ley 5/2019, de 15 de marzo",
         pub="2019-03-16", vigor="2019-06-16", ambito="nacional", ccaa="", prov="", terr="España", mercado="compra",
         rx_vigor=r"entrará en vigor a los tres meses de su publicación",
         desc="Ley hipotecaria: transparencia precontractual, reparto de gastos, límites al vencimiento anticipado y a intereses de demora, regulación de tipos de interés."),
    dict(id="E04", nombre="RDL 8/2020 (COVID): moratoria hipotecaria vivienda habitual",
         norma="Real Decreto-ley 8/2020, de 17 de marzo", bid="BOE-A-2020-3824", tit="Real Decreto-ley 8/2020, de 17 de marzo",
         pub="2020-03-18", vigor="2020-03-18", ambito="nacional", ccaa="", prov="", terr="España", mercado="compra",
         desc="Medidas COVID-19 que incluyen moratoria de deuda hipotecaria para vivienda habitual de deudores vulnerables (arts. 7-16)."),
    dict(id="E05", nombre="RDL 11/2020 (COVID): moratoria de alquiler y suspensión de desahucios",
         norma="Real Decreto-ley 11/2020, de 31 de marzo", bid="BOE-A-2020-4208", tit="Real Decreto-ley 11/2020, de 31 de marzo",
         pub="2020-04-01", vigor="2020-04-02", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Suspensión de desahucios y lanzamientos de hogares vulnerables, prórroga extraordinaria de contratos de alquiler y moratoria de la renta (arts. 1-9)."),
    dict(id="E06", nombre="RDL 37/2020: vulnerabilidad en vivienda (desahucios durante el estado de alarma)",
         norma="Real Decreto-ley 37/2020, de 22 de diciembre", bid="BOE-A-2020-16824", tit="Real Decreto-ley 37/2020, de 22 de diciembre",
         pub="2020-12-23", vigor="2020-12-23", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"entrará en vigor el mismo día de su publicación",
         desc="Suspensión del desahucio y lanzamiento arrendaticios de personas vulnerables sin alternativa habitacional durante el estado de alarma."),
    dict(id="E07", nombre="RDL 16/2025: prórroga de la suspensión de desahucios hasta 31-12-2026 (derogado)",
         norma="Real Decreto-ley 16/2025, de 23 de diciembre", bid="BOE-A-2025-26458", tit="Real Decreto-ley 16/2025, de 23 de diciembre",
         pub="2025-12-24", vigor="2025-12-25", fin="2026-01-28", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Prorrogaba hasta 2026-12-31 la suspensión de desahucios de hogares vulnerables; fecha de fin = derogación recogida en metadatos BOE."),
    dict(id="E08", nombre="RDL 2/2026: nueva prórroga de la suspensión de desahucios (derogado)",
         norma="Real Decreto-ley 2/2026, de 3 de febrero", bid="BOE-A-2026-2547", tit="Real Decreto-ley 2/2026, de 3 de febrero",
         pub="2026-02-04", vigor="2026-02-05", fin="2026-02-28", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Segundo intento de prórroga de medidas de vulnerabilidad en vivienda; fecha de fin = derogación recogida en metadatos BOE (prensa cita otra fecha)."),
    dict(id="E09", nombre="Ley catalana 11/2020 de contención de rentas",
         norma="Ley 11/2020 del Parlamento de Cataluña, de 18 de septiembre", bid="BOE-A-2020-11363",
         tit="Ley 11/2020, de 18 de septiembre, de medidas urgentes en materia de contención de rentas",
         pub="2020-09-21", vigor="2020-09-22", fin="2022-04-08", ambito="CCAA", ccaa="09", prov="08;17;25;43",
         terr="Cataluña: áreas con mercado de vivienda tenso (Barcelona y otros ámbitos)", mercado="alquiler",
         pub_regional=True,
         desc="Contención de rentas en áreas tensas con índice de referencia. Anulada en sus preceptos principales por STC 37/2022 (fin = publicación de la sentencia)."),
    dict(id="E10", nombre="STC 37/2022: anulación parcial de la Ley catalana 11/2020",
         norma="Sentencia del Tribunal Constitucional 37/2022, de 10 de marzo", bid="BOE-A-2022-5807", tit="Pleno. Sentencia 37/2022, de 10 de marzo de 2022",
         pub="2022-04-08", vigor="2022-04-08", ambito="CCAA", ccaa="09", prov="08;17;25;43", terr="Cataluña", mercado="alquiler",
         vigor_nota="Sentencia de 2022-03-10; produce efectos generales desde su publicación en el BOE (art. 38.1 LOTC).",
         desc="Declara inconstitucionales y nulos arts. 1, 6-13, 15 y 16.2, DA 1-4, DT 1 y DF 4.b de la Ley 11/2020 (competencia estatal sobre legislación civil/renta)."),
    dict(id="E11", nombre="RDL 6/2022 art. 46: limitación extraordinaria de la actualización anual de la renta",
         norma="Real Decreto-ley 6/2022, de 29 de marzo", bid="BOE-A-2022-4972", tit="Real Decreto-ley 6/2022, de 29 de marzo",
         pub="2022-03-30", vigor="2022-03-31", fin="2024-12-31", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Limita la actualización anual de rentas de contratos LAU; periodo 2022-2023 ligado al Índice de Garantía de Competitividad y 2024 al 3 % (texto consolidado). Fin = 31-12-2024."),
    dict(id="E12", nombre="RDL 11/2022: prórroga y modificación del tope de actualización de rentas",
         norma="Real Decreto-ley 11/2022, de 25 de junio", bid="BOE-A-2022-10557", tit="Real Decreto-ley 11/2022, de 25 de junio",
         pub="2022-06-26", vigor="2022-06-27", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Modifica el art. 46 del RDL 6/2022: prorroga la limitación de actualización de rentas y fija como referencia el Índice de Garantía de Competitividad."),
    dict(id="E13", nombre="RDL 20/2022: tope de actualización de rentas hasta 31-12-2023 y desahucios hasta 30-06-2023",
         norma="Real Decreto-ley 20/2022, de 27 de diciembre", bid="BOE-A-2022-22685", tit="Real Decreto-ley 20/2022, de 27 de diciembre",
         pub="2022-12-28", vigor="2022-12-28", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"entrará en vigor el mismo día de su publicación",
         desc="Prorroga el art. 46 RDL 6/2022 para 2023 (actualización limitada al IGC) y la suspensión de desahucios de hogares vulnerables hasta 30-06-2023."),
    dict(id="E14", nombre="Ley 12/2023 por el derecho a la vivienda",
         norma="Ley 12/2023, de 24 de mayo", bid="BOE-A-2023-12203", tit="Ley 12/2023, de 24 de mayo, por el derecho a la vivienda",
         pub="2023-05-25", vigor="2023-05-26", ambito="nacional", ccaa="", prov="", terr="España; declaración de zonas tensionadas por CCAA (ver ZT*)",
         mercado="alquiler",
         desc="Define gran tenedor, crea zonas de mercado residencial tensionado (art. 18) con límite de renta por índice de referencia, modifica la LAU y fija el 3 % en 2024."),
    dict(id="E15", nombre="Ley 12/2023 DF 6: tope del 3 % a la actualización de rentas en 2024",
         norma="Ley 12/2023, de 24 de mayo, disposición final sexta", bid="BOE-A-2023-12203", tit="Ley 12/2023, de 24 de mayo, por el derecho a la vivienda",
         pub="2023-05-25", vigor="2023-05-26", fin="2024-12-31", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         desc="Reescribe el art. 46 RDL 6/2022: para actualizaciones entre 2024-01-01 y 2024-12-31 el incremento no puede superar el 3 %. Sin prórroga hallada para 2025."),
    dict(id="E16", nombre="Ley 12/2023 DF 2: incentivos IRPF al arrendamiento de vivienda",
         norma="Ley 12/2023, de 24 de mayo, disposición final segunda", bid="BOE-A-2023-12203", tit="Ley 12/2023, de 24 de mayo, por el derecho a la vivienda",
         pub="2023-05-25", vigor="2024-01-01", ambito="nacional", ccaa="", prov="", terr="España (salvo regímenes forales)", mercado="alquiler",
         rx_vigor=r"excepto la disposición final segunda, que entrará en vigor el 1 de enero del año siguiente",
         desc="Modifica la Ley del IRPF (art. 23.2) para reducciones por arrendamiento de vivienda en contratos posteriores a la entrada en vigor; efectos desde 2024-01-01."),
    dict(id="E17", nombre="Resolución de 14-03-2024: sistema estatal de índices de precios de referencia del alquiler",
         norma="Resolución de 14 de marzo de 2024, de la Secretaría de Estado de Vivienda y Agenda Urbana", bid="BOE-A-2024-5213",
         tit="Resolución de 14 de marzo de 2024, de la Secretaría de Estado de Vivienda y Agenda Urbana, por la que se determina",
         pub="2024-03-15", vigor="2024-03-16", ambito="nacional", ccaa="", prov="", terr="España (aplicable en zonas tensionadas declaradas)",
         mercado="alquiler", rx_vigor=r"surtirá efectos desde el día siguiente al de su publicación",
         desc="Aprueba el sistema de índices de precios de referencia del alquiler por ámbitos territoriales, base del límite de renta en zonas tensionadas."),
    dict(id="E18", nombre="Actualización del sistema de índices de referencia (29-09-2025)",
         norma="Resolución de 29 de septiembre de 2025, de la Secretaría de Estado de Vivienda y Agenda Urbana", bid="BOE-A-2025-19403",
         tit="Resolución de 29 de septiembre de 2025, de la Secretaría de Estado de Vivienda y Agenda Urbana",
         pub="2025-09-30", vigor="2025-10-01", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"surtirá efectos desde el día siguiente al de su publicación",
         desc="Actualiza los índices de precios de referencia del alquiler con nuevos datos y metodología."),
    dict(id="E19", nombre="Actualización del sistema de índices de referencia (16-04-2026)",
         norma="Resolución de 16 de abril de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana", bid="BOE-A-2026-8691",
         tit="Resolución de 16 de abril de 2026, de la Secretaría de Estado de Vivienda y Agenda Urbana",
         pub="2026-04-20", vigor="2026-04-21", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"surtirá efectos desde el día siguiente al de su publicación",
         desc="Nueva actualización del sistema estatal de índices de precios de referencia del alquiler."),
    dict(id="E20", nombre="IRAV: índice de referencia para la actualización de la renta (INE)",
         norma="Resolución de 18 de diciembre de 2024, de la Presidencia del INE", bid="BOE-A-2024-26685",
         tit="Resolución de 18 de diciembre de 2024, de la Presidencia del Instituto Nacional de Estadística",
         pub="2024-12-20", vigor="2025-01-01", ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler",
         rx_vigor=r"surtirá efectos a partir del 1 de enero de 2025",
         desc="Define el índice (IRAV) de referencia para actualizar la renta de contratos de vivienda (art. 18 LAU) desde 2025-01-01."),
    dict(id="E21", nombre="Fin de las 'golden visas' por inversión inmobiliaria (LO 1/2025)",
         norma="Ley Orgánica 1/2025, de 2 de enero (modifica arts. 63-67 Ley 14/2013)", bid="BOE-A-2025-76",
         tit="Ley Orgánica 1/2025, de 2 de enero, de medidas en materia de eficiencia del Servicio Público de Justicia",
         pub="2025-01-03", vigor="2025-04-03", ambito="nacional", ccaa="", prov="", terr="España", mercado="no residentes",
         desc="Deja sin contenido los arts. 63-67 de la Ley 14/2013 (visado/residencia de inversores por compra de inmuebles); mantiene solicitudes previas y renovaciones."),
    dict(id="E22", nombre="RD 1312/2024: Registro Único de Arrendamientos (alquiler de corta duración)",
         norma="Real Decreto 1312/2024, de 23 de diciembre", bid="BOE-A-2024-26931", tit="Real Decreto 1312/2024, de 23 de diciembre",
         pub="2024-12-24", vigor="2025-01-02", ambito="nacional", ccaa="", prov="", terr="España",
         mercado="alquiler turístico",
         vigor_nota="Entra en vigor 2025-01-02; sus disposiciones despliegan efectos el 2025-07-01 (disposición final).",
         desc="Crea el Registro Único de Arrendamientos y la ventanilla única digital; número de registro obligatorio para anunciar alquileres turísticos y de temporada."),
    dict(id="E23", nombre="Decreto-ley catalán 3/2023: régimen urbanístico de viviendas de uso turístico",
         norma="Decreto-ley 3/2023 de Cataluña, de 7 de noviembre", bid="BOE-A-2024-281",
         tit="Decreto-ley 3/2023, de 7 de noviembre, de medidas urgentes sobre el régimen urbanístico de las viviendas de uso turístico",
         pub="2023-11-08", vigor="2023-11-09", ambito="CCAA", ccaa="09", prov="08;17;25;43", terr="Cataluña (incluye Barcelona)",
         mercado="alquiler turístico", pub_regional=True,
         desc="Somete el uso turístico de viviendas a planeamiento urbanístico municipal (modifica art. 187.1 y añade DA 27 del texto refundido de la Ley de urbanismo)."),
    dict(id="E24", nombre="Decreto-ley valenciano 9/2024: viviendas de uso turístico",
         norma="Decreto-ley 9/2024 del Consell, de 2 de agosto", bid="DOGV-r-2024-90168",
         tit="Decreto-ley 9/2024, de 2 de agosto, del Consell, de modificación de la normativa reguladora de las viviendas de uso turístico",
         pub="2024-08-07", vigor="2024-08-08", ambito="CCAA", ccaa="10", prov="03;12;46", terr="Comunitat Valenciana",
         mercado="alquiler turístico", pub_regional=True, url_kind="doc",
         desc="Modifica la normativa de viviendas de uso turístico: habilita límites municipales, exige referencia catastral individualizada y compatibilidad urbanística."),
    dict(id="E25", nombre="Decreto-ley balear 4/2025 contra la oferta turística ilegal",
         norma="Decreto-ley 4/2025 de Illes Balears, de 11 de abril", bid="BOE-A-2025-14462",
         tit="Decreto-ley 4/2025, de 11 de abril, contra la oferta ilegal",
         pub="2025-04-15", vigor="2025-04-16", ambito="CCAA", ccaa="04", prov="07", terr="Illes Balears", mercado="alquiler turístico", pub_regional=True,
         desc="Medidas transitorias contra la oferta ilegal y por la calidad turística; limita nuevas plazas turísticas en viviendas (alcance exacto: ver texto en BOIB/BOE)."),
    dict(id="E26", nombre="Ley canaria 6/2025 de ordenación sostenible del uso turístico de viviendas",
         norma="Ley 6/2025 de Canarias, de 10 de diciembre", bid="BOE-A-2025-26358",
         tit="Ley 6/2025, de 10 de diciembre, de Ordenación Sostenible del Uso Turístico de Viviendas",
         pub="2025-12-12", vigor="2025-12-13", ambito="CCAA", ccaa="05", prov="35;38", terr="Canarias", mercado="alquiler turístico", pub_regional=True,
         rx_vigor=r"entrará en vigor el día siguiente al de su publicación en el «Boletín Oficial de Canarias»",
         desc="Regula el uso turístico de viviendas: exige que el planeamiento municipal lo permita expresamente."),
]

# Eventos sin fuente oficial accesible o sin norma publicada: sin fechas.
NV = [
    dict(id="N01", nombre="Plan Reside (Madrid): restricción de viviendas de uso turístico", norma="Modificación puntual del Plan General de Madrid (aprobación definitiva por Consejo de Gobierno de la Comunidad de Madrid)",
         ambito="municipio", ccaa="13", prov="28", terr="Madrid (municipio 28079)", mercado="alquiler turístico",
         desc="Limita el uso turístico en edificios residenciales de Madrid capital.",
         sec="https://www.garrigues.com/es_ES/noticia/plan-reside-entra-vigor-modificacion-plan-general-madrid-proteccion-mejora-uso-residencial",
         nota="Fechas (acuerdo 2025-08-27, BOCM 2025-09-04 y 2025-09-22) solo constan en fuente secundaria (Garrigues); BOCM/BOAM no consultados."),
    dict(id="N02", nombre="Normativa municipal de apartamentos turísticos de València (moratoria 2024 y modificación de normas urbanísticas 2026)", norma="Ordenanza/normas urbanísticas del Ayuntamiento de València",
         ambito="municipio", ccaa="10", prov="46", terr="València (municipio 46250)", mercado="alquiler turístico",
         desc="Moratoria de licencias de apartamentos turísticos y posterior modificación de las normas urbanísticas.",
         sec="https://www.valencia.es/cas/actualidad/-/content/el-pleno-aprueba-definitivamente-normativa-apartamentos-tur%C3%ADsticos-val%C3%A8ncia",
         nota="No se localizó el acto en BOP/DOGV; la fecha de pleno y de BOP no consta en fuente oficial consultada."),
    dict(id="N03", nombre="Normativa municipal de Barcelona sobre viviendas de uso turístico (PEUAT y fin de licencias)", norma="Plan especial urbanístico de alojamientos turísticos (Ayuntamiento de Barcelona)",
         ambito="municipio", ccaa="09", prov="08", terr="Barcelona (municipio 08019)", mercado="alquiler turístico",
         desc="Planeamiento municipal sobre alojamientos turísticos; el marco autonómico verificado es el Decreto-ley 3/2023 (E23).",
         sec="", nota="No se accedió a la fuente oficial municipal (BOPB/Gaseta Municipal); sin fecha inventada."),
    dict(id="N04", nombre="Impuesto estatal a la compra de inmuebles por no residentes extracomunitarios", norma="Proposición de ley (no publicada como norma)",
         ambito="nacional", ccaa="", prov="", terr="España", mercado="no residentes",
         desc="Propuesta de impuesto complementario sobre adquisiciones por no residentes en la UE; sin norma publicada localizada.",
         sec="https://periscopiofiscalylegal.pwc.es/nuevo-impuesto-sobre-la-transmision-de-muebles-a-no-residentes-en-la-ue/",
         nota="Solo fuentes secundarias (proposición registrada en 2025); no se encontró publicación en BOE ni estado de tramitación en 2026. No usar como tratamiento."),
    dict(id="N05", nombre="Sentencia del Tribunal Supremo sobre el Registro Único de Arrendamientos (RD 1312/2024)", norma="Sentencia TS (referencia no confirmada)",
         ambito="nacional", ccaa="", prov="", terr="España", mercado="alquiler turístico",
         desc="Una única fuente secundaria indica anulación del registro por el Tribunal Supremo; no confirmada en CENDOJ/BOE.",
         sec="https://www.abogadosparatodos.net/entra-en-vigor-el-real-decreto-1312-2024/",
         nota="Verificar en CENDOJ/BOE antes de usar; el estado BOE de E22 a fecha de descarga figura como no derogado ni anulado."),
    dict(id="N06", nombre="Recargo de IBI a viviendas vacías: modulación estatal (Ley 12/2023) y recargos municipales", norma="Texto refundido Ley Reguladora de Haciendas Locales, art. 72 (modulado por Ley 12/2023)",
         ambito="municipios concretos", ccaa="", prov="", terr="Municipios que lo aprueben", mercado="compra",
         desc="El recargo depende de ordenanza municipal; no se verificó la fecha de cada ordenanza ni la redacción vigente del art. 72.",
         sec="", nota="Ley 12/2023 contiene un precepto de 'Modulación del recargo a los inmuebles de uso residencial desocupados' (sumario BOE) pero no se contrastó fecha por municipio."),
]


# --------------------------------------------------------------------------------------------------
def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", html.unescape(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def to_iso(y, m, d):
    return f"{int(y):04d}-{int(m):02d}-{int(d):02d}"


def ymd8(s):
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if s and len(s) == 8 else ""


def get_xml(bid: str) -> str:
    return uf.get(f"https://www.boe.es/diario_boe/xml.php?id={bid}", as_json=False)


def tag(t, k):
    m = re.search(rf"<{k}>(.*?)</{k}>", t, re.S)
    return m.group(1).strip() if m else ""


def text_of(t):
    i = t.find("<texto")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t[i:] if i >= 0 else t))


def regional_pub(t):
    """Fecha del boletín autonómico a partir de 'Publicada en el X núm. N, de D de mes de AAAA'."""
    m = re.search(r"Publicada en el [^,]*?,\s*de (\d{1,2}) de (\w+) de (\d{4})", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
    if m and m.group(2).lower() in MESES:
        return to_iso(m.group(3), MESES[m.group(2).lower()], m.group(1))
    return ""


def page_title(url):
    r = requests.get(url, headers=UA, timeout=60, allow_redirects=True)
    r.raise_for_status()
    m = re.search(r"<title>(.*?)</title>", r.text, re.S | re.I)
    return html.unescape(m.group(1)).strip() if m else ""


def url_for(e):
    if e.get("url_kind") == "doc":
        return f"https://www.boe.es/buscar/doc.php?id={e['bid']}"
    return f"https://www.boe.es/diario_boe/txt.php?id={e['bid']}"


def verify_event(e):
    """Devuelve (estado, nota, fecha_publicacion, fecha_vigor, fecha_fin) contrastando con la fuente oficial."""
    notas, ok = [], True
    t = get_xml(e["bid"])
    tit = re.sub(r"\s+", " ", html.unescape(tag(t, "titulo")))
    if not norm(tit).startswith(norm(e["tit"])):
        ok = False
        notas.append(f"título XML distinto: {tit[:80]}")
    pub_x = regional_pub(t) if e.get("pub_regional") else ymd8(tag(t, "fecha_publicacion"))
    if e.get("pub_regional") and not pub_x:
        pub_x = ymd8(tag(t, "fecha_publicacion"))
    if pub_x != e["pub"]:
        ok = False
        notas.append(f"pub esperada {e['pub']} vs oficial {pub_x}")
    vig_x = ymd8(tag(t, "fecha_vigencia"))
    if vig_x and e["vigor"] != vig_x and e["id"] not in ("E16", "E20"):
        ok = False
        notas.append(f"vigor esperada {e['vigor']} vs metadato BOE {vig_x}")
    if e.get("rx_vigor") and not re.search(e["rx_vigor"], text_of(t)):
        ok = False
        notas.append("cláusula de vigencia no encontrada en el texto")
    if not vig_x and not e.get("rx_vigor") and not e.get("vigor_nota"):
        notas.append("vigencia sin metadato BOE ni cláusula contrastada")
    der = tag(t, "estatus_derogacion")
    fecha_der = ymd8(tag(t, "fecha_derogacion"))
    anul = tag(t, "judicialmente_anulada")
    if e.get("fin") and e["id"] in ("E07", "E08"):
        if der != "S" or fecha_der != e["fin"]:
            ok = False
            notas.append(f"fin esperado {e['fin']} vs BOE derog={der} {fecha_der}")
    elif e.get("fin") in ("2024-12-31",):
        notas.append("fin = último día del periodo que fija el art. 46 RDL 6/2022 (texto BOE consolidado)")
    elif e["id"] == "E09":
        notas.append("fin = fecha de publicación de STC 37/2022 (E10); la ley sigue en vigor en lo no anulado")
    elif der == "S" and not e.get("fin"):
        ok = False
        notas.append(f"BOE indica derogación {fecha_der} no reflejada")
    if e.get("vigor_nota"):
        notas.append(e["vigor_nota"])
    # página pública: el <title> debe contener el título de la norma
    url = url_for(e)
    try:
        pt = page_title(url)
        if not norm(e["tit"]) in norm(pt):
            ok = False
            notas.append(f"título de página no coincide: {pt[:70]}")
    except Exception as ex:  # noqa: BLE001
        ok = False
        notas.append(f"URL no responde: {ex}")
    return ("VERIFICADO" if ok else "DISCREPANCIA"), " | ".join(notas), url


# --------------------------------------------------------------------------------------------------
# Zonas tensionadas (art. 18 Ley 12/2023): una resolución trimestral del MIVAU por cada BOE
ZT_RES = [
    ("BOE-A-2024-5214", "Cataluña, 1.ª ronda (Resolución TER/800/2024)"),
    ("BOE-A-2024-20576", "Cataluña, 2.ª ronda (Resolución TER/2408/2024)"),
    ("BOE-A-2025-1721", "País Vasco: Errenteria"),
    ("BOE-A-2025-8636", "País Vasco: Lasarte-Oria, Zumaia, Barakaldo, Irun"),
    ("BOE-A-2025-15728", "Navarra (21), A Coruña, Galdakao (D2), Donostia"),
    ("BOE-A-2025-21901", "País Vasco: Astigarraga, Bilbao, Usurbil, Vitoria-Gasteiz"),
    ("BOE-A-2026-2448", "País Vasco: Hernani, Lezo, Tolosa"),
    ("BOE-A-2026-9175", "País Vasco: Pasaia, Zestoa, Mondragón"),
    ("BOE-A-2026-16532", "Asturias (ámbitos), Santiago de Compostela, Basauri"),
]


def cells(row_html):
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
            for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row_html, re.S)]


def split_depth0(s):
    out, cur, d = [], "", 0
    for ch in s:
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
        if ch == "," and d == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def clean_munis(cell):
    cell = cell.strip().rstrip(".")
    cell = cell.replace("Manresa el Masnou", "Manresa, el Masnou")  # errata de la propia resolución (falta una coma)
    toks = split_depth0(cell)
    res = []
    for tk in toks:
        if tk.startswith("Platja d'Aro i S'Agar") and res:
            res[-1] = res[-1] + ", " + tk
        elif tk.lower().startswith("excepto") and res:  # p. ej. «Vitoria-Gasteiz, excepto la zona rural...»
            res[-1] = res[-1] + " (" + tk + ")"
        else:
            res.append(re.sub(r"^i\s+", "", tk))  # «Vilassar de Dalt i Vilassar de Mar»
    out = []
    for r in res:
        m = re.match(r"^(.*?)\s*\((.*)\)$", r)
        out.append((m.group(1).strip(), m.group(2).strip()) if m else (r.strip(), ""))
    return out


def load_dicc():
    p = uf.download(DICC_URL, uf.RAW / "ine_diccionario_municipios_2026.xlsx")
    d = pd.read_excel(p, header=1, dtype=str)
    d["cod"] = d["CPRO"].str.zfill(2) + d["CMUN"].str.zfill(3)
    idx = {}
    for _, r in d.iterrows():
        nm = r["NOMBRE"]
        m = re.match(r"^(.*), (El|La|Los|Las|L'|A|O|Os|As|Els|Les|Es|Sa)$", nm)
        full = (m.group(2) + " " + m.group(1)).replace("' ", "'") if m else nm
        keys = {norm(full), norm(nm)}
        for part in re.split(r"[/-]", full):
            keys.add(norm(part))
        keys |= {norm(k.replace("l ", "l")) for k in list(keys)}
        for k in keys:
            idx.setdefault((r["CPRO"].zfill(2), k), r["cod"])
    return idx


ALIAS = {  # nombre en la resolución (norm) -> nombre INE alternativo
    "castell d aro platja d aro i s agaro": "castell platja d aro",
    "la coruna": "coruna a",
    "mondragon": "arrasate mondragon",
    "donostia san sebastian": "donostia san sebastian",
    "tudela": "tudela",
    "pamplona iruna": "pamplona iruna",
    "baztan": "baztan",
    "l hospitalet de llobregat": "hospitalet de llobregat l",
}


def muni_code(idx, ccaa_cod, name):
    provs = CCAA_PROV[ccaa_cod]
    ks = {norm(name), norm(name.replace("l'", "l")), norm(name).replace(" ", "")}
    if norm(name) in ALIAS:
        ks.add(ALIAS[norm(name)])
    for p in re.split(r"[/-]", name):
        ks.add(norm(p))
    ks |= {k.replace("l ", "l") for k in list(ks)}
    for pv in provs:
        for k in ks:
            if (pv, k) in idx:
                return idx[(pv, k)]
    # sin separadores: comparar contra claves sin espacios
    for pv in provs:
        for k in ks:
            kk = k.replace(" ", "")
            for (p2, k2), c in idx.items():
                if p2 == pv and k2.replace(" ", "") == kk:
                    return c
    return ""


def parse_resolution(bid, idx):
    t = get_xml(bid)
    tit = re.sub(r"\s+", " ", html.unescape(tag(t, "titulo")))
    assert "zonas de mercado residencial tensionado" in tit, (bid, tit)
    pub = ymd8(tag(t, "fecha_publicacion"))
    body = t[t.find("<texto"):]
    intro_txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body[:body.find("<table")])))
    efecto = (dt.date.fromisoformat(pub) + dt.timedelta(days=1))
    fin = efecto.replace(year=efecto.year + 3)
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S)
    out = []
    for r in rows:
        c = cells(r)
        if len(c) < 6 or c[0].lower().startswith("comunidad"):
            continue
        ccaa = c[0].rstrip(".").strip()
        cc = CCAA_COD.get(ccaa, "")
        decl = c[5]
        mdec = re.search(r"Declaración:\s*(.*?)(?:\s*–\s*Memoria|$)", decl)
        decl_txt = (mdec.group(1) if mdec else decl)[:400]
        urls = re.findall(r"https?://\S+", decl_txt)
        url_decl = urls[0].rstrip(".") if urls else ""
        # fecha de disposición y de publicación autonómica
        md = re.search(r"(?:de|del) (\d{1,2}) de (\w+)(?: de (\d{4}))?", decl_txt)
        yr = md.group(3) if md and md.group(3) else (re.search(r"\d+/(\d{4})", decl_txt).group(1) if re.search(r"\d+/(\d{4})", decl_txt) else "")
        f_decl = to_iso(yr, MESES[md.group(2).lower()], md.group(1)) if md and md.group(2).lower() in MESES and yr else ""
        mp = re.search(r"núm\.\s*\d+,\s*(\d{1,2}) de (\w+) de (\d{4})", decl_txt)
        f_pub_aut = to_iso(mp.group(3), MESES[mp.group(2).lower()], mp.group(1)) if mp else ""
        if not f_pub_aut and cc != "09":
            mq = re.search(re.escape(decl_txt[:95]) + r"[^–]{0,700}?publicad\w+ en el «[^»]+» el (\d{1,2}) de (\w+) de (\d{4})", intro_txt)
            if mq and mq.group(2).lower() in MESES:
                f_pub_aut = to_iso(mq.group(3), MESES[mq.group(2).lower()], mq.group(1))
        if not f_pub_aut and cc == "09":
            mq = re.search(r"el (\d{1,2}) de (\w+) de (\d{4}) ha sido publicada", intro_txt)
            if mq:
                f_pub_aut = to_iso(mq.group(3), MESES[mq.group(2).lower()], mq.group(1))
        for nombre, alcance in clean_munis(c[1]):
            code = muni_code(idx, cc, nombre) if cc else ""
            out.append(dict(ccaa=ccaa, cod_ccaa=cc, cod_provincia=code[:2], municipio_resolucion=nombre, cod_ine_municipio=code,
                            alcance=("parcial: " + alcance) if alcance else "municipio completo",
                            declaracion_autonomica=decl_txt.split(" http")[0][:300], fecha_declaracion_autonomica=f_decl,
                            fecha_publicacion_autonomica=f_pub_aut, url_declaracion=url_decl,
                            resolucion_boe=bid, fecha_publicacion_boe=pub, fecha_efecto=efecto.isoformat(),
                            fecha_fin_prevista=fin.isoformat(),
                            url_resolucion=f"https://www.boe.es/diario_boe/txt.php?id={bid}"))
    return tit, pub, out


def main():
    if uf.cached(OUT_EV) and uf.cached(OUT_ZT) and FALLIDAS.exists():
        return
    fallos = []
    filas = []
    for e in EV:
        try:
            est, nota, url = verify_event(e)
        except Exception as ex:  # noqa: BLE001
            est, nota, url = "NO VERIFICADO", f"error al consultar la fuente oficial: {ex}", ""
            fallos.append((e["id"], e["bid"], str(ex)))
        sin_fecha = est == "NO VERIFICADO"
        filas.append(dict(id=e["id"], nombre=e["nombre"], norma=e["norma"],
                          fecha_publicacion="" if sin_fecha else e["pub"], fecha_entrada_vigor="" if sin_fecha else e["vigor"],
                          fecha_fin="" if sin_fecha else D(e.get("fin")), ambito=e["ambito"], codigos_ine_ccaa=e["ccaa"],
                          codigos_ine_provincia=e["prov"], territorios_afectados=e["terr"], mercado=e["mercado"],
                          descripcion_breve=e["desc"], url_oficial=url, url_secundaria="", estado=est, nota_verificacion=nota,
                          verificado_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    # zonas tensionadas
    idx = load_dicc()
    zt_rows, zt_ev = [], []
    for k, (bid, desc) in enumerate(ZT_RES, 1):
        try:
            tit, pub, rows = parse_resolution(bid, idx)
            url = f"https://www.boe.es/diario_boe/txt.php?id={bid}"
            pt = page_title(url)
            ok = norm(tit[:60]) in norm(pt)
            zt_rows += rows
            ef = (dt.date.fromisoformat(pub) + dt.timedelta(days=1))
            ccs = sorted({r["cod_ccaa"] for r in rows})
            pvs = sorted({r["cod_provincia"] for r in rows if r["cod_provincia"]})
            nuevos = len(rows)
            filas.append(dict(id=f"ZT{k:02d}", nombre=f"Zonas tensionadas (art. 18 Ley 12/2023): {desc}", norma=tit[:230],
                              fecha_publicacion=pub, fecha_entrada_vigor=ef.isoformat(), fecha_fin=ef.replace(year=ef.year + 3).isoformat(),
                              ambito="CCAA" if len(ccs) == 1 and nuevos > 10 else "municipios concretos",
                              codigos_ine_ccaa=";".join(ccs), codigos_ine_provincia=";".join(pvs),
                              territorios_afectados=f"{nuevos} municipios/ámbitos; detalle en {OUT_ZT} (resolucion_boe={bid})",
                              mercado="alquiler", descripcion_breve="Relación trimestral de zonas declaradas; tope de renta en nuevos contratos de grandes tenedores según índice de referencia. Vigencia 3 años desde el día siguiente al BOE.",
                              url_oficial=url, url_secundaria="", estado="VERIFICADO" if ok else "DISCREPANCIA",
                              nota_verificacion="fecha_entrada_vigor = día siguiente a la publicación de la resolución (regla de la propia resolución); fecha_fin = +3 años (±1 día según cómputo). Fecha de la declaración autonómica por municipio en el CSV de zonas.",
                              verificado_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
        except Exception as ex:  # noqa: BLE001
            fallos.append((f"ZT{k:02d}", bid, str(ex)))
    zt = pd.DataFrame(zt_rows)
    sin_cod = zt[zt["cod_ine_municipio"] == ""]
    for e in NV:
        filas.append(dict(id=e["id"], nombre=e["nombre"], norma=e["norma"], fecha_publicacion="", fecha_entrada_vigor="", fecha_fin="",
                          ambito=e["ambito"], codigos_ine_ccaa=e["ccaa"], codigos_ine_provincia=e["prov"], territorios_afectados=e["terr"],
                          mercado=e["mercado"], descripcion_breve=e["desc"], url_oficial="", url_secundaria=e["sec"],
                          estado="NO VERIFICADO", nota_verificacion=e["nota"],
                          verificado_utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    ev = pd.DataFrame(filas)[COLS_EV]
    uf.RAW.mkdir(parents=True, exist_ok=True)
    ev.to_csv(uf.RAW / OUT_EV, index=False)
    zt.to_csv(uf.RAW / OUT_ZT, index=False)
    # manifiesto
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new = pd.DataFrame([
        dict(archivo=OUT_EV, fuente="BOE/boletines oficiales", n_series=ev["id"].nunique(),
             primera_fecha=ev["fecha_publicacion"].replace("", pd.NA).dropna().min(), ultima_fecha=ev["fecha_publicacion"].replace("", pd.NA).dropna().max(),
             n_obs=len(ev), n_nan=int((ev["fecha_publicacion"] == "").sum()), descargado_utc=now),
        dict(archivo=OUT_ZT, fuente="BOE (Secretaría de Estado de Vivienda, art. 18 Ley 12/2023)", n_series=zt["resolucion_boe"].nunique(),
             primera_fecha=zt["fecha_efecto"].min(), ultima_fecha=zt["fecha_efecto"].max(), n_obs=len(zt),
             n_nan=int((zt["cod_ine_municipio"] == "").sum()), descargado_utc=now)])
    man = pd.read_csv(uf.MANIFEST)
    man = pd.concat([man[~man["archivo"].isin(new["archivo"])], new], ignore_index=True).sort_values("archivo")
    man.to_csv(uf.MANIFEST, index=False)
    # fallidas
    FALLIDAS.parent.mkdir(parents=True, exist_ok=True)
    L = ["# Eventos de política de vivienda: fuentes fallidas y no verificadas", "",
         f"Generado por src/build_eventos.py ({now}).", "",
         "| id | evento | URL probada / fuente | problema | alternativa |", "|---|---|---|---|---|"]
    for e in NV:
        L.append(f"| {e['id']} | {e['nombre']} | {e['sec'] or '(sin URL oficial hallada)'} | {e['nota']} | Consultar boletín oficial (BOCM, BOP, BOPB, DOGV, CENDOJ, Congreso) y completar fechas en la tabla EV/NV de src/build_eventos.py |")
    for f in fallos:
        L.append(f"| {f[0]} | (error de descarga) | {f[1]} | {f[2]} | Reintentar con FORCE=1 |")
    for _, r in ev[ev["estado"] == "DISCREPANCIA"].iterrows():
        L.append(f"| {r['id']} | {r['nombre']} | {r['url_oficial']} | DISCREPANCIA: {r['nota_verificacion']} | Revisar fecha esperada en la tabla |")
    if len(sin_cod):
        L += ["", f"Municipios de zonas tensionadas sin código INE tras el cruce con el diccionario INE 2026 ({len(sin_cod)}):", ""]
        L += [f"- {r.ccaa}: {r.municipio_resolucion} ({r.resolucion_boe})" for r in sin_cod.itertuples()]
    FALLIDAS.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(ev["estado"].value_counts().to_dict(), "| zonas:", len(zt), "sin código INE:", len(sin_cod))


if __name__ == "__main__":
    main()
