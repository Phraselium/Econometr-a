"""V15-F3.3 · Sellado de la validación V15 ANTES de estimar (docs/v15/preregistro_v15.md, sección 2). Sin red; SEED=20261010.

1. Extrae de data/base/hechos.parquet (sin la muestra sellada de v6) y del padrón municipal por nacionalidad (data/raw/v9) las
   variables de cada pregunta pre-registrada, en formato largo.
2. Escribe docs/v15/sellado_v15.json: fecha de corte, último periodo visto por variable|nivel|frecuencia, recuentos y huellas
   (sha256) de las fuentes. Es la definición del bloque temporal: todo periodo posterior queda sellado.
3. Llama a holdout.sellar_v15 por pregunta: la parte sellada (bloque espacial + temporal) va a data/sealed/v15_<pregunta>.parquet
   y SOLO la de entrenamiento a data/processed/v15/<pregunta>.parquet, que es lo único que leerán los módulos de la fase 4.
Se niega a ejecutarse dos veces (si existe el manifiesto) salvo --rehacer, que exige que la puerta siga cerrada.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import duckdb
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

SAL = RAIZ / "data" / "processed" / "v15"
HECHOS = RAIZ / "data" / "base" / "hechos.parquet"
PADRON = RAIZ / "data" / "raw" / "v9" / "ine_padron_nacionalidad" / "padron_nacionalidad_2003_2022.csv.gz"
COLS = ["territorio_codigo", "nivel", "periodo", "frecuencia", "variable", "desagregacion", "valor", "unidad", "fuente", "edicion",
        "metodo_dato", "redistribuible"]

# variables por pregunta (prefijos con %; docs/v15/preregistro_v15.md)
PREGUNTAS = {
    "p6_zonas_tensionadas": ["incasol_renta_media", "incasol_contratos", "zt_vigente", "zt_declarada"],
    "p5_turismo_seccion": ["serpavi_alquiler_m2_mediana", "serpavi_alquiler_mes_mediana", "ine_vut_%", "ipva_indice", "ipva_tam_indice"],
    "p4_inmigracion": ["serpavi_alquiler_m2_mediana", "pob_censo_anual", "pob_total", "ipc_alquiler_indice", "ipc_alquiler_yoy"],
    "p9_prediccion": ["p_tasado", "ipv", "compraventas", "compraventas_sa", "hip_n", "hip_importe", "visados", "iniciadas", "tipo_hip",
                      "tipo_hip_bde", "euribor", "ocupados", "ocupados_sa", "renta_hog", "renta_hog_real", "ipc_general", "pob_total",
                      "credito_nuevo", "ipc_alquiler", "monitor_%"],
    "p2_fundamentales": ["valor_tasado", "valor_tasado_ccaa", "ipc_alquiler_indice", "ipc_alquiler", "ipv", "tipo_hip_real%",
                         "tipo_hip_bde", "renta_hog_real", "inflacion_ipc_yoy"],
    "p7_demografia_obra": ["v12_%", "obra_nueva_neta_catastro", "catastro_unidades_urbanas_residenciales", "terminadas%", "pob_censo_anual",
                           "hogares_ecp", "serpavi_alquiler_m2_mediana", "ipc_alquiler_indice"],
    "p10_espacial": ["serpavi_alquiler_m2_mediana", "serpavi_n_contratos_recuento"],
    "p5_cv_cataluna": ["idescat_hut_%", "idescat_apartamentos_%", "incasol_renta_media", "incasol_contratos", "vut_registro_gva_reconstruido",
                       "vut_registro_gva", "serpavi_alquiler_m2_mediana"],
}
NIVELES = {"p4_inmigracion": ("municipio", "provincia"), "p10_espacial": ("municipio",), "p5_turismo_seccion": ("seccion", "distrito"),
           "p6_zonas_tensionadas": ("municipio",)}


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def extraer(pregunta: str) -> pd.DataFrame:
    cond = " OR ".join(f"variable LIKE '{v}'" for v in PREGUNTAS[pregunta])
    niv = NIVELES.get(pregunta)
    w = f" AND nivel IN ({', '.join(repr(n) for n in niv)})" if niv else ""
    con = duckdb.connect()
    d = con.execute(f"SELECT {', '.join(COLS)} FROM read_parquet('{HECHOS}') WHERE NOT coalesce(muestra_sellada_v6, false) AND ({cond}){w}").df()
    if pregunta == "p4_inmigracion":
        p = pd.read_csv(PADRON, dtype={"cod_municipio": str, "anio": str, "nacionalidad": str})
        p = p.groupby(["cod_municipio", "anio", "nacionalidad"], as_index=False).poblacion.sum()
        d = pd.concat([d, pd.DataFrame({"territorio_codigo": p.cod_municipio.str.zfill(5), "nivel": "municipio", "periodo": p.anio,
                                        "frecuencia": "A", "variable": "padron_municipal_nacionalidad", "desagregacion": "nacionalidad=" + p.nacionalidad,
                                        "valor": p.poblacion, "unidad": "personas", "fuente": "INE, padrón continuo por nacionalidad (data/raw/v9)",
                                        "edicion": "", "metodo_dato": "observado", "redistribuible": True})], ignore_index=True)
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rehacer", action="store_true")
    a = ap.parse_args()
    if holdout.MANIFIESTO_V15.exists() and not a.rehacer:
        print("f3_sellado: ya sellado (docs/v15/sellado_v15.json); no se repite.")
        return 0
    sys.path.insert(0, str(RAIZ / "src" / "v15"))
    from puerta import abierta
    if abierta()[0]:
        raise SystemExit("f3_sellado: la puerta V15 ya está abierta; el sellado no se rehace después del depósito.")
    ext = {q: extraer(q) for q in PREGUNTAS}
    todo = pd.concat(ext.values(), ignore_index=True)
    clave = todo.variable.astype(str) + "|" + todo.nivel.astype(str) + "|" + todo.frecuencia.astype(str)
    man = {"fecha_corte": dt.date.today().isoformat(), "semilla": holdout.SEED_V15, "fraccion_espacial": holdout.FRACCION_V15,
           "celda_grados": holdout.CELDA_V15, "celdas_selladas": holdout.celdas_selladas_v15(),
           "n_municipios_sellados": len(holdout.municipios_sellados_v15()), "n_distritos_sellados": len(holdout.distritos_sellados_v15()),
           "fuentes_sha256": {str(HECHOS.relative_to(RAIZ)): _sha(HECHOS), str(PADRON.relative_to(RAIZ)): _sha(PADRON)},
           "ultimo_periodo_visto": dict(sorted(todo.assign(k=clave).groupby("k").periodo.max().astype(str).items())), "preguntas": {}}
    holdout.MANIFIESTO_V15.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    SAL.mkdir(parents=True, exist_ok=True)
    for q, d in ext.items():
        tr = holdout.sellar_v15(d, q)
        tr.to_parquet(SAL / f"{q}.parquet", index=False)
        man["preguntas"][q] = {"filas": len(d), "filas_entrenamiento": len(tr), "filas_selladas": len(d) - len(tr),
                               "variables": sorted(d.variable.unique().tolist())}
        print(f"f3_sellado: {q}: {len(tr)} entrenamiento, {len(d) - len(tr)} selladas")
    holdout.MANIFIESTO_V15.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
