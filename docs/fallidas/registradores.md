# Registradores: intentos fallidos y alternativas

Script: `src/extract_registradores.py`. Resultados en `data/raw/pdf/registradores_*.csv`; validación en `data/raw/pdf/registradores_validacion.csv`.

| Intento | URL | Paso | Resultado | Alternativa usada |
|---|---|---|---|---|
| Portal de datos abiertos (microdatos, CSV/XLSX) | https://opendata.registradores.org/dataset/dataset/compraventas-de-inmuebles-uso-residencial-por-provincia | 1 CSV | OK pero con un reparo: con User-Agent mínimo el WAF devuelve HTTP 200 "Request Rejected" (HTML); con cabeceras de navegador estándar (UA + Accept-Language) responde. CSV trimestral 2007T1-2026T2 de compraventas de vivienda, importe medio y €/m² (también garajes y trasteros), nacional/CCAA/provincia, en 4 trimestres móviles. | Usado (`registradores_opendata_compraventas.csv`). |
| Open Data: compras de extranjeros, nacionalidad, hipotecas | catálogo opendata.registradores.org (11 datasets: solo compraventas residencial/comercial y mercantil) | 1 | No existe dataset de extranjeros ni de hipotecas de vivienda. | Anuarios ERI en PDF. |
| Excel/CSV del anuario o trimestral ERI | https://www.registradores.org/actualidad/portal-estadistico-registral/estadisticas-de-propiedad | 1 | Solo PDF (ERI trimestrales 2004-2026 y Anuarios 2004-2025). | Anuarios PDF 2023, 2024, 2025. |
| Anuarios ERI 2023-2025 (PDF con texto) | https://www.registradores.org/documents/33383/148210/ERI+Anuario+2025.pdf/... (y 2024, 2023) | 2 pdfplumber | OK (182 págs. cada uno; solo se extraen las tablas pedidas; páginas localizadas por título). No hizo falta camelot/tabula ni OCR. | Usado (`registradores_eri_anuario.csv`). |
| Compras de extranjeros por provincia/CCAA en número absoluto | Anuarios | - | El Anuario publica % (CCAA y provincia) y nº solo para ~10 nacionalidades principales en gráficos (no tabla). No se estimaron. Nacionalidad por provincia: solo "nacionalidad cabecera" (gráfico). | % de extranjeros × compraventas (cálculo posterior; implícitos contrastados con notarios en validación). Nacionalidad por CCAA (top 10, incl. C. Valenciana) sí extraída. |
| Hipotecas (nº, importe; hipotecas de extranjeros) | Anuario caps. 17-24 | - | Fuera del alcance acordado (solo tablas de compras de extranjeros y compraventas); no extraído. | pendiente si se requiere. |
| València municipio | Anuario p.31/43 (capitales de provincia: compraventas y €/m²) | 2 | OK (capital = "València"), anual. Compras de extranjeros por municipio no se publican. | Usado para compraventas y €/m². |

Notas de calidad
- La tabla "% s/extranjeros por nacionalidad" de España (p.78) suma 97,96% (2025; 98,04% en 2024; 97,99% en 2023) en el propio PDF; los valores extraídos coinciden con el render. Se marca `validado=no` en el cuadre; no se corrige.
- Ceuta y Melilla: el Anuario las incluye en Cádiz y Almería (y en Andalucía); el CSV las lista aparte. La conciliación (CSV + Ceuta/Melilla) da error 0 frente al PDF; sin ella la diferencia es 1.347 en Andalucía.
- CSV opendata y Anuario son series de 4 trimestres móviles / año natural, no flujo trimestral.
- Las series % extranjeros CCAA de los tres Anuarios coinciden entre ediciones (sin revisiones).

Corrección tras la revisión F1 (2026-10-09)
- El CSV opendata es una **suma móvil de 4 trimestres** (p. ej. España 2025T1-T4 = 667.058 / 691.863 / 699.638 / 705.357). La serie trimestral se renombra con sufijo `_4T_movil` (`compraventas_viv_num_4T_movil`, etc.), `fecha` = inicio del último trimestre de la ventana y columna `ventana` = `AAAAQq-AAAAQq`. No usar como flujo trimestral (MA(3) mecánico y solapamiento).
- Serie anual para el modelo: `registradores_opendata_anual.csv` (solo T4 = año natural; fecha AAAA-01-01, periodo AAAA, series sin sufijo).
- **No recuperable**: los trimestres individuales por diferencias, Q_t = S_t − S_{t−1} + Q_{t−4}, exigen cuatro valores iniciales Q no observados (el CSV solo publica sumas móviles). No se calcula ni se imputa.
- Las filas `*_extranjeros_implicitos_vs_notarios_CGN` pasan de `validado=si/no` a `validado=plausibilidad` (contraste entre fuentes y fechas distintas, sin umbral de cuadre).
- Reproducibilidad: caché a nivel de salida (sin FORCE=1 y con los 4 CSV presentes, el script termina sin red; probado con HTTPS_PROXY inválido, exit 0).
