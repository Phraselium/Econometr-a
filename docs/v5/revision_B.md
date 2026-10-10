# Revisión independiente · Módulo B de v5 (necesidades y territorio)

Fecha: 2026-10-10. Revisor independiente: no hizo el trabajo. Objeto: output/v5/B1-B4 y src/v5/b*_*.py.
No se ha reejecutado `make all` ni se ha leído data/sealed.

## Comprobaciones realizadas
- **Reproducibilidad.** b1_run, b2_run, b3_run, b4_run y cifras_clave se ejecutan sin red (HTTPS_PROXY=http://127.0.0.1:9) y salen con código 0. Hay dos ejecuciones con md5 idéntico en los 58 ficheros de output/v5/B1-B4 y en cifras_clave.csv, y los ficheros son además idénticos byte a byte a los versionados (`git status` limpio).
- **Lecturas de ficheros.** Las lecturas trazadas con strace (36 ficheros) están todas versionadas. Ninguna toca data/sealed.
- **Comprobaciones automáticas.** `check_texto` da 0 errores, `check_v5` da 0 errores y `ruff` pasa.
- **Pre-registro.** El tag `prereg-v5` (8803f04, 19:11) es anterior a la potencia (6bb37f5, 19:16), que solo contiene b3_data.py y b3_potencia.py; b3_potencia.py no lee la variable dependiente. Las estimaciones de B3 se versionan después (a5e998b, 19:22).
- **Holm.** Holm sobre 8 familias × Y1 × P1, recalculado con statsmodels: coincide.
- **BH.** BH sobre las 40 exploratorias, recalculado sobre p_mayor: coincide (error máximo 1e-15).
- **Resto del pre-registro.** Se cumplen Conley a 100 y 200 km con el mayor p, Freedman-Lane con 5.000 permutaciones y un multiverso de 32 especificaciones (2 periodos × 2 fuentes × pesos Bartik 2011/2015 × con o sin grandes × HC3/c200).
- **Sumas.** La suma provincial coincide con la nacional en B1 (10 tablas, incluida la necesidad total) y en B2 (5 tablas).
- **Capas.** Ningún resultado es C3. Las capas de los totales son la mínima de sus componentes: C4 en B1, B2, B3 y B4; F es C2.

## Valoración por criterio
- **B1.**
  - El método stock-flujo es coherente y las cotas están bien construidas: los extremos se combinan con el signo correcto (b1_run.py:281-283).
  - No hay doble cómputo entre A1 y A2. A1 son hogares formados en 2021-2025 menos terminadas; A2 son hogares no formados respecto a las tasas de 2008. Las personas no solapan.
  - F (desde el 1-ene-2026) y A1 (hasta 2025T4) no solapan en el tiempo.
  - No restar L es correcto: la proyección de hogares del INE es neta de disoluciones. La variante literal se da aparte.
  - La vacancia del 2-4 % se declara como supuesto del encargo, aunque la etiqueta de la referencia es incorrecta (n.º 5).
- **B2.**
  - Los supuestos son explícitos.
  - El signo es «indeterminado» cuando el rango cruza 0 (b2_run.py:165, 274).
  - Es C4.
  - El retardo es discutible (n.º 7).
- **B3.**
  - Cumple el pre-registro y declara 10 desviaciones.
  - Se presenta como «descriptivo honesto» con un EMD de 0,62 DT.
  - El aviso de F4 está en desviaciones.md y en B4-V3.
  - La convergencia necesita mostrar el control (n.º 3).
- **B4.**
  - «No estable» se sostiene sobre todo en la discordancia M1 frente a M2 dentro de v2 (τ = 0; 0; 0,33 en compra).
  - Nada es C3.
  - Los veredictos de las fichas («ANALIZADA, NO CONCLUYENTE») son coherentes con C4.

## Hallazgos

| N.º | Tipo | Fichero:línea | Hallazgo | Corrección |
|---|---|---|---|---|
| 1 | **Bloqueante** | src/v5/b4_run.py:324, 327, 337, 343, 346 (→ output/v5/B4/fichas_verificador.json) | Lenguaje causal o de efecto en capa C4: «la población extranjera **puede explicar** como máximo el 45,2 %», «la demografía **contribuye** −3,0 a −4,1 pp», «la oferta contemporánea **contribuye**», «caída del coste de uso **permite** como máximo», «**el efecto** sobre precio», «**el efecto** de los tipos se fija en 0», «**el efecto** común de los tipos». check_texto no lo detecta. | Redactar en términos contables o de asociación, por ejemplo: «la población extranjera representa como máximo el 45,2 % de la creación de hogares (cota de cantidad)», «contribución contable de −3,0 a −4,1 pp (no es efecto)», «la cota de coste de uso es compatible con hasta +23,5-78,0 %», «la asociación con el precio», «el componente de tipos se fija en 0». Añadir estos patrones a check_texto. |
| 2 | **Bloqueante** | src/v5/b4_run.py:331 frente a 151 y 330 | La ficha B4-V2 se contradice: el intervalo dice «precio ≤1,2-8,3 %», mientras que la magnitud y la nota de la línea 151 dan ≤2,7-8,3 % para \|ε_d\| entre 1,0 y 0,33. | Generar intervalo y magnitud a partir de la misma variable (no con texto fijo) y corregir la cifra. Hacer lo mismo con el resto de cifras escritas a mano en las fichas de b4_run.py:320-350. |
| 3 | **Bloqueante** | output/v5/B3/hechos.json (B3-H-B3-6-b/-p); src/v5/b3_salidas.py:94 | H-B3-6 aparece en hechos y en cifras_clave como rechazada (Holm 0,0013; −16 por DT) sin el control de error de medida. Con el precio inicial de Registradores, b = −0,090 por DT y el p principal (el mayor de HC3 y Conley) es 0,058, es decir, no significativo a α = 0,05 sin ajustar (p de permutación 0,016). La advertencia de resultado.json remite a «hip['H-B3-6']», una variable interna, en lugar de dar las cifras. | Añadir a hechos.json un hecho «H-B3-6 con precio inicial de Registradores» (b, p_mayor 0,058, p_perm 0,016), con nota en las entradas de H-B3-6, y escribir en la advertencia: «el coeficiente se reduce a la mitad y deja de ser significativo con el criterio principal; la convergencia no es robusta al error de medida». |
| 4 | No bloqueante | output/v5/B1/metodo.md:1-5 | El método tiene 5 líneas: le faltan la definición de cada componente, la matriz de solapamientos (está en tablas/B1_atraso_solapamientos.csv) y el motivo de no restar L. | Ampliarlo con una tabla de componentes (definición, fuente, fecha, capa, solapamiento) y el argumento sobre F y L. |
| 5 | No bloqueante | src/v5/b1_run.py:502 (→ fichas B1-V1) | «Gabriel y Nothaft (2001) … VERIFICADA (Crossref), cuartil no verificado». Según CLAUDE.md, VERIFICADA exige DOI y cuartil Scimago. | Rotular «NO VERIFICADA (DOI Crossref comprobado; cuartil no verificado)» o añadir el cuartil Scimago. |
| 6 | No bloqueante | src/v5/b1_run.py:34, 215-228 | V suma vacancia friccional en provincias con presión mientras M supone que entre el 70 % y el 90 % de los 3,83 M de vacías siguen vacías. El comentario «0 si ya hay ≥ objetivo» no se implementa: V_min = 0 en todos los casos. | Documentar que V se refiere al alquiler disponible y no al stock vacío censal, o implementar la condición. |
| 7 | No bloqueante | src/v5/b2_run.py:41-44, 115-118 | El retardo (3,2 años) iguala iniciadas y terminadas acumuladas desde 1991. Mezcla el retraso con las obras iniciadas y nunca terminadas (2008-2012), que lo sesgan al alza. | Declararlo en metodo.md y añadir una variante que empiece la acumulación en 2014. No cambia el signo nacional (empeora en los 3 escenarios). |
| 8 | No bloqueante | src/v5/b1_run.py:156-158 frente a src/v5/b2_run.py:86 | El déficit de partida es distinto en B1 (A1 = mediana de A4, 788.153) y en B2 (D2025 con bajas 0, 700.934). No se explica. | Explicar la diferencia en ambos metodo.md o usar la misma base. |
| 9 | No bloqueante | src/v5/b3_run.py:398; src/v5/r1b_sens.py:80 | Oster: 1,3·R² = 1,18 se acota a Rmax = 1,0. No figura en desviaciones.md. La potencia supone K = 12 y el modelo tiene 13 regresores. | Añadir ambas cosas a desviaciones.md (el veredicto «descriptivo honesto» no cambia: el EMD sube). |
| 10 | No bloqueante | output/v5/B4/hechos.json (B4-b3-shapley-residuo) → cifras_clave.csv:85 | El valor es NaN y se propaga a cifras_clave como celda vacía. | Calcular el central (1 − suma de cuotas) o excluir el hecho. |
| 11 | No bloqueante | output/v5/B4/hechos.json y estabilidad.csv | Etiquetas de periodo «2015-2019 / 2019-2025» para ventanas v2 de 2014Q1-2019Q4 y 2020Q1-2024Q1. «B3_transversal_coef 2019-2025» corresponde a P2 = 2021-2025. | Usar en el id la ventana real. |
| 12 | No bloqueante | output/v5/B4/estabilidad.csv; b4_run.py:193-227 | La τ mezcla comparaciones entre estimandos distintos (cuota de R² transversal frente a contribución temporal), cuya discordancia es esperable, y ordena por valor absoluto mezclando signos. | Dar por separado la τ dentro de cada método (M1 frente a M2), que es la que sostiene «no estable», y declarar que el orden es por \|valor\|. |
| 13 | No bloqueante | docs/v5/decisiones.md | Faltan las secciones de B2 y B4 (retardo, escenarios, umbral τ = 0,67). | Añadirlas. |
| 14 | No bloqueante | output/v5/B2/hechos.json (B2-H6) | Los campos valor/min/max se usan para contar empeora, mejora e indeterminado. | Separarlo en tres hechos. |
| 15 | No bloqueante | output/v5/B3/resultado.json (notas) | `notas` es una cadena, no una lista. | Convertirla en lista. |
| 16 | No bloqueante | src/v5/b1_run.py:505 | Hay un anglicismo («ranges no son IC»). | Escribir «rangos». |

## Veredicto: **REHACER**

Hay que corregir tres bloqueantes concretos y de bajo coste:
1. Quitar el lenguaje causal de las fichas de B4.
2. Corregir la cifra contradictoria de B4-V2.
3. Incluir en hechos y fichas el control de error de medida de H-B3-6.

El método de B1-B3, el pre-registro, Holm/BH y la reproducibilidad están correctos. Los no bloqueantes pueden ir en la misma pasada.
