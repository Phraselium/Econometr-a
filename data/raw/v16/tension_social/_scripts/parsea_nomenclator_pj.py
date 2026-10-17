"""Extrae del PDF del Nomenclator de Partidos Judiciales (Min. Justicia, 30/12/2025) la tabla
partido judicial (n.º dentro de provincia) -> codigo INE de municipio. Uso: python3 -I parsea_nomenclator_pj.py <pdf> <salida.csv>
Requiere pdftotext. Derivado: el original sin transformar es el PDF."""
import re, subprocess, sys, csv
pdf, out = sys.argv[1], sys.argv[2]
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
rx = re.compile(r"^\s*(\d{1,3})\s+(\d{5})\s+([\d\.]+)\s+(.+?)\s*$")
prov = ""
rows = []
for ln in txt.splitlines():
    m = re.match(r"^\s*PROVINCIA DE (.+?)\s*$", ln)
    if m:
        prov = m.group(1)
        continue
    m = rx.match(ln)
    if m:
        pj, cod, pob, nom = m.groups()
        rows.append((cod[:2], prov, int(pj), cod, int(pob.replace(".", "")), nom))
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cod_provincia", "provincia_pdf", "partido_judicial_n", "cod_municipio_ine", "poblacion", "municipio"])
    w.writerows(rows)
print(len(rows), "filas;", len({r[3] for r in rows}), "municipios unicos;", len({(r[0], r[2]) for r in rows}), "partidos")
