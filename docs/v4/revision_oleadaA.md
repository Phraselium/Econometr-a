# Revisión independiente · v4 · puerta de la oleada A (M0, M1, M2)

Revisor independiente. Rama r4/main, HEAD del 2026-10-10. Alcance acotado por el encargo: capas, interpretación, neutralidad y coherencia entre módulos. No se ha reproducido el pipeline. Sí se han hecho comprobaciones puntuales de solo lectura sobre las tablas de salida y sobre una función de `src/v4/m1_run.py`.

## Veredicto: **REHACER**

Hay un error de código en M1 que invalida todas sus cifras de déficit (A1). Hay además un error de unidades que cambia dos veredictos de la convención B del verificador (A2). Y en M2 hay capas C1 que no cumplen el requisito de tener ≥2 fuentes independientes (A3). M0 se acepta, con correcciones de redacción (A8, A9).

## Cambios obligatorios, por orden de prioridad

### A1. M1: las terminadas MIVAU valen 0 en todas las combinaciones (error de código, crítico)
- Origen: en `terminadas_mivau()`, las columnas de `lib` y `pro` son cadenas (`'2021'`), pero en `deficit_provincial` se consultan con enteros: `lib.loc[terr].get(y)` con `y` entero devuelve `None`, y `np.nansum` da 0. Comprobado con `r.get(2021) -> None` y `r.get('2021') -> 701.0`.
- Consecuencia: en `M1_provincias_combinaciones.csv`, la columna `altas` de la ruta «MIVAU fin de obra» es 0 (con bajas = 0) en las 208 filas, en ambos periodos y con y sin protegida. El déficit de esa ruta es por tanto Δhogares + bajas: no resta ninguna terminada.
- Esto explica la pregunta de la puerta. El máximo nacional de 1,37 M es igual a ΔH(ECP) más las bajas al 0,2 %. Las ocho sumas nacionales (48 provincias) son 288 mil, 646 mil, 747 mil, 848 mil, 657 mil, 1.116 mil, 1.242 mil y 1.368 mil. Su mediana de 797 mil sale de combinaciones erróneas. **El rango 288 mil-1,37 M no es coherente con v3 ni con M0, y no debe usarse.**
- Mientras no se corrija y se vuelva a ejecutar, quedan invalidados: el déficit nacional 2012-2025 y 2021-2025, el top-10, la concentración (n50/n80), los excedentes provinciales y la asignación de capas por provincia (las 25 en C1 y 27 en C4 dependen del signo, y la ruta MIVAU es positiva por construcción).
- Hay que añadir una aserción que impida que se repita: altas MIVAU > 0 en cada provincia y año, y suma nacional de 2021-2025 dentro del ±1 % de la de M0 (434.765 en territorio común).

### A2. Verificador, convención B: error de unidades en V01 y V03; V11 sin tratamiento A/B
- **V01 (B = «NO RESPALDADA»)** compara una cota en Δln del alquiler (≤8,3 %) con el «50 % de la subida». La subida observada en el mismo periodo (2020M08-2024M08) es de 6,27 % (`b1_nacional_sensibilidad.csv`, `dlnR_obs_pct`). Con |ε_d| = 0,33, la cota admite el 133 % de la subida y `no_explica` vale 0. Solo con |ε_d| ≥ 0,75 la cota baja del 50 %. Con la propia regla, el veredicto B es «no concluyente» (depende de ε), no «NO RESPALDADA».
- **V03 (B = «PARCIALMENTE, no respaldada para compra»)**: la cota de compra en 2014-2025 es de 26,3 % en Δln, y la subida observada es de 33,2 % (`b2_nacional_sensibilidad.csv`). La cota admite el 79 % de la subida, no menos del 50 %. Para la compra, el veredicto B es «no concluyente».
- V12 sí está bien: en 2021-2025 el signo es contrario y en 2014-2021 la cota supera la subida.
- Hay que expresar todas las cotas B como fracción de la subida observada en el mismo periodo, usando las columnas `no_explica_*` que ya existen.
- **Ficha que falta:** V11 (simulación P-D con rangos de elasticidades y coste unitario como parámetro). Es una traducción a esfuerzo y precio que descansa en supuestos estructurales no estimados. Con la convención A estricta sería C4, pero figura como C2/PARCIALMENTE sin mostrar las dos convenciones. Hay que aplicarle A/B o justificar por escrito por qué no le corresponde.
- **Regla de capas:** la convención B no puede cambiar la capa. Debe rotularse como «lectura condicional a supuestos estructurales; la capa sigue siendo C4». El veredicto del verificador es el de A, como ya hace la cabecera.

