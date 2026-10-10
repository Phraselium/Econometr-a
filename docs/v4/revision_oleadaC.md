# Revisión independiente: oleada C de la v4 (M5, M6, M7 y entregables)

- Fecha: 2026-10-10. Rama r4/main, HEAD c6439fe.
- Alcance: capas, neutralidad, interpretación y coherencia de cifras. No se ha reproducido el pipeline, por encargo. `src/v3/check_texto.py` da 0 errores, pero el control léxico no detecta ninguno de los problemas que siguen.

## Veredicto: **REHACER**

Las cifras en general cuadran: de 30 comprobadas, 26 coinciden con su fuente. Hay que rehacer por cuatro motivos:
1. Una cifra C1 es errónea y aparece en tres entregables.
2. La codificación de M5 tiene asimetrías que afectan a la neutralidad.
3. M5 promueve de capa las magnitudes de P-D v3.
4. V11 y M5-V1 aplican reglas distintas a evidencia del mismo tipo.

Ninguno de los cambios exige datos nuevos.

## Cambios obligatorios (por prioridad)

### C1. Viviendas terminadas «91.000-101.000 al año en 2019-2024»: cifra errónea (C1 en tres entregables)
- **Dónde aparece.** working_paper §5.1, informe_tecnico §1.2, lo_que_sabemos y policy_brief (mensaje 2).
- **Qué dice la fuente.** `output/v4/M0/terminadas_triangulacion.csv`:
  - en el territorio común, que es donde se hace la triangulación C1, la serie va de **72.009-72.264 (2019) a 91.121-94.426 (2024)**;
  - en el total nacional del Ministerio va de 78.810 a 100.980.
- **Corrección.** Usar el rango por año en territorio común, o «72.000-94.000 al año» con la nota de que no incluye el País Vasco ni Navarra.
- En el policy brief, además, no comparar ΔH acumulado en 5 años con terminadas anuales: hay que dar las dos magnitudes para la misma ventana.

### C2. M5: codificación asimétrica de I01 y un «n_documentos» que suma posiciones opuestas
- **Codificación desigual.** En `medidas_programas.csv`, las propuestas de derogar la ley o el control de rentas se codifican de dos maneras:
  - en dos documentos, como «I01 … (propuesta de derogación)»;
  - en otro documento (pasada 2), con dos filas («acabaremos con … el control de rentas», «derogaremos la Ley por el derecho a la vivienda»), como I01 a favor.
- **Fila mal asignada.** Una fila de otro documento (deducciones del IRPF y recargo en el Impuesto sobre Sociedades) es fiscalidad de arrendadores (I15), no I01.
- **Consecuencia en la matriz.** `_n_docs()` corta el código por el primer token, así que la matriz da a I01 `n_documentos = 6`, cuando son 3 a favor y 3 en contra. Contradice la definición de la columna («0 = no propuesto»).
- **Corrección.**
  - Recodificar con una sola regla.
  - Añadir la columna de dirección (a favor / derogar o reducir).
  - Separar en la matriz `n_documentos_a_favor` y `n_documentos_en_contra`.
  - Revisar con esa regla las 88 filas.

### C3. M5: 9 de los 29 instrumentos propuestos faltan en la matriz sin criterio declarado
- **Qué falta.** La matriz dice «Rúbrica idéntica para todos», pero omite I03 (3 documentos), I11 (1), I15 (2), I18 (3), I19 (2), I22 (1), I24 (2), I25 (1) e I28 (1).
- **Por qué es un problema.** Sí incluye I12 e I29, con un documento cada uno. La selección no es neutral por construcción.
- **Corrección.** Añadir todas las filas, con «sin evaluar» si procede, o declarar en `matriz_instrumentos.md` y en `decisiones.md` un criterio de inclusión objetivo y aplicarlo a todos.

