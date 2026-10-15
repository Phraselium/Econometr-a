"""V11-DATOS (bloque 4, punto 16): Euskadi, Registro de Empresas y Actividades Turísticas (REATE), viviendas y
habitaciones de vivienda particular para uso turístico (Open Data Euskadi, CC BY 4.0):
https://opendata.euskadi.eus/contenidos/ds_recursos_turisticos/habitaciones_viviendas_turisti/opendata/{viviendas,habitaciones}.xlsx
Corte VIGENTE con «Fecha inscripción REATE» (alta); el fichero abierto no trae bajas (solo el servicio de intercambio
con certificado, tipo M «movimientos»; no accesible). Se eliminan los campos identificativos (nombre comercial,
dirección, web, teléfono, correo); se conservan nº de registro, fecha de inscripción, tipo, modalidad, código postal,
código INE de municipio (provincia + municipio a 3 dígitos), capacidad, baños y superficie.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "euskadi_vut"
DIR = RAW11 / FUENTE
URL = "https://opendata.euskadi.eus/contenidos/ds_recursos_turisticos/habitaciones_viviendas_turisti/opendata/{f}.xlsx"
LIC = "Open Data Euskadi: CC BY 4.0"
QUITAR = ["Nombre comercial", "Dirección", "Web", "Teléfono", "Email", "Localidad"]


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    hoy = dt.date.today().isoformat()
    for f in ("viviendas", "habitaciones"):
        zp = descargar(URL.format(f=f), DIR / "original" / f"{f}_{hoy}.xlsx", timeout=300)
        d = pd.read_excel(zp, dtype=str).drop(columns=QUITAR, errors="ignore")
        d["cod_municipio"] = d["Código provincia"].str.zfill(2) + d["Código municipio"].str.zfill(3)
        d["fecha_inscripcion"] = pd.to_datetime(d["Fecha inscripción REATE"], dayfirst=True, errors="coerce").dt.date.astype(str)
        r = DIR / f"reate_{f}_{hoy}.csv.gz"
        d.to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, URL.format(f=f), edicion=f"REATE, corte {hoy}", periodo=f"{d.fecha_inscripcion.min()}–{d.fecha_inscripcion.max()} (inscripciones vigentes)",
                  nivel_territorial="registro individual (municipio INE, código postal)", licencia=LIC, redistribuible=True,
                  notas="sin campos identificativos; solo altas vigentes (sin bajas)")
        registrar(FUENTE, zp, URL.format(f=f), edicion=f"REATE, corte {hoy}", periodo=hoy, nivel_territorial="registro individual",
                  licencia=LIC, redistribuible=False, notas="original con datos de contacto: no se versiona")
        print(f, len(d), d.fecha_inscripcion.min(), d.fecha_inscripcion.max())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
