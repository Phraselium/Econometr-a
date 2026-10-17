# V16 · Tareas del autor

## 1. Publicar las etiquetas de pre-registro interno (bloqueo B-1; prioridad máxima)
Desde esta sesión el remoto rechaza las etiquetas (HTTP 403). Los commits ya están en la rama `claude/housing-price-spain-econometric-95dhj3`. Desde tu clon:

```
git fetch origin claude/housing-price-spain-econometric-95dhj3
git tag -a prereg-v15 542b4fdf398970c817af7abfcd20c92dda299c69 -m "V15: pre-registro interno sin sello externo (preregistro_v15.md y adendas 1-2)"
git tag -a prereg-v2 910c42aef06348b884ea70e7b6cdc510d58e48c1 -m "pre-registro v2"
git tag prereg-v3 204c073e9e2c9e0edd6ac23dad7edf3049ba4428
git tag -a prereg-v5 8803f049c0f46ae4db8a79221470594295931d86 -m "pre-registro v5"
git tag -a prereg-v6 a33c167080fbd4b86a9239dcb3744d070e501429 -m "pre-registro v6"
git tag prereg-v7 3fad305fc51bbcec67ec9ae298a31c58b8bd0fd0
git tag prereg-v8 91e618be1a2d17879808982a1fe87729d7f5afaf
git tag prereg-v9 2977349e3ed3092a51c8a3ad309140cf0b83dca8
git tag prereg-v9-a1 9cb2200e7cb487fcd22d9da1e8b40ba68a3303d7
git tag prereg-v9-a1b 4639772d1dbac4e01af0e24bc0a8501117fe1324
git push origin --tags
git ls-remote --tags origin "prereg-*"
```

La lista de etiquetas, commits y tipos de objeto está en docs/v16/etiquetas_prereg.csv.

Cuando se cierre la fase 4 de V16 se añadirá aquí el comando de prereg-v16. Hasta que esté en el remoto, la guarda (f) mantiene bloqueadas las fases 5 a 7 de V16, por diseño.

## 2. Decidir sobre la independencia de dh_2125 (aumento de hogares 2021-2025, C1)
Sus dos fuentes son la ECP y la EPA del INE. La EPA se calibra con las cifras de población que salen de la ECP, de modo que las dos fuentes podrían no ser independientes en el sentido que llevó a las 11 bajadas de la 1.0. Opciones:
- (a) mantener C1 y explicar por qué la jefatura de hogar de la EPA es una medición distinta;
- (b) bajar a C4 sin cambiar el valor, con la línea «dh_2125 | capa C1 → C4» en ERRATA.md y una fila en docs/v15/bajadas_capa.csv.
V16 no lo cambia por su cuenta: la cifra figura como C1 en la página de hechos. Las cifras nuevas V16-* aplican ya esta vara (fase 2).
