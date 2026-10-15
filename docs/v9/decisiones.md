# Decisiones V9 COMPLETO (datos, modelización local e integración en la web)

Rama local `r9/main`, subida a la rama remota designada (`claude/housing-price-spain-econometric-95dhj3`), la única a la que se puede subir (CLAUDE.md). Las decisiones de la descarga de datos de V9 siguen en docs/v9/decisiones_datos.md (D0-D7). Referencias: v8.1 para resultados y V10 para base y web.

## E0 — Correcciones de la web de V10 (F0)
- **Sobrecarga en alquiler** (V10-ATL-A1 y A3; 38,1 % → 26,8 %, 2018-2025). El atlas y la página «Quién soporta el coste» explican tres cosas para que no se lea como «el problema mejora»:
  - la ECV mide a todos los inquilinos, sobre todo con contratos antiguos;
  - la renta es la del año anterior;
  - el periodo coincide con subidas salariales.
  - Al lado se ponen las cifras C1 de contratos nuevos: A23-A10, Comunitat Valenciana 28,5 % (2021-2024); A23-A9, Cataluña 16,9 %.
- **Brecha del IPVA** (V10-ATL-B1). Se presenta como «diferencia de puntos de índice (base 2015)» y se aclara explícitamente que no es un porcentaje de encarecimiento.
- **València +39,8 % (2019-2024)**: «C4, fuente única (SERPAVI)» en el atlas, la figura F10, las fichas municipales (nueva fila de variación del alquiler) y los mapas.
- **Cifras.** Ninguna cambia: solo cambia el texto. `make web` y `make check` (rc = 0).

## E1 — F1: datos (detalle en decisiones_datos.md, D8)
- **Prioridad.** Primero las fuentes que necesitan D1-D7. Lo que ningún diseño usa queda aplazado y documentado (auditoria_exhaustividad.md).
- **Exposición de D5.** Los volúmenes por fijación no existen por país, así que se usa la cuota RAI (BCE).
- **Accesibilidad de D3.** Se mide como distancia al centro, sin GTFS.

## E2 — F2: potencia antes de estimar
- **Método.** El MDE sale de placebos entre nunca tratados (DiD) o de permutaciones de la exposición (dosis, diferencias largas, shift-share, proyecciones locales). Nunca se usa la relación tratamiento-resultado de los tratados.
- **Regla.** Una hipótesis es confirmatoria si su MDE con Holm ≤ la referencia de la literatura.
- **Resultado.**
  - Confirmatorias: D1a (renta y contratos), D1b (renta), D2 (renta, COVID y reapertura) y D4 (IPC de alquiler en la réplica).
  - Exploratorias: el resto.
  - Descriptivo: D3.
  - D6 no se estima: la ECV no tiene mes de nacimiento.
- **Datos de los paneles.**
  - Incasòl: los municipios solo tienen datos anuales antes de 2019. D1b usa la ventana trimestral 2019T1-2022T1, con robustez anual; D2 usa el panel anual 2014-2025.
  - Precios de D5: BIS nominal (18 países). El fichero de prc_hpi_q del proyecto solo tenía 6.
  - Valor tasado de D4: panel provincial de v7 (código INE). Las CCAA uniprovinciales se completan con el panel anual de CCAA (código INE de CCAA → provincia, tabla fija).
- **Referencia de D5.** Es un orden de magnitud NO VERIFICADO (5 % por punto de shock y DE de exposición). Aun con esa referencia generosa el diseño no tiene potencia, así que es exploratorio.

## E3 — Revisión de F2 (REHACER 1 de 2) y addendum A1 (2026-10-15, antes de estimar)
- **Respuesta.** docs/v9/revision_f2.md se responde con docs/v9/hipotesis_addendum_a1.md (etiqueta local `prereg-v9-a1`), con potencia recalculada en src/v9/f2b_potencia_addendum.py.
- **Desviaciones respecto de prereg-v9:**
  1. el conjunto confirmatorio queda en {H1a-renta, H1b-renta}; H1a-contratos, H2 y H4 pasan a exploratorias;
  2. la prueba 4 de D1 pasa a ser una permutación de etiquetas con umbral 0,05, obligatoria para C3;
  3. D3 usa 2025 como año final, la cuota provincial como resultado y una excepción declarada para la exposición;
  4. F4 queda limitada a C3/C3s con cotas de Manski;
  5. umbrales de D2 y D4, y la sensibilidad de D2 a una tendencia por dosis;
  6. cifras corregidas: 28 países; D1c con 7 tratados y al menos un trimestre posterior;
  7. el valor tasado uniprovincial queda declarado, con robustez sin esas 7 provincias.
- **Corrección técnica.** En `construir`, los shocks pasan a estar en puntos para que el error AKM tenga la escala de Z. src/v9/d4_inmigracion.py todavía no se había ejecutado.
- **Robustez de D1a que no se puede hacer.** El IPVA municipal solo tiene nombres, sin código INE, así que se elimina y lo mismo ocurre con su uso municipal en D4 (cruces solo por código).

