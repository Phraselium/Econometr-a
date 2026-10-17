# V15 · Tareas del autor

## PUERTA DE LA FASE 3: depósito en OSF (lo hace el autor)

1. **Registro en OSF.** Cree un registro en OSF («OSF Preregistration» o «Open-Ended Registration») con:
   - el texto de abajo;
   - adjuntos: docs/v15/preregistro_v15.md, docs/v15/preregistro_v15_adenda.md y docs/v15/sellado_v15.json, en la versión de la etiqueta local `prereg-v15`.
2. **Etiqueta.** Si quiere publicarla, súbala usted (`git push origin prereg-v15`). Claude no sube etiquetas.
3. **proyecto.json.** Añada `"osf_prereg_v15": "<DOI o URL del registro OSF>"` y la fecha del depósito. Sin ese campo, la puerta (src/v15/puerta.py y la guarda del hook) mantiene cerradas las fases 4 y 5.
4. **Al reanudar.** Claude comprobará que la fecha del depósito es anterior a cualquier estimación de V15.

### Texto exacto para OSF

**Título:** Vivienda en España, V15: preguntas pre-registradas sobre regulación del alquiler, vivienda turística, inmigración y predicción (pre-registro y adenda)

**Autor:** Borja Romero (economista; firma individual e independiente)

**Resumen (ES):**
- **Qué es.** Pre-registro de la versión 15 de un estudio reproducible sobre la vivienda en España, depositado antes de estimar ningún efecto.
- **Hipótesis confirmatorias** (Holm, m = 3):
  - H1 y H2: asociación de la declaración de zonas tensionadas (Ley 12/2023) en Cataluña con la renta y el número de contratos de alquiler nuevos (Incasòl), con Callaway-Sant'Anna y SDID, Honest DiD y preperiodo posterior a la anulación de los topes de 2020-2022;
  - H4: inmigración y alquiler municipal con un instrumento shift-share (padrón 2003-2022), inferencia AKM y Anderson-Rubin.
- **Asociación pre-registrada** (C4): H3, densidad de vivienda turística (INE) y alquiler declarado (SERPAVI) por sección censal.
- **Contraste predictivo:** H5, combinación de modelos frente a la línea base más exigente (AR(4), ECM v1 y paseo aleatorio), con Diebold-Mariano y Model Confidence Set.
- **Exploratorias:** cuatro, con BH.
- **Descartadas antes de estimar:** tres, por falta de datos o de potencia.
- **Validación sellada,** fijada antes de estimar:
  - datos publicados después del depósito, con mínimos por hipótesis y evaluación única;
  - un bloque espacial aleatorio (SEED=20261010) de 33 celdas de 0,5° y el 15 % de los distritos de las grandes ciudades.
- **Condiciones de la capa causal (C3):** superar todas las pruebas declaradas y la evaluación sellada temporal. Un diseño válido sin efecto se reporta como nulo acotado (TOST).
- **Historial.** Se declaran las especificaciones previas de las versiones 1 a 14 y la multiplicidad entre versiones.

**Abstract (EN):**
- **What this is.** Pre-registration of version 15 of a reproducible study of housing in Spain, deposited before any effect is estimated.
- **Confirmatory hypotheses** (Holm, m = 3):
  - H1 and H2: association of the designation of stressed rental areas (Law 12/2023) in Catalonia with new-lease rents and the number of new leases (Incasòl deposits), using Callaway-Sant'Anna and synthetic difference-in-differences with Honest DiD, and a pre-period after the 2020-2022 rent caps were annulled;
  - H4: immigration and municipal rents with a shift-share instrument (municipal register 2003-2022), AKM and Anderson-Rubin inference.
- **Pre-registered association** (no causal layer): H3, short-term rental density (INE) and declared rents (SERPAVI) by census tract.
- **Predictive test:** H5, a forecast combination against the most demanding benchmark (AR(4), the v1 error-correction model and a random walk with drift), using Diebold-Mariano and the Model Confidence Set.
- **Exploratory questions:** four, with BH.
- **Dropped before estimation:** three, for lack of data or power.
- **Sealed validation,** fixed before estimation:
  - data released after the deposit, with minimum amounts per hypothesis and a single evaluation;
  - a random spatial block (SEED=20261010) of 33 cells of 0.5° and 15 % of large-city districts.
- **Causal layer (C3):** requires passing all declared tests and the temporal sealed evaluation. A valid design with no effect is reported as a bounded null (TOST).
- **History.** Prior specifications from versions 1 to 14 and cross-version multiplicity are disclosed.

**Fecha de corte de los datos:** 2026-10-17 (docs/v15/sellado_v15.json, con sha256 de las fuentes).
**Etiqueta del repositorio:** prereg-v15. **Repositorio:** URL de proyecto.json.


## Pendiente de decisión (de la fase 0)
- ~~**Capa de las cifras C1 de la 1.0**~~ Resuelto antes del depósito: 11 cifras bajan a C4 sin cambiar su valor (ERRATA, adenda V15 del historial; decisiones G8).
- ~~**Metadatos de la base pública 1.0**~~ Resuelto antes del depósito: año de la obra neta del Catastro, base del IPC de alquiler y unidad y fuente de permisos (ERRATA; decisiones G8; docs/v15/cambios_publicacion_web.md).
- **Cuartiles Scimago** (descarga no automatizable: Cloudflare; docs/v6/fuentes_fallidas.md).
  1. Descargue el ranking de 2024 desde https://www.scimagojr.com/journalrank.php («Download data»).
  2. Deje en docs/v15/scimago_cuartiles.csv solo las revistas citadas en docs/v15/literatura/, con las columnas revista, issn, cuartil, categoria, anio_scimago y fecha_consulta.
  3. `python3 src/v15/verificar_referencias.py --sin-red` rellenará los cuartiles.

  Mientras tanto, todas las referencias con DOI quedan «VERIFICADA (Crossref; cuartil no verificado)».
- **AEAT 2013-2015** (auditoría de renta y microdatos). Los ficheros municipales de esos años no traen declaraciones, renta bruta media ni renta disponible media, y sus valores parecen recuentos. **No son utilizables como renta en euros.** La base usa 2016-2024, así que ninguna cifra publicada cambia. Si se quieren esos años, hay que volver a descargarlos con todas las columnas (descarga HTML por municipio, no automatizada en el repositorio).
- ~~**Filas sub-provinciales de las provincias selladas en v6**~~ Resuelto antes del depósito: docs/v15/contaminacion_v6.md, todos los casos sin efecto, marca en la base y control en make check (decisiones G7).
