# Revisión de la rama BM (modelos predictivos; H7): puerta antes de la evaluación sellada

Revisor independiente (opus). Rama `r2/BM`, commit `d64da2d` (con r2/main fusionado hasta `d590094`). Fecha: 2026-10-10.

## Veredicto: **REHACER** (dos bloqueantes en `evaluar_H7`; la parte de entrenamiento está bien)

La validación en bloques, el presupuesto, el registro, la regla de elección y el lenguaje son correctos y se reproducen bit a bit. Pero `evaluar_H7` no puede ejecutarse todavía:
- **C1.** Con el sellado anterior a `26d2e83`, que está en base 2025, el evaluador concatena NIVELES de índices en bases distintas. Esto destruye los objetivos A y B. Lo he comprobado numéricamente.
- **C2.** Un fallo en un análisis secundario se lleva por delante el resultado principal y gasta el único acceso.

Ambos son baratos de arreglar. Después basta una re-revisión breve de `bm_h7_sellado.py`, del test y de `decisiones.md`.

---

## 1. Reproducción (clon aislado, sin red)

- Clon de `r2/BM` en el scratchpad. `HTTPS_PROXY=http://127.0.0.1:9`, `OMP/OPENBLAS/MKL_NUM_THREADS=1`.
- `python3 src/v2/bm_run.py` dos veces: exit 0 y exit 0. Los md5 de todos los ficheros de `output/v2/BM/` (salvo `tiempos.json`) son **idénticos entre sí e idénticos a los versionados**: `git diff` solo muestra cambios en `tiempos.json`. Cada ejecución tarda unos 5 min.
- `pytest tests/test_bm_h7_sellado.py`: **4 passed**. Cubre el ensayo en seco, todas las clases de modelo, el aborto con menos de 8 periodos y que la historia de las selladas no mueve las pendientes.

## 2. Fuga de información (entrenamiento)

| Punto | Comprobación | Resultado |
|---|---|---|
| Acceso a datos | `bm_*.py` y el test solo usan `vc.load` (→ `holdout.load_train`). No hay `read_csv` ni referencias a `data/sealed`. `bm_h7_sellado.py` no llama a `evaluate` | OK |
| Ventana | `preparar_*` recorta a `tmax=2024Q2`. Las líneas base usan `Q_TRAIN_FIN` | OK |
| Splits | `vc.block_splits(h=4, embargo=4)`: hay max(4,h)=4 periodos entre L y el primer origen de test. Las filas de entrenamiento cumplen `pos+4 ≤ L` | OK |
| Escalado, imputación y FE | En `ajustar`, la mediana, la media/DE, la DE de y y el FE por unidad se calculan solo con las filas de entrenamiento del split | OK |
| Hiperparámetros | Se fijan por configuración; la elección se hace con la métrica de bloques del propio entrenamiento. No hay CV no temporal | OK |
| VAR/TVP-VAR | Se usan datos con `pos ≤ L`; los coeficientes se filtran hasta L y quedan fijos en test; el pronóstico usa retardos ≤ t | OK |
| Importancias | La permutación y SHAP se calculan sobre los bloques de test de la validación de entrenamiento y el ALE sobre el entrenamiento del último split. Todo es ≤ 2024Q2 y no toca nada sellado | OK |
| Población | Se usa el último 1 de enero observado («en escalera»), sin interpolar. Hay retraso de publicación (no es tiempo real) y está declarado | Aceptable, declarado |

## 3. Especificaciones, presupuesto y FDR

