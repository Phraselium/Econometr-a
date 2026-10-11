# Fuentes fallidas v6

Cada entrada: fuente, endpoint probado, edición, fecha de la prueba y error.


## M0 (datos, paneles, sellado, potencia)

- M0 no descargó nada: reutilizó data/raw, data/processed y las salidas v5/v5_1 versionadas. No hubo intento de acceso a endpoints.
- Sin dato por cobertura de la fuente (no fallo de acceso): Notariado fuera de Comunitat Valenciana; valor tasado provincial de Baleares, La Rioja, Madrid, Murcia, Navarra, Asturias, Cantabria, Ceuta y Melilla; VUT municipal (`ln_vut_viviendas_mun` vacía); emigración provincial (sin flujo neto); renta disponible provincial; jóvenes en casa de los padres provincial. Ver docs/v6/diccionario.md, sección 3.
