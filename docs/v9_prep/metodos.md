# Métodos econométricos recientes aplicables a v9

Tabla completa: [metodos.csv](metodos.csv) (23 métodos). BibTeX en [referencias.bib](referencias.bib).

Fecha: 2026-10-14. Detalle por método en `metodos.csv` (columnas completas). DOI: los marcados «Crossref 2026-10-14» se comprobaron hoy; los marcados «docs/literatura.md» ya estaban verificados en v1-v8 y no se han vuelto a consultar (hay que reflejar los nuevos en docs/literatura.md: M07, M12, M13, M14, M15, M16, M20, M21 y Li et al. 2024). Versiones de librerías: JSON de PyPI consultado hoy; «mantenido» = release en 2026. Cuartil: Scimago devolvió 403; se reutilizan los valores de revista ya registrados en docs/literatura.md.

Todas las fichas son metodológicas: «resultado con signo y magnitud» solo aplica a M21 (cifras del resumen institucional, sin releer el texto).

| id | Método | Referencia | Revista (cuartil) | Python | Usado |
|---|---|---|---|---|---|
| M01 | DiD escalonado CS | Callaway y Sant'Anna 2021 | J. Econometrics (Q1) | csdid 0.4.2; differences 0.3.0; moderndid 0.2.0 | parcial (v3, un momento) |
| M02 | Event study IW | Sun y Abraham 2021 | J. Econometrics (Q1) | pyfixest 0.60.0 (sunab no verificado) | no |
| M03 | DiD por imputación | Borusyak, Jaravel y Spiess 2024 | REStud (Q1) | implementar | no |
| M04 | DiD continuo | Callaway, Goodman-Bacon y Sant'Anna 2024 | NBER WP 32117 (WP; sin versión en revista localizada) | R contdid; Python no verificado | no |
| M05 | Synthetic DiD | Arkhangelsky et al. 2021 | AER (Q1) | synthdid 0.10.1 (baja actividad) | no |
| M06 | Control sintético | Abadie, Diamond y Hainmueller 2010; Abadie 2021 | JASA; JEL (Q1) | pysyncon 1.7.0 | no |
| M07 | SC aumentado | Ben-Michael, Feller y Rothstein 2021 | JASA (Q1) | implementar | no |
| M08 | Honest DiD | Rambachan y Roth 2023 | REStud (Q1) | moderndid; diff-diff (terceros) | no |
| M09-M11 | Shift-share | Goldsmith-Pinkham et al. 2020; Borusyak, Hull y Jaravel 2022; Adão, Kolesár y Morales 2019 | AER; REStud; QJE (Q1) | implementar | sí (diagnósticos; LOO) |
| M12-M14 | RD | Calonico, Cattaneo y Titiunik 2014; Cattaneo, Idrobo y Titiunik 2019/2024; Kolesár y Rothe 2018; Cattaneo, Jansson y Ma 2020 | Econometrica; AER; JASA (Q1) | rdrobust 2.1.1; rddensity 3.0 | no |
| M15 | RD espacial | Keele y Titiunik 2015 | Political Analysis (cuartil no verificado) | rdrobust (distancia) | no |
| M16 | CausalImpact | Brodersen et al. 2015 | Annals of Applied Statistics (cuartil no verificado) | tfcausalimpact 0.0.19 | no |
| M17-M18 | DML; bosques causales | Chernozhukov et al. 2018; Wager y Athey 2018 | Econometrics J.; JASA (Q1) | doubleml 0.11.4; econml 0.17.0 | DML manual (v8) |
| M19 | Proyecciones locales | Jordà 2005; Montiel Olea y Plagborg-Møller 2021; Li et al. 2024 | AER; Econometrica; J. Econometrics (Q1) | implementar | sí (v8) |
| M20 | SVAR signos/ceros | Arias, Rubio-Ramírez y Waggoner 2018 | Econometrica (Q1) | implementar | sí (v8) |
| M21 | Parcial frente a inducido | Sanchis-Guarner 2023 | RSUE (Q1) | implementar | no |
| M22 | Conley | Conley 1999 | J. Econometrics (Q1) | implementar; panelbox (tercero) | sí |
| M23 | WCB pocos clústeres | Cameron, Gelbach y Miller 2008; MacKinnon y Webb 2018; Roodman et al. 2019 | REStat; Econometrics J. (Q1); Stata J. (no verificado) | wildboottest 0.3.2; pyfixest | sí |

## Notas de aplicabilidad (hipótesis de trabajo, no resultados)

- Bono Alquiler Joven (18-35): RD por edad exige microdatos individuales con edad y resultado; con edad en años la variable es discreta (M14). No se localizó evaluación RD publicada del programa (búsqueda 2026-10-14; solo normativa y un estudio de percepción en la UIB).
- Zonas tensionadas: la adopción escalonada por CCAA/municipio permite M01-M03 con M08 como sensibilidad; con 1-2 unidades tratadas, M05-M07 con inferencia por placebo y cautela con M23 (MacKinnon y Webb 2018 advierten de sobrerrechazo con pocos tratados).
- Fronteras (M15): la frontera administrativa suele coincidir con otras diferencias; exigir pruebas de continuidad de covariables.
- Contradicciones/matices: los estimadores M01-M03 difieren en supuestos y eficiencia; si discrepan, se reportan ambos (regla del proyecto). Para inmigración, M21 separa efecto parcial e inducido, lo que matiza las cifras de IV totales de Saiz (2007) y Sá (2015) ya en docs/literatura.md (signos opuestos).
- Las librerías Python de DiD/Honest DiD son de terceros y jóvenes: validar por Monte Carlo (regla V7) frente al paquete R de referencia o a la implementación numpy propia antes de usarlas.
