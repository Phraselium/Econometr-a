# V16 · Q7a · Bono Alquiler Joven, diferencia en discontinuidades (grupo A, entrenamiento)

**Capa C4, descriptiva, pendiente de evaluación sellada.** Sin lenguaje causal ni intervalo (no se usa Kolesár-Rothe porque no se muestra ninguno). Fecha de corte 2026-10-17.

## Diseño
Inquilinos de mercado (ECV), edad del sustentador principal entre 35−h y 35+h; corte entre 35 y 36 años; antes = 2018-2021, después = 2023-2025 (2022 fuera). Lineal local con pendientes por lado y periodo, pesos DB090. Anchos 3, 5 (principal) y 7; resultados: log del alquiler mensual (HH060) y alquiler anual / renta del hogar.

<a id="v16-q7-1"></a>
## Resultado
- Principal (±5, log alquiler): **-0,120** (≈ -11,3 %). Salto antes 0,082, después -0,038. Hogares: antes 2358, después 2703.
- Anchos 3/5/7: 3: -0,148, 5: -0,120, 7: -0,136. Alquiler / renta: 3: -0,039, 5: -0,013, 7: -0,011 (proporción de la renta).
- Cota de incidencia con cobertura plena: 13.9 %; la potencia está en el límite (MDE 13,2 %).

<a id="v16-q7-2"></a>
**Umbrales placebo:** 31|32: -0,053, 39|40: -0,135. Son del mismo orden que el principal: no hay separación entre señal y ruido.

<a id="v16-q7-3"></a>
**Proporción de inquilinos en el corte:** diferencia en discontinuidades -0,046.

## Plan Estatal 2018-2021 (punto 8 de la adenda)
BOE-A-2018-3358 (RD 106/2018), capítulo IX, programa de ayuda a los jóvenes (2026-10-17): ayuda al alquiler para quien tiene «menos de treinta y cinco años» en el momento de solicitar, con ingresos limitados. **Sí tenía un programa para menores de 35 años**, así que la diferencia en discontinuidades mide un CAMBIO de generosidad entre el Plan 2018-2021 y el Bono Alquiler Joven (hasta 35 años inclusive), no el efecto de un programa nuevo; el corte legal difiere en un año (34|35 frente a 35|36) y la edad de la ECV es la diferencia de años de nacimiento.

## Diagnósticos (superados y fallidos)
| Prueba | Estado | Detalle |
|---|---|---|
| Q7a · umbrales placebo (31|32 y 39|40, ±3) | informativa (sin umbral pre-registrado) | -0,053 y -0,135 frente a -0,120 del principal: del mismo orden |
| Q7a · balance de covariables en el umbral (diferencia en discontinuidades) | informativa | ln_renta_hogar -0,023; n_pers 0,297; extranjero -0,089 |
| Q7a · proporción de inquilinos en el umbral | informativa | salto antes -0,009, después -0,054, diferencia -0,046 |
| Q7a · densidad por edad (edad discreta) | informativa | razón de hogares de edad 35/36: antes 1,06, después 0,93; McCrary no aplica con edad entera |
| Q7a · Plan Estatal 2018-2021 con programa para menores de 35 | informativa (cambio de generosidad) | sí: RD 106/2018, programa de ayuda a los jóvenes («menos de treinta y cinco años»); la diferencia en discontinuidades mide un cambio de generosidad, no un programa nuevo |
| Q7a · anchos 0,5× y 2× del óptimo; rdrobust | no aplica | edad discreta de 11 valores: anchos de 3, 5 y 7 años declarados; sin rdrobust (en RD difuso/dif-en-disc no validado) |
| Q7a · intervalo de Kolesár-Rothe | no mostrado | no se muestra ningún intervalo |
| Q7a · sensibilidad a confusores (Oster, Cinelli-Hazlett, E-value) | no evaluable | sin errores típicos ni controles en el diseño de corte |
| Q7a · exclusión de grandes ciudades e islas | no aplica | la ECV no lleva provincia (solo NUTS2) |

## Límites
Descriptiva. La edad no asigna el bono por sí sola (renta, contrato, límites de precio). Potencia en el límite (MDE 13,2 % frente a cota de 13,9 %). El corte legal del Plan 2018-2021 (<35) difiere en un año del Bono (≤35). Sin magnitud de referencia numérica creíble → (b) no se cumple. Lista de p-valores: vacía. Ficha reproducible: `python3 src/v16/q7_bono.py` (ECV 2018-2025 en data/raw/v9/ine_microdatos/ecv y v16/renta_parque/ecv; extracto output/v16/q7/hogares_edad_28_42.parquet).
