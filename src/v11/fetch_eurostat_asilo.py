"""V11-DATOS (bloque 1, punto 6, respaldo): Eurostat, protección internacional, protección temporal y permisos de
residencia en vigor, España (geo = ES), por nacionalidad. Nivel NACIONAL: Interior (Oficina de Asilo y Refugio) e
Inclusión (OPI), que publican el desglose provincial, rechazan la conexión desde el entorno (Cloudflare o WAF; ver
docs/v11/fuentes_fallidas.md). Estas series no sustituyen al desglose provincial; documentan el agregado y la
composición por nacionalidad.

Tablas: migr_asyappctzm (solicitantes, mensual, 2008-), migr_asydcfstq (resoluciones de primera instancia,
trimestral, 2008-), migr_asytpsm (beneficiarios de protección temporal a fin de mes, 2022-03-), migr_asytpfm
(concesiones de protección temporal, mensual, 2022-03-), migr_asytpfa (anual), migr_resvalid (permisos de residencia
en vigor a 31-12 por motivo y duración, 2008-). Licencia Eurostat: reutilización con cita (Decisión 2011/833/UE).
Salida: data/raw/v11/eurostat_asilo/<tabla>_es.csv.gz (formato largo: dimensiones, periodo, valor, marca,
posterior_prereg). Se guardan solo sexo = T y edad = TOTAL
y se omiten las celdas con valor 0 (ausencia de fila = 0 o no disponible).
"""
from __future__ import annotations

import gzip
import io
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import GZ_PANDAS, RAW11, descargar, marcar_posterior_prereg, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "eurostat_asilo"
DIR = RAW11 / FUENTE
URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{c}/?format=TSV&compressed=true"
LIC = "Eurostat: reutilización con cita (Decisión 2011/833/UE)"
TABLAS = {"migr_asyappctzm": "solicitantes de protección internacional por nacionalidad, sexo, edad y tipo (mensual)",
          "migr_asydcfstq": "resoluciones de primera instancia por nacionalidad y decisión (trimestral)",
          "migr_asytpsm": "beneficiarios de protección temporal a fin de mes por nacionalidad",
          "migr_asytpfm": "concesiones de protección temporal por nacionalidad (mensual)",
          "migr_asytpfa": "concesiones de protección temporal por nacionalidad (anual)",
          "migr_resvalid": "permisos de residencia en vigor a 31-12 por motivo, duración y nacionalidad"}


def largo(zp: Path) -> pd.DataFrame:
    with gzip.open(zp, "rt", encoding="utf-8") as f:
        cab = f.readline().rstrip("\n").split("\t")
        filas = [ln.rstrip("\n").split("\t") for ln in f if ln.split("\t", 1)[0].endswith(",ES")]
    dims = cab[0].split("\\")[0].split(",")
    d = pd.DataFrame(filas, columns=[c.strip() for c in cab])
    d[dims] = d[cab[0]].str.split(",", expand=True)
    d = d.drop(columns=cab[0]).melt(id_vars=dims, var_name="periodo", value_name="bruto")
    d["valor"] = pd.to_numeric(d.bruto.str.extract(r"^\s*([\d.]+)")[0], errors="coerce")
    d["marca"] = d.bruto.str.extract(r"^\s*[\d.:]*\s*([a-z]*)\s*$")[0].fillna("")
    d = d[d.valor.notna() & (d.valor != 0)].drop(columns=["bruto", "geo"])
    for dim, tot in (("sex", "T"), ("age", "TOTAL")):  # solo totales de sexo y edad (tamaño)
        if dim in d:
            d = d[d[dim] == tot].drop(columns=dim)
    d["periodo"] = d.periodo.str.strip()
    d = marcar_posterior_prereg(d.assign(_f=d.periodo.str.replace("-Q", "Q", regex=False)), "_f").drop(columns="_f")
    return d


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    for c, desc in TABLAS.items():
        zp = descargar(URL.format(c=c), DIR / "original" / f"{c}.tsv.gz", timeout=600)
        d = largo(zp)
        r = DIR / f"{c}_es.csv.gz"
        d.sort_values(list(d.columns[:-3])).to_csv(r, index=False, compression=GZ_PANDAS)
        registrar(FUENTE, r, URL.format(c=c), edicion=f"Eurostat {c} (descarga {pd.Timestamp.today():%Y-%m-%d})",
                  periodo=f"{d.periodo.min()}–{d.periodo.max()}", nivel_territorial="España (nacional)", licencia=LIC,
                  redistribuible=True, notas=f"{desc}; filas posteriores a 2026-07-01 marcadas posterior_prereg="
                                              f"{int(d.posterior_prereg.sum())}")
        print(c, len(d), d.periodo.min(), d.periodo.max())
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