### C4. Promoción de capa en las magnitudes de P-D v3 y trato desigual de las ayudas a la demanda
- **Qué dice v3.** `src/v3/pd_run.py` (notas de `resultado.json`): «Capa C2 solo para cantidades contables y signo bajo supuestos débiles; magnitudes de precio condicionales a ε (C4)». Además, |εd| «sin estimación verificada para España».
- **Qué hace M5.** Rotula como C2 las magnitudes de esfuerzo de P1 (−24,4 a −0,8 %), I02 (−13,1 a 0 %) e I10 (−4,5 a −0,1 %). Lo mismo hacen el informe técnico §5 y la tabla del working paper §6.
- **La asimetría.** La incidencia de las ayudas, construida con el mismo tipo de rejilla de elasticidades, queda en C4. Su signo (el beneficiario gana y el no beneficiario paga más, en toda la rejilla con εs > 0) es tan robusto como el de P1, y aun así queda en C4.
- **Corrección, con una sola regla para todos.**
  - **Signo estable en la rejilla:** C2. Afecta a P1, I10, I02 (débil) y a las ayudas (por grupo: beneficiario y no beneficiario).
  - **Magnitudes de precio o esfuerzo:** C4 en todos los instrumentos.
  - Usar la **misma rejilla de oferta** que P-D v3 (η ∈ {0; 0,45; 1,75} y \|εd\| ∈ {0,3 … 1,5}) en lugar de 0,2-2. Con η = 0 la parte que se traslada al precio llega al 100 % y el rango pasa a 15-100 %.

### C5. Simetría de veredictos V11 frente a M5-V1
- **V11** («Construir vivienda pública resolvería…») recibe PARCIALMENTE en las dos convenciones, con el argumento de que «el signo no depende de la traducción a precio».
- **M5-V1** («Las ayudas a los jóvenes abaratan su acceso») recibe NO CONCLUYENTE con la convención A, aunque el signo para el beneficiario también es estable en toda la rejilla.
- **Problema de fondo.** El esfuerzo de acceso solo existe a través de la traducción a precio, así que el argumento de V11 vale igual para M5-V1.
- **Corrección.** Aplicar una regla común:
  - o las dos reciben PARCIALMENTE, cada una acotada a lo que muestra la rejilla: en V11 «reduce o deja igual, lejos de la brecha»; en M5-V1 «abarata para el beneficiario, encarece para el resto»;
  - o las dos reciben NO CONCLUYENTE con la convención A.
- **Revisar «resolvería» en V11.** Con 10.000-25.000 viviendas al año frente a una brecha de 104.000-413.000 al año, la propia ficha describe una magnitud insuficiente para «resolver». Hay que justificar por qué no es NO RESPALDADA en ese componente.

### C6. M7, alquiler: «C1 en dirección; cuantía no establecida» es **aceptable**, con tres condiciones
**Por qué es aceptable.** IPC de alquiler (INE) y SERPAVI (AEAT) son independientes, y las dos variaciones son positivas y lejos de cero en 2015-2024 (+11 % y +43 %) y en 2021-2024 (+6 % y +15 %). El signo es un hecho C1. No procede bajar la dirección a C4.

**Por qué la cuantía no es C1.**
- La regla de ±5 pp anuales no discrimina: con crecimientos del 1-6 % anual admite fuentes que difieren en un factor de 4.
- Con la regla de niveles (±15 % sobre el índice acumulado), 1,109 frente a 1,430 da un 29 % y no pasaría.

**Condiciones.**
- (a) En `variacion_alquiler.csv` y `variacion_precio.csv`, la columna `capa` debe pasar a `capa_direccion = C1` / `capa_cuantia = C4`, y hay que quitar o rotular `mediana_pct`, que se lee como cifra C1.
- (b) **La misma regla para el precio de compra.** INE frente al Ministerio (+80 % frente a +44 %; 25 % con la regla de niveles) es el mismo caso. Hoy el working paper y lo_que_sabemos dan al precio un C1 pleno «+44 % a +80 %» y al alquiler «cuantía no establecida». El precio sí tiene un núcleo de cuantía: Ministerio, Notariado y Registradores, +44 % a +56 %, dentro de ±15 % en nivel. Si se considera C1, hay que declarar la independencia parcial entre el Ministerio y el Notariado. INE IPV queda como fuente discrepante.
- (c) **Corregir la explicación de la discrepancia.** «Una mide precios y la otra un stock de contratos» no es exacto: las dos cubren contratos vigentes. El IPC sigue la renta de las mismas viviendas, con una actualización anual limitada por ley en 2022-2024 (sin verificar en BOE). SERPAVI es la renta media declarada, que incorpora contratos nuevos y cambios de composición.

