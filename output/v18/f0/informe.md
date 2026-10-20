# V18 · Fase 0 · Inventario de datos por estudio

Generado por `python3 src/v18/f0_inventario.py` (2026-10-20); no editar a mano. No estima nada y no lee datos: solo manifiestos, el diccionario de la base, los inventarios de V13, V16 y V17 y los nombres de los ficheros. La tabla completa está en `output/v18/f0/inventario.csv`. Los veredictos son preliminares: la fase 3 (plan de replicación) los fija antes de estimar.

## Comprobación de V17

- `docs/v17/referencias_bde.md`: existe
- `output/v17/lectura_bde`: existe
- `output/v17/auditoria/tabla_final.md`: existe
- `data/raw/v17`: existe
- `python3 src/v17/check_v17.py`: check_v17: 0 errores (código 0)

## Unidades selladas (v6) que se excluyen de toda estimación

- CCAA enteras: Aragón (02), Asturias (03), Illes Balears (04), Canarias (05), Madrid (13), Región de Murcia (14), Navarra (15), La Rioja (17).
- Provincias (11): Illes Balears (Palma) (07), Huesca (22), La Rioja (26), Madrid (28), Murcia (30), Navarra (31), Asturias (33), Las Palmas (35), Santa Cruz de Tenerife (38), Teruel (44), Zaragoza (50).
- Barcelona (08) NO está sellada; Madrid (28) está sellada. Paneles provinciales: 39 provincias sin Ceuta ni Melilla.
- Fuente: `holdout.provincias_selladas_v6()` y `holdout.CCAA_PROV` (cálculo con la semilla, sin abrir datos sellados).
- La nación no se sella espacialmente: los diseños solo nacionales (E7 nacional, F1 nacional) no pierden muestra.

## Resumen

| Estudio | Veredicto preliminar | Variables disponibles | Parciales | Faltan |
|---|---|---|---|---|
| E1 | replicable en parte | 5 | 5 | 4 |
| E2 | replicable en parte | 5 | 2 | 2 |
| E3 | replicable en parte | 8 | 2 | 0 |
| E4 | NO ESTIMABLE con los datos actuales | 2 | 2 | 1 |
| E5 | replicable en parte | 4 | 3 | 4 |
| E6 | replicable en parte | 2 | 1 | 2 |
| E7 | replicable en parte | 5 | 3 | 0 |
| E8 | replicable en parte | 3 | 1 | 2 |
| E9 | replicable en parte | 1 | 3 | 0 |
| E10 | NO ESTIMABLE con los datos actuales | 1 | 3 | 0 |
| E11 | NO ESTIMABLE con los datos actuales | 2 | 2 | 1 |
| E12 | NO ESTIMABLE con los datos actuales | 3 | 1 | 1 |
| F1 | replicable en parte | 6 | 2 | 0 |
| F2 | replicable en parte | 2 | 1 | 0 |
| F3 | replicable en parte | 3 | 3 | 0 |

## E1 · Vivienda turística (Garcia-López, Jofre-Monseny, Martínez-Mazza y Segú, 2020)

