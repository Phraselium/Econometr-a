"""V11-DATOS (bloque 4, punto 15; instrumento migratorio): Seguridad Social, afiliados EXTRANJEROS por provincia
(último día del periodo de cada fichero anual: diciembre, o el último mes publicado del año en curso), total del sistema.
Página: «Afiliados Extranjeros» (EST8/EST10/EST305/EST307); los enlaces a los xlsx anuales se leen de la página en
cada ejecución (hoja «3.TS SEXO PROV CCAA REG»: filas con código numérico de provincia; columnas 2-4 = mujer, varón,
total del sistema; se toma solo el primer bloque, UE + no UE). El fichero municipal (MUNCNAE) no distingue nacionalidad. Licencia: reutilización con cita.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, descargar, marcar_posterior_prereg, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "ss_afiliacion_extranjeros"
DIR = RAW11 / FUENTE
PAG = "https://www.seg-social.es/wps/portal/wss/internet/EstadisticasPresupuestosEstudios/Estadisticas/EST8/EST10/EST305/EST307"
LIC = "Seguridad Social: reutilización con cita (Ley 37/2007)"
MESES = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
         "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    html = requests.get(PAG, headers=CABECERAS, timeout=120).text
    enlaces = sorted(set(re.findall(r'href="(/wps/wcm/connect/wss/[^"]*Extranjeros[^"]*\.xlsx)', html)))
    filas = []
    for e in enlaces:
        anio = re.search(r"(20\d\d)", e).group(1)
        zp = descargar("https://www.seg-social.es" + e + "?MOD=AJPERES", DIR / "original" / f"extranjeros_{anio}.xlsx", timeout=300)
        x = pd.read_excel(zp, sheet_name="3.TS SEXO PROV CCAA REG", header=None)
        fecha = str(x.iloc[1, 0]).strip()
        m = re.search(r"(\d{1,2})\s+(\w+)\s+(\d{4})", fecha)
        mes = f"{m.group(3)}-{MESES[m.group(2).lower()]:02d}" if m else f"{anio}-12"
        c0 = x[0].astype(str).str.strip()
        ini = c0[c0 == "TOTAL"].index[0]
        fin = next((i for i in c0[c0 == "PROVINCIA"].index if i > ini), len(x))
        b = x.loc[ini:fin - 1]   # primer bloque: Unión Europea + no Unión Europea
        p = b[pd.to_numeric(b[0], errors="coerce").between(1, 52)]
        for r in p.itertuples(index=False):
            filas.append({"mes": mes, "cod_provincia": f"{int(r[0]):02d}", "mujeres": r[2], "varones": r[3], "total": r[4]})
        registrar(FUENTE, zp, "https://www.seg-social.es" + e, edicion=f"Afiliados extranjeros, {fecha}", periodo=mes,
                  nivel_territorial="provincia", licencia=LIC, redistribuible=True, notas="original xlsx; no versionado")
    D = marcar_posterior_prereg(pd.DataFrame(filas).sort_values(["mes", "cod_provincia"]), "mes")
    r = DIR / "afiliados_extranjeros_provincia.csv.gz"
    D.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, PAG, edicion="Seguridad Social, afiliados extranjeros (ficheros anuales)", periodo=f"{D.mes.min()}–{D.mes.max()}",
              nivel_territorial="provincia", licencia=LIC, redistribuible=True, notas=f"total del sistema; meses={sorted(D.mes.unique())}")
    print(D.groupby("mes").total.sum())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
