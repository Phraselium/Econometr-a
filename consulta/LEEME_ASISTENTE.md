<!-- Generado por `make consulta` (src/consulta/generar.py). No editar a mano: se regenera y un test lo comprueba. -->

# Guía para asistentes: cómo usar este repositorio

Estás ante una base de evidencia sobre la vivienda en España. Autor: Borja Romero, economista (firma individual, independiente). Esta guía resume qué es vigente, cómo leer las capas y qué reglas seguir al responder. Léela entera antes de contestar; es corta.

## 1. Versión vigente

- Versión pública: **1.0** (2026-10-16). Reúne las versiones internas de desarrollo v1 a V12 (correspondencia en CHANGELOG.md). Metadatos en [version.json](version.json). Para cada tema vale una versión interna:
- **V8** (redacción y tablas de v8.1) para la modelización: por qué ha subido la vivienda, factores, periodos y factor común (SVAR, factor común, instrumentos, multiverso, predicción).
- **V9** para qué causa qué: diseños pre-registrados; ninguno alcanza C3 ni C3s.
- **V10** (sin modelos nuevos): base única, atlas descriptivo (ids `V10-ATL-*`), figuras, web y monitor; los datos desde 2026T3 no se contrastan con predicciones.
- **V12** (descriptivo, datos de V11): demografía, hogares, titularidad, oferta, condiciones por origen y turismo (ids `V12-*`).
- **v7.1 y v7.2** para el **déficit y la necesidad de vivienda**, las simulaciones de instrumentos (dosis y coste) y el atlas regional. v5 a v6.3 siguen vigentes en lo que no han sido superadas.
- Repositorio: https://github.com/Phraselium/vivienda-espana-evidencia. DOI: PENDIENTE. Fecha verificable del pre-registro: PENDIENTE (también en [version.json](version.json)).
- Una cifra **superada** no se cita nunca: las lista [output/v5/cifras_superadas.csv](../output/v5/cifras_superadas.csv) con su sustituta. El registro completo está en [hallazgos.md](hallazgos.md) y [hallazgos.json](hallazgos.json) (campo `estado`: vigente, superada o retirada).

## 2. Capas de evidencia y cómo citarlas

| Capa | Qué es | Cómo se redacta |
|---|---|---|
| C1 | Hecho: al menos dos fuentes que coinciden en la tolerancia declarada | «es», «fue»; rango entre fuentes |
| C2 | Cota con supuestos explícitos, o dirección estable en una rejilla de escenarios | «como máximo», «en todos los escenarios de la rejilla» |
| C3 | Efecto identificado (instrumento externo o diseño que supera las pruebas) | lenguaje causal permitido; ningún resultado del proyecto la alcanza |
| C3s | Descomposición del SVAR con restricciones de signo y de cero explícitas | siempre «condicionado a las restricciones de signo y de cero»; con banda |
| C4 | Exploratorio: asociación, contabilidad, proyección, predicción, simulación | «se asocia», «en la simulación»; sin lenguaje causal |

La capa de un resultado es la menor de las de sus componentes; **nunca se promueve de capa**. Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Cita cada cifra así: «valor (id; capa; periodo; fecha del dato)». Ejemplo: `V8-M5-c3` = 0 instrumentos; capa C4; dato 2025T3.

## 3. Reglas para responder

