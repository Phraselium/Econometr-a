# V16 · Errata V8-M5: Navarra y La Rioja fuera del instrumento Bartik (B-3, opción (a))

Orden expresa del autor (2026-10-18): corregir V8-M5 excluyendo Navarra (ES22) y La Rioja (ES23) del instrumento Bartik (IV3), por falta de datos en el año base 2008. Después, regenerar M5 → F5 → F6 → publicacion/. Si cambia algo más que las 8 filas de tablas_v8.xlsx y lo que derive estrictamente de ellas, se para.

## Dependencias de M5 (antes de regenerar)

Lista obtenida buscando en src/ quién lee output/v8/M5 y sus derivados:

| Paso | Script | Lee | Escribe |
|---|---|---|---|
| 1 | src/v8/m5_lpiv.py | Eurostat lfst_r_lfe2en2 (data/raw), paneles de V8 | output/v8/M5/ (atribucion.csv, coeficientes.csv, hipotesis_m5.csv, iv3_rotemberg.csv, registro.csv, resultado.json, resumen.md, tiempos.json) |
| 2 | src/v8/f5_atribucion.py | output/v8/M0-M9 | output/v8/F5/ (atribucion_combinada.csv, regla §9, fichas, resultado.json) |
| 3 | src/v8/f6_tablas.py | output/v8/M0-M9, F5 | output/v8/tablas_v8.xlsx, tablas_modelos_destacados.*, F6/resultado.json (sha256 del xlsx) |
| 4 | src/v8/f6_hechos.py | output/v8/M0-M9, F5 | output/v8/F6/hechos.json (cifras V8-*) |
| 5 | src/v8/f6_verificador.py | output/v8/F6/hechos.json | output/v8/fichas_verificador_v8.json, verificador_v8.md |
| 6 | src/v5/cifras_clave.py | output/*/hechos.json | output/v5/cifras_clave.csv (no puede cambiar) |
| 7 | src/v8/render_v8.py | salidas de V8 | informe de V8 renderizado |
| 8 | src/v10/base.py | output/v8/F5/atribucion_combinada.csv | data/base (tabla de atribuciones) |
| 9 | src/consulta/generar.py | hechos y tablas | consulta/ |
| 10 | `make publicacion` (src/v7_1/publicacion.py) | output/v8/tablas_v8.xlsx y otros | publicacion/tablas_v8.xlsx, metodologia/ |

No dependen de M5, aunque lo citen, y no se ejecutan:
- src/v8/f6_congelar.py: predicciones congeladas, no usa M5.
- src/v8/m7_multiverso.py: solo nombra M2/M5 como clave de cruce.
- src/v5/d1_run.py y src/v5/verificador.py: se refieren a v4-M5, otro módulo.
- src/v6_3/ver_hechos.py: no lee M5.

## Corrección

En src/v8/m5_lpiv.py (`construye_bartik`), una CCAA con alguna celda sin dato en el año base 2008 queda sin cuotas (NaN) y su instrumento no está definido. Se descarta en el panel, en lugar de imponer cuota 0. Las celdas de otros años y de Ceuta y Melilla, que solo entran en el total nacional del leave-one-out, siguen como estaban.

## Comprobación después de regenerar

- **M5.**
  - Cambian las 8 filas IV3_bartik_h1-2 de atribucion.csv, los coeficientes IV3, iv3_rotemberg, el registro, resultado.json y el resumen (etiqueta «panel 15 CCAA»).
  - hipotesis_m5.csv no cambia.
  - Valores de `contribucion_pp`:

| Fila | Antes | Después |
|---|---|---|
| compra P2 | 24,32 | 22,77 |
| compra P3 | −18,14 | −17,00 |
| compra P4 | 0,73 | 0,72 |
| compra P5 | −9,09 | −8,58 |
| alquiler P2 | 7,32 | 6,57 |
| alquiler P3 | −5,46 | −4,90 |
| alquiler P4 | 0,22 | 0,21 |
| alquiler P5 | −2,74 | −2,48 |

- **F5.** atribucion_combinada.csv: las mismas 8 filas.
- **F6.**
  - tablas_v8.xlsx: comparado hoja a hoja; solo cambian 8 filas (27 celdas) de la hoja «Atribucion». Las demás hojas son idénticas.
  - F6/resultado.json: solo el sha256 del xlsx.
  - F6/hechos.json y las fichas del verificador: sin cambios.
- **cifras_clave.csv:** idéntico byte a byte (sha256 comprobado).
- **render_v8:** sin cambios, salvo la nota añadida a la plantilla del informe.
- **data/base/v8_atribucion.parquet** y su copia pública: las mismas 8 filas. Se regeneraron con el código de src/v10/base.py; antes de la errata, ese código reproducía byte a byte el fichero versionado.
- **publicacion/:** tablas_v8.xlsx, MANIFIESTO (sha256) e informe_econometrico_v8.md (nota).
- **metodologia/:** desviaciones_v8.md (errata) y MANIFIESTO.

**Efectos colaterales revertidos (no derivan de las 8 filas)**
- f6_verificador.py reescribió docs/v6_1/historial_conclusiones.md con su versión de V8, sin la adenda de V9. Se restauró desde git.
- consulta/version.json solo cambiaba de commit y fecha. Se restauró.

**Ninguna cifra de cifras_clave, capa ni conclusión cambia.**

**Pendiente:** el paquete de depósito de la 1.0 (_deposito/vivienda-espana-evidencia-1.0) conserva el sha256 anterior del parquet de la base. Se regenerará al preparar el depósito.
