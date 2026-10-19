Análisis a posteriori (V17). Ficha de auditoría de la fila «burbuja» (D1, discurso político). Grupo demanda_precios. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Ids nuevos: V17-AUD-DP-BUR-*; se usan los V17-B5-* de output/v17/lectura_bde/medidas_referencia/.

# «Hay burbuja» / «no hay burbuja»

## 1. Texto auditado

> «Hay burbuja» / «no hay burbuja»: ninguna de las dos se puede afirmar; no hay exuberancia estadística.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- **Una exuberancia estadística no identifica una burbuja.** Una burbuja, en sentido estricto, es un precio que se separa de su valor fundamental por la expectativa de reventa. Ningún contraste disponible la identifica.
- **El Banco de España tampoco habla de burbuja.** Habla de desequilibrio («sobrevaloración») respecto a renta y tipos. Lo sitúa entre el 10 % y el 15 % en diciembre de 2025, «similar al registrado en 2004» y muy por debajo del máximo promedio del 24 % de finales de 2007 (IEF primavera 2026, p. 100).
- **Riesgos contenidos.** Su indicador sintético de riesgos está en niveles de 2002 (IEF 2026, p. 101) o de 2001 (IA2025, p. 122). La propia fuente advierte de una «notable incertidumbre».
- **El crédito y el apalancamiento no se parecen a 2005-2007** (V17-B5):

| Indicador | Último | 2007 |
|---|---|---|
| Crédito a hogares para vivienda, % del PIB | 30,2 % (2026-06) | 59,0 % |
| Crecimiento interanual de ese crédito | 3,7 % | 17,0 % |
| Préstamos con LTV > 80 % | 9,6 % | 14,3 % |
| Dudosidad | 1,45 % | 0,59 % (por debajo de su media de 2,66 %) |

  Compraventas por 1.000 hogares: 3,8, frente a cerca de 6 en 2006 (IEF 2026, p. 97).
- **Nuestros contrastes, tras el ajuste múltiple.** Con el GSADF corregido de V7.2 no hay ningún cociente ni nivel nacional ni comunidad con exuberancia en la familia publicada (V72-GSADF-*).

**En contra.**
- **«No hay exuberancia estadística» es una lectura de un contraste sin potencia.**
  - En el Monte Carlo de V16, el GSADF del factor común con bootstrap salvaje rechaza la alternativa explosiva simulada un 6,4 % de las veces sin saltos y un 13,2 % con saltos, para un tamaño de 1,7-4,6 % (V17-AUD-DP-BUR-GSADF-POTENCIA).
  - Con T = 78-98, no rechazar es casi lo que se espera tanto si hay exuberancia como si no.
  - La 1.0 lo dice: «la ausencia no demuestra alineación con los fundamentales» (informe integral, VII.1).
- **Sí hay rechazos sin ajuste.**
  - Precio/renta (IPV / renta del hogar): p = 0,010; 1 de 4 cocientes sin ajuste; 1 tras el ajuste en la familia de 4 (V72-GSADF-ratios-p05 y -bh4-sens).
  - Q9-g (factor común del valor tasado / IPC de alquiler): 5,9 frente a un valor crítico de 3,3, p = 0,004. Queda q = 0,306 tras Benjamini-Yekutieli con m = 21.
  - «No hay» resume como ausencia lo que es «no sobrevive al ajuste».
- **Los indicadores de valoración del Banco de España apuntan a precios altos frente a renta y alquiler, y en aumento.**
  - Precio/renta bruta por hogar: 8,36 años en junio de 2026, un 38 % por encima de su media de 1987-2025 (6,04) y un 11 % por debajo de 2007 (9,36) (V17-AUD-DP-BUR-PRECIO-RENTA-FRENTE-2007).
  - Rentabilidad bruta del alquiler: 2,84 %, un 39 % por debajo de su media (4,69 %) y ya en el nivel de 2007 (2,94 %).
  - El desequilibrio estimado pasó del 0,8-4,8 % (junio de 2024) al 10-15 % (diciembre de 2025).
- **El crédito nuevo se acelera.** Nuevo crédito hipotecario +22,4 % interanual en 2025T4; LTP > 80 % en el 43,8 % de la nueva producción, frente al 39,2 % a comienzos de 2024 (IEF 2026, pp. 101-103).

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_demanda_precios.py (lee output/v16/montecarlo/gsadf_factor/resultado.json y output/v17/lectura_bde/medidas_referencia/medidas.csv).

**3.1 Indicadores de sobrevaloración del Banco de España, con valores.**

