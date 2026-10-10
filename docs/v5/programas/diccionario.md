# Diccionario de palabras clave A5

Texto normalizado (minusculas, sin tildes); los terminos son expresiones regulares sobre el texto de cada pagina (pdftotext -layout, lineas unidas, guiones de corte eliminados). Variantes en castellano, catalan (ca) y gallego (gl). Fuente de verdad: `src/v5/a5_dict.py`.

## Reglas

- Unidad: frase (delimitada por . ; ! ? o vineta) que contiene el termino; una fila por documento x instrumento x direccion x pagina (primera frase). Las paginas son indices del PDF (no la numeracion impresa).
- Instrumentos con contexto obligatorio (hay palabra de vivienda/alquiler/hipoteca/suelo a +-250 caracteres): I06, I08, I09, I11, I15, I18, I21, I22, I24, I25, I28, I29, N1, N2, N3.
- Direccion, regla de v4: `a favor/ampliar` por defecto; `derogar/reducir` si en la frase (hasta 70 caracteres antes del termino, incluido este) aparece un verbo de supresion: `deroga|suprim|eliminar|eliminaci|supress|derogaci|revoca|dejar sin efecto|acabar[ea]mos con|poner fin|pondremos fin|derogarem|suprimir|abolir|abolici|retirar`. En I14 (desalojos) los verbos de paralizacion/suspension (`paraliz|suspen|moratoria|prohib\w+ (?:de )?(?:los )?(?:desahucios|desalojos|lanzamientos)|parar los desahucios|frenar (?:los )?desahucios|evitar (?:los )?desahucios`) dan `revisar`: pueden describir una medida existente o una propuesta y no se decide automaticamente.
- Alias N de la matriz v4: N5=I12; N6=I05; N7=I10; N8=I02; N9=I06-I09. No se duplican busquedas.
- I17 e I23 no tienen definicion en `docs/v4/instrumentos.md`: no se buscan (registrado como hueco).
- Limites: es una busqueda de candidatos. Una coincidencia no es una medida validada (ver `output/v5/A5/validacion_precision.csv`); una medida redactada sin ninguno de los terminos no se detecta (recall medido contra v4 en `docs/v5/programas/conciliacion_v4.csv`).

## Terminos por instrumento

### I01 Regulacion de precios del alquiler

- `zonas? (?:de mercado residencial )?tensionad`
- `zones? (?:de mercat residencial )?tensionad`
- `indice de referencia`
- `indexs? de referencia`
- `tope[s]? (?:a|al|de|del|en) (?:los |el |la )?(?:precio|alquiler|renta|incremento|subida)`
- `limit\w+ (?:de )?(?:el |los |la |las )?(?:precio|precios|renta|rentas|alquiler|alquileres|subida)`
- `control de (?:las )?(?:rentas|precios|alquileres)`
- `contencion de (?:los )?(?:precios|rentas)`
- `congel\w+ (?:de )?(?:los |el )?(?:alquiler|alquileres|rentas)`
- `contenci[oó] de (?:les )?(?:rendes|preus)`
- `limitaci[oó] (?:del|dels|de) (?:preu|preus|lloguers?|rendes)`
- `(?:contencion|limitacion) (?:das|dos) (?:rendas|prezos)`
- `ley (?:por el derecho a la|de) vivienda`
- `ley 12/2023`

### I02 Parque publico o social de alquiler a gran escala

- `parque (?:publico|social)`
- `parc (?:public|social)`
- `parque (?:publico|social) de (?:vivenda|aluguer)`
- `vivienda[s]? (?:publica|publicas|social|sociales)`
- `habitatges? (?:public|publics|social|socials)`
- `vivendas? (?:publica|publicas|social|sociais)`
- `alquiler (?:social|asequible|publico)`
- `lloguer (?:social|assequible|public)`
- `aluguer (?:social|accesible|publico)`
- `vivienda[s]? (?:de )?(?:proteccion|promocion) publica`
- `vivienda[s]? asequible`

### I03 Reservas de suelo para vivienda protegida

