# Auditoría V16 fase 1: oferta_suelo (C4, descriptivo)

Script: `src/v16/auditoria/oferta_suelo.py` (SEED=20261010; la parte geométrica tarda unos minutos). Excluye municipios de provincias de la muestra sellada. Detalle en `resultado.json`.

## 1. IMM (INE, nacional mensual, 22 series)
- **Huecos**: solo en 4 series de materiales específicos, todos entre 2019-07 y 2020-06 (calzado 8 meses, equipos eléctricos 6, minerales no metálicos 10, textiles 4): coincide con la pandemia. No se interpolan (correcto). Las otras 18 series están completas (mano de obra 1995-01 a 2026-03: 375 meses; materiales 2012-01 a 2026-03: 171).
- **Fin de serie**: 2026-03 (7 meses de retraso a 2026-10): comprobar si el INE ha publicado meses posteriores antes de usar la ventana final.
- **Rupturas de base**: no hay saltos mensuales >25 %. Las series 2011=100 arrancan en 2012-01 entre 98 y 106 (coherente con la base). IMM1 (mano de obra) está en base julio 1980 (258,6 a 488,4): no comparable en nivel con el resto. Su variación mediana mensual es negativa en enero (-0,47 %) y julio (-0,44 %) y positiva en abril/octubre: patrón de revisiones por convenios, no es error pero impone ajuste estacional si se usa mensual.
- **Atípicos (|z robusto|>5 en variación mensual log)**: se concentran en 2021-2023 (shock de costes): cerámica 2022-01/03, cemento 2022-01 y 2023-02, madera 2022-02, acero 2021-2022, energía 2022-03 (+19 %) y 2026-03 (+18 %), mano de obra 2022-03; focos y luminarias tiene 30 por tener variación casi nula y MAD muy pequeño (2013-04, 2024-09), no es error. Son movimientos reales de precios, no unidades dudosas.
- **Valores repetidos**: plantas (IMM110) repite el mismo valor hasta 47 meses seguidos (actualización probablemente anual o muestra fija): no usar en frecuencia mensual. Textiles y focos, rachas de 6 y 8.

## 2. Red Natura 2000 por municipio (MITECO 2025; 6.498 municipios no sellados; terceros, solo agregados)
- **Rango**: 0 valores fuera de [0, 100]; 0 NaN; el porcentaje guardado coincide con el recalculado (dif. 0). Pero el acotado a [0,100] oculta excesos: el cociente superficie Natura / superficie municipal nunca supera 100 % (exceso máx. 0,0000 %), así que no hay recortes silenciosos. 150 municipios con 100 % y 338 entre 95 y 100 %.
- **Áreas**: ninguna <=0; 4 municipios <50 ha (mínimo 46117 con 2,6 ha) y 2 atípicos intraprovinciales de área (|z|>5); máximo 10037 con 175.144 ha. Conviene contrastar las 4 áreas pequeñas con la superficie oficial del INE (no disponible en el repositorio).
- **Costeros**: el INE trabaja con polígonos terrestres, así que la parte marina de los sitios queda fuera por diseño. Los 576 municipios de frontera exterior (costa más frontera terrestre; no se distinguen con esta geometría) tienen 32,2 % de su área en Natura (mediana 13,7 %) frente a 26,1 % en los interiores (mediana 2,2 %); solo 4 llegan al 100 %. No se aprecia infravaloración sistemática en la costa, pero el indicador no mide protección marina.
- **Suma nacional**: sin los municipios sellados, la suma es 10,66 Mha sobre 39,98 Mha (26,7 %); por provincia, del 3,6 % (52, Melilla) al 45,4 % (12, Castellón). La ficha no recoge la superficie Natura 2000 publicada por MITECO, por lo que no se puede contrastar el total; la cifra de referencia habitual (~27 % de la superficie terrestre) es de memoria y NO VERIFICADA. Para cerrar la comprobación hay que anotar en la ficha el total terrestre de MITECO y compararlo con la suma completa de la capa (cálculo posible fuera de la muestra sellada si se hace con la capa MITECO entera, no con la base de resultados).
- **Cobertura**: 73 códigos sin geometría (52 «PP000» y 21 municipios nuevos) siguen sin valor; ya listados en la ficha.

Nivel de evidencia: DESCRIPTIVO.
