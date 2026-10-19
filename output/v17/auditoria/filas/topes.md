Análisis a posteriori (V17). Ficha de auditoría de la fila «topes» (D1, medida 2). Grupo regulacion_ayudas. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia. Versión tras la ronda 1 del abogado del diablo (sección 8).

# Medida 2 · Regular la renta de los contratos nuevos

## 1. Texto auditado

> «Regular la renta de los contratos nuevos: prometedora para el inquilino con contrato regulado. Tiene efectos secundarios documentados: contratos de temporada, menos oferta de alquiler. En Cataluña solo hay una pista de signo.»

La frase junta tres afirmaciones, que se auditan por separado:
- (a) el efecto sobre la renta del contrato regulado;
- (b) dos efectos secundarios «documentados»;
- (c) el estado de la evidencia en Cataluña.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**

- **(a) La renta del contrato regulado baja.** Dos estudios con el registro de fianzas del Incasòl, es decir, con contratos, estiman para la Ley 11/2020 la misma caída de la renta media: −0,049 en logaritmo.
  - Jofre-Monseny, Martínez-Mazza y Segú (2023), con error estándar 0,006.
  - Monràs y García-Montalvo (UPF WP 1836, abril de 2022, tabla I), con error estándar 0,011. En la versión FRBSF 2023-28 el precio en exceso baja entre un 4 % y un 8 % (docs/v17/referencias/d2_versiones.md).
  - Nuestra V9-D1b-renta-att da −5,85 % (−7,35 a −4,36) [C4].
  - La réplica con el Incasòl de este repositorio da entre −5,1 % y −6,8 % en 24 especificaciones, todas con p de BH < 0,05 (V17-AUD-RA-TOP-INC-RENTA-RANGO). Varían el control, los vecinos, la ventana y la ponderación.
- **(b) Menos contratos nuevos.** Las estimaciones de cantidad son negativas en:
  - Monràs y García-Montalvo: PPML −0,102 (0,034) en la versión de abril de 2022; −10 % a −14 % en su introducción; en torno a −15 % en la de mayo de 2022; en torno a −10 % en la de 2023.
  - Pérez García (2026, preprint), para las zonas de 2024: en torno a −13 % de contratos, robusto a tres diseños, con pretendencias rechazadas.
  - Nuestra H2-SDID (V15): −14,2 % (IC Webb −19,3 a −8,7; tamaño real del contraste: 9,3 %; V17-AUD-RA-TOP-H2-SDID).
  - V9-D1a, para las zonas de 2024: −6,25 % (−13,2 a 0,7), con pretendencias rechazadas.
  - Con anuncios: Abel et al. (2024, NO VERIFICADA), −30 %, y Pinto (2026), descriptivo, −20,5 % en Cataluña.
- **(b) Fuera de España sí está documentada la caída de la oferta.** Diamond, McQuade y Qian (2019, San Francisco) hallan menos oferta de alquiler. En el recuento de Kholodilin (2024), 12 de 16 estudios sobre oferta tienen signo negativo.
- **(b) Temporada.** El Banco de España (DO 2432, Khametshin, López Rodríguez y Pérez García, 2024) documenta con anuncios que la oferta de temporada creció un 55 % interanual a mediados de 2024. En el mismo periodo, los anuncios de alquiler residencial cayeron más de un 15 %. El documento lo atribuye a un marco regulatorio más laxo.

**En contra.**

- **(b) Menos contratos: con contratos y para la misma ley, la evidencia discrepa.**
  - Jofre-Monseny et al. hallan 0,001 (0,021) en contratos firmados, −0,006 (0,023) en contratos terminados y 0,002 (0,007) en el stock activo. Es decir, ni salida del mercado ni menos rotación.
  - V9-D1b-contratos-att da −1,32 % (−7,02 a 4,39).
  - Nuestra descomposición (sección 3.1) no reproduce ninguna caída en 60 especificaciones.
  - Las cifras negativas españolas vienen de un estudio con contratos (Monràs y García-Montalvo), de diseños sobre las zonas de 2024 con pretendencias rechazadas (Pérez García, V9-D1a) o de anuncios (Abel et al., Pinto). Que «la mayoría» sean negativas mezcla medidas y diseños de calidad distinta.