- `reserva[s]? (?:de |del |obligatoria de )?(?:suelo|sol|solo|edificabilidad)`
- `reserva[s]? (?:del )?\d+ ?%`
- `\bvpo\b`
- `vivienda[s]? protegida`
- `habitatges? protegit`
- `vivendas? protexid`
- `vivienda[s]? de proteccion oficial`

### I04 Movilizacion de suelo y patrimonio publicos

- `suelos? publico`
- `sol public`
- `solo publico`
- `patrimonio (?:publico|de suelo|inmobiliario)`
- `patrimoni public`
- `\bsepes\b`
- `\bsareb\b`
- `sociedad de gestion de activos`
- `cesion de suelo`
- `derecho de superficie`
- `dret de superficie`
- `suelos? de titularidad publica`
- `entidad publica empresarial de suelo`
- `\bsegipsa\b`

### I05 Captura de plusvalias del suelo

- `plusvalias? (?:del suelo|urbanistica|derivada)`
- `captura de plusvalias`
- `recuperacion de (?:las )?plusvalias`
- `cesion de aprovechamiento`
- `plusvalues urbanistiques`
- `participacion (?:de la comunidad )?en las plusvalias`

### I06 Avales publicos a hipotecas

- `avales? (?:publico|del estado|ico|hipotecari)`
- `avales? (?:a|para) (?:jovenes|la compra|hipotecas|la primera)`
- `linea de avales`
- `garantia publica`
- `avals? (?:public|hipotecari)`
- `\baval(?:es)?\b`

### I07 Fiscalidad y ahorro para vivienda en propiedad

- `deduccion(?:es)? (?:por|de|en el irpf por) (?:la )?(?:compra|adquisicion|vivienda habitual)`
- `deducci[oó] (?:per|de) (?:compra|adquisici|habitatge)`
- `iva (?:reducido |superreducido )?(?:de|en|a) (?:la )?(?:vivienda|compra|construccion)`
- `cuenta[s]? (?:vivienda|ahorro.vivienda|de ahorro)`
- `ahorro.vivienda`
- `itp (?:reducido|bonificado)`
- `impuesto de transmisiones patrimoniales`
- `desgravacion`
- `iva .{0,40}vivienda`
- `fiscalidade sobre a vivenda`
- `fiscalidad .{0,20}(?:sobre )?(?:la )?vivienda`

### I08 Ayudas directas al alquiler

- `ayudas? (?:directas? )?(?:al|para el|para pagar el|de) alquiler`
- `bono (?:de )?alquiler`
- `bono joven`
- `subvencion(?:es)? (?:al|de|para el) alquiler`
- `cheque alquiler`
- `ajudes? (?:al|per al|de) lloguer`
- `axudas? (?:ao|para o|de) aluguer`
- `deduccion(?:es)? (?:por|de) alquiler`
- `bono xove`
- `bono de vivenda`
- `bono joven de alquiler`

### I09 Ayudas a hogares hipotecados

- `hipotecad`
- `hipotecari[oa]s? (?:en|con) (?:dificultad|vulnerab)`
- `codigo de buenas practicas`
- `dacion en pago`
- `moratoria hipotecari`
- `deudores hipotecarios`
- `tipo variable`
- `subrogacion (?:de )?(?:prestamos )?hipotecari`
- `hipotec\w+ a tipo fijo`
- `euribor`
- `hipoteca[s]? (?:variable|a tipo)`
- `dacio en pagament`
- `cancel.lacio de deutes`
- `cancelacion de deudas`

### I10 Movilizacion de vivienda vacia

- `viviendas? (?:vacia|vacias|deshabitada|desocupada|sin uso)`
- `habitatges? (?:buit|buits|desocupat)`
- `vivendas? (?:baleir|desocupad)`
- `parque vacio`
- `inmuebles? vacio`
- `pisos? vacio`
- `registro de viviendas vacias`
- `movilizacion de (?:las )?viviendas`
- `tanteo y retracto`
- `recuperacio de la possessio`

