"""Muestra sellada (holdout) de la v2.

Único punto de acceso a data/sealed. Reglas (docs/v2/decisiones.md, CLAUDE.md):
- Sellado temporal: los últimos 8 trimestres, 2024Q3-2026Q2 (en datos anuales: años >= 2025
  sellados y 2024 como EMBARGO, excluido de entrenamiento y de evaluación, porque mezcla
  trimestres de entrenamiento y sellados).
- Sellado transversal: 3 provincias elegidas con semilla fija (SEED=20261010) se excluyen de
  entrenamiento en TODOS los periodos (y sus municipios en los paneles municipales).
- Las ramas solo leen `load_train(nombre)`. `evaluate(hipotesis, fn)` abre la muestra sellada
  UNA vez por hipótesis confirmatoria, registra el acceso y se niega a repetirlo.
- data/sealed se resuelve en el repositorio PRINCIPAL (git common dir), no en el worktree.

Uso:
    python3 src/holdout.py build        # (re)genera train/ y sealed/ desde data/processed/v2
    from holdout import load_train, evaluate
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20261010
Q_SELLO_INI, Q_SELLO_FIN = "2024Q3", "2026Q2"
ANIO_EMBARGO, ANIO_SELLO_INI = 2024, 2025
N_PROV_SELLADAS = 3

HERE = Path(__file__).resolve().parents[1]          # raíz del worktree o del repo
TRAIN = HERE / "data" / "processed" / "v2" / "train"  # paneles de entrenamiento (versionados)


def _repo_principal() -> Path:
    """Raíz del repositorio principal aunque se ejecute desde un worktree."""
    try:
        common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
        return Path(common).parent
    except Exception:  # noqa: BLE001
        return HERE


SEALED = _repo_principal() / "data" / "sealed"
LOG = SEALED / "_accesos.log"
SRC_V2 = SEALED / "_full"                             # paneles completos (NO versionados)
LOG_MD = _repo_principal() / "docs" / "v2" / "holdout_accesos.md"

# Catálogo de paneles: nombre -> (frecuencia, columna de periodo, columna de provincia o None)
CATALOGO = {
    "panel_prov_q": ("Q", "trimestre", "cod_prov"),
    "panel_prov_a": ("A", "anio", "cod_prov"),
    "panel_muni_a": ("A", "anio", "cod_prov"),
    "panel_ue_a": ("A", "anio", None),
    "panel_ue_q": ("Q", "trimestre", None),
    "nacional_q_v2": ("Q", "trimestre", None),
    "eventos_q": ("Q", "trimestre", None),
}

# 52 provincias (códigos INE 01-52)
PROVINCIAS = [f"{i:02d}" for i in range(1, 53)]


def provincias_selladas() -> list[str]:
    rng = np.random.default_rng(SEED)
    return sorted(rng.choice(PROVINCIAS, size=N_PROV_SELLADAS, replace=False).tolist())


def _mascara_sellada(df: pd.DataFrame, freq: str, col_t: str, col_geo: str | None):
    """Devuelve (sellado, embargo) como máscaras booleanas."""
    if freq == "Q":
        t = df[col_t].astype(str)
        temporal = t >= Q_SELLO_INI   # todo lo posterior al inicio del sellado (incluye filas > 2026Q2 si existen)
        embargo = pd.Series(False, index=df.index)
    else:
        a = pd.to_numeric(df[col_t], errors="coerce")
        temporal = a >= ANIO_SELLO_INI
        embargo = a == ANIO_EMBARGO
    geo = pd.Series(False, index=df.index)
    if col_geo is not None and col_geo in df.columns:
        geo = df[col_geo].astype(str).str.zfill(2).isin(provincias_selladas())
    return temporal | geo, embargo & ~(temporal | geo)


def _sin_interpolacion_hacia_sellado(tr: pd.DataFrame, col_t: str, col_geo: str | None) -> pd.DataFrame:
    """Anula en entrenamiento los valores interpolados POSTERIORES a la última observación de entrenamiento.

    Una interpolación entre la última observación de entrenamiento y la primera sellada (p. ej. población
    de 2024Q2 entre el 1-ene-2024 y el 1-ene-2025) usa información sellada: fuga. Esos valores (y sus
    transformaciones ln_/d_ln_/d4_ln_) pasan a NaN.
    """
    met = [c for c in tr.columns if c.endswith("_metodo")]
    grupos = tr.groupby(col_geo) if col_geo and col_geo in tr.columns else [(None, tr)]
    for _, g in grupos:
        for mc in met:
            var = mc[: -len("_metodo")]
            obs = g.loc[g[mc] == "observado", col_t]
            if obs.empty:
                continue
            ult = obs.astype(str).max()
            idx = g.index[(g[mc] == "interpolado_loglineal") & (g[col_t].astype(str) > ult)]
            if len(idx):
                cols = [c for c in (var, f"ln_{var}", f"d_ln_{var}", f"d4_ln_{var}") if c in tr.columns]
                tr.loc[idx, cols] = np.nan
                tr.loc[idx, mc] = "anulado_fuga_sellado"
    return tr


# Índices publicados en base 2025=100 (INE IPV e IPC): su nivel incorpora información de 2025 (sellada).
# En entrenamiento se rebasan a media de 2015 = 100 por unidad; las diferencias logarítmicas no cambian.
INDICES_BASE_2025 = ["ipc_alquiler", "ipv", "ipv_nueva", "ipv_usada"]


def _rebase_indices_2015(tr: pd.DataFrame, nombre: str, col_t: str, col_geo: str | None) -> pd.DataFrame:
    anio = tr[col_t].astype(str).str[:4]
    unidad = tr[col_geo].astype(str) if col_geo and col_geo in tr.columns else pd.Series("_", index=tr.index)
    lnf = {}
    for v in INDICES_BASE_2025:
        if v not in tr.columns:
            continue
        base = tr[v].where(anio == "2015").groupby(unidad).transform("mean")
        f = 100.0 / base
        tr[v] = tr[v] * f
        lnf[v] = np.log(f)
        if f"ln_{v}" in tr.columns:
            tr[f"ln_{v}"] = tr[f"ln_{v}"] + lnf[v]
    if "ratio_precio_alquiler_idx" in tr.columns and "ipc_alquiler" in lnf:
        ajuste = -lnf["ipc_alquiler"]
        if nombre == "nacional_q_v2" and "ipv" in lnf:   # nacional: ln ipv − ln ipc_alquiler
            ajuste = ajuste + lnf["ipv"]
        tr["ratio_precio_alquiler_idx"] = tr["ratio_precio_alquiler_idx"] + ajuste
    return tr


def build() -> dict:
    """Genera data/processed/v2/train/<p>.csv y data/sealed/<p>.csv para cada panel existente."""
    TRAIN.mkdir(parents=True, exist_ok=True)
    SEALED.mkdir(parents=True, exist_ok=True)
    resumen = {"provincias_selladas": provincias_selladas(), "paneles": {}}
    for nombre, (freq, col_t, col_geo) in CATALOGO.items():
        src = SRC_V2 / f"{nombre}.csv"
        if not src.exists():
            src = SRC_V2 / f"{nombre}.csv.gz"
        if not src.exists():
            continue
        df = pd.read_csv(src, dtype={col_geo: str} if col_geo else None)
        # Rebase ANTES de separar: entrenamiento y sellado quedan en la MISMA base (2015=100 por unidad).
        # El factor usa solo valores de 2015 (anteriores al sellado). Rebasar solo el entrenamiento
        # anulaba por construcción efectos medidos concatenando niveles (revisión BP).
        df = _rebase_indices_2015(df, nombre, col_t, col_geo)
        sell, emb = _mascara_sellada(df, freq, col_t, col_geo)
        tr = _sin_interpolacion_hacia_sellado(df[~sell & ~emb].copy(), col_t, col_geo)
        tr.to_csv(TRAIN / f"{nombre}.csv", index=False)
        df[sell].to_csv(SEALED / f"{nombre}.csv", index=False)
        resumen["paneles"][nombre] = {"filas": len(df), "train": int((~sell & ~emb).sum()),
                                      "sellado": int(sell.sum()), "embargo": int(emb.sum())}
    (TRAIN / "_sellado.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False))
    return resumen


def load_train(nombre: str) -> pd.DataFrame:
    """Lectura permitida para las ramas: solo la parte de entrenamiento."""
    _freq, _col_t, col_geo = CATALOGO[nombre]
    return pd.read_csv(TRAIN / f"{nombre}.csv", dtype={col_geo: str} if col_geo else None)


def _accesos() -> list[dict]:
    if not LOG.exists():
        return []
    return [json.loads(x) for x in LOG.read_text().splitlines() if x.strip()]


def evaluate(hipotesis: str, fn, rama: str, paneles: list[str]):
    """Evalúa UNA vez una hipótesis confirmatoria (id de docs/v2/hipotesis.md) en la muestra sellada.

    fn(dict nombre->DataFrame sellado, dict nombre->DataFrame train) -> dict serializable.
    """
    # Cualquier acceso previo (apertura o evaluación) cuenta: una sola apertura por hipótesis, aunque falle.
    if any(a["hipotesis"] == hipotesis for a in _accesos()):
        raise PermissionError(f"La hipótesis {hipotesis} ya abrió la muestra sellada (una sola vez).")
    SEALED.mkdir(parents=True, exist_ok=True)
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": hipotesis, "rama": rama, "paneles": paneles}
    with open(LOG, "a") as f:   # se registra ANTES de leer nada sellado
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], hipotesis, rama, paneles, "APERTURA (antes de leer)")
    sellado = {}
    for p in paneles:
        _freq, _col_t, col_geo = CATALOGO[p]
        sellado[p] = pd.read_csv(SEALED / f"{p}.csv", dtype={col_geo: str} if col_geo else None)
    train = {p: load_train(p) for p in paneles}
    res = fn(sellado, train)
    reg = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "evaluacion",
           "hipotesis": hipotesis, "rama": rama, "paneles": paneles, "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    _log_md(reg["utc"], hipotesis, rama, paneles, json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


HIPOTESIS_V2_SELLADAS = ("H1", "H2", "H6", "H7")   # las cuatro con evaluación sellada en v2


def load_full(nombre: str, uso: str) -> pd.DataFrame:
    """v3: panel COMPLETO (entrenamiento + sellado v2) para hechos (C1) y cotas (C2).

    Solo se permite cuando todas las evaluaciones selladas de v2 ya se hicieron: el sellado v2 ya no
    protege ninguna hipótesis pendiente. Cada lectura se registra (evento «v3_completo»).
    El sellado v3 propio (secciones censales) es otro y no pasa por aquí.
    """
    hechas = {a["hipotesis"] for a in _accesos() if a.get("evento") == "evaluacion"}
    if LOG_MD.exists():   # copia versionada del registro (un clon limpio no tiene data/sealed/_accesos.log)
        for linea in LOG_MD.read_text().splitlines():
            celdas = [c.strip() for c in linea.split("|")]
            if len(celdas) > 5 and celdas[2] in HIPOTESIS_V2_SELLADAS and not celdas[5].startswith("APERTURA"):
                hechas.add(celdas[2])
    faltan = [h for h in HIPOTESIS_V2_SELLADAS if h not in hechas]
    if faltan:
        raise PermissionError(f"Evaluaciones selladas v2 pendientes: {faltan}")
    _freq, _col_t, col_geo = CATALOGO[nombre]
    src = SRC_V2 / f"{nombre}.csv"
    df = pd.read_csv(src, dtype={col_geo: str} if col_geo else None)
    df = _rebase_indices_2015(df, nombre, _col_t, col_geo)
    reg = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "v3_completo",
           "hipotesis": "-", "rama": uso, "paneles": [nombre]}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    return df


# ---------------------------------------------------------------- sellado v3 (secciones censales, P-C)
ULTIMA_OLEADA_V3 = "2026M05"          # última oleada de VUT del INE: sellada para todas las unidades
FRACCION_DISTRITOS_V3 = 0.20
VUT_SECCION = HERE / "data" / "raw" / "v3" / "ine_v3_vut_seccion.csv.gz"


def bloques_distritos_v3(distritos: list[str]) -> dict[str, str]:
    """distrito (7 dígitos: municipio 5 + distrito 2) -> bloque espacial.

    Sin cartografía: en municipios con ≥2 distritos, pares de distritos de numeración consecutiva (01-02, 03-04…);
    en municipios con un solo distrito, el propio municipio. Supuesto documentado en docs/v3/decisiones.md.
    """
    dist = sorted(set(distritos))
    por_mun: dict[str, list[str]] = {}
    for d in dist:
        por_mun.setdefault(d[:5], []).append(d)
    out = {}
    for mun, ds in por_mun.items():
        for d in ds:
            out[d] = mun if len(ds) == 1 else f"{mun}-{(int(d[5:]) - 1) // 2:02d}"
    return out


def distritos_sellados_v3() -> list[str]:
    """20 % de los distritos por bloques espaciales completos, ESTRATIFICADO: en municipios con ≥4 bloques el
    estrato es el municipio (cada gran ciudad conserva ~80 % de sus distritos para estimar); el resto de bloques
    se estratifica por provincia. En cada estrato, bloques en orden aleatorio (SEED) hasta alcanzar el 20 % de sus
    distritos. Lista de distritos de la oleada 2024M02 (estable)."""
    v = pd.read_csv(VUT_SECCION, usecols=["periodo", "nivel", "codigo"], dtype={"codigo": str})
    dist = v.loc[(v["nivel"] == "distrito") & (v["periodo"] == "2024M02"), "codigo"].str.zfill(7).unique().tolist()
    bl = bloques_distritos_v3(dist)
    miembros: dict[str, list[str]] = {}
    for d, b in bl.items():
        miembros.setdefault(b, []).append(d)
    n_bloques_mun: dict[str, int] = {}
    for b in miembros:
        n_bloques_mun[b[:5]] = n_bloques_mun.get(b[:5], 0) + 1
    estratos: dict[str, list[str]] = {}
    for b in sorted(miembros):
        e = b[:5] if n_bloques_mun[b[:5]] >= 4 else b[:2]
        estratos.setdefault(e, []).append(b)
    rng = np.random.default_rng(SEED)
    sel = set()
    for e in sorted(estratos):
        bs = estratos[e]
        objetivo = FRACCION_DISTRITOS_V3 * sum(len(miembros[b]) for b in bs)
        n = 0
        for i in rng.permutation(len(bs)):
            if n >= objetivo - 1e-9 or n + len(miembros[bs[i]]) > objetivo + 1:   # no pasarse más de 1 distrito
                continue
            sel.add(bs[i])
            n += len(miembros[bs[i]])
    return sorted(d for d, b in bl.items() if b in sel)


def es_sellado_v3(codigo_seccion_o_distrito: pd.Series, periodo: pd.Series | None = None,
                  sellados: list[str] | None = None) -> pd.Series:
    """True si la unidad pertenece a un distrito sellado o la observación es de la última oleada."""
    sellados = set(sellados if sellados is not None else distritos_sellados_v3())
    m = codigo_seccion_o_distrito.astype(str).str.zfill(7).str[:7].isin(sellados)
    if periodo is not None:
        m = m | (periodo.astype(str) >= ULTIMA_OLEADA_V3)
    return m


def sellar_v3(df: pd.DataFrame, nombre: str, col_codigo: str, col_periodo: str | None = None,
              col_municipio: str | None = None) -> pd.DataFrame:
    """Separa un panel v3 construido por una rama: escribe la parte sellada en data/sealed/v3_<nombre>.csv
    (sin devolverla ni mostrarla) y devuelve SOLO la parte de entrenamiento.

    Unidades selladas: distrito sellado (código de sección o distrito) o, en paneles municipales
    (col_municipio), municipios con ≥50 % de sus distritos sellados; más la última oleada si col_periodo.
    """
    sell = distritos_sellados_v3()
    if col_municipio is not None:
        v = pd.read_csv(VUT_SECCION, usecols=["periodo", "nivel", "codigo"], dtype={"codigo": str})
        dist = v.loc[(v["nivel"] == "distrito") & (v["periodo"] == "2024M02"), "codigo"].str.zfill(7)
        frac = dist.isin(set(sell)).groupby(dist.str[:5]).mean()
        mun_sell = set(frac[frac >= 0.5].index)
        m = df[col_municipio].astype(str).str.zfill(5).isin(mun_sell)
    else:
        m = es_sellado_v3(df[col_codigo], None, sell)
    if col_periodo is not None:
        m = m | (df[col_periodo].astype(str) >= ULTIMA_OLEADA_V3)
    SEALED.mkdir(parents=True, exist_ok=True)
    df[m].to_csv(SEALED / f"v3_{nombre}.csv", index=False)
    return df[~m].copy()


def sellar_fuente_v3(df: pd.DataFrame, nombre: str) -> None:
    """Validación sellada POR FUENTE (P-C3): guarda el panel entero en data/sealed/v3_<nombre>.csv sin devolverlo.
    La rama lo construye sin mirarlo (sin describe ni estimaciones) y solo se lee vía evaluate_v3."""
    SEALED.mkdir(parents=True, exist_ok=True)
    df.to_csv(SEALED / f"v3_{nombre}.csv", index=False)


def evaluate_v3(hipotesis: str, fn, rama: str, nombres: list[str]):
    """Como evaluate(), para paneles v3 escritos por sellar_v3. Una sola apertura por hipótesis (registrada antes
    de leer). fn(dict nombre->DataFrame sellado) -> dict serializable."""
    if any(a["hipotesis"] == hipotesis for a in _accesos()):
        raise PermissionError(f"La hipótesis {hipotesis} ya abrió la muestra sellada (una sola vez).")
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": hipotesis, "rama": rama, "paneles": [f"v3_{n}" for n in nombres]}
    with open(LOG, "a") as f:
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], hipotesis, rama, apertura["paneles"], "APERTURA (antes de leer)")
    sellado = {n: pd.read_csv(SEALED / f"v3_{n}.csv", dtype={c: str for c in ("codigo", "seccion", "distrito",
                                                                           "cod_ine", "cod_muni", "cusec")})
               for n in nombres}
    res = fn(sellado)
    reg = {**apertura, "utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "evento": "evaluacion", "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    _log_md(reg["utc"], hipotesis, rama, apertura["paneles"], json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


def _log_md(utc, hipotesis, rama, paneles, texto):
    LOG_MD.parent.mkdir(parents=True, exist_ok=True)
    nuevo = not LOG_MD.exists()
    with open(LOG_MD, "a") as f:
        if nuevo:
            f.write("# Accesos a la muestra sellada (copia versionada de data/sealed/_accesos.log)\n\n"
                    "| UTC | hipótesis | rama | paneles | evento / resultado |\n|---|---|---|---|---|\n")
        f.write(f"| {utc} | {hipotesis} | {rama} | {', '.join(paneles)} | {texto} |\n")


# ============================================================================== v6
# Validación sellada NUEVA de v6 (docs/v6/decisiones.md, docs/v6/hipotesis.md), distinta de v2 y v3:
# - temporal: el último año disponible de cada panel (lo indica la rama al sellar);
# - transversal, por bloques espaciales: 20 % de las provincias, por bloques completos de CCAA, excluidas las CCAA con
#   provincias selladas en v2; los municipios y distritos de esas provincias quedan sellados (≈20 % en cada nivel; una
#   sola partición espacial, sin fuga entre niveles); los distritos sellados en v3 se excluyen de todo uso.
SEED_V6 = SEED + 6
FRACCION_V6 = 0.20
CCAA_PROV = {"01": "16", "02": "08", "03": "10", "04": "01", "05": "07", "06": "11", "07": "04", "08": "09", "09": "07",
             "10": "11", "11": "01", "12": "10", "13": "08", "14": "01", "15": "12", "16": "08", "17": "09", "18": "01",
             "19": "08", "20": "16", "21": "01", "22": "02", "23": "01", "24": "07", "25": "09", "26": "17", "27": "12",
             "28": "13", "29": "01", "30": "14", "31": "15", "32": "12", "33": "03", "34": "07", "35": "05", "36": "12",
             "37": "07", "38": "05", "39": "06", "40": "07", "41": "01", "42": "07", "43": "09", "44": "02", "45": "08",
             "46": "10", "47": "07", "48": "16", "49": "07", "50": "02"}
CCAA_PROV.update({"51": "18", "52": "19"})


def provincias_selladas_v6() -> list[str]:
    """20 % de las 52 provincias por bloques completos de CCAA (orden aleatorio con SEED_V6), sin CCAA que contengan
    provincias selladas en v2 ni Ceuta/Melilla. Se añaden bloques mientras no se supere el 20 % en más de 2 provincias."""
    excl = {CCAA_PROV[p] for p in provincias_selladas()} | {"18", "19"}
    bloques: dict[str, list[str]] = {}
    for prov, cc in sorted(CCAA_PROV.items()):
        if cc not in excl:
            bloques.setdefault(cc, []).append(prov)
    objetivo = FRACCION_V6 * len(PROVINCIAS)
    rng = np.random.default_rng(SEED_V6)
    sel: list[str] = []
    claves = sorted(bloques)
    for i in rng.permutation(len(claves)):
        b = bloques[claves[i]]
        if len(sel) >= objetivo:
            break
        if len(sel) + len(b) <= objetivo + 2:
            sel += b
    return sorted(sel)


def municipio_sellado_v6(cod_mun: str) -> bool:
    """Municipio (5 dígitos) sellado si su provincia lo está: una sola partición espacial para todos los niveles
    (≈20 % de provincias, municipios y distritos), sin fuga entre niveles en modelos jerárquicos."""
    return str(cod_mun).zfill(5)[:2] in set(provincias_selladas_v6())


def excluir_sellados_v6(df: pd.DataFrame, col: str, nivel: str) -> pd.DataFrame:
    """V17-V18 (guarda de fuga v6, docs/v17/decisiones.md): devuelve df sin las filas de las unidades selladas en v6.

    nivel: «ccaa» (código de 2 dígitos de CCAA), «provincia» (2), «municipio» (5), «distrito» (7) o «seccion» (10); para los
    niveles por debajo de la CCAA se toma la provincia de los 2 primeros dígitos. «nacional» devuelve df sin cambios. Solo
    filtra con los códigos calculados aquí; nunca abre la muestra sellada."""
    if nivel == "nacional":
        return df
    cod = df[col].astype(str).str.strip()
    if nivel == "ccaa":
        return df[~cod.str.zfill(2).isin(ccaa_selladas_v6())]   # K8 de V16 (definida más abajo)
    ancho = {"provincia": 2, "municipio": 5, "distrito": 7, "seccion": 10}
    if nivel not in ancho:
        raise ValueError(f"nivel desconocido: {nivel}")
    return df[~cod.str.zfill(ancho[nivel]).str[:2].isin(provincias_selladas_v6())]


def distrito_sellado_v6(cod_dist: str) -> bool | None:
    """Distrito (7 dígitos) sellado si su provincia lo está. None si fue sellado en v3: se EXCLUYE de todo uso en v6."""
    d = str(cod_dist).zfill(7)
    if d in set(distritos_sellados_v3()):
        return None
    return d[:2] in set(provincias_selladas_v6())


def sellar_v6(df: pd.DataFrame, nombre: str, nivel: str, col_anio: str, ultimo_anio: int,
              col_prov: str | None = None, col_mun: str | None = None, col_dist: str | None = None) -> pd.DataFrame:
    """Separa un panel v6: escribe la parte sellada en data/sealed/v6_<nombre>.csv (sin devolverla) y devuelve SOLO la
    de entrenamiento. Sellado = año >= ultimo_anio, o unidad sellada según el nivel ('provincia', 'municipio',
    'distrito'/'seccion'). Los distritos sellados en v3 se descartan de ambas partes."""
    a = pd.to_numeric(df[col_anio], errors="coerce") >= ultimo_anio
    if nivel == "provincia":
        u = df[col_prov].astype(str).str.zfill(2).isin(set(provincias_selladas_v6()))
        fuera = pd.Series(False, index=df.index)
    elif nivel == "municipio":
        u = df[col_mun].astype(str).str.zfill(5).map(municipio_sellado_v6).astype(bool)
        fuera = pd.Series(False, index=df.index)
    elif nivel in ("distrito", "seccion"):
        dd = df[col_dist].astype(str).str.zfill(10 if nivel == "seccion" else 7).str[:7]
        r = dd.map({d: distrito_sellado_v6(d) for d in dd.unique()})
        fuera = r.isna()
        u = r.fillna(False).astype(bool)
    else:
        raise ValueError(nivel)
    m = (a | u) & ~fuera
    SEALED.mkdir(parents=True, exist_ok=True)
    df[m].to_csv(SEALED / f"v6_{nombre}.csv", index=False)
    return df[~m & ~fuera].copy()


def evaluate_v6(modelo_id: str, fn, rama: str, nombres: list[str]):
    """Abre los paneles v6 sellados UNA vez por modelo/hipótesis (registrado antes de leer). fn(dict) -> dict."""
    clave = f"v6:{modelo_id}"
    if any(a["hipotesis"] == clave for a in _accesos()):
        raise PermissionError(f"{clave} ya abrió la muestra sellada v6 (una sola vez).")
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": clave, "rama": rama, "paneles": [f"v6_{n}" for n in nombres]}
    with open(LOG, "a") as f:
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], clave, rama, apertura["paneles"], "APERTURA (antes de leer)")
    sellado = {n: pd.read_csv(SEALED / f"v6_{n}.csv", dtype={c: str for c in ("codigo", "cod_prov", "cod_mun", "distrito",
                                                                           "seccion", "cusec")}) for n in nombres}
    res = fn(sellado)
    reg = {**apertura, "utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "evaluacion",
           "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    _log_md(reg["utc"], clave, rama, apertura["paneles"], json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


# ============================================================================== v15
# Validación sellada NUEVA de V15 (docs/v15/plan.md, fase 3.3; docs/v15/sellado_v15.md), fijada ANTES de estimar nada:
# - temporal: todo dato posterior al depósito del pre-registro (periodo posterior al último visto de cada variable, registrado
#   en docs/v15/sellado_v15.json al sellar, o edición publicada después de la fecha de corte);
# - espacial, por bloques aleatorios (SEED=20261010): celdas de 0,5° × 0,5° sobre los centroides municipales (≈ 45 km); se sella
#   el 15 % de las celdas con municipios del universo V15. Los municipios con 5 distritos o más nunca se sellan enteros: se sella
#   el 15 % de sus distritos (bloques intramunicipales para los diseños por sección). Partición anidada: un municipio sellado
#   sella todas sus secciones y distritos. Fuga declarada: el agregado municipal de una gran ciudad (entrenamiento) contiene sus
#   distritos sellados; por eso la evaluación por sección de esas ciudades no se combina con modelos municipales.
# - Universo V15: provincias visibles en la base (las selladas en v6 siguen fuera de todo uso; las de v2 ya se evaluaron).
SEED_V15 = SEED
FRACCION_V15 = 0.15
CELDA_V15 = 0.5
GEO = HERE / "data" / "base" / "geo"
MANIFIESTO_V15 = HERE / "docs" / "v15" / "sellado_v15.json"
PROYECTO = HERE / "proyecto.json"


def _centroides_municipios() -> pd.DataFrame:
    import shapely
    m = pd.read_parquet(GEO / "municipios.parquet", columns=["cod_municipio", "cod_provincia", "geometry"])
    c = shapely.centroid(shapely.from_wkb(m.geometry.values))
    return pd.DataFrame({"cod_municipio": m.cod_municipio.astype(str).str.zfill(5), "cod_provincia": m.cod_provincia.astype(str).str.zfill(2),
                         "lon": shapely.get_x(c), "lat": shapely.get_y(c)})


def celdas_selladas_v15() -> list[str]:
    m = _centroides_municipios()
    m = m[~m.cod_provincia.isin(set(provincias_selladas_v6()))]
    celda = (np.floor(m.lon / CELDA_V15).astype(int).astype(str) + "_" + np.floor(m.lat / CELDA_V15).astype(int).astype(str))
    todas = sorted(celda.unique())
    rng = np.random.default_rng(SEED_V15)
    n = int(round(FRACCION_V15 * len(todas)))
    return sorted(np.array(todas)[rng.permutation(len(todas))[:n]].tolist())


def _municipios_grandes() -> set[str]:
    """Municipios con 5 distritos o más: nunca se sellan enteros; se sellan por distritos (regla fijada antes de sortear)."""
    s = pd.read_parquet(GEO / "secciones.parquet", columns=["cod_distrito", "cod_municipio"]).astype(str)
    n = s.groupby(s.cod_municipio.str.zfill(5)).cod_distrito.nunique()
    return set(n[n >= 5].index)


def municipios_sellados_v15() -> set[str]:
    m = _centroides_municipios()
    m = m[~m.cod_provincia.isin(set(provincias_selladas_v6()))]
    celda = (np.floor(m.lon / CELDA_V15).astype(int).astype(str) + "_" + np.floor(m.lat / CELDA_V15).astype(int).astype(str))
    return set(m.cod_municipio[celda.isin(set(celdas_selladas_v15()))]) - _municipios_grandes()


def distritos_sellados_v15() -> set[str]:
    """15 % de los distritos (7 dígitos) de cada municipio no sellado con ≥ 5 distritos, más todos los de municipios sellados."""
    s = pd.read_parquet(GEO / "secciones.parquet", columns=["cod_distrito", "cod_municipio"]).astype(str)
    s["cod_distrito"] = s.cod_distrito.str.zfill(7)
    s["cod_municipio"] = s.cod_municipio.str.zfill(5)
    mun = municipios_sellados_v15()
    sel = set(s.cod_distrito[s.cod_municipio.isin(mun)])
    rng = np.random.default_rng(SEED_V15 + 15)
    for cod, g in s[~s.cod_municipio.isin(mun)].groupby("cod_municipio"):
        d = sorted(g.cod_distrito.unique())
        if len(d) >= 5:
            k = max(1, int(round(FRACCION_V15 * len(d))))
            sel |= set(np.array(d)[rng.permutation(len(d))[:k]].tolist())
    return sel


def unidad_sellada_v15(codigo: pd.Series, nivel: str) -> pd.Series:
    """True si la unidad está en el bloque espacial sellado de V15. Provincias y CCAA no se sellan espacialmente (solo
    temporalmente): su validación es la temporal. Las provincias selladas en v6 devuelven True (siguen fuera de uso)."""
    c = codigo.astype(str)
    v6 = set(provincias_selladas_v6())
    if nivel == "municipio":
        return c.str.zfill(5).isin(municipios_sellados_v15()) | c.str.zfill(5).str[:2].isin(v6)
    if nivel in ("distrito", "seccion"):
        return c.str.zfill(7 if nivel == "distrito" else 10).str[:7].isin(distritos_sellados_v15()) | c.str[:2].isin(v6)
    if nivel == "provincia":
        return c.str.zfill(2).isin(v6)
    return pd.Series(False, index=codigo.index)


def _manifiesto_v15() -> dict:
    return json.loads(MANIFIESTO_V15.read_text(encoding="utf-8")) if MANIFIESTO_V15.exists() else {}


def sellar_v15(hechos: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Separa filas de la base (formato largo de data/base/hechos.parquet): escribe la parte sellada en
    data/sealed/v15_<nombre>.parquet (sin devolverla) y devuelve SOLO la de entrenamiento. Sellado = unidad del bloque espacial
    V15, o periodo posterior al último visto de la variable en el manifiesto, o edición posterior a la fecha de corte.
    Sin manifiesto (docs/v15/sellado_v15.json) se niega: el corte se fija antes de sellar."""
    man = _manifiesto_v15()
    if not man:
        raise RuntimeError("Falta docs/v15/sellado_v15.json: fije el corte (fase 3.3) antes de sellar.")
    esp = pd.Series(False, index=hechos.index)
    for nivel, idx in hechos.groupby("nivel").groups.items():
        esp.loc[idx] = unidad_sellada_v15(hechos.loc[idx, "territorio_codigo"], nivel).values
    ultimo = hechos.variable.astype(str) + "|" + hechos.nivel.astype(str) + "|" + hechos.frecuencia.astype(str)
    tope = ultimo.map(man["ultimo_periodo_visto"])
    tem = tope.notna() & (hechos.periodo.astype(str) > tope.astype(str))
    tem |= tope.isna()   # variable o combinación no vista al depositar: entera al sellado
    if "edicion" in hechos:
        tem |= pd.to_datetime(hechos.edicion, errors="coerce") > pd.Timestamp(man["fecha_corte"])
    m = esp | tem
    SEALED.mkdir(parents=True, exist_ok=True)
    hechos[m].to_parquet(SEALED / f"v15_{nombre}.parquet", index=False)
    with open(LOG, "a") as f:
        f.write(json.dumps({"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "sellado",
                            "hipotesis": f"v15:{nombre}", "filas_selladas": int(m.sum()), "filas_entrenamiento": int((~m).sum())},
                           ensure_ascii=False) + "\n")
    return hechos[~m].copy()


