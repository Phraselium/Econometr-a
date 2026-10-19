Análisis a posteriori (V17). Ficha de auditoría de la fila «topes» (D1, medida 2). Grupo regulacion_ayudas. Capa de toda cifra nueva: C4. Ninguna cifra ni capa publicada cambia.

# Medida 2 · Regular la renta de los contratos nuevos

## 1. Texto auditado

> «Regular la renta de los contratos nuevos: prometedora para el inquilino con contrato regulado. Tiene efectos secundarios documentados: contratos de temporada, menos oferta de alquiler. En Cataluña solo hay una pista de signo.»

La frase junta tres afirmaciones distintas: (a) el efecto sobre la renta del contrato regulado, (b) dos efectos secundarios «documentados» y (c) el estado de la evidencia en Cataluña. Se auditan por separado.

## 2. Mejor argumento a favor y mejor argumento en contra

**A favor.**
- (a) Dos estudios con el registro de fianzas del Incasòl, es decir, con contratos y no con anuncios, estiman para la Ley 11/2020 la misma caída de la renta: −0,049 en logaritmo. Jofre-Monseny, Martínez-Mazza y Segú (2023) dan un error estándar de 0,006 y Monràs y García-Montalvo (UPF WP 1836, tabla I) uno de 0,011. Fuente: docs/v16/literatura/L1_control_alquileres_efectos.csv, periodo 2016-2022. Nuestra V9 da lo mismo: V9-D1b-renta-att = −5,85 % (−7,35 a −4,36), C4, que supera pretendencias y placebo.
- (b) Menos oferta. Monràs y García-Montalvo hallan −0,102 en contratos nuevos (PPML; e.e. 0,034). Pérez García (2026, preprint con DOI de DataCite), sobre las zonas de 2024, halla unos −6,6 contratos por 10.000 habitantes (≈ −13 %) en los tres diseños. Nuestra H2-SDID (V15) da −14,2 % en contratos (IC Webb −19,3 a −8,7; p = 0,0001). El contraste rechaza un 9,3 % de las veces bajo la nula, así que pasa el criterio B2 (output/v17/lectura_bde/v15_v16_micro/inferencia.csv; V17-AUD-RA-TOP-H2-SDID).
- (b) Temporada. El Banco de España (DO 2432, DOI 10.53479/37872, leído en parte) documenta con datos de portales que la oferta de temporada creció un 55 % interanual a mediados de 2024. En el mismo periodo, los anuncios de alquiler residencial cayeron más de un 15 %. El documento lo atribuye a un marco regulatorio más laxo.

**En contra.**
- (b) Menos oferta: los estudios con el mismo registro no coinciden. Jofre-Monseny et al. estiman 0,001 (e.e. 0,021) en contratos firmados y 0,002 (0,007) en el stock activo. Nuestra V9-D1b-contratos-att da −1,32 % (−7,02 a 4,39). El −14 % de H2-SDID no basta: H2-CS y H2-PPML no son fiables (tamaño real del 21,6 %) y en V9-D1a se rechazan las pretendencias de contratos (p = 0,031). La lectura publicada de H2 («sin señal que se distinga del ruido previo») sigue en pie.
- (b) Temporada: no hay ninguna estimación con diseño, en España ni en la literatura leída, que atribuya al tope el paso a temporada. DO 2432 es descriptivo y su autor no identifica el efecto. Pinto (2026, Fedea, NO VERIFICADA) también es descriptivo, con anuncios. La propia ficha P6 lo dice: «Ninguna fuente leída estima el desplazamiento a alquiler de temporada con datos de contratos». Lo «documentado» es una coincidencia temporal medida con anuncios.
- (c) «Solo una pista de signo» es demasiado prudente. Describe nuestra estimación de la Ley 12/2023 (H1, con placebo y pretendencias fallidos), no la evidencia sobre Cataluña. Para la Ley 11/2020 hay dos estudios con diseño, microdatos de contratos y error estándar que coinciden en la magnitud (−4 % a −6 %). Uno está publicado en una revista con revisión por pares (RSUE).
- (a) «Para el inquilino con contrato regulado» no reparte bien el efecto. Monràs y García-Montalvo hallan subidas de la renta en el tramo bajo, por debajo de la referencia, y bajadas en el alto. Con sus coeficientes, en torno a dos quintos de la caída media es composición: −0,049 en la base frente a −0,030 con efectos fijos de vivienda (V17-AUD-RA-TOP-COMPOSICION = 38,8 %). Los autores hablan de «la mitad». Jofre-Monseny et al. hallan, en cambio, caídas parecidas en viviendas nuevas en el mercado (−0,047) y en ya alquiladas (−0,056), lo que apunta a menos composición.

