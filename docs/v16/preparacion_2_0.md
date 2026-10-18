# V16 · Preparación de la 2.0 (fase 7, punto 4)

Ensayo, sin publicar nada: `python3 src/v14/arbol_publico.py --destino <directorio temporal> --sin-git`, y después `python3 src/v14/escaneo_terceros.py --arbol <ese directorio> --valores --salida docs/v16/escaneo_terceros_2_0.csv`. El árbol se borró después del escaneo.

## Rutas locales y datos personales (corregido)
El control de árbol_publico (patrón PRIVADO) paró la primera ejecución en dos grupos de ficheros, y se corrigieron sin cambiar ninguna cifra:
- **Rutas absolutas a /home/user/Econometr-a.**
  - En docs/v15/inventario_anotaciones.csv e inventario_variables.{csv,md}: pasan a rutas relativas al repositorio.
  - En los scripts de réplica de V16 (src/v16/replica/*.py) y en src/v16/montecarlo/cips_bootstrap_diagnostico.py: la raíz se deduce de la ubicación del fichero.
  - En la guarda de salidas cerradas (.claude/hooks/guarda_salidas_cerradas.py) y su test: lo mismo.
- **Rutas del directorio temporal de la sesión** en output/v16/replica/h5/reconciliacion.md y v10_d/reconciliacion.md: se sustituyen por «directorio temporal de la sesión».

Con esto, el árbol se genera sin errores: 3.766 ficheros, 1.091 versionados excluidos, 31 tablas redactadas.

## Escaneo de terceros (Notariado, Registradores, AEAT, CGPJ) sobre el árbol
Resultado: docs/v16/escaneo_terceros_2_0.csv (por nombre y clave) y docs/v16/escaneo_terceros_2_0_valores.csv (por valores). En el ámbito «árbol» quedan **14 ficheros PENDIENTES de revisión manual**, todos de V12-V16:
- docs/v14/escenarios_resultado.json y docs/v16/sellado_v16.json;
- output/v12/b5/aeat_cv_2013_2015.csv y aeat_cv_declarantes_inmuebles.csv;
- output/v15/auditoria/precios_compra/resultado.json y output/v15/auditoria/renta_microdatos/ (4 CSV y resultado.json);
- output/v16/auditoria/tension_social/resultado.json, output/v16/f2_hechos/control.json, output/v16/potencia/resultado.json y output/v16/replica/v10_a/resultado.json.

Para la 1.0 se revisaron uno a uno y se anotaron en `REVISADOS` (src/v14/escaneo_terceros.py) o se redactaron con `terceros_1_0`. Para la 2.0 hay que hacer lo mismo con estos 14: decidir si cada uno es un agregado propio o metadatos (se anota como revisado) o contiene la serie (se redacta o se excluye).

Es una decisión sobre licencias de terceros y queda en docs/v16/tareas_autor.md. No bloquea V16: el árbol 1.0 publicado no cambia.

## Lo que no se hace en V16
- No se crea el repositorio público de la 2.0 ni se cambia la versión vigente: proyecto.json sigue en 1.0.
- El commit «Versión 1.0» de arbol_publico.py y el paquete de depósito se adaptarán cuando el autor decida publicar la 2.0.
