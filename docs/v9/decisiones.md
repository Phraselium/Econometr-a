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
