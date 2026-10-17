# Q3 · Inmigración: valor tasado, compraventas y barrio (V16, fase 6)

**Capa C4. Asociación C4; pendiente de evaluación sellada. Sin lenguaje causal.** Datos: solo entrenamiento. Desviaciones de operativización: docs/v16/desviaciones.md (D2). Registro: output/v16/q3/registro.csv.

## Resultado
| Diseño | Estimación | Inferencia | Lectura |
|---|---|---|---|
| Q3-c1 (log valor tasado, 38 prov., 2011-2022) | 0,0119 log por punto (≈ 1,19 % por punto) | solo puntual (AKM/AKM0 NO APTOS) | 1,19 veces la referencia de Saiz (0,01); descriptivo |
| Q3-c2 (log compraventas, 41 prov.) | -0,0282 log por punto | solo puntual | signo negativo; sin referencia comparable |
| Q3-b (Δlog SERPAVI 2021-24, 9916 secciones) | 0,0091 por DT (IC 95 % Conley 2 km 0,0060 a 0,0122; p = 7.6e-09) | Conley 2 km, solo escenario principal | correlación; **pretendencia placebo no nula** |
| BLP/GATES (Q3-b) | GATES Q4-Q1 = 0,0002; ganancia de R² dentro = 0,0021 | NO APTO: solo puntual | sin heterogeneidad apreciable |

Multiverso (resumen, sin IC): Q3-c1 16 especificaciones, mediana 0,0078 por DT, 100 % con el mismo signo; Q3-c2 16, mediana -0,0181, 100 %; Q3-b 6, mediana 0,0058, 100 % (variantes puntuales).

## Pruebas
- Superadas: Q3-b: Conley 2 km APTO solo en el escenario principal; Q3-b: sin grandes ciudades, mismo signo (0,0104 por DT); Q3-b: Cinelli-Hazlett RV_q=1 = 0,0586 (≥ 0,05); Q3-c1/c2: sin grandes ciudades, mismo signo; Q3-c1: pendiente previa 2003-2008 pequeña frente al efecto.
- Fallidas: Q3-b: pretendencia placebo 2018-2021 = 0,0051 por DT (IC Conley 0,0005 a 0,0097) excluye el 0; Q3-b: no robusto a la sensibilidad del rango espacial (radios 0,5 y 1,5 km no pasan); Q3-c: F efectivo no evaluable con herramienta APTA; en V9-D4 fue de 3,4 a 3,7 (< 10); Q3-c1: estimación inestable al controlar por el instrumento retardado (de 0,0119 a 0,0077).
- No evaluables: AKM, AKM0 (NO APTOS); BLP/GATES (NO APTO): solo puntual; TOST (sin magnitud en Q3-b; sin SE en Q3-c); desbordamientos a 15 km (no aplica a escala provincial, D2); Honest DiD / raíces unitarias con dependencia transversal (CIPS NO APTO): no aplican a una forma reducida con efectos fijos.
- Sensibilidad: Q3-b Oster δ = -14,2 (negativo: los efectos fijos acercan la estimación a un valor mayor, no frágil por la regla δ < 1); E-value del punto 1,41 (límite del IC 1,32). Q3-c1: δ = -95,1, E-value 1,61.
- Balance Q3-b con FE de municipio (coeficiente estandarizado por DT de cuota): renta ADRH -0,50, población 0,11, % vivienda turística 0,39: desbalance notable en renta y vivienda turística (sin umbral pre-registrado).
- Rotemberg (Q3-c): Rumanía 0,475, Reino Unido 0,157; suma de pesos negativos -0,056. Primera etapa descriptiva (coef. 0,89, R² dentro 0,47); F efectivo con herramienta APTA no disponible.
- Moran de residuos: provincial I = -0,067; secciones I = -0,048 (efecto de la demedia por municipio).

## Regla de hallazgo
(a) q ≤ 0,10: pendiente del control BY global (único p-valor propio: Q3-b). (b) Q3-b no tiene magnitud de referencia; Q3-c carece de SE válido: errores S y M no evaluables. (c) sellada: pendiente. **Sin hallazgo.** TOST: «no concluyente».
Frente a la conclusión publicada V9-D4 (instrumento débil, C4): ninguna contradicción de dirección; no hay parada D.

## Fichas reproducibles
Comando: `python src/v16/q3_shiftshare.py && python src/v16/q3_seccion.py && python src/v16/qb_informe.py` (SEED 20261010).
- <a id="q3-c1"></a>**q3-c1.** x_pt = 100·Σ_o F_{po,2003}·(N_{o,t,-p}/N_{o,2003,-p})/Pob_{p,2003} (28 orígenes; padron_pob_nacionalidad provincial); log valor tasado anual (base_precio) ~ x + FE provincia + FE año, 2011-2022, N = 451. Rango = 8 especificaciones con x en puntos (orígenes, año base 2003/2004, efectos temporales).
- <a id="q3-c2"></a>**q3-c2.** Igual con log compraventas provinciales anuales (INE ETDP 6150, total de vivienda), N = 492.
- <a id="q3-b"></a>**q3-b.** Δlog de la mediana €/m² SERPAVI (tipología VC) 2021→2024 ~ cuota de extranjeros 2022 estandarizada + FE municipio; Conley 2 km (núcleo de Bartlett), secciones de entrenamiento (`unidad_sellada_v16`), municipios con ≥ 2 secciones. Rango = 6 variantes puntuales.
- <a id="q3-blp"></a>**q3-blp.** Interacciones exposición × {renta ADRH 2019, población 2022, cuota extranjeros, % VUT 2021-02, obra per cápita 2018-21}; GATES por cuartiles con 2 mitades por municipio.
- <a id="q3-rotemberg"></a>**q3-rotemberg.** α_o = Σ c̃_o·B̃ / Σ B̃², c̃ residualizado en FE (output/v16/q3/q3c_rotemberg.csv).
- <a id="q3-pretendencia"></a>Pretendencia: igual que q3-b con Δlog 2018→2021.
