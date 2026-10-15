# Revisión final de V9 (2026-10-15) — hecha por el orquestador, no independiente

El revisor independiente de F3 superó su tope de tokens (unos 114.000 frente a 100.000). Por la regla del prompt no se volvió a delegar ninguna revisión. Esta revisión la hace el orquestador y **no sustituye** una revisión humana independiente (docs/v9/tareas_autor.md, punto 9).

## Puertas de control (`make check`, check_v9)

| Control | Resultado |
|---|---|
| Cruces solo por código INE | Sin errores: análisis por AST de merge, join, map, set_index y pivot en src/v9. El IPVA municipal, que solo tiene nombres, se excluyó |
| Ninguna cifra publicada cambiada sin ERRATA | 1.092 huellas previas idénticas (docs/v9/cifras_base_v81.csv); solo se añaden 61 ids `V9-` |
| p ajustados | Holm en {H1a-renta, H1b-renta}; BH en todas las exploratorias salvo D3, que es descriptivo; con instrumento débil, el p es el de AR |
| Lenguaje causal solo en C3/C3s | Hay 0 C3/C3s y ningún texto de V9 contiene léxico causal sin negar (informe, verificador, cotas, plantillas). Solo se exceptúa la afirmación citada y evaluada en el verificador |
| Nada no redistribuible en la capa pública | Incasòl, Registre, IEET y los shocks JK no están en data/base/publica; output/v9 solo contiene estimaciones agregadas |
| Resultados de la web trazables | Cada id V9 de la web y del verificador existe en cifras_clave; cada script citado existe |
| Tests | 361 aprobados, incluida la validación de las herramientas de V9 |

## Comprobaciones de contenido

- **Pre-registro.**
  - Las especificaciones principales y alternativas coinciden con docs/v9/hipotesis.md y el addendum A1.
  - Las especificaciones que no se estiman están documentadas (E6).
  - Ninguna especificación se eligió por su p y todas constan en output/v9/registry.csv.
- **Capas.** Las reglas se aplican en src/v9/f3_capas.py sin excepciones. H1b-renta supera todas las pruebas salvo la robustez a desviaciones de tendencia (Rambachan y Roth, M̄ = 1). Se informa así, sin relajar la regla después de ver el resultado.
- **Herramientas.**
  - CS, BJS, dCDH, bootstrap salvaje, IV/AR/AKM, Conley y Holm/BH están validados por Monte Carlo (tests/v9).
  - El IC de Rambachan y Roth es una implementación propia (contraste condicional de ARP por pieza, unión de piezas), no el paquete HonestDiD. En la validación por Monte Carlo el tamaño es de 7,3 % con 400 réplicas, algo por encima del nominal. Eso no afecta a ninguna capa, porque un exceso de rechazo solo favorecería pasar a C3.
- **Neutralidad.** Se evalúan normas y afirmaciones, nunca partidos ni personas; el verificador lo dice en cada ficha.

## Reservas que debe conocer el lector

1. **D1a.** Solo hay 20 municipios de control con datos completos. Las pretendencias se rechazan.
2. **D1b.** Las pretendencias usan una ventana trimestral corta (2019T1-2020T3), que incluye el confinamiento. La robustez anual coincide en el signo y en la magnitud.
3. **D3.** El resultado (2024→2025) es anterior a la mayor parte de la caída del registro, cuya exposición se mide con un corte posterior al 2026-07-01 (excepción declarada). El placebo muestra una asociación del mismo signo.
4. **D4.** El instrumento es débil en todas las variantes. Los conjuntos de AR no están acotados en varias.
5. **D7.** Es contable. El componente población de la Comunitat Valenciana (112 %) supera el 100 % porque bajó la tasa de jefatura.
6. **El revisor de F3 no aprobó él mismo las correcciones.** La re-revisión es del orquestador.

## Veredicto

**APROBAR con las reservas anteriores.** El siguiente paso es la revisión humana y la publicación, no otra versión de modelización (docs/v9/cierre.md).