Además:
- En lo_que_sabemos, «coinciden cuatro fuentes … en las 17 comunidades» es falso: las CCAA tienen 3 fuentes y Navarra 2.
- La regla de ±5 pp debe figurar en `decisiones.md` como regla de **dirección**, no de cuantía.

### C7. Procedencia de los programas: cifras y etiquetas incoherentes entre documentos
- **Copias de medios.** `fuentes_fallidas.md` dice que **tres** programas se leyeron en copias alojadas por medios, además del marcado «copia no oficial». En total son 4 de 9 en copias de prensa.
- **Qué dicen los entregables.**
  - Working paper: contribución 4, «Las medidas proceden de documentos oficiales», y limitaciones, «uno se leyó en copia no oficial».
  - Informe técnico §5 y README: «Webs oficiales de los partidos».
  - Ninguna de las tres afirmaciones es cierta.
- **Corrección.** Una sola etiqueta para las 4 copias y la misma frase en todos los documentos.
- **Recuentos de `instrumentos.md`.**
  - Dice 89 medidas; el CSV tiene 88.
  - La columna «Docs (de 8)» está desfasada: I01 = 5, I02 = 6, I13 = 1 y N1 = 0 no cuadran con el CSV.
  - La sección «Pendiente» no está cerrada.
  - Hay que recalcular desde el CSV.

### C8. Esfuerzo de recogida y de literatura: hay que documentar el equilibrio
- **Recogida desigual.** La lectura parcial varía entre documentos (de 2-3 páginas a unas 35). Las medidas por documento van de 2 a 22. Con ese protocolo, los recuentos de `n_documentos` dependen de cuánto se leyó.
- **Corrección de la recogida.** Añadir una tabla de cobertura por documento anonimizado (páginas leídas sobre totales y términos de búsqueda) y aplicar a los 9 documentos el mismo protocolo de búsqueda por palabras clave sobre el texto completo. Los dos programas no accesibles ya están bien documentados: no se intentó sortear el bloqueo y el esfuerzo fue comparable.
- **Literatura desigual.** Según `literatura_v4.md`, varios temas quedaron «no buscados»: fiscalidad en España, industrialización, captura de plusvalías y el impuesto de Vancouver. Otros no tienen búsqueda registrada: límites a no residentes, seguridad jurídica y licencias con magnitud. En cambio, sí se buscaron dos o más referencias para las ayudas, la vacancia y la regulación de rentas.
- **Corrección de la literatura.** Con la misma búsqueda para cada instrumento, «sin evaluar» debe significar «sin evidencia hallada», no «no buscada». Hay que reintentar Sinai y Waldfogel (2005), sobre el desplazamiento en la vivienda pública, y Fack (2006). Hoy I02 no cita ningún resultado sobre desplazamiento, mientras que I01 sí cita su riesgo (Diamond et al.).

### C9. Demanda latente por jefatura: la capa no sigue la regla B5
- M2-H1 declara la jefatura por edad de fuente única (EPA), C4.
- La cota latente por jefatura (16-34 años: ±23.000; 20-34 años: +84.000 a +161.000) se publica como C2 en el working paper §5.2, en lo_que_sabemos y en el policy brief.
- Según B5, «C2 exige que todo lo medido sea C1». Hay que pasarla a C4 o justificar por qué la tasa de 2008 es un supuesto acotado y no un componente medido.
- La cota por convivencia (188.000-506.000; Eurostat/ECV y EPA, C1 en v3) puede quedarse en C2.

