# data/cache/v12 · caché interna (NO difundible)

`od_seleccion.csv.gz`: flujos origen-destino de los microdatos de la EVR (2002-2020) y la EMCR (2021-2024) del INE con
origen o destino en las cinco áreas de V12-B2, por año × edad × nacionalidad. Se versiona solo para que `make v12`
funcione sin los microdatos completos (no versionados por tamaño). Contiene celdas pequeñas (muchas < 5): no se
publica, no entra en la base ni en la web; las salidas difundibles (output/v12/b2) son agregados por área y periodo.
Se regenera borrándola y ejecutando `python3 src/v12/b2_flujos.py` con los microdatos en data/raw/v11.
