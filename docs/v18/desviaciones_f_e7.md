# V18 · Desviaciones y decisiones del modelizador de F1-F4 y E7 (fase 4)

*Análisis V18; capa C4; pre-registro interno plan-replicacion-v18.* Redactado el 2026-10-20 por el modelizador de F y E7. Cada entrada tiene su motivo; ninguna se
eligió por un resultado (el orden del código es MDE → registro previo en el Registry → estimación). Este fichero es propio de este módulo para no chocar con los otros
modelizadores que escriben a la vez; el orquestador puede fusionarlo en `desviaciones.md`. Código: `src/v18/estimacion/{f_nucleo,f_datos,f_conjunto,e7_tipos}.py`.

## A. Datos y muestra (F1-F3)

1. **Panel provincial de 33-38 provincias, no 39.** Las provincias no selladas con valor tasado son 38; cinco tienen un hueco anual en el valor tasado (22 años en vez de 23), y
   los estimadores de panel exigen panel equilibrado. Ventanas: F1-R2 2002-2018 (el plan decía 2000-2018: el valor tasado provincial anual, el paro, la población y el IPC de
   alquiler empiezan en 2002). Se dice en cada cifra y en tabla.csv (columnas N y T).
2. **Renta de los hogares provincial.** No está en el repositorio (`posterior_prereg`: `ine_cre_renta_hogares_provincial`; sin red). Por la regla (g) del plan se usa el PIB
   provincial corriente por habitante (data/raw/ine_v2_cre.csv), deflactado con el deflactor nacional (el IPC provincial no está en la base: se declara). La variante «PIB per
   cápita como sustituto» (F1-R2-v1, F1-A1-v2) coincide con la principal y no se ejecuta aparte.
3. **Hogares provinciales (F2).** Los hogares provinciales anteriores a 2021 requieren la EPA provincial (`posterior_prereg`, no descargada). F2-R1 y F2-A1 usan la población como
   sustituto de los hogares (declarado); F2-R1-v2 («sin hogares») los quita. F4-2 (hogares en F2) no se hace por la regla AD-F.
4. **Población nacional trimestral.** De los 110 trimestres de F1-R1 (1999T1-2026T2), 44 están interpolados (metodo_dato `interpolado`, 1999-2020). CLAUDE.md limita lo interpolado a
   robustez; se mantiene la población en la principal porque el plan la fija, se rotula en cada cifra y se añade F1-R1-v5 sin población (**holgura nº 1**: no cuenta en I5 ni
   en B5). El plan decía «población de 20 a 64 años o, si no está, la total»: solo está la total, así que F1-R1-v1 («población total») coincide con la principal y no se ejecuta aparte.
5. **F1-A2 (anual).** El parque por hogar no existe antes de 2021: se usa el parque per cápita (data/raw/mivau_parque.csv entre población). UECM con p = 1 (24 observaciones). Medias anuales
   solo de años completos (regla 1.4 b).
6. **«Sin 2008-2013».** En series (F1-R1-v2, F1-A2-v2, F3-A1-v2) se omiten las filas de ese periodo de la estimación (los rezagos usan los niveles reales; el contraste simulado omite las
   mismas filas). En paneles provinciales el resto de la muestra (2014-2024) tiene T = 11 < 12: **NO ESTIMABLE** (F1-A1-v1, F2-R1-v3, F2-A1-v2, F3-A2-v3). Las variantes 2000-2008 de F1-R2 también
   son NO ESTIMABLES (no hay datos provinciales antes de 2002).
7. **F3-R1 y F3-A1 (CCAA no selladas).** Iniciadas = viviendas **libres** iniciadas (MIVAU, anual desde 1991), sumadas por CCAA desde las provincias; Cantabria, uniprovincial, solo se publica como
   comunidad y se trata como la provincia 39 (misma unidad). Instrumentos: valor tasado real retardado 1 y 2 años y coste de construcción retardado; el coste contemporáneo entra como control. La
   ventana efectiva es 1997-2004 (1995-1996 solo como retardos). «Precio sin retardo» (F3-R1-v2) se interpreta como la versión sin instrumentos (MCO con efectos fijos), porque el plan no la define.
   F3-A2 usa `iniciadas_anual_tabla` (2002-2024), el precio del suelo urbano provincial de la tabla 4 del MIVAU (36400500, media anual de años completos) y el crédito a promotores nacional.
8. **F3-A3 NO ESTIMABLE.** Falta la afiliación provincial por sector de 2001 (`ss_afiliacion_provincial_cnae_2001`, `posterior_prereg`) y todavía no existe E5-R1.
9. **F2-A2.** El coste de uso usa como ganancia esperada la media de las dos variaciones anuales previas del valor tasado real (equivale a la media móvil de 8 trimestres del pre-registro de V15
   en datos anuales); ratio con SERPAVI provincial de vivienda colectiva (tipología VC), 2013-2024. La variante «amortización del 3 %» solo desplaza una constante, que los efectos fijos absorben:
   coincide con la principal (se ejecuta y se rotula).

