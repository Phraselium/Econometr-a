"""V18 · Fase 3 · Sellado de V18: topes de entrenamiento por variable y unidades excluidas (adenda 1.4 y 1.5; decisión K3).

Genera docs/v18/sellado_v18.json de forma determinista, sin red y sin elección: los valores salen de las reglas (a)-(g) de la
sección 1.4 de docs/v18/plan_replicacion_adenda.md aplicadas a
- los manifiestos docs/v15/sellado_v15.json y docs/v16/sellado_v16.json (claves «variable|nivel|frecuencia», conjuntos y preguntas);
- los metadatos de la base (data/base/hechos.parquet: solo `variable, nivel, frecuencia, min(periodo), max(periodo)` agrupados;
  nunca valores), cuya huella debe coincidir con la registrada en los manifiestos de V15 y V16 (estado de la base en la etiqueta);
- los manifiestos de data/raw leídos en el commit de la etiqueta (`git show <commit>:<ruta>`; fechas y ediciones, nunca datos);
- las funciones de src/holdout.py que devuelven listas de unidades selladas (ninguna abre data/sealed).

Solo lee metadatos: no abre ninguna fila de datos ni la muestra sellada, y no ejecuta ningún sellar_* ni evaluate_*.
Por eso declara ALCANCE_TERRITORIAL = "sin lectura de datos" (guarda «fuga v6» de check_v17). El filtro territorial de la fase 4
(holdout.excluir_sellados_v6 más V15 y V16) lo aplica src/v18/sellado.py.

Orden de las reglas (adenda 1.4): (f) sustituto → hereda la clave de la variable sustituida; (b) media anual desde T o M;
(a) clave de la frecuencia usada (manda la menor de V15 y V16); (c) clave en otra frecuencia del mismo nivel (final del periodo
más antiguo); (d) variable de un conjunto de V15/V16 sin clave en ese nivel → sellada entera; (e) variable fuera de todo conjunto
→ último periodo presente en el repositorio en el commit de la etiqueta; (g) ediciones: hasta 2026-10-17 con clave, hasta la fecha
de la etiqueta en (e). Si el Anexo C de la adenda declara un corte más restrictivo que la regla literal, se aplica el más
restrictivo de los dos y se anota la discrepancia (nunca se aplica el más permisivo).

Uso: python3 src/v18/f3_sellado.py   (make v18_f3, antes de src/v18/f3_plan.py)
"""
from __future__ import annotations

import calendar
import csv
import datetime as dt
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v18"))
import etiqueta  # noqa: E402
import holdout  # noqa: E402

SALIDA = RAIZ / "docs" / "v18" / "sellado_v18.json"
MAN15 = RAIZ / "docs" / "v15" / "sellado_v15.json"
MAN16 = RAIZ / "docs" / "v16" / "sellado_v16.json"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
HECHOS_REL = "data/base/hechos.parquet"
RAW_RAIZ = "data/raw/_manifest.csv"

PATRON = {"A": r"^\d{4}$", "T": r"^\d{4}T[1-4]$", "M": r"^\d{4}-\d{2}$", "D": r"^\d{4}-\d{2}-\d{2}$"}

# ------------------------------------------------------------------ tabla de variables (plan + adenda, Anexo C, tabla consolidada)
E1R = ["E1-R1", "E1-R2", "E1-R3", "E1-R4"]
E7N = ["E7-R1", "E7-R1-ipv", "E7-R1-cv", "E7-R1-alq", "E7-R2"]
E3T = ["E3-R1", "E3-R1q", "E3-R2", "E3-R2b", "E3-R2q", "E3-A1", "E3-A2", "E3-A3", "E3-A4", "E3-A5"]
F1P = ["F1-R2", "F1-R2-alt", "F1-R2-pmg", "F1-A1"]


def V(var, nivel, frec, specs, origen=None, de=None, hereda=None, meta=None, anexo=None, nota=None):
    """Una fila: variable|nivel|frecuencia usada. de: frecuencia de origen de una media (regla b); hereda: variable con clave
    de la que es sustituto (regla f); meta: dónde está el último periodo de una serie de data/raw (regla e); anexo: corte del
    Anexo C para la comprobación cruzada (nunca más permisivo que la regla)."""
    return {"variable": var, "nivel": nivel, "frecuencia": frec, "especificaciones": specs, "origen": origen or [f"base:{var}"],
            "de": de, "hereda": hereda, "meta": meta, "anexo_c": anexo, "nota": nota}


