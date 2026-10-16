# Padrón Municipal de València (Oficina d'Estadística): ficheros y variantes de nombre

Sondeo del 2026-10-16 (petición HEAD/rango a cada variante, años 1990-2026; 206 = existe). Base: `https://www.valencia.es/estadistica/Padron/`.

| Publicación | Patrón que existe | Años | Variantes que NO existen | Usada |
|---|---|---|---|---|
| Padrón, «Características de la población» | `<A>/Padron<A>.pdf` | 2001-2013, 2015 | `...Cast.pdf`/`...Val.pdf` en esos años; 1990-2000 ningún patrón | sí |
| | `<A>/Padron<A>Cast.pdf` y `<A>/Padron<A>Val.pdf` | 2016-2026 | `Padron<A>.pdf` | Cast 2016-2024; **Val 2025-2026** (el Cast usa fuentes sin mapa Unicode: «(cid:..)») |
| | — | **2014** | ninguna variante (`Padron2014.pdf`, `Cast`, `Val`) | — |
| Población extranjera | `<A>/Pob_estrangera_<A>.pdf` | 2001-2015 (incl. 2014) | `_Cas/_Cast/_Val` | sí |
| | `<A>/Pob_estrangera_<A>_Cas.pdf` y `_Val.pdf` | 2016-2023 | `_Cast` | Cas |
| | `<A>/Pob_estrangera_<A>_Cast.pdf` y `_Val.pdf` | 2024-2026 | `_Cas` | Cast 2024; Val 2025-2026 (con OCR en las páginas «(cid:..)») |
| Altas y bajas | `AltasBajas/<A>/AltasBajasPadron<A>.pdf` | 2004-2016 | 2017-2026 en ambas rutas | sí |
| | `<A>/AltasBajasPadron<A>.pdf` | 2007-2014 (copias) | — | no (duplicados) |

Extracción: `src/v11/extrae_vlc_padron.py` (pdfplumber; OCR con ocrmypdf `-l spa` solo en páginas con «(cid:»). Códigos: barrio = 46250 + DD + BB y
distrito = 46250 + DD, leídos del número «D.B.» impreso en el PDF (nunca por nombre). La tabla `data/raw/v11/vlc_padron/equivalencias_barrios.csv`
compara el nombre del PDF con el del geoportal: 2.175 pares, 31 sin coincidencia de nombre, todos revisados (Mauella = Rafalell-Vistabella, 17.5;
Les Moreres 11.6 solo en 2002; 2001 con valores desplazados en Poblats Marítims, reparados con el total del distrito).
