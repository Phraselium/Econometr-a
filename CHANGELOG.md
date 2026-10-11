# Registro de cambios

Formato: versión, fecha y cambios principales. Las correcciones de resultados ya publicados van en ERRATA.md.

## v6.0 (2026-10-11)

Alquiler y compraventa: qué explica y qué predice (módulos M0-M4; decisiones en docs/v6/decisiones.md). Todo es C4; ninguna cifra existente cambia de valor ni de capa.

Cifras nuevas en output/v5/cifras_clave.csv:
- Leídas de output/v6/*/hechos.json: `M0-*` (paneles y sellado), `m1a_*` (asociaciones con el alquiler de stock en €/mes), `m1b_*` (elasticidad precio-alquiler, ratio precio/alquiler, rentabilidad bruta y coste de uso, GSADF por CCAA, Durbin espacial), `m2_pip_*` (PIP del BMA por mercado), `m3a_*` y `m3b_*` (validación interna) y `V6-M4-*` (error sellado del mejor modelo y de la persistencia, variables «relevantes con seguridad»).
- Auxiliares nuevas en `src/v5/e_hechos_v6.py` (ids `E-V6-`): provincias selladas y de entrenamiento, PIP del BMA núcleo, deep learning frente a gradient boosting (M3a y M3b), persistencia en la validación interna trimestral, parte temporal sellada del volumen trimestral, recuentos de confirmatorias que pasan Holm y de CCAA con exuberancia GSADF.

Capas: todos los resultados v6 son C4 (predicción y asociación). Ninguna hipótesis confirmatoria pasa Holm (`E-V6-M1A-HOLM`, `E-V6-M1B-HOLM`); ninguna variable es «relevante con seguridad» (`V6-M4-N-REL`); la identificación disponible no alcanza C3. Validación sellada espacial nueva (11 provincias) y temporal ya vista en v2 y de forma descriptiva en v4-v5.

Entregables:
- informe_tecnico: sección nueva 11, «Alquiler y compraventa: qué explica y qué predice (v6)» (medidas, validación sellada y su limitación, mejor modelo por mercado, medida y nivel, peso de cada variable con las discrepancias M2/M4, relación entre mercados, diferencias provinciales y resultados negativos); punto nuevo en 10.1.
- working_paper: subsecciones 4.5 (resultados) y 5.5 (validación sellada y negativos).
- lo_que_sabemos: tres ítems v6 en «Probable pero no demostrado (C4)» y dos en «No se puede afirmar». «Afirmable con seguridad» no cambia (solo C1 y C2).
- policy_brief: párrafo «Alquiler y compraventa: qué predice y qué no (v6)» y punto en «Lo que este brief no afirma».
- una_pagina: línea nueva en «Lo que NO se puede afirmar».
- `src/v5/render.py`: los recuentos en «variables», «hipótesis» y «CCAA» se muestran como enteros.

Auditoría del repositorio para su publicación (módulo G, 2026-10-11; detalle en docs/v6/auditoria.md):
- README.md principal y docs/MAPA.md (vigente frente a histórico).
- Salidas superadas de v3 y v4 trasladadas a archive/ con `git mv` (registro en archive/README.md): output/v3/{articulo, informe_politica, lo_que_sabemos}.md y output/v4/{working_paper, policy_brief}.md. Ninguna cifra cambia.
- Makefile: `src/v5/a5_validacion.py` y `src/v5/b3_potencia.py` entran en `V5_ORDEN`; ya generaban salidas versionadas y reproducen los mismos ficheros byte a byte.
- CITATION.cff, .zenodo.json y README_REPLICACION.md pasan a la versión 5.1.
- Rutas locales absolutas eliminadas de documentos internos (docs/v2, docs/v5, docs/v5_1, docs/fallidas).

## v5.1 (2026-10-11)

Cifras y capas cambiadas en los entregables (todas desde output/v5/cifras_clave.csv):
- Déficit 2021-2024 con bajas: `deficit_2124_c2` (cota C2 hasta 902.808, bajas supuestas del 0,1-0,2 %) → `T3-H2` (C4, hasta 744.144, bajas estimadas en T1). Motivo: ningún dato observado respalda el supuesto de v4. `deficit_2124_c1` (C1, sin bajas) no cambia.
- Bajas del parque: supuesto de v4 del 0,1-0,2 % anual → tasa C4 de T1 (0 / 0,026 % / 0,052 %, máximo de las demoliciones con licencia); cota física 0 en C2. Motivo: las identidades de stock dan bajas negativas y las demoliciones con licencia son 0,02-0,04 % del parque.
- Necesidad 2026-2035: `B1-H1` / `E-B1-anual` (94.000-310.000 al año, C4) → base `T3-H5b` (99.000 / 210.000 / 292.000, C4) con la sensibilidad `T3-H5` (124.000 / 246.000 / 339.000, C4). Motivo: reposición con las bajas de T1 y componente X de T2, que suma.
- Nuevo: descomposición del rango de la necesidad (movilizables 34 %, el supuesto que más pesa) y frase frente a la producción con la misma cobertura (`T3-H9`, 1,4 / 2,7 / 3,8 veces). Motivo: revisión de v5.1 (B1).
- Proyección 2026-2030: `B2-H1` y `B2-H6` (C4; provincias 20 / 5 / 27) → `T4-H1`, `T4-H2` y `T4-H3`: dirección nacional «empeora» en C2 (180 escenarios), magnitud C4; provincias 15 / 0 / 37. A 2035, dirección indeterminada (C4). Motivo: rejilla de T4 que separa dirección y magnitud.
- Liberadas por envejecimiento: `E-B1-L` (1,42 M en diez años, C4) → `T2-H1` (1,86 M en 2026-2035, C4), con la parte que llega al mercado (`T2-H6`), el reparto por tipo de municipio y el desajuste territorial; frase explícita de que no se restan de la necesidad en todos los entregables. Motivo: T2.
- Verificador: ficha `B2-V1` → `T4-V1` (NO RESPALDADA, C2); la ponencia cita `T2-V1` para el mito del envejecimiento.
- Cifras auxiliares nuevas en `src/v5/e_hechos_t7.py` (ids `E-T7-`): demoliciones con licencia en 2024 en % del parque, terminadas con País Vasco y Navarra, pesos de la descomposición y liberadas por tipo de municipio.

## v5.0 (2026-10-10)
- Módulo R. Se recuperan pendientes:
  - no residentes por provincia;
  - conciliación VUT INE/GVA;
  - efecto donut;
  - sensibilidad de Oster y Cinelli-Hazlett en los diseños de v2;
  - GSADF con tamaño corregido;
  - tabla de quién posee las viviendas;
  - capacidad de la construcción;
  - pendientes técnicos (ficheros >50 MB, ediciones del Notariado, distritos SERPAVI).
- Módulo A. Tabla única de cifras clave (output/v5/cifras_clave.csv), puente IPV frente a núcleo de precio, alquiler de stock frente a contratos nuevos (fianzas), coste oficial y reclasificación territorial, y programas oficiales con búsqueda por palabras clave.
- Módulo B. Necesidad 2026-2035 por provincia, proyección del déficit a 2030, diferencias entre provincias (pre-registrado: `prereg-v5`) y contribuciones a la subida.
- Módulo C. Comparación europea, crédito a promotores, compras al contado, seguridad jurídica, fiscalidad del alquiler, peso de las empresas, desigualdad y salidas del régimen de protección.
- Módulo D. Matriz de instrumentos completa, política por territorio y convergencia con otros organismos.
- Módulo E. Paquete de publicación.
- Puerta `make check` ampliada (check_v5): cifras de los entregables leídas de cifras_clave, suma provincial = nacional, lecturas versionadas y recuentos oficiales.

## v4 (2026-10-10)
Geografía del déficit, descomposición de hogares, factibilidad, parque frente a mercado, evaluación de instrumentos, preguntas abiertas y verificador ampliado.

## v3, v2, v1
Véanse docs/v3/estado.md, docs/v2 y output/informe.md.
