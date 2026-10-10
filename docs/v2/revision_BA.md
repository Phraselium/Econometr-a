# Revisión v2: rama BA (alquiler), fase de entrenamiento

Revisor independiente (opus). Objeto: rama `r2/BA`, commit `d4cdc85` (worktree /home/user/wt-BA): src/v2/ba_*.py y output/v2/BA/. Pre-registro: docs/v2/hipotesis.md en `910c42a`, sin cambios desde entonces. Fecha: 2026-10-10. Para que el criterio sea el mismo en todas las ramas, he tenido en cuenta docs/v2/revision_BV.md.

## Veredicto: **REHACER**

El análisis de entrenamiento está bien hecho: se reproduce byte a byte, el registro está completo, no hay lenguaje causal y el turismo se trata con prudencia. Aun así hay cuatro problemas bloqueantes:
- (i) Se ejecutó con el train que contenía la fuga de 2024Q2.
- (ii) El nivel de evidencia («ASOCIACIÓN ROBUSTA provisional») contradice el pre-registro y la escala.
- (iii) `evaluar_H1`, que se ejecuta una sola vez, estima las pendientes incluyendo las provincias selladas. No usa los parámetros de entrenamiento, y en eso difiere del criterio fijado para BV.
- (iv) Falta un ensayo en seco versionado.

Los cambios están acotados. No hace falta rediseñar el análisis: basta con fusionar, corregir y reejecutar.

## 1. Reproducción (clon aislado, sin red)

- `git clone --branch r2/BA` del repositorio principal en el scratchpad (sin data/sealed), en el commit `d4cdc85`. `HTTPS_PROXY=HTTP_PROXY=http://127.0.0.1:9`.
- `python3 src/v2/ba_run.py` dos veces: **exit 0** en ambas. Los md5 de los 17 ficheros (csv/json/md) son **idénticos** entre las dos ejecuciones e **idénticos a los versionados** en el commit.
- `python3 src/v2/ba_run.py --smoke` dos veces: exit 0. Los 7 ficheros de smoke/ son idénticos entre sí y a los versionados.
- `make models` ejecuta `src/v2/ba_*.py` en orden alfabético. `ba_h1_sellado.py`, `ba_informe.py` y `ba_lib.py` no hacen nada al importarse (no tienen `__main__`), así que es seguro, pero conviene blindarlo (C6).
- `resumen.md` y `resultado.json` los genera `ba_informe.py`, no están escritos a mano: OK.

## 2. Fuga de información

