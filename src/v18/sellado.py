"""V18 · Sellado para la fase 4: topes de entrenamiento y filtro territorial (adenda 1.4 y 1.5; docs/v18/sellado_v18.json).

- `tope(variable, nivel, frecuencia)`: último periodo de entrenamiento de V18 según docs/v18/sellado_v18.json (src/v18/f3_sellado.py).
- `filtrar(df, columna_codigo, nivel, columna_periodo, variable, frecuencia)`: devuelve df sin
  1. las unidades selladas en v6 (holdout.excluir_sellados_v6: 8 CCAA, 11 provincias y sus municipios, distritos y secciones);
  2. las unidades de los bloques espaciales de V15 y V16 (municipios, distritos y, por su distrito, secciones; listas del manifiesto);
  3. los periodos posteriores al tope de la variable en ese nivel y frecuencia, y las ediciones posteriores a su edición máxima
     (regla g), si df tiene la columna «edicion»; y las filas marcadas `muestra_sellada_v6`, si existe la columna.
  Error si la variable|nivel|frecuencia no está en sellado_v18.json (una variable nueva se añade a la tabla de f3_sellado.py y se
  regenera el manifiesto, cuyo valor fija la regla), si la combinación está sellada entera (regla d), si su tope está pendiente
  (datos posteriores a la etiqueta) o si los periodos de df no tienen el formato de la frecuencia.

Nunca abre data/sealed ni ejecuta sellar_* o evaluate_*. Los totales municipales de las ciudades con distritos sellados quedan en
entrenamiento (fuga declarada, adenda 1.5): `municipios_con_distritos_sellados()` da la lista para la variante sin ellos.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src"))
import holdout  # noqa: E402

MANIFIESTO = RAIZ / "docs" / "v18" / "sellado_v18.json"
PATRON = {"A": r"^\d{4}$", "T": r"^\d{4}T[1-4]$", "M": r"^\d{4}-\d{2}$", "D": r"^\d{4}-\d{2}-\d{2}$"}
SIN_TERRITORIO = {"nacional", "pais", "zona_euro", "agregado_ue"}
ANCHO = {"municipio": 5, "distrito": 7, "seccion": 10}
_CACHE: dict[str, dict] = {}


def cargar(manifiesto: dict | str | Path | None = None) -> dict:
    """El manifiesto de V18 (por defecto docs/v18/sellado_v18.json); acepta un dict ya cargado (tests)."""
    if isinstance(manifiesto, dict):
        return manifiesto
    ruta = Path(manifiesto) if manifiesto else MANIFIESTO
    clave = str(ruta.resolve())
    if clave not in _CACHE:
        if not ruta.exists():
            raise FileNotFoundError(f"Falta {ruta}: genérelo con python3 src/v18/f3_sellado.py (después de la etiqueta, antes de estimar)")
        _CACHE[clave] = json.loads(ruta.read_text(encoding="utf-8"))
    return _CACHE[clave]


def entrada(variable: str, nivel: str, frecuencia: str, manifiesto: dict | str | Path | None = None) -> dict:
    man = cargar(manifiesto)
    k = f"{variable}|{nivel}|{frecuencia}"
    if k not in man["topes"]:
        raise KeyError(f"{k} no está en sellado_v18.json: añádala a la tabla de src/v18/f3_sellado.py y regenere el manifiesto antes de usarla")
    return man["topes"][k]


def tope(variable: str, nivel: str, frecuencia: str, manifiesto: dict | str | Path | None = None) -> str:
    """Último periodo de entrenamiento (incluido) de variable|nivel|frecuencia."""
    e = entrada(variable, nivel, frecuencia, manifiesto)
    if e.get("sellada_entera"):
        raise PermissionError(f"{variable}|{nivel}|{frecuencia} está sellada entera (regla {e.get('regla')}): no se usa en V18")
    if not e.get("tope"):
        raise PermissionError(f"{variable}|{nivel}|{frecuencia}: tope pendiente ({e.get('fuente_clave', '')})")
    return str(e["tope"])


def _lista(man: dict, nivel: str, bloque: str) -> set[str]:
    return set(man["unidades_excluidas"].get(nivel, {}).get(bloque, {}).get("unidades", []))


def municipios_con_distritos_sellados(manifiesto: dict | str | Path | None = None) -> set[str]:
    return set(cargar(manifiesto)["unidades_excluidas"]["fuga_declarada"]["municipios_con_distritos_sellados"])


def mascara_v15_v16(codigo: pd.Series, nivel: str, manifiesto: dict | str | Path | None = None) -> pd.Series:
    """True si la unidad está en un bloque espacial sellado de V15 o V16 (municipios; distritos; secciones por su distrito)."""
    man = cargar(manifiesto)
    c = codigo.astype(str).str.strip()
    if nivel == "municipio":
        return c.str.zfill(5).isin(_lista(man, "municipio", "v15") | _lista(man, "municipio", "v16"))
    if nivel in ("distrito", "seccion"):
        dist = _lista(man, "distrito", "v15") | _lista(man, "distrito", "v16")
        return c.str.zfill(ANCHO[nivel]).str[:7].isin(dist)
    return pd.Series(False, index=codigo.index)


def _territorio(df: pd.DataFrame, col: str, nivel: str, man: dict) -> pd.DataFrame:
    if nivel in SIN_TERRITORIO:
        return df
    if nivel in ("ccaa", "provincia", "municipio", "distrito", "seccion"):
        out = holdout.excluir_sellados_v6(df, col, nivel)
        return out[~mascara_v15_v16(out[col], nivel, man)] if nivel in ANCHO else out
    if nivel == "partido_judicial":   # PJ-pp-n hereda su provincia (holdout.unidad_sellada_v16)
        v6 = set(man["unidades_excluidas"]["provincia"]["v6"]["unidades"])
        return df[~df[col].astype(str).str[3:5].isin(v6)]
    raise ValueError(f"nivel {nivel!r} sin regla territorial de V18: pase los códigos INE de sección, distrito, municipio o provincia")


def filtrar(df: pd.DataFrame, columna_codigo: str, nivel: str, columna_periodo: str, variable: str, frecuencia: str,
            manifiesto: dict | str | Path | None = None) -> pd.DataFrame:
    """Entrenamiento de V18 para variable|nivel|frecuencia: sin unidades selladas (v6, V15, V16), sin periodos posteriores al tope
    y sin ediciones posteriores a la edición máxima. Devuelve una copia."""
    man = cargar(manifiesto)
    e = entrada(variable, nivel, frecuencia, man)
    t = tope(variable, nivel, frecuencia, man)
    per = df[columna_periodo].astype(str).str.strip()
    malos = per[~per.str.match(PATRON[frecuencia])]
    if len(malos):
        raise ValueError(f"{columna_periodo}: periodos sin formato de frecuencia {frecuencia}: {sorted(malos.unique())[:5]}")
    out = df[per <= t]
    if "muestra_sellada_v6" in out:
        out = out[~out["muestra_sellada_v6"].fillna(False).astype(bool)]
    if "edicion" in out and e.get("edicion_maxima"):
        out = out[~(pd.to_datetime(out["edicion"], errors="coerce") > pd.Timestamp(e["edicion_maxima"]))]
    return _territorio(out, columna_codigo, nivel, man).copy()