1. **Solo cifras de `output/v5/cifras_clave.csv`**, con su id y la fecha del dato. Si no está allí, no es una cifra del proyecto: dilo. Nunca cites una cifra superada.
2. **Sin causalidad fuera de C3 y C3s.** Nada causal desde SHAP, importancias, dominancia (LMG) ni coeficientes de aprendizaje automático. Predecir no es explicar. Los resultados C3s valen solo bajo las restricciones del modelo.
3. **Atribuciones siempre con banda** (68 % en el SVAR; 95 % donde se indique). Si la banda incluye el cero, no digas que el factor «explica» nada.
4. **Di «no concluyente» cuando lo sea.** Es el resultado más frecuente de V8: ninguna regla designa un factor único. Un veredicto «ANALIZADA, NO CONCLUYENTE» no es una evasiva, es el resultado.
5. **Neutralidad.** Se evalúan afirmaciones e instrumentos, nunca partidos ni personas; sin lenguaje valorativo. Si te piden juzgar a quien dice algo, evalúa la afirmación con la ficha del verificador y nada más. Los programas electorales y la divulgación quedan fuera de alcance.
6. **Distingue mercados y medidas.** Compra no es alquiler. En el alquiler, el **parque** (stock de contratos vigentes: IPC de alquiler, SERPAVI) no es **contratos nuevos** (fianzas, IPVA); en la compra, el valor tasado no es el precio de escritura ni el IPV. Cada resultado declara su medida de precio; no mezcles medidas.
7. **Distingue unidades.** `pp` son puntos porcentuales (log por 100); las proyecciones de hogares y viviendas son por año o por periodo según el id; no sumes rangos de escenarios distintos.
8. **No inventes ni redondees al alza.** Si una cifra no cuadra con su id, prevalece `cifras_clave`. Si la pregunta requiere un dato que el proyecto no tiene (por ejemplo, un índice nacional trimestral de contratos nuevos), dilo y señala la tarea pendiente en [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md).
9. **Las referencias bibliográficas** están VERIFICADAS (DOI y cuartil) o marcadas NO VERIFICADA; respeta la marca.
10. **Ante una discrepancia entre métodos**, reporta ambos (media y mediana, con y sin bajas, MCO y 2SLS).

## 4. Qué sostiene y qué no sostiene la evidencia (V8)

- Sostiene: no hay un factor único designable; la subida reciente es muy común entre comunidades; el precio español acompaña al europeo (asociación, C4); el precio sigue su propia inercia a corto plazo.
- No sostiene: que un único factor explique la subida; que la subida de tipos frenara el precio; que el turismo sea el motor; efectos causales de los instrumentos (los tres son débiles).
- Evaluación diferida: `make evaluate_v7` y `make evaluate_v8` se ejecutan una sola vez, en 2027. No hay validación limpia de V7 ni V8 todavía.

## 5. Si te preguntan X, mira Y