### A3. M2: capas C1 sin dos fuentes independientes
- **M2-H0.** 2006-2007, 2008-2013, 2014-2019 y 2020-2025 están en C1, pero solo comparan «EPA hogares» con «padrón × tasas de jefatura EPA». Las dos dependen de la EPA y para esos años no hay ECP. No hay dos fuentes independientes, así que van a C4, o a C2 con el supuesto explícito. Solo 2021-2025 (EPA frente a ECP, 3,2 %) puede quedar en C1. Conviene anotar que la EPA se calibra con la población del INE.
- **Contradicción no tratada.** La única fuente externa que cubre 2011-2021, el censo (+456 mil), discrepa del total EPA corregido (+1.039 mil) en un factor de 2,3, y lo hace precisamente en el tramo de los periodos marcados como C1. M2 se limita a poner «C4 (no coinciden en 15 %)» y no lo interpreta. Hay que añadir una interpretación:
  - el Censo 2011 era muestral y está medido como viviendas principales; el Censo 2021 se basa en registros y mide hogares;
  - la EPA tiene la ruptura de 2021;
  - no se resuelve qué medida es correcta y se reportan ambas.

  Hay que enlazarlo con M1 2012-2025 (que usa la ruta censal) y con el signo indeterminado de v3 en 2012-2021.
- **M2-H2 (C1).** Eurostat `migr_imm1ctz` recibe sus datos del INE, así que no es independiente. Además, la serie del INE falta en 2006-2007, 2020-2025 y 2021-2025. Es C4, o C1 solo si se encuentra otra fuente.

### A4. M2: la corrección de la ruptura de la EPA de 2021 no es la declarada y corrige solo la mitad de un salto persistente
- `corrige_ruptura` multiplica todos los años t ≥ 2021 por k = √(h2020·h2022)/h2021. Si la ruptura es un salto de nivel persistente s (h = s·g desde 2021), entonces k ≈ s^(-1/2) y queda un salto residual de s^(1/2): se elimina la mitad del salto en logaritmos.
- En los totales de hogares pasa lo mismo. El ajuste `epa21 − ½(epa20+epa22)` ≈ S/2 se resta de forma permanente.
- El docstring dice «mismo criterio que v1 (Δ2021 := media de los Δ adyacentes)», pero el código no aplica ese criterio. El ajuste de M2 en 2020-2025 es de ≈190 mil, mientras que M0/v1 usa 242.400.
- Hay que fijar una sola definición (la variación 2020→2021 se sustituye por la media de las adyacentes, en log) y aplicarla en M0, M1 y M2. También hay que justificar k = 1,458 en el tramo 0-19.
- **Sensibilidad que debe ir al texto.** El componente de población extranjera es el 60 % de ΔH en 2020-2025 con la corrección y el 76 % sin ella (615.726/806.485). En 2021-2025 es el 56 % y el 58 %. Hay que reportar el rango, no solo la cifra corregida.

