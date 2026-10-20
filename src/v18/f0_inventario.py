"""V18 · Fase 0 · Inventario de datos por estudio (E1-E12) y por modelo de conjunto (F1-F3) de docs/v18/plan.md, secciones E y F.

No estima nada y NO lee datos. Solo lee:
- manifiestos (data/raw/**/_manifest*.csv), el diccionario de la base (docs/v10/diccionario_base.md) y los inventarios
  (docs/v13/datos_inventario.csv, docs/v16/inventario_fuentes.csv, output/v17/f1/inventario.csv);
- los NOMBRES de los ficheros de data/raw y data/processed (nunca su contenido) y de docs/v16/fuentes y docs/v17/fuentes;
- de src/holdout.py, solo la partición v6 (provincias_selladas_v6 y CCAA_PROV), que se calcula sin abrir datos.
La carpeta de la muestra sellada no se recorre ni se nombra.

Cada variable se declara abajo con sus fuentes candidatas; el script comprueba que cada fuente existe (variable del diccionario,
fichero de un manifiesto o inventario, o nombre en disco) y rebaja el estado si no la encuentra. Nivel y periodo de las
variables de la base salen del diccionario. Determinista y sin red.

Salidas: output/v18/f0/inventario.csv y output/v18/f0/informe.md.
Uso: python3 src/v18/f0_inventario.py
"""
from __future__ import annotations

import csv
import io
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

ALCANCE_TERRITORIAL = "sin lectura de datos"   # guarda de fuga v6 (check_v17): solo manifiestos, diccionarios, inventarios y nombres

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v18" / "f0"
FECHA = "2026-10-20"
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402  (solo la partición v6, calculada con la semilla; sin lectura de datos)

_PROHIBIDA = "data/" + "sealed"
COLUMNAS = ["estudio", "uso", "variable", "estado", "fuente_en_repo", "nivel", "periodo", "falta", "requiere_autor"]
ESTADOS = ("disponible", "parcial", "falta")
VEREDICTOS = ("replicable", "replicable en parte", "NO ESTIMABLE con los datos actuales")

CCAA = {"01": "Andalucía", "02": "Aragón", "03": "Asturias", "04": "Illes Balears", "05": "Canarias", "06": "Cantabria",
        "07": "Castilla y León", "08": "Castilla-La Mancha", "09": "Cataluña", "10": "Comunitat Valenciana", "11": "Extremadura",
        "12": "Galicia", "13": "Madrid", "14": "Región de Murcia", "15": "Navarra", "16": "País Vasco", "17": "La Rioja",
        "18": "Ceuta", "19": "Melilla"}
PROV = {"01": "Araba/Álava", "02": "Albacete", "03": "Alicante", "04": "Almería", "05": "Ávila", "06": "Badajoz",
        "07": "Illes Balears (Palma)", "08": "Barcelona", "09": "Burgos", "10": "Cáceres", "11": "Cádiz", "12": "Castellón",
        "13": "Ciudad Real", "14": "Córdoba", "15": "A Coruña", "16": "Cuenca", "17": "Girona", "18": "Granada",
        "19": "Guadalajara", "20": "Gipuzkoa", "21": "Huelva", "22": "Huesca", "23": "Jaén", "24": "León", "25": "Lleida",
        "26": "La Rioja", "27": "Lugo", "28": "Madrid", "29": "Málaga", "30": "Murcia", "31": "Navarra", "32": "Ourense",
        "33": "Asturias", "34": "Palencia", "35": "Las Palmas", "36": "Pontevedra", "37": "Salamanca",
        "38": "Santa Cruz de Tenerife", "39": "Cantabria", "40": "Segovia", "41": "Sevilla", "42": "Soria", "43": "Tarragona",
        "44": "Teruel", "45": "Toledo", "46": "València", "47": "Valladolid", "48": "Bizkaia", "49": "Zamora", "50": "Zaragoza",
        "51": "Ceuta", "52": "Melilla"}


@dataclass
class Var:
    uso: str                 # réplica | ampliación
    variable: str
    estado: str              # declarado; el script lo rebaja si una fuente no aparece
    fuentes: list[str]       # "base:<variable>", ruta de fichero (admite comodines) o ruta de docs/
    nivel: str = ""
    periodo: str = ""
    falta: str = ""
    autor: str = ""          # sí | no | "" (nada falta)
    esencial: bool = False   # sin ella no hay réplica del diseño original


@dataclass
class Estudio:
    id: str
    titulo: str
    veredicto: str
    porque: str
    clave: dict[str, str]    # provincias que importan para la réplica o la ampliación: código → papel
    vars: list[Var] = field(default_factory=list)
    nota_sellado: str = ""


def _r(*a, **k) -> Var:
    return Var("réplica", *a, **k)


def _a(*a, **k) -> Var:
    return Var("ampliación", *a, **k)


SERPAVI = ["base:serpavi_alquiler_m2_mediana", "data/raw/v3/serpavi_secciones_nacional_v3.csv.gz"]
IPVA = ["base:ipva_indice", "data/raw/v9/ine_ipva/ipva_provincia_antiguedad.csv"]
CONTROLES_SECCION = ["base:adrh_renta_neta_persona", "base:pob_censo_anual", "data/raw/v16/renta_parque/_grandes/adrh/*"]

