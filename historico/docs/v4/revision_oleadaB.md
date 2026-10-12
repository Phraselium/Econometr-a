# Revisión independiente · v4 · puerta de la oleada B (M3, M4) y verificación de la oleada A

Revisor independiente, en modo de solo lectura. No se ha reproducido el pipeline, por instrucción de la puerta. Se han revisado capas, interpretación, neutralidad y coherencia sobre el HEAD fac62ca de r4/main.

## Veredicto: **REHACER**

M3 y M4 son en general prudentes: no usan lenguaje causal, no ofrecen cifras de efecto y el coste supuesto está declarado. Aun así hay cuatro problemas que obligan a rehacer:
- dos capas C1 sin dos fuentes concordantes e independientes (M4: compradores extranjeros y viviendas turísticas);
- una regla de veredicto asimétrica entre M3-V1 y M4-V3, y además M3-V1 tiene un error de denominador;
- una ficha duplicada (V14 frente a M4-V1) con cifras de MIVAU contradictorias;
- tres correcciones de la oleada A sin cerrar (A3, A6 y A10).

## Cambios obligatorios, por prioridad

### B1. Verificador: V14 y M4-V1 son la misma afirmación y dan cifras distintas de la misma fuente
- Las dos fichas evalúan «Los compradores extranjeros encarecen la vivienda en España». V14 da «MIVAU 9,6-11,0 %» y M4-V1 da «MIVAU 16,9 %». La primera cifra corresponde solo a los residentes extranjeros. La segunda suma residentes y no residentes.
- Hay que retirar V14 de la tabla, o marcarla como «sustituida por M4-V1», y usar una sola definición en todas las cifras que se publiquen. Si se usa «residentes», debe decirse.

### B2. M4: el peso de los compradores extranjeros no cumple C1
- **Independencia.** La estadística de transacciones del MIVAU se elabora, según su metodología, con datos del Consejo General del Notariado. Hay que comprobarlo y declararlo. La serie lo sugiere: en 2007 da 7,12 % frente a 7,3 %, y en 2008 6,37 % frente a 6,8 %. MIVAU y Notariado no son dos fuentes independientes. La única independiente es Registradores, que mide la inscripción y no la escritura.
- **Concordancia.** Con la regla de ±15 % de M0, Registradores (13,8 % en 2025) se separa de Notariado (18,8 %) un 27-36 % en términos relativos, y del MIVAU (16,9 %) un 18-22 %. No cumple C1 en nivel.
  - Opción 1: el nivel pasa a C4 y se reportan las dos cifras (regla de CLAUDE.md: si dos métodos discrepan, se reportan ambos).
  - Opción 2: queda C1 un enunciado más débil, declarado con su umbral antes de mirar, por ejemplo «entre 1/8 y 1/5 de las compraventas, con la misma tendencia» (la correlación provincial entre MIVAU y Registradores es de 0,99).
- **Definiciones.** Falta explicar la diferencia, que hoy solo se atribuye a la «cobertura». Hay que tratar:
  - nacionalidad frente a residencia, y cómo trata cada fuente al comprador con NIE;
  - vivienda libre (Notariado) frente a total (MIVAU);
  - fecha de escritura frente a fecha de inscripción, con su desfase;
  - compraventa frente a otras transmisiones.
- El veredicto de M4-V1 («ANALIZADA, NO CONCLUYENTE») no cambia. Cambian la capa y el texto de «capa» en `hechos.json`, `resultado.json` y `estado.md`.

### B3. M4: las viviendas turísticas y la tenencia no son C1
- «C1 turísticas (INE y registro GVA)» no se sostiene por dos razones. Las dos fuentes **discrepan** en un factor de 1,5-2,2: Alicante 69.286 frente a 32.148, Castellón 14.136 frente a 6.990 y Valencia 17.749 frente a 12.130. Además, la GVA solo cubre 3 provincias. La cifra nacional de 341.001 es de fuente única: C4, con las dos cifras valencianas reportadas.
- La tenencia (Censo 2021, tabla 59523) es de fuente única. Pasa a C4, salvo que se triangule con ECV o EPA.
- `resultado.json` dice «C1 (stock por uso, tenencia, extranjeros)». Debe pasar a C4 en los tres (o en dos, si se acepta la opción 2 de B2).
- La decisión de M4 en `decisiones.md` («turísticas … que discrepan → C1») se contradice a sí misma y hay que corregirla.

