# E1 · Vivienda turística · resumen de la fase 1 (bibliotecario, grupo A, 2026-10-20)

Criterios: docs/v18/bib/criterios.md (sin cambios). Fichas: una por estudio en este directorio. Todas con estado «NO VERIFICADA»; solo src/v15/verificar_referencias.py lo cambia. Cifras tal como las dan los autores, con la versión leída indicada en cada ficha.

## Tabla

| clave | diseño | país | periodo | efecto | unidad | error | paquete |
|---|---|---|---|---|---|---|---|
| garcialopez2020 | efectos fijos con tendencias por barrio; shift-share (atractivos × Google); eventos | España (Barcelona) | 2007-2017 | alquiler +1,9 % (barrio medio), +7 % (decil alto); transacción +4,6 % / +17 %; anunciados +3,7 % / +14 % | log por cada 100 anuncios en la BSA (0,035 con efectos fijos; 0,022 y 0,033 con instrumental) | 0,009 (FE); 0,011 y 0,010 (IV) | no |
| segu2018 | Bartik con distancia a la playa, 2SLS | España (Barcelona) | 2009-2016 | alquiler +4 % | log del alquiler por punto de densidad de Airbnb (0,038) | 0,012 | no |
| benitez2023 | DiD con choque COVID como instrumento, FGLS | España (Barcelona) | 2018-2021 | alquiler 0,0748 y compra 0,390 (lectura del autor: −1 % de densidad → −7 % y −39 %) | coeficiente de Tratado×ln(densidad) sobre log precio/m² | t = 2,95 y 13,86 | no |
| casanova2019 | hedónico MCO/2SLS/SAR (contexto) | España (Madrid) | corte de abril de 2018 | 0,017 (MCO), 0,023 (2SLS), 0,012 (SAR I), 0,009 n. s. (SAR II) | coeficiente por anuncio a 500 m sobre alquiler/m² | no extraído | no |
| pastor2022 | hedónico en dos etapas, corte transversal (contexto) | España (València, Madrid, Barcelona) | 2021 | +0,87 % por 100 anuncios; +0,82 % con efectos fijos de distrito; elasticidad 0,057 | % del alquiler por 100 anuncios en el barrio; elasticidad | 0,0000244; 0,0061 | no |
| chavesfonseca2026 | shift-share (distancia × Google Trends); mediación | España (Madrid) | 2010-2018 | precios +2 % por 100 anuncios; entradas de población −50 por 100 anuncios | log precio por 100 anuncios (0,020 y 0,022) | 0,004 y 0,005 | sí (CC BY 4.0) |
| mozo2023 | no leído | España (San Sebastián) | no leído | +49,45 € al mes por +1 anuncio por 100 viviendas | euros/mes de renta anunciada | no | no |
| duso2024 | dos reformas de la ley de uso de viviendas; PDS-Lasso IV | Alemania (Berlín) | 2014-2019 | +0,165 €/m² (≈ +1,8 %) por anuncio de alta disponibilidad a 250 m | €/m² de renta anunciada por vivienda entera adicional | IC95: 0,089 a 0,241 | no (CC BY 4.0 del PDF, descarga bloqueada) |
| goncalves2022 | DiD con discontinuidad espacial de la zonificación | Portugal (Lisboa) | 2015-2019 | precio −8 % (−20 % en dos dormitorios) | log precio (−0,087) | 0,02 | no |
| robertson2023 | DiD y triple diferencia | Francia (Burdeos) | 2016-2020 | días reservados −43,9 % de la media | días reservados por mes y distrito (−322) | 124 | no |
| franco2021 | no leído (DiD según resumen) | Portugal | no leído | +3,7 % de precio por punto de cuota municipal | % por punto de cuota | no | no |
| almagro2024 | estructural dinámico; IV shift-share | Países Bajos (Ámsterdam) | hasta 2017 | elasticidad del alquiler 0,091 a 0,205 | log-log sobre anuncios comerciales | 0,021 a 0,093 | no |
| barron2021 | shift-share con Google Trends × atractivo | EE. UU. (validez limitada) | 2008-2016 | elasticidad 0,018 en el código postal mediano | log-log | 0,003 (coef. base) | no localizado |
| koster2021 | RDD en panel; DiD | EE. UU. (validez limitada) | 2014-2018 | anuncios −50 %; precio −2,9 % a −4,2 %; alquiler −3,4 % a −4,9 % | log tras la ordenanza | 0,0067; 0,0080; 0,0118 | no |
| bibler2021 | DiD con registro obligatorio | EE. UU. (validez limitada) | 2014-2019 | precio −0,053; ejecuciones +0,059 | log precio; ejecuciones por sección-mes | 0,012; 0,009 | no |
| calderwang2021 | estructural | EE. UU. (validez limitada) | 2018 | alquiler +0,71 % (reasignación del 0,68 % del parque) | % del alquiler | no | no |
| valentin2019 | diff-in-disc en la frontera | EE. UU. (validez limitada) | hasta 2018 | precio ≈ −60 % en el borde (borrador); ≈ −30 % (publicada) | log precio/pie² | no extraído | no |
| wachsmuth2026 | DiD escalonado | Canadá | 2017-2022 | −24 y −55 USD/mes (nota de prensa) | dólares por mes | no | no |
| bekkerman2023 | regulación y frontera | EE. UU. | no leído | anuncios −9,0 %; permisos −11,0 % | % a 12 meses | no | no |
| ayouba2019 | hedónico por ciudad (contexto) | Francia | no leído | sin cifra | densidad de Airbnb | no | no |
| kim2025 | panel espacial y regla de 90 días | Reino Unido (Londres) | no leído | sin cifra | no consta | no | no |
| brunstein2025 | bosques causales | Francia (Córcega) | no leído | elasticidad 0,21 | % por 1 % de anuncios | no | no |