def evaluate_v15(hipotesis: str, fn, rama: str, nombres: list[str]):
    """Abre la muestra sellada V15 UNA vez por hipótesis confirmatoria (registrado antes de leer), solo con la puerta abierta
    (etiqueta prereg-v15 publicada en el remoto en 542b4fd;
    src/v15/puerta.py). fn(dict) -> dict."""
    sys.path.insert(0, str(HERE / "src" / "v15"))
    from puerta import abierta
    ok, motivo = abierta(json.loads(PROYECTO.read_text(encoding="utf-8")))
    if not ok:
        raise PermissionError(f"Puerta V15 cerrada: {motivo}")
    clave = f"v15:{hipotesis}"
    if any(a["hipotesis"] == clave and a.get("evento") == "apertura" for a in _accesos()):
        raise PermissionError(f"{clave} ya abrió la muestra sellada V15 (una sola vez).")
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": clave, "rama": rama, "paneles": [f"v15_{n}" for n in nombres]}
    with open(LOG, "a") as f:
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], clave, rama, apertura["paneles"], "APERTURA (antes de leer)")
    res = fn({n: pd.read_parquet(SEALED / f"v15_{n}.parquet") for n in nombres})
    reg = {**apertura, "utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "evaluacion", "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    _log_md(reg["utc"], clave, rama, apertura["paneles"], json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


# ============================================================================== v16
# Validación sellada de V16 (docs/v16/plan.md, fase 4.4; docs/v16/preregistro_v16.md), fijada ANTES de estimar nada de V16:
# - no toca las de v6 ni V15: sus unidades siguen fuera (unidad_sellada_v16 devuelve True para ellas);
# - espacial: el 15 % de las celdas de 0,5° × 0,5° que quedan tras quitar las provincias de v6 y las celdas de V15 (generador
#   independiente: semilla [SEED, 16]); los municipios con 5 distritos o más nunca se sellan enteros: se sella el 15 % de sus
#   distritos que no estén ya sellados por V15;
# - temporal: todo periodo posterior al último visto de cada variable|nivel|frecuencia en docs/v16/sellado_v16.json, y toda
#   edición publicada después de la fecha de corte (la del commit con la etiqueta prereg-v16).
# La puerta de evaluate_v16 es la etiqueta prereg-v16 publicada en el remoto (src/v16/etiquetas.py).
FRACCION_V16 = 0.15
MANIFIESTO_V16 = HERE / "docs" / "v16" / "sellado_v16.json"


def _celda(m: pd.DataFrame) -> pd.Series:
    return np.floor(m.lon / CELDA_V15).astype(int).astype(str) + "_" + np.floor(m.lat / CELDA_V15).astype(int).astype(str)


def celdas_selladas_v16() -> list[str]:
    m = _centroides_municipios()
    m = m[~m.cod_provincia.isin(set(provincias_selladas_v6()))]
    todas = sorted(set(_celda(m).unique()) - set(celdas_selladas_v15()))
    rng = np.random.default_rng([SEED, 16])
    n = int(round(FRACCION_V16 * len(todas)))
    return sorted(np.array(todas)[rng.permutation(len(todas))[:n]].tolist())


def municipios_sellados_v16() -> set[str]:
    m = _centroides_municipios()
    m = m[~m.cod_provincia.isin(set(provincias_selladas_v6()))]
    return set(m.cod_municipio[_celda(m).isin(set(celdas_selladas_v16()))]) - _municipios_grandes()


def distritos_sellados_v16() -> set[str]:
    """15 % de los distritos (7 dígitos) no sellados por V15 de cada municipio grande no sellado, más todos los de municipios sellados V16."""
    s = pd.read_parquet(GEO / "secciones.parquet", columns=["cod_distrito", "cod_municipio"]).astype(str)
    s["cod_distrito"] = s.cod_distrito.str.zfill(7)
    s["cod_municipio"] = s.cod_municipio.str.zfill(5)
    s = s[~s.cod_municipio.str[:2].isin(set(provincias_selladas_v6()))]
    mun = municipios_sellados_v16()
    sel = set(s.cod_distrito[s.cod_municipio.isin(mun)])
    ya = distritos_sellados_v15()
    rng = np.random.default_rng([SEED, 16, 7])
    for cod, g in s[~s.cod_municipio.isin(mun | municipios_sellados_v15())].groupby("cod_municipio"):
        d = sorted(set(g.cod_distrito.unique()) - ya)
        if len(set(g.cod_distrito.unique())) >= 5 and d:
            k = max(1, int(round(FRACCION_V16 * len(d))))
            sel |= set(np.array(d)[rng.permutation(len(d))[:k]].tolist())
    return sel


def ccaa_selladas_v6() -> set[str]:
    """CCAA cuyas provincias están todas en la muestra v6 (docs/v16/decisiones.md K8): su total autonómico duplica la información
    sellada (cinco son uniprovinciales), así que V16 no las usa a escala de CCAA (adenda del pre-registro V16, punto R7)."""
    t = pd.read_parquet(HERE / "data" / "base" / "publica" / "territorios.parquet", columns=["territorio_codigo", "nivel", "cod_ccaa"])
    p = t[t.nivel == "provincia"].astype(str)
    v6 = set(provincias_selladas_v6())
    return {c for c, g in p.groupby("cod_ccaa") if set(g.territorio_codigo) <= v6}


def unidad_sellada_v16(codigo: pd.Series, nivel: str) -> pd.Series:
    """True si la unidad está fuera del entrenamiento de V16: bloque espacial V16, bloque V15 o provincias de v6; a escala de CCAA,
    las 8 CCAA enteras de v6. La nación no se sella espacialmente (su validación es la temporal). Partidos judiciales (PJ-pp-n)
    heredan su provincia."""
    c = codigo.astype(str)
    v6 = set(provincias_selladas_v6())
    if nivel == "ccaa":
        return c.str.zfill(2).isin(ccaa_selladas_v6())
    previo = unidad_sellada_v15(codigo, nivel)
    if nivel == "municipio":
        return previo | c.str.zfill(5).isin(municipios_sellados_v16())
    if nivel in ("distrito", "seccion"):
        return previo | c.str.zfill(7 if nivel == "distrito" else 10).str[:7].isin(distritos_sellados_v16())
    if nivel == "partido_judicial":
        return c.str[3:5].isin(v6)
    return previo


def _manifiesto_v16() -> dict:
    return json.loads(MANIFIESTO_V16.read_text(encoding="utf-8")) if MANIFIESTO_V16.exists() else {}


def sellar_v16(hechos: pd.DataFrame, nombre: str) -> pd.DataFrame:
    """Como sellar_v15, con el manifiesto docs/v16/sellado_v16.json: la parte sellada (espacial V16/V15/v6 o temporal posterior
    al corte) va a data/sealed/v16_<nombre>.parquet sin devolverse; devuelve SOLO el entrenamiento. Sin manifiesto se niega."""
    man = _manifiesto_v16()
    if not man:
        raise RuntimeError("Falta docs/v16/sellado_v16.json: fije el corte (fase 4.4) antes de sellar.")
    esp = pd.Series(False, index=hechos.index)
    for nivel, idx in hechos.groupby("nivel").groups.items():
        esp.loc[idx] = unidad_sellada_v16(hechos.loc[idx, "territorio_codigo"], nivel).values
    if "muestra_sellada_v6" in hechos:
        esp |= hechos.muestra_sellada_v6.fillna(False).astype(bool)
    clave = hechos.variable.astype(str) + "|" + hechos.nivel.astype(str) + "|" + hechos.frecuencia.astype(str)
    tope = clave.map(man["ultimo_periodo_visto"])
    # nunca más allá del corte de V15: para las claves que V15 selló temporalmente manda el mínimo de los dos manifiestos
    tope15 = clave.map(_manifiesto_v15().get("ultimo_periodo_visto", {}))
    ambos = tope.notna() & tope15.notna()
    tope = tope.where(~ambos, pd.Series([min(str(a), str(b)) for a, b in zip(tope, tope15)], index=tope.index))
    tem = (tope.notna() & (hechos.periodo.astype(str) > tope.astype(str))) | tope.isna()
    if "edicion" in hechos:
        corte = min(pd.Timestamp(man["fecha_corte"]), pd.Timestamp(_manifiesto_v15().get("fecha_corte", man["fecha_corte"])))
        tem |= pd.to_datetime(hechos.edicion, errors="coerce") > corte
    m = esp | tem
    SEALED.mkdir(parents=True, exist_ok=True)
    hechos[m].to_parquet(SEALED / f"v16_{nombre}.parquet", index=False)
    with open(LOG, "a") as f:
        f.write(json.dumps({"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "sellado",
                            "hipotesis": f"v16:{nombre}", "filas_selladas": int(m.sum()), "filas_entrenamiento": int((~m).sum())},
                           ensure_ascii=False) + "\n")
    return hechos[~m].copy()


# Variables de V15 por hipótesis (docs/v15/sellado_v15.json, «preguntas»): ninguna apertura de V16 que las contenga antes de que
# su hipótesis de V15 se haya evaluado (adenda del pre-registro V16, punto R6).
HIPOTESIS_V15_POR_PREGUNTA = {"p6_zonas_tensionadas": ["H1", "H2"], "p5_turismo_seccion": ["H3"], "p4_inmigracion": ["H4"],
                              "p9_prediccion": ["H5"]}


def hipotesis_v15_pendientes(variables: set[str]) -> list[str]:
    """Hipótesis de V15 que comparten alguna variable con `variables` y aún no tienen evento «evaluacion» en el registro."""
    man = _manifiesto_v15().get("preguntas", {})
    hechas = {a["hipotesis"] for a in _accesos() if a.get("evento") == "evaluacion"}
    pend = []
    for p, hs in HIPOTESIS_V15_POR_PREGUNTA.items():
        if variables & set(man.get(p, {}).get("variables", [])):
            pend += [h for h in hs if not any(x.startswith(f"v15:{h}") for x in hechas)]
    return sorted(set(pend))


def evaluate_v16(hipotesis: str, fn, rama: str, nombres: list[str]):
    """Abre la muestra sellada V16 UNA vez por pregunta (registrado antes de leer), solo si la etiqueta prereg-v16 está publicada
    en el remoto (src/v16/etiquetas.py) y si ninguna hipótesis de V15 que comparta variables con esos paneles sigue pendiente de
    evaluar. fn(dict) -> dict."""
    vars_ = set()
    for n in nombres:
        vars_ |= set(_manifiesto_v16().get("conjuntos", {}).get(n, {}).get("variables", []))
    pend = hipotesis_v15_pendientes(vars_)
    if pend:
        raise PermissionError(f"V16 no abre {nombres}: comparte variables con {pend} de V15, aún sin evaluar.")
    import importlib.util
    spec = importlib.util.spec_from_file_location("v16_etiquetas", HERE / "src" / "v16" / "etiquetas.py")
    et = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(et)
    ok, motivo = et.prereg_v16_publicada(HERE)
    if not ok:
        raise PermissionError(f"Puerta V16 cerrada: {motivo}")
    clave = f"v16:{hipotesis}"
    if any(a["hipotesis"] == clave and a.get("evento") == "apertura" for a in _accesos()):
        raise PermissionError(f"{clave} ya abrió la muestra sellada V16 (una sola vez).")
    apertura = {"utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "apertura",
                "hipotesis": clave, "rama": rama, "paneles": [f"v16_{n}" for n in nombres]}
    with open(LOG, "a") as f:
        f.write(json.dumps(apertura, ensure_ascii=False) + "\n")
    _log_md(apertura["utc"], clave, rama, apertura["paneles"], "APERTURA (antes de leer)")
    res = fn({n: pd.read_parquet(SEALED / f"v16_{n}.parquet") for n in nombres})
    reg = {**apertura, "utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": "evaluacion", "resultado": res}
    with open(LOG, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False, default=str) + "\n")
    _log_md(reg["utc"], clave, rama, apertura["paneles"], json.dumps(res, ensure_ascii=False, default=str)[:300])
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "bloques_v16":
        mun, dis = municipios_sellados_v16(), distritos_sellados_v16()
        print(json.dumps({"celdas_selladas": len(celdas_selladas_v16()), "municipios_sellados": len(mun),
                          "distritos_sellados": len(dis)}, ensure_ascii=False))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        print(json.dumps(build(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "bloques_v15":
        mun, dis = municipios_sellados_v15(), distritos_sellados_v15()
        print(json.dumps({"celdas_selladas": len(celdas_selladas_v15()), "municipios_sellados": len(mun),
                          "distritos_sellados": len(dis), "municipios_grandes": len(_municipios_grandes())}, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "provincias_v6":
        print(provincias_selladas_v6())
    elif len(sys.argv) > 1 and sys.argv[1] == "provincias":
        print(provincias_selladas())
    else:
        print(__doc__)
