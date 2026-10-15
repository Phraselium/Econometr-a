<!-- Generado por `make publicacion` desde output/v9/verificador_v9.md. No editar a mano: se regenera y un test lo comprueba. -->

# Verificador V9 · qué causa qué

Borja Romero, economista (firma individual, independiente). Generado por src/v9/f5_verificador.py; cifras de output/v5/cifras_clave.csv (ids «V9-…»). El veredicto se refiere a la afirmación, nunca a quién la hace. Ningún resultado de V9 alcanza C3/C3s: no hay lectura causal.

## V9-V1 · Pisos turísticos

**Afirmación.** Los pisos turísticos han encarecido el alquiler.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** Cataluña (D2, exploratorio): por cada desviación típica más de plazas turísticas por habitante en 2019, la renta de los contratos nuevos varió 0,22 % en 2020-2021 (IC [−0,55; 0,99]) y 1,05 % en 2022-2025 (IC [0,39; 1,70]), respecto a 2019. Las pretendencias se rechazan (p < 0,001): la asociación de la reapertura no se puede separar de tendencias previas. Comunitat Valenciana (D3, descriptivo): coeficiente de −0,20 % en la fianza media 2024→2025 por cada variación de +1 VUT registrada por 100 viviendas (IC [−0,41; 0,02]); como el registro cayó, una caída mayor se asocia con una fianza media algo mayor, y el placebo 2021→2023 muestra una asociación del mismo signo, de modo que no se separa de diferencias previas entre códigos postales.

**Intervalo.** IC 95 % con bootstrap salvaje por municipio (D2) y errores de Conley a 10 km (D3).

**Literatura.** Garcia-López et al. (2020, LA01, VERIFICADA, Q1): +1,9 % en el barrio medio de Barcelona; unidades no comparables. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Sin diseño que supere sus pruebas; dosis municipal, no por barrio; D3 compara un resultado anterior a la mayor parte de la caída del registro.

**Evidencia.** `output/v9/d2/tabla_d2.csv`, `output/v9/d3/tabla_d3.csv`, `output/v9/f3/tabla_revista.md`

## V9-V2 · Topes de renta (Ley catalana 11/2020)

**Afirmación.** Los topes de renta de la Ley catalana 11/2020 redujeron la renta de los contratos nuevos.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** D1b (confirmatoria): ATT −5,9 % (IC [−7,3; −4,4]), p de Holm < 0,001; pretendencias p 0,282, placebo de fecha p 0,408. No supera la prueba de Honest DiD con M̄ = 1 (M̄ de ruptura 0,5), exigida en el pre-registro: queda en C4. Contratos nuevos: −1,3 % (IC [−7,0; 4,4]), sin diferencia detectable.

**Intervalo.** IC 95 % con bootstrap multiplicador por municipio; p de Holm en la familia confirmatoria {H1a-renta, H1b-renta}.

**Literatura.** Jofre-Monseny, Martínez-Mazza y Segú (2023, LB01, VERIFICADA, Q1): −4 % a −6 % en la renta y sin caída de la oferta, con los mismos registros. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** La regla pre-registrada no se relaja tras ver el resultado; la magnitud coincide con la literatura pero la evidencia no alcanza C3.

**Evidencia.** `output/v9/d1/tabla_d1.csv`, `output/v9/d1/pruebas.csv`, `docs/v9/hipotesis_addendum_a1.md`

## V9-V3 · Zonas tensionadas (Ley 12/2023)

**Afirmación.** La declaración de zonas tensionadas ha reducido los alquileres de los contratos nuevos en Cataluña.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** D1a (confirmatoria): ATT −5,8 % (IC [−8,5; −3,2]), p de Holm < 0,001. No supera las pruebas: pretendencias p < 0,001, placebo de fecha p 0,007 y Honest DiD con M̄ = 1 incluye el 0: queda en C4. Euskadi (D1c, exploratorio, pocos trimestres): −2,5 % (IC [−3,5; −1,4]).

**Intervalo.** IC 95 % con bootstrap multiplicador por municipio; 20 municipios de control con datos completos.

**Literatura.** Fedea (Pinto 2026, LB03, sin DOI, no revisado por pares): comparación descriptiva Cataluña frente a España. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Los municipios declarados ya tenían una evolución distinta antes de 2024; con pocos controles, la comparación es frágil.

**Evidencia.** `output/v9/d1/tabla_d1.csv`, `output/v9/d1/pruebas.csv`, `output/v9/d1/fig_d1a_eventos.png`

## V9-V4 · Regulación y oferta de alquiler

**Afirmación.** La regulación de rentas ha reducido el número de contratos de alquiler.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** Zonas tensionadas (D1a, exploratorio): −6,2 % (IC [−13,2; 0,7]); Ley 11/2020 (D1b, exploratorio): −1,3 % (IC [−7,0; 4,4]). Ninguna diferencia detectable tras el ajuste de Benjamini-Hochberg.

