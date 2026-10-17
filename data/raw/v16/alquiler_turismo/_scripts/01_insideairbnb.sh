#!/bin/bash
# Descarga listings.csv.gz de las instantaneas espanolas de Inside Airbnb que faltan en data/raw/v9/insideairbnb.
# Listado de instantaneas: https://insideairbnb.com/page-data/sq/d/3176684073.json (country == Spain), consultado 2026-10-17.
# Licencia CC BY 4.0. Uso: bash 01_insideairbnb.sh <directorio_destino> (por defecto, el directorio original/insideairbnb)
DEST="${1:-/home/user/Econometr-a/data/raw/v16/alquiler_turismo/original/insideairbnb}"
mkdir -p "$DEST"
LISTA='catalonia/barcelona/2025-12-14 catalonia/barcelona/2026-03-21 catalonia/barcelona/2026-06-24
pv/euskadi/2025-12-31 pv/euskadi/2026-03-31 pv/euskadi/2026-06-30 pv/euskadi/2026-09-25
catalonia/girona/2025-12-31 catalonia/girona/2026-03-31 catalonia/girona/2026-06-30 catalonia/girona/2026-09-25
comunidad-de-madrid/madrid/2025-12-14 comunidad-de-madrid/madrid/2026-03-24 comunidad-de-madrid/madrid/2026-06-20
andaluc%C3%ADa/malaga/2025-12-31 andaluc%C3%ADa/malaga/2026-03-31 andaluc%C3%ADa/malaga/2026-06-30
islas-baleares/mallorca/2025-12-25 islas-baleares/mallorca/2026-03-26 islas-baleares/mallorca/2026-06-23
islas-baleares/menorca/2025-12-31 islas-baleares/menorca/2026-03-31 islas-baleares/menorca/2026-06-30 islas-baleares/menorca/2026-09-28
andaluc%C3%ADa/sevilla/2025-12-30 andaluc%C3%ADa/sevilla/2026-03-31 andaluc%C3%ADa/sevilla/2026-06-30 andaluc%C3%ADa/sevilla/2026-09-25
vc/valencia/2025-12-27 vc/valencia/2026-03-28 vc/valencia/2026-06-26'
for p in $LISTA; do
  ciudad=$(echo "$p" | cut -d/ -f2); fecha=$(echo "$p" | cut -d/ -f3)
  out="$DEST/listings_${ciudad}_${fecha}.csv.gz"
  [ -s "$out" ] && continue
  code=$(curl -sS -m 300 -o "$out" -w "%{http_code}" "https://data.insideairbnb.com/spain/$p/data/listings.csv.gz")
  echo "$ciudad $fecha $code $(stat -c %s "$out")"
  [ "$code" = 200 ] || rm -f "$out"
  sleep 2
done
sha256sum "$DEST"/*.csv.gz > "$DEST/sha256.txt"
