# V18 · Plan de replicación (B1): pre-registro interno

Documento de la fase 3 de V18 (docs/v18/plan.md, secciones B1 y D, fase 3). Redactado el 2026-10-20 por el agente de la fase 3 para el autor (Borja Romero), antes de cualquier estimación de V18 con nuestros datos. Sigue el estilo de un Documento de Trabajo del Banco de España: cada especificación tiene un identificador estable (V18-E3-R1, V18-E3-A1...), y el código y las salidas de la fase 4 irán en src/v18/estimacion/ y output/v18/estimacion/. check_v18 comprueba que esos ficheros entran en git después del commit etiquetado.

Convenciones:
- **R** es la réplica de la especificación original, en el periodo y el territorio más parecidos.
- **A** es una ampliación (periodo, territorio, escala o resultado). Cada A es una especificación separada.
- **L** es una magnitud que sale solo de la literatura.
- **X** es una especificación declarada NO ESTIMABLE.

Las cifras de los estudios proceden de sus fichas de la fase 1 (docs/v18/bib/<factor>/<clave>.md), que se citan en cada caso. Las cifras ya vistas del proyecto proceden de output/v17/lectura_bde/tabla_comparativa.md y de los informes de V8, V9, V15 y V16 que se citan.

---

## 0. Preámbulo

### 0.1 Naturaleza del documento
- **Es un pre-registro interno, sin sello externo.** Lo fija la etiqueta git local `plan-replicacion-v18`. La puerta de la fase 4 exige además que el commit de la etiqueta esté en la rama remota (docs/v18/decisiones.md, K1). No es un pre-registro depositado (OSF u otro) y no debe describirse como tal.
- **Revisión.** Antes de etiquetarlo lo revisan revisor-preregistro y abogado-del-diablo. Su respuesta irá en una adenda (docs/v18/plan_replicacion_adenda.md), que **prevalece donde difiera**.
- **Lo hecho con datos antes de este documento.** No se ha estimado ningún efecto de V18 con nuestros datos. Sí se ha hecho lo siguiente:
  - el inventario de variables por estudio (fase 0), que solo lee manifiestos y nombres;
  - las fichas bibliográficas (fase 1);
  - tres reproducciones con los paquetes de sus autores, sin datos del proyecto (fase 2: Chaves-Fonseca 2026, Mense 2025 y Borusyak-Hull-Jaravel 2022; las tres «coincide», docs/v18/reproduccion.md).
- **Desviaciones.** Toda desviación de este plan irá a docs/v18/desviaciones.md con fecha y motivo, antes de mirar el resultado afectado.
- **Datos nuevos.** Las fuentes abiertas que el inventario de la fase 0 marca como «falta, no requiere al autor» (Censo de 2001 por nacionalidad, OpenStreetMap, Google Trends, Open Data BCN, afiliación por sector, tipos de cambio, fechas de las leyes del ITP, recaudación del ITP, renta de los hogares por provincia, hogares por provincia, Atlas de Áreas Urbanas) se descargan después de la etiqueta. Llevan la marca `posterior_prereg`. Su adquisición se limita a descargar, normalizar y auditar la calidad, sin cruzarlas con ningún resultado. Si una no puede descargarse, la especificación que la necesita pasa a NO ESTIMABLE y se anota en docs/v6/fuentes_fallidas.md.

### 0.2 Lo que ya se ha visto (y por qué parte del trabajo es a posteriori)
El proyecto ya ha estimado casi todos los factores de la sección E con estos mismos datos. Las réplicas de V18 no son, por tanto, primeras miradas. La tabla resume lo visto y su cifra principal.

| Factor | Ya visto en el proyecto (cifra principal y fuente) | Qué parte de V18 es a posteriori |
|---|---|---|
| E1 Turismo | H3 (V15): 0,0030 % de alquiler por desviación típica intra-sección, p = 0,931. Q2a (V16): 0,0132 por DT en el IPC de alquiler provincial (herramienta NO APTA, solo puntual). Q2c: −0,0054 por DT. Q2b (Andalucía): mediana 0,0002. V9-D2: asociación positiva tras la reapertura, pretendencias rechazadas. V9-D3: descriptivo. v3, v6 y V8: «no concluyente». V17 B4: 1,0-2,1 % del alquiler a escala nacional (ilustración con García-López et al.) | E1-A1 a E1-A3 (secciones de toda España con INE-VUT y SERPAVI 2021-2024) repiten la exposición y el resultado de H3 y Q2. Es nuevo el periodo 2011-2019 de Barcelona con SERPAVI (E1-R3) y el instrumento de E1-R2 |
| E2 Topes | V9-D1b (Ley 11/2020): renta de contratos nuevos −5,9 % (M̄ de ruptura 0,5; C4). V9-D1a: −5,8 %, pretendencias rechazadas. Contratos de V9: sin diferencia detectable. H1 y H2 de V15 en entrenamiento (zonas de 2024): H1-CS −7,18 %, H1-SDID −3,64 %, H2-CS −4,22 %, H2-SDID −14,16 %, H2-PPML −9,95 %, pendientes de evaluación sellada. Q1c (V16): −0,048 en compraventas. V17 B4: −4,9 % | E2-R1 repite V9-D1b con el mismo Incasòl. E2-A1 y E2-A2 repiten H1 y H2 en entrenamiento (no sustituyen a su evaluación sellada). Es nuevo el análisis por tramo de E2-R2 |
| E3 Inmigración | V9-D4: F efectivo de 3,4 a 4,6; réplica 2003-2012 con IPC de alquiler 0,0072 y con valor tasado −0,0029; ampliación 2015-2022 0,0153 y 0,129 (puntuales). H4 (V15): 0,305 % de alquiler por punto de población extranjera, p = 0,259 (AKM0). Q3-c1: 0,0119 log del valor tasado por punto (puntual). Q3-c2: −0,0282 en compraventas. Q3-b: 0,0091 por DT en secciones, con pretendencia placebo del 56 %. V17 D3: la migración neta explica el 128 % del crecimiento de la población 2015-2026 | Casi toda E3: V9-D4 ya intentó la réplica de González y Ortega con cuotas del padrón de 2003. Es nuevo el año base (Censo de 2001) y las dos ventanas originales |
| E4 Ayudas | V9-D6: no estimable. Q7a (V16): −0,120 en el log del alquiler, con placebos del mismo orden. V17: traslación mediana del 46 % (41-65 %) en la literatura | Todo. No se estima nada nuevo |
| E5 Oferta y suelo | Q4a (V16): −0,1297 por DT de Red Natura (no exógena). Q4b: −0,0014. P1 de V15, descartada. V17 D3: suelo como freno en Barcelona | La elasticidad provincial con Bartik de empleo (E5-R1) es nueva. Ningún resultado del proyecto usa ese instrumento |
| E6 Obra nueva | V17 B4: −0,37 a −0,63 % del alquiler medio (ilustración con Mense, 2025). E2 de V15: correlaciones obra nueva-alquiler | Es nuevo el diseño por distancia (E6-R1) |
| E7 Tipos | Q5 (V16): −0,51 % por DT de sorpresa a h = 4, con F de la primera etapa de 2,1 a 2,9. V8 H8-5 a H8-7: LP-IV con instrumentos débiles y primera etapa de signo contrario. Descomposición SVAR de V8 (crédito y tipos, C3s). V9-D5: tipo variable × choques, sin potencia. V17 B4: −5 a −16 % calibrado | Casi toda E7: la debilidad del instrumento ya se conoce |
| E8 ITP | Q6-v (V16): 0,0251 en el log de compraventas por punto (placebo mayor que el efecto). Q6-p: −0,0020 en el valor tasado. V17 B4: MDE de 4,3 % por punto | E8-R1 y E8-R2 repiten el diseño de Q6 con fechas corregidas |
| E9 No residentes | Q8 (V16): −1,33 pp de cuota tras 2025T2 (descriptivo). V17: 7,4 % de las compras. R1A-H4: asociación bivariada | El shift-share por riesgo en origen (E9-R1) es nuevo |
| E10 Grandes tenedores | V12-B5 y V17: 4,2 % del parque total; 2-12 % del alquiler con supuestos | No hay estimación nueva identificada |
| E11 Vacías | V17: «se sostiene con matices» (censos) | No hay estimación nueva |
| E12 Vivienda pública | V17: «se sostiene con matices» | El desplazamiento provincial de E12-A1 es nuevo |
| F1-F3 | V7.2 y V8-M4: no se demuestra cointegración (ARDL rechaza). V15 E1-P2: θ del CS-ARDL 0,64 (velocidad no fiable). Q9-c: θ del CS-ARDL 0,84; Q9-g: GSADF 5,9. V8: SVAR con cinco choques por periodo, sin factor designado | F1 y F2 repiten paneles ya vistos. Es nueva la réplica del DT 1941 del Banco de España con la misma especificación |

**Consecuencia.** El plan fija las especificaciones antes de estimarlas en V18, pero muchas repiten preguntas cuyo resultado ya se conoce. Por eso:
- (i) Cada estimación de V18 se comparará con todas las anteriores de la misma pregunta (metodologia/historial_conclusiones.md).
- (ii) Las especificaciones que repiten una ya vista llevan la marca `repite_visto` en su registro y en el Documento de Trabajo.
- (iii) No se elegirá ninguna variante por su resultado.
- (iv) El Documento de Trabajo separará lo pre-registrado aquí de lo hecho a posteriori (anexo de la fase 6).

### 0.3 Unidades selladas: exclusión
- **v6.** Se excluyen de toda estimación las 8 CCAA de K8 (docs/v16/decisiones.md): Aragón, Asturias, Illes Balears, Canarias, Madrid, Región de Murcia, Navarra y La Rioja. También sus 11 provincias (07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50) y todos sus municipios, distritos y secciones. El filtro es `holdout.excluir_sellados_v6(df, columna, nivel)`, en cada lectura con detalle territorial (guarda «fuga v6» de check_v17, K5 de V17).
  - Quedan fuera, entre otras, las ciudades de Madrid, Palma, Zaragoza, Murcia, Las Palmas de Gran Canaria, Santa Cruz de Tenerife, Oviedo, Gijón, Pamplona y Logroño.
  - Barcelona (08) no está sellada.
- **V15 y V16.** También se excluyen los municipios, distritos y secciones de los bloques espaciales sellados de V15 y V16 (plan, sección A: «las muestras selladas de V15 y V16»), con `holdout.unidad_sellada_v16(codigo, nivel)`, que incluye v6, V15 y V16.
  - En los municipios con cinco distritos o más (Barcelona, València, Sevilla, Málaga, Alicante y otros) eso aparta una parte de sus distritos: en torno al 15 % por cada bloque, según docs/v15/preregistro_v15.md (sección 2) y docs/v16/preregistro_v16.md (sección 5).
  - Toda estimación con distritos o secciones de esas ciudades lo declara, y declara cuántas unidades pierde.
- **Sellado temporal de V15 y V16.** No se usa ningún periodo posterior al último visto de cada variable de V15 o V16 (docs/v15/sellado_v15.json y docs/v16/sellado_v16.json, leídos como manifiesto, sin abrir datos), ni ninguna edición publicada después de esas fechas. Por ejemplo: Incasòl no pasa de 2026T1, SERPAVI no pasa de 2024 y el valor tasado no pasa de 2026T2.
- **Prohibiciones.**
  - No se lee data/sealed.
  - No se leen las filas con `muestra_sellada_v6`.
  - No se ejecuta ningún `evaluate_*`.
- **Totales autonómicos.** Los totales de CCAA de las 8 comunidades selladas no se usan en lugar de sus provincias.
- **La nación** no está sellada espacialmente: los diseños solo nacionales (E7-R1 a E7-R3, F1-R1) no pierden muestra. Sí respetan el sellado temporal.

### 0.4 Reglas de inferencia (B2, tal cual) y su aplicación
**B2 (texto del plan).** Inferencia convencional, la de un trabajo publicado:
- errores agrupados al nivel del tratamiento;
- wild cluster bootstrap (pesos de Webb) con menos de 40 clusters;
- AKM o Borusyak-Hull-Jaravel en shift-share;
- Conley en datos espaciales;
- Driscoll-Kraay en paneles con dependencia transversal;
- Newey-West en series;
- intervalos de Anderson-Rubin y F efectivo de Montiel Olea-Pflueger con instrumentos.

Se publica siempre, con la distorsión medida por Monte Carlo (V16 y V17) cuando exista.

**Aplicación en V18:**
- **Siempre se publica.** La inferencia convencional de B2 se publica siempre. Al lado va el tamaño empírico al 5 % y la cobertura al 95 % que mida el Monte Carlo de V18 (sección 1.13) con el proceso generador de ese diseño, o los de V16 y V17 si el diseño es el mismo (metodologia/validacion_montecarlo_v16.md).
- **Bandas.**
  - **apta:** tamaño en [0,03; 0,08] y cobertura en [0,92; 0,97], con R ≥ 2.000 réplicas;
  - **distorsión moderada:** tamaño en (0,08; 0,15]. Se publica además el p-valor con el valor crítico corregido por tamaño del Monte Carlo;
  - **no fiable:** tamaño superior a 0,15. Se publica con la etiqueta «no fiable», y la clasificación no puede apoyarse en ella.
- **Wild cluster bootstrap de Webb:** 9.999 réplicas, SEED = 20261010.
- **Shift-share.** La principal es BHJ con src/v18/reproduccion/bhj_lib.py (`ssaggregate`, `iv_cluster`, `ar_ic_nulo_impuesto`), herramienta reproducida en la fase 2 y pendiente de su Monte Carlo con nuestro proceso generador. AKM y AKM0 van como alternativa.
- **Instrumentos.** Siempre se publican el F efectivo de Montiel Olea-Pflueger y el intervalo de Anderson-Rubin al 95 %. Con un solo instrumento y un solo regresor endógeno, el AR es robusto a la debilidad.
- **Series.** Newey-West con ancho de banda h + 1 en proyecciones locales. Como alternativa, proyección local aumentada con rezagos y errores de Eicker-Huber-White (Montiel Olea y Plagborg-Møller), si su Monte Carlo la valida.

### 0.5 Clasificación V18 (B3, tal cual) y su aplicación
**B3 (texto del plan).** Clasificación V18 de cada estimación (no sustituye a las capas del proyecto, que se muestran al lado):
- **IDENTIFICADO:** diseño cuasi experimental creíble, primera etapa fuerte (F efectivo > 10 o intervalo AR informativo), pretendencias y placebos superados, robusto a especificaciones razonables y coherente en signo y orden de magnitud con la literatura o con una explicación de por qué difiere. Se puede hablar de causa, con los supuestos.
- **SUGESTIVO:** diseño creíble con alguna prueba débil o fallida no decisiva. Se dice «la evidencia sugiere», con la limitación concreta.
- **ASOCIACIÓN:** sin identificación suficiente. Sin lenguaje causal.
- **NO ESTIMABLE:** faltan datos o variación; se dice qué datos lo harían estimable.

**Criterios numéricos comunes (I1 a I8).** Cada apartado de la sección 1 los concreta.
- **I1 · Diseño creíble.** El que declara la letra (a) de cada estudio, con su supuesto de identificación escrito.
- **I2 · Primera etapa.** F efectivo de Montiel Olea-Pflueger > 10, o intervalo AR al 95 % acotado que excluye el cero.
- **I3 · Pretendencias:**
  - en diferencias en diferencias, contraste conjunto de los adelantos con p > 0,10, y el intervalo de Honest DiD (Rambachan-Roth, magnitudes relativas) con M̄ = 1 excluye el cero;
  - en shift-share, el instrumento no predice la variación del resultado en el periodo previo (p > 0,10) y los choques están equilibrados frente a las características iniciales (contraste conjunto con p > 0,10).
