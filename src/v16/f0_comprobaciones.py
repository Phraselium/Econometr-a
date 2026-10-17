"""V16-F0.2 · Comprueba que siguen aplicadas las correcciones previas al depósito de V15 (docs/v15/decisiones.md G7 y G8).

1. Filas de las 11 provincias de v6 marcadas `muestra_sellada_v6` en provincia, municipio, distrito y sección (base y capa
   pública).
2. Las 11 bajadas de capa de docs/v15/bajadas_capa.csv están en output/v5/cifras_clave.csv y publicacion/cifras_clave.csv.
3. Los tres metadatos corregidos (obra neta del Catastro 2012-2025, IPC de alquiler 2025=100, permisos de Eurostat).
Escribe output/v16/f0/comprobaciones.json. Sin red; solo lee la base (nunca filas marcadas: cuenta con agregados).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import duckdb
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

SAL = RAIZ / "output" / "v16" / "f0"


def marca_v6() -> dict:
    sell = sorted(holdout.provincias_selladas_v6())
    lista = ", ".join(f"'{p}'" for p in sell)
    res = {}
    for rel in ("data/base/hechos.parquet", "data/base/publica/hechos.parquet"):
        f = RAIZ / rel
        if not f.exists():
            res[rel] = "no existe en este árbol"
            continue
        # recuento agregado: no se leen valores de las filas marcadas
        n_sin = duckdb.sql(f"""SELECT count(*) FROM read_parquet('{f}') WHERE nivel IN ('provincia','municipio','distrito','seccion')
                              AND substr(territorio_codigo,1,2) IN ({lista}) AND NOT muestra_sellada_v6""").fetchone()[0]
        n_con = duckdb.sql(f"SELECT count(*) FROM read_parquet('{f}') WHERE muestra_sellada_v6").fetchone()[0]
        res[rel] = {"marcadas": int(n_con), "sin_marcar_de_v6": int(n_sin), "ok": n_sin == 0 and n_con > 0}
    return res


def bajadas() -> dict:
    b = pd.read_csv(RAIZ / "docs/v15/bajadas_capa.csv", dtype=str)
    out = {}
    for rel in ("output/v5/cifras_clave.csv", "publicacion/cifras_clave.csv"):
        ck = pd.read_csv(RAIZ / rel, dtype=str).set_index("id")
        ok = [i for i, c in zip(b.id, b.capa_nueva) if i in ck.index and ck.at[i, "capa"] == c]
        out[rel] = {"bajadas": len(b), "aplicadas": len(ok), "ok": len(ok) == len(b) == 11}
    return out


def metadatos() -> dict:
    v = pd.read_parquet(RAIZ / "data/base/publica/variables.parquet").set_index("variable")
    o = v.loc["obra_nueva_neta_catastro"]
    return {"obra_nueva_neta_catastro": {"periodo": f"{o.primer_periodo}-{o.ultimo_periodo}", "ok": (o.primer_periodo, o.ultimo_periodo) == ("2012", "2025")},
            "ipc_alquiler_indice": {"unidad": v.at["ipc_alquiler_indice", "unidad"], "ok": v.at["ipc_alquiler_indice", "unidad"] == "índice 2025=100"},
            "permisos": {"unidad": v.at["permisos", "unidad"], "fuente": v.at["permisos", "fuente"],
                         "ok": v.at["permisos", "unidad"] == "índice 2021=100 (SCA)" and v.at["permisos", "fuente"].startswith("Eurostat")}}


def main() -> int:
    r = {"marca_v6": marca_v6(), "bajadas_capa": bajadas(), "metadatos": metadatos()}
    oks = [x["ok"] for g in r.values() for x in g.values() if isinstance(x, dict)]
    r["todo_ok"] = all(oks)
    SAL.mkdir(parents=True, exist_ok=True)
    (SAL / "comprobaciones.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["todo_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