## B. Herramientas y contrastes (F)

10. **Contraste de cointegración de panel.** Westerlund, CIPS y CS-ARDL son NO APTOS (V15/V16) y el Driscoll-Kraay con T <= 30 también (V18 montecarlo/driscoll_kraay). El plan exige un contraste de
    panel con valores críticos validados por Monte Carlo: se usa un Gτ propio (media de las t de la velocidad de ajuste de un UECM(1; 0) por provincia) con bootstrap conjunto en el tiempo
(conserva la dependencia transversal), y se valida con un proceso generador con la estructura de cada diseño (N, T, k; factor común; deriva; R = 200, B = 99). **No sustituye al Monte Carlo del agente
    montecarlo**: si su tamaño cae fuera de [0,02; 0,15] el contraste se declara «no fiable» y no se publican elasticidades de largo plazo. La potencia con T <= 23 es limitada y se publica.
    **Cambio de bootstrap, declarado.** La primera versión remuestreaba por bloques de 2 periodos (como el CIPS de V16). Su validación dio tamaño 0,000-0,005 en los nueve diseños (potencia 0 con
    T = 14-17 y k = 4-5): el remuestreo duplica periodos y el contraste es inútil. Se sustituyó por el bootstrap de signos común (Rademacher), cuya validación da tamaño 0,025-0,05 y potencia 0,83-1,0
    con T = 17-23. El cambio se decidió por la validación del tamaño, no por los datos; para que conste, los p de datos de la primera versión eran: F1-R2 0,906; F1-R2-alt 0,959; F1-A1 0,520;
    F2-R1 0,993; F3-A2 0,147 (ninguno rechazaba). Los p de la versión vigente están en tabla.csv.
11. **Inferencia de panel.** DOLS-FE con Driscoll-Kraay y con error agrupado: ambos NO APTOS sin efectos de año; PMG con error asintótico y bootstrap de provincias (sin validar). Se publican con
    esa etiqueta y la clasificación no se apoya en ellos (tope ASOCIACIÓN de todos modos).
12. **F1-P-V72 NO ESTIMABLE.** V7.2 usó un panel de 17 CCAA (Westerlund/Pedroni); 8 están selladas por v6 y reproducirlo con las 9 restantes deja de ser la especificación de origen.
    F1-P-M4: UECM p = 2 caso III y DOLS k = 1 con ln PIB, tipo real y población (vector C2 de V8-M4); sin crédito ni oferta porque `credito_stock_bde` y las terminadas acumuladas no tienen clave
    en sellado_v18.json. F1-P-E1P2: CS-ARDL(1,0) con medias transversales contemporáneas (V15 usó CS-ARDL(1,1) con 4 rezagos de las medias); herramienta NO APTA: solo descriptivo.
13. **MDE en la familia F.** El Anexo B no da referencia ni δ para F («—»): no hay umbral para declarar NO ESTIMABLE por variación. El MDE se calcula antes de estimar (R = 2.000, SEED 20261010)
    con la variación real de los regresores y σ del residuo de la propia muestra, **declarada ya vista** (no hay σ de V15/V16 para estos resultados), y se publica como diagnóstico.
14. **Sobrevaloración y F4.** Sin cointegración (todas las especificaciones principales, Holm al 5 %), F1-A3 y F4-1 a F4-5 no se hacen (regla AD-F); en tabla.csv figuran como NO ESTIMABLE por regla,
    con su motivo. Si alguna cointegrase, F4 quedaría «pendiente» hasta que existan E3, E5 y E6 de los otros modelizadores.
15. **Fuera de muestra.** F1-ECM = AR(4) + y_{t-1}, X_{t-1}, ΔX_{t-1} (anida al AR(4), para Clark-West); ECM v1 «aproximado» como en v6 (Δy sobre y_{t-1} y X_{t-1}); deriva; K = 5 bloques con embargo
    de 4 trimestres; DM-HLN, CW, GW y MCS (T_max). Solo para el F1-R1 nacional.

## C. E7

16. **Controles.** PIB (Δ ln, ×100) e inflación interanual, 4 rezagos de cada uno, más 4 rezagos de y y de Δi. **El crédito nuevo se omite**: empieza en 2003T1 y recortaría 16 trimestres de una
    muestra ya corta (el plan lo lista entre los controles). Declarado; no se estima la variante con crédito.
