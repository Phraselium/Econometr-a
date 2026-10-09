"""Padrón de València (municipio INE 46250): total y Comunitat Valenciana por nacionalidad.

Fuentes (API JSON wstempus del INE):
- Tabla 2903 (Cifras oficiales de población, op. DPOP, provincia de Valencia por municipios):
  València municipio (no la provincia) total, hombres y mujeres, anual. Series DPOP21796 /
  DPOP21797 / DPOP21798. La serie "Valencia/València" (DPOP21046) es la provincia y se descarta.
- Tabla 29005 (Cifras oficiales del padrón por municipio, op. DPOP): solo para validación
  cruzada del último año de València (DATOS_TABLA nult=1). No se guarda.
- Tabla 56942 (Estadística Continua de Población, op. ECP): Comunitat Valenciana por nacionalidad
  (grupos de países) y sexo, anual. Se seleccionan series por nombre.

Limitaciones (ver docs/fallidas/padron_valencia.md): la API no ofrece población por nacionalidad
a nivel municipal anual, así que el desglose por nacionalidad es solo a nivel Comunitat Valenciana.

Idempotente: si data/raw/ine_padron_valencia.csv existe no se vuelve a bajar (salvo FORCE=1).
Formato largo estándar (utils_fetch.save). Series = código INE; nombre = Nombre del INE.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import cached, get, save  # noqa: E402

BASE = "https://servicios.ine.es/wstempus/js/ES"
NAME = "ine_padron_valencia.csv"
NULT = 300
TOL = 0.5  # personas: tolerancia para identidades exactas (total = hombres + mujeres)
TOL_CV = 5  # personas: la ECP redondea cada celda, sumas de nacionalidades difieren 1-2 personas

# COD -> prefijo de Nombre esperado (se verifica para no confundir series)
MUNI = {
    "DPOP21796": "València. Total.",
    "DPOP21797": "València. Hombres.",
    "DPOP21798": "València. Mujeres.",
}
COD_VAL = "DPOP21796"


def fetch_serie(cod: str) -> dict:
    """Devuelve la serie INE completa (DATOS_SERIE/{cod})."""
    d = get(f"{BASE}/DATOS_SERIE/{cod}", params={"nult": NULT})
    if isinstance(d, list):
        d = d[0]
    if not d.get("Data"):
        raise RuntimeError(f"Serie {cod} sin datos: {str(d)[:200]}")
    return d


def rows_from_serie(s: dict, url: str) -> list[dict]:
    rows = []
    unidad = s["Nombre"].strip().rstrip(".").split(".")[-1].strip()
    for x in s["Data"]:
        # FK_Periodo: 28 = anual; 19-22 = T1-T4 (ECP trimestral, verificado en fetch_ine.py)
        fk, anyo = int(x["FK_Periodo"]), int(x["Anyo"])
        if fk == 28:
            fecha, lab = dt.date(anyo, 1, 1), str(anyo)
        elif fk in (19, 20, 21, 22):
            q = {19: 1, 20: 2, 21: 3, 22: 4}[fk]
            fecha, lab = dt.date(anyo, 3 * q - 2, 1), f"{anyo}T{q}"
        else:
            raise ValueError(f"{s['COD']}: FK_Periodo no reconocido ({fk})")
        rows.append({
            "fecha": fecha.isoformat(), "periodo": lab, "serie": s["COD"],
            "valor": None if x.get("Secreto") else x.get("Valor"), "unidad": unidad,
            "fuente": "INE", "url": url, "nombre": s["Nombre"].strip(),
            "fk_unidad": s.get("FK_Unidad"),
        })
    return rows


def pivot(df: pd.DataFrame) -> pd.DataFrame:
    return df.pivot_table(index="fecha", columns="serie", values="valor", aggfunc="first")


def cv_series_codes() -> dict[str, str]:
    """Códigos de la Comunitat Valenciana en la tabla 56942 (nacionalidad x sexo, todas las edades)."""
    d = get(f"{BASE}/DATOS_TABLA/56942", params={"nult": 1})
    pat = re.compile(r"^Comunitat Valenciana\. Todas las edades\. (.+?)\. (Total|Hombres|Mujeres)\. Población\. Número\.")
    out = {}
    for x in d:
        m = pat.match(x["Nombre"])
        if not m:
            continue
        grupo, sexo = m.group(1), m.group(2)
        # Total de nacionalidades x sexo Total, y el desglose por sexo de Total / Española / Extranjera
        if sexo == "Total" or grupo in ("Total", "Española", "Extranjera"):
            out[x["COD"]] = f"{grupo}|{sexo}"
    return out


def cifras_municipio_ultimo() -> dict[str, float]:
    """Último año de València en 'Cifras oficiales del padrón por municipio' (tabla 29005)."""
    d = get(f"{BASE}/DATOS_TABLA/29005", params={"nult": 1})
    for x in d:
        if x["COD"] == COD_VAL and x["Nombre"].startswith("València. Total."):
            return {str(r["Anyo"]): r["Valor"] for r in x["Data"]}
    raise RuntimeError("Serie de València no encontrada en la tabla 29005")


def validate(df: pd.DataFrame, cv: pd.DataFrame, cifras: dict[str, float]) -> list[str]:
    msgs = []
    p = pivot(df[df.serie.isin(MUNI)])
    tot, h, m = p["DPOP21796"], p["DPOP21797"], p["DPOP21798"]
    d1 = (tot - (h + m)).abs().max()
    msgs.append(f"València: |total - (hombres+mujeres)| máx = {d1:.1f} personas "
                f"({'OK' if d1 <= TOL else 'FALLA'})")

    c = pivot(cv)
    # Total CV = Española + Extranjera (sexo Total)
    tot_cv = c[cv_code(cv, "Total", "Total")]
    esp = c[cv_code(cv, "Española", "Total")]
    ext = c[cv_code(cv, "Extranjera", "Total")]
    d2 = (tot_cv - (esp + ext)).abs().max()
    msgs.append(f"CV: |total - (española+extranjera)| máx = {d2:.1f} personas "
                f"({'OK' if d2 <= TOL_CV else 'FALLA'})")
    # Extranjera = suma de grupos (UE28 sin España + Europa resto + África + Am. Norte + Centro Am. y
    # Caribe + Sudamérica + Asia + Oceanía + Apátridas)
    grupos = ["País de la UE28 sin España", "País de Europa menos UE28", "De Africa",
              "De América del Norte", "De Centro América y Caribe", "De Sudamérica",
              "De Asia", "De Oceanía", "Apátridas"]
    try:
        suma = sum(c[cv_code(cv, g, "Total")] for g in grupos)
        d3 = (ext - suma).abs().max()
        msgs.append(f"CV: |extranjera - suma grupos de países| máx = {d3:.1f} personas "
                    f"({'OK' if d3 <= TOL_CV else 'FALLA: los grupos no suman el total, revisar'})")
    except KeyError as e:
        msgs.append(f"CV: grupo no encontrado para suma ({e})")
    # València total: tabla 2903 vs tabla 29005 (último año publicado)
    comp = {a: (tot.loc[f"{a}-01-01"], v) for a, v in cifras.items() if f"{a}-01-01" in tot.index}
    for a, (x, y) in comp.items():
        msgs.append(f"València total {a}: 2903={x:.0f} vs 29005={y:.0f}, diferencia = {x - y:.0f} "
                    f"({'OK' if abs(x - y) <= TOL else 'FALLA'})")
    return msgs


def cv_code(cv: pd.DataFrame, grupo: str, sexo: str) -> str:
    sub = cv[(cv["nombre"].str.contains(f"Todas las edades. {re.escape(grupo)}. {sexo}. ", regex=True))]
    if sub.empty:
        raise KeyError(f"{grupo}/{sexo}")
    return sub["serie"].iloc[0]


def main() -> None:
    if cached(NAME):
        return
    rows = []
    # 1) València municipio (serie de la tabla 2903)
    for cod, pref in MUNI.items():
        s = fetch_serie(cod)
        assert s["Nombre"].startswith(pref), (cod, s["Nombre"])
        rows += rows_from_serie(s, f"{BASE}/DATOS_SERIE/{cod}")
    # 2) Comunitat Valenciana por nacionalidad (tabla 56942)
    codes = cv_series_codes()
    print(f"[cv] {len(codes)} series de Comunitat Valenciana seleccionadas en 56942")
    for cod in codes:
        s = fetch_serie(cod)
        rows += rows_from_serie(s, f"{BASE}/DATOS_SERIE/{cod}")

    df = pd.DataFrame(rows)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    cv = df[df.serie.isin(codes)].copy()
    for msg in validate(df, cv, cifras_municipio_ultimo()):
        print("[val]", msg)
    print(f"[val] NaN: {int(df['valor'].isna().sum())} de {len(df)} observaciones")
    save(df, NAME, "INE")


if __name__ == "__main__":
    main()