### I11 Rehabilitacion del parque

- `rehabilitacion`
- `rehabilitaci[oó]`
- `reabilitacion`
- `regeneracion urbana`
- `eficiencia energetica (?:de|en) (?:los )?(?:edificios|viviendas)`
- `renovacion (?:energetica )?de (?:los )?edificios`

### I12 Industrializacion de la construccion

- `industrializ\w+ (?:de )?(?:la )?construccion`
- `construccion industrializada`
- `construccion modular`
- `prefabricad`
- `industrialitzaci`
- `construccio industrialitzada`
- `metodos modernos de construccion`
- `\bmmc\b`

### I13 Agilizacion y seguridad juridica urbanistica

- `agiliz\w+ (?:de |los |las |el )?(?:tramit|licencias|planeamiento|procedimientos urbanis|urbanis)`
- `seguridad juridica (?:en el |del )?(?:urbanis|planeamiento|suelo)`
- `liberaliz\w+ (?:de |del )?(?:el )?suelo`
- `ley (?:de bases )?del suelo`
- `ley de suelo`
- `simplificacion (?:administrativa )?(?:urbanistic|de los tramites urbanis)`
- `suelo urbanizable`

### I14 Seguridad juridica y procedimientos de desalojo

- `okupa`
- `ocupacion ilegal`
- `ocupacion ilicita`
- `ocupacio il`
- `ocupacion de inmuebles`
- `usurpacion`
- `allanamiento de morada`
- `desahucio expres`
- `desalojo`
- `desahucio`
- `desnonament`
- `lanzamiento`
- `inquiokup`
- `defensa de la propiedad`
- `desafiuzamento`
- `ocupacion de viviendas`
- `ocupas`

### I15 Fiscalidad de arrendadores e inversores

- `reduccion (?:del |en el )?(?:rendimiento|irpf)\w* (?:de|del|por|para)? ?(?:los |el )?(?:arrend|alquiler)`
- `bonificacion\w* (?:fiscal )?(?:a|para|de) (?:los |las )?(?:arrendador|propietarios|alquiler)`
- `incentivos? fiscal\w* (?:a|para|al) (?:el |la |los |las )?(?:alquiler|arrend|propietario)`
- `fiscalidad (?:del|de los|de las) (?:alquiler|arrend|inversor|grandes tenedor)`
- `recargo\w* (?:en )?(?:el )?(?:ibi|impuesto)`
- `arrendadores`
- `socimi`
- `fondos? de inversion inmobiliari`
- `incentivos fiscales de la ley de vivienda`
- `rendes de lloguer`
- `irpf.{0,60}(?:lloguer|alquiler|arrend)`
- `beneficios fiscales.{0,60}(?:propietarios|inmobiliari|socimi)`

### I16 Alquiler turistico y de temporada

- `alquiler(?:es)? turistic`
- `viviendas? (?:de uso |con fines |para uso )?turistic`
- `alquiler(?:es)? de temporada`
- `arrendamientos? de temporada`
- `lloguer(?:s)? (?:turistic|de temporada)`
- `habitatges? d.us turistic`
- `aluguer (?:turistico|de tempada)`
- `alquiler de habitaciones`
- `pisos turisticos`
- `registro (?:unico )?de arrendamientos de corta duracion`
- `corta duracion`
- `habitatges? de temporada`
- `vivendas? de tempada`
- `contractes d arrendament d habitatges`

### I17 (Sin definicion en v4; no se busca)

- (sin terminos)

### I18 Duracion y prorroga de contratos de alquiler

- `duracion (?:minima )?(?:de los |del )?(?:contrato|arrend)`
- `prorroga\w* (?:del |de los |obligatoria|extraordinaria)`
- `prorrogas? de (?:los )?contratos`
- `ley de arrendamientos urbanos`
- `\blau\b`
- `estabilidad (?:de los |del )?(?:contrato|alquiler)`
- `contratos? de alquiler de (?:cinco|5|siete|7)`
- `durada (?:del|dels) contracte`
- `duracion dos contratos`
- `prorroga automatica`
- `contratos mas largos`
- `contractes mes llargs`
- `contratos mais longos`
- `contratos? mais (?:longos|estables)`
- `contratos mas longos`
- ` contratos mais longos e estabeis`
- `contratos maximo`

