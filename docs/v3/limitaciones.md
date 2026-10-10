# Limitaciones v3

**Limitaciones v3 heredadas de la revisión de la oleada 1.**
1. *Validación sellada de P-C3.* Los coeficientes de P-C3 con fianzas (topes y zonas) se calcularon una vez con todos los municipios, incluidos los sellados, antes de fijar el pre-registro. La validación sellada de P-C3 no es espacial sino por fuente (SERPAVI municipal, stock IRPF). Esa fuente mide el mismo mercado, en los mismos municipios y en el mismo periodo: no es una muestra independiente y su efecto esperado está atenuado. Un resultado C3 de P-C3 debe leerse con esta salvedad.
2. *Estimaciones de P-C1 conocidas.* Las estimaciones de P-C1 en la muestra no sellada se conocían al pre-registrar. Solo la evaluación sellada es confirmatoria.
3. *Exploración previa.* Antes de fijar el sellado se hizo un `describe()` global del tratamiento VUT, incluida la oleada 2026M05. Fueron estadísticos marginales, sin el resultado; la contaminación se considera baja.
4. *B2 (inmigración).* La población extranjera se mide por nacionalidad: las nacionalizaciones sesgan a la baja la entrada neta de nacidos fuera. Con el extremo lógico (1 persona por hogar), la cota de la cuota de ΣΔhogares es del 100 %: no es informativa.
5. *Traducciones a precio (B1, B2).* Son C4 condicionales a |ε_d|. No hay estimación verificada para España, y las formas reducidas citadas no son elasticidades de demanda.
6. *B4.* Sin suelo para uc, la cota de 2014-2021 no es finita. La conclusión sobre 2021-2025 depende del tipo nominal y de una ganancia esperada constante.
7. *A1.* Las ventanas C1 se añadieron después de ver qué fuentes había disponibles. Las cinco ventanas preespecificadas son C4 (una sola fuente de hogares). La EPA y la ECP no son plenamente independientes.
8. *Réplica de García-López et al.* El objetivo T depende de la razón entre VUT del INE y anuncios (rango 0,012-0,117 por pp). Esa razón se observa en una sola fecha (2025).