| Indicador | Valor | Referencia | Fuente |
|---|---|---|---|
| Desequilibrio del precio respecto a renta y tipos (rango de 4 métodos) | 10-15 % (dic. 2025) | 5,3-12,7 % (jun. 2025); 3,0-9,4 % (dic. 2024); máximo promedio 24 % (2007) | IEF primavera 2026, p. 100; IEF otoño 2025, p. 96 |
| Indicador sintético de riesgos | nivel de 2002 | > 0,6 en el auge; ≈ 0,9 en 2007 | IEF 2026, p. 101; IA2023, p. 256 |
| Precio / renta bruta por hogar | 8,36 años (+38 % sobre la media) | 9,36 en 2007 | V17-B5-PRECIO-RENTA |
| Rentabilidad bruta por alquiler | 2,84 % (−39 % frente a la media) | 2,94 % en 2007 | V17-B5-RENTABILIDAD-ALQUILER |
| Precio real frente al máximo de 2007 | −14,7 % (2025T4) | — | IEF 2026, p. 98 |

**3.2 Potencia del GSADF con nuestra muestra.**
- **Factor común** (V16, T = 98, R = 2.000): potencia 0,064 sin saltos y 0,132 con saltos.
- **Serie nacional** (v5, R1B-G-tam, T = 78): con valores críticos iid, el tamaño real es del 15 % si Δy es AR(1) con φ = 0,5. Con bootstrap AR, del 4 % (R1B-G-tam-corr).
- **Lectura.** El contraste corregido controla el tamaño, pero apenas tiene potencia. Un «no rechaza» no es evidencia de ausencia.

**3.3 Crédito y apalancamiento frente a 2005-2007.** Saldo de crédito para vivienda: 28,8 puntos de PIB menos que en 2007 (V17-AUD-DP-BUR-CREDITO-FRENTE-2007). LTV medio de transacción del 63,7 %, igual que en 2007 (63,5 %); préstamos con LTV > 80 % por debajo (9,6 % frente a 14,3 %). Lectura del Banco de España: los riesgos para la estabilidad financiera son contenidos; la tensión está en la valoración frente a la renta, no en el crédito.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Phillips, Shi y Yu (2015), International Economic Review 56(4), DOI 10.1111/iere.12132 | VERIFICADA (Crossref, 2026-10-19; cuartil no verificado) | resumen (método del GSADF) |
| Alves, Broto, Gil y Lamas (2023), BdE DO 2314, DOI 10.53479/33154 | VERIFICADA (Crossref) | resumen e índice |
| Banco de España, IEF primavera 2026, otoño 2025 y primavera 2025 (cap. 4); IA2023 (cap. 4); IA2025 (cap. 2) | NO VERIFICADA (sin DOI) | páginas citadas (docs/v17/referencias/bde_informes.md) |
| BCE, Financial Stability Review nov. 2023 (artículo especial) y Boletín Económico 2/2025 | NO VERIFICADA (sin DOI) | conversor |

## 5. Veredicto

**Engañosa.**
- La primera mitad se sostiene: no se puede afirmar «hay burbuja» ni «no hay burbuja», y el Banco de España tampoco lo hace.
- La segunda mitad, «no hay exuberancia estadística», presenta como hecho la falta de rechazo de un contraste con potencia del 6-13 %. Omite que hay rechazos sin ajuste.
- La frase calla lo que sí se puede afirmar con los indicadores del Banco de España: una sobrevaloración moderada y creciente frente a la renta, sin el desequilibrio de crédito de 2007.

## 6. Texto corregido y confianza

> «Hay burbuja» / «no hay burbuja»: ninguna de las dos se puede afirmar, porque no hay forma de identificar una burbuja con estos datos. Lo que sí se puede decir, con los indicadores del Banco de España, es otra cosa. A finales de 2025 el precio estaba entre un 10 % y un 15 % por encima de lo que justifican la renta y los tipos. Es un nivel parecido al de 2004, lejos del 24 % de 2007, y va en aumento. A diferencia de 2007, el crédito no se ha disparado: es el 30 % del PIB, frente al 59 %. Nuestros contrastes de exuberancia no dan señal tras corregir por pruebas múltiples, pero apenas tienen potencia, así que eso no prueba que no la haya.

Confianza:
- sobrevaloración moderada frente a la renta: **la evidencia sugiere** (rango entre métodos del Banco de España; los métodos no incluyen la oferta);
- crédito lejos de 2007: **la evidencia indica**;
- burbuja (sí o no): **la evidencia no permite concluir**.

## 7. Parada

No hay parada. La 1.0 (informe integral, VII.1; lo_que_sabemos.md) dice que ninguna de las dos se puede afirmar. También dice que «la ausencia tampoco la descarta» y que el contraste tiene poca potencia. La paráfrasis de D1, «no hay exuberancia estadística», es más tajante que la 1.0 y no figura en publicacion/. Se señala al autor.