### A5. M1: ventanas, ruta «Censo anual» y criterio de C1
- **Ventanas mezcladas.** La ruta ECP usa 2021T1-2025T4 (si 2025T4 corresponde al 1 de octubre de 2025, son 4,75 años) contra 5 años de altas. La ruta «Censo anual» usa 1-ene-2021 a 1-ene-2025 (4 años). Las dos se mezclan en un único rango «2021-2025». Hay que homogeneizar las ventanas o rotularlas por separado.
- **Supuesto de hogares municipales.** «Hogares = personas / tamaño medio de 2021» está marcado como supuesto en el código, en las notas y en `M1-H-nacional`, pero **falta en los hechos municipales** (concentración y excedentes). Además, no es un supuesto neutro. Mantener constante el tamaño del hogar cuando este cae sesga ΔH a la baja: con las 48 provincias, ΔH de Censo anual es 646-667 mil frente a 1.116-1.169 mil de ECP. Según la regla de CLAUDE.md, esta ruta solo puede entrar en robustez, nunca en el rango principal ni en el criterio de C1. Hay que cuantificar el sesgo.
- **Independencia.** ECP y Censo anual son registros del INE derivados del padrón: no son dos fuentes independientes de hogares.
- **Criterio de C1.** «Mismo signo en todas las combinaciones» es más laxo que el ±15 % de M0 y admite rangos que varían en un factor de 4. Hay que armonizarlo con M0.
- Un déficit que depende de bajas supuestas es C2, como dice M0. C1 solo vale para los componentes triangulados.
- Las cuatro provincias forales quedan correctamente fuera de C1, por falta de Catastro.

### A6. Coherencia de las cifras de déficit entre módulos y fichas
- Hoy conviven tres versiones del mismo déficit 2021-2025:
  - V04 y V05: C1, 560-969 mil;
  - M0: «en niveles, con bajas, C2»;
  - M1: C1, 288 mil-1,37 M.
- Tras A1 y A5 hay que dejar una sola cifra con una sola capa. V05 debe pasar a C2 si incluye bajas supuestas, o separar el componente C1 (bajas = 0) de la cota C2.
- Hay que unificar qué significa «2021-2025» en M0, M1 y M2: 4 años, 4,75 o 5.
- **M0, conciliación.** La cadena cierra de forma aritmética: 866.100 − 55.164 − 53.679 − 56.323 = 700.934, y + 49.066 = 750.000. Pero el paso «medida de hogares: stock a 1 de enero frente a media trimestral» (−53.679) es en gran parte una diferencia de ventana. Del 1-ene-2021 al 1-ene-2026 frente a 2021T1-2025T4 falta aproximadamente un trimestre, que equivale a ~1/20 de 1,22 M, unas 61 mil. Por eso no se sostienen ni «periodo 0 por construcción» ni la conclusión «no por el periodo». Hay que rotularlo como «ventana (≈1 trimestre)».
- **Residuo frente al BdE.** Está bien declarado como no descomponible, con la fuente de hogares ECP marcada como inferencia y la cifra como NO VERIFICADA. Se mantiene.

### A7. Verificador: simetría de «NO ANALIZADA: FALTAN DATOS»
- **V13.** Los datos sí existen: precio, alquiler y las razones de A4 y A6, que ya se analizaron y discrepan. Lo que falta es el test (GSADF), no los datos. Con el mismo criterio que V14 («hay un hecho C1 sin diseño» → ANALIZADA), V13 sería «ANALIZADA, NO CONCLUYENTE». La alternativa es crear una tercera etiqueta, «NO ANALIZADA: ANÁLISIS NO REALIZADO», y aplicarla también a V10, cuyo motivo mezcla «faltan datos» con «el diseño no se realizó».
- V02 y V09 están bien clasificadas.
- **V04, literatura.** La referencia «Banco de España ... (DOI no comprobado)» debe pasar a «NO VERIFICADA».

### A8. M0, terminadas: independencia y umbral
- **Independencia.** La independencia es parcial y debe declararse. El alta catastral de una obra nueva suele apoyarse en la escritura de obra nueva o la declaración de alteración, que a su vez exigen el certificado final de obra. El documento de origen es común aunque el proceso administrativo sea distinto.
- **Contradicción interna.** Se dice «mide el aumento neto de unidades» y, a la vez, «no resta bajas». Una variación del stock es neta por construcción. Hay que corregirlo y explicar que la coincidencia de un flujo bruto (MIVAU) con un flujo neto (Catastro) puede deberse a que las regularizaciones compensan las bajas.
- **Umbral de ±15 %.** Es razonable como umbral declarado de antemano. Pero 2018 (−12,1 %), 2022 (+12,1 %) y 2025 (+14,9 %) están cerca del límite, y con las alineaciones alternativas 2018 y 2025 salen del conjunto. El núcleo robusto, presente en las tres alineaciones, es 2019-2024. Hay que marcar 2018 y 2025 como C1 frágil y añadir una sensibilidad con ±10 %.
- **Redacción.** Hay que eliminar «C1 de fuente única», que contradice la definición de C1.