### B4. M3-V1 («Hay suelo de sobra»): error de denominador, prueba que no informa y regla asimétrica
- **Error.** En `escribir_json`, las cuatro provincias forales tienen `uu_solar` = NaN, y `NaN*v/déficit >= 1` vale False. Por eso cuentan como «no cubre». El 92 % es 48/52: en realidad los solares cubren el **100 % de las 48 provincias con dato**. Hay que excluir las forales del denominador y decirlo.
- **No informa.** La cobertura es la misma con 5, 10 y 20 viviendas por solar: 3,09 M de solares frente a un déficit de unos 0,7 M. A escala provincial la prueba sale positiva por construcción. Si se quiere evaluar «donde hace falta», hay que calcular la cobertura municipal en los 703 municipios de M3, que ya tienen déficit y solares.
- **Asimetría con M4-V3.** Las dos fichas están en C4 y se apoyan en una fuente única:
  - M3-V1 recibe PARCIALMENTE gracias a un umbral numérico fijado para «de sobra»;
  - M4-V3 recibe NO CONCLUYENTE porque «“muchas” no tiene umbral».

  Hace falta una regla común: **con evidencia C4, el veredicto máximo es «ANALIZADA, NO CONCLUYENTE»**, y PARCIALMENTE exige como mínimo C2. Con esa regla, M3-V1 pasa a ANALIZADA, NO CONCLUYENTE.
- **Rama NO RESPALDADA.** La regla actual impide RESPALDADA pero admite NO RESPALDADA con la misma fuente. Sin embargo, la medida catastral está sesgada en las dos direcciones (ver el punto siguiente). Con C4 no debe caber ninguno de los dos veredictos extremos.
- **Qué mide el uso «solar» del Catastro.** Hay que añadirlo a los límites de la ficha y del hecho. Mide un recuento de unidades urbanas sin edificar, sin superficie, uso urbanístico, edificabilidad, estado de urbanización ni disponibilidad en el mercado.
  - Sobreestima el suelo disponible: incluye solares de uso industrial o terciario, parcelas residuales y suelo sin urbanizar del todo.
  - Lo subestima: deja fuera el suelo urbanizable sin planeamiento de desarrollo aprobado, que catastralmente sigue siendo rústico, y no ve el SIU.

  Por eso no es una medida de «suelo disponible». Es una cota superior y ruidosa del suelo urbano vacante.

### B5. M1: un hecho de fuente única no es C2. Regla propuesta
- **Regla.** La capa de un agregado contable es la **menor de las capas de sus componentes medidos**:
  - un componente es C1 si tiene al menos dos fuentes independientes dentro del ±15 % en el mismo nivel geográfico y la misma ventana;
  - si es de fuente única, es C4;
  - los supuestos con rango declarado, como las bajas del 0-0,2 %, rebajan como mucho a C2;
  - C2 exige que todo lo medido sea C1 y que lo no medido sea un supuesto acotado.
- **Aplicación al nivel nacional 2021-2025.** ΔH es C1 (EPA frente a ECP, M2-H0) y las altas son C1, así que la capa es C2. Es correcto. Hay que cambiar el límite «hogares de una sola fuente» por «ΔH nacional C1 (M2)» y quitar «tramo 2011-2021», que no corresponde a esa ventana.
- **Aplicación al nivel provincial.**
  - 2021-2025: ΔH procede solo de la ECP, porque el Censo anual no es independiente (A5). Las 13 provincias C2 pasan a **C4**, salvo que se triangulen con la EPA provincial dentro del ±15 %.
  - 2012-2025: las 8 provincias C2 pasan a **C4**. El tramo 2011-2021 es de fuente única y además lo contradice el censo (A3, factor 2,3).
- Con esta regla, la capa efectiva de M3, que ya está limitada por M1, no cambia (C4).

### B6. M3: la etiqueta «brecha regulatoria» atribuye una causa
- La clase 2 es «precio > r·(coste + suelo repercutido)», calculada con un coste supuesto. Llamarla «regulatoria» atribuye la brecha a la regulación, que es la lectura de Glaeser y Gyourko como «impuesto regulatorio» y que aquí no se ha identificado. Ese lenguaje está por encima de C4.
- Hay que renombrarla, por ejemplo «2 falta y precio > r·(coste + suelo), coste supuesto», en `ETIQ`, `hechos.json`, `resultado.json`, las tablas y la figura.
- Por el mismo motivo, «rentable» y «no rentable» (clases 1 y 3) deben llevar «con coste supuesto».

