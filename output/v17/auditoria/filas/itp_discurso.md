Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada. Revisada tras la ronda 1 del abogado del diablo.

# Fila D1 · itp_discurso

## 1. Texto auditado
«Bajar el ITP abarata la vivienda»: no evaluable en España.

En lo publicado: informe integral III.4 («No evaluable con los datos disponibles») y VII.8.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** No hay evaluación española con diseño de un cambio autonómico del ITP:
- La búsqueda de V16 (ficha L4) dio trabajos jurídicos y un DSGE.
- Las de esta auditoría (2026-10-19, en español e inglés, dos rondas) solo dieron guías fiscales y prensa.
- Hay cambios posteriores a 2016 sin evaluar. Por prensa, que solo sirve para localizarlos: Andalucía, del 8-10 % al 7 % en 2021; Comunitat Valenciana, del 10 % al 9 % en 2026. Son candidatos a un diseño futuro.

Evidencia española parcial: Montalvo, Piolatto y Raya (2020; DOI verificado según el informe integral; ficha L4, resumen) documentan, con datos españoles de pago real, valor declarado y tasación, que el comprador declara por debajo para pagar menos impuesto. Implicaciones:
- El tipo efectivo es menor que el nominal.
- Una rebaja del tipo nominal se traslada menos de lo que dice el tipo.
- No estiman la incidencia en el precio.

El diseño propio (Q6 de V16) no informa (output/v17/lectura_bde/v15_v16_micro/inferencia.csv):
- Q6-p (valor tasado): −0,0020 log por punto, IC95 [−0,032; 0,028], p = 0,886.
- Q6-v (compraventas): +0,025, IC95 [−0,015; 0,065], p = 0,218.
- Hay 8 CCAA y 14 cambios de tipo concentrados en 2012-2013. La aleatorización rechaza un 7,8 % de las veces bajo la nula, y la herramienta figura NO APTA en su Monte Carlo.

**En contra (la frase es demasiado prudente).** La literatura internacional con diseño creíble es bastante coherente. Hay que separar los cambios temporales de los permanentes:
- **Rebajas temporales.** Adelantan compraventas, que se revierten en parte o del todo al terminar: +8 % en Reino Unido, revertido casi del todo (Besley, Meads y Surico, 2014); +20 % con la eliminación temporal de un 1 %, revertido menos de la mitad (Best y Kleven, 2018). En el precio, el comprador se quedó con unos 3/5 de la rebaja temporal en Reino Unido (Besley et al.).
- **Cambios permanentes.**
  - Volumen: −7 % por punto en Alemania (Fritzsche y Vandrei, 2019); −14 % con un tipo medio del 1,1 % en Toronto (Dachis, Duranton y Turner, 2012).
  - Precio antes de impuestos: el impuesto recae sobre todo en el vendedor. Toronto: el precio cae casi tanto como el impuesto. Alemania: −3 % por punto, más que la carga del comprador (Dolls et al., 2025). Davidoff y Leigh (2013), y Kopczuk y Munroe (2015) en el umbral.
  - Hay excepciones sin efecto en el precio: Petkova y Weichenrieder (NO VERIFICADA), en las casas unifamiliares alemanas.
- **Lectura.** Si la incidencia es simétrica, una rebaja permanente tiende a subir el precio antes de impuestos. El ahorro del comprador va desde una parte de la rebaja (Reino Unido, temporal) hasta casi ninguno (Toronto y Alemania, donde el precio absorbe todo o más). «Abarata la vivienda» es falso para el precio de mercado. Para el coste total del comprador, el resultado es incierto y depende del mercado.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Potencia de Q6.** Efecto mínimo detectable al 80 % de potencia (5 % bilateral):
  - Q6-p: 0,043 log por punto (V17-AUD-OT-ITP-Q6-p-MDE80). Más de 4 veces la incidencia plena en el vendedor (−0,01 por punto). No distingue incidencia nula, plena o superior al 100 %.
  - Q6-v: 0,057 (V17-AUD-OT-ITP-Q6-v-MDE80).
