# E2-R1 · réplica ciega V18; capa C4

Ley 11/2020 de Cataluña, Incasòl municipio-trimestre 2019T1-2022T1, ln de la renta media de contratos nuevos. Código: src/v18/replica/e2_r1.py (SEED 20261010). Clasificación V18: no se clasifica (réplica ciega); nivel_evidencia EXPLORATORIO.

## Resultado

| | Réplica ciega | Orquestador |
|---|---|---|
| Coeficiente (Reg x Post) | -0,0378 | -0,038 |
| IC95 | [-0,0499; -0,0256] (Webb, percentil-t); CR1 municipio [-0,0499; -0,0256] | [-0,051; -0,026] |
| Diferencia | +0,0002 absoluta; 0,5 % relativa | |
| Error típico (CR1, municipio) | 0,0062 | |

Cada estimación cae en el IC95 de la otra. Veredicto: **coincide** (diferencia < 10 % del coeficiente y dentro del error).

## Muestra y decisiones

- Tratados: 49 municipios de la Ley 11/2020 tras quitar Barcelona ciudad y exigir panel equilibrado (renta y contratos en los 13 trimestres). Controles: 93 municipios no regulados con crecimiento anual compuesto de la renta anual 2014 a 2019 superior al 4,15 %. Mínimo de la adenda 1.3 (30 y 30) cumplido. N = 1.846 (142 municipios x 13).
- Posterior = 2020T4-2022T1; anticipación 2020T3 (coeficiente +0,0136, EE 0,0108).
- Covariable: ln paro registrado (SEPE, media trimestral de los meses). Sin covariables: -0,0375. Sin 2020T1-2020T3 (v1): -0,0377.

## Lecturas que admitía el texto y cómo se resolvieron

1. **Agrupación.** La adenda fija comarca (42) con Webb como inferencia alternativa; no hay correspondencia municipio-comarca en el repositorio. Se usó cluster por municipio, con CR1 y con wild cluster bootstrap de Webb (9.999). Un cluster por comarca ensancharía el IC.
2. **Crecimiento 2014-2019.** Lo he leído como tasa anual compuesta 2014-2019 (2019 = media de los cuatro trimestres ponderada por contratos). Una tasa media de variaciones anuales daría otro grupo de control.
3. **Población y ERTE.** Población municipal 2019-2022 no está en la base y ERTE tampoco: se omiten. La estimación casi no cambia sin covariables.
4. **Entradas y salidas del régimen / parcialmente tratados.** El fichero no las identifica: no se excluyen.
5. **Paro.** Anual de la base no tiene 2020; se usó el mensual del SEPE (mismo dato, regla 1.4 f).
6. **Base 2019T4:** en la DiD agrupada es irrelevante; no hay estudio de eventos en esta réplica.

Episodio histórico: nunca C3. Sin pretendencias, Honest DiD ni placebos (fuera del alcance de la réplica ciega de la cifra principal).