| Comprobación | Resultado |
|---|---|
| Lecturas de datos en src/v2/ba_*.py | Solo `vc.load(...)` (→ `holdout.load_train`) de panel_prov_q, panel_prov_a, panel_muni_a y nacional_q_v2. No hay `read_csv` directo, ni lecturas de data/raw, data/sealed o la red. OK |
| Cobertura del train | panel_prov_q 2002Q1-2024Q2, panel_prov_a y panel_muni_a ≤ 2023 (2024 en embargo), nacional ≤ 2024Q2. No aparecen las provincias 11, 16 ni 45. OK |
| **Población interpolada 2024Q2** | **FUGA confirmada** (build_dataset_v2.py `stock_q`): T2-T4 del año *y* se interpolan entre el 1-ene-*y* y el 1-ene-*y+1*. En el train, `pob_20_34` y `pob_extranj` de **2024Q2 usan el dato del 1-ene-2025** (sellado). Las 49 filas de 2024Q2 entran en H1 principal, en las robusteces trimestrales, en periodos (P4) y en las contribuciones C1/C2. El orquestador la ha corregido en r2/main (valor anulado, método `anulado_fuga_sellado`); BA se ejecutó con el train antiguo. Magnitud (mi comprobación quitando 2024Q2): β pob 20-34 pasa de 0,1454 (p 0,0065) a 0,1488 (p 0,0056) y β extranjera de −0,0185 a −0,0184. El efecto es despreciable, pero hay que reejecutar con el train corregido |
| Interpolación dentro del entrenamiento | Más allá de 2024Q2, cada T2-T4 usa el 1 de enero siguiente (información de hasta 3 trimestres después). No es una fuga hacia la muestra sellada, pero el regresor principal de H1 está interpolado en ~75 % de las filas, y eso choca con la regla «interpolaciones solo en robustez». Atenuante: las versiones sin interpolar (solo T1 observado: 0,143, p 0,004; panel anual: 0,149, p WCB 0,004) coinciden. Ver C7 |
| Fuera de muestra | `make_feat` usa la población «en escalera» (último 1 de enero OBSERVADO, `ffill(limit=3)`), sin interpolación: sin fuga. Reestimación por split con orígenes s+h ≤ L, embargo max(4,h)=4 y ventana expansiva (v2_common). No hay escalado aprendido. OK. Limitación en tiempo real (no es fuga): el padrón del 1-ene-*y* se publica a mediados de *y*, de modo que en los orígenes T1-T2 el dato aún no estaba disponible |
| ECM v1 / DOLS | `_dols` recorta a pos ≤ L *antes* de construir adelantos: los adelantos posteriores a L son NaN. OK |
| Accesos a la muestra sellada | docs/v2/holdout_accesos.md no existe en ninguna rama, worktree ni historial git (git log --all). `evaluate` lo crea en la primera evaluación. El revisor no tiene permiso para leer data/sealed/_accesos.log (denegado), así que la comprobación es indirecta. No hay ninguna llamada a `holdout.evaluate` en el código. **H1 no ha sido evaluada.** OK |
| Robustez del propio `holdout.evaluate` (infraestructura) | El acceso se registra solo **después** de que `fn` termine. Si `fn` falla tras leer data/sealed, no queda registro y se podría repetir. Recomendación al orquestador: registrar un evento «apertura» antes de leer (C10) |

## 3. Fidelidad al pre-registro y nivel de evidencia

**H1 (pre-registrada):** «Δ4 ln IPC alquiler se asocia positivamente con el crecimiento de la población de 20-34 años **y** de la población extranjera». Panel 2008Q1-2024Q2, FE de provincia y trimestre, EE cluster por provincia, Holm sobre la familia de 7 y, en la muestra sellada, mejora del RMSE frente al AR(4) de panel (DM-HLN).

| Elemento | Código | Valoración |
|---|---|---|
| Especificación principal | Δ4 ln ipc_alquiler ~ Δ4 ln pob 20-34 + Δ4 ln pob extranj + Δ4 ln ocupados, FE prov + trimestre, CR1 cluster, t(G−1), WCR Webb B=9.999 | Coincide con el pre-registro. He revisado la implementación de FWL/QR, CR1 y WCR: correcta |
| Resultado | 20-34: 0,145 [0,043; 0,248], p WCB 0,0094. Extranjera: −0,018 [−0,054; 0,017], p 0,30. Ocupados ≈ 0 | Cifras del resumen coherentes con los CSV |
| Hipótesis conjunta | Se informa correctamente que la conjunción NO se confirma | Bien informado |
| **Regla del nivel** (ba_informe.py:94-99) | `nivel = "ASOCIACIÓN ROBUSTA" if (ok_pob or ok_ext) else "EXPLORATORIO"` | **Incorrecta.** H1 es conjunta: el contraste adecuado es de intersección-unión (se rechaza solo si se rechazan ambos componentes; p_H1 = máx. de los p unilaterales en la dirección +). Con β_extranjera < 0, p_H1 ≈ 0,85: **H1 no se sostiene**. Con un «o», la conjunción pasa a ser una disyunción elegida a posteriori |
| «Provisional» | Etiqueta ASOCIACIÓN ROBUSTA «provisional» antes del sellado | No existe en la escala. ROBUSTA exige sobrevivir a Holm (familia de 7), a las submuestras **y** a la muestra sellada cuando aplica, y aquí aplica |
| Holm | m=2 dentro de H1 | El pre-registro pide Holm sobre las 7 confirmatorias. Hay que llamarlo «Holm intra-H1» y entregar al orquestador el p de H1 (intersección-unión) para la familia de 7 |
| Criterio de submuestras | Signo + en todas las submuestras trimestrales y en el panel anual | Razonable. Se dice «fijado antes de mirar», pero no se puede auditar (un solo commit, como en BV): hay que declararlo en decisiones.md. Hay que anotar también que en pre-COVID la extranjera es **negativa y significativa** (−0,049, p 0,03) |