- **Q6-v frente a la literatura.** El IC95 de Q6-v [−0,015; 0,065] excluye el −0,07 por punto de Alemania (Fritzsche y Vandrei). Con salvedades:
  - la herramienta figura NO APTA en el Monte Carlo (aunque B2 permite publicarla, con un tamaño real del 7,8 %);
  - el placebo falla (es mayor y de signo contrario);
  - hay 8 clusters;
  - las compraventas son el total de vivienda, incluida la nueva, que no paga ITP;
  - los cambios se concentran en la crisis de 2012-2013.
- Conclusión: no se lee como evidencia contra la literatura, sino como otro indicio de que el diseño no separa el ITP del ciclo.

## 4. Literatura (ficha docs/v16/literatura/L4_fiscalidad_compra.md)
Todas son VERIFICADA (DOI en Crossref; cuartil no verificado) y se leyeron solo en resumen, salvo Dachis et al.:
- Besley, Meads y Surico (2014), 10.1016/j.jpubeco.2014.07.005.
- Best y Kleven (2018), 10.1093/restud/rdx032.
- Dachis, Duranton y Turner (2012), 10.1093/jeg/lbr007. Texto parcial.
- Dolls, Fuest, Krolage y Neumeier (2025), 10.1016/j.jue.2024.103717.
- Fritzsche y Vandrei (2019), 10.1016/j.regsciurbeco.2018.08.005.
- Kopczuk y Munroe (2015), 10.1257/pol.20130361.
- Davidoff y Leigh (2013), 10.1111/1475-4932.12056.
- Slemrod, Weber y Shan (2017), 10.1016/j.jue.2017.05.005. Discrepancia: sin bloqueo lejos de las muescas.
- Montalvo, Piolatto y Raya (2020): evidencia española parcial; DOI verificado según el informe integral III.4; resumen.

Validez externa: el ITP español (6-13 % según la CCAA, sin verificar aquí) es mucho mayor que los impuestos estudiados (1-4,5 %). Además, solo grava la segunda mano.

## 5. Veredicto
**Se sostiene con matices.** Sobre España es cierta: no hay evaluación, el diseño propio no tiene potencia ni separa el ITP del ciclo, y la única evidencia española (evasión) es parcial. Pero es incompleta de un modo que confunde. Fuera, una rebaja permanente no baja el precio de mercado y puede subirlo antes de impuestos. El ahorro del comprador va de parcial a casi nulo según el mercado. Las rebajas temporales sobre todo adelantan compraventas.

## 6. Texto corregido y confianza
«Bajar el ITP abarata la vivienda»: en España no se ha medido. Fuera, con diseños creíbles, una rebaja no baja el precio de la vivienda. Las rebajas temporales adelantan compras. Las permanentes aumentan las compraventas, y el precio antes de impuestos tiende a subir. El comprador se ahorra, según el mercado, desde una parte de la rebaja hasta casi nada.

Confianza:
- «La evidencia sugiere» (literatura de otros países, con tipos menores, leída en resumen).
- Magnitud en España: «no permite concluir».

## 7. PARADA
No hay.

## Respuesta a la ronda 1
- **Retirar «el comprador paga menos en total» como general. Aplicado:** ahora es un rango, de un ahorro parcial a casi ninguno.
- **Separar temporales y permanentes. Aplicado.**
- **El IC de Q6-v excluye el −0,07 alemán. Aplicado,** con las salvedades de inferencia, placebo y composición de las compraventas.
- **Escenario V71-S1-f1 como apoyo (circular). Retirado:** su signo lo fija la fórmula de incidencia, como dice la 1.0.
- **Montalvo, Piolatto y Raya como evidencia española parcial. Aplicado.**
- **Búsqueda de cambios posteriores a 2016. Ampliada:** dos búsquedas más. No hay evaluación; se citan Andalucía 2021 y la Comunitat Valenciana 2026 como cambios sin evaluar, localizados solo por prensa.