- **(b) Temporada: no hay ninguna estimación con diseño.** No la hay en España ni en lo leído de fuera. DO 2432 y Pinto son descriptivos y usan anuncios. La ficha P6 lo dice así: «Ninguna fuente leída estima el desplazamiento a alquiler de temporada con datos de contratos».
- **(c) Demasiado prudente.** Hay dos estudios con diseño, contratos y errores estándar que coinciden en la renta. Nuestra propia V9-D1b supera pretendencias y placebo. «Solo una pista de signo» describe nuestra H1 de 2024, no la evidencia sobre Cataluña.
- **(a) «Para el inquilino con contrato regulado» no reparte bien el efecto.**
  - Monràs y García-Montalvo hallan subidas de renta en el tramo barato y bajadas en el caro. Hay +40,8 % de contratos por debajo de la referencia y −36,2 % por encima (UPF 1836, tabla IV; V17-AUD-RA-TOP-TRAMO-ABAJO y -ARRIBA).
  - En 2023 registran un incumplimiento de hasta el 74 %: el efecto es el de un tope aplicado solo en parte.
- **Matiz sobre el control de Jofre-Monseny et al.** Sus vecinos no regulados ven caer la renta la mitad que los regulados. Su control puede estar contaminado, lo que sesga hacia cero tanto la renta como las cantidades. Nuestra variante sin vecinos no cambia el resultado de cantidad (sección 3.1).

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_regulacion_ayudas.py. Lee el Incasòl de data/raw/v9 en solo lectura y filtra muestra_sellada_v6 (Cataluña no está en la muestra cerrada). Registro: output/v17/auditoria/regulacion_ayudas_registro.csv, con 84 especificaciones. Test: tests/v17/test_f3_regulacion_ayudas.py.

### 3.1 Descomposición de la discrepancia con el Incasòl del repositorio (el fichero de V9-D1b)

**Datos.** Fianzas nuevas por municipio y trimestre, 2019T1-2022T1. Es un panel equilibrado de 416 municipios con contratos en los 13 trimestres: 60 tratados por la Ley 11/2020 desde 2020T4. Se estima un DiD con efectos fijos de municipio y de trimestre, y errores agrupados por municipio.

**Dimensiones que se varían:**

| Dimensión | Variantes |
|---|---|
| Control | todos los no tratados (356); «tensos», aproximación al control de Jofre-Monseny et al. (los municipios declarados tensos en 2024 que no estaban en la Ley 11/2020; 209); cada uno con y sin vecinos a menos de 5 km de un tratado (70 vecinos) |
| Forma | log de contratos; log per cápita (padrón); PPML |
| Ponderación | sin ponderar; ponderado por los contratos previos (en PPML solo sin ponderar: ya pondera por niveles, y su versión ponderada no tiene errores agrupados fiables en statsmodels) |
| Ventana | la de V9 (hasta 2022T1); la de Monràs y García-Montalvo (hasta 2021T2); sin los trimestres de la COVID (2020T2-T3) |

**Resultado** (V17-AUD-RA-TOP-INC-*):
- **Renta media de los contratos nuevos.** 24 de 24 especificaciones son negativas, entre −5,1 % y −6,8 % (mediana −5,8 %), y todas significativas tras BH.
- **Contratos nuevos.** De 60 especificaciones, la mediana es +3,6 % y el rango va de −1,3 % a +7,6 %. Solo 5 son negativas, y ninguna con p < 0,05. Las 4 con p < 0,05 son positivas (log per cápita, ventana hasta 2021T2), y ninguna sobrevive a BH.
- **Especificación de referencia** (todos los controles, log, sin ponderar, ventana de V9): +0,9 % (−2,5 a 4,5).

