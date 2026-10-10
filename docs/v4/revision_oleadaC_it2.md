# Revisión de la oleada C, iteración 2 (revisión acotada)

Fecha: 2026-10-10. Alcance: comprobar si se resolvieron los cambios C1-C14 de `docs/v4/revision_oleadaC.md`. No se reejecutó `make all` ni se leyó data/sealed. `python3 src/v3/check_texto.py`: 0 errores.

## Veredicto: **REHACER** (acotado: dos correcciones de texto, sin recálculo)

## Estado de C1-C14

| Cambio | Estado | Comprobación |
|---|---|---|
| C1 Terminadas | resuelto | WP, informe y lo_que_sabemos dan 72.000 (2019) a 94.000 (2024) en territorio común, sin País Vasco ni Navarra. El policy brief compara hogares y terminadas en la misma ventana (2021-2024). |
| C2 Codificación de I01 | resuelto | El CSV tiene la columna `direccion`. La matriz separa a favor y en contra: I01 = 3 / 3. |
| C3 Instrumentos omitidos | resuelto | Las 9 filas (I03, I11, I15, I18, I19, I22, I24, I25, I28) están en la matriz, con un criterio de inclusión declarado. |
| C4 Capas signo / magnitud | resuelto (con una recomendación) | Matriz e informe §5: el signo es C2 y la magnitud C4; la rejilla da el 15-100 %. El policy brief deja las ayudas en «C4» sin el signo por grupo C2 (R1). |
| C5 Simetría V11 / M5-V1 | resuelto | Las dos fichas reciben PARCIALMENTE con regla común y acotada. V11 explica que «resolvería» no se sostiene a las dosis simuladas. |
| C6 Alquiler y precio | resuelto (con una recomendación) | CSV con `capa_direccion`, `capa_cuantia` y `mediana_pct_no_C1`. Precio: núcleo de 44-56 % y el IPV como fuente discrepante. Explicación de IPC frente a SERPAVI corregida. CCAA: 3 fuentes (Navarra, 2). La definición C1 del WP (l. 52) aún presenta el ±5 pp sin decir que es regla de dirección (R2). |
| C7 Procedencia de los programas | **pendiente** | «4 de 9 en copia no oficial» figura en WP §limitaciones, informe, README y cobertura. Pero WP l. 18 (contribución 4) mantiene «Las medidas proceden de documentos oficiales». Es falso y contradice la l. 126 del mismo documento. Recuentos de instrumentos.md: 88, cerrado. |
| C8 Esfuerzo de recogida y literatura | **pendiente** | La cobertura por documento está bien documentada y declara el límite técnico (cotas inferiores). Sinai-Waldfogel se reintentó (429) y Fack quedó VERIFICADA. Sin embargo, la matriz rotula I18, I22, I24, I25 e I28 como «sin evidencia hallada en la búsqueda registrada», y `literatura_v4.md` (l. 72) los declara «No buscados». |
| C9 Jefatura (B5) | resuelto | Figura como C4 por la regla B5 en WP, informe, lo_que_sabemos y policy brief. La convivencia sigue en C2. |
| C10 Conclusiones | resuelto | Conclusión 1: [C1] desfase / [C4] concentración. Resumen, conclusión 4 e informe: «entre los instrumentos simulados», signo C2, magnitud C4. Baum-Snow y Marion figura en las referencias. |
| C11 Restos de versiones anteriores | resuelto | Las fichas V13 y V14 ya no están en `verificador/fichas/`. La pregunta abierta 10 está reformulada (GSADF ejecutado). |
| C12 Ficha M5-V1 | resuelto | Declara la cota superior para la ayuda focalizada y que los avales no son ayuda por unidad. Carozzi et al. se usa solo como referencia cualitativa. |
| C13 Neutralidad léxica | resuelto | No quedan «antiocupación», «especulativ» ni «todo el espectro». El dominio del grupo está redactado en `fuentes_fallidas.md`. |
| C14 README | resuelto | Tiempo de ≈20-21 min coherente con el WP (apéndice B). Notariado y Registradores marcados como «no verificadas». Hay correspondencia de tablas con programas. Acceso a los programas: webs (5) y copias de medios (4). |

## Problemas bloqueantes

1. **B1. La matriz atribuye una búsqueda que no se hizo (C8; neutralidad del esfuerzo).** `src/v4/m5_run.py`, l. 141, aplica la misma etiqueta «sin evidencia hallada en la búsqueda registrada» a todas las filas añadidas. Para I18, I22, I24, I25 e I28, el registro dice «No buscados (… no equivale a "sin evidencia")».
   - **Corrección:** en esas filas, «no buscada (pendiente; docs/v4/literatura_v4.md)». Hay que aplicarla en el generador y regenerar la matriz y el informe si los reproduce.
   - **Alternativa:** hacer la consulta y registrarla.
   - Así lo pide el criterio de C8: «sin evaluar» no puede significar a la vez hallado y no buscado.
2. **B2. Procedencia en el working paper (C7).** La l. 18 dice «Las medidas proceden de documentos oficiales».
   - **Corrección:** sustituirla por la frase común: «de 9 programas: 5 en la web del grupo y 4 en copia no oficial alojada por un medio».
   - El informe (l. 162, «documentos oficiales o de programas») debería usar la misma frase.

Ninguna de las dos correcciones cambia cifras ni capas.

## Recomendaciones (no bloqueantes)

- **R1.** En la fila de ayudas del policy brief, añadir «signo por grupo C2 (el beneficiario no paga más; los no beneficiarios pagan más); conjunto y magnitud C4», como en la matriz y el informe.
- **R2.** En WP l. 52, decir «±5 pp anuales: regla de dirección; la cuantía exige ±15 % en nivel», como en `decisiones.md` (C6).
- **R3.** El encabezado del mensaje 1 del policy brief («sobre todo en pocas provincias») mezcla C1 y C4. Ya lo aclaran las viñetas etiquetadas, pero conviene un encabezado neutro en capa («Faltan viviendas»).
- **R4.** Gibbons y Manning y Baum-Snow y Marion figuran como «VERIFICADA, cuartil no verificado». Según CLAUDE.md, VERIFICADA exige el cuartil Scimago: o se completa el cuartil o se rotulan «DOI verificado; cuartil no verificado».
- **R5.** Hay una independencia parcial entre fuentes de precio que no se describe igual en todas partes:
  - las notas de M7 dicen que el INE y Notariado comparten fuente;
  - lo_que_sabemos dice que la independencia parcial es entre el Ministerio y Notariado.

  Conviene unificar la descripción.
