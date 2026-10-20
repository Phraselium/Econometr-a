# V18 · E1-R4 (Sagrada Família) · réplica ciega V18; capa C4

Código: src/v18/replica/e1_r4.py (SEED 20261010, sin red). Salida: resultado.json y datos_intermedios.json. Sin clasificación V18 (réplica ciega); nivel_evidencia EXPLORATORIO.

## Lecturas de la ficha (plan 1.1 E1-R4 y adenda 1.5, R-15, Anexo B)
- Ecuación: ln SERPAVI_st = β·Radio_s·1[t ≥ 2014] + α_s + γ_t + ε_st. SERPAVI = mediana €/m², vivienda colectiva (serie ALQM2_LV_M_VC), 2011-2019, base 2013, preperiodo 2011-2012 (adenda R-15).
- Muestra: src/v18/sellado.filtrar (sin Gràcia, Sant Andreu ni Nou Barris), solo secciones con los 9 años.
- Distancia de la sección al templo (41,4036 N; 2,1744 E): **centroide** de la sección (la ficha no lo precisa; decisión mía). Radio < 500 m; anillo 500-1.000 m.
- Cluster por barrio (ficha, e); wild cluster bootstrap de Webb (WCR, 9.999 réplicas); IC por inversión del test.
- TOST con δ = 0,05 en log (Anexo B, E1-R4: «no aplica» referencia; δ = 0,05).

## Resultados (principal)
- Secciones: 21 en el radio y 56 en el anillo (tras el sellado); 5 clusters (barrios). Estimable: retención de radio 87,5 % y de anillo 78,9 % (> 75 %).
- β = 0,0011; error típico CR1 0,0069; p de Webb = 0,845.
- IC95 de Webb [−0,0470; 0,0716]; IC90 [−0,0384; 0,0544].
- TOST (δ = 0,05): **el nulo no queda acotado** (el IC90 supera +0,05 por arriba). Con 5 clusters el IC es ancho; clase de la adenda: NO CONCLUYENTE (sin potencia), si el resto del diseño se sostiene.
- Adelantos 2011-2012 conjuntos: F p = 0,068 (débil, entre 0,01 y 0,10). Placebo de fecha 2012 (ventana 2011-2013): −0,0151, p Webb 0,199. Placebo de resultado: no aplicable (adenda R-15). Honest DiD no calculado en esta réplica.

## Comparación con el orquestador
| | Orquestador | Réplica |
|---|---|---|
| Estimación | 0,0018 | 0,0011 |
| IC95 Webb | [−0,0446; 0,0418] | [−0,0470; 0,0716] |
| Secciones radio / anillo | 77 / 693 | 21 / 56 |
| Clusters | 6 | 5 |

- Diferencia absoluta −0,00068 (−38 % relativa); es 0,099 de mi error típico CR1 (0,0069) y 0,03 del error típico implícito del orquestador (≈ 0,022). Cada estimación cae en el IC95 de la otra.
- **Veredicto: coincide** (diferencia < 10 % del error típico), pero en el límite con mi error CR1; al redondeo a 4 decimales no coincide (0,0011 frente a 0,0018). Ambas cifras son nulas con IC anchos.

## Por qué los recuentos difieren (decisiones con varias lecturas)
- 77 secciones: con el centroide a < 1.000 m del templo hay 77 secciones no selladas. Y 693 ≈ resto de Barcelona no sellada (769 − 77 = 692). Por tanto el orquestador parece usar un radio efectivo mayor (≈ 1 km) con el resto de la ciudad como control, no «500 m frente a 500-1.000 m». La ficha escribe 500 m y anillo; el recuento sugiere otra lectura del radio, o del anillo (variante v1, «resto de Barcelona»).
- Variantes declaradas, no principales (solo β, CR1): resto de Barcelona como control (21 vs 743): −0,0001; 300 m vs 300-800 m: 0,0014; distancia al polígono (32 vs 63): −0,0059; centroide < 1.000 m frente al resto (77 vs 687; 46 clusters): −0,0010.
- Otras lecturas abiertas: centroide o polígono; coordenadas del templo; qué es un cluster (barrio frente a 6 unidades del orquestador; yo obtengo 5 barrios); exclusión de secciones con serie incompleta (aquí 9 años en todas).
- Todo apunta a muestra y definición (radio, medida de distancia, control), no al estimador: DiD TWFE con las mismas bases.