**Lectura.** Con el agregado público del Incasòl, ninguna de las causas candidatas acerca el resultado a la caída de Monràs y García-Montalvo: el control (tensos), la exclusión de vecinos, PPML frente a log per cápita, la ponderación y su ventana. El agregado reproduce a Jofre-Monseny et al. Las causas que quedan solo se pueden contrastar con microdatos y quedan como hipótesis declaradas:
1. la depuración de la AHC, que elimina falsos contratos de menos de 100 €, aumentos de fianza (Monràs y García-Montalvo, nota 13);
2. su muestra y su definición de control a nivel de vivienda;
3. el reparto por tramo de precio, que solo existe en sus microdatos.

**Altas, bajas y stock (rotación frente a salida del mercado).** No se pueden separar con el repositorio. El fichero público del Incasòl solo trae fianzas nuevas (altas). Las bajas y el stock activo están solo en los microdatos que usaron Jofre-Monseny et al.: sus resultados (bajas −0,006, stock 0,002) son la única evidencia sobre ese margen.

### 3.2 Ley 12/2023 y zonas de 2024

- **Estudios españoles.**
  - Pérez García (2026, preprint): renta −3 puntos de crecimiento trimestral, no robusta al emparejamiento ni al DiD sintético; contratos en torno a −13 %, robusto, con pretendencias rechazadas.
  - Pinto (2026, Fedea): descriptivo.
  - Banco de España: DO 2432 (2024) es descriptivo, y el Informe Anual 2025 no evalúa la norma.
- **Ministerio y AIReF.** No se ha localizado ninguna evaluación (búsqueda del 2026-10-19).

### 3.3 Nuestras estimaciones con inferencia convencional

Fuente: output/v17/lectura_bde/v15_v16_micro/inferencia.csv. Todas son C4.

| id | estimación | lectura convencional | tamaño real bajo la nula | publicable (B2) |
|---|---|---|---|---|
| H1-CS (renta, zonas de 2024) | −7,18 % | — | 21,6 % | no fiable |
| H1-SDID (renta) | −3,64 % | — | 20,8 % | no fiable |
| H2-CS (contratos) | −4,22 % | — | 21,6 % | no fiable |
| H2-SDID (contratos) | −14,16 % | p = 0,0001; IC −19,3 a −8,7 | 9,3 % | sí |
| H2-PPML (contratos) | −9,95 % | — | 21,6 % | no fiable |
| Q1c global (compraventas, provincias) | −0,048 Δlog | p = 0,094 | 6,6 % | sí |
| Q1c sin grandes | −0,064 Δlog | p = 0,040 (Holm 0,080) | 6,6 % | sí |

### 3.4 Temporada

No es medible: no hay fianzas por tipo de contrato. Es la laguna n.º 1 de D3-4.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916, 10.1016/j.regsciurbeco.2023.103916 | VERIFICADA (Crossref; cuartil no verificado) | texto parcial del preprint, tablas 3 y 4 (L1) |
| Monràs y García-Montalvo, FRBSF WP 2023-28, 10.24148/wp2023-28 | VERIFICADA | texto parcial, pp. 1-20 (d2_versiones.md; en esta ficha, sección 3) |
| Monràs y García-Montalvo (abril y mayo de 2022), UPF WP 1836 y copia FRBSF | NO VERIFICADAS (sin DOI) | texto parcial (L1; d2_versiones.md) |
| Monràs y Montalvo (2025), 10.2139/ssrn.5677822; CEPR DP 20018 | VERIFICADA (Crossref) | solo el resumen de CEPR |
| Pérez García (2026), 10.48550/arXiv.2602.08631 | VERIFICADA (DataCite; preprint) | texto parcial (P6) |
| Khametshin, López Rodríguez y Pérez García (2024), BdE DO 2432, 10.53479/37872 | VERIFICADA | texto parcial (L1) |
| Pinto (2026), Fedea; Abel, Carrer y Luque (2024) | NO VERIFICADAS | texto parcial (P6) |
| Diamond, McQuade y Qian (2019), 10.1257/aer.20181289; Kholodilin (2024) | VERIFICADAS | resumen (P6, L1) |

