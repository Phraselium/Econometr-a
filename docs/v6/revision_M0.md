# Revisión independiente de M0 v6 (puerta previa a `prereg-v6`)

Fecha: 2026-10-11. Commit revisado: `1da30e8` (r6/main). Revisor independiente: no ha hecho el trabajo; no ha leído `data/sealed` ni ejecutado `evaluate_v6`.

## Veredicto: **REHACER**

Hay tres bloqueantes de datos (B1-B3), que son fugas o huecos que cambian el contenido de la muestra sellada, y dos de pre-registro (B4-B5). Todos se corrigen en M0, sin estimar nada. Una vez etiquetado `prereg-v6`, cambiar el sellado ya no sería limpio, así que conviene hacerlo antes.

## Comprobaciones realizadas

- **`check_v6.py` y `check_texto.py`:** 0 errores en ambos.
- **Reproducción en un clon aislado sin red** (`git clone` en el scratchpad, `HTTPS_PROXY=http://127.0.0.1:9`, sin `data/sealed` previo):
  - `m0_run.py` termina con exit 0 en dos ejecuciones;
  - los recuentos de filas de entrenamiento y selladas coinciden con `sellado_info.json`;
  - el contenido numérico de los seis `*_train.csv.gz` coincide con HEAD.
- **Los md5 NO son idénticos entre ejecuciones**, por dos causas (ver N1):
  - la cabecera gzip lleva la hora (`mtime`);
  - la columna `provincia` cambia de etiqueta («araba» / «arabaalava»), porque `NOMBRE_PROV` se construye recorriendo un `set` y depende de `PYTHONHASHSEED`. Por eso también cambian los md5 de `data/sealed/v6_prov_*.csv`. Solo se calcularon los md5; su contenido no se leyó.
- **Regla de partición (`holdout.provincias_selladas_v6`):**
  - resultado: 07, 22, 26, 28, 30, 31, 33, 35, 38, 44 y 50, es decir, 11 de 52 en bloques completos de CCAA, sin Andalucía ni Castilla-La Mancha (las CCAA de v2: 11, 16 y 45) y sin Ceuta ni Melilla;
  - he comprobado a mano la tabla `CCAA_PROV`.
- **`cache_sellado` (m0_run.py:724-747):**
  - sustituye en memoria `holdout.distrito_sellado_v6` y `municipio_sellado_v6` por versiones con las listas precalculadas;
  - su lógica es idéntica a la original, línea por línea;
  - no modifica `src/holdout.py`; `sellar_v6` resuelve las funciones por nombre global del módulo, así que la caché se aplica;
  - **es segura**, con una reserva: la muestra de verificación no contiene ningún distrito v3, de modo que la rama `None` no se prueba (N6).
- **Paneles de entrenamiento:** los he leído con pandas para comprobar años y cobertura por variable.

## Tabla de hallazgos

