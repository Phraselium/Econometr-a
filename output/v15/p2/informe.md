# E1 · Precio frente a alquiler y coste de uso (panel provincial) · informe
**Resultado (puntual; Westerlund, CIPS y CS-ARDL NO APTOS).** Elasticidad de largo plazo valor tasado–alquiler: CS-ARDL (p = 1, sin coste de uso) 0.64; MG y PMG dan valores distintos y de signo variable (multiverso.csv). La velocidad de ajuste del CS-ARDL (-0.281 trimestral) no es fiable: cobertura 0,003 en el Monte Carlo. No se contrasta cointegración. Capa C4, descriptivo.

## Ficha reproducible {#theta}
`python3 src/v15/p2_fundamentales.py`. 36 especificaciones: {MG, CS-ARDL, PMG} × {0,1,2 rezagos} × {con/sin coste de uso} × {valor tasado provincial, IPV CCAA}. CS-ARDL tasado: θ entre 0.302 y 0.7.

## Semivida {#semivida}
MG y PMG sin coste de uso (valor tasado): semivida mediana ≈ 3,6–4,2 años (puntual). PMG con coste de uso: no identificado (θ en el límite).

## Diagnósticos
CD de Pesaran (Δlog valor tasado): 129 (correlación media 0.501) → fuerte dependencia transversal. CIPS (estadístico, descriptivo): precio -1.73, alquiler -2.21. Fallidas: Westerlund, CIPS y CS-ARDL (NO APTOS); potencia de Westerlund frente a −0,04 no alcanzada.

## Límites
C4 (entrenamiento), `pendiente_sellada`: true. Lenguaje de asociación. Multiplicidad (Holm en H, BH/BY en E) la aplica el orquestador con `p_valores_para_BY` de resultado.json. Desviaciones: docs/v15/desviaciones.md (DV15-B). Semilla 20261010.