## 5. Veredicto

**Engañosa.** Se mantiene tras la ronda 1; las razones están en la sección 8.
- (a) Se sostiene, con el matiz del reparto por tramos.
- (b) Presenta como «documentado» un efecto que en España, con contratos y para la misma ley, está en disputa (y nuestra réplica no lo encuentra). Presenta también como documentado un desplazamiento a temporada que nadie ha estimado con diseño.
- (c) Es demasiado prudente.

## 6. Texto corregido y confianza

> «Regular la renta de los contratos nuevos: en Cataluña (Ley 11/2020) dos estudios con contratos registrados hallan una renta media un 4-6 % más baja en los contratos regulados, y nuestros datos dan lo mismo; en el tramo barato la renta pudo subir. Si reduce el número de contratos nuevos está en disputa: un estudio halla en torno a un 10 % menos, concentrado en las viviendas caras, y otro, con el mismo registro, no halla caída ni en contratos ni en el stock. Para las zonas de 2024 hay indicios de menos contratos, con pruebas previas que fallan. El paso a alquiler de temporada coincide en el tiempo con la regulación, pero solo se ha medido con anuncios y sin diseño. Fuera de España, la menor oferta de alquiler sí está documentada en varios estudios.»

**Confianza:**
- renta del contrato regulado: **la evidencia indica**;
- menos contratos nuevos (Ley 11/2020): **la evidencia no permite concluir**;
- menos contratos nuevos (zonas de 2024): **la evidencia es compatible con** una caída;
- temporada: **la evidencia no permite concluir**.

## 7. Parada

No hay parada. Nada de la frase es falso en sentido estricto. Se señala la redacción de (c), y la referencia D2 que atribuía «anuncios» a Monràs y García-Montalvo: todas sus versiones usan contratos del Incasòl (docs/v17/referencias/d2_versiones.md).

## 8. Respuesta a la ronda 1

| Punto del abogado del diablo | Respuesta |
|---|---|
| Ejecutar la descomposición con el Incasòl del repositorio | **Aplicado** (sección 3.1): 60 especificaciones de cantidad y 24 de renta en el Registry. Ninguna variante reproduce la caída de contratos. |
| Separar altas, bajas y stock | **No es posible** con el repositorio: el fichero público solo trae altas. Queda como hipótesis declarada, con los resultados de Jofre-Monseny et al. como única evidencia. |
| Reconsiderar «engañosa» frente a «se sostiene con matices» | **Rebatido; se mantiene «engañosa».** La mayoría negativa mezcla anuncios, diseños con pretendencias rechazadas (2024) y un solo estudio con contratos para 2020. Con contratos y para la misma ley, un estudio publicado y nuestras 60 especificaciones no hallan caída. «Contratos de temporada» presentado como efecto documentado no tiene ningún estudio con diseño. Se acepta que fuera de España la menor oferta está documentada: se añade al texto corregido. |
| «Menos contratos nuevos» en lugar de «menos oferta» | **Aplicado.** |
| Stock nulo de Jofre-Monseny et al., control contaminado e incumplimiento de hasta el 74 % | **Aplicado** (sección 2). |
| Incluir Pérez García (2024) y H2 | **Aplicado.** Pérez García figura como coautor de DO 2432 (2024, descriptivo) y como autor del preprint de 2026 (zonas de 2024). H2-SDID está en las secciones 2 y 3.3. |
| Retirar el 38,8 % de composición | **Aplicado.** El hecho V17-AUD-RA-TOP-COMPOSICION se retira: mezclaba dos especificaciones de la versión de 2022, y la de 2023 ya no lo afirma. |
| Cifras por versión de Monràs y García-Montalvo | **Aplicado.** Cada cifra lleva su versión. |
