<!-- Generado por `make publicacion` desde docs/v7_1/guia_revisor.md. No editar a mano: se regenera y un test lo comprueba. -->

# Guía para el revisor externo (versión pública 2.0; déficit y necesidad: versión interna v7.2)

**Autor:** Borja Romero, economista (firma individual e independiente).

**Versión del documento:** v7.1 (versión interna, con las correcciones de v7.2). La v6.2 queda como histórica. La correspondencia entre versiones internas y la versión pública 2.0 está en CHANGELOG.md.

**Tiempo estimado:**
- 2-3 horas para lo esencial (secciones 1-4);
- medio día para reproducir y contrastar cifras;
- una hora más para la nota metodológica.

## 1. Qué es el proyecto

Es una investigación reproducible sobre la vivienda en España, con datos públicos oficiales y un único repositorio. Tiene cinco bloques:
- **Hechos.** Hogares, viviendas terminadas, precios y alquileres.
- **Cotas.** Déficit y demanda latente.
- **Contabilidades.** Necesidad por provincia para 2026-2035.
- **Análisis exploratorios.** Asociación y predicción, con validación sellada.
- **Atlas regional de V7.** Paneles de las 17 comunidades autónomas, modelos congelados para una validación diferida y simulaciones condicionales de instrumentos, con dosis y coste.

Un **verificador** evalúa afirmaciones del debate público. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas.

**Capas de evidencia.** Las definiciones están en metodologia/capas.md: C1 hechos, C2 cotas, C3 efectos (ninguno alcanzado) y C4 exploratorio. Hay dos reglas que puede comprobar directamente:
- **Cifras con un solo origen.** Toda cifra difundible sale de publicacion/cifras_clave.csv, que es copia de output/v5/cifras_clave.csv. Un test de `make check` lo vigila.
- **Sin lenguaje causal por debajo de C3.** Esto incluye SHAP, importancias, descomposiciones y simulaciones de política.

## 2. Qué se afirma y con qué capa

Lectura mínima, en este orden:
1. publicacion/una_pagina.md
2. publicacion/lo_que_sabemos.md
3. publicacion/que_cambio.md, la sección única sobre qué cambió entre versiones y por qué.

Afirmaciones centrales:
1. **Hogares y terminadas** [C2]. Entre 2021 y 2024 los hogares crecieron más que las viviendas terminadas. La cuantía es una cota que depende de la corrección del salto de la EPA en 2021.
2. **Precios y alquileres** [C1]. Subieron. Los contratos nuevos suben más que los vigentes donde hay datos.
3. **Necesidad 2026-2035** [C4]. Es una contabilidad con supuestos. Nunca resta las viviendas liberadas por envejecimiento.
4. **Inmigración** [C4, «analizada, no concluyente»]. La asociación total es positiva y la directa no lo es. No se afirma ningún efecto.
5. **Predicción** [C4]. Frente a la base más exigente, los modelos predicen mejor solo en parte de las tareas, provinciales y regionales. Predecir no es explicar.
6. **Atlas regional (V7)** [C4].
   - El componente común domina la variación regional.
   - No se confirma ningún largo plazo regional.
   - En la simulación de traslado, las ayudas a la demanda y la rebaja de ITP/IVA reducen el precio neto del beneficiario y suben el precio de mercado. El signo lo fija la fórmula; lo informativo es la magnitud relativa.
   - Cada instrumento declara su dosis y su coste. Cuando no hay base, el coste figura como «no estimable».

## 3. Dónde mirar primero (estructura v7.1)

| Para… | Ruta |
|---|---|
| Elegir un itinerario de lectura según el perfil | LEEME_PRIMERO.md |
| Todo lo vigente, generado y nunca editado a mano | publicacion/ (con su MANIFIESTO.md) |
| Reconstruir una cifra sin leer código | metodologia/anexo_metodologico.md |
| Definiciones de capas, historial de conclusiones, validación Monte Carlo y pre-registro de V7 | metodologia/ |
| Nota metodológica sobre estimadores de panel con un factor común no estacionario | publicacion/nota_metodologica.md |
| Atlas regional: una ficha por CCAA, resumen y Excel | publicacion/atlas_regional/ |
| Dosis y coste de las simulaciones | metodologia/dosis_coste.md y publicacion/dosis_coste.csv |
| Reproducción, entorno, tiempos y protocolo de la evaluación diferida | reproducir/ |
| Versiones superadas | historico/INDICE.md |
| Erratas | ERRATA.md |