| ID | Tipo | Fichero:línea | Hallazgo | Corrección |
|---|---|---|---|---|
| B1 | **Bloqueante** (fuga entre paneles) | src/v6/m0_run.py:776, 808 | En `prov_trim_compra` el año sellado es 2026, el último con valor tasado trimestral (solo 2026T1). Por eso **2025T1-2025T4 quedan en entrenamiento** para 38 provincias (comprobado en `prov_trim_compra_train.csv.gz`). En `prov_compra_anual`, en cambio, el 2025 anual está sellado, y es la media de esos mismos cuatro trimestres (también `ln_cv_etdp` = suma de los trimestres). El desenlace sellado anual puede reconstruirse exactamente desde el entrenamiento trimestral. | Fijar un único corte temporal por fuente en todos los paneles: sellar desde 2025T1 en el trimestral (`ult_trim = ULT_PRECIO`). Añadir a `check_v6.py` esta comprobación: para cada variable de origen común, el máximo año de entrenamiento en cualquier panel debe ser menor que el mínimo año sellado en cualquier otro panel. |
| B2 | **Bloqueante** (fuga entre paneles) | src/v6/m0_run.py:812 (y 33-34) | `mun_anual` se sella con `ULT_PRECIO=2025`, pero SERPAVI municipal termina en 2024. Así, **`ln_alq_m2_serpavi_mun` de 2024 está en entrenamiento** (1.977 municipios), mientras que el SERPAVI de 2024 está sellado en `prov_alquiler_anual` y en `dis_alquiler_anual`. Además, el último año del desenlace municipal de alquiler no queda sellado, lo que contradice la regla «último año disponible de cada panel». | Sellar por desenlace, no por panel. Dos opciones: (a) dividir `mun_anual` en `mun_compra_anual` (corte 2025) y `mun_alquiler_anual` (corte 2024); o (b) sellar `mun_anual` desde 2024. La misma comprobación de B1 en `check_v6.py`. |
| B3 | **Bloqueante** (medida principal y composición del sellado) | src/v6/m0_run.py:114-124; docs/v6/diccionario.md:104 | Faltan 9 provincias de valor tasado. Son las CCAA uniprovinciales (07, 26, 28, 30, 31, 33 y 39) más Ceuta y Melilla, y **6 de ellas (07, 26, 28, 30, 31 y 33, incluida Madrid) son provincias selladas**. Por eso la parte espacial sellada del precio principal se queda en 5 de 11 provincias (Aragón y Canarias): el trimestral tiene 5 unidades selladas. La ausencia no es razonable, porque `data/raw/mivau_valor_tasado_nacional_ccaa_prov.csv` trae esas series a nivel CCAA de 1995 a 2026T1. Navarra aparece con dos rótulos: «Com. Foral de», 2015-2018, y «Comunidad Foral de». | Asignar la serie CCAA a la provincia en las 7 uniprovinciales, sin duplicar Navarra (prioridad al rótulo con la serie completa; si ambos coinciden en un trimestre, comprobar la igualdad). Marcarlo en el diccionario como «CCAA = provincia (uniprovincial)»; no es una interpolación. Regenerar el sellado y la potencia. |
| B4 | **Bloqueante** (pre-registro) | docs/v6/hipotesis.md:63-90 | Quedan grados de libertad sin fijar que importan: (1) **regresores** «los de la familia con signo», sin decir si entran las variables (?) ni el contemporáneo frente al retardo; (2) **retardos** «en el script de modelo», sin número; (3) niveles o diferencias; (4) **corrección DM** «que se fije en M3», cuando CLAUDE.md exige HLN; (5) «**Holm o BH**», sin elegir, y sin definir la familia de contrastes; (6) número de bloques y longitud del **embargo** de la validación temporal; (7) criterio 1 de «relevante con seguridad»: «dos familias independientes de variables» no tiene sentido para una sola variable (¿se quiere decir dos familias de modelos, como FE, CCE y ML?); (8) cómo se define el ECM v1 «en la misma muestra» a nivel provincial; (9) **efectos fijos de año** junto a regresores nacionales (crédito, tipo), que quedan absorbidos: hay que decir cuáles se excluyen o qué variante se usa. | Fijar por escrito: la lista cerrada de regresores por mercado; los retardos (p. ej. t−1); el desenlace en niveles de log con FE o en diferencias; DM con HLN; Holm para la familia «variables × mercado principal» y BH para la robustez; K bloques y un embargo de ≥1 año; reformular el criterio 1; la especificación exacta del ECM v1 de referencia; el tratamiento de las variables nacionales con FE de año. |
| B5 | **Bloqueante** (validación nueva y su declaración) | docs/v6/decisiones.md:10; output/v6/M0/sellado.md:20 | El corte temporal de v6 (2025 en compra, 2024-2025 en alquiler y 2026T1 en trimestral) **cae dentro de la ventana sellada de v2** (`holdout._mascara_sellada`: 2024T3-2026T2 y años ≥2025 en todas las provincias), que **ya se abrió 8 veces** (H1, H2, H3-1, H3-2, H3-3a, H3-3b, H6 y H7 en docs/v2/holdout_accesos.md). La limitación declarada solo menciona el uso descriptivo en v4-v5. La validación v6 es distinta de la de v2 en lo espacial, pero no es nueva en lo temporal. | Declararlo en decisiones.md, sellado.md e hipotesis.md §5. Pre-registrar que M4 reporta por separado: (i) las provincias selladas v6 en los años de entrenamiento, que es la parte nueva, y (ii) el último año, que es la parte contaminada por v2. Las conclusiones se apoyan en (i). |
| N1 | No bloqueante (reproducibilidad) | src/v6/m0_run.py:76-79, 627 | Los md5 no son estables (ver arriba): `NOMBRE_PROV` depende del orden del `set` y el gzip lleva `mtime`. | Recorrer `sorted(aliases(nom))` empezando por `norm(nom)`, o fijar `NOMBRE_PROV` desde `territorio`; usar `compression={"method": "gzip", "mtime": 0}`. |
| N2 | No bloqueante (reproducibilidad) | Makefile:44 | `m0_run.py` no está en `make all`, y M1-M4 consumen sus salidas versionadas. En un clon limpio `data/sealed` no existe, así que solo se regenera ejecutando m0_run, que es determinista en contenido numérico (comprobado). | Incluirlo en `make all` tras `make data`, una vez resuelto N1. Guardar en `sellado_info.json` el sha256 de cada `data/sealed/v6_*.csv` (sin contenido). `check_v6.py` debe comprobar que coincide, para que una regeneración no cambie la muestra sellada en silencio después de `prereg-v6`. Advertencia: desde un worktree, `_repo_principal()` escribe en el `data/sealed` del repositorio principal. |
| N3 | No bloqueante (fuga potencial) | docs/v6/diccionario.md:81-87; m0_run.py:515-598 | `nacional_trim_desc.csv` (que incluye `cv_etdp_nacional_suma_prov`, `hip_viv_num_nacional_suma_prov`, `pm2_tasado_nacional` e `ipc_alq_nacional_idx`) y `ccaa_ipv_anual_desc.csv` no están sellados, llegan hasta 2025 e incluyen las provincias y CCAA selladas. El diccionario solo pide sellarlos «en el tiempo», y eso no basta: las sumas nacionales contienen el desenlace de las provincias selladas. El IPV CCAA tiene base 100 en 2025 (normalización de la fuente en el año sellado). | Pre-registrar que los agregados que suman desenlaces provinciales no entran como regresores de los modelos provinciales, o reconstruirlos sin las provincias selladas. Usar el IPV en tasas, no en niveles de índice. |
| N4 | No bloqueante (medidas) | docs/v6/diccionario.md:20, 78 | El punto medio p25-p75 del distrito es un sustituto razonable si se declara (lo está), pero p25 y p75 «no están en el panel», así que la robustez declarada no es ejecutable. | Añadir `ln_alq_m2_p25_dis` y `ln_alq_m2_p75_dis` al panel. |
| N5 | No bloqueante (medidas) | output/v6/M0/sellado_info.json | En contratos nuevos (GVA: 03, 12 y 46; Incasòl: 08, 17, 25 y 43) ninguna provincia está sellada. El sellado de ese mercado es solo temporal (2025) y queda dentro de la ventana de v2 (B5). | Declararlo en hipotesis.md §5. |
| N6 | No bloqueante | src/v6/m0_run.py:740-744 | La verificación de `cache_sellado` no incluye ningún distrito sellado en v3, así que la rama `None` no se prueba. | Añadir a la muestra dos códigos de `distritos_sellados_v3()`. |
| N7 | No bloqueante (referencias) | docs/v6/hipotesis.md:6, 22 | Cavalleri et al. (2019) es un OECD Working Paper: tiene DOI, pero no puede tener cuartil Scimago, así que no cumple la definición de VERIFICADA. El revisor no ha re-verificado los DOI (sin red). | Marcarla «DOI verificado; cuartil no aplicable (documento de trabajo)». |
| N8 | No bloqueante (potencia) | docs/v6/potencia.md:5, 9-19; m0_run.py:711-722 | La fórmula (Fisher-z con Bonferroni K y efecto de diseño con ICC supuesto) es correcta y está declarada con honestidad. Tiene tres límites. (a) Usa el N agrupado y la sd total de ln y: con FE de provincia y año la variación útil es la within, así que la potencia real es menor y el efecto en % no corresponde al estimador FE. (b) El texto dice «17 CCAA» y en entrenamiento hay 8-11 clústeres; con tan pocos, debe pre-registrarse un wild cluster bootstrap. (c) K se fija a mano (22, 10, 4...) sin enlazarlo a la lista de regresores de B4. | Recalcular con la sd within y el K de la lista cerrada (B4); corregir el número de clústeres; pre-registrar wild cluster bootstrap (Webb). |
| N9 | No bloqueante | output/v6/M0/paneles/prov_estatico.csv | Las variables estáticas (costa, isla, distancia, Censo 2021) incluyen las provincias selladas. Son covariables previas (2021) y no desenlaces: es aceptable. | Declararlo en el diccionario. |
| N10 | No bloqueante | src/holdout.py:406-411 | Los distritos v3 quedan fuera de `dis_alquiler_anual`, pero siguen dentro de los agregados municipales y provinciales de SERPAVI. Esto afecta a la limpieza del holdout v3, no al de v6. | Una línea en las limitaciones. |