### B7. M3: coherencia interna de la clasificación
- **Etiquetas caducadas.** «PROVISIONAL: déficit de M1 en corrección» ya no es cierto: M3 se regeneró con el M1 corregido (commit 32aae05; Madrid 107.368 coincide con M1). Hay que quitar esa etiqueta o fecharla.
- **Regla de C2 inoperante.** `decisiones.md` y el docstring dicen todavía «C2 si la clase modal ≥ 80 %». Con el coste en nivel supuesto, esa regla ya no se aplica. Hay que escribir que la estabilidad se reporta y que la capa es C4 sea cual sea la estabilidad.
- **Clase 9 = 0 oculta un hueco.** La clase 2 no exige solares, de modo que las 4 provincias forales, que no tienen solares, se clasifican como 2 (Álava: 22 % de especificaciones en 9). Hay que reportar aparte las «unidades sin dato de solares».
- **El multiverso mezcla dos preguntas.** Combina los periodos 2012-2025 y 2021-2025. Las 4 provincias con modal «no falta» (Asturias, Segovia, Soria y Zaragoza, con el 33-67 %) salen del periodo 2012-2025, pero M1 no tiene ninguna provincia con déficit negativo en 2021-2025. Hay que calcular la clase y la estabilidad por periodo.
- **Umbrales previos.** Que se fijaran antes de clasificar no se puede comprobar en git. Los umbrales y la clase 5 aparecen por primera vez en el commit 26c8b8a, junto con las salidas, y la entrada de `decisiones.md` está en el commit 358b246, que también incluye salidas. La propia etiqueta «(clase añadida)» indica que la clase 5 se añadió después.
  - Hay que declarar «prerregistro no verificable; clase 5 añadida después del diseño».
  - La clase 5 tiene recuento 0, así que no cambia los resultados.
- **Cálculo.** La rejilla (3·3·3·2·2·3 = 324 especificaciones × 6 variantes = 1.944) y la estabilidad (frecuencia modal entre especificaciones válidas) están bien calculadas.

### B8. Correcciones de la oleada A sin cerrar
- **A3.** `M2-H2` sigue en **C1** con INE EM y Eurostat `migr_imm1ctz`. Eurostat recibe sus datos del INE, y el INE falta en 2020-2025. Debe pasar a C4.
- **A6.** V04 y V05 siguen en **C1** con el rango 559.752-969.059. El techo incluye bajas supuestas (0,2 %), y M1 dice que el suelo de 560 mil «no se reproduce».
  - Una opción es pasar a C2.
  - La otra es separar el componente C1 (bajas = 0: ≈701 mil, 52 provincias) de la cota C2.

  En cualquier caso, la cifra y la capa deben coincidir con las de M1 (`M1-H-nacional-2021-2025`: C2).
- **A10.** `M1-H-latente-provincias` dice todavía «M2 no estaba disponible al calcular». Hay que remitir a M2-C1.
- **V08 (re-emitida).** Está en C1 aunque su base (las vacías) es C4 de fuente única, como reconoce la propia ficha. Por la regla de B5 pasa a C4, y con la regla de B4 el veredicto máximo es «ANALIZADA, NO CONCLUYENTE». Así queda coherente con M4-V3, que usa los mismos 3,83 M.

### B9. M4: notas que faltan
- **Personas jurídicas como vendedoras (24,7 %).** Incluyen a los promotores que venden obra nueva y a las entidades financieras. Hay que decirlo para que no se lea como «desinversión» de tenedores. ETDP procede del Registro de la Propiedad, igual que Registradores: no hay segunda fuente independiente, así que C4 es correcto.
- **Costa e islas.** El supuesto está declarado en el docstring y en `decisiones.md`, pero no en `hechos.json`, la tabla ni la ficha. Hay que añadirlo. Además, la lista incluye provincias metropolitanas (Barcelona, Valencia, Málaga), así que «costa» mezcla mercados turísticos con metropolitanos. Hace falta una sensibilidad sin esas tres o con municipios costeros.
- **Literatura de M4-V1.** «v2 (BV)» debe llevar referencia completa y el estado VERIFICADA o NO VERIFICADA con su cuartil.