## 3. Pruebas mínimas (plan, fase 3, punto 2)

Script: src/v17/f3_regulacion_ayudas.py (aritmética sobre cifras publicadas; sin red; SEED 20261010; no lee data/). Test: tests/v17/test_f3_regulacion_ayudas.py.

**3.1 Discrepancia entre Jofre-Monseny et al. y Monràs y García-Montalvo.**
- **Lo que no la explica.** La hipótesis «registro de contratos frente a anuncios» (D2) no se sostiene. Monràs y García-Montalvo también usan contratos: «more than half a million rental contracts» del Incasòl, depurados por la AHC (FRBSF WP 2023-28, sección 3, leído). D2 atribuye a ese trabajo «anuncios»: es un error de la referencia de partida.
- **Tamaño.** La distancia en contratos es 0,103 log (IC 95 % 0,025 a 0,181 suponiendo independencia; z = 2,58). Los intervalos de cada estudio solo se solapan entre −0,040 y −0,035 (V17-AUD-RA-TOP-CONTRATOS-DIF). Las muestras se solapan, así que el contraste es orientativo.
- **Causas posibles**, que son hipótesis y no comprobaciones:
  1. **Grupo de control.** Jofre-Monseny et al. usan municipios tensos que no cumplen el umbral de población. Monràs y García-Montalvo usan los no tratados, con variantes restringidas a menos de 40.000 habitantes.
  2. **Depuración.** La AHC elimina los falsos contratos de menos de 100 € (aumentos de fianza), según la nota 13 de Monràs y García-Montalvo. Eso cambia los recuentos más que las rentas.
  3. **Ventana.** Monràs y García-Montalvo llegan a junio de 2021; Jofre-Monseny et al. a 2022. Jofre-Monseny et al. documentan además una anticipación de +0,134 en las dos semanas previas: si se trata de otro modo, cambia la comparación antes y después.
  4. **Estimador y unidad.** Monràs y García-Montalvo usan PPML sobre recuentos; Jofre-Monseny et al., el logaritmo de contratos por municipio y trimestre.
  5. **Heterogeneidad por tramo.** Solo Monràs y García-Montalvo tienen el precio de referencia de cada vivienda. Hallan −36,2 % de contratos por encima de la referencia y +40,8 % por debajo, en exp(b) − 1 (V17-AUD-RA-TOP-TRAMO-ARRIBA y -ABAJO). Una media municipal puede ocultar esa recomposición.
- **Lo que sí coincide** es la renta media. El desacuerdo está en las cantidades.

**3.2 Ley 12/2023 y zonas de 2024.**
- **Estudios españoles.** Pérez García (2026) es un preprint: renta −3 puntos de crecimiento trimestral, no robusta al emparejamiento ni al DiD sintético; contratos −13 %, robusto, pero con pretendencias rechazadas. Pinto (2026, Fedea) es descriptivo con anuncios: precio +5,7 % en Cataluña frente a +10,8 % en España, y anuncios −20,5 % frente a −7,0 % en el resto.
- **Banco de España.** No se ha localizado ningún documento con identificación: DO 2432 es descriptivo y el Informe Anual 2025 no evalúa la norma (docs/v17/referencias/bde_informes.md).
- **Ministerio y AIReF.** No se ha localizado ninguna evaluación (búsqueda del 2026-10-19).

**3.3 Comparación con nuestras estimaciones e inferencia convencional** (inferencia.csv; todas C4):

| id | estimación | lectura convencional | tamaño real bajo la nula | publicable (B2) |
|---|---|---|---|---|
| H1-CS (renta, zonas 2024) | −7,18 % | — | 21,6 % | no fiable |
| H1-SDID (renta) | −3,64 % | — | 20,8 % | no fiable |
| H2-CS (contratos) | −4,22 % | — | 21,6 % | no fiable |
| H2-SDID (contratos) | −14,16 % | p = 0,0001; IC −19,3 a −8,7 | 9,3 % | sí |
| H2-PPML (contratos) | −9,95 % | — | 21,6 % | no fiable |
| Q1c global (compraventas, provincias) | −0,048 Δlog | p = 0,094 | 6,6 % | sí |
| Q1c sin grandes | −0,064 Δlog | p = 0,040 (Holm 0,080) | 6,6 % | sí |