### C10. Conclusiones del working paper y del informe técnico: alcance y capas
- **Conclusión 1.** Mezcla el desfase C1 con «concentrado territorialmente», que es C4. Hay que marcar la capa de cada parte.
- **Conclusión 4, resumen e informe técnico §5.** «Solo las medidas que añaden viviendas … tienen signo estable» debe decir «entre los instrumentos simulados». Siete grupos están sin evaluar, y algunos de ellos (licencias, densidad, suelo) actúan también sobre la oferta. Sin ese matiz, la frase se lee como una ordenación de instrumentos que no se evaluaron.
- **Signo frente a magnitud.** Los tres textos deben decir que el signo es C2 y la magnitud C4 (ver C4).
- **Referencias del working paper.** Falta Baum-Snow y Marion (2009), que se cita en la matriz. Hay que incluir todas las referencias de §6 con su cuartil o «cuartil no verificado».

### C11. Restos de versiones anteriores en el verificador y en M6
- `output/v4/verificador/fichas/V13.json` y `V14.json` siguen versionados con el contenido de v3:
  - V13 dice «no se realizó test GSADF»;
  - V14 sigue en C1.
  
  `verificador.md` y `resumen.csv` ya los excluyen. Hay que borrar los ficheros, o hacer que `verificador.py` limpie el directorio.
- `preguntas_abiertas.md`, pregunta 10, dice «No se ejecutó el test GSADF (V13)». M7 lo ejecutó (5 de 17 CCAA). Hay que actualizarla o retirarla.

### C12. Ficha M5-V1: precisiones sobre la incidencia
- **La fórmula es correcta.** La parte de la ayuda que se traslada al precio es |εd|/(εs+|εd|) para una ayuda **general** por unidad. Con la rejilla actual, el mínimo y el máximo (13 % y 88 %) están bien calculados.
- **Ayuda focalizada.** Para una ayuda a un grupo, como los jóvenes, el traslado al precio por euro se escala por el peso de ese grupo en la demanda, así que el 13-88 % es una cota superior. La ficha debe decirlo.
- **Avales.** Los avales no son una ayuda por unidad: relajan la restricción de entrada. Esa traducción es aún más incierta, y Carozzi et al. (2024) sirven solo como referencia cualitativa.
- **Convenciones.** Las convenciones A y B son correctas en su planteamiento, pero hay que alinearlas con C4 y C5.

### C13. Neutralidad léxica (menor)
- `instrumentos.md` usa «antiocupación» (I14), «compras especulativas» (I21) y «retención especulativa» (N3). Hay que usar los rótulos neutros de la matriz: «procedimientos de desalojo», «con fin de inversión» y «suelo sin edificar».
- `fuentes_fallidas.md` (l. 9) incluye un dominio que identifica a un partido. Hay que redactarlo como los demás.
- `decisiones.md`: «de todo el espectro» debe sustituirse por «de distinto signo».

### C14. README de replicación (menor)
- **Cumple lo esencial del estándar.** Incluye fuentes y licencias por organismo, manifiesto, tiempos medidos, pasos, orden de los programas, hardware, software y la muestra sellada.
- **Falta corregir:**
  - el tiempo: README dice ≈20-21 min y el working paper, apéndice B, «unos 25 minutos»;
  - el acceso a los programas («Webs oficiales»; ver C7);
  - las condiciones de reutilización de Notariado y Registradores, que deben marcarse como «no verificadas» si no se comprobaron;
  - la correspondencia entre figuras o tablas y programas: hoy es por módulo, y hay que darla para las tablas y figuras citadas en el working paper.

## Comprobación de cifras (30 cifras; ✓ = coincide con la fuente)