### B10. M4-V3: veredicto correcto; el C1 por la vía de v3 A3 no es viable
- «ANALIZADA, NO CONCLUYENTE» en C4 es correcto, y la regla de B4 lo confirma.
- La vía Catastro − hogares (v3 A3) no da un C1 de vacías, por dos motivos:
  1. El Censo 2021 construye su parque de viviendas sobre el Catastro y el padrón, así que no es independiente de «Catastro − hogares».
  2. La diferencia mide las viviendas **no principales** (vacías, esporádicas y secundarias), no las vacías.
- Como mucho cabría un hecho sobre «no principales» con independencia parcial declarada, que seguiría en C4 con la regla de B5.
- Hay que mantener la nota del desfase de fechas (vacías 2021 frente a turísticas 2026).

## Neutralidad
- No se encuentran términos valorativos ni partidistas en `output/v4/M3` ni en `output/v4/M4`. «Encarecen» y «dominan» solo aparecen dentro de las afirmaciones que se evalúan.
- La redacción de la nacionalidad (A11) ya está en `M2-H1`: dice que nacionalidad no es origen, que la tasa de jefatura es común y que no se atribuyen precios. Falta que `estado.md` acompañe el «56-58 %» con esas cautelas y con el rango 2020-2025 (53-76 %).
- **Simetría.**
  - Las afirmaciones que señalan como factor a la demanda (extranjeros, empresas) y las que señalan a la oferta (suelo) reciben veredictos de nivel equivalente.
  - La excepción es M3-V1, cuyo PARCIALMENTE en C4 no tiene equivalente en M4-V3 (B4).
  - M4-V2 se trata igual que V02 (NO ANALIZADA: FALTAN DATOS, con el dato de flujo C4 aparte).
  - En M4-V2 se presenta el dato de flujo que va en la dirección contraria a la afirmación (las personas jurídicas venden más de lo que compran) sin valorarlo. Es correcto, si se añade la nota de B9.

## Correcciones de la oleada A comprobadas

| Corrección | Estado | Comprobación |
|---|---|---|
| A1 | Resuelta | Aserciones en `m1_run.py` (l. 158 y 176). |
| A2 | Resuelta | V01 al 133 % y V03 al 79 %; la convención B no cambia la capa; V11 tratada. |
| A4 | Resuelta | k por grupo; rango con y sin corregir en `M2-H1`. |
| A5 | Resuelta | Ventana de 4,75 años rotulada. |
| A7 | Resuelta | V13 pasa a ANALIZADA; BdE como NO VERIFICADA. |
| A8 | Resuelta | Terminadas C1 en 2019-2024, con independencia parcial. |
| A9 | Resuelta | Según `estado.md`. |
| A11 | Parcial | Ver «Neutralidad». |
| A3 | Sin resolver | B8. |
| A6 | Sin resolver | B8. |
| A10 | Parcial | B8. |

## Aspectos correctos
- M3:
  - el coste en nivel figura como supuesto no verificado y todos los hechos y la ficha están en C4;
  - ninguna afirmación depende del coste con más fuerza que C4;
  - el valor tasado figura como aproximación;
  - la capa efectiva queda limitada por M1.
- M4:
  - no hay estimación causal y los resultados son descriptivos;
  - Airbnb solo se usa en robustez;
  - el comprador persona jurídica de la ETDP es de fuente única y está en C4;
  - M4-V2 está bien como NO ANALIZADA por falta de stock por titular.

## Iteración 2 (HEAD 429f70e)

### Veredicto: **REHACER (acotado)**
Quedan dos puntos de capa. Basta con corregirlos y regenerar, sin otra iteración de revisión. Si no se corrigen, el texto propuesto abajo debe ir a `docs/v4/limitaciones.md`.

### Resueltos

| Cambio | Estado | Comprobación |
|---|---|---|
| B1 | Resuelto | V14 retirada. Definición única: MIVAU residentes + no residentes. Se explica que la cifra 9,6-11,0 % de V14 contaba solo residentes. |
| B2 | Resuelto | Extranjeros en C4. MIVAU y Notariado se declaran no independientes (pendiente de confirmar en la web, como dice la ficha). Las definiciones están explicadas. |
| B3 | Resuelto | Turísticas, tenencia y stock por uso en C4. `resultado.json` es coherente. |
| B4 | Resuelto | Ver detalle abajo. |
| B5 | Resuelto | Todos los hechos de M1 en C4, salvo la latente (C2, supuesto contrafactual). |
| B6 | Resuelto | Etiquetas neutras con «coste supuesto». |
| B7 | Resuelto | Ver detalle abajo. |
| B8 | Parcial | Ver detalle abajo. |
| B9 | Resuelto | Nota de promotores y entidades, supuesto de costa en la ficha, `extranjeros_concentracion_sensibilidad.csv` con las metropolitanas aparte, y referencia «v2 (BV)» como NO VERIFICADA. |
| B10 | Resuelto | M4-V3 en C4, ANALIZADA, NO CONCLUYENTE. |