- `presupuesto.json` y `regla_H7.md` se versionaron en `046ecd2` (08:08:55 UTC). Los primeros resultados están en `7fbccdb` (08:20:25), y una ejecución completa dura unos 5 min. Ninguno de los dos ficheros ha cambiado desde `046ecd2` (`git diff 046ecd2 d64da2d` vacío). El historial no permite excluir una ejecución local previa sin commitear, pero no hay indicios de ella.
- **59 de 63 configuraciones**: A 21 (EN 10, PL 1, ARDL 1, TAR 2, BVAR 5, TVP 2), B 19 y C 19. Las 4 restantes eran la reserva del bloque 5. `registro.csv` tiene 59 filas más la del presupuesto y coincide con el código. Las rejillas del código coinciden con las declaradas.
- La selección de los modelos para H7 es la misma en `7fbccdb`, `49e2e05` y `d64da2d` (TVPVAR_k0.95 / LGBM_nl4_n400 / EN_l10.7_a0.4). El rebase de niveles no la alteró.
- **BH** (`bm_run.bh`): la implementación es correcta (paso a paso hacia arriba con mínimo acumulado). Se aplica por objetivo sobre las configuraciones, por separado frente a AR(4) y frente a ECM v1: 0 de 59 sobreviven. El Holm intra-H7 (`_holm`, m=3, paso a paso hacia abajo con parada) también es correcto.
- **Discrepancia menor (C3).** `presupuesto.json` dice que el BVAR elige λ por verosimilitud marginal. El código trata los 5 λ como candidatos que compiten por RMSE y solo informa de la logML. No cambia la elección: el mejor BVAR (0,0664) queda por encima de TVP (0,0593). Hay que declararlo.

## 4. Misma muestra, AR(4), ECM v1 y DM-HLN

`vc.evaluar` compara sobre la intersección modelo ∩ AR(4) ∩ ECM v1, con DM-HLN a h=4 (en los paneles, media transversal por periodo). La regla de cobertura (≥ 90 %) excluye ARDL (0,89) de la elección, conforme a lo declarado.

## 5. Regla H7 (dictamen sobre el punto 4 del encargo)

- **Fiel al pre-registro.** La H7 pre-registrada habla de «algún modelo **con variables**». Incluir el AR(4) como candidato sería incoherente con la hipótesis y la haría trivialmente no evaluable. Excluir las líneas base es correcto.
- Elegir **un modelo por objetivo** con Holm m=3 y regla «algún objetivo cumple» es una lectura razonable de «Algún modelo… elegir UN modelo» que controla el FWER de la afirmación «algún modelo». Es una interpretación, así que debe constar en `decisiones.md` (C3).
- **Los modelos elegidos frente al AR(4) con la métrica declarada** (RMSE medio en bloques, muestra común; lo he recalculado):
  - A: TVP-VAR 0,0593 frente a AR(4) 0,0614. Con la métrica de elección SÍ mejora; solo con el RMSE agregado es peor (0,0726 frente a 0,0699).
  - B: LGBM 0,0118 frente a 0,0126.
  - C: elastic net 0,0498 frente a 0,0408, peor también en entrenamiento.
