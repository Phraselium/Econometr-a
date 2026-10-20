# E8-R1 · réplica ciega V18; capa C4

ITP por CCAA, ln valor tasado provincial trimestral, dCDH con dosis continua, efecto acumulado a 4 trimestres por +1 pp del tipo general. Código: src/v18/replica/e8_r1.py (SEED 20261010). Clasificación V18: no se clasifica (réplica ciega); nivel_evidencia EXPLORATORIO. La adenda fija además tope SUGESTIVO (sin control de recaudación previa, que no está descargada).

## Resultado

| | Réplica ciega | Orquestador |
|---|---|---|
| Coeficiente (l = 4) | +0,01461 | +0,0146 |
| Diferencia | +0,00001 absoluta; 0,06 % relativa | |
| EE, cluster CCAA (7 clusters) | 0,0047 | |
| IC95 (inversión de aleatorización) | [0,0013; 0,0303] | |
| IC95 normal por cluster | [0,0054; 0,0238] | |
| p aleatorización del calendario (9.999) | 0,044 | |
| p Webb (WCR, 9.999) | 0,0001 | |

La cifra del orquestador cae en mi IC95. Veredicto: **coincide** (misma cifra al redondeo).

## Muestra y decisiones

- Tratamiento: tipo general del ITP de data/raw/v16/intervenciones/intervenciones.csv (memorias de Hacienda). Andalucía mezcla las etiquetas «tipo general» y «mínimo de la escala»: por fecha se toma la general si existe, si no la mínima.
- Fechas: día <= 15, ese mes; si no, el siguiente; trimestre de ese mes. Cambios de una CCAA a menos de 12 meses, un solo evento con dosis acumulada (Comunitat Valenciana 2013: +3).
- 16 eventos en 8 CCAA; en el panel analizado, 13 cambios en 7 CCAA (Cantabria sale). Mínimo de la adenda (8 cambios, 4 CCAA) cumplido.
- Panel 2010T1-2026T2 (el fichero no da tipos antes de 2010). 30 provincias con serie completa, N = 1.980.
- Horizontes: l=0 +0,0030; l=2 +0,0017; l=4 +0,0146; l=6 -0,0003; l=8 -0,0047 (patrón no monótono).

## Lecturas que admitía el texto

1. **Provincias con huecos.** Valor tasado provincial falta en 2012T2-T4 en 34, 40, 42, 16 y 32; Cantabria (39) no tiene serie provincial. Principal: solo series completas (30 de 36). Con huecos interpolados (solo robustez): 35 provincias, +0,0122.
2. **Inicio del panel.** Sin tipos antes de 2010 no se extrapola; no cambia el estimador (no hay eventos antes).
3. **Horizonte.** «Efecto a 4 trimestres» como DID_4 acumulado (Y_{t+4} - Y_{t-1}).
4. **Fechas.** Fechas -3 meses: +0,0088; +3 meses: +0,0131. Sin 2012-2013: -0,0079 (cambia de signo; la adenda lo marca como tope SUGESTIVO).
5. **Inferencia.** Calendarios permutados entre las 7 CCAA presentes (no entre años). IC por inversión con 1.999 permutaciones en rejilla de 61 puntos; el p principal usa 9.999. Con 7 clusters, el IC normal es optimista.
6. **Recaudación previa.** No disponible: se omite.

Estimación sensible a la ventana 2012-2013 y a la fecha: valorar con cautela (episodio histórico, nunca C3).
