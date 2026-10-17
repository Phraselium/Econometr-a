#!/bin/bash
# INE Tempus (API oficial): EOAP (op 239), EOH (op 238), OAT (op 429), IPAP (op 61), VTE (op 410).
# nult=1000 devuelve toda la serie disponible de cada tabla. Licencia: aviso legal INE (reutilizacion con cita).
# Uso: bash 02_ine_turismo.sh <directorio_destino>
DEST="${1:-/home/user/Econometr-a/data/raw/v16/alquiler_turismo/original/ine_turismo}"
mkdir -p "$DEST"
TABLAS="2072 2083 75193 2021 2022 2082 75191 2063 61766 67191 75192 1993 3151 2025 61768
2074 2066 67190 49371 2078 2076 75197 75198 2039 2013
48441 48440 48424 48429 48427 48426 48431 48432 48423 48428
1989 2050
39364 39363 46141 39365 39366"
for t in $TABLAS; do
  out="$DEST/ine_tabla_${t}_2026-10-17.json"
  [ -s "$out" ] && continue
  code=$(curl -sS -m 300 -o "$out" -w "%{http_code}" "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/${t}?nult=1000")
  echo "$t $code $(stat -c %s "$out")"
  [ "$code" = 200 ] || rm -f "$out"
  sleep 1
done
