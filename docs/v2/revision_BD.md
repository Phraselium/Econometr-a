# Revisión independiente — rama BD (descomposición por periodos)

Rama `r2/BD`, commit `93686b1`. Revisor independiente v2 (opus). Fecha: 2026-10-10.

## Veredicto: **REHACER**

Motivo bloqueante: el código versionado **no se ejecuta** (exit 1), por lo que `make models` (y `make all`) se rompen al fusionar, y el `registro.csv` versionado procede de una ejecución abortada. Las cifras sí son correctas: con un arreglo de una línea, el pipeline reproduce **bit a bit** todas las salidas versionadas salvo `registro.csv`. Además hay problemas de contenido (contribución de una variable en niveles, etiquetas de evidencia desactualizadas, resultados no replicados destacados como hallazgos) que deben corregirse en la misma iteración.

---

## 1. Reproducción (clon aislado, sin red, 1 hilo)

- Dos clones `git clone -b r2/BD` en el scratchpad (sin `data/sealed`), `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`, `OMP/OPENBLAS/MKL_NUM_THREADS=1`, salidas versionadas apartadas antes de ejecutar.
- **Commit tal cual: exit 1 en las dos ejecuciones.**
  ```
  File "src/v2/bd_panel.py", line 82, in decompone
      for nm in sorted(cfdf["escenario"].unique()):
  KeyError: 'escenario'
  ```
  La llamada de turismo (`con_cf=False`) genera un `cfdf` vacío sin columnas. Falla igual con `--smoke`.
- El `registro.csv` versionado (md5 `d5d27a7d…`) es **idéntico** al que deja la ejecución abortada: tiene 29 entradas y le faltan `nacional_ECMv1_real_LP_DOLS` y `nacional_ECMv1_real_CP`. Las demás salidas proceden de una ejecución anterior con otro código (marcas de tiempo: `bd_panel.py` editado a las 09:54:08, csv a las 09:54:55, `registro.csv` reescrito a las 09:55:54).
- **Con el parche mínimo** (solo en los clones: `for nm in (sorted(cfdf["escenario"].unique()) if len(cfdf) else []):`): exit 0 en las dos ejecuciones (unos 70 s cada una) y **md5 idénticos entre ellas**. Coinciden con lo versionado en los 17 ficheros (csv, json, md, 5 png), excepto `registro.csv`, que ahora sí trae las 2 entradas nacionales (31 en total).
- `Makefile`: `models` ejecuta `src/v2/*_run.py` con `|| exit 1`. Con este commit, `make all` se detiene en BD.

## 2. Fuga de información

- Datos: solo `v2_common.load` (`panel_prov_q`, `nacional_q_v2`) y `bv_lib.preparar_panel` (recorta a `Q_TRAIN_FIN`). No hay lecturas directas de ficheros, ni `data/sealed`, ni `holdout.evaluate`. El log de accesos (`docs/v2/holdout_accesos.md`) no tiene ninguna entrada de BD. El clon no contiene `data/sealed` y el pipeline corre igual.
- Muestras: el panel cubre 2008Q1-2024Q1 (no usa 2024Q2, cuya población está anulada) y el nacional llega como máximo a 2024Q2. Nada ≥2024Q3.
- La exposición hipotecaria se estandariza entre provincias con datos de 2005-2007 (anteriores a la muestra). El ffill de `pob_w` mira solo hacia atrás.
- Bootstrap: remuestrea filas, provincias o trimestres de la propia muestra de entrenamiento. Sin datos externos.
- **Sin fuga.**

## 3. Coherencia con BA/BV y especificaciones

- La reestimación con una especificación conjunta propia está **declarada** (`decisiones.md`, entrada BD; `resumen.md`, «Método»). Las 4 descomposiciones, el turismo, los 2 ECM nacionales y los 24 contrafactuales están en `registro.csv` cuando el código se ejecuta entero. Hoy faltan los 2 nacionales (ver §1).
- **No contradicen a BA/BV.** Alquiler M1, 20-34 por periodo: BD 0,165/0,208/0,180/0,079 frente a BA 0,171/0,212/0,178/0,081 (`BA/periodos_coef.csv`); los demás coeficientes también son casi iguales. Compra M1, `cu_x_expo`: P1 −0,0062 y P3 −0,0121 en BD frente a −0,0075 y −0,0129 en BV; crédito ≈0,005-0,007 en ambas. M2 difiere más, lo esperable al no tener efectos de tiempo. En compra M2 el coeficiente de Δ4 coste de uso nacional es +0,006, de signo contrario al esperado (IC por bloques de tiempo incluye 0). Conviene mencionarlo.
- Interpretación de M1: la cautela que ya figura («el coeficiente se identifica con diferencias entre provincias y se aplica a la media nacional») es correcta. Pero el «Método» afirma que los efectos de tiempo recogen «el movimiento común de las propias familias», y eso **no es lo que se calcula**: el código atribuye a las familias b·x̄ (media nacional ponderada), así que l_t solo recoge la parte del movimiento común que b no explica. El «común» de M1 no es grande «por construcción». En alquiler llega al 140 % desde 2014 porque la demografía aporta en negativo.

