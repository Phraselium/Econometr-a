"""Fuente 2 (demanda_internacional): Banco de España, nuevas operaciones de crédito a la vivienda
de hogares por periodo inicial de fijación del tipo (Boletín Estadístico, cap. 19).

Tablas (CSV del BdE, codificación latin-1, formato ancho; una serie por columna):
- be1903: TEDR nuevas operaciones, crédito a la vivienda (total, excluidas y renegociadas).
- be1904: TEDR nuevas operaciones por periodo de fijación (hasta 1 año, 1-5, 5-10, más de 10).
- be1911: importes totales estimados de nuevas operaciones, crédito a la vivienda.
- be1912: importes por periodo de fijación (hasta 1 año, 1-5, 5-10, más de 10).

Limitación: el BdE clasifica por periodo inicial de fijación, no por «fijo» frente a «variable»;
«hasta 1 año» es la aproximación a tipo variable y «más de 1 año» a tipo fijo inicial. Se declara en la ficha.

Caché: no vuelve a descargar si el original existe, salvo FORCE=1.
Uso: python3 -I bce_fijacion.py
"""
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifiesto import FAMILIA_DIR, ahora_utc, descargar, registrar, relativa, sha256_fichero  # noqa: E402

CARPETA = os.path.join(FAMILIA_DIR, "bde_fijacion")
FORCE = os.environ.get("FORCE") == "1"
BASE = "https://www.bde.es/webbe/es/estadisticas/compartido/datos/csv/"
TABLAS = ["be1903", "be1904", "be1911", "be1912"]
MESES = {"ENE": 1, "FEB": 2, "MAR": 3, "ABR": 4, "MAY": 5, "JUN": 6, "JUL": 7,
         "AGO": 8, "SEP": 9, "SET": 9, "OCT": 10, "NOV": 11, "DIC": 12}
SALIDA = os.path.join(CARPETA, "bde_nuevas_fijacion_vivienda.csv")


def leer_tabla(ruta):
    with open(ruta, encoding="latin-1", newline="") as f:
        return list(csv.reader(f, delimiter=","))


def parsear(nombre_tabla, ruta):
    filas = leer_tabla(ruta)
    url = BASE + nombre_tabla + ".csv"
    series, unidad, frec, cabeceras = {}, {}, {}, {}
    filas_datos = []
    for fila in filas:
        if not fila:
            continue
        etiqueta = fila[0].strip()
        valores = fila[1:]
        if etiqueta == "CÓDIGO DE LA SERIE":
            for i, cod in enumerate(valores):
                series[i] = cod
        elif etiqueta == "DESCRIPCIÓN DE LA SERIE":
            for i, d in enumerate(valores):
                cabeceras[i] = d
        elif etiqueta == "DESCRIPCIÓN DE LAS UNIDADES":
            for i, u in enumerate(valores):
                unidad[i] = u
        elif etiqueta == "FRECUENCIA":
            pass
        elif re.match(r"^[A-Z]{3} \d{4}$", etiqueta):
            mes, anio = etiqueta.split()
            filas_datos.append((int(anio), MESES[mes], valores))
    registros = []
    for anio, mes, valores in filas_datos:
        for i, v in enumerate(valores):
            if i not in series or i not in cabeceras:
                continue
            desc = cabeceras[i]
            if "Crédito vivienda" not in desc and "Crédito a la vivienda" not in desc:
                continue
            if "Hogares" not in desc:
                continue
            valor = "" if v.strip() in ("_", "") else v.strip()
            periodo = f"{anio}-{mes:02d}"
            registros.append({
                "fecha": f"{periodo}-01",
                "periodo": periodo,
                "serie": series[i],
                "valor": valor,
                "unidad": unidad.get(i, ""),
                "fuente": "BdE",
                "url": url,
                "territorio": "España",
                "nivel": "nacional",
                "codigo": nombre_tabla,
                "descripcion": desc,
            })
    return registros, series, cabeceras


def main():
    os.makedirs(CARPETA, exist_ok=True)
    originales = os.path.join(CARPETA, "originales")
    os.makedirs(originales, exist_ok=True)
    todos = []
    for t in TABLAS:
        ruta = os.path.join(originales, t + ".csv")
        if os.path.exists(ruta) and not FORCE:
            print("caché:", relativa(ruta))
        else:
            descargar(BASE + t + ".csv", ruta)
            print("descargado:", relativa(ruta))
        registros, series, cab = parsear(t, ruta)
        todos.extend(registros)
        print(t, "series de vivienda:", len({r["serie"] for r in registros}))
    todos.sort(key=lambda r: (r["serie"], r["fecha"]))
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(todos[0].keys()))
        w.writeheader()
        w.writerows(todos)
    sha_sal = sha256_fichero(SALIDA)
    n_nan = sum(1 for r in todos if r["valor"] == "")
    fechas = sorted({r["periodo"] for r in todos})
    registrar({
        "fuente": "Banco de España, nuevas operaciones de crédito a la vivienda por periodo de fijación (BE tablas 19.3, 19.4, 19.11, 19.12)",
        "fichero": relativa(SALIDA),
        "url": BASE + "be1903.csv; " + BASE + "be1904.csv; " + BASE + "be1911.csv; " + BASE + "be1912.csv",
        "fecha_descarga": ahora_utc(),
        "edicion": "CSV del BdE vigentes en la fecha de descarga (sin número de edición en el fichero)",
        "periodo": f"{fechas[0]} a {fechas[-1]}",
        "nivel_territorial": "nacional",
        "n_filas": len(todos),
        "sha256": sha_sal,
        "licencia": "Banco de España: reutilización con cita de la fuente (aviso legal del BdE: https://www.bde.es/wbe/es/aviso-legal/); robots.txt sin restricción sobre /csv/",
        "redistribuible": "sí",
        "notas": f"Formato largo. NaN (celdas «_» del BdE) = {n_nan}. Clasificación por periodo inicial de fijación, no fijo/variable: «hasta 1 año» aproxima variable. Originales en {relativa(originales)}.",
    })
    print("filas:", len(todos), "NaN:", n_nan, "sha256:", sha_sal)


if __name__ == "__main__":
    main()
