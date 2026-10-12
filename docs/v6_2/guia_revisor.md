# Guía para el revisor externo (v6.2)

**Autor:** Borja Romero, economista (firma individual e independiente).

**Versión:** 6.2 (cierre para revisión externa).

**Tiempo estimado de lectura:** 2-3 horas para lo esencial (secciones 1-4) y medio día para reproducir y contrastar cifras.

## 1. Qué es el proyecto

Investigación reproducible sobre la vivienda en España, con un único repositorio y datos públicos oficiales. Cubre cuatro bloques:
- **Hechos** sobre hogares, viviendas terminadas, precios y alquileres.
- **Cotas** sobre el déficit y la demanda latente.
- **Contabilidades** de necesidad por provincia para 2026-2035.
- **Análisis exploratorios** de qué variables se asocian con el alquiler y la compraventa, y de qué modelos predicen mejor, con validación sellada.

Tiene además un **verificador** de afirmaciones del debate público. Evalúa afirmaciones e instrumentos, nunca partidos ni personas.

Cada resultado lleva una **capa de evidencia**:

| Capa | Qué significa | Ejemplo |
|---|---|---|
| C1 | Hecho con dos o más fuentes independientes que coinciden (±15 %) | Viviendas terminadas al año, variación del precio de compra |
| C2 | Cota con supuestos explícitos | Déficit 2021-2024, según cómo se corrija el salto de la EPA |
| C3 | Efecto identificado | Ninguno alcanzado |
| C4 | Exploratorio, de una sola fuente o de un modelo | Necesidad 2026-2035, asociaciones con inmigración, comparación de modelos |

Reglas que el revisor puede comprobar:
- **Sin lenguaje causal por debajo de C3.** Las importancias de modelos (SHAP, PIP) nunca se leen como efectos.
- **Cifras con un solo origen.** Toda cifra de un entregable sale de `output/v5/cifras_clave.csv`, con periodo, fuente, fecha del dato y capa.

## 2. Qué se afirma (y con qué capa)

El resumen de una página es `output/v5/una_pagina.md`. Lo que se puede y no se puede afirmar está en `output/v5/lo_que_sabemos.md`. Las cifras aptas para difusión, y las que no deben citarse fuera de contexto, están en `docs/v6_2/cifras_publicables.md`.

Las afirmaciones centrales son:
1. **Hogares y terminadas.** Entre 2021 y 2024 los hogares crecieron más que las viviendas terminadas [C2]. El signo lo confirman dos fuentes de hogares (EPA, ECP) y dos de terminadas (Ministerio, Catastro). La cuantía es una cota porque depende de cómo se corrija el salto metodológico de la EPA en 2021 (`output/v6_2/L3/deficit_alternativas.md`).
2. **Precios y alquileres.**
   - El precio de compra y el alquiler de los contratos vigentes subieron [C1].
   - Los contratos nuevos suben más que los vigentes donde hay datos (Cataluña y Comunitat Valenciana) [C1].
3. **Necesidad 2026-2035.** Es una contabilidad con supuestos [C4] y nunca resta las viviendas liberadas por envejecimiento, porque la proyección del INE ya las descuenta.
4. **Inmigración** [C4, «analizada, no concluyente»].
   - La asociación total, sin controlar por población, es positiva.
   - La asociación directa, a igual población, no lo es. Pero controlar por población es un mal control: la población crece por la propia inmigración.
   - No se afirma ningún efecto.
5. **Modelos.** Frente a la línea base más exigente, los modelos de árboles predicen mejor en 6 de 9 tareas, sobre todo el alquiler de stock [C4]. Predecir no es explicar.

## 3. Dónde mirar primero

