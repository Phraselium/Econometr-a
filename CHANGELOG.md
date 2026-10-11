# Registro de cambios

Formato: versión, fecha y cambios principales. Las correcciones de resultados ya publicados van en ERRATA.md.

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