- **Dictamen.** Llevar al sellado un modelo ya peor en entrenamiento (C) es conservador: sesga hacia el nulo y no infla el error de tipo I. La regla se fijó antes, no depende del resultado frente a las bases y está escrita así de forma explícita. **No se cambia a posteriori**: no hay error demostrable en ella. Debe declararse antes de abrir que en C se espera un nulo y cómo se leerá («no hay evidencia de mejora», no «evidencia de ausencia»), igual que en A, donde n=8 da una potencia mínima.
- El pre-registro dice «nacional y provincias selladas». El contraste principal con las 52 provincias en la ventana sellada sigue el criterio ya aplicado a H1 y H2 (`revision_BA.md` C3; `revision_BV.md`), con las selladas como secundario (b) y (b'). Hay que declararlo como desviación o interpretación (C3).

## 6. `evaluar_H7` frente al pre-registro y al estándar

Lo que está bien:
- Orígenes 2023Q3-2025Q2, con objetivos ≤ 2026Q2.
- Pendientes solo con las 49 provincias y objetivos ≤ 2024Q2.
- FE propio de 11, 16 y 45 con su historia ≤ 2024Q2, también en el AR(4) y el ECM v1 (reutiliza `ba_h1_sellado._parches`, ya revisado).
- DM-HLN frente a AR(4) y ECM v1 con p_IUT = máx., Holm m=3.
- Aborta si hay menos de 8 periodos.
- Secundarios (a), (b) y (b').
- El test 4 prueba que perturbar la historia de las selladas no mueve el RMSE de las 49 (diferencia < 1e-12).

### C1 [BLOQUEANTE]: concatenación de niveles en bases distintas

`_evaluar` concatena entrenamiento y sellado (`_concat`). Los objetivos se construyen con niveles: `vc._lvl_fn` usa `np.log(ipv)` o `ln_ipc_alquiler`, y el ECM nacional usa niveles en el DOLS. Con `holdout.build` anterior a `26d2e83`, el entrenamiento estaba rebasado (2015=100) y el sellado no (base 2025). El resultado es un salto de ln f en 2024Q2→2024Q3, que contamina:
- y en los orígenes 2023Q3-2024Q2;
- los retardos de ΔY en los orígenes de 2024Q3 en adelante;
- el ECT.

El objetivo C (p_tasado en euros, deflactor sin rebasar) no se ve afectado.

**Prueba.** He reproducido el pseudo-sellado del test y he multiplicado los índices de la parte sellada por una constante (cambio de base: IPV ×0,62, IPC alquiler ×0,87; `ln_` desplazado igual; los `d_ln`/`d4_ln` sin tocar):

| Objetivo | Sin cambio de base: RMSE modelo / AR4 / ECM | Con cambio de base: RMSE modelo / AR4 / ECM |
|---|---|---|
| A | 0,0414 / 0,0538 / 0,0743 | **0,3867 / 0,5101 / 0,3189** |
| B | 0,0118 / 0,0109 / 0,0100 | **0,0913 / 0,1131 / 0,1079** |
| C | 0,0735 / 0,0399 / 0,0738 | 0,0735 / 0,0399 / 0,0738 (invariante) |

Con el sellado en otra base, H7 en A y B sería ruido determinado por el salto, y podría incluso «cumplirse» de forma espuria: en B el modelo baja de 0,113 a 0,091.

El orquestador informa de que `r2/main` (`26d2e83`) ya rebasa el panel completo antes de separar. Exigido:
1. Fusionar `r2/main` (≥ `26d2e83`) en `r2/BM`. Confirmar que `data/sealed` se regeneró con el `build` corregido antes de llamar (lo hace el orquestador). Reejecutar `bm_run.py`: el entrenamiento no cambia y los md5 deben seguir iguales.
2. **Guarda de continuidad** en `_evaluar`, ANTES de ajustar nada. Para `ipv` (nacional) e `ipc_alquiler` (cada provincia de entrenamiento, y el nacional si se usa) se comprueba que |ln X(2024Q3) − ln X(2024Q2) − d_ln X(2024Q3)| < 1e-6.
   - Recomendación, para no gastar el acceso: si la guarda falla, reencadenar los niveles sellados de esa unidad con `d_ln` (desplazamiento constante por unidad), dejar constancia de `"reencadenado": [...]` en el resultado y abortar solo si falta el `d_ln` necesario.
   - Las provincias selladas (toda su historia en el sellado) son coherentes consigo mismas y quedan exentas.
3. **Test** `test_sellado_en_otra_base`. Es el experimento de arriba (`scratchpad/exp/base_shift.py`), con el siguiente aserto: el resultado de A, B y C con el pseudo-sellado en otra base es igual al del pseudo-sellado sin cambio, con tolerancia 1e-8 (tras la guarda o el reencadenado).

### C2 [BLOQUEANTE]: el resultado principal debe quedar antes que los secundarios

Ahora mismo el bucle calcula, para cada objetivo, el principal y después los secundarios (incluido (b'), que vuelve a correr toda la validación en bloques del modelo, unos 100 s en B). Una excepción en un secundario de B o C pierde también los principales ya calculados. Como `holdout.evaluate` registra la apertura antes, el acceso quedaría gastado sin resultado (el mismo problema que C1 de `revision_BP.md`). Además, la comprobación de 8 o más periodos se hace por objetivo: si C no llega a 8, se pierden A y B.

Exigido:
- (i) Una comprobación previa y barata de los tres objetivos antes de ajustar nada: disponibilidad de y y de los regresores del modelo elegido en los 8 orígenes. En A, el TVP-VAR necesita dY, dOcup, dTipoR y dCred sin NaN hasta 2025Q2, y el IPV hasta 2026Q2.
- (ii) Calcular los principales de A, B y C, el Holm y `H7_cumple`, y fijarlos en el dict de resultado.
- (iii) Secundarios cada uno en `try/except`, con el error guardado como texto.
- (iv) Test que inyecte un fallo en un secundario y compruebe que se devuelve el principal.

### C3 [antes de abrir; no requiere re-ejecución] Declaraciones en `docs/v2/decisiones.md`

- Interpretación de la regla: un modelo por objetivo; Holm m=3; principal con 52 provincias frente a «provincias selladas» del pre-registro; secundarios.
- Lectura del nulo: C ya es peor en entrenamiento y A tiene n=8.
- Que el abortar con menos de 8 periodos gasta el acceso.
- Discrepancia del BVAR (logML declarada frente a ranking por RMSE; sin efecto en la elección).
- Constantes no declaradas pero fijas: RF con 300 árboles y max_features 0,5; LGBM con min_child_samples 30 y subsample 0,8; TVP con λ0 0,2 y decay 0,98.

### C4 [requerido para cerrar la rama, NO para la apertura de H7] Bloque 6, deep learning

«No ejecutado» no es aceptable como cierre. La instrucción del usuario («deep learning solo sobre paneles y solo si supera al gradient boosting con DM-HLN; si no, resultado negativo») presupone intentarlo: un resultado negativo exige ejecutarlo, y «torch no instalado» es un problema de entorno, no de datos.

Exigido:
- Instalar torch para CPU, con la versión fijada en requirements; queda en local y `make all` sigue sin red.
- Declarar ANTES, en un commit separado, un presupuesto mínimo: p. ej. `presupuesto_bloque6.json` con 2 configuraciones de un LSTM pequeño (1 capa, 16 y 32 unidades, ventana de 8 trimestres, semilla fija, `torch.use_deterministic_algorithms`, 1 hilo) solo en el panel B. Opcionalmente también en C. Esto se suma a las 59 y supera las 63 declaradas: se declara como ampliación.
- Mismos bloques y escalado dentro del split. DM-HLN frente a LGBM_nl4_n400 (y frente a AR(4)) en la misma muestra. BH sobre las configuraciones.
- Informar de un negativo o un positivo real.
- El LSTM **no entra** en la elección de H7: la regla ya está fijada.
- Si la reproducibilidad bit a bit con torch no se logra, informar de la tolerancia observada.

### C5 [menor]

- Bloque 5. Omitir los spillovers por falta de coordenadas es aceptable, aunque la contigüidad provincial podría construirse a mano; el factor dinámico se omitió con la reserva sin usar. Basta con anotarlo en `docs/v2/limitaciones.md`.
- `output/v2/BM/smoke/` está versionado: hay que borrarlo o etiquetarlo como salida de humo, que no cuenta como especificaciones.

## 7. Lenguaje y escala de evidencia

- Correcto. SHAP, la permutación y el ALE están etiquetados como EXPLORATORIO, con «se publica por transparencia, NO como explicación» porque ningún modelo mejora al AR(4). PDS y las proyecciones locales llevan «Asociación, no causalidad», con avisos de colinealidad y de T pequeño.
- El nivel máximo antes del sellado es EXPLORATORIO (criterio uniforme b), y tras el sellado, como mucho, ASOCIACIÓN ROBUSTA predictiva.
- No hay lenguaje causal.

## 8. Datos y referencias

- Solo se usan paneles de entrenamiento versionados.
- La población no está interpolada (escalera de observados). La imputación por mediana se hace dentro del split, y LightGBM usa NaN nativos.
- No hay datos de PDF ni OCR en el modelo principal.
- Las referencias metodológicas citadas en el resumen (Giannone-Lenza-Primiceri 2015, Primiceri 2005, Koop-Korobilis 2013, Apley-Zhu 2020, BCH) se usan solo como descripción de métodos. Su estado VERIFICADA/NO VERIFICADA y el cuartil deben figurar en `docs/literatura.md` antes de BS; no lo he auditado en esta puerta.

## Cambios priorizados

1. **C1** (bloqueante): fusionar r2/main ≥ `26d2e83` y confirmar que el sellado está regenerado; guarda de continuidad 2024Q2→2024Q3 con reencadenado; `test_sellado_en_otra_base`.
2. **C2** (bloqueante): comprobación previa de los tres objetivos; principales y Holm antes de los secundarios; secundarios en `try/except`; test de fallo de un secundario.
3. **C3**: declaraciones en `decisiones.md` antes de la apertura.
4. **C4**: bloque 6 con LSTM mínimo en el panel B y presupuesto declarado antes (necesario para cerrar la rama; independiente de H7).
5. **C5**: limitaciones del bloque 5; `smoke/`.

Tras C1-C3: re-revisión breve de `bm_h7_sellado.py`, del test y de `decisiones.md`. Si se aprueba, el orquestador puede abrir H7 aunque C4 siga pendiente.

---

## Re-revisión (iteración 2 de 2): commit `83af813` en `r2/BM` (con r2/main ≥ `26d2e83` fusionado)

### Veredicto final: **APROBAR**. H7 puede abrirse UNA vez con `holdout.evaluate("H7", bm_h7_sellado.evaluar_H7, "BM", ["panel_prov_q", "nacional_q_v2"])`.

### Comprobaciones

- **Reproducción.** Nuevo clon aislado de `83af813`, sin red, con OMP/OpenBLAS/MKL a 1 hilo y torch 2.14.1+cpu. Dos ejecuciones de `bm_run.py`: exit 0 y exit 0. Los md5 son idénticos entre sí y a los versionados, LSTM incluido (solo cambia `tiempos.json`). `pytest tests/test_bm_h7_sellado.py`: **7 passed**.
- **H7 sin evaluar.** `docs/v2/holdout_accesos.md` (r2/main `f316bc5`) solo registra aperturas y resultados de H1, H2 y H6. No hay ninguna fila de H7. `bm_h7_sellado.py` no llama a `evaluate`.
- **La elección de H7 no cambia.** `seleccion_H7.json` es idéntico a `d64da2d` (TVPVAR_k0.95 / LGBM_nl4_n400 / EN_l10.7_a0.4) y `regla_H7.md` no ha cambiado desde `046ecd2`.
- **C1, resuelto.**
  - `holdout.build` (r2/main) rebasa el panel completo antes de separar.
  - Además, `_reencadenar` rehace `ipv` e `ipc_alquiler` (y `ln_`) del sellado desde el nivel de 2024Q2 con sus `d_ln`. Para las provincias selladas lo hace desde su propio nivel en L, lo que equivale a la identidad en su base.
  - `_guarda_continuidad` (umbral 0,05) aborta antes de ajustar nada.
  - Tests:
    - con el sellado en otra base, el resultado es el mismo (tolerancia 1e-9 en A, B y C), lo que reproduce mi experimento de la iteración 1;
    - con la concatenación ingenua, la guarda aborta.
  - El riesgo de falso aborto es mínimo. En entrenamiento, |Δln IPV| trimestral ≤ 0,035 desde 2019. El máximo |Δln| del IPC de alquiler 2024Q2→Q3 declarado por el orquestador es 0,0129.
  - Observación: el umbral se fijó después de esa declaración (acceso de comprobación ya registrado en `decisiones.md`). Es un parámetro de seguridad, no de inferencia, así que no invalida nada.
- **C2, resuelto.**
  - Etapa 1: los principales de A, B y C (cada uno aborta si tiene menos de 8 periodos), luego Holm m=3 y `H7_cumple`.
  - Etapa 2: los secundarios, cada uno en `try/except` con el error registrado. Hay un test con un fallo inyectado en (b').
  - Pendiente menor: la comprobación de 8 o más periodos sigue siendo por objetivo y no previa a los tres. Un aborto en C perdería A y B, pero el acceso se gasta igualmente al abortar, así que no cambia el riesgo.
- **C4, resuelto.**
  - `presupuesto.json` se modificó en `8cc303f` (09:20:44 UTC), ANTES de los resultados del LSTM (`83af813`, 09:37:25). Reasigna explícitamente la reserva del bloque 5 (4 → 0) a `lstm_panel_B` (4: hidden {8,16} × epochs {25,50}; fijos: ventana 8, lr 0,003, wd 1e-3, 1 capa, batch 256; semilla y algoritmos deterministas).
  - El total sigue en 63 = 21 + 19 + 19 + 4, y `registro.csv` y `presupuesto_usado.json` lo cuadran. La reasignación respeta el presupuesto declarado, no lo amplía.
  - Sin fuga en `bm_lstm.py`: filas de entrenamiento con pos+4 ≤ L; mediana, media/DE, FE y DE de y solo con entrenamiento; ventanas que terminan en el origen. Usa los mismos splits.
  - DM-HLN frente a LGBM_nl4_n400 en la misma muestra (n=2254): el mejor LSTM (h16_e25) tiene RMSE 0,0141 frente a 0,0124; DM −0,84, p=0,40. Es un **resultado negativo** y queda fuera de H7. Con BH sobre las 4 configuraciones no cambia nada: ninguna mejora al GB y dos son significativamente peores.
- **C3, parcial.** `decisiones.md` recoge la regla, que el modelo de C es peor en entrenamiento (prueba conservadora), los bloques 5 y 6, y que el principal con 52 provincias y Holm m=3 está en `regla_H7.md`, commiteada antes. No impide aprobar: lo que falta pasa a limitaciones (abajo).

### A `docs/v2/limitaciones.md` (BM)

1. H7 tiene potencia baja:
   - en A, n=8 orígenes nacionales con DM-HLN;
   - el modelo elegido para C (elastic net) ya es peor que el AR(4) en entrenamiento;
   - un nulo se lee como «no hay evidencia de mejora», no como evidencia de ausencia.
2. El contraste principal de los paneles usa las 52 provincias en la ventana sellada; el pre-registro decía «provincias selladas», que pasan a secundario (b) y (b'). Es el mismo criterio que en H1 y H2.
3. Abortar con menos de 8 periodos en cualquier objetivo gasta el único acceso. La comprobación se hace por objetivo, no antes de los tres.
4. BVAR: el presupuesto decía «elección de λ por verosimilitud marginal», pero el código compite con los 5 λ por RMSE y solo informa de la logML. Sin efecto en la elección.
5. Hiperparámetros fijos no declarados en la rejilla:
   - RF: 300 árboles, max_features 0,5;
   - LGBM: min_child_samples 30, subsample 0,8;
   - TVP: λ0 0,2, decay 0,98.
6. Bloque 5 no ejecutado (sin contigüidad provincial ni factor dinámico). La reserva se reasignó al LSTM.
7. Bloque 6: LSTM solo en el panel B, 4 configuraciones pequeñas. El resultado negativo vale para ese presupuesto, no para el deep learning en general.
8. La población «en escalera» no está disponible en tiempo real (retraso del padrón). Las importancias (SHAP, permutación, ALE) y PDS son EXPLORATORIO, sobre modelos que no mejoran al AR(4).
9. Umbral de continuidad (0,05) fijado después del acceso de comprobación declarado del orquestador.
10. `output/v2/BM/smoke/` sigue versionado. Es salida de humo y no cuenta como especificaciones (limpieza pendiente, C5).
