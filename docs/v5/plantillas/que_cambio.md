# Qué cambió entre versiones y por qué (sección única, versión de referencia v7.1)

**Borja Romero, economista.** Esta es la única sección del proyecto sobre los cambios entre versiones. Los demás entregables remiten aquí. El detalle, conclusión por conclusión, está en el historial de conclusiones (`docs/v6_1/historial_conclusiones.md`). Los errores que cambiaron una cifra publicada están en la fe de erratas (ERRATA.md). Solo es citable la versión de referencia: hoy, la v7.1.

**Cómo leer esta página.** Un cambio de cifra o de lectura entre versiones casi nunca es una contradicción. Se debe a una de cuatro razones:
- se incorporó una fuente;
- cambió la muestra o la medida;
- se corrigió un error;
- se aplicó un criterio más exigente.

En cada caso se dice cuál fue la razón.

## De la primera versión a la v5: de asociaciones a capas de evidencia

- **Escala de capas.** Las primeras versiones estimaban asociaciones con datos nacionales, por comunidad y por provincia, y las rotulaban como exploratorias. Desde la v3 rige la escala de capas: [C1] hecho con dos fuentes, [C2] cota con supuestos, [C3] efecto identificado (ninguno alcanzado) y [C4] exploratorio. Varias lecturas de la primera versión (inmigración, empleo, tipos) pasaron a «no concluyente» al exigir pretendencias, placebos y validación sellada. No cambió el dato, cambió el estándar.
- **Necesidad de vivienda.** La v5 sustituyó un supuesto de bajas del parque por bajas estimadas (v5.1) y recalculó la necesidad 2026-2035 sin restar las viviendas liberadas por envejecimiento, porque la proyección de hogares del INE ya las descuenta. La necesidad anual quedó en {{T3-H5b:rango}} [C4].

## v6 y v6.1: predicción frente a explicación, y líneas base más exigentes

- [C4] **Modelos.** La v6 añadió modelos de predicción con una validación sellada nueva. La v6.1 exigió batir a la línea base más exigente. La ventaja predictiva se mantiene en {{K1-N-MEJOR:num}} de las {{K1-N-TAREAS:valor}} y desaparece en el precio municipal, con Registradores y en el volumen anual. Predecir no es explicar: ninguna variable es «relevante con seguridad».
- [C4] **Inmigración.** La v2 la asociaba más con el alquiler y la v6 con la compra. El orden depende del método, de la medida de alquiler y de los controles, no de un resultado estable que se haya invertido.
  - **Asociación total** (sin controlar por población; la inmigración es un componente contable del crecimiento de la población según la Estadística de Migraciones del INE):
    - con valor tasado, {{K2-CUOTA-COMPRA-SINPOB-SIN}}; con controles de costa y demanda externa, {{K2-CUOTA-COMPRA-SINPOB-EXT}};
    - en el alquiler de stock, {{K2-CUOTA-ALQ-SINPOB-SIN}}; con demanda externa, {{K2-CUOTA-ALQ-SINPOB-EXT}}.
  - **Asociación directa** (a igual población): compra, {{K2-CUOTA-COMPRA-SIN}}; alquiler, {{K2-CUOTA-ALQ-NUCLEO-SIN}}.
  - **Por qué ninguna de las dos basta.** La población crece en buena parte por la propia inmigración, así que controlar por ella es un mal control. La asociación total puede recoger otros factores ligados al crecimiento de la población (empleo, costa, demanda externa).
  - El signo negativo en compra no significa que la inmigración abarate la vivienda. Solo indica que, a igual población, más cuota de extranjeros no se asocia con más precio.
  - «ANALIZADA, NO CONCLUYENTE» [C4]: ninguna de las dos lecturas identifica un efecto.
- [C4] **Iniciadas y alquiler.** La asociación es del mismo año. No hay orden temporal detectable, y no indica que construir suba el alquiler.
- [C4] **Otras conclusiones que cambiaron.** Empleo, renta, iniciadas y turísticos cambian de signo o de mercado según la medida, el método y los controles. Ningún intervalo de la especificación final excluye el cero (`output/v6_1/K2/otros_cambios.md`). La correlación entre cuota de extranjeros y población dentro de cada provincia es {{K2-CORR-POB-DENTRO:num}}; las islas no se pueden contrastar porque están en la muestra sellada.
- [C4] **Ratio precio/alquiler.** Según la medida de precio, va de {{K3-RATIO-2015:rango}} en 2015 a {{K3-RATIO-2023:rango}} en 2023 (provincias de entrenamiento).
- **Correcciones** (ERRATA.md). Los contratos nuevos de la Comunitat Valenciana pasan a {{A23-A10:valor}} ({{A23-A10:rango}}) por un error de ponderación del peso de Valencia. También se corrigieron el redondeo de los recuentos de más de un millón, las fianzas de Incasòl (solo un descriptivo) y la descripción de las fuentes del déficit. Ninguna conclusión cambia.

