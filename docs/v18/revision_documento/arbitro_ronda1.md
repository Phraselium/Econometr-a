# V18 · Fase 6 · Árbitro del Documento de Trabajo, ronda 1 (2026-10-21)

Revisión de solo lectura de output/v18/documento/documento_v18.md como revisor de Documentos de Trabajo del Banco de España. **Veredicto: REVISAR.** Estructura completa, tono prudente y neutral, lo no estimable declarado y lo a posteriori separado (anexo F); la conclusión central (ninguna estimación IDENTIFICADO; toda la variación «no explicada») se sostiene. Hay errores que pueden inducir a una lectura equivocada; se corrigen sin estimar de nuevo.

## Mayores
1. **Tabla 5.1b mal rotulada.** Las cifras por comunidad son desviaciones respecto a la media de las provincias no selladas («relativa entre provincias, sin el componente común»), el primer periodo provincial empieza en 2002T1 y la frase «no suman el total nacional, que incluye las provincias selladas» da una razón equivocada. Corregir rótulo, cabecera y frase.
2. **Clases V18 mal propagadas.** 14 ids aparecen como SUGESTIVO, pero solo E2-R1 lo es; E1-P-H3 («no se clasifica»), E2-R1-REV (IC con el cero), las robusteces B6, V18-B5-E2, la ilustración C5I y E1-R4-v3 heredan la etiqueta. Clase propia por especificación en f6_hechos.py; robusteces como «robustez a posteriori».
3. **E8 contradictorio en la tabla de impactos:** NO ESTIMABLE en la clase y «ASOCIACIÓN» en la limitación. La clase es la de E8-R1: ASOCIACIÓN.
4. **E2-R1 frente a V17, incompleto.** V17 da −5,8 % (−6,8 a −5,1 %, V17-AUD-RA-TOP-INC-RENTA-RANGO); E2-R1 −3,77 % (−2,3 % con trayectorias por tamaño). Explicar la diferencia (controles, paro, sin Barcelona, exclusiones selladas) y dar: SERPAVI −0,005, multiverso −0,005 a −0,056, sesgo indetectable de Roth 0,061.
5. **Frase de limitación no literal.** IC95 redondeado (−0,05 a −0,03 en vez de −0,051 a −0,026), muestra añadida y porcentaje cambiado; publicar el intervalo con M̄ = 0,5 (−0,087 a 0,025) junto a la advertencia de potencia.
6. **Contabilidad ilustrativa:** E3 y E9 (relativas) restadas de la variación nacional; en Cataluña E2-R1 sola aunque B5 no da magnitud para E2; −2,7 pp junto a −2,8 pp sin repetir «ilustración, no atribución».
7. **F1 sin evaluación fuera de muestra** (ECM 1,358 frente a AR(4) 1,285; DM p = 0,19; «no predice mejor», K1 de v6.1); corto plazo con PMG que supone cointegración rechazada: estimar en diferencias o retirar; F2 con signo negativo sin comentario.

## Menores
8. E4: «IC95» con dos estudios no fiable; θ = 0,04 lejos de la mediana de V17 (46 %).
9. E1: magnitud preferida de un documento de trabajo NO VERIFICADO (Segú 2018); pretendencias rechazadas en E1-R3 (p = 0,008); E1-R3 unas nueve veces menor que la literatura sin explicar; 769 frente a 766 unidades.
10. Rangos de E8 y E9 de un solo estudio; comparación circular con San Juan en 5.1g.
11. E8: Holm 0,087 sin informar; «ocho» comunidades (son siete); «la primera» evaluación española del ITP no sostenible; Dölls/Dolls.
12. Lenguaje (K2): «ATT» en el resumen ejecutivo; «V17 limitaba el efecto local»; «contribución del factor».
13. Regla de ASOCIACIÓN (3.3) con placebo «del mismo signo» frente al motivo publicado de E2-R1c (signo contrario).
14. Anexo E: dos criterios de «apto» (encargo y adenda 1.12) sin exponer.
15. Reglas y unidades: AR no acotado → NO ESTIMABLE en E7-R1 y ASOCIACIÓN en E12-A2; E7-R2 y E7-A2 sin unidad; unidad de E12-A2.
16. BVAR: extracciones explosivas (15 % en E7-R3, 74,6 % en E7-A1) sin declarar.
17. Factibilidad (6.1): «2,8 a 4,4 veces» no se deduce de las cifras dadas; conciliar con T3-H9 (2,7; 1,4-3,8).
18. Restos: el anexo A dice que los valores por estudio no están en cifras_clave (sí están); periodo «1983-2024» repetido en B5; «clasificación provisional» en varios resultado.json.
19. Estrategia A de Hahn fijada en la fase 5: decisión a posteriori en el anexo F.
20. Tablas 6.2 y 6.3: falta el enunciado auditado.
21. Formato: abstract con español y comas decimales y largo; faltan códigos JEL y resumen en español; resumen ejecutivo de más de una página.
22. Falta publicacion/documento_v18/; colores de tablas_v18.xlsx sin comprobar.
23. Umbral de choques efectivos no declarado (E3 7,9 pasa; E9 6,3 no); BHJ NO APTA con pocos choques y E3-R1 clasificada sobre esa base.