| Para… | Fichero |
|---|---|
| Reconstruir una cifra sin leer código | `output/v6_2/anexo_metodologico.md` (una ficha por cifra; L2 lo validó con 15 de 15 reproducidas a ciegas) |
| Ver todas las cifras con su capa y fecha | `output/v5/cifras_clave.csv` |
| Ver qué cambió entre versiones y por qué | `docs/v6_1/historial_conclusiones.md` (con las adendas v6.2) |
| Auditoría de código y estadística | `docs/v6_1/auditoria.md`, `docs/v6_1/doble_implementacion.md`, `output/v6_2/L2/comparacion.csv` |
| Erratas (cifras publicadas que cambiaron) | `ERRATA.md` |
| Informe técnico y working paper | `output/v5/informe_tecnico.md`, `output/v5/working_paper.md` |
| Pre-registro y validación sellada | `docs/v6/hipotesis.md`, `docs/v2/holdout_accesos.md`, `output/v6_1/K1/tabla_modelos_k1.md` |
| Mapa del repositorio | `docs/MAPA.md` |

## 4. Cómo reproducir

En una orden, sin red: `make all`. Tarda unas 2 h en un solo hilo; los tiempos medidos están en `README_REPLICACION.md`. Las comprobaciones de puerta se lanzan con `make check`, en unos 6 min, y cubren:
- léxico valorativo o causal;
- cifras fuera de marcador;
- sumas provinciales;
- la integridad del sellado;
- los tests de cifras;
- la doble implementación de `tests/doble_impl`.

Dos ejecuciones de `make all` en un clon limpio dan ficheros idénticos (md5), salvo los tiempos de ejecución.

## 5. Objeciones ya recibidas y respuesta

En v6.1 hubo una revisión por pares simulada con dos árbitros: uno académico y otro de política pública. La hicieron agentes de IA, **no sustituye a la suya**. Los documentos son `docs/v6_1/informe_arbitro_academico.md`, `docs/v6_1/informe_arbitro_politica.md` y `docs/v6_1/carta_respuesta.md`, con una adenda de v6.2.

| Objeción | Respuesta |
|---|---|
| A-01: la capa C1 del déficit dependía de una corrección constante de la EPA | Recalculado con siete correcciones alternativas: pasa a cota C2 (ERRATA) |
| A-02/A-03: validación sellada con 11 provincias, segunda mirada a la muestra | Permutación exacta, DM por periodo y rótulo «frágil»; la muestra nueva queda en limitaciones |
| P-02/P-03: riesgo de citar cifras fuera de contexto | Recuadro «cómo citar» y la lista de cifras publicables; un test impide citar cifras superadas |
| P-05/A-07: lenguaje de mecanismo e inmigración | Lenguaje asociativo; separación entre asociación total y directa |

## 6. Preguntas concretas para el revisor

1. **Déficit.** ¿Le parece adecuada la cota C2, que combina siete correcciones del salto de la EPA más la constante de v1? ¿Excluiría las dos variantes que conservan el salto? Sin ellas, el rango se estrecha (L3-DEF-2124-SENS). ¿Añadiría el Censo 2021 como ancla?
2. **Aumento de hogares 2021-2025.** El aumento de hogares (C1) usa la EPA sin corrección, porque las medias de 2021 y 2025 son posteriores a la ruptura, y la compara con la ECP, un stock a 1 de enero. ¿Le parece aceptable mezclar una diferencia de medias anuales con una de stocks?
3. **Necesidad 2026-2035.** ¿Son razonables los componentes A+R+V+F−M−K y sus rangos? ¿Falta alguno o hay doble cómputo con la proyección del INE?
4. **Inmigración.** ¿Es correcta la lectura de la asociación total frente a la directa? ¿Hay un diseño identificable con datos públicos que debiéramos intentar?
5. **Validación sellada.** ¿Es suficiente la comparación con la línea base más exigente (AR con factor común, efectos fijos, crecimiento nacional) para decir «predice mejor»?
6. **Traslado de ayudas (D1).** ¿La rejilla de elasticidades (0,3-1,5) es defendible para España, o debe presentarse solo como ilustración?
7. **Comunicación.** ¿Hay alguna frase de los entregables de difusión (una página, policy brief, artículo del Colegio) que pueda leerse como causal o partidista?
8. **Reproducción.** ¿Pudo reconstruir con el anexo al menos tres cifras de su elección?

Envíe sus comentarios con referencia a fichero y línea. Las respuestas se incorporarán a una carta pública y a ERRATA si cambian cifras.
