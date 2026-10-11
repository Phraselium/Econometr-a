# Desviaciones y notas (M3b) - 2026-10-11

1. BART: no hay paquete instalado; sustituto declarado = bosque con bootstrap bayesiano (BBF, arboles poco profundos con pesos Dirichlet). No es BART.
2. Bayesiano jerarquico: PyMC y NumPyro no estan instalados; sustituto = MixedLM (statsmodels), pendientes aleatorias por provincia (y1, ln_pib_pc) y componente de varianza por municipio. La prediccion usa efectos fijos mas efectos de provincia (sin efecto municipal).
3. Panel municipal: N=1.708 filas (200 municipios con valor tasado), no 20.000 (los 20.530 son filas del panel, de las que solo 1.909 tienen precio).
4. Validacion: orígenes 2018/2020/2022, embargo 1 año (4 trimestres), validacion de 2 años. Hiperparametros elegidos con bloques espaciales (k-means de centroides, 5 grupos) dentro del entrenamiento: no hay bloque temporal interno (panel anual demasiado corto) y hay fuga por choques comunes dentro del año solo en la seleccion, no en la evaluacion externa.
5. Panel anual: el pliegue 2018 entrena con un solo año de objetivo (2016); DM con 6 periodos, potencia baja.
6. Lineas base: AR y M1b_ADL trimestrales reproducen M1b (3,546 % y 3,509 %). En anual/municipal, AR(1) y ADL(1) con FE de unidad (extension de M1b, que solo valido el trimestral). Se añaden persistencia y, en trimestral, y_{t-4}: la persistencia SUPERA a AR(4), ECM v1 y M1b_ADL en todos los paneles; los ML no la baten con significacion (DM p>0,07).
7. Indice triangulado A23 e IPV INE: sin desagregacion provincial; Notariado solo C. Valenciana: no hay robustez con ellos. Robustez de precio: Registradores (provincia anual).
8. Interpretacion (SHAP, permutacion agrupada, ALE, PDP) sobre LightGBM; descriptiva C4. VIF muy alto (rezagos de y y poblacion/ocupados): atribuciones inestables entre pliegues.
9. Un ejecucion previa con MLP defectuoso (escalado sin recorte) se descarto; las cifras vigentes son las de esta ejecucion.
10. output/v6/M3B/_smoke contiene una ejecucion de humo (SMOKE=1) que no pude borrar por permisos; ignorar.

## Añadida tras la revisión final (N4)
- El ML trimestral de compra usa `tipo_hip_ecb_pct` y `ln_cred_nuevas` (nacionales), `ln_ipc_alq_idx` y `other_l1`, que no están en CP_REG. hipotesis.md §3 excluye las variables nacionales de los modelos provinciales con efectos fijos de año. Aquí no hay efectos fijos de año: los árboles usan esas variables como contexto temporal común. Es una desviación del pre-registro y la interpretación de esas variables es nula (no varían entre provincias).
