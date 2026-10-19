Análisis a posteriori (V17). Auditoría de la fase 3, grupo «oferta_titularidad». Capa C4; no cambia ninguna cifra ni capa publicada.

# Fila D1 · itp_medida (medida 6, parte del ITP)

## 1. Texto auditado
6. Vivienda pública e ITP: sin evidencia en España. (Esta ficha audita solo la parte del ITP; la de vivienda pública está en `vivienda_publica.md`.)

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.** Es cierto que no hay estudio español con diseño (ficha L4; búsqueda propia del 2026-10-19 sin resultados académicos). Q6 de V16 no tiene potencia: el efecto mínimo detectable en el valor tasado es de 0,043 log por punto, frente al −0,01 de incidencia plena (V17-AUD-OT-ITP-Q6-p-MDE80).

**En contra.**
- **La medida está mal agrupada.** Poner el ITP en la misma línea que la vivienda pública, al final de una lista «ordenada por solidez», mezcla dos instrumentos sin relación de mecanismo. Además sugiere que el ITP es tan poco conocido como la vivienda pública en España.
- **«Sin evidencia» describe mal la literatura.** Para el objetivo declarado en el informe integral (III.4: «abaratar el acceso a la compra»), la literatura con diseño sí tiene evidencia, aunque de otros países. Va en contra de que baje el precio y a favor de una traslación parcial al comprador (Dachis et al., 2012; Besley et al., 2014; Dolls et al., 2025; Kopczuk y Munroe, 2015; Davidoff y Leigh, 2013). También indica más compraventas y más movilidad (Best y Kleven, 2018; Hilber y Lyytikäinen, 2017; Fritzsche y Vandrei, 2019).
- **La regla de umbral del catálogo no pide estudios españoles.** Con su escala (III.1), la parte de volumen sería «prometedora». La parte del precio de mercado estaría entre «sin evidencia» (por las discrepancias: Petkova y Weichenrieder; Slemrod et al.) y una evidencia que va contra el abaratamiento del precio antes de impuestos.
- **El escenario de la 1.0 apunta en el mismo sentido.** El precio de mercado sube 1,4 puntos % por cada 100 M€ anuales (V71-S1-f1, [C4]). La 1.0 avisa de que ese signo lo fija en gran parte la fórmula de incidencia.

## 3. Pruebas mínimas (src/v17/f3_oferta_titularidad.py)
- Potencia de Q6-p y Q6-v (V17-AUD-OT-ITP-Q6-p-MDE80 y -Q6-v-MDE80).
- Inferencia convencional: output/v17/lectura_bde/v15_v16_micro/inferencia.csv.
  - Q6-p: p = 0,886.
  - Q6-v: p = 0,218.
  - Tamaño real del 7,8 %, publicable según B2. La herramienta figura NO APTA en su Monte Carlo.
- No se estima nada nuevo.

## 4. Literatura
Las mismas referencias VERIFICADAS de `itp_discurso.md` (ficha L4), leídas en resumen salvo Dachis et al. (texto parcial). Una más:
- **Hilber y Lyytikäinen (2017)**, 10.1016/j.jue.2017.06.002, VERIFICADA, resumen. Menos movilidad ligada a la vivienda con tipos más altos.

No hay referencia española con diseño.

## 5. Veredicto
**Se sostiene con matices.** «Sin evidencia en España» es literalmente cierto. Pero hay que corregir dos cosas:
- La agrupación con la vivienda pública, que no comparte mecanismo.
- La lectura de la literatura. Hay evidencia internacional con diseño sobre el volumen (a favor) y sobre el precio (en contra de que baje).

## 6. Texto corregido y confianza
6b. Rebajar el ITP: no evaluado en España. Fuera, con diseños creíbles, aumenta las compraventas y la movilidad. No baja el precio de mercado, porque parte de la rebaja se la queda el vendedor, y el comprador ahorra menos que la rebaja. Cuesta recaudación autonómica.

Confianza:
- Volumen: «la evidencia sugiere».
- Precio: «la evidencia es compatible con» una traslación parcial al vendedor.
- Magnitud en España: «no permite concluir».

## 7. PARADA
No hay.
