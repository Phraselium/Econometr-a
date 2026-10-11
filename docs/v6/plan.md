# Plan v6 (alquiler y compraventa)

| Módulo | Límite | Corte 80 % | Contenido |
|---|---|---|---|
| G auditoría del repositorio | 0,15 M | 0,12 M | README, MAPA, archive/, comprobaciones, tareas del autor |
| M0 datos y pre-registro | 0,25 M | 0,20 M | medidas de resultado, paneles, diccionario, sellado v6, hipótesis, potencia, `prereg-v6` |
| M1 econometría explicativa | 0,45 M | 0,36 M | FE/CCE/SDM/MG por mercado y nivel; identificación; relación entre mercados |
| M2 incertidumbre de modelo | 0,25 M | 0,20 M | BMA, elastic net con PDS, multiverso, tabla de pesos |
| M3 predicción y ML | 0,45 M | 0,36 M | líneas base, RF, GBM y BART, jerárquico bayesiano, DL solo con N grande |
| M4 comparación y síntesis | 0,25 M | 0,20 M | tabla en la validación sellada, síntesis por variable, fichas y entregables |
| Revisores (tras M0 y al final) | — | — | con cargo a la reserva |
| Reserva de cierre | 0,22 M | — | — |
| **Total** | **2,2 M** | **1,76 M** | La suma de límites (1,8 M) cabe en el total. |

- **Orden:** G → M0 → M1 y M2 en paralelo → M3 → M4. Dentro de cada módulo, primero el alquiler y luego la compra.
- **Validación sellada v6** (src/holdout.py):
  - el último año disponible de cada panel, más 11 provincias (por bloques completos de CCAA, distintas de las CCAA de v2), con sus municipios y distritos;
  - los distritos sellados en v3 se excluyen;
  - `evaluate_v6` abre una vez por modelo.
