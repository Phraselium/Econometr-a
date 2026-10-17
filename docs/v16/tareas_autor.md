# V16 · Tareas del autor

## 1. Publicar las etiquetas de pre-registro interno (bloqueo B-1; prioridad máxima)
Desde esta sesión el remoto rechaza las etiquetas (HTTP 403). Los commits ya están en la rama `claude/housing-price-spain-econometric-95dhj3`. Desde tu clon:

```
git fetch origin claude/housing-price-spain-econometric-95dhj3
git tag -a prereg-v15 542b4fdf398970c817af7abfcd20c92dda299c69 -m "V15: pre-registro interno sin sello externo (preregistro_v15.md y adendas 1-2)"
git tag -a prereg-v2 910c42aef06348b884ea70e7b6cdc510d58e48c1 -m "pre-registro v2"
git tag prereg-v3 204c073e9e2c9e0edd6ac23dad7edf3049ba4428
git tag -a prereg-v5 8803f049c0f46ae4db8a79221470594295931d86 -m "pre-registro v5"
git tag -a prereg-v6 a33c167080fbd4b86a9239dcb3744d070e501429 -m "pre-registro v6"
git tag prereg-v7 3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0
git tag prereg-v8 91e618be1a2d17879808982a1fe87729d7f5afaf
git tag prereg-v9 2977349e3ed3092a51c8a3ad309140cf0b83dca8
git tag prereg-v9-a1 9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7
git tag prereg-v9-a1b 4639772d1dbac4e01af0e24bc0a8501117fe1324
git push origin --tags
git ls-remote --tags origin "prereg-*"
```

La lista de etiquetas, commits y tipos de objeto está en docs/v16/etiquetas_prereg.csv.

Y el de V16 (fase 4 cerrada el 2026-10-17):

```
git tag -a prereg-v16 a8304ecc07aacc8db9ca59d90baf522ac1b305d7 -m "V16: pre-registro interno sin sello externo (preregistro_v16.md y adenda; sellado_v16.json)"
git push origin prereg-v16
```
 Hasta que esté en el remoto, la guarda (f) mantiene bloqueadas las fases 5 a 7 de V16, por diseño.

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
