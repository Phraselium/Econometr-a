"""V15 · Marca `muestra_sellada_v6` en las filas de municipio, distrito y sección de las 11 provincias selladas en v6.

Aplica a la base ya construida la misma regla que src/v10/base.py desde V15 (docs/v15/contaminacion_v6.md):
    muestra_sellada_v6 = nivel ∈ {provincia, municipio, distrito, seccion} y provincia del código ∈ sellado de v6.
Solo cambia esa columna: mismas filas, mismo orden (clave de la base) y misma compresión. Comprueba que el resto de
columnas queda idéntico. Actualiza data/base/hechos.parquet, data/base/publica/hechos.parquet y la tabla `hechos` de
data/base/vivienda.duckdb si existe. Sin red; idempotente.
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

CLAVE = "territorio_codigo, nivel, periodo, frecuencia, variable, desagregacion"
NIVELES = ("provincia", "municipio", "distrito", "seccion")


def regla(sell: list[str]) -> str:
    lista = ", ".join(f"'{p}'" for p in sell)
    niv = ", ".join(f"'{n}'" for n in NIVELES)
    return f"(nivel IN ({niv}) AND substr(territorio_codigo, 1, 2) IN ({lista}))"


def marcar_parquet(p: Path, sell: list[str]) -> dict:
    con = duckdb.connect()
    con.execute("SET threads TO 4")
    con.execute(f"CREATE TABLE h AS SELECT * FROM read_parquet('{p}')")
    cols = [c for c, in con.execute("SELECT column_name FROM (DESCRIBE h)").fetchall()]
    otros = ", ".join(c for c in cols if c != "muestra_sellada_v6")
    antes = con.execute(f"SELECT count(*), sum(CASE WHEN muestra_sellada_v6 THEN 1 ELSE 0 END), md5(string_agg(md5(concat_ws('|', {otros})), '' ORDER BY {CLAVE})) FROM h").fetchone()
    con.execute(f"UPDATE h SET muestra_sellada_v6 = {regla(sell)}")
    tmp = p.with_suffix(".tmp.parquet")
    con.execute(f"COPY (SELECT {', '.join(cols)} FROM h ORDER BY {CLAVE}) TO '{tmp}' (FORMAT parquet, COMPRESSION zstd)")
    con2 = duckdb.connect()
    despues = con2.execute(f"SELECT count(*), sum(CASE WHEN muestra_sellada_v6 THEN 1 ELSE 0 END), md5(string_agg(md5(concat_ws('|', {otros})), '' ORDER BY {CLAVE})) FROM read_parquet('{tmp}')").fetchone()
    if antes[0] != despues[0] or antes[2] != despues[2]:
        tmp.unlink()
        raise SystemExit(f"marca_v6: {p} cambiaría algo más que la marca; no se escribe")
    tmp.replace(p)
    return {"fichero": str(p.relative_to(RAIZ)), "filas": int(antes[0]), "marcadas_antes": int(antes[1]), "marcadas_despues": int(despues[1])}


def main() -> int:
    sell = sorted(holdout.provincias_selladas_v6())
    for rel in ("data/base/hechos.parquet", "data/base/publica/hechos.parquet"):
        p = RAIZ / rel
        if p.exists():
            print("marca_v6:", marcar_parquet(p, sell))
    db = RAIZ / "data/base/vivienda.duckdb"
    if db.exists():
        con = duckdb.connect(str(db))
        tablas = {t for t, in con.execute("SELECT table_name FROM information_schema.tables").fetchall()}
        vistas = {t for t, in con.execute("SELECT view_name FROM duckdb_views() WHERE NOT internal").fetchall()}
        if "hechos" in tablas and "hechos" not in vistas:
            con.execute(f"UPDATE hechos SET muestra_sellada_v6 = {regla(sell)}")
            n = con.execute("SELECT sum(CASE WHEN muestra_sellada_v6 THEN 1 ELSE 0 END) FROM hechos").fetchone()[0]
            print(f"marca_v6: data/base/vivienda.duckdb (tabla hechos): {n} filas marcadas")
        else:
            print("marca_v6: vivienda.duckdb sin tabla hechos propia (vista o ausente): nada que cambiar")
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
