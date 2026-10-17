"""V16-F4.4 · Sellado de la validación V16 ANTES de estimar (docs/v16/preregistro_v16.md, sección 5). Sin red; SEED=20261010.

1. Reúne, en formato largo, los datos que usarán las preguntas Q1-Q10 de V16:
   - todos los parquets normalizados de data/processed/v16/<familia>.parquet (y los *_terceros.parquet si están en disco);
   - de data/base/hechos.parquet (sin la muestra v6), las variables de la base que usan las preguntas (VARIABLES_BASE).
2. Escribe docs/v16/sellado_v16.json: fecha de corte, bloque espacial (holdout: celdas, municipios y distritos V16), último periodo
   visto por variable|nivel|frecuencia, huellas sha256 de las fuentes y recuentos. Define el bloque temporal: todo periodo posterior
   queda sellado.
3. Llama a holdout.sellar_v16 por conjunto: la parte sellada (bloque espacial V16 + V15 + v6, y temporal) va a la carpeta sellada
   de V16 dentro de src/holdout.py, y SOLO el entrenamiento a data/processed/v16/entrenamiento/<conjunto>.parquet, que es lo único
   que leerán los módulos de la fase 6.
Se niega a ejecutarse dos veces (si existe el manifiesto) salvo --rehacer, que exige que la etiqueta prereg-v16 aún no esté publicada.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import duckdb
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

PROC = RAIZ / "data" / "processed" / "v16"
SAL = PROC / "entrenamiento"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
PADRON = RAIZ / "data" / "raw" / "v9" / "ine_padron_nacionalidad" / "padron_nacionalidad_2003_2022.csv.gz"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "metodo_dato", "redistribuible"]
FAMILIAS = ["alquiler_turismo", "demanda_internacional", "oferta_suelo", "renta_parque", "tension_social"]
# variables de la base que usan Q1-Q10 (patrones LIKE; docs/v16/preregistro_v16.md, sección 2)
VARIABLES_BASE = {
    "base_alquiler": ["serpavi_%", "ipva_%", "incasol_%", "ipc_alquiler%", "emal_%", "fianzas_%", "gva_fianzas%"],
    "base_precio": ["p_tasado%", "valor_tasado%", "ipv%", "compraventas%", "hip_%", "visados", "iniciadas", "terminadas%"],
    "base_macro": ["tipo_hip%", "euribor%", "tipo_bce", "tipo_dfr", "tipo_mro", "renta_hog%", "ocupados%", "ipc_general%",
                   "inflacion_ipc%", "credito_nuevo%", "monitor_%", "afiliacion%", "paro%"],
    "base_regulacion": ["zt_%"],
    "base_turismo": ["ine_vut_%", "idescat_%", "vut_registro_%", "pernoctaciones%"],
    "base_poblacion": ["pob_%", "hogares_%", "padron_%", "extranjeros%", "v12_%"],
    "base_oferta": ["obra_nueva_neta_catastro", "catastro_%", "adrh_%"],
}


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _publicada() -> bool:
    spec = importlib.util.spec_from_file_location("v16_etiquetas", RAIZ / "src" / "v16" / "etiquetas.py")
    et = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(et)
    return et.prereg_v16_publicada(RAIZ)[0]


def conjuntos() -> dict[str, pd.DataFrame]:
    out = {}
    for fam in FAMILIAS:
        for sufijo in ("", "_terceros"):
            f = PROC / f"{fam}{sufijo}.parquet"
            if f.exists():
                d = pd.read_parquet(f)
                if "variable" not in d:          # tablas de correspondencia, no datos
                    continue
                d = d[~d.get("muestra_sellada_v6", pd.Series(False, index=d.index)).fillna(False).astype(bool)]
                out[f"{fam}{sufijo}"] = d[[c for c in COLS if c in d]]
    con = duckdb.connect()
    for nombre, pats in VARIABLES_BASE.items():
        cond = " OR ".join(f"variable LIKE '{v}'" for v in pats)
        out[nombre] = con.execute(f"SELECT {', '.join(COLS)} FROM read_parquet('{HECHOS}') "
                                  f"WHERE NOT coalesce(muestra_sellada_v6, false) AND ({cond})").df()
    p = pd.read_csv(PADRON, dtype={"cod_municipio": str, "anio": str, "nacionalidad": str})
    p = p.groupby(["cod_municipio", "anio", "nacionalidad"], as_index=False).poblacion.sum()
    out["padron_nacionalidad"] = pd.DataFrame({
        "territorio_codigo": p.cod_municipio.str.zfill(5), "nivel": "municipio", "periodo": p.anio, "frecuencia": "A",
        "variable": "padron_municipal_nacionalidad", "desagregacion": "nacionalidad=" + p.nacionalidad, "valor": p.poblacion,
        "unidad": "personas", "fuente": "INE, padrón continuo por nacionalidad (data/raw/v9)", "edicion": "", "metodo_dato": "observado",
        "redistribuible": True})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rehacer", action="store_true")
    a = ap.parse_args()
    if holdout.MANIFIESTO_V16.exists() and not a.rehacer:
        print("f4_sellado: ya sellado (docs/v16/sellado_v16.json); no se repite.")
        return 0
    if _publicada():
        raise SystemExit("f4_sellado: prereg-v16 ya está en el remoto; el sellado no se rehace después de fijar el pre-registro.")
    ext = conjuntos()
    todo = pd.concat([d[["variable", "nivel", "frecuencia", "periodo"]] for d in ext.values()], ignore_index=True)
    clave = todo.variable.astype(str) + "|" + todo.nivel.astype(str) + "|" + todo.frecuencia.astype(str)
    fuentes = [HECHOS, PADRON] + [PROC / f"{n}.parquet" for n in ext if (PROC / f"{n}.parquet").exists()]
    man = {"fecha_corte": dt.date.today().isoformat(), "semilla": [holdout.SEED, 16], "fraccion_espacial": holdout.FRACCION_V16,
           "celda_grados": holdout.CELDA_V15, "celdas_selladas": holdout.celdas_selladas_v16(),
           "n_municipios_sellados": len(holdout.municipios_sellados_v16()), "n_distritos_sellados": len(holdout.distritos_sellados_v16()),
           "fuentes_sha256": {str(f.relative_to(RAIZ)): _sha(f) for f in fuentes},
           "ultimo_periodo_visto": dict(sorted(todo.assign(k=clave).groupby("k").periodo.max().astype(str).items())), "conjuntos": {}}
    holdout.MANIFIESTO_V16.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    SAL.mkdir(parents=True, exist_ok=True)
    for n, d in ext.items():
        tr = holdout.sellar_v16(d.reset_index(drop=True), n)
        tr.to_parquet(SAL / f"{n}.parquet", index=False)
        man["conjuntos"][n] = {"filas": len(d), "filas_entrenamiento": len(tr), "filas_selladas": len(d) - len(tr),
                               "variables": int(d.variable.nunique())}
        print(f"f4_sellado: {n}: {len(tr)} entrenamiento, {len(d) - len(tr)} selladas")
    holdout.MANIFIESTO_V16.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
