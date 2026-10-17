"""V15 · Correcciones de metadatos de la base 1.0 antes del depósito (ERRATA.md; docs/v15/decisiones.md G4 y G8).

Aplica a la base ya construida lo mismo que hacen ahora src/v10/base.py y src/v11/base_v11.py:
1. `obra_nueva_neta_catastro`: el fichero «año t» del Catastro es el stock a 31-12-(t−1), así que la diferencia etiquetada t
   es la obra neta del año t−1: periodo − 1, fecha_dato = 31-12 de ese año y `posterior_prereg` recalculado. Valores iguales.
2. `ipc_alquiler_indice`: unidad «índice 2025=100» (la media de 2025 es 100; la de 2021, 92,7).
3. `permisos`: unidad «índice 2021=100 (SCA)» y fuente Eurostat sts_cobp_q (no visados del MIVAU).
Ficheros: data/base/{hechos,variables}.parquet, data/base/publica/{hechos,variables}.parquet y las tablas `hechos` y
`variables` de data/base/vivienda.duckdb. Comprueba que ningún valor cambia. Idempotente; sin red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
CLAVE = "territorio_codigo, nivel, periodo, frecuencia, variable, desagregacion"
U_IPC, U_PERM = "índice 2025=100", "índice 2021=100 (SCA)"
F_PERM = "Eurostat, sts_cobp_q: permisos de construcción, número de viviendas (BPRM_DW), índice desestacionalizado"
OBRA = "obra_nueva_neta_catastro"


def sql_hechos(t: str) -> list[str]:
    return [f"UPDATE {t} SET unidad = '{U_IPC}' WHERE variable = 'ipc_alquiler_indice'",
            f"UPDATE {t} SET unidad = '{U_PERM}', fuente = '{F_PERM}' WHERE variable = 'permisos'",
            # solo si sigue con la etiqueta antigua (fecha_dato = 31-12 del periodo y primer periodo 2013): idempotente
            f"""UPDATE {t} SET periodo = CAST(CAST(periodo AS INTEGER) - 1 AS VARCHAR),
                    fecha_dato = CAST(CAST(periodo AS INTEGER) - 1 AS VARCHAR) || '-12-31',
                    posterior_prereg = (CAST(CAST(periodo AS INTEGER) - 1 AS VARCHAR) || '-12-31') >= '2026-07-01'
                WHERE variable = '{OBRA}' AND (SELECT min(periodo) FROM {t} WHERE variable = '{OBRA}') = '2013'"""]


def sql_variables(t: str) -> list[str]:
    return [f"UPDATE {t} SET unidad = '{U_IPC}' WHERE variable = 'ipc_alquiler_indice'",
            f"UPDATE {t} SET unidad = '{U_PERM}', fuente = '{F_PERM}' WHERE variable = 'permisos'",
            f"""UPDATE {t} SET primer_periodo = CAST(CAST(primer_periodo AS INTEGER) - 1 AS VARCHAR),
                    ultimo_periodo = CAST(CAST(ultimo_periodo AS INTEGER) - 1 AS VARCHAR)
                WHERE variable = '{OBRA}' AND primer_periodo = '2013'"""]


def huella_valores(con, t: str) -> tuple:
    """Huella independiente del orden de las filas (sin periodo, que es lo que se corrige en la obra neta)."""
    e = "hash(concat_ws('|', territorio_codigo, nivel, frecuencia, variable, desagregacion, CAST(valor AS VARCHAR)))"
    return con.execute(f"SELECT count(*), sum(CAST({e} AS HUGEINT)), bit_xor({e}) FROM {t}").fetchone()


def corregir_parquet(hechos: Path, variables: Path) -> None:
    con = duckdb.connect()
    con.execute("SET threads TO 4")
    con.execute("SET preserve_insertion_order=true")
    con.execute(f"CREATE TABLE h AS SELECT * FROM read_parquet('{hechos}')")
    cols = [c for c, in con.execute("SELECT column_name FROM (DESCRIBE h)").fetchall()]
    antes = huella_valores(con, "h")
    for s in sql_hechos("h"):
        con.execute(s)
    if huella_valores(con, "h") != antes:
        raise SystemExit(f"correcciones_metadatos: {hechos} cambiaría valores; no se escribe")
    tmp = hechos.with_suffix(".tmp.parquet")
    con.execute(f"COPY (SELECT {', '.join(cols)} FROM h ORDER BY {CLAVE}) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
    tmp.replace(hechos)
    import pandas as pd
    v = pd.read_parquet(variables)
    con.register("v0", v)
    con.execute("CREATE TABLE v AS SELECT * FROM v0")
    for s in sql_variables("v"):
        con.execute(s)
    out = con.execute("SELECT * FROM v").df()[v.columns]
    out.to_parquet(variables, index=False, compression="zstd")
    print(f"correcciones_metadatos: {hechos.relative_to(RAIZ)} y {variables.relative_to(RAIZ)} corregidos")


def main() -> int:
    for base in (RAIZ / "data/base", RAIZ / "data/base/publica"):
        if (base / "hechos.parquet").exists():
            corregir_parquet(base / "hechos.parquet", base / "variables.parquet")
    db = RAIZ / "data/base/vivienda.duckdb"
    if db.exists():
        con = duckdb.connect(str(db))
        con.execute("BEGIN TRANSACTION")
        antes = huella_valores(con, "hechos")
        for s in sql_hechos("hechos") + sql_variables("variables"):
            con.execute(s)
        if huella_valores(con, "hechos") != antes:
            con.execute("ROLLBACK")
            raise SystemExit("correcciones_metadatos: vivienda.duckdb cambiaría valores")
        con.execute("COMMIT")
        con.close()
        print("correcciones_metadatos: data/base/vivienda.duckdb corregido")
    return 0


if __name__ == "__main__":
    sys.exit(main())
