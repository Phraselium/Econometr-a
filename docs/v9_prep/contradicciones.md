# Contradicciones en la literatura y cómo podría resolverlas el proyecto (V9-PREP)

Fecha: 2026-10-14. Ids de [literatura.csv](literatura.csv) y de [fuentes_datos.csv](fuentes_datos.csv). Se evalúan resultados y diseños, no a sus autores ni a quienes los citan.

## 1. Topes al alquiler: ¿cae la oferta?

| Estudio | Tipo | Resultado | Datos y diseño |
|---|---|---|---|
| Jofre-Monseny, Martínez-Mazza y Segú (2023, LB01, Q1) | artículo revisado | Alquiler medio pagado −4 % a −6 %; **sin caída de la oferta** (contratos firmados, terminadas, stock activo) | Microdatos de fianzas de Cataluña; DiD municipal, ley catalana de 2020 (vigente unos 18 meses) |
| Diamond, McQuade y Qian (2019, LB02, Q1) | artículo revisado | Los propietarios afectados reducen la oferta de alquiler un **~15 %** | San Francisco, 1994; discontinuidad por año de construcción; largo plazo |
| Pinto (Fedea 2026, LB03) | think tank, descriptivo | Anuncios de alquiler **−20,5 %** en Cataluña (T1 2024-T4 2025); precio +5,7 % frente a +10,8 % en España | Anuncios de portales; comparación descriptiva; el autor lo presenta como indicio, no como estimación |
| Instituto Juan de Mariana (2026, LB33) | think tank | Caída de la oferta (no verificado) | Sin DOI; solo hipótesis |

**Por qué discrepan.**
- **Medida de la oferta.** Contratos registrados (stock activo) en LB01; anuncios de portales en LB03. Los anuncios pueden caer porque rota menos el parque (contratos más largos) sin que caiga el stock en alquiler.
- **Horizonte.** Un año y medio (LB01) frente a décadas (LB02).
- **Margen de ajuste.** Conversión a propiedad horizontal en San Francisco; en España, posible paso a temporada o habitaciones, que los datos de fianzas pueden no recoger.
- **Ley evaluada.** La ley catalana de 2020 (LB01) frente a la Ley 12/2023 y las zonas tensionadas (LB03).

**Cómo podría resolverlo el proyecto.**
- DiD escalonado con las declaraciones de zonas tensionadas, usando la fecha de cada municipio. Se hace por Callaway-Sant'Anna, Sun-Abraham y Honest DiD (metodos M01, M02 y M08) sobre las fianzas del Incasòl (F06) y SERPAVI (F04).
- Distinguir tres medidas de oferta:
  - contratos nuevos (fianzas);
  - stock (SERPAVI);
  - anuncios (privados, solo como contraste, F36).
- Contrastar si crece la temporada con las fianzas de corta duración, si la GVA o el Incasòl las desagregan.

## 2. Inversores institucionales y alquileres

| Estudio | Resultado |
|---|---|
| Banti y Phylaktis (2025, LB06, cuartil no verificado) | Flujos a REIT residenciales: **precios al alza y alquileres a la baja** (57 ciudades, 15 países) |
| Gurun et al. (2023, LB07, Q1) | Grandes propietarios unifamiliares en EE. UU.: **alquileres al alza** |
| Lee y Wylie (2024, LB09, documento de trabajo) | Inversores institucionales: **alquileres al alza** y cambio de barrio |
| Garriga, Gete y Tsouderou (2023, LB08) | Inversores pequeños y medianos: precios al alza en el tramo bajo, revertido a medio plazo |
| Banco de España DO 2432 (LA20) | En España la inversión institucional en alquiler residencial es escasa; la oferta crece en manos de particulares |

**Por qué discrepan.**
- **Tipo de inversor.** REIT multifamiliar (que construye y añade oferta) frente a compradores de vivienda unifamiliar existente (que solo cambia de manos).
- **Nivel de agregación.** Ciudad frente a código postal.
- **País.** El caso español es distinto: el peso institucional es bajo.

**Cómo podría resolverlo el proyecto.**
- La pregunta relevante para España es la de los grandes tenedores (≥5 o ≥10 viviendas, según la Ley 12/2023).
- Sin datos de propiedad no es replicable.
- Con el umbral legal de gran tenedor se podría plantear una discontinuidad (metodos, RD) si se obtuviesen datos registrales (Registradores, F26), que no son abiertos.
- Prioridad baja hasta tener datos.

## 3. Capitalización de las ayudas al alquiler

| Estudio | Resultado |
|---|---|
| Fack (2006, LB17, Q1), Francia | **78 céntimos** de alquiler por euro de ayuda |
| Kangasharju (2010, LB19, Q2), Finlandia | **60-70 céntimos** por euro |
| Gibbons y Manning (2006, LB18, Q1), Reino Unido | Recortes de la ayuda: alquileres −6 % a −11 % |
| Eerola y Lyytikäinen (2021, LB20, Q2), Finlandia | Sin discontinuidad en el alquiler pagado: **sin capitalización** |
| Eerola, Lyytikäinen, Saarimaa y Vanhapelto (2026, LB21, Q1), Finlandia | **0,036 euros** por euro (EE 0,028): capitalización prácticamente nula |

