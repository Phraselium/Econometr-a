# Limitaciones v3

**Limitaciones v3 heredadas de la revisión de la oleada 1.**
1. *Validación sellada de P-C3.* Los coeficientes de P-C3 con fianzas (topes y zonas) se calcularon una vez con todos los municipios, incluidos los sellados, antes de fijar el pre-registro. La validación sellada de P-C3 no es espacial sino por fuente (SERPAVI municipal, stock IRPF). Esa fuente mide el mismo mercado, en los mismos municipios y en el mismo periodo: no es una muestra independiente y su efecto esperado está atenuado. Un resultado C3 de P-C3 debe leerse con esta salvedad.
2. *Estimaciones de P-C1 conocidas.* Las estimaciones de P-C1 en la muestra no sellada se conocían al pre-registrar. Solo la evaluación sellada es confirmatoria.
3. *Exploración previa.* Antes de fijar el sellado se hizo un `describe()` global del tratamiento VUT, incluida la oleada 2026M05. Fueron estadísticos marginales, sin el resultado; la contaminación se considera baja.
4. *B2 (inmigración).* La población extranjera se mide por nacionalidad: las nacionalizaciones sesgan a la baja la entrada neta de nacidos fuera. Con el extremo lógico (1 persona por hogar), la cota de la cuota de ΣΔhogares es del 100 %: no es informativa.
5. *Traducciones a precio (B1, B2).* Son C4 condicionales a |ε_d|. No hay estimación verificada para España, y las formas reducidas citadas no son elasticidades de demanda.
6. *B4.* Sin suelo para uc, la cota de 2014-2021 no es finita. La conclusión sobre 2021-2025 depende del tipo nominal y de una ganancia esperada constante.
7. *A1.* Las ventanas C1 se añadieron después de ver qué fuentes había disponibles. Las cinco ventanas preespecificadas son C4 (una sola fuente de hogares). La EPA y la ECP no son plenamente independientes.
8. *Réplica de García-López et al.* El objetivo T depende de la razón entre VUT del INE y anuncios (rango 0,012-0,117 por pp). Esa razón se observa en una sola fecha (2025).

## Heredadas de la revisión de la oleada 2 (L-v3-W3)
1. *Estándar único para las traducciones a precio.* Tras la revisión (R4), toda traducción de una cota a precio que descansa en un supuesto estructural no estimado se trata como C4. Hay dos casos: la elasticidad ε para VUT e inmigración, y P/R = 1/uc para los tipos. Por eso V12 (tipos) pasa de PARCIALMENTE a SIN EVIDENCIA SUFICIENTE. Con el estándar alternativo, en el que ambas serían C2, V01 sería NO RESPALDADA (≤8,3 % de la subida) y V12, PARCIALMENTE. Se informa porque el veredicto depende de esa convención.
2. *«Probable pero no demostrado».* Es una sección exigida en el entregable, pero «probable» no es una capa de la escala: sus ítems son C4 y no deciden veredictos.
3. *P-D no modela costes* (fiscal, de suelo, de movilización, pérdida para propietarios, demanda turística desplazada). La dominancia y el mínimo arrepentimiento solo comparan efectos sobre el esfuerzo y la oferta, y favorecen mecánicamente a las dosis mayores.
4. *Familia de H3-1.* El único contraste confirmatorio fue el nacional. El sellado de las 6 ciudades, secundario, tiene signo opuesto (β = −0,0013, p = 0,20). Con ambas muestras en la familia (m = 5) no cambia ninguna conclusión.

## Heredadas de la revisión de la oleada 3
1. *Vacías.* La cifra total (3,8 millones) procede de una sola fuente: el Censo 2021, por consumo eléctrico. El reparto por tercil de presión se calcula sobre 277 municipios con dato y depende de la definición de presión (27,5-40,3 % en el tercil alto).
2. *VUT del INE.* Es una estadística experimental: la suma de secciones cubre ≈90 % del total publicado. Las oleadas son de meses distintos y tienen estacionalidad, así que las comparaciones solo son válidas entre oleadas del mismo mes.
3. *Terminadas del MIVAU.* Son de fuente única (certificados de fin de obra) y cubren menos que la variación del parque.
4. *Módulo València.* La ciudad y la provincia usan medidas de alquiler distintas (SERPAVI e IPC), y la ciudad y las secciones, periodos distintos (2020-2024 y 2021M08-2024M08). Las filas no son comparables entre sí.
5. *V05 y la ventana de A1.* El veredicto de V05 (PARCIALMENTE) depende de las ventanas C1 de A1, elegidas tras ver la disponibilidad de fuentes (limitación 7 de la oleada 1).
6. *Réplicas de García-López con 8-16 clústeres.* Las p sin ajustar pueden engañar: todas las p de Holm superan 0,04.