ESTUDIOS: list[Estudio] = [
    Estudio(
        "E1", "Vivienda turística (Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú, 2020)", "replicable en parte",
        "Barcelona por barrio se puede rehacer con el registro HUT (2018-2026) y el alquiler SERPAVI por sección o el IPVA por "
        "distrito, pero el periodo original (anuncios de Airbnb 2012-2016) y los dos instrumentos (atractivos y búsquedas) no "
        "están en el repositorio; la ampliación a València, Málaga, Sevilla y Alicante tiene registros e INE-VUT, pero "
        "InsideAirbnb solo tiene instantáneas desde 2025-12.",
        {"08": "réplica (Barcelona)", "46": "ampliación", "29": "ampliación", "41": "ampliación", "03": "ampliación",
         "28": "ampliación", "07": "ampliación"},
        [
            _r("Viviendas de uso turístico (HUT) por barrio de Barcelona", "parcial",
               ["data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz", "base:bcn_hut_registro",
                "data/manual/v11/bcn_hut_trimestral/*"],
               nivel="barrio (66) y municipio", periodo="2018T2-2026T3 (cortes); año de expediente de las licencias vigentes",
               falta="las licencias dadas de baja antes de 2018 no constan; no reproduce el stock 2012-2016 del original",
               autor="no", esencial=True),
            _r("Anuncios de Airbnb por barrio 2012-2016 (exposición del original)", "falta", [],
               falta="histórico de InsideAirbnb (Archived Data Request, docs/v17/fuentes/turismo_local.md) o datos de AirDNA",
               autor="sí", esencial=True),
            _r("Alquiler por barrio o sección de Barcelona", "parcial", SERPAVI + ["base:ipva_indice"],
               nivel="sección y distrito (SERPAVI); distrito (IPVA)", periodo="2011-2024 anual",
               falta="alquiler trimestral por barrio (Open Data BCN, «lloguer mitjà mensual per barri», de las fianzas de "
                     "Incasòl; abierto, se descarga sin el autor)", autor="no", esencial=True),
            _r("Precio de compra por barrio de Barcelona", "falta", [],
               falta="Open Data BCN (precio de compraventa por barrio; por verificar la fuente y la licencia) o anuncios de "
                     "portales", autor="no"),
            _r("Instrumento «dónde»: atractivos turísticos georreferenciados", "falta", [],
               falta="OpenStreetMap (tourism=attraction; ODbL) o inventario municipal de atractivos; geometría de secciones ya "
                     "en data/raw/v10/geo/seccionado_2025.zip", autor="no", esencial=True),
            _r("Instrumento «cuándo»: búsquedas en Google de Airbnb", "falta", [],
               falta="Google Trends (índice de búsquedas; condiciones de uso por verificar)", autor="no", esencial=True),
            _r("Geometría de secciones y barrios (distancias, caso Sagrada Família)", "disponible",
               ["data/raw/v10/geo/seccionado_2025.zip", "data/raw/v3/cartografia/Cartografia_secc.zip"],
               nivel="sección censal", periodo="2025"),
            _r("Controles por sección (renta, población)", "disponible", CONTROLES_SECCION),
            _a("Viviendas turísticas INE (experimental) por sección y distrito", "disponible",
               ["base:ine_vut_vivienda_turistica", "data/raw/v3/ine_v3_vut_seccion.csv.gz"]),
            _a("Registros autonómicos de vivienda turística con fecha de alta", "parcial",
               ["base:vut_registro_gva_reconstruido", "data/raw/v9/gva_vut/gva_vut_panel_municipio.csv",
                "data/raw/v16/alquiler_turismo/_terceros/openrta_all_2026-10-17.csv.gz", "base:reate_viviendas_uso_turistico",
                "base:idescat_hut_n", "data/raw/v9/cat_turisme/registre_turisme_agregat_municipi.csv.gz"],
               nivel="municipio (GVA, IDESCAT, Euskadi) y establecimiento (Andalucía)",
               periodo="GVA 2015-2026; IDESCAT 2015-2025; Andalucía con fecha de alta; Euskadi un corte",
               falta="altas con fecha de Cataluña (registre complet), Ibiza y Formentera; Madrid y Baleares están selladas",
               autor="sí"),
            _a("InsideAirbnb por sección (9 áreas)", "parcial",
               ["base:iab_n_anuncios", "data/raw/v9/insideairbnb/insideairbnb_seccion.csv.gz",
                "data/raw/v17/turismo_local/insideairbnb/*"],
               falta="solo instantáneas desde 2025-12; el histórico requiere la Archived Data Request", autor="sí"),
            _a("Alquiler por sección en las ciudades de la ampliación", "disponible", SERPAVI),
            _a("Demanda turística (pernoctaciones y plataformas)", "disponible",
               ["base:eurostat_plataformas_noches", "base:ine_tmov_receptor_turistas", "data/raw/v9/eurostat_plataformas/*"]),
            _a("Regulaciones locales (PEUAT, moratorias) como tratamiento", "parcial",
               ["data/raw/v16/intervenciones/intervenciones.csv", "base:vut_regulacion_ccaa"],
               nivel="CCAA y municipio (fecha)", periodo="2014-2026",
               falta="geometría de las zonas del PEUAT y fechas de moratorias de otras ciudades (ayuntamientos)", autor="sí"),
        ]),
    Estudio(
        "E2", "Topes al alquiler (Jofre-Monseny, Martínez-Mazza y Segú, 2023; Monràs y García-Montalvo, 2023)",
        "replicable en parte",
        "La réplica de Jofre-Monseny et al. es posible: Incasòl da renta y número de contratos por municipio y trimestre desde "
        "2007, con tramos de renta, y la lista de municipios de la Ley 11/2020 está en el repositorio. Monràs y García-Montalvo "
        "necesitan anuncios (composición y tramo de precio del anuncio): NO ESTIMABLE sin microdatos de portales. El "
        "desplazamiento a temporada no tiene datos.",
        {"08": "réplica", "17": "réplica", "25": "réplica", "43": "réplica", "48": "ampliación (zonas 2024)",
         "31": "ampliación (zonas 2024)", "33": "ampliación (zonas 2024)", "15": "ampliación (zonas 2024)"},
        [
            _r("Renta media y número de contratos por municipio (Cataluña)", "disponible",
               ["data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz", "data/raw/v3/incasol_fianzas_municipio_v3.csv.gz"],
               nivel="municipio (Cataluña)", periodo="2007T1-2026T1 trimestral", esencial=True),
            _r("Contratos por tramo de renta", "parcial", ["data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz"],
               nivel="municipio", periodo="2007T1-2026T1",
               falta="tramos fijos en euros/mes, sin la renta anterior del contrato ni la superficie; microdatos de contratos "
                     "del registro de fianzas (Agència de l'Habitatge de Catalunya)", autor="sí"),
            _r("Municipios y vigencia del tope (Ley 11/2020, STC 37/2022)", "disponible",
               ["data/raw/v3/cataluna_contencion_rentas_v3.csv", "base:tope_rentas_ccaa", "base:tope_rentas_ccaa_alt_v3"],
               nivel="municipio (lista) y CCAA (indicador)", periodo="2020-09-22 a 2022-04-08 (dos ventanas)", esencial=True),
            _r("Controles municipales (población, renta, paro)", "disponible",
               ["base:pob_total", "base:aeat_irpf_renta_disponible_media", "base:sepe_paro_registrado_media_anual"]),
            _r("Anuncios de alquiler 2019-2022 (Monràs y García-Montalvo)", "falta", [],
               falta="microdatos de portales (Idealista, Fotocasa, Habitaclia): precio, superficie, ubicación y fechas",
               autor="sí", esencial=True),
            _a("Zonas tensionadas 2024 con fecha de efecto", "disponible",
               ["base:zt_vigente", "data/raw/v9/regulacion/zonas_tensionadas_v9.csv",
                "data/raw/v16/intervenciones/zonas_tensionadas_v16_nuevas.csv"]),
            _a("Renta de contratos en otras CCAA con zonas (País Vasco)", "parcial",
               ["base:emal_renta_mensual_eur", "data/raw/v9/emal/emal_largo.csv"] + IPVA,
               falta="Navarra y Asturias están selladas; A Coruña solo tiene IPVA y SERPAVI anuales hasta 2024", autor="no"),
            _a("Contratos de temporada y por habitaciones", "falta", [],
               falta="fianzas por tipo de contrato o estadísticas del Registro Único de Arrendamientos (RD 1312/2024)",
               autor="sí"),
            _a("Desplazamiento a la venta (compraventas y valor tasado)", "disponible",
               ["base:compraventas", "base:p_tasado", "data/raw/mivau_transacciones_municipios.csv"]),
        ]),
    Estudio(
        "E3", "Inmigración (González y Ortega, 2013; Saiz, 2007)", "replicable en parte",
        "Hay población por nacionalidad y provincia desde 2003, flujos nacionales por nacionalidad, valor tasado provincial desde "
        "1995 y obra nueva provincial, pero las cuotas «históricas» del instrumento solo arrancan en 2003, dentro del periodo "
        "de la réplica (2001/2003-2008); el Censo de 2001 por nacionalidad y provincia (abierto) las daría. El alquiler "
        "(SERPAVI, IPVA) llega hasta 2024.",
        {"28": "réplica", "07": "réplica", "30": "réplica", "35": "réplica", "38": "réplica", "08": "réplica",
         "03": "réplica", "29": "réplica"},
        [
            _r("Población extranjera por nacionalidad y provincia", "disponible",
               ["base:padron_pob_nacionalidad", "data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz",
                "base:ecp_pob_nacionalidad"], esencial=True),
            _r("Cuotas históricas por nacionalidad (asentamientos previos)", "parcial",
               ["data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz", "base:pob_extranjera"],
               nivel="provincia y municipio", periodo="por nacionalidad desde 2003; total de extranjeros desde 1998",
               falta="Censo de 2001 (o 1991) por nacionalidad y provincia: INE, descarga abierta", autor="no", esencial=True),
            _r("Entradas nacionales por nacionalidad (choque, sin la propia provincia)", "disponible",
               ["data/raw/ine_migraciones_nacionalidad.csv", "base:inmig_anual_eurostat", "base:evr_inmigracion_exterior",
                "data/raw/v9/ine_migraciones/ine_em_24323.csv.gz"]),
            _r("Precio de compra provincial", "disponible", ["base:valor_tasado", "base:ipv"],
               falta="el IPV solo es autonómico y desde 2007; la réplica usa el valor tasado"),
            _r("Obra nueva provincial", "disponible",
               ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv", "base:iniciadas", "base:terminadas"]),
            _r("Controles provinciales (PIB, empleo)", "disponible",
               ["data/raw/ine_v2_cre.csv", "base:ocupados_epa", "base:pib_miles_eur"]),
            _a("Alquiler provincial y municipal 2011-2024", "disponible", SERPAVI + IPVA + ["base:ipc_alquiler_indice"],
               falta="SERPAVI e IPVA terminan en 2024; 2025 solo con el IPC de alquiler"),
            _a("Población por nacionalidad en municipio y sección 2021-2025", "disponible",
               ["data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz", "base:pob_censo_anual"]),
            _a("Tenencia por nacionalidad (compra frente a alquiler)", "parcial",
               ["data/raw/v11/ine_censo2021/*", "data/raw/v11/ine_ecepov/*", "data/raw/v11/ine_censos_microdatos/*"],
               periodo="2011 y 2021", falta="solo dos cortes censales; no hay serie anual de tenencia por nacionalidad",
               autor="no"),
            _a("Compras de extranjeros residentes", "disponible", ["base:tx_extranj_ccaa", "data/raw/mivau_transacciones_extranjeros.csv"]),
        ]),
    Estudio(
        "E4", "Ayudas a la demanda (Fack, 2005-2006; Gibbons y Manning, 2006; Banque de France WP 886)",
        "NO ESTIMABLE con los datos actuales",
        "No hay microdatos de perceptores del Bono Alquiler Joven ni de ayudas autonómicas, ni convocatorias autonómicas con "
        "fecha. Lo único posible es una forma reducida débil por la edad de 35 años en la ECV (la edad no asigna el bono por sí "
        "sola). La magnitud preferida saldrá solo de la literatura, rotulada así.",
        {},
        [
            _r("Perceptores de ayudas al alquiler (edad, renta, municipio, fecha, importe)", "falta", [],
               falta="microdatos de beneficiarios del Bono Alquiler Joven y de ayudas autonómicas (MIVAU y CCAA)",
               autor="sí", esencial=True),
            _r("Alquiler pagado por hogares inquilinos por edad (ECV)", "disponible",
               ["data/raw/v9/ine_microdatos/ecv/*", "data/raw/v16/renta_parque/*"],
               nivel="hogar (nacional; CCAA de residencia)", periodo="2004-2025"),
            _r("Calendario y requisitos de las ayudas", "parcial", ["data/raw/v16/intervenciones/intervenciones.csv"],
               periodo="RD 42/2022 (2022-01-20)",
               falta="convocatorias autonómicas (fechas de resolución, requisitos de renta y edad) y la Renta Básica de "
                     "Emancipación 2008-2012 (BOE y diarios oficiales)", autor="no"),
            _a("Gasto en alquiler por hogar (EPF)", "disponible", ["data/raw/v16/renta_parque/*"]),
            _a("Alquiler por sección para un diseño por intensidad territorial", "parcial", SERPAVI,
               falta="perceptores por municipio o sección", autor="sí"),
        ],
        nota_sellado="la ECV identifica la CCAA de residencia: los hogares de las 8 CCAA selladas se excluyen de la forma "
                     "reducida, lo que reduce los cerca de 2.200-2.500 hogares por ventana de Q7a de V16."),
    Estudio(
        "E5", "Oferta y suelo (Saiz, 2010)", "replicable en parte",
        "Hay oferta (obra nueva neta del Catastro, iniciadas y terminadas), precios municipales y provinciales, solares y precio "
        "del suelo, pero faltan las restricciones del diseño de Saiz: pendiente (MDT05), agua y suelo no urbanizable, y "
        "planeamiento (SIU). La Red Natura no se usa como instrumento (falló en Q4). El Bartik de empleo es parcial (afiliación "
        "municipal desde 2011 con celdas suprimidas).",
        {"08": "réplica", "46": "réplica", "29": "réplica", "28": "réplica", "07": "réplica"},
        [
            _r("Oferta: obra nueva y parque", "disponible",
               ["base:obra_nueva_neta_catastro", "base:obra_nueva_viviendas_inspire", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv"],
               esencial=True),
            _r("Precio de compra municipal y provincial", "disponible", ["base:p_tasado", "base:valor_tasado"], esencial=True),
            _r("Restricción física: pendiente (MDT05)", "falta", [],
               falta="MDT05 del CNIG (centro de descargas con registro)", autor="sí", esencial=True),
            _r("Restricción física: costa", "parcial", ["data/raw/v10/geo/seccionado_2025.zip"],
               falta="línea de costa o DPMT del MITECO (dpmt.zip); hoy solo la geometría municipal", autor="sí"),
            _r("Restricción física: agua y suelo no urbanizable", "falta", [],
               falta="CORINE Land Cover 2018 o SIOSE (cuenta en el CLMS)", autor="sí", esencial=True),
            _r("Restricción de planeamiento (SIU)", "falta", [],
               falta="Sistema de Información Urbana del MIVAU (suelo urbano y urbanizable por municipio)", autor="sí",
               esencial=True),
            _r("Red Natura 2000 (solo control, no instrumento)", "parcial",
               ["data/raw/v16/oferta_suelo/_terceros/_grandes/n2000_2025_shp.zip"],
               falta="licencia por confirmar (en _terceros)", autor="sí"),
            _r("Suelo disponible y precio del suelo", "disponible",
               ["data/raw/v4/catastro_solares_municipios.csv.gz", "data/raw/mivau_v2_suelo.csv"],
               nivel="municipio (solares); CCAA y provincia (precio del suelo)", periodo="2012-2026; 2004-2026"),
            _r("Bartik de empleo (cuotas sectoriales locales y crecimiento nacional por sector)", "parcial",
               ["base:ss_afiliados_cota_inferior", "data/raw/v11/ss_afiliacion_municipio/*",
                "data/raw/v17/oferta_capacidad/ine/ine_tabla_65123.json"],
               nivel="municipio (afiliación); nacional (EPA por rama)", periodo="2011-2026",
               falta="afiliación por provincia y sección CNAE desde 2001 (Seguridad Social, abierta); celdas <5 suprimidas",
               autor="no", esencial=True),
            _r("Unidad de análisis: áreas urbanas", "falta", [],
               falta="Atlas de las Áreas Urbanas del MIVAU (municipios por área urbana; abierto)", autor="no"),
            _a("Choques de demanda de E3 para la interacción", "disponible",
               ["data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz"]),
        ]),
    Estudio(
        "E6", "Obra nueva y alquileres cercanos (literatura reciente; por localizar en la fase 1)", "replicable en parte",
        "El año de construcción por edificio con geometría (INSPIRE) solo está para unos 94 municipios, casi todos de la "
        "provincia de València; con SERPAVI por sección (anual, stock) cabe un piloto allí. Para el resto de España hace falta "
        "la descarga masiva del Catastro (o ampliar INSPIRE), y el alquiler a escala de anuncio o contrato no existe en el "
        "repositorio. Fuera de València: NO ESTIMABLE.",
        {"46": "réplica (piloto)", "08": "ampliación", "28": "ampliación"},
        [
            _r("Edificios nuevos con fecha y geometría (por parcela)", "parcial",
               ["data/raw/v11/catastro_inspire/original/BU_*.zip", "data/raw/v11/catastro_inspire/edificios_seccion.csv.gz",
                "base:catastro_inspire_viviendas_por_antiguedad"],
               nivel="edificio (unos 94 municipios, provincia de València) y sección", periodo="stock vigente 2026 (año de construcción)",
               falta="resto de España: descarga masiva alfanumérica del Catastro (certificado electrónico) o INSPIRE "
                     "Buildings por municipio (abierto)", autor="sí", esencial=True),
            _r("Alquiler por sección", "disponible", SERPAVI, esencial=True),
            _r("Alquiler por anuncio o contrato georreferenciado", "falta", [],
               falta="anuncios de portales o fianzas georreferenciadas (agencias autonómicas)", autor="sí"),
            _r("Controles por sección", "disponible", CONTROLES_SECCION),
            _a("Uso, superficie y fecha por inmueble en toda España", "falta", [],
               falta="descarga masiva alfanumérica del Catastro", autor="sí"),
        ]),
    Estudio(
        "E7", "Tipos de interés (Banco de España y BCE)", "replicable en parte",
        "A escala nacional todo está: sorpresas de Jarociński-Karadi (mensuales, CC BY), tipos hipotecarios, precios, "
        "compraventas, crédito y controles. El panel provincial con exposición no: el peso de la hipoteca variable solo es "
        "nacional y las compras sin hipoteca por provincia solo se aproximan (compraventas menos hipotecas).",
        {"28": "panel", "08": "panel", "07": "panel", "30": "panel"},
        [
            _r("Sorpresas de política monetaria (instrumento externo)", "disponible",
               ["data/raw/v16/demanda_internacional/bce_sorpresas/*"], nivel="zona del euro (reunión y mes)",
               periodo="1999-2025", esencial=True),
            _r("EA-MPD (robustez)", "parcial", ["data/raw/v16/demanda_internacional/_terceros/bce_sorpresas/*"],
               falta="licencia por decidir (en _terceros)", autor="sí"),
            _r("Tipos hipotecarios y Euríbor", "disponible",
               ["base:tipo_hip_bde", "base:tipo_hip_bce", "base:euribor_1y"], esencial=True),
            _r("Precios, alquiler y compraventas nacionales", "disponible",
               ["base:p_tasado", "base:ipv", "base:compraventas", "base:ipc_alquiler"], esencial=True),
            _r("Crédito nuevo y controles macro", "disponible",
               ["base:credito_nuevo", "base:pib_vol_idx", "base:inflacion_ipc_yoy", "base:ocupados"]),
            _r("Peso de la hipoteca a tipo variable por provincia", "parcial",
               ["base:bce_cuota_tipo_variable", "data/raw/v16/demanda_internacional/bde_fijacion/*"],
               nivel="nacional", periodo="2003-2026",
               falta="desglose provincial (Registradores, Estadística Registral, no redistribuible; o Banco de España)",
               autor="sí", esencial=True),
            _r("Compras sin hipoteca por provincia", "parcial",
               ["data/raw/ine_v2_etdp_prov.csv", "data/raw/ine_v2_hipotecas_prov.csv"], nivel="provincia",
               periodo="2007-2026",
               falta="solo aproximación (compraventas menos hipotecas); compras al contado del Notariado", autor="sí"),
            _a("Precio, compraventas e hipotecas provinciales", "disponible",
               ["base:valor_tasado", "base:compraventas", "base:hip_n"]),
        ],
        nota_sellado="las proyecciones locales y el SVAR nacionales no pierden muestra (la nación solo tiene sellado temporal)."),
    Estudio(
        "E8", "Fiscalidad de la compra (Best y Kleven, 2018; Besley et al., 2014)", "replicable en parte",
        "El DiD escalonado es posible con los cambios del tipo general del ITP (Hacienda, régimen común) y las compraventas de "
        "vivienda usada y el valor tasado provinciales, con fechas aproximadas y pocos clusters. El bunching no: no hay "
        "compraventas por tramo de precio. Faltan tipos reducidos y forales.",
        {"28": "CCAA de régimen común", "30": "CCAA de régimen común", "07": "CCAA de régimen común",
         "35": "CCAA de régimen común", "08": "CCAA de régimen común", "46": "CCAA de régimen común",
         "41": "CCAA de régimen común"},
        [
            _r("Calendario de tipos de ITP y AJD por CCAA", "parcial", ["data/raw/v16/intervenciones/intervenciones.csv"],
               nivel="CCAA (régimen común)", periodo="2010-2026",
               falta="fechas exactas de las leyes (hoy casi todas a 1 de enero), tipos reducidos (jóvenes, familias, VPO) y "
                     "tipos forales: leyes autonómicas en BOE y diarios oficiales", autor="no", esencial=True),
            _r("Compraventas de vivienda usada por provincia", "disponible", ["data/raw/ine_v2_etdp_prov.csv", "base:compraventas"],
               nivel="provincia", periodo="2007-01 a 2026-07 mensual", esencial=True),
            _r("Precio provincial", "disponible", ["base:valor_tasado"], esencial=True),
            _r("Compraventas por tramo de precio (bunching)", "falta", [],
               falta="Notariado (CIEN) o Registradores por tramo, o AEAT (modelo 600) por tramo", autor="sí"),
            _r("Recaudación del ITP por CCAA (primera etapa)", "falta", [],
               falta="liquidación de tributos cedidos (Ministerio de Hacienda; abierta)", autor="no"),
            _a("Compraventas municipales (municipios grandes)", "disponible",
               ["data/raw/mivau_transacciones_municipios.csv", "base:trans_total"]),
        ]),
    Estudio(
        "E9", "Compradores no residentes (Badarinza y Ramadorai, 2018; Cvijanović y Spaenjers, 2021)", "replicable en parte",
        "Hay compras por nacionalidad del comprador por CCAA (Notariado, semestral desde 2007) y por provincia sin serie larga "
        "(Registradores, anuario 2016-2025, no redistribuible), y la exposición se puede aproximar con el padrón de 2003 por "
        "nacionalidad. Faltan tipos de cambio y la serie provincial por nacionalidad. La golden visa (fin en 2025) tiene uno o "
        "dos semestres posteriores. Las provincias con más compra extranjera están en gran parte selladas.",
        {"07": "réplica", "35": "réplica", "38": "réplica", "30": "réplica", "28": "réplica", "03": "réplica",
         "29": "réplica", "17": "réplica", "08": "réplica"},
        [
            _r("Compras de vivienda por nacionalidad del comprador y territorio", "parcial",
               ["data/raw/pdf/notariado_cgn_extranjeros_semestral.csv", "data/raw/pdf/registradores_eri_anuario.csv",
                "data/raw/pdf/notariado_cv_prov_trimestral.csv", "data/raw/mivau_transacciones_residencia.csv"],
               nivel="CCAA (Notariado); provincia y CCAA (Registradores); provincias de la C. Valenciana (Notariado)",
               periodo="2007S1-2025 (Notariado); 2016-2025 (Registradores)",
               falta="serie provincial por nacionalidad (Notariado, portal estadístico)", autor="sí", esencial=True),
            _r("Exposición histórica por nacionalidad", "disponible",
               ["data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz"],
               falta="es población residente, no compradores: aproximación declarada"),
            _r("Choques en los países de origen (PIB, precios, tipo de cambio, riesgo)", "parcial",
               ["data/raw/eu_hpi.csv", "data/raw/oecd_house_prices.csv", "data/raw/eu_income_emp.csv"],
               nivel="país", periodo="2000-2025",
               falta="tipos de cambio bilaterales y primas de riesgo (BCE y bancos centrales; abiertos)", autor="no"),
            _r("Fin de la golden visa (LO 1/2025)", "parcial",
               ["data/raw/v16/intervenciones/intervenciones.csv", "data/raw/pdf/notariado_cgn_extranjeros_semestral.csv"],
               falta="autorizaciones de residencia por inversión (OPI); periodo posterior de uno o dos semestres", autor="sí"),
        ]),
    Estudio(
        "E10", "Grandes tenedores e inversores institucionales (literatura de EE. UU. y Europa)",
        "NO ESTIMABLE con los datos actuales",
        "No hay variación temporal de la titularidad por zona: la estadística catastral por tramo y tipo de titular solo tiene "
        "tres cortes (2024-2026) y la serie 2012-2023 tiene otra definición. Solo cabe una asociación transversal, con lo que "
        "dicen los datos parciales de V17.",
        {"08": "réplica", "28": "réplica"},
        [
            _r("Entrada de grandes tenedores por zona y año (panel de titularidad)", "parcial",
               ["data/raw/v11/catastro_titularidad/p_spi_mun_v_tpf.csv.gz", "base:v12_titularidad_pct_mas10",
                "base:v12_titularidad_pct_pj", "base:catastro_titulares_jaxi"],
               nivel="municipio", periodo="2024-2026 (tramos); 2012-2023 con otra definición (no encadenable)",
               falta="serie homogénea por tramo de titular 2012-2026 (petición al Catastro)", autor="sí", esencial=True),
            _r("Compras de personas jurídicas", "parcial",
               ["data/raw/v16/demanda_internacional/ine_etdp_titular/*", "data/raw/v4/ine_v4_t50256.csv"],
               nivel="nacional", periodo="2007-2026", falta="desglose provincial (Notariado)", autor="sí"),
            _r("Titularidad del parque de alquiler", "parcial", ["data/raw/v17/titularidad/*"],
               falta="solo documentos (Barcelona, Ministerio); microdatos del Panel de Hogares AEAT-IEF", autor="sí"),
            _r("Alquiler por sección y municipio", "disponible", SERPAVI),
        ]),
    Estudio(
        "E11", "Viviendas vacías (Segú, 2020)", "NO ESTIMABLE con los datos actuales",
        "Falta el tratamiento: la adopción municipal del recargo del IBI (Ley 12/2023) y el calendario del impuesto catalán no "
        "están en el repositorio, y la vacancia solo tiene dos cortes censales con métodos distintos (2011 y 2021, este por "
        "consumo eléctrico).",
        {"08": "réplica", "28": "réplica"},
        [
            _r("Viviendas vacías, Censo 2021 (consumo eléctrico)", "disponible",
               ["data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv", "data/raw/v11/ine_censo2021/*"],
               nivel="municipio y sección", periodo="2021"),
            _r("Viviendas vacías, Censo 2011", "parcial", ["base:censo2011_viviendas", "data/raw/v9/ine_censos/censo_t3457.csv.gz"],
               nivel="provincia", periodo="2011",
               falta="vacías por municipio en 2011 (INE, abierto)", autor="no", esencial=True),
            _r("Vacancia anual por consumo eléctrico", "falta", [],
               falta="estadística experimental del INE de viviendas vacías por consumo (por verificar edición)", autor="no"),
            _r("Recargo del IBI por municipio y año e impuesto catalán sobre vacías", "parcial",
               ["data/raw/v16/intervenciones/intervenciones.csv"], nivel="estatal (norma habilitante)", periodo="2023",
               falta="ordenanzas fiscales municipales (adopción y fecha del recargo) y Ley catalana 14/2015", autor="sí",
               esencial=True),
            _r("Alquiler por sección y municipio", "disponible", SERPAVI),
        ]),
    Estudio(
        "E12", "Vivienda pública (desplazamiento de la promoción privada)", "NO ESTIMABLE con los datos actuales",
        "No hay promociones públicas por municipio y año. Las calificaciones de vivienda protegida por provincia y año permiten "
        "solo una asociación provincial con la obra libre, sin variación exógena.",
        {"28": "réplica", "08": "réplica"},
        [
            _r("Promociones públicas por municipio y año", "falta", [],
               falta="registros del MIVAU, CASA 47 (antes SEPES) y de las empresas públicas autonómicas", autor="sí",
               esencial=True),
            _r("Calificaciones de vivienda protegida", "disponible", ["data/raw/mivau_v2_protegida.csv"],
               nivel="CCAA y provincia", periodo="1991-2026"),
            _r("Obra privada (libre) iniciada y terminada", "disponible", ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv"]),
            _r("Precios del entorno", "disponible", ["base:p_tasado"] + SERPAVI),
            _a("Parque social y gasto público", "parcial", ["data/raw/v17/parque_social/*"],
               falta="solo agregados nacionales y por CCAA en PDF", autor="no"),
        ]),
    Estudio(
        "F1", "Precio de largo plazo con corrección de error (nacional y panel provincial)", "replicable en parte",
        "Nacional, completo desde 1995-1999. Panel provincial: falta la renta disponible de los hogares por provincia (INE, "
        "Contabilidad Regional, abierta) y los hogares provinciales antes de 2021; hoy solo PIB provincial, IRPF desde 2016 y "
        "ADRH desde 2015.",
        {"28": "panel", "07": "panel", "30": "panel"},
        [
            _r("Precio real de compra", "disponible", ["base:p_tasado", "base:valor_tasado", "base:deflactor"], esencial=True),
            _r("Renta disponible real de los hogares (nacional)", "disponible", ["base:renta_hog_real"], esencial=True),
            _r("Renta disponible de los hogares por provincia", "parcial",
               ["data/raw/ine_v2_cre.csv", "base:aeat_irpf_renta_disponible_media", "base:adrh_renta_neta_hogar"],
               falta="renta disponible bruta de los hogares por provincia (INE, Contabilidad Regional; abierta)",
               autor="no", esencial=True),
            _r("Tipo hipotecario real", "disponible", ["base:tipo_hip_real_bde"]),
            _r("Población y hogares", "parcial",
               ["base:pob_total", "base:hogares_epa", "data/raw/ine_v2_hogares_prov.csv"],
               falta="hogares por provincia antes de 2021 (EPA por provincia; INE, abierta)", autor="no"),
            _r("Parque de viviendas por hogar", "disponible", ["data/raw/mivau_parque.csv"],
               nivel="nacional, CCAA y provincia", periodo="2001-2025"),
            _r("Indicador de sobrevaloración del Banco de España (comparación)", "disponible",
               ["data/raw/v17/credito/bde_si_1_5.csv", "docs/v17/referencias_bde.md"], nivel="nacional"),
            _a("Paneles provinciales ya construidos", "disponible",
               ["data/processed/v7/panel_prov_q_v7.csv", "data/processed/v8/cv_prov_q_v8.csv"]),
        ]),
    Estudio(
        "F2", "Alquiler equivalente por provincia", "replicable en parte",
        "El alquiler provincial existe (SERPAVI e IPVA 2011-2024 en niveles e índices; IPC de alquiler desde 2002 solo como "
        "índice), pero la serie en niveles es corta (14 años) y comparte con F1 la falta de renta de los hogares provincial.",
        {"28": "panel", "07": "panel"},
        [
            _r("Alquiler real por provincia", "disponible", SERPAVI + IPVA + ["base:ipc_alquiler_indice"],
               falta="niveles solo 2011-2024", esencial=True),
            _r("Renta de los hogares por provincia", "parcial", ["data/raw/ine_v2_cre.csv"],
               falta="ver F1", autor="no", esencial=True),
            _r("Hogares, parque y tipos", "disponible", ["data/raw/mivau_parque.csv", "base:pob_total", "base:tipo_hip_real_bde"]),
        ]),
    Estudio(
        "F3", "Elasticidad de la oferta y del parque por provincia", "replicable en parte",
        "Iniciadas y terminadas por provincia desde 1991 y precio provincial desde 1995; los costes de construcción solo son "
        "nacionales (salvo el precio del suelo provincial) y los visados no tienen desglose provincial; las restricciones son "
        "las de E5 (parciales).",
        {"28": "panel", "07": "panel"},
        [
            _r("Iniciadas y terminadas por provincia", "disponible",
               ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv", "base:iniciadas"], esencial=True),
            _r("Precio provincial", "disponible", ["base:valor_tasado"], esencial=True),
            _r("Costes de construcción", "parcial",
               ["base:costes_constr", "data/raw/v17/oferta_capacidad/ine/ine_tabla_8381.json", "data/raw/mivau_v2_suelo.csv"],
               nivel="nacional (costes); CCAA y provincia (suelo)",
               falta="costes con variación provincial (no hay serie oficial)", autor="no", esencial=True),
            _r("Visados por provincia", "parcial", ["base:visados"], falta="desglose provincial (MIVAU o CSCAE; abierto)",
               autor="no"),
            _r("Restricciones físicas y de planeamiento", "parcial", ["data/raw/v4/catastro_solares_municipios.csv.gz"],
               falta="las de E5: MDT05, agua, SIU", autor="sí"),
            _r("Crédito a promotores", "disponible", ["base:credito_promotor"]),
        ]),
]


# ── lectura de metadatos (nunca de datos) ─────────────────────────────────────────────────────────────────────────────
def _leer_csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def diccionario() -> dict[str, tuple[str, str]]:
    """variable → (niveles, periodo) del diccionario de la base (docs/v10/diccionario_base.md)."""
    out = {}
    fila = re.compile(r"^\| `([^`]+)` \|.*\| ([^|]*) \| ([^|]*) \|\s*$")
    for linea in (RAIZ / "docs" / "v10" / "diccionario_base.md").read_text(encoding="utf-8").splitlines():
        m = fila.match(linea)
        if m:
            out[m.group(1)] = (m.group(2).strip(), m.group(3).strip())
    return out


def ficheros_declarados() -> set[str]:
    """Rutas (relativas a la raíz) que citan los manifiestos de data/raw y los inventarios de V13, V16 y V17."""
    rutas: set[str] = set()
    raw = RAIZ / "data" / "raw"
    for m in sorted(raw.rglob("_manifest*.csv")):
        base = m.parent.relative_to(RAIZ).as_posix()
        for r in _leer_csv(m):
            f = (r.get("fichero") or r.get("archivo") or "").strip()
            if f:
                rutas.add(f if f.startswith("data/") else f"{base}/{f}")
    for p, col in ((RAIZ / "docs" / "v13" / "datos_inventario.csv", "fichero"),
                   (RAIZ / "docs" / "v16" / "inventario_fuentes.csv", "fichero")):
        rutas |= {r[col].strip() for r in _leer_csv(p) if r.get(col)}
    for r in _leer_csv(RAIZ / "output" / "v17" / "f1" / "inventario.csv"):
        rutas |= {x.strip() for x in (r.get("rutas_presentes") or "").split(";") if x.strip()}
    return {x for x in rutas if not x.startswith(_PROHIBIDA)}


def nombres_en_disco() -> set[str]:
    """Nombres (no contenido) de ficheros y carpetas de data/raw, data/processed, data/manual y docs/v16-v17/fuentes."""
    nombres: set[str] = set()
    for d in ("data/raw", "data/processed", "data/manual", "data/base/geo", "docs/v16/fuentes", "docs/v17/fuentes", "docs/v17"):
        raiz = RAIZ / d
        if not raiz.exists():
            continue
        for actual, dirs, fich in os.walk(raiz):
            rel = Path(actual).relative_to(RAIZ).as_posix()
            assert not rel.startswith(_PROHIBIDA)
            dirs[:] = sorted(x for x in dirs if not x.startswith("."))
            nombres.add(rel)
            nombres |= {f"{rel}/{f}" for f in fich}
    return nombres


def _resolver(ref: str, dic: dict, rutas: set[str]) -> bool:
    if ref.startswith("base:"):
        return ref[5:] in dic
    if any(c in ref for c in "*?["):
        return any(fnmatch(r, ref) for r in rutas)
    return ref in rutas or any(r.startswith(ref.rstrip("/") + "/") for r in rutas)


# ── construcción ─────────────────────────────────────────────────────────────────────────────────────────────────────
def sellado() -> dict:
    prov = sorted(holdout.provincias_selladas_v6())
    por_ccaa: dict[str, list[str]] = {}
    for p, c in holdout.CCAA_PROV.items():
        por_ccaa.setdefault(c, []).append(p)
    ccaa = sorted(c for c, ps in por_ccaa.items() if set(ps) <= set(prov))
    return {"provincias": prov, "ccaa": ccaa}


def construir() -> tuple[list[dict], list[dict]]:
    dic = diccionario()
    rutas = ficheros_declarados() | nombres_en_disco()
    filas, resumen = [], []
    for e in ESTUDIOS:
        assert e.veredicto in VEREDICTOS, e.id
        for v in e.vars:
            assert v.estado in ESTADOS and v.uso in ("réplica", "ampliación"), (e.id, v.variable)
            ok = [f for f in v.fuentes if _resolver(f, dic, rutas)]
            no = [f for f in v.fuentes if f not in ok]
            estado, falta, autor = v.estado, v.falta, v.autor
            if v.fuentes and not ok:
                estado = "falta"
            elif no and estado == "disponible":
                estado = "parcial"
            if no:
                falta = "; ".join(x for x in (falta, "no encontradas en el repositorio: " + ", ".join(no)) if x)
                autor = autor or "no"
            nivel, periodo = v.nivel, v.periodo
            bases = [dic[f[5:]] for f in ok if f.startswith("base:")]
            if bases and not nivel:
                nivel = "; ".join(dict.fromkeys(b[0] for b in bases if b[0]))
            if bases and not periodo:
                periodo = "; ".join(dict.fromkeys(b[1] for b in bases if b[1]))
            filas.append({"estudio": e.id, "uso": v.uso, "variable": v.variable, "estado": estado,
                          "fuente_en_repo": "; ".join(ok), "nivel": nivel, "periodo": periodo, "falta": falta,
                          "requiere_autor": autor if estado != "disponible" else (autor if autor == "sí" else "")})
        rep = [(f, v) for f, v in zip(filas[-len(e.vars):], e.vars) if v.uso == "réplica"]
        esenciales = [f["estado"] for f, v in rep if v.esencial]
        if e.veredicto == "replicable":
            assert all(s == "disponible" for s in esenciales), e.id
        elif e.veredicto.startswith("NO ESTIMABLE"):
            assert any(s != "disponible" for s in esenciales), e.id
        else:
            assert any(f["estado"] == "disponible" for f, _ in rep) and any(s != "disponible" for s in esenciales), e.id
        resumen.append({"estudio": e.id, "veredicto": e.veredicto,
                        **{k: sum(f["estado"] == k for f in filas[-len(e.vars):]) for k in ESTADOS}})
    return filas, resumen


def comprobar_v17() -> list[str]:
    """Paso 1 de la fase 0: piezas de V17 (por nombre) y check_v17 (solo lectura)."""
    lineas = []
    for p in ("docs/v17/referencias_bde.md", "output/v17/lectura_bde", "output/v17/auditoria/tabla_final.md", "data/raw/v17"):
        lineas.append(f"- `{p}`: {'existe' if (RAIZ / p).exists() else 'NO EXISTE'}")
    r = subprocess.run([sys.executable, str(RAIZ / "src" / "v17" / "check_v17.py")], cwd=RAIZ, capture_output=True, text=True)
    ult = [x for x in r.stdout.splitlines() if x.startswith("check_v17:")]
    lineas.append(f"- `python3 src/v17/check_v17.py`: {ult[-1] if ult else 'sin salida'} (código {r.returncode})")
    return lineas


def informe(filas: list[dict], resumen: list[dict], sel: dict, v17: list[str]) -> str:
    sp = set(sel["provincias"])
    nombres_ccaa = ", ".join(f"{CCAA[c]} ({c})" for c in sel["ccaa"])
    nombres_prov = ", ".join(f"{PROV[p]} ({p})" for p in sel["provincias"])
    n_libres = len([p for p in PROV if p not in sp and p not in ("51", "52")])
    o = [
        "# V18 · Fase 0 · Inventario de datos por estudio",
        "",
        f"Generado por `python3 src/v18/f0_inventario.py` ({FECHA}); no editar a mano. No estima nada y no lee datos: solo "
        "manifiestos, el diccionario de la base, los inventarios de V13, V16 y V17 y los nombres de los ficheros. La tabla "
        "completa está en `output/v18/f0/inventario.csv`. Los veredictos son preliminares: la fase 3 (plan de replicación) "
        "los fija antes de estimar.",
        "",
        "## Comprobación de V17",
        "",
        *v17,
        "",
        "## Unidades selladas (v6) que se excluyen de toda estimación",
        "",
        f"- CCAA enteras: {nombres_ccaa}.",
        f"- Provincias ({len(sel['provincias'])}): {nombres_prov}.",
        f"- Barcelona (08) {'está sellada' if '08' in sp else 'NO está sellada'}; Madrid (28) "
        f"{'está sellada' if '28' in sp else 'no está sellada'}. Paneles provinciales: {n_libres} provincias sin Ceuta ni Melilla.",
        "- Fuente: `holdout.provincias_selladas_v6()` y `holdout.CCAA_PROV` (cálculo con la semilla, sin abrir datos sellados).",
        "- La nación no se sella espacialmente: los diseños solo nacionales (E7 nacional, F1 nacional) no pierden muestra.",
        "",
        "## Resumen",
        "",
        "| Estudio | Veredicto preliminar | Variables disponibles | Parciales | Faltan |",
        "|---|---|---|---|---|",
    ]
    o += [f"| {r['estudio']} | {r['veredicto']} | {r['disponible']} | {r['parcial']} | {r['falta']} |" for r in resumen]
    for e in ESTUDIOS:
        fe = [f for f in filas if f["estudio"] == e.id]
        excl = [f"{PROV[p]} [{e.clave[p]}]" for p in sorted(e.clave) if p in sp]
        dentro = [PROV[p] for p in sorted(e.clave) if p not in sp]
        o += ["", f"## {e.id} · {e.titulo}", "", f"**Veredicto preliminar: {e.veredicto}.** {e.porque}", ""]
        if excl:
            resto = (f"siguen {', '.join(dentro)}" if dentro else f"el panel sigue con las {n_libres} provincias no selladas")
            o.append(f"- **Sellado v6 (reduce la muestra):** se excluyen {'; '.join(excl)}; {resto}.")
        if e.nota_sellado:
            o.append(f"- **Sellado v6:** {e.nota_sellado}")
        if not excl and not e.nota_sellado:
            o.append("- **Sellado v6:** ninguna unidad clave del diseño está sellada.")
        for uso in ("réplica", "ampliación"):
            xs = [f for f in fe if f["uso"] == uso]
            if not xs:
                continue
            o.append(f"- **{uso.capitalize()}:**")
            for f in xs:
                extra = f" Falta: {f['falta']}." if f["falta"] and f["estado"] != "disponible" else ""
                aut = " Requiere al autor." if f["requiere_autor"] == "sí" else ""
                fuente = f" ({f['fuente_en_repo']})" if f["fuente_en_repo"] else ""
                o.append(f"  - {f['variable']}: **{f['estado']}**{fuente}.{extra}{aut}")
    sin_autor = [f for f in filas if f["estado"] != "disponible" and f["requiere_autor"] == "no"]
    o += ["", "## Lo que falta y no requiere al autor (fuentes abiertas, para descargar en la fase 1 o antes de la 4)", ""]
    o += [f"- {f['estudio']} · {f['variable']}: {f['falta']}." for f in sin_autor]
    con_autor = sorted({f["estudio"] for f in filas if f["requiere_autor"] == "sí"}, key=[e.id for e in ESTUDIOS].index)
    o += ["", f"Lo que requiere al autor está en docs/v18/tareas_autor.md, sección «V18 · fase 0» (estudios afectados: "
          f"{', '.join(con_autor)})."]
    o += ["", "## F4 · Coherencia", "",
          "No necesita datos propios: compara en signo y orden de magnitud las elasticidades de F1-F3 con las de la sección E. "
          "Depende de que E3, E5, E7 y F1-F3 lleguen a estimarse.", ""]
    return "\n".join(o)


def _csv(filas: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNAS, lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
    return buf.getvalue()


def main(salida: Path = OUT) -> int:
    filas, resumen = construir()
    sel = sellado()
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "inventario.csv").write_text(_csv(filas), encoding="utf-8")
    (salida / "informe.md").write_text(informe(filas, resumen, sel, comprobar_v17()), encoding="utf-8")
    for r in resumen:
        print(f"{r['estudio']}: {r['veredicto']} (disponibles {r['disponible']}, parciales {r['parcial']}, faltan {r['falta']})")
    print(f"escrito {salida.relative_to(RAIZ) if salida.is_relative_to(RAIZ) else salida}/inventario.csv e informe.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