## 4. Aritmética de la descomposición

- La identidad observado = Σ familias + común + residuo se cumple con error 0 en las 24 celdas mercado × modelo × ventana. También se cumplen familias = explicado y demografía = 20-34 + extranjera. Es cierta por construcción: el común se define como Y − Xb − e.
- **Recálculo independiente** (LSDV con dummies, sin la rutina de demeaning de la rama) de la ventana P2-P4:
  - alquiler M1: familias −2,702, 20-34 −2,674, residuo −0,190;
  - alquiler M2: −3,513, −3,611, −0,928;
  - compra M1: −5,852;
  - compra M2: −8,289.

  Todo coincide con `contribuciones_todas.csv`. El contrafactual (b) de compra M1 da −0,993/−2,807/−0,678 (total −4,477) y también coincide. Los contrafactuales (a) son exactamente el opuesto de la contribución demográfica, como debe ser.
- Ponderación: media por trimestre ponderada por `pob_w` (población total, ffill); la estimación es MCO sin ponderar. Está declarado de forma implícita; debe decirse explícitamente.
- IC: B=999 confirmado. La envolvente toma el mínimo de los inferiores y el máximo de los superiores de dos bootstraps percentil, ambos reestimando el modelo: (i) remuestreo de provincias con reposición; (ii) bloques móviles de 4 trimestres dentro de cada periodo. Están bien construidos. Limitación: P3 tiene 8 trimestres (2 bloques, 5 posibles inicios) y P4 tiene 9, así que el IC temporal de esos periodos es poco fiable. Debe declararse.
- **Error de contenido (prioritario).** `cu_x_expo` es una variable en NIVEL (coste de uso × exposición), pero su contribución se calcula como b × media del nivel, no como una variación respecto a una base. Ese reparto depende del origen arbitrario del coste de uso: un cambio de origen lo absorbe el FE de provincia y cambia la cifra atribuida a «crédito/coste de uso» frente a «común». Además, como la exposición está estandarizada sin ponderar, su media ponderada ≠ 0 solo por la ponderación por población. BA y BV usan β·(media_P(x) − media muestral). En compra M1 P1, de los −6,26 pp de «crédito/coste de uso» que cita la lectura, **−4,58 pp** salen de este término de nivel (comprobado). Los contrafactuales (b) y (c) no tienen este problema porque usan diferencias.
- Efecto de borde de Σ Δ4/4: ya figura en `observado_niveles_referencia.csv`, pero es grande. En alquiler P2 da 1,58 frente a 2,30 en niveles, y en compra P2 3,39 frente a 4,76. Debe decirse en el texto, no solo en un fichero.

## 5. Contrafactuales y lenguaje

- Las advertencias de que son ceteris paribus, sin equilibrio general y sin identificación causal están bien. No se encontraron afirmaciones causales («causó», «impulsó», «debido a»): todo se presenta como asociación o contabilidad.
- **Resultados no replicados entre M1 y M2 presentados como hallazgos**, en contra de la regla:
  1. «Respuesta breve» y «Lectura» de alquiler: «solo la población de 20-34 años aparece con IC>0 en M2 (0,57 [0,09; 1,04])». En M1 el IC incluye el 0 (0,34 [−0,11; 0,85]). Es además una selección entre unos 14 componentes × 2 modelos sin corrección por multiplicidad.
  2. Contrafactual (a1) de alquiler en P4: −0,53 en M2 (IC excluye 0) frente a −0,31 en M1 (IC incluye 0). Se presentan juntos como si coincidieran.
  3. Compra (b) en M1 (−4,48): el texto ya dice «no se replica en M2», pero sigue en la respuesta breve. Debe pasar a una lista de «no replicados».
  4. Explicar que el efecto agregado de (b) y (c) en M1 de compra es b·Δcu·(media ponderada de la exposición), es decir, existe solo por la ponderación.
- La fila (c) de alquiler M1, «0,00 [0,00; 0,00]», es trivial por construcción: debe marcarse «no aplica».
- Texto fijo en `bd_texto.py`: «−0,14 [−0,55; 0,27]» y las frases de (b)/(c) no se leen de las tablas. Hay que generarlas desde los datos.

## 6. Niveles de evidencia, nacional y figuras

- **Etiqueta desactualizada y engañosa.** Las filas 20-34 de alquiler dicen «ASOCIACIÓN ROBUSTA (candidato…; Holm-7 pendiente en BS)». Hay tres problemas:
  - Holm-7 ya se ejecutó (`decisiones.md`, `4a9da9c`): ninguna confirmatoria sobrevive, H1 conjunta tiene p_holm = 1, y el componente 20-34 queda a decisión de BS.
  - La etiqueta empieza por un nivel que no se ha alcanzado.
  - El nivel heredado corresponde al **coeficiente** de H1 en BA, no a esta contribución reestimada con otra especificación. Esa contribución es negativa desde 2014, y en P4 el coeficiente de BD tiene un IC por provincias que incluye 0.

  Debe decir: «EXPLORATORIO (coeficiente análogo al componente 20-34 de H1; su nivel lo fija BS)». El resto de etiquetas (EXPLORATORIO, H2 no confirmada, tope que falló placebos y pretendencias) es coherente con `decisiones.md`.
