Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · itp_discurso

## 1. Texto auditado
«Bajar el ITP abarata la vivienda»: no evaluable en España.

En lo publicado: informe integral III.4 («No evaluable con los datos disponibles») y VII.8; verificador.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** No hay evaluación española con diseño de un cambio autonómico del ITP.
- La búsqueda de V16 (ficha L4) dio solo trabajos jurídicos, DSGE (Mora-Sanguinetti y Rubio, 2014) y evasión (Montalvo, Piolatto y Raya, 2020).
- La de esta auditoría, en español e inglés (2026-10-19), dio solo guías fiscales y prensa.
- El diseño propio (Q6 de V16) no informa:
  - Q6-p (valor tasado): −0,0020 log por punto de tipo, IC95 convencional [−0,032; 0,028], p = 0,886. El contraste por aleatorización rechaza un 7,8 % de las veces bajo la nula (output/v17/lectura_bde/v15_v16_micro/inferencia.csv).
  - Hay 8 CCAA y 14 cambios de tipo concentrados en 2012-2013.

**En contra (la frase es demasiado prudente).** «No evaluable en España» deja entender que no se sabe nada, y la literatura internacional con diseño creíble es bastante coherente:
- **Volumen.** Las compraventas responden al impuesto. Subidas permanentes: −7 % por punto en Alemania (Fritzsche y Vandrei, 2019) y −14 % con un tipo medio del 1,1 % en Toronto (Dachis, Duranton y Turner, 2012). Rebajas temporales: +8 % en Reino Unido (Besley, Meads y Surico, 2014) y +20 % (Best y Kleven, 2018).
- **Precio antes de impuestos.** La incidencia recae sobre todo en el vendedor:
  - Toronto: el precio cae casi tanto como el impuesto.
  - Alemania: −3 % por punto a 12 meses, más que la carga del comprador (Dolls et al., 2025).
  - Australia: el vendedor soporta la carga (Davidoff y Leigh, 2013).
  - Nueva York y Nueva Jersey: la incidencia en el umbral recae en el vendedor (Kopczuk y Munroe, 2015).
  - Reino Unido: con un recorte medio de unas 1.500 libras, el precio después de impuestos baja unas 900. El comprador se queda con unos 3/5 (Besley et al., 2014).
- Lectura: una rebaja del ITP tiende a subir el precio de mercado antes de impuestos y a repartir la rebaja entre comprador y vendedor. «Abarata la vivienda» es falso para el precio y solo parcialmente cierto para el coste total del comprador.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Potencia de Q6.** Efecto mínimo detectable al 80 % de potencia (5 % bilateral):
  - Q6-p: 0,043 log por punto (V17-AUD-OT-ITP-Q6-p-MDE80). Es más de 4 veces la incidencia plena en el vendedor (−0,01 por punto) y mayor que el −0,03 de Dolls et al.
  - Conclusión: el diseño español no puede distinguir entre incidencia nula, plena o superior al 100 %.
  - Q6-v (compraventas): efecto mínimo detectable de 0,057 log por punto (V17-AUD-OT-ITP-Q6-v-MDE80). Está por debajo del −0,07 de Alemania, pero el punto es de signo contrario (+0,025) y el placebo falla.
  - «No evaluable con nuestros datos» se sostiene.
- No se calcula ningún efecto nuevo.

## 4. Literatura (fichas en docs/v16/literatura/L4_fiscalidad_compra.md)
Todas son VERIFICADA (DOI en Crossref; cuartil no verificado) y se leyeron solo en resumen, salvo Dachis et al.:
- Besley, Meads y Surico (2014), 10.1016/j.jpubeco.2014.07.005.
- Best y Kleven (2018), 10.1093/restud/rdx032.
- Dachis, Duranton y Turner (2012), 10.1093/jeg/lbr007. Texto parcial del documento de trabajo, págs. 1-4 y 16-21.
- Dolls, Fuest, Krolage y Neumeier (2025), 10.1016/j.jue.2024.103717.
- Fritzsche y Vandrei (2019), 10.1016/j.regsciurbeco.2018.08.005.
- Kopczuk y Munroe (2015), 10.1257/pol.20130361.
- Davidoff y Leigh (2013), 10.1111/1475-4932.12056.
- Slemrod, Weber y Shan (2017), 10.1016/j.jue.2017.05.005. Es la discrepancia: no hallan efecto de bloqueo lejos de las muescas.

Validez externa:
- El ITP español (6-13 % según la CCAA, sin verificar en esta auditoría) es mucho mayor que los impuestos estudiados (1-4 %). La respuesta puede no ser lineal.
- El ITP grava solo la segunda mano; la obra nueva paga IVA y AJD.
- Petkova y Weichenrieder (NO VERIFICADA) no hallan efecto en el precio de las casas unifamiliares alemanas.

## 5. Veredicto
**Se sostiene con matices.** Como afirmación sobre la evidencia española es cierta: no hay evaluación española y el diseño propio no tiene potencia. Pero es incompleta de un modo que puede confundir. La literatura internacional con diseño indica que una rebaja no baja el precio de mercado (tiende a subirlo antes de impuestos), que solo una parte llega al comprador y que sí aumenta las compraventas.

## 6. Texto corregido y confianza
«Bajar el ITP abarata la vivienda»: en España no se ha medido. Fuera, con diseños creíbles, una rebaja aumenta las compraventas, pero no baja el precio: parte de la rebaja se la queda el vendedor. El comprador paga menos en total, pero menos de lo que se rebaja el impuesto.

Confianza:
- «La evidencia sugiere» (literatura de otros países con tipos menores, leída en resumen).
- «No permite concluir» la magnitud en España.

## 7. PARADA
No hay. La conclusión de la 1.0 y del informe integral («no evaluable») no es falsa.
