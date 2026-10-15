# V12 · Decisiones (análisis descriptivo: población, propiedad y oferta)

Reglas generales:
- solo análisis descriptivo y contable; ningún modelo causal ni predictivo;
- capas C1 (≥2 fuentes coincidentes en ese nivel), C2 (cotas) y C4 (descriptivo o asociación);
- neutralidad: se describen flujos y condiciones, nunca se atribuyen responsabilidades;
- celdas pequeñas: se respeta «<5» de origen y no se publican cruces con < 10 casos ni con error relativo > 30 %.

## F0
1. **`make check` no escribe ficheros versionados**:
   - `src/v10/web.py` toma la ruta del resumen de `web.RESUMEN`; `tests/v10/test_web.py` construye la web y el resumen
     en un directorio temporal;
   - `src/v12/git_limpio.py` guarda `git status` al empezar `make check` y falla si cambia al terminar;
   - `tests/conftest.py` hace lo mismo para la sesión de pytest; `tests/v12/test_git_limpio.py` prueba el guardia.
2. **Titularidad del Catastro: dos series que NO se encadenan.**
   - **2012-2023 (JAXI):** titulares catastrales; cuenta todos los cotitulares y derechos.
   - **2024-2026 (CSV):** sujetos pasivos del IBI, un contribuyente por inmueble.
   - **Salto nacional 2023 → 2024:** −32,1 % en inmuebles urbanos (33,72 → 22,90 millones). Ratio municipal mediano 0,671 (p10-p90: 0,61-0,74). Es cambio de definición, no variación real. Va marcado en el diccionario de la base.
   - **Ámbito de los tramos:** el nº de inmuebles del titular se cuenta DENTRO de cada ámbito territorial.
     - Comprobación: la suma municipal de viviendas de personas jurídicas con > 100 inmuebles es 139.295 en 2025, frente a 290.427 en el fichero nacional.
     - Consecuencia: la concentración municipal es una cota inferior de la nacional, y los análisis de grandes tenedores usan también los ficheros nacional, autonómico y provincial.
3. **AEAT: declarantes aproximados con rentas de bienes inmuebles = importe ÷ media (2016-2024).**
   - **Error de redondeo:** ≤ 0,5/media (mediana 0,04 %).
   - **Qué incluye el concepto:** alquileres E imputación de rentas de inmuebles no alquilados, así que no mide «caseros». Cuotas > 1 (10 municipio-año) se marcan y no entran en la base.
   - **2013-2015:** otro diseño. Separa alquileres e imputaciones, pero sin media; unidades por verificar; no se usa en cálculos.