### I19 Sinhogarismo y vivienda de emergencia

- `sinhogar`
- `sense llar`
- `housing first`
- `personas sin hogar`
- `vivienda de emergencia`
- `habitatge d.emergencia`
- `sen fogar`
- `emergencia habitacional`
- `emergencia residencial`
- `infravivienda`

### I20 Colaboracion publico-privada y nuevas modalidades

- `colaboracion publico.privada`
- `col.laboracio public.privada`
- `colaboracion publicoprivada`
- `cooperativas? de (?:vivienda|cesion)`
- `concesion\w* (?:administrativa )?(?:de suelo|para)`
- `colaboracion con el sector privado`
- `promocion privada de alquiler`
- `vivienda colaborativa`
- `cohousing`
- `asociaciones de vivienda`
- `organizaciones sin (?:animo de )?lucro`
- `entidades sin animo de lucro`

### I21 Limitacion de compras con fin de inversion o de no residentes

- `no residentes`
- `extranjeros no (?:comunitarios|residentes)`
- `compra\w* (?:de |por )?(?:vivienda |viviendas )?(?:con fines|con fin) (?:de )?(?:inversion|especulativ)`
- `visado de residencia`
- `golden visa`
- `visados? (?:de oro|por inversion)`
- `residencia por inversion`
- `autorizacion\w* (?:administrativa\w* )?de compraventa`
- `compradores? (?:no residentes|extranjeros)`
- `especulacion inmobiliaria`
- `fondos? (?:buitre|de inversion)`
- `condicionar .{0,60}compraventa`
- `visat de residencia`
- `adquisicion\w* de vivienda\w* por (?:no residentes|extranjeros)`

### I22 Obligaciones a grandes tenedores

- `grandes? tenedor`
- `grans tenidor`
- `grandes propietarios`
- `persona[s]? juridica[s]? propietaria`
- `fondos? (?:buitre|de inversion)`
- `alquiler social obligatorio`
- `cuota (?:minima )?de alquiler social`
- `lloguer social obligatori`

### I24 Derecho subjetivo a la vivienda

- `derecho subjetivo`
- `derecho (?:exigible|efectivo) a la vivienda`
- `dret subjectiu`
- `dereito subxectivo`
- `derecho exigible`
- `derecho reclamable`
- `justiciable`

### I25 Coordinacion multinivel (pacto de Estado)

- `pacto de estado (?:por|de|sobre|en materia de) (?:la )?vivienda`
- `pacto (?:nacional )?(?:por|de|sobre) (?:la )?vivienda`
- `pacte d.estat`
- `conferencia sectorial de vivienda`
- `gran acuerdo (?:nacional )?(?:por|de|sobre) (?:la )?vivienda`
- `pacto por la vivienda`
- `consenso\w* (?:entre|con) (?:las )?comunidades`
- `agencia estatal de vivienda`
- `cooperacion interadministrativa`

### I26 Gravamen sobre suelo urbanizable ocioso

- `suelo (?:ocioso|sin edificar|urbanizable sin|sin desarrollar)`
- `solares? (?:sin edificar|ocioso)`
- `sol (?:sense edificar|ociós)`
- `gravamen\w* (?:sobre )?(?:el )?suelo`
- `solares? vacios`
- `edificacion forzosa`
- `venta forzosa`
- `suelos? .{0,40}ocios`
- `gravamen sobre los suelos`

### I27 Recargo o impuesto a la vivienda vacia

- `recargo\w* (?:en|del|sobre|al|de) (?:el )?(?:ibi|impuesto).{0,60}vacia`
- `impuesto (?:a|sobre) (?:las )?viviendas? vacia`
- `recargo.{0,40}viviendas? (?:vacia|desocupada)`
- `gravar (?:las )?viviendas? vacia`
- `impost (?:sobre|als) habitatges? buit`
- `ibi.{0,60}vacia`
- `vacia.{0,60}ibi`
- `recargo (?:do|del|en el) ibi`
- `recargo de ibi`

