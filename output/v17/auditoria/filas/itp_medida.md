Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada. Revisada tras la ronda 1 del abogado del diablo.

# Fila D1 · itp_medida (medida 6, parte del ITP)

## 1. Texto auditado
6. Vivienda pública e ITP: sin evidencia en España. (Esta ficha audita solo la parte del ITP; la de vivienda pública está en `vivienda_publica.md`.)

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** Es cierto que no hay estudio español con diseño:
- Ficha L4 y dos búsquedas propias del 2026-10-19 sin resultados académicos. Los cambios de Andalucía (2021) y la Comunitat Valenciana (2026), localizados por prensa, no tienen evaluación.
- La única evidencia española es parcial y trata de la evasión (Montalvo, Piolatto y Raya, 2020): el tipo efectivo es menor que el nominal.
- Q6 de V16 no tiene potencia: el efecto mínimo detectable en el valor tasado es de 0,043 log por punto, frente al −0,01 de incidencia plena (V17-AUD-OT-ITP-Q6-p-MDE80).

**En contra.**
- **La medida está mal agrupada.** Poner el ITP en la misma línea que la vivienda pública, al final de una lista «ordenada por solidez», mezcla dos instrumentos sin relación de mecanismo.
- **«Sin evidencia» describe mal la literatura.** Para el objetivo declarado en el informe integral (III.4, «abaratar el acceso a la compra»), la literatura con diseño sí tiene evidencia, aunque sea de otros países:
  - Contra el abaratamiento del precio antes de impuestos en los cambios permanentes: Dachis et al., 2012; Dolls et al., 2025; Davidoff y Leigh, 2013; Kopczuk y Munroe, 2015.
  - Un ahorro del comprador que va de parcial (Besley et al., 2014, rebaja temporal) a casi nulo.
  - Más compraventas: Best y Kleven, 2018; Fritzsche y Vandrei, 2019.
  - Más movilidad ligada a la vivienda: Hilber y Lyytikäinen, 2017.
- **Con la regla de umbral del catálogo (III.1),** el volumen sería «prometedora». El precio quedaría entre «sin evidencia» (por las discrepancias: Petkova y Weichenrieder; Slemrod et al.) y una evidencia contraria al abaratamiento del precio antes de impuestos.
- **Recaudación.** En Francia, la subida de 2014 quedó en el tramo creciente de la curva de Laffer (Bérard y Trannoy, 2018; VERIFICADA, 10.24187/ecostat.2018.500t.1951; texto parcial). Una rebaja reduciría la recaudación. En un modelo calibrado para Helsinki, la curva tiene su máximo en torno al 10 % (Määttänen y Terviö, 2022; VERIFICADA, 10.1093/ej/ueab080; resumen). Con tipos españoles del 6-13 %, cuánto se pierde depende de la CCAA. No se ha estimado.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- **Potencia de Q6-p y Q6-v** (V17-AUD-OT-ITP-*-MDE80).
- **Inferencia convencional de la fase 2.** Q6-p: p = 0,886. Q6-v: p = 0,218. Tamaño real del 7,8 %; la herramienta figura NO APTA en su Monte Carlo.
- El IC de Q6-v excluye el −0,07 alemán. No se lee como evidencia en contra, por el placebo fallido y la concentración de los cambios en la crisis (véase `itp_discurso.md`).

## 4. Literatura
- Las referencias VERIFICADAS de `itp_discurso.md` (ficha L4), leídas en resumen salvo Dachis et al. (texto parcial).
- Hilber y Lyytikäinen (2017), 10.1016/j.jue.2017.06.002.
- Bérard y Trannoy (2018).
- Määttänen y Terviö (2022).
- Montalvo, Piolatto y Raya (2020), evidencia española parcial.

## 5. Veredicto
**Se sostiene con matices.** «Sin evidencia en España» es literalmente cierto. Hay que corregir dos cosas:
- La agrupación con la vivienda pública.
- La lectura de la literatura: hay evidencia internacional con diseño sobre el volumen (a favor) y sobre el precio (en contra de que baje).

## 6. Texto corregido y confianza
6b. Rebajar el ITP: no evaluado en España. Fuera, con diseños creíbles, las rebajas temporales adelantan compras. Las permanentes aumentan las compraventas y la movilidad, pero no bajan el precio de mercado. El comprador ahorra, según el mercado, desde una parte de la rebaja hasta casi nada. Reduce la recaudación donde el tipo está por debajo del máximo de ingresos.

Confianza:
- Volumen: «la evidencia sugiere».
- Precio: «la evidencia es compatible con» una traslación al vendedor de parcial a total.
- Magnitud y recaudación en España: «no permite concluir».

## 7. PARADA
No hay.

## Respuesta a la ronda 1
- **«El comprador ahorra menos que la rebaja» como general. Sustituido** por un rango: de parcial a casi nada.
- **Temporales y permanentes. Separados.**
- **IC de Q6-v. Informado,** con salvedades.
- **V71-S1-f1 retirado como apoyo:** es circular.
- **Montalvo et al. tratado como evidencia española parcial.**
- **Búsqueda posterior a 2016. Ampliada,** sin evaluaciones.
- **«Cuesta recaudación». Ahora con fuente:** Bérard y Trannoy; Määttänen y Terviö. Matizado: depende del tipo de partida.