## 4. Cómo reproducir

Las órdenes se lanzan sin red, en un solo hilo y con SEED = 20261010:
- `make all`: v1-v6.3, unas dos horas.
- `make v7`: atlas regional y V7.1, unos 50 minutos.
- `make publicacion`: regenera publicacion/, metodologia/ y reproducir/ en segundos.
- `make check`: ruff, tests, control de texto, cifras y capas; unos 6 minutos.

Dos ejecuciones en un clon limpio dan ficheros idénticos (md5), salvo los tiempos de reloj. El ensayo de la evaluación diferida con datos simulados está en reproducir/ensayo_evaluate_v7.md.

## 5. Objeciones ya recibidas y respuesta

La revisión por pares de v6.1 y las revisiones de V7 las hicieron agentes de IA. **No sustituyen a la suya.**

| Objeción | Respuesta |
|---|---|
| A-01: el C1 del déficit dependía de una corrección constante | Se pasó a cota C2 con siete correcciones alternativas (ERRATA) |
| A-02/A-03: validación sellada pequeña, segunda mirada a la muestra | Permutación exacta y rótulo «frágil». En V7, validación limpia diferida con modelos congelados (2027) |
| A-09: publicar las ecuaciones del método de traslado | Publicadas (output/v7/R6/metodo.md y el anexo de ecuaciones del atlas) |
| P-10: costes y magnitudes por euro | V7.1-S1: coste donde hay base y «no estimable», con su motivo, donde no la hay |
| Revisión de R2 (V7): ningún estimador era apto con un factor común I(1) | Regla de triangulación entre estimadores y magnitudes en rango (nota metodológica, §4) |
| Revisión de R4 (V7): inferencia de φ sin valor crítico válido | Valor crítico simulado. Las φ regionales se publican sin inferencia |

## 6. Preguntas concretas para el revisor

1. **Déficit.** ¿Es adecuada la cota C2? ¿Excluiría las variantes que conservan el salto de la EPA?
2. **Necesidad 2026-2035.** ¿Faltan componentes o hay doble cómputo con la proyección del INE?
3. **Nota metodológica.** ¿El diseño Monte Carlo (escenario F: factor común I(1) con cargas heterogéneas) es representativo de los paneles regionales de vivienda? ¿Cambiaría el criterio de aptitud (sesgo de hasta el 10 % y cobertura de 0,90 a 0,98)?
4. **Regla de triangulación.** ¿Es razonable exigir el mismo signo en MG con demeaning, PMG con demeaning y CS-DL, y publicar la magnitud como rango?
5. **Componente común.** El R² frente a la media de las 17 CCAA es descriptivo e incluye a la propia comunidad. ¿Prefiere otra medida, como las cargas de un factor estimado, aunque sea un modelo nuevo?
6. **Dosis y coste.** ¿Es correcta la normalización: efecto por cada 10.000 viviendas en los instrumentos de cantidad y por cada 100 M€ anuales en los de coste? ¿Conoce un coste unitario verificable de la vivienda pública o de la movilización de vacías que permita completar la tabla?
7. **Evaluación diferida.** ¿Le parece correcto el protocolo de reproducir/evaluacion_2027.md, incluida la sensibilidad del alquiler sin 2026T3?
8. **Comunicación.** ¿Hay alguna frase de los entregables de difusión que pueda leerse como causal o partidista?
9. **Reproducción.** ¿Pudo reconstruir con el anexo al menos tres cifras de su elección?

Envíe sus comentarios con referencia a fichero y línea. Las respuestas se incorporarán a una carta pública y, si cambian cifras, a ERRATA.
