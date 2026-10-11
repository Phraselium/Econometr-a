# Desviaciones del pre-registro (M2, 2026-10-11)

1. **n_mun_tensionados** no entra: es constante (cero) en el entrenamiento (la zona tensionada es posterior al corte), así que queda fuera del BMA y del multiverso. Solo se estima n_mun_topes_cat.
2. **Doble BMA.** El pre-registro fija un BMA con priores uniformes. Se reporta ese (set completo, solo observaciones con ln_vut y ln_suelo: alquiler N=106, compra N=64) y, como robustez, un «núcleo» sin ln_vut/ln_suelo (N=281 y 342). Se añade prior beta-binomial(1,1) como sensibilidad. El set completo tiene poca potencia; ambas lecturas se reportan.
3. **Muestra no común en el multiverso:** cada especificación usa su muestra completa (depende de los controles, retardo y diferencias); no hay una muestra única. Los BMA/PDS sí usan una muestra fija por variante.
4. **Regresores de alquiler:** el panel de alquiler de M0 no trae ln_pob, share_ext_pob, ln_pib_pc ni oferta; se unen por (cod, anio) desde el panel de compra (mismas fuentes M0).
5. **Municipio y distrito:** los regresores provinciales se unen a cada municipio/distrito. Hay pseudo-replicación (varias unidades comparten el mismo valor), así que los PIP y errores del BMA municipal están sobreestimados en confianza; el clúster (provincia) solo se aplica en PDS y multiverso. Distrito: K=2, solo 2 especificaciones válidas. Contratos nuevos: sin modelo (N≈15), como en hipotesis.md §3.
6. **Compra de municipio** solo con el desenlace tasado municipal (200 municipios); precio alternativo (Registradores) solo a nivel provincial.
7. **Fuera de muestra (AR(4), ECM v1, DM-HLN):** no se evalúa en M2 (BMA/PDS/multiverso describen soporte dentro de muestra, no predicción); queda a M4. `fuera_muestra` = null en resultado.json.
8. **«Selección en PDS»:** se reporta la selección del elastic net conjunto (CV en bloques con embargo de 1 año, orígenes 2018/2020/2022) y el coeficiente post-double-selection de cada variable con IC95 agrupado por unidad/provincia (t, no wild bootstrap).
9. **Capa:** todo C4. No hay revisión posterior con M1 en esta entrega.
10. Retardo 0 en el multiverso (robustez) rompe el pre-registro de t−1 solo como especificación alternativa, no como principal. Las diferencias y tendencias son robustez, como en el pre-registro.