**Veredicto preliminar: replicable en parte.** Barcelona por barrio se puede rehacer con el registro HUT (2018-2026) y el alquiler SERPAVI por sección o el IPVA por distrito, pero el periodo original (anuncios de Airbnb 2012-2016) y los dos instrumentos (atractivos y búsquedas) no están en el repositorio; la ampliación a València, Málaga, Sevilla y Alicante tiene registros e INE-VUT, pero InsideAirbnb solo tiene instantáneas desde 2025-12.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [ampliación]; Madrid [ampliación]; siguen Alicante, Barcelona, Málaga, Sevilla, València.
- **Réplica:**
  - Viviendas de uso turístico (HUT) por barrio de Barcelona: **parcial** (data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz; base:bcn_hut_registro; data/manual/v11/bcn_hut_trimestral/*). Falta: las licencias dadas de baja antes de 2018 no constan; no reproduce el stock 2012-2016 del original.
  - Anuncios de Airbnb por barrio 2012-2016 (exposición del original): **falta**. Falta: histórico de InsideAirbnb (Archived Data Request, docs/v17/fuentes/turismo_local.md) o datos de AirDNA. Requiere al autor.
  - Alquiler por barrio o sección de Barcelona: **parcial** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz; base:ipva_indice). Falta: alquiler trimestral por barrio (Open Data BCN, «lloguer mitjà mensual per barri», de las fianzas de Incasòl; abierto, se descarga sin el autor).
  - Precio de compra por barrio de Barcelona: **falta**. Falta: Open Data BCN (precio de compraventa por barrio; por verificar la fuente y la licencia) o anuncios de portales.
  - Instrumento «dónde»: atractivos turísticos georreferenciados: **falta**. Falta: OpenStreetMap (tourism=attraction; ODbL) o inventario municipal de atractivos; geometría de secciones ya en data/raw/v10/geo/seccionado_2025.zip.
  - Instrumento «cuándo»: búsquedas en Google de Airbnb: **falta**. Falta: Google Trends (índice de búsquedas; condiciones de uso por verificar).
  - Geometría de secciones y barrios (distancias, caso Sagrada Família): **disponible** (data/raw/v10/geo/seccionado_2025.zip; data/raw/v3/cartografia/Cartografia_secc.zip).
  - Controles por sección (renta, población): **disponible** (base:adrh_renta_neta_persona; base:pob_censo_anual; data/raw/v16/renta_parque/_grandes/adrh/*).
- **Ampliación:**
  - Viviendas turísticas INE (experimental) por sección y distrito: **disponible** (base:ine_vut_vivienda_turistica; data/raw/v3/ine_v3_vut_seccion.csv.gz).
  - Registros autonómicos de vivienda turística con fecha de alta: **parcial** (base:vut_registro_gva_reconstruido; data/raw/v9/gva_vut/gva_vut_panel_municipio.csv; data/raw/v16/alquiler_turismo/_terceros/openrta_all_2026-10-17.csv.gz; base:reate_viviendas_uso_turistico; base:idescat_hut_n; data/raw/v9/cat_turisme/registre_turisme_agregat_municipi.csv.gz). Falta: altas con fecha de Cataluña (registre complet), Ibiza y Formentera; Madrid y Baleares están selladas. Requiere al autor.
  - InsideAirbnb por sección (9 áreas): **parcial** (base:iab_n_anuncios; data/raw/v9/insideairbnb/insideairbnb_seccion.csv.gz; data/raw/v17/turismo_local/insideairbnb/*). Falta: solo instantáneas desde 2025-12; el histórico requiere la Archived Data Request. Requiere al autor.
  - Alquiler por sección en las ciudades de la ampliación: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz).
  - Demanda turística (pernoctaciones y plataformas): **disponible** (base:eurostat_plataformas_noches; base:ine_tmov_receptor_turistas; data/raw/v9/eurostat_plataformas/*).
  - Regulaciones locales (PEUAT, moratorias) como tratamiento: **parcial** (data/raw/v16/intervenciones/intervenciones.csv; base:vut_regulacion_ccaa). Falta: geometría de las zonas del PEUAT y fechas de moratorias de otras ciudades (ayuntamientos). Requiere al autor.

## E2 · Topes al alquiler (Jofre-Monseny, Martínez-Mazza y Segú, 2023; Monràs y García-Montalvo, 2023)

**Veredicto preliminar: replicable en parte.** La réplica de Jofre-Monseny et al. es posible: Incasòl da renta y número de contratos por municipio y trimestre desde 2007, con tramos de renta, y la lista de municipios de la Ley 11/2020 está en el repositorio. Monràs y García-Montalvo necesitan anuncios (composición y tramo de precio del anuncio): NO ESTIMABLE sin microdatos de portales. El desplazamiento a temporada no tiene datos.

- **Sellado v6 (reduce la muestra):** se excluyen Navarra [ampliación (zonas 2024)]; Asturias [ampliación (zonas 2024)]; siguen Barcelona, A Coruña, Girona, Lleida, Tarragona, Bizkaia.
- **Réplica:**
  - Renta media y número de contratos por municipio (Cataluña): **disponible** (data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz; data/raw/v3/incasol_fianzas_municipio_v3.csv.gz).
  - Contratos por tramo de renta: **parcial** (data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz). Falta: tramos fijos en euros/mes, sin la renta anterior del contrato ni la superficie; microdatos de contratos del registro de fianzas (Agència de l'Habitatge de Catalunya). Requiere al autor.
  - Municipios y vigencia del tope (Ley 11/2020, STC 37/2022): **disponible** (data/raw/v3/cataluna_contencion_rentas_v3.csv; base:tope_rentas_ccaa; base:tope_rentas_ccaa_alt_v3).
  - Controles municipales (población, renta, paro): **disponible** (base:pob_total; base:aeat_irpf_renta_disponible_media; base:sepe_paro_registrado_media_anual).
  - Anuncios de alquiler 2019-2022 (Monràs y García-Montalvo): **falta**. Falta: microdatos de portales (Idealista, Fotocasa, Habitaclia): precio, superficie, ubicación y fechas. Requiere al autor.
- **Ampliación:**
  - Zonas tensionadas 2024 con fecha de efecto: **disponible** (base:zt_vigente; data/raw/v9/regulacion/zonas_tensionadas_v9.csv; data/raw/v16/intervenciones/zonas_tensionadas_v16_nuevas.csv).
  - Renta de contratos en otras CCAA con zonas (País Vasco): **parcial** (base:emal_renta_mensual_eur; data/raw/v9/emal/emal_largo.csv; base:ipva_indice; data/raw/v9/ine_ipva/ipva_provincia_antiguedad.csv). Falta: Navarra y Asturias están selladas; A Coruña solo tiene IPVA y SERPAVI anuales hasta 2024.
  - Contratos de temporada y por habitaciones: **falta**. Falta: fianzas por tipo de contrato o estadísticas del Registro Único de Arrendamientos (RD 1312/2024). Requiere al autor.
  - Desplazamiento a la venta (compraventas y valor tasado): **disponible** (base:compraventas; base:p_tasado; data/raw/mivau_transacciones_municipios.csv).

## E3 · Inmigración (González y Ortega, 2013; Saiz, 2007)

**Veredicto preliminar: replicable en parte.** Hay población por nacionalidad y provincia desde 2003, flujos nacionales por nacionalidad, valor tasado provincial desde 1995 y obra nueva provincial, pero las cuotas «históricas» del instrumento solo arrancan en 2003, dentro del periodo de la réplica (2001/2003-2008); el Censo de 2001 por nacionalidad y provincia (abierto) las daría. El alquiler (SERPAVI, IPVA) llega hasta 2024.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [réplica]; Madrid [réplica]; Murcia [réplica]; Las Palmas [réplica]; Santa Cruz de Tenerife [réplica]; siguen Alicante, Barcelona, Málaga.
- **Réplica:**
  - Población extranjera por nacionalidad y provincia: **disponible** (base:padron_pob_nacionalidad; data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz; base:ecp_pob_nacionalidad).
  - Cuotas históricas por nacionalidad (asentamientos previos): **parcial** (data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz; base:pob_extranjera). Falta: Censo de 2001 (o 1991) por nacionalidad y provincia: INE, descarga abierta.
  - Entradas nacionales por nacionalidad (choque, sin la propia provincia): **disponible** (data/raw/ine_migraciones_nacionalidad.csv; base:inmig_anual_eurostat; base:evr_inmigracion_exterior; data/raw/v9/ine_migraciones/ine_em_24323.csv.gz).
  - Precio de compra provincial: **disponible** (base:valor_tasado; base:ipv).
  - Obra nueva provincial: **disponible** (data/raw/mivau_v2_iniciadas_terminadas_prov.csv; base:iniciadas; base:terminadas).
  - Controles provinciales (PIB, empleo): **disponible** (data/raw/ine_v2_cre.csv; base:ocupados_epa; base:pib_miles_eur).
- **Ampliación:**
  - Alquiler provincial y municipal 2011-2024: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz; base:ipva_indice; data/raw/v9/ine_ipva/ipva_provincia_antiguedad.csv; base:ipc_alquiler_indice).
  - Población por nacionalidad en municipio y sección 2021-2025: **disponible** (data/raw/v9/ine_censo_anual/censo_seccion_pais.csv.gz; base:pob_censo_anual).
  - Tenencia por nacionalidad (compra frente a alquiler): **parcial** (data/raw/v11/ine_censo2021/*; data/raw/v11/ine_ecepov/*; data/raw/v11/ine_censos_microdatos/*). Falta: solo dos cortes censales; no hay serie anual de tenencia por nacionalidad.
  - Compras de extranjeros residentes: **disponible** (base:tx_extranj_ccaa; data/raw/mivau_transacciones_extranjeros.csv).

## E4 · Ayudas a la demanda (Fack, 2005-2006; Gibbons y Manning, 2006; Banque de France WP 886)

**Veredicto preliminar: NO ESTIMABLE con los datos actuales.** No hay microdatos de perceptores del Bono Alquiler Joven ni de ayudas autonómicas, ni convocatorias autonómicas con fecha. Lo único posible es una forma reducida débil por la edad de 35 años en la ECV (la edad no asigna el bono por sí sola). La magnitud preferida saldrá solo de la literatura, rotulada así.

- **Sellado v6:** la ECV identifica la CCAA de residencia: los hogares de las 8 CCAA selladas se excluyen de la forma reducida, lo que reduce los cerca de 2.200-2.500 hogares por ventana de Q7a de V16.
- **Réplica:**
  - Perceptores de ayudas al alquiler (edad, renta, municipio, fecha, importe): **falta**. Falta: microdatos de beneficiarios del Bono Alquiler Joven y de ayudas autonómicas (MIVAU y CCAA). Requiere al autor.
  - Alquiler pagado por hogares inquilinos por edad (ECV): **disponible** (data/raw/v9/ine_microdatos/ecv/*; data/raw/v16/renta_parque/*).
  - Calendario y requisitos de las ayudas: **parcial** (data/raw/v16/intervenciones/intervenciones.csv). Falta: convocatorias autonómicas (fechas de resolución, requisitos de renta y edad) y la Renta Básica de Emancipación 2008-2012 (BOE y diarios oficiales).
- **Ampliación:**
  - Gasto en alquiler por hogar (EPF): **disponible** (data/raw/v16/renta_parque/*).
  - Alquiler por sección para un diseño por intensidad territorial: **parcial** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz). Falta: perceptores por municipio o sección. Requiere al autor.

## E5 · Oferta y suelo (Saiz, 2010)

**Veredicto preliminar: replicable en parte.** Hay oferta (obra nueva neta del Catastro, iniciadas y terminadas), precios municipales y provinciales, solares y precio del suelo, pero faltan las restricciones del diseño de Saiz: pendiente (MDT05), agua y suelo no urbanizable, y planeamiento (SIU). La Red Natura no se usa como instrumento (falló en Q4). El Bartik de empleo es parcial (afiliación municipal desde 2011 con celdas suprimidas).

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [réplica]; Madrid [réplica]; siguen Barcelona, Málaga, València.
- **Réplica:**
  - Oferta: obra nueva y parque: **disponible** (base:obra_nueva_neta_catastro; base:obra_nueva_viviendas_inspire; data/raw/mivau_v2_iniciadas_terminadas_prov.csv).
  - Precio de compra municipal y provincial: **disponible** (base:p_tasado; base:valor_tasado).
  - Restricción física: pendiente (MDT05): **falta**. Falta: MDT05 del CNIG (centro de descargas con registro). Requiere al autor.
  - Restricción física: costa: **parcial** (data/raw/v10/geo/seccionado_2025.zip). Falta: línea de costa o DPMT del MITECO (dpmt.zip); hoy solo la geometría municipal. Requiere al autor.
  - Restricción física: agua y suelo no urbanizable: **falta**. Falta: CORINE Land Cover 2018 o SIOSE (cuenta en el CLMS). Requiere al autor.
  - Restricción de planeamiento (SIU): **falta**. Falta: Sistema de Información Urbana del MIVAU (suelo urbano y urbanizable por municipio). Requiere al autor.
  - Red Natura 2000 (solo control, no instrumento): **parcial** (data/raw/v16/oferta_suelo/_terceros/_grandes/n2000_2025_shp.zip). Falta: licencia por confirmar (en _terceros). Requiere al autor.
  - Suelo disponible y precio del suelo: **disponible** (data/raw/v4/catastro_solares_municipios.csv.gz; data/raw/mivau_v2_suelo.csv).
  - Bartik de empleo (cuotas sectoriales locales y crecimiento nacional por sector): **parcial** (base:ss_afiliados_cota_inferior; data/raw/v11/ss_afiliacion_municipio/*; data/raw/v17/oferta_capacidad/ine/ine_tabla_65123.json). Falta: afiliación por provincia y sección CNAE desde 2001 (Seguridad Social, abierta); celdas <5 suprimidas.
  - Unidad de análisis: áreas urbanas: **falta**. Falta: Atlas de las Áreas Urbanas del MIVAU (municipios por área urbana; abierto).
- **Ampliación:**
  - Choques de demanda de E3 para la interacción: **disponible** (data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz).

## E6 · Obra nueva y alquileres cercanos (literatura reciente; por localizar en la fase 1)

**Veredicto preliminar: replicable en parte.** El año de construcción por edificio con geometría (INSPIRE) solo está para unos 94 municipios, casi todos de la provincia de València; con SERPAVI por sección (anual, stock) cabe un piloto allí. Para el resto de España hace falta la descarga masiva del Catastro (o ampliar INSPIRE), y el alquiler a escala de anuncio o contrato no existe en el repositorio. Fuera de València: NO ESTIMABLE.

- **Sellado v6 (reduce la muestra):** se excluyen Madrid [ampliación]; siguen Barcelona, València.
- **Réplica:**
  - Edificios nuevos con fecha y geometría (por parcela): **parcial** (data/raw/v11/catastro_inspire/original/BU_*.zip; data/raw/v11/catastro_inspire/edificios_seccion.csv.gz; base:catastro_inspire_viviendas_por_antiguedad). Falta: resto de España: descarga masiva alfanumérica del Catastro (certificado electrónico) o INSPIRE Buildings por municipio (abierto). Requiere al autor.
  - Alquiler por sección: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz).
  - Alquiler por anuncio o contrato georreferenciado: **falta**. Falta: anuncios de portales o fianzas georreferenciadas (agencias autonómicas). Requiere al autor.
  - Controles por sección: **disponible** (base:adrh_renta_neta_persona; base:pob_censo_anual; data/raw/v16/renta_parque/_grandes/adrh/*).
- **Ampliación:**
  - Uso, superficie y fecha por inmueble en toda España: **falta**. Falta: descarga masiva alfanumérica del Catastro. Requiere al autor.

## E7 · Tipos de interés (Banco de España y BCE)

**Veredicto preliminar: replicable en parte.** A escala nacional todo está: sorpresas de Jarociński-Karadi (mensuales, CC BY), tipos hipotecarios, precios, compraventas, crédito y controles. El panel provincial con exposición no: el peso de la hipoteca variable solo es nacional y las compras sin hipoteca por provincia solo se aproximan (compraventas menos hipotecas).

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [panel]; Madrid [panel]; Murcia [panel]; siguen Barcelona.
- **Sellado v6:** las proyecciones locales y el SVAR nacionales no pierden muestra (la nación solo tiene sellado temporal).
- **Réplica:**
  - Sorpresas de política monetaria (instrumento externo): **disponible** (data/raw/v16/demanda_internacional/bce_sorpresas/*).
  - EA-MPD (robustez): **parcial** (data/raw/v16/demanda_internacional/_terceros/bce_sorpresas/*). Falta: licencia por decidir (en _terceros). Requiere al autor.
  - Tipos hipotecarios y Euríbor: **disponible** (base:tipo_hip_bde; base:tipo_hip_bce; base:euribor_1y).
  - Precios, alquiler y compraventas nacionales: **disponible** (base:p_tasado; base:ipv; base:compraventas; base:ipc_alquiler).
  - Crédito nuevo y controles macro: **disponible** (base:credito_nuevo; base:pib_vol_idx; base:inflacion_ipc_yoy; base:ocupados).
  - Peso de la hipoteca a tipo variable por provincia: **parcial** (base:bce_cuota_tipo_variable; data/raw/v16/demanda_internacional/bde_fijacion/*). Falta: desglose provincial (Registradores, Estadística Registral, no redistribuible; o Banco de España). Requiere al autor.
  - Compras sin hipoteca por provincia: **parcial** (data/raw/ine_v2_etdp_prov.csv; data/raw/ine_v2_hipotecas_prov.csv). Falta: solo aproximación (compraventas menos hipotecas); compras al contado del Notariado. Requiere al autor.
- **Ampliación:**
  - Precio, compraventas e hipotecas provinciales: **disponible** (base:valor_tasado; base:compraventas; base:hip_n).

## E8 · Fiscalidad de la compra (Best y Kleven, 2018; Besley et al., 2014)

**Veredicto preliminar: replicable en parte.** El DiD escalonado es posible con los cambios del tipo general del ITP (Hacienda, régimen común) y las compraventas de vivienda usada y el valor tasado provinciales, con fechas aproximadas y pocos clusters. El bunching no: no hay compraventas por tramo de precio. Faltan tipos reducidos y forales.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [CCAA de régimen común]; Madrid [CCAA de régimen común]; Murcia [CCAA de régimen común]; Las Palmas [CCAA de régimen común]; siguen Barcelona, Sevilla, València.
- **Réplica:**
  - Calendario de tipos de ITP y AJD por CCAA: **parcial** (data/raw/v16/intervenciones/intervenciones.csv). Falta: fechas exactas de las leyes (hoy casi todas a 1 de enero), tipos reducidos (jóvenes, familias, VPO) y tipos forales: leyes autonómicas en BOE y diarios oficiales.
  - Compraventas de vivienda usada por provincia: **disponible** (data/raw/ine_v2_etdp_prov.csv; base:compraventas).
  - Precio provincial: **disponible** (base:valor_tasado).
  - Compraventas por tramo de precio (bunching): **falta**. Falta: Notariado (CIEN) o Registradores por tramo, o AEAT (modelo 600) por tramo. Requiere al autor.
  - Recaudación del ITP por CCAA (primera etapa): **falta**. Falta: liquidación de tributos cedidos (Ministerio de Hacienda; abierta).
- **Ampliación:**
  - Compraventas municipales (municipios grandes): **disponible** (data/raw/mivau_transacciones_municipios.csv; base:trans_total).

## E9 · Compradores no residentes (Badarinza y Ramadorai, 2018; Cvijanović y Spaenjers, 2021)

**Veredicto preliminar: replicable en parte.** Hay compras por nacionalidad del comprador por CCAA (Notariado, semestral desde 2007) y por provincia sin serie larga (Registradores, anuario 2016-2025, no redistribuible), y la exposición se puede aproximar con el padrón de 2003 por nacionalidad. Faltan tipos de cambio y la serie provincial por nacionalidad. La golden visa (fin en 2025) tiene uno o dos semestres posteriores. Las provincias con más compra extranjera están en gran parte selladas.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [réplica]; Madrid [réplica]; Murcia [réplica]; Las Palmas [réplica]; Santa Cruz de Tenerife [réplica]; siguen Alicante, Barcelona, Girona, Málaga.
- **Réplica:**
  - Compras de vivienda por nacionalidad del comprador y territorio: **parcial** (data/raw/pdf/notariado_cgn_extranjeros_semestral.csv; data/raw/pdf/registradores_eri_anuario.csv; data/raw/pdf/notariado_cv_prov_trimestral.csv; data/raw/mivau_transacciones_residencia.csv). Falta: serie provincial por nacionalidad (Notariado, portal estadístico). Requiere al autor.
  - Exposición histórica por nacionalidad: **disponible** (data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz).
  - Choques en los países de origen (PIB, precios, tipo de cambio, riesgo): **parcial** (data/raw/eu_hpi.csv; data/raw/oecd_house_prices.csv; data/raw/eu_income_emp.csv). Falta: tipos de cambio bilaterales y primas de riesgo (BCE y bancos centrales; abiertos).
  - Fin de la golden visa (LO 1/2025): **parcial** (data/raw/v16/intervenciones/intervenciones.csv; data/raw/pdf/notariado_cgn_extranjeros_semestral.csv). Falta: autorizaciones de residencia por inversión (OPI); periodo posterior de uno o dos semestres. Requiere al autor.

## E10 · Grandes tenedores e inversores institucionales (literatura de EE. UU. y Europa)

**Veredicto preliminar: NO ESTIMABLE con los datos actuales.** No hay variación temporal de la titularidad por zona: la estadística catastral por tramo y tipo de titular solo tiene tres cortes (2024-2026) y la serie 2012-2023 tiene otra definición. Solo cabe una asociación transversal, con lo que dicen los datos parciales de V17.

- **Sellado v6 (reduce la muestra):** se excluyen Madrid [réplica]; siguen Barcelona.
- **Réplica:**
  - Entrada de grandes tenedores por zona y año (panel de titularidad): **parcial** (data/raw/v11/catastro_titularidad/p_spi_mun_v_tpf.csv.gz; base:v12_titularidad_pct_mas10; base:v12_titularidad_pct_pj; base:catastro_titulares_jaxi). Falta: serie homogénea por tramo de titular 2012-2026 (petición al Catastro). Requiere al autor.
  - Compras de personas jurídicas: **parcial** (data/raw/v16/demanda_internacional/ine_etdp_titular/*; data/raw/v4/ine_v4_t50256.csv). Falta: desglose provincial (Notariado). Requiere al autor.
  - Titularidad del parque de alquiler: **parcial** (data/raw/v17/titularidad/*). Falta: solo documentos (Barcelona, Ministerio); microdatos del Panel de Hogares AEAT-IEF. Requiere al autor.
  - Alquiler por sección y municipio: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz).

## E11 · Viviendas vacías (Segú, 2020)

**Veredicto preliminar: NO ESTIMABLE con los datos actuales.** Falta el tratamiento: la adopción municipal del recargo del IBI (Ley 12/2023) y el calendario del impuesto catalán no están en el repositorio, y la vacancia solo tiene dos cortes censales con métodos distintos (2011 y 2021, este por consumo eléctrico).

- **Sellado v6 (reduce la muestra):** se excluyen Madrid [réplica]; siguen Barcelona.
- **Réplica:**
  - Viviendas vacías, Censo 2021 (consumo eléctrico): **disponible** (data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv; data/raw/v11/ine_censo2021/*).
  - Viviendas vacías, Censo 2011: **parcial** (base:censo2011_viviendas; data/raw/v9/ine_censos/censo_t3457.csv.gz). Falta: vacías por municipio en 2011 (INE, abierto).
  - Vacancia anual por consumo eléctrico: **falta**. Falta: estadística experimental del INE de viviendas vacías por consumo (por verificar edición).
  - Recargo del IBI por municipio y año e impuesto catalán sobre vacías: **parcial** (data/raw/v16/intervenciones/intervenciones.csv). Falta: ordenanzas fiscales municipales (adopción y fecha del recargo) y Ley catalana 14/2015. Requiere al autor.
  - Alquiler por sección y municipio: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz).

## E12 · Vivienda pública (desplazamiento de la promoción privada)

**Veredicto preliminar: NO ESTIMABLE con los datos actuales.** No hay promociones públicas por municipio y año. Las calificaciones de vivienda protegida por provincia y año permiten solo una asociación provincial con la obra libre, sin variación exógena.

- **Sellado v6 (reduce la muestra):** se excluyen Madrid [réplica]; siguen Barcelona.
- **Réplica:**
  - Promociones públicas por municipio y año: **falta**. Falta: registros del MIVAU, CASA 47 (antes SEPES) y de las empresas públicas autonómicas. Requiere al autor.
  - Calificaciones de vivienda protegida: **disponible** (data/raw/mivau_v2_protegida.csv).
  - Obra privada (libre) iniciada y terminada: **disponible** (data/raw/mivau_v2_iniciadas_terminadas_prov.csv).
  - Precios del entorno: **disponible** (base:p_tasado; base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz).
- **Ampliación:**
  - Parque social y gasto público: **parcial** (data/raw/v17/parque_social/*). Falta: solo agregados nacionales y por CCAA en PDF.

## F1 · Precio de largo plazo con corrección de error (nacional y panel provincial)

**Veredicto preliminar: replicable en parte.** Nacional, completo desde 1995-1999. Panel provincial: falta la renta disponible de los hogares por provincia (INE, Contabilidad Regional, abierta) y los hogares provinciales antes de 2021; hoy solo PIB provincial, IRPF desde 2016 y ADRH desde 2015.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [panel]; Madrid [panel]; Murcia [panel]; el panel sigue con las 39 provincias no selladas.
- **Réplica:**
  - Precio real de compra: **disponible** (base:p_tasado; base:valor_tasado; base:deflactor).
  - Renta disponible real de los hogares (nacional): **disponible** (base:renta_hog_real).
  - Renta disponible de los hogares por provincia: **parcial** (data/raw/ine_v2_cre.csv; base:aeat_irpf_renta_disponible_media; base:adrh_renta_neta_hogar). Falta: renta disponible bruta de los hogares por provincia (INE, Contabilidad Regional; abierta).
  - Tipo hipotecario real: **disponible** (base:tipo_hip_real_bde).
  - Población y hogares: **parcial** (base:pob_total; base:hogares_epa; data/raw/ine_v2_hogares_prov.csv). Falta: hogares por provincia antes de 2021 (EPA por provincia; INE, abierta).
  - Parque de viviendas por hogar: **disponible** (data/raw/mivau_parque.csv).
  - Indicador de sobrevaloración del Banco de España (comparación): **disponible** (data/raw/v17/credito/bde_si_1_5.csv; docs/v17/referencias_bde.md).
- **Ampliación:**
  - Paneles provinciales ya construidos: **disponible** (data/processed/v7/panel_prov_q_v7.csv; data/processed/v8/cv_prov_q_v8.csv).

## F2 · Alquiler equivalente por provincia

**Veredicto preliminar: replicable en parte.** El alquiler provincial existe (SERPAVI e IPVA 2011-2024 en niveles e índices; IPC de alquiler desde 2002 solo como índice), pero la serie en niveles es corta (14 años) y comparte con F1 la falta de renta de los hogares provincial.

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [panel]; Madrid [panel]; el panel sigue con las 39 provincias no selladas.
- **Réplica:**
  - Alquiler real por provincia: **disponible** (base:serpavi_alquiler_m2_mediana; data/raw/v3/serpavi_secciones_nacional_v3.csv.gz; base:ipva_indice; data/raw/v9/ine_ipva/ipva_provincia_antiguedad.csv; base:ipc_alquiler_indice).
  - Renta de los hogares por provincia: **parcial** (data/raw/ine_v2_cre.csv). Falta: ver F1.
  - Hogares, parque y tipos: **disponible** (data/raw/mivau_parque.csv; base:pob_total; base:tipo_hip_real_bde).

## F3 · Elasticidad de la oferta y del parque por provincia

**Veredicto preliminar: replicable en parte.** Iniciadas y terminadas por provincia desde 1991 y precio provincial desde 1995; los costes de construcción solo son nacionales (salvo el precio del suelo provincial) y los visados no tienen desglose provincial; las restricciones son las de E5 (parciales).

- **Sellado v6 (reduce la muestra):** se excluyen Illes Balears (Palma) [panel]; Madrid [panel]; el panel sigue con las 39 provincias no selladas.
- **Réplica:**
  - Iniciadas y terminadas por provincia: **disponible** (data/raw/mivau_v2_iniciadas_terminadas_prov.csv; base:iniciadas).
  - Precio provincial: **disponible** (base:valor_tasado).
  - Costes de construcción: **parcial** (base:costes_constr; data/raw/v17/oferta_capacidad/ine/ine_tabla_8381.json; data/raw/mivau_v2_suelo.csv). Falta: costes con variación provincial (no hay serie oficial).
  - Visados por provincia: **parcial** (base:visados). Falta: desglose provincial (MIVAU o CSCAE; abierto).
  - Restricciones físicas y de planeamiento: **parcial** (data/raw/v4/catastro_solares_municipios.csv.gz). Falta: las de E5: MDT05, agua, SIU. Requiere al autor.
  - Crédito a promotores: **disponible** (base:credito_promotor).

## Lo que falta y no requiere al autor (fuentes abiertas, para descargar en la fase 1 o antes de la 4)

- E1 · Viviendas de uso turístico (HUT) por barrio de Barcelona: las licencias dadas de baja antes de 2018 no constan; no reproduce el stock 2012-2016 del original.
- E1 · Alquiler por barrio o sección de Barcelona: alquiler trimestral por barrio (Open Data BCN, «lloguer mitjà mensual per barri», de las fianzas de Incasòl; abierto, se descarga sin el autor).
- E1 · Precio de compra por barrio de Barcelona: Open Data BCN (precio de compraventa por barrio; por verificar la fuente y la licencia) o anuncios de portales.
- E1 · Instrumento «dónde»: atractivos turísticos georreferenciados: OpenStreetMap (tourism=attraction; ODbL) o inventario municipal de atractivos; geometría de secciones ya en data/raw/v10/geo/seccionado_2025.zip.
- E1 · Instrumento «cuándo»: búsquedas en Google de Airbnb: Google Trends (índice de búsquedas; condiciones de uso por verificar).
- E2 · Renta de contratos en otras CCAA con zonas (País Vasco): Navarra y Asturias están selladas; A Coruña solo tiene IPVA y SERPAVI anuales hasta 2024.
- E3 · Cuotas históricas por nacionalidad (asentamientos previos): Censo de 2001 (o 1991) por nacionalidad y provincia: INE, descarga abierta.
- E3 · Tenencia por nacionalidad (compra frente a alquiler): solo dos cortes censales; no hay serie anual de tenencia por nacionalidad.
- E4 · Calendario y requisitos de las ayudas: convocatorias autonómicas (fechas de resolución, requisitos de renta y edad) y la Renta Básica de Emancipación 2008-2012 (BOE y diarios oficiales).
- E5 · Bartik de empleo (cuotas sectoriales locales y crecimiento nacional por sector): afiliación por provincia y sección CNAE desde 2001 (Seguridad Social, abierta); celdas <5 suprimidas.
- E5 · Unidad de análisis: áreas urbanas: Atlas de las Áreas Urbanas del MIVAU (municipios por área urbana; abierto).
- E8 · Calendario de tipos de ITP y AJD por CCAA: fechas exactas de las leyes (hoy casi todas a 1 de enero), tipos reducidos (jóvenes, familias, VPO) y tipos forales: leyes autonómicas en BOE y diarios oficiales.
- E8 · Recaudación del ITP por CCAA (primera etapa): liquidación de tributos cedidos (Ministerio de Hacienda; abierta).
- E9 · Choques en los países de origen (PIB, precios, tipo de cambio, riesgo): tipos de cambio bilaterales y primas de riesgo (BCE y bancos centrales; abiertos).
- E11 · Viviendas vacías, Censo 2011: vacías por municipio en 2011 (INE, abierto).
- E11 · Vacancia anual por consumo eléctrico: estadística experimental del INE de viviendas vacías por consumo (por verificar edición).
- E12 · Parque social y gasto público: solo agregados nacionales y por CCAA en PDF.
- F1 · Renta disponible de los hogares por provincia: renta disponible bruta de los hogares por provincia (INE, Contabilidad Regional; abierta).
- F1 · Población y hogares: hogares por provincia antes de 2021 (EPA por provincia; INE, abierta).
- F2 · Renta de los hogares por provincia: ver F1.
- F3 · Costes de construcción: costes con variación provincial (no hay serie oficial).
- F3 · Visados por provincia: desglose provincial (MIVAU o CSCAE; abierto).

Lo que requiere al autor está en docs/v18/tareas_autor.md, sección «V18 · fase 0» (estudios afectados: E1, E2, E4, E5, E6, E7, E8, E9, E10, E11, E12, F3).

## F4 · Coherencia

No necesita datos propios: compara en signo y orden de magnitud las elasticidades de F1-F3 con las de la sección E. Depende de que E3, E5, E7 y F1-F3 lleguen a estimarse.
