# E2 · Topes al alquiler · resumen de la fase 1 (bibliotecario, grupo A, 2026-10-20)

Criterios: docs/v18/bib/criterios.md (sin cambios). Todas las fichas están en «NO VERIFICADA». Cifras tal como las dan los autores y con la versión leída indicada en cada ficha.

## Tabla

| clave | diseño | país | periodo | efecto | unidad | error | paquete |
|---|---|---|---|---|---|---|---|
| jofremonseny2023 | DiD y estudio de eventos con registro de contratos, 148 municipios | España (Cataluña) | 2020-2022 (25 trimestres) | renta −4,4 a −4,5 % (resumen: −4 % a −6 %); contratos sin cambio | log de la renta media; log de contratos por 1.000 habitantes | 0,006 (renta); 0,021 (contratos) | no |
| monras2023 | DiD a nivel de contrato con precio de referencia; distribución del precio en exceso | España (Cataluña) | 2016-2021 | log precio −0,058 (con efectos fijos de unidad −0,080); contratos nuevos −0,207 (MCO) y −0,111 (PPML); oferta −10 % | log del precio; log del número de contratos | 0,014; 0,021; 0,018 | no |
| abel2024 | DiD y eventos con anuncios de Fotocasa | España (Cataluña) | 2020-2022 | anuncios de alquiler −0,324; anuncios de venta +0,178; renta media sin efecto significativo | log del número de anuncios | 0,068; 0,040 | no |
| perezgarcia2026 | DiD, eventos y PSM con datos públicos de la Generalitat | España (Cataluña, zonas tensionadas 2024) | 2022-2025 | crecimiento de renta −0,0298 (n. s. con PSM); contratos −6,6 por 10.000 habitantes (≈ −13 %) | puntos de crecimiento de la renta; contratos por 10.000 habitantes | 0,0113; 1,135 | no |
| pinto2026 | descriptivo (contexto) | España (Cataluña, Madrid, resto) | 2024 T1-2025 T4 | renta +5,7 % Cataluña frente a +8,5 % Madrid y +10,8 % España; anuncios −20,5 % Cataluña | % acumulado | sin error | no |
| hahn2021 | DiD con GAM hedónico, viviendas sujetas frente a exentas | Alemania (Berlín) | 2019-2020 | −0,113 (estrategia A) y −0,075 (B) en renta anunciada; sin efecto por el anuncio | log de la renta anunciada | 0,019; 0,022 | no |
| mense2019 | DiD escalonado y RDiT | Alemania | 2015 | nuevas viviendas (libres) +0,038; existentes −0,018 | log de la renta | 0,015; 0,006 | no |
| kholodilin2026 | DiD escalonado robusto (CS, SA, Gardner) | Alemania (≈ 11.000 municipios) | 2010-2024 | terminaciones totales −0,109 a −0,475 | log de terminaciones + 1 | solo niveles de significación | no |
| breuille2025 | DiD con SeLoger y PSM | Francia (París y cinco ciudades) | 2018-2024 | −5,0 % (−0,051) en la renta por m²; sin caída duradera de anuncios | log de la renta por m² | 0,007 | no |
| morin2025 | DiD, anuncios SeLoger | Francia (París) | 2018-2023 | −3,7 % a −4,2 % | % de la renta | no leído | no |
| toussaint2025 | DiD (solo resumen) | Francia (Lille) | 2020- | rentas de viviendas grandes al alza; retornos de capital a la baja | sin cifra | no | no |
| otoole2023 | DiD y corrección de error (solo resumen) | Irlanda | 2016- | moderación de 2 a 5 puntos de crecimiento | puntos porcentuales de crecimiento | no | no |
| kholodilin2022 | DiD (solo resumen de V15) | España (Cataluña) | 2017-2022 | caída también en no controlados; sin cifras | sin cifra | no | no |
| diamond2019 | DiD con regla por antigüedad del edificio | EE. UU. (validez limitada) | 1994- | misma dirección +0,0218 a +0,0354; oferta −15 %; rentas +5,1 % | puntos de probabilidad; % | 0,0083 a 0,0088 | sí, openICPSR 116215 (licencia no comprobada) |
| kholodilin2024 | revisión (contexto) | varios | 1967-2023 | rentas sujetas frenadas; efectos adversos amplios | dirección | no | no aplica |

## Lectura

- Cataluña 2020-2022: tres estudios con identificación distinta coinciden en que la renta pagada o anunciada baja (−4 % a −6 %), y discrepan en la oferta: sin caída (Jofre-Monseny et al., contratos por 1.000 habitantes), −10 % de contratos nuevos (Monràs y García-Montalvo) y −30 % de anuncios (Abel et al.). Las tres medidas de oferta no son la misma variable.
- La versión de 2022 de Monràs y García-Montalvo atribuye la mitad de la caída a composición, mientras que la de 2023 da un efecto mayor al introducir efectos fijos de unidad (−0,080); hay que leer la versión vigente antes de citar el reparto.
- Corrección sobre el plan (E2): Monràs y García-Montalvo usan contratos de Incasòl (más precios de referencia de la Agència de l'Habitatge y datos de los Registradores), no anuncios; el plan decía que solo era replicable con anuncios. Los contratos de Incasòl por municipio son los mismos de Jofre-Monseny et al.
- Zonas tensionadas de 2024: la evidencia disponible es Pérez García (datos públicos de la Generalitat; renta con pretendencias no paralelas y sin efecto con PSM; contratos −13 %) y Pinto (descriptivo). Ninguna cumple todavía los criterios con un estimador robusto.
- Desbordamiento y selección: Hahn et al. (Potsdam), Mense et al. (segmento libre al alza), Jofre-Monseny et al. (vecinos no regulados caen la mitad) y Kholodilin et al. (caída también en no controlados) avisan de interferencia entre controles; en la réplica conviene elegir controles fuera de Cataluña y probar sensibilidad.
- Efecto sobre construcción: Kholodilin y Voigtländer (Alemania) encuentran caída de terminaciones con la segunda generación; en España no hay equivalente leído.

## No incluidos, y por qué

- Autor, Palmer y Pathak (2014), Sims (2007), Asquith (2019), Ahern y Giacoletti (2022): EE. UU. y diseño con equivalente europeo disponible; no fichados (criterio de datos). Sus fichas de V15/V16 siguen vigentes. Autor et al. (NBER w18125) se descargó por error al intentar otro documento y se eliminó.
- Mense et al. (2019, 2023) en su versión del JUE: solo se leyó el documento de DIW.
- Breidenbach et al. (2021, RSUE 103737) y Kholodilin y Voigtländer: el primero sin versión abierta ni resumen localizado; no fichado.
- Monràs y García-Montalvo (2025, SSRN 5677822 / CEPR DP 20018) y Abel, Carrer y Luque (2025, SSRN 5883882, «Rent Control and Decontrol»): existen según Crossref, pero ni el PDF ni el resumen fueron accesibles; sin ficha. Conviene leerlos antes de citar la versión de 2023-2024.
- Nuevos fichados en E2 (fuera del plan y de V15/V16): morin2025 y toussaint2025. Se dejaron 0 por el tope de 15.
