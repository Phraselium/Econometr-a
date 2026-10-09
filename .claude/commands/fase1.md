---
description: F1 Datos — descarga en paralelo por fuente, construye base trimestral nacional y panel CCAA; para en la puerta de revisión.
---
Fase 1 (Datos). Como orquestador:
1. Lanza en PARALELO un subagente `data-fetcher` por fuente: INE (IPV nacional/CCAA/nueva-usada, EPA, ECP población total/extranjera, hogares, migraciones, transmisiones),
   Eurostat (renta B6G, permisos, costes de construcción, prc_hpi_q), BCE (tipo hipotecario, Euríbor), Ministerio de Vivienda/IVE/Ajuntament de València (valor tasado, visados, fin de obra, SERPAVI, padrón, VUT).
   En paralelo, lanza `lit-researcher` para docs/literatura.md.
2. Cuando terminen, lanza `data-cleaner` para data/processed y docs/diccionario_variables.md.
3. Ejecuta `make data clean` y comprueba N, rangos y huecos.
4. PUERTA: resume estado (series OK, fallidas, huecos) y propone `/revisar`. No avances a F2 sin APROBAR.
$ARGUMENTS