Lectura: en la renta, nuestras estimaciones de 2024 no tienen inferencia fiable. En los contratos, solo un estimador de tres la tiene, y apunta a la baja, como Pérez García. Q1 mide compraventas, no alquiler. Nada de esto sube de capa.

**3.4 Temporada.** No es medible con los datos del repositorio: no hay fianzas por tipo de contrato fuera de Cataluña, y en el Incasòl no se separa la temporada. Es la laguna n.º 1 de D3-4.

## 4. Literatura

| Referencia | Estado | Lectura |
|---|---|---|
| Jofre-Monseny, Martínez-Mazza y Segú (2023), RSUE 101, 103916, DOI 10.1016/j.regsciurbeco.2023.103916 | VERIFICADA (Crossref; cuartil no verificado) | texto parcial del preprint, tablas 3 y 4 (L1, ficha 12) |
| Monràs y García-Montalvo (2023), FRBSF WP 2023-28, DOI 10.24148/wp2023-28 | VERIFICADA (Crossref) | texto parcial; en V17 se leyeron la introducción, la revisión y la sección 3 (datos) |
| Monràs y García-Montalvo (2022), UPF WP 1836 | NO VERIFICADA (sin DOI) | texto parcial, tablas I a V (L1, ficha 11) |
| Monràs y Montalvo (2025), «The Effect of Rent Controls along the ‘Excess’ Price Distribution», DOI 10.2139/ssrn.5677822; CEPR DP 20018 | VERIFICADA (Crossref) | solo el resumen de CEPR (vía buscador): subidas en el tramo bajo, bajadas en el alto, salida de oferta arriba |
| Pérez García (2026), arXiv 2602.08631, DOI 10.48550/arXiv.2602.08631 | VERIFICADA (DataCite; preprint) | texto parcial (P6) |
| Pinto (2026), Fedea Apuntes 2026/15 | NO VERIFICADA (sin DOI) | texto parcial (P6) |
| Khametshin, López Rodríguez y Pérez García (2024), Banco de España DO 2432, DOI 10.53479/37872 | VERIFICADA (Crossref) | texto parcial, pp. 27-33 (L1, ficha 14) |
| Abel, Carrer y Luque (2024) | NO VERIFICADA (sin DOI) | texto parcial; anuncios (P6) |
| Diamond, McQuade y Qian (2019), AER 109(9), DOI 10.1257/aer.20181289 | VERIFICADA | resumen (P6): menor oferta de alquiler de los arrendadores afectados en San Francisco |
| Kholodilin (2024), DOI verificado (L1) | VERIFICADA | resumen y nota del autor: recuento de signos |

Prensa (idealista/news, 2026) consultada solo para localizar originales; no se cita ninguna cifra suya.

## 5. Veredicto

**Engañosa.**
- (a) Se sostiene, con el matiz de reparto entre tramos de precio.
- (b) Exagera: «documentados» sugiere un efecto establecido. En España, «menos oferta» está en disputa entre estudios con el mismo registro, y «temporada» solo está documentada como coincidencia temporal medida con anuncios, sin diseño.
- (c) Es demasiado prudente y confunde nuestra estimación con la evidencia disponible.

## 6. Texto corregido y confianza

> «Regular la renta de los contratos nuevos: en Cataluña (Ley 11/2020) dos estudios con contratos registrados hallan una renta un 4-6 % más baja en los contratos regulados; parte de la caída es cambio de composición, y en el tramo barato la renta pudo subir. Si reduce la oferta está en disputa: un estudio halla en torno a un 10 % menos de contratos, concentrado en las viviendas caras, y otro no halla caída. El paso a alquiler de temporada coincide en el tiempo con la regulación, pero solo se ha medido con anuncios y sin diseño. Para las zonas de 2024 no hay aún evaluación robusta.»

Confianza:
- renta del contrato regulado: **la evidencia indica**;
- menos oferta: **la evidencia es compatible con** una caída concentrada en el tramo alto;
- temporada: **la evidencia no permite concluir**;
- zonas de 2024: **la evidencia no permite concluir**.

## 7. Parada

No hay parada. Ninguna de las tres afirmaciones es falsa en sentido estricto: (b) exagera y (c) es imprecisa. «Solo hay una pista de signo» sería incorrecta si se lee como el estado de la evidencia sobre Cataluña, y no como nuestra estimación de 2024. Se señala para que el autor decida la redacción.

Aviso aparte, no es una parada: la referencia de partida D2 atribuye «anuncios» a Monràs y García-Montalvo. Su sección 3 dice que usan contratos del Incasòl.
