# Ideas futuras (fuera del alcance de V8)

V8 es la última versión de modelización (docs/v8/cierre_proyecto.md). Estas ideas solo se abordarían en un v9 con datos nuevos, o en la fase de propuestas y publicaciones si no requieren estimar modelos.

| Idea | Por qué no ahora | Coste estimado |
|---|---|---|
| SVAR con identificación externa combinada (signos más un instrumento de alta frecuencia como «proxy-SVAR») | Los shocks del BCE son débiles para el precio y el alquiler españoles (F efectivo muy por debajo de diez); un proxy débil no mejora la identificación | Alto (nueva herramienta y su Monte Carlo) |
| Alquiler de contratos nuevos trimestral nacional (fianzas de todas las CCAA o índice de contratos nuevos del INE) | No existe una serie trimestral nacional de contratos nuevos; el IPC de alquiler sigue el parque | Medio, si las CCAA o el INE publican la serie |
| SVAR regional (panel BVAR por CCAA) para designar factores por comunidad | Con las series regionales disponibles (alquiler desde 2008, crédito sin desagregar) el número de parámetros supera a los datos | Alto |
| Empuje migratorio con flujos bilaterales por provincia de destino | Solo hay cuotas iniciales nacionales; con cuotas provinciales el instrumento ganaría variación | Medio (datos del INE bajo petición) |
| Turismo con una serie larga (antes de 2016) y viviendas de uso turístico por municipio | El turismo solo cubre 2016-2026 y se confunde con el ciclo reciente | Medio |
| Compras de extranjeros por provincia y trimestre con serie larga (Notariado, Registradores) | Las series públicas son cortas o anuales | Bajo-medio (petición de datos) |
| Prior jerárquico que reduzca la atenuación de magnitudes del BVAR (documentada en F3) | Cambiaría la herramienta validada después del pre-registro | Medio |
| Muestreo directo de rotaciones con ceros para la identificación de dos trimestres (Arias, Rubio-Ramírez y Waggoner, NO VERIFICADA) | La tabla pre-registrada no aceptó rotaciones; un muestreador nuevo exigiría otra validación y otro pre-registro | Alto |
