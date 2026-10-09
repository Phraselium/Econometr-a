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

    # Agregado Espana = media de medianas de CCAA ponderada por n de contratos (VC). DERIVADO, no oficial.
    c = ccaa[(ccaa.tipologia == "VC")]
    a = c[(c.variable == "alquiler_m2") & (c.estadistico == "mediana")][["periodo", "codigo", "valor"]]
    n = c[(c.variable == "n_contratos")][["periodo", "codigo", "valor"]].rename(columns={"valor": "n"})
    m = a.merge(n, on=["periodo", "codigo"])
    agg = m.groupby("periodo").apply(lambda g: pd.Series({
        "valor": np.average(g.valor, weights=g.n), "n_ccaa": len(g), "n": g.n.sum()}), include_groups=False).reset_index()
    esp = pd.DataFrame({"fecha": agg.periodo.astype(str) + "-01-01", "periodo": agg.periodo,
                        "serie": "SERPAVI_ESP_VC_alquiler_m2_mediana_pond", "valor": agg.valor, "unidad": "EUR/m2/mes",
                        "fuente": "MIVAU-SERPAVI (AEAT IRPF); agregado propio", "url": XLSX_URL, "origen": "xls",
                        "pagina": "hoja CCAA", "nivel": "ESP", "codigo": "00", "nombre": "Espana (agregado ponderado CCAA)",
                        "tipologia": "VC", "variable": "alquiler_m2", "estadistico": "mediana_ponderada",
                        "n_ccaa": agg.n_ccaa, "n_contratos": agg.n})
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


def _tasa(s):
    return s.sort_index().pct_change() * 100


def validar():
    """Contraste con IPVA INE (Valencia municipio IPVA8471; CV IPVA4932; Total nacional IPVA4962) e IPC alquiler."""
    mun = pd.read_csv(OUT / "serpavi_municipios_46.csv", dtype={"codigo": str})
    ccaa = pd.read_csv(OUT / "serpavi_ccaa.csv", dtype={"codigo": str})
    esp = pd.read_csv(OUT / "serpavi_esp_agregado.csv")
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
         sp(mun, codigo="46250", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ser(ipva_m, "IPVA8471")),
        ("Comunitat Valenciana (mediana VC) vs IPVA INE CV total (IPVA4932)",
         sp(ccaa, codigo="10", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ser(ipva_n, "IPVA4932")),
        ("Espana agregado (mediana VC pond.) vs IPVA INE Total Nacional (IPVA4962)",
         esp.set_index("periodo")["valor"], ser(ipva_n, "IPVA4962")),
        ("Espana agregado (mediana VC pond.) vs IPC alquiler nacional (IPC290887, media anual)",
         esp.set_index("periodo")["valor"], ipc_anual("IPC290887")),
        ("Comunitat Valenciana (mediana VC) vs IPC alquiler CV (IPC296644, media anual)",
         sp(ccaa, codigo="10", tipologia="VC", variable="alquiler_m2", estadistico="mediana"), ipc_anual("IPC296644")),
    ]
    out = []
    for nombre, a, b in pares:
        ta, tb = _tasa(a), _tasa(b)
        j = pd.concat([ta, tb], axis=1, keys=["serpavi", "ref"]).dropna()
        j = j[j.index >= 2012]
        dif = (j.serpavi - j.ref).abs()
        out.append({"tabla": nombre, "validado": "si" if len(j) >= 5 and j.serpavi.corr(j.ref) > 0.5 else "no",
                    "n_anos": len(j), "anos": f"{j.index.min()}-{j.index.max()}",
                    "corr_tasas_anuales": round(j.serpavi.corr(j.ref), 3),
                    "dif_max_pp": round(dif.max(), 2), "ano_dif_max": int(dif.idxmax()),
                    "dif_media_pp": round(dif.mean(), 2),
                    "error_max": round(dif.max(), 2),
                    "metodo": "origen xls (no PDF/OCR): contraste de tasas de variacion anual con serie INE solapada",
                    "paginas_revisadas": "n/a (xls)"})
    pd.DataFrame(out).to_csv(OUT / "serpavi_validacion.csv", index=False)
    print(pd.DataFrame(out).drop(columns=["metodo", "paginas_revisadas"]).to_string())


if __name__ == "__main__":
    main()