VARIABLES = [
    # E1 · vivienda turística
    V("serpavi_alquiler_m2_mediana", "seccion", "A", E1R + ["E1-A1", "E1-A2", "E1-A3", "E6-R1", "E6-A1"],
      ["base:serpavi_alquiler_m2_mediana", "data/raw/v3/serpavi_secciones_nacional_v3.csv.gz"], anexo="2024"),
    V("serpavi_alquiler_mes_mediana", "seccion", "A", E1R + ["E1-A1"], nota="diagnóstico de composición por tamaño (adenda, AD-E1)"),
    V("serpavi_n_contratos_recuento", "seccion", "A", E1R,
      nota="prueba de composición por número de contratos: NO ESTIMABLE a escala de sección (adenda, AD-E1)"),
    V("bcn_hut_registro", "municipio", "T", E1R, nota="ventana de E1 hasta 2024 (Anexo C)"),
    V("bcn_hut_registro", "barrio", "T", E1R, ["data/manual/v11/bcn_hut_trimestral/*"],
      meta={"tipo": "nombres", "ruta": "data/raw/v11/manual/_manifest.csv", "campo": "fichero", "patron": r"bcn_hut_trimestral/(\d{4})_(\d)T_"},
      nota="cortes trimestrales del registro (descarga manual del autor); ventana de E1 hasta 2024 (Anexo C)"),
    V("bcn_hut_expediente", "barrio", "A", ["E1-R1"], ["data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz"],
      meta={"tipo": "fecha", "ruta": "data/raw/v9/bcn_hut/_manifest.csv", "campo_clave": "fichero", "valor": "bcn_hut_barrio_anio_expediente",
            "campo": "fecha_descarga", "frec": "D"},
      nota="reconstrucción por año de expediente: solo robustez (plan, E1 b)"),
    V("eurostat_plataformas_noches", "nuts3", "A", ["E1-R2", "E1-A1"], ["base:eurostat_plataformas_noches", "data/raw/v9/eurostat_plataformas/*"]),
    V("adrh_renta_neta_persona", "seccion", "A", E1R + ["E6-R2", "E10-A1"], anexo="2023"),
    V("pob_censo_anual", "seccion", "A", E1R + ["E6-R1"], anexo="2025"),
    V("ipva_indice", "distrito", "A", E1R + ["E1-A1"], nota="medida de alquiler alternativa"),
    V("ine_vut_vivienda_turistica", "seccion", "A", ["E1-A1"], de="M", anexo="2025", nota="media anual de la serie mensual"),
    V("ine_vut_vivienda_turistica", "seccion", "M", ["E1-A1"], anexo="2026-05"),
    V("openrta_altas_acumuladas", "seccion", "A", ["E1-A2"], ["data/raw/v16/alquiler_turismo/_terceros/openrta_all_2026-10-17.csv.gz"],
      meta={"tipo": "fecha", "ruta": "data/raw/v16/alquiler_turismo/_manifest.csv", "campo_clave": "fichero", "valor": "openrta_all",
            "campo": "fecha_descarga", "frec": "D"},
      nota="serie nueva por sección (altas con fecha agregadas); el mismo registro tiene clave municipal en V16 "
           "(andalucia_rta_altas_acumuladas_numero|municipio|A = 2025), que da el mismo tope"),
    V("vut_registro_gva_reconstruido", "municipio", "M", ["E1-A3"], anexo="2025-01"),
    # E2 · topes al alquiler
    V("incasol_renta_media", "municipio", "T", ["E2-R1", "E2-A1", "E2-A4"],
      ["base:incasol_renta_media", "data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz", "data/raw/v3/incasol_fianzas_municipio_v3.csv.gz"],
      anexo="2026T1"),
    V("incasol_contratos", "municipio", "T", ["E2-R1", "E2-R1c", "E2-A1", "E2-A4"],
      ["base:incasol_contratos", "data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz", "data/raw/v3/incasol_fianzas_municipio_v3.csv.gz"],
      anexo="2026T1"),
    V("incasol_renta_media", "municipio", "A", ["E2-R1"], anexo="2025", nota="robustez anual 2014-2021"),
    V("incasol_contratos", "municipio", "A", ["E2-R1c"], anexo="2025", nota="robustez anual 2014-2021"),
    V("pob_total", "municipio", "A", ["E2-R1", "E2-R1c", "E2-A1", "E2-A4", "E3-A3", "E10-A1"]),
    V("sepe_paro_registrado_media_anual", "municipio", "A", ["E2-R1", "E2-R1c", "E2-A4"]),
    V("aeat_irpf_renta_disponible_media", "municipio", "A", ["E2-R1", "E2-R1c"], nota="control municipal de renta (inventario de la fase 0)"),
    V("idescat_hut_n", "municipio", "A", ["E2-R1", "E2-R1c"], anexo="2025"),
    V("serpavi_alquiler_m2_mediana", "municipio", "A", ["E2-R1", "E2-A1", "E3-A3", "E10-A1"]),
    V("c21md_hogares_muestra", "municipio", "D", ["E2-R1c"],
      ["base:c21md_hogares_muestra", "data/raw/v11/ine_censo2021/hogares_muestra_municipio_nacionalidad.csv.gz"],
      nota="añadida DESPUÉS de la etiqueta (desviación B6-1, ronda 1 del abogado del diablo): hogares en alquiler (tenencia = 3) del Censo 2021, "
           "recuento MUESTRAL del 10 % solo de municipios de 10.000 habitantes o más, fijo en el tiempo; denominador de E2-R1c-v1 (adenda AD-E2, medida)"),
    V("zt_vigente", "municipio", "T", ["E2-A1", "E2-A2"], anexo="2026T3"),
    V("emal_renta_mensual_eur", "municipio", "T", ["E2-A2"], anexo="2025T4"),
    V("p_tasado", "municipio", "T", ["E2-A3"], anexo="2026T2"),
    V("p_tasado", "municipio", "A", ["E3-A3", "E5-A3"], de="T", anexo="2025"),
    V("trans_total", "municipio", "T", ["E2-A3", "E8-A2"], ["base:trans_total", "data/raw/mivau_transacciones_municipios.csv"], anexo="2024T4",
      nota="compraventas municipales; el Anexo C les aplica (f) con la clave provincial de compraventas (2024-12)"),
    # E3 · inmigración
    V("valor_tasado", "provincia", "A", E3T[:6] + ["E3-A4", "E3-A5", "E5-R1", "E5-A1", "E5-A2", "E12-A2", "F2-A2", "F3-A1", "F3-A2", "F3-A3"] + F1P,
      de="T", anexo="2024"),
    V("valor_tasado", "provincia", "T", ["E7-A2", "E8-R1", "E9-R1", "E9-R2", "E9-A1", "E9-A2"], anexo="2026T2"),
    V("pob_total", "provincia", "A", ["E3-R1", "E3-R2", "E3-R2b", "E3-A1", "E3-A2", "E3-A4", "E3-A5", "E8-R1", "E8-R2", "F1-A3"] + F1P, anexo="2024"),
    V("pob_extranj", "provincia", "A", ["E3-R1", "E3-R2", "E3-R2b", "E3-A1", "E3-A2", "E3-A4", "E3-A5"]),
    V("pob_extranjera", "municipio", "A", ["E3-R1", "E3-R2", "E3-A3", "E3-A5"], anexo="2022"),
    V("padron_pob_nacionalidad", "provincia", "A", E3T + ["E5-A1", "E9-R1", "E9-R2", "E9-A1", "E9-A2"],
      ["base:padron_pob_nacionalidad", "data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz"], anexo="2022"),
    V("padron_municipal_nacionalidad", "municipio", "A", ["E3-A3"], anexo="2022"),
    V("ecp_pob_nacionalidad", "provincia", "D", ["E3-A1", "E3-A2", "E3-A4"], hereda="padron_pob_nacionalidad", anexo="2022-12-31"),
    V("ine_migraciones_nacionalidad", "nacional", "A", E3T + ["E5-A1"], ["data/raw/ine_migraciones_nacionalidad.csv"],
      hereda="ine_emcr_inmigraciones_exterior_personas", anexo="2024", nota="entradas nacionales por nacionalidad (choque)"),
    V("iniciadas", "provincia", "A", ["E3-R1q", "E3-R2q", "E5-R1", "E5-A1", "E5-A2", "F3-R1", "F3-A1", "F3-A2", "F3-A3"],
      ["base:iniciadas", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv"], de="T", anexo="2024"),
    V("iniciadas_anual_tabla", "provincia", "A", ["E3-R1q", "E3-R2q", "E5-R1", "E5-A2", "F3-R1", "F3-A1", "F3-A2", "F3-A3"],
      hereda="iniciadas", anexo="2024"),
    V("terminadas", "provincia", "A", ["E3-R1q", "E3-R2q", "E5-R1", "F3-A1", "F3-A2"],
      ["base:terminadas", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv"], de="T", anexo="2024"),
    V("terminadas_anual_tabla", "provincia", "A", ["E3-R1q", "E3-R2q", "E5-R1"], anexo="2024"),
    V("terminadas", "provincia", "T", ["E6-R2", "E6-A3"], ["base:terminadas", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv"], anexo="2026T2"),
    V("ocupados_epa", "provincia", "A", ["E3-R1", "E3-R2", "E3-A1", "E3-A2", "E3-A5", "E6-R2"]),
    V("pib_provincial_cre", "provincia", "A", ["E3-R1", "E3-R2", "E3-A1", "E3-A5", "E12-A1"] + F1P, ["data/raw/ine_v2_cre.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "ine_v2_cre.csv", "campo": "ultima_fecha", "frec": "A"},
      nota="PIB provincial (control; sustituto de la renta provincial en F1-R2)"),
    V("ipc_alquiler_indice", "provincia", "A", ["E3-A2", "E6-R2", "E6-A3", "F2-R1", "F2-A1", "F2-A2"], anexo="2024"),
    V("ipc_alquiler_indice", "provincia", "T", ["E3-A2", "E6-R2", "E6-A3"], anexo="2026T2"),
    V("ipva_indice", "provincia", "A", ["E3-A2", "E6-R2", "F2-R1"], anexo="2024"),
    V("serpavi_alquiler_m2_mediana", "provincia", "A", ["E3-A2", "E3-A4", "F2-R1", "F2-A1"], anexo="2024"),
    V("censo2011_tenencia_nacionalidad", "provincia", "A", ["E3-A4"], ["data/raw/v11/ine_censos_microdatos/*"],
      meta={"tipo": "fijo", "periodo": "2011", "frec": "A"}, nota="corte único del Censo de 2011, anterior a la ventana (plan, E3-A4)"),
    # E5 · oferta y suelo
    V("obra_nueva_neta_catastro", "municipio", "A", ["E5-R1", "E5-A3"], anexo="2025"),
    V("deflactor", "nacional", "T", E7N + ["E7-R3", "E7-A1", "F1-R1", "F1-A3"], anexo="2026T2"),
    V("deflactor", "nacional", "A", ["E5-R1", "E5-A1", "E5-A2", "E5-A3", "E12-A2", "F1-A2", "F2-R1", "F2-A1", "F2-A2", "F3-A1", "F3-A2", "F3-A3"] + F1P,
      de="T", anexo="2025"),
    V("ss_afiliados_cota_inferior", "municipio", "M", ["E5-A3"]),
    V("ss_afiliados_cota_inferior", "municipio", "A", ["E5-A3"], de="M"),
    V("catastro_solares", "municipio", "A", ["E5-A1"], ["data/raw/v4/catastro_solares_municipios.csv.gz"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "v4/catastro_solares_municipios.csv.gz", "campo": "ultima_fecha", "frec": "A"},
      nota="se usa el corte de 2012"),
    # E6 · obra nueva
    V("catastro_inspire_viviendas_por_antiguedad", "seccion", "D", ["E6-R1", "E6-A1"],
      ["base:catastro_inspire_viviendas_por_antiguedad", "data/raw/v11/catastro_inspire/edificios_seccion.csv.gz"], anexo="2026-08-21"),
    # E7 · tipos de interés
    V("bce_jk_mp_median_m", "zona_euro", "M", E7N + ["E7-A2"],
      ["data/raw/v16/demanda_internacional/bce_sorpresas/*", "data/raw/v8/jk_shocks_ecb_mensual.csv"], anexo="2025-10"),
    V("bce_jk_mp_median_m", "zona_euro", "T", E7N + ["E7-A2"],
      ["data/raw/v16/demanda_internacional/bce_sorpresas/*", "data/raw/v8/jk_shocks_ecb_mensual.csv"], de="M", anexo="2025T3",
      nota="suma trimestral de la sorpresa mensual"),
    V("bce_jk_mp_pm_m", "zona_euro", "M", E7N, ["data/raw/v16/demanda_internacional/bce_sorpresas/*", "data/raw/v8/jk_shocks_ecb_mensual.csv"],
      anexo="2025-10", nota="sensibilidad «poor man's»"),
    V("bce_jk_mp_pm_m", "zona_euro", "T", E7N, ["data/raw/v16/demanda_internacional/bce_sorpresas/*", "data/raw/v8/jk_shocks_ecb_mensual.csv"],
      de="M", anexo="2025T3", nota="sensibilidad «poor man's»"),
    V("tipo_hip_bde", "nacional", "T", E7N + ["E7-A1", "E7-A2"], anexo="2026T2"),
    V("tipo_hip_bde", "nacional", "A", F1P, de="T", anexo="2025"),
    V("tipo_hip_real_bde", "nacional", "T", ["F1-R1", "F1-A3"], anexo="2026T2"),
    V("tipo_hip_real_bde", "nacional", "A", ["F1-A2", "F2-R1", "F2-A1", "F2-A2"], de="T", anexo="2025"),
    V("euribor_1y", "nacional", "T", E7N + ["E7-R3", "E7-A1"], anexo="2026T2"),
    V("p_tasado", "nacional", "T", E7N + ["E7-R3", "E7-A1", "F1-R1", "F1-A3"], anexo="2026T2"),
    V("p_tasado", "nacional", "A", ["F1-A2"], de="T", anexo="2025"),
    V("ipv", "nacional", "T", ["E7-R1-ipv"], anexo="2026T2"),
    V("ipv", "ccaa", "T", ["E8-R1", "E9-R1", "F1-R1"], nota="robustez de la medida de precio (IPV por CCAA)"),
    V("ipv", "ccaa", "A", ["E3-A1", "F1-R2"], de="T", nota="robustez de la medida de precio (IPV por CCAA)"),
    V("compraventas", "nacional", "T", ["E7-R1-cv", "E7-R2", "E7-R3", "E7-A1"], anexo="2026T2"),
    V("ipc_alquiler", "nacional", "T", ["E7-R1-alq"], anexo="2026T2"),
    V("pib_vol_idx", "nacional", "T", E7N + ["E7-R3", "E7-A1"], anexo="2026T2"),
    V("inflacion_ipc_yoy", "nacional", "T", E7N + ["E7-R3", "E7-A1"], anexo="2026T2"),
    V("credito_nuevo", "nacional", "T", E7N + ["E7-R3", "E7-A1"], anexo="2026T2"),
    V("visados", "nacional", "T", ["E7-R3", "E7-A1"]),
    V("pob_total", "nacional", "T", ["E7-R1", "F1-R1", "F1-A3"], nota="placebo de E7 y población de F1"),
    V("pob_total", "nacional", "A", ["F1-A2"], de="T", anexo="2025"),
    V("hip_n", "provincia", "M", ["E7-A2"], ["data/raw/ine_v2_hipotecas_prov.csv"], nota="exposición 2007-2019"),
    V("compraventas", "provincia", "M", ["E7-A2", "E8-R2"], ["data/raw/ine_v2_etdp_prov.csv"], anexo="2024-12"),
    # E9 · no residentes
    V("cuota_no_residentes_mivau", "provincia", "T", ["E9-R2", "E9-A2"], ["data/raw/mivau_transacciones_residencia.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_transacciones_residencia.csv", "campo": "ultima_fecha", "frec": "T"}),
    V("cuota_no_residentes_mivau", "provincia", "A", ["E9-R2"], ["data/raw/mivau_transacciones_residencia.csv"], de="T",
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_transacciones_residencia.csv", "campo": "ultima_fecha", "frec": "T"}),
    V("oecd_hpi", "pais", "T", ["E9-R1", "E9-R2", "E9-A1"], ["data/raw/oecd_house_prices.csv"], nota="precio de la vivienda en los países de origen"),
    V("eu_hpi", "pais", "T", ["E9-R1", "E9-R2", "E9-A1"], ["data/raw/eu_hpi.csv"], hereda="oecd_hpi"),
    V("eu_income_emp", "pais", "A", ["E9-R1", "E9-R2", "E9-A1"], ["data/raw/eu_income_emp.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "eu_income_emp.csv", "campo": "ultima_fecha", "frec": "A"},
      nota="PIB y empleo de los países de origen (riesgo en origen)"),
    V("tx_extranj_ccaa", "ccaa", "T", ["E9-A2"]),
    # E10 · grandes tenedores
    V("v12_titularidad_pct_mas10", "municipio", "A", ["E10-A1"], anexo="2026"),
    V("v12_titularidad_pct_pj", "municipio", "A", ["E10-A1"], anexo="2026"),
    # E12 · vivienda protegida
    V("mivau_obra_libre_iniciadas", "provincia", "A", ["E12-A1", "E12-A2"], ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv"], hereda="iniciadas",
      anexo="2024"),
    V("mivau_obra_libre_terminadas", "provincia", "A", ["E12-A1"], ["data/raw/mivau_v2_iniciadas_terminadas_prov.csv"], hereda="terminadas",
      anexo="2024", nota="añadida DESPUÉS de la etiqueta (desviación B6-1, ronda 1 del abogado del diablo): obra libre terminada, variante E12-A1-v3 [M] de la adenda"),
    V("mivau_calificaciones_protegida", "provincia", "A", ["E12-A1", "E12-A2"], ["data/raw/mivau_v2_protegida.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_v2_protegida.csv", "campo": "ultima_fecha", "frec": "M"}),
    V("mivau_parque", "provincia", "A", ["E12-A1", "E12-A2", "F1-R2-alt", "F2-R1", "F2-A1"], ["data/raw/mivau_parque.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_parque.csv", "campo": "ultima_fecha", "frec": "A"}),
    V("mivau_parque", "nacional", "A", ["F1-A2"], ["data/raw/mivau_parque.csv"],
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_parque.csv", "campo": "ultima_fecha", "frec": "A"}),
    # F1-F3 · modelos de conjunto
    V("renta_hog_real", "nacional", "T", ["F1-R1", "F1-A3"], anexo="2026T2"),
    V("renta_hog_real", "nacional", "A", ["F1-A2"], de="T", anexo="2025"),
    V("parados_epa", "provincia", "A", F1P),
    V("hogares_ecp_provincial", "provincia", "A", ["F2-R1", "F2-A1"], ["data/raw/ine_v2_hogares_prov.csv"], de="T",
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "ine_v2_hogares_prov.csv", "campo": "ultima_fecha", "frec": "T"}),
    V("costes_constr", "nacional", "A", ["F3-R1", "F3-A1", "F3-A2"], de="T", anexo="2025"),
    V("credito_promotor", "nacional", "A", ["F3-A1", "F3-A2"], de="T", anexo="2025"),
    V("mivau_v2_suelo", "provincia", "A", ["F3-A2"], ["data/raw/mivau_v2_suelo.csv"], de="T",
      meta={"tipo": "fecha", "ruta": RAW_RAIZ, "campo_clave": "archivo", "valor": "mivau_v2_suelo.csv", "campo": "ultima_fecha", "frec": "T"}),
    V("valor_tasado_ccaa", "ccaa", "A", ["F3-R1", "F3-A1"], de="T"),
]

# Datos que el plan descarga después de la etiqueta («posterior_prereg»): no están en el repositorio en el commit de la etiqueta.
POSTERIOR_PREREG = [
    ("censo2001_nacionalidad_provincia", ["E3-R1", "E3-R1q", "E3-R2", "E3-R2b", "E3-R2q", "E3-A1", "E3-A2", "E3-A4", "E3-A5", "E5-A1"],
     "cuotas del año base (INE, abierto)"),
    ("osm_atractivos_turisticos", ["E1-R2", "E1-A1"], "geometría sin dimensión temporal (OpenStreetMap, ODbL)"),
    ("google_trends_airbnb_barcelona", ["E1-R2"], "índice anual de búsquedas"),
    ("opendata_bcn_fianzas_barrio", E1R, "medida de alquiler alternativa (Incasòl por barrio)"),
    ("ss_afiliacion_provincial_cnae_2001", ["E5-R1", "E5-A1", "E5-A2", "F3-A3"], "cuotas sectoriales del Bartik"),
    ("atlas_areas_urbanas_mivau", ["E5-A2"], "unidad territorial sin dimensión temporal"),
    ("aemet_rachas_lluvia", ["E6-R2", "E6-A3"], "instrumento de Mense"),
    ("itp_fechas_entrada_en_vigor", ["E8-R1", "E8-R2", "E8-A1", "E8-A2"], "BOE y diarios oficiales"),
    ("itp_recaudacion_ccaa", ["E8-A1"], "liquidación de tributos cedidos (Hacienda)"),
    ("bce_tipos_cambio", ["E9-A1"], "tipos de cambio bilaterales frente al euro"),
    ("ine_cre_renta_hogares_provincial", F1P + ["F2-R1", "F2-A1"], "renta disponible bruta de los hogares por provincia"),
    ("ine_padron_edad_provincial", ["E3-R1", "E3-R2", "E3-R2b", "E3-R2q"], "población en edad de trabajar"),
    ("epa_hogares_provincial", ["F2-R1", "F2-A1"], "hogares por provincia antes de 2021"),
]

# Calendarios de tratamiento (fechas normativas, sin periodo de resultado): solo la regla (g) de ediciones.
CALENDARIOS = [
    ("data/raw/v3/cataluna_contencion_rentas_v3.csv", RAW_RAIZ, "archivo", "v3/cataluna_contencion_rentas_v3.csv", "descargado_utc",
     ["E2-R1", "E2-R1c", "E2-A3", "E2-A4"]),
    ("data/raw/v16/intervenciones/intervenciones.csv", "data/raw/v16/intervenciones/_manifest.csv", "fichero", "intervenciones/intervenciones.csv",
     "fecha_descarga", ["E8-R1", "E8-R2", "E8-A1", "E8-A2"]),
    ("data/raw/v16/intervenciones/zonas_tensionadas_v16_nuevas.csv", "data/raw/v16/intervenciones/_manifest.csv", "fichero",
     "zonas_tensionadas_v16_nuevas.csv", "fecha_descarga", ["E2-A2"]),
]

# Especificaciones de la tabla consolidada: (ids, estado, corte del Anexo C, «como»: especificaciones cuyas variables usa).
NE, P, DER = "NO ESTIMABLE", "coprincipal", "derivada"
ESPECIFICACIONES = [
    (E1R, "principal", "SERPAVI hasta 2024. HUT de Barcelona y noches de Eurostat por la regla (e), dentro de la ventana hasta 2024. "
                       "ADRH por sección hasta 2023. Población del censo anual hasta 2025", []),
    (["E1-A1"], "principal", "INE-VUT: clave mensual 2026-05, medias anuales hasta 2025. Ventana limitada por SERPAVI: 2021-2024", []),
    (["E1-A2", "E1-A3"], "principal / variante", "Registro de Andalucía por la regla (e). Registro reconstruido de la GVA hasta 2025-01", []),
    (["E1-A4", "E1-A5", "E1-X1"], NE, None, []),
    (["E1-P-H3"], P, None, ["E1-A1"]), (["E1-P-D2"], P, None, ["E1-R1"]), (["E1-P-Q2b"], P, None, ["E1-A2"]),
    (["E2-R1", "E2-R1c"], "principal", "Incasòl trimestral hasta 2026T1 (prueba de reversión hasta 2023T4) y anual hasta 2025 (robustez "
                                       "2014-2021). Paro del SEPE por la regla (e). HUT de IDESCAT hasta 2025", []),
    (["E2-R2", "E2-R2s", "E2-R2-X1", "E2-A5"], NE, None, []),
    (["E2-A1"], "principal (provisional)", "Incasòl hasta 2026T1. Zonas tensionadas vigentes hasta 2026T3", []),
    (["E2-A2"], "principal", "EMAL hasta 2025T4", []),
    (["E2-A3"], "principal", "Valor tasado municipal (p_tasado) trimestral hasta 2026T2. Compraventas municipales por la regla (f): hasta "
                             "2024-12. Ventana 2016-2022", []),
    (["E2-A4"], "principal", None, []),
    (["E2-P-D1b"], P, None, ["E2-R1"]), (["E2-P-D1b-c"], P, None, ["E2-R1c"]), (["E2-P-H1", "E2-P-H2"], P, None, ["E2-A1"]),
    (["E2-P-D1c"], P, None, ["E2-A2"]), (["E2-P-Q1c"], P, None, ["E2-A3"]),
    (["E3-R1", "E3-R1q", "E3-R2", "E3-R2b", "E3-R2q"], "principal", "Ventanas dentro de 1998-2010. Valor tasado provincial anual hasta 2024. "
                                                                    "Población provincial hasta 2024", []),
    (["E3-A1", "E3-A2", "E3-A3", "E3-A4"], "principal", "Padrón por nacionalidad provincial y municipal hasta 2022. ECP por nacionalidad, "
                                                        "por sustitución, hasta 2022. Ventanas 2014-2022", []),
    (["E3-A5"], "principal", "2002-2019", []),
    (["E3-P-D4"], P, None, ["E3-R1"]), (["E3-P-Q3c1"], P, None, ["E3-A1"]), (["E3-P-H4"], P, None, ["E3-A3"]),
    (["E4-X1"], NE, None, []), (["E4-X2"], "no se estima (Q7a)", None, []), (["E4-L1"], "solo literatura", None, []),
    (["E5-R1", "E5-A1", "E5-A2"], "principal", "Iniciadas y terminadas anuales hasta 2024. Valor tasado anual hasta 2024. Ventana 2002-2024", []),
    (["E5-R2"], NE, None, []),
    (["E5-A3"], "principal", "Obra nueva del Catastro hasta 2025. Valor tasado municipal: años completos hasta 2025", []),
    (["E5-P-Q4a"], P, None, ["E5-R1"]),
    (["E6-R1", "E6-A1"], "principal", "SERPAVI hasta 2024. Catastro INSPIRE hasta 2026-08-21", []),
    (["E6-R2", "E6-A3"], "principal", "IPVA hasta 2024. Terminadas trimestrales hasta 2026T2. IPC de alquiler provincial (ipc_alquiler_indice) "
                                      "hasta 2024 (A) y 2026T2 (T)", []),
    (["E6-A2"], NE, None, []),
    (E7N + ["E7-R3", "E7-A1", "E7-A2"], "principal", "Sorpresa monetaria hasta 2025-10 (trimestral hasta 2025T3). Tipo hipotecario, euríbor, "
                                                    "renta, crédito e inflación hasta 2026T2. Último origen con h = 8: 2024T2", []),
    (["E7-A3", "E7-A2-X1"], NE, None, []),
    (["E7-P-Q5", "E7-P-H8-5", "E7-P-H8-6", "E7-P-H8-7"], P, None, ["E7-R1", "E7-R2"]), (["E7-P-D5"], P, None, ["E7-A2"]),
    (["E8-R1"], "principal", "Valor tasado trimestral hasta 2026T2", []),
    (["E8-R2"], "principal", "Compraventas mensuales hasta 2024-12", []),
    (["E8-A1", "E8-A2"], "principal", None, []),
    (["E8-X1", "E8-X2"], NE, None, []),
    (["E8-P-Q6p"], P, None, ["E8-R1"]), (["E8-P-Q6v"], P, None, ["E8-R2"]),
    (["E9-R1", "E9-R2", "E9-A1", "E9-A2"], "principal", "Valor tasado hasta 2026T2. Cuota de no residentes del MIVAU por la regla (e)", []),
    (["E9-X1", "E9-X2", "E10-X1", "E11-X1", "E11-X2", "E12-X1"], NE, None, []),
    (["E10-A1"], "principal", "SERPAVI hasta 2024. Titularidad hasta 2026", []),
    (["E12-A1", "E12-A2"], "principal", "Obra libre anual hasta 2024. Protegida del MIVAU por la regla (e)", []),
    (["F1-R1", "F1-R2", "F1-R2-alt", "F1-R2-pmg", "F1-A1", "F1-A2", "F2-R1", "F2-A1", "F2-A2", "F3-R1", "F3-A1", "F3-A2", "F3-A3"], "principal",
     "Variables nacionales hasta 2026T2 (medias anuales hasta 2025). Provinciales: anuales hasta 2024", []),
    (["F1-A3"], "principal (no se publica sin cointegración)", None, ["F1-R1", "F1-A2", "F1-R2"]),
    (["F1-P-V72", "F1-P-M4"], P, None, ["F1-R1"]), (["F1-P-E1P2"], P, None, ["F1-A1"]),
    (["F4-1", "F4-2", "F4-3", "F4-4", "F4-5", "B5-*", "C5-*"], DER, None, []),
]
COMO_EXTRA = {"E5-A2": ["E5-R1"], "F3-A3": ["E5-R1"]}


# ------------------------------------------------------------------------------------------------------------- periodos
def frecuencia_de(p: str) -> str:
    for f, pat in PATRON.items():
        if re.match(pat, str(p)):
            return f
    raise ValueError(f"periodo no reconocido: {p!r}")


def fin(p: str) -> dt.date:
    """Último día del periodo."""
    f = frecuencia_de(p)
    if f == "A":
        return dt.date(int(p), 12, 31)
    if f == "T":
        y, q = int(p[:4]), int(p[5])
        return dt.date(y, 3 * q, calendar.monthrange(y, 3 * q)[1])
    if f == "M":
        y, m = int(p[:4]), int(p[5:7])
        return dt.date(y, m, calendar.monthrange(y, m)[1])
    return dt.date.fromisoformat(p)


def ultimo_hasta(fecha: dt.date, f: str) -> str:
    """Último periodo de frecuencia f que termina no después de `fecha` (periodo completo)."""
    if f == "D":
        return fecha.isoformat()
    if f == "A":
        return str(fecha.year if fecha >= dt.date(fecha.year, 12, 31) else fecha.year - 1)
    if f == "M":
        if fecha.day == calendar.monthrange(fecha.year, fecha.month)[1]:
            return f"{fecha.year}-{fecha.month:02d}"
        y, m = (fecha.year, fecha.month - 1) if fecha.month > 1 else (fecha.year - 1, 12)
        return f"{y}-{m:02d}"
    if f == "T":
        q = (fecha.month - 1) // 3 + 1
        if fecha >= fin(f"{fecha.year}T{q}"):
            return f"{fecha.year}T{q}"
        return f"{fecha.year}T{q - 1}" if q > 1 else f"{fecha.year - 1}T4"
    raise ValueError(f)


def periodo_en(fecha_inicio: dt.date, f: str) -> str:
    """Periodo de frecuencia f que contiene la fecha (las fechas de los manifiestos marcan el inicio del último periodo)."""
    if f == "A":
        return str(fecha_inicio.year)
    if f == "T":
        return f"{fecha_inicio.year}T{(fecha_inicio.month - 1) // 3 + 1}"
    if f == "M":
        return f"{fecha_inicio.year}-{fecha_inicio.month:02d}"
    return fecha_inicio.isoformat()


def menor(a: str, b: str) -> str:
    return a if fin(a) <= fin(b) else b


# ------------------------------------------------------------------------------------------------------------- fuentes
def _git_show(commit: str, ruta: str) -> str:
    r = subprocess.run(["git", "show", f"{commit}:{ruta}"], cwd=RAIZ, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{ruta} no está en el commit de la etiqueta ({commit[:7]})")
    return r.stdout


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def metadatos_base(variables: set[str]) -> dict[tuple[str, str, str], tuple[str, str]]:
    """{(variable, nivel, frecuencia): (primer periodo, último periodo)}: solo metadatos agregados, nunca valores."""
    import duckdb
    con = duckdb.connect()
    q = ("select variable, nivel, frecuencia, min(periodo), max(periodo) from read_parquet(?) "
         "where variable in (select unnest(?)) group by variable, nivel, frecuencia")
    return {(v, n, f): (a, b) for v, n, f, a, b in con.execute(q, [str(HECHOS), sorted(variables)]).fetchall()}


class Reglas:
    def __init__(self, m15: dict, m16: dict, base: dict, commit: str, fecha_etiqueta: str, sha_hechos: str):
        self.k15, self.k16 = m15["ultimo_periodo_visto"], m16["ultimo_periodo_visto"]
        self.base, self.commit, self.fecha_etiqueta, self.sha = base, commit, fecha_etiqueta, sha_hechos
        self.corte = min(m15["fecha_corte"], m16["fecha_corte"])
        self.conjuntos: dict[str, list[str]] = {}
        for k, v in m15.get("preguntas", {}).items():
            for x in v["variables"]:
                self.conjuntos.setdefault(x, []).append(f"V15:{k}")
        for k, v in m16.get("conjuntos", {}).items():
            for x in v["variables"]:
                self.conjuntos.setdefault(x, []).append(f"V16:{k}")
        self._csv: dict[str, list[dict]] = {}

    # claves de V15/V16 -------------------------------------------------------------------------------------------
    def clave(self, v: str, n: str, f: str) -> tuple[str, str] | None:
        k = f"{v}|{n}|{f}"
        a, b = self.k15.get(k), self.k16.get(k)
        if a is None and b is None:
            return None
        if a is not None and b is not None:
            t = menor(str(a), str(b))
            return t, f"sellado_v15.json = {a}; sellado_v16.json = {b} (manda la menor) [{k}]"
        return (str(a), f"sellado_v15.json = {a} [{k}]") if a is not None else (str(b), f"sellado_v16.json = {b} [{k}]")

    def claves_nivel(self, v: str, n: str) -> dict[str, tuple[str, str]]:
        fs = {k.split("|")[2] for k in list(self.k15) + list(self.k16) if k.split("|")[0] == v and k.split("|")[1] == n}
        return {f: self.clave(v, n, f) for f in sorted(fs)}

    # último periodo presente (regla e) ---------------------------------------------------------------------------
    def _filas(self, ruta: str) -> list[dict]:
        if ruta not in self._csv:
            self._csv[ruta] = list(csv.DictReader(io.StringIO(_git_show(self.commit, ruta))))
        return self._csv[ruta]

    def ultimo_presente(self, e: dict, f_fuente: str) -> tuple[str, str, str | None]:
        """(periodo, frecuencia, fuente) del último periodo presente en el repositorio en el commit de la etiqueta."""
        m = e["meta"]
        if m is None:
            for f in [f_fuente] + sorted({k[2] for k in self.base if k[:2] == (e["variable"], e["nivel"])}):
                if (e["variable"], e["nivel"], f) in self.base:
                    ult = self.base[(e["variable"], e["nivel"], f)][1]
                    return ult, f, f"{HECHOS_REL} (sha256 {self.sha[:12]}…): último periodo de base:{e['variable']}|{e['nivel']}|{f} = {ult}"
            raise RuntimeError(f"{e['variable']}|{e['nivel']}: sin clave, fuera de todo conjunto y sin metadatos en la base ni en data/raw")
        if m["tipo"] == "fijo":
            return m["periodo"], m["frec"], f"corte único declarado ({m['periodo']})"
        if m["tipo"] == "nombres":
            cortes = sorted(f"{a}T{b}" for r in self._filas(m["ruta"]) for a, b in re.findall(m["patron"], r.get(m["campo"], "")))
            if not cortes:
                raise RuntimeError(f"{m['ruta']}: sin cortes para {e['variable']}")
            return cortes[-1], "T", f"{m['ruta']} en {self.commit[:7]}: último corte {cortes[-1]} ({len(cortes)} cortes)"
        filas = [r for r in self._filas(m["ruta"]) if m["valor"] in r.get(m["campo_clave"], "")]
        if not filas:
            raise RuntimeError(f"{m['ruta']}: no figura {m['valor']}")
        fechas = sorted(r[m["campo"]][:10] for r in filas if r.get(m["campo"]))
        ultima = dt.date.fromisoformat(fechas[-1])
        fuente = f"{m['ruta']} en {self.commit[:7]}: {m['campo']} = {fechas[-1]} ({m['valor']})"
        if m["campo"] == "fecha_descarga":   # registro completo a la fecha de descarga: último periodo completo antes de ella
            return (ultima - dt.timedelta(days=1)).isoformat(), "D", fuente
        return periodo_en(ultima, m["frec"]), m["frec"], fuente

    # motor de reglas ---------------------------------------------------------------------------------------------
    def tope_fuente(self, e: dict, v: str, n: str, f: str) -> dict:
        """Tope de v|n en la frecuencia f por (a), (c), (d) o (e)."""
        ks = self.claves_nivel(v, n)
        if f in ks:
            t, fu = ks[f]
            return {"tope": t, "regla": "(a)", "fuente_clave": fu}
        if ks:
            p = min((t for t, _ in ks.values()), key=fin)
            return {"tope": ultimo_hasta(fin(p), f), "regla": "(c)",
                    "fuente_clave": "; ".join(fu for _, fu in ks.values()) + f" → final del periodo más antiguo: {fin(p).isoformat()}"}
        if v in self.conjuntos:
            return {"tope": None, "regla": "(d)", "fuente_clave": f"{v} figura en {', '.join(self.conjuntos[v])} sin clave en el nivel {n}: "
                                                                  "combinación sellada entera"}
        p, fp, fu = self.ultimo_presente(e, f)
        return {"tope": ultimo_hasta(fin(p), f) if fp != f or f == "D" else p, "regla": "(e)", "fuente_clave": fu}

    def calcular(self, e: dict) -> dict:
        v, n, f = e["variable"], e["nivel"], e["frecuencia"]
        vc = e["hereda"] or v
        if e["de"] and f == "A":
            src = self.tope_fuente(e, vc, n, e["de"])
            if src["tope"] is None:
                r = dict(src)
            else:
                completos = ultimo_hasta(fin(src["tope"]), "A")
                ka = self.clave(vc, n, "A")
                tope = menor(ka[0], completos) if ka else completos
                fu = f"años completos bajo la clave de origen {e['de']} ({src['regla']}: {src['fuente_clave']}) = {completos}"
                if ka:
                    fu += f"; clave anual {ka[1]}"
                r = {"tope": tope, "regla": f"(b) con {src['regla']}", "fuente_clave": fu}
        else:
            r = self.tope_fuente(e, vc, n, f)
        if e["hereda"]:
            r["regla"] = f"(f) {r['regla']}"
            r["fuente_clave"] = f"sustituto de {e['hereda']}|{n}: {r['fuente_clave']}"
        sellada = r["tope"] is None
        e_like = r["regla"].endswith("(e)") and not e["hereda"]
        out = {"variable": v, "nivel": n, "frecuencia": f, "tope": r["tope"], "sellada_entera": sellada, "regla": r["regla"],
               "fuente_clave": r["fuente_clave"], "origen": e["origen"], "media_desde": e["de"],
               "edicion_maxima": self.fecha_etiqueta if e_like else self.corte,
               "conjuntos_v15_v16": self.conjuntos.get(vc, []), "especificaciones": sorted(set(e["especificaciones"]))}
        notas = [e["nota"]] if e["nota"] else []
        if e["anexo_c"] is not None:
            out["anexo_c"] = e["anexo_c"]
            if sellada:
                notas.append(f"el Anexo C da {e['anexo_c']}, pero la regla literal sella la combinación entera: manda la regla")
            elif e["anexo_c"] != r["tope"]:
                if fin(e["anexo_c"]) < fin(r["tope"]):
                    notas.append(f"regla literal {r['regla']} = {r['tope']}; el Anexo C fija {e['anexo_c']}, más restrictivo: se aplica el del Anexo C")
                    out["tope"] = e["anexo_c"]
                    out["regla"] = f"{r['regla']} + Anexo C"
                else:
                    notas.append(f"el Anexo C da {e['anexo_c']}; la regla literal da {r['tope']}, más restrictiva: se aplica la regla")
            out["coincide_anexo_c"] = (e["anexo_c"] == r["tope"]) and not sellada   # regla literal frente al Anexo C
        if notas:
            out["nota"] = "; ".join(notas)
        return out


# ------------------------------------------------------------------------------------------------------------- unidades
def unidades_excluidas() -> dict:
    p6 = sorted(holdout.provincias_selladas_v6())
    c6 = sorted(holdout.ccaa_selladas_v6())
    m15, m16 = sorted(holdout.municipios_sellados_v15()), sorted(holdout.municipios_sellados_v16())
    d15, d16 = sorted(holdout.distritos_sellados_v15()), sorted(holdout.distritos_sellados_v16())
    sm = set(m15) | set(m16)
    con_dist = sorted({d[:5] for d in set(d15) | set(d16)} - sm - {x for x in sm if x[:2] in p6})
    por_prov: dict[str, int] = {}
    for x in sm:
        por_prov[x[:2]] = por_prov.get(x[:2], 0) + 1
    adenda_prov = {"08": 83, "25": 86, "43": 7, "17": 0, "46": 101, "03": 38, "12": 35, "29": 41, "41": 37, "48": 107, "20": 79, "01": 6}
    adenda_ciud = {"08019": (["0801906", "0801909"], ["0801908"]), "46250": (["4625004", "4625010", "4625016"], ["4625009", "4625019"]),
                   "41091": (["4109102", "4109111"], ["4109110"]), "29067": (["2906701", "2906708"], ["2906705"]),
                   "03014": (["0301402"], ["0301405"]), "48020": (["4802007"], ["4802008"])}
    ciud = {m: {"v15": sorted(d for d in d15 if d[:5] == m), "v16": sorted(d for d in d16 if d[:5] == m)} for m in adenda_ciud}
    regla6 = "toda unidad cuyo código empieza por una provincia v6 (2 primeros dígitos): holdout.excluir_sellados_v6"
    return {
        "ccaa": {"v6": {"unidades": c6, "origen": "holdout.ccaa_selladas_v6() (K8 de V16): sus totales autonómicos tampoco se usan"}},
        "provincia": {"v6": {"unidades": p6, "origen": "holdout.provincias_selladas_v6()"}},
        "municipio": {"v6": {"regla": regla6},
                      "v15": {"unidades": m15, "origen": "holdout.municipios_sellados_v15()"},
                      "v16": {"unidades": m16, "origen": "holdout.municipios_sellados_v16()"}},
        "distrito": {"v6": {"regla": regla6},
                     "v15": {"unidades": d15, "origen": "holdout.distritos_sellados_v15()"},
                     "v16": {"unidades": d16, "origen": "holdout.distritos_sellados_v16()"}},
        "seccion": {"v6": {"regla": regla6},
                    "v15": {"regla": "sección (10 dígitos) cuyo distrito (7 primeros) está en distrito.v15 (holdout.unidad_sellada_v15)"},
                    "v16": {"regla": "sección (10 dígitos) cuyo distrito (7 primeros) está en distrito.v16 (holdout.unidad_sellada_v16)"}},
        "partido_judicial": {"v6": {"regla": "PJ-pp-n hereda su provincia pp (holdout.unidad_sellada_v16)"}},
        "nacional": "no se sella espacialmente (plan 0.3); respeta el sellado temporal",
        "fuga_declarada": {
            "municipios_con_distritos_sellados": con_dist,
            "regla": "municipios con 5 distritos o más: nunca se sellan enteros; su agregado municipal queda en entrenamiento aunque contiene "
                     "distritos sellados (adenda 1.5). Cada diseño municipal lo declara y añade la variante sin estos municipios; no se "
                     "combinan en un modelo los datos por sección y los municipales de estas ciudades"},
        "resumen": {"ccaa_v6": len(c6), "provincias_v6": len(p6), "municipios_v15": len(m15), "municipios_v16": len(m16),
                    "distritos_v15": len(d15), "distritos_v16": len(d16), "municipios_con_distritos_sellados": len(con_dist)},
        "comprobacion_adenda_1_5": {
            "distritos_grandes_ciudades": ciud,
            "distritos_coinciden": all(ciud[m]["v15"] == a and ciud[m]["v16"] == b for m, (a, b) in adenda_ciud.items()),
            "municipios_sellados_por_provincia": {p: por_prov.get(p, 0) for p in sorted(adenda_prov)},
            "municipios_coinciden": all(por_prov.get(p, 0) == k for p, k in adenda_prov.items())},
        "no_aplicado": "Los distritos sellados en v3 (holdout.distritos_sellados_v3) no forman parte de las reglas de V18 (plan 0.3, adenda 1.5); "
                       "src/holdout.py los aparta de todo uso en v6 (distrito_sellado_v6). Si V18 debe excluirlos, lo decide el autor",
    }


# ------------------------------------------------------------------------------------------------------------- principal
def construir() -> dict:
    commit = etiqueta.commit_etiqueta()
    if not commit:
        raise SystemExit(f"f3_sellado V18: no existe la etiqueta {etiqueta.ETIQUETA}: el sellado se genera después de la etiqueta")
    r = subprocess.run(["git", "log", "-1", "--format=%cI", commit], cwd=RAIZ, capture_output=True, text=True)
    fecha_etq = r.stdout.strip()
    m15 = json.loads(MAN15.read_text(encoding="utf-8"))
    m16 = json.loads(MAN16.read_text(encoding="utf-8"))
    sha = _sha256(HECHOS)
    esperados = {m15["fuentes_sha256"].get(HECHOS_REL), m16["fuentes_sha256"].get(HECHOS_REL)}
    if esperados != {sha}:
        raise SystemExit(f"f3_sellado V18: {HECHOS_REL} (sha256 {sha[:12]}…) no es la base registrada en los manifiestos de V15/V16: "
                         "la regla (e) se refiere a la base en el commit de la etiqueta")
    nombres = {e["variable"] for e in VARIABLES} | {e["hereda"] for e in VARIABLES if e["hereda"]}
    reglas = Reglas(m15, m16, metadatos_base(nombres), commit, fecha_etq[:10], sha)

    topes: dict[str, dict] = {}
    for e in VARIABLES:
        k = f"{e['variable']}|{e['nivel']}|{e['frecuencia']}"
        if k in topes:
            raise RuntimeError(f"variable repetida en la tabla: {k}")
        topes[k] = reglas.calcular(e)

    prereg = {n: {"tope": None, "regla": "(e) + (g)", "especificaciones": sorted(s), "nota": d,
                  "fuente_clave": f"fuera del repositorio en el commit de la etiqueta ({commit[:7]}): se descarga después (`posterior_prereg`); "
                                  f"solo ediciones publicadas no después de {fecha_etq[:10]}; su tope se fija al descargar, sin mirar resultados"}
              for n, s, d in POSTERIOR_PREREG}

    cal = {}
    for ruta, man, campo_k, valor, campo, specs in CALENDARIOS:
        filas = [x for x in reglas._filas(man) if valor in x.get(campo_k, "")]
        ed = sorted(x[campo][:10] for x in filas if x.get(campo))[-1] if filas else None
        cal[ruta] = {"especificaciones": specs, "edicion": ed, "manifiesto": man, "regla": "(g)",
                     "edicion_valida": bool(ed) and ed <= reglas.corte}

    # especificaciones: variables propias más las de las que reproduce («como»)
    por_spec: dict[str, list[str]] = {}
    for k, t in topes.items():
        for s in t["especificaciones"]:
            por_spec.setdefault(s, []).append(k)
    pp_spec: dict[str, list[str]] = {}
    for n, t in prereg.items():
        for s in t["especificaciones"]:
            pp_spec.setdefault(s, []).append(n)
    specs: dict[str, dict] = {}
    for ids, estado, anexo, como in ESPECIFICACIONES:
        for i in ids:
            base_ids = [i] + como + COMO_EXTRA.get(i, [])
            vs = sorted({k for b in base_ids for k in por_spec.get(b, [])})
            specs[i] = {"estado": estado, "variables": vs, "posterior_prereg": sorted({n for b in base_ids for n in pp_spec.get(b, [])})}
            if como:
                specs[i]["como"] = como
            if anexo:
                specs[i]["corte_anexo_c"] = anexo
    huerfanas = sorted(set(por_spec) - set(specs)) + sorted(set(pp_spec) - set(specs))
    if huerfanas:
        raise RuntimeError(f"especificaciones sin fila en la tabla consolidada: {huerfanas}")
    sin_var = sorted(i for i, s in specs.items() if s["estado"] not in (NE, DER, "solo literatura", "no se estima (Q7a)") and not s["variables"] and not s["posterior_prereg"])
    if sin_var:
        raise RuntimeError(f"especificaciones estimables sin variables: {sin_var}")

    reglas_n: dict[str, int] = {}
    for t in topes.values():
        reglas_n[t["regla"]] = reglas_n.get(t["regla"], 0) + 1
    return {
        "version": "V18",
        "descripcion": "Topes de entrenamiento por variable|nivel|frecuencia (adenda 1.4, reglas a-g) y unidades excluidas (plan 0.3, adenda 1.5). "
                       "Generado por src/v18/f3_sellado.py solo con metadatos; lo usan src/v18/sellado.py (fase 4), sellar_v18 y evaluate_v18 (1.11).",
        "etiqueta": {"nombre": etiqueta.ETIQUETA, "commit": commit, "fecha": fecha_etq},
        "fecha_corte_v15_v16": reglas.corte,
        "fuentes": {"docs/v15/sellado_v15.json": _sha256(MAN15), "docs/v16/sellado_v16.json": _sha256(MAN16), HECHOS_REL: sha,
                    "manifiestos_data_raw": f"leídos en el commit de la etiqueta ({commit[:7]})"},
        "reglas": {"(a)": "clave «v|n|f» de sellado_v16.json; con clave también en V15, manda la menor",
                   "(b)": "media anual desde T o M: años no posteriores a la clave «v|n|A» y completos bajo la clave de la frecuencia de origen",
                   "(c)": "sin clave en la frecuencia usada: final del periodo más antiguo entre las claves del mismo nivel",
                   "(d)": "variable de un conjunto de V15/V16 sin clave en ese nivel: combinación sellada entera",
                   "(e)": "variable fuera de todo conjunto: último periodo presente en el repositorio en el commit de la etiqueta",
                   "(f)": "sustituto de la misma magnitud y nivel: hereda el tope de la variable con clave",
                   "(g)": f"ediciones: hasta {reglas.corte} con clave; hasta la fecha de la etiqueta en (e)",
                   "anexo_c": "si el Anexo C fija un corte más restrictivo que la regla literal, se aplica el del Anexo C (nunca el más permisivo)"},
        "resumen": {"n_variables": len(topes), "n_selladas_enteras": sum(t["sellada_entera"] for t in topes.values()),
                    "por_regla": dict(sorted(reglas_n.items())), "n_posterior_prereg": len(prereg),
                    "n_discrepancias_anexo_c": sum(1 for t in topes.values() if "anexo_c" in t and not t.get("coincide_anexo_c")),
                    "n_especificaciones": len(specs)},
        "topes": dict(sorted(topes.items())),
        "posterior_prereg": prereg,
        "calendarios": cal,
        "especificaciones": specs,
        "unidades_excluidas": unidades_excluidas(),
    }


def main() -> int:
    d = construir()
    texto = json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    SALIDA.write_text(texto, encoding="utf-8")
    r = d["resumen"]
    print(f"f3_sellado V18: {r['n_variables']} variables ({r['n_selladas_enteras']} selladas enteras), {r['n_posterior_prereg']} posteriores a la "
          f"etiqueta, {r['n_discrepancias_anexo_c']} discrepancias con el Anexo C → {SALIDA.relative_to(RAIZ)}")
    u = d["unidades_excluidas"]
    print(f"  unidades: {u['resumen']}; adenda 1.5: distritos {u['comprobacion_adenda_1_5']['distritos_coinciden']}, "
          f"municipios {u['comprobacion_adenda_1_5']['municipios_coinciden']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
