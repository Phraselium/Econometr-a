"""V11-DATOS, segunda pasada (punto 5, réplica parcial de la OPI): Comunidad de Madrid, portal de datos abiertos
(datos.comunidad.madrid, CC BY 4.0), republicación de la estadística de la OPI «Extranjeros con certificado de registro o
tarjeta de residencia en vigor» para la Comunidad de Madrid (provincia 28): por continente y país de nacionalidad y
sexo; por grupos de edad y tipo de documentación; certificados de registro por motivo de concesión. Anual (31-12),
2013-2025. La fuente original (inclusion.gob.es) rechaza el acceso desde el entorno (bloqueo del servidor, 403 por
IP también con navegador). Solo cubre Madrid: no sustituye el desglose provincial de toda España.
Codificación latin-1, separador «;».
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "opi_replica_madrid"
DIR = RAW11 / FUENTE
B = "https://datos.comunidad.madrid/dataset/"
LIC = "Comunidad de Madrid: CC BY 4.0 (republicación de datos de la OPI, Ministerio de Inclusión)"
RECURSOS = {
    "pais_sexo": B + "cb6c6347-7bd2-46e7-bee4-d5c1c1f2682a/resource/8097ecf3-0e9a-4b0d-af38-27f75564970c/download/"
                 "extranjeros-con-certificado-de-registro-o-tarjeta-de-residencia-en-vigor-por-continente-pais-de-.csv",
    "edad_tipo": B + "1d63d5a5-9419-4b86-8524-64e07e1e9879/resource/115f75c5-0557-43bd-89d8-d845fc3e09d5/download/"
                 "extranjeros-con-certificado-de-registro-o-tarjeta-de-residencia-en-vigor-por-grupos-de-edad-y-ti.csv",
    "motivo": B + "b4b8f6be-abfc-46fe-a914-8b0fd94fecd7/resource/15104612-9827-4b64-bfe4-92f3551904f4/download/"
              "extranjeros-con-certificado-de-registro-en-vigor-por-motivo-de-concesion.csv",
}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for k, url in RECURSOS.items():
        zp = descargar(url, DIR / "original" / f"{k}.csv", timeout=300)
        d = pd.read_csv(zp, sep=";", encoding="latin-1", dtype=str, keep_default_na=False)
        d.columns = ["anio", "concepto", "tipo_territorio", "codigo_territorio", "territorio", "sexo", "valor", "unidad", "estado_dato"][:len(d.columns)]
        d = d[d.anio.str.fullmatch(r"\d{4}")]
        r = DIR / f"opi_madrid_{k}.csv.gz"
        d.to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, url, edicion="datos.comunidad.madrid (modificado 2026-09-16)", periodo=f"{d.anio.min()}-{d.anio.max()}",
                  nivel_territorial="Comunidad de Madrid (provincia 28)", licencia=LIC, redistribuible=True, notas=f"{k}; filas={len(d)}")
        print(k, len(d), d.anio.min(), d.anio.max())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