## Criterios de la puerta

1. **Validación sellada.**
   - La regla es nueva y distinta de la de v2 y la de v3 en lo espacial, y se aplica bien en cada nivel: provincia, municipio por prefijo, distrito por prefijo con los distritos v3 excluidos.
   - Fallos: dos fugas entre paneles (B1 y B2), un hueco en el precio principal que vacía media muestra sellada (B3) y una declaración de contaminación incompleta (B5).
   - Las variables derivadas (`d_ln_*`, ratios, tensionadas) solo usan datos contemporáneos o pasados de la misma provincia: no hay fuga.
   - No hay normalizaciones propias con todo el periodo.
   - El Bartik no está construido en M0.
2. **Medidas.**
   - Hay una medida principal y una de robustez por nivel y mercado.
   - Stock y contratos nuevos van separados.
   - La medida de precio está declarada en `resultado.json`.
   - La falta de las 9 provincias de valor tasado no es razonable (B3). El punto medio p25-p75 es aceptable si está declarado (N4).
3. **Diccionario.**
   - Recoge capa, fuente, fecha, transformación y cobertura.
   - No hay interpolaciones (el código usa agregación con un mínimo de observaciones; las imputaciones `fillna(0)` de las zonas tensionadas son indicadores 0/1 de no declaradas).
4. **Hipótesis.**
   - Los signos están razonados por mercado.
   - No basta como pre-registro (B4).
5. **Potencia.** Correcta en la fórmula y honesta en lo que declara, pero optimista con FE y con pocos clústeres (N8).
6. **Reproducibilidad.**
   - Exit 0 sin red y contenido numérico determinista.
   - Los bytes no son idénticos (N1).
   - Debe entrar en `make all`, con checksum del sellado (N2).

## Prioridad de cambios

B1 → B2 → B3: regenerar el sellado una sola vez con las tres correcciones y añadir el check entre paneles. Después B5 y B4 (texto del pre-registro), luego N1-N2 y, por último, el resto.
