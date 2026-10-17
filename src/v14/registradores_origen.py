"""V14.3-1 · Origen de cada cifra y tabla que depende de Registradores: datos abiertos (ODbL 1.0) o Anuario ERI.

Salida: docs/v14/registradores_origen.{csv,md} y docs/v14/licencias_tablas.csv. Solo lee; no cambia ninguna cifra.

Productos:
- «ODbL»: conjunto abierto «Compraventas de inmuebles, uso residencial, por provincia» (opendata.registradores.org, Open
  Database License 1.0): data/raw/pdf/registradores_opendata_{anual,compraventas}.csv y las variables construidas con
  ellos (registr_pm2_4tm, registr_num_4tm, registradores_compraventas_anual, ln_pm2_registradores, ln_cv_registradores…).
- «ERI»: Anuario de la Estadística Registral Inmobiliaria (PDF; «no está permitida la reproducción»):
  data/raw/pdf/registradores_eri_anuario.csv, la variable registradores_extranj_pct y las hipotecas tecleadas del anuario
  (REGISTRADORES_HIP en src/v5/ca_run.py).
- «ambos»: usa los dos.

Reglas para las cifras (docs/v14/cifras_terceros.csv, fuente Registradores), en este orden:
1. La tabla MANUAL, si la cifra está en ella (motivo escrito en cada caso).
2. `fuentes` o el enunciado nombran el producto (ERI/Anuario; opendata/datos abiertos).
3. Si no, los scripts del módulo (cifras_terceros._scripts) leen solo uno de los dos.
4. Las «técnicas» (el modelo no usa la serie) heredan el origen del panel; no se retiran nunca.
Tablas: ficheros versionados con columnas, claves o nombre de Registradores (docs/v14/escaneo_terceros.csv) y los ficheros
de origen de las cifras ODbL; el origen sale del nombre de la columna (extranj, _ext_, hipotecas → ERI).
Determinista y sin red.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v14"))
sys.path.insert(0, str(RAIZ))
import cifras_terceros as CT  # noqa: E402

SAL = RAIZ / "docs" / "v14"
ERI_T = re.compile(r"\bERI\b|Anuario|Estad[ií]stica Registral", re.I)
ODB_T = re.compile(r"opendata|open data|datos abiertos", re.I)
ERI_S = re.compile(r"eri_anuario|registradores_extranj_pct|REGISTRADORES_HIP")
ODB_S = re.compile(r"registradores_opendata|registr_pm2|registr_num|registradores_compraventas_anual|ln_pm2_registradores|"
                   r"ln_cv_registradores|prov_compra_anual|pm2_reg")
MANUAL = {
    "CA-CT-ratio-triang-*": ("ambos", "compraventas del CSV de datos abiertos e hipotecas tecleadas del Anuario ERI (REGISTRADORES_HIP, src/v5/ca_run.py)"),
    "A23-P4": ("ODbL", "pesos de importe por CCAA del CSV de datos abiertos (src/v5/a23_run.py); el ERI solo da la prima nueva/usada de A23-P5"),
    "A23-P10": ("ODbL", "precio por m² del CSV de datos abiertos en el factor común de las 4 fuentes (src/v5/a23_run.py)"),
    "B4-*": ("ODbL", "reparto de Shapley de B3, cuyo precio de Registradores es el CSV de datos abiertos (src/v5/b3_data.py)"),
    "K1-*": ("ODbL", "tarea PROV_PRECIO_ANUAL_REGISTRADORES: panel provincial de M0 con el CSV de datos abiertos (src/v6/m0_run.py)"),
}
PANEL_ORIGEN = {   # paneles con series de Registradores (cifras «técnicas»)
    "nacional_q_v8": "ODbL", "cv_prov_q_v8": "ODbL", "prov_compra_anual": "ODbL", "output/v6/M0/paneles": "ODbL",
    "nacional_q_v2": "ambos", "panel_ccaa_a": "ambos", "nacional_q.csv": "ambos",
}
COL_ERI = re.compile(r"extranj|_ext_|_ext$|pct_publicado|cobertura_ccaa|hipotecas", re.I)


def _manual(i: str):
    return MANUAL.get(i) or next((v for k, v in MANUAL.items() if k.endswith("*") and i.startswith(k[:-1])), None)


def _o(e: bool, o: bool) -> str | None:
    return "ambos" if e and o else "ERI" if e else "ODbL" if o else None


def cifras() -> pd.DataFrame:
    d = pd.read_csv(SAL / "cifras_terceros.csv")
    d = d[d.fuente == "Registradores"]
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    filas = []
    for r in d.itertuples():
        row = ck.loc[r.id]
        txt = f"{r.id} {row.indicador} {row.fuentes}"

        class _R:
            id, origen, fuentes = r.id, row.origen, row.fuentes
        scr = CT._scripts(_R)
        codigo = " ".join(p.read_text(encoding="utf-8", errors="ignore") for p in scr)
        if r.dependencia.startswith("técnica"):
            k = next((k for k in PANEL_ORIGEN if k in f"{row.fuentes} {row.origen}"), None)
            origen, regla = PANEL_ORIGEN.get(k, "ambos"), f"técnica: panel {k or 'con series de Registradores'}"
        elif m := _manual(r.id):
            origen, regla = m[0], "1: " + m[1]
        elif o := _o(bool(ERI_T.search(txt)), bool(ODB_T.search(txt))):
            origen, regla = o, "2: fuentes o enunciado"
        elif (o := _o(bool(ERI_S.search(codigo)), bool(ODB_S.search(codigo)))) in ("ERI", "ODbL"):
            origen, regla = o, "3: scripts del módulo"
        else:
            origen, regla = "SIN CLASIFICAR", "revisar a mano"
        filas.append({"tipo": "cifra", "id_o_fichero": r.id, "dependencia": r.dependencia, "origen": origen,
                      "fichero": row.origen.split(":")[0], "evidencia": " ".join(p.relative_to(RAIZ).as_posix() for p in scr), "regla": regla})
    return pd.DataFrame(filas)


def tablas(c: pd.DataFrame) -> pd.DataFrame:
    esc = pd.read_csv(SAL / "escaneo_terceros.csv")
    esc = esc[(esc.ambito == "repositorio") & esc.hallazgos.str.contains("registr", case=False) & (esc.fichero != "proyecto.json")]
    filas = []
    for r in esc.itertuples():
        cols = re.findall(r"(?:columna|clave|variable =|indicador =) ([^;()]+)", r.hallazgos)
        cols = [x.strip() for x in cols if re.search(r"registr|reg_", x, re.I)] or [r.hallazgos[:80]]
        e = any(COL_ERI.search(x) for x in cols)
        o = any(not COL_ERI.search(x) for x in cols)
        if "data/processed/" in r.fichero:
            origen = "ambos" if "extranj_pct" in r.hallazgos else "ODbL"
        else:
            origen = _o(e, o) or "ODbL"
        filas.append({"tipo": "tabla", "id_o_fichero": r.fichero, "dependencia": f"árbol: {r.arbol}; paquete: {r.paquete}",
                      "origen": origen, "fichero": r.fichero, "evidencia": "; ".join(cols)[:300], "regla": "columnas o claves (escaneo_terceros.csv)"})
    ls = subprocess.run(["git", "ls-files", "output"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.split()
    vistos = {f["fichero"] for f in filas}
    for f in ls:   # resultados de modelos con el precio de Registradores (por el nombre del fichero)
        if "PROV_PRECIO_ANUAL_REGISTRADORES" in f and f not in vistos:
            filas.append({"tipo": "tabla", "id_o_fichero": f, "dependencia": "árbol y paquete: sí (resultado propio)", "origen": "ODbL",
                          "fichero": f, "evidencia": "modelo con ln_pm2_registradores (datos abiertos)", "regla": "nombre del fichero"})
            vistos.add(f)
    for f in sorted(set(c[(c.origen == "ODbL") & ~c.dependencia.str.startswith("técnica")].fichero) - vistos):
        filas.append({"tipo": "tabla", "id_o_fichero": f, "dependencia": "árbol y paquete: sí (origen de cifras ODbL)", "origen": "ODbL",
                      "fichero": f, "evidencia": "fichero de origen de cifras con origen ODbL", "regla": "origen de las cifras"})
    return pd.DataFrame(filas)


from src.v14.terceros_1_0 import AVISO_ODBL as AVISO  # noqa: E402

REGISTROS = ("output/v5/cifras_clave.csv", "publicacion/cifras_clave.csv", "data/base/publica/cifras_clave.parquet", "consulta/hallazgos.json")


def licencias(t: pd.DataFrame) -> pd.DataFrame:
    """Ficheros que van al árbol o al paquete con variables o cifras construidas desde los datos abiertos de Registradores."""
    ls = set(subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.split())
    sel = t[t.origen.isin(["ODbL", "ambos"]) & ~t.fichero.str.startswith("data/processed/") & ~t.fichero.str.startswith("data/base/variables")
            & ~t.dependencia.str.contains("árbol: no entra; paquete: no entra")]
    filas = [{"fichero": f, "licencia": "ODbL 1.0 (variables o cifras construidas desde los datos abiertos de Registradores); el resto, CC BY 4.0",
              "aviso": AVISO} for f in sorted(set(sel.fichero) & ls)]
    filas += [{"fichero": f, "licencia": "ODbL 1.0 para las filas con origen ODbL o ambos en docs/v14/registradores_origen.csv; el resto, CC BY 4.0",
               "aviso": AVISO} for f in REGISTROS]
    return pd.DataFrame(filas).drop_duplicates("fichero").sort_values("fichero")


def _md(c: pd.DataFrame, t: pd.DataFrame, lic: pd.DataFrame) -> str:
    L = ["# V14.3 · Origen de las cifras y tablas de Registradores: datos abiertos (ODbL) o Anuario ERI", "",
         "Generado por `python3 src/v14/registradores_origen.py`. Lista completa: [registradores_origen.csv](registradores_origen.csv) "
         "(tipo, id o fichero, dependencia, origen, fichero, evidencia, regla). Licencias por fichero: [licencias_tablas.csv](licencias_tablas.csv).", "",
         "- **ODbL**: conjunto abierto «Compraventas de inmuebles, uso residencial, por provincia», bajo la Open Database License 1.0. "
         "Con terceros_1_0.registradores_odbl = «agregados» sus cifras se publican con el aviso de la ODbL y la serie no se redistribuye.",
         "- **ERI**: Anuario de la Estadística Registral Inmobiliaria (derechos reservados). Con terceros_1_0.registradores_eri = «excluir» "
         "sus cifras (y las «ambos») se retiran de publicacion/, web/ y consulta/; siguen en cifras_clave sin cambios.", "",
         "## Cifras", "", "| Dependencia | ODbL | ERI | ambos |", "|---|---|---|---|"]
    for dep, g in c.groupby("dependencia"):
        n = g.origen.value_counts()
        L.append(f"| {dep} | {n.get('ODbL', 0)} | {n.get('ERI', 0)} | {n.get('ambos', 0)} |")
    L += ["", "Cifras con origen ERI o ambos (las que usan la serie y se retiran con registradores_eri = «excluir»):", "",
          "| id | origen | dependencia | fichero | regla |", "|---|---|---|---|---|"]
    for r in c[c.origen.isin(["ERI", "ambos"]) & ~c.dependencia.str.startswith("técnica")].itertuples():
        L.append(f"| {r.id_o_fichero} | {r.origen} | {r.dependencia} | {r.fichero} | {r.regla} |")
    L += ["", "Cifras con origen ODbL que usan la serie (se publican con el aviso):", "",
          ", ".join(c[(c.origen == "ODbL") & ~c.dependencia.str.startswith("técnica")].id_o_fichero), "",
          "## Tablas y ficheros", "", "| Fichero | Origen | Árbol / paquete | Columnas o claves |", "|---|---|---|---|"]
    for r in t.itertuples():
        L.append(f"| {r.fichero} | {r.origen} | {r.dependencia} | {str(r.evidencia).replace('|', '/')[:120]} |")
    L += ["", f"## Licencia ODbL en el árbol y el paquete ({len(lic)} ficheros)", "",
          "Cada fichero de [licencias_tablas.csv](licencias_tablas.csv) que contiene variables o cifras construidas desde los datos abiertos "
          "se publica, en esa parte, bajo la ODbL 1.0 (4.4, «share alike»), con este aviso (4.2 y 4.3):", "", f"> {AVISO}", ""]
    return "\n".join(L) + "\n"


INI, FIN = "<!-- licencias V14.3: inicio (src/v14/registradores_origen.py) -->", "<!-- licencias V14.3: fin -->"


def seccion_diccionario() -> str:
    """Licencia por tabla para el diccionario de la base (docs/v10/diccionario_base.md); src/v10/base.py la añade al regenerarlo."""
    lic = pd.read_csv(SAL / "licencias_tablas.csv")
    L = [INI, "", "## Licencias por tabla (V14.3)", "",
         "- Las tablas de la capa pública (data/base/publica: hechos, variables, territorios, regulacion_zonas) no contienen series ni "
         "variables de Registradores, Notariado o AEAT (las variables `aeat_*` se quitan según proyecto.json → terceros_1_0). "
         "Su licencia es la de la columna `licencia` de variables.parquet para cada variable y CC BY 4.0 para lo propio.",
         "- `cifras_clave` (publica/cifras_clave.parquet y publicacion/cifras_clave.csv): las filas con origen «ODbL» o «ambos» en "
         "docs/v14/registradores_origen.csv se publican bajo la Open Database License 1.0; el resto, CC BY 4.0.",
         "- Las variables de Registradores de la base completa (registr_pm2_4tm, registr_num_4tm, registradores_compraventas_anual: datos "
         "abiertos, ODbL 1.0; registradores_extranj_pct: Anuario ERI, no redistribuible) no están en la capa pública ni en el depósito.",
         f"- Ficheros de output/ y del registro con partes bajo ODbL 1.0: {len(lic)} (lista en docs/v14/licencias_tablas.csv).", "",
         f"Aviso de atribución: {AVISO}", "", FIN]
    return "\n".join(L) + "\n"


def escribir_diccionario() -> None:
    p = RAIZ / "docs" / "v10" / "diccionario_base.md"
    t = p.read_text(encoding="utf-8")
    if INI in t:
        t = t[:t.index(INI)] + t[t.index(FIN) + len(FIN) + 1:]
    p.write_text(t.rstrip("\n") + "\n\n" + seccion_diccionario(), encoding="utf-8")


def main() -> int:
    c = cifras()
    if (c.origen == "SIN CLASIFICAR").any():
        raise SystemExit("registradores_origen: cifras sin clasificar: " + ", ".join(c[c.origen == "SIN CLASIFICAR"].id_o_fichero))
    t = tablas(c)
    lic = licencias(t)
    pd.concat([c, t]).to_csv(SAL / "registradores_origen.csv", index=False)
    lic.to_csv(SAL / "licencias_tablas.csv", index=False)
    (SAL / "registradores_origen.md").write_text(_md(c, t, lic), encoding="utf-8")
    escribir_diccionario()
    print("registradores_origen:", c.groupby(["origen"]).size().to_dict(), "· tablas", t.origen.value_counts().to_dict(), "· licencias ODbL", len(lic))
    return 0


if __name__ == "__main__":
    sys.exit(main())