### Criterio uniforme entre ramas (dictamen)
Debe aplicarse por igual a BA, BV, BI y las siguientes:
1. `nivel_evidencia` de resultado.json califica la **hipótesis pre-registrada completa**, tal como está escrita. Las hipótesis conjuntas se contrastan por intersección-unión. Los componentes sueltos o las variantes son resultados secundarios y su nivel máximo es EXPLORATORIO.
2. En la fase de entrenamiento, si la hipótesis tiene evaluación sellada, el nivel máximo es **EXPLORATORIO**. Se puede añadir el diagnóstico `candidata_a_robusta: true/false`, que exige Holm-7 orientativo (Bonferroni ×7 o p ≤ 0,05/7 como cota) y el criterio de submuestras. ROBUSTA solo se asigna después de evaluar en la muestra sellada y aplicar el Holm de la familia de 7 (orquestador).
3. La validación fuera de muestra *en entrenamiento* (el `oos_ok` de BV o la tabla OOS de BA) es informativa. No forma parte del pre-registro y no puede subir ni bajar el nivel por sí sola. El criterio predictivo es el sellado.
4. Si la evaluación sellada falla, o si la hipótesis ya falla en entrenamiento (como H1 por la conjunción), el nivel final es EXPLORATORIO («no confirmada»).

Aplicación a BA: **H1 = EXPLORATORIO (no confirmada: falla la conjunción)**. El componente pob 20-34 se describe como «asociación en entrenamiento que sobrevive a Holm intra-H1 y a todas las submuestras (EXPLORATORIO, resultado parcial no pre-registrado por separado)». La evaluación sellada de H1 se ejecuta igualmente, una vez, tal como se pre-registró (es la parte predictiva). Su resultado se informa, pero **no puede llevar H1 a ROBUSTA**. Para BV coincide con el nivel EXPLORATORIO dictado, aunque el motivo correcto es el punto 2 y no `oos_ok`.

## 4. Especificaciones, presupuesto y FDR

- registro.csv tiene 50 filas, que he cotejado con el código una a una. H1 principal: 1. H1_rob: 28 (6 submuestras, 19 sin una CCAA, sin FE de tiempo, anual IPC y anual SERPAVI). Periodos: 1. Contribuciones: 4 (C1-C4). Turismo: 9 (6 municipales con placebo y 3 provinciales). OOS: presupuesto declarado n_max=6 y 4 configuraciones usadas (A-D). Líneas base: 2. **No hay especificaciones en el código que falten en el registro.** No se pueden auditar iteraciones previas (un solo commit).
- El presupuesto OOS (≤ 6) se respeta: 4 de 6. El modelo primario B (AR(4) + variables de H1) es el AR(4) anidado más las variables de la hipótesis. Es coherente con el criterio dictado para BV (C3 allí) y no lo eligió el ranking: C tiene un RMSE algo menor y no se eligió.
- Holm (econ_utils.holm) y BH (ba_lib.bh): implementaciones correctas. En periodos se aplica BH sobre 12 y se informa también Holm.
- La familia F4 de turismo hace BH solo sobre 3 de los 8 contrastes de interés no placebo. Hay que incluirlos todos (C8).