- **ECM nacional.** Es una réplica fiel de v1: coeficientes LP 1,63/0,009/0,043/−0,60 frente a 1,48/0,002/0,032/−0,66; mismas variables de corto plazo. Hay cuatro problemas:
  - El bootstrap de residuos por bloques con regresores fijos **subestima** la incertidumbre del DOLS. Los permisos tienen un IC que excluye 0 en los 4 periodos, mientras que en v1 su p HAC era 0,27, y el propio texto dice que eran «no significativos». Hay que corregir el método (bloques de pares (y, X) o más largos, o un IC a partir del EE HAC) o, como mínimo, advertirlo y no leer esos IC.
  - La tabla LP del resumen **omite la fila «estacional (dummies)»** y no cuadra: en P4 los componentes suman 7,8 frente a un observado de 4,8, porque falta ≈ −3,0.
  - El texto dice «LP … 2008Q2-2024Q2», pero el DOLS se estima en 2007Q1-2023Q4 (registro).
  - Figura `descomposicion_nacional_ecm.png`: la barra LP de P2 queda cortada por arriba.
- El resto de figuras se leen bien, tienen fuente y aviso sin interpretación causal, y el IC es la envolvente con B=999.

## 7. `output/v2/BD/smoke` (sin versionar)

**No versionar la actual**: es obsoleta. La generó un código anterior al commit, porque su registro trae los nacionales y el código actual aborta antes de llegar a ellos. Precedente: BA y BV versionan su `smoke/`. Tras el arreglo: regenerar con `python3 src/v2/bd_run.py --smoke` y **versionarla** por coherencia con BA/BV. Si el orquestador prefiere no versionar smoke, borrarla y añadirla a `.gitignore`; lo que no vale es dejarla sin versionar.

---

## Cambios requeridos (por prioridad)

**P0 — bloqueantes**
1. `bd_panel.decompone`: proteger el bucle del registro de contrafactuales cuando `cfdf` está vacío (`con_cf=False`). Reejecutar `bd_run.py` completo y versionar las salidas, sobre todo `registro.csv` con las 31 entradas.
2. Comprobar que `make models` pasa por BD sin error, y que dos ejecuciones en clon sin red dan md5 idénticos.
3. `smoke/`: regenerarla con el código corregido y versionarla, o borrarla e ignorarla (ver §7).

**P1 — contenido**
4. Contribución de `cu_x_expo` (variable en nivel): medirla respecto a una base (media muestral como BA/BV, o nivel al inicio del periodo). Rehacer la lectura «crédito/coste de uso pesa en P1 (−6,26)».
5. Etiquetas de evidencia: sustituir «ASOCIACIÓN ROBUSTA (candidato…, Holm-7 pendiente)» por «EXPLORATORIO (coeficiente análogo al componente 20-34 de H1; nivel según BS)». Citar el resultado de Holm-7 ya ejecutado.
6. Sacar de la «Respuesta breve» y de las lecturas como hallazgos lo que no se replica en M1 y M2: 20-34 desde 2020 (solo M2), (a1) de alquiler en P4, (b) de compra en M1. Agruparlos en «no replicados / no robustos» e indicar que no hay corrección por multiplicidad.
7. ECM nacional: corregir o advertir la subestimación del IC LP (permisos); añadir la fila «estacional» a la tabla LP para que cuadre; corregir la muestra del DOLS (2007Q1-2023Q4); arreglar el recorte de la figura.
8. Corregir la frase de M1 «los efectos de tiempo recogen … el movimiento común de las propias familias»: las familias reciben b·x̄ y l_t es el resto. Explicar que el efecto agregado de los canales por exposición en M1 depende de la media ponderada de la exposición.

**P2 — menores**
9. `bd_texto.py`: eliminar cifras y conclusiones escritas a mano (−0,14 [−0,55; 0,27]; frases de (b)/(c)) y generarlas desde las tablas.
10. Marcar como «no aplica» la fila (c) de alquiler M1 (0 por construcción).
11. Añadir una sección BD a `docs/v2/limitaciones.md` con:
    - el efecto de borde Σ Δ4/4 frente al cambio en niveles (alquiler P2 1,58 frente a 2,30; compra P2 3,39 frente a 4,76);
    - el IC temporal con 2-3 bloques en P3/P4;
    - estimación sin ponderar y agregación ponderada;
    - población intra-anual interpolada (heredada de BA);
    - el coeficiente positivo de Δ4 coste de uso en compra M2;
    - ausencia de corrección por multiplicidad.

## Comprobado y correcto
- Sin fuga ni uso de la muestra sellada.
- Determinismo: md5 idénticos en dos ejecuciones con el parche.
- Identidad contable exacta, y recálculo independiente coincidente en 4 modelos y 1 contrafactual.
- B=999 y envolvente bien construida.
- Desviaciones declaradas en `decisiones.md`.
- Coeficientes coherentes con BA/BV.
- Advertencias de los contrafactuales y ausencia de lenguaje causal.
- Figuras con fuente.
