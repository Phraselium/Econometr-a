# Registro de cambios

Formato: versión, fecha y cambios principales. Las correcciones de resultados ya publicados van en ERRATA.md.

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
