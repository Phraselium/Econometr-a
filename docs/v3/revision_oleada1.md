# Revisión independiente, oleada 1 (v3)

Fecha: 2026-10-10 · Rama r3/main (HEAD) · Revisor independiente; no hice el trabajo revisado.
Alcance (según el encargo): identificación, asignación de capas C1-C4, neutralidad de la redacción y si las conclusiones se siguen de los números. No reproduje el pipeline (lo hace el orquestador con `make check` y `make all`). Leí docs/v3/{plan, especificacion_PA_PB, decisiones, literatura_v3, estado}.md, output/v3/{PA,PB,POT,GL}/* y, en src/v3/{pa_a1, pb_run, pot_run, gl_data, gl_run}.py, solo las definiciones concretas que cito.

## Veredicto: **REHACER**

Nada de lo revisado obliga a rehacer la oleada entera. Pero hay cuatro problemas de identificación que no son de redacción:
1. Varias «cotas» C2 no son el extremo de su propio rango de supuestos, y en otras la dirección del sesgo está invertida.
2. Hay dos hechos C1 cuyo signo no está establecido.
3. La conversión de unidades del objetivo de García-López está mal hecha.
4. P-C3 no excluye las unidades selladas, y sus coeficientes ya se han calculado y publicado.

La puerta go/no-go de P-C no debe darse por cerrada hasta corregir O1, O2, O8 y O9.

---

## Cambios obligatorios (por prioridad)

### O1. Sellado y contaminación de P-C (afecta a la puerta)
- **P-C3 no excluye las unidades selladas.**
  - `pot_run.pc3()` / `incasol()` leen todas las fianzas municipales de Incasòl y no llaman a `holdout.es_sellado_v3`. El sellado v3 cubre los municipios de un distrito: cada uno es un bloque y el sorteo se estratifica por provincia, así que incluye municipios catalanes.
  - Los coeficientes ya están calculados y publicados en `output/v3/POT/potencia.md`: topes −0,0218 y +0,0019; zonas −0,0468 y −0,2027.
  - Consecuencia: la validación sellada de P-C3 ya no está limpia. Hay que hacer cuatro cosas:
    - (a) anotarlo en decisiones.md y en el registro de accesos;
    - (b) definir un holdout de P-C3 todavía no visto (p. ej., el año completo 2026 de fianzas cuando exista) o declarar que P-C3 no puede cumplir el requisito de «validación sellada» de C3;
    - (c) recalcular la potencia excluyendo las unidades selladas;
    - (d) en adelante, que la potencia publique el EE y no el coeficiente.
- **Coeficientes de P-C1 ya vistos fuera del sellado.**
  - POT y GL estiman la especificación de P-C1 (efectos fijos de sección y año) en la muestra no sellada y publican los coeficientes: nacional +0,0011, Barcelona −0,0042 y el resto de ciudades.
  - Eso no rompe el sellado, pero el pre-registro `prereg-v3` debe decir que esas estimaciones eran conocidas y que **solo la evaluación sellada es confirmatoria**.
- **La exploración previa con `describe()` global** declarada por el subagente de GL:
  - Si se limitó a estadísticos marginales (medias, dispersión, recuentos), no revela la asociación entre tratamiento y resultado. La contaminación es baja y no invalida la réplica ni P-C1.
  - Aun así debe constar en decisiones.md y en el registro de `holdout`: qué tabla, qué columnas y si incluía 2026M05.
  - No encontré rastro de ella en los ficheros: solo está la declaración del subagente.

### O2. C1 con dirección no establecida: A6 y A1 (2012-2021, 2012-2025)
- **A6, ratio precio/alquiler.**
  - Hoy es C1 con magnitud 17,3 %, el punto medio de +43,9 % y −9,3 %. Ese punto medio de dos medidas de signo contrario no tiene interpretación y hay que eliminarlo.
  - Una dirección que no está establecida no puede ser un hecho C1. Lo que sí es C1 es la discrepancia misma.
  - Redacción propuesta:
    > «Entre 2015 y 2024, la dirección de la variación de la razón precio/alquiler no está establecida con las fuentes disponibles: +43,9 % con índices (IPV / IPC de alquiler) y −9,3 % con niveles (valor tasado / SERPAVI ×12; de 20,3 a 18,4 años de alquiler). La diferencia procede sobre todo de la medida de alquiler: el IPC de alquiler sube un 10,9 % y SERPAVI un 43 %. Ambas son medidas de stock de contratos.»
  - Campos: `magnitud: null`; `intervalo` [−9,3; +43,9]. Se puede mantener como C1 de la discrepancia, o pasar a C4 («dirección no establecida»).
  - Se sugiere añadir las dos combinaciones cruzadas, valor tasado/IPC y IPV/SERPAVI, para localizar el origen de la discrepancia. Con la tabla A6_ratio_nacional salen ≈ +17 % y ≈ +12 %.
- **A1 2012-2021**: intervalo −1,02 M a +0,69 M. **A1 2012-2025**: −0,44 M a +1,13 M.
  - Ambos son C1 con mediana, pero su signo no está determinado. El enunciado debe decirlo así: «el signo no está determinado por las fuentes (rango −1,02 M a +0,69 M)». No vale presentar solo la mediana.
  - En docs/v3/estado.md, «2012-21: −132 mil (excedente)» es asimétrico: da nombre a una mediana cuyo intervalo cruza el cero, mientras que 2021-2025 se presenta con su intervalo. Hay que sustituirlo por el rango y por «signo no determinado».

### O3. A1: elección de periodos y fuentes
- **Periodos.** La especificación fijó 2002-07, 2008-13, 2014-19, 2020-25 y 2014-25.
  - Las cinco ventanas especificadas salen como C4. El motivo: la ECP cargada empieza en 2021, no en 2013 como suponía la especificación.
  - Las ventanas C1 (2012-21, 2022-25, 2012-25, 2021-25) se añadieron después, sin anotarlo en decisiones.md.
  - Su elección responde a la disponibilidad de fuentes (Censos y ECP) y no al resultado, lo cual es neutro. Pero hay que:
    - (a) anotar la desviación y su motivo en decisiones.md;
    - (b) declarar que 2021-2025 se añade para comparar con el BdE;
    - (c) presentar todas las ventanas en una sola tabla, empezando por las preespecificadas, cada una con su capa;
    - (d) no dar una sola ventana como titular.
  - El cambio de signo entre periodos (negativo en 2002-07 y 2008-13; positivo desde 2014) es en sí un hecho que debe figurar.
- **Dependencia entre fuentes.** Los factores de elevación de la EPA se calibran con las cifras de población del INE, y la ECP está anclada al Censo 2021. La independencia entre «EPA» y «Censo+ECP» es parcial y debe decirse en `limites`.
- **Cifra de comparación del BdE** (≈ 750.000, Informe Anual 2025). En literatura_v3 su DOI figura como «no comprobado en Crossref». La comparación debe llevar ese estado («NO VERIFICADA» o «DOI no comprobado»).

### O4. Cotas de precio de B1 y B2: el supuesto extremo no es el extremo
- `EPS_MIN = 0,33`, pero `EPS_GRID` incluye 0,25. Por eso, en todas las filas de precio, `sensibilidad_max` es mayor que `cota_superior`. Ejemplos:
  - B1 nacional: 8,32 frente a 10,98;
  - B2 compra 2014-2025: 13,1 frente a 17,4;
  - B2 alquiler: 113,7 frente a 150,1.

  Una cota tiene que ser el máximo bajo el supuesto extremo declarado.
- **|ε_d| no procede de ninguna estimación.** La parte B de la literatura declara la laguna. Además, los valores «implícitos» de González-Ortega (2013) y de Saiz (2007) son formas reducidas de equilibrio (población → precio, que incluyen la respuesta de la construcción), no elasticidades de demanda.
- Por tanto, las traducciones a precio no cumplen «supuestos débiles». Hay dos opciones:
  - (a) publicarlas como una función explícita, cota(ε) = desplazamiento / |ε|, y marcarlas como «condicionales a un parámetro no verificado» (C4);
  - (b) usar directamente la forma reducida publicada (p. ej., González-Ortega para inmigración en España) como escenario, citado con su estado de verificación.
- **Las cotas de cantidad sí son C2**: B1, desplazamiento ≤ 2,75 % del stock de alquiler (81.771 viviendas); B2, cuota de ΣΔhogares.
- Corregir también docs/v3/estado.md («precio ≤ 8,3 %»).

### O5. B1 con ΔVUT negativo: dirección de la cota invertida
- Afecta a Barcelona ciudad, Barcelona provincia, Illes Balears, Ceuta y nacional 2024M08-2026M05.
- Cuando las viviendas turísticas caen, la sustitución s ∈ [0,1] da un efecto en [−|ΔVUT|/stock/|ε|, 0]. La **cota superior es 0**; el valor negativo (p. ej., −10,8 % en Barcelona) es la **cota inferior**.
- Hay que corregir `cota_superior`, añadir `cota_inferior` y reordenar `sensibilidad_min/max`, que hoy van invertidos.
- La «frase» generada dice «como máximo −6,3 % … puede atribuirse a el aumento de viviendas turísticas». No tiene sentido con ΔVUT < 0 y además contiene «a el». «Liberación de oferta» es interpretativo: presupone que las viviendas vuelven al alquiler. Debe decir «ΔVUT negativo».

### O6. B2 inmigración: no es una cota superior bajo lo declarado
- **Nacionalidad en vez de nacimiento.** Se usa `pob_extranjera_todas` (nacionalidad, padrón). Las nacionalizaciones restan de ese stock, así que ΔPoblación extranjera infravalora la entrada neta. El sesgo va **hacia abajo**: lo publicado no es una cota superior. Hay que usar la población nacida en el extranjero (padrón o ECP por país de nacimiento), que es lo que dice la especificación («o nacida fuera»), o declarar el sesgo.
- **El tamaño 2,0 no es el extremo lógico.** Es el extremo de un rango supuesto (2,0-3,0). El extremo lógico es 1 persona por hogar, que da una cuota ≥ 100 % en 2014-2025 y 2020-2025, es decir, una cota no informativa.
- **Asimetría con B1.** B1 usa el extremo lógico de cantidad (sustitución 1:1); B2 no. Los dos factores deben tratarse con el mismo criterio. Hay que publicar la cota con 1,0 y presentar 2,0-3,0 como sensibilidad.
- **Máximo entre fuentes.** En 2021-2025 la fila ECP da 76,9 % frente al 71,0 % publicado (EPA). La cota debe ser el máximo entre fuentes de hogares, o mostrar las dos.
- **Etiqueta errónea.** «% de Σ Δhogares (máx. fracción del déficit atribuible)» mezcla dos magnitudes distintas. La cuota de ΣΔhogares no es la fracción del déficit. La que se refiere al déficit es la fila `viviendas` = min(ΔH_ext, D).
- **«No explica» en 2008-2013 y 2009-2014** (100 %): en esos periodos los precios cayeron y el déficit A1 fue negativo, así que no hay subida ni déficit que explicar. Debe figurar como «no definido», que es lo que la propia nota del código hace con las filas de precio.

### O7. B4 tipos
- **La cota depende del suelo de uc.** Con suelo 1 % sale 78,0 %; con suelo 0,5 % sale 109,6 % (`sens_max`). Cuando uc tiende a 0 no hay cota finita. Hay que declararlo: «sin cota finita; con suelo de uc = s, la cota es …». La conclusión, ya correcta, es que en 2014-2021 la cota no es informativa (no_explica = 0).
- **Etiqueta del extremo invertida.** En 2021-2025 el extremo dep = 3, ganancia = 0, IBI = 1 es el uc *más alto*, no «el más bajo permitido».
- **«No explica el 100 %» de 2021-2025 es condicional.** Depende del tipo nominal y de una ganancia esperada constante entre años. La variante con tipo real sale «casi toda indefinida», y en 2022-2023 el tipo real cayó. La frase debe condicionarse a esos supuestos.
- **Simetría.** El periodo 2007-2014 también tiene «signo contrario»: los tipos bajan y los precios caen un 34 %. Se calcula pero se excluye de cotas.json. Hay que publicarlo junto a 2021-2025: muestra los límites del modelo de estado estacionario en las dos direcciones.
- **«Alquiler: 0, no explica el 100 %».** Es un supuesto, no una cota: los tipos pueden afectar al alquiler a través de la elección de tenencia. Debe figurar como «no acotado por este modelo», no como cota 0.
- Desviación respecto a la especificación (2022-2025 → 2021-2025): anotarla en decisiones.md.

### O8. Réplica de García-López: conversión de unidades
- La unidad de GL es el AEB: 233 áreas con una media de 7.122 habitantes (literatura_v3, A1). La conversión usa 73 barrios (11.079 viviendas por unidad).
- Con 808.751 / 233 ≈ 3.471 viviendas por AEB, el objetivo es **T ≈ 0,035 × 0,347 ≈ 0,012 log-puntos por pp**, no 0,039. El rango con 5.000-20.000 viviendas tampoco corresponde a un AEB.
- Las clasificaciones no cambian con T = 0,012:
  - Barcelona: IC [−0,0078; −0,0005], signo contrario;
  - València: IC [0,0001; 0,0099], no contiene T → sigue PARCIAL por el criterio;
  - Madrid, Málaga y España: excluyen T.

  Pero hay que corregir T en `output/v3/GL/*`, `resultado.json` y estado.md, y publicar la clasificación sobre un rango de T acorde con el tamaño de los AEB. Con unidades pequeñas, València podría contener T.
- **Otro factor de escala que falta**: las VUT del INE (todas las plataformas, sin duplicados) no son los «anuncios activos con reseña» de GL. Si las VUT son más numerosas, el T por VUT es menor. Hay que declararlo como fuente de incertidumbre de T.
- **«PARCIAL» para València** (mismo signo, magnitud 2-8 veces menor, IC que excluye T) se lee como una réplica a medias. Se sugiere la etiqueta «mismo signo, magnitud distinta».
- **Placebo de permutación**: no se debe publicar `p_perm = 0,0` con 500 réplicas; corresponde p < 1/501. La permutación debe hacerse por clúster (distrito): la dispersión del placebo, 0,0009, es menor que el EE de clúster, 0,0015, lo que indica una permutación por sección, anticonservadora. Hoy el p del placebo contradice el p de Holm (0,27).
- **Capa C4: bien declarada** (replicacion.md, resultado.json). No hay lenguaje causal.

### O9. Potencia y go/no-go
- **Diseños por ciudad con 8 clústeres** (Barcelona, Sevilla, Málaga) y 15-16 (València, Madrid).
  - El EMD analítico usa z (2,80) y no t(G−1); con G = 8, t₇ da 3,26.
  - La potencia simulada en el propio EMD queda en 0,53-0,74, por debajo de 0,80. Por tanto, el EMD real es mayor que el publicado.
  - Esas filas no deben figurar como «estimable». Hay que recalcularlas con t(G−1) y con un EMD calibrado por bootstrap (o wild cluster bootstrap). El GO de P-C1 debe limitarse al conjunto de las 6 ciudades (G = 56) y al nacional.
- **P-C3.**
  - El GO es condicional. Ya se exige recalcular con la lista oficial (61 municipios).
  - Además, la nueva entrada de decisiones.md fija el fin de vigencia en 2021-09-21, mientras que `pc3` codifica la exposición de 2022 como 0,2. Hay que alinearlo.
  - Hay que usar los códigos corregidos de Rubí (08184) y Mont-roig del Camp (43092), y excluir las unidades selladas (O1).
- **Resto de veredictos**: la regla EMD ≤ EER es razonable y está fijada ex ante.
  - P-C1 nacional, GO: correcto.
  - Shift-share nacional, NO-GO: correcto (F = 0,25 y 5,3).
  - Shift-share en 6 ciudades, GO: correcto (F = 24-29).
  - P-C2, NO-GO: correcto.
  - P-C4, NO-GO: correcto.
- Con T bien convertido (≈ 0,012 por pp), el EER de P-C1 (0,01 por pp) sigue siendo coherente con García-López.

### O10. Capas de P-A que hay que ajustar
- **A2.** Las tasas de convivencia con los padres (ECV/Eurostat y EPA) son C1. Los «hogares implícitos» dependen de una tasa de referencia contrafactual: España 2008, o la UE-27, que sale solo de la ECV. No son una medida descriptiva. Deben ser C2, con el supuesto explícito, o separar en el intervalo la parte debida a la medida de la debida a la referencia. Sin desagregación por CCAA (la especificación la pedía): declararlo.
- **A4 nacional.** El precio tiene una sola fuente (valor tasado) y el tipo una sola serie. Hay que añadir Registradores en el ámbito nacional, como se hace en provincias, o declarar el numerador como de fuente única.
- **A5 (65+).** Eurostat ilc_lvho02 procede de la ECV (EU-SILC): no es una fuente independiente de la ECV. Cuenta como dos fuentes (EFF y ECV), no tres.
- **A3.** Las dos medidas de vacancia comparten las viviendas principales del Censo 2021, así que la independencia es parcial y debe decirse. El rango publicado mezcla tres medidas de presión (definición, no medición) y muestras de distinto tamaño (277 frente a 1.806 municipios). Hay que separar el rango de medida del rango de definición.

---

## Cambios sugeridos
1. Usar un nombre neutro para la magnitud A1, que puede ser negativa: «balance contable hogares − altas netas»; «déficit» solo cuando sea positivo.
2. B1, «no explica 25 %» (nacional): el umbral de 0,1 pp admite hasta ≈ 0,3 pp de alquiler con |ε| = 0,33 en esos municipios, así que conviene matizar «no explica». En las filas nacionales de precio, el campo `no_explica` contiene el dato geográfico (25 %). El dato agregado (cota 8,3 % frente al +6,1 % del IPC de alquiler: no informativa) debería ir en un campo distinto.
3. B1 y B2 comparan con el IPC de alquiler; SERPAVI da +17,3 % (ponderado, 2020-2024). Hay que mostrar ambos denominadores, porque el «no explica» depende de cuál se use.
4. B1 nacional: el periodo titular, 2020M08-2024M08, maximiza la cota; parte de un mínimo de la pandemia. Es aceptable para una cota superior si se dice así, con las otras ventanas junto a ella (1,98 % hasta 2026M05).
5. En la réplica de GL, las filas «por 100 VUT (homogéneo)» se etiquetan a la vez como «homogéneo» y «unidad no homogénea». Unificar.
6. En `resultado.json` de PB, el texto «|ε_d| (0,33-1,0) es implícito de González y Ortega (2013) y Saiz (2007)» debe decir que no son elasticidades de demanda (ver O4).
7. Añadir a `check_texto.py` términos como «excedente» y «liberación», y comprobar que ninguna `frase` de cotas.json describe como «aumento» un ΔVUT negativo.

## Neutralidad (resumen)
- No encontré léxico partidista ni alusiones a partidos o personas en output/v3.
- Asimetrías detectadas:
  - A1: «excedente» frente a una cifra con intervalo (O2);
  - B1 y B2 con extremos de distinta exigencia (O6);
  - B4 publica el «signo contrario» de 2021-2025 y omite el de 2007-2014 (O7);
  - frases de B1 con ΔVUT negativo (O5).
- Corregidas esas asimetrías, la redacción «como máximo X puede atribuirse a Y bajo el supuesto Z» es adecuada para C2.

## Lo que está bien
- Las capas C4 de fuente única en A1 y en las provincias.
- Las advertencias en `limites`: el déficit contable no equivale a demanda insatisfecha, y SERPAVI es un stock.
- El sellado aplicado en GL y en P-C1, con los distritos 09 y 10 de Barcelona y 2026M05 excluidos.
- La regla go/no-go fijada ex ante.
- B3 en espera, sin una cifra inventada.
- El intervalo de la réplica de GL calculado con t(G−1).