## v6.2 y v6.3: el déficit pasa de hecho a cota, y propagación de correcciones

- [C2] **Déficit 2021-2024 sin bajas.** Se probaron siete correcciones del salto de la EPA en 2021 y dos fuentes de viviendas terminadas. El rango quedó en {{L3-DEF-2124-SINBAJAS:rango}}. Como su amplitud supera la tolerancia de un hecho [C1], pasó a cota [C2]. El signo se mantiene en todas las variantes. Sin las dos correcciones que conservan el salto, el rango es {{L3-DEF-2124-SENS:rango}}.
- **v6.3.** Propagó a la política por territorio la necesidad recalculada en v5.1 y corrigió pendientes de redacción. Las cifras afectadas están en ERRATA.md.

## v7: atlas econométrico regional

- [C4] **Componente común.** La variación interanual de cada comunidad acompaña en gran medida a la media de las 17: el R² mediano es {{V71-S3-comun-r2-compra:valor}} en compra y {{V71-S3-comun-r2-alquiler:valor}} en alquiler. Es una descripción, no un modelo. Con un componente común así, ningún estimador de panel regional es fiable en la simulación (nota metodológica).
- [C4] **Sin largo plazo regional confirmado.** Se confirman {{V71-S3-largo-confirmadas:num}} de las siete hipótesis pre-registradas. Esto confirma, con otra herramienta, que en v1 y v6 no había variables «relevantes con seguridad». No prueba que esas relaciones no existan: el panel no permite separarlas del componente común.
- [C4] **Predicción regional.** El mejor modelo por comunidad bate a la base más exigente en {{V71-S3-R5-exigente-alquiler:num}} de 17 comunidades en alquiler y en {{V71-S3-R5-exigente-compra:num}} de 17 en compra, con selección en muestra. Matiza la v6.1. La validación limpia es diferida (2026T3-2027T2).
- [C4] **Ayudas a la demanda y rebaja de ITP/IVA.** En la simulación de traslado, reducen el precio neto que paga el beneficiario, pero suben el precio de mercado: un {{V71-S3-R6-e_ayuda_demanda-compra-precio10a:valor}} y un {{V71-S3-R6-f1_rebaja_ITP_IVA_vivienda_nueva-compra-precio10a:valor}} a diez años (mediana entre comunidades). El signo lo fija en gran parte la fórmula de incidencia. Lo informativo son las magnitudes relativas.

## v7.1: dosis, coste y versión de referencia

- [C4] **Dosis y coste.** Cada instrumento simulado declara a qué cantidad se aplica, a qué horizonte y, cuando hay base, su coste fiscal aproximado:
  - Coste anual mediano por comunidad: ayudas a la demanda, {{V71-S1-e_ayuda_demanda-compra-coste_anual_meur:valor}}; rebaja de ITP/IVA, {{V71-S1-f1_rebaja_ITP_IVA_vivienda_nueva-compra-coste_anual_meur:valor}}; rebaja de impuestos y costes de construcción, {{V71-S1-f2_impuestos_construccion-compra-coste_anual_meur:valor}}. El efecto por euro de esta última está sobrestimado por construcción del escenario: no debe leerse como el instrumento más eficiente por euro.
  - Construcción, vacías, vivienda pública y turísticos: coste no estimable (no hay coste unitario verificado). Tampoco lo es el de las ayudas al alquiler.
  - Los instrumentos de cantidad se comparan por su efecto por cada diez mil viviendas. En compra es {{V71-S1-b_vacias-compra-efecto_10k:valor}} en vacías, vivienda pública y turísticos (igual por construcción de la fórmula) y {{V71-S1-a_construccion-compra-efecto_10k:valor}} en construcción adicional (mediana entre comunidades).
- **Versión de referencia.** La v7.1 reúne todo lo vigente en publicacion/. La v6.2 pasa a histórica (historico/INDICE.md). No se añadió ningún análisis: solo ordenación, dosis y coste, y la nota metodológica.