- **B4.**
  - M3-V1 usa ahora 48 provincias en el denominador y dice que la prueba provincial no informa.
  - Se añadió la cobertura municipal (454 municipios con dato; da también el 100 %).
  - Veredicto: ANALIZADA, NO CONCLUYENTE.
  - La regla «C4 ⇒ como máximo no concluyente» está en `src/v3/check_texto.py:79` y en `src/v4/verificador.py:95`.
- **B7.**
  - PROVISIONAL retirado.
  - Capa C4 siempre.
  - Clase 9 con las 4 forales.
  - Periodo principal 2021-2025 y 2012-2025 aparte.
  - Prerregistro no verificable y clase 5 añadida después: ambos declarados.
- **B8.**
  - M2-H2 está en C4.
  - V08 está en C4 y es NO CONCLUYENTE.
  - Lo que sigue pendiente se detalla en el apartado siguiente.

### Pendiente
1. **V04/V05 (A6/B8): siguen rotuladas como C1 con cifras que no son C1.**
   - El intervalo principal sigue siendo [559.752; 969.059] para 2021-2025. Según el propio texto de la ficha, 2021-2025 es C4.
   - La cifra nueva de 2021-2024, 732.750 [562.692; 902.808], incluye bajas supuestas (0,1-0,2 %), y eso la deja en C2 por la regla B5.
   - En `output/v4/M0/deficit_2021_2024.csv`, las 12 filas dicen C1, también las que tienen bajas > 0. La columna `bajas_pct` vale 0 en todas las filas aunque `bajas` sea 107.058 o 214.116: es un error de columna.
   - Corrección:
     - En el CSV: C1 solo con bajas = 0, rango [562.692; 688.692] (EPA y ECP difieren un 8,4 % en ΔH; las terminadas de 2021-2024 están en el núcleo C1 de A8). Las filas con bajas, a C2. Hay que arreglar `bajas_pct`.
     - En V04/V05: intervalo principal de 2021-2024 con bajas = 0 en C1, y la cota con bajas en C2. Hay que retirar de la cabecera el rango de 2021-2025 o rotularlo como C4.
   - El veredicto PARCIALMENTE de V05 se sostiene incluso con el suelo C1 (562.692 ≥ «cientos de miles»).
2. **M7-V1 repite la afirmación de V13** («Hay una burbuja…»). Es el mismo patrón que B1: hay que retirar V13 o marcarla como «sustituida por M7-V1».
3. **Detalles menores, que no bloquean.**
   - `M1-H-latente-provincias` dice todavía «M2 no estaba disponible» (A10).
   - `M1-H-nacional-2021-2025` mantiene el límite «tramo 2011-2021», que no corresponde a esa ventana.
   - `output/v4/M3/_smoke/` conserva la etiqueta «brecha regulatoria»: hay que regenerarlo o borrarlo.
   - M1 nacional 2021-2025 está en C4 y M0 2021-2024 en C1. Es más conservador de lo que exige B5 (ΔH nacional C1 por EPA frente a ECP) y no es una promoción. Conviene que el texto lo explique: ventana distinta y terminadas de 2025 frágiles.

### Texto propuesto para docs/v4/limitaciones.md (solo si no se corrigen 1 y 2)
> **Capas del déficit nacional (V04/V05).** Solo es un hecho C1 el déficit contable 2021-2024 sin bajas: 562.692-688.692 viviendas (hogares ECP o EPA corregida; terminadas MIVAU con o sin protegida). Las cifras con bajas del parque del 0,1-0,2 % anual (hasta 902.808) dependen de un supuesto y son C2. El rango 2021-2025 (559.752-969.059) es C4, por la fragilidad de las terminadas de 2025. Donde una ficha o una tabla rotule estas cifras como C1, prevalece esta nota.
>
> **Fichas duplicadas.** V13 y M7-V1 evalúan la misma afirmación. La ficha vigente es M7-V1.