### A9. M0, García-López: afirma algo más de lo que permiten los datos
- La estimación propia tiene p Holm = 0,27. Tras la corrección por multiplicidad, el signo negativo no se distingue de 0. Hay que reformular «el signo opuesto queda sin explicar» como «el coeficiente propio no es distinguible de 0 tras Holm; su IC95 sin ajustar excluye λT».
- «CUANTIFICADA y real» debe sustituirse por «cuantificada en una sola ciudad, con 3-12 diferencias anuales». En 2012-2016 la razón es negativa (−0,68) y las pendientes van de 0,07 a 0,46.
- «Apunta a heterogeneidad» debe pasar a «es compatible con heterogeneidad o con ruido: con estimaciones C4 no se distingue».
- El resto (capa C4, sin afirmar refutación ni confirmación) es correcto.

### A10. Latente M1/A2 frente a latente M2: son conceptos distintos y no se explican
- M1 parte de la convivencia con los padres (tasa de 2008) y obtiene 188-506 mil hogares implícitos. M2 parte de la jefatura de hogar por edad (tasa de 2008): +70 mil en 16-34 (EPA) y +211 mil en 20-34 (padrón).
- Miden cosas distintas: emanciparse no equivale a encabezar un hogar, por las parejas y los pisos compartidos. Además, M1 no compensa las demás edades. Los órdenes de magnitud se solapan (≈190-210 mil) y deben conciliarse en un párrafo común.
- M1 dice todavía que «M2 no estaba disponible»: hay que actualizarlo.
- «Sin latente neta» en M2 compensa el déficit juvenil con una jefatura mayor en 35-44 (−772 mil). Es una elección de agregación, no una medida de demanda insatisfecha. El titular debe darse por edades y la compensación neta debe ir como dato secundario. La magnitud de 35-44 debe contrastarse con la ruptura de 2021 (A4).

### A11. Neutralidad de la redacción sobre la inmigración (M2, estado.md)
- No se han encontrado términos valorativos ni causales en `output/v4/M0`, `M1` o `M2` ni en `estado.md`. La descomposición se presenta como contable (Shapley, C4).
- Aun así, «extranjeros 56 %» en `estado.md`, y cualquier frase del tipo «por efecto de la población extranjera», debe redactarse así: «componente de tamaño de la población de nacionalidad extranjera en la descomposición contable de ΔH (C4)».
- A esa frase deben acompañarla siempre:
  - el rango con y sin corrección de la ruptura (56-76 %, A4);
  - que «nacionalidad» no es «origen» (las nacionalizaciones trasladan población al componente nativo);
  - que la tasa de jefatura es común a ambos grupos;
  - que no mide flujos migratorios ni atribuye precios.

## Aspectos correctos
- **M0.** La cadena de v1 a la referencia de v3 cierra exactamente. El residuo frente al BdE está declarado como no descomponible. Δparque y BdE se descartan correctamente como fuentes no independientes. La contaminación de H3-3 (V06 y V07) queda bien declarada sin promover de capa.
- **Verificador.** La separación en dos veredictos está implementada solo sobre las fichas que antes eran «SIN EVIDENCIA SUFICIENTE». V12 está bien aplicada con las dos convenciones.
- **M1 y M2.** Los supuestos de la latente (tasa de 2008, 1,5-2,0 personas por hogar joven, la misma brecha en todas las provincias) son explícitos, como corresponde a C2. Los componentes de M2 están en C4 por tener la jefatura una sola fuente: es correcto.

## Comprobaciones realizadas (solo lectura)
- Suma de la cadena de M0.
- Lectura de `b1_nacional_sensibilidad.csv`, `b2_nacional_sensibilidad.csv` y `b4_periodos.csv` (v3/PB).
- Agregación de `M1_provincias_combinaciones.csv` por ruta, fuente y bajas.
- Inspección del tipo de las columnas de `terminadas_mivau()`.
- Lectura de `corrige_ruptura` y `total_dH` en `m2_run.py`.
- Búsqueda de léxico causal y valorativo.
