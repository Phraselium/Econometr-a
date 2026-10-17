#!/bin/bash
# Descarga INE (jaxiT3 CSV y PC-Axis). Uso: bash descarga_ine.sh <directorio_destino>
set -u
D="$1"; mkdir -p "$D/emcr" "$D/padron_seccion_2022_nacionalidad_continentes" "$D/padron_cifras_oficiales"
UA="Mozilla/5.0 (investigacion academica; Econometr-a)"
# EMCR (op 455) y Cifras oficiales padron (op 22) por municipio
for t in 69696 69711 69743 69745 69744 69746 69767; do
  curl -sS -m 180 -A "$UA" -o "$D/emcr/ine_emcr_tabla_$t.csv" -w "emcr $t %{http_code} %{size_download}\n" "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/$t.csv?nocab=1"; sleep 2
done
curl -sS -m 180 -A "$UA" -o "$D/padron_cifras_oficiales/ine_cifras_oficiales_padron_municipio_29005.csv" -w "29005 %{http_code} %{size_download}\n" "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/29005.csv?nocab=1"
# Padron por seccion censal 2022, sexo x seccion x nacionalidad (continentes): ficheros NN02.px, NN = provincia
for p in $(seq -w 1 52); do
  curl -sS -m 120 -A "$UA" -o "$D/padron_seccion_2022_nacionalidad_continentes/${p}02.px" -w "px $p %{http_code} %{size_download}\n" "https://www.ine.es/jaxi/files/_px/es/px/t20/e245/p07/a2022/l0/${p}02.px"; sleep 1
done
find "$D" -type f -exec sha256sum {} +