## Lectura

- Los diseños con identificación europea (García-López 2020, Duso 2024, Gonçalves 2022, Chaves-Fonseca 2026) coinciden en el signo, pero no en la unidad: efectos por 100 anuncios (barrios de Barcelona y Madrid), por anuncio a 250 m (Berlín) o por reforma (Lisboa). Los efectos medios sobre el alquiler van del 1 % al 4 % según el estudio y la unidad; el del decil de mayor actividad en Barcelona es del 7 %.
- Los estudios con peor identificación (Casanova 2019, Pastor 2022, Benítez-Aurioles 2023) no aportan una cifra comparable: el de Madrid con efectos espaciales no encuentra efecto; el de València da +0,87 % por 100 anuncios en una asociación transversal; el de Barcelona con choque de COVID da magnitudes no comparables (la lectura del autor es 7 % de alquiler por 1 % de densidad).
- La versión leída difiere de la publicada en tres casos (Koster 2019, Barron 2019, Valentin 2019): antes de usar una cifra hay que leer la publicada. Valentin da 60 % en el borrador y 30 % en el resumen publicado.
- Para la réplica E1 (Barcelona con HUT 2018-2026): ningún estudio leído cubre 2018-2026 en España; el de Madrid llega a 2018 en el panel principal y el paquete trae una extensión 2019-2024/25 (data/bib/replicacion/chavesfonseca2026).

## Estudios localizados sin ficha o excluidos

- Todd, Musah y Cheshire (2021, Londres, 10.1177/23998083211001836): efectos fijos y aleatorios, asociación; excluido por diseño. Resumen leído, sin PDF.
- Reina (2026, PEUAT en Barcelona, 10.4995/jpeval.2026.25574): método mixto descriptivo; excluido por diseño. El PDF de la revista no se descargó.
- Horn y Merante (2017, Boston): sin versión abierta localizada y EE. UU.; no fichado.
- Estudios españoles de V15/V16 sin versión abierta o de solo contexto (López-Rodríguez y Matea 2019; Khametshin et al. 2024; Martínez-Caldentey et al. 2020; Dong 2026; Chaves Fonseca 2024 Santa Monica, Banabak y Sielker 2026, Slaymaker 2025): no fichados en esta pasada; sus fichas de V15/V16 siguen vigentes.
- Quedan fuera por el tope de 15 estudios nuevos: ninguno (nuevos fichados en E1: segu2018, ayouba2019, kim2025, brunstein2025; 4 de 15).

## Búsqueda

- OpenAlex «search» devolvió 429 (cuota diaria agotada, aviso de reintento en unas 12 horas; la cuota se comparte con el otro bibliotecario). La búsqueda sistemática se hizo con Crossref «query.bibliographic» y con búsquedas web de los términos de criterios.md; las consultas por DOI a OpenAlex y Unpaywall sí funcionaron. Cobertura de la búsqueda, por tanto, menor que la prevista; conviene repetirla con OpenAlex cuando se restablezca la cuota.
