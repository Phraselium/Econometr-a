# H4 · Inmigración y alquiler (shift-share municipal) · informe
**Resultado (puntual, sin p ni IC: AKM y AKM0 NO APTOS).** La población extranjera predicha por cuotas de origen de 2003 se asocia con un alquiler SERPAVI (VC) 0.305 % mayor por punto porcentual (OLS: 0.0684 %), N = 13417 observaciones municipio-año, 1273 municipios, 2012-2022, efectos provincia × año. Instrumento sin UE-14 residenciales. Capa C4; pendiente de evaluación sellada (2022→2025).

## Ficha reproducible {#beta}
`python3 src/v15/p4_inmigracion.py`. Δlog alquiler(t) sobre 100·ΔPobExt(t)/Pob(t−1); instrumento Σ_k cuota_k,2003 · g_kt (leave-one-out), 28 países menos Alemania, Francia, Italia, Portugal y Reino Unido. Multiverso (64): β entre -0.143 y 0.388 % por p.p., mediana 0.0795; signo positivo en 71.9 % de las especificaciones.

## Primera etapa {#F}
F robusto HC1 (descriptivo): 70.2 (rango en el multiverso 49.4–176). El procedimiento MOP/AR/AKM no es APTO; no se declara instrumento fuerte ni débil por inferencia. V9-D4 (provincial, IPC/valor tasado) tuvo F 2,8–4,6: no es comparable (otro nivel y otra medida).

## Rotemberg {#rotemberg}
Orígenes de mayor peso: Colombia (0.35), Bulgaria (0.14), Ecuador (0.12), Marruecos (0.10). Número efectivo de choques (1/HHI): 5.46.

## Diagnósticos (descriptivos)
- Pretendencias SERPAVI 2011-2013 frente al instrumento medio: pendiente -0.0209, correlación -0.0318.
- Balance 2003: corr con log población -0.00745, con cuota extranjera -0.0514.
- Instrumento retardado (JRS): β 0.532 %; sin 5 orígenes de mayor peso: -0.192 %; desbordamiento 15 km: 0.24 %; sin Barcelona y València: 0.308 %; sin 1 % superior de exposición: 0.278 %; 28 orígenes: -0.0734 %.
- Fallidas/no evaluables: AKM, AKM0 y agrupación por provincia (NO APTOS); evaluación sellada (pendiente); TOST (sin inferencia).

## Límites
C4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con `p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.
