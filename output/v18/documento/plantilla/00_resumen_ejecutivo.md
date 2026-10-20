## Resumen ejecutivo

Este documento reproduce, replica y amplía con datos españoles los estudios publicados sobre nueve factores de la evolución del precio de la vivienda: vivienda turística, topes al alquiler, inmigración, ayudas a la demanda, oferta y suelo, obra nueva, tipos de interés, fiscalidad de la compra y compradores no residentes. Para cada factor busca una magnitud preferida que combine las estimaciones propias con las de la literatura, y con ellas ensaya una contabilidad de la subida por periodo y territorio.

Toda cifra V18 es de capa C4 (exploratoria) y lleva al lado su clasificación V18: IDENTIFICADO, SUGESTIVO, ASOCIACIÓN, NO CONCLUYENTE o NO ESTIMABLE. El diseño es un pre-registro interno sin sello de tiempo externo (etiqueta git plan-replicacion-v18 sobre el commit ad4385c, 2026-10-20). Los análisis posteriores a ese commit se declaran a posteriori (anexo F).

{{tabla.impactos}}

**Resultado.**

- Ninguna estimación propia alcanza la clase IDENTIFICADO. La única de clase SUGESTIVO es la de los topes al alquiler en Cataluña (E2-R1): una diferencia negativa de la renta de los contratos nuevos en los municipios regulados frente a los de control, que no es estable en el tiempo ni se separa de otros cambios de la época. Su cifra solo se difunde con la frase de limitación de la sección 4.2.
- El resto de las estimaciones propias son ASOCIACIÓN (por ejemplo, E1-R3 y E8-R1), NO CONCLUYENTE (E1-R4 y E3-R1) o NO ESTIMABLE por falta de variación o de datos.
- Solo E1, E4 y E6 tienen magnitud preferida, y en los tres casos procede de uno o dos estudios de la literatura, no de una estimación propia. En E2, E3 y E5 las estimaciones de la literatura son heterogéneas y no hay magnitud preferida. En E7, E8 y E9 la literatura da rangos sin error típico.
- Contabilidad de la subida. La regla fijada de antemano admite solo factores con una estimación propia válida dentro de la magnitud preferida. Ningún factor la cumple, de modo que toda la variación observada queda en «no explicado». Por ejemplo, la variación del precio real de compra en 1995T1-2007T4 que queda sin explicar es de {{V18-C5-1995T1-2007T4-00-NOEXPL-P:valor}} ({{V18-C5-1995T1-2007T4-00-NOEXPL-P:clasificacion}}). Una ilustración aparte con magnitudes de la literatura, que no es una atribución, deja también sin explicar la mayor parte de la variación en casi todos los periodos y territorios (sección 5).
- El documento no permite decir qué factor explica la mayor parte de la subida en ningún periodo ni territorio. Tampoco modifica los veredictos de la auditoría de V17 (sección 6).

**Qué datos lo resolverían** (docs/v18/tareas_autor.md).

- Ayudas a la demanda (E4): microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas, con fecha de solicitud y concesión.
- Topes y turismo (E2, E1): registros de contratos de alquiler con renta anterior, superficie y tipo de contrato, y microdatos de portales de anuncios.
- Oferta, obra nueva y grandes tenedores (E5, E6, E10): descarga masiva del Catastro, Sistema de Información Urbana y restricciones físicas del suelo.
- Tipos y no residentes (E7, E9): compras por nacionalidad y al contado (Notariado, Registradores), más series de riesgo de los países de origen y la Encuesta Financiera de las Familias.
- Vacías y vivienda pública (E11, E12): calendario del recargo del IBI y del impuesto catalán, y promociones públicas por municipio y año.
- Para cualquier clase superior a las actuales: la evaluación sellada diferida (evaluate_v18), con datos posteriores a la etiqueta.
