"""SERPAVI (MIVAU) -> data/raw/pdf/serpavi_*.csv  (origen=xls).

Escalera paso 1 (formato abierto): la BD completa 2011-2024 del Sistema Estatal de Referencia del
Precio del Alquiler de Vivienda (explotacion AEAT/IRPF) se publica como XLSX en cdn.mivau.gob.es
(el enlace sale de la pagina www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi, que el WAF
bloquea desde este entorno; la URL se tomo del repo publico CGTCastello/observatori-habitatge).
La URL cambia con cada publicacion anual: actualizar XLSX_URL.

Salidas (formato largo: fecha, periodo, serie, valor, unidad, fuente, url, origen, pagina + nivel,
codigo, nombre, tipologia, variable, estadistico):
  serpavi_ccaa.csv, serpavi_provincias.csv, serpavi_esp_agregado.csv (derivado, ver nota),
  serpavi_municipios_46.csv (todos los municipios de la provincia de Valencia, CPRO 46),
  serpavi_valencia_distritos.csv, serpavi_valencia_secciones.csv (CUMUN 46250).
Tambien genera serpavi_validacion.csv (contraste con IPVA INE e IPC alquiler).

Agregado Espana (serpavi_esp_agregado.csv), tres series DERIVADAS (no oficiales; una media ponderada de medianas
de CCAA no es una mediana nacional):
  * _composicion_variable: media de medianas CCAA ponderada por contratos de cada anyo, con las CCAA disponibles
    ese anyo. La composicion cambia (Navarra desde 2021, Pais Vasco desde 2024; Gipuzkoa 2022 solo existe a nivel
    provincial), lo que infla el crecimiento de 2024 en ~0,7 pp. Solo para robustez.
  * _composicion_constante (PRINCIPAL): solo las CCAA presentes en los 14 anyos 2011-2024 (17: todas salvo Navarra y
    Pais Vasco; incluye Ceuta y Melilla), con pesos FIJOS = contratos medios 2011-2024 de cada CCAA.
  * _encadenada: indice base 2011=100 (nivel inicial = nivel de la constante en 2011) encadenado con la variacion
    anual t-1 -> t calculada con las CCAA comunes a ambos anyos, ponderadas por los contratos medios de ese par.
    Incorpora Navarra/Pais Vasco cuando ya hay dos anyos consecutivos, sin saltos de composicion.
AVISO de validacion: el contraste con el IPVA del INE NO es independiente, pues ambos proceden de datos tributarios
de la AEAT (IRPF). La validacion externa independiente (encuesta) es el IPC alquiler del INE (IPC290887 nacional,
IPC296644 CV), que se contrasta ademas con la serie de composicion constante.
Idempotente: usa cache de descarga (FORCE=1 para rehacer). No toca data/processed.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils_fetch import FORCE, RAW, download  # noqa: E402

XLSX_URL = ("https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/"
            "2026-03-09_bd_SERPAVI_2011-2024%20-%20DEFINITIVO%20WEB.xlsx")
PAGE_URL = "https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi"
OUT = RAW / "pdf"
XLSX = OUT / "originales" / "serpavi_bd_2011-2024.xlsx"

COL_RE = re.compile(r"^(BI_ALVHEPCO|ALQM2(?:mes)?_LV|ALQTBID12|SLVM2)_(M|25|75|TVC|TVU)(?:_(VC|VU))?_(\d{2})$")
VAR = {"BI_ALVHEPCO": ("n_contratos", "viviendas"), "ALQM2_LV": ("alquiler_m2", "EUR/m2/mes"),
       "ALQM2mes_LV": ("alquiler_m2", "EUR/m2/mes"), "ALQTBID12": ("alquiler_mes", "EUR/mes"),
       "SLVM2": ("superficie", "m2")}
STAT = {"M": "mediana", "25": "p25", "75": "p75"}


def parse_cols(header):
    cols = {}
    for i, h in enumerate(header):
        m = COL_RE.match(str(h).strip())
        if not m:
            continue
        v, s, t, yy = m.groups()
        if v == "BI_ALVHEPCO":
            t, s = {"TVC": "VC", "TVU": "VU"}[s], "recuento"
        else:
            s = STAT[s]
        cols[i] = (2000 + int(yy), t, VAR[v][0], VAR[v][1], s)
    return cols


def to_long(rows, header, id_idx, name_idx, nivel, pagina):
    cols = parse_cols(header)
    recs = []
    for r in rows:
        cod = str(r[id_idx]).strip()
        if nivel in ("CCAA", "PROV"):
            cod = cod.zfill(2)
        nom = str(r[name_idx]).strip() if name_idx is not None else ""
        for i, (y, t, var, uni, st) in cols.items():
            v = r[i]
            if v is None or v == "":
                continue
            try:
                v = float(v)
            except (TypeError, ValueError):
                continue
            recs.append((f"{y}-01-01", y, f"SERPAVI_{nivel}_{cod}_{t}_{var}_{st}", v, uni, "MIVAU-SERPAVI (AEAT IRPF)",
                         XLSX_URL, "xls", pagina, nivel, cod, nom, t, var, st))
    return pd.DataFrame(recs, columns=["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "origen",
                                       "pagina", "nivel", "codigo", "nombre", "tipologia", "variable", "estadistico"])


def read_sheet(wb, name, keep):
    it = wb[name].iter_rows(values_only=True)
    header = next(it)
    rows = [r for r in it if keep(r)]
    return header, rows


def main():
    import openpyxl
    OUT.mkdir(parents=True, exist_ok=True)
    # Caché a nivel de salida: si los CSV extraídos ya existen, no se necesita el XLSX
    # (71 MB, excluido de git) y `make all` corre sin red.
    if (OUT / "serpavi_validacion.csv").exists() and (OUT / "serpavi_ccaa.csv").exists() and not FORCE:
        print("[cache] serpavi_*.csv")
        return
    download(XLSX_URL, XLSX, timeout=900)
    wb = openpyxl.load_workbook(XLSX, read_only=True)

    h, r = read_sheet(wb, "CCAA", lambda r: r[0] is not None)
    ccaa = to_long(r, h, 0, 1, "CCAA", "hoja CCAA")
    ccaa.to_csv(OUT / "serpavi_ccaa.csv", index=False)

    h, r = read_sheet(wb, "Provincias", lambda r: r[0] is not None)
    prov = to_long(r, h, 0, 1, "PROV", "hoja Provincias")
    prov.to_csv(OUT / "serpavi_provincias.csv", index=False)

    esp = agregados_esp(ccaa)
    esp.to_csv(OUT / "serpavi_esp_agregado.csv", index=False)

    h, r = read_sheet(wb, "Municipios", lambda r: str(r[0]).zfill(2) == "46")
    to_long(r, h, 2, 3, "MUN", "hoja Municipios").to_csv(OUT / "serpavi_municipios_46.csv", index=False)

    h, r = read_sheet(wb, "Distritos", lambda r: str(r[2]) == "46250")
    to_long(r, h, 4, 3, "DIST", "hoja Distritos").to_csv(OUT / "serpavi_valencia_distritos.csv", index=False)

    h, r = read_sheet(wb, "Secciones censales", lambda r: str(r[2]) == "46250")
    sec = to_long(r, h, 4, 3, "SEC", "hoja Secciones censales")
    sec = sec[sec.variable != "superficie"]  # reduce tamano; superficie sigue en el XLSX original
    sec.to_csv(OUT / "serpavi_valencia_secciones.csv", index=False)
    wb.close()
    validar()


def agregados_esp(ccaa):
    """Tres agregados DERIVADOS de Espana desde la hoja CCAA (ver docstring del modulo)."""
    c = ccaa[ccaa.tipologia == "VC"]
    a = c[(c.variable == "alquiler_m2") & (c.estadistico == "mediana")].pivot(index="periodo", columns="codigo", values="valor")
    n = c[c.variable == "n_contratos"].pivot(index="periodo", columns="codigo", values="valor").reindex_like(a)
    ok = a.notna() & n.notna()
    a, n = a.where(ok), n.where(ok)
    comunes = list(a.columns[a.notna().all()])           # CCAA presentes todos los anyos (17)
    w_fijo = n[comunes].mean()                            # pesos fijos: contratos medios del periodo
    base = dict(tipologia="VC", variable="alquiler_m2", nivel="ESP", codigo="00", unidad="EUR/m2/mes",
                fuente="MIVAU-SERPAVI (AEAT IRPF); agregado propio", url=XLSX_URL, origen="xls", pagina="hoja CCAA")
    filas = []

    def fila(y, serie, valor, nombre, est, unidad=None, n_ccaa=None, n_contr=None):
        filas.append({**base, "fecha": f"{y}-01-01", "periodo": y, "serie": serie, "valor": valor, "nombre": nombre,
                      "estadistico": est, "n_ccaa": n_ccaa, "n_contratos": n_contr,
                      **({"unidad": unidad} if unidad else {})})

    nom_v = "Espana (agregado ponderado CCAA, composicion variable)"
    nom_c = f"Espana (agregado CCAA, composicion constante {len(comunes)} CCAA, pesos fijos)"
    nom_e = "Espana (indice encadenado CCAA comunes a pares de anyos; base 2011=nivel constante)"
    prev = None
    for y in a.index:
        g = a.loc[y].dropna()
        fila(y, "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_variable",
             np.average(g, weights=n.loc[y, g.index]), nom_v, "mediana_ponderada", n_ccaa=len(g), n_contr=n.loc[y, g.index].sum())
        vc = np.average(a.loc[y, comunes], weights=w_fijo)
        fila(y, "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_composicion_constante", vc, nom_c, "mediana_ponderada_const",
             n_ccaa=len(comunes), n_contr=n.loc[y, comunes].sum())
        if prev is None:
            enc = vc
            fila(y, "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_encadenada", enc, nom_e, "mediana_ponderada_encadenada",
                 n_ccaa=len(comunes), n_contr=n.loc[y, comunes].sum())
        else:
            par = list(a.loc[[prev, y]].dropna(axis=1).columns)
            w = n.loc[[prev, y], par].mean()
            var = np.average(a.loc[y, par], weights=w) / np.average(a.loc[prev, par], weights=w)
            enc *= var
            fila(y, "SERPAVI_ESP_VC_alquiler_m2_mediana_pond_encadenada", enc, nom_e, "mediana_ponderada_encadenada",
                 n_ccaa=len(par), n_contr=n.loc[y, par].sum())
        prev = y
    cols = ["fecha", "periodo", "serie", "valor", "unidad", "fuente", "url", "origen", "pagina", "nivel", "codigo",
            "nombre", "tipologia", "variable", "estadistico", "n_ccaa", "n_contratos"]
    return pd.DataFrame(filas)[cols]


def _tasa(s):
    return s.sort_index().pct_change() * 100


def validar():
    """Contraste con IPVA INE (Valencia municipio IPVA8471; CV IPVA4932; Total nacional IPVA4962) e IPC alquiler."""
    mun = pd.read_csv(OUT / "serpavi_municipios_46.csv", dtype={"codigo": str})
    ccaa = pd.read_csv(OUT / "serpavi_ccaa.csv", dtype={"codigo": str})
    espl = pd.read_csv(OUT / "serpavi_esp_agregado.csv")
    esp_var = espl[espl.serie.str.endswith("composicion_variable")]
    esp_con = espl[espl.serie.str.endswith("composicion_constante")]
    esp_enc = espl[espl.serie.str.endswith("encadenada")]
    ipva_m = pd.read_csv(RAW / "ine_ipva_municipal.csv")
    ipva_n = pd.read_csv(RAW / "ine_ipva_nacional_ccaa.csv")
    ipc = pd.read_csv(RAW / "ine_ipc_alquiler.csv")

    def sp(df, **f):
        d = df
        for k, v in f.items():
            d = d[d[k] == v]
        return d.set_index("periodo")["valor"]

    def ser(df, code):
        d = df[df.serie == code].copy()
        d["periodo"] = d.periodo.astype(str).str[:4].astype(int)
        return d.set_index("periodo")["valor"]

    # IPC alquiler: indice mensual -> media anual
    def ipc_anual(code):
        d = ipc[ipc.serie == code].copy()
        d["y"] = d.periodo.str[:4].astype(int)
        return d.groupby("y")["valor"].mean()

    pares = [
        ("Valencia municipio (mediana VC EUR/m2) vs IPVA INE Valencia municipio (IPVA8471 indice)",
         sp(mun, codigo="46250", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ser(ipva_m, "IPVA8471"),
         "NO independiente (ambos AEAT)"),
        ("Comunitat Valenciana (mediana VC) vs IPVA INE CV total (IPVA4932)",
         sp(ccaa, codigo="10", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ser(ipva_n, "IPVA4932"),
         "NO independiente (ambos AEAT)"),
        ("Espana composicion CONSTANTE vs IPVA INE Total Nacional (IPVA4962)",
         esp_con.set_index("periodo")["valor"], ser(ipva_n, "IPVA4962"), "NO independiente (ambos AEAT)"),
        ("Espana composicion VARIABLE vs IPVA INE Total Nacional (IPVA4962)",
         esp_var.set_index("periodo")["valor"], ser(ipva_n, "IPVA4962"), "NO independiente (ambos AEAT)"),
        ("Espana encadenada vs IPVA INE Total Nacional (IPVA4962)",
         esp_enc.set_index("periodo")["valor"], ser(ipva_n, "IPVA4962"), "NO independiente (ambos AEAT)"),
        ("Espana composicion CONSTANTE vs IPC alquiler nacional (IPC290887, media anual)",
         esp_con.set_index("periodo")["valor"], ipc_anual("IPC290887"), "validacion externa (encuesta IPC)"),
        ("Espana composicion VARIABLE vs IPC alquiler nacional (IPC290887, media anual)",
         esp_var.set_index("periodo")["valor"], ipc_anual("IPC290887"), "validacion externa (encuesta IPC)"),
        ("Espana encadenada vs IPC alquiler nacional (IPC290887, media anual)",
         esp_enc.set_index("periodo")["valor"], ipc_anual("IPC290887"), "validacion externa (encuesta IPC)"),
        ("Comunitat Valenciana (mediana VC) vs IPC alquiler CV (IPC296644, media anual)",
         sp(ccaa, codigo="10", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ipc_anual("IPC296644"),
         "validacion externa (encuesta IPC)"),
    ]
    out = []
    for nombre, a, b, indep in pares:
        ta, tb = _tasa(a), _tasa(b)
        j = pd.concat([ta, tb], axis=1, keys=["serpavi", "ref"]).dropna()
        j = j[j.index >= 2012]
        dif = (j.serpavi - j.ref).abs()
        out.append({"tabla": nombre, "validado": "si" if len(j) >= 5 and j.serpavi.corr(j.ref) > 0.5 else "no",
                    "independencia_fuente": indep,
                    "n_anos": len(j), "anos": f"{j.index.min()}-{j.index.max()}",
                    "corr_tasas_anuales": round(j.serpavi.corr(j.ref), 3),
                    "dif_max_pp": round(dif.max(), 2), "ano_dif_max": int(dif.idxmax()),
                    "dif_media_pp": round(dif.mean(), 2),
                    "error_max": round(dif.max(), 2),
                    "metodo": "origen xls (no PDF/OCR): contraste de tasas de variacion anual con serie INE solapada; IPVA = AEAT/IRPF igual que SERPAVI, no es contraste independiente",
                    "paginas_revisadas": "n/a (xls)"})
    pd.DataFrame(out).to_csv(OUT / "serpavi_validacion.csv", index=False)
    print(pd.DataFrame(out).drop(columns=["metodo", "paginas_revisadas"]).to_string())


if __name__ == "__main__":
    main()