17. **Choque principal = mediana de Jarociński-Karadi** (la que usó V16 Q5 como primera opción). La variante v4 («mediana») coincide con la principal y no se ejecuta aparte; v3 es la «poor man's».
18. **Choque total (v5).** pc1 = MP + CBI vive en el mismo fichero y con el mismo corte, pero no tiene clave propia en sellado_v18.json: hereda la de `bce_jk_mp_median_m|zona_euro|M` (2025-10).
19. **E7-R1-v2 y E7-R2-v2 NO ESTIMABLES.** No hay serie trimestral del diferencial soberano a 10 años: solo la anual `irt_lt_mcby_a` (Eurostat), sin clave en sellado_v18.json. Se necesita la serie mensual del
    BCE (`posterior_prereg`). **El encargo «controlando el diferencial soberano» no se pudo cumplir**; sigue pendiente de la descarga.
20. **SVAR.** VAR(2) en [tipo hipotecario, ln precio real, ln compraventas, ln PIB, inflación, euríbor] con 73 observaciones (2007T1-2025T3, por las compraventas); respuesta normalizada a +100 pb de
    impacto en el tipo hipotecario. «Sin 2010-2013» (v1): el proxy se sustituye por su media en esos trimestres (su covarianza con los residuos no aporta); se mantiene la muestra del VAR.
21. **Fuente de las sorpresas.** `data/bib/replicacion/jarocinski_karadi2020/shocks_ecb_mpd_me_m.csv` (Jarociński y Karadi 2020, DOI 10.1257/mac.20180090, actualizado con EA-MPD de Altavilla et al. 2019,
    DOI 10.1016/j.jmoneco.2019.08.016; repositorio github.com/marekjarocinski/jkshocks_update_ecb, descargado el 2026-10-20, sin licencia declarada: solo local). El fichero coincide byte a byte con
    `data/raw/v16/demanda_internacional/bce_sorpresas/jk_shocks_ecb_mpd_me_m.csv` (la ruta del manifiesto de sellado); el código lo comprueba. Sumas trimestrales de trimestres completos hasta 2025T3.
22. **MDE de E7.** σ del error de la LP a h = 4 del valor tasado, derivada del MDE declarado en V16 Q5 (1,47 % por desviación típica, n = 101): σ4 = 1,47/2,8·√101 = 5,28; a h = 8 se escala por √(h/4)
    (ya visto, declarado). Para IPV, compraventas y alquiler no hay σ de V16: se usa el residuo propio de la LP (ya visto). MDE con el AR de EHW al 5 % frente a β0 = 0, R = 2.000, con la variación real
    del instrumento y la primera etapa estimada (π, σ_v), que se leen sin mirar el coeficiente de interés. El umbral es |San Juan| = 2 % (3 % en compraventas); sin referencia, 2δ = 2,0.
    Con primera etapa débil el MDE es infinito (la potencia del AR queda acotada por el F): es el resultado esperado de V8/Q5 y deja E7-R1, R2 y las demás **NO ESTIMABLES por variación**, que
    se publican como estimación informativa fuera de clasificación.
23. **P (coprincipales).** E7-P-Q5: forma reducida (MCO) de la LP a h = 4 por unidad de sorpresa trimestral (Q5 la daba por desviación típica; se publica la desviación típica). E7-P-H8-5 y -6: LP-IV con
    Δ euríbor, h = 4-8 agregado, 2 rezagos y ficticia COVID (V8 IV1). **E7-P-H8-7 NO ESTIMABLE** aquí (IV2 es el empuje migratorio: pertenece a E3). **E7-P-D5 NO ESTIMABLE** (panel de 18 países con exposición
    por país; no está en sellado_v18.json).
24. **E7-A2.** Exposición E_p = Σ hipotecas sobre vivienda (número) / Σ compraventas (total), 2007-2019, INE, con las claves `hip_n|provincia|M` y `compraventas|provincia|M` (tope 2024-12); 33 provincias con
    valor tasado trimestral completo desde 2002T1. Efectos de provincia y de periodo; Webb WCR (9.999 réplicas en la principal); h = 4 y h = 12 como **holgura nº 2 y 3** (el plan dice «h = 0..12»; no cuentan en I5
    ni B5). **E7-A2-v1 (cuota de compradores extranjeros) no se estima**: el dato (data/raw/mivau_transacciones_residencia.csv) no figura entre las variables del manifiesto de E7-A2 y su carga es de E9.
    Unidad: % del precio por pp de sorpresa y por unidad de exposición; no es comparable con la referencia sin una primera etapa fiable (+100 pb queda muy fuera del soporte: sd de la sorpresa trimestral ≈ 0,05 pp).
25. **No encargado a este módulo:** E7-R3 y E7-A1 (BVAR de San Juan) y E7-A3 (EA-MPD, pendiente de licencia).
26. **Clase provisional.** Toda clase es provisional hasta I8 (réplica ciega, B6); ninguna especificación llega a IDENTIFICADO ni a SUGESTIVO por el gate de la adenda 1.3 o por el tope de F.

## D. Holgura usada (adenda 1.8; máximo 200)

F1-R1-v5 (sin población), E7-A2-h4 y E7-A2-h12 (horizontes). Total: 3. Ninguna apoya clasificaciones ni entra en I5 o B5.
