# Q5 · Tipos de interés: proyecciones locales sobre la sorpresa de Jarociński-Karadi (C4, pendiente de evaluación sellada)

**Capa y alcance.** C4 (asociación), entrenamiento; no pasa a C3 sin evaluación sellada temporal. Sin lenguaje causal. Herramienta de inferencia (Newey-West de b fija) NO APTA
(tamaño 0,0642-0,0925, veredictos.csv): solo estimación puntual, **sin p-valor ni IC**. La sorpresa de JK termina en 2025Q4; la ventana efectiva acaba ahí (la adenda dice 2026T2).

## Especificación (pre-registrada)
LP a h = 4: y(t+4) − y(t−1) (log x 100) sobre la sorpresa mediana de JK (suma trimestral, estandarizada), 4 rezagos del choque y de Δy. Ventanas nominales 1999T1 (Q5-p) y 2002T1 (Q5-a); muestras efectivas tras los rezagos y el horizonte: 2000Q2-2025Q2 y 2003Q2-2025Q2.
Multiverso: 64 especificaciones (4 resultados x 4 horizontes x 2 choques x 2 rezagos), en registro.csv; ninguna se elige por su resultado.

## Resultados puntuales
<a id="q5p"></a>**Q5-p (valor tasado), h = 4:** -0,51 % por DT de sorpresa (n = 101, 2000Q2-2025Q2). Respuesta puntual: h=1: -0,45; h=4: -0,51; h=8: 0,23; h=12: 2,30.
Referencia de la literatura (P3 de V15): −0,6 % por DT; cociente estimación/referencia = 0,85; mismo signo: True.
Multiverso (63 restantes): mediana 0,15, rango [-0,64; 2,30], proporción con el mismo signo 0,47.
El MDE del valor tasado a h = 4 (1,47 %) supera la referencia: sin potencia aunque la inferencia fuera válida.

<a id="q5a"></a>**Q5-a (IPC de alquiler), h = 4:** -0,06 % por DT (n = 89, 2003Q2-2025Q2). Respuesta puntual: h=1: 0,02; h=4: -0,06; h=8: -0,26; h=12: -0,30.
Sin magnitud comparable (la referencia es de precio): la condición (b) no se cumple. Multiverso: mediana -0,18, rango [-0,58; 0,02], mismo signo 0,87.

## Diagnósticos (todos reportados; ninguno decide la capa)
- Primera etapa (sorpresa → Δ tipo hipotecario BdE): h=0: -0,041 pp por DT, F robusto 2,1; h=4: -0,237 pp, F 2,9 (descriptivo). F < 10: instrumento débil en el sentido de la regla del pre-registro; **no se supera la prueba de fuerza** y se dice.
- Controles negativos (h=4): población total -0,032 %; inflación yoy -0,296 pp.
- Placebo temporal (choque adelantado 8 trimestres), heterocedasticidad (Breusch-Pagan), autocorrelación (Breusch-Godfrey) y sup-F de ruptura: en resultado.json (descriptivos).
- Oster, Cinelli-Hazlett y E-value, pretendencias, Honest DiD, Moran y exclusión de grandes ciudades: no aplican (serie nacional única, choque externo).

## Regla de hallazgo (punto 9)
(a) sin p-valor: no evaluable; (b) sin errores típicos válidos: no evaluable (Q5-a sin magnitud); (c) sellada: pendiente. Resultado: estimación puntual C4, ni hallazgo ni pista.
Los p-valores para el control BY están en resultado.json (`p_valores_para_BY`, p null por NO APTO).