- **I4 · Placebos:**
  - de fecha (adopción falsa ocho trimestres o dos años antes, dentro del preperiodo) con p > 0,10;
  - de resultado (población de 65 años o más e IPC general provincial, que no deberían moverse) con p > 0,10.
- **I5 · Robustez.** Mismo signo en todas las pruebas B4 que aplican: excluir Barcelona, las islas (si quedan en la muestra) y los atípicos (unidades en el 1 % superior de exposición y en el 1 % extremo de la variación del resultado), y cambiar la medida de precio o de alquiler. Además, cada estimación de robustez tiene su IC95 solapado con el de la principal, y al menos el 80 % del multiverso declarado tiene el mismo signo.
- **I6 · Coherencia con la literatura.** La razón entre nuestra estimación y la referencia de la ficha está entre 1/3 y 3, o los dos IC95 se solapan. Si no, debe haber una explicación escrita de la diferencia, por medida, periodo o mercado, aceptada en la revisión B6.
- **I7 · Significación.** p < 0,05 tras Holm dentro de la familia del factor (0.6), con una inferencia «apta» o con el valor crítico corregido por tamaño.
- **I8 · Réplica ciega (B6).** replicador-ciego reproduce la estimación desde este plan: diferencia menor que el 5 % del coeficiente y dentro de un error típico. Sin I8 no se clasifica.

**Reglas de clasificación:**
- **IDENTIFICADO:** I1 a I8.
- **SUGESTIVO:** I1 e I8, sin fallo decisivo y con al menos una de I2 a I7 débil o fallida. Pruebas débiles o fallidas no decisivas:
  - F efectivo entre 5 y 10 con AR informativo;
  - pretendencias con p entre 0,01 y 0,10;
  - M̄ de ruptura entre 0,5 y 1;
  - razón con la literatura fuera de [1/3; 3] sin explicación aceptada;
  - p entre 0,05 y 0,10 tras Holm;
  - inferencia con distorsión moderada.
- **ASOCIACIÓN.** El diseño no es creíble (por ejemplo, regresión transversal sin variación exógena), o hay algún fallo decisivo:
  - F efectivo < 5 con AR no informativo;
  - pretendencias con p < 0,01 o M̄ de ruptura < 0,5;
  - placebo de fecha significativo al 5 %, del mismo signo y de al menos la mitad del efecto;
  - cambio de signo en una prueba B4;
  - inferencia «no fiable» sin alternativa apta.
- **NO ESTIMABLE.** Falta un dato imprescindible, o la comprobación de variación del tratamiento hecha antes de estimar (sin mirar resultados) no alcanza el mínimo declarado.
- **Nulo identificado.** Una estimación que cumple I1 a I5, I7 (en la versión «sin efecto») e I8, y cuyo IC95 excluye ± la mitad de la magnitud de referencia de la literatura, se clasifica IDENTIFICADO con la etiqueta «efecto nulo acotado».

**Capa del proyecto, al lado.** V18 no evalúa en muestra sellada (no se ejecuta ningún `evaluate_*`). Por metodologia/capas.md, ninguna estimación de V18 puede pasar de C4 y la capa que se muestra al lado es C4. La clasificación V18 no promueve de capa (check_v8 a check_v17). Los textos de una estimación IDENTIFICADO usan la fórmula de B3, «con los supuestos [lista], el diseño identifica…», y llevan siempre al lado «capa del proyecto C4: sin evaluación en muestra sellada». check_v18 rechaza el lenguaje causal en toda cifra que no sea IDENTIFICADO. Este contraste entre B3 y las capas queda señalado para la revisión y para el autor.

### 0.6 Multiplicidad, registro y multiverso
- **Familias de Holm por factor (α = 0,05).** La familia de un factor la forman las especificaciones principales (R y A) que este plan declara, con un contraste por identificador: el coeficiente principal, en su resultado principal. La tabla final da el número de cada familia.
- **Multiverso.** Las variantes de cada identificador se controlan con Benjamini-Yekutieli al 10 %. En V16 el Monte Carlo dejó NO APTO el BH jerárquico y APTO el BY (metodologia/validacion_montecarlo_v16.md). Se publican los q-valores.
- **Registro.**
  - Toda especificación, incluidas las variantes y las que fallen, se registra en el Registry de src/econ_utils.py (output/v18/estimacion/<id>/registro.csv) antes de leer su resultado, con su identificador V18-*.
  - Ningún modelo se elige por su p-valor.
  - Cada subagente devuelve output/v18/estimacion/<id>/resultado.json con el formato de CLAUDE.md: rama, pregunta, capa, datos, N, metodo, estimacion, ic95, p_ajustado, nivel_evidencia (aquí, la clasificación V18), diagnosticos, fuera_muestra y notas.
- **Multiverso acotado.** Como máximo 1.500 especificaciones en todo V18: unas 320 declaradas en la tabla final y el resto como holgura para desviaciones, cada una con su motivo en desviaciones.md. Con lo registrado desde v1, el proyecto sigue muy por debajo del tope de 50.000 de V8.
- **Semilla.** SEED = 20261010 en todo lo aleatorio: bootstrap, permutaciones, Monte Carlo y propagación.

### 0.7 Pruebas mínimas por diseño (B4, tal cual)
- **Diferencias en diferencias:** estudio de eventos con pretendencias; Callaway-Sant'Anna o Sun-Abraham si la adopción es escalonada; Honest DiD (Rambachan-Roth) para sensibilidad; placebos de fecha y de resultado.
- **Variables instrumentales y shift-share:** primera etapa, pruebas de Rotemberg, exclusión de los orígenes de más peso, pretendencias del instrumento, sobreidentificación si hay varios instrumentos.
- **Regresión discontinua:** densidad, balance y anchos óptimos con rdrobust.
- **Series temporales y SVAR:** raíces unitarias, estabilidad, sensibilidad a la identificación (restricciones alternativas) y bandas.
- **Siempre:** robustez a la exclusión de Madrid, Barcelona, islas y unidades atípicas; a la medida de precio (IPV, valor tasado, Registradores) y a la de alquiler (SERPAVI, IPVA, fianzas, IPC).

Notas de aplicación:
- Madrid ya está fuera por el sellado, y Baleares y Canarias también. Por eso «sin Madrid» y «sin islas» no cambian la muestra provincial y se dice así.
- Registradores no es redistribuible sin autorización (docs/v18/tareas_autor.md, punto 8). Sus agregados solo se usan como contraste interno, no como cifra publicada.
- El IPV solo existe por CCAA y desde 2007. En los diseños provinciales, la robustez con IPV se hace a escala de CCAA con las 9 CCAA no selladas.

---

## 1. Estudios E1-E12

### 1.1 E1 · Vivienda turística

#### Estudio clave: García-López, Jofre-Monseny, Martínez-Mazza y Segú (2020), JUE 119, 103278
Ficha: docs/v18/bib/turismo/garcialopez2020.md. Sin paquete de replicación (docs/v18/reproduccion.md).

**(a) Especificación original (según la ficha):**
- **Muestra y datos:** Barcelona, 2007-2017. Unidad: 220 áreas pequeñas (BSA, unos 7.000 habitantes).
- **Resultado:** residuo hedónico medio por BSA del alquiler y del precio anunciados (Idealista, diciembre) y de los precios de transacción de segunda mano (2009-2016).
- **Tratamiento:** anuncios activos de Airbnb por BSA, en centenares.
- **Ecuación:** ln y_bt = β·(Airbnb_bt/100) + α_b + γ_t + tendencias heterogéneas (lineales o cuadráticas, por características de 2012 o propias de cada BSA) + ε_bt.
- **Instrumento:** proximidad a atractivos turísticos (dónde) × búsquedas de Google «Airbnb» (cuándo).
- **Otros diseños:** estudio de eventos del decil superior de actividad; caso de la Sagrada Família.
- **Inferencia:** errores por BSA (la ficha da errores típicos, no el nivel; se asume el de la BSA).
- **Cifras de la ficha:**
  - efectos fijos con controles (tabla 3, col. 2): alquiler 0,035 (0,009);
  - con tendencias propias de BSA (col. 5): 0,058 (0,020);
  - con instrumento (tabla 5): 0,022 (0,011) y 0,033 (0,010), con F de 192,2 y 70,2;
  - barrio medio: +1,9 % en el alquiler; decil superior: +7 %.