## 5. Fuera de muestra (entrenamiento)

- Misma muestra: `muestra_comun` cruza A-D, AR(4) de panel y ECM v1 de panel (n=1.974, primer test 2012Q1, h=4, embargo 4). DM-HLN por periodo (media transversal) con t(n−1) frente a ambos. OK.
- Ningún modelo mejora significativamente al AR(4). B: RMSE 0,01169 frente a 0,01244 (p 0,65); frente al ECM v1, p 0,16. Está bien informado y sin exagerar.

## 6. Turismo, lenguaje y datos

- Turismo etiquetado EXPLORATORIO. Se advierten la causalidad inversa y la selección, y hay un placebo de pretendencia (ΔSERPAVI 2017→2020 sobre ΔVUT futura, p 0,81). El resultado provincial (Δ VUT por 1.000 hab., p 0,0007) se presenta como dependiente de la métrica, con N temporal = 6. Correcto. Un retoque: signos_vs_literatura.csv marca ese contraste como «significativo_5% True». Hay que añadir «EXPLORATORIO; N_t=6» en la misma fila.
- No hay lenguaje causal en resumen.md. Las contribuciones por periodo se presentan con la categoría «no explicado» y el aviso de que los IC no recogen los shocks comunes. Conviene añadir «descomposición contable, no atribución causal».
- Fuentes: IPC alquiler, padrón y EPA (INE), SERPAVI (BD oficial XLSX del MIVAU, no OCR) y VUT (INE). No se usan datos de PDF/OCR sin validar. La población interpolada está marcada (ver C7).
- Referencias citadas (Khametshin et al. 2024; Helfer et al. 2023; Garcia-López et al. 2020; Garriga et al. 2019; Torres-Téllez y Montero-Soler 2023): todas figuran como VERIFICADA en docs/literatura.md, con cuartil (Torres-Téllez: cuartil no verificado; Khametshin: documento ocasional sin cuartil). signos_vs_literatura.csv no recoge ese estado: hay que añadir las columnas `estado` y `cuartil`.

## 7. `evaluar_H1` (src/v2/ba_h1_sellado.py)

He hecho un ensayo en seco solo con entrenamiento (pseudo-sellado: ajuste hasta 2022Q2, test 2022Q3-2024Q2 y provincias pseudo-selladas 02, 33 y 50). Corre de principio a fin, con 8 periodos objetivo y un DM informativo (n=392; DM 0,84, p 0,43). Puntos:

| Punto | Estado |
|---|---|
| Ventana | Orígenes 2023Q3-2025Q2 → objetivos 2024Q3-2026Q2 (8 periodos). Correcto (sin el defecto de BV) |
| Modelo | B = AR(4) + variables de H1, fijado: fiel al pre-registro |
| Provincias selladas 11, 16 y 45 | Se incluyen, con su historia hasta 2024Q2 sacada de la muestra sellada. **Pero las pendientes se reestiman con las 52 provincias** (`_fit_predict` usa todas las unidades con s+h ≤ L), así que no se usan los parámetros de entrenamiento. El docstring afirma que solo se estima su efecto fijo, y eso es inexacto. Criterio uniforme con BV: pendientes = las de entrenamiento (49 provincias); efecto fijo de cada sellada = media del residuo en su propia historia con objetivos ≤ 2024Q2, igual para B, AR(4) y ECM v1 |
| Regla de decisión | `rmse < rmse_AR4 y DM > 0 y p bilateral < 0,05` en «todas» (52 provincias). Es razonable, pero hay que declararla en decisiones.md ANTES de la llamada como contraste principal único. Los demás (solo train_provs; solo selladas en la ventana; y, como en BV, selladas en toda su historia (b')) son secundarios. Falta además (b') |
| Comprobaciones previas | No hay comprobación de n_periodos ≥ 8 (solo de n ≥ 8 observaciones). Hay que añadirla |
| Ensayo en seco versionado | No existe. Hay que añadirlo (C5) |

## Cambios requeridos (por prioridad)

1. **C1 [bloqueante]** Fusionar r2/main en r2/BA (holdout corregido: pob 2024Q2 anulada, `anulado_fuga_sellado`), reejecutar `ba_run.py` y regenerar todas las salidas. Comprobar que `_step_ln` sigue considerando «observado» solo el T1 y que el número de observaciones de H1 cae en 49 filas.
2. **C2 [bloqueante]** Nivel de evidencia según el criterio uniforme (§3). En ba_informe.py:94-99, sustituir el `or` por el contraste de intersección-unión de H1. `nivel_evidencia = "EXPLORATORIO"` para H1 («no confirmada: falla la conjunción»). Eliminar «ASOCIACIÓN ROBUSTA (provisional)» de resultado.json y resumen.md. Dejar el componente 20-34 como resultado parcial EXPLORATORIO. Llamar «Holm intra-H1» al m=2 y añadir a resultado.json `p_H1_IUT` (unilateral +) para el Holm de la familia de 7 del orquestador.
3. **C3 [bloqueante]** `evaluar_H1`: pendientes estimadas solo con las 49 provincias de entrenamiento (objetivos ≤ 2024Q2), y efectos fijos de 11, 16 y 45 con su propia historia ≤ 2024Q2 (en B, AR(4) y ECM v1). Contraste principal único: 52 provincias, objetivos 2024Q3-2026Q2. Secundarios: 49 provincias; selladas en la ventana; selladas en toda su historia (b'). Comprobación de n_periodos ≥ 8. Corregir el docstring. Declarar en decisiones.md la regla de decisión y que el resultado no puede elevar H1 a ROBUSTA.
4. **C4 [bloqueante]** Test de ensayo en seco de `evaluar_H1` solo con entrenamiento (pseudo-sellado 2022Q3-2024Q2 + 3 provincias pseudo-selladas; mi guion en el scratchpad sirve de modelo), versionado (tests/ o src/v2/ba_test_*.py, fuera de `make models` si es lento). Debe pasar antes de llamar a `holdout.evaluate`.
5. **C5 [alta]** Guarda en `ba_h1_sellado.py`: `if __name__ == "__main__": raise SystemExit("solo vía holdout.evaluate")`.
6. **C6 [alta]** decisiones.md: declarar como decisiones de la rama, cuya fecha previa no se puede auditar, el criterio de signos de las submuestras, el modelo primario B y el presupuesto OOS (4/6).
7. **C7 [media]** Interpolación en el modelo principal: declararla como desviación de la regla «interpolaciones solo en robustez», justificada por el pre-registro trimestral. Que la calificación del componente 20-34 dependa también de las versiones sin interpolar (T1 observado y anual), presentadas en resumen.md con el mismo peso que la principal. Anotar como limitación el retraso de publicación del padrón en el OOS.
8. **C8 [media]** Turismo: BH sobre los 8 contrastes de interés no placebo; aviso «EXPLORATORIO; N_t=6» en signos_vs_literatura.csv; mencionar que la extranjera es negativa y significativa en pre-COVID.
9. **C9 [baja]** signos_vs_literatura.csv: columnas `estado` (VERIFICADA/NO VERIFICADA) y `cuartil` desde docs/literatura.md. En las contribuciones, la frase «descomposición contable, no atribución causal».
10. **C10 [orquestador, infraestructura]** `holdout.evaluate`: registrar un evento «apertura» en _accesos.log antes de leer data/sealed, para que un fallo de `fn` no permita un segundo acceso sin rastro.

Tras C1-C5, basta una re-revisión breve: diff de ba_informe.py y ba_h1_sellado.py, el test y las nuevas cifras de H1. Solo entonces debe ejecutarse `holdout.evaluate("H1", ...)`.
