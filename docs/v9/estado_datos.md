# Estado de V9-DATOS-COMPLETO (para retomar con `claude --continue`)

Rama local `v9-datos` → remota `claude/housing-price-spain-econometric-95dhj3`.

## Hecho
- V9-DATOS (primera pasada): 93 ficheros, 11 fuentes (docs/v9/decisiones_datos.md, D0-D6).

- **Bloque 0** (D7):
  - regulacion/: 1.992 títulos del BOE, 102 normas con su XML, 318 zonas tensionadas verificadas frente al BOE (ninguna nueva hasta 2026-10-14) y alcance por CCAA;
  - actualizaciones/: inventario; todas las series al día.

## Interrumpido (2026-10-14)
- El autor abrió V10-DIFUSIÓN y considera V9-DATOS completado. Los bloques 1-9 de V9-DATOS-COMPLETO quedan **aplazados**: no se han descargado.
- Exploración del bloque 1 hecha, aún sin descargar. Si se retoma, empezar por aquí:
  - **Registre de Turisme de Catalunya** (Socrata t2h3-cgys; 112.696 filas):
    - sin fecha de alta y con nombres de titulares (datos personales);
    - solo se versionarían agregados por municipio (código IDESCAT de 6 dígitos = INE de 5 + dígito de control);
    - licencia «See Terms of Use», igual que Incasòl: no redistribuible.
  - **IDESCAT, HUT por municipio 2015-2025** (`https://www.idescat.cat/pub/?id=turall&n=16722&geo=mun&t=<aaaa>00&lang=es&f=ssv`):
    - stock y plazas por municipio y año desde 2015;
    - total de Cataluña: 47.242 en 2015 y 105.399 en 2025;
    - el mismo patrón sirve para apartamentos turísticos (n=16721), hoteles (6033), campings (6034) y turismo rural (6037).
  - **IEET por municipio y tipología** (Socrata q4sr-68c3): semestral 2017S1-2025S1; HT = viviendas de uso turístico.
  - **IDESCAT `afi`**: afiliados a la Seguridad Social por residencia padronal y municipio (bloque 5).
  - **Bloqueo de red:** web.archive.org está bloqueado por la política de red del entorno, lo que impide la segunda vía (cortes antiguos) del bloque 9.

## Subagentes
- Ninguno en V9-DATOS-COMPLETO.
