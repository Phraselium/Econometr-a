# Revisión independiente · pre-registro V9 (F2)

Fecha: 2026-10-15. Revisor independiente; no ha participado en el trabajo revisado.
Objeto: docs/v9/hipotesis.md (commit sellado 2977349, etiqueta `prereg-v9`), src/v9/f2_potencia.py, output/v9/potencia/mde.csv y src/v9/paneles.py. No se ha leído data/sealed.

## Veredicto: **REHACER** (enmienda acotada al pre-registro, antes de estimar ningún efecto)

El pre-registro es reproducible y no hay fuga en el cálculo de potencia. Hay dos problemas de diseño de capa e inferencia (hallazgos 1 y 2) y varios supuestos de potencia que pueden cambiar qué hipótesis son confirmatorias (3 a 6). Como el documento está sellado, las correcciones deben entrar como **desviaciones fechadas en docs/v9/decisiones.md** y como un addendum al pre-registro con un nuevo commit y etiqueta, **antes** de cualquier estimación de D1-D5.

## Comprobaciones realizadas

- **Reproducción.** El código se extrajo de la etiqueta `prereg-v9` (git archive) a un directorio aislado, con data/ enlazada y sin red (HTTPS_PROXY=http://127.0.0.1:9). Se ejecutó `src/v9/f2_potencia.py` dos veces. Las dos ejecuciones terminan con exit 0 y dan el mismo md5: mde.csv `9e2e455a…6182` y resultado.json `cd3bf3c6…4d84`. El md5 de mde.csv coincide con el fichero versionado.
- **Fuga en la potencia.** No hay fuga.
  - D1 usa placebos solo entre nunca tratados (`placebo_did` recibe `nunca`; f2_potencia.py:90-92 y 101-103).
  - D2-D4 permutan la exposición y D5 permuta el calendario de shocks por bloques. Ninguna rutina usa el contraste entre tratados y controles reales.
- **Fechas de tratamiento** (paneles.py:72-90). Se comprobaron 140 municipios con efecto el 2024-03-16, asignados a 2024T2, y 131 con efecto el 2024-10-10, asignados a 2024T4. Los 61 municipios de la Ley 11/2020 empiezan en 2020T4. La regla de los 45 días se aplica de forma coherente y concuerda con hipotesis.md:62-64 y 89.
- **Agregación de Incasòl por tramos** (paneles.py:43-69). Hay exactamente una fila por municipio y trimestre (19.656 combinaciones con una sola fila). El tramo clasifica al municipio y no se suma entre tramos, así que no hay doble recuento. Los periodos acumulados (gener-juny y gener-setembre) se excluyen del panel anual. Las filas sin renta (19.964) salen del panel de renta y no se imputan.
- **Cruces.** Todos usan el código INE: municipios con 5 dígitos en Incasòl, IDESCAT, zonas tensionadas y padrón, y provincias con 2 dígitos. La correspondencia CCAA→provincia de las comunidades uniprovinciales (paneles.py:191) es correcta. D3 cruza por código postal, como declara el pre-registro.
- **Neutralidad.** No se nombran partidos ni personas como objeto de evaluación. Se evalúan normas (Ley 11/2020, Ley 12/2023) y estimaciones (proyecto, Banco de España, OCDE).

## Hallazgos

1. **ALTA · Promoción de capa en F4 y lenguaje atributivo sobre resultados C4.** hipotesis.md:30 y 257-262.
   - **Problema.** F4 convierte efectos «C3 o C4 robustos» en cotas C2 de «contribución atribuible por factor», calculadas como efecto × exposición. Una asociación C4 pasa así a una capa superior (C2) e implica una interpretación causal por debajo de C3/C3s. Esto contradice «Nunca promover de capa» y «Nada sube de capa por robustez» (hipotesis.md:28).
   - **Otros problemas del mismo bloque.**
     - El adjetivo «robusto» se define con p de BH < 0,10, que es el umbral exploratorio.
     - La línea 30 habla de «equilibrio general» y la 261 de «equilibrio parcial».
   - **Corrección.** Limitar F4 a efectos C3/C3s que hayan superado todas las pruebas.
     - Si se quiere conservar algo de C4, presentarlo como «escenario ilustrativo C4, no atribución». Debe ir sin la palabra «contribución» ni «atribuible».
     - Construir las cotas C2 con supuestos explícitos al estilo Manski, no con el IC de una asociación.
     - Unificar la advertencia: equilibrio parcial.

2. **ALTA · D1a renta: 23 controles nunca tratados frente a 208 tratados. El placebo de territorio pre-registrado es inviable y la potencia se extrapola.**
   - **Dónde.** hipotesis.md:36, 67-69 y 83; mde.csv, fila D1a renta (controles = 23, k_pseudo = 11); f2_potencia.py:51-71.
   - **Placebo inviable.** La prueba 4 pide 500 asignaciones aleatorias del tratamiento entre nunca tratados, pero no se pueden asignar 208 pseudo-tratados entre 23 municipios. Además, la prueba no fija un umbral de superación, a diferencia de las pruebas 1 y 3.
   - **Potencia extrapolada.** El MDE (0,037 frente a la referencia de 0,05) sale de 11 pseudo-tratados entre 23 controles. El factor sqrt((1/n_t+1/n_c)/(1/k+1/(m−k))) supone errores iid y homogéneos entre municipios tratados (mayores) y no tratados (menores). Esa extrapolación determina que H1a-renta sea confirmatoria.
   - **Inferencia.** Con 23 conglomerados de control, el bootstrap salvaje por conglomerados de CS con nunca tratados tiene un tamaño poco fiable.
   - **Corrección.**
     - Redefinir la prueba 4: permutación de etiquetas sobre el conjunto tratados + nunca tratados, o placebo con el mismo número de unidades que el grupo de control. Fijar el umbral (por ejemplo, p de permutación < 0,05 del ATT real).
     - Recalcular la potencia con un método que no dependa del factor iid. Por ejemplo, simulación de datos nulos con remuestreo por bloques de los residuos de los nunca tratados, con el tamaño real n_t/n_c.
     - Pre-registrar como principal la variante con «aún no tratados», o declarar H1a-renta exploratoria si el MDE recalculado supera 0,05.

3. **MEDIA · Las familias de Holm del pre-registro no coinciden con la m usada en la potencia.**
   - **Dónde.** hipotesis.md:19-22 frente a f2_potencia.py:93, 104, 146 y 213.
   - **Problema.** El código usa m = 4 en D1, D2 y D4. Las familias declaradas tienen 3 hipótesis (D1), 2 (D2) y 1 (D4). Es conservador y no cambia ninguna clasificación: lo he comprobado para D1b contratos con m = 3 (MDE 0,103 > 0,10) y para D4 réplica del valor tasado con m = 1 (0,0122 > 0,01). Aun así, el pre-registro y el código deben coincidir.
   - **Corrección.**
     - Usar la m de cada familia.
     - Documentar la regla de cierre: la familia se fija con la m máxima posible y no se reduce a posteriori.

4. **MEDIA · Las referencias de magnitud que deciden el estatus confirmatorio no están en las mismas unidades que el MDE.**
   - **Dónde.** hipotesis.md:37, 41-42 y 47; f2_potencia.py:96, 149-150 y 216.
   - **D2.** La referencia 0,019 (LA01) es el efecto del nivel medio de anuncios de Airbnb en un barrio de Barcelona. El MDE está en «1 DE de plazas HUT por cada 100 habitantes entre municipios catalanes» y mide un shock COVID, no la entrada de oferta. Las dos magnitudes no son comparables sin conversión.
   - **D1a contratos.** La referencia 0,10 no tiene fuente: LB01 informa de que no hay caída de la oferta, no de una magnitud de 10 %.
   - **D4.** La referencia 0,01 de LA09 es estructural (1 % por cada 1 % de población). El MDE es de forma reducida por punto de Z, así que habría que multiplicar la referencia por la primera etapa esperada.
   - **Corrección.**
     - Convertir cada referencia a las unidades del MDE y documentar la conversión.
     - Si no hay fuente para H1a-contratos, declararla exploratoria.

5. **MEDIA · Las permutaciones iid de la exposición en D2 y D4 ignoran la dependencia espacial y la de shift-share. Es probable que los MDE sean optimistas.**
   - **Dónde.** f2_potencia.py:139-144 y 211.
   - **D4.** La inferencia confirmatoria pre-registrada usa AKM (hipotesis.md:195), cuyos errores suelen ser mayores que los de una permutación provincial iid. El margen de H4-réplica-alquiler es estrecho: MDE de Holm 0,0074 frente a 0,01. La regresión de potencia omite además los controles pre-registrados (log de la población inicial y suma de cuotas).
   - **D2.** Las dosis HUT están concentradas geográficamente (costa y área metropolitana).
   - **Corrección.**
     - D4: recalcular el MDE con el error AKM, o con permutación de los shocks nacionales por país, incluyendo los controles.
     - D2: usar permutación restringida dentro de comarca o provincia.
     - Si cualquiera de los dos supera la referencia, reclasificar la hipótesis como exploratoria.

6. **MEDIA · D3 incumple la regla común de exclusión posterior al pre-registro y compara un año parcial con uno completo.**
   - **Dónde.** hipotesis.md:11 frente a 139 y 145; paneles.py:134-154.
   - **Problema.**
     - El corte VUT del 2026-10-14 y el fichero de fianzas de la GVA de 2026 son posteriores a 2026-07-01. El fichero de 2026 está descargado el 2026-10-10, es parcial según docs/v5/fuentes_fallidas.md:28 y no tiene mes ni columna `posterior_prereg`.
     - El número de fianzas de 2026 (28.381) se compara con el de 2024, un año completo (32.838). El Δ log del número de fianzas mezcla la cobertura parcial con la variación real y puede diferir por código postal si la estacionalidad difiere.
     - La columna `devuelta` no se usa: no se distingue entre flujo y stock.
   - **Corrección.**
     - Declarar en el pre-registro la excepción explícita a la regla de la línea 11 para D3, o usar 2025 como año final.
     - Usar Δ de cuota (o un resultado normalizado por el total provincial del año).
     - Documentar el tratamiento de `devuelta`.

7. **MEDIA · Faltan criterios de superación y pruebas de sensibilidad en D2 y D4.**
   - **Dónde.** hipotesis.md:122-126 y 192-197.
   - **D2.** El placebo de permutación de la dosis (500) no tiene umbral. A diferencia de D1a, no hay prueba de sensibilidad a tendencias (Honest DiD o equivalente).
   - **D4.** No hay placebo de periodo previo con resultado anterior a 2003. El único contraste de pretendencia es Δ log P 2002→2003 para las cuotas de los cinco países con mayor peso de Rotemberg.
   - **Corrección.** Fijar los umbrales y añadir:
     - Honest DiD o una cota de tendencia lineal por dosis en D2;
     - un placebo con resultado previo en D4, o declararlo inviable.

8. **BAJA · Inconsistencias en D1c.**
   - **Dónde.** hipotesis.md:40 y 106 («≤ 9 controles») frente a f2_potencia.py:109 y 119 («≤ 7»). mde.csv muestra 9 controles.
   - **Problema.** De los 11 «tratados», 4 tienen 0 trimestres posteriores: 20040, 20055, 20071 y 48015.
   - **Corrección.** Unificar la cifra de controles e informar de 7 tratados con al menos un trimestre posterior.

9. **BAJA · El instrumento D4 usa 28 países, no los 26 declarados.**
   - **Dónde.** hipotesis.md:165 frente a la salida de `instrumento()` (f2_potencia.py:184-185).
   - **Detalle.** Quedan 28 nacionalidades individuales. Las cuotas cubren el 87 % de los extranjeros en 2003 y en 2012.
   - **Corrección.** Corregir la cifra y anotar la cobertura.

10. **BAJA · D1b remite a «las pruebas de D1a», pero la ventana solo permite e ∈ [−7, −2].** hipotesis.md:95-96 frente a 80.
    - **Corrección.** Especificar la ventana de pretendencias de D1b.

11. **BAJA · Formulaciones con carga causal en diseños que no son C3.**
    - **D5** (hipotesis.md:208, C4): «¿Responden más los precios…?» → «¿Es mayor la variación de precios asociada a los shocks…?».
    - **D2** (hipotesis.md:133): el mecanismo «porque las HUT pasan al alquiler residencial» debe presentarse como hipótesis de mecanismo no contrastada.
    - **D7** (hipotesis.md:238): «efecto población» → «componente población» (descomposición contable).
    - **D4** (hipotesis.md:158): condicionar «¿Cuánto suben…?» a que se superen los diagnósticos C3.

12. **BAJA · Estado de verificación de las referencias.** hipotesis.md:85, 100, 135, 204, 248-249.
    - **Problema.** Solo LA21 y la referencia de D5 llevan la marca NO VERIFICADA. Las demás aparecen sin estado ni cuartil, aunque docs/v9_prep/literatura.csv sí los tiene (por ejemplo, LA09 está VERIFICADA y es Q1). LB03 (Fedea) y LA18 (BdE) no tienen cuartil aplicable.
    - **Corrección.** Añadir VERIFICADA / NO VERIFICADA y el cuartil, o «no aplica».

13. **BAJA · Mezcla de fuentes en el valor tasado de D4.** paneles.py:190-197.
    - **Problema.** Para las CCAA uniprovinciales se toma `p_tasado` del panel v1 de CCAA. Es un relleno desde otra fuente; está marcado en `valor_tasado_origen`, pero hipotesis.md:176 no lo cita como tal.
    - **Corrección.** Declararlo y añadir una robustez sin esas 7 provincias.

## Lo que no requiere cambios

- **D6.** Su exclusión por falta de mes de nacimiento en la ECV está razonada.
- **D7.** Es contable, sin p-valores, y respeta la regla v5.1.
- **D5.** Está correctamente fuera de C3s porque el MDE de Holm (0,117 a 0,152) supera la referencia (0,05).
- **Diseños sin potencia.** Ninguno figura como confirmatorio (D1b contratos, D1c, D2 contratos, D3, D4 valor tasado, D4 ampliación y D5).
- **Semilla.** Se usa la misma en todo el cálculo de potencia (B = 300, declarado en resultado.json).

## Re-revisión A1

Fecha: 2026-10-15.

**Objeto.** docs/v9/hipotesis_addendum_a1.md (commit 9cb2200, etiqueta `prereg-v9-a1`), src/v9/f2b_potencia_addendum.py, output/v9/potencia/mde_addendum.csv y la desviación E3 en docs/v9/decisiones.md. No se ha leído data/sealed.

**Reproducción.** Se ejecutó f2b_potencia_addendum.py desde `git archive 9cb2200` en un directorio aislado y sin red, dos veces. Las dos ejecuciones terminan con exit 0 y dan el mismo md5 de mde_addendum.csv (`d4940…e973`), que coincide con el fichero versionado.

### Veredicto: **APROBAR**

Quedan observaciones de gravedad baja que deben resolverse al estimar, no en la puerta.

### Estado de los hallazgos 1-13

| # | Estado | Comprobación |
|---|---|---|
| 1 | Resuelto | A1.7 limita F4 a C3/C3s. Las cotas son de Manski con supuestos explícitos. Si no hay C3, la tabla dice «no identificado». Los resultados C4 solo pueden aparecer como escenario ilustrativo, sin «contribución» ni «atribuible». La advertencia es única: equilibrio parcial. |
| 2 | Resuelto | **Prueba de territorio.** Ahora es una aleatorización de Fisher sobre tratados + nunca tratados, con umbral p < 0,05, y es exigida para C3. **Potencia.** Simulación nula con n_t = 199 y n_c = 20 reales y bloques de residuos previos: MDE de Holm 0,041 ≤ 0,05. |
| 3 | Resuelto | La familia de Holm es {H1a-renta, H1b-renta}, m = 2. La potencia usa m = 3, que es conservador. La regla de cierre está declarada. |
| 4 | Resuelto | H1a-contratos y D2 pasan a exploratorias. La referencia de D4 está ahora en unidades de forma reducida (0,01 × π̂). |
| 5 | Resuelto | D2 usa permutación dentro de provincia. D4 usa AKM con la nula impuesta y controles; H4 pasa a exploratoria (0,0079 > 0,0040). |
| 6 | Resuelto | El año final del resultado es 2025, con Δ de cuota provincial. La excepción de la exposición está declarada y el tratamiento de `devuelta` está definido. |
| 7 | Resuelto | Hay umbrales en D2. La sensibilidad de D2 es una tendencia lineal por dosis. El placebo previo de D4 se declara inviable y está razonado. |
| 8 | Resuelto | D1c: 7 municipios con al menos un trimestre posterior y 9 controles. |
| 9 | Resuelto | 28 nacionalidades, con una cobertura del 87 %. |
| 10 | Resuelto | Pretendencias de D1b en e ∈ [−7, −2]. |
| 11 | Resuelto | Las formulaciones de D5, D4 y D7 están reescritas y el mecanismo de D2 queda como no contrastado. |
| 12 | Resuelto | Cada referencia tiene estado y cuartil, o «no aplica». |
| 13 | Resuelto | El relleno uniprovincial está declarado y hay robustez sin esas 7 provincias. |

### Problemas nuevos

**Fuga.** No hay fuga material. La simulación de D1a usa residuos de las unidades tratadas, pero solo de 2019T1 a 2024T1 y sin el contraste entre tratados y controles. La primera etapa de D4 no usa el resultado. Ninguna hipótesis sin potencia figura como confirmatoria, y no hay promoción de capa.

**Observaciones bajas** (resolver en la fase de estimación; no bloquean):

- **A1-a · Ventana previa de D1a** (f2b_potencia_addendum.py:49).
  - **Problema.** La ventana «previa» incluye 2024T1. La cohorte de 140 municipios tiene efecto desde el 2024-03-16, así que esos residuos incluyen unas dos semanas tratadas.
  - **Además.** La misma ventana incluye 2020T4-2022T1 de la Ley 11/2020 para 61 municipios. Este efecto infla la varianza, lo que es conservador.
  - **Corrección.** Recalcular como sensibilidad con la ventana 2019T1-2023T4 e informar del MDE. Si superase 0,05, H1a-renta pasaría a exploratoria, y eso debe anotarse en decisiones.md **antes** de estimar.
- **A1-b · Factor de escala en H1b-renta.** El factor iid no es estrictamente conservador: con 60 pseudo-tratados entre 181 controles, el factor es aproximadamente 0,94. El margen del MDE (0,025 frente a 0,05) absorbe esta diferencia. Conviene corregir la frase del addendum.
- **A1-c · Desfase temporal en D3.** El resultado (2024→2025) es anterior a la mayor parte de la exposición (ΔVUT entre 2025-01 y 2026-10). Debe decirse expresamente en la presentación descriptiva. No se puede leer como respuesta a la caída del registro.