**(b) Traslado a nuestros datos (inventario de la fase 0):**
- **Unidad.** La sección censal de Barcelona (código INE), agregada a barrio con la correspondencia oficial sección-barrio del Ajuntament. Se excluyen las secciones de distritos sellados en V15 y V16. Los barrios con datos de HUT son 66 según el inventario.
- **Tratamiento principal.** Licencias de vivienda de uso turístico (HUT) vigentes en cada corte del registro (data/manual/v11/bcn_hut_trimestral/*; base:bcn_hut_registro), por 100 viviendas del parque de la sección o el barrio. No es lo mismo que los anuncios del original. La reconstrucción por año de expediente (data/raw/v9/bcn_hut/bcn_hut_barrio_anio_expediente.csv.gz) solo entra en robustez: no conserva las bajas y tiene sesgo de supervivencia.
- **Alquiler principal.**
  - SERPAVI, mediana en €/m² de vivienda colectiva por sección (base:serpavi_alquiler_m2_mediana; 2011-2024, anual, stock de alquileres declarados).
  - Alternativas: el alquiler medio de las fianzas por barrio de Open Data BCN (trimestral, Incasòl; descarga abierta, `posterior_prereg`) y el IPVA por distrito (base:ipva_indice).
- **Precio de compra.** No hay precio por barrio. La réplica del precio es NO ESTIMABLE (X1) mientras no se descargue y verifique el precio de compraventa por barrio de Open Data BCN.
- **Controles:** renta ADRH por sección (base:adrh_renta_neta_persona, 2019-2023) y población (base:pob_censo_anual, 2021-2025), cuando sus años cubran la ventana; si no, efectos fijos de sección y tendencias.

**Especificaciones:**
- **V18-E1-R1 (efectos fijos con tendencias).**
  - Ecuación: ln alquiler_st = β·HUT_st + α_s + γ_t + δ_b·t + ε_st, con HUT en licencias por 100 viviendas, ventana 2018-2024.
  - Comprobación previa sin resultados: si la desviación típica intra-unidad del tratamiento es menor que 0,25 licencias por 100 viviendas, o si menos de 20 barrios cambian su stock en más de un 10 % entre cortes, R1 es NO ESTIMABLE (sin variación; moratoria desde 2014 y PEUAT desde 2017).
- **V18-E1-R2 (variable instrumental).**
  - Instrumento: Z_st = ln(proximidad a los tres atractivos más cercanos de OpenStreetMap, tourism=attraction, ODbL, `posterior_prereg`) × índice anual de Google Trends «Airbnb Barcelona» (`posterior_prereg`; condiciones de uso por verificar).
  - Variante: el índice de Google sustituido por las noches en plataformas de Eurostat de la NUTS3 de Barcelona (base:eurostat_plataformas_noches).
  - Misma ventana que R1.
- **V18-E1-R3 (estudio de eventos en el periodo original).**
  - Ecuación: ln alquiler_st = Σ_k β_k·D_s·1[t = k] + α_s + γ_t + ε_st, con D_s = densidad HUT del primer corte (2018T2) estandarizada (dosis continua), años k = 2011-2019 y base 2013.
  - Supuesto declarado: la moratoria hace que el stock de 2018 aproxime el de 2014. El preperiodo es corto (2011-2012).
  - Es lo más cercano al periodo de García-López et al. con nuestros datos. SERPAVI mide contratos vigentes declarados, no anuncios.
- **V18-E1-R4 (Sagrada Família).**
  - Diferencias en diferencias de las secciones a menos de 500 m del templo frente a las del anillo de 500-1.000 m, con el resto de Barcelona como control en la variante.
  - Años 2011-2019 de SERPAVI, base 2013.
  - Si las secciones del radio caen en un distrito sellado en V15 o V16, NO ESTIMABLE (sin mirar resultados).
- **X1:** precio de compra por barrio de Barcelona (falta el dato).

**(c) Ampliaciones (cada una por separado):**
- **V18-E1-A1 · Shift-share por sección en las ciudades no selladas** (València, Málaga, Sevilla, Alicante y Barcelona, sin los distritos sellados en V15 y V16).
  - Ecuación: ln SERPAVI_st sobre % de viviendas turísticas INE-VUT (base:ine_vut_vivienda_turistica, media anual) con efectos de sección y de municipio × año, 2021-2024.
  - Instrumento: proximidad a atractivos OSM × noches en plataformas de la NUTS3 (Eurostat).
  - Repite la exposición y el resultado de H3 (`repite_visto`). Lo nuevo es el instrumento.
- **V18-E1-A2 · Registro de Andalucía con fecha de alta** (Málaga y Sevilla; data/raw/v16/alquiler_turismo/_terceros/openrta_all_2026-10-17.csv.gz, agregado por sección).
  - Estudio de eventos de dosis continua con altas acumuladas, 2015-2024, frente al SERPAVI de la sección.
  - Repite Q2b a escala de sección (`repite_visto`).
  - La serie está reconstruida con sesgo de supervivencia: solo admite SUGESTIVO como máximo.
- **V18-E1-A3 · Registro de la GVA** (municipal, reconstruido; base:vut_registro_gva_reconstruido).
  - Solo robustez de A1 para la Comunitat Valenciana: «las interpolaciones y fuentes no validadas solo entran en robustez».
  - Clasificación máxima: ASOCIACIÓN.
- **V18-E1-A4 · Regulaciones locales (PEUAT y moratorias) como diferencias en diferencias.** NO ESTIMABLE: faltan la geometría del PEUAT y las fechas de las moratorias (docs/v18/tareas_autor.md, punto 13). En V16 la moratoria de València, con un solo año posterior, dio un rechazo placebo de 0,85.
- **V18-E1-A5 · InsideAirbnb como exposición.** NO ESTIMABLE: solo hay instantáneas desde 2025-12; el histórico requiere la Archived Data Request (tareas_autor, punto 14).

**(d) Pruebas B4 y criterios:**
- **R1, A1:**
  - placebo de adelanto (HUT en t+1 sin efecto, controlada la de t; p > 0,10);
  - exclusión de las secciones en el 1 % superior de exposición;
  - medida de alquiler alternativa (fianzas de Open Data BCN en R1; IPVA por distrito en A1), con el mismo signo y el IC95 solapado.
- **R2, A1 (instrumento):**
  - F efectivo > 10;
  - pretendencias del instrumento: Z de 2018-2024 no predice Δln SERPAVI 2011-2017 (p > 0,10);
  - sobreidentificación de Hansen con p > 0,10 si se usan las dos medidas del «cuándo» a la vez;
  - exclusión de los atractivos de mayor peso: Sagrada Família, Park Güell y Casa Batlló en Barcelona.
- **R3, R4, A2 (estudio de eventos):**
  - adelantos conjuntamente con p > 0,10;
  - Honest DiD con M̄ hasta 1;
  - placebo de fecha (base falsa en 2011 para la variación 2011-2012);
  - placebo de resultado (población de 65 años o más por sección).
- **Siempre:** sin Barcelona (en A1); sin atípicos.
  - No hay islas en la muestra no sellada.
  - Precio: no aplicable, sin precio por barrio.
  - Alquiler: SERPAVI frente a fianzas (Barcelona) e IPVA (resto).

**(e) Inferencia B2:**
- **R1 a R4:** cluster por barrio (unos 60 clusters tras el sellado; si quedan menos de 40, wild cluster bootstrap de Webb), Conley a 1 km y Driscoll-Kraay como alternativas.
- **R2:** AR y F efectivo.
- **A1:**
  - cluster por municipio × distrito;
  - Conley a 2 km (NO APTO en V16 a escala de sección: requiere Monte Carlo nuevo);
  - AR y F efectivo;
  - BHJ no aplica (el instrumento no es una suma de choques por origen).
- **A2:** cluster por municipio (2 clusters) es insuficiente. Se usa cluster por distrito postal o sección con Conley a 1 km. Si el Monte Carlo no lo valida, solo descriptivo.

**(f) Clasificación:**
- **IDENTIFICADO** solo para R2 o A1, con I1 a I8: F efectivo > 10, pretendencias del instrumento superadas, mismo signo con fianzas o IPVA, y razón con la literatura en [1/3; 3] una vez convertida la unidad (sección 3).
- **R1 y R3:** sin instrumento, como máximo SUGESTIVO (efectos fijos con tendencias; la exogeneidad estricta no se contrasta).
- **R4:** caso de un solo grupo tratado, como máximo SUGESTIVO.
- **A2:** como máximo SUGESTIVO. **A3:** ASOCIACIÓN como máximo.
- **ASOCIACIÓN** si falla el placebo de adelanto o la pretendencia del instrumento con p < 0,01.

**(g) NO ESTIMABLE y qué lo haría estimable:**
- X1 (precio por barrio): Open Data BCN o microdatos de portales (tareas_autor, punto 2).
- A4: geometría del PEUAT y fechas de las moratorias (punto 13).
- A5: InsideAirbnb 2015-2024 (punto 14).
- El periodo original de anuncios 2012-2016: histórico de InsideAirbnb o AirDNA (punto 14).

#### Estudio de apoyo: Chaves-Fonseca (2026), SERIEs
Ficha docs/v18/bib/turismo/chavesfonseca2026.md; reproducido en la fase 2 (0,01965 frente a 0,020; «coincide»).
- No se replica con nuestros datos: es Madrid, sellada (v6).
- Su diseño (proximidad × Google Trends) es el de E1-R2 y E1-A1, y su cifra entra en la sección 3 si la unidad es convertible.

### 1.2 E2 · Topes al alquiler

#### Estudio clave 1: Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916
Ficha: docs/v18/bib/topes/jofremonseny2023.md. Sin paquete.

**(a) Especificación original (según la ficha):**
- **Muestra:** Cataluña, municipio-trimestre, 148 municipios, 3.698 observaciones, 25 trimestres. Datos: microdatos del registro de fianzas del Incasòl.
- **Grupos:** municipios regulados por la Ley 11/2020 frente a municipios no regulados que también tenían mercado tensionado. Se excluyen los parcialmente tratados.
- **Diseño:** diferencias en diferencias y estudio de eventos, con un término de anticipación (−0,004 con error 0,009 en el alquiler).
- **Resultados:** log de la renta media; log de contratos por 1.000 habitantes.
- **Robustez:** COVID-19 (expedientes de regulación temporal de empleo, paro, contratos) y desbordamiento a vecinos, que caen la mitad.
- **Cifras de la ficha (tabla 2):**
  - renta −0,044 (0,006), −0,044 (0,006) y −0,045 (0,006);
  - contratos −0,011 (0,021), −0,010 (0,020) y −0,003 (0,021);
  - contratos con anticipación: +0,130 (0,029).
- **Vigencia de la norma:** de septiembre de 2020 a marzo de 2022.

**(b) Traslado:**
- **Datos:** Incasòl por municipio y trimestre: renta media y número de contratos nuevos (data/raw/v9/incasol/incasol_qww9-bvhh_actual.csv.gz; data/raw/v3/incasol_fianzas_municipio_v3.csv.gz; 2007T1-2026T1).
- **Tratados:** municipios de la Ley 11/2020 (data/raw/v3/cataluna_contencion_rentas_v3.csv; vigencia del 2020-09-22 al 2022-04-08).
- **Controles (los de JMS no están en el repositorio):** municipios catalanes no regulados con al menos 5 contratos en cada trimestre del preperiodo, situados a más de 10 km de un regulado (centroides de data/base/geo). En la variante, los del tercil superior de renta media y de su crecimiento en 2016-2019.
- **Ventana:** 2016T1-2022T1, es decir, 25 trimestres que terminan con la vigencia. Es un supuesto nuestro: la ficha no da las fechas.
  - Posterior = 2020T4-2022T1.
  - 2020T3 es parcial y se trata como anticipación.
- **Covariables:** población (base:pob_total) y paro registrado (base:sepe_paro_registrado_media_anual).
- **Exclusiones:** los municipios de los bloques sellados de V15 y V16. Ninguna provincia catalana está sellada en v6.

**Especificación:**
- **V18-E2-R1.** ln y_mt = β·Reg_m·Post_t + θ·Reg_m·1[t = 2020T3] + α_m + γ_t + X'_mt·λ + ε_mt, con y = renta media (principal) y contratos por 1.000 habitantes (segundo resultado, con su propio identificador de Holm: **V18-E2-R1c**).
- Repite V9-D1b (`repite_visto`).

#### Estudio clave 2: Monràs y García-Montalvo (2023), FRBSF WP 2023-28
Ficha: docs/v18/bib/topes/monras2023.md.

**Corrección de la fase 1.** Usan contratos del Incasòl (enero de 2016 a junio de 2021), no anuncios. E2 es replicable en parte con Incasòl por tramo, porque los datos públicos tienen tramos fijos de renta.

**(a) Especificación original (según la ficha):**
- **Diseño:** diferencias en diferencias a nivel de contrato y de municipio-mes, con efectos fijos de municipio y mes (con tendencias por provincia y unidad en algunas columnas).
- **Resultados:** precio en exceso respecto al precio de referencia, log del precio y log de contratos nuevos, por encima y por debajo de la referencia.
- **Cifras de la ficha:**
  - log del precio −0,058 (0,014); con efectos fijos de unidad −0,080 (0,014);
  - log de contratos nuevos −0,207 (0,021) con MCO y −0,111 (0,018) con PPML;
  - por encima de la referencia −0,577 (0,042); por debajo +0,166 (0,038).

**(b) Traslado:**
- Contratos por tramo fijo de renta en €/mes, municipio y trimestre (mismo fichero del Incasòl), 2016T1-2021T2.
- No hay precio de referencia por vivienda, ni renta anterior, ni superficie. El precio en exceso y el efecto composición (efectos fijos de unidad) son NO ESTIMABLES (X1).

**Especificación:**
- **V18-E2-R2.** PPML del número de contratos nuevos por municipio × tramo × trimestre:
  - E[n_mkt] = exp(β_k·Reg_m·Post_t + α_mk + γ_kt);
  - β_k por tramo k, con un contraste principal: la diferencia entre los tramos superiores e inferiores a la mediana de renta de 2019 de Cataluña, fijada antes de estimar.
- **V18-E2-R2s.** Proporción de contratos en los tramos superiores, en diferencias en diferencias.

**(c) Ampliaciones:**
- **V18-E2-A1 · Zonas tensionadas de 2024 en Cataluña** (Ley 12/2023; base:zt_vigente). Réplica de Pérez García (2026):
  - datos: Incasòl 2022T1-2026T1;
  - diseño: diferencias en diferencias, estudio de eventos y emparejamiento por puntuación de propensión;
  - resultados: crecimiento de la renta y contratos por 10.000 habitantes.
  - Ficha docs/v18/bib/topes/perezgarcia2026.md: renta −0,0298 (0,0113), no significativa con el emparejamiento; contratos −6,586 (1,135).
  - Solapa con H1 y H2 de V15 (`repite_visto`). No sustituye a su evaluación sellada ni la condiciona.
- **V18-E2-A2 · Zonas tensionadas fuera de Cataluña.** País Vasco, con la renta del EMAL por municipio y trimestre (base:emal_renta_mensual_eur; 2016T1-2025T4), frente a municipios vascos sin zona.
  - Fechas de efecto: base:zt_vigente y data/raw/v16/intervenciones/zonas_tensionadas_v16_nuevas.csv.
  - Solo hay entre 2 y 3 trimestres posteriores. Navarra y Asturias están selladas, y A Coruña no tiene periodo posterior en SERPAVI ni en el IPVA (2024).
  - Comprobación previa: con menos de 3 trimestres posteriores por cohorte, A2 es solo descriptiva.
- **V18-E2-A3 · Desplazamiento a la venta.** Compraventas (base:compraventas) y valor tasado (base:p_tasado) de los municipios regulados frente a los controles, 2016-2022. Repite Q1c en otro periodo.
- **V18-E2-A4 · Desbordamiento.** Municipios no regulados a menos de 10 km de uno regulado frente a los de más de 25 km.
- **V18-E2-A5 · Desplazamiento al alquiler de temporada.** NO ESTIMABLE: faltan las fianzas por tipo de contrato y el Registro Único (tareas_autor, punto 4).

**(d) Pruebas B4 y criterios:**
- **Pretendencias:** adelantos de 2016T1 a 2020T2 con p > 0,10; potencia de Roth para una pendiente del 1 % anual.
- **Honest DiD:** IC con M̄ = 1 que excluye el cero. V9-D1b dio un M̄ de ruptura de 0,5: el fallo ya visto se declara.
- **Placebo de fecha:** adopción falsa en 2018T4, p > 0,10.
- **Placebo de resultado:** población de 65 años o más; contratos de locales, si existen en Incasòl (si no, se omite y se dice).
- **Permutaciones:** 1.000 asignaciones del tratamiento entre municipios catalanes.
- **Robustez:**
  - sin Barcelona ciudad;
  - sin el 1 % de municipios con más contratos;
  - con controles a 0 y 25 km;
  - Callaway-Sant'Anna en A1, porque la adopción por cohortes es escalonada;
  - medida de alquiler alternativa: SERPAVI municipal anual 2016-2022, que es stock y no contratos nuevos, con el mismo signo exigido.
- **Precio (A3):** valor tasado frente a compraventas.

**(e) Inferencia B2:**
- **R1, R2, A1, A4:** cluster por municipio (más de 40 clusters esperados; si no, Webb), más inferencia por aleatorización y Driscoll-Kraay.
- **A2:** pocos municipios tratados. Conley-Taber, que fue APTO en V16 en el escenario A con tamaño 0,0575; hay que revalidarlo para A2.
- **SDID y Callaway-Sant'Anna con Webb:** NO APTO en V16 (cs_webb, tamaño 0,0655 y cobertura 0,9015). Requieren Monte Carlo nuevo.

**(f) Clasificación:**
- **R1 IDENTIFICADO** si cumple I1 a I8. En particular:
  - Honest DiD con M̄ = 1 excluye el cero;
  - la razón con −0,044 (ficha) está en [1/3; 3].
  - Con M̄ de ruptura entre 0,5 y 1: SUGESTIVO. Por debajo de 0,5: ASOCIACIÓN.
- **R1c (contratos):** un IC95 que excluye ±0,05 en log se clasifica como nulo acotado. Si no, se dice que no hay potencia.
- **R2:** como máximo SUGESTIVO, porque el estimando no es el del original (tramo fijo en euros frente a precio de referencia).
- **A1:** como H1 y H2 de V15. Un resultado IDENTIFICADO no cambia H1 ni H2: es una repetición en entrenamiento.
- **A2:** con menos de 3 trimestres posteriores, NO ESTIMABLE.

**(g) NO ESTIMABLE:**
- R2-X1 (precio en exceso y composición): microdatos de contratos con renta anterior, superficie y precio de referencia de la Agència de l'Habitatge (tareas_autor, punto 4).
- A5: fianzas por tipo de contrato o Registro Único (punto 4).
- La parte de Monràs y García-Montalvo con anuncios (Idealista como contraste): microdatos de portales (punto 2).

### 1.3 E3 · Inmigración

#### Estudio clave: González y Ortega (2013), J. Regional Science 53(1), 37-59, y su versión IZA de 2009

**Corrección de la fase 1.** La edición publicada (2013) usa 2000-2010 y atribuye a la inmigración «un cuarto» del aumento de precios. El «un tercio» de 1998-2008 es del documento IZA de 2009. Se replican las dos ventanas.

Fichas:
- docs/v18/bib/inmigracion/gonzalez_ortega_2013.md (solo resumen);
- gonzalez_ortega_2009_iza.md (texto completo);
- gonzalez_ortega_2011_chicagofed.md (versión previa a la publicada; da la especificación de 2000-2010).

**(a) Especificación original:**
- **IZA 2009** (ficha gonzalez_ortega_2009_iza):
  - 50 provincias, 1998-2008, 500 observaciones provincia-año;
  - primeras diferencias, ponderadas por la población de 1998;
  - resultado: precio en €/m² del Ministerio de Vivienda;
  - endógena: entrada de extranjeros en puntos de población;
  - instrumento de redes étnicas: Censo de 1991, 16 grupos de origen, aplicado a los flujos nacionales anuales;
  - efectos región-año;
  - primera etapa: 0,186 con t = 5,4 (no da F);
  - precio: 44,72 €/m² (18,58) por punto, «3,2 %» por cada 1 % de la población;
  - cantidad: 0,462 (0,033) viviendas por inmigrante en edad de trabajar;
  - agregado: el 52 % del precio y el 37 % de la obra nueva.
- **2013 / Chicago Fed 2011** (ficha gonzalez_ortega_2011_chicagofed):
  - provincias, 2001-2010 y 2001-2008;
  - primeras diferencias en logaritmos, ponderadas por la población en edad de trabajar;
  - efectos fijos de año y de 9 macrorregiones;
  - instrumentos: redes (1991) y «gateways» (accesibilidad por aire, tierra y mar);
  - elasticidad del precio respecto a la población en edad de trabajar: 0,866 (0,803) en 2001-2010 y 0,997 (0,424) en 2001-2008; solo con redes, 0,959 (0,984) y 0,927 (0,596);
  - cantidad: 1,05 (0,578).
  - El resumen publicado da 2000-2010, un 2 % anual de precio y un cuarto del aumento.

**(b) Traslado:**
- **Unidad:** 39 provincias no selladas (las 11 de v6 fuera; entre ellas Madrid, Baleares, Murcia, Las Palmas y Santa Cruz de Tenerife).
- **Precio principal:** valor tasado provincial en €/m² (base:valor_tasado, 1995T1-2026T2, media anual), la misma fuente ministerial que el original. El IPV solo es autonómico y desde 2007: robustez a escala de CCAA solo en las ampliaciones.
- **Endógena:** variación anual de la población extranjera sobre la población del año anterior. Fuentes: base:pob_extranjera (total desde 1998) y base:padron_pob_nacionalidad (por nacionalidad desde 2003).
- **Cuotas del año base:** Censo de 2001 por nacionalidad y provincia (INE, abierto, `posterior_prereg`), en los grupos de origen más parecidos a los 16 del original. Variante: padrón de 2003 (dentro de la ventana, contaminado; solo robustez).
- **Choque:** entradas nacionales por nacionalidad (data/raw/ine_migraciones_nacionalidad.csv, 1998-2024), sin la propia provincia cuando hay detalle provincial (desde 2003, con la variación del stock por nacionalidad). Antes, el flujo nacional sin corrección, declarado.
- **Ponderación:** población de 1998 (R1) o de 2000 (R2). Si no hay población en edad de trabajar por provincia en la base, se descarga del padrón por edad (`posterior_prereg`); la alternativa es la población total.
- **Cantidad:** iniciadas y terminadas provinciales (base:iniciadas, base:terminadas; data/raw/mivau_v2_iniciadas_terminadas_prov.csv).
- **Controles:** PIB y empleo provinciales (data/raw/ine_v2_cre.csv; base:ocupados_epa), efectos de año y de macrorregión (las 9 macrorregiones del original se rehacen con las provincias no selladas).
- No hay «gateways»: R2 usa solo redes, como la columna de Chicago Fed solo con redes.

**Especificaciones:**
- **V18-E3-R1 (ventana IZA).** Δp_pt = β·(ΔF_pt/P_p,t−1) + μ_rt + ε_pt, 1998-2008, en €/m².
  - Instrumento: Σ_c s_pc,2001·(entradas nacionales_ct sin p)/P_p,t−1.
  - Ponderación por la población de 1998.
  - Resultado secundario: viviendas iniciadas por inmigrante (**V18-E3-R1q**).
- **V18-E3-R2 (ventana publicada).** Δln p_pt = β·Δln(población en edad de trabajar)_pt + μ_t + μ_r + ε_pt, 2000-2010, instrumentada con las redes.
  - Subperiodo 2001-2008: **V18-E3-R2b**.
  - Cantidad: **V18-E3-R2q**.

**(c) Ampliaciones:**
- **V18-E3-A1 (precio 2014-2025).** Δln valor tasado sobre ΔF/P, con cuotas de 2001 y choques nacionales.
- **V18-E3-A2 (alquiler 2014-2024).** Δln SERPAVI provincial (base:serpavi_alquiler_m2_mediana, 2011-2024).
  - Alternativas: IPVA (2011-2024) e IPC de alquiler (2002-2026T2).
  - Solapa con H4 y Q3 (`repite_visto`).
- **V18-E3-A3 (municipios).** Panel municipal 2014-2024 con cuotas del padrón de 2003 por municipio (las de H4), SERPAVI municipal y valor tasado de los municipios con dato (base:p_tasado). Se excluyen los municipios sellados en v6, V15 y V16. Repite H4 (`repite_visto`).
- **V18-E3-A4 (separación entre compra y alquiler).** Dos regresores endógenos: entradas predichas de las nacionalidades con más inquilinos y de las que tienen menos, clasificadas por la tenencia del Censo de 2011 (data/raw/v11/ine_censo2021/* y censos de 2011; se fija con el de 2011, anterior a la ventana). Resultados: valor tasado y SERPAVI provinciales, 2014-2024.
- **V18-E3-A5 (ventana larga 1998-2019).** Con la partición por periodos de Torres Montero (2023): 2001-2010 frente a 2011-2019.

**(d) Pruebas B4 y criterios:**
- **Primera etapa:** F efectivo > 10.
- **Pretendencias del instrumento:**
  - el de 1998-2008 no predice Δp de 1995-1998 (valor tasado desde 1995), p > 0,10;
  - en A1 y A2, el de 2014-2024 no predice Δ de 2008-2013 (precio) ni de 2011-2013 (alquiler).
- **Balance BHJ:** choques frente a las características de 2001 (renta, paro, cuota urbana), p conjunto > 0,10.
- **Rotemberg:** pesos publicados; sin los 5 orígenes de mayor peso, el signo se mantiene y la estimación queda dentro del IC95 principal.
- **Jaeger-Ruist-Stuhler:** con el instrumento retardado como control, la estimación se mantiene dentro del IC95. Q3-c1 ya mostró inestabilidad: de 0,0119 a 0,0077.
- **Sobreidentificación:** solo en A4 (dos instrumentos por grupo), Hansen con p > 0,10.
- **Robustez:**
  - sin Barcelona;
  - sin Alicante y Málaga (las de más cuota extranjera no selladas);
  - sin atípicos;
  - con cuotas del padrón de 2003 (sabiendo que están contaminadas);
  - sin ponderar;
  - precio con IPV por CCAA (A1, 9 CCAA) y alquiler con IPVA e IPC (A2).
- **Placebo de resultado:** población de 65 años o más nacida en España.

**(e) Inferencia B2:**
- Principal: BHJ a nivel de choque (bhj_lib, `ssaggregate` + `iv_cluster`, cluster por origen), con el intervalo AR con el nulo impuesto (`ar_ic_nulo_impuesto`).
- Alternativas:
  - AKM y AKM0 (NO APTOS en V16: tamaño 0,3762 y 0,0108; requieren Monte Carlo nuevo);
  - cluster por provincia con wild cluster bootstrap de Webb (39 clusters < 40);
  - Driscoll-Kraay.
- F efectivo e intervalo AR siempre.

**(f) Clasificación:**
- **IDENTIFICADO** si cumple I1 a I8. En particular:
  - F efectivo > 10;
  - pretendencia 1995-1998 con p > 0,10;
  - Rotemberg y Jaeger-Ruist-Stuhler superados;
  - razón en [1/3; 3] con la referencia de su versión: 3,2 % por 1 % (IZA) en R1 tras convertir los euros con el precio medio de la muestra; 0,866 a 0,997 (Chicago Fed) en R2.
- **SUGESTIVO:** F efectivo entre 5 y 10 con AR informativo, como en el resto de diseños.
- **ASOCIACIÓN:** F efectivo < 5 con AR no informativo. Es lo que dio V9-D4 con cuotas de 2003: si se repite, se clasifica así y se dice.
- **A4:** SUGESTIVO como máximo (la clasificación por tenencia es de un solo corte).

**(g) NO ESTIMABLE:**
- R1 y R2 lo son si el Censo de 2001 no puede descargarse: con cuotas de 2003, la especificación pasa a robustez y la clasificación máxima es ASOCIACIÓN.
- Los «gateways» del original exigirían construir la accesibilidad por origen (no en el repositorio).
- Saiz (2007) es solo referencia metodológica (ficha saiz_2007_philly).

### 1.4 E4 · Ayudas a la demanda

#### Estudios clave
Fack (2005, 2006), Gibbons y Manning (2006) y Grislain-Letrémy y Trevien (2022, Banque de France WP 886). Fichas: docs/v18/bib/ayudas/fack_2005_cepremap.md, fack_2006.md, gibbons_manning_2003_lse.md y grislain_trevien_2022_bdf.md.

**(a) Especificación original (según las fichas):**
- **Fack (2005):** diferencias y triples diferencias con la extensión de las ayudas de los noventa (encuestas Logement de 1984 a 2002), con la ayuda por m² instrumentada.
  - θ = 0,76 (0,26) y 0,39 (0,24) en doble diferencia;
  - 1,42 (0,63) y 1,02 (0,52) en triple diferencia.
- **Gibbons y Manning:** recorte del Housing Benefit por fecha de mudanza. −10,3 % y −16,2 %; con tendencias por antigüedad, −3,5 % y −6,8 %.
- **Grislain-Letrémy y Trevien:** discontinuidad geográfica difusa (zona II), 60 aglomeraciones. +0,052 (0,019) en el log del alquiler por m², por un diferencial de 15-40 €/mes.

**(b) Traslado.** No hay microdatos de perceptores del Bono Alquiler Joven ni de las ayudas autonómicas, ni convocatorias con fecha. La ECV no asigna el bono por la edad: en el Plan 2018-2021 ya existía un programa para menores de 35 años (docs/v16 Q7, output/v16/q7/informe.md).

**Especificaciones:**
- **V18-E4-X1 (réplica con perceptores).** NO ESTIMABLE.
- **V18-E4-X2 (discontinuidad por la edad en la ECV).** No se repite: Q7a ya la estimó (−0,120, con placebos de 31|32 y 39|40 del mismo orden). Su estimando es un cambio de generosidad, no la incidencia.
- **V18-E4-L1.** La magnitud preferida sale solo de la literatura, rotulada «solo literatura, sin estimación propia».

**(c) Ampliaciones:** ninguna estimable.

**(d)-(f):** no aplican. No hay estimación propia que clasificar.

**(g) Qué lo haría estimable:**
- Microdatos de beneficiarios con edad, renta, municipio, fechas de solicitud y concesión, importe y alquiler declarado (tareas_autor, punto 3). Con ellos:
  - diferencias en diferencias por fecha de concesión y municipio (estilo Fack);
  - discontinuidad en el umbral de renta del bono (rdrobust: densidad, balance y anchos óptimos, con 0,5 y 2 veces el ancho; F de la primera etapa > 10 en el RD difuso).
- Si llegan, se escribirá una adenda **antes** de mirarlos.

### 1.5 E5 · Oferta y suelo

#### Estudio clave: Saiz (2010), QJE 125(3)
Ficha docs/v18/bib/oferta_suelo/saiz_2010.md (solo resumen). Apoyo: Baum-Snow y Han (2024), ficha baum_snow_han_2020_nberconf.md; Taltavull (2006), ficha taltavull_2006_funcas.md.

**(a) Especificación original:**
- **Saiz (2010):** elasticidades de oferta por área metropolitana con instrumentos geográficos (pendiente, agua) y un índice de suelo no edificable. La ficha no recoge cifras ni tablas (solo resumen).
- **Baum-Snow y Han:**
  - tractos de EE. UU., 2000-2010;
  - choques de demanda laboral en los destinos de desplazamiento (Bartik);
  - errores con autocorrelación espacial a 25 km;
  - unidades 0,26 (0,11) y 0,31 (0,12).
- **Taltavull:** CCAA, 1987-2004, MC2E con instrumentos retardados, elasticidad de los inicios de 0,46 a 0,87.

**(b) Traslado:**
- **Unidad:** 39 provincias no selladas, anual, 2002-2025.
- **Oferta (Q):**
  - iniciadas de vivienda libre (data/raw/mivau_v2_iniciadas_terminadas_prov.csv; base:iniciadas);
  - alternativas: terminadas y obra nueva neta del Catastro (base:obra_nueva_neta_catastro, municipal desde 2012, agregada a provincia).
- **Precio:** valor tasado provincial real (base:valor_tasado deflactado con base:deflactor).
- **Instrumento de demanda:** Bartik de empleo, B_pt = Σ_k s_pk,2001·g_k,t(−p).
  - Cuotas por sección de la CNAE de la afiliación provincial de 2001, o la primera disponible (Seguridad Social, abierta, `posterior_prereg`).
  - Crecimiento nacional por sector sin la propia provincia.
- **Restricciones físicas y de planeamiento:** MDT05, agua, costa y SIU no están en el repositorio. La Red Natura no se usa como instrumento: falló en Q4.

**Especificaciones:**
- **V18-E5-R1.** Δln Q_pt = ε·Δln P_pt + α_p + γ_t + u_pt, con Δln P instrumentada por B_pt (y B_p,t−1 en la variante), 2002-2025.
  - Estimando: elasticidad precio media de la oferta.
- **V18-E5-R2 (heterogeneidad tipo Saiz).** Δln Q_pt = (ε0 + ε1·R_p)·Δln P_pt + ..., con R_p = la restricción física. NO ESTIMABLE sin MDT05, agua, costa o SIU (X1).

**(c) Ampliaciones:**
- **V18-E5-A1 · Interacción con el choque de E3.** Δln P_pt = φ·Z^inm_pt + ψ·Z^inm_pt·S_p + ..., donde Z^inm es el instrumento de inmigración de E3-A1 y S_p, el suelo disponible por vivienda en 2012 (solares del Catastro; data/raw/v4/catastro_solares_municipios.csv.gz).
  - S_p es endógeno al mercado: clasificación máxima ASOCIACIÓN.
  - Si llegan las restricciones del punto 5 de tareas_autor, se escribe la versión con R_p (A1-R) antes de mirarla.
- **V18-E5-A2 · Áreas urbanas.** R1 con las áreas urbanas del Atlas del MIVAU (abierto, `posterior_prereg`) como unidad.
- **V18-E5-A3 · Municipios.** Obra nueva neta del Catastro (2012-2025) frente al valor tasado municipal (municipios con dato), con un Bartik municipal de afiliación (2011-2026; celdas menores que 5 suprimidas, declarado).
  - Se excluyen los municipios sellados en v6, V15 y V16.
  - Clasificación máxima: SUGESTIVO.

**(d) Pruebas B4 y criterios:**
- **Primera etapa:** F efectivo > 10.
- **Rotemberg:** pesos por sector; sin los 3 sectores de más peso (incluida la construcción si está entre ellos), el signo se mantiene y la estimación queda dentro del IC95.
- **Exclusión del Bartik:** en la variante, se excluye la construcción de las cuotas y de los choques, para que el instrumento no lleve la propia oferta.
- **Pretendencias:** el Bartik de 2002-2007 no predice Δln Q de 1995-2001, si la serie lo cubre (p > 0,10).
- **Robustez:**
  - sin Barcelona;
  - sin las provincias costeras de más cuota de no residentes (Alicante, Málaga y Girona);
  - sin atípicos;
  - Q = terminadas;
  - precio con IPV por CCAA (desde 2007).
- **Placebo de resultado:** Δ de la población de 65 años o más.

**(e) Inferencia B2:**
- Cluster por provincia (39 < 40): wild cluster bootstrap de Webb.
- Driscoll-Kraay por la dependencia transversal.
- BHJ a nivel de sector, con los choques g_kt (bhj_lib), y AKM como alternativa.
- AR y F efectivo.
- **A3:** Conley a 25 km, como Baum-Snow y Han.

**(f) Clasificación:**
- **R1 IDENTIFICADO** si cumple I1 a I8 y la elasticidad es coherente con la literatura española: Taltavull, de 0,46 a 0,87, y la cota superior de 0,45 que cita el Banco de España (ficha docs/v18/bib/no_residentes/bde_ia2025_en.md). Una razón fuera de [1/3; 3] respecto a 0,46-0,87 exige una explicación (unidades frente a superficie: Baum-Snow y Han).
- **A1:** ASOCIACIÓN como máximo.
- **A3:** SUGESTIVO como máximo.

**(g) NO ESTIMABLE:** R2 y la versión de A1 con restricciones exógenas requieren el SIU, MDT05, CORINE o SIOSE y DPMT (tareas_autor, punto 5).

### 1.6 E6 · Obra nueva y alquileres cercanos

#### Estudios clave
Asquith, Mast y Reed (2023), REStat 105(2), y Mense (2025), JPE Macroeconomics 3(1). Fichas: docs/v18/bib/obra_nueva/asquith_mast_reed_2020_philly.md y mense_2025_jpemacro.md. Mense se reprodujo en la fase 2 (−0,1916 frente a −0,192).

**(a) Especificación original:**
- **Asquith et al.:**
  - anuncios de Zillow 2013-2018 y edificios grandes terminados en 2015-2016;
  - diferencias en diferencias: cerca (250 m) frente a lejos (250-600 m), cerca frente a cerca (edificios de 2019 como control) y triple diferencia;
  - errores por edificio;
  - −0,049 (0,021), −0,062 (0,037) y −0,071 (0,033).
- **Mense:**
  - 94 regiones alemanas, 2010-2017;
  - IV en panel con efectos fijos de región y año;
  - instrumento: duración de las rachas de lluvia de julio a septiembre;
  - −0,192 (0,065) en el log del alquiler por unidad terminada en el cuarto trimestre, relativa a la media anual;
  - F de Kleibergen-Paap de 17,4 a 19,0.

**(b) Traslado:**
- **Asquith (piloto en la provincia de València):**
  - edificios con año de construcción y geometría INSPIRE (data/raw/v11/catastro_inspire/edificios_seccion.csv.gz; unos 94 municipios);
  - alquiler SERPAVI por sección (2011-2024, stock);
  - se excluyen las secciones de distritos sellados en V15 y V16 de València ciudad.
- **Mense (provincias):**
  - terminadas trimestrales por provincia (data/raw/mivau_v2_iniciadas_terminadas_prov.csv);
  - alquiler: IPVA provincial (2011-2024) o IPC de alquiler provincial;
  - lluvia: AEMET OpenData (abierta con clave gratuita; `posterior_prereg`; si el proxy lo impide, tarea del autor).

**Especificaciones:**
- **V18-E6-R1 (Asquith, «cerca frente a cerca»).** ln SERPAVI_st = Σ_k β_k·1[t − T_s = k] + α_s + γ_mt + ε_st.
  - Tratadas: secciones con un edificio residencial de al menos 20 viviendas terminado en 2014-2019, en la sección o en una sección contigua.
  - Control: secciones con un edificio igual terminado 3 a 5 años después (2022-2024).
  - Estimador: Sun-Abraham; resumen: media de k = 0..3.
  - Comprobación previa: con menos de 30 secciones tratadas tras el sellado, NO ESTIMABLE.
- **V18-E6-R2 (Mense).** ln alquiler_pt = β·(T^Q4_p,t−1 / media de T_p) + α_p + γ_t + ε_pt, con T^Q4/media instrumentado por la duración media de las rachas de lluvia de julio a septiembre en t−1 (estaciones de AEMET de la provincia), 2011-2024.
  - Si no hay lluvia de AEMET, NO ESTIMABLE (X1).

**(c) Ampliaciones:**
- **V18-E6-A1.** R1 con umbral de 50 viviendas por edificio y un anillo de distancia de 250 m (con la geometría de los edificios).
- **V18-E6-A2.** R1 en el resto de España. NO ESTIMABLE sin la descarga masiva del Catastro (tareas_autor, punto 1).
- **V18-E6-A3.** R2 con el IPC de alquiler 2002-2025 (stock) en lugar del IPVA.

**(d) Pruebas B4 y criterios:**
- **R1:**
  - adelantos k = −4..−1 con p > 0,10;
  - Honest DiD con M̄ hasta 1;
  - placebo de fecha (T falso 3 años antes);
  - placebo de resultado (población de 65 años o más de la sección).
- **R2:**
  - F efectivo > 10;
  - placebo: la lluvia de enero a marzo no predice T^Q4 (p > 0,10);
  - exclusión: la lluvia no predice la renta ADRH ni el empleo.
- **Robustez:** sin València ciudad (en R1); sin Barcelona (en R2); sin atípicos; medida de alquiler IPVA frente a IPC (R2) y frente a SERPAVI de vivienda unifamiliar (R1).

**(e) Inferencia B2:**
- **R1:** cluster por sección del edificio (más de 40 previstos), Conley a 1 km (requiere Monte Carlo) y Webb si quedan menos de 40.
- **R2:** cluster por provincia (39 < 40) con Webb, Driscoll-Kraay, AR y F efectivo.

**(f) Clasificación:**
- **R1:** IDENTIFICADO si cumple I1 a I8 y la razón con −0,049 a −0,071 (Asquith) está en [1/3; 3]. SERPAVI es stock y diluye el efecto: una razón por debajo de 1/3 con esa explicación pasa a SUGESTIVO si lo demás se cumple.
- **R2:** IDENTIFICADO con F efectivo > 10 y razón con −0,192 en [1/3; 3].

**(g) NO ESTIMABLE:**
- A2: descarga masiva del Catastro (tareas_autor, punto 1).
- Alquiler por anuncio o contrato georreferenciado: punto 2 o fianzas georreferenciadas (punto 4).
- R2 sin AEMET.

### 1.7 E7 · Tipos de interés

#### Estudios clave
San Juan (2023), Boletín Económico del Banco de España 2023/T2 (ficha docs/v18/bib/tipos/sanjuan_2023_bde_be2302art09.md). Recuadro del Boletín Económico del BCE 6/2022 (ficha bce_eb_2022_6_battistini_gareis_roma.md). Battistini et al. (2022; ficha battistini_etal_2022_ecbwp2752.md). Sorpresas de Jarociński y Karadi (ficha jarocinski_karadi_2018_ecbwp2133.md).

**(a) Especificación original:**
- **San Juan:**
  - BVAR trimestral 2004-2022 con compraventas, precio nominal, visados, PIB, IPCA, euríbor a 1 año y saldo de préstamos de vivienda;
  - identificación recursiva;
  - +100 pb en el tipo hipotecario: precio algo menos de −2 % a 8 trimestres; compraventas algo más de −3 %; visados casi −11 %;
  - intervalos al 68 %.
- **BCE (2022):** proyecciones locales del área del euro, 1995T1-2019T4, con choque de diferencial hipotecario. −5 % de precio por +1 pp a dos años (−9 % con tipos bajos).
- **Battistini et al.:** SPVAR con sorpresas de alta frecuencia (signos y ceros), 106 regiones. +0,15 % en el pico por un choque de 5,2 pb.

**(b) Traslado (nacional):**
- **Choque:** sorpresas de política monetaria de Jarociński-Karadi (data/raw/v16/demanda_internacional/bce_sorpresas/*; mensuales, 1999-2025, sumadas por trimestre), choque monetario «puro», separado del de información.
- **Tipo:** tipo hipotecario (base:tipo_hip_bde) y euríbor a 1 año (base:euribor_1y).
- **Resultados:**
  - log del valor tasado real (principal; base:p_tasado / base:deflactor);
  - IPV (2007-);
  - compraventas (base:compraventas, 2007-);
  - IPC de alquiler real (base:ipc_alquiler, 2002-).
- **Controles:** PIB (base:pib_vol_idx), inflación (base:inflacion_ipc_yoy) y crédito nuevo (base:credito_nuevo).
- **Ventana:** 1999T1-2025T4. La sorpresa termina en 2025T4.

**Especificaciones:**
- **V18-E7-R1 (proyección local con instrumento).** y_t+h − y_t−1 = β_h·Δi_t + Σ_{l=1..4}(controles y rezagos) + ε_t+h, con Δi instrumentado por la sorpresa de Jarociński-Karadi, h = 0..12.
  - Contraste principal: h = 8, en % por +100 pb.
  - Resultados secundarios en la familia: IPV (**R1-ipv**), compraventas (**R1-cv**) y alquiler (**R1-alq**).
- **V18-E7-R2 (SVAR con instrumento externo).** VAR trimestral [tipo hipotecario, ln precio real, ln compraventas, ln PIB, IPCA, euríbor] con la sorpresa como proxy; respuesta a 8 trimestres escalada a +100 pb.
- **V18-E7-R3 (réplica de San Juan).** BVAR recursivo 2004-2022 con sus siete variables y su orden (visados: base:visados; saldo de préstamos de vivienda: base:credito_nuevo o el saldo si está en la base; se declara cuál). +100 pb a 8 trimestres, bandas al 68 % y al 90 %.

**(c) Ampliaciones:**
- **V18-E7-A1.** R3 hasta 2026T2.
- **V18-E7-A2 (panel provincial con exposición).** Δ_h ln p_pt = β_h·(choque_t × E_p) + α_p + γ_t + ..., con E_p = proporción media de compraventas con hipoteca en 2007-2019 (data/raw/ine_v2_hipotecas_prov.csv frente a data/raw/ine_v2_etdp_prov.csv, como aproximación), en 39 provincias.
  - El peso de la hipoteca variable provincial no existe: X1.
- **V18-E7-A3.** R1 y R2 con EA-MPD como choque alternativo. Solo cuando su licencia esté decidida (tareas_autor, punto 14); hasta entonces, no se estima.

**(d) Pruebas B4 y criterios:**
- **Raíces unitarias:** ADF y KPSS de las series en niveles; las LP en diferencias acumuladas no las requieren.
- **Estabilidad:** sup-F de ruptura en 2008 y 2015; raíces del VAR dentro del círculo unidad.
- **Primera etapa:** F efectivo > 10 con la sorpresa sobre Δ del tipo hipotecario. Q5 dio de 2,1 a 2,9 y V8, primera etapa de signo contrario: se espera que falle, y entonces decide el AR.
- **Sensibilidad a la identificación:** sorpresa «poor man's» frente a la mediana; choque total frente a choque monetario puro.
- **Placebos:** resultados que no deberían moverse (población total; Q5 dio −0,032 %); choque adelantado 8 trimestres.
- **Robustez de la medida:** valor tasado frente a IPV y frente a precio de Registradores (contraste interno); alquiler IPC frente a IPVA (2011-).
- **A2:** sin Barcelona; sin atípicos.

**(e) Inferencia B2:**
- **R1:** Newey-West con ancho h + 1 (NO APTO en V16 en su versión de b fija: tamaño 0,0642-0,0925). Alternativa: proyección local aumentada con rezagos y errores de Eicker-Huber-White (Monte Carlo nuevo). AR por horizonte con el F efectivo.
- **R2:** bandas robustas a la debilidad del instrumento (Montiel Olea, Stock y Watson, 2021) y bootstrap por bloques.
- **R3:** bandas bayesianas al 68 % y al 90 %.
- **A2:** Driscoll-Kraay y cluster por provincia con Webb (39).

**(f) Clasificación:**
- **R1 y R2:** IDENTIFICADO si el F efectivo > 10 o el AR a h = 8 es informativo (acotado y sin el cero), con pruebas superadas y razón con −2 % por 100 pb (San Juan) o −5 % (BCE) en [1/3; 3]. Con F < 5 y AR no informativo: ASOCIACIÓN.
- **R3:** ASOCIACIÓN como máximo (identificación recursiva, sin variación externa). Es una réplica de un resultado del Banco de España, y se dice.
- **A2:** SUGESTIVO como máximo (la exposición es endógena al mercado local).

**(g) NO ESTIMABLE:** A2-X1 (peso provincial de la hipoteca variable) requiere Registradores con autorización (tareas_autor, punto 8) o la EFF (punto 6). Las compras al contado por provincia requieren el Notariado (punto 7).

### 1.8 E8 · Fiscalidad de la compra (ITP)

#### Estudios clave
- Best y Kleven (2018), REStud 85(1) (ficha docs/v18/bib/fiscalidad/best_kleven_2018.md, solo resumen).
- Besley, Meads y Surico (2014), JPubE 119 (ficha besley_meads_surico_2016_lse.md).
- Dolls et al. (2025), JUE 145 (ficha dolls_etal_2020_vfs.md).
- Fritzsche y Vandrei (2019), RSUE 74 (ficha fritzsche_vandrei_2017_eres.md).
- No hay evaluación española del ITP con diseño. Esta sería la primera, y así se rotula.

**(a) Especificación original:**
- **Best y Kleven:** muescas del Stamp Duty y suspensión temporal de 2008-2009. Una rebaja de 1 punto eleva la actividad cerca de un 20 % a corto plazo, y se revierte menos de la mitad.
- **Besley et al.:** suspensión de 2008-2009. El precio después de impuestos baja unas 900 libras sobre una rebaja de unas 1.500 (≈ 0,6), y las transacciones suben en torno a un 8 %.
- **Dolls et al.:**
  - estudio de eventos mensual con las subidas escalonadas por Land desde 2006, unos 17 millones de registros, 2005-2018;
  - precio −3,5 % por +1 pp a 12 meses (versión de trabajo); −3 % en la publicada según V16.
- **Fritzsche y Vandrei:** efectos fijos con las subidas por Land. Unas 6 % menos compraventas por +1 pp a largo plazo, con anticipación grande.

**(b) Traslado:**
- **Tratamiento:** cambios del tipo general del ITP en las CCAA de régimen común no selladas (data/raw/v16/intervenciones/intervenciones.csv: Andalucía, Cantabria, Castilla y León, Castilla-La Mancha, Cataluña, C. Valenciana, Extremadura y Galicia).
- **Fechas:** la principal exige las fechas de entrada en vigor de cada ley autonómica (BOE y diarios oficiales, `posterior_prereg`). Las fechas aproximadas al 1 de enero solo entran en robustez, como en V16.
- **Resultados:**
  - compraventas de vivienda usada provinciales mensuales (data/raw/ine_v2_etdp_prov.csv; 2007-01 a 2026-07; se usa hasta el último mes visto en V16);
  - valor tasado provincial trimestral (base:valor_tasado).
- **Unidad:** 30 provincias de esas 8 CCAA (excluidos los territorios forales y Ceuta y Melilla).

**Especificaciones:**
- **V18-E8-R1 (Dolls).** Estudio de eventos del log del valor tasado por trimestre relativo al cambio, con dosis = Δ del tipo en pp.
  - Estimadores: de Chaisemartin-D'Haultfœuille (dosis continua) y Sun-Abraham para subidas y bajadas por separado.
  - Contraste principal: efecto a 4 trimestres por +1 pp.
- **V18-E8-R2 (Fritzsche-Vandrei / Best-Kleven).** Mismo diseño con el log de las compraventas mensuales.
  - Contraste principal: efecto a 12 meses por +1 pp.
  - Se publican los meses −1 y +1 (anticipación) sin contraste en la familia.

**(c) Ampliaciones:**
- **V18-E8-A1 (primera etapa fiscal).** Recaudación del ITP por CCAA (liquidación de tributos cedidos, Hacienda, abierta, `posterior_prereg`) frente al cambio del tipo.
- **V18-E8-A2.** R2 con compraventas municipales de los municipios grandes (data/raw/mivau_transacciones_municipios.csv, trimestral).
- **V18-E8-X1 (bunching en los umbrales de los tipos reducidos).** NO ESTIMABLE: no hay compraventas por tramo de precio (tareas_autor, punto 7).
- **V18-E8-X2 (tipos reducidos para jóvenes y familias).** NO ESTIMABLE sin el calendario de tipos reducidos.

**(d) Pruebas B4 y criterios:**
- **Pretendencias:** adelantos de −8 a −2 trimestres (R1) o de −12 a −2 meses (R2, excluido el mes −1), con p > 0,10.
- **Honest DiD:** con M̄ hasta 1.
- **Placebo de fecha:** 2 años antes, p > 0,10. Q6-v dio un placebo con ΔY retardado mayor que el efecto: el fallo ya visto se declara.
- **Placebo de resultado:** log de la población.
- **Robustez:** con fechas del 1 de enero (robustez); sin Barcelona; sin 2012-2013 (los cambios están concentrados ahí); precio con IPV por CCAA.

**(e) Inferencia B2:**
- Tratamiento por CCAA: 8 clusters.
- Wild cluster bootstrap de Webb e inferencia por aleatorización del calendario entre CCAA y años. La aleatorización de dCDH fue NO APTO en V16 (tamaño 0,0775): Monte Carlo nuevo.
- Driscoll-Kraay como alternativa.

**(f) Clasificación:**
- **IDENTIFICADO** si cumple I1 a I8 con inferencia apta en 8 clusters y razón con −3 % a −3,5 % por pp (Dolls) en R1, o con −6 % (Fritzsche-Vandrei) en R2, en [1/3; 3].
- Con fechas solo aproximadas, SUGESTIVO como máximo.
- La potencia es baja: el MDE de V16 fue de 9,4 a 18,8 %. Un nulo no se lee como ausencia de efecto salvo que su IC95 excluya ± la mitad de la referencia.

**(g) NO ESTIMABLE:** X1 y X2 requieren el Notariado o la AEAT (modelo 600) por tramo (tareas_autor, punto 7) y el calendario de tipos reducidos (fuente abierta: leyes autonómicas). Los territorios forales requieren sus tipos y no entran en la réplica.

### 1.9 E9 · Compradores no residentes

#### Estudios clave
Badarinza y Ramadorai (2018; ficha docs/v18/bib/no_residentes/badarinza_ramadorai_2015_bde_conf.md), Sá (2016; ficha sa_2016_lse_cfm2016_39.md) y Cvijanović y Spaenjers (2021; ficha cvijanovic_spaenjers_2020_warwick.md). Referencia española sin instrumento: Álvarez, Blanco y García-Posada (2020; ficha alvarez_blanco_garciaposada_2020_bde_be2002art14.md).

**(a) Especificación original:**
- **Badarinza y Ramadorai:**
  - Londres, 1995-2013;
  - barrios con alta cuota de residentes de un país × meses de riesgo alto en ese país;
  - +1,62 pp de precio (quintil superior frente a los demás);
  - +2,21 pp en barrios de renta alta;
  - efectos transitorios, de unos dos años.
- **Sá:**
  - autoridades locales de Inglaterra y Gales, 1999-2014;
  - cuota de compras de sociedades extranjeras instrumentada con el riesgo económico exterior × el origen censal;
  - +2 % de precio por +1 pp de cuota en volumen (IV) y +1,4 % en valor.
- **Cvijanović y Spaenjers:** París; flujos por nacionalidad repartidos con el censo de 1982; efecto positivo, pequeño y no significativo.
- **Álvarez et al.:** MCO transversal entre 50 provincias, 2013T4-2019; 2,55 (2,26) y 2,44 (1,68), no significativos.

**(b) Traslado:**
- **Unidad:** 39 provincias no selladas, trimestral o anual, 2007-2025. Fuera, por el sellado: Baleares, Las Palmas, Santa Cruz de Tenerife y Murcia, cuatro de las de más cuota de no residentes. Quedan Alicante, Málaga y Girona.
- **Exposición:** cuotas de residentes por nacionalidad del padrón de 2003 (data/raw/v9/ine_padron_nacionalidad/padron_nacionalidad_2003_2022.csv.gz). Es población residente, no compradores: aproximación declarada.
- **Riesgo en origen** (data/raw/eu_hpi.csv, data/raw/oecd_house_prices.csv, data/raw/eu_income_emp.csv):
  - caída del PIB o del empleo de cada país de origen;
  - variación del precio de la vivienda en origen;
  - tipo de cambio bilateral frente al euro en los orígenes fuera del euro (BCE, abierto, `posterior_prereg`).
- **Endógena (para la IV de Sá):** cuota de compras de no residentes sobre el total por provincia (data/raw/mivau_transacciones_residencia.csv; nivel provincial según output/v16/q8/q8_provincias.csv).
- **Precio:** valor tasado provincial.

**Especificaciones:**
- **V18-E9-R1 (Badarinza-Ramadorai, forma reducida).** Δln p_pt = β·Σ_c s_pc,2003·riesgo_ct + α_p + γ_t + ε_pt.
  - riesgo_ct = indicador de que la caída del PIB del país c está en el quintil superior de su historia, con el efecto medio a 4 trimestres.
- **V18-E9-R2 (Sá, IV).** Δln p_pt = β·Δcuota_no_residentes_pt + ..., con la cuota instrumentada por el índice de R1. Unidad: % de precio por +1 pp de cuota.

**(c) Ampliaciones:**
- **V18-E9-A1.** R1 con el tipo de cambio como choque (la libra en 2016 y otras monedas fuera del euro).
- **V18-E9-A2.** R2 con compras de extranjeros residentes (base:tx_extranj_ccaa; CCAA, 9 no selladas) como resultado de la primera etapa alternativa.
- **V18-E9-X1 (fin de la golden visa como diferencias en diferencias, LO 1/2025).** NO ESTIMABLE: no hay compras separadas entre la UE y fuera de la UE, ni autorizaciones de la OPI (tareas_autor, punto 14). Q8 es solo descriptivo (−1,33 pp, con −0,68 pp el año anterior).
- **V18-E9-X2 (introducción de 2013, Martínez-Toledano et al.).** NO ESTIMABLE: requiere el universo de transacciones (ficha martinez_toledano_etal_2025.md, solo resumen).

**(d) Pruebas B4 y criterios:**
- **Primera etapa (R2):** F efectivo > 10.
- **Pretendencias:** el índice de riesgo de t+4 no predice Δp de t (p > 0,10).
- **Rotemberg:** sin los 3 orígenes de mayor peso (se espera el Reino Unido, Alemania y Francia), mismo signo y dentro del IC95.
- **Balance de los choques:** frente a la cuota extranjera, la renta y el paro de 2003.
- **Robustez:** sin Alicante; sin Málaga; sin Barcelona; sin atípicos; exposición con Registradores 2016 (contraste interno); precio con IPV por CCAA.

**(e) Inferencia B2:**
- BHJ a nivel de origen (pocos choques: unos 10 a 15 orígenes; con menos de 20 choques efectivos, BHJ no es fiable y la principal pasa a cluster por provincia con Webb).
- AKM0 y Driscoll-Kraay.
- AR y F efectivo en R2.

**(f) Clasificación:**
- **R2:** IDENTIFICADO si cumple I1 a I8 con razón con +2 % por pp (Sá) en [1/3; 3].
- **R1:** como máximo SUGESTIVO (forma reducida, con la exposición aproximada por residentes).
- La comparación con Álvarez et al. (2020) es solo de signo: es MCO transversal.

**(g) NO ESTIMABLE:**
- X1: autorizaciones de la OPI y compras por nacionalidad UE/fuera de la UE por provincia (tareas_autor, puntos 7 y 14).
- X2: universo de transacciones (Registradores o Notariado).
- La exposición por compradores, en vez de residentes, requiere el Notariado por provincia y nacionalidad (punto 7).

### 1.10 E10 · Grandes tenedores e inversores institucionales
Fichas: docs/v18/bib/grandes_tenedores/mccarthy2026.md y francke2023.md. No hay estudios con datos españoles (fase 1).

**(a) Especificación original:**
- **McCarthy (Irlanda, 2007-2019):** diferencias en diferencias escalonadas (Mundlak-Wooldridge) con el registro de contratos. Renta +0,041 (≈ 4,1 pp) tras una compra institucional; indirecto +0,023 (0,007) a 100 m.
- **Francke et al. (Países Bajos, 2019-2022):** prohibición de comprar para alquilar. Precio +0,1 % (IC95 −1,5 a +1,7); renta +0,043 (0,013).

**(b) Traslado.** Falta la variación: la titularidad por tramo solo tiene tres cortes (2024-2026) y la serie de 2012-2023 tiene otra definición (data/raw/v11/catastro_titularidad/p_spi_mun_v_tpf.csv.gz; base:v12_titularidad_pct_mas10). SERPAVI termina en 2024.

**Especificaciones:**
- **V18-E10-X1 (réplica de McCarthy).** NO ESTIMABLE.
- **V18-E10-A1 (asociación transversal).** ln SERPAVI_m,2024 y Δln SERPAVI_m,2019-2024 frente al % de viviendas de titulares con más de 10 inmuebles en 2024, con efectos de provincia y controles de renta ADRH y población, en los municipios no sellados.
  - Clasificación máxima: ASOCIACIÓN. El orden temporal está invertido y no hay variación exógena.

**(d)-(e) para A1:**
- Robustez: sin Barcelona; con el % de personas jurídicas (base:v12_titularidad_pct_pj).
- Inferencia: Conley a 10 km y cluster por provincia con Webb.

**(f) Clasificación:** ASOCIACIÓN como máximo.

**(g) Qué lo haría estimable:**
- serie homogénea de titularidad 2012-2026 (tareas_autor, punto 9);
- Panel de Hogares AEAT-IEF (punto 10);
- compras de personas jurídicas por provincia del Notariado (punto 7);
- con ellas, un diseño escalonado de entrada de grandes tenedores por zona frente a la renta de contratos.

### 1.11 E11 · Viviendas vacías
Ficha docs/v18/bib/vacias/segu2020.md. No hay estudios con datos españoles (fase 1).

**(a) Especificación original (Segú, Francia):**
- diferencias en diferencias con emparejamiento por puntuación de propensión sobre la primera diferencia de la vacancia fiscal 1997-2001;
- 6 clusters tratados y 23 de control;
- bootstrap por bloques de unidad urbana;
- vacancia −0,799 (0,146) pp en 2001, ≈ −13 %.

**(b) Traslado.** Falta el tratamiento: no están la adopción municipal del recargo del IBI (Ley 12/2023) ni el calendario del impuesto catalán. La vacancia solo tiene dos cortes con métodos distintos: el Censo de 2011 y el de 2021, este por consumo eléctrico.

**Especificaciones:**
- **V18-E11-X1 (recargo del IBI).** NO ESTIMABLE.
- **V18-E11-X2 (impuesto catalán sobre viviendas vacías).** NO ESTIMABLE (calendario y bases no localizados).

**(c)-(f):** no aplican. No se estima nada: con dos cortes de métodos distintos, cualquier diferencia en diferencias confundiría el método con el efecto.

**(g) Qué lo haría estimable:**
- ordenanzas fiscales con la fecha de adopción del recargo (tareas_autor, punto 12);
- la estadística experimental del INE de vacías por consumo, si existe en serie anual (abierta, por verificar);
- las vacías por municipio en 2011 (INE, abierto).
- Con ellas: diferencias en diferencias escalonadas de los municipios con recargo frente a los que no lo tienen sobre la vacancia anual y el SERPAVI municipal, con las pruebas de 0.7 y cluster por municipio. Se escribirá una adenda antes de mirarlos.

### 1.12 E12 · Vivienda pública
Fichas: docs/v18/bib/vivienda_publica/chapelle_2015_tresor.md y chapelle_gobillon_vignolles_2025_iza.md.

**(a) Especificación original (Chapelle, Francia, 1999-2010):**
- variación del parque privado sobre la contribución de la vivienda social, por MCO e IV;
- instrumento shift-share: tendencia nacional × peso inicial local (F de 445,6);
- efectos fijos de departamento;
- IV −1,604 (0,219) viviendas privadas por vivienda social; MCO +1,070 (0,125).

**(b) Traslado.**
- No hay promociones públicas por municipio y año.
- Sí hay calificaciones de vivienda protegida por provincia y año (data/raw/mivau_v2_protegida.csv, 1991-2026), que incluyen la promoción privada protegida, y obra libre iniciada y terminada por provincia (data/raw/mivau_v2_iniciadas_terminadas_prov.csv).

**Especificaciones:**
- **V18-E12-X1 (promociones públicas, réplica).** NO ESTIMABLE.
- **V18-E12-A1 (desplazamiento de la obra libre por la protegida, estilo Chapelle).** ΔLibre_pt / Parque_p,t−1 = β·ΔProtegida_pt / Parque_p,t−1 + α_p + γ_t + ε_pt, 2002-2025, 39 provincias, con ΔProtegida instrumentada por (calificaciones nacionales sin la propia provincia)_t × cuota provincial de protegidas en 1991-1995.
  - Mide la vivienda **protegida**, no la pública. Se rotula así.
- **V18-E12-A2.** A1 con el valor tasado provincial como resultado.

**(d) Pruebas B4 y criterios:**
- F efectivo > 10;
- pretendencias: el instrumento de 2002-2007 no predice ΔLibre de 1996-2001 (p > 0,10);
- exclusión: la cuota de 1991-1995 no se asocia con el crecimiento del PIB provincial de 1995-2001;
- sin Barcelona; sin atípicos.

**(e) Inferencia B2:** cluster por provincia con Webb (39), Driscoll-Kraay, AR y F efectivo.

**(f) Clasificación:** A1 y A2, como máximo SUGESTIVO: el estimando difiere del original (protegida frente a pública) y la exclusión del instrumento de tendencia es discutible, como avisan los propios autores.

**(g) Qué lo haría estimable:** promociones públicas por municipio y año con número de viviendas, régimen y fechas (MIVAU, CASA 47 y empresas públicas autonómicas; tareas_autor, punto 11).

### 1.13 Herramientas que requieren Monte Carlo antes de usarse (agente montecarlo)
Cada una se valida con un proceso generador que reproduce la estructura del diseño: unidades no selladas, periodos, número de clusters, calendario, distancias, número de choques y dependencia transversal. Los resultados son simulados: ningún dato real de resultado ni ninguna muestra sellada.

Criterio: tamaño al 5 % en [0,03; 0,08] y cobertura al 95 % en [0,92; 0,97], con R ≥ 2.000. Fuera de ese rango, se aplican las bandas de 0.4. Resultados en output/v18/montecarlo/ y en metodologia/validacion_montecarlo_v18.md (con make publicacion).

| Herramienta | Diseños | Estado previo |
|---|---|---|
| BHJ a nivel de choque (bhj_lib: `iv_cluster`, `ar_ic_nulo_impuesto`) con 39 provincias y 10 a 30 choques | E3-R1, R2, A1, A2; E5-R1; E9-R1, R2 | Código reproducido (fase 2); sin Monte Carlo con nuestra estructura |
| AKM y AKM0 | Alternativa en E3, E5 y E9 | NO APTO en V16 (0,3762 y 0,0108) |
| Wild cluster bootstrap de Webb en TWFE con 8, 30 y 39 clusters | E5, E6-R2, E7-A2, E8, E9, E12 | Sin validar en V18; cs_webb NO APTO en V16 |
| Callaway-Sant'Anna y Sun-Abraham con Webb | E2-A1, E6-R1, E8 | NO APTO en V16 |
| de Chaisemartin-D'Haultfœuille con dosis continua y aleatorización | E8-R1, R2 | NO APTO en V16 (0,0775) |
| Honest DiD (Rambachan-Roth, magnitudes relativas) | E1-R3, R4, A2; E2; E6-R1; E8 | Implementación de V9 con tamaño del 7,3 % en 400 réplicas: se revalida o se sustituye |
| SDID y Conley-Taber con pocos tratados | E2-A1, A2 | Conley-Taber APTO en V16 (escenario A, 0,0575): se revalida |
| Inferencia por aleatorización (permutaciones) | E2, E8 | Sin validar en V18 |
| PPML con cluster por municipio | E2-R2, R1c | Sin validar |
| Conley (1, 2, 10 y 25 km) en sección y municipio | E1, E5-A3, E6-R1, E10-A1 | NO APTO en V16 en sección (0,0963) |
| Driscoll-Kraay en paneles provinciales con T de 14 a 30 | E3, E5, E7-A2, E8, E12, F1-F3 | Sin validar en V18 |
| F efectivo de Montiel Olea-Pflueger e intervalos AR (también con dos endógenas en E3-A4) | Toda IV | Sin validar en V18 |
| Proyección local con instrumento: Newey-West y versión aumentada con rezagos (EHW) | E7-R1 | Newey-West de b fija NO APTO en V16 |
| SVAR con proxy y bandas robustas a la debilidad | E7-R2 | Sin validar |
| BVAR recursivo (cobertura de las bandas) | E7-R3, A1 | Sin validar |
| DOLS con Driscoll-Kraay, PMG, MG, CS-ARDL, CIPS y Westerlund | F1-R2, F1-A1, F2, F3 | CS-ARDL y CIPS NO APTOS en V16 |
| Metaanálisis bayesiano de efectos aleatorios (cobertura de μ y de τ con 2 a 10 estudios) | Sección 3 | Modelo jerárquico de V16 NO APTO (otra especificación): se valida el nuevo |
| Propagación por Monte Carlo de la contabilidad (comprobación de que el intervalo de la suma es coherente con extracciones conjuntas) | Sección 4 | Comprobación de código, no de tamaño |

Ninguna estimación se clasifica con una herramienta sin su veredicto. Las réplicas de los estudios con paquete (fase 2) no sustituyen al Monte Carlo: validan el código, no su tamaño con nuestra estructura.

---

## 2. Modelos de conjunto F1-F4

### 2.1 F1 · Precio de largo plazo con corrección del error (nacional y panel provincial)

#### Estudios clave
Álvarez y García-Posada (2019), Banco de España DT 1941 (ficha docs/v18/bib/modelos_conjunto/alvarez_garciaposada_2019_bde_dt1941.md), y Martínez Pagés y Maza (2003), DT 0307 (ficha martinez_pages_maza_2003_bde_dt0307.md). Comparación: rango de sobrevaloración del IEF (fichas bde_2025_ief_otono_cap4.md y bde_2026_ief_primavera_cap4.md).

**(a) Especificación original:**
- **DT 1941:**
  - 50 provincias, 1985-2018;
  - precio de Sociedad de Tasación de vivienda nueva, deflactado con el IPC provincial;
  - DOLS con efectos fijos y errores de Driscoll-Kraay;
  - ECM con efectos fijos dinámicos y PMG;
  - vector básico: renta per cápita 0,629 (0,089), paro −0,009 (0,003), densidad 1,032 (0,162);
  - vector alternativo: renta 0,409 (0,037), paro −0,011, tipo hipotecario nominal −0,015 (0,004), parque per cápita −0,268 (0,045), densidad 0,079;
  - ajuste −0,068 (0,014) con efectos fijos dinámicos y −0,085 (0,006) con PMG.
- **DT 0307:** ECM anual 1976-2002; elasticidad de renta de 2,8 sin restricción; con renta unitaria, crédito 0,35 y tipo nominal −4,5.
- **IEF del Banco de España:** sobrevaloración del 10-15 % en diciembre de 2025 y del 5,3-12,7 % en junio de 2025 (rango entre métodos).

**(b) Traslado:**
- **Nacional:**
  - log del valor tasado real (base:p_tasado / base:deflactor);
  - log de la renta disponible real de los hogares (base:renta_hog_real, 1999T1-);
  - tipo hipotecario real (base:tipo_hip_real_bde, 1996T1-);
  - log de la población de 20 a 64 años o, si no está, la total (base:pob_total);
  - ventana 1999T1-2026T2.
- **Parque por hogar** (data/raw/mivau_parque.csv): es anual (2001-2025). Entra solo en la versión anual: repetir el dato en los trimestres sería una interpolación, solo admitida en robustez.
- **Provincial (39 provincias):**
  - valor tasado real (base:valor_tasado; IPC provincial como deflactor si está en la base, y si no el nacional, declarado);
  - renta disponible bruta de los hogares por provincia (INE, Contabilidad Regional, abierta, `posterior_prereg`);
  - paro (EPA provincial);
  - densidad (pob_total / superficie);
  - tipo hipotecario nacional;
  - parque per cápita (data/raw/mivau_parque.csv);
  - anual, 2000-2024.

**Especificaciones:**
- **V18-F1-R1 (nacional, trimestral).** ECM de Engle-Granger y ARDL de Pesaran-Shin-Smith (contraste de límites) con ln p = β1·ln renta + β2·tipo real + β3·ln población.
  - Velocidad de ajuste y desviación respecto al equilibrio, por trimestre.
- **V18-F1-R2 (réplica del DT 1941, provincial).** DOLS con efectos fijos (±1 adelanto y retardo) y Driscoll-Kraay, vector básico [renta, paro, densidad] y vector alternativo [renta, paro, tipo, parque per cápita, densidad] (**R2-alt**). Más ECM por PMG (**R2-pmg**). Ventana 2000-2018, la más parecida.

**(c) Ampliaciones:**
- **V18-F1-A1.** R2 hasta 2024 y con CS-ARDL (dependencia transversal).
- **V18-F1-A2.** R1 en frecuencia anual 2001-2025 con el parque por hogar (vector completo de la sección F del plan).
- **V18-F1-A3.** Sobrevaloración: desviación del precio respecto a su equilibrio con R1, A2 y R2 (media provincial ponderada por población), comparada en rango con el IEF.

**(d) Pruebas:**
- Raíces unitarias: ADF y KPSS nacionales; CIPS en el panel con valores críticos por bootstrap (NO APTO en V16: Monte Carlo nuevo).
- Cointegración: contraste de límites de ARDL; Westerlund con bootstrap en el panel.
- Estabilidad de los coeficientes de largo plazo: recursivos y sup-F en 2008 y 2014.
- Dependencia transversal: CD de Pesaran.
- Sensibilidad: con y sin 2008-2013; precio con IPV (desde 2007, CCAA) y Registradores (contraste interno).
- Fuera de muestra: comparación con el AR(4) y con el ECM v1 en la misma muestra, con validación en bloques con embargo (CLAUDE.md); se rellena el campo fuera_muestra de resultado.json.

**(e) Inferencia B2:** Newey-West en R1 y A2; Driscoll-Kraay en R2 y A1; PMG con sus errores asintóticos y bootstrap por bloques de provincia.

**(f) Clasificación.** F1 no tiene diseño cuasi experimental: las elasticidades de F1 son ASOCIACIÓN como máximo. Sirven para la coherencia de F4, no para la sección 4 como si fuesen efectos.

**(g) NO ESTIMABLE:** sin la renta disponible de los hogares por provincia, R2 usa el PIB provincial per cápita (data/raw/ine_v2_cre.csv), declarado como sustituto. Los hogares por provincia anteriores a 2021 requieren la EPA provincial (abierta).

### 2.2 F2 · Alquiler equivalente por provincia
**(a) Referencia.** No hay un estudio del Banco de España con este modelo en las fichas. La especificación sigue el vector de F1 con el alquiler como resultado (plan, sección F2).

**(b) Traslado.**
- Resultado: log del IPC de alquiler provincial real (2002-2025; stock).
- Variante: SERPAVI provincial (2011-2024).
- Regresores: renta de los hogares provincial, hogares (EPA provincial, `posterior_prereg`; antes de 2021), parque y tipo hipotecario real.
- Anual, 39 provincias.

**Especificaciones:**
- **V18-F2-R1.** PMG del alquiler sobre renta, hogares, parque y tipo.
- **V18-F2-A1.** CS-ARDL.
- **V18-F2-A2.** Ratio precio/alquiler y coste de uso (tipo real + 2 % de amortización − ganancia esperada), como en E1 de V15 (`repite_visto`).

**(d)-(f).** Las pruebas son las de F1. La clasificación máxima es ASOCIACIÓN. La serie de SERPAVI en niveles es corta (14 años): A1 con SERPAVI solo es descriptiva si el Monte Carlo de CS-ARDL con T = 14 no da tamaño apto.

### 2.3 F3 · Elasticidad de la oferta y del parque
**(a) Referencia.** Taltavull (2006): MC2E con datos de panel de CCAA, 1987-2004; 0,87 en el panel de 1990-2004 (ficha taltavull_2006_funcas.md).

**(b) Traslado.**
- Iniciadas y terminadas provinciales.
- Valor tasado real.
- Costes: base:costes_constr (nacional) y precio del suelo provincial (data/raw/mivau_v2_suelo.csv, 2004-).
- Crédito a promotores (base:credito_promotor, nacional).
- 39 provincias, 2004-2025.

**Especificaciones:**
- **V18-F3-R1 (réplica de Taltavull).** MC2E en el panel de las 9 CCAA no selladas, 1995-2004, con instrumentos de coste y precio retardados.
- **V18-F3-A1.** R1 hasta 2025.
- **V18-F3-A2.** PMG provincial de ln iniciadas sobre ln precio real, ln coste del suelo y crédito a promotores.
- **V18-F3-A3.** A2 con el precio instrumentado por el Bartik de E5-R1 (la versión «de conjunto» de E5).

**(d)-(f).**
- R1, A1 y A2: ASOCIACIÓN, porque los instrumentos retardados no son exógenos.
- A3 hereda los criterios de E5-R1: F efectivo > 10 y pruebas de E5. Como máximo, la clasificación de E5-R1.
- Inferencia: Driscoll-Kraay; cluster por provincia con Webb.
- Las restricciones físicas son NO ESTIMABLES (tareas_autor, punto 5).

### 2.4 F4 · Coherencia
Comparaciones fijadas antes de estimar (signo y orden de magnitud: razón en [1/3; 3] o IC95 solapados):

| Comparación | Elasticidad de conjunto | Elasticidad de la sección E |
|---|---|---|
| F4-1 | Población en F1 (precio) | E3-R2 y E3-A1 (precio por 1 % de población) |
| F4-2 | Hogares en F2 (alquiler) | E3-A2 (alquiler) |
| F4-3 | Tipo real en F1 (semielasticidad) | E7-R1 y E7-R2 (% por +100 pb), convertidas a largo plazo con la velocidad de ajuste de F1 |
| F4-4 | Precio en F3 | E5-R1 |
| F4-5 | Parque per cápita en F1 | E6-R2 (alquiler) y E5-R1, solo en signo |

Si no son compatibles, se explica por qué: corto frente a largo plazo, medida, periodo, o identificación frente a asociación. La sección 4 usa la combinación más defendible, que es la elasticidad de la sección E si es IDENTIFICADO o SUGESTIVO, y deja la de F como sensibilidad. La elección se hace con esta regla y no a la vista de la contabilidad.

---

## 3. Magnitud preferida por factor (B5)

**B5 (texto del plan).** Para cada factor, combina nuestras estimaciones (IDENTIFICADO o SUGESTIVO) con las de la literatura en la misma unidad, mediante un metaanálisis bayesiano de efectos aleatorios. Si hay muy pocos estudios, haz una media ponderada por precisión y enséñala junto a cada estimación. Resultado: magnitud preferida con su intervalo y heterogeneidad. Si las unidades no son comparables, no se combinan y se dice.

**Qué entra:**
- **Nuestras estimaciones:** solo las IDENTIFICADO o SUGESTIVO, una por identificador (la principal; nunca varias variantes del mismo diseño).
- **Literatura:**
  - estudios con diseño cuasi experimental o estructural con identificación declarada (criterios de docs/v18/bib/criterios.md);
  - en la misma unidad;
  - con error típico disponible o reconstruible desde el IC o el t;
  - en la versión publicada si la ficha la ha leído, y si no en la versión leída, declarada.
- **Qué no entra:** los «solo resumen» sin error, las asociaciones (MCO transversal) y los descriptivos. Se muestran al lado.

**Unidad común por factor (con la conversión que se permite):**

| Factor | Unidad común | Conversión permitida | Estudios candidatos (ficha) |
|---|---|---|---|
| E1 | Δln alquiler por +1 pp de viviendas turísticas sobre el parque | «Por 100 anuncios» solo se convierte si el estudio da viviendas por unidad; el dato se lee en la fuente en la fase 5 y se documenta. Si no, no se combina | segu2018 (0,038 por pp); garcialopez2020, chavesfonseca2026, duso2024 si son convertibles |
| E2 | ATT en ln de la renta de los contratos regulados; aparte, ln de los contratos | Ninguna | jofremonseny2023 (−0,044), monras2023 (−0,058), breuille2025 (−0,051), hahn2021 (−0,113 / −0,075) |
| E3 | % de precio (o de alquiler) por 1 % de población por entrada de inmigrantes | Semielasticidad por punto de tasa de inmigración ≈ % por 1 %; elasticidad respecto a la población en edad de trabajar, declarada como aproximación | gonzalez_ortega_2009_iza (3,2), gonzalez_ortega_2011_chicagofed (0,866 / 0,997), sanchis_guarner_2017_lse (3,046; alquiler 0,947), saiz_2007_philly (1,607; 0,935), sa_2015_iza (−1,627), accetturo_2012_bdi, unal_2022_marburg |
| E4 | θ: euros de alquiler por euro de ayuda | Grislain-Trevien solo con la θ implícita, marcada «cálculo del auditor de V17» | fack_2005_cepremap, kangasharju_2008_vatt458, eerola_etal_2026_jpube (0,036), collinson_ganong_2016_jchs, hyslop_rea_2018_motu |
| E5 | Elasticidad precio de la oferta de unidades | Ninguna (no se mezclan unidades con superficie) | taltavull_2006_funcas, baum_snow_han_2020_nberconf (0,26 / 0,31), paciorek_2012_feds (0,84 IV) |
| E6 | % del alquiler por 1 % de oferta nueva | Asquith está en otra unidad (Δln cerca de un edificio): no se combina con Mense | mense_2025_jpemacro (−0,192), li_2022 (−0,1; solo resumen, sin error: fuera) |
| E7 | % del precio real por +100 pb del tipo hipotecario a 8 trimestres | Escalado lineal solo si el autor lo hace; las «conversiones del bibliotecario» no entran | sanjuan_2023 (≈ −2), bce_eb_2022_6 (−5, sin error: fuera del metaanálisis, al lado) |
| E8 | % de precio por +1 pp del ITP a 12 meses; aparte, % de compraventas por +1 pp | Ninguna | dolls_etal_2020_vfs (−3,5 / −3), fritzsche_vandrei_2017_eres (−6, volumen), berard_trannoy_2018_insee |
| E9 | % de precio por +1 pp de cuota de compras de no residentes | Ninguna | sa_2016_lse_cfm2016_39 (2 / 1,4) |
| E10-E12 | No se combina: no hay estimación propia IDENTIFICADO o SUGESTIVO prevista, salvo E12-A1, cuya unidad (viviendas libres por vivienda protegida) se compara con chapelle_2015_tresor sin combinarla, por ser otra intervención | — | — |

**Modelo (si hay 3 estudios o más en la misma unidad):**
- y_i ~ N(θ_i, se_i²); θ_i ~ N(μ, τ²).
- Prior de la media: μ ~ N(0, s_f²), con s_f fijado antes de ver ningún resultado propio, en la unidad del factor:
  - E1: 0,1;
  - E2: 0,1;
  - E3: 3;
  - E4: 1;
  - E5: 2;
  - E6: 0,5;
  - E7: 10;
  - E8: 5 (precio) y 20 (volumen);
  - E9: 5.
  Es el orden de magnitud del rango de la literatura de cada factor, sin centrarlo en ningún estudio.
- Prior de la heterogeneidad: τ ~ semi-normal(0, (s_f/2)²).
- Sensibilidad: s_f × 2 y s_f / 2, y τ ~ semi-Cauchy(0, s_f/2).
- Cálculo: muestreo NUTS (4 cadenas, SEED = 20261010; R̂ < 1,01 y tamaño efectivo > 1.000) o cuadratura determinista si el número de estudios es pequeño.
- Se publican: μ con su intervalo de credibilidad al 95 %, τ, I² y el intervalo de predicción de un estudio nuevo. Además, la versión solo con estudios españoles y la versión solo con estudios europeos, si cada una tiene 3 o más.
- Herramienta validada por Monte Carlo (1.13).

**Con menos de 3 estudios:** media ponderada por la inversa de la varianza (efecto fijo), con su IC95, mostrada junto a cada estimación individual. Sin τ.

**Cuándo no se combinan:**
- Si las unidades no son convertibles con las reglas de la tabla.
- Si nuestra estimación y la literatura miden intervenciones distintas (por ejemplo, la protegida frente a la social en E12).
- Si el I² supera el 75 % con 3 o más estudios y el intervalo de predicción cambia de signo. Entonces se publica el rango de estudios sin magnitud preferida y se dice.
- **E4** se rotula «solo literatura, sin estimación propia» (V18-E4-L1).

Identificadores: **V18-B5-E1** … **V18-B5-E9**, y **V18-B5-F** para las elasticidades de conjunto mostradas al lado, sin combinar.

---

## 4. Contabilidad de la subida (fase 5)

**Qué es.** Contabilidad con elasticidades estimadas: contribución_f = magnitud preferida_f × variación observada del factor f. **No es una descomposición estructural.** No hay interacciones ni efectos de equilibrio general, y los factores no son ortogonales. Se dice así en cada tabla.

**Periodos.** Se alinean con V8 (docs/v8/hipotesis.md) para poder comparar:
- 1995T1-2007T4;
- 2008T1-2013T4 (V8 empieza P2 en 2008T3: se publica también con ese inicio);
- 2014T1-2019T4;
- 2020T1-2022T2 (V8: 2020T2);
- 2022T3-2026T2.

**Resultados:**
- variación del log del precio real de compra: valor tasado deflactado (principal); IPV desde 2007 (robustez);
- variación del log del alquiler real: IPC de alquiler desde 2002 (principal, stock); SERPAVI 2011-2024 (robustez).
- 1995-2007 no tiene alquiler.

**Territorios:**
- nacional;
- 9 CCAA no selladas;
- 39 provincias donde la variación del factor exista por provincia;
- grandes ciudades no selladas (Barcelona, València, Sevilla, Málaga, Alicante, Bilbao y las demás con dato), solo para los factores con dato municipal (turismo, inmigración, topes).

Las tablas provinciales no suman el total nacional (faltan las 11 provincias selladas). Ninguna cifra nacional se obtiene sumando provincias.

**Variación observada de cada factor (fuente):**

| Factor | Variable | Fuente | Unidad compatible con B5 |
|---|---|---|---|
| Inmigración | Δ de la población extranjera / población inicial (pp) | base:pob_extranjera, base:padron_pob_nacionalidad, base:ecp_pob_nacionalidad | % de precio por 1 % de población |
| Turismo | Δ del % de viviendas turísticas | INE-VUT (2020-), HUT de Barcelona y registros; antes de 2020 «no medido» (no cero) | Δln por pp |
| Tipos | Δ del tipo hipotecario (pb) | base:tipo_hip_bde | % por +100 pb |
| Oferta | Δ del log de las terminadas o del parque por hogar | data/raw/mivau_parque.csv, base:terminadas | elasticidad |
| Topes | Proporción de contratos en municipios regulados × vigencia | Incasòl, Ley 11/2020 (Cataluña, 2020T4-2022T1) | ATT |
| ITP | Δ del tipo general (pp) | data/raw/v16/intervenciones/intervenciones.csv (con fechas corregidas) | % por pp |
| No residentes | Δ de la cuota de compras de no residentes (pp) | data/raw/mivau_transacciones_residencia.csv | % por pp |
| Renta y fundamentales (F1, solo sensibilidad) | Δ del log de la renta real | base:renta_hog_real | elasticidad (ASOCIACIÓN) |

**Qué factores entran:**
- **Principal:** solo los factores con magnitud preferida construida con al menos una estimación V18 IDENTIFICADO o SUGESTIVO.
- **Secundaria (rotulada):** añade las magnitudes «solo literatura» en la misma unidad (por ejemplo E4) y las de F1 (ASOCIACIÓN), como sensibilidad.
- **Sin doble cómputo:** inmigración (E3) y población (F1) no se suman; tipos (E7) y crédito no se suman. Si un factor no tiene magnitud, su fila dice «sin magnitud», no cero.

**Propagación de la incertidumbre:**
- 10.000 extracciones con SEED = 20261010.
- Magnitud: de la distribución posterior de B5 o, si es una media ponderada, de N(μ̂, se²).
- Variación observada: con dos fuentes, uniforme entre ellas; con una, la variación publicada sin error (declarado).
- Independencia entre factores, con sensibilidad a una correlación de ±0,5 entre magnitudes del mismo modelo.
- Se publica la mediana con los intervalos al 68 % (para comparar con V8) y al 90 %.

**Fila «no explicado».** Δ observada menos la suma de contribuciones, extracción a extracción, con su intervalo. Se publica siempre, también cuando supera el 100 % o es negativa.

**Comparaciones:**
- **Con V8:** descomposición histórica del SVAR (C3s, bandas del 68 %, cinco choques en P2-P5 y tres en P1; ningún factor designado). Por periodo, se compara el signo y si los intervalos se solapan con estas correspondencias: demográfico ↔ inmigración; crédito y tipos ↔ tipos; oferta ↔ oferta; actividad y renta ↔ renta de F1 (sensibilidad).
- **Con el Banco de España:**
  - sobrevaloración del IEF (10-15 % en diciembre de 2025);
  - San Juan (2023) en tipos;
  - Lajer Baron et al. (2024) en el diferencial entre hogares y viviendas (365.000) y en los no residentes (unas 120.000);
  - el Informe Anual 2025 en los no residentes (7,4 % de las compras) y en la elasticidad de oferta (0,45, cota superior).
  Las fichas son las de docs/v18/bib/modelos_conjunto/ y docs/v18/bib/no_residentes/.

**Respuesta por periodo y territorio.** Para cada periodo y territorio, qué factores explican la mayor parte, con su clasificación y su intervalo, y qué queda sin explicar. La «confianza» usa la escala del Banco de España (V17) y no supera la clasificación del factor de menor nivel que la sostiene.

Identificadores: **V18-C5-<periodo>-<territorio>-<factor>** y **V18-C5-<periodo>-<territorio>-NOEXPL**.

---

## 5. Paradas G y contradicciones con lo publicado

**Paradas (sección G del plan; se documentan en docs/v18/bloqueos.md y se espera al autor donde se indica):**
- **G1.** Una cifra publicada que cambiaría de valor o de capa. Parada y espera. Nada de lo publicado cambia: check_v8, check_v9, check_v13, check_v16 y check_v17 lo comprueban.
- **G2.** Un acceso a muestras selladas fuera de src/holdout.py. Parada inmediata, registro del acceso y espera.
- **G3.** Una estimación IDENTIFICADO que contradiga una conclusión publicada. Se documenta y se espera la decisión del autor.
- **G4.** Una reproducción que no coincide sin explicación. Se documenta y se sigue con los demás. En la fase 4 se aplica también a una réplica ciega (B6) que discrepa: la estimación no se clasifica hasta resolverlo.
- **G5.** Más de 6 millones de tokens de subagentes en una fase.

**Qué es contradecir una conclusión publicada.** Un signo opuesto, o un IC95 que excluye la cifra publicada, en una conclusión de la versión 1.0 o de V8-V17 vigente. Ejemplos:
- «no se detecta caída del número de contratos» (V9, C4), frente a una caída IDENTIFICADO en E2-R1c;
- «turísticos: no concluyente» (v3, v6, V8, V9) solo se contradice con un signo negativo IDENTIFICADO; un efecto positivo IDENTIFICADO la matiza;
- «ningún modelo supera al AR(4)» (K1), si F1-R1 lo superase fuera de muestra.

**Procedimiento si una estimación IDENTIFICADO contradice algo publicado:**
1. No se escribe en cifras_clave ni en ningún entregable.
2. Se documenta en docs/v18/bloqueos.md: la conclusión publicada y su identificador, la estimación de V18, las pruebas, la réplica ciega y la explicación candidata.
3. abogado-del-diablo la ataca (dos rondas).
4. Se espera la decisión del autor. Si el autor la acepta, el cambio va a ERRATA.md si altera una cifra publicada (CLAUDE.md, V6.1 y V13), y nunca cambia la capa de lo publicado: la estimación V18 sigue en C4.

Mientras se espera, el trabajo sigue con los demás estudios.

---

## 6. Tabla final

Abreviaturas:
- **Pruebas:** ET = estudio de eventos y pretendencias; HD = Honest DiD con M̄ hasta 1; PF = placebo de fecha; PR = placebo de resultado; PE = permutaciones; FE1 = F efectivo y primera etapa; ROT = Rotemberg y exclusión de orígenes o sectores; PI = pretendencias del instrumento; BAL = balance de choques; JRS = control por el instrumento retardado; SO = sobreidentificación; RU = raíces unitarias; EST = estabilidad; ID = sensibilidad a la identificación; B4 = robustez a Barcelona, islas, atípicos y medidas.
- **Inferencia:** CL = cluster; W = Webb; BHJ; AKM; CO = Conley; DK = Driscoll-Kraay; NW = Newey-West; AR; MOP; RI = aleatorización.
- **Variantes:** número de variantes del multiverso declarado de cada identificador (BY al 10 %).

| Estudio | Especificación principal (id) | Ampliaciones (ids) | Pruebas | Inferencia | Clasificación posible | Datos que faltan |
|---|---|---|---|---|---|---|
| E1 García-López et al. (2020) | V18-E1-R1 (8 variantes), V18-E1-R2 (4), V18-E1-R3 (4), V18-E1-R4 (2) | V18-E1-A1 (8), V18-E1-A2 (4), V18-E1-A3 (robustez); A4, A5 y X1 NO ESTIMABLES | ET, HD, PF, PR, FE1, PI, SO, B4 | CL barrio (W si < 40), CO 1-2 km, DK, AR, MOP | R2 y A1: hasta IDENTIFICADO; R1, R3, R4 y A2: hasta SUGESTIVO; A3: ASOCIACIÓN | OSM y Google Trends; fianzas por barrio de Open Data BCN (abierto); precio por barrio; PEUAT y moratorias (punto 13); InsideAirbnb histórico (punto 14) |
| E2 Jofre-Monseny et al. (2023) | V18-E2-R1 (8), V18-E2-R1c (4) | V18-E2-A1 (8), V18-E2-A2 (4), V18-E2-A3 (4), V18-E2-A4 (2); A5 NO ESTIMABLE | ET, HD, PF, PR, PE, B4 | CL municipio, RI, DK; Conley-Taber en A2 | R1: hasta IDENTIFICADO; R1c: nulo acotado posible; A2: NO ESTIMABLE si hay menos de 3 trimestres posteriores | Fianzas por tipo de contrato y Registro Único (punto 4) |
| E2 Monràs y García-Montalvo (2023) | V18-E2-R2 (5), V18-E2-R2s (2); R2-X1 NO ESTIMABLE | — | ET, HD, PF, B4 | CL municipio, RI | Hasta SUGESTIVO | Renta anterior, superficie y precio de referencia por contrato (punto 4) |
| E3 González y Ortega (2013 y 2009) | V18-E3-R1 (8), V18-E3-R1q (2), V18-E3-R2 (8), V18-E3-R2b (2), V18-E3-R2q (2) | V18-E3-A1 (6), V18-E3-A2 (6), V18-E3-A3 (8), V18-E3-A4 (4), V18-E3-A5 (2) | FE1, PI, BAL, ROT, JRS, SO (A4), PR, B4 | BHJ, AKM y AKM0, CL provincia + W, DK, AR, MOP | Hasta IDENTIFICADO (R1, R2, A1-A3); A4: hasta SUGESTIVO; ASOCIACIÓN si el F < 5 | Censo de 2001 por nacionalidad (abierto); población en edad de trabajar por provincia (abierto) |
| E4 Fack; Gibbons y Manning; Grislain-Letrémy y Trevien | V18-E4-X1 NO ESTIMABLE | V18-E4-X2 (no se repite: Q7a); V18-E4-L1 (solo literatura) | — | — | NO ESTIMABLE | Microdatos de beneficiarios (punto 3) |
| E5 Saiz (2010); Baum-Snow y Han; Taltavull | V18-E5-R1 (8); V18-E5-R2 NO ESTIMABLE | V18-E5-A1 (4), V18-E5-A2 (4), V18-E5-A3 (8) | FE1, ROT, PI, PR, B4 | CL provincia + W, DK, BHJ, AKM, AR, MOP; CO 25 km en A3 | R1: hasta IDENTIFICADO; A3: hasta SUGESTIVO; A1: ASOCIACIÓN | Afiliación provincial por CNAE desde 2001 y Atlas de Áreas Urbanas (abiertos); SIU, MDT05, CORINE y DPMT (punto 5) |
| E6 Asquith et al. (2023); Mense (2025) | V18-E6-R1 (8), V18-E6-R2 (4) | V18-E6-A1 (4), V18-E6-A3 (4); A2 NO ESTIMABLE | ET, HD, PF, PR, FE1, B4 | CL sección, CO 1 km, W; CL provincia + W, DK, AR, MOP | Hasta IDENTIFICADO (R1, R2); SUGESTIVO si la dilución del stock explica la razón | Lluvia de AEMET (abierta con clave); descarga masiva del Catastro (punto 1) |
| E7 San Juan (2023); BCE (2022); Jarociński-Karadi | V18-E7-R1 (32), V18-E7-R2 (8), V18-E7-R3 (4) | V18-E7-A1 (2), V18-E7-A2 (8); A3 pendiente de licencia | RU, EST, FE1, ID, PR, PF, B4 | NW y LP aumentada con EHW, AR, MOP; bandas robustas a la debilidad; bayesianas; DK y W en A2 | R1 y R2: hasta IDENTIFICADO (ASOCIACIÓN con F < 5 y AR no informativo); R3: ASOCIACIÓN; A2: hasta SUGESTIVO | Peso provincial de la hipoteca variable (puntos 6 y 8); compras al contado (punto 7); licencia de EA-MPD (punto 14) |
| E8 Dolls et al.; Fritzsche y Vandrei; Best y Kleven; Besley et al. | V18-E8-R1 (6), V18-E8-R2 (6) | V18-E8-A1 (2), V18-E8-A2 (2); X1 y X2 NO ESTIMABLES | ET, HD, PF, PR, B4 | CL CCAA (8) + W, RI, DK | Hasta IDENTIFICADO con fechas exactas; con fechas aproximadas, hasta SUGESTIVO | Fechas de las leyes y recaudación del ITP (abiertas); compraventas por tramo (punto 7) |
| E9 Badarinza y Ramadorai; Sá (2016) | V18-E9-R1 (8), V18-E9-R2 (8) | V18-E9-A1 (4), V18-E9-A2 (4); X1 y X2 NO ESTIMABLES | FE1, PI, ROT, BAL, B4 | BHJ (o CL provincia + W si hay menos de 20 choques), AKM0, DK, AR, MOP | R2: hasta IDENTIFICADO; R1: hasta SUGESTIVO | Tipos de cambio (abierto); Notariado por provincia y nacionalidad (punto 7); OPI (punto 14) |
| E10 McCarthy (2026); Francke et al. (2023) | V18-E10-X1 NO ESTIMABLE | V18-E10-A1 (4) | B4 | CO 10 km, CL provincia + W | ASOCIACIÓN como máximo | Titularidad 2012-2026 (punto 9); AEAT-IEF (punto 10); Notariado (punto 7) |
| E11 Segú (2020) | V18-E11-X1, V18-E11-X2 NO ESTIMABLES | — | — | — | NO ESTIMABLE | Recargo del IBI por municipio (punto 12); vacancia anual (INE) |
| E12 Chapelle (2015) | V18-E12-X1 NO ESTIMABLE | V18-E12-A1 (4), V18-E12-A2 (2) | FE1, PI, B4 | CL provincia + W, DK, AR, MOP | A1 y A2: hasta SUGESTIVO (vivienda protegida, no pública) | Promociones públicas por municipio y año (punto 11) |
| F1 DT 1941; DT 0307; IEF | V18-F1-R1 (6), V18-F1-R2 (6), V18-F1-R2-alt, V18-F1-R2-pmg | V18-F1-A1 (6), V18-F1-A2 (4), V18-F1-A3 | RU, cointegración, EST, CD, fuera de muestra frente a AR(4) y ECM v1 | NW, DK, PMG + bootstrap | ASOCIACIÓN | Renta de los hogares por provincia y hogares EPA provinciales (abiertos) |
| F2 Alquiler equivalente | V18-F2-R1 (6) | V18-F2-A1 (6), V18-F2-A2 (4) | Las de F1 | DK, PMG | ASOCIACIÓN | Las de F1 |
| F3 Taltavull (2006) | V18-F3-R1 (4) | V18-F3-A1 (4), V18-F3-A2 (6), V18-F3-A3 (4) | Las de F1 y, en A3, las de E5-R1 | DK, CL + W, AR y MOP en A3 | ASOCIACIÓN; A3: como E5-R1 | Restricciones (punto 5); visados provinciales (abierto) |
| F4 Coherencia | F4-1 a F4-5 | — | Razón en [1/3; 3] o IC95 solapados | — | No aplica | — |

**Familias de Holm por factor** (contrastes principales; las variantes van a BY):

| Factor | Contrastes | Número |
|---|---|---|
| E1 | R1, R2, R3, R4, A1, A2 | 6 |
| E2 | R1, R1c, R2, A1, A2, A3, A4 | 7 |
| E3 | R1, R1q, R2, R2b, R2q, A1, A2, A3, A4 (dos contrastes) y A5 | 11 |
| E5 | R1, A1, A2, A3 | 4 |
| E6 | R1, R2, A1, A3 | 4 |
| E7 | R1 (precio, IPV, compraventas y alquiler), R2, R3, A1 y A2 | 8 |
| E8 | R1, R2, A1, A2 | 4 |
| E9 | R1, R2, A1, A2 | 4 |
| E10 | A1 | 1 |
| E12 | A1, A2 | 2 |
| F | Sin contraste de efecto en la familia: son ASOCIACIÓN; sus contrastes de cointegración se ajustan por Holm dentro de F | — |

**Recuento del multiverso declarado.** Unas 320 variantes en total; con la holgura, el máximo de V18 es de 1.500 (0.6).

---

*Fin del plan. Una vez revisado, con la adenda de la revisión que prevalece, se fija con la etiqueta local `plan-replicacion-v18` antes de la primera estimación.*
