# V18 · Fase 3 · Revisor del pre-registro sobre el plan de replicación (2026-10-20)

Revisión de solo lectura de docs/v18/plan_replicacion.md (commit d4e9869). **Veredicto: APTO CON CAMBIOS**; la etiqueta plan-replicacion-v18 espera a que la adenda resuelva los hallazgos de gravedad alta (1-9).

## Alta
1. **E2, ventana 2016T1-2022T1 no existe en trimestres.** Incasòl municipal es trimestral solo desde 2019T1 (docs/v3/decisiones.md:125; docs/v9/decisiones.md:29; src/v9/paneles.py:56-57). Corrección: leer la ventana exacta de JMS en su PDF; principal trimestral 2019T1-2022T1 marcada repite_visto (es V9-D1b); variante sin 2020T1-2020T3 en pretendencias; robustez anual 2014-2021 con Honest DiD; paro registrado trimestral (y ERTE si hay); placebo de fecha en la serie anual (2017); término de anticipación desde 2019T2 (RDL 7/2019 y Decreto-ley catalán 9/2019, a verificar en el DOGC); comprobar el calendario solo con metadatos.
2. **E2-R2 y R2s (por tramo) no estimables.** `tram_preus` clasifica al municipio, no reparte contratos (src/v9/paneles.py:58; docs/v9/revision_f2.md:17). Corrección: NO ESTIMABLES (X), fuera de la familia de Holm de E2 (7 → 6); corregir output/v18/f0/informe.md.
3. **Sellado temporal en E3.** El padrón por nacionalidad provincial y la población extranjera municipal tienen último periodo visto 2022 (docs/v16/sellado_v16.json:680,696); E3-A1 a A4 usan años posteriores. Corrección: cortar en 2022; regla de frecuencia (manda la clave de la frecuencia usada; una media anual no incluye años posteriores a la clave anual); variables sin manifiesto: selladas enteras (src/holdout.py:711).
4. **IDENTIFICADO (B3) frente a la capa C4.** metodologia/capas.md:11-12 (C3 exige evaluación sellada; C4 sin lenguaje causal) y CLAUDE.md (causalidad solo en C3/C3s) frente a B3 («se puede hablar de causa»). Corrección: decisión K del autor antes de la etiqueta; por defecto la restrictiva (nivel_evidencia EXPLORATORIO en C4, campo clasificacion_v18 aparte, fórmula condicional solo en secciones técnicas del Documento de Trabajo, nunca en cifras_clave, web ni resúmenes; lo comprueba check_v18); vía a C3 con una evaluación sellada diferida (evaluate_v18) con datos posteriores; los episodios históricos (E2-R1, E3-R1) no pueden llegar a C3 con la definición actual.
5. **Multiverso sin enumerar.** Corrección: enumerar cada variante (control, ventana, medida, peso, estimador) antes de la etiqueta; holgura limitada (p. ej. 200); la holgura no apoya IDENTIFICADO ni entra en B5.
6. **B5 filtra por significación** (maldición del ganador). Corrección: B5 admite las estimaciones con diseño válido (I1-I6, I8) sea cual sea p; clase «NO CONCLUYENTE (sin potencia)»; nulo acotado por TOST con δ por factor.
7. **B5 cuenta dos veces el mismo episodio** (E2 con JMS y Monràs; E3 con González-Ortega; E1 con García-López; E7 con San Juan). Corrección: una estimación propia por factor fijada ahora; si el episodio coincide, sustituye o se combina con correlación modelada.
8. **repite_visto incoherente.** Faltan E3-R1/R2 (V9-D4), E3-A1 (Q3-c1), E7-R1 (Q5, V8 H8-5 a H8-7), E8-R1/R2 (Q6), E2-A3 (Q1c), E1-R1/R3 (V9-D2), F1-R1/R2/A1 (V7.2, V8-M4, V15). Corrección: marcar toda coincidencia en resultado, exposición, unidad y periodo; estimar al lado la especificación anterior exacta; si la clase mejora solo por un cambio que corrige un fallo conocido, tope SUGESTIVO.
9. **I2 confunde fuerza y significación.** Corrección: I2 = F efectivo > 10 o conjunto AR acotado (sin exigir excluir el cero); significación solo en I7; con F < 10, tope SUGESTIVO.

