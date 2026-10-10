# Estado v4

| Tarea | Oleada | Estado | Capa | Resultado principal | Tokens subagentes |
|---|---|---|---|---|---|
| Setup | 0 | hecho | — | — | 0 |
| M0 verificador (veredictos separados, convenciones A/B), topes fuera de C3 | A | hecho | — | 14 fichas reclasificadas | 0 (orquestador) |
| M0 conciliación del déficit, terminadas y GL | A | hecho | C1/C2/C4 | Cadena v1→v3 exacta (hogares −55 mil; protegida −56 mil; stock a 1-ene −54 mil); BdE: residuo +49 mil; terminadas C1 2018-2025 (2024: 91-94 mil); GL: la atenuación del stock explica la magnitud, no el signo | 86.130 |
| M2 descomposición de hogares | A | hecho | C1 (ΔH)/C4 (componentes)/C2 (latente) | 2021-25: ΔH +998 mil; extranjeros 56 %, nativos 9 %, estructura 17 %, tasa 17 % (C4); sin latente neta total; 16-34 +70 mil (C2) | 88.168 |
| M1 geografía del déficit | A | hecho | C1 (25 prov.)/C4 | 2021-25 suma provincial mediana 797 mil [288 mil-1,37 M]; 5 provincias = 50 %, 17 = 80 %; municipios 25 = 50 % (C4) | 83.864 |
| M3 ¿se puede construir? | B | en curso | — | — | — |
| Revisión oleada A (M0-M2) | A | en curso | — | — | — |
| M4 parque frente a mercado | B | en curso | — | — | — |

**Hecho:** setup; M0.
**Siguiente:** M1, M2 (corrección), M4 → revisión de la oleada A → M3 → M5 → M6.
**Tokens de subagentes v4:** 258.162 / 2.500.000 (cierre al 80 %: 2.000.000).

## M3 (2026-10-10)
- Hecho: extracción Catastro (data/raw/v4/catastro_solares_municipios.csv.gz), brecha precio-coste, multiverso, clasificación en output/v4/M3. Recuentos PROVISIONALES: dependen de M1 (en corrección).
- Siguiente: reejecutar `python3 src/v4/m3_run.py` cuando M1 esté corregido. Sin fuente de coste en nivel (supuesto 900-1.500).
- Tokens de subagente M3: aprox. 100.000.

## M4 parque frente a mercado (subagente)
- Hecho: stock por uso (nacional, 50 provincias, 7 ciudades), tenencia Censo 2021, flujo de personas jurídicas (ETDP), ficha de extranjeros (MIVAU, Notariado, Registradores), Airbnb como robustez, 3 fichas. Salidas en output/v4/M4/; descargas en data/raw/v4.
- Fallos: ver docs/v4/fuentes_fallidas.md (titulares del Catastro, arrendador de Incasòl).
- Siguiente: integrar M4 en el informe; si se obtiene una fuente de titularidad, reabrir M4-V2.