**Por qué discrepan.**
- **Diseño.** Reformas que amplían la población elegible, con equilibrio general y oferta inelástica (Francia y Reino Unido en los años noventa y dos mil), frente a escalones individuales que no cambian la demanda agregada (Finlandia).
- **Elasticidad de la oferta local.**
- **Grado de focalización.**

**Cómo podría resolverlo el proyecto.**
- El Bono Alquiler Joven tiene un corte de edad (35 años) que permite una discontinuidad de regresión por edad, o un DiD frente a hogares de 36-40 años.
- Haría falta el alquiler pagado individual: no es público. La ECV (F29) tiene alquiler pagado y edad, con muestra pequeña.
- Agregado: comparar la evolución del IPVA y SERPAVI en municipios con alta y baja proporción de jóvenes beneficiarios. Exige la estadística de beneficiarios por municipio, que no está publicada.

## 4. Inmigración y precios: ¿signo y magnitud?

- **Positivo:**
  - Saiz (2007, LA09) para alquileres en EE. UU.;
  - González y Ortega (2013, LA08) en España, 2000-2010;
  - Sanchis-Guarner (2023, LA07), en el efecto directo.
- **Negativo:**
  - Sá (2015, LA34) en el Reino Unido, por la salida de nativos;
  - Torres-Téllez y Montero-Soler (2023, LA26), en neto para España 2001-2019.
- **Por qué.**
  - **Unidad geográfica:** ciudad frente a área local. La salida de nativos dentro del mercado amortigua el efecto local.
  - **Periodo:** auge frente a crisis.
  - **Medida:** precio frente a alquiler.
  - **Instrumento:** shift-share con cuotas de 1990-2001.
- **Proyecto.**
  - V8 no identifica el efecto (instrumento débil).
  - La réplica de Sanchis-Guarner con datos 2015-2025 por provincia y municipio es el diseño 1 de plan_v9. Separaría el efecto directo del inducido, con diagnósticos de shift-share (GPSS, BHJ y AKM; metodos M09-M11) y la descomposición de M21.

## 5. Airbnb: ¿cuánto pesa?

- **Barcelona** (LA01): +1,9 % en alquileres y +4,6 % en precios en los barrios con más actividad.
- **Madrid** (LA02): +2 % en precios por cada 100 anuncios.
- **San Sebastián** (LA03): efectos mayores.
- **Nivel nacional** [B4-v3-vut-cantidad, C2]: el proyecto acota el desplazamiento en un máximo del 2,75 % del stock de alquiler.
- **Por qué no se contradicen del todo.** Son efectos locales en zonas muy turísticas frente a una cota agregada. La contradicción es de escala, no de signo.
- **Proyecto.** El diseño 2 de plan_v9 lo resolvería en València por sección, con Inside Airbnb, el INE VUT y las fianzas de la GVA.

## 6. Déficit de vivienda: ¿cuántas faltan?

- **Banco de España** (LA18): unas 750.000 en 2021-2025.
- **OCDE** (LA21): unas 600.000 en 2022-2025, sin verificar en el original.
- **Proyecto:** 706.000-735.000 en 2021-2025 según las bajas [L3-DEF-2125, T1-H10, C4].
- **Por qué discrepan.** Periodo, fuente de hogares (ECP o EPA), tratamiento de las bajas y de la vivienda protegida, y si se cuenta la emancipación retrasada. El orden de magnitud coincide.
- **Proyecto.** Una tabla de reconciliación que reproduzca las tres cifras con los mismos supuestos: barata (C4) y útil para el debate.

## 7. Crédito frente a expectativas

- **Kaplan, Mitman y Violante** (2020, LA12): el boom estadounidense se explica sobre todo por las creencias, no por el crédito.
- **Boom español:** Gimeno y Martínez-Carrascal (2010, LA33) y Martín, Moral-Benito y Schmitz (2021, LA15) sitúan el crédito en el centro.
- **Por qué discrepan.** País, estructura de la financiación (tipo variable en España) y modelo estructural frente a evidencia reducida.
- **Proyecto.** V8 no identifica ninguno de los dos: el SVAR deja crédito y tipos con signo indeterminado en 2022-2026. Separar expectativas exigiría encuestas de expectativas de precios, que en España no tienen serie larga pública.

## 8. Factor común europeo

- **Ghirelli et al.** (2023, LA22): convergencia entre ciudades españolas hasta 2009 y divergencia posterior.
- **Maynou et al.** (2021, LA23): clubes de convergencia en Europa, con el resultado sin extraer.
- **Proyecto.** V8 halla una asociación del factor español con la zona euro (r = 0,60, H8-9, C4).
- **Tensión posible.** Comovimiento con Europa y divergencia interna pueden convivir. No hay contradicción demostrada.