### I28 Inembargabilidad de la vivienda habitual

- `inembargab`
- `embargo de la vivienda habitual`
- `vivienda habitual.{0,40}embarg`
- `embargab`

### I29 Reduccion de tributos sobre la promocion y construccion de vivienda

- `iva (?:de|en|para) (?:la )?(?:promocion|construccion|obra nueva)`
- `reduccion (?:de )?(?:los )?(?:impuestos|tributos|tasas) .{0,40}(?:promocion|construccion|vivienda nueva)`
- `bonificacion\w* .{0,30}(?:icio|construcciones)`
- `tasas? (?:de )?licencias?`
- `impuesto sobre construcciones`
- `iva superreducido`

### N1 Agilizacion de licencias (medios tecnicos municipales)

- `licencias? (?:de obras?|urbanistic|de edificacion|de construccion)`
- `agiliz\w+ (?:de )?(?:las )?licencias`
- `silencio (?:administrativo )?positivo`
- `plazos? (?:de )?(?:concesion de )?licencias`
- `llicencies? d.obres`
- `medios (?:tecnicos|humanos) .{0,30}ayuntamientos`
- `ventanilla unica`

### N2 Mayor edificabilidad o densidad

- `mayor edificabilidad`
- `aumento de (?:la )?edificabilidad`
- `incremento de (?:la )?edificabilidad`
- `densidad (?:urbana|edificatoria|residencial)`
- `verticalizacion`
- `altura\w* (?:de )?(?:los )?edificios`
- `mes densitat`
- `mayor densidad`

### N3 Impuesto sobre el valor del suelo

- `impuesto sobre el valor del suelo`
- `impuesto (?:al|sobre el) valor (?:del )?suelo`
- `impuesto (?:de )?(?:solares|sobre el suelo)`
- `impuesto sobre el suelo`
- `valor del suelo`
- `land value tax`
- `impost sobre el valor del sol`

### N4 Incentivo fiscal a la promocion privada de alquiler asequible

- `credito fiscal`
- `incentivos? fiscal\w* .{0,40}promoci`
- `bonificacion\w* .{0,40}promocion .{0,30}alquiler`
- `deduccion\w* .{0,40}promocion .{0,30}alquiler`
- `alquiler asequible .{0,60}(?:fiscal|bonific|deduc|ventaja)`
- `(?:fiscal|bonific|deduc|ventaja).{0,60}alquiler asequible`
- `build to rent`
- `promocion de vivienda en alquiler.{0,40}(?:fiscal|incentiv|bonific)`

## Extraccion de texto por documento

| doc_id | metodo | paginas | palabras |
|---|---|---|---|
| A5-D03 | texto | 5 | 1359 |
| A5-D05 | texto | 182 | 104839 |
| A5-D06 | texto | 132 | 65467 |
| A5-D07 | texto | 16 | 3528 |
| A5-D08 | texto | 52 | 22442 |
| A5-D09 | texto | 68 | 17986 |
| A5-D10 | texto | 6 | 1572 |
| A5-D11 | texto | 61 | 36329 |
| A5-D12 | texto | 97 | 56683 |
| A5-D17 | texto | 21 | 11490 |
| A5-D18 | texto | 17 | 9429 |
| A5-D19 | texto | 11 | 6509 |
| A5-D20 | texto | 4 | 1760 |
| A5-D21 | texto | 5 | 2115 |
| A5-D22 | texto | 5 | 2350 |
| A5-D23 | texto | 5 | 2404 |
| A5-D24 | texto | 4 | 2275 |
| A5-D25 | texto | 5 | 2321 |
| A5-D26 | texto | 14 | 8044 |
| A5-D27 | texto | 5 | 2246 |
| A5-D28 | texto | 15 | 8854 |
| A5-D29 | texto | 11 | 5823 |
