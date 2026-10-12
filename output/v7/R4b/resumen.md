# V7-R4b: jerarquico, proyecciones locales, regulacion y provincia (C4, EXPLORATORIO)

Rotulo: informativo, muestra ya vista en v1. Datos al 2026-10-10. Asociaciones, sin lenguaje causal. Sin validacion fuera de muestra en este encargo (fuera_muestra = null). Todas las especificaciones estan en registro.csv (Registry).

## F-H. ECM jerarquico (pymc NUTS, 4 cadenas, 700 muestras + 1000 de ajuste; muestra comun 2007Q3-2025Q1, 17 CCAA, n=1173)
Niveles con demeaning transversal y por CCAA; theta comun, phi_i y delta_i aleatorios por CCAA (no centrado); MixedLM (forma ECM sin restringir) como contraste.
| mercado/spec | phi medio (IC95 creible) | sd entre CCAA | R-hat max / ESS min | MixedLM phi medio |
|---|---|---|---|---|
| alquiler A | -0,0014 (-0,013; 0,004) | 0,008 | 1,52 / 7 (NO converge) | -0,017 |
| alquiler B | -0,0027 (-0,014; 0,002) | 0,008 | 1,006 / 841 | -0,016 (no converge) |
| compra A | -0,010 (-0,078; 0,017) | 0,055 | 1,53 / 7 (NO converge) | -0,077 (no converge) |
| compra B | -0,051 (-0,118; 0,021) | 0,204 | 1,005 / 774 | -0,062 |
- Negativo: en alquiler, el modelo con theta comun lleva phi a cero (el IC incluye 0): theta no queda identificado (A: no converge; B: converge pero con phi ~ 0). En compra el IC de phi medio incluye 0 en ambas especificaciones. La media de los phi individuales por MCO (-0,06 a -0,12) es mucho mayor en magnitud que la jerarquica en alquiler: el encogimiento es casi total (ratio medio ~1 en A).
- Compra B es el unico modelo con buena convergencia y heterogeneidad apreciable (sd_phi 0,20).
- Los resultados de A (R-hat > 1,05) no deben interpretarse; se dan solo como diagnostico.
- Por CCAA (individual, encogido, IC creible): jerarquico_{alquiler,compra}.csv.

## F-L. Proyecciones locales (h=0..8; shock = residuo AR(2) estandarizado de la variacion del tipo hipotecario nacional, y de Delta ln credito nuevo, x exposicion z-estandarizada 2015-19; EF CCAA y trimestre)
- Alquiler: sin efecto diferencial detectable (0 de 9 horizontes con q BH<0,10 en tipo; 0 en credito). Coeficientes ~1e-4 en log (stock IPC, muy suave).
- Compra (IPV): coef. diferencial h=0: +0,13 pp, h=1: +0,10 pp (q BH 0,036 y 0,041; h=2 q 0,13); luego cambia de signo y no es significativo. DK da p>0,10 en h>=1, de modo que la señal depende del metodo (wild vs DK). Credito nuevo: 0 de 9 con q<0,10. El signo positivo a h=0 no coincide con la lectura habitual; puede reflejar la construccion del shock (variacion contemporanea, no exogena). Sin lectura causal.
- Figuras: figuras/irf_diferencial_{alquiler,compra}.png.

## F-R. Regulacion (exploratorio; Delta ln IPC alquiler; EF CCAA y trimestre; 15 contrastes, BH)
- zt_declarada contemporanea: -0,19 pp por trimestre, q BH 0,045 (4 CCAA tratadas). Con adelanto de 4 trimestres (placebo) el coeficiente contemporaneo pierde significacion (q 0,36); el adelanto no es significativo (q 0,36) pero tiene el mismo signo: no se descarta pretendencia, coherente con lo hallado en v3. Con 4 CCAA tratadas el p wild es poco fiable.
- Topes de rentas (E09, variante v3, fraccion) y zt_cuota: ninguno significativo (q >= 0,36). Solo Cataluña tratada (1 cluster): sin poder inferencial.

## F-P. Provincia anual (FE bidireccional con wild Webb y DK; CCEP y CCE-MG; solo spec core: padron, EPA, hipotecas)
- La spec full (+ETDP, iniciadas) solo se estima por FE (13 anos por provincia, CCE inviable con 12 parametros).
- Valor tasado: FE hipotecas +0,023 (q BH 0,024), padron +0,51 (q 0,12), EPA +0,07 (q 0,14). IPC alquiler: padron +0,30 (q<0,001). Con CCE: solo EPA sobre IPC alquiler resiste en CCE-MG (q 0,02); el resto pierde significacion (1 de 12): los resultados FE no son robustos a factores comunes. Hay provincias selladas en v2/v6 en el panel (exploratorio).
- Comunitat Valenciana (03, 12, 46): coeficientes por provincia en provincia_valencia.csv (heterogeneos y ruidosos, 21 observaciones).
