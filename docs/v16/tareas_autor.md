# V16 · Tareas del autor

## 1. Publicar las etiquetas de pre-registro interno — RESUELTA (2026-10-17)
- **Qué se hizo.** El autor publicó las 11 etiquetas prereg-* desde su ordenador, a las 17:42 UTC, como etiquetas anotadas con el mensaje «Pre-registro interno <versión>, fijado en el commit <hash>; sin sello de tiempo externo».
- **Comprobación en esta sesión.** Con `git ls-remote --tags origin`, cada etiqueta apunta a su commit (línea `^{}`):
  - prereg-v2 → 910c42a, prereg-v3 → 204c073, prereg-v5 → 8803f04, prereg-v6 → a33c167;
  - prereg-v7 → 3fad305, prereg-v8 → 91e618b;
  - prereg-v9 → 2977349, prereg-v9-a1 → 9cb2200, prereg-v9-a1b → 4639772;
  - prereg-v15 → 542b4fd, prereg-v16 → a8304ec.
- **Registro.** Fechas y huellas en docs/preregistros.md; las fechas, en docs/v16/etiquetas_prereg.csv.

## 2. Decidir sobre la independencia de dh_2125 (aumento de hogares 2021-2025, C1)
Sus dos fuentes son la ECP y la EPA del INE. La EPA se calibra con las cifras de población que salen de la ECP, de modo que las dos fuentes podrían no ser independientes en el sentido que llevó a las 11 bajadas de la 1.0. Opciones:
- (a) mantener C1 y explicar por qué la jefatura de hogar de la EPA es una medición distinta;
- (b) bajar a C4 sin cambiar el valor, con la línea «dh_2125 | capa C1 → C4» en ERRATA.md y una fila en docs/v15/bajadas_capa.csv.
V16 no lo cambia por su cuenta: la cifra figura como C1 en la página de hechos. Las cifras nuevas V16-* aplican ya esta vara (fase 2).

## 3. Datos que dependen de ti (fase 1)
El trabajo sigue sin ellos. Cada paso exacto está en la ficha de su familia, en docs/v16/fuentes/.

**Por orden de valor para las preguntas de V16:**
1. **Q1 y Q2 · Inside Airbnb anterior a 2025-12.** Formulario en https://insideairbnb.com/data-requests/, pidiendo las ciudades españolas y todo el histórico.
2. **Q8 · Golden visa (OPI).** Autorizaciones de residencia por inversión, por nacionalidad y año. Descarga manual desde inclusion.gob.es (el servidor da 403 al agente). Destino: data/raw/v16/demanda_internacional/_terceros/golden_visa/.
3. **Q4 · Restricciones físicas y de planeamiento:**
   - SIU del MIVAU (suelo urbano y urbanizable por municipio);
   - MDT05 del CNIG (pendientes);
   - DPMT del MITECO (dpmt.zip, 12 MB, uso libre con cita);
   - cuenta en CLMS para CORINE 2018.
   - Sin estos datos, la elasticidad tipo Saiz solo puede usar la Red Natura y la línea de costa.
4. **Q5 · Licencias:**
   - EA-MPD del BCE: decidir si se acepta su uso con cita. Hoy está en _terceros.
   - Choques de Jarociński-Karadi: la versión mensual en abierto ya está en el repositorio con CC BY 4.0.
5. **Fase 2 · Catastro y EFF:**
   - descarga masiva alfanumérica del Catastro (certificado electrónico; parque por año de construcción, uso y superficie);
   - microdatos de la EFF (solicitud a BELab del Banco de España).
6. **Q1 y Q2 · Registro Único de Arrendamientos (RD 1312/2024).** Pedir estadísticas agregadas por provincia o municipio y mes al MIVAU y al Colegio de Registradores (Portal de Transparencia).
7. **Q1 · Fianzas por tipo de contrato** (temporada, habitación) en Madrid, Andalucía y Baleares, y altas de viviendas turísticas de Catalunya con fecha, Ibiza y Formentera: solicitud a las agencias autonómicas.
8. **Licencias por confirmar** (hoy en _terceros):
   - estadísticas judiciales del CGPJ (lanzamientos);
   - Nomenclátor de partidos judiciales;
   - Red Natura 2000 (MITECO);
   - ITP y AJD del panorama del REAF: el CSV solo lleva tipos impositivos, con las leyes autonómicas como fuente normativa.
9. **ECV longitudinal 2017-2025** (unos 510 MB): decidir si se descarga. La transversal ya está completa (2004-2025).

## 4. Comprobaciones pequeñas (auditorías de la fase 1)
- Confirmar que «Noáin (Valle de Elorz)» corresponde al código INE 31088, uno de los 11 alias manuales del ADRH (output/v16/auditoria/renta_parque/). Cae en Navarra, que está en la muestra sellada v6, así que no afecta a ningún análisis de V16 hasta la evaluación.
- Vivienda pública por habitante frente a la UE (fase 2): falta el indicador PH4.2 de la OCDE (Affordable Housing Database). Si se descarga a data/raw/v16/demanda_internacional/, el hecho se añade como C4.
