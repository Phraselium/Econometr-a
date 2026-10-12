# Notas de entorno (orquestador, 2026-10-12)

## Repositorio
- Rama de trabajo r6.2/main en 462ebf1, «v6.2 cerrada». El remoto es la rama claude/housing-price-spain-econometric-95dhj3.
- Etiquetas locales: prereg-v2, prereg-v3, prereg-v5, prereg-v6, v5.0, v5.1, v6.0, v6.1 y v6.2.
- Etiquetas en el remoto: 0. El envío de etiquetas falla (HTTP 403 o el remoto corta la conexión).
- Commits de cierre:

  | Versión | Commit |
  |---|---|
  | v5.0 | cc69e02 |
  | v5.1 | bac2fda |
  | v6.0 | 08d7629 |
  | v6.1 | 7a63f9f |
  | v6.2 | 462ebf1 |

## Entorno
- Python 3.13.16.
- Librerías instaladas:

  | Librería | Versión |
  |---|---|
  | statsmodels | 0.15.0 |
  | linearmodels | 7.0 |
  | lightgbm | 4.7.0 |
  | xgboost | 3.4.1 |
  | shap | 0.53.0 |
  | econml | 0.17.0 |
  | doubleml | 0.11.4 |
  | torch | 2.14.1+cpu |
  | scikit-learn | 1.9.1 |
  | pandas | 3.0.5 |
  | numpy | 2.5.3 |
  | scipy | 1.18.1 |

- No instaladas: pymc, arviz, numpyro, jax, arch, torch_geometric, bartpy, pysal, libpysal y spreg. En v6, BART y PyMC se sustituyeron por alternativas propias (bootstrap bayesiano de bosque, GraphSAGE implementado en torch); ver output/v6/M3A y M4/notas.

## Tiempos y pruebas
- `make all` sin red, un solo hilo:

  | Versión | Ejecución 1 | Ejecución 2 |
  |---|---|---|
  | v6.0 | 7.564 s | 7.776 s |
  | v6.1 | 7.498 s | 6.947 s |
  | v6.2 | 7.928 s | 8.054 s |

  Unas 2 h 10 min por ejecución.
- `make check`: unos 6 min, 89 tests (pytest), más check_texto, check_v5 y check_v6.

## Consumo de subagentes
| Versión | Tokens | Presupuesto |
|---|---|---|
| v6 | 1.541.747 | 2,2 M |
| v6.1 | 1.132.386 | 1,4 M |
| v6.2 | 462.880 | 0,6 M |

Las cifras de v1-v5.1 están en docs/*/estado.md.
