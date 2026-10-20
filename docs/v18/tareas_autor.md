# V18 (incluye V17) · Tareas del autor

No paran el trabajo: se anotan y se sigue con lo demás.

## V18 · fase 0 (2026-10-20)
Del inventario de datos por estudio (output/v18/f0/inventario.csv e informe.md; filas con requiere_autor = sí). Por orden de valor para la sección E del plan. Lo que se puede descargar sin ti (Censo 2001 por nacionalidad, renta de los hogares por provincia, alquiler por barrio de Open Data BCN, tipos de cambio, afiliación por sector, etc.) está en el informe y no va aquí.

1. **Descarga masiva alfanumérica del Catastro.**
   - Desbloquea: E6 fuera de la provincia de València (hoy solo hay INSPIRE de unos 94 municipios); E5 y F3 (parque por año, uso y superficie); E10 (unidades por titular, si la descarga lo incluye).
   - Fuente: Sede Electrónica del Catastro (https://www.sedecatastro.gob.es/), descarga masiva de datos no protegidos.
   - Cómo: identificarse con certificado electrónico y solicitar la descarga por provincias; guardar en data/raw/v18/catastro_masivo/ (fuera de git por tamaño, con sha256). Paso ya descrito en docs/v16/fuentes/renta_parque.md (ficha 6).
2. **Microdatos de portales de anuncios (alquiler y venta).**
   - Desbloquea: E2, la parte de Monràs y García-Montalvo (hoy NO ESTIMABLE: composición y tramo de precio del anuncio); E1 (precio por barrio de Barcelona); E6 (alquiler por anuncio cerca de edificios nuevos).
   - Fuente: Idealista, Fotocasa o Habitaclia (precio, superficie, coordenadas o sección, fecha de alta y baja; 2016-2026).
   - Cómo: pedir un convenio de datos para investigación al portal. Solo se publican agregados propios; los microdatos no se redistribuyen.
3. **Microdatos de beneficiarios de ayudas al alquiler.**
   - Desbloquea: E4 (hoy NO ESTIMABLE; sin ellos, la magnitud preferida sale solo de la literatura).
   - Fuente: MIVAU (Bono Alquiler Joven, RD 42/2022) y consejerías de vivienda de las CCAA no selladas (ayudas propias y Renta Básica de Emancipación 2008-2012 si se conserva).
   - Cómo: solicitud por el Portal de Transparencia (Ley 19/2013) o convenio con anonimización: edad, tramo de renta, municipio, fecha de solicitud y de concesión, importe y alquiler declarado.
4. **Registros de contratos de alquiler por tramo y con la renta anterior.**
   - Desbloquea: E2 (análisis por tramo de renta y desplazamiento a temporada), E1 y E3 (alquiler de nuevos contratos fuera de Cataluña).
   - Fuente: Agència de l'Habitatge de Catalunya (microdatos de fianzas de Incasòl con renta anterior y superficie); registros de fianzas de la C. Valenciana, Andalucía y País Vasco (detalle por contrato y por tipo: temporada, habitación); estadísticas del Registro Único de Arrendamientos (RD 1312/2024).
   - Cómo: solicitud a cada agencia autonómica (Portal de Transparencia autonómico) y, para el Registro Único, al MIVAU y al Colegio de Registradores. Amplía el punto 7 de la §3 de docs/v16/tareas_autor.md.
5. **SIU y restricciones físicas (MDT05, agua, costa).**
   - Desbloquea: E5 (elasticidad tipo Saiz) y F3. Sin ellos, la réplica de Saiz no tiene sus restricciones y no se usa la Red Natura como instrumento.
   - Fuente: Sistema de Información Urbana del MIVAU (suelo urbano y urbanizable por municipio); MDT05 del CNIG; CORINE 2018 o SIOSE (CLMS); DPMT del MITECO.
   - Cómo: descarga del SIU desde su visor o petición al MIVAU; registro en el centro de descargas del CNIG; cuenta en el CLMS. Ya en la §3, punto 3, de docs/v16/tareas_autor.md.
6. **Microdatos de la EFF (Encuesta Financiera de las Familias).**
   - Desbloquea: E7 (exposición por hipoteca a tipo variable y compras sin hipoteca por tipo de hogar), E10 (hogares con varias viviendas y rentas de alquiler) y F1 (riqueza y endeudamiento).
   - Fuente: Banco de España, BELab.
   - Cómo: solicitud de acceso a BELab con la descripción del proyecto. Ya en la §3, punto 5, de docs/v16/tareas_autor.md.
7. **Notariado: compras por nacionalidad, al contado, por persona jurídica y por tramo de precio, por provincia.**
   - Desbloquea: E9 (exposición y compras por nacionalidad por provincia; hoy solo CCAA), E7 (compras sin hipoteca por provincia), E8 (bunching en umbrales del ITP) y E10 (compras de personas jurídicas por provincia).
   - Fuente: Portal Estadístico del Notariado (penotariado.com) o Consejo General del Notariado.
   - Cómo: exportación manual o autorización del Consejo (las condiciones del portal no permiten extracción automática). Amplía el punto 1 de la sección V17 de este fichero.
8. **Registradores: uso de las tablas de la Estadística Registral.**
   - Desbloquea: E7 (tipo de interés y peso del tipo variable por CCAA) y E9 (compras por nacionalidad por provincia, 2016-2025).
   - Fuente: Colegio de Registradores (ERI trimestral y anuario; ya en data/raw/pdf y data/raw/v17/credito/_terceros).
   - Cómo: pedir autorización para usar y citar agregados propios (el aviso legal prohíbe reproducir); sin ella solo se usan para contraste, no en estimaciones publicables.
9. **Catastro: serie homogénea de titularidad por tramo 2012-2026.**
   - Desbloquea: E10 (hoy NO ESTIMABLE: tres cortes 2024-2026 y una serie anterior con otra definición).
   - Fuente: Dirección General del Catastro.
   - Cómo: solicitud por el Portal de Transparencia de viviendas por tramo de número de inmuebles del titular y tipo de persona, por municipio y año. Complementa el punto 3 de la sección V17.
10. **Panel de Hogares AEAT-IEF.**
    - Desbloquea: E10 (multiarrendadores y concentración del alquiler).
    - Fuente: Instituto de Estudios Fiscales. Cómo: solicitud de acceso a microdatos (docs/v17/fuentes/titularidad.md).
11. **Promociones de vivienda pública por municipio y año.**
    - Desbloquea: E12 (hoy NO ESTIMABLE).
    - Fuente: MIVAU (Observatorio de Vivienda y Suelo), CASA 47 (antes SEPES) y empresas públicas autonómicas.
    - Cómo: solicitud por transparencia de promociones con municipio, número de viviendas, régimen y fechas de inicio y entrega.
12. **Recargo del IBI sobre viviendas vacías por municipio.**
    - Desbloquea: E11 (hoy NO ESTIMABLE: falta el calendario de tratamiento).
    - Fuente: ordenanzas fiscales municipales (diputaciones, FEMP) o Ministerio de Hacienda (coordinación con las entidades locales); para Cataluña, la Agència Tributària de Catalunya (impuesto sobre viviendas vacías, Ley 14/2015).
    - Cómo: petición por transparencia de la lista de municipios que aplican el recargo, con el año de entrada en vigor.
13. **Geometría de las zonas del PEUAT y fechas de moratorias locales.**
    - Desbloquea: E1 (regulaciones locales como diferencias en diferencias). Fuente: Ajuntament de Barcelona y ayuntamientos de la ampliación. Cómo: confirmar si Open Data BCN publica las zonas; si no, pedirlas.
14. **Ya anotadas y que V18 también necesita:** InsideAirbnb anterior a 2025-12 (E1; punto 6 de la sección V17), autorizaciones de golden visa de la OPI (E9; §3, punto 2, de docs/v16/tareas_autor.md) y las licencias de EA-MPD (E7) y de la Red Natura (E5) (§3, puntos 4 y 8, de docs/v16/tareas_autor.md).

## V17 · Fase 1 (datos)
1. **Notariado (Penotariado).** Compras al contado, compras de personas jurídicas y compras por nacionalidad.
   - No hay fichero ni API.
   - Las condiciones del portal no permiten extraer los gráficos de forma automática.
   - Hay que exportarlo a mano o pedir autorización al Consejo General del Notariado (docs/v17/fuentes/credito.md).
2. **SERPAVI.** El portal del MIVAU bloquea a los clientes automáticos: descargar a mano la última edición por sección y municipio en data/raw/v17/serpavi/.
3. **Catastro por transparencia (más de diez viviendas).** El 4,3 % del parque total (1.046.188 inmuebles) solo consta en prensa. Hay que localizar la resolución original (Portal de Transparencia o Consejo de Transparencia), o pedírsela al medio. Con los datos de V11 se reproduce un 4,30 % en 2025.
4. **«15 % de la oferta de alquiler en grandes propietarios» (Ministerio).** No se ha encontrado el documento: indicar cuál es.
5. **Condiciones de uso de la OCDE (Affordable Housing Database).** Devolvieron HTTP 403: confirmarlas en el navegador antes de redistribuir los xlsx de data/raw/v17/parque_social/.
6. **InsideAirbnb.** Ediciones de 2019-2020: enviar una «Archived Data Request». Se descargó la edición de septiembre de 2026 de 9 áreas; queda fuera de git porque su política pide no republicar los datos (solo agregados propios).
7. **Plazos de licencias.** No hay serie oficial; solo hay una nota de prensa de EY-ASPRIMA (2020, 12 meses de media). Decidir si se piden a los ayuntamientos o a ASPRIMA.
