
## BA (alquiler) — aprobada en re-revisión
- C6: el criterio de signos y la elección del modelo primario fuera de muestra no son auditables como fijados de antemano (no estaban en el pre-registro con ese detalle).
- C7: la población del modelo principal está interpolada intra-anual (T2-T4) y el padrón se publica con retraso: en tiempo real el dato no estaría disponible.
- C8: módulo de turismo con solo 6 periodos y corrección BH parcial; la población extranjera sale con signo negativo en 2008-2019.

## BV (compra) — aprobada en re-revisión
- El secundario (b′) de evaluar_H2 llega a orígenes 2023Q4 y solapa dos trimestres con la ventana sellada.
- Potencia baja en la evaluación sellada; en entrenamiento el modelo pre-registrado C3 es peor que el AR(4) de panel (RMSE 0,0605 vs 0,0418).
- Simultaneidad del crédito con el precio (con el crédito retardado 4 trimestres el coeficiente no es significativo); coste de uso aproximado (sin impuestos ni depreciación).
- No residentes: sin datos provinciales.

## BI (inmigración) — aprobada en re-revisión
- La identificación descansa en las cuotas 2002 de Sudamérica (68 % del peso de Rotemberg), correlacionadas con el tamaño, el precio y el enclave extranjero de 2002: la exogeneidad de las cuotas no es creíble; con los controles GPSS (extranjeros 2002 × año) β_alquiler deja de ser significativo y con todos los controles F = 4,3.
- Los placebos (alquiler y precio pasados sobre el flujo instrumentado de t) rechazan con fuerza: el diseño no separa el efecto del flujo de t de ajustes acumulados o tendencias provinciales (problema de Jaeger, Ruist y Stuhler 2018).
- Las pretendencias 2003-2007 no son pre-tratamiento (boom de llegadas a los mismos enclaves) y no informan.
- 8 agrupaciones de países: BHJ/AKM con poca potencia; Sargan rechaza en la ecuación de precio.
- Submuestra 2009-2014 sin primera etapa (F 0,7); 2015-2021, p=0,073. β_alquiler>0 y H3 quedan EXPLORATORIO; la magnitud (0,8-5) no está identificada.
- Flujos de inmigración provinciales solo hasta 2021-2022: sin evaluación sellada posible.

## BO (oferta y suelo) — aprobada en re-revisión
- H4 inestable y endógena: falla en 2005-2013 y 2014-2023; el IV con desplazadores de demanda no la respalda (J rechaza); el placebo de precio futuro es significativo (ciclo común). EXPLORATORIO.
- Oferta medida con viviendas LIBRES iniciadas/terminadas (no totales); sin licencias municipales.
- Déficit 2021Q1-2024Q2: incluye 14.873 viviendas protegidas SUPUESTAS (ritmo constante) además de las 34.704 observadas; no comparable con el periodo 2021-2025 del BdE.
- Suelo: serie ruidosa; sin señal anticipatoria robusta tras BH/Holm sobre 160 contrastes.
- Panel UE: sin inferencia válida para la comparación de España (un único clúster); el resultado de alquiler (−6) lo producen 2008-2010 y 2021-2023.
- Fuera de muestra: ningún modelo de precio con variables de oferta mejora al AR(4); el de iniciadas mejora (p 0,03) pero no sobrevive a BH.

## BM (modelos) — aprobada en re-revisión
- Ningún modelo con variables (59 configuraciones + 4 LSTM) supera al AR(4) ni al ECM v1 en la validación por bloques de entrenamiento tras BH; el ECM v1 es peor que el AR(4) en los tres objetivos. Importancias (SHAP, permutación, ALE) solo EXPLORATORIO.
- H7: potencia baja (8 orígenes; objetivo nacional con n=8); el modelo elegido para compra provincial ya era peor que el AR(4) en entrenamiento; el contraste principal usa las 52 provincias, no solo las selladas; un aborto con <8 periodos consumiría el acceso.
- El código del BVAR no sigue exactamente lo declarado (verosimilitud marginal) sin efecto en la elección; algunas constantes fijas no declaradas.
- Bloque 5 (factor dinámico, spillovers espaciales) no ejecutado: sin coordenadas en los paneles. Deep learning solo probado en el panel de alquiler (LSTM; resultado negativo frente a LightGBM).
- El umbral de continuidad (0,05) se fijó después del acceso de comprobación declarado por el orquestador (docs/v2/decisiones.md).
