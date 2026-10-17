"""Fuente 4 (demanda_internacional, alternativa oficial): INE, ETDP, compraventas de vivienda
según condición del transmitente y del titular (persona física o jurídica), nacional.

Sustituye como alternativa oficial a las cifras de compra por personas jurídicas de Registradores
(ERI, derechos reservados) y de Notariado (portal con uso personal). El INE no publica desglose
por nacionalidad del comprador en el ETDP (se revisaron las 17 tablas de la operación ETDP).

Tablas: 50256 (anual) y 50272 (periodicidad según FK_Periodo en el propio fichero), servicio
wstempus del INE (DATOS_TABLA; respeta el uso del servicio: una petición por tabla).

Caché: no vuelve a descargar si el original existe, salvo FORCE=1.
Uso: python3 -I ine_etdp_titular.py
"""
import csv
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manifiesto import FAMILIA_DIR, ahora_utc, descargar, registrar, relativa, sha256_fichero  # noqa: E402

CARPETA = os.path.join(FAMILIA_DIR, "ine_etdp_titular")
FORCE = os.environ.get("FORCE") == "1"
TABLAS = {"50256": "mensual (FK_Periodo 1-12 = mes; 28 = año; verificado con fechas)", "50272": "mensual (FK_Periodo 1-12 = mes; 28 = año)"}
SALIDA = os.path.join(CARPETA, "ine_etdp_titular_largo.csv")


def url_tabla(cod):
    return f"https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{cod}?nult=400"


def main():
    os.makedirs(os.path.join(CARPETA, "originales"), exist_ok=True)
    filas = []
    for cod, frec in TABLAS.items():
        ruta = os.path.join(CARPETA, "originales", f"tabla_{cod}.json")
        if os.path.exists(ruta) and not FORCE:
            print("caché:", relativa(ruta))
        else:
            descargar(url_tabla(cod), ruta)
            print("descargado:", relativa(ruta))
        with open(ruta, encoding="utf-8") as f:
            serie_json = json.load(f)
        for s in serie_json:
            for d in s["Data"]:
                # El INE marca medianoche local (CET) como UTC del día anterior: se suma 12 h antes de truncar.
                f_ms = d["Fecha"] / 1000.0 + 12 * 3600
                fecha = datetime.fromtimestamp(f_ms, tz=timezone.utc).strftime("%Y-%m-%d")
                filas.append({
                    "fecha": fecha,
                    "periodo": f"{d['Anyo']}-{d['FK_Periodo']:02d}" if d["FK_Periodo"] <= 12 else f"{d['Anyo']}-anual",
                    "serie": s["COD"],
                    "valor": "" if d["Valor"] is None or d.get("Secreto") else d["Valor"],
                    "unidad": "porcentaje",
                    "fuente": "INE",
                    "url": url_tabla(cod),
                    "territorio": "España",
                    "nivel": "nacional",
                    "codigo": cod,
                    "descripcion": s["Nombre"].strip(),
                    "frecuencia_fuente": frec,
                    "fk_periodo": d["FK_Periodo"],
                    "secreto": d.get("Secreto", False),
                })
    filas.sort(key=lambda r: (r["serie"], r["fecha"]))
    os.makedirs(CARPETA, exist_ok=True)
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    sha = sha256_fichero(SALIDA)
    n_nan = sum(1 for r in filas if r["valor"] == "")
    registrar({
        "fuente": "INE, ETDP: compraventas de vivienda según condición del transmitente y del titular (50256, 50272)",
        "fichero": relativa(SALIDA),
        "url": url_tabla("50256") + "; " + url_tabla("50272"),
        "fecha_descarga": ahora_utc(),
        "edicion": "tablas INE vigentes en la fecha de descarga",
        "periodo": f"{min(r['fecha'] for r in filas)} a {max(r['fecha'] for r in filas)}",
        "nivel_territorial": "nacional",
        "n_filas": len(filas),
        "sha256": sha,
        "licencia": "INE: reutilización con cita (Ley 37/2007; aviso legal del INE: https://www.ine.es/aviso_legal.htm)",
        "redistribuible": "sí",
        "notas": f"Porcentajes de compraventa de vivienda por tipo de transmitente y titular (persona física/jurídica). No hay desglose por nacionalidad del comprador en el ETDP. NaN = {n_nan}. Originales en {relativa(os.path.join(CARPETA, 'originales'))}.",
    })
    print("filas:", len(filas), "NaN:", n_nan, "sha256:", sha)


if __name__ == "__main__":
    main()
