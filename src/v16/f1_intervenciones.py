"""V16-F1 · Base de intervenciones: calendario fechado y por territorio de cada medida, con su fuente normativa (docs/v16/plan.md, fase 1).

Une, sin red y de forma determinista:
- data/raw/v16/intervenciones/intervenciones.csv (medidas nuevas de V16: ITP/AJD, topes, bono alquiler joven, avales ICO, planes, desahucios,
  golden visa, IBI, vivienda turística, incentivos fiscales, vivienda pública anunciada y entregada);
- data/raw/v9/regulacion/zonas_tensionadas_v9.csv (318 municipios declarados, ya verificados en V9) y, si existe,
  data/raw/v16/intervenciones/zonas_tensionadas_v16_nuevas.csv (declaraciones posteriores), como filas `zona_tensionada` municipales.
Valida: instrumento y ámbito permitidos, fechas ISO, código INE existente en data/base/publica/territorios.parquet para su nivel (cruces SOLO por
código INE), fuente normativa y URL no vacías, y que no haya filas duplicadas.
Escribe output/v16/f1/intervenciones.csv, output/v16/f1/intervenciones_resumen.md y output/v16/f1/intervenciones_resultado.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ENT = RAIZ / "data" / "raw" / "v16" / "intervenciones"
SAL = RAIZ / "output" / "v16" / "f1"
COLUMNAS = ["id", "instrumento", "medida", "ambito", "cod_ine", "territorio", "fecha_publicacion", "fecha_efecto", "fecha_fin",
            "parametro", "valor", "unidad", "fuente_normativa", "url", "verificacion", "notas"]
INSTRUMENTOS = {"zona_tensionada", "tope_actualizacion_rentas", "bono_alquiler_joven", "avales_ico", "plan_estatal", "itp", "ajd",
                "ibi_recargo_vacias", "vut_moratoria", "vut_regulacion", "golden_visa", "suspension_desahucios",
                "incentivo_fiscal_alquiler", "vivienda_publica_anuncio", "vivienda_publica_entrega"}
NIVEL = {"estatal": "nacional", "ccaa": "ccaa", "provincia": "provincia", "municipio": "municipio", "zona": "municipio"}
FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _zonas() -> pd.DataFrame:
    partes = [RAIZ / "data/raw/v9/regulacion/zonas_tensionadas_v9.csv", ENT / "zonas_tensionadas_v16_nuevas.csv"]
    z = pd.concat([pd.read_csv(p, dtype=str).fillna("") for p in partes if p.exists()], ignore_index=True)
    # un municipio puede tener varias zonas parciales con la misma fecha (Llanes, 2026): sufijo por orden de aparición
    n = z.groupby(["cod_ine_municipio", "fecha_efecto"]).cumcount()
    out = pd.DataFrame({
        "id": "ZT-" + z.cod_ine_municipio + "-" + z.fecha_efecto + n.map(lambda k: "" if k == 0 else f"-{k + 1}"),
        "instrumento": "zona_tensionada",
        "medida": "declaración de zona de mercado residencial tensionado (Ley 12/2023, art. 18): " + z.alcance,
        "ambito": "municipio", "cod_ine": z.cod_ine_municipio, "territorio": z.municipio_resolucion,
        "fecha_publicacion": z.fecha_publicacion_boe, "fecha_efecto": z.fecha_efecto, "fecha_fin": z.fecha_fin_prevista,
        "parametro": "", "valor": "", "unidad": "",
        "fuente_normativa": z.resolucion_boe, "url": z.url_resolucion,
        "verificacion": "VERIFICADA (texto de la disposición; V9)",
        "notas": "fecha_fin = fin previsto de la declaración (tres años, prorrogable); declaración autonómica: " + z.declaracion_autonomica.str[:160],
    })
    return out


def main() -> int:
    f = ENT / "intervenciones.csv"
    if not f.exists():
        print("f1_intervenciones: falta data/raw/v16/intervenciones/intervenciones.csv")
        return 1
    nuevas = pd.read_csv(f, dtype=str).fillna("")
    errores = [f"columnas {list(nuevas.columns)} != {COLUMNAS}"] if list(nuevas.columns) != COLUMNAS else []
    if errores:
        print("ERROR", errores[0])
        return 1
    base = pd.concat([nuevas[nuevas.instrumento != "zona_tensionada"], _zonas(), nuevas[nuevas.instrumento == "zona_tensionada"]],
                     ignore_index=True)
    ter = pd.read_parquet(RAIZ / "data/base/publica/territorios.parquet", columns=["territorio_codigo", "nivel"])
    validos = {(n, c) for c, n in zip(ter.territorio_codigo, ter.nivel)}
    for i, r in base.iterrows():
        donde = f"fila {r.id or i}"
        if r.instrumento not in INSTRUMENTOS:
            errores.append(f"{donde}: instrumento «{r.instrumento}»")
        if r.ambito not in NIVEL:
            errores.append(f"{donde}: ámbito «{r.ambito}»")
        elif (NIVEL[r.ambito], r.cod_ine) not in validos:
            errores.append(f"{donde}: código INE {r.cod_ine} no existe como {NIVEL[r.ambito]}")
        for c in ("fecha_publicacion", "fecha_efecto", "fecha_fin"):
            if r[c] and not FECHA.match(r[c]):
                errores.append(f"{donde}: {c} «{r[c]}» no es AAAA-MM-DD")
        if not r.fecha_efecto and not r.fecha_publicacion:
            errores.append(f"{donde}: sin fecha")
        if not r.fuente_normativa or not r.url:
            errores.append(f"{donde}: sin fuente normativa o URL")
    dup = base[base.duplicated(["id"], keep=False)]
    if len(dup):
        errores.append(f"ids duplicados: {sorted(set(dup.id))[:10]}")
    for e in errores[:50]:
        print("ERROR", e)
    base = base.sort_values(["instrumento", "ambito", "cod_ine", "fecha_efecto", "id"]).reset_index(drop=True)
    SAL.mkdir(parents=True, exist_ok=True)
    base.to_csv(SAL / "intervenciones.csv", index=False, lineterminator="\n")
    ver = base.verificacion.str.extract(r"^(VERIFICADA|SECUNDARIA|NO VERIFICADA)")[0].fillna("otra")
    tab = (base.assign(v=ver).groupby(["instrumento", "v"]).size().unstack(fill_value=0)
           .reindex(columns=["VERIFICADA", "SECUNDARIA", "NO VERIFICADA", "otra"], fill_value=0))
    amb = base.groupby("instrumento").ambito.agg(lambda s: ", ".join(sorted(set(s))))
    fechas = base.assign(f=base.fecha_efecto.where(base.fecha_efecto != "", base.fecha_publicacion)).groupby("instrumento").f.agg(["min", "max"])
    L = ["# V16 · Base de intervenciones (resumen)", "",
         "Generado por `python3 src/v16/f1_intervenciones.py`. Calendario normativo descriptivo: no evalúa ninguna medida. "
         "Una fila es una medida × territorio × tramo temporal. Cruces solo por código INE.", "",
         "| Instrumento | Filas | Verificadas | Secundarias | No verificadas | Ámbitos | Desde | Hasta |", "|---|---|---|---|---|---|---|---|"]
    for ins, r in tab.iterrows():
        L.append(f"| {ins} | {int(r.sum())} | {r['VERIFICADA']} | {r['SECUNDARIA']} | {r['NO VERIFICADA']} | {amb[ins]} | "
                 f"{fechas.at[ins, 'min']} | {fechas.at[ins, 'max']} |")
    L += ["", f"Total: {len(base)} filas. Errores de validación: {len(errores)}.", ""]
    (SAL / "intervenciones_resumen.md").write_text("\n".join(L), encoding="utf-8")
    res = {"rama": "v16-f1-intervenciones", "pregunta": "Calendario fechado y por territorio de las medidas de vivienda",
           "capa": "C1", "datos": ["data/raw/v16/intervenciones/intervenciones.csv", "data/raw/v9/regulacion/zonas_tensionadas_v9.csv"],
           "N": int(len(base)), "metodo": "base normativa (BOE y diarios oficiales)", "estimacion": None, "ic95": None,
           "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"errores_validacion": len(errores), "por_verificacion": {k: int(v) for k, v in ver.value_counts().items()}},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Capa C1 solo para las filas VERIFICADAS con el texto oficial; las SECUNDARIAS y NO VERIFICADAS son C4 hasta verificarse."}
    (SAL / "intervenciones_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"f1_intervenciones: {len(base)} filas, {len(errores)} errores")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