| Cifra en los entregables | Fuente | Estado |
|---|---|---|
| Déficit 2021-2024: 563.000-689.000; con bajas, hasta 903.000 | M0 | ✓ |
| ΔH 2021-2025: 982.000-1.013.000 | M2 `total_dH_fuentes` | ✓ |
| Terminadas: 91.000-101.000 al año (2019-2024) | M0 | ✗ (C1) |
| Precio: +44/+80 % (2015-2025) y +24/+36 % (2021-2025) | M7 | ✓ (cuantía, ver C6) |
| «Cuatro fuentes en las 17 CCAA» | M7 | ✗ (3 fuentes; Navarra, 2) |
| Alquiler: +11/+43 % y +6/+15 % | M7 | ✓ |
| 7 provincias suman el 50 % y 19 el 80 %; 249 municipios con 71.000 viviendas | M1 | ✓ |
| Componente extranjero: 56-58 % (53-76 %) | M2 (55,6 %) | ✓ (redondeo) |
| Extranjeros: 16,9/10,1/6,8 % y 18,8/11,6/7,2 %; Registradores 13,8-15,0 % | M4 | ✓ |
| Personas jurídicas: 11,3 % compradoras, 24,7 % vendedoras, 5,6 % en 2007 | M4 | ✓ |
| Vacías 3,83 M (14,4 %); esporádicas 2,52 M (9,5 %); VUT 341.000 (1,3 %); tenencia 75,5/16,1/8,4 %; EFF 46,8 % | M4 | ✓ |
| Clases 16/30/4 provincias; 298/156/247 municipios; 22 estables | M3 | ✓ |
| Latente: 188.000-506.000; 20-34 años, +84.000/+161.000; 16-34 años, −22.000/+23.000 | M1, M2 | ✓ (capa, ver C9) |
| GSADF: 5 de 17 CCAA; tamaño 12,7 % | M7 | ✓ |
| P-D: −24,4/−0,8; −13,1/0; −4,5/−0,1; 4,6-51,2 %; −2,9/+7,3; −1,7/0 | v3 PD | ✓ (capa de la magnitud, ver C4) |
| Incidencia de las ayudas: 13-88 % | M5 | ✓ (rejilla, ver C4) |
| Propiedad de menores de 35: 30,7-31,8 %; convivencia con los padres: 40-50 %; p Holm de GL = 0,27 | v3, M0 | ✓ |
| Solares: 3,09 M; VUT ≤ 2,7 % del stock de alquiler | M3, v3 | ✓ |
| València ciudad: déficit 13.000; brecha +1.217; clase 2 con estabilidad del 97 %; 8,8/7,3/1,3 % | M1, M3, M4 | ✓ |
| Provincia de València: 59.000-80.000 (mediana 69.000); 69 % de 79.000 hogares; brecha +243 (estabilidad 42 %); latente 18.000; esfuerzo 3,0 años y 16,3 % | M1, M2, M3, v3 PA | ✓ |
| `n_documentos` de I01 = 6 | CSV | ✗ (posiciones opuestas sumadas, ver C2) |

## Módulo València
- Las cifras y las capas coinciden con su fuente: todas en C4 salvo el precio regional, que es C1 en dirección.
- Hay que añadir las variaciones de la Comunitat Valenciana:
  - precio 2015-2025: +50 % a +67 %;
  - alquiler 2015-2024: +13,7 % (IPC) a +57,2 % (SERPAVI). Es la mayor discrepancia entre fuentes de alquiler de todas las CCAA, y debe llevar la etiqueta «dirección C1; cuantía C4».
- Hay que anotar en la fila de VUT que el 1,3 % mezcla viviendas turísticas de 2026 con el Censo de 2021.

## Lo que está bien
- **Fichas pedidas.** Están las cinco: M5-V2, M5-V3, M3-V1, M4-V2 y M5-V1.
- **Simetría entre afirmaciones de oferta y de demanda.** Es correcta en M3-V1, M4-V1, M4-V3, M5-V3, M5-V4, M5-V5 y M7-V1: todas en C4, con veredicto como máximo NO CONCLUYENTE (B4). La excepción es V11 (C5).
- **M7-V1.** La lectura del GSADF es prudente: exuberancia no es burbuja, y la ficha informa del sobre-rechazo y de la baja potencia del bootstrap salvaje. La columna `exuberancia_holm05` aplica BH; conviene cambiarle el nombre.
- **Neutralidad.** No hay nombres de partido en las salidas de M5, M7 ni en los entregables (con la excepción de C13).
- **Working paper.** La estructura académica está completa: resumen de 168 palabras, 4 contribuciones y todas las secciones pedidas.
- **Solicitudes de M6.** Están bien especificadas.
