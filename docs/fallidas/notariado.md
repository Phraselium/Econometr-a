# Notariado: intentos fallidos y alternativas

Script: `src/extract_notariado.py`. Resultados en `data/raw/pdf/notariado_*.csv`; validación en `data/raw/pdf/notariado_validacion.csv`.

| Intento | URL | Paso | Resultado | Alternativa usada |
|---|---|---|---|---|
| Portal Estadístico del Notariado (compraventas y €/m², nuevo visor) | https://penotariado.com/inmobiliario/ (Next.js; API `/inmobiliario/rest/v1`) | 1 API | Solo `/public/masters/*` (provincias, periodos, tipos) y `/public/map-tour-views` son abiertos. Los datos estadísticos (`/private/statistics?lang=`, `/private/shared-statistics`) devuelven HTTP 400 `Authorization header not found`: exigen cuenta (login Keycloak). No se creó cuenta ni se eludió la autenticación. | Informe CGN (xlsx abierto) + estadísticas del Colegio Notarial de Valencia (PDF). **El €/m² de todas las compraventas (no solo extranjeros) y por provincia/municipio queda no recuperable** sin cuenta; el xlsx del CGN trae €/m² solo para compradores extranjeros/nacionales (España) y extranjeros por CCAA. |
| Visor CIEN "Estadísticas al completo" | https://www.notariado.org/liferay/web/cien/estadisticas-al-completo (endpoint `getFiltrosWeb`, `/cienServices/service/buscador/json\|excel`) | 1 API | Catálogo abierto, pero ya no contiene compraventa de vivienda (el grupo 05 empieza en 502; sí hay préstamos hipotecarios "adquisición de vivienda" por provincia, no extraídos por no estar en el alcance). | Ver arriba. |
| Informe "Compraventa de vivienda por extranjeros" 2S25 (CGN) | https://www.notariado.org/liferay/web/cien/sala-de-prensa/noticias/detalle?...NOTARIO_INFORMA_DETALLE_ID=32452895 | 1 xlsx | OK: anexo xlsx (`get_file?uuid=125f548a-...`) con series semestrales 1S07-2S25: España (residentes/no residentes, nacionales), CCAA, nacionalidad (total/residentes/no residentes), nº y €/m². Solo vivienda libre. El PDF del informe (17 págs.) se guardó pero no se extrajo (redundante). | Usado. |
| Estadísticas CV por extranjeros (Colegio Notarial de Valencia / CTN) | https://valencia.notariado.org/portal/noticias (noticia 4T 2025, id 5024637) | 2 PDF texto | OK con pdfplumber (tablas con celdas vacías preservadas). Provincias de València, Alicante y Castellón: viviendas vendidas a españoles/extranjeros y cuantía media (2018T1-2025T4), y por nacionalidad (24 países + otras). | Usado. |
| Actos de compraventa de inmuebles por provincia (mensual) | mismas noticias "Datos Estadísticos Notariales de la CV" / "Comparativa" | 2 PDF texto | OK (2019-01 a 2026-03, 7 ediciones solapadas con revisiones de hasta 6%). Cuenta actos sobre inmuebles, no solo viviendas. | Usado; conservar `edicion` y usar la más reciente. |
| Extranjeros por municipio (València ciudad y otros) | PDF "por municipios" 4T 2021-4T 2025 | 2 PDF texto | OK: compras anuales por nacionalidad por municipio de la provincia de València (solo ediciones de cierre de año). | Usado. |
| Informes nacionales/CCAA anteriores a 2007 o por municipio de València con €/m² | - | - | No existen en abierto. | no recuperable |

Notas de calidad
- El PDF provincial entrelaza letras en celdas de etiqueta de varias líneas ("Reino Unido, Gran Bretaña, Irlanda del Norte", "Otras nacionalidades", "República Eslovaca"); se repuso el nombre canónico (de la tabla anual limpia de la p.7) por igualdad de multiconjunto de letras. No se alteró ningún valor numérico.
- Celdas vacías en origen (p. ej. Estonia 2023T3, Noruega 2025T1) no se imputan.
- Fila sin etiqueta en el xlsx (tabla 2, entre Cataluña y C. Valenciana): se conserva como `SIN_ETIQUETA_EN_ORIGEN` (cuadra con el total nacional).
- Viviendas españolas + extranjeras en el PDF provincial solapan ~4-6% (un acto con compradores de ambos tipos cuenta en los dos grupos); el ratio vs. MIVAU es estable.
- Contrastes que no cuadran (ver validación): INE ETDP (concepto registral, ±49%), MIVAU extranjeros provincia de València (ratio 1,06-1,20 sistemático), actos vs INE (inmuebles vs viviendas).
