# Notas de publicación (para pegar en GitHub)

Generado por `src/v7_1/s6_paquete.py` desde docs/v7_1/plantillas/release_notes.md. Las cifras salen de output/v5/cifras_clave.csv. Hay una sección por release: péguela tal cual en la descripción de cada una.

---

## Release `prereg-v7` · Pre-registro V7 (validación diferida)

**Commit:** `3fad305` (etiqueta local `prereg-v7`).

**Qué es.** El pre-registro de los modelos regionales de V7, escrito antes de estimar con datos reales:
- hipótesis confirmatorias de largo plazo con su regla de triangulación entre estimadores;
- familias exploratorias con su corrección;
- la validación limpia diferida, que se evaluará una sola vez con datos publicados después de esta release (2026T3-2027T2).

**Por qué importa la fecha.** La fecha de esta release, o la de su DOI en Zenodo, es la fecha verificable del pre-registro. Los datos publicados después son la muestra limpia.

**Ficheros:**
- [docs/v7/hipotesis.md](../v7/hipotesis.md), también en [metodologia/preregistro_v7.md](../../metodologia/preregistro_v7.md);
- docs/v7/desviaciones.md;
- docs/v7/validacion_herramientas.md (validación por Monte Carlo anterior a la estimación).

**Valor crítico de la velocidad de ajuste media, fijado por simulación:** -8,83 estadístico t.

---

## Release `v7.0` · Atlas econométrico regional

**Commit:** `3d1170c` (etiqueta local `v7.0`).

**Resumen.** Paneles de las 17 comunidades autónomas (2007T1-2026T2), herramientas de panel validadas por Monte Carlo, modelos explicativos, predicción con congelación de modelos y propuestas condicionales. Todo es C4 («informativo, muestra ya vista»).

**Cifras principales** (todas C4):
- **Ninguna relación regional de largo plazo confirmada:** 0 de siete hipótesis pre-registradas.
- **Ningún estimador apto con un factor común I(1) de cargas heterogéneas.** Sesgo de 20,3 % con MG con demeaning y de 10,9 % con CS-DL.
- **Predicción.** El mejor modelo bate a la base más exigente en 6 de 17 comunidades en alquiler y en 5 de 17 en compra, con selección en muestra. Los modelos se congelaron con sha256 `93795a94…0a9a0646`.
- **Simulación de traslado a diez años.** La movilización de vacías baja el alquiler de mercado -3,8 % (mediana). Las ayudas a la demanda suben el precio de mercado 4,4 %. El signo lo fija la fórmula de incidencia.

**Enlaces:** output/v7/atlas_resumen.md y output/v7/atlas/; versión ampliada en [publicacion/atlas_regional/](../../publicacion/atlas_regional/atlas_resumen.md).

---

## Release `v7.1` · Versión de referencia: consolidación y estructura para publicación

**Commit:** el del cierre de V7.1 (etiqueta local `v7.1`).

**Resumen.** No añade análisis. Ordena todo lo vigente para el lector, declara la v7.1 versión de referencia (la v6.2 pasa a histórica) y añade:
- la dosis y el coste de las simulaciones de política;
- una nota metodológica;
- una sección única sobre qué cambió entre versiones;
- el ensayo de la evaluación diferida.

**Cifras principales** (todas C4):
- **Componente común.** El R² mediano de la variación interanual de cada comunidad frente a la media de las 17 es 93,6 % en compra y 86,1 % en alquiler. Es un descriptivo.
- **Coste fiscal anual mediano por comunidad.** Ayudas a la demanda: 378,2 M€/año. Rebaja de ITP/IVA: 93,3 M€/año. En los instrumentos de oferta, coste no estimable.
- **Efecto por cada diez mil viviendas en el alquiler** (mediana): -1,7 puntos % con la movilización de vacías y -3,2 puntos % con vivienda pública.
- **Ensayo de `make evaluate_v7`** con datos futuros simulados: superado (reproducir/ensayo_evaluate_v7.md).

**Enlaces:**
- [LEEME_PRIMERO.md](../../LEEME_PRIMERO.md)
- [publicacion/](../../publicacion/MANIFIESTO.md), con [cifras_clave.csv](../../publicacion/cifras_clave.csv)
- [metodologia/](../../metodologia/MANIFIESTO.md)
- [reproducir/](../../reproducir/MANIFIESTO.md)
- [nota metodológica](../../publicacion/nota_metodologica.md)
- [qué cambió](../../publicacion/que_cambio.md)

**Cambios en cifras publicadas:** ninguno (ERRATA.md sin entradas nuevas).
