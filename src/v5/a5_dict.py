"""Diccionario A5: instrumento -> (nombre, direccion_rule, [regex]). Texto normalizado: minusculas, sin tildes.

Variantes en castellano, catalan (ca) y gallego (gl). Los terminos son regex sobre texto normalizado.
"""
V = r"(?:vivienda|viviendas|habitatge|habitatges|vivenda|vivendas|etxebizitza|inmueble|inmuebles|immoble|immobles)"

D = {
 "I01": ("Regulacion de precios del alquiler", [
    r"zonas? (?:de mercado residencial )?tensionad", r"zones? (?:de mercat residencial )?tensionad",
    r"indice de referencia", r"indexs? de referencia",
    r"tope[s]? (?:a|al|de|del|en) (?:los |el |la )?(?:precio|alquiler|renta|incremento|subida)",
    r"limit\w+ (?:de )?(?:el |los |la |las )?(?:precio|precios|renta|rentas|alquiler|alquileres|subida)",
    r"control de (?:las )?(?:rentas|precios|alquileres)", r"contencion de (?:los )?(?:precios|rentas)",
    r"congel\w+ (?:de )?(?:los |el )?(?:alquiler|alquileres|rentas)", r"contenci[oó] de (?:les )?(?:rendes|preus)",
    r"limitaci[oó] (?:del|dels|de) (?:preu|preus|lloguers?|rendes)", r"(?:contencion|limitacion) (?:das|dos) (?:rendas|prezos)",
    r"ley (?:por el derecho a la|de) vivienda", r"ley 12/2023"]),
 "I02": ("Parque publico o social de alquiler a gran escala", [
    r"parque (?:publico|social)", r"parc (?:public|social)", r"parque (?:publico|social) de (?:vivenda|aluguer)",
    r"vivienda[s]? (?:publica|publicas|social|sociales)", r"habitatges? (?:public|publics|social|socials)",
    r"vivendas? (?:publica|publicas|social|sociais)", r"alquiler (?:social|asequible|publico)", r"lloguer (?:social|assequible|public)",
    r"aluguer (?:social|accesible|publico)", r"vivienda[s]? (?:de )?(?:proteccion|promocion) publica", r"vivienda[s]? asequible"]),
 "I03": ("Reservas de suelo para vivienda protegida", [
    r"reserva[s]? (?:de |del |obligatoria de )?(?:suelo|sol|solo|edificabilidad)", r"reserva[s]? (?:del )?\d+ ?%", r"\bvpo\b",
    r"vivienda[s]? protegida", r"habitatges? protegit", r"vivendas? protexid", r"vivienda[s]? de proteccion oficial"]),
 "I04": ("Movilizacion de suelo y patrimonio publicos", [
    r"suelos? publico", r"sol public", r"solo publico", r"patrimonio (?:publico|de suelo|inmobiliario)", r"patrimoni public",
    r"\bsepes\b", r"\bsareb\b", r"sociedad de gestion de activos", r"cesion de suelo", r"derecho de superficie", r"dret de superficie",
    r"suelos? de titularidad publica", r"entidad publica empresarial de suelo", r"\bsegipsa\b"]),
 "I05": ("Captura de plusvalias del suelo", [
    r"plusvalias? (?:del suelo|urbanistica|derivada)", r"captura de plusvalias", r"recuperacion de (?:las )?plusvalias",
    r"cesion de aprovechamiento", r"plusvalues urbanistiques", r"participacion (?:de la comunidad )?en las plusvalias"]),
 "I06": ("Avales publicos a hipotecas", [
    r"avales? (?:publico|del estado|ico|hipotecari)", r"avales? (?:a|para) (?:jovenes|la compra|hipotecas|la primera)",
    r"linea de avales", r"garantia publica", r"avals? (?:public|hipotecari)", r"\baval(?:es)?\b"]),
 "I07": ("Fiscalidad y ahorro para vivienda en propiedad", [
    r"deduccion(?:es)? (?:por|de|en el irpf por) (?:la )?(?:compra|adquisicion|vivienda habitual)",
    r"deducci[oó] (?:per|de) (?:compra|adquisici|habitatge)", r"iva (?:reducido |superreducido )?(?:de|en|a) (?:la )?(?:vivienda|compra|construccion)",
    r"cuenta[s]? (?:vivienda|ahorro.vivienda|de ahorro)", r"ahorro.vivienda", r"itp (?:reducido|bonificado)",
    r"impuesto de transmisiones patrimoniales", r"desgravacion", r"iva .{0,40}vivienda", r"fiscalidade sobre a vivenda", r"fiscalidad .{0,20}(?:sobre )?(?:la )?vivienda"]),
 "I08": ("Ayudas directas al alquiler", [
    r"ayudas? (?:directas? )?(?:al|para el|para pagar el|de) alquiler", r"bono (?:de )?alquiler", r"bono joven",
    r"subvencion(?:es)? (?:al|de|para el) alquiler", r"cheque alquiler", r"ajudes? (?:al|per al|de) lloguer",
    r"axudas? (?:ao|para o|de) aluguer", r"deduccion(?:es)? (?:por|de) alquiler", r"bono xove", r"bono de vivenda", r"bono joven de alquiler"]),
 "I09": ("Ayudas a hogares hipotecados", [
    r"hipotecad", r"hipotecari[oa]s? (?:en|con) (?:dificultad|vulnerab)", r"codigo de buenas practicas", r"dacion en pago",
    r"moratoria hipotecari", r"deudores hipotecarios", r"tipo variable", r"subrogacion (?:de )?(?:prestamos )?hipotecari",
    r"hipotec\w+ a tipo fijo", r"euribor", r"hipoteca[s]? (?:variable|a tipo)", r"dacio en pagament", r"cancel.lacio de deutes", r"cancelacion de deudas"]),
 "I10": ("Movilizacion de vivienda vacia", [
    r"viviendas? (?:vacia|vacias|deshabitada|desocupada|sin uso)", r"habitatges? (?:buit|buits|desocupat)", r"vivendas? (?:baleir|desocupad)",
    r"parque vacio", r"inmuebles? vacio", r"pisos? vacio", r"registro de viviendas vacias", r"movilizacion de (?:las )?viviendas",
    r"tanteo y retracto", r"recuperacio de la possessio"]),
 "I11": ("Rehabilitacion del parque", [
    r"rehabilitacion", r"rehabilitaci[oó]", r"reabilitacion", r"regeneracion urbana", r"eficiencia energetica (?:de|en) (?:los )?(?:edificios|viviendas)",
    r"renovacion (?:energetica )?de (?:los )?edificios"]),
 "I12": ("Industrializacion de la construccion", [
    r"industrializ\w+ (?:de )?(?:la )?construccion", r"construccion industrializada", r"construccion modular", r"prefabricad",
    r"industrialitzaci", r"construccio industrialitzada", r"metodos modernos de construccion", r"\bmmc\b"]),
 "I13": ("Agilizacion y seguridad juridica urbanistica", [
    r"agiliz\w+ (?:de |los |las |el )?(?:tramit|licencias|planeamiento|procedimientos urbanis|urbanis)", r"seguridad juridica (?:en el |del )?(?:urbanis|planeamiento|suelo)",
    r"liberaliz\w+ (?:de |del )?(?:el )?suelo", r"ley (?:de bases )?del suelo", r"ley de suelo", r"simplificacion (?:administrativa )?(?:urbanistic|de los tramites urbanis)",
    r"suelo urbanizable"]),
 "I14": ("Seguridad juridica y procedimientos de desalojo", [
    r"okupa", r"ocupacion ilegal", r"ocupacion ilicita", r"ocupacio il", r"ocupacion de inmuebles", r"usurpacion", r"allanamiento de morada",
    r"desahucio expres", r"desalojo", r"desahucio", r"desnonament", r"lanzamiento", r"inquiokup", r"defensa de la propiedad",
    r"desafiuzamento", r"ocupacion de viviendas", r"ocupas"]),
 "I15": ("Fiscalidad de arrendadores e inversores", [
    r"reduccion (?:del |en el )?(?:rendimiento|irpf)\w* (?:de|del|por|para)? ?(?:los |el )?(?:arrend|alquiler)", r"bonificacion\w* (?:fiscal )?(?:a|para|de) (?:los |las )?(?:arrendador|propietarios|alquiler)",
    r"incentivos? fiscal\w* (?:a|para|al) (?:el |la |los |las )?(?:alquiler|arrend|propietario)", r"fiscalidad (?:del|de los|de las) (?:alquiler|arrend|inversor|grandes tenedor)",
    r"recargo\w* (?:en )?(?:el )?(?:ibi|impuesto)", r"arrendadores", r"socimi", r"fondos? de inversion inmobiliari", r"incentivos fiscales de la ley de vivienda", r"rendes de lloguer", r"irpf.{0,60}(?:lloguer|alquiler|arrend)", r"beneficios fiscales.{0,60}(?:propietarios|inmobiliari|socimi)"]),
 "I16": ("Alquiler turistico y de temporada", [
    r"alquiler(?:es)? turistic", r"viviendas? (?:de uso |con fines |para uso )?turistic", r"alquiler(?:es)? de temporada", r"arrendamientos? de temporada",
    r"lloguer(?:s)? (?:turistic|de temporada)", r"habitatges? d.us turistic", r"aluguer (?:turistico|de tempada)", r"alquiler de habitaciones",
    r"pisos turisticos", r"registro (?:unico )?de arrendamientos de corta duracion", r"corta duracion", r"habitatges? de temporada", r"vivendas? de tempada", r"contractes d arrendament d habitatges"]),
 "I17": ("(Sin definicion en v4; no se busca)", []),
 "I18": ("Duracion y prorroga de contratos de alquiler", [
    r"duracion (?:minima )?(?:de los |del )?(?:contrato|arrend)", r"prorroga\w* (?:del |de los |obligatoria|extraordinaria)", r"prorrogas? de (?:los )?contratos",
    r"ley de arrendamientos urbanos", r"\blau\b", r"estabilidad (?:de los |del )?(?:contrato|alquiler)", r"contratos? de alquiler de (?:cinco|5|siete|7)",
    r"durada (?:del|dels) contracte", r"duracion dos contratos", r"prorroga automatica", r"contratos mas largos", r"contractes mes llargs", r"contratos mais longos", r"contratos? mais (?:longos|estables)", r"contratos mas longos", r" contratos mais longos e estabeis", r"contratos maximo"]),
 "I19": ("Sinhogarismo y vivienda de emergencia", [
    r"sinhogar", r"sense llar", r"housing first", r"personas sin hogar", r"vivienda de emergencia", r"habitatge d.emergencia", r"sen fogar",
    r"emergencia habitacional", r"emergencia residencial", r"infravivienda"]),
 "I20": ("Colaboracion publico-privada y nuevas modalidades", [
    r"colaboracion publico.privada", r"col.laboracio public.privada", r"colaboracion publicoprivada", r"cooperativas? de (?:vivienda|cesion)",
    r"concesion\w* (?:administrativa )?(?:de suelo|para)", r"colaboracion con el sector privado",
    r"promocion privada de alquiler", r"vivienda colaborativa", r"cohousing", r"asociaciones de vivienda", r"organizaciones sin (?:animo de )?lucro", r"entidades sin animo de lucro"]),
 "I21": ("Limitacion de compras con fin de inversion o de no residentes", [
    r"no residentes", r"extranjeros no (?:comunitarios|residentes)", r"compra\w* (?:de |por )?(?:vivienda |viviendas )?(?:con fines|con fin) (?:de )?(?:inversion|especulativ)",
    r"visado de residencia", r"golden visa", r"visados? (?:de oro|por inversion)", r"residencia por inversion", r"autorizacion\w* (?:administrativa\w* )?de compraventa",
    r"compradores? (?:no residentes|extranjeros)", r"especulacion inmobiliaria", r"fondos? (?:buitre|de inversion)", r"condicionar .{0,60}compraventa", r"visat de residencia", r"adquisicion\w* de vivienda\w* por (?:no residentes|extranjeros)"]),
 "I22": ("Obligaciones a grandes tenedores", [
    r"grandes? tenedor", r"grans tenidor", r"grandes propietarios", r"persona[s]? juridica[s]? propietaria", r"fondos? (?:buitre|de inversion)",
    r"alquiler social obligatorio", r"cuota (?:minima )?de alquiler social", r"lloguer social obligatori"]),
 "I24": ("Derecho subjetivo a la vivienda", [
    r"derecho subjetivo", r"derecho (?:exigible|efectivo) a la vivienda", r"dret subjectiu", r"dereito subxectivo",
    r"derecho exigible", r"derecho reclamable", r"justiciable"]),
 "I25": ("Coordinacion multinivel (pacto de Estado)", [
    r"pacto de estado (?:por|de|sobre|en materia de) (?:la )?vivienda", r"pacto (?:nacional )?(?:por|de|sobre) (?:la )?vivienda", r"pacte d.estat",
    r"conferencia sectorial de vivienda", r"gran acuerdo (?:nacional )?(?:por|de|sobre) (?:la )?vivienda", r"pacto por la vivienda",
    r"consenso\w* (?:entre|con) (?:las )?comunidades", r"agencia estatal de vivienda", r"cooperacion interadministrativa"]),
 "I26": ("Gravamen sobre suelo urbanizable ocioso", [
    r"suelo (?:ocioso|sin edificar|urbanizable sin|sin desarrollar)", r"solares? (?:sin edificar|ocioso)", r"sol (?:sense edificar|ociós)", r"gravamen\w* (?:sobre )?(?:el )?suelo",
    r"solares? vacios", r"edificacion forzosa", r"venta forzosa", r"suelos? .{0,40}ocios", r"gravamen sobre los suelos"]),
 "I27": ("Recargo o impuesto a la vivienda vacia", [
    r"recargo\w* (?:en|del|sobre|al|de) (?:el )?(?:ibi|impuesto).{0,60}vacia", r"impuesto (?:a|sobre) (?:las )?viviendas? vacia", r"recargo.{0,40}viviendas? (?:vacia|desocupada)",
    r"gravar (?:las )?viviendas? vacia", r"impost (?:sobre|als) habitatges? buit", r"ibi.{0,60}vacia", r"vacia.{0,60}ibi", r"recargo (?:do|del|en el) ibi", r"recargo de ibi"]),
 "I28": ("Inembargabilidad de la vivienda habitual", [
    r"inembargab", r"embargo de la vivienda habitual", r"vivienda habitual.{0,40}embarg", r"embargab"]),
 "I29": ("Reduccion de tributos sobre la promocion y construccion de vivienda", [
    r"iva (?:de|en|para) (?:la )?(?:promocion|construccion|obra nueva)", r"reduccion (?:de )?(?:los )?(?:impuestos|tributos|tasas) .{0,40}(?:promocion|construccion|vivienda nueva)",
    r"bonificacion\w* .{0,30}(?:icio|construcciones)", r"tasas? (?:de )?licencias?", r"impuesto sobre construcciones", r"iva superreducido"]),
 "N1": ("Agilizacion de licencias (medios tecnicos municipales)", [
    r"licencias? (?:de obras?|urbanistic|de edificacion|de construccion)", r"agiliz\w+ (?:de )?(?:las )?licencias", r"silencio (?:administrativo )?positivo",
    r"plazos? (?:de )?(?:concesion de )?licencias", r"llicencies? d.obres", r"medios (?:tecnicos|humanos) .{0,30}ayuntamientos", r"ventanilla unica"]),
 "N2": ("Mayor edificabilidad o densidad", [
    r"mayor edificabilidad", r"aumento de (?:la )?edificabilidad", r"incremento de (?:la )?edificabilidad", r"densidad (?:urbana|edificatoria|residencial)",
    r"verticalizacion", r"altura\w* (?:de )?(?:los )?edificios", r"mes densitat", r"mayor densidad"]),
 "N3": ("Impuesto sobre el valor del suelo", [
    r"impuesto sobre el valor del suelo", r"impuesto (?:al|sobre el) valor (?:del )?suelo", r"impuesto (?:de )?(?:solares|sobre el suelo)",
    r"impuesto sobre el suelo", r"valor del suelo", r"land value tax", r"impost sobre el valor del sol"]),
 "N4": ("Incentivo fiscal a la promocion privada de alquiler asequible", [
    r"credito fiscal", r"incentivos? fiscal\w* .{0,40}promoci", r"bonificacion\w* .{0,40}promocion .{0,30}alquiler",
    r"deduccion\w* .{0,40}promocion .{0,30}alquiler", r"alquiler asequible .{0,60}(?:fiscal|bonific|deduc|ventaja)", r"(?:fiscal|bonific|deduc|ventaja).{0,60}alquiler asequible",
    r"build to rent", r"promocion de vivienda en alquiler.{0,40}(?:fiscal|incentiv|bonific)"]),
}

ALIAS_N = {"N5": "I12", "N6": "I05", "N7": "I10", "N8": "I02", "N9": "I06-I09"}

# Direccion: derogar/reducir si en la ventana aparece un verbo de supresion; I14 ademas con verbos de paralizacion.
NEG = (r"deroga|suprim|eliminar|eliminaci|supress|derogaci|revoca|dejar sin efecto|acabar[ea]mos con|poner fin|pondremos fin|"
       r"derogarem|suprimir|abolir|abolici|retirar")
NEG_I14 = NEG + r"|paraliz|suspen|moratoria|prohib\w+ (?:de )?(?:los )?(?:desahucios|desalojos|lanzamientos)|parar los desahucios|frenar (?:los )?desahucios|evitar (?:los )?desahucios"
# Terminos que no son 'instrumento' cuando el instrumento es el propio rotulo (p.ej. I14 'ocupacion ilegal' se codifica a favor).
CONTEXT_REQ = {"I06", "I08", "I09", "I15", "I18", "I29", "I11", "I24", "I21", "I22", "N1", "N2", "N3", "I25", "I28"}
