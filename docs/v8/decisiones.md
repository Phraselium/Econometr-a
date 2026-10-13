# Decisiones V8 (Y = decisión de V8)

- **Y0.** V8 parte de r7.2/main.
  - F0 estaba casi completo en v7.2 (retirada de cifras superadas, dosis de construcción, ficha de burbuja, test). Aquí solo se añade el rótulo del marcador de fecha de publicación.
  - La v7.1 sigue siendo la referencia y la v7.2 es su corrección, con ERRATA.
- **Y1. Capas de V8:**
  - C1: hechos;
  - C2: cotas;
  - C3: identificación por un instrumento externo o por un diseño que supera sus pruebas;
  - C3s: identificación por supuestos estructurales explícitos (restricciones de signo), solo con los supuestos declarados;
  - C4: exploratorio o asociación.
  
  El lenguaje causal solo se admite en C3 y C3s, y en C3s siempre condicionado a los supuestos.
- **Y2.** No está instalada la biblioteca de EBM (interpret). Se usa un GAM con splines de statsmodels (GLMGam) como modelo aditivo interpretable, y no se añade ninguna dependencia nueva.
