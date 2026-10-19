# V18 (incluye V17) · Tareas del autor

No paran el trabajo: se anotan y se sigue con lo demás.

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
