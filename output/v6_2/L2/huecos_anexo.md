# Huecos y ambigüedades del anexo (L2, doble implementación a ciegas)

Resultado: 15/15 cifras reproducidas sin leer `src/`. Ningún hueco impidió la reproducción. Las frases siguientes harían la ficha autosuficiente. Capa C4.

1. **A2 (terminadas).** Añadir: «Si una serie protegida no tiene dato en un año, se toma 0.»
2. **A5 (Catastro).** Añadir: «UU(año) = suma de `valor` de todas las filas de `unidades_urbanas_residenciales` con ese `periodo`, sin filtro adicional de régimen ni de municipios.»
3. **A6 (bajas).** Añadir: «Las bajas exactas son 0,002 × 107.057.889 = 214.115,8; el 214.116 es solo la cifra redondeada.»
4. **A7 (IPVA).** Añadir: «El IPVA `Contrato existente` (tabla 59005) tiene base 2021 = 100 y solo cubre 2021-2024; por eso se divide entre 100. El IPVA `Total` es la tabla 59058 (base 2015 = 100). Si dos subconjuntos empatan en tamaño, gana el de menor amplitud.»
5. **A8 (núcleo de precios).** Añadir: «Los candidatos son MIVAU, Notariado y Registradores; el IPV (A23-P1) se excluye de antemano porque su amplitud respecto al resto supera el 15 %.»
6. **A9 (CV).** Añadir: «La clave de cruce es el nombre sin acentos, en minúsculas y cortado en "/" (`Valencia/Valéncia` y `Valencia/València` dan `valencia`). `devuelta` no se filtra.»
7. **A11 (ECV × ECP).** Añadir los nombres de serie: `ecv_pct_hogares_tenencia|Alquiler a precio de mercado|edad_persona_referencia=Total|sexo=Ambos sexos` y `…|Alquiler inferior al precio de mercado|…` en `data/raw/v3/ine_ecv_tenencia_edad_v3.csv`, `periodo == 2021` (15,2 + 2,8).
8. **A12 (convivencia).** Añadir: «En `ine_t65944.json` cada serie tiene un dato por año (`Anyo`, `FK_Periodo` 28); se suman los dos tramos de edad (25-29 y 30-34) por separado para Total e Hijo/a. Los extremos se redondean con `round(x, -3)`.»
9. **A13-A14 (hogares proyectados).** Añadir: «Las colisiones de clave (Navarra, Madrid, Asturias, Murcia, La Rioja: fila de CCAA y de provincia) se resuelven con la primera fila del fichero; ambas son idénticas. La lista de 52 claves sale de aplicar la clave a `clasificacion_provincias.csv:provincia`.»
10. **A15 (B1-H1).** Añadir: «Las columnas de `B1_nacional.csv` son `componente,min,central,max`; la fila `N10` de esa tabla incluye L y no se usa.»
11. **A16-A17 (D1).** Añadir: «Los percentiles son interpolación lineal (numpy por defecto). La clase es la columna `clase_2021_2025`. D1-H11 = clase 1; D1-H12 = clase 2.»

No se detectó ningún error en las cifras publicadas (comparación en `comparacion.csv`).