- Si te preguntan por **Por qué ha subido el precio o el alquiler; qué factor pesa más**, mira [output/v8/por_que_ha_subido.md](../output/v8/por_que_ha_subido.md).
- Si te preguntan por **Qué responde V8 y qué no pudo hacerse**, mira [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md).
- Si te preguntan por **Contribución de cada factor por periodo (SVAR, descomposición histórica)**, mira [output/v8/M2/resumen.md](../output/v8/M2/resumen.md).
- Si te preguntan por **Fichas de atribución y regla de designación del factor**, mira [output/v8/F5/fichas.md](../output/v8/F5/fichas.md).
- Si te preguntan por **Factor común entre comunidades y relación con la zona euro**, mira [output/v8/M1/resumen.md](../output/v8/M1/resumen.md).
- Si te preguntan por **Periodos detectados y efectos por periodo**, mira [output/v8/M0/resumen.md](../output/v8/M0/resumen.md).
- Si te preguntan por **Relación de largo plazo, cointegración, contabilidad hogares-viviendas**, mira [output/v8/M4/resumen.md](../output/v8/M4/resumen.md).
- Si te preguntan por **Instrumentos externos (LP-IV, Anderson-Rubin, F efectivo)**, mira [output/v8/M5/resumen.md](../output/v8/M5/resumen.md).
- Si te preguntan por **Colinealidad y dominancia entre factores**, mira [output/v8/M6/resumen.md](../output/v8/M6/resumen.md).
- Si te preguntan por **Multiverso de especificaciones**, mira [output/v8/M7/resumen.md](../output/v8/M7/resumen.md).
- Si te preguntan por **Descomposición regional (CCAA)**, mira [output/v8/M8/resumen.md](../output/v8/M8/resumen.md).
- Si te preguntan por **Predicción, aprendizaje automático, SHAP**, mira [output/v8/M9/resumen.md](../output/v8/M9/resumen.md).
- Si te preguntan por **Predicciones congeladas y evaluación diferida de V8**, mira [docs/v8/evaluate_v8_accesos.md](../docs/v8/evaluate_v8_accesos.md).
- Si te preguntan por **Evaluar una afirmación del debate público**, mira [publicacion/verificador/verificador_v8.md](../publicacion/verificador/verificador_v8.md).
- Si te preguntan por **Fichas de afirmaciones en formato máquina**, mira [publicacion/verificador/fichas_v8.json](../publicacion/verificador/fichas_v8.json).
- Si te preguntan por **Verificador de afirmaciones de v5 y fichas de V7.1**, mira [publicacion/verificador/verificador.md](../publicacion/verificador/verificador.md).
- Si te preguntan por **Déficit de vivienda y necesidad 2026-2035**, mira [publicacion/lo_que_sabemos.md](../publicacion/lo_que_sabemos.md).
- Si te preguntan por **Informe técnico con déficit, necesidad y oferta**, mira [publicacion/informe_tecnico.md](../publicacion/informe_tecnico.md).
- Si te preguntan por **Resumen en una página**, mira [publicacion/una_pagina.md](../publicacion/una_pagina.md).
- Si te preguntan por **Qué cambió entre versiones**, mira [publicacion/que_cambio.md](../publicacion/que_cambio.md).
- Si te preguntan por **Simulaciones de instrumentos, dosis y coste**, mira [metodologia/dosis_coste.md](../metodologia/dosis_coste.md).
- Si te preguntan por **Atlas regional por comunidad autónoma**, mira [publicacion/atlas_regional/atlas_resumen.md](../publicacion/atlas_regional/atlas_resumen.md).
- Si te preguntan por **Burbuja y exuberancia (GSADF)**, mira [output/v7_2/gsadf/ficha_burbuja.md](../output/v7_2/gsadf/ficha_burbuja.md).
- Si te preguntan por **Paneles regionales de largo plazo**, mira [output/v7/R4](../output/v7/R4).
- Si te preguntan por **Compradores extranjeros y no residentes**, mira [output/v5/R1A](../output/v5/R1A).
- Si te preguntan por **Turismo y alquiler; topes de precios en provincias**, mira [output/v6/M1A](../output/v6/M1A).
- Si te preguntan por **Vivienda protegida y política de suelo**, mira [output/v5/CC](../output/v5/CC).
- Si te preguntan por **Instrumentos de política evaluados con rúbrica**, mira [output/v5/D1](../output/v5/D1).
- Si te preguntan por **Validación sellada y predicción provincial**, mira [output/v6_1/K1](../output/v6_1/K1).
- Si te preguntan por **Qué significa cada capa y cómo se redacta**, mira [metodologia/capas.md](../metodologia/capas.md).
- Si te preguntan por **Conclusiones por versión y su estado actual**, mira [metodologia/historial_conclusiones.md](../metodologia/historial_conclusiones.md).
- Si te preguntan por **Cómo se calcula una cifra del anexo**, mira [metodologia/anexo_metodologico.md](../metodologia/anexo_metodologico.md).
- Si te preguntan por **Pre-registro de V8 y desviaciones**, mira [metodologia/preregistro_v8.md](../metodologia/preregistro_v8.md).
- Si te preguntan por **Cómo reproducir los resultados**, mira [reproducir/instrucciones.md](../reproducir/instrucciones.md).
- Si te preguntan por **Errores corregidos tras publicar**, mira [ERRATA.md](../ERRATA.md).
- Si te preguntan por **Cómo citar y licencias**, mira [CITATION.cff](../CITATION.cff).
- Si te preguntan por **Referencias bibliográficas y estado de verificación**, mira [docs/literatura.md](../docs/literatura.md).
- Si te preguntan por **Pendientes del autor (DOI, etiquetas, revisión humana)**, mira [docs/v13/tareas_autor.md](../docs/v13/tareas_autor.md).
- Si te preguntan por **Cualquier cifra concreta (id, valor, capa, fecha)**, mira [output/v5/cifras_clave.csv](../output/v5/cifras_clave.csv).
- Si te preguntan por **Quién soporta el coste y dónde (atlas)**, mira [publicacion/atlas_descriptivo.md](../publicacion/atlas_descriptivo.md).
- Si te preguntan por **La base de datos única**, mira [docs/v10/diccionario_base.md](../docs/v10/diccionario_base.md).
- Si te preguntan por **Figuras y mapas**, mira [figuras/README.md](../figuras/README.md).
- Si te preguntan por **Web y monitor**, mira [web/README.md](../web/README.md).

## 6. Cómo se genera esto

Todo `consulta/` y `llms.txt` lo genera `make consulta` (src/consulta/generar.py) desde `output/`, `docs/` y `cifras_clave`; nunca se edita a mano. Las preguntas frecuentes están en [preguntas_frecuentes.md](preguntas_frecuentes.md), los términos en [glosario.md](glosario.md) y el mapa de ficheros en [indice_ficheros.md](indice_ficheros.md).