**Intervalo.** IC 95 %; p ajustados en output/v9/f3/tabla_capas.csv.

**Literatura.** LB01 (VERIFICADA, Q1): sin caída de la oferta con la Ley 11/2020. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** El número de fianzas mide contratos registrados, no la oferta total (no observa el paso a temporada ni la economía sumergida).

**Evidencia.** `output/v9/d1/tabla_d1.csv`

## V9-V5 · Inmigración

**Afirmación.** La llegada de inmigrantes explica la subida de los alquileres y de los precios.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** D4 (réplica 2003-2012, exploratorio): 0,72 % del IPC de alquiler por punto de población extranjera (IC [−0,81; 2,26]); valor tasado −0,29 % (IC [−2,72; 2,15]). Instrumento débil: F efectiva 4,6 (umbral 23,1). Ampliación 2015-2022, valor tasado: 12,88 % (IC [−1,45; 27,21]), también con instrumento débil.

**Intervalo.** IC 95 % de 2SLS; IC de Anderson-Rubin y errores AKM en output/v9/d4/tabla_d4.csv.

**Literatura.** Saiz (2007, LA09, VERIFICADA, Q1); González y Ortega (2013, LA08, VERIFICADA, Q1); Sanchis-Guarner (2023, LA07, VERIFICADA, Q1). Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Con 50 provincias el instrumento de redes de origen es débil; la réplica usa 2003 (primer año con país) y el IPC de alquiler (parque de contratos).

**Evidencia.** `output/v9/d4/tabla_d4.csv`, `output/v9/d4/diagnosticos.csv`, `output/v9/d4/rotemberg.csv`

## V9-V6 · Tipos de interés

**Afirmación.** Las subidas de tipos del BCE abaratan más la vivienda donde las hipotecas son a tipo variable.

**Veredicto.** ANALIZADA, NO CONCLUYENTE [C4]

**Magnitud.** D5 (exploratorio, 18 países): precio a 4 trimestres −5,3 (IC [−15,6; 5,1]) y a 8 −4,4 (IC [−17,5; 8,8]) puntos log ×100 por unidad de shock y desviación típica de exposición; alquiler (IPCA) a 4 trimestres −11,7 (IC [−17,4; −6,0]).

**Intervalo.** IC 95 % Driscoll-Kraay.

**Literatura.** Koeniger, Lennartz y Ramelet (2022, LA25, VERIFICADA, Q1), cualitativo. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Sin potencia para un contraste confirmatorio; la asociación del alquiler no se mantiene a 8 trimestres en la principal.

**Evidencia.** `output/v9/d5/tabla_d5.csv`, `output/v9/d5/fig_d5.png`

## V9-V7 · Ayudas a jóvenes

**Afirmación.** El Bono Alquiler Joven ha subido los alquileres de los jóvenes.

**Veredicto.** NO EVALUABLE [C4]

**Magnitud.** No evaluable con datos públicos: la ECV no publica el mes de nacimiento (no hay edad exacta en los 35 años) y ninguna fuente identifica a los receptores (D6).

**Intervalo.** —

**Literatura.** Laguna documentada (LB23 en docs/v9_prep/literatura.csv). Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Haría falta el número de beneficiarios por edad en meses, CCAA y año (solicitud de transparencia (d)).

**Evidencia.** `docs/v9/hipotesis.md`, `docs/v9/solicitudes_transparencia.md`

## V9-V8 · Hogares y población

**Afirmación.** El aumento de hogares se debe sobre todo al crecimiento de la población.

**Veredicto.** DESCRIPTIVA (CONTABLE) [C4]

**Magnitud.** D7 (contable): en 2022-2025 el componente población supone 92 % del aumento de hogares en España (698943 hogares) y 112 % en la Comunitat Valenciana (más del 100 % significa que el componente tasa de jefatura fue negativo: menos hogares por persona). Periodo: stocks a 1-1-2022 y 1-1-2025. En 2011-2021 pesa más el componente tasa de jefatura (componente población 14 % en España). Censo 2021 y ECP coinciden en 1,5 % [C1].

**Intervalo.** Descomposición exacta (identidad); sin intervalo.

**Literatura.** Banco de España (LA18) y OCDE (LA21, NO VERIFICADA) para el déficit: output/v9/d7/reconciliacion_deficit.csv. Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila).

**Límites.** Es una identidad contable, no una atribución causal; población y hogares de 2022-2025 vienen de fuentes con un año de desfase (marcado).

**Evidencia.** `output/v9/d7/descomposicion_provincia.csv`, `output/v9/d7/reconciliacion_deficit.csv`
