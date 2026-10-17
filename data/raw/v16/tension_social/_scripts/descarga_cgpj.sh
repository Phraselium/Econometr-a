#!/bin/bash
# Descarga ficheros CGPJ (Efecto de la crisis en los organos judiciales). Crawl-delay 5 s (robots.txt).
# Destino: _terceros (licencia no clara -> redistribuible dudoso). Uso: bash descarga_cgpj.sh <directorio_destino>
set -u
D="$1"; mkdir -p "$D"
B="https://www.poderjudicial.es/stfls/ESTADISTICA/FICHEROS/Crisis/"
get() {
  local out="$1" name="$2"
  curl -sS -m 180 -A "Mozilla/5.0 (investigacion academica; Econometr-a)" -o "$D/$out" -w "$out %{http_code} %{size_download}\n" "$B$(python3 -I -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$name")"
  sleep 6
}
get cgpj_lanzamientos_partidos_judiciales_2013_2025.xlsx "Lanzamientos por PJs_2013_ 2025.xlsx"
get cgpj_series_tsj_2T2026.xlsx "Series - Efecto de la crisis en los organos judiciales por TSJ 2T-2026.xlsx"
get cgpj_series_provincias_2T2026.xlsx "Series - Efecto de la crisis en los organos judiciales por provincias 2T-2026.xlsx"
get cgpj_datos_crisis_2T2026.xlsx "Datos sobre el efecto de la crisis en los organos judiciales 2T-2026- con Microempresas.xlsx"
get cgpj_datos_crisis_anual2025.xlsx "Datos sobre el efecto de la crisis en los organos judiciales - Anual 2025.xlsx"
sha256sum "$D"/*.xlsx
