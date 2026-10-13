# Decisiones V8.1

## Z0 — Alcance y entorno (2026-10-13)
- V8.1 no estima modelos ni abre muestras selladas: solo redacción, tablas, capa de consulta, retirada de datos de terceros y publicación.
- El encargo dice «en local con `gh` autenticado», pero esta sesión corre en un contenedor en la nube: `gh auth status` informa de que el token GH_TOKEN no es válido, y el remoto rechaza el push de etiquetas. Los bloques A-D se hacen aquí; el bloque E se prepara (comandos exactos en docs/v8_1/publicacion_github.md) y cada acción irreversible se consulta al autor antes de ejecutarla, si el entorno lo permite.
