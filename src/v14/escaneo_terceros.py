"""V14.2-B1 · Escaneo de series de Notariado, Registradores o AEAT en todos los formatos de datos → docs/v14/escaneo_terceros.{md,csv}.

Uso: python3 src/v14/escaneo_terceros.py [--arbol DIR] [--paquete DIR]
- repositorio: ficheros versionados (.csv, .gz, .parquet, .xlsx, .zip, .json, .duckdb), salvo data/sealed, que no se lee.
  Para cada hallazgo indica si el fichero entra en el árbol público y en el paquete, y si sale redactado.
- árbol y paquete: todos sus ficheros de esos formatos, tal como quedaron (lo que se publicaría).
Solo lee; no escribe nada fuera de docs/v14/escaneo_terceros.* y no cambia ninguna cifra.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v14 import terceros as T  # noqa: E402

EXT = (".csv", ".gz", ".parquet", ".xlsx", ".zip", ".json", ".duckdb")
NOMBRE = re.compile(r"notariado|registradores|(?:^|_)registr(?:_|$)|aeat|cgpj|(?:^|_)cgn(?:_|$)", re.I)
# hallazgos revisados a mano: nombran la fuente, pero son resultados propios o metadatos, no la serie (decisiones.md, E3-bis)
REVISADOS = {
    "data/base/publica/cifras_clave.parquet": "registro de cifras: enunciados que nombran la fuente; sin series",
    "data/base/publica/variables.parquet": "catálogo de variables (metadatos); la serie de la AEAT se quita de hechos.parquet salvo «redistribuir»",
    "output/v12/b5/resultado.json": "aeat_cv_cuota_pct: agregado propio (cuota de la Comunitat Valenciana 2016-2024)",
    "output/v12/f0/resultado.json": "metadatos de la validación (municipios, ejercicios, errores relativos)",
    "output/v4/M4/hechos.json": "cifras nacionales publicadas por la fuente, citadas (un valor por año), y cálculos propios",
    "output/v4/M4/resultado.json": "ídem, y diagnósticos propios (correlación, diferencia media, cobertura)",
    "output/v4/M7/hechos.json": "variaciones acumuladas y anuales calculadas: resultado propio",
    "output/v5/A23/calculos.json": "variaciones y factores calculados: resultado propio",
    "output/v5/A23/resultado.json": "ídem",
    "output/v6_1/K4B/calculos.json": "ídem",
    "output/v5/B3/resultado.json": "R² de Shapley: resultado propio",
    "output/v5/B3/tablas/resumen_interno.json": "contraste de hipótesis: resultado propio",
    "output/v5/B3/tablas/shapley_R2.csv": "cuota de R² (REVISADAS_SIN_SERIES)",
    "output/v5/B3/_smoke/tablas/shapley_R2.csv": "ídem (ejecución de prueba)",
    "output/v6/M0/cobertura_train.json": "recuento de cobertura (n, unidades, años); sin valores",
    "output/v6/M3B/resultado.json": "métricas de predicción y SHAP de un modelo con el precio de Registradores: resultado propio",
    "output/v6/M3B/tablas/interpretacion_resumen.json": "ídem",
    "output/v6/M3B/tablas/resumen_por_setting.json": "ídem",
    "output/v8/F1/resultado.json": "correlación de tasas: resultado propio",
    "revision_externa/hoja_revision.xlsx": "enunciados publicados que nombran la fuente; sin series",
    "proyecto.json": "configuración (campo terceros_1_0)",
    # K16 (2026-10-23): hallazgos posteriores a la revisión de la 1.0, clasificados con las reglas de terceros_1_0
    "docs/v14/escenarios_resultado.json": "metadatos: valores de la política terceros_1_0 por escenario; sin series",
    "docs/v16/sellado_v16.json": "metadatos del sellado: último periodo visto por variable (fechas); sin valores",
    "docs/v18/sellado_v18.json": "metadatos del sellado: topes de fecha por variable; sin valores",
    "output/v15/auditoria/precios_compra/resultado.json": "diagnósticos propios de calidad (recuentos de pares, diferencias relativas medias, número de descargas); sin series",
    "output/v16/f2_hechos/control.json": "metadatos: grupo de independencia de cada fuente; sin valores",
    "output/v16/potencia/resultado.json": "recuentos de unidades tras exclusiones; sin valores de la fuente",
    "output/v16/replica/v10_a/resultado.json": "variaciones porcentuales calculadas (agregados propios; Notariado con atribución, Registradores con el aviso de la ODbL)",
    "revision_externa/2_0/hoja_revision.xlsx": "enunciados publicados que nombran la fuente y cifras propias; sin series",
    "output/v12/b5/aeat_cv_2013_2015.csv": "AEAT (terceros_1_0.aeat = redistribuir; atribución AVISO_AEAT)",
    "output/v12/b5/aeat_cv_declarantes_inmuebles.csv": "AEAT (redistribuir, con atribución)",
    "output/v15/auditoria/renta_microdatos/aeat_comprobacion_unidades_2016_2024.csv": "AEAT (redistribuir, con atribución)",
    "output/v15/auditoria/renta_microdatos/aeat_estructura_por_ejercicio.csv": "AEAT (redistribuir, con atribución)",
    "output/v15/auditoria/renta_microdatos/aeat_hipotesis_recuentos_2015.csv": "AEAT (redistribuir, con atribución)",
    "output/v15/auditoria/renta_microdatos/aeat_razones_entre_ejercicios.csv": "AEAT (redistribuir, con atribución)",
    "output/v15/auditoria/renta_microdatos/resultado.json": "diagnósticos propios sobre la AEAT (redistribuir, con atribución)",
    "output/f6/fig_notariado_provincia.png": "figura de la serie, citando la fuente (agregado publicado); queda en output/, no en publicacion/",
}
REVISADOS_PATRON = (
    (re.compile(r"^output/v6(_1)?/(M3B|M4|K1)/.*PROV_PRECIO_ANUAL_REGISTRADORES"),
     "resultados de un modelo con el precio de Registradores (métricas, SHAP, ALE, PDP, VIF, modelo ajustado): resultado propio, sin la serie"),
)


def _revisado(f: str) -> str | None:
    return REVISADOS.get(f) or next((m for pat, m in REVISADOS_PATRON if pat.search(f)), None)


FUENTE_TEXTO = (("aeat", re.compile(r"aeat", re.I)),
                ("notariado", re.compile(r"notariado|\bcgn\b", re.I)),
                ("registradores", re.compile(r"registr", re.I)),
                ("cgpj", re.compile(r"cgpj", re.I)))


def _redistribuido(f: str, hallazgos: str = "") -> str | None:
    """K16: un hallazgo cuyas fuentes (por la ruta y los hallazgos) se redistribuyen todas con terceros_1_0 no queda pendiente."""
    from src.v14 import terceros_1_0 as T10
    fuentes = {n for n, pat in FUENTE_TEXTO if pat.search(f) or pat.search(hallazgos)}
    if fuentes and all(T10.redistribuye(x) for x in fuentes):
        return "redistribuido: " + ", ".join(sorted(fuentes)) + " (terceros_1_0 = redistribuir; atribución en LICENSE, punto 5)"
    return None


def _ficheros_repo() -> list[str]:
    r = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True)
    return sorted(f for f in r.stdout.split("\0") if f.endswith(EXT) and not f.startswith("data/sealed") and (RAIZ / f).is_file())


def _ficheros_dir(d: Path) -> list[str]:
    return sorted(p.relative_to(d).as_posix() for p in d.rglob("*")
                  if p.is_file() and p.name.endswith(EXT) and ".git" not in p.relative_to(d).parts)


def _estado(f: str, en: bool, hallazgos: str = "") -> str:
    if not en:
        return "no entra"
    if f == "data/base/publica/hechos.parquet":
        return "filtrado (terceros_1_0)" if T10_excluye() else "redistribuido: aeat (terceros_1_0 = redistribuir; atribución en LICENSE, punto 5)"
    a, _ = T.accion(f, RAIZ / f)
    if a in ("redactar", "vaciar"):
        return {"redactar": "redactado", "vaciar": "vaciado"}[a]
    return "revisado: " + _revisado(f) if _revisado(f) else (_redistribuido(f, hallazgos) or "PENDIENTE")


def escanear_repo() -> list[dict]:
    """Ficheros versionados con columnas, claves u hojas de la fuente (escanear) o con su nombre en la ruta."""
    from src.v13 import paquete_zenodo as PZ
    from src.v14 import arbol_publico as AP
    inc_paq = set(PZ.seleccionar()[0])
    todos = subprocess.run(["git", "ls-files", "-z"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.split("\0")
    por_nombre = {f for f in todos if f.startswith("output/") and NOMBRE.search(Path(f).name) and (RAIZ / f).is_file()}
    filas = []
    for f in sorted(set(_ficheros_repo()) | por_nombre | set(T.COLUMNAS_SERIE)):
        hits = T.escanear(RAIZ / f) if f.endswith(EXT) else []
        if f in por_nombre:
            hits = ["nombre del fichero"] + hits
        if f in T.COLUMNAS_SERIE:
            hits += [f"columna {c} (serie de {v}; escaneo por valores)" for c, v in T.COLUMNAS_SERIE[f].items()]
        if not hits:
            continue
        filas.append({"ambito": "repositorio", "fichero": f, "hallazgos": "; ".join(hits),
                      "arbol": _estado(f, not AP.excluir(f), "; ".join(hits)), "paquete": _estado(f, f in inc_paq, "; ".join(hits))})
    return filas


def _estado_dir(rel: str, p: Path, hallazgos: str = "") -> str:
    """Estado de un fichero ya publicado (árbol o paquete): vaciado, revisado o PENDIENTE."""
    if T.es_tabla(p) and len(T.cabecera(p)) and sum(1 for _ in T._abrir(p)) <= 1:
        return "vaciado (solo la cabecera)"
    if p.suffix == ".md" and p.read_text(encoding="utf-8", errors="ignore").startswith(T.NOTA_VACIADO.split("\n")[0]):
        return "vaciado (nota)"
    if (RAIZ / rel).is_file() and T.accion(rel, RAIZ / rel)[0] == "vaciar":
        return "vaciado (nota)" if p.read_text(encoding="utf-8", errors="ignore").startswith(T.NOTA_VACIADO.split("\n")[0]) else "PENDIENTE"
    if (RAIZ / rel).is_file() and T.accion(rel, RAIZ / rel)[0] == "redactar":
        quitar = T.accion(rel, RAIZ / rel)[1]
        return "redactado (verificado)" if not set(quitar) & set(T.cabecera(p)) else "PENDIENTE"
    return "revisado: " + _revisado(rel) if _revisado(rel) else (_redistribuido(rel, hallazgos) or "PENDIENTE")


def T10_excluye() -> bool:
    from src.v14 import terceros_1_0 as T10
    return T10.variables_excluidas() is not None


def escanear_dir(ambito: str, d: Path) -> list[dict]:
    """Ficheros publicados en el árbol o el paquete con columnas, claves u hojas de la fuente, o con su nombre en la ruta."""
    filas = []
    todos = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and ".git" not in p.relative_to(d).parts)
    for f in todos:
        hits = T.escanear(d / f) if f.endswith(EXT) else []
        if f.startswith("output/") and NOMBRE.search(Path(f).name):
            hits = ["nombre del fichero"] + hits
        if hits:
            filas.append({"ambito": ambito, "fichero": f, "hallazgos": "; ".join(hits), "arbol": _estado_dir(f, d / f, "; ".join(hits)), "paquete": ""})
    return filas


# ---------------------------------------------------------------- búsqueda por valores (el nombre de la fuente puede no estar)
FUENTES_BRUTAS = {
    "Notariado": ["data/raw/pdf/notariado_cgn_extranjeros_semestral.csv", "data/raw/pdf/notariado_cv_actos_mensual.csv",
                  "data/raw/pdf/notariado_cv_municipios_anual.csv", "data/raw/pdf/notariado_cv_prov_trimestral.csv"],
    "Registradores": ["data/raw/pdf/registradores_eri_anuario.csv", "data/raw/pdf/registradores_opendata_anual.csv",
                      "data/raw/pdf/registradores_opendata_compraventas.csv"],
    "AEAT": ["data/raw/v11/aeat_irpf_municipios/irpf_municipios_cv.csv.gz"],
}
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])")
TEXTO = (".csv", ".gz", ".json", ".md", ".html", ".txt", ".tex", ".svg", ".js")


def _clave(v: float) -> str | None:
    """Valor «distintivo» normalizado a 2 decimales: |v| ≥ 100, sin años ni múltiplos de 100 (coinciden por azar)."""
    if v != v or abs(v) < 100 or abs(v) > 1e13 or (float(v).is_integer() and (1900 <= v <= 2100 or v % 100 == 0)):
        return None
    return f"{round(v, 2):.2f}"


def conjuntos_fuente() -> dict[str, tuple[set, set]]:
    """Por fuente: (valores distintivos de sus ficheros brutos, control = los mismos valores + 1)."""
    import pandas as pd
    out = {}
    for fuente, rutas in FUENTES_BRUTAS.items():
        s, c = set(), set()
        for r in rutas:
            p = RAIZ / r
            if not p.exists():
                continue
            d = pd.read_csv(p, low_memory=False)
            for col in d.columns:
                x = pd.to_numeric(d[col], errors="coerce").dropna().unique()
                for v in x:
                    if (k := _clave(float(v))) is not None:
                        s.add(k)
                        c.add(f"{round(float(v) + 1, 2):.2f}")
        out[fuente] = (s, c)
    return out


def _tokens(p: Path) -> set[str]:
    if p.name.endswith(".parquet"):
        import pyarrow.parquet as pq
        import pyarrow.types as pt
        t = pq.read_table(p)
        vals = set()
        for col in t.column_names:
            if pt.is_floating(t.schema.field(col).type) or pt.is_integer(t.schema.field(col).type):
                for v in t.column(col).unique().to_pylist():
                    if v is not None and (k := _clave(float(v))) is not None:
                        vals.add(k)
        return vals
    if p.name.endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as fh:
            txt = fh.read()
    else:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    out = set()
    for m in NUM.findall(txt):
        try:
            k = _clave(float(m))
        except ValueError:
            continue
        if k is not None:
            out.add(k)
    return out


# K16 (2026-10-23): coincidencias por valores revisadas a mano (falsos positivos: años, recuentos o citas, no la serie)
FALSOS_POSITIVOS_VALORES = {
    "docs/v18/bib/inmigracion/sa_2015_iza.md": "ficha bibliográfica: años y cifras del estudio citado, no la serie del Notariado",
    "output/v15/auditoria/alquiler/cobertura_temporal_variables.csv": "tabla de cobertura temporal: años y recuentos de periodos, no la serie de Registradores",
    "output/v18/estimacion/e6/informe.md": "informe de estimación: años, recuentos y coeficientes propios, no la serie del Notariado",
}


def por_valores(ambito: str, d: Path, fuentes: dict, min_coinc: int = 10, margen: float = 0.25) -> list[dict]:
    """Ficheros de d cuyos valores distintivos coinciden con los de una fuente muy por encima del control."""
    filas = []
    for f in sorted(p for p in d.rglob("*") if p.is_file() and p.name.endswith((*TEXTO, ".parquet"))
                    and ".git" not in p.relative_to(d).parts and not p.relative_to(d).as_posix().startswith("data/raw/")):
        tok = _tokens(f)
        if len(tok) < min_coinc:
            continue
        for fuente, (s, c) in fuentes.items():
            n, nc = len(tok & s), len(tok & c)
            if n >= min_coinc and (n - nc) / len(tok) >= margen:
                filas.append({"ambito": ambito, "fichero": f.relative_to(d).as_posix(), "fuente": fuente, "valores": len(tok),
                              "coinciden": n, "control": nc, "fraccion": round(n / len(tok), 3), "fraccion_control": round(nc / len(tok), 3),
                              "revision": FALSOS_POSITIVOS_VALORES.get(f.relative_to(d).as_posix())
                              or _redistribuido(fuente.lower()) or "PENDIENTE"})
    return filas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arbol")
    ap.add_argument("--paquete")
    ap.add_argument("--salida", default=str(RAIZ / "docs" / "v14" / "escaneo_terceros.csv"))
    ap.add_argument("--valores", action="store_true", help="también búsqueda por valores (árbol y paquete)")
    a = ap.parse_args()
    filas = escanear_repo()
    if a.arbol:
        filas += escanear_dir("árbol", Path(a.arbol))
    if a.paquete:
        filas += escanear_dir("paquete", Path(a.paquete))
    if a.valores:
        fu = conjuntos_fuente()
        print("valores distintivos por fuente:", {k: len(v[0]) for k, v in fu.items()})
        vf = []
        for ambito, d in (("árbol", a.arbol), ("paquete", a.paquete)):
            if d:
                vf += por_valores(ambito, Path(d), fu)
        sal_v = Path(a.salida).with_name(Path(a.salida).stem + "_valores.csv")
        with sal_v.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, ["ambito", "fichero", "fuente", "valores", "coinciden", "control", "fraccion", "fraccion_control", "revision"],
                               lineterminator="\n")
            w.writeheader()
            w.writerows(vf)
        print(f"por valores: {len(vf)} coincidencias por encima del control; pendientes: {sum(r['revision'] == 'PENDIENTE' for r in vf)}")
        for r in vf:
            print("  ", r)
    with open(a.salida, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, ["ambito", "fichero", "hallazgos", "arbol", "paquete"], lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    for ambito in ("repositorio", "árbol", "paquete"):
        sub = [r for r in filas if r["ambito"] == ambito]
        publ = [r for r in sub if "PENDIENTE" in (r["arbol"], r["paquete"])]
        print(f"{ambito}: {len(sub)} ficheros con hallazgos; pendientes: {len(publ)}")
        for r in publ[:60]:
            print("  ", r["fichero"], "|", r["hallazgos"][:200], "|", r["arbol"], r["paquete"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
