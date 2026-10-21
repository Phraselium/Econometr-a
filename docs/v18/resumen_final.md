# V18 · Resumen final (2026-10-21)

Documento de Trabajo: publicacion/documento_v18/ (documento_v18.md y tablas_v18.xlsx). Todas las cifras V18 son capa C4; la clase V18 va al lado (K2). Pre-registro interno: plan_replicacion.md + adenda, etiqueta plan-replicacion-v18 (ad4385c). `make check` limpio.

**Tabla de impactos.** Ningún factor tiene una estimación propia IDENTIFICADO.
- Topes al alquiler (Ley 11/2020): −0,038 en log de la renta de los contratos nuevos del Incasòl, **SUGESTIVO**, con frase de limitación obligatoria: la diferencia es máxima en 2021T1, se apaga antes de la STC 37/2022 y baja a −0,023 con trayectorias por tamaño; no se separa de un choque de la COVID ni de un cambio de composición. Sin magnitud preferida: la combinación con la literatura no es robusta a la prior (I² 0,95).
- ITP: ASOCIACIÓN (cambia de signo sin 2012-2013; fechas sin contrastar con el BOE).
- Inmigración y Sagrada Família: NO CONCLUYENTE (sin potencia).
- Turismo, ayudas y obra nueva: magnitud solo de la literatura. Oferta, tipos y no residentes: NO ESTIMABLE (instrumentos débiles o pocos choques). Grandes tenedores, vacías y vivienda pública: ASOCIACIÓN o NO ESTIMABLE por falta de datos.
- Modelos de conjunto: sin cointegración tras Holm; F1 no predice mejor que el AR(4).

**Contabilidad de la subida.** Con la regla restrictiva (K10), ninguna magnitud propia entra: en los cinco periodos (1995-2007, 2008-2013, 2014-2019, 2020-2022, 2022-2026), a escala nacional, por comunidades no selladas y en Barcelona, el 100 % de la variación queda «no explicado». La ilustración con magnitudes de la literatura va aparte y no es una atribución. Es compatible con V8 (ningún factor designable) y con el Banco de España.

**Estudios.** Reproducidos con su paquete y coincidentes: Chaves-Fonseca (2026), Mense (2025) y Borusyak-Hull-Jaravel (2022). Replicados con nuestros datos: Jofre-Monseny et al. (SUGESTIVO), González y Ortega (NO CONCLUYENTE), Garcia-López et al. (ASOCIACIÓN o NO ESTIMABLE), Mense en España (NO ESTIMABLE) y los demás según la tabla. 181 fichas bibliográficas; 15 herramientas validadas por Monte Carlo (6 NO APTAS); réplica ciega y dos rondas del abogado del diablo en cada estimación clasificada por encima de ASOCIACIÓN.

**Cambios en las tablas de V17.** Ninguno en los veredictos de medidas ni de discurso: V18 no aporta una estimación que los cambie. Matiz en topes: la diferencia de la renta se apaga dentro de la vigencia.

**Pendiente del autor** (docs/v18/tareas_autor.md):
- Subir la etiqueta plan-replicacion-v18 desde tu ordenador (el proxy no la deja subir).
- Confirmar las dos filas añadidas a docs/v16/escrituras_autorizadas.csv (cifras_clave).
- Datos que harían estimable lo que no lo es: descarga masiva del Catastro, clave de AEMET, histórico de InsideAirbnb, fianzas por barrio y por tramo, perceptores de ayudas, anuncios de portales, SIU, cuartiles de Scimago.
- `make base` si quieres data/base/vivienda.duckdb en disco (K13).
- evaluate_v18 (vía a C3) no antes de 2027, con tu orden.

Tokens de subagentes: F0 0,26 M; F1 1,63 M; F2 0,18 M; F3 0,99 M; F4 4,73 M; F5 0,35 M; F6 2,38 M; total ≈ 10,5 M (ninguna fase supera 6 M).