## Media
10. **Umbrales de comprobación previa arbitrarios y ambiguos** (E1-R1 casi seguro NO ESTIMABLE con la moratoria; definiciones de la desviación intra-unidad, «10 % entre cortes», denominador, paso de cortes a años, corte de 2024T1; E2-A2 contradictorio; faltan mínimos en E2-R1, E6-R1, E8, E9 y choques efectivos en E3/E5). Corrección: regla común sin mirar resultados: estimable si el MDE por Monte Carlo con la variación real y la σ residual de V15/V16 es ≤ la referencia de la literatura convertida; si no, «NO ESTIMABLE por variación».
11. **BHJ con pocos choques** (E3 ~16 orígenes; E5 ~21 secciones). Corrección: si 1/HHI < 20, principal con cluster por provincia y Webb, más AR; publicar 1/HHI.
12. **E3-R1, cuotas de 2001 dentro de 1998-2008**; choque sin quitar la propia provincia antes de 2003; referencia de R2 imprecisa; unidades distintas en B5. Corrección: principal 2002-2008 (1998-2008 como variante); fijar el precio medio de conversión; convertir por la proporción en edad de trabajar o no combinar.
13. **I6 laxo.** Corrección: razón en [1/3; 3] respecto a una referencia única por especificación; el solapamiento solo si el error de la referencia es menor que la mitad del coeficiente.
14. **E1-R2/A1, primera etapa y exclusión** (moratoria; COVID; pretendencias contaminadas por el auge 2012-2016). Corrección: endógena INE-VUT (desde 2020); variante sin 2020-2021; pretendencias 2007-2011 si SERPAVI llega, si no tope SUGESTIVO; fijar la consulta de Trends.
15. **Placebos inexistentes o sin fecha** (65+ por sección solo 2021-2025; E1-R4 sin fecha; E1-R3 con dos años de preperiodo; E1-A2 dosis continua escalonada). Corrección: placebo con padrón por sección y edad o no aplicable; fecha de R4 o NO ESTIMABLE; de Chaisemartin-D'Haultfœuille o Callaway, Goodman-Bacon y Sant'Anna en A2.
16. **E2, controles emparejados por el resultado previo.** Corrección: quitar esa variante o emparejar por covariables; mínimo de controles; variante con municipios tensionados no regulados.
17. **E5-R1, exclusión del Bartik** y cambio CNAE-93 a CNAE-2009. Corrección: principal sin construcción ni inmobiliarias; tabla de correspondencia fijada; auge y caída por separado.
18. **E8, 8 clusters tratados, cambios en 2012-2013**; las 8 CCAA suman 36 provincias, no 30. Corrección: aleatorización del calendario y Webb restringido; tope SUGESTIVO salvo tamaño de Monte Carlo en [0,04; 0,06]; corregir el recuento.
19. **Banda «apta» del Monte Carlo laxa.** Corrección: valor crítico corregido por tamaño fuera de [0,04; 0,06].
20. **Totales municipales con distritos sellados** (V15/V16). Corrección: declarar la convención de V16; robustez sin esos municipios; publicar antes de la etiqueta qué distritos de Barcelona salen (distritos_sellados_v16(), sin abrir datos).
21. **Contabilidad con unidades dinámicas mal casadas** (E7 a 8 trimestres frente a 13 años; E3 sin las provincias de más inmigración). Corrección: respuesta acumulada a un cambio sostenido; validez externa en cada fila.
22. **Parada G3 asimétrica.** Corrección: G3 con cualquier IDENTIFICADO incompatible con «no concluyente», en cualquier signo.
23. **E2-A1 frente a H1/H2 pendientes.** Corrección: no difundir antes de la evaluación sellada de V15, o rotular provisional.

## Baja
24. Holm: familia solo con las que pueden llegar a SUGESTIVO o IDENTIFICADO; m tras las comprobaciones previas.
25. Priors de B5: tres variantes; combinar solo si la decisión coincide en las tres.
26. Referencias de I6 y B5 de fichas NO VERIFICADAS: verificarlas o rotularlas.
27. Ambigüedades: E7-R3 (saldo, posterior_prereg); sorpresa hasta 2025-10; E1-R1 sin controles variables en el tiempo; desfase de E6-R1.
28. Potencia: MDE previo por especificación principal (hallazgo 10).
