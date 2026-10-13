"""Comprobaciones de puerta V8 (entran en `make check`). Sin red.

1. Ninguna cifra previa a V8 (v1-v7.2) cambia sin figurar en ERRATA.md (huellas en docs/v8/cifras_base_v72.csv).
2. Todo p de los coeficientes de V8 lleva p ajustado y método (Holm o BH).
3. Ningún modelo destacado se elige por su p (motivo_destacado: regla del §8 + multiverso o error fuera de muestra).
4. Las atribuciones que votan en la regla del §9 llevan banda del 68 %.
5. Sin lenguaje causal en líneas C4 ni a partir de SHAP, importancias, dominancia, Granger o DML; sin léxico valorativo ni
   partidista (entregables V8, plantillas y fichas del verificador V8).
6. Cruces territoriales solo por código: ningún merge/join de src/v8 por columnas de nombre.
7. Toda cifra es trazable: plantillas V8 sin cifras fuera de marcadores, entregables sin marcadores sin resolver, cifras V8
   con origen en un hechos.json de output/v8 y coeficientes con su script.
K9 (revisión final): CAUSAL ampliado y NEG por proposición (negación ANTES del verbo); herencia de la capa C4 de la sección o de la tabla;
alcance ampliado (F5, cierre); cruces por AST (merge/join/map/set_index/pivot, left_on/right_on/index); bandas en F5 para todo método que compite;
metodo_ajuste ∈ {Holm, BH}; ERRATA con línea «id | sha256_nuevo»; destacado = menor RMSE de su familia; trazabilidad contra el hechos.json de origen.
Sale con código 1 si hay errores.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "src" / "v3"))
sys.path.insert(0, str(RAIZ / "src" / "v5"))
from check_texto import revisar_texto  # noqa: E402
from check_v5 import _sin_libres  # noqa: E402

OUT = RAIZ / "output" / "v8"
PLANT = RAIZ / "docs" / "v8" / "plantillas"
CK = RAIZ / "output" / "v5" / "cifras_clave.csv"
BASE = RAIZ / "docs" / "v8" / "cifras_base_v72.csv"
ERRATA = RAIZ / "ERRATA.md"
MARC = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([a-z_]+))?\}\}")
COLS = ["id", "indicador", "valor", "min", "max", "unidad", "periodo", "cobertura", "fuentes", "capa", "fecha_dato"]

CAUSAL = re.compile(r"\b(caus[aó]\w*|provoc\w*|efecto causal|impacto causal|se debe a|debido a|gracias a|hace que|"
                    r"ha hecho (?:subir|bajar)|explica[nr]? (?:la|el|que)|impuls\w*|empuj(?:a|an|ar|ó|aron|ando)|motor|(?<!se )mueve[n]?|desv(?:ía|ían|iar|ió)|fren(?:a|an|ar|ó|aron|ando)|"
                    r"se explica\w*|determin(?!ist)\w*)\b", re.I)
# negación que precede al término causal dentro de la misma proposición; la negación posterior («..., aunque sin identificación») no exime
NEGAR = re.compile(r"\b(no|nunca|ni|nada|tampoco|sin|ning[uú]n\w*)\b", re.I)
NEG = re.compile(r"\b(no|nunca|ni|sin|nada)\b[^.]{0,60}\b(causal\w*|caus\w*|atribuci[óo]n|identifica\w*)", re.I)   # compatibilidad con tests previos
METODOS_AJUSTE = {"Holm", "BH"}
METODOS_BANDA = {"svar_hd", "dominancia", "lpiv", "contabilidad"}
INTERP = re.compile(r"\b(SHAP|importancias?|dominancia|Granger|DML)\b", re.I)
# cifras permitidas en plantillas V8 además de las de v5: umbrales pre-registrados, capas, fases, decisiones y hallazgos
LIBRE_V8 = [r"\b(?:50|68|80|90|95) ?%", r"×100", r"\bC3s\b", r"\b[FJMRYH]\d{1,2}(?:-\d+)?\b", r"\bsha256\b", r"\bq = 0,10\b",
            r"\bSEED = \d+\b", r"\bAR\(\d\)"]


def _libres(linea: str) -> str:
    for p in LIBRE_V8:
        linea = re.sub(p, " ", linea)
    return _sin_libres(linea)


def _huella(ck, i: str) -> str:
    fila = [i] + [ck.at[i, c] for c in COLS[1:]]
    return hashlib.sha256("|".join(fila).encode()).hexdigest()


def _en_errata(errata: str, i: str, h: str | None) -> bool:
    """Línea de ERRATA.md con `id | sha256_nuevo` (cifra cambiada) o `id | desaparecida` (cifra retirada); no basta con citar el id."""
    clave = h if h else "desaparecida"
    pat = re.compile(r"(?:^|\|)\s*`?" + re.escape(i) + r"`?\s*\|\s*`?" + re.escape(clave), re.M)
    return bool(pat.search(errata))


def cifras_previas() -> list[str]:
    if not BASE.exists() or not CK.exists():
        return [f"falta {BASE.relative_to(RAIZ) if not BASE.exists() else CK.relative_to(RAIZ)}"]
    base = pd.read_csv(BASE, comment="#", dtype=str).set_index("id")["sha256"]
    ck = pd.read_csv(CK, dtype=str).fillna("").set_index("id")
    errata = ERRATA.read_text(encoding="utf-8") if ERRATA.exists() else ""
    err = []
    for i, h in base.items():
        if i not in ck.index:
            if not _en_errata(errata, i, None):
                err.append(f"cifra previa a V8 desaparecida sin línea «{i} | desaparecida» en ERRATA: {i}")
            continue
        nueva = _huella(ck, i)
        if nueva != h and not _en_errata(errata, i, nueva):
            err.append(f"cifra previa a V8 cambiada sin línea «{i} | {nueva[:12]}…» en ERRATA: {i}")
    return err


def _p_ajustados_df(c: pd.DataFrame, nombre: str) -> list[str]:
    err = []
    if "p" in c.columns:
        col = next((x for x in ("p_ajustado", "p_holm") if x in c.columns), None)
        if col is None:
            return [f"{nombre}: falta la columna p_ajustado (o p_holm)"]
        if "metodo_ajuste" not in c.columns:
            return [f"{nombre}: falta la columna metodo_ajuste"]
        con_p = c[c["p"].notna()]
        sin = con_p[con_p[col].isna() | con_p["metodo_ajuste"].isna()]
        if len(sin):
            err.append(f"{nombre}: {len(sin)} p sin {col} o sin metodo_ajuste")
        mal = con_p[con_p[col].notna() & ~con_p["metodo_ajuste"].astype(str).isin(METODOS_AJUSTE)]
        if len(mal):
            err.append(f"{nombre}: {len(mal)} filas con metodo_ajuste fuera de {sorted(METODOS_AJUSTE)}")
    elif "p_holm" in c.columns or "p_ajustado" in c.columns:
        col = "p_holm" if "p_holm" in c.columns else "p_ajustado"
        if "metodo_ajuste" not in c.columns:
            return [f"{nombre}: falta la columna metodo_ajuste"]
        con = c[c[col].notna()]
        mal = con[~con["metodo_ajuste"].astype(str).isin(METODOS_AJUSTE)]
        if len(mal):
            err.append(f"{nombre}: {len(mal)} filas con metodo_ajuste fuera de {sorted(METODOS_AJUSTE)}")
    return err


def p_ajustados() -> list[str]:
    err = []
    for p in sorted(OUT.glob("M*/coeficientes.csv")):
        c = pd.read_csv(p, low_memory=False)
        err += _p_ajustados_df(c, str(p.relative_to(RAIZ)))
        if "p" in c.columns and "script" in c.columns and c["script"].isna().any():
            err.append(f"{p.relative_to(RAIZ)}: coeficientes sin script")
    for p in sorted(OUT.glob("M*/hipotesis_m*.csv")):
        err += _p_ajustados_df(pd.read_csv(p, low_memory=False), str(p.relative_to(RAIZ)))
    return err


def destacados_vs_oos(t: pd.DataFrame, oos: pd.DataFrame) -> list[str]:
    """El destacado (b) de cada (módulo, familia, mercado, periodo) es el de menor RMSE fuera de muestra entre los candidatos de su módulo.
    Candidatos (columna `rmse` de f6_tablas.leer_oos): M0 AR1+X*, M4 *_SR y *_ECM, M6 ols_*."""
    cand = {"M0": lambda m: m.startswith("AR1+X"), "M4": lambda m: m.endswith(("_SR", "_ECM")), "M6": lambda m: m.startswith("ols_")}
    err = []
    d = t[t["destacado"].astype(str).str.lower().isin(["si", "sí", "true"])]
    for (mod, fam, mer, per), g in d.groupby(["modulo", "familia_modelo", "mercado", "periodo"]):
        if mod not in cand:
            err.append(f"tablas_modelos_destacados: módulo {mod} sin regla de candidatos para comprobar el destacado")
            continue
        o = oos[(oos["modulo"] == mod) & (oos["mercado"] == mer)]
        o = o[o["modelo"].map(cand[mod])]
        if o.empty:
            err.append(f"tablas_modelos_destacados: sin OOS para {mod} {mer}")
            continue
        mejor = float(o["rmse"].min())
        for r in g.drop_duplicates("modelo_id").itertuples():
            if abs(float(r.rmse_oos) - mejor) > 1e-6:
                err.append(f"tablas_modelos_destacados: {r.modelo_id} ({fam}, {mer}, {per}) tiene RMSE {float(r.rmse_oos):.4f}, pero el menor de {mod} es {mejor:.4f}")
    return err


def destacados() -> list[str]:
    p = OUT / "tablas_modelos_destacados.csv"
    if not p.exists():
        return ["falta output/v8/tablas_modelos_destacados.csv"]
    t = pd.read_csv(p, low_memory=False)
    d = t[t["destacado"].astype(str).str.lower().isin(["si", "sí", "true"])]
    err = []
    for r in d.itertuples():
        m = str(r.motivo_destacado)
        if not re.search(r"fuera de muestra|regla", m, re.I) or re.search(r"\bp\b|p-valor|p ajustado|significa", m, re.I):
            err.append(f"tablas_modelos_destacados: {r.modelo_id} con motivo no admitido «{m[:60]}»")
    try:
        sys.path.insert(0, str(RAIZ / "src" / "v8"))
        import f6_tablas
        err += destacados_vs_oos(t, f6_tablas.leer_oos())
    except Exception as ex:   # sin la tabla OOS no se puede comprobar: error controlado
        err.append(f"tablas_modelos_destacados: no se pudo recalcular el OOS ({type(ex).__name__}: {ex})")
    return err


def bandas_df(a: pd.DataFrame) -> list[str]:
    v = a[(a["compite"].astype(str) == "si") & a["metodo"].isin(METODOS_BANDA)]
    sin = v[v["b68_lo"].isna() | v["b68_hi"].isna()]
    sin = sin[~sin["notas"].fillna("").str.contains("sin banda", case=False)]
    return [f"F5: atribución que compite sin banda del 68 % ni nota «sin banda»: {r.metodo} {r.mercado} {r.periodo} {r.factor}" for r in sin.itertuples()]


def bandas() -> list[str]:
    p = OUT / "F5" / "atribucion_combinada.csv"
    if not p.exists():
        return ["falta output/v8/F5/atribucion_combinada.csv"]
    return bandas_df(pd.read_csv(p))


def _textos() -> list[Path]:
    extra = [OUT / "F5" / "fichas.md", OUT / "F5" / "resumen.md", RAIZ / "docs" / "v8" / "cierre_proyecto.md"]
    return sorted(p for p in PLANT.rglob("*.md") if p.name != "README.md") + sorted(OUT.glob("*.md")) + extra


def causal_sin_negar(texto: str) -> bool:
    """Hay un término causal en alguna proposición (dividida por «.» y «;») sin negación previa en esa proposición (tras la última coma)."""
    for prop in re.split(r"[.;]", texto):
        for m in CAUSAL.finditer(prop):
            previo = prop[max(0, m.start() - 70):m.start()].split(",")[-1]
            if not NEGAR.search(previo):
                return True
    return False


def _es_c4_propio(linea: str):
    """True/False si la línea declara su propia capa; None si no la declara (hereda)."""
    tags = re.findall(r"\bC[1-4]s?\b", linea)
    if "[C4]" in linea:
        return True
    if not tags:
        return None
    return "C4" in tags and "C3s" not in tags


def lineas_causales(t: str, nombre: str) -> list[str]:
    err = []
    sec_c4 = False
    tbl_c4 = False
    prev = ""
    prev_tabla = False
    for i, linea in enumerate(t.splitlines(), 1):
        if linea.lstrip().startswith("#"):
            tg = re.findall(r"\bC[1-4]s?\b", linea)
            sec_c4 = "C4" in tg and "C3s" not in tg
            tbl_c4 = False
        es_tabla = linea.lstrip().startswith("|")
        if es_tabla and not prev_tabla:   # primera fila de una tabla: la cabecera o el rótulo anterior declaran su capa
            tg = re.findall(r"\bC[1-4]s?\b", linea + " " + prev)
            tbl_c4 = "C4" in tg and "C3s" not in tg
        if not es_tabla:
            tbl_c4 = False
        prev_tabla = es_tabla
        if linea.strip():
            prev = linea
        if "check:ok" in linea or not CAUSAL.search(linea) or not causal_sin_negar(linea):
            continue
        propio = _es_c4_propio(linea)
        c4 = propio if propio is not None else (tbl_c4 if es_tabla else sec_c4) or sec_c4
        if re.search(r"condicionad\w* a las restricciones", linea) and "[C4]" not in linea:
            c4 = False
        if c4:
            err.append(f"{nombre}:{i}: lenguaje causal en línea C4: «{linea.strip()[:90]}»")
        if INTERP.search(linea):
            err.append(f"{nombre}:{i}: lectura causal desde SHAP, importancias, dominancia, Granger o DML: «{linea.strip()[:90]}»")
    return err


def texto() -> list[str]:
    err = []
    for p in _textos() + [OUT / "fichas_verificador_v8.json"]:
        if not p.exists():
            continue
        nombre = str(p.relative_to(RAIZ))
        t = p.read_text(encoding="utf-8")
        err += revisar_texto(t, nombre)
        err += lineas_causales(t, nombre)
    return err


NOMBRE = re.compile(r"nombre|name", re.I)


def cruces_en(src: str, nombre: str) -> list[str]:
    """Cruces por columnas de nombre en merge/join/set_index/pivot (on, left_on, right_on, index, by) y .map( sobre columnas de nombre."""
    err = []
    try:
        arbol = ast.parse(src)
    except SyntaxError as ex:
        return [f"{nombre}: no se pudo analizar ({ex})"]

    def cadenas(n):
        return [x.value for x in ast.walk(n) if isinstance(x, ast.Constant) and isinstance(x.value, str)]
    for n in ast.walk(arbol):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)):
            continue
        at = n.func.attr
        cand: list[str] = []
        if at in ("merge", "join", "set_index", "pivot", "pivot_table"):
            for k in n.keywords:
                if k.arg in ("on", "left_on", "right_on", "index", "by"):
                    cand += cadenas(k.value)
            args = n.args if at == "set_index" else n.args[1:]
            for a in args:
                cand += cadenas(a)
        elif at == "map":
            cand += cadenas(n.func.value)
        for c in cand:
            if NOMBRE.search(c):
                err.append(f"{nombre}:{n.lineno}: cruce por nombre «{c}» en .{at}( (V8: solo por código INE)")
    return err


def cruces() -> list[str]:
    err = []
    for p in sorted((RAIZ / "src" / "v8").rglob("*.py")):
        err += cruces_en(p.read_text(encoding="utf-8"), str(p.relative_to(RAIZ)))
    return err


def origen_hechos(v8: pd.DataFrame) -> list[str]:
    """Abre el hechos.json de `origen` («ruta:id») y comprueba que existen el id y que su valor coincide con el de cifras_clave."""
    err, cache = [], {}
    for r in v8.itertuples():
        o = str(r.origen)
        ruta, _, i = o.partition(":")
        f = RAIZ / ruta
        if not ruta.startswith("output/v8/") or not f.is_file():
            err.append(f"cifras_clave: {r.id}: el origen {ruta} no existe")
            continue
        if ruta not in cache:
            cache[ruta] = {h["id"]: h for h in json.loads(f.read_text(encoding="utf-8"))}
        h = cache[ruta].get(i or r.id)
        if h is None:
            err.append(f"cifras_clave: {r.id}: el id {i or r.id} no está en {ruta}")
            continue
        va, vb = h.get("valor"), str(r.valor)
        if va is None:
            ok = vb in ("", "nan")
        else:
            try:
                ok = vb not in ("", "nan") and abs(float(vb) - float(va)) <= 1e-6 * max(1.0, abs(float(va)))
            except ValueError:
                ok = False
        if not ok:
            err.append(f"cifras_clave: {r.id}: valor {vb} distinto del de {ruta} ({va})")
    return err


def trazabilidad() -> list[str]:
    err = []
    for p in sorted(PLANT.rglob("*.md")):
        if p.name == "README.md":
            continue
        for i, linea in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if "check:cifra-libre" in linea:
                continue
            if re.search(r"\d", _libres(MARC.sub(" ", linea))):
                err.append(f"{p.relative_to(RAIZ)}:{i}: cifra fuera de cifras_clave: «{linea.strip()[:90]}»")
        dest = OUT / p.relative_to(PLANT)
        if not dest.exists():
            err.append(f"falta el entregable renderizado {dest.relative_to(RAIZ)}")
    for p in sorted(OUT.glob("*.md")):
        if MARC.search(p.read_text(encoding="utf-8")):
            err.append(f"{p.relative_to(RAIZ)}: marcador sin resolver")
    if CK.exists():
        ck = pd.read_csv(CK, dtype=str)
        v8 = ck[ck["id"].str.startswith("V8-")]
        mal = v8[~v8["origen"].fillna("").str.startswith("output/v8/")]
        err += [f"cifras_clave: {r.id} sin origen en output/v8" for r in mal.itertuples()]
        err += origen_hechos(v8)
    return err


def main() -> int:
    err = cifras_previas() + p_ajustados() + destacados() + bandas() + texto() + cruces() + trazabilidad()
    for e in err:
        print(e)
    print(f"check_v8: {len(err)} errores")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