## E4 — Re-revisión A1 de F2: APROBAR (2026-10-15)
- **Pendientes de gravedad baja, resueltos antes de estimar:**
  - A1-a: la ventana previa de la simulación de D1a pasa a 2019T1-2023T4. El MDE con Holm queda en 0,046 ≤ 0,05 y H1a-renta sigue confirmatoria.
  - A1-b: corregida la frase sobre el factor iid.
  - A1-c: declarado el desfase temporal de D3.
- **Etiqueta local:** `prereg-v9-a1b`.

## E5 — F3: ejecución de D1-D5 y D7 (2026-10-15)
- **Ejecución.** Cada diseño tiene su script en src/v9 (d1_zonas, d2_turisticos, d3_valencia, d4_inmigracion, d5_tipos, d7_hogares); src/v9/f3_capas.py consolida y asigna la capa con las reglas pre-registradas.
- **Resultado de las confirmatorias.** Ninguna llega a C3.
  - H1a-renta: no cumple pretendencias (p < 0,001), placebo de fecha (p = 0,007) ni Honest DiD con M̄ = 1.
  - H1b-renta: cumple pretendencias, placebo de fecha, permutación y Holm, pero no Honest DiD con M̄ = 1 (M̄ de ruptura 0,8; con M̄ = 0,5 el IC excluye el 0). Queda en C4 por la regla pre-registrada, que no se relaja después de ver el resultado.
- **Desviaciones técnicas** (no cambian ninguna regla de capa):
  1. **D3, València ciudad (26 CP).** Si más de la mitad de los pares de CP están dentro del corte, el error de Conley degenera (X'u = 0). En ese caso se informa HC1 y queda indicado en la especificación.
  2. **D4, AKM.** No está definido con un solo shock (variantes de un solo país): se informa «—». El IC de Anderson-Rubin lleva la bandera `AR_acotado`.
  3. **D1 y D2, Honest DiD.** Versión simplificada de magnitudes relativas, validada por Monte Carlo y conservadora frente a Rambachan y Roth (2023). La regla del addendum se aplica tal cual.

## E6 — Revisión de F3 (REHACER 1 de 2) y correcciones (2026-10-15)
- **Tope del revisor.** El revisor de F3 (docs/v9/revision_f3.md) usó unos 114.000 tokens, por encima del tope de 100.000. Conforme a la regla del prompt, **no se vuelve a delegar ninguna revisión**: la re-revisión de F3 y la revisión final las hace el orquestador y lo declara (docs/v9/revision_f3.md, sección «Re-revisión propia»; docs/v9/revision_final.md).
- **Hallazgo 1 (alta): Honest DiD.**
  - **Cambio.** Se sustituye el IC por sustitución por el de Rambachan y Roth (2023) para magnitudes relativas: Δ^RM se descompone en piezas poliédricas (una por diferencia previa y signo) y cada pieza usa el contraste «least favorable» de Andrews, Roth y Pakes. El IC es la unión sobre piezas.
  - **Validez.** El contraste LF es válido y algo más conservador que el híbrido del paquete HonestDiD.
  - **Validación por Monte Carlo:** output/v9/validacion/honest_rr_mc.csv (src/v9/validar_honest_rr.py) y tests/v9/test_herramientas.py.
  - **Regla de capa.** La regla pre-registrada (IC con M̄ = 1 que excluya el 0) se aplica tal cual con el IC de RR.
  - **Complemento.** La versión simplificada se publica solo como complemento. Se corrige la frase de E5.3, que la calificaba de conservadora sin haberlo comprobado.
- **Hallazgo 2.** En D4, con instrumento débil, la familia BH usa el p de Anderson-Rubin (con un instrumento, el de la forma reducida). El de Wald se conserva como `p_wald`.
- **Hallazgo 3.** La rejilla de AR pasa a ±5. Los conjuntos no acotados se marcan como tales.
- **Hallazgo 4.** La capa de cada exploratoria enumera las pruebas que no supera:
  - pretendencias;
  - placebo de fecha;
  - permutación;
  - tendencia por dosis;
  - pretendencias de Rotemberg;
  - placebo de D3.
- **Hallazgo 5: D7.** Hogares y población se miden en las mismas fechas (stocks a 1-1-2022 y 1-1-2025; ECP 2025T1 en lugar de 2026T1). El umbral de C1 (±2 %) queda documentado en src/v9/d7_hogares.py.
  - Con las fechas alineadas, el componente población pasa a explicar la mayor parte del aumento en ambos territorios.
  - Ninguna cifra publicada cambia: las de V9 aún no se habían difundido fuera de la rama.
- **Bajos:**
  - p de permutación con +1 en el numerador y el denominador;
  - registro de D4 completo (también el efecto total);
  - «diferencia o asociación» en lugar de «efecto» en la tabla.
- **Especificaciones pre-registradas que no se estiman, y por qué:**
  1. IPVA municipal (D1a y D4 municipal): no tiene código INE.
  2. D4 2022-2025 con los 22 grupos del censo anual: es una robustez que no cambia ninguna capa. Queda aplazada a docs/v9/ideas_futuras.md.
  3. Barcelona por barrios (D2): solo descriptiva, porque no hay resultado por barrio.
